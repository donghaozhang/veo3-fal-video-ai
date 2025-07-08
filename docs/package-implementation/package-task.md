# AI Content Generation Platform - Python Package Creation Guide

## 📋 Overview

This document provides a comprehensive step-by-step guide to convert the AI Content Generation Platform codebase into a professional Python package that can be distributed via PyPI.

## 🎯 Project Summary

**Current Structure**: Multi-module repository with 9 specialized AI content generation implementations
**Target**: Single unified Python package `ai-content-platform` with modular sub-packages
**Key Features**: 
- Unified AI Content Pipeline (flagship)
- Multiple AI service integrations (FAL AI, Google Veo, ElevenLabs, OpenRouter)
- Parallel execution capabilities
- Cost-conscious design with comprehensive testing

## 📦 Package Architecture Design

### Main Package Structure
```
ai-content-platform/
├── setup.py                     # Main package setup
├── setup.cfg                    # Package configuration
├── pyproject.toml               # Modern Python packaging
├── MANIFEST.in                  # Include additional files
├── README.md                    # Package overview
├── LICENSE                      # License file
├── requirements/                # Dependency management
│   ├── base.txt                # Core dependencies
│   ├── google.txt              # Google Veo dependencies
│   ├── fal.txt                 # FAL AI dependencies
│   ├── tts.txt                 # Text-to-speech dependencies
│   ├── video.txt               # Video processing dependencies
│   └── dev.txt                 # Development dependencies
├── ai_content_platform/         # Main package directory
│   ├── __init__.py             # Package initialization
│   ├── __version__.py          # Version management
│   ├── core/                   # Core pipeline functionality
│   ├── services/               # AI service implementations
│   ├── utils/                  # Shared utilities
│   ├── config/                 # Configuration management
│   └── cli/                    # Command-line interfaces
├── tests/                      # Comprehensive test suite
├── docs/                       # Documentation
├── examples/                   # Usage examples
└── scripts/                    # Build and deployment scripts
```

## 🚀 Phase 1: Project Setup and Core Structure

### Step 1.1: Create Root Package Structure

First, let's create the main package directory structure:

```bash
# Create new package directory
mkdir ai-content-platform
cd ai-content-platform

# Create main package structure
mkdir -p ai_content_platform/{core,services,utils,config,cli}
mkdir -p {tests,docs,examples,scripts,requirements}

# Create essential files
touch setup.py setup.cfg pyproject.toml MANIFEST.in
touch ai_content_platform/__init__.py
touch ai_content_platform/__version__.py
touch README.md LICENSE
```

### Step 1.2: Version Management Setup

Create `ai_content_platform/__version__.py`:
```python
"""Version information for AI Content Platform."""

__version__ = "1.0.0"
__author__ = "AI Content Platform Team"
__email__ = "contact@aicontentplatform.com"
__description__ = "Comprehensive AI content generation platform with unified pipeline"
__url__ = "https://github.com/username/ai-content-platform"
```

### Step 1.3: Main Package Initialization

Create `ai_content_platform/__init__.py`:
```python
"""
AI Content Platform - Unified AI Content Generation

A comprehensive platform for generating content using multiple AI services
with parallel execution capabilities and cost-conscious design.
"""

from ai_content_platform.__version__ import __version__
from ai_content_platform.core.pipeline import Pipeline
from ai_content_platform.core.executor import PipelineExecutor

# Main public API
__all__ = [
    "__version__",
    "Pipeline",
    "PipelineExecutor",
]

# Package metadata
__author__ = "AI Content Platform Team"
__email__ = "contact@aicontentplatform.com"
```

### Step 1.4: Requirements Management

Create `requirements/base.txt` (core dependencies):
```txt
# Core dependencies
pyyaml>=6.0
requests>=2.28.0
python-dotenv>=0.19.0
typing-extensions>=4.0.0
pydantic>=1.10.0
click>=8.0.0
rich>=12.0.0
tqdm>=4.64.0
```

