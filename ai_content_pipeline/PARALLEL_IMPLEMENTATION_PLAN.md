# Parallel Pipeline Execution - Implementation Plan

## Overview
This document outlines the step-by-step implementation plan for adding parallel execution support to the AI Content Pipeline.

## Phase 1: Core Data Structures (Week 1)

### 1.1 Update StepType Enum
**File**: `ai_content_pipeline/pipeline/chain.py`

```python
class StepType(Enum):
    # Existing types...
    PARALLEL_GROUP = "parallel_group"
    MERGE_RESULTS = "merge_results"
    SPLIT_INPUT = "split_input"
    BATCH_PROCESS = "batch_process"
```

### 1.2 Create New Data Classes
**File**: `ai_content_pipeline/pipeline/parallel_types.py` (new file)

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class MergeStrategy(Enum):
    COLLECT_ALL = "collect_all"          # Return list of all results
    FIRST_SUCCESS = "first_success"      # Return first successful result
    BEST_QUALITY = "best_quality"        # Return highest quality result
    COMBINE_OUTPUTS = "combine_outputs"  # Combine outputs (e.g., merge images)

class SplitStrategy(Enum):
    DUPLICATE = "duplicate"              # Same input to all branches
    ROUND_ROBIN = "round_robin"          # Distribute list items
    CUSTOM = "custom"                    # Custom splitting logic

@dataclass
class ParallelGroup:
    """Configuration for parallel execution group."""
    group_id: str
    parallel_steps: List[PipelineStep]
    max_workers: int = 3                 # Limit concurrent executions
    fail_fast: bool = False              # Stop on first failure
    merge_strategy: MergeStrategy = MergeStrategy.COLLECT_ALL
    
@dataclass
class ParallelResult:
    """Result from parallel execution."""
    group_id: str
    results: List[Dict[str, Any]]
    successful_count: int
    failed_count: int
    total_time: float
    total_cost: float
```

### 1.3 Update PipelineStep
**File**: `ai_content_pipeline/pipeline/chain.py`

```python
@dataclass
class PipelineStep:
    # Existing fields...
    parallel_config: Optional[ParallelGroup] = None
    depends_on: Optional[List[str]] = None  # Step dependencies
```

## Phase 2: Chain Validation (Week 1)

### 2.1 Update Chain Validation
**File**: `ai_content_pipeline/pipeline/chain.py`

Add validation methods:
```python
def _validate_parallel_group(self, step: PipelineStep) -> List[str]:
    """Validate parallel group configuration."""
    errors = []
    
    if not step.parallel_config:
        errors.append("Parallel group missing configuration")
        return errors
    
    config = step.parallel_config
    
    # Validate parallel steps
    if not config.parallel_steps:
        errors.append(f"Parallel group {config.group_id} has no steps")
    
    # Validate each parallel step
    for i, p_step in enumerate(config.parallel_steps):
        # Check input/output compatibility
        step_errors = self._validate_step_compatibility(p_step)
        errors.extend([f"Parallel step {i+1}: {e}" for e in step_errors])
    
    # Validate merge strategy
    if config.merge_strategy == MergeStrategy.COMBINE_OUTPUTS:
        # Ensure all outputs are compatible for merging
        output_types = set(self._get_step_output_type(s.step_type) 
                          for s in config.parallel_steps)
        if len(output_types) > 1:
            errors.append(f"Cannot merge different output types: {output_types}")
    
    return errors
```

### 2.2 Update Input/Output Type Mappings
```python
def _get_step_input_type(self, step_type: StepType) -> str:
    input_types = {
        # Existing mappings...
        StepType.PARALLEL_GROUP: "any",      # Accepts any input
        StepType.MERGE_RESULTS: "parallel",  # Accepts parallel results
        StepType.SPLIT_INPUT: "list",        # Accepts list input
    }
    return input_types.get(step_type, "unknown")
