# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive AI content generation project supporting multiple platforms and content types:
- **Google Veo** (Vertex AI): High-resolution, enterprise-grade video generation
- **FAL AI Video**: Simple API-based generation with dual models (MiniMax Hailuo-02 and Kling Video 2.1)
- **FAL AI Text-to-Video**: Unified text-to-video generation with dual model support (MiniMax Hailuo-02 Pro and Google Veo 3)
- **FAL AI Avatar**: Talking avatar generation with text-to-speech and audio-to-avatar capabilities
- **FAL AI Text-to-Image**: Multi-model image generation (Imagen 4, Seedream v3, FLUX.1)
- **FAL AI Image-to-Image**: AI-powered image modification using Luma Photon Flash
- **Text-to-Speech**: Professional voice synthesis with ElevenLabs integration
- **Video Tools**: Comprehensive video processing and analysis utilities

## Common Commands

### Google Veo Commands (veo3_video_generation/)
```bash
cd veo3_video_generation
pip install -r requirements.txt

# Quick setup (fixes 90% of permission issues)
python fix_permissions.py

# Run tests
python test_veo.py                    # Basic tests
python test_veo.py --veo3             # Test Veo 3.0
python test_veo.py --compare          # Compare models
python test_veo.py --full             # Comprehensive tests

# Interactive demo
python demo.py
```

### FAL AI Video Commands (fal_video_generation/)
```bash
cd fal_video_generation
pip install -r requirements.txt

# Run tests
python test_fal_ai.py                 # Basic setup test
python test_fal_ai.py --quick         # Quick video generation
python test_fal_ai.py --compare       # Compare both models
python test_fal_ai.py --kling         # Test Kling model only

# Interactive demo
python demo.py
```

### FAL AI Avatar Commands (fal_avatar_generation/)
```bash
cd fal_avatar_generation
pip install -r requirements.txt

# Setup and environment tests (FREE)
python test_setup.py                 # Validate setup without costs
python test_generation.py            # Test avatar generation with costs
python test_official_example.py      # Test with official FAL examples

# Interactive demo
python demo.py
```

### FAL AI Text-to-Image Commands (fal_text_to_image/)
```bash
cd fal_text_to_image
pip install -r requirements.txt

# Setup and environment tests (FREE)
python test_setup.py                 # Validate setup without costs
python test_generation.py            # Test image generation with costs

# Interactive demo
python demo.py
```

### FAL AI Image-to-Image Commands (fal_image_to_image/)
```bash
cd fal_image_to_image
pip install -r requirements.txt

# Setup and environment tests (FREE)
python test_setup.py                 # Validate setup without costs
python test_generation.py            # Test image modification with costs
python test_generation.py --quick    # Quick single test
python test_generation.py --batch    # Batch processing test

# Interactive demo
python demo.py
```

### FAL AI Text-to-Video Commands (fal_text_to_video/)
```bash
cd fal_text_to_video
pip install -r requirements.txt

# Setup and environment tests (FREE)
python test_setup.py                 # Validate setup without costs
python test_generation.py            # Test video generation with costs

# Interactive demo
python demo.py
```

### Text-to-Speech Commands (text_to_speech/)
```bash
cd text_to_speech
pip install -r requirements.txt

# Basic usage examples
python examples/basic_usage.py       # Simple text-to-speech conversion
python cli/quick_start.py           # Quick start CLI interface
python cli/interactive.py           # Interactive voice selection
```

### Video Tools Commands (video_tools/)
```bash
cd video_tools
pip install -r requirements.txt

# Run test suite
python run_tests.py                  # Comprehensive test runner
python tests/run_quick_tests.py      # Quick functionality tests

# Enhanced CLI tool
python enhanced_cli.py              # Interactive video processing
```

## Architecture

### Directory Structure
- `veo3_video_generation/` - Google Veo implementation (function-based)
- `fal_video_generation/` - FAL AI video generation (class-based)
- `fal_text_to_video/` - FAL AI text-to-video generation with dual model support (class-based)
- `fal_avatar_generation/` - FAL AI avatar generation (class-based)
- `fal_text_to_image/` - FAL AI text-to-image generation (class-based)
- `fal_image_to_image/` - FAL AI image-to-image modification (class-based)
- `text_to_speech/` - ElevenLabs text-to-speech integration (class-based)
- `video_tools/` - Video processing utilities (class-based with CLI)

### Google Veo Architecture
- **Function-based approach** in `veo_video_generation.py`
- Key functions: `generate_video_from_text()`, `generate_video_from_image()`, `generate_video_from_local_image()`
- Authentication pattern: Sets environment variables, initializes GenAI client
- Output: GCS URIs, automatic download to `result_folder/`

