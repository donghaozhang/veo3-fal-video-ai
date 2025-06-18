#!/usr/bin/env python3
"""
Simple demo script for FAL AI MiniMax Hailuo-02 Video Generation
"""

import os
import sys
from fal_video_generator import FALVideoGenerator

def main():
    """
    Run a simple demo of FAL AI video generation
    """
    print("🎬 FAL AI MiniMax Hailuo-02 Video Generation Demo")
    print("=" * 50)
    
    try:
        # Check if API key is available
        api_key = os.getenv('FAL_KEY')
        if not api_key:
            print("❌ Error: FAL_KEY environment variable not set!")
            print("Please set your FAL AI API key in the .env file")
            return
        
        # Initialize generator
        print("🔧 Initializing FAL Video Generator...")
        generator = FALVideoGenerator()
        print("✅ Generator initialized successfully!")
        
        # Demo 1: Generate from online image
        print("\n🎯 Demo 1: Generate video from online image")
        print("-" * 40)
        
        result = generator.generate_video_from_image(
            prompt="A man walks into a winter cave with a polar bear, cinematic lighting, dramatic atmosphere",
            image_url="https://storage.googleapis.com/falserverless/model_tests/minimax/1749891352437225630-389852416840474630_1749891352.png",
            duration="6",
            output_folder="demo_output"
        )
        
        if result:
            print("🎉 Success! Video generated:")
            print(f"   📹 Video URL: {result['video']['url']}")
            print(f"   💾 File size: {result['video']['file_size']} bytes")
            if 'local_path' in result:
                print(f"   📁 Local path: {result['local_path']}")
        else:
            print("❌ Failed to generate video from online image")
        
        # Demo 2: Generate from local image (if available)
        local_image_path = "../images/smiling_woman.jpg"
        if os.path.exists(local_image_path):
            print("\n🎯 Demo 2: Generate video from local image")
            print("-" * 40)
            
            result2 = generator.generate_video_from_local_image(
                prompt="A smiling woman in a beautiful garden, gentle breeze moving her hair, warm sunlight",
                image_path=local_image_path,
                duration="6",
                output_folder="demo_output"
            )
            
            if result2:
                print("🎉 Success! Video generated from local image:")
                print(f"   📹 Video URL: {result2['video']['url']}")
                print(f"   💾 File size: {result2['video']['file_size']} bytes")
                if 'local_path' in result2:
                    print(f"   📁 Local path: {result2['local_path']}")
            else:
                print("❌ Failed to generate video from local image")
        else:
            print(f"\n⚠️  Demo 2 skipped: Local image not found at {local_image_path}")
        
        print("\n✨ Demo completed!")
        print("Check the 'demo_output' folder for generated videos.")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 