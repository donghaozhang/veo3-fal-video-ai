# AI Content Pipeline

A unified content creation system that chains multiple AI operations together for seamless content generation.

## 🎯 Vision

Create a powerful pipeline where users can chain multiple AI operations:
**Text → Image → Video → Audio Enhancement → Video Upscaling**

## ✨ Features

### Current Implementation
- **🎨 Multi-Model Text-to-Image**: FLUX.1 Dev/Schnell, Imagen 4, Seedream v3
- **🔗 Chain Configuration**: YAML/JSON-based workflow definitions
- **💰 Cost Estimation**: Transparent pricing for all operations
- **🛠️ Smart Model Selection**: Auto-selection based on criteria and budget
- **📁 File Management**: Automatic handling of intermediate results
- **🖥️ CLI Interface**: Command-line tools for all operations

### Planned Integrations
- **📹 Image-to-Video**: Google Veo, FAL AI models
- **🎵 Audio Generation**: ThinksSound integration
- **📈 Video Upscaling**: Topaz Video Upscale integration
- **🌐 Additional Models**: OpenAI DALL-E, Stability AI

## 🚀 Quick Start

### Installation & Setup

```bash
# Navigate to the pipeline directory
cd ai_content_pipeline

# Install dependencies (from main project root)
cd .. && source venv/bin/activate && pip install -r requirements.txt

# Set up environment (copy from existing FAL modules)
cp ../fal_text_to_image/.env .env
```

### Basic Usage

```bash
# List available models
python -m ai_content_pipeline list-models

# Generate image from text
python -m ai_content_pipeline generate-image --text "epic space battle" --model flux_dev

# Quick video creation (text → image → video)
python -m ai_content_pipeline create-video --text "serene mountain lake"

# Create example configurations
python -m ai_content_pipeline create-examples
```

### Python API Usage

```python
from ai_content_pipeline import AIPipelineManager

# Initialize pipeline
manager = AIPipelineManager()

# Generate image
result = manager.text_to_image.generate(
    prompt="A futuristic cityscape at sunset",
    model="flux_dev",
    aspect_ratio="16:9"
)

print(f"Generated: {result.output_path}")
print(f"Cost: ${result.cost_estimate:.3f}")
```

## 📋 Chain Configuration

### Simple Chain Example

```yaml
name: "simple_image_generation"
steps:
  - type: "text_to_image"
    model: "flux_dev"
    params:
      aspect_ratio: "16:9"
      style: "cinematic"
output_dir: "output"
cleanup_temp: true
```

### Full Content Creation Chain

```yaml
name: "full_content_creation"
steps:
  - type: "text_to_image"
    model: "flux_dev"
    params:
      aspect_ratio: "16:9"
      style: "cinematic"
  - type: "image_to_video"
    model: "veo3"
    params:
      duration: 8
      motion_level: "medium"
  - type: "add_audio"
    model: "thinksound"
    params:
      prompt: "epic cinematic soundtrack"
  - type: "upscale_video"
    model: "topaz"
    params:
      factor: 2
```

## 🏗️ Architecture

### Project Structure

```
ai_content_pipeline/
├── ai_content_pipeline/           # Main package
│   ├── __init__.py               # Package initialization
│   ├── __main__.py               # CLI entry point
│   ├── config/                   # Configuration management
│   │   ├── constants.py          # Model constants and settings
│   │   └── __init__.py
│   ├── models/                   # Model implementations
│   │   ├── base.py               # Base model interface
│   │   ├── text_to_image.py      # Unified text-to-image generator
│   │   └── __init__.py
│   ├── pipeline/                 # Pipeline management
│   │   ├── manager.py            # Main pipeline manager
│   │   ├── chain.py              # Chain configuration classes
│   │   ├── executor.py           # Chain execution engine
│   │   └── __init__.py
│   └── utils/                    # Utility functions
│       ├── file_manager.py       # File management
│       ├── validators.py         # Input validation
│       └── __init__.py
├── examples/                     # Usage examples and demos
│   ├── basic_usage.py            # Basic usage examples
│   └── __init__.py
├── input/                        # Input files for testing
├── output/                       # Generated content output
├── temp/                         # Temporary files
├── tests/                        # Test suite
├── requirements.txt              # Pipeline dependencies
└── README.md                     # This file
```

### Key Components

#### 1. Pipeline Manager (`AIPipelineManager`)
- Orchestrates chain creation and execution
- Handles cost estimation and model recommendations
- Manages file operations and cleanup

#### 2. Chain System (`ContentCreationChain`)
- Defines sequences of content creation steps
- Supports YAML/JSON configuration
- Validates step compatibility and parameters

#### 3. Model Generators
- **UnifiedTextToImageGenerator**: Multi-model text-to-image interface
- **BaseContentModel**: Abstract base for all content models
- Planned: Image-to-video, audio generation, video upscaling

#### 4. File Management (`FileManager`)
- Handles temporary files and cleanup
- Organizes output files by chain and step
- Tracks storage usage and file metadata

## 🎨 Text-to-Image Models

### Currently Available

| Model | Provider | Best For | Cost | Speed |
|-------|----------|----------|------|-------|
| **FLUX.1 Dev** | FAL AI | High quality, artistic | $0.003 | 15s |
| **FLUX.1 Schnell** | FAL AI | Speed, prototyping | $0.001 | 5s |
| **Imagen 4** | Google (FAL AI) | Photorealism | $0.004 | 20s |
| **Seedream v3** | FAL AI | Multilingual, cost-effective | $0.002 | 10s |

