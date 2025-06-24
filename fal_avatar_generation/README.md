# FAL AI Avatar Video Generation

Generate talking avatar videos from images using FAL AI's Avatar models. This implementation provides a Python interface for creating lip-synced avatar videos with both text-to-speech conversion and custom audio file support.

## 🎭 Features

- **Text-to-Speech Avatar Generation**: Convert text to talking avatar videos with 20 voice options
- **Audio-to-Avatar Generation**: Use custom audio files for lip-sync animation
- **Natural Lip-Sync Technology**: Automatic mouth movement synchronization
- **Natural Expressions**: AI-generated facial expressions and movements
- **Customizable Parameters**: Frame count, voice selection, prompts
- **Turbo Mode**: Faster generation with optimized processing
- **Local & Remote Support**: Both local files and URLs for images/audio
- **Cost-Conscious Testing**: Separate FREE and PAID test suites

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install fal-client requests python-dotenv
```

### 2. Configuration

Create a `.env` file with your FAL AI API key:

```env
FAL_KEY=your-fal-ai-api-key-here
```

Get your API key from: https://fal.ai/dashboard

### 3. Basic Usage

#### Text-to-Speech Mode (20 voices available)

```python
from fal_avatar_generator import FALAvatarGenerator

# Initialize generator
generator = FALAvatarGenerator()

# Generate avatar video from text
result = generator.generate_avatar_video(
    image_url="path/to/your/image.jpg",
    text_input="Hello! This is my avatar speaking.",
    voice="Sarah",
    output_path="output/avatar_video.mp4"
)

print(f"Video generated: {result['video']['url']}")
```

#### Audio-to-Avatar Mode (custom audio files)

```python
from fal_avatar_generator import FALAvatarGenerator

# Initialize generator
generator = FALAvatarGenerator()

# Generate avatar video from audio file
result = generator.generate_avatar_from_audio(
    image_url="path/to/your/image.jpg",
    audio_url="path/to/your/audio.mp3",
    output_path="output/avatar_video.mp4"
)

print(f"Video generated: {result['video']['url']}")
```

### 4. Interactive Demo

```bash
python demo.py
```

The demo provides a user-friendly interface to:
- Choose between text-to-speech or audio-to-avatar modes
- Select images (local files, URLs, or sample images)
- Enter text for speech or select audio files
- Choose from 20 available voices (text mode only)
- Configure generation parameters
- Preview cost estimates before generation

## 📋 Available Voices

The FAL AI Avatar model supports 20 different voices:

**Male Voices**: Roger, Charlie, George, Callum, River, Liam, Will, Eric, Chris, Brian, Daniel, Bill

**Female Voices**: Aria, Sarah, Laura, Charlotte, Alice, Matilda, Jessica, Lily

## 🧪 Testing

### FREE Tests (No Cost)

Test your setup without generating videos:

```bash
# Environment and API validation
python test_setup.py
```

This script validates:
- Python environment and dependencies
- FAL AI API key configuration
- Generator class functionality
- Output directory permissions

### PAID Tests (Costs Money)

⚠️ **WARNING**: These tests generate real videos and cost money (~$0.02-0.05 per video)

```bash
# Basic avatar generation test
python test_generation.py

# Quick test with minimal frames (cheaper)
python test_generation.py --quick

# Test specific voice
python test_generation.py --voice Bill

# Compare multiple voices (costs more)
python test_generation.py --compare

# Test custom scenarios
python test_generation.py --scenarios
```

## 💰 Cost Information

**Pricing**: ~$0.02-0.05 per avatar video
- Base cost: ~$0.03 per generation
- Frame count 81: Standard rate
- Frame count >81: 1.25x rate multiplier
- Turbo mode: No additional cost

**Cost Examples**:
- Single video (81 frames): ~$0.030
- Single video (136 frames): ~$0.038
- Voice comparison (3 voices, 136 frames): ~$0.114
- Custom scenarios (2 videos, 136 frames): ~$0.076

## 🎛️ API Reference

### FALAvatarGenerator Class

#### `__init__(api_key=None)`
Initialize the avatar generator.

**Parameters**:
- `api_key` (str, optional): FAL AI API key. Uses `FAL_KEY` environment variable if not provided.

#### `generate_avatar_video(**kwargs)`
Generate a talking avatar video.

**Parameters**:
- `image_url` (str): Image URL or local file path
- `text_input` (str): Text for the avatar to speak
- `voice` (str): Voice name (default: "Sarah")
- `prompt` (str): Generation prompt (default: natural speaking)
- `num_frames` (int): Frame count 81-129 (default: 136)
- `seed` (int, optional): Random seed for reproducibility
- `turbo` (bool): Enable turbo mode (default: True)
- `output_path` (str, optional): Local save path

**Returns**:
- Dictionary with video information and metadata

#### `get_available_voices()`
Get list of available voice options.

**Returns**:
- List of voice names

#### `test_connection()`
Test API connection without generating videos.

**Returns**:
- Boolean indicating connection status

## 🔧 Configuration Options

### Environment Variables

```env
# Required
FAL_KEY=your-api-key

