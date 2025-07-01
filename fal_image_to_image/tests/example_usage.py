#!/usr/bin/env python3
"""
Example usage of FAL Image-to-Image as a Python module
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fal_image_to_image import FALImageToImageGenerator

def main():
    # Change to parent directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Initialize generator
    generator = FALImageToImageGenerator()
    
    # Example 1: Upscale an image with Clarity
    print("🔍 Example 1: Upscaling with Clarity")
    result = generator.upscale_local_image(
        image_path="input/death.jpeg",
        scale=2,
        enable_enhancement=True,
        prompt="enhance details and improve quality"
    )
    
    if result.get("success"):
        print(f"✅ Success! Output: {result.get('local_path')}")
    else:
        print(f"❌ Failed: {result.get('error')}")
    
    # Example 2: Modify with Photon
    print("\n🎨 Example 2: Modifying with Photon")
    result = generator.modify_local_image(
        prompt="transform into cyberpunk style",
        image_path="input/death.jpeg",
        model="photon",
        strength=0.8,
        aspect_ratio="16:9"
    )
    
    if result.get("success"):
        print(f"✅ Success! Output: {result.get('local_path')}")
    else:
        print(f"❌ Failed: {result.get('error')}")
    
    # Example 3: Get model information
    print("\n📊 Example 3: Model Information")
    models = generator.get_supported_models()
    print(f"Supported models: {', '.join(models)}")
    
    # Get specific model info
    clarity_info = generator.get_model_info("clarity")
    print(f"\nClarity Upscaler features:")
    for feature in clarity_info.get("features", [])[:3]:
        print(f"  • {feature}")


if __name__ == "__main__":
    main()