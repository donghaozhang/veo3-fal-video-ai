"""
Main generator class for FAL Video to Video
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path
import fal_client
from dotenv import load_dotenv

from .models.thinksound import ThinkSoundModel
from .utils.validators import validate_model, validate_video_url, validate_video_path
from .utils.file_utils import upload_video, get_video_info
from .config.constants import SUPPORTED_MODELS, MODEL_DISPLAY_NAMES


class FALVideoToVideoGenerator:
    """
    Main interface for FAL Video to Video generation.
    
    This class provides methods to generate audio for videos using various
    FAL AI models like ThinkSound.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the generator.
        
        Args:
            api_key: Optional FAL API key. If not provided, will look for FAL_KEY env var.
        """
        # Load environment variables
        load_dotenv()
        
        # Set API key
        self.api_key = api_key or os.getenv("FAL_KEY")
        if not self.api_key:
            raise ValueError(
                "FAL API key not found. Please provide api_key or set FAL_KEY environment variable."
            )
        
        fal_client.api_key = self.api_key
        
        # Initialize models
        self.models = {
            "thinksound": ThinkSoundModel()
        }
        
        print("✅ FAL Video to Video Generator initialized")
    
    def add_audio_to_video(
        self,
        video_url: str,
        model: str = "thinksound",
        prompt: Optional[str] = None,
        seed: Optional[int] = None,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Add AI-generated audio to a video using URL input.
        
        Args:
            video_url: URL of the input video
            model: Model to use (default: "thinksound")
            prompt: Optional text prompt to guide audio generation
            seed: Optional random seed for reproducibility
            output_dir: Custom output directory
            **kwargs: Additional model-specific parameters
            
        Returns:
            Dictionary containing:
                - success: Whether generation was successful
                - model: Model used
                - local_path: Path to downloaded video with audio
                - response: Full API response
                - processing_time: Time taken for generation
        """
        # Validate inputs
        model = validate_model(model)
        video_url = validate_video_url(video_url)
        
        # Get model instance
        model_instance = self.models[model]
        
        # Prepare parameters
        params = {
            "prompt": prompt,
            "seed": seed,
            **kwargs
        }
        
        # Generate audio
        return model_instance.generate(
            video_url=video_url,
            output_dir=output_dir,
            **params
        )
    
    def add_audio_to_local_video(
        self,
        video_path: str,
        model: str = "thinksound",
        prompt: Optional[str] = None,
        seed: Optional[int] = None,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Add AI-generated audio to a local video file.
        
        Args:
            video_path: Path to local video file
            model: Model to use (default: "thinksound")
            prompt: Optional text prompt to guide audio generation
            seed: Optional random seed for reproducibility
            output_dir: Custom output directory
            **kwargs: Additional model-specific parameters
            
        Returns:
            Dictionary containing generation results
        """
        # Validate inputs
        model = validate_model(model)
        video_path = validate_video_path(video_path)
        
        # Get video info
        video_info = get_video_info(video_path)
        if video_info:
            print(f"📹 Video info:")
            print(f"   Duration: {video_info.get('duration', 'Unknown')}s")
            print(f"   Resolution: {video_info.get('width', '?')}x{video_info.get('height', '?')}")
            print(f"   Has audio: {'Yes' if video_info.get('has_audio') else 'No'}")
        
        # Upload video
        video_url = upload_video(video_path)
        
        # Generate audio
        return self.add_audio_to_video(
            video_url=video_url,
            model=model,
            prompt=prompt,
            seed=seed,
            output_dir=output_dir,
            **kwargs
        )
    
    def get_model_info(self, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about available models.
        
        Args:
            model: Specific model to get info for. If None, returns info for all models.
            
        Returns:
            Dictionary containing model information
        """
        if model:
            model = validate_model(model)
            return self.models[model].get_model_info()
        else:
            # Return info for all models
            return {
                model_key: model_instance.get_model_info()
                for model_key, model_instance in self.models.items()
            }
    
    def list_models(self) -> list:
        """
        List all available models.
        
        Returns:
            List of available model names
        """
        return SUPPORTED_MODELS
    
    def __repr__(self) -> str:
        """String representation of the generator."""
        return f"FALVideoToVideoGenerator(models={self.list_models()})"