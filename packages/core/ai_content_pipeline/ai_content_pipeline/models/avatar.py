"""Avatar generation models for AI Content Pipeline."""

import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

# Add avatar package to path
avatar_path = Path(__file__).parent.parent.parent.parent.parent / "providers" / "fal" / "avatar"
if str(avatar_path) not in sys.path:
    sys.path.append(str(avatar_path))

from ..utils.file_manager import FileManager
from .base import BaseContentModel, ModelResult


class ReplicateMultiTalkGenerator(BaseContentModel):
    """Replicate MultiTalk generator for multi-person conversational videos."""
    
    def __init__(self, file_manager: Optional[FileManager] = None, **kwargs):
        """Initialize the MultiTalk generator."""
        super().__init__("avatar")  # Call parent with model_type
        self.file_manager = file_manager
        self.generator = None
        self._initialize_generator()
    
    def _initialize_generator(self):
        """Initialize the Replicate MultiTalk generator."""
        try:
            from replicate_multitalk_generator import ReplicateMultiTalkGenerator as MultiTalkGen
            self.generator = MultiTalkGen()
            print("✅ Replicate MultiTalk generator initialized")
        except ImportError as e:
            print(f"❌ Failed to initialize MultiTalk: {e}")
            print("💡 Make sure replicate is installed: pip install replicate")
        except Exception as e:
            print(f"❌ Error initializing MultiTalk: {e}")
    
    def generate(self, input_data: Any = None, model: str = "multitalk", **kwargs) -> ModelResult:
        """Generate a multi-person conversational video.
        
        Args:
            image: URL or path to image containing person(s)
            first_audio: URL or path to first audio file
            second_audio: Optional URL or path to second audio file
            prompt: Text description of the scene
            num_frames: Number of frames (25-201, default 81)
            turbo: Enable turbo mode (default True)
            sampling_steps: Enhancement iterations (2-100, default 40)
            
        Returns:
            ModelResult with video URL and metadata
        """
        self._start_timing()  # Start timing
        
        if not self.generator:
            return self._create_error_result(model, "MultiTalk generator not initialized")
        
        try:
            # Map parameters to generator format
            image_url = kwargs.get('image', kwargs.get('image_url'))
            first_audio = kwargs.get('first_audio', kwargs.get('first_audio_url'))
            second_audio = kwargs.get('second_audio', kwargs.get('second_audio_url'))
            
            if not image_url or not first_audio:
                return self._create_error_result(model, "Missing required parameters: image and first_audio")
            
            # Generate the video
            print("🔄 Calling Replicate MultiTalk API (this will take several minutes)...")
            if second_audio:
                print("💬 Generating multi-person conversation video...")
                result = self.generator.generate_conversation_video(
                    image_url=image_url,
                    first_audio_url=first_audio,
                    second_audio_url=second_audio,
                    prompt=kwargs.get('prompt', 'A natural conversation'),
                    num_frames=kwargs.get('num_frames', 81),
                    turbo=kwargs.get('turbo', True),
                    sampling_steps=kwargs.get('sampling_steps', 40),
                    seed=kwargs.get('seed')
                )
            else:
                print("👤 Generating single-person speaking video...")
                result = self.generator.generate_single_person_video(
                    image_url=image_url,
                    audio_url=first_audio,
                    prompt=kwargs.get('prompt', 'A person speaking naturally'),
                    num_frames=kwargs.get('num_frames', 81),
                    turbo=kwargs.get('turbo', True),
                    sampling_steps=kwargs.get('sampling_steps', 40),
                    seed=kwargs.get('seed')
                )
            
            print("🎥 Video generation completed, processing result...")
            
            # Extract video URL
            video_url = result.get('video', {}).get('url')
            if not video_url:
                return self._create_error_result(model, "No video URL in result")
            
            # Download video if file manager available
            output_path = None
            if self.file_manager:
                import time
                timestamp = int(time.time())
                filename = f"multitalk_conversation_{timestamp}.mp4"
                output_path = self.file_manager.create_output_path(filename)
                print(f"📥 Downloading video to: {output_path}")
                self._download_file(video_url, output_path)
                print(f"✅ Video saved locally: {output_path}")
            else:
                print(f"🔗 Video available at: {video_url}")
            
            return self._create_success_result(
                model=model,
                output_path=output_path,
                output_url=video_url,
                metadata={
                    'model': 'replicate/multitalk',
                    'generation_time': result.get('generation_time', 0),
                    'parameters': result.get('parameters', {}),
                    'type': 'conversational_video',
                    'people_count': 2 if second_audio else 1
                }
            )
            
        except Exception as e:
            return self._create_error_result(model, f"MultiTalk generation failed: {str(e)}")
    
    def _download_file(self, url: str, output_path: str):
        """Download file from URL."""
        try:
            import requests
            response = requests.get(url)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
        except Exception as e:
            print(f"Warning: Failed to download video: {e}")
    
    def estimate_cost(self, model: str, **kwargs) -> float:
        """Estimate cost for MultiTalk generation."""
        # MultiTalk cost varies by processing time, provide rough estimate
        return 1.0  # $1.00 average estimate
    
    def get_available_models(self) -> list:
        """Get available MultiTalk models."""
        return ["multitalk"]
    
    def validate_input(self, input_data: Any, model: str, **kwargs) -> bool:
        """Validate input parameters."""
        required = ['image']
        has_audio = any(kwargs.get(key) for key in ['first_audio', 'audio', 'first_audio_url', 'audio_url'])
        
        if not has_audio:
            return False
            
        return all(kwargs.get(key) for key in required)