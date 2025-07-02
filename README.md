# AI Video Generation Project

This project provides comprehensive Python implementations for generating videos using multiple AI platforms and models. It's organized into specialized folders for different video generation services.

## 🎬 Available Implementations

### 1. Google Veo Video Generation (`veo3_video_generation/`)
- **Models**: Veo 2.0 (stable) and Veo 3.0 (preview)
- **Features**: Text-to-video, Image-to-video generation
- **Quality**: High-resolution, cinematic quality
- **Setup**: Requires Google Cloud authentication and configuration

### 2. FAL AI Dual-Model Generation (`fal_video_generation/`)
- **Models**: MiniMax Hailuo-02 and Kling Video 2.1
- **Features**: Production-ready API, dual model support, cost-conscious testing
- **Quality**: 768p (Hailuo) and high-quality (Kling)
- **Setup**: Simple API key authentication
- **⚠️ Cost Warning**: Video generation costs money (~$0.02-0.05 per video)

### 3. FAL AI Avatar Generation (`fal_avatar_generation/`)
- **Model**: AI Avatar Single-Text (MultiTalk)
- **Features**: Text-to-speech avatar videos with lip-sync
- **Quality**: Talking avatars with natural expressions
- **Voices**: 20 different voice options
- **Setup**: Simple API key authentication
- **⚠️ Cost Warning**: Avatar generation costs money (~$0.02-0.05 per video)

### 4. 📹 **NEW!** FAL AI Video-to-Video Package (`fal_video_to_video/`)
- **Models**: ThinksSound (AI audio generation) and Topaz Video Upscale (professional enhancement)
- **Features**: Dual-model architecture with unified CLI interface
- **Capabilities**: Add AI-generated audio to videos, upscale videos up to 4x with frame interpolation
- **Audio Generation**: Automatic audio track creation based on video content
- **Video Upscaling**: Professional-grade video enhancement with Topaz technology
- **Setup**: Simple API key authentication (FAL AI)
- **⚠️ Cost Warning**: Video processing costs money (~$0.05-2.50 per video depending on model)

### 5. ✨ ElevenLabs Text-to-Speech Package (`text_to_speech/`)
- **Features**: Comprehensive modular TTS package with OpenRouter AI integration
- **Architecture**: Professional modular structure with 15+ focused modules
- **Capabilities**: Voice control, dialogue generation, timing control, 3000+ voices
- **Pipeline**: Complete AI content generation (OpenRouter → ElevenLabs TTS)
- **Models**: Support for top 10 OpenRouter models (Claude, Gemini, DeepSeek, etc.)
- **Setup**: Simple API key authentication (ElevenLabs + OpenRouter)

### 6. 🔧 **ENHANCED!** Video Tools with CLI Parameter Support (`video_tools/`)
- **Features**: Comprehensive video processing utilities with enhanced CLI interface
- **Architecture**: Enhanced with CLI parameter support for major commands
- **Capabilities**: Subtitle generation, AI analysis, transcription, video processing
- **CLI Enhancement**: Support for `-i` (input), `-o` (output), `-f` (format) parameters
- **Formats**: SRT/VTT subtitles, JSON/TXT outputs for analysis
- **Setup**: FFmpeg required, optional Gemini API for AI features

## 📁 Project Structure

