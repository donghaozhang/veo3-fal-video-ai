# AI Content Generation Platform - Package Creation Guide (Part 4)

## 🛠️ Phase 4: Utility Modules, Configuration, and CLI

### Step 4.1: Utility Modules Structure

Create utility modules:
```bash
# Create utils structure
mkdir -p ai_content_platform/utils
touch ai_content_platform/utils/__init__.py
touch ai_content_platform/utils/logger.py
touch ai_content_platform/utils/file_manager.py
touch ai_content_platform/utils/validators.py
touch ai_content_platform/utils/cost_calculator.py
touch ai_content_platform/utils/config_loader.py
```

### Step 4.2: Logging Utility

Create `ai_content_platform/utils/logger.py`:
```python
"""Logging utilities for AI Content Platform."""

import logging
import sys
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Get a configured logger instance."""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    # Set level
    log_level = getattr(logging, (level or 'INFO').upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # Create rich handler for beautiful console output
    console = Console(stderr=True)
    handler = RichHandler(
        console=console,
        show_time=True,
        show_level=True,
        show_path=False,
        markup=True,
        rich_tracebacks=True
    )
    
    # Set format
    formatter = logging.Formatter(
        "%(message)s",
        datefmt="[%X]"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.propagate = False
    
    return logger


def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Setup global logging configuration."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RichHandler(show_time=True, show_level=True, show_path=False)
        ]
    )
    
    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(file_handler)
```

### Step 4.3: File Management Utility

Create `ai_content_platform/utils/file_manager.py`:
```python
"""File management utilities."""

import os
import aiohttp
import asyncio
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse

from ai_content_platform.utils.logger import get_logger


logger = get_logger(__name__)


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if not."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


async def save_file_from_url(
    url: str, 
    output_dir: Union[str, Path], 
    filename: Optional[str] = None
) -> str:
    """Download file from URL and save to directory."""
    output_dir = ensure_directory(output_dir)
    
    if not filename:
        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path) or "downloaded_file"
        
        # Add extension if missing
        if '.' not in filename:
            filename += '.bin'
    
    output_path = output_dir / filename
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
        
        logger.info(f"File saved: {output_path}")
        return str(output_path)
        
    except Exception as e:
        logger.error(f"Failed to download file from {url}: {e}")
        raise


def get_file_size(path: Union[str, Path]) -> int:
    """Get file size in bytes."""
    return Path(path).stat().st_size


def get_file_extension(path: Union[str, Path]) -> str:
    """Get file extension."""
    return Path(path).suffix.lower()


def is_valid_file_type(path: Union[str, Path], allowed_types: list) -> bool:
    """Check if file type is in allowed list."""
    extension = get_file_extension(path)
    return extension in [ext.lower() for ext in allowed_types]


def cleanup_temp_files(temp_dir: Union[str, Path], max_age_hours: int = 24):
    """Clean up temporary files older than max_age."""
    import time
    
    temp_dir = Path(temp_dir)
    if not temp_dir.exists():
        return
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for file_path in temp_dir.iterdir():
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                    logger.info(f"Cleaned up temp file: {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to clean up {file_path}: {e}")
```

### Step 4.4: Validation Utilities

