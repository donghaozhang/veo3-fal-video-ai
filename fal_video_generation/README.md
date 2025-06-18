# FAL AI MiniMax Hailuo-02 Video Generation

This project provides Python utilities for generating videos using FAL AI's MiniMax Hailuo-02 model, which offers advanced image-to-video generation with 768p resolution.

## Features

- **Image-to-Video Generation**: Convert images to videos with text prompts
- **Local Image Support**: Upload and process local image files
- **Async Processing**: Support for both synchronous and asynchronous processing
- **Automatic Downloads**: Download generated videos locally
- **Comprehensive Error Handling**: Robust error handling and logging
- **Flexible Configuration**: Customizable duration, prompt optimization, and output settings

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

### Basic Usage

```python
from fal_video_generator import FALVideoGenerator

# Initialize the generator
generator = FALVideoGenerator()

# Generate video from online image
result = generator.generate_video_from_image(
    prompt="Man walked into winter cave with polar bear",
    image_url="https://example.com/image.jpg",
    duration="6",
    output_folder="output"
)

if result:
    print(f"Video URL: {result['video']['url']}")
    print(f"Local path: {result['local_path']}")
```

### Generate from Local Image

```python
# Generate video from local image file
result = generator.generate_video_from_local_image(
    prompt="A beautiful sunset over mountains",
    image_path="path/to/your/image.jpg",
    duration="6",
    output_folder="output"
)
```

### Async Processing

```python
# Use async processing for long-running requests
result = generator.generate_video_from_image(
    prompt="Your prompt here",
    image_url="https://example.com/image.jpg",
    duration="10",
    use_async=True
)
```

## API Reference

### FALVideoGenerator Class

#### `__init__(api_key: Optional[str] = None)`
Initialize the FAL Video Generator.

**Parameters:**
- `api_key`: FAL API key (optional if FAL_KEY environment variable is set)

#### `generate_video_from_image(prompt, image_url, duration="6", prompt_optimizer=True, output_folder="output", use_async=False)`
Generate video from an image URL.

**Parameters:**
- `prompt` (str): Text description for video generation
- `image_url` (str): URL of the image to use as the first frame
- `duration` (str): Duration in seconds ("6" or "10")
- `prompt_optimizer` (bool): Whether to use the model's prompt optimizer
- `output_folder` (str): Local folder to save the generated video
- `use_async` (bool): Whether to use async processing

**Returns:**
- Dictionary containing video URL, metadata, and local path

#### `generate_video_from_local_image(prompt, image_path, duration="6", prompt_optimizer=True, output_folder="output", use_async=False)`
Generate video from a local image file.

**Parameters:**
- `prompt` (str): Text description for video generation
- `image_path` (str): Path to the local image file
- `duration` (str): Duration in seconds ("6" or "10")
- `prompt_optimizer` (bool): Whether to use the model's prompt optimizer
- `output_folder` (str): Local folder to save the generated video
- `use_async` (bool): Whether to use async processing

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
- `"6"`: 6-second video (default)
- `"10"`: 10-second video (not supported for 1080p resolution)

### Prompt Optimizer
- `True`: Use FAL AI's automatic prompt optimization (default)
- `False`: Use your prompt as-is

### Processing Modes
- **Synchronous**: Wait for completion before returning result
- **Asynchronous**: Submit request and poll for completion

## Examples

### Example 1: Basic Image-to-Video

```python
from fal_video_generator import FALVideoGenerator

generator = FALVideoGenerator()

result = generator.generate_video_from_image(
    prompt="A peaceful lake with gentle ripples, birds flying overhead",
    image_url="https://example.com/lake.jpg",
    duration="6"
)

if result:
    print(f"✅ Video generated: {result['video']['url']}")
```

### Example 2: Local Image Processing

```python
# Process a local image
result = generator.generate_video_from_local_image(
    prompt="The flowers sway gently in the breeze",
    image_path="./images/flowers.jpg",
    duration="6",
    output_folder="my_videos"
)
```

### Example 3: Async Processing

```python
# For longer videos or when you need to do other work
result = generator.generate_video_from_image(
    prompt="Time-lapse of clouds moving across the sky",
    image_url="https://example.com/sky.jpg",
    duration="10",
    use_async=True
)
```

## Error Handling

The library includes comprehensive error handling:

- **API Key Validation**: Checks for valid FAL API key
- **File Validation**: Verifies local image files exist
- **Network Errors**: Handles upload/download failures
- **API Errors**: Manages FAL AI API response errors
- **Timeout Handling**: Manages long-running requests

## Output Structure

Generated videos are saved with the following structure:

```
output_folder/
├── generated_video_1.mp4
├── generated_video_2.mp4
└── ...
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- GIF (.gif)

## Limitations

- 10-second videos are not supported for 1080p resolution
- Maximum prompt length: varies by model
- File size limits apply for image uploads
- Rate limiting may apply based on your FAL AI plan

## Troubleshooting

### Common Issues

1. **"FAL API key is required"**
   - Ensure FAL_KEY is set in your .env file
   - Verify the API key is correct

2. **"Image file not found"**
   - Check the image path is correct
   - Verify file permissions

3. **"Request failed"**
   - Check your FAL AI account status
   - Verify you have sufficient credits
   - Check internet connection

4. **"No video found in result"**
   - The generation may have failed
   - Check the logs for error messages

### Debug Mode

Enable detailed logging by setting environment variable:

```bash
export FAL_DEBUG=1
```

## API Documentation

For detailed API documentation, visit: [FAL AI MiniMax Hailuo-02 Documentation](https://fal.ai/models/fal-ai/minimax/hailuo-02/standard/image-to-video/api?platform=python)

## License

This project is provided as-is for educational and development purposes. Please refer to FAL AI's terms of service for API usage guidelines. 