# FAL AI Text-to-Image Generator

A comprehensive Python module for generating images using four different FAL AI text-to-image models. This implementation provides a unified interface with cost-conscious testing and production-ready features.

## 🎨 Supported Models

| Model | Endpoint | Description | Strengths | Cost |
|-------|----------|-------------|-----------|------|
| **Imagen 4 Preview Fast** | `fal-ai/imagen4/preview/fast` | Google's cost-effective model | Fast, reliable, cost-effective | ~$0.01 |
| **Seedream v3** | `fal-ai/bytedance/seedream/v3/text-to-image` | Bilingual (Chinese/English) | Bilingual support, high quality | ~$0.01 |
| **FLUX.1 Schnell** | `fal-ai/flux-1/schnell` | Fastest FLUX model | Ultra-fast, good quality | ~$0.01 |
| **FLUX.1 Dev** | `fal-ai/flux-1/dev` | High-quality 12B parameter model | Highest quality, professional | ~$0.02 |

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the fal_text_to_image folder
cd fal_text_to_image

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your FAL AI API key:

```bash
# FAL AI API Configuration
FAL_KEY=your_fal_api_key_here

# Optional: Additional configuration
FAL_TIMEOUT=300
FAL_MAX_RETRIES=3
```

### 3. Test Setup (FREE)

Before generating any images, test your setup:

```bash
# Completely FREE - no image generation
python test_api_only.py
```

### 4. Generate Your First Image

```python
from fal_text_to_image_generator import FALTextToImageGenerator

# Initialize generator
generator = FALTextToImageGenerator()

# Generate with FLUX Schnell (fastest)
result = generator.generate_with_flux_schnell(
    prompt="A beautiful sunset over mountains, digital art style",
    image_size="landscape_4_3"
)

if result['success']:
    print(f"Image URL: {result['image_url']}")
    # Download locally
    local_path = generator.download_image(result['image_url'])
    print(f"Saved to: {local_path}")
```

## 💰 Cost-Conscious Testing

### FREE Tests (No Cost)
```bash
# API connection and setup validation only
python test_api_only.py                    # Completely FREE
python test_text_to_image.py               # FREE setup test
```

### PAID Tests (Generate Real Images)
```bash
# Single model tests (~$0.01-0.02 each)
python test_text_to_image.py --imagen4     # Test Imagen 4
python test_text_to_image.py --seedream    # Test Seedream  
python test_text_to_image.py --flux-schnell # Test FLUX Schnell
python test_text_to_image.py --flux-dev    # Test FLUX Dev

# Comparison test (~$0.04-0.08 - generates 4 images)
python test_text_to_image.py --compare     # Test all models
python test_text_to_image.py --full        # Full test with downloads
```

**⚠️ Cost Protection**: All paid tests require explicit confirmation before charging your account.

## 🎯 Usage Examples

### Universal Interface

```python
from fal_text_to_image_generator import FALTextToImageGenerator

generator = FALTextToImageGenerator()

# Generate with any model
result = generator.generate_image(
    prompt="A futuristic cityscape at night",
    model="flux_schnell",  # or "imagen4", "seedream", "flux_dev"
    negative_prompt="blur, low quality"  # for supported models
)
```

### Model-Specific Methods

#### Imagen 4 Preview Fast
```python
result = generator.generate_with_imagen4(
    prompt="A peaceful garden with flowers",
    image_size="landscape_4_3",  # square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9
    num_inference_steps=4,       # 1-8, faster = lower quality
    guidance_scale=3.0,          # 1.0-10.0, how closely to follow prompt
    num_images=1,                # 1-4 images
    enable_safety_checker=True
)
```

#### Seedream v3 (Bilingual)
```python
# English prompt
result = generator.generate_with_seedream(
    prompt="A dragon flying over a castle",
    image_size="1024x1024",      # 512x512, 768x768, 1024x1024, 1152x896, 896x1152
    negative_prompt="blur, distortion, low quality",
    guidance_scale=7.5,          # 1.0-20.0
    num_inference_steps=20       # 1-50
)

# Chinese prompt
result = generator.generate_with_seedream(
    prompt="一条龙在城堡上空飞翔",  # Chinese text supported
    negative_prompt="模糊，扭曲，低质量"
)
```