Create `ai_content_platform/utils/validators.py`:
```python
"""Validation utilities for inputs and configurations."""

import re
import os
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from ai_content_platform.core.exceptions import ValidationError


def validate_text_input(text: str, min_length: int = 1, max_length: int = 10000) -> bool:
    """Validate text input."""
    if not isinstance(text, str):
        raise ValidationError("Text must be a string")
    
    if len(text.strip()) < min_length:
        raise ValidationError(f"Text must be at least {min_length} characters")
    
    if len(text) > max_length:
        raise ValidationError(f"Text must be less than {max_length} characters")
    
    return True


def validate_url(url: str) -> bool:
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        raise ValidationError(f"Invalid URL format: {url}")


def validate_file_path(path: str, must_exist: bool = False) -> bool:
    """Validate file path."""
    if not isinstance(path, str):
        raise ValidationError("File path must be a string")
    
    if must_exist and not os.path.exists(path):
        raise ValidationError(f"File does not exist: {path}")
    
    return True


def validate_image_dimensions(width: int, height: int, max_dimension: int = 2048) -> bool:
    """Validate image dimensions."""
    if not isinstance(width, int) or not isinstance(height, int):
        raise ValidationError("Width and height must be integers")
    
    if width <= 0 or height <= 0:
        raise ValidationError("Width and height must be positive")
    
    if width > max_dimension or height > max_dimension:
        raise ValidationError(f"Dimensions cannot exceed {max_dimension}x{max_dimension}")
    
    return True


def validate_api_key(api_key: str, service_name: str = "service") -> bool:
    """Validate API key format."""
    if not isinstance(api_key, str):
        raise ValidationError(f"{service_name} API key must be a string")
    
    if len(api_key.strip()) < 10:
        raise ValidationError(f"{service_name} API key appears to be too short")
    
    return True


def validate_cost_limit(cost: float, max_cost: float = 100.0) -> bool:
    """Validate cost against limit."""
    if not isinstance(cost, (int, float)):
        raise ValidationError("Cost must be a number")
    
    if cost < 0:
        raise ValidationError("Cost cannot be negative")
    
    if cost > max_cost:
        raise ValidationError(f"Estimated cost ${cost:.2f} exceeds limit ${max_cost:.2f}")
    
    return True


def validate_pipeline_config(config: Dict[str, Any]) -> bool:
    """Validate pipeline configuration."""
    required_fields = ['pipeline_name', 'steps']
    
    for field in required_fields:
        if field not in config:
            raise ValidationError(f"Missing required field: {field}")
    
    if not isinstance(config['steps'], list):
        raise ValidationError("Steps must be a list")
    
    if len(config['steps']) == 0:
        raise ValidationError("Pipeline must have at least one step")
    
    return True


def validate_step_config(step_config: Dict[str, Any]) -> bool:
    """Validate individual step configuration."""
    if 'step_type' not in step_config:
        raise ValidationError("Step must have step_type")
    
    if 'config' not in step_config:
        raise ValidationError("Step must have config")
    
    return True


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be filesystem-safe."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename


def validate_parallel_config(config: Dict[str, Any]) -> bool:
    """Validate parallel execution configuration."""
    if 'steps' not in config:
        raise ValidationError("Parallel config must have steps")
    
    if not isinstance(config['steps'], list):
        raise ValidationError("Parallel steps must be a list")
    
    if len(config['steps']) < 2:
        raise ValidationError("Parallel execution requires at least 2 steps")
    
    return True
```

### Step 4.5: Cost Calculator Utility

