# FAL Image-to-Image Generator v2.0

A comprehensive, modular Python package for AI-powered image editing using multiple FAL AI models.

## 🆕 What's New in v2.0

- **🏗️ Modular Architecture**: Complete refactor into organized package structure
- **🎯 Multi-Model Support**: Unified interface for 5 different AI models
- **🎨 ByteDance SeedEdit v3**: New model with excellent content preservation
- **🔧 Enhanced API**: Cleaner, more intuitive method signatures
- **📦 Proper Package**: Professional Python package with setup.py
- **🧪 Better Testing**: Organized test suite and examples

## 🎨 Supported Models

| Model | Best For | Strengths |
|-------|----------|-----------|
| **ByteDance SeedEdit v3** | Content preservation | Accurate instruction following, maintains structure |
| **Luma Photon Flash** | Creative modifications | Fast, personalizable, aspect ratio control |
| **Luma Photon Base** | High-quality creative work | Professional grade, commercial ready |
| **FLUX Kontext Dev** | Contextual understanding | Nuanced modifications, style preservation |
| **FLUX Kontext Multi** | Multi-image processing | Experimental capabilities, batch processing |

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from fal_image_to_image import FALImageToImageGenerator

# Initialize with your API key
generator = FALImageToImageGenerator()

# SeedEdit v3 - Best for content preservation
result = generator.modify_image_seededit(
    prompt="Enhance quality and add professional lighting",
    image_url="https://example.com/image.jpg",
    guidance_scale=0.5,
    seed=42
)

# Photon Flash - Best for creative modifications  
result = generator.modify_image_photon(
    prompt="Transform into cyberpunk style",
    image_url="https://example.com/image.jpg",
    strength=0.7,
    aspect_ratio="16:9"
)

if result['success']:
    print(f"Generated: {result['downloaded_files']}")
```

### Local Images

```python
# Process local image files
result = generator.modify_local_image_seededit(
    prompt="Make it more photorealistic",
    image_path="my_image.jpg",
    guidance_scale=0.6
)
```

## 📁 Package Structure

```
fal_image_to_image/
├── fal_image_to_image/          # Main package
│   ├── __init__.py              # Package exports
│   ├── generator.py             # Main generator class
│   ├── models/                  # Model implementations
│   │   ├── base.py             # Base model interface
│   │   ├── seededit.py         # SeedEdit v3
│   │   ├── photon.py           # Photon models
│   │   └── kontext.py          # Kontext models
│   ├── utils/                   # Utilities
│   │   ├── file_utils.py       # File operations
│   │   └── validators.py       # Parameter validation
│   └── config/                  # Configuration
│       └── constants.py        # Model constants
├── examples/                    # Usage examples
│   ├── basic_usage.py          # Getting started
│   └── model_comparison.py     # Model comparison
├── tests/                       # Test suite
├── docs/                        # Documentation
├── assets/                      # Test images
└── output/                      # Generated images
```

## 🎯 Model Selection Guide

### When to Use SeedEdit v3
- ✅ **Content preservation is priority**
- ✅ **Need accurate instruction following**
- ✅ **Want simple parameter tuning**
- ✅ **Require commercial-grade reliability**

```python
result = generator.modify_image_seededit(
    prompt="Enhance lighting and quality",
    image_url=image_url,
    guidance_scale=0.5  # 0.0-1.0, lower = more preservation
)
```

### When to Use Photon Flash
- ✅ **Creative transformations**
- ✅ **Need aspect ratio control**
- ✅ **Fast processing required**
- ✅ **Personalizable outputs**

```python
result = generator.modify_image_photon(
    prompt="Transform to cyberpunk style",
    image_url=image_url,
    strength=0.7,       # 0.0-1.0, higher = more dramatic
    aspect_ratio="16:9"
)
```

### When to Use Kontext Dev
- ✅ **Contextual understanding needed**
- ✅ **Nuanced modifications**
- ✅ **Style preservation important**
- ✅ **Iterative editing workflow**

```python
result = generator.modify_image(
    prompt="Add realistic shadows and lighting",
    image_url=image_url,
    model="kontext",
    num_inference_steps=28,
    guidance_scale=2.5
)
```

## 📊 Parameter Guide

### SeedEdit v3 Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| `guidance_scale` | 0.0-1.0 | 0.5 | Higher = more prompt adherence |
| `seed` | int | None | For reproducible results |

**Guidance Scale Guide:**
- `0.1-0.3`: Subtle quality improvements
- `0.4-0.6`: Balanced editing ⭐ **Recommended**
- `0.7-0.9`: Dramatic transformations

### Photon Parameters

| Parameter | Options | Default | Effect |
|-----------|---------|---------|--------|
| `strength` | 0.0-1.0 | 0.8 | Modification intensity |
| `aspect_ratio` | 1:1, 16:9, 9:16, 4:3, etc. | "1:1" | Output dimensions |

## 🔧 Advanced Features

### Batch Processing

```python
# Process multiple images
results = generator.batch_modify_images(
    prompts=["Make realistic", "Add winter theme", "Enhance colors"],
    image_urls=[url1, url2, url3],
    model="seededit"
)
```

### Model Information

```python
# Get model capabilities
info = generator.get_model_info("seededit")
print(f"Features: {info['features']}")