### FAL AI Architecture
- **Class-based approach** across all FAL AI modules
- Video: `FALVideoGenerator` with dual model support (MiniMax Hailuo-02 and Kling Video 2.1)  
- Text-to-Video: `FALTextToVideoGenerator` with unified dual model support (MiniMax Hailuo-02 Pro and Google Veo 3)
- Avatar: `FALAvatarGenerator` with text-to-speech and audio-to-avatar modes
- Text-to-Image: `FALTextToImageGenerator` with 4 model support (Imagen 4, Seedream v3, FLUX.1 Schnell/Dev)
- Image-to-Image: `FALImageToImageGenerator` with Luma Photon Flash for creative modifications
- Universal methods with model parameter selection
- Async processing support with polling
- Output: Local downloads to `output/` directory

### Text-to-Speech Architecture
- **Class-based approach** with ElevenLabs integration
- Modular design with separate voice management, audio processing, and pipeline control
- Support for 20+ voice options with customizable settings
- CLI interfaces for quick start and interactive usage
- Package structure with proper setup.py for distribution

### Video Tools Architecture  
- **Enhanced class-based approach** with comprehensive video processing
- Modular command system with specialized processors
- Support for AI analysis, audio extraction, subtitle generation
- Interactive CLI with enhanced user experience
- Organized test suite in `tests/` directory with comprehensive coverage

## Configuration Requirements

### Google Veo Setup
1. Run automated setup: `python veo3_video_generation/fix_permissions.py`
2. Configure `.env` in veo3_video_generation/:
   ```
   PROJECT_ID=your-project-id
   OUTPUT_BUCKET_PATH=gs://your-bucket/veo_output/
   ```
3. Google Cloud authentication:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   gcloud config set project your-project-id
   ```

### FAL AI Setup
All FAL AI modules require the same setup:
1. Configure `.env` in each FAL directory (fal_video_generation/, fal_text_to_video/, fal_avatar_generation/, fal_text_to_image/, fal_image_to_image/):
   ```
   FAL_KEY=your_fal_api_key
   ```
2. Run setup tests first: `python test_setup.py` (FREE - no API costs)

### Text-to-Speech Setup
1. Configure `.env` in text_to_speech/:
   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```
2. Install dependencies: `pip install -r requirements.txt`
3. Test with examples: `python examples/basic_usage.py`

### Video Tools Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Optional: Install Gemini requirements: `pip install -r requirements_gemini.txt`
3. Run tests: `python run_tests.py` or `python tests/run_quick_tests.py`

## Development Patterns

### Error Handling
- Google Veo: Return None on failure, use `traceback.print_exc()` for debugging
- FAL AI: Comprehensive try-catch blocks with detailed error messages

### Authentication Patterns
- Google Veo: Environment variable setup, remove GOOGLE_APPLICATION_CREDENTIALS for default auth
- FAL AI: Simple API key via fal_client.api_key

### File Management
- Google Veo: GCS upload/download, local images in `images/`, output in `result_folder/`
- FAL AI: Direct API uploads, output in `output/` and `test_output/`

## Testing Strategy

### Test Files
- `veo3_video_generation/test_veo.py` - Comprehensive Google Veo testing
- `fal_video_generation/test_fal_ai.py` - Unified FAL AI dual-model testing
- `fal_text_to_video/test_setup.py` - FREE setup validation
- `fal_text_to_video/test_generation.py` - Text-to-video generation testing
- `fal_avatar_generation/test_setup.py` - FREE setup validation
- `fal_avatar_generation/test_generation.py` - Avatar generation testing
- `fal_text_to_image/test/test_setup.py` - FREE setup validation
- `fal_text_to_image/test/test_generation.py` - Image generation testing
- `fal_image_to_image/test_setup.py` - FREE setup validation
- `fal_image_to_image/test_generation.py` - Image modification testing
- `text_to_speech/examples/basic_usage.py` - Text-to-speech examples
- `video_tools/run_tests.py` - Comprehensive video tools test runner
- `video_tools/tests/` - Organized test suite with multiple test modules

### Test Command Patterns
All test suites support:
- Setup tests (FREE): `python test_setup.py` 
- Basic tests (default): `python test_[module].py`
- Model-specific tests: `--veo3`, `--kling`, `--flux`, etc.
- Comparison tests: `--compare`
- Quick tests: `--quick`, `--full`

## Model Selection Guidelines

### Use Google Veo when:
- Need highest resolution (1080p+)
- Enterprise/production deployment
- Already using Google Cloud infrastructure
- Quality over speed

### Use FAL AI Video when:
- Quick prototyping and testing
- Simple API key authentication
- Need model comparison capabilities
- Production-ready API requirements