#### FLUX.1 Schnell (Fastest)
```python
result = generator.generate_with_flux_schnell(
    prompt="A robot in a cyberpunk city",
    image_size="landscape_4_3",   # square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9
    num_inference_steps=4,        # 1-4 recommended for Schnell
    num_images=1
)
```

#### FLUX.1 Dev (Highest Quality)
```python
result = generator.generate_with_flux_dev(
    prompt="A professional portrait, photorealistic",
    image_size="portrait_4_3",
    num_inference_steps=28,       # 1-50, more steps = higher quality
    guidance_scale=3.5,           # 1.0-10.0
    negative_prompt="cartoon, anime, low quality, blur",
    num_images=1
)
```

### Model Comparison

```python
# Compare all models with same prompt (EXPENSIVE - ~$0.04-0.08)
results = generator.compare_models(
    prompt="A majestic eagle soaring over mountains",
    negative_prompt="blur, low quality",
    output_folder="comparison_output"
)

# Results contain success/failure info and local paths for each model
for model, result in results.items():
    if result['success']:
        print(f"{model}: {result['result']['image_url']}")
        print(f"Local: {result['result']['local_path']}")
```

## 🔧 Interactive Demo

Run the interactive demo for hands-on experience:

```bash
python demo.py
```

**Demo Features:**
- Cost warnings and confirmation prompts
- Model selection menu with cost estimates
- Single image generation with all models
- Side-by-side model comparison
- Automatic image downloading
- Model information display

## 📊 Model Selection Guide

### Choose **Imagen 4 Preview Fast** when:
- You need reliable, consistent results
- Cost is a primary concern
- You want Google's proven technology
- Speed and reliability are more important than maximum quality

### Choose **Seedream v3** when:
- You need bilingual support (Chinese/English)
- You want negative prompt control
- You need flexible image sizes
- You're working with Asian languages or content

### Choose **FLUX.1 Schnell** when:
- Speed is the top priority
- You need good quality with minimal cost
- You're doing rapid prototyping
- You want the fastest turnaround time

### Choose **FLUX.1 Dev** when:
- Quality is the top priority
- You need professional-grade results
- You're willing to pay more for better output
- You need fine control over generation parameters

## 🛠️ Advanced Features

### Custom Parameters

Each model supports different parameters. Use the universal interface with custom kwargs:

```python
# Imagen 4 with custom parameters
result = generator.generate_image(
    prompt="A landscape painting",
    model="imagen4",
    image_size="landscape_16_9",
    guidance_scale=5.0,
    num_inference_steps=6
)

# FLUX Dev with maximum quality settings
result = generator.generate_image(
    prompt="A detailed architectural drawing",
    model="flux_dev",
    num_inference_steps=50,
    guidance_scale=7.0,
    negative_prompt="sketch, rough, unfinished"
)
```

### Batch Processing

```python
prompts = [
    "A cat sitting on a windowsill",
    "A dog playing in a park", 
    "A bird flying in the sky"
]

results = []
for prompt in prompts:
    result = generator.generate_with_flux_schnell(prompt=prompt)
    if result['success']:
        local_path = generator.download_image(result['image_url'])
        results.append(local_path)
```

### Error Handling

```python
result = generator.generate_image(
    prompt="Your prompt here",
    model="flux_schnell"
)

if result['success']:
    print(f"✅ Success: {result['image_url']}")
    print(f"Size: {result['image_size']}")
    print(f"Model: {result['model']}")
else:
    print(f"❌ Failed: {result['error']}")
    print(f"Model: {result['model']}")
    print(f"Endpoint: {result['endpoint']}")
```

## 📁 Project Structure