```
veo3-video-generation/
├── README.md                           # This overview
├── CLAUDE.md                          # Claude Code project instructions
├── requirements.txt                    # Global dependencies
├── 
├── veo3_video_generation/             # Google Veo Implementation
│   ├── veo_video_generation.py        # Main Veo implementation
│   ├── demo.py                        # Interactive Veo demo
│   ├── test_veo.py                    # Comprehensive test suite
│   ├── fix_permissions.py             # GCP permissions helper
│   ├── README.md                      # Veo-specific documentation
│   └── requirements.txt               # Veo dependencies
│
├── fal_avatar_generation/             # FAL AI Avatar Implementation
│   ├── fal_avatar_generator.py        # Avatar video generator class
│   ├── demo.py                        # Cost-conscious interactive demo
│   ├── test_setup.py                  # FREE environment tests
│   ├── test_generation.py             # PAID avatar generation tests
│   ├── test_official_example.py       # Official FAL examples test
│   ├── README.md                      # Avatar generation documentation
│   └── requirements.txt               # Avatar dependencies
│
├── fal_text_to_image/                 # FAL AI Text-to-Image Implementation
│   ├── fal_text_to_image_generator.py # Multi-model image generator class
│   ├── demo.py                        # Interactive image generation demo
│   ├── test_setup.py                  # FREE environment validation
│   ├── test_generation.py             # PAID image generation tests
│   ├── README.md                      # Text-to-image documentation
│   ├── requirements.txt               # Text-to-image dependencies
│   ├── output/                        # Generated images output
│   └── test_output/                   # Test images output
│
├── fal_image_to_image/                # FAL AI Image-to-Image Implementation
│   ├── fal_image_to_image/            # Main package directory
│   │   ├── __init__.py                # Package initialization
│   │   ├── generator.py               # Core image modification logic
│   │   ├── models/                    # Model implementations
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Base model interface
│   │   │   ├── photon.py              # Luma Photon Flash model
│   │   │   ├── seededit.py            # SeedEdit model
│   │   │   └── kontext.py             # Kontext model
│   │   ├── config/                    # Configuration management
│   │   │   ├── __init__.py
│   │   │   └── constants.py           # Model constants and settings
│   │   └── utils/                     # Utility functions
│   │       ├── __init__.py
│   │       ├── file_utils.py          # File handling utilities
│   │       └── validators.py          # Input validation
│   ├── examples/                      # Usage examples and demos
│   │   ├── __init__.py
│   │   ├── basic_usage.py             # Basic usage examples
│   │   ├── demo.py                    # Interactive demo
│   │   ├── model_comparison.py        # Compare different models
│   │   ├── output/                    # Example output directory
│   │   └── test_output/               # Test output directory
│   ├── tests/                         # Test suite
│   │   ├── __init__.py
│   │   ├── test_setup.py              # FREE environment tests
│   │   ├── test_generation.py         # PAID generation tests
│   │   ├── test_package_structure.py  # Package structure validation
│   │   └── test_models/               # Model-specific tests
│   ├── docs/                          # Documentation
│   │   ├── API_REFERENCE.md           # API documentation
│   │   └── README_SEEDEDIT.md         # SeedEdit model documentation
│   ├── input/                         # Input images for testing
│   ├── output/                        # Generated images output
│   ├── setup.py                       # Package installation
│   ├── requirements.txt               # Image-to-image dependencies
│   ├── README.md                      # Image-to-image documentation
│   └── archive/                       # Legacy implementations
│
├── fal_video_to_video/                # 📹 FAL AI Video-to-Video Implementation
│   ├── fal_video_to_video/            # Main package directory
│   │   ├── __init__.py                # Package initialization
│   │   ├── __main__.py                # CLI entry point (python -m fal_video_to_video)
│   │   ├── generator.py               # Core video-to-video logic
│   │   ├── models/                    # Model implementations
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Base model interface
│   │   │   ├── thinksound.py          # ThinksSound AI audio generation
│   │   │   └── topaz.py               # Topaz Video Upscale model
│   │   ├── config/                    # Configuration management
│   │   │   ├── __init__.py
│   │   │   └── constants.py           # Model constants and settings
│   │   └── utils/                     # Utility functions
│   │       ├── __init__.py
│   │       ├── file_utils.py          # File handling utilities
│   │       └── validators.py          # Input validation
│   ├── examples/                      # Usage examples and demos
│   │   ├── __init__.py
│   │   ├── basic_usage.py             # Basic usage examples
│   │   └── demo.py                    # Interactive demo
│   ├── tests/                         # Test suite
│   │   ├── __init__.py
│   │   ├── test_setup.py              # FREE environment tests
│   │   ├── test_generation.py         # PAID generation tests
│   │   └── test_thinksound_cli.sh     # ThinksSound CLI tests
│   ├── input/                         # Input videos for testing
│   ├── output/                        # Generated videos output
│   ├── setup.py                       # Package installation
│   ├── requirements.txt               # Video-to-video dependencies
│   ├── README.md                      # Video-to-video documentation
│   └── test_topaz_upscale.sh          # Topaz upscale test script
│
├── fal_image_to_video/                # FAL AI Image-to-Video Implementation
│   ├── fal_image_to_video_generator.py # Image-to-video generator class
│   ├── demo.py                        # Cost-conscious interactive demo
│   ├── test_fal_ai.py                 # Cost-conscious test suite
│   ├── test_api_only.py               # FREE API connection test
│   ├── README.md                      # Image-to-video documentation
│   ├── COST_CONSCIOUS_TESTING.md      # Cost protection guide
│   └── requirements.txt               # Image-to-video dependencies
│
├── text_to_speech/                    # ✨ Modular TTS Package
│   ├── __init__.py                    # Package initialization
│   ├── README.md                      # TTS package documentation
│   ├── MIGRATION_GUIDE.md             # Migration from old structure
│   ├── setup.py                       # Package installation
│   ├── requirements.txt               # TTS dependencies
│   ├── models/                        # Data models and enums
│   │   ├── __init__.py
│   │   ├── common.py                  # Common data models
│   │   └── pipeline.py                # Pipeline models
│   ├── tts/                           # Core TTS functionality
│   │   ├── __init__.py
│   │   ├── controller.py              # Main TTS controller
│   │   ├── voice_manager.py           # Voice management
│   │   └── audio_processor.py         # Audio processing utilities
│   ├── pipeline/                      # OpenRouter AI integration
│   │   ├── __init__.py
│   │   └── core.py                    # AI content generation pipeline
│   ├── utils/                         # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py              # Input validation
│   │   ├── file_manager.py            # File management
│   │   └── api_helpers.py             # API helper functions
│   ├── config/                        # Configuration management
│   │   ├── __init__.py
│   │   ├── defaults.py                # Default settings
│   │   ├── voices.py                  # Voice configurations
│   │   └── models.py                  # Model configurations
│   ├── examples/                      # Usage examples
│   │   ├── __init__.py
│   │   └── basic_usage.py             # Basic TTS examples
│   ├── cli/                           # Command line tools
│   │   ├── __init__.py
│   │   ├── interactive.py             # Interactive pipeline
│   │   └── quick_start.py             # Quick start demo
│   ├── dialogue/                      # Dialogue generation (placeholder)
│   │   └── __init__.py
│   └── output/                        # Generated audio files
│
├── video_tools/                       # 🔧 Enhanced Video Processing Utilities
│   ├── README.md                      # Video tools documentation
│   ├── video_audio_utils.py           # 🆕 Enhanced CLI with parameter support
│   ├── image_modify_verify.py         # Image modification and verification
│   ├── real_video_examples.py         # Real video processing examples
│   ├── requirements_gemini.txt        # Gemini-specific requirements
│   ├── video_utils/                   # Core video processing modules
│   │   ├── __init__.py
│   │   ├── core.py                    # Core video processing
│   │   ├── commands.py                # Command utilities
│   │   ├── interactive.py             # Interactive video tools
│   │   ├── file_utils.py              # File management utilities
│   │   ├── video_processor.py         # Video processing engine
│   │   ├── audio_processor.py         # Audio processing engine
│   │   ├── subtitle_generator.py      # Subtitle generation
│   │   ├── subtitle_commands.py       # 🆕 Enhanced subtitle commands with parameters
│   │   ├── video_understanding.py     # Video analysis and understanding
│   │   ├── video_commands.py          # Video manipulation commands
│   │   ├── audio_commands.py          # Audio manipulation commands
│   │   ├── whisper_commands.py        # Whisper integration
│   │   └── ai_analysis_commands.py    # 🆕 Enhanced AI analysis with parameters
│   ├── docs/                          # Documentation
│   │   ├── API_REFERENCE.md           # API documentation
│   │   ├── BETTER_IMPLEMENTATION_ANALYSIS.md # Implementation analysis
│   │   ├── COMMAND_LINE_EXAMPLES.md   # Command line examples
│   │   └── GEMINI_SETUP.md            # Gemini setup instructions
│   ├── input/                         # Input files for testing
│   ├── output/                        # Processed output files
│   └── tests/                         # Test suite
│       ├── test_env_setup.py          # Environment setup tests
│       ├── test_image_workflow.py     # Image workflow tests
│       ├── test_subtitles.py          # Subtitle generation tests
│       ├── test_subtitles_cli.sh      # 🆕 Enhanced CLI testing
│       └── test_video_understanding.py # Video understanding tests
```

