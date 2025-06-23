# 🖱️ Cursor MCP Testing Guide

Since you don't have Claude Desktop, here are the best ways to test the FAL AI Text-to-Image MCP functionality with Cursor:

## ✅ Updated for Cursor Compatibility

I've updated `test_mcp_server.py` to include Cursor-specific testing and created `test_cursor_mcp.py` for direct tool testing.

## 🧪 Testing Options (Recommended Order)

### 1️⃣ **Basic Validation** (Start Here)
```bash
python test_mcp_server.py
```
- ✅ **100% FREE** - No image generation
- ✅ Tests all MCP components 
- ✅ Includes Cursor compatibility check
- ✅ Validates setup without costs

### 2️⃣ **Interactive Demo** (Best User Experience)
```bash
python demo.py
```
- ✅ Full interactive interface
- ✅ Cost confirmations built-in
- ✅ Easy to use for actual generation
- ✅ Multiple model support with comparison

### 3️⃣ **Direct MCP Tool Testing**
```bash
python test_cursor_mcp.py
```
- ✅ Tests MCP tools directly
- ✅ Simulates what Cursor would do with MCP
- ✅ Safe with cost controls
- ✅ Shows tool arguments and responses

### 4️⃣ **Command Line Testing**
```bash
# FREE API test
python test_api_only.py

# Specific model testing (costs money)
python test_text_to_image.py --imagen4
python test_text_to_image.py --flux-schnell
```

### 5️⃣ **Direct Python Usage** (For Integration)
```python
from fal_text_to_image_generator import FALTextToImageGenerator

generator = FALTextToImageGenerator()
result = generator.generate_image(
    prompt="A beautiful landscape", 
    model="imagen4"
)
```

## 🎯 Quick Start for Cursor Users

1. **Validate Setup**: `python test_mcp_server.py`
2. **Try Interactive Demo**: `python demo.py`
3. **Use Direct Python** for actual work

## 🛠️ Available Models

- **Imagen4**: Photorealistic images, portraits
- **Seedream**: Artistic and creative content  
- **FLUX Schnell**: Ultra-fast generation (1-2 seconds)
- **FLUX Dev**: Balanced quality and speed

## 💰 Cost Information

- **All Tests**: Most tests are FREE
- **Image Generation**: ~$0.015 per image
- **Batch Generation**: ~$0.015 × number of models
- **Cost Confirmations**: Built into all tools

## 🔧 Troubleshooting

If you encounter issues:

1. **Check API Key**: Ensure `FAL_KEY` is set in `.env`
2. **Dependencies**: Run `pip install -r requirements.txt`
3. **FREE Test**: Run `python test_api_only.py` first
4. **Imports**: Make sure you're in the `fal_text_to_image` directory

## 📋 What Each Test Does

| Test File | Purpose | Cost | When to Use |
|-----------|---------|------|-------------|
| `test_mcp_server.py` | Validate MCP setup | FREE | First run, troubleshooting |
| `test_cursor_mcp.py` | Test MCP tools directly | FREE* | Test tool functionality |
| `test_api_only.py` | API connection only | FREE | Validate API setup |
| `demo.py` | Interactive generation | PAID | Actual image generation |
| `test_text_to_image.py` | Full system test | PAID | Complete validation |

*Free except when actually generating images

## 🎉 All Set!

Your FAL AI Text-to-Image MCP system is now **Cursor-ready** with multiple testing options! 