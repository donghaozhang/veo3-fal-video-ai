# Comprehensive Testing Plan for Enhanced Class-Based Architecture

This document outlines a systematic approach to testing the new enhanced class-based video tools architecture using existing scripts and creating new tests.

## 📋 Testing Overview

### Test Directory Structure
```
video_tools/
├── tests/                          # Test suite directory
│   ├── __init__.py                 # Test package initialization
│   ├── run_quick_tests.py          # Main test runner
│   ├── test_enhanced_architecture.py  # Architecture validation
│   ├── test_backward_compatibility.py # Legacy compatibility
│   └── test_enhanced_video_processor.py # Enhanced processor tests
└── run_tests.py                    # Main test runner (delegates to tests/)
```

### Testing Strategy
1. **Architecture Validation** - Verify new classes work correctly
2. **Backward Compatibility** - Ensure existing code still works
3. **Enhanced Features** - Test new capabilities
4. **Integration Testing** - Test end-to-end workflows
5. **Performance Testing** - Verify efficiency improvements

### Test Environment Setup
- Input directory: `video_tools/input/`
- Output directory: `video_tools/output/`
- Test media files: Use existing `sample_video.mp4` and audio files
- Documentation: Available in `video_tools/docs/`

## 🏗️ Phase 1: Architecture Validation Tests

### 1.1 Basic Architecture Test (EXISTING)
**File**: `tests/test_enhanced_architecture.py`
**Purpose**: Validate new architecture imports and instantiation
**Status**: ✅ Already exists and passes

```bash
cd /home/zdhpe/veo3-video-generation/video_tools
python3 tests/test_enhanced_architecture.py
# OR use the main test runner:
python3 run_tests.py
```

**Expected Results**:
- ✅ All imports working correctly
- ✅ Classes instantiate successfully
- ✅ Dependency checks functional
- ✅ File operations working
- ✅ Backward compatibility maintained

### 1.2 Environment Setup Test (EXISTING)
**File**: `tests/test_env_setup.py`
**Purpose**: Verify API keys and environment configuration
**Status**: ✅ Already exists

```bash
cd /home/zdhpe/veo3-video-generation/video_tools
python3 tests/test_env_setup.py
```

**Expected Results**:
- ✅ Environment variables loaded
- ✅ API keys validated
- ✅ Dependencies available

## 🔄 Phase 2: Backward Compatibility Tests

### 2.1 Legacy CLI Test
**File**: `examples/video_cli_tool.py`
**Purpose**: Verify original CLI still works
**Status**: ✅ Existing script

```bash
cd /home/zdhpe/veo3-video-generation/video_tools
python3 examples/video_cli_tool.py --help
```

**Test Scenarios**:
1. Cut video: `python3 examples/video_cli_tool.py cut 3`
2. Extract audio: `python3 examples/video_cli_tool.py extract-audio`
3. Generate subtitles: `python3 examples/video_cli_tool.py generate-subtitles`

### 2.2 Legacy Function Import Test
**File**: `test_backward_compatibility.py` (NEW)
**Purpose**: Test that all old function-based imports still work

```python
#!/usr/bin/env python3
"""Test backward compatibility of function-based imports."""

def test_legacy_imports():
    """Test that all legacy function imports work."""
    try:
        # Test core utilities
        from video_utils import check_ffmpeg, get_video_info, find_video_files
        
        # Test video processing
        from video_utils import cut_video_duration
        
        # Test audio processing
        from video_utils import add_audio_to_video, extract_audio_from_video
        
        # Test AI analysis
        from video_utils import analyze_video_file, GeminiVideoAnalyzer
        
        print("✅ All legacy imports successful")
        return True
    except ImportError as e:
        print(f"❌ Legacy import failed: {e}")
        return False

if __name__ == "__main__":
    test_legacy_imports()
```

## 🚀 Phase 3: Enhanced Features Tests

### 3.1 New CLI Test
**File**: `enhanced_cli.py`
**Purpose**: Test new enhanced CLI functionality

```bash
cd /home/zdhpe/veo3-video-generation/video_tools

# Test system status
python3 enhanced_cli.py --command status

# Test media processing
python3 enhanced_cli.py --command media

# Test AI analysis (if keys available)
python3 enhanced_cli.py --command ai

# Test transcription (if keys available)
python3 enhanced_cli.py --command transcribe

# Test with custom directories
python3 enhanced_cli.py --input-dir input --output-dir output

# Test quiet mode
python3 enhanced_cli.py --quiet --command status
```

### 3.2 Enhanced Video Processor Test
**File**: `test_enhanced_video_processor.py` (NEW)
**Purpose**: Test new VideoProcessor capabilities

