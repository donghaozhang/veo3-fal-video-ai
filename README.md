# AI Video Generation Project

This project provides comprehensive Python implementations for generating videos using multiple AI platforms and models. It's organized into specialized folders for different video generation services.

## 🎬 Available Implementations

### 1. Google Veo Video Generation (`veo3_video_generation/`)
- **Models**: Veo 2.0 (stable) and Veo 3.0 (preview)
- **Features**: Text-to-video, Image-to-video generation
- **Quality**: High-resolution, cinematic quality
- **Setup**: Requires Google Cloud authentication and configuration

### 2. FAL AI Dual-Model Generation (`fal_video_generation/`)
- **Models**: MiniMax Hailuo-02 and Kling Video 2.1
- **Features**: Production-ready API, dual model support, cost-conscious testing
- **Quality**: 768p (Hailuo) and high-quality (Kling)
- **Setup**: Simple API key authentication
- **⚠️ Cost Warning**: Video generation costs money (~$0.02-0.05 per video)

### 3. FAL AI Avatar Generation (`fal_avatar_generation/`)
- **Model**: AI Avatar Single-Text (MultiTalk)
- **Features**: Text-to-speech avatar videos with lip-sync
- **Quality**: Talking avatars with natural expressions
- **Voices**: 20 different voice options
- **Setup**: Simple API key authentication
- **⚠️ Cost Warning**: Avatar generation costs money (~$0.02-0.05 per video)

## 📁 Project Structure

```
veo3/
├── README.md                           # This overview
├── requirements.txt                    # Global dependencies
├── .env                               # Global environment variables
├── 
├── veo3_video_generation/             # Google Veo Implementation
│   ├── veo_video_generation.py        # Main Veo implementation
│   ├── demo.py                        # Interactive Veo demo
│   ├── test_veo.py                    # Comprehensive test suite
│   ├── README.md                      # Veo-specific documentation
│   ├── requirements.txt               # Veo dependencies
│   ├── .env                          # Veo configuration
│   ├── images/                       # Input images for testing
│   └── result_folder/                # Generated videos output
│
├── fal_video_generation/             # FAL AI Video Implementation
│   ├── fal_video_generator.py        # Dual-model FAL AI class
│   ├── demo.py                       # Cost-conscious interactive demo
│   ├── test_fal_ai.py               # Cost-conscious test suite
│   ├── test_api_only.py             # FREE API connection test
│   ├── README.md                     # FAL AI documentation
│   ├── COST_CONSCIOUS_TESTING.md    # Cost protection guide
│   ├── requirements.txt              # FAL AI dependencies
│   ├── .env                         # FAL AI configuration
│   ├── output/                      # Generated videos output
│   └── test_output/                 # Test videos output
│
├── fal_avatar_generation/           # FAL AI Avatar Implementation
│   ├── fal_avatar_generator.py      # Avatar video generator class
│   ├── demo.py                      # Cost-conscious interactive demo
│   ├── test_setup.py               # FREE environment tests
│   ├── test_generation.py          # PAID avatar generation tests
│   ├── README.md                    # Avatar generation documentation
│   ├── requirements.txt             # Avatar dependencies
│   ├── .env                        # Avatar configuration
│   ├── output/                     # Generated avatar videos
│   └── test_output/                # Test avatar videos
│
└── archive/                         # Historical implementations
```

## 🚀 Quick Start

### Option 1: Google Veo (High-Quality, Complex Setup)

```bash
cd veo3_video_generation
pip install -r requirements.txt

# Configure Google Cloud authentication
gcloud auth login
gcloud auth application-default login
gcloud config set project your-project-id

# Update configuration in .env file
# PROJECT_ID=your-project-id
# OUTPUT_BUCKET_PATH=gs://your-bucket/veo_output/

# Run demo
python demo.py

# Or run tests
python test_veo.py
```

### Option 2: FAL AI (Simple Setup, Production Ready)

```bash
cd fal_video_generation
pip install -r requirements.txt

# Configure API key in .env file
# FAL_KEY=your-fal-api-key

# Test setup first (FREE)
python test_api_only.py

# Run demo (costs money - has confirmation prompts)
python demo.py

# Or run specific model tests (costs money)
python test_fal_ai.py --hailuo    # ~$0.02-0.05
python test_fal_ai.py --kling     # ~$0.02-0.05
```

## 🔧 Setup Requirements

### Google Veo Requirements
- Google Cloud Project with Vertex AI API enabled
- Google Cloud Storage bucket
- Proper authentication (gcloud CLI)
- Python 3.8+
- Veo 3.0 requires allowlist approval

### FAL AI Requirements
- FAL AI API key (from fal.ai)
- Python 3.8+
- Internet connection

## 📊 Model Comparison

| Feature | Google Veo 2.0 | Google Veo 3.0 | FAL Hailuo-02 | FAL Kling 2.1 |
|---------|----------------|----------------|---------------|----------------|
| **Resolution** | High | Higher | 768p | High-quality |
| **Setup Complexity** | Complex | Complex | Simple | Simple |
| **Authentication** | Google Cloud | Google Cloud | API Key | API Key |
| **Access** | Generally Available | Preview/Allowlist | Public API | Public API |
| **Generation Time** | 2-10 min | 2-10 min | 1-3 min | 1-3 min |
| **Best For** | Cinematic quality | Latest features | Quick prototyping | High-quality production |

