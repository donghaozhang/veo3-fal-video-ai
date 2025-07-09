#!/usr/bin/env python3
"""
FAL AI Clarity Upscaler Test
Tests the Clarity Upscaler model for image upscaling

This script tests the Clarity Upscaler model specifically.
⚠️ WARNING: This script WILL INCUR COSTS when run!

Usage:
    python test_clarity_upscaler.py
    python test_clarity_upscaler.py --yes  # Skip confirmation

Author: AI Assistant  
Date: 2024
"""

import os
import sys
from typing import Dict, Any

def print_cost_warning():
    """Print cost warning and get user confirmation."""
    print("⚠️" * 20)
    print("💰 COST WARNING: This script will incur charges!")
    print("💰 Model: fal-ai/clarity-upscaler")
    print("💰 Estimated cost: $0.01-0.05 per image upscale")
    print("💰 Make sure you have credits in your FAL AI account")
    print("⚠️" * 20)
    
    # Check for --yes flag to skip confirmation
    if '--yes' in sys.argv:
        print("\n✅ Auto-confirmed with --yes flag")
        print("✅ Proceeding with Clarity Upscaler test...")
        return
    
    response = input("\n❓ Do you want to continue and incur charges? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Test cancelled by user")
        sys.exit(0)
    
    print("✅ Proceeding with Clarity Upscaler test...")

