#!/usr/bin/env python3
"""
FAL Text-to-Video Generation Test (COSTS MONEY - ~$0.08 per video)

⚠️ WARNING: This script will generate actual videos and incur API costs!
Each video generation costs approximately $0.08.

Only run this script when you're ready to test actual video generation.
Run test_setup.py first to validate your configuration for free.
"""

import sys
import time
from pathlib import Path

def main():
    """Test actual video generation with cost warnings."""
    print("⚠️ FAL Text-to-Video Generation Test")
    print("💰 WARNING: This will incur API costs!")
    print("=" * 60)
    print("💵 Cost: ~$0.08 per video generated")
    print("📹 Each test generates 1080p videos (6 seconds)")
    print("🚫 Run test_setup.py first for FREE validation")
    print("=" * 60)
    
    # Get user confirmation
    response = input("\nDo you want to proceed with paid video generation? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Test cancelled. No charges incurred.")
        print("💡 Run test_setup.py for free setup validation")
        return
    
    print("\n🔄 Starting video generation tests...")
    
    try:
        from fal_text_to_video_generator import FALTextToVideoGenerator
        
        # Initialize generator
        generator = FALTextToVideoGenerator(verbose=True)
        
        # Print model info
        print("\n🎬 Model Information:")
        generator.print_model_info()
        
        # Test 1: Simple video generation
        print(f"\n{'='*20} Test 1: Simple Generation {'='*20}")
        print("💰 Cost: ~$0.08")
        
        result1 = generator.generate_video(
            prompt="A peaceful cat sitting by a window watching raindrops",
            prompt_optimizer=True,
            output_filename="test_simple_generation.mp4"
        )
        
        if result1['success']:
            print(f"✅ Test 1 PASSED: {result1['local_path']}")
        else:
            print(f"❌ Test 1 FAILED: {result1['error']}")
        
        # Test 2: Different prompt style
        print(f"\n{'='*20} Test 2: Complex Scene {'='*20}")
        print("💰 Cost: ~$0.08")
        
        result2 = generator.generate_video(
            prompt="A futuristic city skyline at night with flying cars and neon lights",
            prompt_optimizer=True,
            output_filename="test_complex_scene.mp4"
        )
        
        if result2['success']:
            print(f"✅ Test 2 PASSED: {result2['local_path']}")
        else:
            print(f"❌ Test 2 FAILED: {result2['error']}")
        
        # Test 3: Batch generation (optional)
        batch_response = input("\nRun batch test (2 more videos, ~$0.16)? (yes/no): ").strip().lower()
        if batch_response in ['yes', 'y']:
            print(f"\n{'='*20} Test 3: Batch Generation {'='*20}")
            print("💰 Cost: ~$0.16 (2 videos)")
            
            prompts = [
                "A butterfly landing on a blooming flower in slow motion",
                "Ocean waves crashing against rocky cliffs at sunrise"
            ]
            
            batch_results = generator.generate_batch(
                prompts=prompts,
                prompt_optimizer=True
            )
            
            successful_batch = sum(1 for r in batch_results.values() if r['success'])
            print(f"✅ Batch test: {successful_batch}/{len(prompts)} videos generated")
        
        # Summary
        tests_run = 2 + (1 if batch_response in ['yes', 'y'] else 0)
        estimated_cost = 0.08 * (2 + (2 if batch_response in ['yes', 'y'] else 0))
        
        print(f"\n{'='*60}")
        print("📊 Generation Test Summary")
        print("=" * 60)
        print(f"🧪 Tests run: {tests_run}")
        print(f"💰 Estimated cost: ~${estimated_cost:.2f}")
        print(f"📁 Output directory: {Path('output').absolute()}")
        
        # Check output files
        output_dir = Path("output")
        video_files = list(output_dir.glob("*.mp4"))
        print(f"📹 Videos generated: {len(video_files)}")
        
        for video_file in video_files:
            if video_file.name.startswith("test_"):
                file_size = video_file.stat().st_size / (1024 * 1024)  # MB
                print(f"   • {video_file.name} ({file_size:.1f} MB)")
        
        print("\n🎉 Generation tests completed!")
        print("💡 Check the output/ directory for generated videos")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Run: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Run test_setup.py first to validate configuration")

if __name__ == "__main__":
    main()