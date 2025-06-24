"""
FAL AI Avatar Video Generator

This module provides a Python interface for generating talking avatar videos using FAL AI's Avatar models.
The AI Avatar model generates talking avatar videos from an image and text input, with automatic 
text-to-speech conversion and lip-sync animation.

Features:
- Single text-to-speech avatar generation
- Multiple voice options (20 different voices)
- Customizable frame count and generation parameters
- Turbo mode for faster generation
- Support for both local and remote images

API Endpoint: fal-ai/ai-avatar/single-text
"""

import os
import time
import fal_client
from typing import Optional, Dict, Any, Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Voice options available for the avatar
VOICE_OPTIONS = [
    "Aria", "Roger", "Sarah", "Laura", "Charlie", "George", "Callum", 
    "River", "Liam", "Charlotte", "Alice", "Matilda", "Will", "Jessica", 
    "Eric", "Chris", "Brian", "Daniel", "Lily", "Bill"
]

VoiceType = Literal[
    "Aria", "Roger", "Sarah", "Laura", "Charlie", "George", "Callum", 
    "River", "Liam", "Charlotte", "Alice", "Matilda", "Will", "Jessica", 
    "Eric", "Chris", "Brian", "Daniel", "Lily", "Bill"
]

class FALAvatarGenerator:
    """
    FAL AI Avatar Video Generator
    
    This class provides methods to generate talking avatar videos from images and text
    using FAL AI's Avatar models.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FAL Avatar Generator
        
        Args:
            api_key (str, optional): FAL AI API key. If not provided, will look for FAL_KEY environment variable.
        """
        self.api_key = api_key or os.getenv('FAL_KEY')
        if not self.api_key:
            raise ValueError("FAL_KEY environment variable not set or api_key not provided")
        
        # Set the API key for fal_client
        os.environ['FAL_KEY'] = self.api_key
        
        # Model endpoint
        self.model_endpoint = "fal-ai/ai-avatar/single-text"
        
        print(f"✅ FAL Avatar Generator initialized")
        print(f"📍 Model endpoint: {self.model_endpoint}")
        print(f"🎭 Available voices: {len(VOICE_OPTIONS)} options")
    
    def generate_avatar_video(
        self,
        image_url: str,
        text_input: str,
        voice: VoiceType = "Sarah",
        prompt: str = "A person speaking naturally with clear lip-sync and natural expressions.",
        num_frames: int = 136,
        seed: Optional[int] = None,
        turbo: bool = True,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a talking avatar video from an image and text
        
        Args:
            image_url (str): URL of the input image or local file path
            text_input (str): The text that the avatar will speak
            voice (VoiceType): Voice to use for speech generation (default: "Sarah")
            prompt (str): Text prompt to guide video generation
            num_frames (int): Number of frames (81-129, default: 136)
            seed (int, optional): Random seed for reproducibility
            turbo (bool): Whether to use turbo mode for faster generation
            output_path (str, optional): Path to save the generated video
            
        Returns:
            Dict containing the generated video information and metadata
        """
        try:
            print(f"🎬 Starting avatar video generation...")
            print(f"📝 Text: {text_input[:50]}{'...' if len(text_input) > 50 else ''}")
            print(f"🎤 Voice: {voice}")
            print(f"🖼️ Image: {image_url}")
            print(f"⚡ Turbo mode: {turbo}")
            
            # Handle local image files
            if os.path.isfile(image_url):
                print(f"📤 Uploading local image: {image_url}")
                image_url = fal_client.upload_file(image_url)
                print(f"✅ Image uploaded: {image_url}")
            
            # Validate parameters
            if voice not in VOICE_OPTIONS:
                raise ValueError(f"Invalid voice '{voice}'. Must be one of: {VOICE_OPTIONS}")
            
            if not (81 <= num_frames <= 129):
                raise ValueError(f"num_frames must be between 81 and 129, got {num_frames}")
            
            # Prepare arguments
            arguments = {
                "image_url": image_url,
                "text_input": text_input,
                "voice": voice,
                "prompt": prompt,
                "num_frames": num_frames,
                "turbo": turbo
            }
            
            if seed is not None:
                arguments["seed"] = seed
            
            print(f"🚀 Submitting request to {self.model_endpoint}...")
            
            # Track generation time
            start_time = time.time()
            
            def on_queue_update(update):
                if isinstance(update, fal_client.InProgress):
                    for log in update.logs:
                        print(f"📋 {log['message']}")
            
            # Generate the avatar video
            result = fal_client.subscribe(
                self.model_endpoint,
                arguments=arguments,
                with_logs=True,
                on_queue_update=on_queue_update
            )
            
            generation_time = time.time() - start_time
            
            if result and 'video' in result:
                video_info = result['video']
                video_url = video_info['url']
                file_size = video_info.get('file_size', 0)
                
                print(f"✅ Avatar video generated successfully!")
                print(f"⏱️ Generation time: {generation_time:.2f} seconds")
                print(f"📊 File size: {file_size / (1024*1024):.2f} MB")
                print(f"🔗 Video URL: {video_url}")
                
                # Download video if output path specified
                if output_path:
                    self._download_video(video_url, output_path)
                
                # Add metadata to result
                result['generation_time'] = generation_time
                result['parameters'] = arguments
                
                return result
            else:
                raise Exception(f"Unexpected result format: {result}")
                
        except Exception as e:
            print(f"❌ Error generating avatar video: {str(e)}")
            raise
    
    def _download_video(self, video_url: str, output_path: str) -> None:
        """Download video from URL to local path"""
        try:
            import requests
            
            print(f"📥 Downloading video to {output_path}...")
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            response = requests.get(video_url)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(output_path)
            print(f"✅ Video downloaded: {output_path} ({file_size / (1024*1024):.2f} MB)")
            
        except Exception as e:
            print(f"❌ Error downloading video: {str(e)}")
            raise
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        return VOICE_OPTIONS.copy()
    
    def test_connection(self) -> bool:
        """Test connection to FAL AI API"""
        try:
            print("🔍 Testing FAL AI connection...")
            
            # Try to get account info or make a simple request
            # This is a simple way to test if the API key is valid
            test_result = fal_client.submit(
                self.model_endpoint,
                arguments={
                    "image_url": "https://via.placeholder.com/512x512/000000/FFFFFF?text=Test",
                    "text_input": "Test",
                    "voice": "Sarah",
                    "prompt": "Test prompt"
                }
            )
            
            if test_result:
                print("✅ FAL AI connection successful")
                return True
            else:
                print("❌ FAL AI connection failed")
                return False
                
        except Exception as e:
            print(f"❌ FAL AI connection test failed: {str(e)}")
            return False

def main():
    """Example usage of the FAL Avatar Generator"""
    try:
        # Initialize generator
        generator = FALAvatarGenerator()
        
        # Test connection
        if not generator.test_connection():
            print("❌ Connection test failed. Please check your API key.")
            return
        
        print("\n🎭 Available voices:")
        for i, voice in enumerate(generator.get_available_voices(), 1):
            print(f"  {i:2d}. {voice}")
        
        print(f"\n📋 Avatar Generation Example:")
        print(f"   - Uses placeholder image")
        print(f"   - Sample text with Sarah voice")
        print(f"   - Turbo mode enabled")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 