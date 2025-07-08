# AI Content Generation Platform - Package Creation Guide (Part 3)

## 🔧 Phase 3: Service Integrations and Parallel Execution

### Step 3.1: Parallel Executor Implementation

Create `ai_content_platform/core/parallel_executor.py`:
```python
"""Parallel execution implementation for pipeline steps."""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional

from ai_content_platform.core.models import (
    ParallelStepConfig, StepResult, MergeStrategy
)
from ai_content_platform.core.step import StepFactory
from ai_content_platform.core.exceptions import ParallelExecutionError
from ai_content_platform.utils.logger import get_logger


logger = get_logger(__name__)


class ParallelExecutor:
    """Executor for parallel step groups."""
    
    def __init__(self, config: ParallelStepConfig):
        self.config = config
        self.max_workers = config.parallel_config.max_workers or min(32, len(config.steps) + 4)
    
    async def execute(self, context: Dict[str, Any]) -> List[StepResult]:
        """Execute steps in parallel and merge results."""
        logger.info(f"Starting parallel execution of {len(self.config.steps)} steps")
        start_time = time.time()
        
        try:
            # Create step instances
            steps = []
            for step_config in self.config.steps:
                step = StepFactory.create_step(step_config)
                steps.append(step)
            
            # Execute steps in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_step = {
                    executor.submit(self._execute_step_sync, step, context.copy()): step 
                    for step in steps
                }
                
                results = []
                for future in as_completed(future_to_step, timeout=self.config.parallel_config.timeout):
                    try:
                        result = future.result()
                        results.append(result)
                        logger.info(f"Step completed: {result.step_type}")
                    except Exception as e:
                        step = future_to_step[future]
                        logger.error(f"Step failed: {step.config.step_type} - {e}")
                        results.append(StepResult(
                            step_id=step.step_id,
                            step_type=step.config.step_type,
                            success=False,
                            error=str(e)
                        ))
            
            # Apply merge strategy
            merged_results = self._apply_merge_strategy(results)
            
            execution_time = time.time() - start_time
            logger.info(f"Parallel execution completed in {execution_time:.2f}s")
            
            return merged_results
            
        except Exception as e:
            logger.error(f"Parallel execution failed: {e}")
            raise ParallelExecutionError(f"Parallel execution failed: {e}")
    
    def _execute_step_sync(self, step, context: Dict[str, Any]) -> StepResult:
        """Execute a single step synchronously (for thread pool)."""
        try:
            # Run async step in new event loop for thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(step.execute(context))
            finally:
                loop.close()
        except Exception as e:
            return StepResult(
                step_id=step.step_id,
                step_type=step.config.step_type,
                success=False,
                error=str(e)
            )
    
    def _apply_merge_strategy(self, results: List[StepResult]) -> List[StepResult]:
        """Apply merge strategy to parallel results."""
        strategy = self.config.parallel_config.merge_strategy
        
        if strategy == MergeStrategy.COLLECT_ALL:
            return results
        
        elif strategy == MergeStrategy.FIRST_SUCCESS:
            # Return first successful result, or all if none succeeded
            for result in results:
                if result.success:
                    return [result]
            return results
        
        elif strategy == MergeStrategy.BEST_QUALITY:
            # Return result with highest quality score (if available in metadata)
            successful_results = [r for r in results if r.success]
            if not successful_results:
                return results
            
            best_result = max(
                successful_results,
                key=lambda r: r.metadata.get('quality_score', 0.0)
            )
            return [best_result]
        
        return results
```

### Step 3.2: Service Integrations Structure

Create the services directory structure:
```bash
# Create services structure
mkdir -p ai_content_platform/services/{fal_ai,google,elevenlabs,openrouter}

# FAL AI services
touch ai_content_platform/services/fal_ai/__init__.py
touch ai_content_platform/services/fal_ai/base.py
touch ai_content_platform/services/fal_ai/text_to_image.py
touch ai_content_platform/services/fal_ai/image_to_image.py
touch ai_content_platform/services/fal_ai/text_to_video.py
touch ai_content_platform/services/fal_ai/video_to_video.py
touch ai_content_platform/services/fal_ai/avatar.py

# Google services
touch ai_content_platform/services/google/__init__.py
touch ai_content_platform/services/google/veo.py
touch ai_content_platform/services/google/gemini.py

# ElevenLabs services
touch ai_content_platform/services/elevenlabs/__init__.py
touch ai_content_platform/services/elevenlabs/tts.py

# OpenRouter services
touch ai_content_platform/services/openrouter/__init__.py
touch ai_content_platform/services/openrouter/client.py
```