Create `ai_content_platform/utils/cost_calculator.py`:
```python
"""Cost calculation utilities."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from ai_content_platform.core.models import StepConfig, StepType
from ai_content_platform.core.step import StepFactory
from ai_content_platform.utils.logger import get_logger


logger = get_logger(__name__)


@dataclass
class CostEstimate:
    """Cost estimate for pipeline execution."""
    total_cost: float
    step_costs: Dict[str, float]
    currency: str = "USD"
    confidence: str = "medium"  # low, medium, high


class CostCalculator:
    """Calculate costs for pipeline execution."""
    
    # Base cost estimates per service (approximate)
    SERVICE_COSTS = {
        StepType.TEXT_TO_SPEECH: {
            'base_cost': 0.001,  # per 1000 characters
            'unit': 'per_1000_chars'
        },
        StepType.TEXT_TO_IMAGE: {
            'base_cost': 0.005,  # per image
            'unit': 'per_image'
        },
        StepType.TEXT_TO_VIDEO: {
            'base_cost': 0.08,   # per video (6 seconds)
            'unit': 'per_video'
        },
        StepType.IMAGE_TO_IMAGE: {
            'base_cost': 0.01,   # per image
            'unit': 'per_image'
        },
        StepType.VIDEO_TO_VIDEO: {
            'base_cost': 0.10,   # per video
            'unit': 'per_video'
        },
        StepType.AVATAR_GENERATION: {
            'base_cost': 0.05,   # per avatar video
            'unit': 'per_video'
        }
    }
    
    @classmethod
    def estimate_pipeline_cost(cls, steps: List[StepConfig]) -> CostEstimate:
        """Estimate total cost for pipeline execution."""
        total_cost = 0.0
        step_costs = {}
        
        for step_config in steps:
            try:
                step = StepFactory.create_step(step_config)
                cost = step.estimate_cost()
                total_cost += cost
                step_costs[f"{step_config.step_type.value}_{step.step_id}"] = cost
                
            except Exception as e:
                logger.warning(f"Could not estimate cost for {step_config.step_type}: {e}")
                # Use fallback estimate
                fallback_cost = cls._get_fallback_cost(step_config)
                total_cost += fallback_cost
                step_costs[f"{step_config.step_type.value}_fallback"] = fallback_cost
        
        return CostEstimate(
            total_cost=total_cost,
            step_costs=step_costs,
            confidence="medium" if len(step_costs) > 0 else "low"
        )
    
    @classmethod
    def _get_fallback_cost(cls, step_config: StepConfig) -> float:
        """Get fallback cost estimate when step creation fails."""
        service_info = cls.SERVICE_COSTS.get(step_config.step_type)
        if not service_info:
            return 0.10  # Default fallback
        
        return service_info['base_cost']
    
    @classmethod
    def estimate_step_cost(cls, step_config: StepConfig) -> float:
        """Estimate cost for a single step."""
        try:
            step = StepFactory.create_step(step_config)
            return step.estimate_cost()
        except Exception:
            return cls._get_fallback_cost(step_config)
    
    @classmethod
    def format_cost_estimate(cls, estimate: CostEstimate) -> str:
        """Format cost estimate for display."""
        lines = [
            f"💰 Cost Estimate: ${estimate.total_cost:.3f} {estimate.currency}",
            f"📊 Confidence: {estimate.confidence}",
            "",
            "📋 Step Breakdown:"
        ]
        
        for step_name, cost in estimate.step_costs.items():
            lines.append(f"  • {step_name}: ${cost:.3f}")
        
        return "\n".join(lines)
    
    @classmethod
    def check_cost_limit(cls, estimate: CostEstimate, limit: float) -> bool:
        """Check if estimate exceeds cost limit."""
        return estimate.total_cost <= limit
    
    @classmethod
    def get_cost_warning_message(cls, estimate: CostEstimate, limit: float) -> Optional[str]:
        """Get warning message if cost is high."""
        if estimate.total_cost > limit:
            return (
                f"⚠️  Estimated cost ${estimate.total_cost:.3f} exceeds limit ${limit:.2f}. "
                f"Continue anyway?"
            )
        elif estimate.total_cost > limit * 0.8:
            return (
                f"💡 Estimated cost ${estimate.total_cost:.3f} is approaching limit ${limit:.2f}."
            )
        
        return None
```

### Step 4.6: Configuration Management