```

## Phase 3: Executor Implementation (Week 2)

### 3.1 Create Parallel Executor Module
**File**: `ai_content_pipeline/pipeline/parallel_executor.py` (new file)

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
import time

from .parallel_types import ParallelGroup, ParallelResult, MergeStrategy
from .chain import PipelineStep

class ParallelExecutor:
    """Handles parallel execution of pipeline steps."""
    
    def __init__(self, base_executor):
        self.base_executor = base_executor
        
    def execute_parallel_group(
        self,
        group: ParallelGroup,
        input_data: Any,
        input_type: str,
        chain_config: Dict[str, Any],
        step_context: Dict[str, Any]
    ) -> ParallelResult:
        """Execute a parallel group of steps."""
        start_time = time.time()
        
        if group.max_workers == 1:
            # Fall back to sequential if max_workers is 1
            return self._execute_sequential(group, input_data, input_type, 
                                          chain_config, step_context)
        
        # Use thread pool for parallel execution
        results = []
        failed_count = 0
        total_cost = 0.0
        
        with ThreadPoolExecutor(max_workers=group.max_workers) as executor:
            # Submit all tasks
            futures = {}
            for step in group.parallel_steps:
                future = executor.submit(
                    self.base_executor._execute_step,
                    step=step,
                    input_data=input_data,
                    input_type=input_type,
                    chain_config=chain_config,
                    step_context=step_context.copy()  # Copy context for thread safety
                )
                futures[future] = step
            
            # Collect results
            for future in as_completed(futures):
                step = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    if not result.get("success", False):
                        failed_count += 1
                        if group.fail_fast:
                            # Cancel remaining futures
                            for f in futures:
                                f.cancel()
                            break
                    total_cost += result.get("cost", 0.0)
                except Exception as e:
                    results.append({
                        "success": False,
                        "error": str(e),
                        "step": step.step_type.value
                    })
                    failed_count += 1
        
        total_time = time.time() - start_time
        
        return ParallelResult(
            group_id=group.group_id,
            results=results,
            successful_count=len(results) - failed_count,
            failed_count=failed_count,
            total_time=total_time,
            total_cost=total_cost
        )
    
    def merge_results(
        self,
        parallel_result: ParallelResult,
        merge_strategy: MergeStrategy
    ) -> Dict[str, Any]:
        """Merge results based on strategy."""
        if merge_strategy == MergeStrategy.COLLECT_ALL:
            return {
                "success": parallel_result.failed_count == 0,
                "outputs": [r for r in parallel_result.results if r.get("success")],
                "errors": [r for r in parallel_result.results if not r.get("success")]
            }
        
        elif merge_strategy == MergeStrategy.FIRST_SUCCESS:
            for result in parallel_result.results:
                if result.get("success"):
                    return result
            return {"success": False, "error": "No successful results"}
        
        elif merge_strategy == MergeStrategy.BEST_QUALITY:
            # Implement quality scoring logic
            successful = [r for r in parallel_result.results if r.get("success")]
            if not successful:
                return {"success": False, "error": "No successful results"}
            # For now, return first successful (implement quality scoring later)
            return successful[0]
        
        elif merge_strategy == MergeStrategy.COMBINE_OUTPUTS:
            # Implement output combination logic based on type
            return self._combine_outputs(parallel_result)
        
        return {"success": False, "error": f"Unknown merge strategy: {merge_strategy}"}
```

### 3.2 Update Main Executor
**File**: `ai_content_pipeline/pipeline/executor.py`

```python
from .parallel_executor import ParallelExecutor
from .parallel_types import ParallelGroup

class ChainExecutor:
    def __init__(self, file_manager: FileManager):
        # Existing init...
        self.parallel_executor = ParallelExecutor(self)
    
    def execute(self, chain: ContentCreationChain, input_data: str, **kwargs):
        # Existing code...
        
        for i, step in enumerate(enabled_steps):
            if step.step_type == StepType.PARALLEL_GROUP:
                # Execute parallel group
                parallel_result = self.parallel_executor.execute_parallel_group(
                    group=step.parallel_config,
                    input_data=current_data,
                    input_type=current_type,
                    chain_config=chain.config,
                    step_context=step_context
                )
                
                # Merge results
                step_result = self.parallel_executor.merge_results(
                    parallel_result,
                    step.parallel_config.merge_strategy
                )
                
                # Update tracking
                step_results.extend(parallel_result.results)
                total_cost += parallel_result.total_cost
                
            else:
                # Existing sequential execution
                step_result = self._execute_step(...)
```

## Phase 4: YAML Schema Support (Week 2)

