"""
FAL AI Avatar Video Generator

This module provides a Python interface for generating talking avatar videos using FAL AI's Avatar models.
The AI Avatar model generates talking avatar videos from images with either text input (with automatic 
text-to-speech conversion) or audio files for lip-sync animation.

Features:
- Single text-to-speech avatar generation (20 voice options)
- Single audio-to-avatar generation (custom audio files)
- Customizable frame count and generation parameters
- Turbo mode for faster generation
- Support for both local and remote images/audio
- Natural lip-sync and facial expressions

API Endpoints: 
- fal-ai/ai-avatar/single-text (text-to-speech)
- fal-ai/ai-avatar (audio-to-avatar)
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
        
        # Model endpoints
        self.text_endpoint = "fal-ai/ai-avatar/single-text"
        self.audio_endpoint = "fal-ai/ai-avatar"
        self.multi_endpoint = "fal-ai/ai-avatar/multi"
        
        print(f"✅ FAL Avatar Generator initialized")
        print(f"📍 Text-to-speech endpoint: {self.text_endpoint}")
        print(f"📍 Audio-to-avatar endpoint: {self.audio_endpoint}")
        print(f"📍 Multi-audio endpoint: {self.multi_endpoint}")
        print(f"🎭 Available voices: {len(VOICE_OPTIONS)} options")
    
    def generate_avatar_video(
        self,
        image_url: str,
        text_input: str,
        voice: VoiceType = "Bill",
        prompt: str = "An elderly man with a white beard and headphones records audio with a microphone. He appears engaged and expressive, suggesting a podcast or voiceover.",
        num_frames: int = 136,
        seed: Optional[int] = 42,
        turbo: bool = True,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a talking avatar video from an image and text
        
        Args:
            image_url (str): URL of the input image or local file path
            text_input (str): The text that the avatar will speak
            voice (VoiceType): Voice to use for speech generation (default: "Bill" - from official example)
            prompt (str): Text prompt to guide video generation (default: official FAL AI example)
            num_frames (int): Number of frames (81-129, default: 136)
            seed (int, optional): Random seed for reproducibility (default: 42 - from official example)
            turbo (bool): Whether to use turbo mode for faster generation (default: True)
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
            
            print(f"🚀 Submitting request to {self.text_endpoint}...")
            
            # Track generation time
            start_time = time.time()
            
            def on_queue_update(update):
                if isinstance(update, fal_client.InProgress):
                    for log in update.logs:
                        print(f"📋 {log['message']}")
            
            # Generate the avatar video
            result = fal_client.subscribe(
                self.text_endpoint,
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
    
    def generate_avatar_from_audio(
        self,
        image_url: str,
        audio_url: str,
        prompt: str = "A person speaking naturally with clear lip-sync and natural expressions.",
        num_frames: int = 145,
        seed: Optional[int] = None,
        turbo: bool = True,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a talking avatar video from an image and audio file
        
        Args:
            image_url (str): URL of the input image or local file path
            audio_url (str): URL of the audio file or local file path
            prompt (str): Text prompt to guide video generation
            num_frames (int): Number of frames (81-129, default: 145)
            seed (int, optional): Random seed for reproducibility
            turbo (bool): Whether to use turbo mode for faster generation
            output_path (str, optional): Path to save the generated video
            
        Returns:
            Dict containing the generated video information and metadata
        """
        try:
            print(f"🎬 Starting avatar video generation from audio...")
            print(f"🖼️ Image: {image_url}")
            print(f"🎵 Audio: {audio_url}")
            print(f"⚡ Turbo mode: {turbo}")
            
            # Handle local image files
            if os.path.isfile(image_url):
                print(f"📤 Uploading local image: {image_url}")
                image_url = fal_client.upload_file(image_url)
                print(f"✅ Image uploaded: {image_url}")
            
            # Handle local audio files
            if os.path.isfile(audio_url):
                print(f"📤 Uploading local audio: {audio_url}")
                audio_url = fal_client.upload_file(audio_url)
                print(f"✅ Audio uploaded: {audio_url}")
            
            # Validate parameters
            if not (81 <= num_frames <= 129):
                raise ValueError(f"num_frames must be between 81 and 129, got {num_frames}")
            
            # Prepare arguments
            arguments = {
                "image_url": image_url,
                "audio_url": audio_url,
                "prompt": prompt,
                "num_frames": num_frames,
                "turbo": turbo
            }
            
            if seed is not None:
                arguments["seed"] = seed
            
            print(f"🚀 Submitting request to {self.audio_endpoint}...")
            
            # Track generation time
            start_time = time.time()
            
            def on_queue_update(update):
                if isinstance(update, fal_client.InProgress):
                    for log in update.logs:
                        print(f"📋 {log['message']}")
            
            # Generate the avatar video
            result = fal_client.subscribe(
                self.audio_endpoint,
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
            print(f"❌ Error generating avatar video from audio: {str(e)}")
            raise
    
    def generate_multi_avatar_conversation(
        self,
        image_url: str,
        first_audio_url: str,
        second_audio_url: str,
        prompt: str = "Two people engaged in a natural conversation, speaking in sequence with clear lip-sync and natural expressions.",
        num_frames: int = 181,
        seed: Optional[int] = None,
        turbo: bool = True,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a multi-person conversation avatar video from an image and two audio files
        
        Args:
            image_url (str): URL of the input image or local file path
            first_audio_url (str): URL of the first person's audio file or local file path
            second_audio_url (str): URL of the second person's audio file or local file path
            prompt (str): Text prompt to guide video generation
            num_frames (int): Number of frames (81-129, default: 181)
            seed (int, optional): Random seed for reproducibility
            turbo (bool): Whether to use turbo mode for faster generation
            output_path (str, optional): Path to save the generated video
            
        Returns:
            Dict containing the generated video information and metadata
        """
        try:
            print(f"🎬 Starting multi-person avatar conversation generation...")
            print(f"🖼️ Image: {image_url}")
            print(f"🎵 First audio: {first_audio_url}")
            print(f"🎵 Second audio: {second_audio_url}")
            print(f"⚡ Turbo mode: {turbo}")
            
            # Handle local image files
            if os.path.isfile(image_url):
                print(f"📤 Uploading local image: {image_url}")
                image_url = fal_client.upload_file(image_url)
                print(f"✅ Image uploaded: {image_url}")
            
            # Handle local audio files
            if os.path.isfile(first_audio_url):
                print(f"📤 Uploading first audio: {first_audio_url}")
                first_audio_url = fal_client.upload_file(first_audio_url)
                print(f"✅ First audio uploaded: {first_audio_url}")
            
            if os.path.isfile(second_audio_url):
                print(f"📤 Uploading second audio: {second_audio_url}")
                second_audio_url = fal_client.upload_file(second_audio_url)
                print(f"✅ Second audio uploaded: {second_audio_url}")
            
            # Validate parameters
            if not (81 <= num_frames <= 129):
                raise ValueError(f"num_frames must be between 81 and 129, got {num_frames}")
            
            # Prepare arguments
            arguments = {
                "image_url": image_url,
                "first_audio_url": first_audio_url,
                "second_audio_url": second_audio_url,
                "prompt": prompt,
                "num_frames": num_frames,
                "turbo": turbo
            }
            
            if seed is not None:
                arguments["seed"] = seed
            
            print(f"🚀 Submitting request to {self.multi_endpoint}...")
            
            # Track generation time
            start_time = time.time()
            
            def on_queue_update(update):
                if isinstance(update, fal_client.InProgress):
                    for log in update.logs:
                        print(f"📋 {log['message']}")
            
            # Generate the multi-avatar conversation video
            result = fal_client.subscribe(
                self.multi_endpoint,
                arguments=arguments,
                with_logs=True,
                on_queue_update=on_queue_update
            )
            
            generation_time = time.time() - start_time
            
            if result and 'video' in result:
                video_info = result['video']
                video_url = video_info['url']
                file_size = video_info.get('file_size', 0)
                
                print(f"✅ Multi-avatar conversation generated successfully!")
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
            print(f"❌ Error generating multi-avatar conversation: {str(e)}")
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
    
    def generate_official_example(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate avatar video using the exact official FAL AI example
        
        This method uses the exact same parameters as shown in the official FAL AI documentation:
        https://fal.ai/models/fal-ai/ai-avatar/single-text/api
        
        Args:
            output_path (str, optional): Path to save the generated video
            
        Returns:
            Dict containing the generated video information and metadata
        """
        print("🎭 Generating avatar video using official FAL AI example...")
        print("📖 Source: https://fal.ai/models/fal-ai/ai-avatar/single-text/api")
        
        return self.generate_avatar_video(
            image_url="https://v3.fal.media/files/panda/HuM21CXMf0q7OO2zbvwhV_c4533aada79a495b90e50e32dc9b83a8.png",
            text_input="Spend more time with people who make you feel alive, and less with things that drain your soul.",
            voice="Bill",
            prompt="An elderly man with a white beard and headphones records audio with a microphone. He appears engaged and expressive, suggesting a podcast or voiceover.",
            num_frames=136,
            seed=42,
            turbo=True,
            output_path=output_path
        )
    
    def test_connection(self) -> bool:
        """Test connection to FAL AI API"""
        try:
            print("🔍 Testing FAL AI connection...")
            
            # Try to get account info or make a simple request
            # This is a simple way to test if the API key is valid
            test_result = fal_client.submit(
                self.text_endpoint,
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
        voices = generator.get_available_voices()
        for i, voice in enumerate(voices, 1):
            # Highlight Bill as the official example voice
            if voice == "Bill":
                print(f"  {i:2d}. {voice} ⭐ (official example)")
            else:
                print(f"  {i:2d}. {voice}")
        
        print(f"\nTotal: {len(voices)} voices available")
        
        print(f"\n📋 Official FAL AI Example Available:")
        print(f"   - Image: Official FAL AI example image")
        print(f"   - Text: 'Spend more time with people who make you feel alive...'")
        print(f"   - Voice: Bill (official example)")
        print(f"   - Prompt: Podcast-style generation")
        print(f"   - Use: generator.generate_official_example()")
        print(f"   - Source: https://fal.ai/models/fal-ai/ai-avatar/single-text/api")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 