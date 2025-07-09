"""Enhanced parallel executor with thread-based processing for 2-3x speedup."""

import asyncio
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable

from ai_content_platform.core.models import (
    PipelineConfig, 
    StepConfig, 
    ParallelStepConfig,
    PipelineResult,
    StepResult,
    StepType
)
from ai_content_platform.core.executor import PipelineExecutor
from ai_content_platform.core.step import BaseStep, StepFactory
from ai_content_platform.core.exceptions import (
    PipelineExecutionError,
    StepExecutionError
)
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.utils.file_manager import FileManager
from ai_content_platform.utils.cost_calculator import CostCalculator


class ParallelPipelineExecutor(PipelineExecutor):
    """Enhanced executor with parallel processing capabilities."""
    
    def __init__(
        self,
        config: PipelineConfig,
        max_workers: Optional[int] = None,
        enable_parallel: bool = True,
        **kwargs
    ):
        super().__init__(config, **kwargs)
        
        # Parallel execution settings
        self.max_workers = max_workers or min(32, (os.cpu_count() or 1) + 4)
        self.enable_parallel = enable_parallel
        self.thread_pool: Optional[ThreadPoolExecutor] = None
        
        # Performance tracking
        self.parallel_stats = {
            "sequential_time": 0.0,
            "parallel_time": 0.0,
            "speedup_factor": 1.0,
            "threads_used": 0,
            "parallel_groups": 0
        }
        
        self.logger.info(f"Parallel execution {'enabled' if enable_parallel else 'disabled'}")
        if enable_parallel:
            self.logger.info(f"Max workers: {self.max_workers}")
    
    async def execute(self) -> PipelineResult:
        """Execute pipeline with parallel optimization.
        
        Returns:
            Pipeline execution result with performance statistics
        """
        if not self.enable_parallel:
            return await super().execute()
        
        try:
            # Initialize thread pool
            self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
            
            self.logger.step(f"Starting parallel pipeline: {self.config.pipeline_name}")
            self.execution_start_time = time.time()
            self.context["start_time"] = self.execution_start_time
            
            # Pre-execution setup (same as parent)
            await self._setup_pipeline()
            
            # Analyze pipeline for parallel opportunities
            execution_plan = self._analyze_parallel_opportunities()
            
            # Execute with optimized plan
            await self._execute_optimized_plan(execution_plan)
            
            # Calculate performance gains
            self._calculate_performance_stats()
            
            # Create enhanced result with parallel stats
            result = await self._create_enhanced_result()
            
            return result
            
        finally:
            # Cleanup thread pool
            if self.thread_pool:
                self.thread_pool.shutdown(wait=True)
    
    def _analyze_parallel_opportunities(self) -> Dict[str, Any]:
        """Analyze pipeline steps to identify parallel execution opportunities.
        
        Returns:
            Execution plan with parallel groups identified
        """
        execution_plan = {
            "sequential_groups": [],
            "parallel_groups": [],
            "estimated_speedup": 1.0,
            "optimization_applied": False
        }
        
        current_group = []
        
        for i, step in enumerate(self.config.steps):
            if isinstance(step, ParallelStepConfig):
                # Already a parallel step
                if current_group:
                    execution_plan["sequential_groups"].append(current_group)
                    current_group = []
                
                execution_plan["parallel_groups"].append({
                    "type": "explicit_parallel",
                    "steps": step.parallel_steps,
                    "merge_strategy": step.merge_strategy,
                    "index": i
                })
                
            else:
                # Check if this step can be parallelized with previous/next steps
                can_parallelize = self._can_parallelize_step(step, i)
                
                if can_parallelize and current_group:
                    # Add to current parallel group
                    current_group.append((step, i))
                else:
                    # Start new group or add sequential step
                    if current_group and len(current_group) > 1:
                        execution_plan["parallel_groups"].append({
                            "type": "implicit_parallel",
                            "steps": [s[0] for s in current_group],
                            "indices": [s[1] for s in current_group],
                            "merge_strategy": "merge_outputs"
                        })
                        execution_plan["optimization_applied"] = True
                    elif current_group:
                        execution_plan["sequential_groups"].append(current_group)
                    
                    current_group = [(step, i)]
        
        # Handle remaining group
        if current_group:
            if len(current_group) > 1:
                execution_plan["parallel_groups"].append({
                    "type": "implicit_parallel",
                    "steps": [s[0] for s in current_group],
                    "indices": [s[1] for s in current_group],
                    "merge_strategy": "merge_outputs"
                })
                execution_plan["optimization_applied"] = True
            else:
                execution_plan["sequential_groups"].append(current_group)
        
        # Estimate speedup
        parallel_groups = len(execution_plan["parallel_groups"])
        if parallel_groups > 0:
            execution_plan["estimated_speedup"] = min(2.5, 1.0 + (parallel_groups * 0.3))
        
        self.logger.info(
            f"Parallel analysis: {parallel_groups} parallel groups, "
            f"estimated speedup: {execution_plan['estimated_speedup']:.1f}x"
        )
        
        return execution_plan
    
    def _can_parallelize_step(self, step: StepConfig, step_index: int) -> bool:
        """Check if a step can be parallelized with others.
        
        Args:
            step: Step configuration
            step_index: Index of the step
            
        Returns:
            True if step can be parallelized
        """
        # Steps that can typically be parallelized
        parallelizable_types = {
            StepType.TEXT_TO_IMAGE,
            StepType.IMAGE_TO_IMAGE,
            StepType.TEXT_TO_SPEECH,
            StepType.AVATAR_GENERATION
        }
        
        if step.step_type not in parallelizable_types:
            return False
        
        # Check for dependencies (simple heuristic)
        # Steps that don't depend on previous step outputs can be parallelized
        step_params = step.parameters
        
        # Check if step uses outputs from previous steps
        uses_previous_output = any(
            isinstance(value, str) and "${" in value
            for value in step_params.values()
            if isinstance(value, str)
        )
        
        return not uses_previous_output
    
    async def _execute_optimized_plan(self, execution_plan: Dict[str, Any]) -> None:
        """Execute pipeline using optimized parallel plan.
        
        Args:
            execution_plan: Execution plan with parallel opportunities
        """
        # Execute sequential groups
        for group in execution_plan["sequential_groups"]:
            for step_info in group:
                if isinstance(step_info, tuple):
                    step, index = step_info
                    self.context["current_step"] = index + 1
                    result = await self._execute_single_step(step)
                    self.results.append(result)
        
        # Execute parallel groups
        for group in execution_plan["parallel_groups"]:
            self.parallel_stats["parallel_groups"] += 1
            
            if group["type"] == "explicit_parallel":
                # Use existing parallel step logic
                parallel_config = ParallelStepConfig(
                    name=f"parallel_group_{len(self.results)}",
                    parallel_steps=group["steps"],
                    merge_strategy=group["merge_strategy"]
                )
                result = await self._execute_enhanced_parallel_step(parallel_config)
                self.results.append(result)
                
            else:
                # Execute implicit parallel group
                result = await self._execute_implicit_parallel_group(group["steps"])
                self.results.extend(result)
    
    async def _execute_enhanced_parallel_step(
        self, 
        parallel_config: ParallelStepConfig
    ) -> StepResult:
        """Execute parallel step with enhanced thread-based processing.
        
        Args:
            parallel_config: Parallel step configuration
            
        Returns:
            Merged step result
        """
        parallel_start_time = time.time()
        
        try:
            step_count = len(parallel_config.parallel_steps)
            self.logger.step(f"Executing {step_count} steps in enhanced parallel mode")
            
            # Create step instances
            step_instances = []
            for step_config in parallel_config.parallel_steps:
                step = StepFactory.create_step(step_config)
                step_instances.append((step, step_config))
            
            # Execute using thread pool for CPU-intensive operations
            # and async for I/O-intensive operations
            if self._is_io_intensive_group(parallel_config.parallel_steps):
                results = await self._execute_async_parallel(step_instances)
            else:
                results = await self._execute_thread_parallel(step_instances)
            
            # Merge results
            merged_result = self._merge_parallel_results(
                results, 
                parallel_config.merge_strategy
            )
            
            merged_result.execution_time = time.time() - parallel_start_time
            self.parallel_stats["parallel_time"] += merged_result.execution_time
            
            return merged_result
            
        except Exception as e:
            execution_time = time.time() - parallel_start_time
            error_msg = f"Enhanced parallel step execution failed: {str(e)}"
            
            return StepResult(
                step_id=f"enhanced_parallel_{int(time.time())}",
                step_type=StepType.PARALLEL_GROUP,
                success=False,
                error=error_msg,
                execution_time=execution_time,
                cost=0.0
            )
    
    async def _execute_async_parallel(
        self, 
        step_instances: List[tuple]
    ) -> List[StepResult]:
        """Execute steps using async parallelization for I/O intensive tasks.
        
        Args:
            step_instances: List of (step, config) tuples
            
        Returns:
            List of step results
        """
        tasks = []
        for step, config in step_instances:
            task = asyncio.create_task(
                self._execute_step_with_context(step, config)
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = StepResult(
                    step_id=f"async_error_{i}_{int(time.time())}",
                    step_type=step_instances[i][1].step_type,
                    success=False,
                    error=str(result),
                    execution_time=0.0,
                    cost=0.0
                )
                processed_results.append(error_result)
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _execute_thread_parallel(
        self, 
        step_instances: List[tuple]
    ) -> List[StepResult]:
        """Execute steps using thread pool for CPU intensive tasks.
        
        Args:
            step_instances: List of (step, config) tuples
            
        Returns:
            List of step results
        """
        loop = asyncio.get_event_loop()
        
        # Submit tasks to thread pool
        future_to_step = {}
        for step, config in step_instances:
            future = self.thread_pool.submit(
                self._execute_step_sync_wrapper, step, config
            )
            future_to_step[future] = (step, config)
        
        self.parallel_stats["threads_used"] = len(future_to_step)
        
        # Collect results as they complete
        results = []
        for future in as_completed(future_to_step):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                step, config = future_to_step[future]
                error_result = StepResult(
                    step_id=f"thread_error_{int(time.time())}",
                    step_type=config.step_type,
                    success=False,
                    error=str(e),
                    execution_time=0.0,
                    cost=0.0
                )
                results.append(error_result)
        
        return results
    
    def _execute_step_sync_wrapper(self, step: BaseStep, config: StepConfig) -> StepResult:
        """Synchronous wrapper for step execution in thread pool.
        
        Args:
            step: Step instance
            config: Step configuration
            
        Returns:
            Step result
        """
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            return loop.run_until_complete(
                self._execute_step_with_context(step, config)
            )
        finally:
            loop.close()
    
    async def _execute_step_with_context(
        self, 
        step: BaseStep, 
        config: StepConfig
    ) -> StepResult:
        """Execute step with proper context and error handling.
        
        Args:
            step: Step instance
            config: Step configuration
            
        Returns:
            Step result
        """
        step_start_time = time.time()
        
        try:
            # Validate step
            if not step.validate_config():
                raise StepExecutionError("Step configuration validation failed")
            
            # Execute step
            result = await step.execute(self.context.copy())
            
            # Update timing and cost
            result.execution_time = time.time() - step_start_time
            
            # Estimate cost
            cost_estimate = self.cost_calculator.estimate_step_cost(config)
            result.cost = cost_estimate.estimated_cost
            
            return result
            
        except Exception as e:
            execution_time = time.time() - step_start_time
            return StepResult(
                step_id=step.step_id,
                step_type=config.step_type,
                success=False,
                error=str(e),
                execution_time=execution_time,
                cost=0.0
            )
    
    def _is_io_intensive_group(self, steps: List[StepConfig]) -> bool:
        """Check if step group is I/O intensive.
        
        Args:
            steps: List of step configurations
            
        Returns:
            True if group is I/O intensive
        """
        io_intensive_types = {
            StepType.TEXT_TO_VIDEO,
            StepType.VIDEO_GENERATION,
            StepType.VIDEO_TO_VIDEO
        }
        
        return any(step.step_type in io_intensive_types for step in steps)
    
    async def _execute_implicit_parallel_group(
        self, 
        steps: List[StepConfig]
    ) -> List[StepResult]:
        """Execute implicitly identified parallel group.
        
        Args:
            steps: List of step configurations
            
        Returns:
            List of step results
        """
        # Create parallel config
        parallel_config = ParallelStepConfig(
            name=f"implicit_parallel_{len(self.results)}",
            parallel_steps=steps,
            merge_strategy="merge_outputs"
        )
        
        # Execute as enhanced parallel step
        merged_result = await self._execute_enhanced_parallel_step(parallel_config)
        
        # Return individual results for each step
        individual_results = []
        for i, step in enumerate(steps):
            individual_result = StepResult(
                step_id=f"implicit_{step.name}_{int(time.time())}",
                step_type=step.step_type,
                success=merged_result.success,
                output_path=merged_result.output_path,
                metadata=merged_result.metadata,
                execution_time=merged_result.execution_time / len(steps),
                cost=merged_result.cost / len(steps)
            )
            individual_results.append(individual_result)
        
        return individual_results
    
    def _calculate_performance_stats(self) -> None:
        """Calculate performance statistics for parallel execution."""
        total_time = time.time() - self.execution_start_time
        
        # Estimate sequential time (rough approximation)
        estimated_sequential_time = sum(r.execution_time for r in self.results)
        
        # Calculate speedup
        if estimated_sequential_time > 0:
            self.parallel_stats["speedup_factor"] = estimated_sequential_time / total_time
        
        self.parallel_stats["sequential_time"] = estimated_sequential_time
        self.parallel_stats["parallel_time"] = total_time
        
        self.logger.info(
            f"Performance: {self.parallel_stats['speedup_factor']:.1f}x speedup "
            f"({estimated_sequential_time:.1f}s → {total_time:.1f}s)"
        )
    
    async def _create_enhanced_result(self) -> PipelineResult:
        """Create pipeline result with enhanced parallel statistics.
        
        Returns:
            Enhanced pipeline result
        """
        # Get base result
        result = await super()._create_base_result()
        
        # Add parallel statistics
        result.metadata.update({
            "parallel_execution": {
                "enabled": self.enable_parallel,
                "max_workers": self.max_workers,
                "threads_used": self.parallel_stats["threads_used"],
                "parallel_groups": self.parallel_stats["parallel_groups"],
                "speedup_factor": self.parallel_stats["speedup_factor"],
                "sequential_time": self.parallel_stats["sequential_time"],
                "parallel_time": self.parallel_stats["parallel_time"]
            }
        })
        
        return result
    
    async def _setup_pipeline(self) -> None:
        """Setup pipeline for execution."""
        # Validate configuration
        self.validator.validate_pipeline_config(self.config)
        
        # Estimate costs
        cost_summary = self.cost_calculator.estimate_pipeline_cost(
            self._flatten_steps(self.config.steps)
        )
        
        # Check cost limits
        max_cost = self.config.global_config.get("max_cost")
        if max_cost:
            self.cost_calculator.check_cost_limit(
                cost_summary.total_estimated_cost, 
                max_cost
            )
        
        self.logger.cost(cost_summary.total_estimated_cost)
        
        # Setup output directory
        output_dir = Path(self.config.output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)
        self.context["output_directory"] = output_dir


