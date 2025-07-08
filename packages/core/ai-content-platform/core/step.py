"""Pipeline step implementation."""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List

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