## 🚀 Quick Start

### Prerequisites: Python Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows

# Install all dependencies from root
pip install -r requirements.txt
```

**🔧 Environment Memory**: The virtual environment is now created at `/home/zdhpe/veo3-video-generation/venv/` with all dependencies installed. Always activate it before running any scripts:
```bash
source venv/bin/activate
```

### Option 1: Google Veo (High-Quality, Complex Setup)

```bash
# After activating venv
cd veo3_video_generation

# Configure Google Cloud authentication
gcloud auth login
gcloud auth application-default login
gcloud config set project your-project-id

# Update configuration in .env file
# PROJECT_ID=your-project-id
# OUTPUT_BUCKET_PATH=gs://your-bucket/veo_output/

# Run demo
python demo.py

# Or run tests
python test_veo.py
```

### Option 2: FAL AI (Simple Setup, Production Ready)

```bash
# After activating venv
cd fal_video_generation

# Configure API key in .env file
# FAL_KEY=your-fal-api-key

# Test setup first (FREE)
python test_api_only.py

# Run demo (costs money - has confirmation prompts)
python demo.py

# Or run specific model tests (costs money)
python test_fal_ai.py --hailuo    # ~$0.02-0.05
python test_fal_ai.py --kling     # ~$0.02-0.05
```

### Option 3: 📹 **NEW!** FAL AI Video-to-Video Package (Audio Generation + Upscaling)

```bash
# After activating venv
cd fal_video_to_video

