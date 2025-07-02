# FAL Video to Video - AI Audio Generation

AI-powered video audio generation using FAL's ThinkSound API. Automatically add realistic audio, sound effects, and music to any video using advanced AI models.

## Features

- 🎵 **AI Audio Generation**: Create realistic audio for any video
- 💬 **Text Prompts**: Guide audio generation with natural language
- 🎬 **Multiple Input Formats**: Support for MP4, MOV, AVI, WebM
- 🔄 **Reproducible Results**: Use seeds for consistent outputs
- 🖥️ **CLI Interface**: Command-line tool for batch processing
- 💰 **Cost-Effective**: ~$0.001 per second of video

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your FAL_KEY
```

### Basic Usage

```python
from fal_video_to_video import FALVideoToVideoGenerator

# Initialize generator
generator = FALVideoToVideoGenerator()

# Add audio to video from URL
result = generator.add_audio_to_video(
    video_url="https://example.com/video.mp4",
    prompt="add dramatic orchestral music"
)

# Add audio to local video
result = generator.add_audio_to_local_video(
    video_path="input/my_video.mp4", 
    prompt="add ambient nature sounds"
)
```

### CLI Usage

```bash
# List available models
python -m fal_video_to_video list-models

# Add audio to video
python -m fal_video_to_video add-audio -i input/video.mp4 -p "add dramatic music"

# Process from URL
python -m fal_video_to_video add-audio -u "https://example.com/video.mp4" -p "add sound effects"

# Batch processing
python -m fal_video_to_video batch -f batch.json
```

## Environment Setup

1. **Get FAL API Key**
   - Sign up at [fal.ai](https://fal.ai)
   - Get your API key from the dashboard

2. **Configure Environment**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env file
   FAL_KEY=your_fal_api_key_here
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## API Reference

### FALVideoToVideoGenerator

Main interface for video audio generation.

#### Methods

##### `add_audio_to_video(video_url, model="thinksound", prompt=None, seed=None, output_dir=None)`

Add AI-generated audio to a video from URL.

**Parameters:**
- `video_url` (str): URL of the input video
- `model` (str): Model to use (default: "thinksound") 
- `prompt` (str, optional): Text prompt to guide audio generation
- `seed` (int, optional): Random seed for reproducibility
- `output_dir` (str, optional): Custom output directory

**Returns:**
- Dictionary with generation results

##### `add_audio_to_local_video(video_path, model="thinksound", prompt=None, seed=None, output_dir=None)`

Add AI-generated audio to a local video file.

**Parameters:**
- `video_path` (str): Path to local video file
- `model` (str): Model to use (default: "thinksound")
- `prompt` (str, optional): Text prompt to guide audio generation  
- `seed` (int, optional): Random seed for reproducibility
- `output_dir` (str, optional): Custom output directory

**Returns:**
- Dictionary with generation results

## Models

### ThinkSound

AI-powered video audio generation that creates realistic sound effects for any video.

**Features:**
- Automatic sound effect generation
- Text prompt guidance
- Video context understanding
- High-quality audio synthesis
- Commercial use license

**Pricing:** $0.001 per second  
**Max Duration:** 300 seconds (5 minutes)  
**Output Format:** MP4

## Examples

### Basic Audio Generation

```python
from fal_video_to_video import FALVideoToVideoGenerator

generator = FALVideoToVideoGenerator()

# Simple audio generation
result = generator.add_audio_to_video(
    video_url="https://example.com/nature_video.mp4",
    prompt="add peaceful forest sounds with birds chirping"
)

if result["success"]:
    print(f"Generated video: {result['local_path']}")
```

### With Custom Settings

```python
# Generate with specific seed for reproducibility
result = generator.add_audio_to_local_video(
    video_path="input/action_scene.mp4",
    prompt="add dramatic music and explosion sound effects",
    seed=42,
    output_dir="custom_output"
)
```

### Batch Processing

```python
# Create batch configuration
batch_config = [
    {
        "video_path": "input/video1.mp4",
        "prompt": "add ambient music",
        "seed": 123
    },
    {
        "video_url": "https://example.com/video2.mp4", 
        "prompt": "add sound effects"
    }
]

# Process batch via CLI
# python -m fal_video_to_video batch -f batch.json
```

## Testing

### Setup Test (Free)

```bash
# Validate environment and setup
python tests/test_setup.py
```

### Generation Test (Costs API credits)

```bash
# Test actual audio generation
python tests/test_generation.py
```

### CLI Test

```bash
# Test command-line interface
bash tests/test_cli.sh
```

## Project Structure

```
fal_video_to_video/
├── input/                    # Input videos
├── output/                   # Generated videos
├── test_output/             # Test outputs
├── fal_video_to_video/      # Main package
│   ├── config/              # Configuration
│   ├── models/              # Model implementations
│   └── utils/               # Utilities
├── tests/                   # Test scripts
├── examples/                # Usage examples
└── docs/                    # Documentation
```

## Error Handling

The generator provides comprehensive error handling:

```python
result = generator.add_audio_to_video(video_url="invalid_url")

if not result["success"]:
    print(f"Error: {result['error']}")
    # Handle error appropriately
```

Common errors:
- Invalid API key
- Video file too large (>100MB)
- Video too long (>5 minutes)
- Unsupported video format
- Network connection issues

## Cost Management

- **Pricing**: ~$0.001 per second of video
- **Example costs**:
  - 10-second video: ~$0.01
  - 1-minute video: ~$0.06
  - 5-minute video: ~$0.30

**Cost-saving tips:**
1. Test with short videos first
2. Use `test_setup.py` for free validation
3. Trim videos to essential content
4. Use batch processing for efficiency

## Supported Formats

**Input formats:**
- MP4, MOV, AVI, WebM
- Max size: 100MB
- Max duration: 300 seconds (5 minutes)

**Output format:**
- MP4 with H.264 video codec
- High-quality audio track added

## License

Commercial use license included with FAL API subscription.

## Support

- 📖 **Documentation**: See `docs/` folder
- 🐛 **Issues**: Report bugs in project issues
- 💬 **API Support**: [FAL AI Support](https://fal.ai/support)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## Changelog

### v0.1.0
- Initial release
- ThinkSound model support
- CLI interface
- Batch processing
- Comprehensive test suite