"""
Base classes for AI Content Pipeline models
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time


@dataclass
class ModelResult:
    """Standard result format for all pipeline models."""
    success: bool
    model_used: str
    processing_time: float
    cost_estimate: float
    output_path: Optional[str] = None
    output_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class BaseContentModel(ABC):
    """
    Abstract base class for all content generation models in the pipeline.
    """
    
    def __init__(self, model_type: str):
        """
        Initialize base model.
        
        Args:
            model_type: Type of model (e.g., "text_to_image", "image_to_video")
        """
        self.model_type = model_type
        self.start_time = None
    
    @abstractmethod
    def generate(self, input_data: Any, model: str, **kwargs) -> ModelResult:
        """
        Generate content using the specified model.
        
        Args:
            input_data: Input data for generation
            model: Specific model to use
            **kwargs: Additional model-specific parameters
            
        Returns:
            ModelResult with generation results
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> list:
        """
        Get list of available models for this content type.
        
        Returns:
            List of available model names
        """
        pass
    
    @abstractmethod
    def estimate_cost(self, model: str, **kwargs) -> float:
        """
        Estimate the cost for generation with given parameters.
        
        Args:
            model: Model to estimate cost for
            **kwargs: Generation parameters
            
        Returns:
            Estimated cost in USD
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Any, model: str, **kwargs) -> bool:
        """
        Validate input data and parameters.
        
        Args:
            input_data: Input data to validate
            model: Model to validate for
            **kwargs: Parameters to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def recommend_model(self, criteria: str = "balanced", budget: Optional[float] = None) -> str:
        """
        Recommend the best model based on criteria and budget.
        
        Args:
            criteria: Selection criteria ("quality", "speed", "cost", "balanced")
            budget: Optional budget constraint
            
        Returns:
            Recommended model name
        """
        from ..config.constants import MODEL_RECOMMENDATIONS, COST_ESTIMATES
        
        model_recs = MODEL_RECOMMENDATIONS.get(self.model_type, {})
        
        # If budget constraint, filter models
        if budget is not None:
            costs = COST_ESTIMATES.get(self.model_type, {})
            affordable_models = [
                model for model, cost in costs.items() 
                if cost <= budget
            ]
            if not affordable_models:
                # Return cheapest model if none are affordable
                return min(costs.keys(), key=lambda k: costs[k])
        
        # Return recommendation based on criteria
        if criteria in model_recs:
            return model_recs[criteria]
        
        # Default to first available model
        available = self.get_available_models()
        return available[0] if available else None
    
    def _start_timing(self):
        """Start timing for processing."""
        self.start_time = time.time()
    
    def _get_processing_time(self) -> float:
        """Get processing time since start."""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time
    
    def _create_success_result(
        self, 
        model: str, 
        output_path: Optional[str] = None,
        output_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ModelResult:
        """Create a successful result."""
        return ModelResult(
            success=True,
            model_used=model,
            processing_time=self._get_processing_time(),
            cost_estimate=self.estimate_cost(model),
            output_path=output_path,
            output_url=output_url,
            metadata=metadata or {}
        )
    
    def _create_error_result(self, model: str, error: str) -> ModelResult:
        """Create an error result."""
        return ModelResult(
            success=False,
            model_used=model,
            processing_time=self._get_processing_time(),
            cost_estimate=0.0,
            error=error
        )