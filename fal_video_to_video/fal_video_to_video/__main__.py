#!/usr/bin/env python3
"""
FAL Video to Video CLI Interface

Allows running the module directly from command line:
    python -m fal_video_to_video [command] [options]
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any

from .generator import FALVideoToVideoGenerator
from .config.constants import SUPPORTED_MODELS, MODEL_INFO


def print_models():
    """Print information about all supported models."""
    print("\n🎵 FAL Video to Video Supported Models")
    print("=" * 50)
    
    for model_key, info in MODEL_INFO.items():
        print(f"\n📦 {model_key}")
        print(f"   Name: {info['model_name']}")
        print(f"   Description: {info['description']}")
        print(f"   Features:")
        for feature in info.get('features', [])[:3]:  # Show first 3 features
            print(f"     • {feature}")
        print(f"   Pricing: {info.get('pricing', 'N/A')}")
        print(f"   Max Duration: {info.get('max_duration', 'N/A')} seconds")


def add_audio(args):
    """Handle add-audio command."""
    try:
        # Initialize generator
        generator = FALVideoToVideoGenerator()
        
        # Prepare kwargs
        kwargs = {}
        
        if args.prompt:
            kwargs["prompt"] = args.prompt
        if args.seed is not None:
            kwargs["seed"] = args.seed
        if args.output_dir:
            kwargs["output_dir"] = args.output_dir
        
        # Execute based on input type
        if args.video_url:
            result = generator.add_audio_to_video(
                video_url=args.video_url,
                model=args.model,
                **kwargs
            )
        else:
            result = generator.add_audio_to_local_video(
                video_path=args.video_path,
                model=args.model,
                **kwargs
            )
        
        # Display results
        if result.get("success"):
            print(f"\n✅ Audio generation successful!")
            print(f"📦 Model: {result.get('model')}")
            if result.get("local_path"):
                print(f"📁 Output: {result.get('local_path')}")
            if result.get("prompt"):
                print(f"💬 Prompt: {result.get('prompt')}")
            print(f"⏱️  Processing time: {result.get('processing_time', 0):.2f} seconds")
        else:
            print(f"\n❌ Audio generation failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        # Save full result if requested
        if args.save_json:
            with open(args.save_json, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\n📄 Full result saved to: {args.save_json}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def batch_process(args):
    """Handle batch processing command."""
    try:
        # Read batch file
        with open(args.batch_file, 'r') as f:
            batch_data = json.load(f)
        
        # Validate batch data
        if not isinstance(batch_data, list):
            raise ValueError("Batch file must contain a JSON array")
        
        # Initialize generator
        generator = FALVideoToVideoGenerator()
        
        print(f"\n🎵 Processing batch of {len(batch_data)} videos...")
        
        results = []
        for i, item in enumerate(batch_data, 1):
            print(f"\n📹 Processing video {i}/{len(batch_data)}")
            
            # Extract parameters
            video_path = item.get("video_path")
            video_url = item.get("video_url")
            model = item.get("model", args.model)
            
            if not (video_path or video_url):
                print(f"⚠️  Skipping item {i}: No video_path or video_url")
                continue
            
            # Prepare kwargs
            kwargs = {k: v for k, v in item.items() 
                     if k not in ["video_path", "video_url", "model"]}
            
            # Process video
            try:
                if video_url:
                    result = generator.add_audio_to_video(
                        video_url=video_url, model=model, **kwargs
                    )
                else:
                    result = generator.add_audio_to_local_video(
                        video_path=video_path, model=model, **kwargs
                    )
                
                results.append(result)
                
                if result.get("success"):
                    print(f"✅ Success: {result.get('local_path', 'No local path')}")
                else:
                    print(f"❌ Failed: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Error processing item {i}: {e}")
                results.append({"success": False, "error": str(e)})
        
        # Summary
        successful = sum(1 for r in results if r.get("success", False))
        print(f"\n📊 Batch complete: {successful}/{len(batch_data)} successful")
        
        # Save results if requested
        if args.save_json:
            with open(args.save_json, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"📄 Results saved to: {args.save_json}")
            
    except Exception as e:
        print(f"\n❌ Batch processing error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FAL Video to Video CLI - Add AI-generated audio to videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all models
  python -m fal_video_to_video list-models
  
  # Add audio to local video
  python -m fal_video_to_video add-audio -i input/video.mp4
  
  # Add audio with text prompt
  python -m fal_video_to_video add-audio -i input/video.mp4 -p "add dramatic music"
  
  # Add audio from URL
  python -m fal_video_to_video add-audio -u https://example.com/video.mp4
  
  # Batch process videos
  python -m fal_video_to_video batch -f batch.json
        """
    )
    
    # Add debug flag to main parser
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List models command
    subparsers.add_parser("list-models", help="List all available models")
    
    # Add audio command
    audio_parser = subparsers.add_parser("add-audio", help="Add audio to a single video")
    
    # Input options (mutually exclusive)
    input_group = audio_parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-i", "--video-path", help="Path to local video file")
    input_group.add_argument("-u", "--video-url", help="URL of video")
    
    # Model and parameters
    audio_parser.add_argument("-m", "--model", choices=SUPPORTED_MODELS, 
                             default="thinksound", help="Model to use (default: thinksound)")
    audio_parser.add_argument("-p", "--prompt", help="Text prompt to guide audio generation")
    audio_parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    
    # Output options
    audio_parser.add_argument("-o", "--output-dir", help="Output directory")
    audio_parser.add_argument("--save-json", help="Save full result as JSON")
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Batch process multiple videos")
    batch_parser.add_argument("-f", "--batch-file", required=True, help="JSON file with batch data")
    batch_parser.add_argument("-m", "--model", choices=SUPPORTED_MODELS, 
                             default="thinksound", help="Default model (can be overridden per video)")
    batch_parser.add_argument("--save-json", help="Save results as JSON")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == "list-models":
        print_models()
    elif args.command == "add-audio":
        add_audio(args)
    elif args.command == "batch":
        batch_process(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()