```python
#!/usr/bin/env python3
"""Test enhanced VideoProcessor capabilities."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "video_utils"))

from video_utils import VideoProcessor

def test_video_processor():
    """Test VideoProcessor class functionality."""
    processor = VideoProcessor(verbose=True)
    
    # Test dependency checks
    deps = processor.check_dependencies()
    print(f"Dependencies: {deps}")
    
    # Test with sample video if available
    input_dir = Path("input")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    sample_video = input_dir / "sample_video.mp4"
    if sample_video.exists():
        print(f"Testing with {sample_video}")
        
        # Test video info
        info = processor.get_video_info(sample_video)
        print(f"Video info: {info}")
        
        # Test cut duration
        cut_output = output_dir / "test_cut_enhanced.mp4"
        success = processor.cut_duration(sample_video, cut_output, duration=3)
        print(f"Cut test: {'✅ Success' if success else '❌ Failed'}")
        
        # Test thumbnail extraction
        thumb_output = output_dir / "test_thumbnail.jpg"
        success = processor.get_thumbnail(sample_video, thumb_output, "00:00:02")
        print(f"Thumbnail test: {'✅ Success' if success else '❌ Failed'}")
        
        # Test validation
        is_valid = processor.validate_video(sample_video)
        print(f"Validation test: {'✅ Valid' if is_valid else '❌ Invalid'}")
        
    else:
        print(f"❌ Sample video not found: {sample_video}")

if __name__ == "__main__":
    test_video_processor()
```

### 3.3 Enhanced Audio Processor Test
**File**: `test_enhanced_audio_processor.py` (NEW)
**Purpose**: Test new AudioProcessor capabilities

```python
#!/usr/bin/env python3
"""Test enhanced AudioProcessor capabilities."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "video_utils"))

from video_utils import AudioProcessor

def test_audio_processor():
    """Test AudioProcessor class functionality."""
    processor = AudioProcessor(verbose=True)
    
    # Test dependency checks
    deps = processor.check_dependencies()
    print(f"Dependencies: {deps}")
    
    # Test with sample files if available
    input_dir = Path("input")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    sample_video = input_dir / "sample_video.mp4"
    if sample_video.exists():
        print(f"Testing with {sample_video}")
        
        # Test audio extraction
        audio_output = output_dir / "test_extracted_enhanced.mp3"
        success = processor.extract_from_video(sample_video, audio_output)
        print(f"Extraction test: {'✅ Success' if success else '❌ Failed'}")
        
        # Test audio info
        if audio_output.exists():
            info = processor.get_audio_info(audio_output)
            print(f"Audio info: {info}")
            
            # Test volume adjustment
            volume_output = output_dir / "test_volume_adjusted.mp3"
            success = processor.adjust_volume(audio_output, volume_output, volume_factor=1.5)
            print(f"Volume adjustment test: {'✅ Success' if success else '❌ Failed'}")
        
    else:
        print(f"❌ Sample video not found: {sample_video}")

if __name__ == "__main__":
    test_audio_processor()
```

### 3.4 AI Analysis Test (EXISTING + ENHANCED)
**File**: `tests/test_video_understanding.py` (existing) + new tests
**Purpose**: Test AI analysis with new architecture

```bash
# Use existing test
cd /home/zdhpe/veo3-video-generation/video_tools
python3 tests/test_video_understanding.py

# Test new AI utilities
python3 -c "
from video_utils import check_ai_requirements, print_ai_status
print_ai_status()
"
```

## 🔗 Phase 4: Integration Tests

### 4.1 End-to-End Workflow Test
**File**: `test_e2e_workflow.py` (NEW)
**Purpose**: Test complete workflows using new architecture

