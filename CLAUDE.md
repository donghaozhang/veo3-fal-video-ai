# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive AI content generation project supporting multiple platforms and content types:
- **Google Veo** (Vertex AI): High-resolution, enterprise-grade video generation
- **FAL AI Video**: Simple API-based generation with dual models (MiniMax Hailuo-02 and Kling Video 2.1)
- **FAL AI Avatar**: Talking avatar generation with text-to-speech and audio-to-avatar capabilities
- **FAL AI Text-to-Image**: Multi-model image generation (Imagen 4, Seedream v3, FLUX.1)
- **FAL AI Image-to-Image**: AI-powered image modification using Luma Photon Flash

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

## Architecture

### Directory Structure
- `veo3_video_generation/` - Google Veo implementation (function-based)
- `fal_video_generation/` - FAL AI video generation (class-based)
- `fal_avatar_generation/` - FAL AI avatar generation (class-based)
- `fal_text_to_image/` - FAL AI text-to-image generation (class-based)
- `fal_image_to_image/` - FAL AI image-to-image modification (class-based)
- `video_tools/` - Video processing utilities

### Google Veo Architecture
- **Function-based approach** in `veo_video_generation.py`
- Key functions: `generate_video_from_text()`, `generate_video_from_image()`, `generate_video_from_local_image()`
- Authentication pattern: Sets environment variables, initializes GenAI client
- Output: GCS URIs, automatic download to `result_folder/`

### FAL AI Architecture
- **Class-based approach** across all FAL AI modules
- Video: `FALVideoGenerator` with dual model support (MiniMax Hailuo-02 and Kling Video 2.1)  
- Avatar: `FALAvatarGenerator` with text-to-speech and audio-to-avatar modes
- Text-to-Image: `FALTextToImageGenerator` with 4 model support (Imagen 4, Seedream v3, FLUX.1 Schnell/Dev)
- Image-to-Image: `FALImageToImageGenerator` with Luma Photon Flash for creative modifications
- Universal methods with model parameter selection
- Async processing support with polling
- Output: Local downloads to `output/` directory

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
1. Configure `.env` in each FAL directory (fal_video_generation/, fal_avatar_generation/, fal_text_to_image/, fal_image_to_image/):
   ```
   FAL_KEY=your_fal_api_key
   ```
2. Run setup tests first: `python test_setup.py` (FREE - no API costs)

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
- `fal_avatar_generation/test_setup.py` - FREE setup validation
- `fal_avatar_generation/test_generation.py` - Avatar generation testing
- `fal_text_to_image/test_setup.py` - FREE setup validation
- `fal_text_to_image/test_generation.py` - Image generation testing
- `fal_image_to_image/test_setup.py` - FREE setup validation
- `fal_image_to_image/test_generation.py` - Image modification testing

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

### Use FAL AI Image-to-Image when:
- Need to modify existing images
- Want creative transformations
- Artistic style transfers
- Photo enhancement and effects

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

## Environment Variables
- Never commit `.env` files
- Each implementation has separate `.env` files
- Use environment-specific configurations
- Google Veo requires multiple Google Cloud environment variables
- All FAL AI modules only require `FAL_KEY`

## Cost Management
- Always run `test_setup.py` first (FREE)
- Use cost-conscious testing: `fal_video_generation/COST_CONSCIOUS_TESTING.md` 
- Avatar generation: ~$0.02-0.05 per video
- Text-to-Image: varies by model (~$0.001-0.01 per image)
- Image-to-Image: ~$0.01-0.05 per modification
- Video generation: ~$0.05-0.10 per video