"""FAL AI service integrations."""

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, Optional, Union

import fal_client
import aiohttp
import aiofiles

from ai_content_platform.core.step import BaseStep
from ai_content_platform.core.models import StepConfig, StepResult, StepType
from ai_content_platform.core.exceptions import StepExecutionError
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.utils.file_manager import FileManager


class BaseFALStep(BaseStep):
    """Base class for FAL AI steps."""
    
    def __init__(self, config: StepConfig):
        super().__init__(config)
        self.logger = get_logger(__name__)
        self.file_manager = FileManager()
        
        # Initialize FAL client
        api_key = self.config.parameters.get("api_key") or self._get_api_key_from_env()
        if api_key:
            fal_client.api_key = api_key
        else:
            raise StepExecutionError("FAL AI API key not found")
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables."""
        import os
        return os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY")
    
    def validate_config(self) -> bool:
        """Validate FAL AI step configuration."""
        required_params = self._get_required_parameters()
        
        for param in required_params:
            if param not in self.config.parameters:
                self.logger.error(f"Missing required parameter: {param}")
                return False
        
        return True
    
    def _get_required_parameters(self) -> list:
        """Get list of required parameters for this step type."""
        return []  # Override in subclasses
    
    async def _download_result(self, result_url: str, output_dir: Path) -> Path:
        """Download result file from URL."""
        try:
            filename = f"{self.config.name}_{int(time.time())}.{self._get_file_extension()}"
            return await self.file_manager.download_file(
                result_url, 
                output_dir, 
                filename
            )
        except Exception as e:
            raise StepExecutionError(f"Failed to download result: {str(e)}") from e
    
    def _get_file_extension(self) -> str:
        """Get expected file extension for this step type."""
        return "bin"  # Override in subclasses


class FALTextToImageStep(BaseFALStep):
    """FAL AI text-to-image generation step."""
    
    def _get_required_parameters(self) -> list:
        return ["prompt"]
    
    def _get_file_extension(self) -> str:
        return "png"
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute text-to-image generation."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating image: {self.config.name}")
            
            # Get parameters
            params = self.config.parameters.copy()
            prompt = params.pop("prompt")
            model = params.pop("model", "flux-1-dev")
            
            # Map model to FAL endpoint
            model_endpoints = {
                "imagen-4": "fal-ai/imagen-4",
                "seedream-v3": "fal-ai/seedream-v3", 
                "flux-1-schnell": "fal-ai/flux/schnell",
                "flux-1-dev": "fal-ai/flux/dev"
            }
            
            endpoint = model_endpoints.get(model, "fal-ai/flux/dev")
            
            # Prepare request
            request_data = {
                "prompt": prompt,
                **params
            }
            
            # Submit request
            self.logger.info(f"Submitting to FAL AI: {endpoint}")
            result = await asyncio.to_thread(
                fal_client.subscribe,
                endpoint,
                arguments=request_data
            )
            
            # Download result
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            image_url = result["images"][0]["url"]
            output_path = await self._download_result(image_url, output_dir)
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "model": model,
                    "prompt": prompt,
                    "image_url": image_url,
                    "width": result.get("width"),
                    "height": result.get("height")
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"Text-to-image generation failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    def estimate_cost(self) -> float:
        """Estimate cost for text-to-image generation."""
        model = self.config.parameters.get("model", "flux-1-dev")
        cost_map = {
            "imagen-4": 0.005,
            "seedream-v3": 0.003,
            "flux-1-schnell": 0.001,
            "flux-1-dev": 0.002
        }
        return cost_map.get(model, 0.002)


class FALImageToImageStep(BaseFALStep):
    """FAL AI image-to-image generation step."""
    
    def _get_required_parameters(self) -> list:
        return ["image_url", "prompt"]
    
    def _get_file_extension(self) -> str:
        return "png"
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute image-to-image generation."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating image-to-image: {self.config.name}")
            
            # Get parameters
            params = self.config.parameters.copy()
            image_url = params.pop("image_url")
            prompt = params.pop("prompt")
            
            # Prepare request
            request_data = {
                "image_url": image_url,
                "prompt": prompt,
                "strength": params.get("strength", 0.8),
                **params
            }
            
            # Submit request
            result = await asyncio.to_thread(
                fal_client.subscribe,
                "fal-ai/luma-photon-flash",
                arguments=request_data
            )
            
            # Download result
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_image_url = result["image"]["url"]
            output_path = await self._download_result(output_image_url, output_dir)
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "prompt": prompt,
                    "input_image_url": image_url,
                    "output_image_url": output_image_url,
                    "strength": request_data.get("strength")
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"Image-to-image generation failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    def estimate_cost(self) -> float:
        """Estimate cost for image-to-image generation."""
        return 0.01


class FALTextToVideoStep(BaseFALStep):
    """FAL AI text-to-video generation step."""
    
    def _get_required_parameters(self) -> list:
        return ["prompt"]
    
    def _get_file_extension(self) -> str:
        return "mp4"
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute text-to-video generation."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating video: {self.config.name}")
            
            # Get parameters
            params = self.config.parameters.copy()
            prompt = params.pop("prompt")
            model = params.pop("model", "minimax-hailuo-02-pro")
            
            # Map model to FAL endpoint
            model_endpoints = {
                "minimax-hailuo-02-pro": "fal-ai/minimax-hailuo-02-pro",
                "google-veo-3": "fal-ai/google-veo-3"
            }
            
            endpoint = model_endpoints.get(model, "fal-ai/minimax-hailuo-02-pro")
            
            # Prepare request
            request_data = {
                "prompt": prompt,
                **params
            }
            
            # Submit request
            self.logger.info(f"Submitting to FAL AI: {endpoint}")
            result = await asyncio.to_thread(
                fal_client.subscribe,
                endpoint,
                arguments=request_data
            )
            
            # Download result
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            video_url = result["video"]["url"]
            output_path = await self._download_result(video_url, output_dir)
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "model": model,
                    "prompt": prompt,
                    "video_url": video_url,
                    "duration": result.get("duration"),
                    "resolution": result.get("resolution")
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"Text-to-video generation failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    def estimate_cost(self) -> float:
        """Estimate cost for text-to-video generation."""
        model = self.config.parameters.get("model", "minimax-hailuo-02-pro")
        cost_map = {
            "minimax-hailuo-02-pro": 0.08,
            "google-veo-3": 4.0
        }
        return cost_map.get(model, 0.08)


class FALVideoGenerationStep(BaseFALStep):
    """FAL AI video generation step (MiniMax/Kling models)."""
    
    def _get_required_parameters(self) -> list:
        return ["prompt"]
    
    def _get_file_extension(self) -> str:
        return "mp4"
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute video generation."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating video: {self.config.name}")
            
            # Get parameters
            params = self.config.parameters.copy()
            prompt = params.pop("prompt")
            model = params.pop("model", "minimax-hailuo-02")
            
            # Map model to FAL endpoint
            model_endpoints = {
                "minimax-hailuo-02": "fal-ai/minimax-hailuo-02",
                "kling-video-2-1": "fal-ai/kling-video-2-1"
            }
            
            endpoint = model_endpoints.get(model, "fal-ai/minimax-hailuo-02")
            
            # Prepare request
            request_data = {
                "prompt": prompt,
                **params
            }
            
            # Submit request
            result = await asyncio.to_thread(
                fal_client.subscribe,
                endpoint,
                arguments=request_data
            )
            
            # Download result
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            video_url = result["video"]["url"]
            output_path = await self._download_result(video_url, output_dir)
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "model": model,
                    "prompt": prompt,
                    "video_url": video_url
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"Video generation failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    def estimate_cost(self) -> float:
        """Estimate cost for video generation."""
        model = self.config.parameters.get("model", "minimax-hailuo-02")
        cost_map = {
            "minimax-hailuo-02": 0.05,
            "kling-video-2-1": 0.07
        }
        return cost_map.get(model, 0.06)


class FALAvatarGenerationStep(BaseFALStep):
    """FAL AI avatar generation step."""
    
    def _get_required_parameters(self) -> list:
        return ["image_url"]
    
    def _get_file_extension(self) -> str:
        return "mp4"
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute avatar generation."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating avatar: {self.config.name}")
            
            # Get parameters
            params = self.config.parameters.copy()
            image_url = params.pop("image_url")
            
            # Check if we have text or audio
            if "text" in params:
                # Text-to-speech avatar
                endpoint = "fal-ai/avatar-text-to-speech"
                request_data = {
                    "image_url": image_url,
                    "text": params["text"],
                    **{k: v for k, v in params.items() if k not in ["text", "image_url"]}
                }
            elif "audio_url" in params:
                # Audio-to-avatar
                endpoint = "fal-ai/avatar-audio-to-avatar"
                request_data = {
                    "image_url": image_url,
                    "audio_url": params["audio_url"],
                    **{k: v for k, v in params.items() if k not in ["audio_url", "image_url"]}
                }
            else:
                raise StepExecutionError("Avatar step requires either 'text' or 'audio_url'")
            
            # Submit request
            result = await asyncio.to_thread(
                fal_client.subscribe,
                endpoint,
                arguments=request_data
            )
            
            # Download result
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            video_url = result["video"]["url"]
            output_path = await self._download_result(video_url, output_dir)
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "image_url": image_url,
                    "video_url": video_url,
                    "endpoint": endpoint,
                    **request_data
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"Avatar generation failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    def estimate_cost(self) -> float:
        """Estimate cost for avatar generation."""
        if "text" in self.config.parameters:
            return 0.02  # Text-to-speech
        else:
            return 0.03  # Audio-to-avatar