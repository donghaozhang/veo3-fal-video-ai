# FAL AI Text-to-Video Generator

**Unified text-to-video generation** supporting multiple models via FAL AI. Choose between cost-effective and premium options with a single, unified interface.

## 🎬 Supported Models

### 1. MiniMax Hailuo-02 Pro (Most Cost-Effective)
- **Cost**: ~$0.08 per video
- **Resolution**: 1080p
- **Duration**: 6 seconds (fixed)
- **Use case**: Most cost-effective, high-quality generation

### 2. Google Veo 3 Fast (Balanced)
- **Cost**: $1.25-$3.20 per video
- **Resolution**: 720p
- **Duration**: 5-8 seconds (variable)
- **Use case**: Balanced cost and quality, faster generation

### 3. Google Veo 3 (Premium)
- **Cost**: $2.50-$6.00 per video
- **Resolution**: 720p
- **Duration**: 5-8 seconds (variable)
- **Use case**: Premium quality, advanced controls, audio support

## ✨ Features

### 🎬 Video Generation
- **1080p resolution** - Professional quality output
- **6-second duration** - Perfect for social media and demos
- **Commercial use allowed** - Use generated videos commercially
- **Prompt optimization** - Automatic prompt enhancement for better results

### 🤖 Model: MiniMax Hailuo-02 Pro
- State-of-the-art text-to-video model
- High-quality, realistic video generation
- Optimized for diverse content types
- Fast generation times

### 💰 Cost-Conscious Design
- **Clear cost warnings** - Always know what you'll pay
- **Free setup testing** - Validate configuration without costs
- **Batch processing** - Efficient for multiple videos
- **~$0.08 per video** - Transparent pricing

## Quick Start

### 1. Installation

```bash
cd fal_text_to_video
pip install -r requirements.txt
```

### 2. Setup Validation (FREE)

```bash
python test_setup.py  # Validates both models without costs
```

### 2. Get API Key

