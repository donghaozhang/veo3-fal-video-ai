#!/usr/bin/env python3
"""
FAL AI Seedream v3 Model Test

Tests the Seedream v3 model specifically.
⚠️ WARNING: This script WILL INCUR COSTS when run!

Usage:
    python test_seedream.py
    python test_seedream.py --yes  # Skip confirmation

Author: AI Assistant
Date: 2024
"""

import os
import sys
from typing import Dict, Any

# Add parent directory to path to import the generator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fal_text_to_image_generator import FALTextToImageGenerator

def print_cost_warning():
    """Print cost warning and get user confirmation."""
    print("⚠️" * 20)
    print("💰 COST WARNING: This script will incur charges!")
    print("💰 Model: Seedream v3")
    print("💰 Estimated cost: ~$0.015 per image")
    print("💰 Make sure you have credits in your FAL AI account")
    print("⚠️" * 20)
    
    # Check for --yes flag to skip confirmation
    if '--yes' in sys.argv:
        print("\n✅ Auto-confirmed with --yes flag")
        print("✅ Proceeding with Seedream test...")
        return
    
    response = input("\n❓ Do you want to continue and incur charges? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Test cancelled by user")
        sys.exit(0)
    
    print("✅ Proceeding with Seedream test...")

def test_seedream_generation() -> Dict[str, Any]:
    """Test Seedream v3 model."""
    print("\n🎨 Testing Seedream v3 Model...")
    print("🤖 Model: seedream")
    
    try:
        # Initialize generator
        generator = FALTextToImageGenerator()
        
        # Test prompt (supports bilingual)
        prompt = "一条威严的中国龙在云雾中飞翔，传统水墨画风格 (A majestic Chinese dragon flying through clouds, traditional ink painting style)"
        
        print(f"📝 Prompt: {prompt}")
        print("🚀 Starting image generation...")
        
        result = generator.generate_seedream(
            prompt=prompt,
            output_dir="output"
        )
        
        if result.get("success"):
            print("\n✅ Seedream generation successful!")
            print(f"📊 Processing time: {result.get('processing_time', 'N/A')} seconds")
            print(f"📁 Images generated: {len(result.get('downloaded_files', []))}")
            
            # Show file details
            for file_path in result.get('downloaded_files', []):
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"   🖼️  {os.path.basename(file_path)} ({file_size:,} bytes)")
            
            return result
        else:
            print(f"\n❌ Seedream generation failed!")
            print(f"💥 Error: {result.get('error', 'Unknown error')}")
            return result
            
    except Exception as e:
        print(f"\n❌ Error during Seedream test: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def main():
    """Main test function."""
    print("🧪 FAL AI Seedream v3 Model Test")
    print("=" * 50)
    
    # Print cost warning and get confirmation
    print_cost_warning()
    
    # Test Seedream model
    result = test_seedream_generation()
    
    # Print final results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("-" * 25)
    
    if result.get("success"):
        print("✅ Seedream Test: PASSED")
        print("🎉 Image generation completed successfully!")
        
        # Show output files
        output_dir = "output"
        if os.path.exists(output_dir):
            output_files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if output_files:
                print(f"\n📁 Generated files in {output_dir}/:")
                for file in output_files[-3:]:  # Show last 3 files
                    file_path = os.path.join(output_dir, file)
                    file_size = os.path.getsize(file_path)
                    print(f"   🖼️  {file} ({file_size:,} bytes)")
    else:
        print("❌ Seedream Test: FAILED")
        print(f"💥 Error: {result.get('error', 'Unknown error')}")
        print("🔧 Check your API key and account balance")
    
    print("\n💡 Test completed!")

if __name__ == "__main__":
    main()