# Configure API key in .env file
# FAL_KEY=your-fal-api-key

# Test setup first (FREE)
python -m fal_video_to_video list-models

# Add AI-generated audio to video
python -m fal_video_to_video add-audio -i input/video.mp4

# Add audio with custom prompt
python -m fal_video_to_video add-audio -i input/video.mp4 -p "add dramatic music"

# Upscale video with 2x factor
python -m fal_video_to_video upscale -i input/video.mp4 --upscale-factor 2

# Upscale with frame interpolation to 60 FPS
python -m fal_video_to_video upscale -i input/video.mp4 --upscale-factor 2 --target-fps 60

# Batch processing
python -m fal_video_to_video batch -f batch.json

# Test with sample video
bash test_topaz_upscale.sh
```

### Option 4: ✨ Text-to-Speech Package (Professional TTS + AI)

```bash
# After activating venv
cd text_to_speech

# Configure API keys in .env file (or environment variables)
# ELEVENLABS_API_KEY=your-elevenlabs-key
# OPENROUTER_API_KEY=your-openrouter-key

# Basic TTS usage
python examples/basic_usage.py

# Interactive pipeline (AI content generation → TTS)
python cli/interactive.py

# Quick start demo
python cli/quick_start.py

# Advanced usage examples
python -c "
from text_to_speech import ElevenLabsTTSController
tts = ElevenLabsTTSController('your-api-key')
tts.text_to_speech_with_timing_control(
    text='Hello! This is the new modular TTS package.',
    voice_name='rachel',
    output_file='output/welcome.mp3'
)
"
```

### Option 5: 🔧 **ENHANCED!** Video Tools with CLI Parameters (Video Processing + AI)

```bash
# After activating venv
cd video_tools

# Test enhanced CLI functionality
bash tests/test_subtitles_cli.sh

# Enhanced subtitle generation with parameters
python3 video_audio_utils.py generate-subtitles -i input/video.mp4 -o output/subtitle.srt -f srt
python3 video_audio_utils.py generate-subtitles -i input/ -o output/ -f vtt

# Enhanced AI analysis with parameters (requires GEMINI_API_KEY)
python3 video_audio_utils.py describe-videos -i input/video.mp4 -o output/description.json
python3 video_audio_utils.py transcribe-videos -i input/video.mp4 -o output/transcript.txt

# Traditional mode (no parameters) - still supported
python3 video_audio_utils.py generate-subtitles
python3 video_audio_utils.py describe-videos

