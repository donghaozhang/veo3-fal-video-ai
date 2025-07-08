"""Input validation utilities."""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from ai_content_platform.core.models import (
    PipelineConfig, 
    StepConfig, 
    ParallelStepConfig,
    StepType
)
from ai_content_platform.core.exceptions import ValidationError
from ai_content_platform.utils.logger import get_logger


class ConfigValidator:
    """Validator for pipeline configurations."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def validate_pipeline_config(self, config: PipelineConfig) -> bool:
        """Validate complete pipeline configuration.
        
        Args:
            config: Pipeline configuration to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            self.logger.debug(f"Validating pipeline config: {config.pipeline_name}")
            
            # Validate basic fields
            self._validate_required_fields(config)
            
            # Validate steps
            self._validate_steps(config.steps)
            
            # Validate output directory
            self._validate_output_directory(config.output_directory)
            
            # Validate global config
            self._validate_global_config(config.global_config)
            
            self.logger.success(f"Pipeline config '{config.pipeline_name}' is valid")
            return True
            
        except Exception as e:
            error_msg = f"Pipeline config validation failed: {str(e)}"
            self.logger.error(error_msg)
            raise ValidationError(error_msg) from e
    
    def _validate_required_fields(self, config: PipelineConfig) -> None:
        """Validate required fields in pipeline config."""
        if not config.pipeline_name or not config.pipeline_name.strip():
            raise ValidationError("Pipeline name is required and cannot be empty")
        
        if not config.steps:
            raise ValidationError("Pipeline must have at least one step")
        
        # Validate pipeline name format
        if not re.match(r'^[a-zA-Z0-9_-]+$', config.pipeline_name):
            raise ValidationError(
                "Pipeline name can only contain letters, numbers, underscores, and hyphens"
            )
    
    def _validate_steps(self, steps: List[Union[StepConfig, ParallelStepConfig]]) -> None:
        """Validate pipeline steps."""
        for i, step in enumerate(steps):
            try:
                if isinstance(step, ParallelStepConfig):
                    self._validate_parallel_step(step)
                else:
                    self._validate_step_config(step)
            except ValidationError as e:
                raise ValidationError(f"Step {i + 1}: {str(e)}") from e
    
    def _validate_step_config(self, step: StepConfig) -> None:
        """Validate individual step configuration."""
        # Validate step type
        if step.step_type not in StepType:
            raise ValidationError(f"Invalid step type: {step.step_type}")
        
        # Validate step name
        if not step.name or not step.name.strip():
            raise ValidationError("Step name is required")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', step.name):
            raise ValidationError(
                "Step name can only contain letters, numbers, underscores, and hyphens"
            )
        
        # Validate parameters based on step type
        self._validate_step_parameters(step)
    
    def _validate_parallel_step(self, step: ParallelStepConfig) -> None:
        """Validate parallel step configuration."""
        if not step.parallel_steps:
            raise ValidationError("Parallel step must contain at least one sub-step")
        
        if len(step.parallel_steps) < 2:
            raise ValidationError("Parallel step should have at least 2 sub-steps")
        
        # Validate each sub-step
        for sub_step in step.parallel_steps:
            self._validate_step_config(sub_step)
        
        # Validate merge strategy
        valid_strategies = ["merge_outputs", "latest_only", "first_only"]
        if step.merge_strategy not in valid_strategies:
            raise ValidationError(f"Invalid merge strategy: {step.merge_strategy}")
    
    def _validate_step_parameters(self, step: StepConfig) -> None:
        """Validate step-specific parameters."""
        params = step.parameters
        
        if step.step_type == StepType.TEXT_TO_SPEECH:
            self._validate_tts_parameters(params)
        elif step.step_type == StepType.TEXT_TO_IMAGE:
            self._validate_text_to_image_parameters(params)
        elif step.step_type == StepType.IMAGE_TO_IMAGE:
            self._validate_image_to_image_parameters(params)
        elif step.step_type == StepType.TEXT_TO_VIDEO:
            self._validate_text_to_video_parameters(params)
        elif step.step_type == StepType.VIDEO_TO_VIDEO:
            self._validate_video_to_video_parameters(params)
        elif step.step_type == StepType.AVATAR_GENERATION:
            self._validate_avatar_parameters(params)
    
    def _validate_tts_parameters(self, params: Dict[str, Any]) -> None:
        """Validate text-to-speech parameters."""
        required = ["text"]
        self._check_required_parameters(params, required)
        
        if "voice_id" in params and not isinstance(params["voice_id"], str):
            raise ValidationError("voice_id must be a string")
        
        if "voice_settings" in params and not isinstance(params["voice_settings"], dict):
            raise ValidationError("voice_settings must be a dictionary")
    
    def _validate_text_to_image_parameters(self, params: Dict[str, Any]) -> None:
        """Validate text-to-image parameters."""
        required = ["prompt"]
        self._check_required_parameters(params, required)
        
        if "model" in params:
            valid_models = ["imagen-4", "seedream-v3", "flux-1-schnell", "flux-1-dev"]
            if params["model"] not in valid_models:
                raise ValidationError(f"Invalid text-to-image model: {params['model']}")
    
    def _validate_image_to_image_parameters(self, params: Dict[str, Any]) -> None:
        """Validate image-to-image parameters."""
        required = ["image_url", "prompt"]
        self._check_required_parameters(params, required)
        
        # Validate image URL
        if not self._is_valid_url(params["image_url"]):
            raise ValidationError("image_url must be a valid URL")
    
    def _validate_text_to_video_parameters(self, params: Dict[str, Any]) -> None:
        """Validate text-to-video parameters."""
        required = ["prompt"]
        self._check_required_parameters(params, required)
        
        if "model" in params:
            valid_models = ["minimax-hailuo-02-pro", "google-veo-3"]
            if params["model"] not in valid_models:
                raise ValidationError(f"Invalid text-to-video model: {params['model']}")
    
    def _validate_video_to_video_parameters(self, params: Dict[str, Any]) -> None:
        """Validate video-to-video parameters."""
        required = ["video_url"]
        self._check_required_parameters(params, required)
        
        # Validate video URL
        if not self._is_valid_url(params["video_url"]):
            raise ValidationError("video_url must be a valid URL")
    
    def _validate_avatar_parameters(self, params: Dict[str, Any]) -> None:
        """Validate avatar generation parameters."""
        # Must have either text or audio_url
        if not params.get("text") and not params.get("audio_url"):
            raise ValidationError("Avatar step requires either 'text' or 'audio_url'")
        
        required = ["image_url"]
        self._check_required_parameters(params, required)
        
        # Validate image URL
        if not self._is_valid_url(params["image_url"]):
            raise ValidationError("image_url must be a valid URL")
    
    def _check_required_parameters(self, params: Dict[str, Any], required: List[str]) -> None:
        """Check if required parameters are present."""
        missing = [param for param in required if param not in params]
        if missing:
            raise ValidationError(f"Missing required parameters: {', '.join(missing)}")
    
    def _validate_output_directory(self, output_dir: str) -> None:
        """Validate output directory."""
        if not output_dir or not output_dir.strip():
            raise ValidationError("Output directory cannot be empty")
        
        # Check if path is valid
        try:
            Path(output_dir)
        except Exception as e:
            raise ValidationError(f"Invalid output directory path: {str(e)}") from e
    
    def _validate_global_config(self, global_config: Dict[str, Any]) -> None:
        """Validate global configuration."""
        if not isinstance(global_config, dict):
            raise ValidationError("Global config must be a dictionary")
        
        # Validate specific global config fields if present
        if "max_cost" in global_config:
            if not isinstance(global_config["max_cost"], (int, float)) or global_config["max_cost"] < 0:
                raise ValidationError("max_cost must be a non-negative number")
        
        if "timeout" in global_config:
            if not isinstance(global_config["timeout"], (int, float)) or global_config["timeout"] <= 0:
                raise ValidationError("timeout must be a positive number")
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False