Get your FAL API key from [FAL AI Dashboard](https://fal.ai/dashboard/keys)

### 3. Set Environment Variable

```bash
export FAL_KEY="your_fal_api_key_here"
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

### 4. Test Setup (FREE)

```bash
python test_setup.py
```

This validates your configuration without any API costs.

### 5. Interactive Demo

```bash
python demo.py
```

User-friendly interface with cost warnings and examples.

## Usage Examples

### Basic Video Generation

```python
from fal_text_to_video_generator import FALTextToVideoGenerator, TextToVideoModel

# Initialize unified generator
generator = FALTextToVideoGenerator(verbose=True)

# Option 1: Cost-effective generation (default)
result1 = generator.generate_video(
    prompt="A majestic eagle soaring over mountains at sunrise",
    model=TextToVideoModel.MINIMAX_HAILUO,  # $0.08
    prompt_optimizer=True
)

# Option 2: Premium generation with advanced controls
result2 = generator.generate_video(
    prompt="A serene lake reflecting autumn colors",
    model=TextToVideoModel.GOOGLE_VEO3,  # $2.50-$6.00
    duration="8s",
    generate_audio=True,
    aspect_ratio="16:9",
    negative_prompt="blurry, low quality"
)

# Check results
for result in [result1, result2]:
    if result['success']:
        print(f"✅ Video saved: {result['local_path']} (${result['cost_usd']:.2f})")
    else:
        print(f"❌ Generation failed: {result['error']}")
```

### Batch Generation

```python
# Generate multiple videos
prompts = [
    "A peaceful cat sleeping in sunlight",
    "Ocean waves at sunset with seagulls",
    "A butterfly landing on a flower"
]

results = generator.generate_batch(
    prompts=prompts,
    prompt_optimizer=True
)

# Check results
for prompt, result in results.items():
    if result['success']:
        print(f"✅ {prompt} → {result['filename']}")
    else:
        print(f"❌ {prompt} → Failed")
```

### Model Information

```python
# Get model details
info = generator.get_model_info()
print(f"Model: {info['model_name']}")
print(f"Resolution: {info['resolution']}")
print(f"Cost: {info['cost_per_video']}")

# Or print formatted info
generator.print_model_info()
```

## Cost Information

### Pricing
- **$0.08 per video** generated
- 1080p resolution, 6 seconds duration
- No additional fees for prompt optimization
- Commercial usage included

### Cost-Conscious Features
- **Free setup testing** with `test_setup.py`
- **Clear cost warnings** before generation
- **User confirmation** required for paid operations
- **Batch estimation** shows total costs upfront

## Testing

### Free Setup Test
```bash
python test_setup.py
```
Validates:
- Dependencies installation
- Environment variables
- API key format
- Directory permissions
- Module imports

### Paid Generation Test
```bash
python test_generation.py
```
⚠️ **Warning**: This incurs costs (~$0.08-0.24 depending on tests chosen)

## File Structure

```
fal_text_to_video/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment configuration template
├── fal_text_to_video_generator.py     # Main generator class
├── test_setup.py                      # Free setup validation
├── test_generation.py                 # Paid generation tests
├── demo.py                            # Interactive demonstration
└── output/                           # Generated videos (auto-created)
```

## API Reference

### FALTextToVideoGenerator

Main class for video generation.

#### Initialization
```python
generator = FALTextToVideoGenerator(
    api_key=None,      # Optional: API key (uses FAL_KEY env var if not provided)
    verbose=True       # Enable detailed output
)
```

#### Methods

##### `generate_video(prompt, prompt_optimizer=True, output_filename=None, timeout=300)`
Generate a single video from text description.

**Parameters:**
- `prompt` (str): Text description for video generation
- `prompt_optimizer` (bool): Enable prompt optimization (default: True)
- `output_filename` (str, optional): Custom output filename
- `timeout` (int): Maximum wait time in seconds (default: 300)

**Returns:** Dict with success status, video URL, local path, and metadata

##### `generate_batch(prompts, prompt_optimizer=True, timeout=300)`
Generate multiple videos from a list of prompts.

**Parameters:**
- `prompts` (list): List of text descriptions
- `prompt_optimizer` (bool): Enable prompt optimization (default: True)
- `timeout` (int): Maximum wait time per video (default: 300)

**Returns:** Dict of results keyed by prompt

##### `test_connection()`
Validate API key and connection without generating videos.

**Returns:** Boolean indicating connection status

##### `get_model_info()`
Get detailed information about the MiniMax Hailuo-02 Pro model.

**Returns:** Dict with model specifications and features

## Prompt Writing Tips

### Best Practices
- **Be specific and descriptive** - Include visual details
- **Mention lighting and mood** - "at sunset", "in soft light"
- **Describe camera angles** - "close-up", "wide shot", "aerial view"
- **Include movement** - "slowly moving", "flying through", "walking"
- **Keep under 200 characters** - Shorter prompts often work better

### Example Prompts

#### Nature Scenes
- "A waterfall cascading into a crystal clear pool surrounded by lush greenery"
- "Morning mist rising from a calm lake with mountains in the background"
- "A field of wildflowers swaying gently in the wind at golden hour"

#### Urban Scenes
- "Rain-soaked city streets at night with colorful neon reflections"
- "Time-lapse of busy traffic flowing through a modern city intersection"
- "A quiet café street scene with people walking under warm streetlights"

#### Abstract/Artistic
- "Colorful paint drops falling into water in slow motion"
- "Geometric shapes morphing and transforming in vibrant colors"
- "Light rays streaming through ancient cathedral windows"

## Model Specifications

### MiniMax Hailuo-02 Pro
- **Resolution**: 1080p (1920x1080)
- **Duration**: 6 seconds
- **Format**: MP4
- **Quality**: High-definition
- **Commercial License**: Included
- **Generation Time**: ~30-60 seconds
- **Prompt Optimization**: Available

### Supported Content
- Natural scenes and landscapes
- Urban environments
- People and animals
- Abstract visuals
- Product demonstrations
- Artistic compositions

## Troubleshooting

### Common Issues

#### "FAL API key not found"
```bash
# Set environment variable
export FAL_KEY="your_api_key_here"

# Or create .env file
echo "FAL_KEY=your_api_key_here" > .env
```

#### "fal-client not installed"
```bash
pip install fal-client
# Or install all dependencies
pip install -r requirements.txt
```

#### "Generation timeout"
- Increase timeout parameter in generate_video()
- Check internet connection
- Try again during off-peak hours

#### "Rate limit exceeded"
- Wait a few minutes between requests
- Use batch processing for multiple videos
- Contact FAL AI for higher rate limits

### Debug Commands

```bash
# Test environment setup
python test_setup.py

# Check dependencies
python -c "import fal_client; print('fal_client OK')"

# Verify API key format
python -c "import os; print('API key format:', 'OK' if os.getenv('FAL_KEY', '').startswith('sk-') else 'Invalid')"
```

## Cost Management

### Before You Start
1. **Run free tests first**: `python test_setup.py`
2. **Understand pricing**: $0.08 per 6-second video
3. **Set spending limits**: Track your usage
4. **Test with single videos**: Before batch processing

### Cost Estimation
- Single video: ~$0.08
- Batch of 5 videos: ~$0.40
- Batch of 10 videos: ~$0.80
- Testing suite: ~$0.24 (3 videos)

### Money-Saving Tips
- Use prompt optimization (included in cost)
- Test prompts with shorter descriptions first
- Batch multiple videos together
- Save successful prompts for reuse

## API Documentation

This implementation is based on the official FAL AI documentation:
- [MiniMax Hailuo-02 Pro API](https://fal.ai/models/fal-ai/minimax/hailuo-02/pro/text-to-video/api)
- [FAL AI Python Client](https://fal.ai/docs/python-client)

## License

This project is for educational and commercial use. Please refer to FAL AI's terms of service for commercial usage rights.

Generated videos can be used commercially as per FAL AI's licensing terms.

## Contributing

Feel free to submit issues and enhancement requests! This implementation covers the core FAL AI text-to-video functionality with cost-conscious design patterns.