# Other video processing commands
python3 video_audio_utils.py cut 10           # Cut first 10 seconds
python3 video_audio_utils.py extract-audio    # Extract audio tracks
```

## 🔧 Setup Requirements

### Google Veo Requirements
- Google Cloud Project with Vertex AI API enabled
- Google Cloud Storage bucket
- Proper authentication (gcloud CLI)
- Python 3.8+
- Veo 3.0 requires allowlist approval

### FAL AI Requirements
- FAL AI API key (from fal.ai)
- Python 3.8+
- Internet connection

### Text-to-Speech Package Requirements
- ElevenLabs API key (from elevenlabs.io)
- OpenRouter API key (from openrouter.ai) - for AI content generation
- Python 3.8+
- Internet connection
- **New Modular Architecture**: Recently refactored for professional development

### Video Tools Requirements
- FFmpeg (required for video processing)
- Python 3.8+
- **Optional**: Gemini API key (for AI analysis features)
- **Enhanced CLI**: Recently added parameter support for major commands

## 📊 Feature Comparison

### Video Generation Models

| Feature | Google Veo 2.0 | Google Veo 3.0 | FAL Hailuo-02 | FAL Kling 2.1 |
|---------|----------------|----------------|---------------|----------------|
| **Resolution** | High | Higher | 768p | High-quality |
| **Setup Complexity** | Complex | Complex | Simple | Simple |
| **Authentication** | Google Cloud | Google Cloud | API Key | API Key |
| **Access** | Generally Available | Preview/Allowlist | Public API | Public API |
| **Generation Time** | 2-10 min | 2-10 min | 1-3 min | 1-3 min |
| **Best For** | Cinematic quality | Latest features | Quick prototyping | High-quality production |

### 📹 Video-to-Video Processing Models

| Feature | ThinksSound | Topaz Video Upscale |
|---------|-------------|---------------------|
| **Purpose** | AI audio generation | Professional video upscaling |
| **Input** | Video files (any format) | Video files (any format) |
| **Output** | Video with AI-generated audio | Upscaled video (up to 4x) |
| **Cost** | ~$0.05-0.10 per video | ~$0.50-2.50 per video |
| **Processing Time** | 30-60 seconds | 30-120 seconds |
| **Features** | Custom prompts, automatic audio | Frame interpolation, quality enhancement |
| **Best For** | Adding soundtracks, audio enhancement | Upscaling, quality improvement |

### ✨ Text-to-Speech Package Features

| Feature | Description | Status |
|---------|-------------|---------|
| **Architecture** | Modular package structure (15+ focused modules) | ✅ Recently refactored |
| **Voice Library** | 3000+ ElevenLabs voices + popular presets | ✅ Comprehensive |
| **AI Integration** | OpenRouter (Claude, Gemini, DeepSeek, etc.) | ✅ Top 10 models |
| **Pipeline** | Description → AI Content → Speech | ✅ End-to-end |
| **Features** | Timing control, dialogue, voice cloning | ✅ Professional |
| **Setup** | Simple API keys (ElevenLabs + OpenRouter) | ✅ Easy |

### 🔧 Video Tools Enhanced CLI Features

| Feature | Description | Status |
|---------|-------------|---------|
| **CLI Parameters** | `-i`, `-o`, `-f` support for major commands | ✅ Recently implemented |
| **Subtitle Generation** | SRT/VTT format with enhanced parameters | ✅ Enhanced |
| **AI Analysis** | describe-videos/transcribe-videos with parameters | ✅ Enhanced |
| **Backward Compatibility** | Traditional mode (no parameters) still supported | ✅ Maintained |
| **Testing** | Automated CLI test suite | ✅ Comprehensive |
| **Video Processing** | Cut, extract, audio manipulation | ✅ Full featured |

## 🎯 Use Cases

### Choose Google Veo When:
- You need the highest quality video generation
- You have Google Cloud infrastructure
- You're building enterprise applications
- Quality is more important than speed

### Choose FAL AI When:
- You want quick setup and testing
- You need reliable production API
- You want to compare multiple models
- You prefer simple API key authentication

### Choose Text-to-Speech Package When:
- You need professional voice synthesis
- You want AI-generated content with speech
- You need multi-speaker dialogue generation
- You want a complete content creation pipeline
- You prefer modular, maintainable code architecture

### Choose FAL AI Video-to-Video When:
- You need to add AI-generated audio to existing videos
- You want to upscale videos for better quality
- You need professional video enhancement capabilities
- You prefer unified CLI interface for multiple video operations
- You want cost-effective video processing with predictable pricing
- You need both batch processing and single video operations

### Choose Video Tools When:
- You need to process existing videos (cut, extract, modify)
- You want to generate subtitles for videos (SRT/VTT formats)
- You need AI-powered video analysis and transcription
- You prefer CLI tools with parameter support
- You want both interactive and batch processing modes
- You need comprehensive video processing utilities

## 🛠️ Development Features

### Google Veo Features
- ✅ Text-to-video generation
- ✅ Image-to-video generation
- ✅ Multiple model support (2.0 + 3.0)
- ✅ Local image processing
- ✅ Automatic GCS upload/download
- ✅ Comprehensive error handling
- ✅ Interactive demo with model selection
- ✅ Full test suite with comparison

### FAL AI Features
- ✅ Dual-model architecture (Hailuo + Kling)
- ✅ Universal methods with full endpoint names
- ✅ Model-specific optimization
- ✅ Cost-conscious interactive demo with confirmation prompts
- ✅ Cost-conscious testing framework with FREE options
- ✅ Production-ready error handling
- ✅ Automatic video download
- ✅ Model performance comparison
- ⚠️ Cost protection with explicit user confirmation required

### 📹 FAL AI Video-to-Video Features
- ✅ **Dual-Model Architecture**: ThinksSound (audio) + Topaz (upscaling)
- ✅ **Unified CLI Interface**: Single command structure for both models
- ✅ **Audio Generation**: AI-powered audio track creation with custom prompts
- ✅ **Video Upscaling**: Professional-grade enhancement up to 4x resolution
- ✅ **Frame Interpolation**: Target FPS control for smooth video playback
- ✅ **Batch Processing**: Process multiple videos with JSON configuration
- ✅ **Cost Management**: Predictable pricing with model-specific cost estimates
- ✅ **File Management**: Automatic upload/download with progress tracking
- ✅ **Error Handling**: Comprehensive validation and error recovery
- ✅ **Testing Suite**: Complete test coverage with sample videos

### ✨ Text-to-Speech Package Features
- ✅ **Modular Architecture**: 15+ focused modules (150-300 lines each)
- ✅ **Professional Package**: setup.py, proper imports, clean structure
- ✅ **Voice Control**: 3000+ voices, popular presets, custom cloning
- ✅ **AI Integration**: OpenRouter (Claude, Gemini, DeepSeek, etc.)
- ✅ **Complete Pipeline**: Description → AI Content → Speech
- ✅ **Multi-Speaker Dialogue**: Emotional tags, voice pairing
- ✅ **Timing Control**: Speed, pauses, natural speech patterns
- ✅ **Utilities**: Validation, file management, error handling
- ✅ **Configuration**: Voice presets, model settings, defaults
- ✅ **Examples & CLI**: Interactive tools, usage examples
- ✅ **Backward Compatible**: Existing code works with minimal changes
- 📚 **Migration Guide**: Complete transition documentation

### 🔧 Video Tools Enhanced Features
- ✅ **Enhanced CLI Architecture**: Parameter support for major commands
- ✅ **Subtitle Generation**: SRT/VTT formats with `-i`, `-o`, `-f` parameters
- ✅ **AI Analysis**: describe-videos and transcribe-videos with parameter support
- ✅ **Video Processing**: Cut, extract audio, format conversion
- ✅ **Batch Processing**: Directory-level operations with enhanced CLI
- ✅ **Backward Compatibility**: Traditional mode (no parameters) still supported
- ✅ **Comprehensive Testing**: Automated CLI test suite with validation
- ✅ **FFmpeg Integration**: Professional video processing capabilities
- ✅ **Gemini AI Integration**: Optional AI-powered video analysis
- ✅ **File Management**: Intelligent input/output path handling

## 📖 Documentation

Each implementation has its own detailed documentation:

- **Google Veo**: See [`veo3_video_generation/README.md`](veo3_video_generation/README.md)
- **FAL AI Video**: See [`fal_video_generation/README.md`](fal_video_generation/README.md)
- **📹 FAL AI Video-to-Video**: See [`fal_video_to_video/README.md`](fal_video_to_video/README.md)
- **FAL AI Avatar**: See [`fal_avatar_generation/README.md`](fal_avatar_generation/README.md)
- **✨ Text-to-Speech**: See [`text_to_speech/README.md`](text_to_speech/README.md)
  - **Migration Guide**: [`text_to_speech/MIGRATION_GUIDE.md`](text_to_speech/MIGRATION_GUIDE.md)
  - **Setup Instructions**: [`text_to_speech/setup.py`](text_to_speech/setup.py)
- **🔧 Video Tools**: See [`video_tools/README.md`](video_tools/README.md)
  - **CLI Examples**: [`video_tools/docs/COMMAND_LINE_EXAMPLES.md`](video_tools/docs/COMMAND_LINE_EXAMPLES.md)
  - **API Reference**: [`video_tools/docs/API_REFERENCE.md`](video_tools/docs/API_REFERENCE.md)

## 🧪 Testing

### Test Google Veo Implementation
```bash
cd veo3_video_generation

