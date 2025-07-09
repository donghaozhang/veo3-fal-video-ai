# AI Content Generation Suite

A comprehensive AI content generation package with multiple providers and services, consolidated into a single installable package.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **⚡ Production-ready Python package with comprehensive CLI, parallel execution, and enterprise-grade architecture**

## 🚀 **FLAGSHIP: AI Content Pipeline**

The unified AI content generation pipeline with parallel execution support, multi-model integration, and YAML-based configuration.

### Core Capabilities
- **🔄 Unified Pipeline Architecture** - YAML/JSON-based configuration for complex multi-step workflows
- **⚡ Parallel Execution Engine** - 2-3x performance improvement with thread-based parallel processing
- **🎯 Type-Safe Configuration** - Pydantic models with comprehensive validation
- **💰 Cost Management** - Real-time cost estimation and tracking across all services
- **📊 Rich Logging** - Beautiful console output with progress tracking and performance metrics

### AI Service Integrations
- **🖼️ FAL AI** - Text-to-image, image-to-image, text-to-video, video generation, avatar creation
- **🗣️ ElevenLabs** - Professional text-to-speech with 20+ voice options
- **🎥 Google Vertex AI** - Veo video generation and Gemini text generation  
- **🔗 OpenRouter** - Alternative TTS and chat completion services

### Developer Experience
- **🛠️ Professional CLI** - Comprehensive command-line interface with Click
- **📦 Modular Architecture** - Clean separation of concerns with extensible design
- **🧪 Comprehensive Testing** - Unit and integration tests with pytest
- **📚 Type Hints** - Full type coverage for excellent IDE support

## 📦 Installation

### Prerequisites
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows
```

### Install Package
```bash
# Install in development mode (recommended)
pip install -e .

# Or install from source
pip install .
```

## 🛠️ Quick Start

### Console Commands
```bash
# List all available AI models
ai-content-pipeline list-models

# Generate image from text
ai-content-pipeline generate-image --text "epic space battle" --model flux_dev

# Create video (text → image → video)
ai-content-pipeline create-video --text "serene mountain lake"

# Run custom pipeline from YAML config
ai-content-pipeline run-chain --config config.yaml --input "cyberpunk city"

# Create example configurations
ai-content-pipeline create-examples

# Shortened command alias
aicp --help
```

### Python API
```python
from packages.core.ai_content_pipeline.pipeline.manager import AIPipelineManager

# Initialize manager
manager = AIPipelineManager()

# Quick video creation
result = manager.quick_create_video(
    text="serene mountain lake",
    image_model="flux_dev",
    video_model="auto"
)

# Run custom chain
chain = manager.create_chain_from_config("config.yaml")
result = manager.execute_chain(chain, "input text")
```

## 📚 Package Structure

### Core Packages
- **[ai_content_pipeline](packages/core/ai_content_pipeline/)** - Main unified pipeline with parallel execution

### Provider Packages

#### Google Services
- **[google-veo](packages/providers/google/veo/)** - Google Veo video generation (Vertex AI)

#### FAL AI Services  
- **[fal-video](packages/providers/fal/video/)** - Video generation (MiniMax Hailuo-02, Kling Video 2.1)
- **[fal-text-to-video](packages/providers/fal/text-to-video/)** - Text-to-video (MiniMax Hailuo-02 Pro, Google Veo 3)
- **[fal-avatar](packages/providers/fal/avatar/)** - Avatar generation with TTS integration
- **[fal-text-to-image](packages/providers/fal/text-to-image/)** - Text-to-image (Imagen 4, Seedream v3, FLUX.1)
- **[fal-image-to-image](packages/providers/fal/image-to-image/)** - Image transformation (Luma Photon Flash)
- **[fal-video-to-video](packages/providers/fal/video-to-video/)** - Video processing (ThinksSound + Topaz)

### Service Packages
- **[text-to-speech](packages/services/text-to-speech/)** - ElevenLabs TTS integration (20+ voices)
- **[video-tools](packages/services/video-tools/)** - Video processing utilities with AI analysis

## 🔧 Configuration

### Environment Setup
Create a `.env` file in the project root:
```env
# FAL AI API Configuration
FAL_KEY=your_fal_api_key

