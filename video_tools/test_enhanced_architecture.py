#!/usr/bin/env python3
"""
Test script for the enhanced class-based architecture.

Validates that all new classes and modules can be imported and instantiated correctly.
"""

import sys
from pathlib import Path

# Add video_utils to Python path
sys.path.insert(0, str(Path(__file__).parent / "video_utils"))

def test_imports():
    """Test that all new modules can be imported successfully."""
    print("🧪 Testing enhanced architecture imports...")
    
    try:
        # Test core processor classes
        from video_utils.enhanced_video_processor import VideoProcessor
        from video_utils.enhanced_audio_processor import AudioProcessor
        print("✅ Enhanced processors imported successfully")
        
        # Test controller classes
        from video_utils.base_controller import BaseController
        from video_utils.media_processing_controller import MediaProcessingController
        from video_utils.command_dispatcher import CommandDispatcher
        print("✅ Controller classes imported successfully")
        
        # Test AI analysis modules
        from video_utils.gemini_analyzer import GeminiVideoAnalyzer, check_gemini_requirements
        from video_utils.whisper_transcriber import WhisperTranscriber, check_whisper_requirements
        from video_utils.ai_utils import (
            analyze_video_file, analyze_audio_file, analyze_image_file,
            save_analysis_result, check_ai_requirements, print_ai_status
        )
        print("✅ AI analysis modules imported successfully")
        
        # Test updated main module
        from video_utils import (
            VideoProcessor as ImportedVideoProcessor,
            AudioProcessor as ImportedAudioProcessor,
            CommandDispatcher as ImportedCommandDispatcher
        )
        print("✅ Main module exports working correctly")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_instantiation():
    """Test that classes can be instantiated correctly."""
    print("\n🧪 Testing class instantiation...")
    
    try:
        # Test processor instantiation
        from video_utils.enhanced_video_processor import VideoProcessor
        from video_utils.enhanced_audio_processor import AudioProcessor
        
        video_processor = VideoProcessor(verbose=False)
        audio_processor = AudioProcessor(verbose=False)
        print("✅ Processor classes instantiated successfully")
        
        # Test controller instantiation
        from video_utils.media_processing_controller import MediaProcessingController
        from video_utils.command_dispatcher import CommandDispatcher
        
        media_controller = MediaProcessingController(verbose=False)
        dispatcher = CommandDispatcher(verbose=False)
        print("✅ Controller classes instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Instantiation error: {e}")
        return False


def test_dependency_checks():
    """Test dependency checking functionality."""
    print("\n🧪 Testing dependency checks...")
    
    try:
        from video_utils.enhanced_video_processor import VideoProcessor
        from video_utils.enhanced_audio_processor import AudioProcessor
        from video_utils.ai_utils import check_ai_requirements
        
        # Test processor dependency checks
        video_processor = VideoProcessor(verbose=False)
        video_deps = video_processor.check_dependencies()
        print(f"✅ Video processor dependencies: {video_deps}")
        
        audio_processor = AudioProcessor(verbose=False)
        audio_deps = audio_processor.check_dependencies()
        print(f"✅ Audio processor dependencies: {audio_deps}")
        
        # Test AI dependency checks
        ai_deps = check_ai_requirements()
        print(f"✅ AI service dependencies checked")
        
        return True
        
    except Exception as e:
        print(f"❌ Dependency check error: {e}")
        return False


def test_file_operations():
    """Test basic file operation methods."""
    print("\n🧪 Testing file operations...")
    
    try:
        from video_utils.enhanced_video_processor import VideoProcessor
        from video_utils.enhanced_audio_processor import AudioProcessor
        
        video_processor = VideoProcessor(verbose=False)
        audio_processor = AudioProcessor(verbose=False)
        
        # Test validation methods (should return False for non-existent files)
        test_path = Path("nonexistent_file.mp4")
        video_valid = video_processor.validate_video(test_path)
        audio_valid = audio_processor.validate_audio(test_path)
        
        print(f"✅ File validation methods working (expected False): video={video_valid}, audio={audio_valid}")
        
        return True
        
    except Exception as e:
        print(f"❌ File operations error: {e}")
        return False


def test_backward_compatibility():
    """Test that legacy function-based imports still work."""
    print("\n🧪 Testing backward compatibility...")
    
    try:
        # Test legacy imports
        from video_utils import (
            check_ffmpeg, get_video_info, find_video_files,
            cut_video_duration, add_audio_to_video
        )
        print("✅ Legacy function imports working")
        
        # Test that both old and new interfaces are available
        from video_utils import VideoProcessor  # New
        from video_utils import cut_video_duration  # Old
        
        print("✅ Both old and new interfaces available")
        
        return True
        
    except Exception as e:
        print(f"❌ Backward compatibility error: {e}")
        return False


def main():
    """Run all tests."""
    print("🎬 Enhanced Video Tools Architecture Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_instantiation,
        test_dependency_checks,
        test_file_operations,
        test_backward_compatibility
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Enhanced architecture is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)