# Optional defaults
DEFAULT_VOICE=Sarah
DEFAULT_FRAMES=136
DEFAULT_TURBO=true
OUTPUT_DIR=output
TEST_OUTPUT_DIR=test_output
```

### Generation Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `num_frames` | int | 81-129 | 136 | Video length in frames |
| `voice` | string | 20 options | "Sarah" | Voice personality |
| `turbo` | boolean | true/false | true | Fast generation mode |
| `seed` | int | any | random | Reproducibility seed |

### Frame Count Guidelines

- **81 frames**: Minimum, standard pricing
- **82-129 frames**: 1.25x pricing multiplier
- **136 frames**: Default, good balance of length and cost
- **129 frames**: Maximum, longest videos

## 🎬 Use Cases

### Professional Content
- Business presentations
- Corporate communications
- Training videos
- Product demonstrations

### Educational Content
- Online courses
- Tutorial videos
- Language learning
- Instructional content

### Creative Projects
- Character voices for stories
- Multilingual content
- Accessibility features
- Interactive experiences

## 📁 Project Structure

```
fal_avatar_generation/
├── fal_avatar_generator.py    # Main generator class
├── demo.py                    # Interactive demonstration
├── test_setup.py             # FREE environment tests
├── test_generation.py        # PAID generation tests
├── requirements.txt          # Python dependencies
├── .env                      # Configuration file
├── README.md                 # This documentation
├── output/                   # Generated videos
└── test_output/             # Test-generated videos
```

## 🛠️ Advanced Usage

### Custom Prompts

```python
# Professional presentation style
result = generator.generate_avatar_video(
    image_url="business_photo.jpg",
    text_input="Welcome to our quarterly review...",
    voice="Roger",
    prompt="A professional person in business attire presenting to an audience with confident and engaging expressions."
)

# Educational content style
result = generator.generate_avatar_video(
    image_url="teacher_photo.jpg",
    text_input="Today we'll learn about...",
    voice="Sarah",
    prompt="An educator explaining concepts with clear articulation and engaging facial expressions."
)
```

### Batch Processing

```python
voices = ["Sarah", "Roger", "Bill"]
text = "This is a voice comparison test."

for voice in voices:
    result = generator.generate_avatar_video(
        image_url="avatar.jpg",
        text_input=text,
        voice=voice,
        output_path=f"output/avatar_{voice.lower()}.mp4"
    )
```

### Error Handling

```python
try:
    result = generator.generate_avatar_video(
        image_url="image.jpg",
        text_input="Hello world!",
        voice="Sarah"
    )
    print("Success:", result['video']['url'])
except ValueError as e:
    print("Configuration error:", e)
except Exception as e:
    print("Generation error:", e)
```

## 🔍 Troubleshooting

### Common Issues

**"FAL_KEY environment variable not set"**
- Solution: Set your API key in `.env` file or environment variable

**"Invalid voice 'XYZ'"**
- Solution: Use `generator.get_available_voices()` to see valid options

**"num_frames must be between 81 and 129"**
- Solution: Adjust frame count to valid range

**"Failed to upload local image"**
- Solution: Check file path and permissions

### Performance Tips

1. **Use turbo mode** for faster generation (enabled by default)
2. **Minimize frame count** for cheaper/faster results
3. **Use remote images** to avoid upload time
4. **Batch similar requests** to optimize API usage

## 📊 Monitoring Usage

Track your API usage and costs:

```python
# Monitor generation results
result = generator.generate_avatar_video(...)

print(f"Generation time: {result['generation_time']:.2f}s")
print(f"File size: {result['video']['file_size'] / (1024*1024):.2f} MB")
print(f"Video URL: {result['video']['url']}")
```

## 🔗 Related Resources

- [FAL AI Documentation](https://fal.ai/models/fal-ai/ai-avatar/single-text)
- [FAL AI Dashboard](https://fal.ai/dashboard)
- [API Pricing](https://fal.ai/pricing)
- [Voice Samples](https://fal.ai/models/fal-ai/ai-avatar/single-text/playground)

## 🤝 Contributing

Contributions are welcome! Please:

1. Test changes with FREE tests first
2. Document any new features
3. Include cost estimates for new functionality
4. Follow the existing code style

## 📄 License

This project follows the same license as the parent repository.

---

**⚠️ Cost Reminder**: Always use FREE tests (`test_setup.py`) for development and validation. Only run PAID tests (`test_generation.py`) when you need to test actual video generation functionality. 