# Basic tests
python test_veo.py

# Test Veo 3.0 specifically
python test_veo.py --veo3

# Compare both models
python test_veo.py --compare

# Full comprehensive tests
python test_veo.py --full
```

### Test FAL AI Implementation

⚠️ **Cost Warning**: Video generation tests cost money! Always start with FREE tests.

```bash
cd fal_video_generation

# FREE Tests (no cost)
python test_api_only.py              # API connection test only
python test_fal_ai.py                # Setup validation only

# Paid Tests (generate real videos)
python test_fal_ai.py --hailuo       # Test Hailuo model (~$0.02-0.05)
python test_fal_ai.py --kling        # Test Kling model (~$0.02-0.05)
python test_fal_ai.py --compare      # Test both models (~$0.04-0.10)
```

### Test Text-to-Speech Package

✅ **No Cost**: Text-to-speech testing supports dummy API keys for structure validation.

```bash
cd text_to_speech

# Test package structure (FREE - no API calls)
python -c "
import sys
sys.path.append('..')
from text_to_speech import ElevenLabsTTSController
print('✅ Package imports working!')
"

# Test with dummy keys (FREE - no API calls)
python examples/basic_usage.py       # Basic TTS examples

# Test individual modules
python -c "
from text_to_speech.utils.validators import validate_text_input
print('✅ Utilities working!')
"

