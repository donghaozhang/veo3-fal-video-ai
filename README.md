# AI Content Generation Suite

A comprehensive monorepo containing multiple AI content generation packages.

## 📦 Packages

### Core Packages
- **[ai-content-platform](packages/core/ai-content-platform/)** - Main platform with CLI
- **[ai-content-pipeline](packages/core/ai-content-pipeline/)** - Legacy pipeline implementation

### Provider Packages

#### Google Services
- **[google-veo](packages/providers/google/veo/)** - Google Veo video generation

#### FAL AI Services  
- **[fal-video](packages/providers/fal/video/)** - Video generation
- **[fal-text-to-video](packages/providers/fal/text-to-video/)** - Text-to-video
- **[fal-avatar](packages/providers/fal/avatar/)** - Avatar generation
- **[fal-text-to-image](packages/providers/fal/text-to-image/)** - Text-to-image
- **[fal-image-to-image](packages/providers/fal/image-to-image/)** - Image transformation
- **[fal-video-to-video](packages/providers/fal/video-to-video/)** - Video processing

### Service Packages
- **[text-to-speech](packages/services/text-to-speech/)** - TTS services
- **[video-tools](packages/services/video-tools/)** - Video processing utilities

## 🚀 Quick Start

```bash
# Install all packages in development mode
make install-dev

# Run tests for all packages
make test-all

# Build all packages
make build-all
```

## 📚 Documentation

See [shared/docs/](shared/docs/) for comprehensive documentation.
