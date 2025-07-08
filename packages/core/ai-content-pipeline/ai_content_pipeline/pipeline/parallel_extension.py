"""
Parallel execution extension for AI Content Pipeline.

This module provides parallel execution capabilities as an optional extension
that doesn't break existing functionality.
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Optional
from enum import Enum

from .chain import StepType, PipelineStep


class MergeStrategy(Enum):
    """Strategies for merging parallel execution results."""
    COLLECT_ALL = "collect_all"          # Return list of all results
    FIRST_SUCCESS = "first_success"      # Return first successful result
    BEST_QUALITY = "best_quality"        # Return highest quality result


class ParallelExtension:
    """
    Optional parallel execution capabilities for the pipeline.
    
    This extension allows running multiple steps in parallel without
    modifying the core pipeline functionality.
    """
    
    def __init__(self, base_executor):
        """Initialize with reference to the base executor."""
        self.base_executor = base_executor
        self.enabled = self._check_if_enabled()
    
    def _check_if_enabled(self) -> bool:
        """Check if parallel execution is enabled via feature flag."""
        return os.getenv("PIPELINE_PARALLEL_ENABLED", "false").lower() == "true"
    
    def is_parallel_step(self, step_data: Dict[str, Any]) -> bool:
        """Check if a step configuration is for parallel execution."""
        return step_data.get("type") == "parallel_group"
    
    def can_execute_parallel(self, step: PipelineStep) -> bool:
        """Check if we can execute this step in parallel."""
        return (self.enabled and 
                step.step_type == StepType.PARALLEL_GROUP and
                hasattr(step, 'params') and
                'parallel_steps' in step.params)
    
    def execute_parallel_group(
        self,
        step: PipelineStep,
        input_data: Any,
        input_type: str,
        chain_config: Dict[str, Any],
        step_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a parallel group of steps.
        
        Args:
            step: PipelineStep with parallel configuration
            input_data: Input data for all parallel steps
            input_type: Type of input data
            chain_config: Chain configuration
            step_context: Execution context
            
        Returns:
            Dict with execution results
        """
        start_time = time.time()
        
        # Extract parallel configuration
        parallel_config = step.params
        parallel_steps_data = parallel_config.get('parallel_steps', [])
        max_workers = parallel_config.get('max_workers', 3)
        merge_strategy = parallel_config.get('merge_strategy', 'collect_all')
        
        print(f"🔄 Executing {len(parallel_steps_data)} steps in parallel (max_workers={max_workers})")
        
        # Convert step data to PipelineStep objects
        parallel_steps = []
        for step_data in parallel_steps_data:
            parallel_step = PipelineStep.from_dict(step_data)
            parallel_steps.append(parallel_step)
        
        # Execute steps in parallel
        results = []
        total_cost = 0.0
        failed_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            futures = {}
            for i, p_step in enumerate(parallel_steps):
                print(f"  📍 Submitting: {p_step.step_type.value} ({p_step.model})")
                future = executor.submit(
                    self.base_executor._execute_step,
                    step=p_step,
                    input_data=input_data,
                    input_type=input_type,
                    chain_config=chain_config,
                    step_context=step_context.copy()  # Thread-safe copy
                )
                futures[future] = (i, p_step)
            
            # Collect results as they complete
            for future in as_completed(futures):
                step_index, p_step = futures[future]
                try:
                    result = future.result()
                    results.append({
                        'step_index': step_index,
                        'step_type': p_step.step_type.value,
                        'model': p_step.model,
                        'result': result
                    })
                    
                    if result.get("success", False):
                        print(f"  ✅ Completed: {p_step.step_type.value} ({p_step.model})")
                    else:
                        print(f"  ❌ Failed: {p_step.step_type.value} ({p_step.model})")
                        failed_count += 1
                    
                    total_cost += result.get("cost", 0.0)
                    
                except Exception as e:
                    print(f"  ❌ Exception: {p_step.step_type.value} - {str(e)}")
                    results.append({
                        'step_index': step_index,
                        'step_type': p_step.step_type.value,
                        'model': p_step.model,
                        'result': {
                            "success": False,
                            "error": str(e)
                        }
                    })
                    failed_count += 1
        
        # Sort results by step index to maintain order
        results.sort(key=lambda x: x['step_index'])
        
        # Merge results based on strategy
        merged_result = self._merge_results(results, merge_strategy)
        
        total_time = time.time() - start_time
        
        # Add parallel execution metadata
        merged_result.update({
            "parallel_execution": True,
            "total_parallel_steps": len(parallel_steps),
            "successful_steps": len(parallel_steps) - failed_count,
            "failed_steps": failed_count,
            "total_time": total_time,
            "cost": total_cost
        })
        
        print(f"⏱️  Parallel execution completed in {total_time:.2f}s")
        print(f"📊 Results: {len(parallel_steps) - failed_count}/{len(parallel_steps)} successful")
        
        return merged_result
    
    def _merge_results(
        self, 
        results: List[Dict[str, Any]], 
        strategy: str
    ) -> Dict[str, Any]:
        """
        Merge parallel execution results based on strategy.
        
        Args:
            results: List of execution results
            strategy: Merge strategy to use
            
        Returns:
            Merged result dictionary
        """
        successful_results = [r for r in results if r['result'].get('success', False)]
        
        if strategy == "collect_all":
            return {
                "success": len(successful_results) > 0,
                "output_data": "parallel_results",  # Special marker
                "parallel_results": results,
                "successful_results": successful_results,
                "merge_strategy": strategy
            }
        
        elif strategy == "first_success":
            if successful_results:
                first_success = successful_results[0]['result']
                first_success["merge_strategy"] = strategy
                return first_success
            else:
                return {
                    "success": False,
                    "error": "No successful results from parallel execution",
                    "parallel_results": results,
                    "merge_strategy": strategy
                }
        
        elif strategy == "best_quality":
            # For now, implement as first_success
            # TODO: Add quality scoring logic
            return self._merge_results(results, "first_success")
        
        else:
            return {
                "success": False,
                "error": f"Unknown merge strategy: {strategy}",
                "parallel_results": results,
                "merge_strategy": strategy
            }