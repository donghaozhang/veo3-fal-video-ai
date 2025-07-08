# Migration Guide: Enhanced Class-Based Architecture

This guide helps you migrate from the function-based video tools to the new enhanced class-based architecture.

## Overview

The video tools have been reorganized with a modern class-based architecture for better:
- **Maintainability**: Smaller, focused modules instead of large monolithic files
- **Extensibility**: Easy to add new features and processors
- **Organization**: Logical grouping of related functionality
- **Testing**: Better separation of concerns for unit testing

## Key Changes

### 1. Architecture Overview

**Before (Function-based):**
```
video_utils/
├── video_understanding.py (1,363 lines - too large!)
├── video_processor.py (37 lines - too small!)
├── audio_processor.py (196 lines)
├── *_commands.py (scattered command functions)
```

**After (Class-based):**
```
video_utils/
├── enhanced_video_processor.py (VideoProcessor class)
├── enhanced_audio_processor.py (AudioProcessor class)
├── gemini_analyzer.py (GeminiVideoAnalyzer class)
├── whisper_transcriber.py (WhisperTranscriber class)
├── ai_utils.py (convenience functions)
├── base_controller.py (BaseController class)
├── media_processing_controller.py (MediaProcessingController class)
├── command_dispatcher.py (CommandDispatcher + main CLI)
```

### 2. Import Changes

**Backward Compatibility**: All existing function-based imports continue to work!

```python
# ✅ STILL WORKS - Legacy function-based imports
from video_utils import (
    cut_video_duration,
    add_audio_to_video,
    analyze_video_file,
    GeminiVideoAnalyzer
)

# ✅ NEW - Enhanced class-based imports  
from video_utils import (
    VideoProcessor,
    AudioProcessor,
    MediaProcessingController,
    CommandDispatcher
)
```

### 3. New Enhanced CLI

**Before:**
```bash
python examples/video_cli_tool.py
```

**After:**
```bash
# New enhanced CLI with class-based architecture
python enhanced_cli.py

# Or run specific commands directly
python enhanced_cli.py --command media
python enhanced_cli.py --command ai
python enhanced_cli.py --command transcribe
```

## Migration Examples

### 1. Video Processing Migration

**Before (Function-based):**
```python
from video_utils import cut_video_duration, get_video_info

# Cut video duration
input_path = Path("input/video.mp4")
output_path = Path("output/video_cut.mp4")
success = cut_video_duration(input_path, output_path, duration=5)

# Get video info
info = get_video_info(input_path)
```

**After (Class-based):**
```python
from video_utils import VideoProcessor

# Create processor instance
processor = VideoProcessor(verbose=True)

# Cut video duration (enhanced with more options)
success = processor.cut_duration(
    input_path, output_path, 
    duration=5, start_time=0
)

# Get comprehensive video info
info = processor.get_video_info(input_path)

# New capabilities
success = processor.resize_video(input_path, output_path, 1920, 1080)
success = processor.get_thumbnail(input_path, thumb_path, "00:00:05")
```

### 2. Audio Processing Migration

**Before (Function-based):**
```python
from video_utils import add_audio_to_video, extract_audio_from_video

# Add audio to video
success = add_audio_to_video(video_path, audio_path, output_path)

# Extract audio
success = extract_audio_from_video(video_path, audio_path)
```

**After (Class-based):**
```python
from video_utils import AudioProcessor

# Create processor instance
processor = AudioProcessor(verbose=True)

# Add audio to video (enhanced options)
success = processor.add_to_video(
    video_path, audio_path, output_path,
    replace_audio=False, sync_to_video=True
)

# Extract audio (enhanced with quality options)
success = processor.extract_from_video(
    video_path, audio_path,
    audio_format='mp3', quality='192k'
)

# New capabilities
success = processor.mix_files(audio_list, output_path, normalize=True)
success = processor.adjust_volume(input_path, output_path, volume_factor=1.5)
```

### 3. AI Analysis Migration

