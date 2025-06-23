# FAL AI Text-to-Image MCP Server

A Model Context Protocol (MCP) server that provides Claude and other AI assistants with access to FAL AI text-to-image generation capabilities.

## Features

### 🎨 Multi-Model Support
- **Imagen4**: Google's high-quality model with excellent realism
- **Seedream**: Artistic and creative generation with unique style
- **FLUX Schnell**: Ultra-fast generation (1-2 seconds)
- **FLUX Dev**: Balanced speed and quality

### 💰 Cost-Conscious Design
- Built-in cost warnings for all operations
- Cost estimation before generation
- Confirmation prompts (configurable)
- Clear cost breakdown in responses

### 🚀 Advanced Capabilities
- Single image generation with any model
- Batch generation with multiple models
- Model information and specifications
- Image download and local storage
- Resource management for generated images
- Rich response formatting with metadata

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The requirements include:
- **Core FAL AI**: `fal-client`, `python-dotenv`, `requests`
- **MCP Server**: `mcp>=1.0.0`, `httpx>=0.25.0`

### 2. Environment Setup

Create or update your `.env` file:

```bash
# FAL AI API Configuration
FAL_KEY=your_fal_api_key_here

# Optional: Additional configuration
FAL_TIMEOUT=300
FAL_MAX_RETRIES=3
```

### 3. Test the Server

```bash
# Test the MCP server directly
python mcp_server.py

# Or test the underlying generator first
python test_api_only.py  # FREE test
```

## MCP Client Configuration

### Claude Desktop Configuration

Add this to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fal-text-to-image": {
      "command": "python",
      "args": ["D:/AI_play/AI_Code/veo3/fal_text_to_image/mcp_server.py"],
      "cwd": "D:/AI_play/AI_Code/veo3/fal_text_to_image",
      "env": {
        "FAL_KEY": "your_fal_api_key_here"
      }
    }
  }
}
```

### Generic MCP Client Configuration

Use the provided `mcp_config.json`:

```json
{
  "mcpServers": {
    "fal-text-to-image": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": ".",
      "env": {
        "FAL_KEY": "your_fal_api_key_here"
      }
    }
  }
}
```

## Available MCP Tools

### 1. `generate_image`

Generate a single image using FAL AI with the specified model.

**Parameters:**
- `prompt` (required): Text prompt describing the image to generate
- `model` (optional): Model to use (`imagen4`, `seedream`, `flux_schnell`, `flux_dev`)
- `negative_prompt` (optional): Negative prompt to avoid certain elements
- `output_folder` (optional): Folder to save the generated image
- `confirm_cost` (optional): Whether to show cost confirmation

**Example:**
```json
{
  "prompt": "A serene mountain landscape at sunset",
  "model": "imagen4",
  "negative_prompt": "blur, distortion, low quality"
}
```

### 2. `batch_generate_images`

Generate images with multiple models for comparison.

**Parameters:**
- `prompt` (required): Text prompt describing the image to generate
- `models` (optional): List of models to use (default: `["imagen4", "flux_dev"]`)
- `negative_prompt` (optional): Negative prompt to avoid certain elements
- `output_folder` (optional): Folder to save the generated images
- `confirm_cost` (optional): Whether to show cost confirmation

**Example:**
```json
{
  "prompt": "A futuristic cityscape with flying cars",
  "models": ["imagen4", "flux_dev", "flux_schnell"],
  "negative_prompt": "blur, artifacts"
}
```

### 3. `list_models`

List all available text-to-image models with their specifications.

**Parameters:** None

### 4. `get_model_info`

Get detailed information about a specific model.

**Parameters:**
- `model` (required): Model to get information about

### 5. `download_image`

Download a generated image from URL to local storage.

**Parameters:**
- `image_url` (required): URL of the image to download
- `output_folder` (optional): Folder to save the downloaded image
- `filename` (optional): Custom filename (with extension)

## Cost Management

### Cost Estimation
- **Single Generation**: ~$0.015 per image
- **Batch Generation**: ~$0.015 × number of models
- **Comparison (4 models)**: ~$0.060 (EXPENSIVE!)

### Cost Protection Features
1. **Upfront Warnings**: Cost estimates before generation
2. **Confirmation Prompts**: Optional confirmation for cost awareness
3. **Clear Breakdown**: Detailed cost information in responses
4. **Model Selection**: Choose appropriate models to manage costs

### Best Practices
- Use **FLUX Schnell** for fast iterations and testing
- Use **Imagen4** for high-quality final results
- Use **batch generation** wisely - costs multiply by model count
- Set `confirm_cost: false` only for automated workflows
- Monitor total costs when using batch operations

## Usage Examples

### Basic Image Generation
```python
# Via MCP client (e.g., Claude)
generate_image(
    prompt="A beautiful sunset over mountains",
    model="imagen4"
)
```

### Creative Comparison
```python
# Compare artistic vs photorealistic styles
batch_generate_images(
    prompt="A magical forest with glowing mushrooms",
    models=["imagen4", "seedream"],
    negative_prompt="blur, low quality"
)
```

### Fast Iteration
```python
# Quick concept testing
generate_image(
    prompt="Logo design for tech startup",
    model="flux_schnell",
    confirm_cost=False  # Skip confirmation for rapid iteration
)
```

## Troubleshooting

### Common Issues

**1. MCP Server Won't Start**
- Check Python version (3.8+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check FAL_KEY environment variable

**2. API Key Errors**
- Verify FAL_KEY is correctly set in environment
- Test with free API test: `python test_api_only.py`
- Check FAL AI account balance

**3. Generation Timeouts**
- Increase FAL_TIMEOUT in environment
- Check network connectivity
- Try different model (FLUX Schnell is fastest)

### Testing

**Free API Tests:**
```bash
python test_api_only.py  # No cost - tests API connection only
```

**Paid Generation Tests:**
```bash
python test_text_to_image.py --imagen4    # ~$0.015
python test_text_to_image.py --batch 1,3  # ~$0.030
```

Remember: **Every image generation costs real money. Test responsibly!**
