#!/usr/bin/env python3
"""
FAL Image-to-Image CLI Interface

Allows running the module directly from command line:
    python -m fal_image_to_image [command] [options]
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any

from .generator import FALImageToImageGenerator
from .config.constants import SUPPORTED_MODELS, MODEL_INFO


def print_models():
    """Print information about all supported models."""
    print("\n🎨 FAL Image-to-Image Supported Models")
    print("=" * 50)
    
    for model_key, info in MODEL_INFO.items():
        print(f"\n📦 {model_key}")
        print(f"   Name: {info['model_name']}")
        print(f"   Description: {info['description']}")
        print(f"   Features:")
        for feature in info.get('features', [])[:3]:  # Show first 3 features
            print(f"     • {feature}")
        if model_key == "clarity":
            print(f"   Scale Range: {info.get('scale_factor_range', 'N/A')}")
        elif model_key == "photon":
            print(f"   Aspect Ratios: {', '.join(info.get('supported_aspect_ratios', [])[:5])}...")


def modify_image(args):
    """Handle image modification command."""
    try:
        # Initialize generator
        generator = FALImageToImageGenerator()
        
        # Prepare kwargs based on model
        kwargs = {}
        
        if args.model == "photon" or args.model == "photon_base":
            if args.strength is not None:
                kwargs["strength"] = args.strength
            if args.aspect_ratio:
                kwargs["aspect_ratio"] = args.aspect_ratio
            
            # Add reframing parameters
            if args.x_start is not None:
                kwargs["x_start"] = args.x_start
            if args.y_start is not None:
                kwargs["y_start"] = args.y_start
            if args.x_end is not None:
                kwargs["x_end"] = args.x_end
            if args.y_end is not None:
                kwargs["y_end"] = args.y_end
            if args.grid_position_x is not None:
                kwargs["grid_position_x"] = args.grid_position_x
            if args.grid_position_y is not None:
                kwargs["grid_position_y"] = args.grid_position_y
            if args.auto_center:
                kwargs["auto_center"] = args.auto_center
            if args.input_width is not None:
                kwargs["input_width"] = args.input_width
            if args.input_height is not None:
                kwargs["input_height"] = args.input_height
                
        elif args.model == "kontext":
            if args.num_inference_steps is not None:
                kwargs["num_inference_steps"] = args.num_inference_steps
            if args.guidance_scale is not None:
                kwargs["guidance_scale"] = args.guidance_scale
                
        elif args.model == "seededit":
            if args.guidance_scale is not None:
                kwargs["guidance_scale"] = args.guidance_scale
            if args.seed is not None:
                kwargs["seed"] = args.seed
                
        elif args.model == "clarity":
            # For clarity, we use the upscale methods
            kwargs["scale"] = args.scale or 2
            kwargs["enable_enhancement"] = not args.no_enhancement
            if args.prompt:
                kwargs["prompt"] = args.prompt
            if args.seed is not None:
                kwargs["seed"] = args.seed
        
        # Add output directory if specified
        if args.output_dir:
            kwargs["output_dir"] = args.output_dir
        
        # Execute based on input type
        if args.model == "clarity":
            # Use upscale methods for clarity
            if args.image_url:
                result = generator.upscale_image(
                    image_url=args.image_url,
                    **kwargs
                )
            else:
                result = generator.upscale_local_image(
                    image_path=args.image_path,
                    **kwargs
                )
        else:
            # Use modify methods for other models
            if args.image_url:
                result = generator.modify_image(
                    prompt=args.prompt,
                    image_url=args.image_url,
                    model=args.model,
                    **kwargs
                )
            else:
                result = generator.modify_local_image(
                    prompt=args.prompt,
                    image_path=args.image_path,
                    model=args.model,
                    **kwargs
                )
        
        # Print results
        if result.get("success"):
            print(f"\n✅ Image modification successful!")
            print(f"📦 Model: {result.get('model', args.model)}")
            if "local_path" in result:
                print(f"📁 Output: {result['local_path']}")
            if "image_url" in result:
                print(f"🔗 URL: {result['image_url']}")
            
            # Print dimensions if available
            if "width" in result and "height" in result:
                print(f"📐 Dimensions: {result['width']}x{result['height']}")
            
            # Save full result if requested
            if args.save_json:
                json_path = Path(args.save_json)
                with open(json_path, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"📄 Full result saved to: {json_path}")
        else:
            print(f"\n❌ Image modification failed!")
            print(f"💥 Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        if args.debug:
            traceback.print_exc()
        sys.exit(1)


def batch_modify(args):
    """Handle batch modification command."""
    try:
        # Read batch file
        with open(args.batch_file, 'r') as f:
            batch_data = json.load(f)
        
        # Validate batch data
        if not isinstance(batch_data, list):
            raise ValueError("Batch file must contain a JSON array")
        
        # Initialize generator
        generator = FALImageToImageGenerator()
        
        print(f"\n🎨 Processing batch of {len(batch_data)} images...")
        
        results = []
        for i, item in enumerate(batch_data, 1):
            print(f"\n📸 Processing image {i}/{len(batch_data)}")
            
            # Extract parameters
            prompt = item.get("prompt", "")
            image_path = item.get("image_path")
            image_url = item.get("image_url")
            model = item.get("model", args.model)
            
            if not (image_path or image_url):
                print(f"⚠️  Skipping item {i}: No image_path or image_url")
                continue
            
            # Prepare kwargs
            kwargs = {k: v for k, v in item.items() 
                     if k not in ["prompt", "image_path", "image_url", "model"]}
            
            # Process image
            try:
                if model == "clarity":
                    if image_url:
                        result = generator.upscale_image(image_url=image_url, **kwargs)
                    else:
                        result = generator.upscale_local_image(image_path=image_path, **kwargs)
                else:
                    if image_url:
                        result = generator.modify_image(
                            prompt=prompt, image_url=image_url, model=model, **kwargs
                        )
                    else:
                        result = generator.modify_local_image(
                            prompt=prompt, image_path=image_path, model=model, **kwargs
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
        description="FAL Image-to-Image CLI - Modify images with AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all models
  python -m fal_image_to_image list-models
  
  # Modify image with Photon
  python -m fal_image_to_image modify -i input/image.jpg -p "make it cyberpunk style" -m photon
  
  # Upscale image with Clarity
  python -m fal_image_to_image modify -i input/image.jpg -m clarity --scale 2
  
  # Batch process images
  python -m fal_image_to_image batch -f batch.json -m photon
        """
    )
    
    # Global options
    parser.add_argument("--debug", action="store_true", help="Show debug information")
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List models command
    list_parser = subparsers.add_parser("list-models", help="List all supported models")
    
    # Modify command
    modify_parser = subparsers.add_parser("modify", help="Modify a single image")
    
    # Input options (mutually exclusive)
    input_group = modify_parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-i", "--image-path", help="Path to local image file")
    input_group.add_argument("-u", "--image-url", help="URL of image")
    
    # Model and prompt
    modify_parser.add_argument("-m", "--model", choices=SUPPORTED_MODELS, 
                              default="photon", help="Model to use (default: photon)")
    modify_parser.add_argument("-p", "--prompt", help="Modification prompt (not needed for clarity)")
    
    # Model-specific options
    modify_parser.add_argument("--strength", type=float, help="Strength for Photon models (0.0-1.0)")
    modify_parser.add_argument("--aspect-ratio", help="Aspect ratio for Photon models")
    modify_parser.add_argument("--num-inference-steps", type=int, help="Steps for Kontext")
    modify_parser.add_argument("--guidance-scale", type=float, help="Guidance scale")
    modify_parser.add_argument("--seed", type=int, help="Random seed")
    modify_parser.add_argument("--scale", type=float, help="Scale factor for Clarity (1-4)")
    modify_parser.add_argument("--no-enhancement", action="store_true", 
                              help="Disable enhancement for Clarity")
    
    # Reframing options for Photon models
    modify_parser.add_argument("--x-start", type=int, help="Start X coordinate for reframing")
    modify_parser.add_argument("--y-start", type=int, help="Start Y coordinate for reframing")
    modify_parser.add_argument("--x-end", type=int, help="End X coordinate for reframing")
    modify_parser.add_argument("--y-end", type=int, help="End Y coordinate for reframing")
    modify_parser.add_argument("--grid-position-x", type=int, help="X position of grid for reframing")
    modify_parser.add_argument("--grid-position-y", type=int, help="Y position of grid for reframing")
    modify_parser.add_argument("--auto-center", action="store_true", 
                              help="Auto-center input image in output aspect ratio")
    modify_parser.add_argument("--input-width", type=int, help="Input image width (for auto-center)")
    modify_parser.add_argument("--input-height", type=int, help="Input image height (for auto-center)")
    
    # Output options
    modify_parser.add_argument("-o", "--output-dir", help="Output directory")
    modify_parser.add_argument("--save-json", help="Save full result as JSON")
    
    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Batch process multiple images")
    batch_parser.add_argument("-f", "--batch-file", required=True, help="JSON file with batch data")
    batch_parser.add_argument("-m", "--model", choices=SUPPORTED_MODELS, 
                             default="photon", help="Default model (can be overridden per image)")
    batch_parser.add_argument("--save-json", help="Save results as JSON")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == "list-models":
        print_models()
    elif args.command == "modify":
        # Validate prompt requirement for non-clarity models
        if args.model != "clarity" and not args.prompt:
            parser.error(f"--prompt is required for {args.model} model")
        modify_image(args)
    elif args.command == "batch":
        batch_modify(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()