### Step 3.3: FAL AI Base Service

Create `ai_content_platform/services/fal_ai/base.py`:
```python
"""Base FAL AI service implementation."""

import os
import time
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

try:
    import fal_client
except ImportError:
    fal_client = None

from ai_content_platform.core.step import BaseStep
from ai_content_platform.core.models import StepResult
from ai_content_platform.core.exceptions import APIKeyError, ServiceNotAvailableError
from ai_content_platform.utils.logger import get_logger


logger = get_logger(__name__)


class FALBaseStep(BaseStep):
    """Base class for FAL AI service steps."""
    
    def __init__(self, config):
        super().__init__(config)
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize FAL AI client."""
        if fal_client is None:
            raise ServiceNotAvailableError("fal-client not installed. Run: pip install fal-client")
        
        api_key = os.getenv('FAL_KEY') or self.config.config.get('api_key')
        if not api_key:
            raise APIKeyError("FAL_KEY environment variable or api_key in config required")
        
        fal_client.api_key = api_key
    
    @abstractmethod
    def get_model_endpoint(self) -> str:
        """Get the FAL AI model endpoint."""
        pass
    
    @abstractmethod
    def prepare_arguments(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare arguments for the FAL AI model."""
        pass
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute FAL AI model."""
        start_time = time.time()
        
        try:
            # Prepare model arguments
            arguments = self.prepare_arguments(context)
            endpoint = self.get_model_endpoint()
            
            logger.info(f"Submitting to FAL AI: {endpoint}")
            
            # Submit job to FAL AI
            handler = fal_client.submit(endpoint, arguments=arguments)
            
            # Wait for completion
            result = handler.get()
            
            # Process result
            output_path = await self._process_result(result, context)
            
            execution_time = time.time() - start_time
            cost = self._calculate_cost(arguments)
            
            return self._create_result(
                success=True,
                output_path=output_path,
                metadata={
                    'model_endpoint': endpoint,
                    'fal_result': result,
                    'arguments': arguments
                },
                execution_time=execution_time,
                cost=cost
            )
            
        except Exception as e:
            logger.error(f"FAL AI execution failed: {e}")
            execution_time = time.time() - start_time
            
            return self._create_result(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    @abstractmethod
    async def _process_result(self, result: Dict[str, Any], context: Dict[str, Any]) -> Optional[str]:
        """Process FAL AI result and return output path."""
        pass
    
    def _calculate_cost(self, arguments: Dict[str, Any]) -> float:
        """Calculate estimated cost for the operation."""
        # Override in subclasses with specific cost models
        return 0.0
    
    def validate_config(self) -> bool:
        """Validate step configuration."""
        required_fields = self.get_required_config_fields()
        for field in required_fields:
            if field not in self.config.config:
                logger.error(f"Missing required config field: {field}")
                return False
        return True
    
    @abstractmethod
    def get_required_config_fields(self) -> list:
        """Get list of required configuration fields."""
        pass
```

### Step 3.4: FAL AI Text-to-Image Service