def test_clarity_upscaler() -> Dict[str, Any]:
    """Test Clarity Upscaler model."""
    print("\n🎨 Testing Clarity Upscaler Model...")
    print("🖼️  Image: ../input/death.jpeg")
    print("🤖 Model: fal-ai/clarity-upscaler")
    
    try:
        # Import required modules
        import fal_client
        from dotenv import load_dotenv
        load_dotenv()
        
        # Set API key
        api_key = os.getenv('FAL_KEY')
        if not api_key:
            print("❌ FAL_KEY not found in environment variables")
            return {"success": False, "error": "API key not found"}
        
        print("✅ API key loaded successfully")
        
        # Check if image exists
        image_path = "../input/death.jpeg"
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return {"success": False, "error": "Image file not found"}
        
        print(f"✅ Image found: {image_path}")
        
        # Upload image to FAL
        print("📤 Uploading image to FAL...")
        image_url = fal_client.upload_file(image_path)
        print(f"✅ Image uploaded: {image_url}")
        
        # Test parameters
        scale = 2  # 2x upscaling
        enable_enhancement = True
        prompt = "enhance details, improve quality, sharpen image"
        
        print(f"📏 Scale: {scale}x")
        print(f"✨ Enhancement: {'Enabled' if enable_enhancement else 'Disabled'}")
        print(f"📝 Prompt: {prompt}")
        
        # Test with Clarity Upscaler endpoint
        print("\n🚀 Starting image upscaling...")
        print("🔗 Endpoint: fal-ai/clarity-upscaler")
        
        result = fal_client.subscribe(
            "fal-ai/clarity-upscaler",
            arguments={
                "image_url": image_url,
                "scale": scale,
                "enable_enhancement": enable_enhancement,
                "prompt": prompt
            }
        )
        
        if result and 'image' in result:
            print("\n✅ Clarity Upscaler transformation successful!")
            
            # Get the image result
            image_result = result.get('image', {})
            image_url_result = image_result.get('url', 'N/A')
            print(f"📹 Result URL: {image_url_result}")
            
            # Download the image
            if image_url_result != 'N/A':
                print("⬇️  Downloading result image...")
                
                # Create output directory if it doesn't exist
                output_dir = "../output"
                os.makedirs(output_dir, exist_ok=True)
                
                # Download image
                import requests
                response = requests.get(image_url_result)
                if response.status_code == 200:
                    # Generate filename
                    import time
                    timestamp = int(time.time())
                    output_filename = f"clarity_upscaled_{scale}x_{timestamp}.png"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    
                    file_size = os.path.getsize(output_path)
                    print(f"✅ Image downloaded: {output_path}")
                    print(f"📊 File size: {file_size:,} bytes")
                    
                    # Get dimensions if available
                    width = image_result.get('width', 'N/A')
                    height = image_result.get('height', 'N/A')
                    if width != 'N/A' and height != 'N/A':
                        print(f"📐 Dimensions: {width}x{height}")
                    
                    return {
                        "success": True,
                        "model": "fal-ai/clarity-upscaler",
                        "image_url": image_url_result,
                        "local_path": output_path,
                        "file_size": file_size,
                        "width": width,
                        "height": height,
                        "scale": scale,
                        "result": result
                    }
                else:
                    print(f"❌ Failed to download image: HTTP {response.status_code}")
            
            return {
                "success": True,
                "model": "fal-ai/clarity-upscaler",
                "result": result
            }
        else:
            print(f"❌ Clarity Upscaler transformation failed: {result}")
            return {"success": False, "error": "Transformation failed", "result": result}
            
    except Exception as e:
        print(f"❌ Error during Clarity Upscaler test: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def test_clarity_with_generator():
    """Test Clarity Upscaler using the generator class."""
    print("\n🎨 Testing Clarity Upscaler with Generator Class...")
    
    try:
        # Add parent directory to path
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from fal_image_to_image import FALImageToImageGenerator
        
        # Initialize generator
        generator = FALImageToImageGenerator()
        print("✅ Generator initialized")
        
        # Test image path
        image_path = "../input/death.jpeg"
        
        # Test 1: Basic upscaling
        print("\n📊 Test 1: Basic 2x upscaling with enhancement")
        result1 = generator.upscale_local_image(
            image_path=image_path,
            scale=2,
            enable_enhancement=True,
            prompt="enhance details, improve quality"
        )
        
        if result1.get("success"):
            print("✅ Test 1 passed: Basic upscaling successful")
        else:
            print("❌ Test 1 failed:", result1.get("error"))
        
        # Test 2: 4x upscaling without enhancement
        print("\n📊 Test 2: 4x upscaling without enhancement")
        result2 = generator.upscale_local_image(
            image_path=image_path,
            scale=4,
            enable_enhancement=False
        )
        
        if result2.get("success"):
            print("✅ Test 2 passed: 4x upscaling successful")
        else:
            print("❌ Test 2 failed:", result2.get("error"))
        
        # Test 3: Get model info
        print("\n📊 Test 3: Get Clarity model info")
        info = generator.get_model_info("clarity")
        print("✅ Model info retrieved:")
        print(f"   Name: {info.get('model_name')}")
        print(f"   Description: {info.get('description')}")
        print(f"   Features: {', '.join(info.get('features', []))}")
        
        return {
            "test1": result1,
            "test2": result2,
            "model_info": info
        }
        
    except Exception as e:
        print(f"❌ Error during generator test: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def main():
    """Main test function."""
    print("🧪 FAL AI Clarity Upscaler Test")
    print("=" * 50)
    
    # Print cost warning and get confirmation
    print_cost_warning()
    
    # Test Clarity Upscaler model directly
    result = test_clarity_upscaler()
    
    # Test with generator class
    print("\n" + "=" * 50)
    generator_results = test_clarity_with_generator()
    
    # Print final results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("-" * 25)
    
    if result.get("success"):
        print("✅ Direct API Test: PASSED")
        
        # Check generator tests
        if generator_results.get("test1", {}).get("success") and generator_results.get("test2", {}).get("success"):
            print("✅ Generator Tests: PASSED")
            print("🎉 All tests completed successfully!")
        else:
            print("❌ Generator Tests: FAILED")
    else:
        print("❌ Direct API Test: FAILED")
        print(f"💥 Error: {result.get('error', 'Unknown error')}")
        print("🔧 Check your API key and account balance")
    
    # Show output files
    output_dir = "../output"
    if os.path.exists(output_dir):
        output_files = [f for f in os.listdir(output_dir) if f.startswith('clarity_upscaled_')]
        if output_files:
            print(f"\n📁 Generated files in {output_dir}/:")
            for file in output_files:
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"   🖼️  {file} ({file_size:,} bytes)")
    
    print("\n💡 Test completed!")

if __name__ == "__main__":
    main()