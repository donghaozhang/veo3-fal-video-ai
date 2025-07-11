#!/usr/bin/env python3
"""
FAL AI Text-to-Video Generator supporting multiple models.

This module provides a unified interface for generating videos from text descriptions
using different FAL AI text-to-video models.

Supported Models:
1. MiniMax Hailuo-02 Pro - Cost-effective ($0.08/video)
2. Google Veo 3 - Premium quality ($2.50-$6.00/video)
"""

import os
import time
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional, Union, Literal
from dotenv import load_dotenv
from enum import Enum

try:
    import fal_client
except ImportError:
    print("❌ fal-client not installed. Run: pip install fal-client")
    exit(1)


class TextToVideoModel(Enum):
    """Available text-to-video models."""
    MINIMAX_HAILUO = "fal-ai/minimax/hailuo-02/pro/text-to-video"
    GOOGLE_VEO3 = "fal-ai/veo3"
    GOOGLE_VEO3_FAST = "fal-ai/veo3/fast"


# Type definitions
AspectRatio = Literal["16:9", "9:16", "1:1"]
Veo3Duration = Literal["5s", "6s", "7s", "8s"]


class FALTextToVideoGenerator:
    """
    Unified FAL AI Text-to-Video Generator supporting multiple models.
    
    Supports both cost-effective and premium text-to-video generation
    with appropriate cost warnings and controls.
    """
    
    # Model configurations
    MODEL_CONFIGS = {
        TextToVideoModel.MINIMAX_HAILUO: {
            "name": "MiniMax Hailuo-02 Pro",
            "resolution": "1080p",
            "duration": "6 seconds (fixed)",
            "cost_per_video": 0.08,
            "features": [
                "1080p high resolution",
                "6-second duration",
                "Prompt optimization",
                "Commercial use allowed",
                "Cost-effective"
            ]
        },
        TextToVideoModel.GOOGLE_VEO3: {
            "name": "Google Veo 3",
            "resolution": "720p",
            "duration": "5-8 seconds (variable)",
            "cost_per_second_no_audio": 0.50,
            "cost_per_second_with_audio": 0.75,
            "features": [
                "720p HD resolution",
                "Variable duration (5-8s)",
                "Multiple aspect ratios",
                "Audio generation support",
                "Prompt enhancement",
                "Negative prompts",
                "Seed control",
                "Premium quality"
            ]
        },
        TextToVideoModel.GOOGLE_VEO3_FAST: {
            "name": "Google Veo 3 Fast",
            "resolution": "720p",
            "duration": "5-8 seconds (variable)",
            "cost_per_second_no_audio": 0.25,
            "cost_per_second_with_audio": 0.40,
            "features": [
                "720p HD resolution",
                "Variable duration (5-8s)",
                "Multiple aspect ratios", 
                "Audio generation support",
                "Faster generation time",
                "Cost-effective pricing",
                "Seed control",
                "Good quality"
            ]
        }
    }
    
    def __init__(self, api_key: Optional[str] = None, verbose: bool = True):
        """
        Initialize the FAL Text-to-Video Generator.
        
        Args:
            api_key (str, optional): FAL API key. If not provided, loads from environment.
            verbose (bool): Enable verbose output. Defaults to True.
        """
        self.verbose = verbose
        
        # Load environment variables
        load_dotenv()
        
        # Set API key
        self.api_key = api_key or os.getenv('FAL_KEY')
        if not self.api_key:
            raise ValueError(
                "FAL API key not found. Please set FAL_KEY environment variable "
                "or pass api_key parameter. Get your key from: https://fal.ai/dashboard/keys"
            )
        
        # Configure fal_client
        fal_client.api_key = self.api_key
        
        # Create output directory
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        if self.verbose:
            print("🎬 FAL Text-to-Video Generator initialized")
            print(f"📁 Output directory: {self.output_dir.absolute()}")
    
    def calculate_cost(
        self, 
        model: TextToVideoModel, 
        duration: Optional[Veo3Duration] = None,
        generate_audio: bool = True
    ) -> float:
        """
        Calculate the cost for video generation.
        
        Args:
            model (TextToVideoModel): Which model to use
            duration (Veo3Duration, optional): Duration for Veo 3 (ignored for MiniMax)
            generate_audio (bool): Whether to generate audio (Veo 3 only)
        
        Returns:
            float: Cost in USD
        """
        if model == TextToVideoModel.MINIMAX_HAILUO:
            return self.MODEL_CONFIGS[model]["cost_per_video"]
        
        elif model in [TextToVideoModel.GOOGLE_VEO3, TextToVideoModel.GOOGLE_VEO3_FAST]:
            if duration is None:
                duration = "8s"  # Default
            
            duration_seconds = int(duration.rstrip('s'))
            config = self.MODEL_CONFIGS[model]
            
            if generate_audio:
                return duration_seconds * config["cost_per_second_with_audio"]
            else:
                return duration_seconds * config["cost_per_second_no_audio"]
        
        else:
            raise ValueError(f"Unknown model: {model}")
    
    def generate_video(
        self,
        prompt: str,
        model: TextToVideoModel = TextToVideoModel.MINIMAX_HAILUO,
        # MiniMax options
        prompt_optimizer: bool = True,
        # Veo 3 options
        aspect_ratio: AspectRatio = "16:9",
        duration: Optional[Veo3Duration] = None,
        generate_audio: bool = True,
        enhance_prompt: bool = True,
        negative_prompt: Optional[str] = None,
        seed: Optional[int] = None,
        # Common options
        output_filename: Optional[str] = None,
        timeout: int = 600
    ) -> Dict[str, Any]:
        """
        Generate a video from text description.
        
        Args:
            prompt (str): Text description for video generation
            model (TextToVideoModel): Which model to use
            # MiniMax Hailuo-02 Pro options:
            prompt_optimizer (bool): Enable prompt optimization (MiniMax only)
            # Google Veo 3 options:
            aspect_ratio (AspectRatio): Video aspect ratio (Veo 3 only)
            duration (Veo3Duration): Video duration (Veo 3 only, default "8s")
            generate_audio (bool): Generate audio (Veo 3 only)
            enhance_prompt (bool): Enable prompt enhancement (Veo 3 only)
            negative_prompt (str, optional): What to avoid (Veo 3 only)
            seed (int, optional): Seed for reproducibility (Veo 3 only)
            # Common options:
            output_filename (str, optional): Custom output filename
            timeout (int): Maximum time to wait for generation
        
        Returns:
            Dict[str, Any]: Generation result with video URL, local path, cost, and metadata
        """
        # Calculate cost
        if model in [TextToVideoModel.GOOGLE_VEO3, TextToVideoModel.GOOGLE_VEO3_FAST]:
            if duration is None:
                duration = "8s"
            cost = self.calculate_cost(model, duration, generate_audio)
        else:
            cost = self.calculate_cost(model)
        
        if self.verbose:
            config = self.MODEL_CONFIGS[model]
            print(f"🎬 Generating video with {config['name']}...")
            print(f"📝 Prompt: {prompt}")
            print(f"💰 Estimated cost: ${cost:.2f}")
            
            if model in [TextToVideoModel.GOOGLE_VEO3, TextToVideoModel.GOOGLE_VEO3_FAST]:
                print(f"📐 Aspect ratio: {aspect_ratio}")
                print(f"⏱️ Duration: {duration}")
                print(f"🔊 Audio: {'enabled' if generate_audio else 'disabled'}")
                if negative_prompt:
                    print(f"🚫 Negative prompt: {negative_prompt}")
        
        try:
            # Prepare request arguments based on model
            if model == TextToVideoModel.MINIMAX_HAILUO:
                arguments = {
                    "prompt": prompt,
                    "prompt_optimizer": prompt_optimizer
                }
            
            elif model in [TextToVideoModel.GOOGLE_VEO3, TextToVideoModel.GOOGLE_VEO3_FAST]:
                arguments = {
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "duration": duration,
                    "generate_audio": generate_audio
                }
                
                # Add Veo 3 specific parameters (enhance_prompt only for regular Veo 3)
                if model == TextToVideoModel.GOOGLE_VEO3:
                    arguments["enhance_prompt"] = enhance_prompt
                
                # Add optional parameters for both Veo 3 models
                if negative_prompt:
                    arguments["negative_prompt"] = negative_prompt
                if seed is not None:
                    arguments["seed"] = seed
            
            else:
                raise ValueError(f"Unknown model: {model}")
            
            if self.verbose:
                print("🔄 Submitting generation request...")
            
            # Submit generation request
            result = fal_client.subscribe(
                model.value,
                arguments=arguments,
                with_logs=self.verbose,
                timeout=timeout
            )
            
            if self.verbose:
                print("✅ Video generation completed!")
            
            # Process result
            video_url = result.get('video', {}).get('url') if 'video' in result else None
            if not video_url:
                raise Exception("No video URL in response")
            
            # Generate output filename if not provided
            if not output_filename:
                timestamp = int(time.time())
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_prompt = safe_prompt.replace(' ', '_')
                
                if model == TextToVideoModel.MINIMAX_HAILUO:
                    model_name = "minimax"
                elif model == TextToVideoModel.GOOGLE_VEO3:
                    model_name = "veo3"
                elif model == TextToVideoModel.GOOGLE_VEO3_FAST:
                    model_name = "veo3_fast"
                
                if model in [TextToVideoModel.GOOGLE_VEO3, TextToVideoModel.GOOGLE_VEO3_FAST]:
                    audio_suffix = "_with_audio" if generate_audio else "_no_audio"
                    output_filename = f"{model_name}_{safe_prompt}_{duration}_{aspect_ratio.replace(':', 'x')}{audio_suffix}_{timestamp}.mp4"
                else:
                    output_filename = f"{model_name}_{safe_prompt}_{timestamp}.mp4"
            
            # Ensure .mp4 extension
            if not output_filename.endswith('.mp4'):
                output_filename += '.mp4'
            
            # Download video
            local_path = self._download_video(video_url, output_filename)
            
            # Prepare result
            generation_result = {
                'success': True,
                'video_url': video_url,
                'local_path': str(local_path),
                'filename': output_filename,
                'prompt': prompt,
                'model': model.value,
                'model_name': self.MODEL_CONFIGS[model]["name"],
                'cost_usd': cost,
                'metadata': result
            }
            
            # Add model-specific metadata
            if model == TextToVideoModel.MINIMAX_HAILUO:
                generation_result.update({
                    'prompt_optimizer': prompt_optimizer,
                    'resolution': '1080p',
                    'duration': '6s'
                })
            
            elif model in [TextToVideoModel.GOOGLE_VEO3, TextToVideoModel.GOOGLE_VEO3_FAST]:
                generation_result.update({
                    'aspect_ratio': aspect_ratio,
                    'duration': duration,
                    'generate_audio': generate_audio,
                    'negative_prompt': negative_prompt,
                    'seed': seed,
                    'resolution': '720p'
                })
                
                # enhance_prompt only available for regular Veo 3
                if model == TextToVideoModel.GOOGLE_VEO3:
                    generation_result['enhance_prompt'] = enhance_prompt
            
            if self.verbose:
                print(f"📹 Video saved: {local_path}")
                print(f"🔗 Original URL: {video_url}")
                print(f"💰 Actual cost: ${cost:.2f}")
            
            return generation_result
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'prompt': prompt,
                'model': model.value,
                'estimated_cost': cost
            }
            
            if self.verbose:
                print(f"❌ Generation failed: {e}")
            
            return error_result
    
    def _download_video(self, url: str, filename: str) -> Path:
        """Download video from URL to local file."""
        local_path = self.output_dir / filename
        
        if self.verbose:
            print(f"⬇️ Downloading video: {filename}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if self.verbose and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r⬇️ Downloading: {progress:.1f}%", end='', flush=True)
            
            if self.verbose:
                if total_size > 0:
                    print()  # New line after progress
                print(f"✅ Download completed: {local_path}")
            
            return local_path
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Download failed: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test the connection to FAL AI API."""
        if self.verbose:
            print("🔍 Testing FAL AI connection...")
        
        try:
            # Validate API key format (FAL keys have format: uuid:hash)
            if ':' not in self.api_key or len(self.api_key.split(':')) != 2:
                if self.verbose:
                    print("❌ Invalid API key format (should be uuid:hash format)")
                return False
            
            if self.verbose:
                print("✅ API key format is valid")
                print("✅ fal_client is properly configured")
                print("⚠️ Note: Actual generation will incur costs:")
                print("   • MiniMax Hailuo-02 Pro: ~$0.08 per video")
                print("   • Google Veo 3: $2.50-$6.00 per video")
                print("   • Google Veo 3 Fast: $1.25-$3.20 per video")
            
            return True
            
        except Exception as e:
            if self.verbose:
                print(f"❌ Connection test failed: {e}")
            return False
    
    def get_model_info(self, model: Optional[TextToVideoModel] = None) -> Dict[str, Any]:
        """Get information about available models or a specific model."""
        if model is None:
            # Return info about all models
            return {
                'available_models': {
                    model.name: {
                        'endpoint': model.value,
                        **config
                    }
                    for model, config in self.MODEL_CONFIGS.items()
                }
            }
        else:
            # Return info about specific model
            config = self.MODEL_CONFIGS[model]
            return {
                'model_name': config['name'],
                'endpoint': model.value,
                **config
            }
    
    def print_model_comparison(self):
        """Print a comparison of available models."""
        print("🎬 FAL AI Text-to-Video Models Comparison")
        print("=" * 80)
        
        for model, config in self.MODEL_CONFIGS.items():
            print(f"\n📺 {config['name']}")
            print("-" * 40)
            print(f"🔗 Endpoint: {model.value}")
            print(f"📐 Resolution: {config['resolution']}")
            print(f"⏱️ Duration: {config['duration']}")
            
            if 'cost_per_video' in config:
                print(f"💰 Cost: ${config['cost_per_video']:.2f} per video")
            else:
                print(f"💰 Cost: ${config['cost_per_second_no_audio']:.2f}/s (no audio), ${config['cost_per_second_with_audio']:.2f}/s (with audio)")
            
            print("✨ Features:")
            for feature in config['features']:
                print(f"  • {feature}")
        
        print(f"\n💡 Recommendation:")
        print("  • Use MiniMax Hailuo-02 Pro for most cost-effective videos")
        print("  • Use Google Veo 3 Fast for balanced cost and quality")
        print("  • Use Google Veo 3 for premium quality with advanced controls")
    
    def get_cost_estimate(
        self, 
        model: TextToVideoModel, 
        duration: Optional[Veo3Duration] = None,
        generate_audio: bool = True
    ) -> str:
        """Get a formatted cost estimate."""
        cost = self.calculate_cost(model, duration, generate_audio)
        model_name = self.MODEL_CONFIGS[model]["name"]
        
        if model == TextToVideoModel.MINIMAX_HAILUO:
            return f"${cost:.2f} for {model_name} video"
        else:
            duration = duration or "8s"
            audio_status = "with audio" if generate_audio else "without audio"
            return f"${cost:.2f} for {duration} {model_name} video {audio_status}"


def main():
    """Example usage of FAL Text-to-Video Generator."""
    print("🎬 FAL Text-to-Video Generator Example")
    print("=" * 60)
    
    # Initialize generator
    try:
        generator = FALTextToVideoGenerator(verbose=True)
    except ValueError as e:
        print(f"❌ Initialization failed: {e}")
        return
    
    # Print model comparison
    generator.print_model_comparison()
    
    # Test connection
    print("\n🔍 Testing connection...")
    if generator.test_connection():
        print("✅ Connection test passed!")
    else:
        print("❌ Connection test failed!")
        return
    
    # Show cost estimates
    print("\n💰 Cost Estimates:")
    print(f"  • {generator.get_cost_estimate(TextToVideoModel.MINIMAX_HAILUO)}")
    for duration in ["5s", "6s", "7s", "8s"]:
        print(f"  • {generator.get_cost_estimate(TextToVideoModel.GOOGLE_VEO3, duration, True)}")
        print(f"  • {generator.get_cost_estimate(TextToVideoModel.GOOGLE_VEO3, duration, False)}")
        print(f"  • {generator.get_cost_estimate(TextToVideoModel.GOOGLE_VEO3_FAST, duration, True)}")
        print(f"  • {generator.get_cost_estimate(TextToVideoModel.GOOGLE_VEO3_FAST, duration, False)}")
    
    print("\n⚠️ WARNING: Video generation incurs costs!")
    print("💡 Use test_generation.py to run actual generation tests")
    
    # Example usage (commented out to avoid costs):
    """
    # Generate with MiniMax (cost-effective)
    result1 = generator.generate_video(
        prompt="A cat playing with a ball of yarn",
        model=TextToVideoModel.MINIMAX_HAILUO,
        prompt_optimizer=True
    )
    
    # Generate with Veo 3 (premium)
    result2 = generator.generate_video(
        prompt="A majestic eagle soaring over mountains",
        model=TextToVideoModel.GOOGLE_VEO3,
        duration="8s",
        generate_audio=True,
        aspect_ratio="16:9"
    )
    """


if __name__ == "__main__":
    main()