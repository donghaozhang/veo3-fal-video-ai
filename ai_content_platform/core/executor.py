"""Main pipeline executor implementation."""

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ai_content_platform.core.models import (
    PipelineConfig, 
    StepConfig, 
    ParallelStepConfig,
    PipelineResult,
    StepResult,
    StepType
)
from ai_content_platform.core.step import BaseStep, StepFactory
from ai_content_platform.core.exceptions import (
    PipelineExecutionError,
    StepExecutionError,
    ConfigurationError
)
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.utils.file_manager import FileManager
from ai_content_platform.utils.cost_calculator import CostCalculator
from ai_content_platform.utils.validators import ConfigValidator


class PipelineExecutor:
    """Main pipeline executor for sequential and parallel execution."""
    
    def __init__(
        self,
        config: PipelineConfig,
        file_manager: Optional[FileManager] = None,
        cost_calculator: Optional[CostCalculator] = None,
        validator: Optional[ConfigValidator] = None
    ):
        self.config = config
        self.logger = get_logger(__name__)
        self.file_manager = file_manager or FileManager()
        self.cost_calculator = cost_calculator or CostCalculator()
        self.validator = validator or ConfigValidator()
        
        # Execution context shared across steps
        self.context: Dict[str, Any] = {
            "pipeline_name": config.pipeline_name,
            "output_directory": Path(config.output_directory),
            "global_config": config.global_config,
            "step_outputs": {},
            "start_time": None,
            "current_step": 0
        }
        
        # Track execution state
        self.results: List[StepResult] = []
        self.total_cost: float = 0.0
        self.execution_start_time: Optional[float] = None
    
    async def execute(self) -> PipelineResult:
        """Execute the complete pipeline.
        
        Returns:
            Pipeline execution result
            
        Raises:
            PipelineExecutionError: If pipeline execution fails
        """
        try:
            self.logger.step(f"Starting pipeline: {self.config.pipeline_name}")
            self.execution_start_time = time.time()
            self.context["start_time"] = self.execution_start_time
            
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
            
            # Execute steps
            for i, step_config in enumerate(self.config.steps):
                self.context["current_step"] = i + 1
                
                if isinstance(step_config, ParallelStepConfig):
                    result = await self._execute_parallel_step(step_config)
                else:
                    result = await self._execute_single_step(step_config)
                
                self.results.append(result)
                
                # Check if step failed and should stop pipeline
                if not result.success:
                    if step_config.required:
                        raise PipelineExecutionError(
                            f"Required step '{step_config.name}' failed: {result.error}"
                        )
                    else:
                        self.logger.warning(
                            f"Optional step '{step_config.name}' failed: {result.error}"
                        )
            
            # Calculate total execution time
            execution_time = time.time() - self.execution_start_time
            
            # Create pipeline result
            pipeline_result = PipelineResult(
                pipeline_name=self.config.pipeline_name,
                success=all(r.success or not self._is_step_required(i) 
                          for i, r in enumerate(self.results)),
                step_results=self.results,
                total_cost=self.total_cost,
                execution_time=execution_time,
                output_directory=str(output_dir),
                metadata={
                    "steps_executed": len(self.results),
                    "successful_steps": sum(1 for r in self.results if r.success),
                    "failed_steps": sum(1 for r in self.results if not r.success),
                    "cost_summary": cost_summary.dict() if cost_summary else None
                }
            )
            
            self.logger.success(
                f"Pipeline '{self.config.pipeline_name}' completed in "
                f"{execution_time:.2f}s with total cost ${self.total_cost:.4f}"
            )
            
            return pipeline_result
            
        except Exception as e:
            error_msg = f"Pipeline execution failed: {str(e)}"
            self.logger.error(error_msg)
            
            # Create failed pipeline result
            execution_time = (time.time() - self.execution_start_time 
                            if self.execution_start_time else 0.0)
            
            return PipelineResult(
                pipeline_name=self.config.pipeline_name,
                success=False,
                step_results=self.results,
                total_cost=self.total_cost,
                execution_time=execution_time,
                output_directory=self.config.output_directory,
                error=error_msg,
                metadata={
                    "steps_executed": len(self.results),
                    "error_step": self.context.get("current_step", 0)
                }
            )
    
    async def _execute_single_step(self, step_config: StepConfig) -> StepResult:
        """Execute a single step.
        
        Args:
            step_config: Step configuration
            
        Returns:
            Step execution result
        """
        step_start_time = time.time()
        
        try:
            self.logger.step(f"Executing step: {step_config.name}")
            
            # Create step instance
            step = StepFactory.create_step(step_config)
            
            # Validate step configuration
            if not step.validate_config():
                raise StepExecutionError(f"Step configuration validation failed")
            
            # Estimate step cost
            cost_estimate = self.cost_calculator.estimate_step_cost(step_config)
            
            # Execute step
            result = await step.execute(self.context)
            
            # Update execution time and cost
            result.execution_time = time.time() - step_start_time
            result.cost = cost_estimate.estimated_cost
            self.total_cost += result.cost
            
            # Store step output in context
            if result.success and result.output_path:
                self.context["step_outputs"][step_config.name] = result.output_path
            
            # Track actual cost
            self.cost_calculator.track_actual_cost(step_config.name, result.cost)
            
            if result.success:
                self.logger.success(
                    f"Step '{step_config.name}' completed in "
                    f"{result.execution_time:.2f}s (${result.cost:.4f})"
                )
            else:
                self.logger.error(f"Step '{step_config.name}' failed: {result.error}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - step_start_time
            error_msg = f"Step execution failed: {str(e)}"
            
            return StepResult(
                step_id=f"{step_config.step_type.value}_{int(time.time())}",
                step_type=step_config.step_type,
                success=False,
                error=error_msg,
                execution_time=execution_time,
                cost=0.0
            )
    
    async def _execute_parallel_step(self, parallel_config: ParallelStepConfig) -> StepResult:
        """Execute parallel steps.
        
        Args:
            parallel_config: Parallel step configuration
            
        Returns:
            Merged step result
        """
        parallel_start_time = time.time()
        
        try:
            self.logger.step(
                f"Executing {len(parallel_config.parallel_steps)} steps in parallel"
            )
            
            # Create tasks for parallel execution
            tasks = []
            for step_config in parallel_config.parallel_steps:
                task = asyncio.create_task(self._execute_single_step(step_config))
                tasks.append(task)
            
            # Wait for all tasks to complete
            step_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle exceptions
            processed_results = []
            for i, result in enumerate(step_results):
                if isinstance(result, Exception):
                    # Create error result for failed task
                    error_result = StepResult(
                        step_id=f"parallel_{i}_{int(time.time())}",
                        step_type=parallel_config.parallel_steps[i].step_type,
                        success=False,
                        error=str(result),
                        execution_time=0.0,
                        cost=0.0
                    )
                    processed_results.append(error_result)
                else:
                    processed_results.append(result)
            
            # Merge results based on strategy
            merged_result = self._merge_parallel_results(
                processed_results, 
                parallel_config.merge_strategy
            )
            
            # Update execution time
            merged_result.execution_time = time.time() - parallel_start_time
            
            # Log parallel execution summary
            successful_count = sum(1 for r in processed_results if r.success)
            total_count = len(processed_results)
            
            self.logger.info(
                f"Parallel execution completed: {successful_count}/{total_count} "
                f"steps successful in {merged_result.execution_time:.2f}s"
            )
            
            return merged_result
            
        except Exception as e:
            execution_time = time.time() - parallel_start_time
            error_msg = f"Parallel step execution failed: {str(e)}"
            
            return StepResult(
                step_id=f"parallel_{int(time.time())}",
                step_type=StepType.PARALLEL_GROUP,
                success=False,
                error=error_msg,
                execution_time=execution_time,
                cost=0.0
            )
    
    def _merge_parallel_results(
        self, 
        results: List[StepResult], 
        strategy: str
    ) -> StepResult:
        """Merge parallel step results based on strategy.
        
        Args:
            results: List of step results to merge
            strategy: Merge strategy ('merge_outputs', 'latest_only', 'first_only')
            
        Returns:
            Merged step result
        """
        if not results:
            return StepResult(
                step_id=f"parallel_empty_{int(time.time())}",
                step_type=StepType.PARALLEL_GROUP,
                success=False,
                error="No results to merge",
                execution_time=0.0,
                cost=0.0
            )
        
        # Calculate aggregated values
        total_cost = sum(r.cost for r in results)
        max_execution_time = max(r.execution_time for r in results)
        successful_results = [r for r in results if r.success]
        
        # Determine overall success
        success = len(successful_results) > 0
        
        # Merge based on strategy
        if strategy == "merge_outputs":
            # Combine all successful outputs
            output_paths = [r.output_path for r in successful_results if r.output_path]
            merged_metadata = {}
            for r in successful_results:
                merged_metadata.update(r.metadata)
            
            return StepResult(
                step_id=f"parallel_merged_{int(time.time())}",
                step_type=StepType.PARALLEL_GROUP,
                success=success,
                output_path=output_paths[0] if output_paths else None,
                metadata={
                    **merged_metadata,
                    "parallel_outputs": output_paths,
                    "parallel_results": len(results),
                    "successful_results": len(successful_results)
                },
                execution_time=max_execution_time,
                cost=total_cost
            )
        
        elif strategy == "latest_only":
            # Use the result with the latest completion time
            latest_result = max(results, key=lambda r: r.execution_time)
            latest_result.cost = total_cost
            return latest_result
        
        elif strategy == "first_only":
            # Use the first successful result, or first result if none successful
            if successful_results:
                first_result = successful_results[0]
                first_result.cost = total_cost
                return first_result
            else:
                first_result = results[0]
                first_result.cost = total_cost
                return first_result
        
        else:
            # Default to merge_outputs
            return self._merge_parallel_results(results, "merge_outputs")
    
    def _flatten_steps(self, steps: List[Union[StepConfig, ParallelStepConfig]]) -> List[StepConfig]:
        """Flatten step configurations for cost estimation.
        
        Args:
            steps: Mixed list of step configurations
            
        Returns:
            Flattened list of individual step configurations
        """
        flattened = []
        for step in steps:
            if isinstance(step, ParallelStepConfig):
                flattened.extend(step.parallel_steps)
            else:
                flattened.append(step)
        return flattened
    
    def _is_step_required(self, step_index: int) -> bool:
        """Check if a step is required.
        
        Args:
            step_index: Index of the step
            
        Returns:
            True if step is required
        """
        if step_index < len(self.config.steps):
            step = self.config.steps[step_index]
            return getattr(step, 'required', True)
        return True