# FAL AI Video Generation

This project provides Python utilities for generating videos using FAL AI's powerful video generation models:

- **MiniMax Hailuo-02**: Advanced image-to-video generation with 768p resolution, 6-10 second duration
- **Kling Video 2.1**: High-quality image-to-video generation with cinematic quality, 5-10 second duration

## Features

- **Dual Model Support**: Choose between MiniMax Hailuo-02 and Kling Video 2.1
- **Image-to-Video Generation**: Convert images to videos with text prompts
- **Local Image Support**: Upload and process local image files
- **Async Processing**: Support for both synchronous and asynchronous processing
- **Automatic Downloads**: Download generated videos locally
- **Comprehensive Error Handling**: Robust error handling and logging
- **Flexible Configuration**: Customizable duration, prompt optimization, and output settings
- **Model Comparison**: Built-in tools to compare outputs from both models

## Model Comparison

| Feature | MiniMax Hailuo-02 | Kling Video 2.1 |
|---------|-------------------|------------------|
| Resolution | 768p | High Quality |
| Duration | 6-10 seconds | 5-10 seconds |
| Special Features | Prompt Optimizer | CFG Scale, Negative Prompts |
| Best For | General video generation | Cinematic quality videos |

## Prerequisites

1. FAL AI account and API key
2. Python 3.7+ installed
3. Internet connection for API calls

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up API Key

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Edit the `.env` file and add your FAL AI API key:

```
FAL_KEY=your_actual_fal_api_key_here
```

## Usage

### Basic Usage - Hailuo Model

```python
from fal_video_generator import FALVideoGenerator

# Initialize the generator
generator = FALVideoGenerator()

# Generate video using MiniMax Hailuo-02
result = generator.generate_video_with_hailuo(
    prompt="Man walked into winter cave with polar bear",
    image_url="https://example.com/image.jpg",
    duration="6",
    output_folder="output"
)

if result:
    print(f"Video URL: {result['video']['url']}")
    print(f"Local path: {result['local_path']}")
```

### Basic Usage - Kling Model

```python
# Generate video using Kling Video 2.1
result = generator.generate_video_with_kling(
    prompt="As the sun dips below the horizon, powerful waves crash against rocks",
    image_url="https://example.com/image.jpg",
    duration="5",
    negative_prompt="blur, distort, low quality",
    cfg_scale=0.5,
    output_folder="output"
)
```

### Universal Method (Model Selection)

```python
# Use the universal method with model selection
result = generator.generate_video_from_image(
    prompt="A beautiful sunset over mountains",
    image_url="https://example.com/image.jpg",
    duration="6",
    model="hailuo"  # or "kling"
)
```

### Generate from Local Image

```python
# Generate video from local image file
result = generator.generate_video_from_local_image(
    prompt="A beautiful sunset over mountains",
    image_path="path/to/your/image.jpg",
    duration="6",
    model="kling",  # Choose model
    output_folder="output"
)
```

### Async Processing

```python
# Use async processing for long-running requests
result = generator.generate_video_with_hailuo(
    prompt="Your prompt here",
    image_url="https://example.com/image.jpg",
    duration="10",
    use_async=True
)
```

## API Reference

### FALVideoGenerator Class

#### `__init__(api_key: Optional[str] = None)`
Initialize the FAL Video Generator with support for both models.

**Parameters:**
- `api_key`: FAL API key (optional if FAL_KEY environment variable is set)

#### `generate_video_with_hailuo(prompt, image_url, duration="6", prompt_optimizer=True, output_folder="output", use_async=False)`
Generate video using MiniMax Hailuo-02 model.

**Parameters:**
- `prompt` (str): Text description for video generation
- `image_url` (str): URL of the image to use as the first frame
- `duration` (str): Duration in seconds ("6" or "10")
- `prompt_optimizer` (bool): Whether to use the model's prompt optimizer
- `output_folder` (str): Local folder to save the generated video
- `use_async` (bool): Whether to use async processing

**Returns:**
- Dictionary containing video URL, metadata, and local path

