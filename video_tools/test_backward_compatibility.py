#!/usr/bin/env python3
"""Test backward compatibility of function-based imports."""

import sys
from pathlib import Path

# Add video_utils to Python path
sys.path.insert(0, str(Path(__file__).parent / "video_utils"))

def test_legacy_imports():
    """Test that all legacy function imports work."""
    print("🔄 Testing Backward Compatibility")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 0
    
    # Test core utilities
    try:
        from video_utils import check_ffmpeg, check_ffprobe, get_video_info
        print("✅ Core utilities import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Core utilities import failed: {e}")
    tests_total += 1
    
    # Test file utilities
    try:
        from video_utils import find_video_files, find_audio_files, find_image_files
        print("✅ File utilities import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ File utilities import failed: {e}")
    tests_total += 1
    
    # Test video processing
    try:
        from video_utils import cut_video_duration
        print("✅ Video processing import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Video processing import failed: {e}")
    tests_total += 1
    
    # Test audio processing
    try:
        from video_utils import (
            add_audio_to_video, 
            extract_audio_from_video,
            mix_multiple_audio_files,
            concatenate_multiple_audio_files
        )
        print("✅ Audio processing import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Audio processing import failed: {e}")
    tests_total += 1
    
    # Test subtitle generation
    try:
        from video_utils import (
            generate_srt_subtitle_file,
            generate_vtt_subtitle_file,
            generate_subtitle_for_video,
            add_subtitles_to_video,
            add_text_subtitles_to_video
        )
        print("✅ Subtitle generation import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Subtitle generation import failed: {e}")
    tests_total += 1
    
    # Test interactive utilities
    try:
        from video_utils import interactive_audio_selection, interactive_multiple_audio_selection
        print("✅ Interactive utilities import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Interactive utilities import failed: {e}")
    tests_total += 1
    
    # Test AI analysis
    try:
        from video_utils import (
            analyze_video_file, 
            analyze_audio_file,
            analyze_image_file,
            save_analysis_result,
            GeminiVideoAnalyzer,
            check_gemini_requirements,
            transcribe_with_whisper,
            batch_transcribe_whisper,
            WhisperTranscriber,
            check_whisper_requirements
        )
        print("✅ AI analysis import successful")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ AI analysis import failed: {e}")
    tests_total += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Backward Compatibility Results: {tests_passed}/{tests_total} passed")
    
    if tests_passed == tests_total:
        print("🎉 All legacy imports work correctly!")
        return True
    else:
        print(f"⚠️ {tests_total - tests_passed} import(s) failed")
        return False

def test_legacy_functionality():
    """Test that legacy functions actually work."""
    print("\n🔧 Testing Legacy Function Calls")
    print("=" * 50)
    
    # Test basic function calls (without actual processing)
    try:
        from video_utils import check_ffmpeg, find_video_files
        
        # Test dependency check
        ffmpeg_available = check_ffmpeg()
        print(f"✅ check_ffmpeg() works: {ffmpeg_available}")
        
        # Test file finding
        input_dir = Path("input")
        if input_dir.exists():
            video_files = find_video_files(input_dir)
            print(f"✅ find_video_files() works: found {len(video_files)} files")
        else:
            print("ℹ️ Input directory doesn't exist, skipping file finding test")
        
        return True
        
    except Exception as e:
        print(f"❌ Legacy function test failed: {e}")
        return False

if __name__ == "__main__":
    import_success = test_legacy_imports()
    function_success = test_legacy_functionality()
    
    overall_success = import_success and function_success
    
    print(f"\n{'='*50}")
    print(f"🏁 Overall Result: {'✅ SUCCESS' if overall_success else '❌ FAILURE'}")
    
    sys.exit(0 if overall_success else 1)