Create `requirements/fal.txt` (FAL AI dependencies):
```txt
fal-client>=0.2.0
pillow>=9.0.0
```

Create `requirements/google.txt` (Google services):
```txt
google-generativeai>=0.3.0
google-cloud-storage>=2.7.0
google-auth>=2.16.0
```

Create `requirements/tts.txt` (Text-to-speech):
```txt
elevenlabs>=0.2.0
openai>=1.0.0  # For OpenRouter compatibility
```

Create `requirements/video.txt` (Video processing):
```txt
ffmpeg-python>=0.2.0
opencv-python>=4.7.0
```

Create `requirements/dev.txt` (Development):
```txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
black>=22.0.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.0.0
sphinx>=6.0.0
sphinx-rtd-theme>=1.2.0
twine>=4.0.0
build>=0.10.0
```

---

## 🔧 Phase 2: Core Pipeline Implementation

### Step 2.1: Core Pipeline Module Structure

Create the core pipeline structure in `ai_content_platform/core/`:

```bash
# Core pipeline files
touch ai_content_platform/core/__init__.py
touch ai_content_platform/core/pipeline.py
touch ai_content_platform/core/executor.py
touch ai_content_platform/core/parallel_executor.py
touch ai_content_platform/core/step.py
touch ai_content_platform/core/models.py
touch ai_content_platform/core/exceptions.py
```

### Step 2.2: Core Models and Types

Create `ai_content_platform/core/models.py`:
```python
"""Core data models for the AI Content Platform."""

from enum import Enum
from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field


class StepType(str, Enum):
    """Available step types in the pipeline."""
    TEXT_TO_SPEECH = "text_to_speech"
    TEXT_TO_IMAGE = "text_to_image"
    IMAGE_TO_IMAGE = "image_to_image"
    TEXT_TO_VIDEO = "text_to_video"
    VIDEO_TO_VIDEO = "video_to_video"
    AVATAR_GENERATION = "avatar_generation"
    PARALLEL_GROUP = "parallel_group"
    IMAGE_UNDERSTANDING = "image_understanding"
    PROMPT_GENERATION = "prompt_generation"


class MergeStrategy(str, Enum):
    """Merge strategies for parallel execution."""
    COLLECT_ALL = "collect_all"
    FIRST_SUCCESS = "first_success"
    BEST_QUALITY = "best_quality"


class StepConfig(BaseModel):
    """Configuration for a single pipeline step."""
    step_type: StepType
    config: Dict[str, Any] = Field(default_factory=dict)
    output_filename: Optional[str] = None
    enabled: bool = True
    timeout: Optional[int] = None
    retry_count: int = 0


class ParallelConfig(BaseModel):
    """Configuration for parallel execution."""
    merge_strategy: MergeStrategy = MergeStrategy.COLLECT_ALL
    max_workers: Optional[int] = None
    timeout: Optional[int] = None


class ParallelStepConfig(BaseModel):
    """Configuration for parallel step group."""
    step_type: StepType = StepType.PARALLEL_GROUP
    parallel_config: ParallelConfig
    steps: List[StepConfig]
    output_directory: Optional[str] = None


class PipelineConfig(BaseModel):
    """Main pipeline configuration."""
    pipeline_name: str
    description: Optional[str] = None
    output_directory: str = "output"
    steps: List[Union[StepConfig, ParallelStepConfig]]
    global_config: Dict[str, Any] = Field(default_factory=dict)


class StepResult(BaseModel):
    """Result of a pipeline step execution."""
    step_id: str
    step_type: StepType
    success: bool
    output_path: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    execution_time: float = 0.0
    cost: Optional[float] = None


class PipelineResult(BaseModel):
    """Result of pipeline execution."""
    pipeline_name: str
    success: bool
    total_steps: int
    successful_steps: int
    failed_steps: int
    total_execution_time: float
    total_cost: float = 0.0
    step_results: List[StepResult]
    output_directory: str
```

