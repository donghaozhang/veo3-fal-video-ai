# Video Tools - Advanced Video & Audio Processing Suite

A comprehensive collection of Python utilities for video and audio processing, including AI-powered video understanding with Google Gemini.

## 🎯 Features

### Core Video/Audio Processing
- **Video Cutting**: Extract specific durations from videos
- **Audio Management**: Add, replace, extract, mix, and concatenate audio
- **Subtitle Generation**: Create SRT/VTT files for video players
- **Format Support**: MP4, AVI, MOV, MKV, WebM, and more

### 🤖 AI-Powered Multimodal Understanding (NEW!)
- **Smart Analysis**: Google Gemini AI for video, audio, and image understanding
- **Transcription**: Speech-to-text with timestamps and speaker identification
- **Description**: Automated video/audio/image summarization
- **Scene Analysis**: Timeline breakdown and key moments for video
- **Content Analysis**: Comprehensive audio quality and acoustic features
- **Event Detection**: Audio events, segments, and sound identification
- **Object Detection**: Identify and locate objects in images
- **OCR**: Extract text from images with context and positioning
- **Classification**: Categorize and classify image content
- **Composition Analysis**: Artistic and technical image analysis
- **Q&A**: Ask specific questions about any media content
- **Information Extraction**: Identify people, places, facts across all media types

## 🚀 Quick Start

### Basic Usage
```bash
# Cut first 5 seconds from all videos
python video_audio_utils.py cut

# Generate subtitles for video players
python video_audio_utils.py generate-subtitles

# AI video analysis (requires Google Gemini API)
python video_audio_utils.py analyze-videos

# AI audio analysis (requires Google Gemini API)
python video_audio_utils.py analyze-audio

# AI image analysis (requires Google Gemini API)
python video_audio_utils.py analyze-images
```

### AI Multimodal Understanding Setup

1. **Install Dependencies**
```bash
# Install required packages
pip install google-generativeai python-dotenv

# Or install from requirements file
pip install -r requirements_gemini.txt
```

2. **Configure API Keys**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your API keys
# Get your Gemini API key from: https://aistudio.google.com/app/apikey
```

3. **Test Your Setup**
```bash
# Verify everything is configured correctly
python test_env_setup.py
```

Your `.env` file should look like this:
```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_actual_api_key_here

# OpenAI API Configuration (Optional)
OPENAI_API_KEY=your_openai_api_key_here
```

# Test analysis
python video_audio_utils.py describe-videos

# Test audio analysis
python video_audio_utils.py describe-audio

# Test image analysis
python video_audio_utils.py describe-images
```

## 📁 Directory Structure

```
video_tools/
├── video_audio_utils.py          # Main CLI interface
├── video_utils/                  # Modular package
│   ├── core.py                   # Core utilities (ffmpeg, video info)
│   ├── video_processor.py        # Video cutting and processing
│   ├── audio_processor.py        # Audio manipulation
│   ├── subtitle_generator.py     # Subtitle creation (SRT/VTT)
│   ├── video_understanding.py    # AI multimodal analysis (NEW!)
│   ├── interactive.py            # User interaction
│   └── commands.py               # CLI command implementations
├── test_subtitles.py             # Subtitle functionality tests
├── test_video_understanding.py   # AI analysis tests
├── GEMINI_SETUP.md              # AI setup guide
├── requirements_gemini.txt       # AI dependencies
├── samples/                      # Sample videos for testing
├── test_output/                  # Generated test files
└── README.md                     # This documentation
```

## 🎬 Available Commands

### Video Processing
```bash
python video_audio_utils.py cut [duration]      # Extract first N seconds (default: 5)
python video_audio_utils.py add-audio           # Add audio to silent videos
python video_audio_utils.py replace-audio       # Replace existing audio
python video_audio_utils.py extract-audio       # Extract audio tracks
```

### Audio Processing  
```bash
python video_audio_utils.py mix-audio           # Mix multiple audio files
python video_audio_utils.py concat-audio        # Concatenate audio files
```

### Subtitles
```bash
python video_audio_utils.py generate-subtitles  # Create .srt/.vtt files for video players
python video_audio_utils.py burn-subtitles      # Embed subtitles permanently into video
```

### 🤖 AI Analysis (NEW!)
```bash
# Video Analysis
python video_audio_utils.py analyze-videos      # Comprehensive AI analysis with multiple options
python video_audio_utils.py transcribe-videos   # Quick speech-to-text transcription
python video_audio_utils.py describe-videos     # AI-powered video description

# Audio Analysis
python video_audio_utils.py analyze-audio       # Comprehensive audio analysis with multiple options
python video_audio_utils.py transcribe-audio    # Quick audio transcription with speaker ID
python video_audio_utils.py describe-audio      # AI-powered audio description

# Image Analysis
python video_audio_utils.py analyze-images      # Comprehensive image analysis with 6 analysis types
python video_audio_utils.py describe-images     # Quick image description and analysis
python video_audio_utils.py extract-text        # Extract text from images (OCR)
```

