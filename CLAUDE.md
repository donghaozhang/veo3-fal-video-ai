# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dual-platform AI video generation project supporting:
- **Google Veo** (Vertex AI): High-resolution, enterprise-grade video generation
- **FAL AI**: Simple API-based generation with dual models (MiniMax Hailuo-02 and Kling Video 2.1)

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

### FAL AI Commands (fal_video_generation/)
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

## Architecture

### Directory Structure
- `veo3_video_generation/` - Google Veo implementation (function-based)
- `fal_video_generation/` - FAL AI implementation (class-based)
- `archive/` - Legacy implementations and video analysis tools

### Google Veo Architecture
- **Function-based approach** in `veo_video_generation.py`
- Key functions: `generate_video_from_text()`, `generate_video_from_image()`, `generate_video_from_local_image()`
- Authentication pattern: Sets environment variables, initializes GenAI client
- Output: GCS URIs, automatic download to `result_folder/`

### FAL AI Architecture
- **Class-based approach** with `FALVideoGenerator` class
- Dual model support: MiniMax Hailuo-02 and Kling Video 2.1
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
1. Configure `.env` in fal_video_generation/:
   ```
   FAL_KEY=your_fal_api_key
   ```

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

### Test Command Patterns
Both test suites support:
- Basic tests (default)
- Model-specific tests (--veo3, --kling)
- Comparison tests (--compare)
- Quick tests (--quick, --full)

## Model Selection Guidelines

### Use Google Veo when:
- Need highest resolution (1080p+)
- Enterprise/production deployment
- Already using Google Cloud infrastructure
- Quality over speed

### Use FAL AI when:
- Quick prototyping and testing
- Simple API key authentication
- Need model comparison capabilities
- Production-ready API requirements

## Important Implementation Details

### Google Veo Specifics
- Veo 3.0 requires allowlist approval
- Uses `us-central1` region for Vertex AI
- Automatic permission fixing via `fix_permissions.py`
- Support for both text-to-video and image-to-video

### FAL AI Specifics
- MiniMax Hailuo-02: 768p, 6-10s, prompt optimizer
- Kling Video 2.1: High-quality, 5-10s, CFG scale, negative prompts
- Unified class handles both models seamlessly
- Built-in async processing with progress updates

## Environment Variables
- Never commit `.env` files
- Each implementation has separate `.env` files
- Use environment-specific configurations
- Google Veo requires multiple Google Cloud environment variables
- FAL AI only requires `FAL_KEY`