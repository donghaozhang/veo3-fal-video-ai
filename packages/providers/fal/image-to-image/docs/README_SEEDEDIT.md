# ByteDance SeedEdit v3 Integration

The FAL Image-to-Image generator now supports **ByteDance SeedEdit v3**, a state-of-the-art image editing model that excels at accurate instruction following and content preservation.

## 🆕 What's New

SeedEdit v3 has been added as the fourth model option alongside:
- **Luma Photon Flash** - Creative modifications with aspect ratio control
- **FLUX Kontext Dev** - Contextual editing with precise control  
- **ByteDance SeedEdit v3** - Accurate editing with content preservation ✨

## 🎯 SeedEdit v3 Features

- **Accurate editing instruction following** - Follows prompts precisely
- **Effective content preservation** - Maintains original image structure
- **Commercial use ready** - Production-grade quality and reliability
- **Simple parameter set** - Easy to use with minimal configuration
- **High-quality results** - Consistent, professional outputs
- **ByteDance developed** - Backed by leading AI research

## 📋 Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `prompt` | string | - | required | Text instruction for image editing |
| `image_url` | string | - | required | URL of input image |
| `guidance_scale` | float | 0.0-1.0 | 0.5 | Controls how closely output follows prompt |
| `seed` | int | - | None | Optional seed for reproducible results |
| `output_dir` | string | - | None | Custom output directory |

## 🚀 Usage Examples

### Basic Usage

```python
from fal_image_to_image_generator import FALImageToImageGenerator

# Initialize generator
generator = FALImageToImageGenerator()

# Edit image with SeedEdit v3
result = generator.modify_image_seededit(
    prompt="Add winter snow and make it more photorealistic",
    image_url="https://example.com/image.jpg",
    guidance_scale=0.7
)
```

### Local Image File

```python
# Edit local image
result = generator.modify_local_image_seededit(
    prompt="Transform into a winter wonderland scene",
    image_path="images/input.jpg",
    guidance_scale=0.5,
    seed=42  # For reproducible results
)
```

### Using General Method

```python
# Using the general modify_image method
result = generator.modify_image(
    prompt="Make it look more realistic and detailed",
    image_url="https://example.com/image.jpg",
    model="seededit",
    guidance_scale=0.6
)
```

## 🎛️ Guidance Scale Guide

The `guidance_scale` parameter (0.0-1.0) controls the balance between prompt following and content preservation:

- **0.1-0.3**: Subtle changes, maximum content preservation
- **0.4-0.6**: Balanced editing (recommended starting point)
- **0.7-0.9**: More dramatic changes, strong prompt following
- **1.0**: Maximum prompt following, minimal content preservation

## 🔄 Model Comparison

| Feature | Photon Flash | FLUX Kontext | SeedEdit v3 |
|---------|-------------|-------------|-------------|
| **Best for** | Creative modifications | Contextual understanding | Content preservation |
| **Complexity** | Medium | High | Low |
| **Speed** | Fast | Medium | Fast |
| **Parameters** | Strength + aspect ratio | Steps + guidance + resolution | Guidance scale only |
| **Guidance Range** | 0.0-1.0 (strength) | 1.0-20.0 | 0.0-1.0 |

## 💡 Best Practices

1. **Start with defaults**: Use `guidance_scale=0.5` for balanced results
2. **Be specific**: Use detailed, descriptive prompts for better accuracy
3. **Use seeds**: Set seed values for reproducible results in production
4. **Content preservation**: Choose SeedEdit v3 when maintaining original structure is crucial
5. **Test guidance scales**: Try different values to find the right balance for your use case

## 🔧 API Reference

### New Methods

#### `modify_image_seededit()`
Convenience method specifically for SeedEdit v3 modifications.

#### `modify_local_image_seededit()`
Convenience method for local image files with SeedEdit v3.

### Updated Methods

#### `modify_image()`
Now supports `model="seededit"` parameter.

#### `get_model_info()`
Returns SeedEdit v3 information when called with `"seededit"`.

#### `get_supported_models()`
Now includes `"seededit"` in the returned list.

## 📊 Example Results

With SeedEdit v3, you can expect:
- High-fidelity edits that preserve image structure
- Accurate interpretation of editing instructions  
- Consistent quality across different image types
- Reliable results suitable for commercial applications

## 🛠️ Setup

No additional setup required! SeedEdit v3 is automatically available in the existing generator class.

Just ensure you have:
1. Valid FAL API key set in `FAL_KEY` environment variable
2. Updated dependencies (`pip install -r requirements.txt`)

## 🎉 Get Started

Try SeedEdit v3 today with any of the usage examples above. The model excels at making precise, content-preserving edits while following your instructions accurately.