# List all supported models
models = generator.get_supported_models()
print(f"Available: {models}")
```

### Custom Output Directory

```python
result = generator.modify_image_seededit(
    prompt="Enhance image",
    image_url=image_url,
    output_dir="custom_output/"
)
```

## 🛠️ Setup

### 1. Get API Key
Get your FAL AI API key from [fal.ai](https://fal.ai/)

### 2. Set Environment Variable
```bash
export FAL_KEY="your_fal_api_key_here"
```

### 3. Install Dependencies
```bash
cd fal_image_to_image
pip install -r requirements.txt
```

### 4. Run Examples
```bash
python examples/basic_usage.py
python examples/model_comparison.py
```

## 📖 Documentation

- **[API Reference](docs/API_REFERENCE.md)**: Complete API documentation
- **[SeedEdit Guide](docs/README_SEEDEDIT.md)**: ByteDance SeedEdit v3 details
- **[Migration Guide](MIGRATION.md)**: Upgrading from v1.x

## 🎨 Prompt Examples

### Artistic Styles
- "Convert to watercolor painting style"
- "Transform into oil painting"
- "Make it look like a pencil sketch"
- "Apply digital art aesthetic"

### Photo Effects  
- "Make this look vintage"
- "Add film grain and warm tones"
- "Convert to black and white with high contrast"
- "Apply HDR effect"

### Creative Transformations
- "Transform into cyberpunk style"
- "Make it look like a comic book illustration"
- "Apply steampunk aesthetic"
- "Convert to anime/manga style"

## 📊 Parameter Guidelines

### SeedEdit v3 - Guidance Scale
- **0.1-0.3**: Subtle quality improvements
- **0.4-0.6**: Balanced editing ⭐ **Recommended**
- **0.7-0.9**: Dramatic transformations

### Photon - Strength
- **0.0-0.3**: Subtle modifications, preserve original structure
- **0.4-0.6**: Moderate changes, balanced transformation
- **0.7-1.0**: Strong transformations, creative reimagining

### Kontext - Inference Steps
- **1-15**: Fast generation but lower quality
- **16-35**: Balanced speed and quality (recommended)
- **36-50**: High quality but slower processing

### Kontext - Guidance Scale
- **1.0-2.0**: More creative freedom, less prompt adherence
- **2.1-5.0**: Balanced prompt following (recommended)
- **5.1-20.0**: Strict prompt adherence, less creativity

## 💰 Cost Information

- **Estimated Cost**: ~$0.01-0.05 per image modification
- **Setup Tests**: Completely FREE
- **Cost Controls**: Built-in warnings and confirmations
- **SeedEdit v3**: Most cost-effective for quality results

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Test setup (no API calls) - FREE
python tests/test_setup.py

# Test with real API (requires FAL_KEY) - PAID
python tests/test_generation.py              # Basic tests
python tests/test_generation.py --quick      # Quick single test
python tests/test_generation.py --batch      # Batch processing test
python tests/test_generation.py --compare    # Compare models
```

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Not Set**:
   ```bash
   echo "FAL_KEY=your_api_key" > .env
   ```

2. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Permission Errors**:
   ```bash
   chmod +x *.py
   ```

### Error Messages

- **"FAL_KEY not found"**: Set your API key in `.env` file
- **"Unsupported aspect ratio"**: Use one of the supported ratios
- **"Strength must be between 0.0 and 1.0"**: Check strength parameter
- **"Inference steps must be between 1 and 50"**: Check inference steps
- **"File not found"**: Verify local image file path

## 📈 Performance

- **SeedEdit v3**: ~15-17 seconds per image ⭐ **Most efficient**
- **Photon Flash**: ~10-15 seconds per image
- **Kontext Dev**: ~20-30 seconds per image

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Links

- **Documentation**: [API Reference](docs/API_REFERENCE.md)
- **Examples**: [examples/](examples/)
- **Issues**: [GitHub Issues](https://github.com/your-username/fal-image-to-image/issues)
- **FAL AI**: [fal.ai](https://fal.ai/)

---

**v2.0** - Modular, production-ready package with multi-model support and ByteDance SeedEdit v3! 🎉