#!/usr/bin/env python3
"""
FAL AI FLUX Pro Kontext Model Test
Tests fal-ai/flux-pro/kontext model with death.jpeg image

This script tests the FLUX Pro Kontext model specifically.
⚠️ WARNING: This script WILL INCUR COSTS when run!

Usage:
    python test_flux_kontext.py

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
    print("💰 Model: fal-ai/flux-pro/kontext")
    print("💰 Estimated cost: $0.01-0.05 per image modification")
    print("💰 Make sure you have credits in your FAL AI account")
    print("⚠️" * 20)
    
    # Check for --yes flag to skip confirmation
    if '--yes' in sys.argv:
        print("\n✅ Auto-confirmed with --yes flag")
        print("✅ Proceeding with FLUX Pro Kontext test...")
        return
    
    response = input("\n❓ Do you want to continue and incur charges? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Test cancelled by user")
        sys.exit(0)
    
    print("✅ Proceeding with FLUX Pro Kontext test...")

def test_flux_kontext() -> Dict[str, Any]:
    """Test FLUX Pro Kontext model with flux_kontext_death_1751335665.png."""
    print("\n🎨 Testing FLUX Pro Kontext Model...")
    print("🖼️  Image: input/flux_kontext_death_1751335665.png")
    print("🤖 Model: fal-ai/flux-pro/kontext")
    
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
        image_path = "input/flux_kontext_death_1751335665.png"
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return {"success": False, "error": "Image file not found"}
        
        print(f"✅ Image found: {image_path}")
        
        # Upload image to FAL
        print("📤 Uploading image to FAL...")
        image_url = fal_client.upload_file(image_path)
        print(f"✅ Image uploaded: {image_url}")
        
        # Test prompt for death/horror theme transformation
        prompt = "Remove text and symbol at top left of image"
        
        print(f"📝 Prompt: {prompt}")
        
        # Test with exact FLUX Pro Kontext endpoint
        print("\n🚀 Starting image transformation...")
        print("🔗 Endpoint: fal-ai/flux-pro/kontext")
        
        result = fal_client.subscribe(
            "fal-ai/flux-pro/kontext",
            arguments={
                "prompt": prompt,
                "image_url": image_url
            }
        )
        
        if result and 'images' in result:
            print("\n✅ FLUX Pro Kontext transformation successful!")
            
            # Get the first image result
            images = result.get('images', [])
            if images:
                image_result = images[0]
                image_url_result = image_result.get('url', 'N/A')
                print(f"📹 Result URL: {image_url_result}")
                
                # Download the image
                if image_url_result != 'N/A':
                    print("⬇️  Downloading result image...")
                    
                    # Create output directory if it doesn't exist
                    output_dir = "output"
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Download image
                    import requests
                    response = requests.get(image_url_result)
                    if response.status_code == 200:
                        # Generate filename
                        import time
                        timestamp = int(time.time())
                        output_filename = f"flux_kontext_death_{timestamp}.png"
                        output_path = os.path.join(output_dir, output_filename)
                        
                        with open(output_path, 'wb') as f:
                            f.write(response.content)
                        
                        file_size = os.path.getsize(output_path)
                        print(f"✅ Image downloaded: {output_path}")
                        print(f"📊 File size: {file_size:,} bytes")
                        
                        return {
                            "success": True,
                            "model": "fal-ai/flux-pro/kontext",
                            "image_url": image_url_result,
                            "local_path": output_path,
                            "file_size": file_size,
                            "result": result
                        }
                    else:
                        print(f"❌ Failed to download image: HTTP {response.status_code}")
            
            return {
                "success": True,
                "model": "fal-ai/flux-pro/kontext",
                "result": result
            }
        else:
            print(f"❌ FLUX Pro Kontext transformation failed: {result}")
            return {"success": False, "error": "Transformation failed", "result": result}
            
    except Exception as e:
        print(f"❌ Error during FLUX Pro Kontext test: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def main():
    """Main test function."""
    print("🧪 FAL AI FLUX Pro Kontext Model Test")
    print("=" * 50)
    
    # Print cost warning and get confirmation
    print_cost_warning()
    
    # Test FLUX Pro Kontext model
    result = test_flux_kontext()
    
    # Print final results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("-" * 25)
    
    if result.get("success"):
        print("✅ FLUX Pro Kontext Test: PASSED")
        print("🎉 All tests completed successfully!")
        
        # Show output files
        output_dir = "output"
        if os.path.exists(output_dir):
            output_files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if output_files:
                print(f"\n📁 Generated files in {output_dir}/:")
                for file in output_files:
                    file_path = os.path.join(output_dir, file)
                    file_size = os.path.getsize(file_path)
                    print(f"   🖼️  {file} ({file_size:,} bytes)")
    else:
        print("❌ FLUX Pro Kontext Test: FAILED")
        print(f"💥 Error: {result.get('error', 'Unknown error')}")
        print("🔧 Check your API key and account balance")
    
    print("\n💡 Test completed!")

if __name__ == "__main__":
    main()