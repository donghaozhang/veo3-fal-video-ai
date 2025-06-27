# FAL AI Image-to-Image Generation

Transform your images with AI-powered modifications using FAL AI's dual-model system:

## Available Models

🔸 **Luma Photon Flash** - Creative, personalizable modifications  
🔸 **Luma Photon Base** - Most creative visual model for creatives  
🔸 **FLUX Kontext** - High-quality, detailed transformations  
🔸 **FLUX Kontext Multi** - Experimental multi-image generation

## Features

- **Quad-Model Support**: Choose between Photon Flash, Photon Base, FLUX Kontext, and FLUX Kontext Multi
- **Creative Image Modification**: Transform images with text prompts
- **Multi-Image Generation**: Generate new images from multiple input images (FLUX Kontext Multi)
- **Model-Specific Parameters**: Fine-tune each model's unique settings
- **Model Comparison**: Compare results from different models side-by-side
- **Multiple Aspect Ratios**: Support for various ratios and resolution modes
- **Batch Processing**: Modify multiple images efficiently with any model
- **Local & Remote Images**: Support for both local files and URLs
- **Cost Management**: Built-in cost warnings and confirmations

## Quick Start

1. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
   echo "FAL_KEY=your_fal_api_key" > .env
   ```

2. **Validate Setup** (FREE):
   ```bash
   python test_setup.py
   ```

3. **Interactive Demo**:
   ```bash
   python demo.py
   ```

## Usage Examples

### Photon Flash (Creative Modifications)
```python
from fal_image_to_image_generator import FALImageToImageGenerator

generator = FALImageToImageGenerator()

# Modify image with URL using Photon Flash
result = generator.modify_image_photon(
    prompt="Convert this to a watercolor painting",
    image_url="https://example.com/image.jpg",
    strength=0.7,
    aspect_ratio="1:1"
)

# Modify local image using Photon Flash
result = generator.modify_local_image_photon(
    prompt="Make this look vintage",
    image_path="path/to/image.jpg",
    strength=0.6,
    aspect_ratio="16:9"
)
```

### Photon Base (Most Creative Visual Model)
```python
# Modify image with URL using Photon Base
result = generator.modify_image_photon_base(
    prompt="Transform into an artistic masterpiece",
    image_url="https://example.com/image.jpg",
    strength=0.8,
    aspect_ratio="1:1"
)

# Modify local image using Photon Base
result = generator.modify_local_image_photon_base(
    prompt="Create a dreamy, ethereal version",
    image_path="path/to/image.jpg",
    strength=0.7,
    aspect_ratio="4:3"
)
```

### FLUX Kontext (High-Quality Transformations)
```python
# Modify image with URL using FLUX Kontext
result = generator.modify_image_kontext(
    prompt="Transform into detailed digital art",
    image_url="https://example.com/image.jpg",
    num_inference_steps=28,
    guidance_scale=2.5,
    resolution_mode="auto"
)

# Modify local image using FLUX Kontext
result = generator.modify_local_image_kontext(
    prompt="Convert to photorealistic painting",
    image_path="path/to/image.jpg",
    num_inference_steps=35,
    guidance_scale=3.0,
    resolution_mode="1280x720"
)
```

### FLUX Kontext Multi (Multi-Image Generation)
```python
# Generate from multiple image URLs
result = generator.modify_multi_images_kontext(
    prompt="Put the little duckling on top of the woman's t-shirt.",
    image_urls=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ],
    guidance_scale=3.5,
    num_images=1,
    aspect_ratio="1:1"
)

# Generate from multiple local images
result = generator.modify_multi_local_images_kontext(
    prompt="Combine these elements into a surreal scene",
    image_paths=["path/to/image1.jpg", "path/to/image2.jpg"],
    guidance_scale=4.0,
    num_images=2,
    aspect_ratio="16:9"
)
```

### Model Comparison
```python
# Compare both models with the same prompt
photon_result = generator.modify_image_photon(
    prompt="Artistic transformation",
    image_url="https://example.com/image.jpg",
    strength=0.7,
    aspect_ratio="1:1"
)

