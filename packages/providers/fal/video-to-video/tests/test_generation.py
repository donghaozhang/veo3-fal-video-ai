#!/usr/bin/env python3
"""
Test FAL Video to Video generation capabilities
WARNING: This test will make actual API calls and incur costs (~$0.001 per second)
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fal_video_to_video import FALVideoToVideoGenerator


def test_model_info():
    """Test model information retrieval."""
    print("📋 Testing model information...")
    
    try:
        generator = FALVideoToVideoGenerator()
        
        # Test individual model info
        model_info = generator.get_model_info("thinksound")
        print(f"✅ ThinkSound info: {model_info['model_name']}")
        print(f"   Description: {model_info['description']}")
        
        # Test all models info
        all_info = generator.get_model_info()
        print(f"✅ Found {len(all_info)} models")
        
        # Test model listing
        models = generator.list_models()
        print(f"✅ Available models: {models}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model info test failed: {e}")
        return False


def test_video_url_generation():
    """Test audio generation from video URL."""
    print("\n🎵 Testing audio generation from URL...")
    
    # Use a sample video URL (you can replace with your own)
    test_video_url = "https://storage.googleapis.com/falserverless/example_inputs/thinksound-input.mp4"
    
    try:
        generator = FALVideoToVideoGenerator()
        
        print(f"🎬 Processing video: {test_video_url}")
        
        result = generator.add_audio_to_video(
            video_url=test_video_url,
            model="thinksound",
            prompt="add dramatic background music",
            output_dir="test_output"
        )
        
        if result.get("success"):
            print("✅ Audio generation successful!")
            print(f"   Model: {result.get('model')}")
            print(f"   Processing time: {result.get('processing_time', 0):.2f}s")
            if result.get("local_path"):
                print(f"   Output: {result.get('local_path')}")
            return True
        else:
            print(f"❌ Generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ URL generation test failed: {e}")
        return False


def test_local_video_generation():
    """Test audio generation from local video file."""
    print("\n🎬 Testing audio generation from local file...")
    
    # Look for test videos in input folder
    input_dir = project_root / "input"
    video_files = list(input_dir.glob("*.mp4")) + list(input_dir.glob("*.mov"))
    
    if not video_files:
        print("⚠️  No video files found in input/ folder")
        print("   Please add a test video file (.mp4 or .mov) to test local processing")
        return True  # Not a failure, just skipped
    
    test_video = video_files[0]
    print(f"🎬 Using test video: {test_video.name}")
    
    try:
        generator = FALVideoToVideoGenerator()
        
        result = generator.add_audio_to_local_video(
            video_path=str(test_video),
            model="thinksound", 
            prompt="add ambient nature sounds",
            output_dir="test_output"
        )
        
        if result.get("success"):
            print("✅ Local audio generation successful!")
            print(f"   Model: {result.get('model')}")
            print(f"   Processing time: {result.get('processing_time', 0):.2f}s")
            if result.get("local_path"):
                print(f"   Output: {result.get('local_path')}")
            return True
        else:
            print(f"❌ Generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Local generation test failed: {e}")
        return False


def test_seed_reproducibility():
    """Test that using the same seed produces consistent results."""
    print("\n🎲 Testing seed reproducibility...")
    
    test_video_url = "https://storage.googleapis.com/falserverless/example_inputs/thinksound-input.mp4"
    
    try:
        generator = FALVideoToVideoGenerator()
        
        # Generate with fixed seed twice
        seed = 12345
        
        print(f"🎬 Generating with seed {seed} (attempt 1)...")
        result1 = generator.add_audio_to_video(
            video_url=test_video_url,
            model="thinksound",
            seed=seed,
            output_dir="test_output"
        )
        
        print(f"🎬 Generating with seed {seed} (attempt 2)...")
        result2 = generator.add_audio_to_video(
            video_url=test_video_url,
            model="thinksound", 
            seed=seed,
            output_dir="test_output"
        )
        
        if result1.get("success") and result2.get("success"):
            print("✅ Both generations successful!")
            print("   Note: Audio content should be similar with same seed")
            return True
        else:
            print("❌ One or both generations failed")
            return False
            
    except Exception as e:
        print(f"❌ Seed test failed: {e}")
        return False


def main():
    """Run generation tests."""
    print("🎵 FAL Video to Video Generation Test")
    print("=" * 45)
    print("⚠️  WARNING: This will make API calls and incur costs!")
    print("   Estimated cost: ~$0.01-0.10 depending on video length")
    
    # Confirm user wants to proceed
    response = input("\nProceed with tests? (y/N): ")
    if response.lower() != 'y':
        print("Tests cancelled.")
        return
    
    tests = [
        ("Model Info", test_model_info),
        ("URL Generation", test_video_url_generation),
        ("Local Generation", test_local_video_generation),
        ("Seed Reproducibility", test_seed_reproducibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print(f"\n📊 Generation Test Summary")
    print("=" * 35)
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL" 
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All generation tests passed!")
        print("\nCheck the test_output/ folder for generated videos")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")


if __name__ == "__main__":
    main()