### Use FAL AI Avatar when:
- Need talking avatar videos
- Text-to-speech integration (20 voice options)
- Custom audio lip-sync
- Marketing/presentation content

### Use FAL AI Text-to-Image when:
- Need multiple model options
- Bilingual text prompts (Seedream v3)
- Fast generation (FLUX.1 Schnell)
- High-quality images (FLUX.1 Dev, Imagen 4)

### Use FAL AI Text-to-Video when:
- Need unified dual model support
- Want cost-effective video generation (MiniMax ~$0.08)
- Need premium quality with advanced controls (Google Veo 3 ~$2.50-$6.00)
- Prefer single interface for multiple models
- Want built-in cost management features

### Use FAL AI Image-to-Image when:
- Need to modify existing images
- Want creative transformations
- Artistic style transfers
- Photo enhancement and effects

### Use Text-to-Speech when:
- Need professional voice synthesis
- Want multiple voice options (20+ voices)
- Require commercial-grade audio quality
- Need ElevenLabs integration

### Use Video Tools when:
- Need comprehensive video processing
- Want AI-powered video analysis
- Require subtitle generation
- Need audio extraction and processing
- Want interactive CLI video editing

## Important Implementation Details

### Google Veo Specifics
- Veo 3.0 requires allowlist approval
- Uses `us-central1` region for Vertex AI
- Automatic permission fixing via `fix_permissions.py`
- Support for both text-to-video and image-to-video

### FAL AI Specifics
**Video Models:**
- MiniMax Hailuo-02: 768p, 6-10s, prompt optimizer
- Kling Video 2.1: High-quality, 5-10s, CFG scale, negative prompts

**Text-to-Video Models:**
- MiniMax Hailuo-02 Pro: 1080p, 6s, cost-effective (~$0.08)
- Google Veo 3: 720p, 5-8s, premium quality (~$2.50-$6.00), audio support
- Unified interface with model selection via TextToVideoModel enum

**Avatar Models:**
- Text-to-Speech: 20 voice options, automatic speech generation
- Audio-to-Avatar: Custom audio files, lip-sync animation
- Supports both local and remote images/audio

**Text-to-Image Models:**
- Imagen 4 Preview Fast: Cost-effective Google model
- Seedream v3: Bilingual (Chinese/English) support
- FLUX.1 Schnell: Fastest inference speed
- FLUX.1 Dev: Highest quality 12B parameter model

**Image-to-Image Model:**
- Luma Photon Flash: Creative, personalizable, intelligent modifications
- Adjustable strength (0.0-1.0) for modification intensity
- 7 aspect ratio options (1:1, 16:9, 9:16, 4:3, 3:4, 21:9, 9:21)
- Support for both local files and remote URLs

**Common Features:**
- Unified class architecture across all modules
- Built-in async processing with progress updates
- Comprehensive error handling and validation

### Text-to-Speech Specifics
- **ElevenLabs Integration**: Professional voice synthesis API
- **Voice Options**: 20+ voices with customizable settings
- **Audio Quality**: High-quality MP3 output
- **Package Structure**: Modular design with CLI interfaces
- **Configuration**: Support for voice settings, stability, and clarity controls

### Video Tools Specifics
- **Enhanced Architecture**: Class-based modular design
- **AI Analysis**: Integration with Gemini for video understanding
- **Audio Processing**: Extract, analyze, and manipulate audio tracks
- **Subtitle Generation**: Automatic subtitle creation and formatting
- **Interactive CLI**: User-friendly command-line interface
- **Test Organization**: Comprehensive test suite in dedicated `tests/` directory

## Environment Variables
- Never commit `.env` files
- Each implementation has separate `.env` files
- Use environment-specific configurations
- Google Veo requires multiple Google Cloud environment variables
- All FAL AI modules only require `FAL_KEY`
- Text-to-Speech requires `ELEVENLABS_API_KEY`
- Video Tools supports optional `GEMINI_API_KEY` for AI analysis

## Cost Management
- Always run `test_setup.py` first (FREE)
- Use cost-conscious testing: `fal_video_generation/COST_CONSCIOUS_TESTING.md` 
- Video generation (MiniMax): ~$0.05-0.10 per video
- Text-to-Video (MiniMax Hailuo-02 Pro): ~$0.08 per video
- Text-to-Video (Google Veo 3): ~$2.50-6.00 per video
- Avatar generation: ~$0.02-0.05 per video
- Text-to-Image: varies by model (~$0.001-0.01 per image)
- Image-to-Image: ~$0.01-0.05 per modification
- Text-to-Speech: varies by usage (ElevenLabs pricing)