kontext_result = generator.modify_image_kontext(
    prompt="Artistic transformation",
    image_url="https://example.com/image.jpg",
    num_inference_steps=28,
    guidance_scale=2.5,
    resolution_mode="auto"
)
```

### Batch Processing
```python
# Batch modify with Photon Flash
results = generator.batch_modify_images_photon(
    prompts=["Oil painting style", "Pencil sketch", "Digital art"],
    image_urls=["url1", "url2", "url3"],
    strength=0.8,
    aspect_ratio="1:1"
)

# Batch modify with FLUX Kontext
results = generator.batch_modify_images_kontext(
    prompts=["Detailed portrait", "Landscape painting", "Abstract art"],
    image_urls=["url1", "url2", "url3"],
    num_inference_steps=28,
    guidance_scale=2.5,
    resolution_mode="auto"
)
```

## API Reference

### FALImageToImageGenerator

#### Photon Flash Methods

- `modify_image_photon(prompt, image_url, strength=0.8, aspect_ratio="1:1", output_dir=None)`
- `modify_local_image_photon(prompt, image_path, strength=0.8, aspect_ratio="1:1", output_dir=None)`
- `batch_modify_images_photon(prompts, image_urls, strength=0.8, aspect_ratio="1:1", output_dir=None)`

#### Photon Base Methods

- `modify_image_photon_base(prompt, image_url, strength=0.8, aspect_ratio="1:1", output_dir=None)`
- `modify_local_image_photon_base(prompt, image_path, strength=0.8, aspect_ratio="1:1", output_dir=None)`

#### FLUX Kontext Methods

- `modify_image_kontext(prompt, image_url, num_inference_steps=28, guidance_scale=2.5, resolution_mode="auto", output_dir=None)`
- `modify_local_image_kontext(prompt, image_path, num_inference_steps=28, guidance_scale=2.5, resolution_mode="auto", output_dir=None)`
- `batch_modify_images_kontext(prompts, image_urls, num_inference_steps=28, guidance_scale=2.5, resolution_mode="auto", output_dir=None)`

#### FLUX Kontext Multi Methods

- `modify_multi_images_kontext(prompt, image_urls, guidance_scale=3.5, num_images=1, aspect_ratio="1:1", output_dir=None)`
- `modify_multi_local_images_kontext(prompt, image_paths, guidance_scale=3.5, num_images=1, aspect_ratio="1:1", output_dir=None)`

#### Utility Methods

- `get_model_info()` - Get information for both models
- `get_supported_aspect_ratios()` - List Photon Flash aspect ratios
- `get_supported_resolution_modes()` - List FLUX Kontext resolution modes

#### Photon Flash Parameters

- **prompt** (str): Text description of desired modification
- **strength** (float): Modification intensity (0.0-1.0)
- **aspect_ratio** (str): Output aspect ratio ("1:1", "16:9", etc.)
- **output_dir** (str, optional): Custom output directory

#### Photon Base Parameters

- **prompt** (str): Text description of desired modification
- **strength** (float): Modification intensity (0.0-1.0)
- **aspect_ratio** (str): Output aspect ratio ("1:1", "16:9", etc.)
- **output_dir** (str, optional): Custom output directory

#### FLUX Kontext Parameters

- **prompt** (str): Text description of desired transformation
- **num_inference_steps** (int): Inference steps (1-50, default: 28)
- **guidance_scale** (float): Guidance scale (1.0-20.0, default: 2.5)
- **resolution_mode** (str): Resolution mode ("auto", "1280x720", etc.)
- **output_dir** (str, optional): Custom output directory

#### FLUX Kontext Multi Parameters

- **prompt** (str): Text description of desired generation
- **image_urls/image_paths** (List[str]): List of input images (2-10 images)
- **guidance_scale** (float): Guidance scale (1.0-20.0, default: 3.5)
- **num_images** (int): Number of output images (1-10, default: 1)
- **aspect_ratio** (str): Output aspect ratio (from supported list)
- **safety_tolerance** (int): Safety level (1-6, default: 2)
- **output_format** (str): Output format ("jpeg" or "png")
- **output_dir** (str, optional): Custom output directory

## Testing

### Setup Validation (FREE)
```bash
python test_setup.py
```

### Generation Testing (PAID)
```bash
python test_generation.py              # Basic tests for both models
python test_generation.py --quick      # Quick single test (Photon Flash)
python test_generation.py --batch      # Batch processing test
python test_generation.py --all        # All aspect ratios (Photon Flash)
python test_generation.py --kontext       # FLUX Kontext only
python test_generation.py --kontext-multi # FLUX Kontext Multi only
python test_generation.py --photon-base   # Luma Photon Base only
python test_generation.py --compare       # Compare models
```

## Cost Information

- **Estimated Cost**: ~$0.01-0.05 per image modification
- **Setup Tests**: Completely FREE
- **Cost Controls**: Built-in warnings and confirmations

## Prompt Examples

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

## Parameter Guidelines

### Photon Flash - Strength
- **0.0-0.3**: Subtle modifications, preserve original structure
- **0.4-0.6**: Moderate changes, balanced transformation
- **0.7-1.0**: Strong transformations, creative reimagining

### FLUX Kontext - Inference Steps
- **1-15**: Fast generation but lower quality
- **16-35**: Balanced speed and quality (recommended)
- **36-50**: High quality but slower processing

### FLUX Kontext - Guidance Scale
- **1.0-2.0**: More creative freedom, less prompt adherence
- **2.1-5.0**: Balanced prompt following (recommended)
- **5.1-20.0**: Strict prompt adherence, less creativity

## Supported Formats

### Photon Flash - Aspect Ratios
- **1:1**: Square format
- **16:9**: Widescreen/landscape
- **9:16**: Portrait/mobile
- **4:3**: Traditional photo
- **3:4**: Portrait photo
- **21:9**: Ultra-wide
- **9:21**: Ultra-tall

### FLUX Kontext - Resolution Modes
- **auto**: Automatic resolution selection
- **1280x720**: HD 720p (16:9)
- **720x1280**: Vertical HD (9:16)
- **1024x1024**: Square HD (1:1)
- **1536x1024**: Wide format (3:2)
- **1024x1536**: Portrait format (2:3)

## Troubleshooting

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
- **"Unsupported aspect ratio"**: Use one of the supported ratios (Photon Flash)
- **"Unsupported resolution mode"**: Use one of the supported modes (FLUX Kontext)
- **"Strength must be between 0.0 and 1.0"**: Check strength parameter (Photon Flash)
- **"Inference steps must be between 1 and 50"**: Check inference steps (FLUX Kontext)
- **"Guidance scale must be between 1.0 and 20.0"**: Check guidance scale (FLUX Kontext)
- **"File not found"**: Verify local image file path

## Model Information

### Luma Photon Flash
- **Endpoint**: `fal-ai/luma-photon/flash/modify`
- **Features**: Creative, personalizable, intelligent modifications
- **Processing**: Fast, artistic results
- **Best for**: Creative transformations, artistic styles, quick iterations

### Luma Photon Base
- **Endpoint**: `fal-ai/luma-photon/modify`
- **Features**: Most creative, personalizable, intelligent visual model
- **Processing**: High-quality image generation with cost efficiency
- **Cost**: $0.019 per megapixel
- **Best for**: Creative image editing, commercial use, step-function cost improvements

### FLUX Kontext
- **Endpoint**: `fal-ai/flux/kontext/image-to-image`
- **Features**: High-quality, detailed transformations with fine control
- **Processing**: Slower but more detailed results
- **Best for**: Detailed modifications, photorealistic changes, precision edits

## Files

- `fal_image_to_image_generator.py` - Main generator class
- `test_setup.py` - FREE setup validation
- `test_generation.py` - Paid generation tests
- `demo.py` - Interactive demo
- `requirements.txt` - Dependencies
- `README.md` - This documentation