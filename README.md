# AI Content Pipeline

🚀 **Production-ready AI content generation with 28+ models, parallel execution, and unified CLI.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/video-ai-studio)](https://pypi.org/project/video-ai-studio/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/donghaozhang/veo3-fal-video-ai/actions/workflows/test.yml/badge.svg)](https://github.com/donghaozhang/veo3-fal-video-ai/actions)

```bash
pip install video-ai-studio
```

## 🎬 **Demo Video**

[![AI Content Generation Suite Demo](https://img.youtube.com/vi/xzvPrlKnXqk/maxresdefault.jpg)](https://www.youtube.com/watch?v=xzvPrlKnXqk)

*Click to watch the complete demo of AI Content Generation Suite in action*

## 🎨 Available AI Models

### Text-to-Image Models
| Model Name | Provider | Cost per Image | Resolution | Special Features |
|------------|----------|----------------|------------|------------------|
| `flux_dev` | FAL AI | $0.003 | 1024x1024 | High quality, FLUX.1 Dev |
| `flux_schnell` | FAL AI | $0.001 | 1024x1024 | Fast generation, FLUX.1 Schnell |
| `imagen4` | FAL AI | $0.004 | 1024x1024 | Google Imagen 4, photorealistic |
| `seedream_v3` | FAL AI | $0.002 | 1024x1024 | Seedream v3, bilingual support |
| `seedream3` | Replicate | $0.003 | Up to 2048px | ByteDance Seedream-3, high-res |
| `gen4` | Replicate | $0.08 | 720p/1080p | **Runway Gen-4, multi-reference guidance** |

### Image-to-Image Models  
| Model Name | Provider | Cost per Image | Special Features |
|------------|----------|----------------|------------------|
| `photon_flash` | FAL AI | $0.02 | Luma Photon Flash, creative & fast |
| `photon_base` | FAL AI | $0.03 | Luma Photon Base, high quality |
| `flux_kontext` | FAL AI | $0.025 | FLUX Kontext Dev, contextual editing |
| `flux_kontext_multi` | FAL AI | $0.04 | FLUX Kontext Multi, multi-image |
| `seededit_v3` | FAL AI | $0.02 | ByteDance SeedEdit v3, precise editing |
| `clarity_upscaler` | FAL AI | $0.05 | Clarity AI upscaler |

### Image-to-Video Models
| Model Name | Provider | Cost per Video | Resolution | Special Features |
|------------|----------|----------------|------------|------------------|
| `veo3` | FAL AI | $3.00 | Up to 1080p | Google Veo 3.0, latest model |
| `veo3_fast` | FAL AI | $2.00 | Up to 1080p | Google Veo 3.0 Fast |
| `veo2` | FAL AI | $2.50 | Up to 1080p | Google Veo 2.0 |
| `hailuo` | FAL AI | $0.08 | 720p | MiniMax Hailuo-02, budget-friendly |
| `kling` | FAL AI | $0.10 | 720p | Kling Video 2.1 |

### Image Understanding Models
| Model Name | Provider | Cost per Analysis | Special Features |
|------------|----------|-------------------|------------------|
| `gemini_describe` | Google | $0.001 | Basic image description |
| `gemini_detailed` | Google | $0.002 | Detailed image analysis |
| `gemini_classify` | Google | $0.001 | Image classification |
| `gemini_objects` | Google | $0.002 | Object detection |
| `gemini_ocr` | Google | $0.001 | Text extraction (OCR) |
| `gemini_composition` | Google | $0.002 | Artistic & technical analysis |
| `gemini_qa` | Google | $0.001 | Question & answer system |

### Text-to-Speech Models
| Model Name | Provider | Cost per Request | Special Features |
|------------|----------|------------------|------------------|
| `elevenlabs` | ElevenLabs | $0.05 | High quality TTS |
| `elevenlabs_turbo` | ElevenLabs | $0.03 | Fast generation |
| `elevenlabs_v3` | ElevenLabs | $0.08 | Latest v3 model |

### Prompt Generation Models
| Model Name | Provider | Cost per Request | Special Features |
|------------|----------|------------------|------------------|
| `openrouter_video_prompt` | OpenRouter | $0.002 | General video prompts |
| `openrouter_video_cinematic` | OpenRouter | $0.002 | Cinematic style prompts |
| `openrouter_video_realistic` | OpenRouter | $0.002 | Realistic style prompts |
| `openrouter_video_artistic` | OpenRouter | $0.002 | Artistic style prompts |
| `openrouter_video_dramatic` | OpenRouter | $0.002 | Dramatic style prompts |

### Audio & Video Processing
| Model Name | Provider | Cost per Request | Special Features |
|------------|----------|------------------|------------------|
| `thinksound` | FAL AI | $0.05 | AI audio generation |
| `topaz` | FAL AI | $1.50 | Video upscaling |

### 🌟 **Featured Model: Runway Gen-4**
The **`gen4`** model is our most advanced text-to-image model, offering unique capabilities:
- **Multi-Reference Guidance**: Use up to 3 reference images with tagging
- **Cinematic Quality**: Premium model for high-end generation  
- **@ Syntax**: Reference tagged elements in prompts (`@woman`, `@park`)
- **Variable Pricing**: $0.05 (720p) / $0.08 (1080p)

**Total Models: 35+ AI models across 7 categories**

## ✨ Features

- **🎯 28+ AI Models** - Text-to-image, image-to-video, TTS, image understanding
- **⚡ Parallel Execution** - 2-3x speedup with thread-based processing  
- **📋 YAML Pipelines** - Multi-step workflows with cost estimation
- **🔧 Unified CLI** - `ai-content-pipeline` and `aicp` commands
- **🧪 Mock Mode** - Full testing without API keys
- **💰 Cost Tracking** - Built-in estimation for all models

## 🚀 Quick Start

```bash
# Install
pip install video-ai-studio

# List models (works without API keys)
ai-content-pipeline list-models

# Generate image (requires FAL_KEY)
ai-content-pipeline generate-image --text "epic space battle" --model flux_dev

# Create video pipeline
ai-content-pipeline create-video --text "serene mountain lake"
```

### 🔑 API Keys (Optional)
Create `.env` file for API access:
```env
FAL_KEY=your_fal_api_key          # fal.ai/dashboard
GEMINI_API_KEY=your_gemini_key    # makersuite.google.com
ELEVENLABS_API_KEY=your_elevenlabs_key
OPENROUTER_API_KEY=your_openrouter_key
```

> **💡 Mock Mode:** All features work without API keys for testing!

## 📋 YAML Pipelines

Create complex workflows with YAML:
```yaml
name: "Text to Video Pipeline"
steps:
  - type: "text_to_image"
    model: "flux_dev"
    params:
      prompt: "{{input}}"
      
  - type: "image_to_video"
    model: "veo3"
    params:
      input_from: "step_1"
      duration: 6
```

```bash
ai-content-pipeline run-chain --config pipeline.yaml --input "epic battle"
```

## 🧪 Testing & Development

```bash
# Run tests (works without API keys)
python tests/test_core.py

# Development mode
pip install -e .
```

## 📚 Documentation

- **[CLAUDE.md](CLAUDE.md)** - Full development guide  
- **[Model Pricing](https://github.com/donghaozhang/veo3-fal-video-ai)** - Cost details for all models

---

**Built with ❤️ for AI content creators** • [Issues](https://github.com/donghaozhang/veo3-fal-video-ai/issues) • [PyPI](https://pypi.org/project/video-ai-studio/)