**Before (Function-based):**
```python
from video_utils import analyze_video_file, GeminiVideoAnalyzer

# Convenience function
result = analyze_video_file(video_path, "description", detailed=True)

# Direct class usage
analyzer = GeminiVideoAnalyzer()
result = analyzer.describe_video(video_path, detailed=True)
```

**After (Class-based - mostly unchanged):**
```python
# ✅ Convenience functions still work exactly the same
from video_utils import analyze_video_file, GeminiVideoAnalyzer

result = analyze_video_file(video_path, "description", detailed=True)

# ✅ Classes now split into focused modules but same interface
from video_utils import GeminiVideoAnalyzer
analyzer = GeminiVideoAnalyzer()
result = analyzer.describe_video(video_path, detailed=True)

# ✅ NEW - Enhanced convenience function
from video_utils import analyze_media_comprehensively
result = analyze_media_comprehensively(file_path, output_dir)
```

### 4. Command Controller Migration

**Before (Scattered command functions):**
```python
# Commands were scattered across multiple files
from video_utils.video_commands import cmd_cut_videos
from video_utils.audio_commands import cmd_add_audio
from video_utils.ai_analysis_commands import cmd_analyze_videos

# Had to call each function separately
cmd_cut_videos()
cmd_add_audio()
cmd_analyze_videos()
```

**After (Organized controller classes):**
```python
from video_utils import MediaProcessingController, CommandDispatcher

# Organized into controller classes
controller = MediaProcessingController(input_dir='input', output_dir='output')
controller.cmd_cut_videos()
controller.cmd_add_audio()

# Or use unified dispatcher
dispatcher = CommandDispatcher()
dispatcher.run()  # Interactive menu for all operations
```

## New Features

### 1. Enhanced Processing Capabilities

```python
from video_utils import VideoProcessor, AudioProcessor

video_processor = VideoProcessor()
audio_processor = AudioProcessor()

# Video enhancements
video_processor.resize_video(input_path, output_path, 1920, 1080)
video_processor.convert_format(input_path, output_path, 'libx265')
video_processor.extract_frames(input_path, frames_dir, frame_rate="1/10")
video_processor.get_thumbnail(input_path, thumb_path, "00:00:05")

# Audio enhancements  
audio_processor.adjust_volume(input_path, output_path, volume_factor=1.5)
audio_processor.trim_audio(input_path, output_path, "00:00:10", duration="00:00:30")
audio_processor.concatenate_files(audio_list, output_path, crossfade_duration=1.0)
```

### 2. Batch Processing

```python
from video_utils import VideoProcessor

processor = VideoProcessor()

# Batch process entire directories
results = processor.batch_process(
    input_dir=Path('input'),
    output_dir=Path('output'), 
    operation='cut_duration',
    duration=5
)

print(f"Processed {len(results)} files")
```

### 3. Dependency Management

```python
from video_utils import VideoProcessor, check_ai_requirements, print_ai_status

# Check processor dependencies
processor = VideoProcessor()
deps = processor.check_dependencies()
print(f"FFmpeg available: {deps['ffmpeg']}")

# Check AI service status
print_ai_status()  # Prints comprehensive status

requirements = check_ai_requirements()
print(f"Gemini ready: {requirements['gemini']['status'][0]}")
```

### 4. Unified Command Interface

```bash
# Interactive menu system
python enhanced_cli.py

# Direct command execution
python enhanced_cli.py --command media    # Media processing menu
python enhanced_cli.py --command ai       # AI analysis menu  
python enhanced_cli.py --command transcribe # Transcription menu
python enhanced_cli.py --command status   # System status check

# Custom directories
python enhanced_cli.py --input-dir custom_input --output-dir custom_output

# Quiet mode
python enhanced_cli.py --quiet
```

## Migration Strategies

### Strategy 1: Gradual Migration (Recommended)

1. **Keep using existing code** - All function-based imports still work
2. **Try new features** - Use new enhanced classes for new functionality
3. **Migrate incrementally** - Replace old code with new classes over time

