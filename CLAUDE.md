# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Git Workflow Commands

**Always run after each successful implementation:**
```bash
git add .
git commit -m "descriptive commit message"
git push origin main
```

## Project Overview

This is a comprehensive AI content generation project supporting multiple platforms and content types:

### 🚀 **FLAGSHIP: AI Content Pipeline** (`ai_content_pipeline/`)
- **Unified Pipeline**: YAML-based multi-step content generation
- **Parallel Execution**: 2-3x speedup with thread-based parallel processing
- **All Models**: Integration with all FAL AI models, ElevenLabs TTS, Google services
- **Commands**: `python -m ai_content_pipeline run-chain --config config.yaml`

### Individual Service Implementations:
- **Google Veo** (Vertex AI): High-resolution, enterprise-grade video generation
- **FAL AI Video**: Simple API-based generation with dual models (MiniMax Hailuo-02 and Kling Video 2.1)
- **FAL AI Text-to-Video**: Unified text-to-video generation with dual model support (MiniMax Hailuo-02 Pro and Google Veo 3)
- **FAL AI Video-to-Video**: Audio generation and video upscaling (ThinksSound + Topaz)
- **FAL AI Avatar**: Talking avatar generation with text-to-speech and audio-to-avatar capabilities
- **FAL AI Text-to-Image**: Multi-model image generation (Imagen 4, Seedream v3, FLUX.1)
- **FAL AI Image-to-Image**: AI-powered image modification using Luma Photon Flash
- **Text-to-Speech**: Professional voice synthesis with ElevenLabs + OpenRouter AI integration
- **Video Tools**: Comprehensive video processing with enhanced CLI parameter support

## Environment Setup

### Python Virtual Environment (Required)
```bash
# Create and activate virtual environment (run from project root)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install all dependencies from root
pip install -r requirements.txt
```

**Memory**: Virtual environment created at `/home/zdhpe/veo3-video-generation/venv/` with all dependencies installed. Always activate before running scripts.

## Common Commands

### 🚀 AI Content Pipeline Commands (ai_content_pipeline/)
```bash
# Activate venv first: source venv/bin/activate
cd ai_content_pipeline

# Run sequential pipeline
python -m ai_content_pipeline run-chain --config input/tts_simple_test.yaml

# Run with parallel execution (2-3x speedup)
PIPELINE_PARALLEL_ENABLED=true python -m ai_content_pipeline run-chain --config input/tts_parallel_test.yaml

# Debug mode
python -m ai_content_pipeline run-chain --config config.yaml --debug
```

### Google Veo Commands (veo3_video_generation/)
```bash
# Activate venv first: source venv/bin/activate
cd veo3_video_generation

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
# Activate venv first: source venv/bin/activate
cd fal_video_generation

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
# Activate venv first: source venv/bin/activate
cd fal_avatar_generation

# Setup and environment tests (FREE)
python test_setup.py                 # Validate setup without costs
python test_generation.py            # Test avatar generation with costs
python test_official_example.py      # Test with official FAL examples

# Interactive demo
python demo.py
```

### FAL AI Text-to-Image Commands (fal_text_to_image/)
```bash
# Activate venv first: source venv/bin/activate
cd fal_text_to_image

# Setup and environment tests (FREE)
python test_setup.py                 # Validate setup without costs
python test_generation.py            # Test image generation with costs

# Interactive demo
python demo.py
```

### FAL AI Image-to-Image Commands (fal_image_to_image/)
```bash
# Activate venv first: source venv/bin/activate
cd fal_image_to_image

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
# Activate venv first: source venv/bin/activate
cd fal_text_to_video

# Setup and environment tests (FREE)
python test_setup.py                 # Validate setup without costs
python test_generation.py            # Test video generation with costs

# Interactive demo
python demo.py
```

### Text-to-Speech Commands (text_to_speech/)
```bash
# Activate venv first: source venv/bin/activate
cd text_to_speech

# Basic usage examples
python examples/basic_usage.py       # Simple text-to-speech conversion
python cli/quick_start.py           # Quick start CLI interface
python cli/interactive.py           # Interactive voice selection
```

### Video Tools Commands (video_tools/)
```bash
# Activate venv first: source venv/bin/activate
cd video_tools

# Run test suite
python run_tests.py                  # Comprehensive test runner
python tests/run_quick_tests.py      # Quick functionality tests

# Enhanced CLI tool
python enhanced_cli.py              # Interactive video processing
```

## Architecture

### Directory Structure
- `ai_content_pipeline/` - **FLAGSHIP**: Unified AI Content Pipeline with parallel execution
- `veo3_video_generation/` - Google Veo implementation (function-based)
- `fal_video_generation/` - FAL AI video generation (class-based)
- `fal_text_to_video/` - FAL AI text-to-video generation with dual model support (class-based)
- `fal_video_to_video/` - FAL AI video-to-video processing (ThinksSound + Topaz)
- `fal_avatar_generation/` - FAL AI avatar generation (class-based)
- `fal_text_to_image/` - FAL AI text-to-image generation (class-based)
- `fal_image_to_image/` - FAL AI image-to-image modification (class-based)
- `text_to_speech/` - Enhanced ElevenLabs + OpenRouter AI integration (modular package)
- `video_tools/` - Enhanced video processing with CLI parameter support (class-based)

### AI Content Pipeline Architecture (FLAGSHIP)
- **YAML-based configuration** for multi-step workflows
- **Parallel execution support** with thread-based processing (2-3x speedup)
- **StepType enum**: `text_to_speech`, `text_to_image`, `image_to_image`, `parallel_group`
- **Feature flag**: `PIPELINE_PARALLEL_ENABLED=true` for parallel execution
- **Output**: Organized results in pipeline output directories

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

## Project Development Guidelines

### 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn't listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Use venv_linux** (the virtual environment) whenever executing Python commands, including for unit tests.

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
  For agents this looks like:
    - `agent.py` - Main agent definition and execution logic 
    - `tools.py` - Tool functions used by the agent 
    - `prompts.py` - System prompts
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_env()** for environment variables.

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a "Discovered During Work" section.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.