### 4.1 Update YAML Parser
**File**: `ai_content_pipeline/pipeline/chain.py`

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'PipelineStep':
    """Create PipelineStep from dictionary configuration."""
    step_type = StepType(data["type"])
    
    if step_type == StepType.PARALLEL_GROUP:
        # Parse parallel configuration
        parallel_steps = [
            PipelineStep.from_dict(s) 
            for s in data.get("parallel_steps", [])
        ]
        
        parallel_config = ParallelGroup(
            group_id=data.get("group_id", f"group_{id(data)}"),
            parallel_steps=parallel_steps,
            max_workers=data.get("max_workers", 3),
            fail_fast=data.get("fail_fast", False),
            merge_strategy=MergeStrategy(data.get("merge_strategy", "collect_all"))
        )
        
        return cls(
            step_type=step_type,
            model="parallel",  # Dummy model for parallel groups
            params={},
            parallel_config=parallel_config,
            enabled=data.get("enabled", True)
        )
    
    # Existing parsing for regular steps...
```

### 4.2 Example YAML Configurations

**Multi-Voice TTS**:
```yaml
name: "multi_voice_tts_parallel"
description: "Generate speech with multiple voices in parallel"
prompt: "Welcome to our AI platform"

steps:
  - type: "parallel_group"
    group_id: "voice_generation"
    max_workers: 3
    merge_strategy: "collect_all"
    parallel_steps:
      - type: "text_to_speech"
        model: "elevenlabs"
        params:
          voice: "rachel"
          output_file: "voice_rachel.mp3"
      - type: "text_to_speech"
        model: "elevenlabs"
        params:
          voice: "drew"
          output_file: "voice_drew.mp3"
      - type: "text_to_speech"
        model: "elevenlabs"
        params:
          voice: "bella"
          output_file: "voice_bella.mp3"
```

**Multi-Model Image Generation**:
```yaml
name: "multi_model_comparison"
description: "Generate images with different models"

steps:
  - type: "parallel_group"
    group_id: "image_models"
    max_workers: 2
    merge_strategy: "collect_all"
    parallel_steps:
      - type: "text_to_image"
        model: "imagen4"
        params:
          output_file: "imagen_result.png"
      - type: "text_to_image"
        model: "flux"
        params:
          output_file: "flux_result.png"
```

## Phase 5: Testing (Week 3)

### 5.1 Unit Tests
**File**: `ai_content_pipeline/tests/test_parallel_execution.py`

```python
import pytest
from ai_content_pipeline.pipeline.parallel_types import ParallelGroup, MergeStrategy
from ai_content_pipeline.pipeline.parallel_executor import ParallelExecutor

def test_parallel_group_creation():
    """Test creating parallel group configuration."""
    # Test code...

def test_parallel_execution():
    """Test parallel execution of steps."""
    # Test code...

def test_merge_strategies():
    """Test different merge strategies."""
    # Test code...

def test_error_handling():
    """Test error handling in parallel execution."""
    # Test code...
```

### 5.2 Integration Tests
- Test YAML parsing with parallel groups
- Test full pipeline execution with parallel steps
- Test resource limits and concurrency control
- Test progress reporting for parallel execution

## Phase 6: Documentation & Examples (Week 3)

### 6.1 Update Documentation
- Add parallel execution section to README
- Document new YAML schema options
- Add performance considerations
- Include troubleshooting guide

### 6.2 Create Example Workflows
- Multi-voice narration workflow
- A/B testing workflow for models
- Batch processing workflow
- Complex fan-out/fan-in workflow

## Implementation Timeline

**Week 1**:
- Days 1-2: Implement core data structures
- Days 3-4: Update chain validation
- Day 5: Initial testing and debugging

**Week 2**:
- Days 1-3: Implement parallel executor
- Days 4-5: Add YAML support and parsing

**Week 3**:
- Days 1-2: Comprehensive testing
- Days 3-4: Documentation and examples
- Day 5: Performance optimization

## Risk Mitigation

1. **API Rate Limits**: Implement rate limiting and retry logic
2. **Resource Exhaustion**: Set reasonable max_workers limits
3. **Error Aggregation**: Ensure all errors are captured and reported
4. **Thread Safety**: Use thread-safe data structures and context copying
5. **Backwards Compatibility**: Ensure existing pipelines continue to work

## Success Metrics

- Parallel execution achieves 2-3x speedup for independent tasks
- No regression in existing sequential pipeline functionality
- Clear error reporting for parallel execution failures
- Intuitive YAML configuration for parallel workflows