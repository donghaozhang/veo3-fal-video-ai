#!/usr/bin/env python3
"""
Simple Hailuo Video Generation Test
Tests FAL AI MiniMax Hailuo-02 model with specific image and prompt
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fal_image_to_video_generator import FALImageToVideoGenerator

def main():
    """Test Hailuo video generation with specific image and prompt"""
    
    print("🎬 Simple Hailuo Video Generation Test")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if FAL_KEY exists
    fal_key = os.getenv('FAL_KEY')
    if not fal_key:
        print("❌ FAL_KEY not found in environment variables")
        print("💡 Make sure .env file exists with FAL_KEY=your_api_key")
        return
    
    print(f"✅ FAL_KEY loaded: {fal_key[:20]}...")
    
    # Initialize generator
    try:
        generator = FALImageToVideoGenerator()
        print("✅ FALImageToVideoGenerator initialized")
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        return
    
    # Define image and prompt files
    image_path = "input/horror_poster_strart_notext.jpg"
    prompt_file = "input/horror_poster_starter_nontext.txt"
    
    # Check if files exist
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return
    
    if not os.path.exists(prompt_file):
        print(f"❌ Prompt file not found: {prompt_file}")
        return
    
    print(f"✅ Image file found: {image_path}")
    print(f"✅ Prompt file found: {prompt_file}")
    
    # Read prompt from file
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
        print(f"✅ Prompt loaded ({len(prompt)} characters)")
        print(f"📝 Prompt: {prompt[:100]}...")
    except Exception as e:
        print(f"❌ Failed to read prompt file: {e}")
        return
    
    # Generate video
    print("\n🎯 Starting video generation...")
    print(f"🖼️  Image: {image_path}")
    print(f"📝 Prompt: {prompt}")
    print(f"⏱️  Duration: 6 seconds")
    print(f"🤖 Model: MiniMax Hailuo-02")
    print(f"💰 Estimated cost: ~$0.02-0.05")
    
    # Confirm before proceeding
    response = input(f"\n⚠️  This will generate a real video. Continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Test cancelled")
        return
    
    try:
        # Generate video using Hailuo model
        result = generator.generate_video_from_local_image(
            prompt=prompt,
            image_path=image_path,
            duration="6",
            model="fal-ai/minimax/hailuo-02/standard/image-to-video"
        )
        
        if result:
            print("\n✅ Video generation successful!")
            print(f"📹 Video URL: {result.get('video_url', 'N/A')}")
            print(f"🎯 Task ID: {result.get('task_id', 'N/A')}")
            
            # Check if video was downloaded
            output_files = []
            if os.path.exists('output'):
                for file in os.listdir('output'):
                    if file.endswith('.mp4'):
                        output_files.append(file)
            
            if output_files:
                print(f"⬇️  Downloaded videos:")
                for file in output_files:
                    file_path = os.path.join('output', file)
                    file_size = os.path.getsize(file_path)
                    print(f"   📁 {file} ({file_size:,} bytes)")
            else:
                print("⚠️  No video files found in output directory")
                
        else:
            print("❌ Video generation failed")
            
    except Exception as e:
        print(f"❌ Error during video generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()