## 🎯 Use Cases

### Choose Google Veo When:
- You need the highest quality video generation
- You have Google Cloud infrastructure
- You're building enterprise applications
- Quality is more important than speed

### Choose FAL AI When:
- You want quick setup and testing
- You need reliable production API
- You want to compare multiple models
- You prefer simple API key authentication

## 🛠️ Development Features

### Google Veo Features
- ✅ Text-to-video generation
- ✅ Image-to-video generation
- ✅ Multiple model support (2.0 + 3.0)
- ✅ Local image processing
- ✅ Automatic GCS upload/download
- ✅ Comprehensive error handling
- ✅ Interactive demo with model selection
- ✅ Full test suite with comparison

### FAL AI Features
- ✅ Dual-model architecture (Hailuo + Kling)
- ✅ Universal methods with full endpoint names
- ✅ Model-specific optimization
- ✅ Cost-conscious interactive demo with confirmation prompts
- ✅ Cost-conscious testing framework with FREE options
- ✅ Production-ready error handling
- ✅ Automatic video download
- ✅ Model performance comparison
- ⚠️ Cost protection with explicit user confirmation required

## 📖 Documentation

Each implementation has its own detailed documentation:

- **Google Veo**: See [`veo3_video_generation/README.md`](veo3_video_generation/README.md)
- **FAL AI**: See [`fal_video_generation/README.md`](fal_video_generation/README.md)

## 🧪 Testing

### Test Google Veo Implementation
```bash
cd veo3_video_generation

# Basic tests
python test_veo.py

# Test Veo 3.0 specifically
python test_veo.py --veo3

# Compare both models
python test_veo.py --compare

# Full comprehensive tests
python test_veo.py --full
```

### Test FAL AI Implementation

⚠️ **Cost Warning**: Video generation tests cost money! Always start with FREE tests.

```bash
cd fal_video_generation

# FREE Tests (no cost)
python test_api_only.py              # API connection test only
python test_fal_ai.py                # Setup validation only

# Paid Tests (generate real videos)
python test_fal_ai.py --hailuo       # Test Hailuo model (~$0.02-0.05)
python test_fal_ai.py --kling        # Test Kling model (~$0.02-0.05)
python test_fal_ai.py --compare      # Test both models (~$0.04-0.10)
```

## 🎮 Interactive Demos

Both implementations include interactive demos:

```bash
# Google Veo Demo
cd veo3_video_generation && python demo.py

# FAL AI Demo (costs money - has confirmation prompts)
cd fal_video_generation && python demo.py
```

The demos provide:
- Model selection menus with cost warnings
- Pre-configured test prompts
- Image-to-video testing
- Model comparison features (expensive - generates 2 videos)
- Configuration validation
- **Cost protection**: Confirmation prompts before generating videos

## 🔍 Troubleshooting

### Common Issues

#### Google Veo Issues
- **"Project not allowlisted"**: Use Veo 2.0 or request Veo 3.0 access
- **Permission denied**: Check GCS bucket permissions
- **Authentication failed**: Run `gcloud auth application-default login`

#### FAL AI Issues
- **Invalid API key**: Check your FAL_KEY in .env file
- **Rate limiting**: Wait between requests or upgrade plan
- **Model not available**: Try alternative model
- **Unexpected charges**: Always use FREE tests first (`test_api_only.py`)

### Getting Help

1. Check the specific README for your implementation
2. Review the test suite output for diagnostic information
3. Run the demo to validate your setup
4. Check the troubleshooting sections in each implementation's README

## ⚠️ Cost Protection

**IMPORTANT**: FAL AI video generation costs money (~$0.02-0.05 per video). This project includes cost protection measures:

- **FREE tests available**: Use `test_api_only.py` for setup validation
- **Cost warnings**: All paid operations show cost estimates
- **Confirmation prompts**: User must explicitly confirm before generating videos
- **Model-specific testing**: Test individual models to avoid unnecessary costs

**Always start with FREE tests before running paid video generation!**

## 🚧 Development Status

- ✅ **Google Veo**: Production ready with comprehensive testing
- ✅ **FAL AI**: Production ready with cost-conscious dual-model support
- 🔄 **Future**: Additional model integrations planned

## 📝 License

This project is open source. Please check individual implementation folders for specific licensing information.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📚 Resources

### Google Veo Resources
- [Veo API Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation)
- [Google GenAI SDK](https://github.com/google/generative-ai-python)
- [Vertex AI Console](https://console.cloud.google.com/vertex-ai)

### FAL AI Resources
- [FAL AI Platform](https://fal.ai/)
- [MiniMax Hailuo Documentation](https://fal.ai/models/fal-ai/minimax-video-01)
- [Kling Video 2.1 Documentation](https://fal.ai/models/fal-ai/kling-video/v2.1/standard/image-to-video/api)

---

**🎬 Happy Video Generating!** Choose the implementation that best fits your needs and start creating amazing AI-generated videos. 