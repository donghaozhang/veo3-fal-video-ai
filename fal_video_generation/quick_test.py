#!/usr/bin/env python3
"""
Quick test to verify video generation is working
"""

from fal_video_generator import FALVideoGenerator
import os
from dotenv import load_dotenv

def main():
    print("🎬 Testing FAL AI Video Generation")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    
    try:
        # Initialize generator
        generator = FALVideoGenerator()
        print("✅ FALVideoGenerator initialized successfully")
        
        # Test with a simple publicly accessible image
        print("🧪 Testing video generation with a test image...")
        
        result = generator.generate_video_from_image(
            image_url="https://picsum.photos/512/512",
            prompt="A beautiful landscape with moving clouds",
            duration="6"
        )
        
        if result and 'video' in result:
            video_url = result['video'].get('url', 'No URL found')
            print(f"✅ Video generation successful!")
            print(f"📹 Video URL: {video_url}")
            print(f"🎯 Duration: {result.get('duration', 'Unknown')} seconds")
            print(f"📐 Resolution: {result.get('width', '?')}x{result.get('height', '?')}")
            
            # Try to download the video
            if video_url and video_url != 'No URL found':
                print("⬇️  Attempting to download video...")
                local_path = generator.download_video(video_url, "test_output", "test_video.mp4")
                if local_path:
                    print(f"✅ Video downloaded to: {local_path}")
                else:
                    print("⚠️  Video download failed")
            
        else:
            print("❌ Video generation failed")
            print("Response:", result)
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main() 