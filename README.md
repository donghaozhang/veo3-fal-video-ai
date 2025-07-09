# AI Content Generation Suite

A comprehensive AI content generation package with multiple providers and services, consolidated into a single installable package.

## 🚀 **FLAGSHIP: AI Content Pipeline**

The unified AI content generation pipeline with parallel execution support, multi-model integration, and YAML-based configuration.

### Key Features
- **🔧 Unified API** - Single interface for all AI services
- **⚡ Parallel Execution** - 2-3x speedup with thread-based processing
- **🎯 Multi-Model Support** - Integration with FAL AI, Google Veo, ElevenLabs, and more
- **📝 YAML Configuration** - Easy-to-use configuration files
- **💰 Cost Management** - Built-in cost estimation and tracking
- **🔌 Console Scripts** - `ai-content-pipeline` and `aicp` commands

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
- **[ai_content_platform](packages/core/ai_content_platform/)** - Platform framework

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

## 🧪 Testing

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

## 🤝 Contributing

1. Follow the development patterns in [CLAUDE.md](CLAUDE.md)
2. Add tests for new features
3. Update documentation as needed
4. Test installation in fresh virtual environment
5. Commit with descriptive messages