# Interactive demos (requires real API keys)
python cli/interactive.py            # Interactive pipeline
python cli/quick_start.py           # Quick start demo
```

### Test Video Tools Enhanced CLI

✅ **No Cost**: Video tools testing uses local files and FFmpeg validation.

```bash
cd video_tools

# Test enhanced CLI functionality (FREE)
bash tests/test_subtitles_cli.sh

# Test individual components
python tests/test_subtitles.py        # Subtitle generation tests
python tests/test_env_setup.py        # Environment validation

# Manual testing with enhanced CLI parameters
# Subtitle generation (requires FFmpeg)
python3 video_audio_utils.py generate-subtitles -i input/sample_video.mp4 -o output/test.srt -f srt

# AI analysis (requires GEMINI_API_KEY - optional)
python3 video_audio_utils.py describe-videos -i input/sample_video.mp4 -o output/description.json

# Traditional mode testing (backward compatibility)
python3 video_audio_utils.py generate-subtitles  # Interactive mode
python3 video_audio_utils.py cut 5               # Cut first 5 seconds
```

## 🎮 Interactive Demos

All implementations include interactive demos:

```bash
# Google Veo Demo
cd veo3_video_generation && python demo.py

# FAL AI Video Demo (costs money - has confirmation prompts)
cd fal_video_generation && python demo.py

# FAL AI Avatar Demo (costs money - has confirmation prompts)
cd fal_avatar_generation && python demo.py

# 📹 FAL AI Video-to-Video Demo (costs money - has confirmation prompts)
cd fal_video_to_video && python examples/demo.py

# ✨ Text-to-Speech Interactive Pipeline
cd text_to_speech && python cli/interactive.py

# ✨ Text-to-Speech Quick Start Demo
cd text_to_speech && python cli/quick_start.py