Create `ai_content_platform/services/fal_ai/text_to_image.py`:
```python
"""FAL AI text-to-image service implementation."""

import os
import aiohttp
from typing import Dict, Any, Optional

from ai_content_platform.services.fal_ai.base import FALBaseStep
from ai_content_platform.core.models import StepType
from ai_content_platform.utils.file_manager import save_file_from_url


class FALTextToImageStep(FALBaseStep):
    """FAL AI text-to-image step implementation."""
    
    def get_model_endpoint(self) -> str:
        """Get the FAL AI text-to-image model endpoint."""
        model = self.config.config.get('model', 'flux-dev')
        
        model_endpoints = {
            'flux-dev': 'fal-ai/flux/dev',
            'flux-schnell': 'fal-ai/flux/schnell',
            'imagen-4': 'fal-ai/imagen-4',
            'seedream-v3': 'fal-ai/seedream-v3'
        }
        
        return model_endpoints.get(model, model_endpoints['flux-dev'])
    
    def prepare_arguments(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare arguments for text-to-image generation."""
        config = self.config.config
        
        arguments = {
            'prompt': config.get('prompt', config.get('text', '')),
            'image_size': config.get('image_size', 'landscape_4_3'),
            'num_inference_steps': config.get('num_inference_steps', 28),
            'guidance_scale': config.get('guidance_scale', 3.5),
            'num_images': config.get('num_images', 1),
            'enable_safety_checker': config.get('enable_safety_checker', True)
        }
        
        # Add negative prompt if specified
        if 'negative_prompt' in config:
            arguments['negative_prompt'] = config['negative_prompt']
        
        # Add seed for reproducibility
        if 'seed' in config:
            arguments['seed'] = config['seed']
        
        return arguments
    
    async def _process_result(self, result: Dict[str, Any], context: Dict[str, Any]) -> Optional[str]:
        """Process FAL AI result and download images."""
        if 'images' not in result or not result['images']:
            raise ValueError("No images generated")
        
        # Get output directory
        output_dir = context.get('output_directory', 'output')
        
        # Download first image (or could download all)
        image_url = result['images'][0]['url']
        filename = self.config.output_filename or f"text_to_image_{int(time.time())}.png"
        
        output_path = await save_file_from_url(image_url, output_dir, filename)
        return output_path
    
    def get_required_config_fields(self) -> list:
        """Get required configuration fields."""
        return ['prompt']
    
    def _calculate_cost(self, arguments: Dict[str, Any]) -> float:
        """Calculate cost based on model and parameters."""
        model = self.config.config.get('model', 'flux-dev')
        num_images = arguments.get('num_images', 1)
        
        # Estimated costs per image (these are approximate)
        costs_per_image = {
            'flux-dev': 0.005,
            'flux-schnell': 0.001,
            'imagen-4': 0.01,
            'seedream-v3': 0.003
        }
        
        cost_per_image = costs_per_image.get(model, 0.005)
        return cost_per_image * num_images
    
    def estimate_cost(self) -> float:
        """Estimate cost for this step."""
        num_images = self.config.config.get('num_images', 1)
        model = self.config.config.get('model', 'flux-dev')
        return self._calculate_cost({'num_images': num_images})


# Register the step
from ai_content_platform.core.step import StepFactory
StepFactory.register_step(StepType.TEXT_TO_IMAGE, FALTextToImageStep)
```

### Step 3.5: FAL AI Text-to-Video Service

