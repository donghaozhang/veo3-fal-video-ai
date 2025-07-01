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
        
        # Generate image using unified method
        result = generator.generate_image(
            prompt=args.prompt,
            model=args.model
        )
        
        # Download image if successful
        if result.get("success") and result.get("image_url"):
            output_dir = args.output_dir or "output"
            try:
                local_path = generator.download_image(result["image_url"], output_dir)
                result["local_path"] = local_path
            except Exception as e:
                print(f"⚠️ Download failed: {e}")
                result["download_error"] = str(e)
        
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
        models = ["imagen4", "seedream", "flux_schnell", "flux_dev"]
        results = {}
        
        for i, model in enumerate(models, 1):
            print(f"\n🎨 Testing model {i}/{len(models)}: {model}")
            
            try:
                # Generate image using unified method
                result = generator.generate_image(prompt=args.prompt, model=model)
                
                # Download image if successful
                if result.get("success") and result.get("image_url"):
                    output_dir = args.output_dir or "output"
                    try:
                        local_path = generator.download_image(result["image_url"], output_dir)
                        result["local_path"] = local_path
                    except Exception as e:
                        result["download_error"] = str(e)
                
                if result.get("success"):
                    print(f"   ✅ {model}: SUCCESS ({result.get('processing_time', 0):.2f}s)")
                else:
                    print(f"   ❌ {model}: FAILED - {result.get('error', 'Unknown error')}")
                
                results[model] = result
                
            except Exception as e:
                print(f"   ❌ {model}: ERROR - {e}")
                results[model] = {"success": False, "error": str(e)}
        
        # Summary
        successful = sum(1 for r in results.values() if r.get("success", False))
        print(f"\n📊 Comparison complete: {successful}/{len(models)} models successful")
        
        if args.save_json:
            with open(args.save_json, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"📄 Results saved to: {args.save_json}")
            
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
  
  # Generate with Imagen 4
  python -m fal_text_to_image generate -p "a dragon in the sky" -m imagen4
  
  # Generate with FLUX Schnell
  python -m fal_text_to_image generate -p "cyberpunk cityscape" -m flux_schnell
  
  # Compare all models
  python -m fal_text_to_image compare -p "majestic phoenix"
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
    generate_parser.add_argument("-p", "--prompt", required=True, help="Text prompt for image generation")
    generate_parser.add_argument("-m", "--model", choices=["imagen4", "seedream", "flux_schnell", "flux_dev"],
                                required=True, help="Model to use")
    generate_parser.add_argument("-o", "--output-dir", help="Output directory")
    generate_parser.add_argument("--seed", type=int, help="Random seed")
    generate_parser.add_argument("--num-inference-steps", type=int, help="Number of inference steps")
    generate_parser.add_argument("--guidance-scale", type=float, help="Guidance scale")
    generate_parser.add_argument("--save-json", help="Save full result as JSON")
    
    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare all models with same prompt")
    compare_parser.add_argument("-p", "--prompt", required=True, help="Text prompt for comparison")
    compare_parser.add_argument("-o", "--output-dir", help="Output directory")
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