Create `ai_content_platform/utils/config_loader.py`:
```python
"""Configuration loading and management utilities."""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union

from ai_content_platform.core.models import PipelineConfig
from ai_content_platform.core.exceptions import PipelineConfigurationError
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.utils.validators import validate_pipeline_config


logger = get_logger(__name__)


class ConfigLoader:
    """Load and validate pipeline configurations."""
    
    @staticmethod
    def load_from_file(config_path: Union[str, Path]) -> PipelineConfig:
        """Load pipeline configuration from file."""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise PipelineConfigurationError(f"Config file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    config_data = yaml.safe_load(f)
                elif config_path.suffix.lower() == '.json':
                    config_data = json.load(f)
                else:
                    raise PipelineConfigurationError(f"Unsupported config format: {config_path.suffix}")
            
            # Validate configuration
            validate_pipeline_config(config_data)
            
            # Convert to PipelineConfig
            return PipelineConfig(**config_data)
            
        except yaml.YAMLError as e:
            raise PipelineConfigurationError(f"Invalid YAML in {config_path}: {e}")
        except json.JSONDecodeError as e:
            raise PipelineConfigurationError(f"Invalid JSON in {config_path}: {e}")
        except Exception as e:
            raise PipelineConfigurationError(f"Error loading config from {config_path}: {e}")
    
    @staticmethod
    def load_from_dict(config_data: Dict[str, Any]) -> PipelineConfig:
        """Load pipeline configuration from dictionary."""
        try:
            validate_pipeline_config(config_data)
            return PipelineConfig(**config_data)
        except Exception as e:
            raise PipelineConfigurationError(f"Invalid configuration: {e}")
    
    @staticmethod
    def save_to_file(config: PipelineConfig, output_path: Union[str, Path]):
        """Save pipeline configuration to file."""
        output_path = Path(output_path)
        
        try:
            config_dict = config.dict()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                if output_path.suffix.lower() in ['.yaml', '.yml']:
                    yaml.dump(config_dict, f, default_flow_style=False, indent=2)
                elif output_path.suffix.lower() == '.json':
                    json.dump(config_dict, f, indent=2)
                else:
                    raise PipelineConfigurationError(f"Unsupported output format: {output_path.suffix}")
            
            logger.info(f"Configuration saved to: {output_path}")
            
        except Exception as e:
            raise PipelineConfigurationError(f"Error saving config to {output_path}: {e}")
    
    @staticmethod
    def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two configurations, with override taking precedence."""
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = ConfigLoader.merge_configs(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    @staticmethod
    def substitute_environment_variables(config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Substitute environment variables in configuration."""
        def substitute_recursive(obj):
            if isinstance(obj, dict):
                return {key: substitute_recursive(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [substitute_recursive(item) for item in obj]
            elif isinstance(obj, str) and obj.startswith('$'):
                env_var = obj[1:]
                return os.getenv(env_var, obj)
            else:
                return obj
        
        return substitute_recursive(config_data)
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default pipeline configuration."""
        return {
            "pipeline_name": "default_pipeline",
            "description": "Default AI content generation pipeline",
            "output_directory": "output",
            "steps": [],
            "global_config": {
                "parallel_enabled": False,
                "cost_limit": 10.0,
                "timeout": 300
            }
        }
    
    @staticmethod
    def validate_and_fix_config(config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration and apply fixes where possible."""
        # Apply defaults
        default_config = ConfigLoader.get_default_config()
        config_data = ConfigLoader.merge_configs(default_config, config_data)
        
        # Substitute environment variables
        config_data = ConfigLoader.substitute_environment_variables(config_data)
        
        # Validate
        validate_pipeline_config(config_data)
        
        return config_data


def load_config(config_path: Union[str, Path]) -> PipelineConfig:
    """Convenience function to load configuration."""
    return ConfigLoader.load_from_file(config_path)


def create_example_config(output_path: Union[str, Path] = "example_pipeline.yaml"):
    """Create an example pipeline configuration file."""
    example_config = {
        "pipeline_name": "example_tts_pipeline",
        "description": "Example text-to-speech pipeline",
        "output_directory": "output",
        "global_config": {
            "parallel_enabled": False,
            "cost_limit": 5.0
        },
        "steps": [
            {
                "step_type": "text_to_speech",
                "config": {
                    "text": "Hello, this is an example of AI-generated speech!",
                    "voice": "Rachel",
                    "model": "eleven_monolingual_v1"
                },
                "output_filename": "example_speech.mp3"
            }
        ]
    }
    
    with open(output_path, 'w') as f:
        yaml.dump(example_config, f, default_flow_style=False, indent=2)
    
    logger.info(f"Example configuration created: {output_path}")
```

---

**Part 4 Complete** - This covers:

1. **Logging Utility** - Rich console logging with file output support
2. **File Management** - Async file downloads, directory management, cleanup
3. **Validation Utilities** - Comprehensive input validation and sanitization
4. **Cost Calculator** - Accurate cost estimation with confidence levels
5. **Configuration Management** - YAML/JSON loading with validation and environment variable substitution

The next part will cover CLI implementation, setup.py, testing framework, and final packaging. Would you like me to continue with Part 5?