Create `ai_content_platform/services/fal_ai/text_to_video.py`:
```python
"""FAL AI text-to-video service implementation."""

import time
from typing import Dict, Any, Optional

from ai_content_platform.services.fal_ai.base import FALBaseStep
from ai_content_platform.core.models import StepType
from ai_content_platform.utils.file_manager import save_file_from_url


class FALTextToVideoStep(FALBaseStep):
    """FAL AI text-to-video step implementation."""
    
    def get_model_endpoint(self) -> str:
        """Get the FAL AI text-to-video model endpoint."""
        model = self.config.config.get('model', 'minimax-hailuo-pro')
        
        model_endpoints = {
            'minimax-hailuo-pro': 'fal-ai/minimax-video-01',
            'google-veo-3': 'fal-ai/google-veo-3',
            'kling-video': 'fal-ai/kling-video/v1.5/pro/text-to-video'
        }
        
        return model_endpoints.get(model, model_endpoints['minimax-hailuo-pro'])
    
    def prepare_arguments(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare arguments for text-to-video generation."""
        config = self.config.config
        model = config.get('model', 'minimax-hailuo-pro')
        
        arguments = {
            'prompt': config.get('prompt', config.get('text', ''))
        }
        
        # Model-specific parameters
        if model == 'minimax-hailuo-pro':
            arguments.update({
                'duration': config.get('duration', 6),
                'aspect_ratio': config.get('aspect_ratio', '16:9'),
                'prompt_optimizer': config.get('prompt_optimizer', True)
            })
        
        elif model == 'google-veo-3':
            arguments.update({
                'duration': config.get('duration', 5),
                'aspect_ratio': config.get('aspect_ratio', '1280:720'),
                'loop': config.get('loop', False)
            })
        
        elif model == 'kling-video':
            arguments.update({
                'duration': config.get('duration', '5'),
                'aspect_ratio': config.get('aspect_ratio', '16:9'),
                'camera_control': config.get('camera_control', {}),
                'cfg_scale': config.get('cfg_scale', 0.5)
            })
        
        return arguments
    
    async def _process_result(self, result: Dict[str, Any], context: Dict[str, Any]) -> Optional[str]:
        """Process FAL AI result and download video."""
        video_url = None
        
        # Different result formats for different models
        if 'video' in result:
            if isinstance(result['video'], dict):
                video_url = result['video'].get('url')
            else:
                video_url = result['video']
        elif 'url' in result:
            video_url = result['url']
        
        if not video_url:
            raise ValueError("No video URL in result")
        
        # Get output directory
        output_dir = context.get('output_directory', 'output')
        
        # Download video
        filename = self.config.output_filename or f"text_to_video_{int(time.time())}.mp4"
        output_path = await save_file_from_url(video_url, output_dir, filename)
        
        return output_path
    
    def get_required_config_fields(self) -> list:
        """Get required configuration fields."""
        return ['prompt']
    
    def _calculate_cost(self, arguments: Dict[str, Any]) -> float:
        """Calculate cost based on model and duration."""
        model = self.config.config.get('model', 'minimax-hailuo-pro')
        duration = arguments.get('duration', 6)
        
        # Estimated costs per second
        costs_per_second = {
            'minimax-hailuo-pro': 0.013,  # ~$0.08 for 6 seconds
            'google-veo-3': 0.50,         # ~$2.50-6.00 range
            'kling-video': 0.008          # ~$0.04 for 5 seconds
        }
        
        cost_per_second = costs_per_second.get(model, 0.013)
        return cost_per_second * duration
    
    def estimate_cost(self) -> float:
        """Estimate cost for this step."""
        duration = self.config.config.get('duration', 6)
        return self._calculate_cost({'duration': duration})


# Register the step
from ai_content_platform.core.step import StepFactory
StepFactory.register_step(StepType.TEXT_TO_VIDEO, FALTextToVideoStep)
```

### Step 3.6: ElevenLabs Text-to-Speech Service