```python
# Phase 1: Keep existing code working
from video_utils import cut_video_duration  # Old, still works

# Phase 2: Try new features
from video_utils import VideoProcessor
processor = VideoProcessor()
processor.get_thumbnail(video_path, thumb_path)  # New capability

# Phase 3: Migrate existing code when convenient
processor.cut_duration(input_path, output_path, duration=5)  # New way
```

### Strategy 2: Full Migration

1. **Update imports** to use new class-based architecture
2. **Update code** to use class methods instead of functions
3. **Benefit from enhanced capabilities** and better organization

### Strategy 3: Hybrid Approach

1. **Use new CLI** for interactive operations
2. **Keep function-based code** for programmatic usage
3. **Add new features** using class-based architecture

## Breaking Changes

### None! 🎉

This migration maintains **100% backward compatibility**. All existing code will continue to work without changes.

The only "breaking change" is that the new enhanced features require updating to the class-based approach.

## Benefits After Migration

### 1. Better Organization
```python
# Before: scattered across multiple files
from video_utils.video_commands import cmd_cut_videos
from video_utils.audio_commands import cmd_add_audio

# After: logically organized
from video_utils import MediaProcessingController
controller = MediaProcessingController()
controller.cmd_cut_videos()
controller.cmd_add_audio()
```

### 2. Enhanced Capabilities
```python
# Before: basic functionality
cut_video_duration(input_path, output_path, 5)

# After: comprehensive options
processor.cut_duration(input_path, output_path, duration=5, start_time=10)
processor.resize_video(input_path, output_path, 1920, 1080, maintain_aspect=True)
processor.batch_process(input_dir, output_dir, 'cut_duration', duration=5)
```

### 3. Better Error Handling
```python
# Classes provide better error handling and validation
processor = VideoProcessor(verbose=True)
deps = processor.check_dependencies()
if not deps['ffmpeg']:
    print("FFmpeg not available - please install")
    return

success = processor.cut_duration(input_path, output_path, duration=5)
if not success:
    print("Video processing failed")
```

### 4. Easier Testing
```python
# Classes are easier to test and mock
def test_video_processing():
    processor = VideoProcessor(verbose=False)
    assert processor.validate_video(test_video_path)
    
    result = processor.cut_duration(test_input, test_output, 5)
    assert result == True
```

## Troubleshooting

### Import Errors

**Problem:** `ImportError: cannot import name 'VideoProcessor'`

**Solution:** Ensure you're importing from the updated `video_utils` module:
```python
from video_utils import VideoProcessor  # ✅ Correct
```

### Module Not Found

**Problem:** `ModuleNotFoundError: No module named 'enhanced_video_processor'`

**Solution:** Import from main module instead:
```python
# ❌ Don't import internal modules directly
from video_utils.enhanced_video_processor import VideoProcessor

# ✅ Import from main module
from video_utils import VideoProcessor
```

### Dependency Issues

**Problem:** Missing dependencies or tools

**Solution:** Check status and install missing components:
```python
from video_utils import print_ai_status
print_ai_status()  # Shows what's missing

# Install missing components:
# pip install google-generativeai  # For Gemini
# pip install openai-whisper       # For local Whisper
# # Install ffmpeg for your system
```

## Getting Help

1. **Test the installation:**
   ```bash
   python test_enhanced_architecture.py
   ```

2. **Check system status:**
   ```bash
   python enhanced_cli.py --command status
   ```

3. **Use interactive help:**
   ```bash
   python enhanced_cli.py
   # Choose option 'h' for help
   ```

4. **Check the documentation:**
   - `README.md` - Main documentation
   - `API_REFERENCE.md` - Detailed API reference
   - `COMMAND_LINE_EXAMPLES.md` - CLI usage examples

## Summary

The enhanced class-based architecture provides:

✅ **100% Backward Compatibility** - All existing code continues to work  
✅ **Better Organization** - Logical grouping in focused modules  
✅ **Enhanced Capabilities** - More features and options  
✅ **Improved Maintainability** - Easier to extend and modify  
✅ **Better Testing** - Classes are easier to test  
✅ **Unified Interface** - Single CLI for all operations  

You can migrate at your own pace, starting with trying new features while keeping existing code unchanged.