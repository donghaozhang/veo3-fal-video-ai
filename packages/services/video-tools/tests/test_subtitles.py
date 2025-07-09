#!/usr/bin/env python3
"""
Test script for subtitle functionality in video_audio_utils.py

This script tests the subtitle generation and video overlay functions.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path so we can import video_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_utils import (
    generate_srt_subtitle_file,
    generate_vtt_subtitle_file, 
    generate_subtitle_for_video,
    add_subtitles_to_video, 
    add_text_subtitles_to_video,
    check_ffmpeg,
    get_video_info
)

def test_srt_generation():
    """Test SRT subtitle file generation."""
    print("🧪 Testing SRT subtitle file generation...")
    
    test_text = """Hello, this is a test subtitle.
This is the second line of subtitles.
And this is the third line."""
    
    output_path = Path("output/test_subtitles.srt")
    output_path.parent.mkdir(exist_ok=True)
    
    # Test with automatic duration
    success = generate_srt_subtitle_file(test_text, output_path, duration=None, words_per_second=2.0)
    
    if success and output_path.exists():
        print("✅ SRT subtitle file generated successfully")
        print(f"📄 Content preview:")
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content[:300] + "..." if len(content) > 300 else content)
        return True
    else:
        print("❌ Failed to generate SRT subtitle file")
        return False

def test_vtt_generation():
    """Test WebVTT subtitle file generation."""
    print("\n🧪 Testing WebVTT subtitle file generation...")
    
    test_text = """Welcome to the WebVTT test.
This format is perfect for web players.
It supports styling and positioning."""
    
    output_path = Path("output/test_subtitles.vtt")
    output_path.parent.mkdir(exist_ok=True)
    
    # Test with automatic duration
    success = generate_vtt_subtitle_file(test_text, output_path, duration=15.0, words_per_second=1.5)
    
    if success and output_path.exists():
        print("✅ WebVTT subtitle file generated successfully")
        print(f"📄 Content preview:")
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content[:300] + "..." if len(content) > 300 else content)
        return True
    else:
        print("❌ Failed to generate WebVTT subtitle file")
        return False

def test_video_subtitle_generation():
    """Test generating subtitle files for actual videos."""
    print("\n🧪 Testing subtitle file generation for videos...")
    
    # Look for sample video
    sample_video = Path("samples/sample_video.mp4")
    
    if not sample_video.exists():
        print(f"⚠️  Sample video not found: {sample_video}")
        print("💡 Place a test video at 'samples/sample_video.mp4' to test")
        return False
    
    # Get video info
    info = get_video_info(sample_video)
    print(f"📹 Video info: {info['duration']:.1f}s, Audio: {info['has_audio']}")
    
    test_text = """Welcome to this test video.
This demonstrates subtitle functionality.
The text should appear synchronized with the video duration.
You can load this subtitle file in any video player."""
    
    # Test SRT generation for video
    srt_path = generate_subtitle_for_video(
        sample_video, 
        test_text, 
        format_type="srt",
        words_per_second=1.5
    )
    
    # Test VTT generation for video
    vtt_path = generate_subtitle_for_video(
        sample_video, 
        test_text, 
        format_type="vtt",
        words_per_second=1.5
    )
    
    if srt_path and srt_path.exists() and vtt_path and vtt_path.exists():
        print("✅ Both SRT and VTT subtitle files created successfully")
        print(f"📄 Files created:")
        print(f"   - {srt_path.name}")
        print(f"   - {vtt_path.name}")
        print("💡 Load these files in your video player alongside the video")
        return True
    else:
        print("❌ Failed to generate subtitle files for video")
        return False

def test_subtitle_validation():
    """Test subtitle file format validation."""
    print("\n🧪 Testing subtitle file format validation...")
    
    # Test SRT format validation
    srt_path = Path("output/test_subtitles.srt")
    if srt_path.exists():
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check SRT format markers
        has_numbers = any(line.strip().isdigit() for line in content.split('\n'))
        has_timestamps = '-->' in content
        has_commas = ',' in content  # SRT uses commas for milliseconds
        
        if has_numbers and has_timestamps and has_commas:
            print("✅ SRT format validation passed")
            srt_valid = True
        else:
            print("❌ SRT format validation failed")
            srt_valid = False
    else:
        print("⚠️  No SRT file to validate")
        srt_valid = False
    
    # Test VTT format validation
    vtt_path = Path("output/test_subtitles.vtt")
    if vtt_path.exists():
        with open(vtt_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check VTT format markers
        has_webvtt = content.startswith('WEBVTT')
        has_timestamps = '-->' in content
        has_dots = ':' in content and '.' in content  # VTT uses dots for milliseconds
        
        if has_webvtt and has_timestamps and has_dots:
            print("✅ WebVTT format validation passed")
            vtt_valid = True
        else:
            print("❌ WebVTT format validation failed")
            vtt_valid = False
    else:
        print("⚠️  No WebVTT file to validate")
        vtt_valid = False
    
    return srt_valid and vtt_valid

def main():
    """Run all subtitle tests."""
    print("📝 STANDALONE SUBTITLE FUNCTIONALITY TESTS")
    print("=" * 50)
    print("💡 Testing subtitle file generation for video players")
    
    # Check requirements
    print("\n🔧 Checking requirements...")
    if not check_ffmpeg():
        print("❌ Error: ffmpeg is not installed or not in PATH")
        print("📥 Please install ffmpeg to run video tests")
        print("💡 Subtitle generation works without ffmpeg")
    else:
        print("✅ ffmpeg found")
    
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    if test_srt_generation():
        tests_passed += 1
    
    if test_vtt_generation():
        tests_passed += 1
    
    if test_subtitle_validation():
        tests_passed += 1
    
    if test_video_subtitle_generation():
        tests_passed += 1
    
    # Summary
    print(f"\n📊 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Subtitle functionality is working correctly.")
    elif tests_passed >= 3:
        print("✅ Core functionality working! Video tests may need sample video.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\n💡 To generate subtitles for your videos:")
    print("   1. Place video files in the current directory")
    print("   2. Run: python video_audio_utils.py generate-subtitles")
    print("   3. Follow the interactive prompts")
    print("   4. Load the generated .srt/.vtt files in your video player")
    
    print("\n📺 Supported video players:")
    print("   - VLC Media Player (auto-loads same-name subtitle files)")
    print("   - Windows Media Player")
    print("   - Web browsers (for .vtt files)")
    print("   - Most modern video players")

if __name__ == "__main__":
    main()