#### `generate_video_with_kling(prompt, image_url, duration="5", negative_prompt="blur, distort, and low quality", cfg_scale=0.5, output_folder="output", use_async=False)`
Generate video using Kling Video 2.1 model.

**Parameters:**
- `prompt` (str): Text description for video generation
- `image_url` (str): URL of the image to use as the first frame
- `duration` (str): Duration in seconds ("5" or "10")
- `negative_prompt` (str): Negative prompt to avoid certain elements
- `cfg_scale` (float): CFG scale for guidance (0.5 default)
- `output_folder` (str): Local folder to save the generated video
- `use_async` (bool): Whether to use async processing

**Returns:**
- Dictionary containing video URL, metadata, and local path

#### `generate_video_from_image(prompt, image_url, duration="6", prompt_optimizer=True, output_folder="output", use_async=False, model="hailuo")`
Universal method that supports both models.

**Parameters:**
- `prompt` (str): Text description for video generation
- `image_url` (str): URL of the image to use as the first frame
- `duration` (str): Duration in seconds (varies by model)
- `prompt_optimizer` (bool): Whether to use prompt optimizer (Hailuo only)
- `output_folder` (str): Local folder to save the generated video
- `use_async` (bool): Whether to use async processing
- `model` (str): Model to use ("hailuo" or "kling")

**Returns:**
- Dictionary containing video URL, metadata, and local path

#### `generate_video_from_local_image(prompt, image_path, duration="6", prompt_optimizer=True, output_folder="output", use_async=False, model="hailuo")`
Generate video from a local image file using either model.

**Parameters:**
- `prompt` (str): Text description for video generation
- `image_path` (str): Path to the local image file
- `duration` (str): Duration in seconds (varies by model)
- `prompt_optimizer` (bool): Whether to use prompt optimizer (Hailuo only)
- `output_folder` (str): Local folder to save the generated video
- `use_async` (bool): Whether to use async processing
- `model` (str): Model to use ("hailuo" or "kling")

**Returns:**
- Dictionary containing video URL, metadata, and local path

#### `upload_local_image(image_path)`
Upload a local image file to FAL AI.

**Parameters:**
- `image_path` (str): Path to the local image file

**Returns:**
- URL of the uploaded image or None if failed

## Configuration Options

### Duration Settings

**MiniMax Hailuo-02:**
- `"6"`: 6-second video (default)
- `"10"`: 10-second video

**Kling Video 2.1:**
- `"5"`: 5-second video (default)
- `"10"`: 10-second video

### Model-Specific Options

**Hailuo Options:**
- `prompt_optimizer`: Use FAL AI's automatic prompt optimization (default: True)

**Kling Options:**
- `negative_prompt`: Elements to avoid in generation (default: "blur, distort, and low quality")
- `cfg_scale`: Classifier Free Guidance scale (default: 0.5)

### Processing Modes
- **Synchronous**: Wait for completion before returning result
- **Asynchronous**: Submit request and poll for completion

## Examples

### Example 1: Compare Both Models

```python
from fal_video_generator import FALVideoGenerator

generator = FALVideoGenerator()

# Generate with Hailuo
result_hailuo = generator.generate_video_with_hailuo(
    prompt="A peaceful lake with gentle ripples",
    image_url="https://example.com/lake.jpg",
    duration="6"
)

# Generate with Kling
result_kling = generator.generate_video_with_kling(
    prompt="A peaceful lake with gentle ripples, cinematic quality",
    image_url="https://example.com/lake.jpg",
    duration="5"
)

print(f"Hailuo: {result_hailuo['video']['url']}")
print(f"Kling: {result_kling['video']['url']}")
```

### Example 2: Kling with Custom Settings

```python
# Use Kling with custom negative prompt and CFG scale
result = generator.generate_video_with_kling(
    prompt="Epic dragon flying over medieval castle, cinematic lighting",
    image_url="https://example.com/castle.jpg",
    duration="10",
    negative_prompt="blur, distort, low quality, cartoon, anime",
    cfg_scale=0.7,
    output_folder="epic_videos"
)
```