### Step 2.3: Custom Exceptions

Create `ai_content_platform/core/exceptions.py`:
```python
"""Custom exceptions for AI Content Platform."""


class AIPlatformError(Exception):
    """Base exception for AI Content Platform."""
    pass


class PipelineConfigurationError(AIPlatformError):
    """Raised when pipeline configuration is invalid."""
    pass


class StepExecutionError(AIPlatformError):
    """Raised when a pipeline step fails to execute."""
    pass


class ServiceNotAvailableError(AIPlatformError):
    """Raised when a required AI service is not available."""
    pass


class APIKeyError(AIPlatformError):
    """Raised when API key is missing or invalid."""
    pass


class CostLimitExceededError(AIPlatformError):
    """Raised when estimated cost exceeds user-defined limits."""
    pass


class ParallelExecutionError(AIPlatformError):
    """Raised when parallel execution fails."""
    pass


class ValidationError(AIPlatformError):
    """Raised when input validation fails."""
    pass
```

### Step 2.4: Step Implementation

Create `ai_content_platform/core/step.py`:
```python
"""Pipeline step implementation."""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ai_content_platform.core.models import StepConfig, StepResult, StepType
from ai_content_platform.core.exceptions import StepExecutionError


class BaseStep(ABC):
    """Base class for all pipeline steps."""
    
    def __init__(self, config: StepConfig):
        self.config = config
        self.step_id = f"{config.step_type.value}_{int(time.time())}"
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute the step and return result."""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate step configuration."""
        pass
    
    @abstractmethod
    def estimate_cost(self) -> float:
        """Estimate cost for this step execution."""
        pass
    
    def _create_result(
        self, 
        success: bool, 
        output_path: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        execution_time: float = 0.0,
        cost: float = 0.0
    ) -> StepResult:
        """Helper to create step result."""
        return StepResult(
            step_id=self.step_id,
            step_type=self.config.step_type,
            success=success,
            output_path=output_path,
            metadata=metadata or {},
            error=error,
            execution_time=execution_time,
            cost=cost
        )


class StepFactory:
    """Factory for creating pipeline steps."""
    
    _step_registry: Dict[StepType, type] = {}
    
    @classmethod
    def register_step(cls, step_type: StepType, step_class: type):
        """Register a step class for a step type."""
        cls._step_registry[step_type] = step_class
    
    @classmethod
    def create_step(cls, config: StepConfig) -> BaseStep:
        """Create a step instance from configuration."""
        step_class = cls._step_registry.get(config.step_type)
        if not step_class:
            raise StepExecutionError(f"Unknown step type: {config.step_type}")
        
        return step_class(config)
    
    @classmethod
    def get_available_steps(cls) -> List[StepType]:
        """Get list of available step types."""
        return list(cls._step_registry.keys())
```

### Step 2.5: Pipeline Executor

