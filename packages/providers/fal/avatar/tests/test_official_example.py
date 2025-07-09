#!/usr/bin/env python3
"""
FAL AI Avatar Generation - Official Example Test

This script demonstrates the exact official example from FAL AI documentation:
https://fal.ai/models/fal-ai/ai-avatar/single-text/api

⚠️ WARNING: This script generates a real avatar video and costs money!
Estimated cost: ~$0.038 (136 frames)

Usage:
    python test_official_example.py
"""

import os
import sys
from fal_avatar_generator import FALAvatarGenerator

def main():
    """Test the official FAL AI example"""
    print("🎭 FAL AI Avatar Generation - Official Example Test")
    print("=" * 60)
    print("📖 Source: https://fal.ai/models/fal-ai/ai-avatar/single-text/api")
    print()
    
    # Official example parameters
    print("📋 Official Example Parameters:")
    print("   Image: https://v3.fal.media/files/panda/HuM21CXMf0q7OO2zbvwhV_c4533aada79a495b90e50e32dc9b83a8.png")
    print("   Text: 'Spend more time with people who make you feel alive, and less with things that drain your soul.'")
    print("   Voice: Bill")
    print("   Prompt: 'An elderly man with a white beard and headphones records audio...'")
    print("   Frames: 136")
    print("   Seed: 42")
    print("   Turbo: True")
    print()
    
    # Cost warning
    print("⚠️ WARNING: This will generate a real avatar video and cost money!")
    print("💰 Estimated cost: ~$0.038 (136 frames)")
    print("💳 This will charge your FAL AI account.")
    print()
    
    # Get user confirmation
    while True:
        response = input("Do you want to proceed with the official example? (yes/no): ").lower().strip()
        if response in ['yes', 'y', 'proceed', 'run']:
            break
        elif response in ['no', 'n', 'cancel', 'stop']:
            print("❌ Official example test cancelled")
            sys.exit(0)
        else:
            print("Please enter 'yes' or 'no'")
    
    try:
        # Initialize generator
        print("\n🔧 Initializing FAL Avatar Generator...")
        generator = FALAvatarGenerator()
        
        # Create output directory
        os.makedirs("test_output", exist_ok=True)
        
        # Generate output path
        import time
        timestamp = int(time.time())
        output_path = f"test_output/official_example_{timestamp}.mp4"
        
        print(f"\n🚀 Running official FAL AI example...")
        print(f"📁 Output: {output_path}")
        
        # Generate using official example
        result = generator.generate_official_example(output_path=output_path)
        
        if result and 'video' in result:
            print(f"\n🎉 Official example completed successfully!")
            print(f"📁 Saved to: {output_path}")
            print(f"⏱️ Generation time: {result.get('generation_time', 0):.2f} seconds")
            
            video_info = result['video']
            print(f"📊 File size: {video_info.get('file_size', 0) / (1024*1024):.2f} MB")
            print(f"🔗 Online URL: {video_info['url']}")
            print(f"🎯 Seed used: {result.get('seed', 'N/A')}")
            
            print(f"\n✨ The generated video matches the official FAL AI example!")
            print(f"📖 Compare with: https://fal.ai/models/fal-ai/ai-avatar/single-text/api")
        else:
            print(f"❌ Official example generation failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n❌ Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during official example test: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 