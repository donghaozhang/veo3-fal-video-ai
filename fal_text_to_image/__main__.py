#!/usr/bin/env python3
"""
FAL Text-to-Image CLI Interface

Allows running the module directly from command line:
    python -m fal_text_to_image [command] [options]
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any

from .fal_text_to_image_generator import FALTextToImageGenerator

def print_models():
    """Print information about all supported models."""
    print("\n🎨 FAL Text-to-Image Supported Models")
    print("=" * 50)
    
    try:
        generator = FALTextToImageGenerator()
        model_info = generator.get_model_info()
        
        for model_key, info in model_info.items():
            print(f"\n📦 {model_key}")
            print(f"   Name: {info['name']}")
            print(f"   Description: {info['description']}")
            print(f"   Features:")
            for feature in info.get('features', [])[:3]:  # Show first 3 features
                print(f"     • {feature}")
    except Exception as e:
        print(f"❌ Error getting model info: {e}")

def generate_image(args):
    """Handle image generation command."""
    try:
        # Initialize generator
        generator = FALTextToImageGenerator()
        
        # Prepare kwargs based on model
        kwargs = {}
        
        # Add optional parameters
        if args.output_dir:
            kwargs["output_dir"] = args.output_dir
        if args.seed is not None:
            kwargs["seed"] = args.seed
        if args.num_inference_steps is not None:
            kwargs["num_inference_steps"] = args.num_inference_steps
        if args.guidance_scale is not None:
            kwargs["guidance_scale"] = args.guidance_scale
        
        # Prepare model-specific parameters
        model_params = {}
        if args.seed is not None:
            model_params["seed"] = args.seed
        if args.num_inference_steps is not None:
            model_params["num_inference_steps"] = args.num_inference_steps
        if args.guidance_scale is not None:
            model_params["guidance_scale"] = args.guidance_scale
        if args.image_size:
            model_params["image_size"] = args.image_size
        if args.negative_prompt:
            model_params["negative_prompt"] = args.negative_prompt
        if args.num_images is not None:
            model_params["num_images"] = args.num_images
        
        # Use the new CLI function
        result = generator.generate_from_cli(
            prompt_input=args.prompt,
            model=args.model,
            output_path=args.output_dir,
            **model_params
        )
        
        # Print results
        if result.get("success"):
            print(f"\n✅ Image generation successful!")
            print(f"📦 Model: {args.model}")
            print(f"📝 Prompt: {args.prompt}")
            print(f"⏱️  Processing time: {result.get('processing_time', 'N/A'):.2f}s")
            
            # Show generated files
            downloaded_files = result.get('downloaded_files', [])
            if downloaded_files:
                print(f"📁 Generated {len(downloaded_files)} image(s):")
                for file_path in downloaded_files:
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        print(f"   🖼️  {os.path.basename(file_path)} ({file_size:,} bytes)")
            
            # Save full result if requested
            if args.save_json:
                json_path = Path(args.save_json)
                with open(json_path, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"📄 Full result saved to: {json_path}")
        else:
            print(f"\n❌ Image generation failed!")
            print(f"💥 Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        if args.debug:
            traceback.print_exc()
        sys.exit(1)

def test_setup(args):
    """Handle setup testing command (FREE)."""
    try:
        print("🔧 Testing FAL Text-to-Image Setup...")
        print("=" * 40)
        
        # Check environment
        env_file = ".env"
        if os.path.exists(env_file):
            print(f"✅ Found {env_file}")
        else:
            print(f"⚠️  No {env_file} file found")
        
        # Initialize generator
        generator = FALTextToImageGenerator()
        print("✅ Generator initialized successfully")
        
        # Check API key
        if generator.api_key:
            print("✅ FAL_KEY found")
            masked_key = f"{generator.api_key[:8]}...{generator.api_key[-4:]}"
            print(f"🔑 API Key: {masked_key}")
        else:
            print("❌ FAL_KEY not found")
            sys.exit(1)
        
        # Check models
        model_info = generator.get_model_info()
        print(f"✅ Found {len(model_info)} models:")
        for model_name, info in model_info.items():
            print(f"   • {info.get('name', model_name)}")
        
        print("\n✅ Setup test completed successfully!")
        
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def compare_models(args):
    """Handle model comparison command."""
    try:
        print("🆚 Comparing all models with same prompt...")
        print("⚠️  This will generate 4 images and incur costs!")
        
        generator = FALTextToImageGenerator()
        
        # Use the new CLI batch function
        results = generator.batch_generate_from_cli(
            prompt_input=args.prompt,
            models=None,  # Use all models
            output_path=args.output_dir,
            save_results=args.save_json
        )
            
    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FAL Text-to-Image CLI - Generate images with AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all models
  python -m fal_text_to_image list-models
  
  # Test setup (FREE)
  python -m fal_text_to_image test-setup
  
  # Generate with text prompt
  python -m fal_text_to_image generate -p "a dragon in the sky" -m imagen4 -o my_output
  
  # Generate with prompt file
  python -m fal_text_to_image generate -p prompts/fantasy.txt -m flux_schnell
  
  # Generate with advanced parameters
  python -m fal_text_to_image generate -p "cyberpunk cityscape" -m flux_dev \\
    --image-size landscape_16_9 --guidance-scale 4.0 --num-inference-steps 30
  
  # Generate with negative prompt
  python -m fal_text_to_image generate -p "beautiful landscape" -m seedream \\
    --negative-prompt "blurry, low quality" --seed 42
  
  # Compare all models with prompt file
  python -m fal_text_to_image compare -p prompts/test.txt --save-json results.json
        """
    )
    
    # Global options
    parser.add_argument("--debug", action="store_true", help="Show debug information")
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List models command
    list_parser = subparsers.add_parser("list-models", help="List all supported models")
    
    # Test setup command
    setup_parser = subparsers.add_parser("test-setup", help="Test environment setup (FREE)")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate an image")
    generate_parser.add_argument("-p", "--prompt", required=True, 
                                help="Text prompt or path to prompt file (.txt, .md, .prompt)")
    generate_parser.add_argument("-m", "--model", choices=["imagen4", "seedream", "flux_schnell", "flux_dev"],
                                required=True, help="Model to use")
    generate_parser.add_argument("-o", "--output-dir", help="Output directory (default: output)")
    
    # Model-specific parameters
    generate_parser.add_argument("--seed", type=int, help="Random seed (seedream, flux_dev)")
    generate_parser.add_argument("--num-inference-steps", type=int, help="Number of inference steps")
    generate_parser.add_argument("--guidance-scale", type=float, help="Guidance scale (imagen4, seedream, flux_dev)")
    generate_parser.add_argument("--image-size", help="Image size (e.g., landscape_4_3, square, portrait_16_9)")
    generate_parser.add_argument("--negative-prompt", help="Negative prompt (seedream, flux_dev only)")
    generate_parser.add_argument("--num-images", type=int, help="Number of images to generate (default: 1)")
    generate_parser.add_argument("--save-json", help="Save full result as JSON")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare all models with same prompt")
    compare_parser.add_argument("-p", "--prompt", required=True, 
                               help="Text prompt or path to prompt file (.txt, .md, .prompt)")
    compare_parser.add_argument("-o", "--output-dir", help="Output directory (default: output)")
    compare_parser.add_argument("--save-json", help="Save comparison results as JSON")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == "list-models":
        print_models()
    elif args.command == "test-setup":
        test_setup(args)
    elif args.command == "generate":
        generate_image(args)
    elif args.command == "compare":
        compare_models(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()