# Google Cloud Configuration (for Veo)
PROJECT_ID=your-project-id
OUTPUT_BUCKET_PATH=gs://your-bucket/veo_output/

# ElevenLabs Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# Optional: Gemini for AI analysis
GEMINI_API_KEY=your_gemini_api_key

# Optional: OpenRouter for additional models
OPENROUTER_API_KEY=your_openrouter_api_key
```

### YAML Pipeline Configuration
```yaml
name: "Text to Video Pipeline"
description: "Generate video from text prompt"
steps:
  - name: "generate_image"
    type: "text_to_image"
    model: "flux_dev"
    aspect_ratio: "16:9"
    
  - name: "create_video"
    type: "image_to_video"
    model: "kling_video"
    input_from: "generate_image"
    duration: 8
```

### Parallel Execution
Enable parallel processing for 2-3x speedup:
```bash
# Enable parallel execution
PIPELINE_PARALLEL_ENABLED=true ai-content-pipeline run-chain --config config.yaml
```

Example parallel pipeline configuration:
```yaml
name: "Parallel Processing Example"
steps:
  - type: "parallel_group"
    steps:
      - type: "text_to_image"
        model: "flux_schnell"
        params:
          prompt: "A cat"
      - type: "text_to_image"
        model: "flux_schnell"
        params:
          prompt: "A dog"
      - type: "text_to_image"
        model: "flux_schnell"
        params:
          prompt: "A bird"
```

## 💰 Cost Management

### Cost Estimation
Always estimate costs before running pipelines:
```bash
# Estimate cost for a pipeline
ai-content-pipeline estimate-cost --config config.yaml
```

### Typical Costs
- **Text-to-Image**: $0.001-0.004 per image
- **Image-to-Image**: $0.01-0.05 per modification  
- **Text-to-Video**: $0.08-6.00 per video (model dependent)
- **Avatar Generation**: $0.02-0.05 per video
- **Text-to-Speech**: Varies by usage (ElevenLabs pricing)
- **Video Processing**: $0.05-2.50 per video (model dependent)

### Cost-Conscious Usage
- Use cheaper models for prototyping (`flux_schnell`, `hailuo`)
- Test with small batches before large-scale generation
- Monitor costs with built-in tracking

## 🧪 Testing

### Consolidated Test Suite
The package includes a comprehensive test suite:

```bash
# Quick smoke tests (30 seconds)
python tests/test_core.py

# Full integration tests (2-3 minutes)
python tests/test_integration.py

# Interactive demonstration
python tests/demo.py --interactive

# Run all tests
python tests/run_all_tests.py

# Quick test mode
python tests/run_all_tests.py --quick
```

### Run Individual Package Tests
```bash
# Activate virtual environment
source venv/bin/activate

# AI Content Pipeline
cd packages/core/ai_content_pipeline
python -m pytest tests/

# Google Veo
cd packages/providers/google/veo
python test_veo.py

# FAL AI services
cd packages/providers/fal/video
python test_fal_ai.py

# Text-to-Speech
cd packages/services/text-to-speech
python examples/basic_usage.py
```

### Setup Tests (No API costs)
```bash
# Most packages have free setup tests
python test_setup.py  # Validates configuration without API calls
```

## 💰 Cost Management

### Estimation
- **FAL AI Video**: ~$0.05-0.10 per video
- **FAL AI Text-to-Video**: ~$0.08 (MiniMax) to $2.50-6.00 (Google Veo 3)
- **FAL AI Avatar**: ~$0.02-0.05 per video
- **FAL AI Images**: ~$0.001-0.01 per image
- **Text-to-Speech**: Varies by usage (ElevenLabs pricing)

### Best Practices
1. Always run `test_setup.py` first (FREE)
2. Use cost estimation in pipeline manager
3. Start with cheaper models for testing
4. Monitor usage through provider dashboards

## 🔄 Development Workflow

### Making Changes
```bash
# Make your changes to the codebase
git add .
git commit -m "Your changes"
git push origin main
```

### Testing Installation
```bash
# Create test environment
python3 -m venv test_env
source test_env/bin/activate