Create `ai_content_platform/core/executor.py`:
```python
"""Pipeline executor implementation."""

import asyncio
import os
import time
from typing import Dict, List, Any, Optional

from ai_content_platform.core.models import (
    PipelineConfig, PipelineResult, StepResult, StepType, ParallelStepConfig
)
from ai_content_platform.core.step import StepFactory, BaseStep
from ai_content_platform.core.exceptions import (
    PipelineConfigurationError, StepExecutionError
)
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.utils.file_manager import ensure_directory


logger = get_logger(__name__)


class PipelineExecutor:
    """Main pipeline executor."""
    
    def __init__(self, config: PipelineConfig, parallel_enabled: bool = False):
        self.config = config
        self.parallel_enabled = parallel_enabled
        self.context: Dict[str, Any] = {}
        
    async def execute(self) -> PipelineResult:
        """Execute the complete pipeline."""
        logger.info(f"Starting pipeline execution: {self.config.pipeline_name}")
        start_time = time.time()
        
        # Ensure output directory exists
        ensure_directory(self.config.output_directory)
        
        # Initialize context with global config
        self.context.update(self.config.global_config)
        self.context["output_directory"] = self.config.output_directory
        
        step_results: List[StepResult] = []
        total_cost = 0.0
        
        try:
            for step_config in self.config.steps:
                if isinstance(step_config, ParallelStepConfig):
                    if self.parallel_enabled:
                        results = await self._execute_parallel_group(step_config)
                        step_results.extend(results)
                    else:
                        # Fall back to sequential execution
                        results = await self._execute_sequential_group(step_config)
                        step_results.extend(results)
                else:
                    result = await self._execute_step(step_config)
                    step_results.append(result)
                
                # Accumulate costs
                for result in step_results[-1:] if not isinstance(step_config, ParallelStepConfig) else step_results[-len(step_config.steps):]:
                    if result.cost:
                        total_cost += result.cost
            
            execution_time = time.time() - start_time
            successful_steps = sum(1 for r in step_results if r.success)
            
            return PipelineResult(
                pipeline_name=self.config.pipeline_name,
                success=successful_steps == len(step_results),
                total_steps=len(step_results),
                successful_steps=successful_steps,
                failed_steps=len(step_results) - successful_steps,
                total_execution_time=execution_time,
                total_cost=total_cost,
                step_results=step_results,
                output_directory=self.config.output_directory
            )
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            execution_time = time.time() - start_time
            
            return PipelineResult(
                pipeline_name=self.config.pipeline_name,
                success=False,
                total_steps=len(step_results),
                successful_steps=sum(1 for r in step_results if r.success),
                failed_steps=len(step_results) - sum(1 for r in step_results if r.success),
                total_execution_time=execution_time,
                total_cost=total_cost,
                step_results=step_results,
                output_directory=self.config.output_directory
            )
    
    async def _execute_step(self, step_config) -> StepResult:
        """Execute a single step."""
        logger.info(f"Executing step: {step_config.step_type}")
        
        try:
            step = StepFactory.create_step(step_config)
            
            # Validate configuration
            if not step.validate_config():
                raise StepExecutionError(f"Invalid configuration for step: {step_config.step_type}")
            
            # Execute step
            result = await step.execute(self.context)
            
            # Update context with result
            if result.output_path:
                self.context[f"last_{step_config.step_type.value}_output"] = result.output_path
            
            return result
            
        except Exception as e:
            logger.error(f"Step execution failed: {e}")
            return StepResult(
                step_id=f"{step_config.step_type.value}_failed",
                step_type=step_config.step_type,
                success=False,
                error=str(e)
            )
    
    async def _execute_parallel_group(self, parallel_config: ParallelStepConfig) -> List[StepResult]:
        """Execute steps in parallel."""
        logger.info(f"Executing parallel group with {len(parallel_config.steps)} steps")
        
        # Import here to avoid circular imports
        from ai_content_platform.core.parallel_executor import ParallelExecutor
        
        parallel_executor = ParallelExecutor(parallel_config)
        return await parallel_executor.execute(self.context)
    
    async def _execute_sequential_group(self, parallel_config: ParallelStepConfig) -> List[StepResult]:
        """Execute parallel group sequentially (fallback)."""
        logger.warning("Parallel execution disabled, falling back to sequential")
        
        results = []
        for step_config in parallel_config.steps:
            result = await self._execute_step(step_config)
            results.append(result)
        
        return results
```

---

**Part 2 Complete** - This covers the core pipeline implementation including:

1. **Core Models** - Data structures for pipeline configuration and results
2. **Custom Exceptions** - Specific exception types for error handling
3. **Step Implementation** - Base step class and factory pattern
4. **Pipeline Executor** - Main execution engine with parallel support

Would you like me to continue with **Part 3**, which will cover:
- Service integrations (FAL AI, Google Veo, ElevenLabs)
- Parallel executor implementation
- Configuration management
- Utility modules