# 🔧 Video Tools Enhanced CLI (Interactive & Batch modes)
cd video_tools && python3 video_audio_utils.py generate-subtitles  # Interactive mode
cd video_tools && bash tests/test_subtitles_cli.sh                 # Automated testing
```

The demos provide:
- **Video Generation**: Model selection menus with cost warnings
- **Video Features**: Pre-configured test prompts, image-to-video testing
- **Cost Protection**: Confirmation prompts before generating videos
- **✨ TTS Pipeline**: AI content generation → speech conversion
- **✨ TTS Features**: Voice selection, timing control, multi-speaker dialogue
- **🔧 Video Processing**: Enhanced CLI with parameter support, batch operations
- **🔧 Subtitle Generation**: Interactive and parameterized subtitle creation
- **Configuration Validation**: Setup verification for all platforms

## 🔍 Troubleshooting

### Common Issues

#### Google Veo Issues
- **"Project not allowlisted"**: Use Veo 2.0 or request Veo 3.0 access
- **Permission denied**: Check GCS bucket permissions
- **Authentication failed**: Run `gcloud auth application-default login`

#### FAL AI Issues
- **Invalid API key**: Check your FAL_KEY in .env file
- **Rate limiting**: Wait between requests or upgrade plan
- **Model not available**: Try alternative model
- **Unexpected charges**: Always use FREE tests first (`test_api_only.py`)

#### ✨ Text-to-Speech Issues
- **Import errors**: Ensure `PYTHONPATH` includes project root or install with `pip install -e .`
- **Invalid API key**: Check `ELEVENLABS_API_KEY` and `OPENROUTER_API_KEY` in environment
- **Missing List import**: Fixed in latest version (use `from typing import List`)
- **Old import errors**: Use migration guide to update from monolithic structure
- **Package structure**: Use new modular imports (see `MIGRATION_GUIDE.md`)

### Getting Help

1. Check the specific README for your implementation
2. Review the test suite output for diagnostic information
3. Run the demo to validate your setup
4. Check the troubleshooting sections in each implementation's README

## ⚠️ Cost Protection

**IMPORTANT**: FAL AI video generation costs money (~$0.02-0.05 per video). This project includes cost protection measures:

- **FREE tests available**: Use `test_api_only.py` for setup validation
- **Cost warnings**: All paid operations show cost estimates
- **Confirmation prompts**: User must explicitly confirm before generating videos
- **Model-specific testing**: Test individual models to avoid unnecessary costs

**Always start with FREE tests before running paid video generation!**

## 🚧 Development Status

- ✅ **Google Veo**: Production ready with comprehensive testing
- ✅ **FAL AI Video**: Production ready with cost-conscious dual-model support
- ✅ **📹 FAL AI Video-to-Video**: Production ready with dual-model audio/upscaling support
  - 🆕 **Architecture**: Unified CLI interface for ThinksSound and Topaz models
  - ✅ **Audio Generation**: AI-powered soundtrack creation with prompt support
  - ✅ **Video Upscaling**: Professional 4x enhancement with frame interpolation
  - ✅ **Testing**: Complete test coverage with automated validation scripts
- ✅ **FAL AI Avatar**: Production ready with text-to-speech integration
- ✅ **✨ Text-to-Speech**: Recently refactored to modular architecture - fully functional
  - 🆕 **Architecture**: Transformed from 3 monolithic files (2,500+ lines) to 15+ focused modules
  - ✅ **Testing**: Comprehensive test suite with import validation
  - ✅ **Migration**: Complete migration guide and backward compatibility
  - ✅ **Professional**: Setup.py, proper package structure, CLI tools
- ✅ **🔧 Video Tools**: Recently enhanced with CLI parameter support - fully functional
  - 🆕 **Enhanced CLI**: Added `-i`, `-o`, `-f` parameter support for major commands
  - ✅ **Subtitle Generation**: SRT/VTT format support with enhanced parameters
  - ✅ **AI Integration**: describe-videos and transcribe-videos with parameter support
  - ✅ **Backward Compatibility**: Traditional mode (no parameters) still supported
  - ✅ **Testing**: Automated CLI test suite with comprehensive validation
- 🔄 **Future**: Additional model integrations and enhanced pipeline features planned

## 📝 License

This project is open source. Please check individual implementation folders for specific licensing information.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📚 Resources

### Google Veo Resources
- [Veo API Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation)
- [Google GenAI SDK](https://github.com/google/generative-ai-python)
- [Vertex AI Console](https://console.cloud.google.com/vertex-ai)

### FAL AI Resources
- [FAL AI Platform](https://fal.ai/)
- [MiniMax Hailuo Documentation](https://fal.ai/models/fal-ai/minimax-video-01)
- [Kling Video 2.1 Documentation](https://fal.ai/models/fal-ai/kling-video/v2.1/standard/image-to-video/api)
- [FAL AI Avatar Documentation](https://fal.ai/models/fal-ai/avatar-video)
- [📹 ThinksSound API Documentation](https://fal.ai/models/fal-ai/thinksound/api)
- [📹 Topaz Video Upscale Documentation](https://fal.ai/models/fal-ai/topaz/upscale/video/api)

### ✨ Text-to-Speech Resources
- [ElevenLabs API Documentation](https://elevenlabs.io/docs/capabilities/text-to-speech)
- [OpenRouter Platform](https://openrouter.ai/)
- [ElevenLabs Voice Library](https://elevenlabs.io/app/speech-synthesis/text-to-speech)
- [Text-to-Dialogue Documentation](https://elevenlabs.io/docs/cookbooks/text-to-dialogue)
- [Package Migration Guide](text_to_speech/MIGRATION_GUIDE.md)

---

**🎬 Happy Creating!** Choose the implementation that best fits your needs and start creating amazing AI-generated videos and professional text-to-speech content! 🎙️ 