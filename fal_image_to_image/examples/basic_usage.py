#!/usr/bin/env python3
"""
Basic usage examples for FAL Image-to-Image package

This script demonstrates the core functionality of the refactored package.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fal_image_to_image import FALImageToImageGenerator

def basic_seededit_example():
    """Basic SeedEdit v3 usage example"""
    print("🎨 Basic SeedEdit v3 Example")
    print("-" * 40)
    
    try:
        # Initialize generator
        generator = FALImageToImageGenerator()
        
        # Example with SeedEdit v3 (best for content preservation)
        result = generator.modify_image_seededit(
            prompt="Enhance image quality and make it more photorealistic",
            image_url="https://example.com/image.jpg",  # Replace with actual URL
            guidance_scale=0.5,
            seed=42
        )
        
        if result['success']:
            print(f"✅ Success! Generated: {result['downloaded_files']}")
            print(f"⏱️  Processing time: {result['processing_time']:.1f}s")
        else:
            print(f"❌ Failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def photon_example():
    """Basic Photon Flash usage example"""
    print("\n🎨 Basic Photon Flash Example")
    print("-" * 40)
    
    try:
        generator = FALImageToImageGenerator()
        
        # Example with Photon Flash (best for creative modifications)
        result = generator.modify_image_photon(
            prompt="Transform into a futuristic cyberpunk scene",
            image_url="https://example.com/image.jpg",  # Replace with actual URL
            strength=0.7,
            aspect_ratio="16:9"
        )
        
        if result['success']:
            print(f"✅ Success! Generated: {result['downloaded_files']}")
            print(f"⏱️  Processing time: {result['processing_time']:.1f}s")
        else:
            print(f"❌ Failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def local_image_example():
    """Local image processing example"""
    print("\n🎨 Local Image Processing Example")
    print("-" * 40)
    
    # Check if test image exists
    image_path = "../test_ai_image.jpg"
    if not Path(image_path).exists():
        print(f"⚠️  Test image not found: {image_path}")
        print("   Add a test image to try this example")
        return
    
    try:
        generator = FALImageToImageGenerator()
        
        # Process local image with SeedEdit v3
        result = generator.modify_local_image_seededit(
            prompt="Add professional studio lighting and enhance details",
            image_path=image_path,
            guidance_scale=0.6,
            seed=123
        )
        
        if result['success']:
            print(f"✅ Success! Generated: {Path(result['downloaded_files'][0]).name}")
            print(f"⏱️  Processing time: {result['processing_time']:.1f}s")
            print(f"📁 Output directory: {result['output_directory']}")
        else:
            print(f"❌ Failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def model_info_example():
    """Show model information"""
    print("\n📋 Model Information Example")
    print("-" * 40)
    
    try:
        generator = FALImageToImageGenerator()
        
        print("Supported models:")
        for model in generator.get_supported_models():
            info = generator.get_model_info(model)
            print(f"   • {info['model_name']} ({model})")
        
        # Show detailed info for SeedEdit v3
        print(f"\n📊 SeedEdit v3 Details:")
        seededit_info = generator.get_model_info("seededit")
        print(f"   Description: {seededit_info['description']}")
        print(f"   Guidance Scale: {seededit_info['guidance_scale_range']}")
        print(f"   Features:")
        for feature in seededit_info['features']:
            print(f"     - {feature}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all basic examples"""
    print("FAL Image-to-Image Basic Usage Examples")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv('FAL_KEY'):
        print("⚠️  FAL_KEY environment variable not set")
        print("   Set your API key: export FAL_KEY='your_api_key'")
        print("   The examples below will show errors without a valid key.\n")
    
    # Run examples (they will show the expected usage patterns)
    model_info_example()
    basic_seededit_example()
    photon_example()
    local_image_example()
    
    print("\n" + "=" * 60)
    print("🎉 Basic examples completed!")
    print("💡 Set FAL_KEY environment variable to make real API calls")

if __name__ == "__main__":
    main()