```
fal_text_to_image/
├── fal_text_to_image_generator.py   # Main generator class
├── demo.py                          # Interactive demo with cost warnings
├── test_text_to_image.py           # Cost-conscious test suite
├── test_api_only.py                # FREE API connection test
├── requirements.txt                # Python dependencies
├── .env                           # Configuration file
├── .env.example                   # Example configuration
├── README.md                      # This documentation
├── output/                        # Generated images from demo
└── test_output/                   # Generated images from tests
```

## 🔐 Security Best Practices

1. **Never commit your `.env` file** - it contains your API key
2. **Use environment variables** in production
3. **Mask API keys** in logs (automatically done)
4. **Validate inputs** before sending to API
5. **Handle errors gracefully** to avoid exposing sensitive information

## 🐛 Troubleshooting

### Common Issues

#### "FAL_KEY not found"
```bash
# Check your .env file
cat .env

# Make sure it contains:
FAL_KEY=your_actual_api_key_here
```

#### "Failed to import fal_client"
```bash
# Install the FAL client
pip install fal-client

# Or install all dependencies
pip install -r requirements.txt
```

#### "Model validation failed"
```bash
# Test your setup first
python test_api_only.py

# Check supported models
python -c "from fal_text_to_image_generator import FALTextToImageGenerator; print(list(FALTextToImageGenerator.MODEL_ENDPOINTS.keys()))"
```

#### Generation fails with API errors
1. Check your API key is valid
2. Ensure you have sufficient credits
3. Try a different model
4. Reduce inference steps or image size

### Debugging Steps

1. **Run FREE tests first**:
   ```bash
   python test_api_only.py
   ```

2. **Test individual models**:
   ```bash
   python test_text_to_image.py --flux-schnell
   ```

3. **Check model information**:
   ```python
   from fal_text_to_image_generator import FALTextToImageGenerator
   generator = FALTextToImageGenerator()
   print(generator.get_model_info())
   ```

## 📈 Performance Tips

1. **Use FLUX Schnell for speed** - optimized for 1-4 inference steps
2. **Use appropriate image sizes** - larger sizes cost more and take longer
3. **Optimize prompts** - clear, specific prompts work better
4. **Use negative prompts** - for models that support them (Seedream, FLUX Dev)
5. **Batch similar requests** - reuse the generator instance
6. **Cache results** - download and store successful generations

## 🔄 Migration from Other Tools

### From OpenAI DALL-E
```python
# DALL-E style
# response = openai.Image.create(prompt="A cat", size="1024x1024")

# FAL AI equivalent
result = generator.generate_with_seedream(
    prompt="A cat",
    image_size="1024x1024"
)
```

### From Stability AI
```python
# Stability AI style  
# response = stability_api.generate(prompt="A landscape")

# FAL AI equivalent
result = generator.generate_with_flux_dev(
    prompt="A landscape",
    guidance_scale=7.0,
    negative_prompt="low quality"
)
```

## 📜 License & Credits

This module uses the FAL AI platform for image generation. Please ensure you comply with:
- [FAL AI Terms of Service](https://fal.ai/terms)
- [FAL AI Usage Policies](https://fal.ai/policies)
- Respect rate limits and fair usage

**Model Credits:**
- Imagen 4: Google DeepMind
- Seedream v3: ByteDance
- FLUX.1: Black Forest Labs

## 🤝 Contributing

Contributions are welcome! Please:
1. Test your changes with the FREE test suite
2. Update documentation for new features
3. Follow the cost-conscious testing patterns
4. Ensure backward compatibility

## 📞 Support

For issues with this module:
1. Run `python test_api_only.py` first
2. Check the troubleshooting section
3. Review FAL AI documentation
4. Open an issue with test results

For FAL AI platform issues:
- Visit [FAL AI Documentation](https://docs.fal.ai/)
- Contact [FAL AI Support](https://fal.ai/support)

---

**⚠️ Remember: Every image generation costs money. Always test with FREE tests first!** 