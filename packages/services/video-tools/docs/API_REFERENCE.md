# Video Tools API Reference

Complete API documentation for the Video Tools suite.

## 📋 Table of Contents

- [Core Modules](#core-modules)
- [Video Processing](#video-processing)
- [Audio Processing](#audio-processing)
- [AI Analysis](#ai-analysis)
- [Utility Functions](#utility-functions)
- [Command Line Interface](#command-line-interface)

## 🏗️ Core Modules

### video_utils Package

The main package containing all video processing functionality.

```python
from video_utils import (
    VideoProcessor,
    AudioProcessor,
    SubtitleGenerator,
    VideoUnderstanding
)
```

#### VideoProcessor Class

Main class for video manipulation operations.

```python
class VideoProcessor:
    def __init__(self, input_path: str, output_dir: str = "test_output")
    
    def cut_video(self, start: float, duration: float, output_name: str = None) -> str
    def extract_audio(self, output_name: str = None) -> str
    def add_audio(self, audio_path: str, output_name: str = None) -> str
    def replace_audio(self, audio_path: str, output_name: str = None) -> str
```

**Parameters:**
- `input_path` (str): Path to input video file
- `output_dir` (str): Directory for output files (default: "test_output")
- `start` (float): Start time in seconds
- `duration` (float): Duration in seconds
- `audio_path` (str): Path to audio file for mixing/replacement
- `output_name` (str): Custom output filename

**Returns:**
- `str`: Path to generated output file

#### AudioProcessor Class

Dedicated audio processing functionality.

```python
class AudioProcessor:
    def __init__(self, input_path: str, output_dir: str = "test_output")
    
    def extract_segment(self, start: float, duration: float, output_name: str = None) -> str
    def mix_audio(self, audio_paths: List[str], output_name: str = None) -> str
    def concatenate_audio(self, audio_paths: List[str], output_name: str = None) -> str
    def convert_format(self, output_format: str = "mp3", output_name: str = None) -> str
```

#### SubtitleGenerator Class

Generate subtitles and captions for videos.

```python
class SubtitleGenerator:
    def __init__(self, video_path: str, output_dir: str = "test_output")
    
    def generate_srt(self, output_name: str = None) -> str
    def generate_vtt(self, output_name: str = None) -> str
    def generate_both(self, output_name: str = None) -> Tuple[str, str]
```

## 🎬 Video Processing

### Core Video Operations

#### Cut Video
```python
from video_utils import VideoProcessor

processor = VideoProcessor("input_video.mp4")
output_path = processor.cut_video(start=10.5, duration=30.0)
print(f"Cut video saved to: {output_path}")
```

#### Extract Audio from Video
```python
audio_path = processor.extract_audio()
print(f"Audio extracted to: {audio_path}")
```

#### Add Audio Track
```python
mixed_video = processor.add_audio("background_music.mp3")
print(f"Video with audio: {mixed_video}")
```

#### Replace Audio Track
```python
new_video = processor.replace_audio("new_soundtrack.mp3")
print(f"Video with replaced audio: {new_video}")
```

### Advanced Video Operations

#### Batch Processing
```python
import os
from video_utils import VideoProcessor

video_dir = "input_videos/"
for filename in os.listdir(video_dir):
    if filename.endswith(('.mp4', '.avi', '.mov')):
        processor = VideoProcessor(os.path.join(video_dir, filename))
        processor.cut_video(start=0, duration=5)  # First 5 seconds
```

## 🔊 Audio Processing

### Audio Operations

#### Extract Audio Segment
```python
from video_utils import AudioProcessor

audio_proc = AudioProcessor("input_audio.mp3")
segment = audio_proc.extract_segment(start=15.0, duration=10.0)
```

#### Mix Multiple Audio Files
```python
mixed_audio = audio_proc.mix_audio([
    "voice.mp3",
    "background.mp3",
    "effects.mp3"
])
```

#### Concatenate Audio Files
```python
concatenated = audio_proc.concatenate_audio([
    "intro.mp3",
    "main_content.mp3",
    "outro.mp3"
])
```

#### Convert Audio Format
```python
wav_file = audio_proc.convert_format(output_format="wav")
```

## 🤖 AI Analysis

### VideoUnderstanding Class

AI-powered video, audio, and image analysis using Google Gemini.

```python
from video_utils import VideoUnderstanding

# Initialize with API key
analyzer = VideoUnderstanding(api_key="your_gemini_api_key")
```

#### Video Analysis

```python
# Analyze video content
result = analyzer.analyze_video(
    video_path="sample_video.mp4",
    analysis_type="comprehensive",  # or "transcription", "description"
    custom_prompt="Describe the main activities in this video"
)

print(f"Analysis: {result['analysis']}")
print(f"Processing time: {result['processing_time']} seconds")
```

**Analysis Types:**
- `"transcription"`: Speech-to-text with timestamps
- `"description"`: Content description and summarization
- `"comprehensive"`: Full analysis including scene breakdown
- `"custom"`: Use with custom_prompt parameter

#### Audio Analysis

```python
# Analyze audio content
audio_result = analyzer.analyze_audio(
    audio_path="sample_audio.mp3",
    analysis_type="transcription",
    include_timestamps=True
)

print(f"Transcription: {audio_result['transcription']}")
print(f"Confidence: {audio_result['confidence']}")
```

#### Image Analysis

```python
# Analyze image content
image_result = analyzer.analyze_image(
    image_path="sample_image.jpg",
    analysis_type="description",
    custom_prompt="What objects are visible in this image?"
)

print(f"Description: {image_result['description']}")
print(f"Objects detected: {image_result['objects']}")
```

#### Advanced Analysis Options

```python
# Q&A Analysis
qa_result = analyzer.analyze_media(
    media_path="video.mp4",
    analysis_type="qa",
    questions=[
        "What is the main topic discussed?",
        "Who are the speakers?",
        "What time does the presentation start?"
    ]
)

# Information Extraction
info_result = analyzer.extract_information(
    media_path="presentation.mp4",
    extract_types=["people", "places", "dates", "facts"]
)
```

### Configuration Options

#### Model Configuration
```python
analyzer = VideoUnderstanding(
    api_key="your_api_key",
    model_name="gemini-1.5-pro",  # or "gemini-1.5-flash"
    temperature=0.7,
    max_tokens=2048,
    timeout=120
)
```

#### Analysis Parameters
```python
result = analyzer.analyze_video(
    video_path="video.mp4",
    analysis_type="comprehensive",
    max_duration=300,  # Limit to first 5 minutes
    sample_rate=1.0,   # Analyze every frame (0.5 = every other frame)
    include_metadata=True,
    output_format="json"  # or "text", "structured"
)
```

## 🔧 Utility Functions

### File Management

```python
from video_utils.file_utils import (
    ensure_output_dir,
    get_video_info,
    validate_file_path,
    cleanup_temp_files
)

# Ensure output directory exists
ensure_output_dir("output/processed_videos")

# Get video metadata
info = get_video_info("input_video.mp4")
print(f"Duration: {info['duration']} seconds")
print(f"Resolution: {info['width']}x{info['height']}")
print(f"FPS: {info['fps']}")

# Validate file exists and is readable
if validate_file_path("video.mp4"):
    print("File is valid")

# Clean up temporary files
cleanup_temp_files("temp_dir/")
```

### Format Utilities

```python
from video_utils.core import (
    seconds_to_timecode,
    timecode_to_seconds,
    get_supported_formats
)

# Convert seconds to HH:MM:SS format
timecode = seconds_to_timecode(3661.5)  # "01:01:01.500"

# Convert timecode back to seconds
seconds = timecode_to_seconds("01:01:01.500")  # 3661.5

# Get supported file formats
formats = get_supported_formats()
print(f"Supported video formats: {formats['video']}")
print(f"Supported audio formats: {formats['audio']}")
```

## 📟 Command Line Interface

### Basic Commands

```bash
# Cut videos (interactive)
python video_audio_utils.py cut

# Cut with specific parameters
python video_audio_utils.py cut --start 10 --duration 30

# Generate subtitles
python video_audio_utils.py generate-subtitles

# AI analysis
python video_audio_utils.py analyze-videos --type comprehensive
python video_audio_utils.py analyze-audio --type transcription
python video_audio_utils.py analyze-images --type description
```

### Advanced Command Options

```bash
# Batch processing with filters
python video_audio_utils.py cut --input-dir videos/ --output-dir processed/ --start 0 --duration 60

# Audio operations
python video_audio_utils.py extract-audio --input video.mp4 --output audio.mp3
python video_audio_utils.py mix-audio --inputs voice.mp3,music.mp3 --output mixed.mp3

# Subtitle generation with customization
python video_audio_utils.py generate-subtitles --format both --language en --confidence 0.8
```

### AI Analysis Commands

```bash
# Video analysis with custom prompts
python video_audio_utils.py analyze-videos \
    --type custom \
    --prompt "Identify all the people and their actions in this video"

# Audio analysis with timestamps
python video_audio_utils.py analyze-audio \
    --type transcription \
    --timestamps \
    --speaker-id

# Image analysis batch processing
python video_audio_utils.py analyze-images \
    --input-dir images/ \
    --type comprehensive \
    --output-dir analysis_results/
```

## 🔍 Error Handling

### Common Exceptions

```python
from video_utils.exceptions import (
    VideoProcessingError,
    AudioProcessingError,
    AIAnalysisError,
    FileNotFoundError
)

try:
    processor = VideoProcessor("nonexistent.mp4")
    processor.cut_video(0, 10)
except FileNotFoundError as e:
    print(f"File error: {e}")
except VideoProcessingError as e:
    print(f"Processing error: {e}")
```

### Error Recovery

```python
# Robust processing with fallbacks
def safe_video_processing(video_path, operations):
    try:
        processor = VideoProcessor(video_path)
        results = []
        
        for operation in operations:
            try:
                result = operation(processor)
                results.append(result)
            except Exception as e:
                print(f"Operation failed: {e}, continuing...")
                continue
                
        return results
    except Exception as e:
        print(f"Critical error: {e}")
        return None
```

## 📊 Performance Considerations

### Optimization Tips

1. **Batch Processing**: Process multiple files in sequence for better resource utilization
2. **Memory Management**: Use `cleanup_temp_files()` regularly for long-running processes
3. **AI Analysis**: Use `gemini-1.5-flash` for faster analysis, `gemini-1.5-pro` for higher quality
4. **File Formats**: MP4 H.264 provides best compatibility and performance

### Resource Monitoring

```python
import psutil
from video_utils import VideoProcessor

# Monitor memory usage during processing
process = psutil.Process()
initial_memory = process.memory_info().rss

processor = VideoProcessor("large_video.mp4")
result = processor.cut_video(0, 60)

final_memory = process.memory_info().rss
memory_used = (final_memory - initial_memory) / 1024 / 1024  # MB
print(f"Memory used: {memory_used:.2f} MB")
```

## 🚀 Best Practices

### File Organization
```python
# Recommended directory structure
project/
├── input/          # Source files
├── output/         # Processed files
├── temp/           # Temporary files
├── config/         # Configuration files
└── logs/           # Processing logs
```

### Configuration Management
```python
# Use configuration files for consistent settings
import json

config = {
    "video": {
        "default_codec": "h264",
        "default_quality": "high",
        "output_format": "mp4"
    },
    "audio": {
        "default_codec": "aac",
        "sample_rate": 44100,
        "bitrate": "192k"
    },
    "ai": {
        "model": "gemini-1.5-pro",
        "temperature": 0.7,
        "max_tokens": 2048
    }
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
```

### Logging Setup
```python
import logging

# Configure logging for debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_processing.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Starting video processing pipeline")
```

---

For more examples and advanced usage, see the [examples directory](../examples/) and [main README](../README.md).