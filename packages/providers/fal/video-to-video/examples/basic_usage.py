#!/usr/bin/env python3
"""
Basic usage examples for FAL Video to Video
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fal_video_to_video import FALVideoToVideoGenerator


def example_url_generation():
    """Example: Generate audio for video from URL."""
    print("🎵 Example 1: Audio generation from URL")
    print("=" * 40)
    
    # Initialize generator
    generator = FALVideoToVideoGenerator()
    
    # Example video URL
    video_url = "https://storage.googleapis.com/falserverless/example_inputs/thinksound-input.mp4"
    
    # Generate audio with prompt
    result = generator.add_audio_to_video(
        video_url=video_url,
        model="thinksound",
        prompt="add dramatic orchestral music with sound effects"
    )
    
    # Display results
    if result.get("success"):
        print("✅ Success!")
        print(f"   Output: {result.get('local_path')}")
        print(f"   Processing time: {result.get('processing_time'):.2f}s")
    else:
        print(f"❌ Failed: {result.get('error')}")


def example_local_video():
    """Example: Generate audio for local video file."""
    print("\n🎬 Example 2: Audio generation from local file")
    print("=" * 45)
    
    # Check for local video
    input_dir = project_root / "input"
    video_files = list(input_dir.glob("*.mp4"))
    
    if not video_files:
        print("⚠️  No video files found in input/ folder")
        print("   Add a .mp4 file to input/ to test this example")
        return
    
    # Initialize generator
    generator = FALVideoToVideoGenerator()
    
    # Use first video found
    video_path = str(video_files[0])
    print(f"📁 Using: {video_files[0].name}")
    
    # Generate audio
    result = generator.add_audio_to_local_video(
        video_path=video_path,
        model="thinksound",
        prompt="add ambient nature sounds and birds chirping",
        output_dir="examples/output"
    )
    
    # Display results
    if result.get("success"):
        print("✅ Success!")
        print(f"   Output: {result.get('local_path')}")
        print(f"   Processing time: {result.get('processing_time'):.2f}s")
    else:
        print(f"❌ Failed: {result.get('error')}")


def example_with_seed():
    """Example: Generate reproducible audio with seed."""
    print("\n🎲 Example 3: Reproducible generation with seed")
    print("=" * 45)
    
    # Initialize generator
    generator = FALVideoToVideoGenerator()
    
    # Example video URL
    video_url = "https://storage.googleapis.com/falserverless/example_inputs/thinksound-input.mp4"
    
    # Generate with fixed seed
    result = generator.add_audio_to_video(
        video_url=video_url,
        model="thinksound",
        prompt="add electronic music",
        seed=42,  # Fixed seed for reproducibility
        output_dir="examples/output"
    )
    
    # Display results
    if result.get("success"):
        print("✅ Success!")
        print(f"   Used seed: {result.get('seed')}")
        print(f"   Output: {result.get('local_path')}")
        print("   Note: Same seed should produce similar audio")
    else:
        print(f"❌ Failed: {result.get('error')}")


def example_model_info():
    """Example: Get model information."""
    print("\n📋 Example 4: Model information")
    print("=" * 35)
    
    # Initialize generator
    generator = FALVideoToVideoGenerator()
    
    # Get info for specific model
    thinksound_info = generator.get_model_info("thinksound")
    print(f"Model: {thinksound_info['model_name']}")
    print(f"Description: {thinksound_info['description']}")
    print(f"Pricing: {thinksound_info['pricing']}")
    print(f"Max duration: {thinksound_info['max_duration']}s")
    
    # List all available models
    models = generator.list_models()
    print(f"\nAvailable models: {models}")


def main():
    """Run all examples."""
    print("🎵 FAL Video to Video Examples")
    print("=" * 35)
    print("⚠️  Note: These examples make real API calls")
    
    # Check if user wants to run examples that cost money
    print("\nSome examples will incur API costs (~$0.001 per second)")
    response = input("Run examples with API calls? (y/N): ")
    
    run_api_examples = response.lower() == 'y'
    
    # Always run model info (free)
    example_model_info()
    
    if run_api_examples:
        # Run API examples
        example_url_generation()
        example_local_video()
        example_with_seed()
        
        print("\n🎉 All examples completed!")
        print("Check the examples/output/ folder for generated videos")
    else:
        print("\n📖 API examples skipped (to avoid costs)")
        print("To run with actual generation:")
        print("1. Set FAL_KEY in .env file")
        print("2. Run this script and answer 'y' to API calls")


if __name__ == "__main__":
    main()