## 🔧 Requirements

### System Dependencies
- **ffmpeg** - Video/audio processing engine
- **Python 3.8+** - Runtime environment

### Python Dependencies
```bash
# Core functionality (no additional dependencies needed)

# AI functionality (optional)
pip install google-generativeai  # For Gemini video understanding
```

## 🎯 Detailed Features

### Video Operations
- **Smart Cutting**: Extract precise durations with stream copy for speed
- **Format Support**: Universal support for major video formats
- **Batch Processing**: Automatically processes all videos in directory
- **Quality Preservation**: Maintains original quality when possible

### Audio Operations
- **Silent Video Detection**: Automatically identifies videos without audio
- **Audio Mixing**: Combine multiple tracks with automatic normalization
- **Audio Concatenation**: Join audio files in sequence
- **Format Conversion**: Support for all major audio formats

### Subtitle Generation
- **SRT Format**: Universal subtitle format for most players
- **WebVTT Format**: Web-optimized subtitles for browsers
- **Auto-Timing**: Intelligent timing based on words per second
- **Player Compatible**: Files load automatically in VLC, Media Player, etc.

### 🤖 AI Multimodal Understanding
- **Multi-Model Support**: Powered by Google Gemini 2.0/2.5 with multimodal capabilities
- **Comprehensive Analysis**: Description, transcription, scene detection, content analysis
- **Audio Features**: Event detection, acoustic analysis, speaker identification
- **Image Features**: Object detection, OCR, classification, composition analysis
- **Question Answering**: Ask specific questions about video, audio, or image content
- **Timestamp Support**: Precise timing information for all video/audio analysis
- **Multiple Formats**: Results saved as both JSON and text files

## 📖 Documentation

- **[Complete AI Setup Guide](GEMINI_SETUP.md)** - Step-by-step Gemini configuration
- **[Test Scripts](test_video_understanding.py)** - Comprehensive functionality tests
- **[Package API](video_utils/)** - Modular component documentation

## 🎯 Use Cases

### Content Creation
- Extract highlights from long videos
- Add background music to silent clips
- Generate professional subtitles
- Create video descriptions automatically

### Video Analysis & Research
- Transcribe interviews and meetings with timestamps
- Extract key information from educational content
- Analyze video content for indexing and search
- Generate metadata for video libraries

### Accessibility & Compliance
- Create subtitle files for deaf/hard-of-hearing viewers
- Generate video descriptions for visually impaired users
- Provide multiple subtitle formats for broad compatibility
- Meet accessibility standards for web content

### Business & Education
- Process training videos for searchable transcripts
- Analyze marketing content for key messaging
- Create summaries of long presentations
- Extract actionable insights from video conferences

## 🔒 Security & Privacy

- **Local Processing**: Core video operations run entirely offline
- **Secure API Handling**: Environment variables for API keys
- **No Data Retention**: AI services don't store video content
- **File Cleanup**: Automatic cleanup of temporary files
- **Safe Operations**: Existing file protection and validation

## 🚀 Getting Started

### 1. Clone and Setup
```bash
cd video_tools
python --version  # Ensure Python 3.8+
ffmpeg -version   # Ensure ffmpeg is installed
```

### 2. Basic Operations
```bash
# Test with sample video
python video_audio_utils.py cut 3

# Generate subtitles
python video_audio_utils.py generate-subtitles
```

### 3. AI Analysis (Optional)
```bash
# Install AI dependencies
pip install -r requirements_gemini.txt

# Configure API key (see GEMINI_SETUP.md)
export GEMINI_API_KEY=your_api_key

# Test AI features
python video_audio_utils.py describe-videos
```

### 4. Run Tests
```bash
# Test core functionality
python test_subtitles.py

# Test AI functionality
python test_video_understanding.py
```

## 📊 Performance & Optimization

- **Stream Copy**: Default mode for maximum speed and quality
- **Batch Processing**: Efficient handling of multiple files
- **Memory Efficient**: Optimized for large video files
- **Progress Tracking**: Real-time feedback for long operations
- **Error Handling**: Robust error recovery and reporting

## 🔄 Architecture

The video tools are built with a modular architecture:

- **Core Layer**: Basic video/audio operations (ffmpeg integration)
- **Processing Layer**: Specialized operations (cutting, mixing, subtitles)
- **AI Layer**: Machine learning analysis (Gemini integration)
- **Interface Layer**: CLI commands and user interaction
- **Test Layer**: Comprehensive validation and testing

This design ensures maintainability, testability, and easy extension for new features.

---

**🎉 Ready to process your videos with both traditional and AI-powered tools!**