```python
#!/usr/bin/env python3
"""End-to-end workflow tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "video_utils"))

from video_utils import (
    VideoProcessor, AudioProcessor, 
    MediaProcessingController, CommandDispatcher
)

def test_media_processing_workflow():
    """Test media processing workflow."""
    print("🎬 Testing Media Processing Workflow")
    
    # Setup
    input_dir = Path("input")
    output_dir = Path("output")
    
    video_processor = VideoProcessor(verbose=False)
    audio_processor = AudioProcessor(verbose=False)
    
    sample_video = input_dir / "sample_video.mp4"
    if not sample_video.exists():
        print(f"❌ Sample video not found: {sample_video}")
        return False
    
    # Step 1: Cut video
    cut_output = output_dir / "workflow_cut.mp4"
    success1 = video_processor.cut_duration(sample_video, cut_output, duration=3)
    
    # Step 2: Extract audio
    audio_output = output_dir / "workflow_audio.mp3"
    success2 = audio_processor.extract_from_video(cut_output, audio_output)
    
    # Step 3: Adjust audio volume
    volume_output = output_dir / "workflow_audio_loud.mp3"
    success3 = audio_processor.adjust_volume(audio_output, volume_output, volume_factor=2.0)
    
    # Step 4: Add modified audio back to video
    final_output = output_dir / "workflow_final.mp4"
    success4 = audio_processor.add_to_video(cut_output, volume_output, final_output, replace_audio=True)
    
    results = [success1, success2, success3, success4]
    print(f"Workflow results: {results}")
    
    if all(results):
        print("✅ End-to-end workflow successful")
        return True
    else:
        print("❌ End-to-end workflow failed")
        return False

def test_controller_integration():
    """Test controller integration."""
    print("🎮 Testing Controller Integration")
    
    controller = MediaProcessingController(verbose=False)
    
    # Test dependency validation
    deps = controller.validate_dependencies()
    print(f"Controller dependencies: {deps}")
    
    # Test directory setup
    setup_ok = controller.setup_directories()
    print(f"Directory setup: {'✅ Success' if setup_ok else '❌ Failed'}")
    
    return setup_ok

if __name__ == "__main__":
    test_media_processing_workflow()
    test_controller_integration()
```

### 4.2 CLI Integration Test
**File**: `test_cli_integration.py` (NEW)
**Purpose**: Test CLI commands programmatically

```python
#!/usr/bin/env python3
"""CLI integration tests."""

import subprocess
import sys
from pathlib import Path

def run_cli_test(command, description):
    """Run a CLI command and check result."""
    print(f"Testing: {description}")
    
    try:
        result = subprocess.run(
            ["python3", "enhanced_cli.py"] + command,
            cwd="/home/zdhpe/veo3-video-generation/video_tools",
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - Timeout")
        return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def test_cli_commands():
    """Test various CLI commands."""
    tests = [
        (["--help"], "Help display"),
        (["--command", "status"], "System status check"),
        (["--quiet", "--command", "status"], "Quiet mode"),
        (["--input-dir", "input", "--output-dir", "output", "--command", "status"], "Custom directories"),
    ]
    
    results = []
    for command, description in tests:
        result = run_cli_test(command, description)
        results.append(result)
    
    successful = sum(results)
    total = len(results)
    
    print(f"\n📊 CLI Tests: {successful}/{total} successful")
    return successful == total

if __name__ == "__main__":
    test_cli_commands()
```

## ⚡ Phase 5: Performance Tests

### 5.1 Batch Processing Test
**File**: `test_batch_performance.py` (NEW)
**Purpose**: Test batch processing performance

```python
#!/usr/bin/env python3
"""Batch processing performance tests."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "video_utils"))

from video_utils import VideoProcessor, AudioProcessor

def test_batch_performance():
    """Test batch processing performance."""
    print("⚡ Testing Batch Processing Performance")
    
    video_processor = VideoProcessor(verbose=False)
    
    input_dir = Path("input")
    output_dir = Path("output")
    
    # Create multiple test videos if sample exists
    sample_video = input_dir / "sample_video.mp4"
    if not sample_video.exists():
        print(f"❌ Sample video not found: {sample_video}")
        return False
    
    # Test batch cutting
    start_time = time.time()
    
    results = video_processor.batch_process(
        input_dir=input_dir,
        output_dir=output_dir,
        operation='cut_duration',
        duration=2
    )
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"📊 Batch Results:")
    print(f"   Files processed: {total}")
    print(f"   Successful: {successful}")
    print(f"   Processing time: {processing_time:.2f}s")
    print(f"   Average per file: {processing_time/total:.2f}s" if total > 0 else "   No files processed")
    
    return successful > 0

if __name__ == "__main__":
    test_batch_performance()
```

## 📊 Phase 6: Comprehensive Test Suite

### 6.1 Master Test Runner
**File**: `run_all_tests.py` (NEW)
**Purpose**: Run all tests in sequence