class InputValidator:
    """General input validation utilities."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def validate_file_path(self, file_path: Union[str, Path]) -> Path:
        """Validate and return Path object.
        
        Args:
            file_path: File path to validate
            
        Returns:
            Validated Path object
            
        Raises:
            ValidationError: If path is invalid
        """
        try:
            path = Path(file_path)
            if not path.exists():
                raise ValidationError(f"File does not exist: {file_path}")
            return path
        except Exception as e:
            raise ValidationError(f"Invalid file path: {str(e)}") from e
    
    def validate_url(self, url: str) -> str:
        """Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            Validated URL
            
        Raises:
            ValidationError: If URL is invalid
        """
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValidationError(f"Invalid URL format: {url}")
            return url
        except Exception as e:
            raise ValidationError(f"URL validation failed: {str(e)}") from e
    
    def validate_api_key(self, api_key: str, service_name: str) -> str:
        """Validate API key format.
        
        Args:
            api_key: API key to validate
            service_name: Name of the service (for error messages)
            
        Returns:
            Validated API key
            
        Raises:
            ValidationError: If API key is invalid
        """
        if not api_key or not api_key.strip():
            raise ValidationError(f"{service_name} API key cannot be empty")
        
        if len(api_key.strip()) < 10:
            raise ValidationError(f"{service_name} API key appears to be too short")
        
        return api_key.strip()
    
    def validate_positive_number(self, value: Union[int, float], name: str) -> Union[int, float]:
        """Validate positive number.
        
        Args:
            value: Number to validate
            name: Parameter name (for error messages)
            
        Returns:
            Validated number
            
        Raises:
            ValidationError: If number is invalid
        """
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{name} must be a number")
        
        if value <= 0:
            raise ValidationError(f"{name} must be positive")
        
        return value
    
    def validate_email(self, email: str) -> str:
        """Validate email format.
        
        Args:
            email: Email to validate
            
        Returns:
            Validated email
            
        Raises:
            ValidationError: If email is invalid
        """
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        if not email_pattern.match(email):
            raise ValidationError(f"Invalid email format: {email}")
        
        return email