### Model Selection

```python
# Automatic selection based on criteria
result = manager.text_to_image.generate(
    prompt="your prompt",
    model="auto",
    criteria="quality",    # "quality", "speed", "cost", "balanced"
    budget=0.01           # Optional budget constraint
)

# Compare models for a prompt
comparison = manager.text_to_image.compare_models(
    prompt="futuristic city",
    models=["flux_dev", "imagen4", "seedream_v3"]
)
```

## 💰 Cost Management

### Cost Estimation

```python
# Estimate cost for a chain
chain = manager.create_simple_chain(["text_to_image", "image_to_video"])
cost_info = manager.estimate_chain_cost(chain)

print(f"Total cost: ${cost_info['total_cost']:.3f}")
for step in cost_info['step_costs']:
    print(f"{step['step']}: ${step['cost']:.3f}")
```

### Budget-Aware Model Selection

```python
# Generate within budget
result = manager.text_to_image.generate(
    prompt="expensive prompt",
    model="auto",
    budget=0.002  # Will choose cheapest suitable model
)
```

## 🖥️ CLI Interface

### Available Commands

```bash
# List all available models with details
python -m ai_content_pipeline list-models

# Generate single image
python -m ai_content_pipeline generate-image \
    --text "epic space battle" \
    --model flux_dev \
    --aspect-ratio 16:9 \
    --output-dir results/

# Quick video creation (when video models are integrated)
python -m ai_content_pipeline create-video \
    --text "serene mountain lake" \
    --image-model flux_dev \
    --video-model veo3

# Run custom chain from configuration
python -m ai_content_pipeline run-chain \
    --config my_chain.yaml \
    --input-text "cyberpunk cityscape"

# Create example configuration files
python -m ai_content_pipeline create-examples \
    --output-dir examples/
```

### CLI Options

- `--debug`: Enable debug output with stack traces
- `--base-dir`: Set base directory for operations
- `--save-json`: Save results in JSON format
- `--no-confirm`: Skip confirmation prompts

## 🧪 Examples & Testing

### Run Examples

```bash
# Run basic usage examples
python examples/basic_usage.py

# Create example configurations
python -m ai_content_pipeline create-examples
```

### Example Outputs

The examples demonstrate:
- ✅ Text-to-image generation with multiple models
- 📊 Model comparison and cost analysis
- 💾 Storage usage monitoring
- ⚠️ Error handling for unimplemented features

## 🔧 Development Status

### ✅ Completed Features
- **Core Architecture**: Pipeline manager, chain system, base models
- **Text-to-Image Integration**: Full FAL AI model support with auto-selection
- **Configuration System**: YAML/JSON chain definitions with validation
- **Cost Management**: Transparent pricing and budget constraints
- **File Management**: Automatic cleanup and organization
- **CLI Interface**: Complete command-line tools
- **Documentation**: Comprehensive examples and API docs

### 🚧 In Progress
- **Image-to-Video Integration**: Google Veo and FAL AI models
- **Audio Generation**: ThinksSound API integration
- **Video Upscaling**: Topaz Video Upscale integration
- **Additional Models**: OpenAI DALL-E, Stability AI

### 📋 Planned Features
- **Parallel Processing**: Batch operations and concurrent generation
- **Chain Templates**: Pre-built workflows for common use cases
- **Progress Tracking**: Real-time status updates for long chains
- **Result Caching**: Avoid regenerating identical content
- **Web Interface**: Browser-based pipeline management

## 🔗 Integration with Existing Modules

The pipeline seamlessly integrates with existing project modules:

```python
# Uses existing FAL text-to-image generator
from fal_text_to_image_generator import FALTextToImageGenerator

# Will integrate with video-to-video pipeline
from fal_video_to_video import FALVideoToVideoGenerator

# Planned integrations
from veo3_video_generation import VeoVideoGenerator
```

## 📝 Configuration Examples

### Cost-Conscious Chain

```yaml
name: "budget_content"
steps:
  - type: "text_to_image"
    model: "flux_schnell"  # Fastest, cheapest
    params:
      aspect_ratio: "16:9"
```

### High-Quality Chain

```yaml
name: "premium_content"
steps:
  - type: "text_to_image"
    model: "flux_dev"  # Highest quality
    params:
      aspect_ratio: "16:9"
      style: "photorealistic"
  - type: "image_to_video"
    model: "veo3"  # Premium video model
    params:
      duration: 10
      motion_level: "high"
```

## 🤝 Contributing

1. **Add New Models**: Extend `BaseContentModel` for new content types
2. **Improve Integrations**: Connect existing project modules
3. **Add Chain Templates**: Create common workflow configurations
4. **Enhance CLI**: Add new commands and options
5. **Write Tests**: Ensure reliability and error handling

## 🚨 Known Limitations

- **Video Models**: Not yet integrated (image-to-video, audio, upscaling)
- **Parallel Processing**: Sequential execution only
- **Result Caching**: Not implemented
- **Progress Tracking**: Basic console output only

## 📚 Resources

- **FAL AI Platform**: https://fal.ai/
- **Model Documentation**: See individual model providers
- **Project Integration**: Links to existing module READMEs
- **Configuration Schema**: YAML/JSON format specifications

---

**🎬 Start Creating!** Use the AI Content Pipeline to build amazing content creation workflows with multiple AI models working together seamlessly.