# Install and test
pip install -e .
ai-content-pipeline --help
```

## 📋 Available Commands

### AI Content Pipeline Commands
- `ai-content-pipeline list-models` - List all available models
- `ai-content-pipeline generate-image` - Generate image from text
- `ai-content-pipeline create-video` - Create video from text
- `ai-content-pipeline run-chain` - Run custom YAML pipeline
- `ai-content-pipeline create-examples` - Create example configs
- `aicp` - Shortened alias for all commands

### Individual Package Commands
See [CLAUDE.md](CLAUDE.md) for detailed commands for each package.

## 📚 Documentation

- **[Project Instructions](CLAUDE.md)** - Comprehensive development guide
- **[Documentation](docs/)** - Additional documentation and guides
- **Package READMEs** - Each package has its own README with specific instructions

## 🏗️ Architecture

- **Unified Package Structure** - Single `setup.py` with consolidated dependencies
- **Consolidated Configuration** - Single `.env` file for all services
- **Modular Design** - Each service can be used independently or through the unified pipeline
- **Parallel Execution** - Optional parallel processing for improved performance
- **Cost-Conscious Design** - Built-in cost estimation and management

## 📚 Resources

### 🚀 AI Content Pipeline Resources
- [Pipeline Documentation](packages/core/ai_content_pipeline/docs/README.md)
- [Getting Started Guide](packages/core/ai_content_pipeline/docs/GETTING_STARTED.md)
- [YAML Configuration Reference](packages/core/ai_content_pipeline/docs/YAML_CONFIGURATION.md)
- [Parallel Execution Design](packages/core/ai_content_pipeline/docs/parallel_pipeline_design.md)

### Google Veo Resources
- [Veo API Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation)
- [Google GenAI SDK](https://github.com/google/generative-ai-python)
- [Vertex AI Console](https://console.cloud.google.com/vertex-ai)

### FAL AI Resources
- [FAL AI Platform](https://fal.ai/)
- [MiniMax Hailuo Documentation](https://fal.ai/models/fal-ai/minimax-video-01)
- [Kling Video 2.1 Documentation](https://fal.ai/models/fal-ai/kling-video/v2.1/standard/image-to-video/api)
- [FAL AI Avatar Documentation](https://fal.ai/models/fal-ai/avatar-video)
- [ThinksSound API Documentation](https://fal.ai/models/fal-ai/thinksound/api)
- [Topaz Video Upscale Documentation](https://fal.ai/models/fal-ai/topaz/upscale/video/api)

### Text-to-Speech Resources
- [ElevenLabs API Documentation](https://elevenlabs.io/docs/capabilities/text-to-speech)
- [OpenRouter Platform](https://openrouter.ai/)
- [ElevenLabs Voice Library](https://elevenlabs.io/app/speech-synthesis/text-to-speech)
- [Text-to-Dialogue Documentation](https://elevenlabs.io/docs/cookbooks/text-to-dialogue)
- [Package Migration Guide](packages/services/text-to-speech/docs/MIGRATION_GUIDE.md)

### Additional Documentation
- [Project Instructions](CLAUDE.md) - Comprehensive development guide
- [Documentation](docs/) - Additional documentation and guides
- [Package Organization](docs/repository_organization_guide.md) - Package structure guide

## 🤝 Contributing

1. Follow the development patterns in [CLAUDE.md](CLAUDE.md)
2. Add tests for new features
3. Update documentation as needed
4. Test installation in fresh virtual environment
5. Commit with descriptive messages
