"""Configuration loading and management utilities."""

import os
import yaml
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

from ai_content_platform.core.models import PipelineConfig
from ai_content_platform.core.exceptions import ConfigurationError
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.utils.validators import ConfigValidator


class ConfigLoader:
    """Configuration loader with support for YAML and JSON."""
    
    def __init__(self, validator: Optional[ConfigValidator] = None):
        self.logger = get_logger(__name__)
        self.validator = validator or ConfigValidator()
    
    def load_pipeline_config(self, config_path: Union[str, Path]) -> PipelineConfig:
        """Load and validate pipeline configuration.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Validated pipeline configuration
            
        Raises:
            ConfigurationError: If loading or validation fails
        """
        try:
            config_path = Path(config_path)
            
            if not config_path.exists():
                raise ConfigurationError(f"Configuration file not found: {config_path}")
            
            self.logger.info(f"Loading pipeline config from {config_path}")
            
            # Load raw configuration
            raw_config = self._load_raw_config(config_path)
            
            # Process environment variables
            processed_config = self._process_environment_variables(raw_config)
            
            # Create Pydantic model
            pipeline_config = PipelineConfig(**processed_config)
            
            # Validate configuration
            self.validator.validate_pipeline_config(pipeline_config)
            
            self.logger.success(f"Successfully loaded config: {pipeline_config.pipeline_name}")
            return pipeline_config
            
        except Exception as e:
            error_msg = f"Failed to load pipeline config from {config_path}: {str(e)}"
            self.logger.error(error_msg)
            raise ConfigurationError(error_msg) from e
    
    def save_pipeline_config(
        self, 
        config: PipelineConfig, 
        output_path: Union[str, Path],
        format: str = "yaml"
    ) -> Path:
        """Save pipeline configuration to file.
        
        Args:
            config: Pipeline configuration to save
            output_path: Output file path
            format: File format ('yaml' or 'json')
            
        Returns:
            Path to saved file
            
        Raises:
            ConfigurationError: If saving fails
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Saving pipeline config to {output_path}")
            
            # Convert to dictionary
            config_dict = config.dict()
            
            # Save based on format
            if format.lower() == "yaml":
                self._save_yaml(config_dict, output_path)
            elif format.lower() == "json":
                self._save_json(config_dict, output_path)
            else:
                raise ConfigurationError(f"Unsupported format: {format}")
            
            self.logger.success(f"Saved config to {output_path}")
            return output_path
            
        except Exception as e:
            error_msg = f"Failed to save pipeline config: {str(e)}"
            self.logger.error(error_msg)
            raise ConfigurationError(error_msg) from e
    
    def load_environment_config(self, env_file: Optional[Union[str, Path]] = None) -> Dict[str, str]:
        """Load environment configuration from .env file.
        
        Args:
            env_file: Path to .env file (defaults to .env in current directory)
            
        Returns:
            Dictionary of environment variables
            
        Raises:
            ConfigurationError: If loading fails
        """
        try:
            if env_file is None:
                env_file = Path.cwd() / ".env"
            else:
                env_file = Path(env_file)
            
            env_vars = {}
            
            if env_file.exists():
                self.logger.info(f"Loading environment config from {env_file}")
                
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                env_vars[key.strip()] = value.strip().strip('"\'')
                
                self.logger.success(f"Loaded {len(env_vars)} environment variables")
            else:
                self.logger.warning(f"Environment file not found: {env_file}")
            
            return env_vars
            
        except Exception as e:
            error_msg = f"Failed to load environment config: {str(e)}"
            self.logger.error(error_msg)
            raise ConfigurationError(error_msg) from e
    
    def merge_configs(
        self, 
        base_config: Dict[str, Any], 
        override_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge two configuration dictionaries.
        
        Args:
            base_config: Base configuration
            override_config: Override configuration
            
        Returns:
            Merged configuration
        """
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def _load_raw_config(self, config_path: Path) -> Dict[str, Any]:
        """Load raw configuration from file."""
        suffix = config_path.suffix.lower()
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if suffix in ['.yaml', '.yml']:
                    return yaml.safe_load(f) or {}
                elif suffix == '.json':
                    return json.load(f) or {}
                else:
                    raise ConfigurationError(f"Unsupported file format: {suffix}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML format: {str(e)}") from e
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON format: {str(e)}") from e
    
    def _process_environment_variables(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Process environment variable substitutions in configuration."""
        def replace_env_vars(obj):
            if isinstance(obj, str):
                # Replace ${VAR_NAME} or $VAR_NAME with environment variable
                import re
                pattern = r'\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)'
                
                def replacer(match):
                    var_name = match.group(1) or match.group(2)
                    return os.getenv(var_name, match.group(0))
                
                return re.sub(pattern, replacer, obj)
            elif isinstance(obj, dict):
                return {k: replace_env_vars(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [replace_env_vars(item) for item in obj]
            else:
                return obj
        
        return replace_env_vars(config)
    
    def _save_yaml(self, config: Dict[str, Any], output_path: Path) -> None:
        """Save configuration as YAML."""
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(
                config,
                f,
                default_flow_style=False,
                indent=2,
                sort_keys=False,
                allow_unicode=True
            )
    
    def _save_json(self, config: Dict[str, Any], output_path: Path) -> None:
        """Save configuration as JSON."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(
                config,
                f,
                indent=2,
                ensure_ascii=False,
                sort_keys=False
            )
    
    def validate_config_file(self, config_path: Union[str, Path]) -> bool:
        """Validate configuration file without loading into model.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            True if valid
            
        Raises:
            ConfigurationError: If validation fails
        """
        try:
            config_path = Path(config_path)
            
            # Check file exists
            if not config_path.exists():
                raise ConfigurationError(f"Configuration file not found: {config_path}")
            
            # Load and validate basic structure
            raw_config = self._load_raw_config(config_path)
            
            # Check required top-level fields
            required_fields = ["pipeline_name", "steps"]
            missing = [field for field in required_fields if field not in raw_config]
            if missing:
                raise ConfigurationError(f"Missing required fields: {', '.join(missing)}")
            
            self.logger.success(f"Configuration file {config_path} is valid")
            return True
            
        except Exception as e:
            error_msg = f"Configuration validation failed: {str(e)}"
            self.logger.error(error_msg)
            raise ConfigurationError(error_msg) from e
    
    def get_config_template(self, step_types: Optional[list] = None) -> Dict[str, Any]:
        """Generate configuration template.
        
        Args:
            step_types: List of step types to include
            
        Returns:
            Configuration template
        """
        template = {
            "pipeline_name": "example_pipeline",
            "description": "Example AI content generation pipeline",
            "output_directory": "output",
            "global_config": {
                "max_cost": 10.0,
                "timeout": 300
            },
            "steps": []
        }
        
        if step_types:
            for step_type in step_types:
                step_template = self._get_step_template(step_type)
                if step_template:
                    template["steps"].append(step_template)
        
        return template
    
    def _get_step_template(self, step_type: str) -> Optional[Dict[str, Any]]:
        """Get template for specific step type."""
        templates = {
            "text_to_speech": {
                "name": "example_tts",
                "step_type": "text_to_speech",
                "parameters": {
                    "text": "Hello, this is a test message.",
                    "voice_id": "example_voice",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }
            },
            "text_to_image": {
                "name": "example_image",
                "step_type": "text_to_image",
                "parameters": {
                    "prompt": "A beautiful landscape with mountains and lakes",
                    "model": "flux-1-dev",
                    "width": 1024,
                    "height": 1024
                }
            },
            "text_to_video": {
                "name": "example_video",
                "step_type": "text_to_video",
                "parameters": {
                    "prompt": "A time-lapse of a sunrise over mountains",
                    "model": "minimax-hailuo-02-pro",
                    "duration": 6
                }
            }
        }
        
        return templates.get(step_type)