```python
#!/usr/bin/env python3
"""Master test runner for enhanced architecture."""

import subprocess
import sys
from pathlib import Path

def run_test(test_file, description):
    """Run a test file and return result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"File: {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run(
            ["python3", test_file],
            cwd="/home/zdhpe/veo3-video-generation/video_tools",
            timeout=120
        )
        
        success = result.returncode == 0
        print(f"Result: {'✅ PASSED' if success else '❌ FAILED'}")
        return success
        
    except subprocess.TimeoutExpired:
        print("Result: ⏰ TIMEOUT")
        return False
    except Exception as e:
        print(f"Result: ❌ ERROR - {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Enhanced Architecture - Comprehensive Test Suite")
    print("🏗️ Testing class-based video tools architecture")
    
    tests = [
        ("test_enhanced_architecture.py", "Architecture Validation"),
        ("tests/test_env_setup.py", "Environment Setup"),
        ("test_backward_compatibility.py", "Backward Compatibility"),
        ("test_enhanced_video_processor.py", "Enhanced Video Processor"),
        ("test_enhanced_audio_processor.py", "Enhanced Audio Processor"),
        ("test_e2e_workflow.py", "End-to-End Workflow"),
        ("test_cli_integration.py", "CLI Integration"),
        ("test_batch_performance.py", "Batch Performance"),
    ]
    
    results = []
    
    for test_file, description in tests:
        if Path(test_file).exists() or Path(f"/home/zdhpe/veo3-video-generation/video_tools/{test_file}").exists():
            result = run_test(test_file, description)
            results.append((description, result))
        else:
            print(f"⚠️ Skipping {description} - test file not found: {test_file}")
            results.append((description, None))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print('='*60)
    
    passed = 0
    failed = 0
    skipped = 0
    
    for description, result in results:
        if result is True:
            print(f"✅ {description}")
            passed += 1
        elif result is False:
            print(f"❌ {description}")
            failed += 1
        else:
            print(f"⚠️ {description} (skipped)")
            skipped += 1
    
    total = passed + failed
    print(f"\n📈 Results: {passed}/{total} passed")
    if skipped > 0:
        print(f"⚠️ {skipped} tests skipped")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"🎯 Success rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 Test suite PASSED!")
        return True
    else:
        print("❌ Test suite FAILED!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

## 📋 Testing Execution Plan

### Quick Test (5 minutes)
```bash
cd /home/zdhpe/veo3-video-generation/video_tools

# 1. Run the complete quick test suite
python3 run_tests.py

# OR run individual tests:
python3 tests/test_enhanced_architecture.py
python3 tests/test_backward_compatibility.py  
python3 tests/test_enhanced_video_processor.py

# 2. Environment check (if exists)
python3 tests/test_env_setup.py

# 3. CLI help
python3 enhanced_cli.py --help

# 4. System status
python3 enhanced_cli.py --command status
```

### Comprehensive Test (30 minutes)
```bash
cd /home/zdhpe/veo3-video-generation/video_tools

# Create all test files (run the scripts above)
# Then run master test suite
python3 run_all_tests.py
```

### Manual Interactive Test (15 minutes)
```bash
cd /home/zdhpe/veo3-video-generation/video_tools

# Test interactive CLI
python3 enhanced_cli.py

# Navigate through menus:
# 1 -> Media Processing -> Test cut videos
# 2 -> AI Analysis -> Check status
# 5 -> System Status
# h -> Help
# q -> Quit
```

## 🎯 Success Criteria

### Phase 1: Architecture ✅
- All new classes import and instantiate correctly
- Dependencies are properly checked
- Backward compatibility is maintained

### Phase 2: Functionality ✅
- Legacy CLI still works
- New CLI provides enhanced features
- All processors function correctly

### Phase 3: Integration ✅
- End-to-end workflows complete successfully
- Controllers work with processors
- Error handling is robust

### Phase 4: Performance ✅
- Batch processing is efficient
- No significant performance regression
- Memory usage is reasonable

## 📝 Test Documentation

### Test Results Format
```
Test: [Test Name]
Status: ✅ PASSED / ❌ FAILED / ⚠️ SKIPPED
Duration: [X.X seconds]
Notes: [Any relevant notes]
```

### Issue Tracking
- Document any failures with error messages
- Note performance issues or unexpected behavior
- Track compatibility problems
- Record suggestions for improvements

## 🔧 Troubleshooting

### Common Issues
1. **Import Errors**: Check Python path and module structure
2. **Dependency Missing**: Run `python3 enhanced_cli.py --command status`
3. **File Not Found**: Ensure sample media files are in `input/` directory
4. **Permission Errors**: Check file permissions and directory access
5. **API Key Issues**: Verify environment variables with `tests/test_env_setup.py`

### Debug Commands
```bash
# Check Python path
python3 -c "import sys; print('\\n'.join(sys.path))"

# Test imports manually
python3 -c "from video_utils import VideoProcessor; print('✅ Import successful')"

# Check file structure
ls -la video_tools/video_utils/

# Verify executable permissions
ls -la video_tools/enhanced_cli.py
```

This testing plan provides a comprehensive approach to validating the enhanced class-based architecture while leveraging existing test infrastructure and ensuring backward compatibility.