Create `ai_content_platform/services/elevenlabs/tts.py`:
```python
"""ElevenLabs text-to-speech service implementation."""

import os
import time
from typing import Dict, Any, Optional

try:
    import elevenlabs
    from elevenlabs import generate, save
except ImportError:
    elevenlabs = None

from ai_content_platform.core.step import BaseStep
from ai_content_platform.core.models import StepResult, StepType
from ai_content_platform.core.exceptions import APIKeyError, ServiceNotAvailableError
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.utils.file_manager import ensure_directory


logger = get_logger(__name__)


class ElevenLabsTTSStep(BaseStep):
    """ElevenLabs text-to-speech step implementation."""
    
    def __init__(self, config):
        super().__init__(config)
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize ElevenLabs client."""
        if elevenlabs is None:
            raise ServiceNotAvailableError("elevenlabs not installed. Run: pip install elevenlabs")
        
        api_key = os.getenv('ELEVENLABS_API_KEY') or self.config.config.get('api_key')
        if not api_key:
            raise APIKeyError("ELEVENLABS_API_KEY environment variable or api_key in config required")
        
        elevenlabs.set_api_key(api_key)
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute text-to-speech generation."""
        start_time = time.time()
        
        try:
            config = self.config.config
            
            # Get text to convert
            text = config.get('text', '')
            if not text:
                raise ValueError("No text provided for TTS")
            
            # Get voice settings
            voice = config.get('voice', 'Rachel')
            model = config.get('model', 'eleven_monolingual_v1')
            
            # Voice settings
            voice_settings = {
                'stability': config.get('stability', 0.5),
                'similarity_boost': config.get('similarity_boost', 0.5),
                'style': config.get('style', 0.0),
                'use_speaker_boost': config.get('use_speaker_boost', True)
            }
            
            logger.info(f"Generating TTS for text: {text[:50]}...")
            
            # Generate audio
            audio = generate(
                text=text,
                voice=voice,
                model=model,
                voice_settings=elevenlabs.VoiceSettings(**voice_settings)
            )
            
            # Save audio file
            output_dir = context.get('output_directory', 'output')
            ensure_directory(output_dir)
            
            filename = self.config.output_filename or f"tts_{int(time.time())}.mp3"
            output_path = os.path.join(output_dir, filename)
            
            save(audio, output_path)
            
            execution_time = time.time() - start_time
            cost = self._calculate_cost(text)
            
            return self._create_result(
                success=True,
                output_path=output_path,
                metadata={
                    'voice': voice,
                    'model': model,
                    'text_length': len(text),
                    'voice_settings': voice_settings
                },
                execution_time=execution_time,
                cost=cost
            )
            
        except Exception as e:
            logger.error(f"ElevenLabs TTS failed: {e}")
            execution_time = time.time() - start_time
            
            return self._create_result(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def validate_config(self) -> bool:
        """Validate step configuration."""
        if 'text' not in self.config.config:
            logger.error("Missing required config field: text")
            return False
        return True
    
    def _calculate_cost(self, text: str) -> float:
        """Calculate cost based on text length."""
        # ElevenLabs pricing is typically per character
        # This is an estimate - actual pricing may vary
        characters = len(text)
        cost_per_1000_chars = 0.001  # Approximate cost
        return (characters / 1000) * cost_per_1000_chars
    
    def estimate_cost(self) -> float:
        """Estimate cost for this step."""
        text = self.config.config.get('text', '')
        return self._calculate_cost(text)


# Register the step
from ai_content_platform.core.step import StepFactory
StepFactory.register_step(StepType.TEXT_TO_SPEECH, ElevenLabsTTSStep)
```

### Step 3.7: Service Registration Module

Create `ai_content_platform/services/__init__.py`:
```python
"""Service integrations for AI Content Platform."""

# Import all services to register them
from ai_content_platform.services.fal_ai import text_to_image, text_to_video
from ai_content_platform.services.elevenlabs import tts

# Optional imports (with graceful fallback)
try:
    from ai_content_platform.services.fal_ai import image_to_image, video_to_video, avatar
except ImportError:
    pass

try:
    from ai_content_platform.services.google import veo, gemini
except ImportError:
    pass

try:
    from ai_content_platform.services.openrouter import client
except ImportError:
    pass


def get_available_services():
    """Get list of available services."""
    from ai_content_platform.core.step import StepFactory
    return StepFactory.get_available_steps()


def check_service_dependencies():
    """Check which service dependencies are available."""
    dependencies = {}
    
    # Check FAL AI
    try:
        import fal_client
        dependencies['fal_ai'] = True
    except ImportError:
        dependencies['fal_ai'] = False
    
    # Check ElevenLabs
    try:
        import elevenlabs
        dependencies['elevenlabs'] = True
    except ImportError:
        dependencies['elevenlabs'] = False
    
    # Check Google services
    try:
        import google.generativeai
        dependencies['google'] = True
    except ImportError:
        dependencies['google'] = False
    
    return dependencies
```

---

**Part 3 Complete** - This covers:

1. **Parallel Executor** - Thread-based parallel execution with merge strategies
2. **Service Structure** - Organized directory structure for all AI services
3. **FAL AI Base Service** - Abstract base class for all FAL AI integrations
4. **Text-to-Image Service** - Complete FAL AI text-to-image implementation
5. **Text-to-Video Service** - Multi-model text-to-video with cost calculation
6. **ElevenLabs TTS Service** - Professional text-to-speech integration
7. **Service Registration** - Automatic service discovery and dependency checking

The next part will cover utility modules, configuration management, CLI implementation, and packaging setup. Would you like me to continue with Part 4?