### Example 3: Local Image with Model Selection

```python
# Process a local image with model choice
result = generator.generate_video_from_local_image(
    prompt="The flowers sway gently in the breeze, magical atmosphere",
    image_path="./images/flowers.jpg",
    duration="5",
    model="kling",  # Use Kling for cinematic quality
    output_folder="my_videos"
)
```

## Testing

### Cost-Conscious Testing

⚠️ **Important**: Video generation costs money! Choose your tests carefully to avoid unnecessary charges.

### FREE Testing (No Costs)

```bash
# Test API connection only - completely FREE
python test_api_only.py

# Basic setup test - FREE (no video generation)
python test_fal_ai.py
```

### Paid Testing (Generates Real Videos)

```bash
# Test single model - ~$0.02-0.05 per test
python test_fal_ai.py --hailuo      # Test Hailuo model only
python test_fal_ai.py --kling       # Test Kling model only
python test_fal_ai.py --quick       # Same as --hailuo

# Full test with detailed output - ~$0.02-0.05
python test_fal_ai.py --full

# Compare both models - ~$0.04-0.10 (EXPENSIVE!)
python test_fal_ai.py --compare     # Generates 2 videos
```

### Test Options Summary

| Command | Cost | Description |
|---------|------|-------------|
| `python test_api_only.py` | **FREE** | API connection test only |
| `python test_fal_ai.py` | **FREE** | Setup + API test (no videos) |
| `python test_fal_ai.py --hailuo` | ~$0.02-0.05 | Test Hailuo model |
| `python test_fal_ai.py --kling` | ~$0.02-0.05 | Test Kling model |
| `python test_fal_ai.py --compare` | ~$0.04-0.10 | Test both models |

### Interactive Demo

⚠️ **Cost Warning**: The demo generates real videos that cost money!

```bash
python demo.py
```

The demo offers:
1. **Cost warnings** and confirmation prompts
2. Model selection (Hailuo vs Kling) with cost estimates
3. Multiple demo scenarios with individual cost indicators
4. Custom input options
5. Side-by-side comparison (expensive - generates 2 videos)

Each demo option shows estimated costs before generation.

## Troubleshooting

### Common Issues

**1. API Key Issues**
```
❌ Error: FAL API key is required
```
- Ensure `.env` file exists with valid `FAL_KEY`
- API key should start with `fal-`

**2. Model-Specific Errors**
```
❌ Duration "10" not supported for 1080p
```
- Use duration "5" or "6" for high-resolution outputs
- Check model-specific duration limits

**3. Image Upload Failures**
```
❌ Error uploading image
```
- Verify image file exists and is readable
- Check image format (JPEG, PNG, WebP, GIF supported)
- Ensure stable internet connection

**4. Video Generation Timeout**
```
❌ Request timeout
```
- Try using `use_async=True` for longer requests
- Check FAL AI service status
- Reduce video duration if possible

### Model Selection Guide

**Choose MiniMax Hailuo-02 when:**
- You want consistent 768p resolution
- You need the prompt optimizer feature
- You prefer 6-10 second durations
- You want reliable, fast generation

**Choose Kling Video 2.1 when:**
- You want the highest quality output
- You need fine control with CFG scale and negative prompts
- You're creating cinematic content
- You want 5-10 second durations

## File Structure

```
fal_video_generation/
├── fal_video_generator.py    # Main generator class
├── demo.py                   # Interactive demo
├── test_fal_ai.py           # Comprehensive test suite
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── output/                 # Generated videos folder
```

## Requirements

See `requirements.txt` for the complete list of dependencies:

- `fal-client`: FAL AI client library
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests
- `typing-extensions`: Type hints support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Run the test suite to diagnose problems
3. Review FAL AI documentation: https://fal.ai/models
4. Create an issue in the repository

## Model Endpoints

- **MiniMax Hailuo-02**: `fal-ai/minimax/hailuo-02/standard/image-to-video`
- **Kling Video 2.1**: `fal-ai/kling-video/v2.1/standard/image-to-video`

Both models are production-ready and actively maintained by FAL AI. 