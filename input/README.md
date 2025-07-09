# Input Directory

This directory is for user input files, test data, and configurations that work across multiple packages in the AI Content Generation Suite.

## 📁 Purpose

- **Cross-package input files**: Files that multiple packages might use
- **Test data**: Sample images, videos, audio files for testing
- **Configuration files**: YAML/JSON configs for pipelines
- **User content**: Personal files for processing

## 🚫 Gitignore

This directory is added to `.gitignore` to prevent accidentally committing:
- Personal/sensitive files
- Large media files
- Temporary test data
- User-specific configurations

## 📋 Current Structure

This directory is now organized with all input files from across the monorepo:

```
input/
├── pipelines/        # YAML pipeline configurations (18 files)
├── images/           # Image files organized by type
│   ├── portraits/    # Character and people images (2 files)
│   ├── scenes/       # Scene and environment images (2 files)
│   ├── processed/    # Ready-to-use processed images (19 files)
│   ├── anime/        # Anime-style images
│   ├── horror/       # Horror-themed images (3 files)
│   └── flux_outputs/ # FLUX model generated images (4 files)
├── videos/           # Video files for processing (2 files)
├── audio/            # Audio files for testing (1 file)
├── text/             # Text content and descriptions (5 files)
├── prompts/          # Text prompts for AI generation (2 files)
├── metadata/         # JSON metadata and descriptions (3 files)
├── subtitles/        # Subtitle files (SRT, VTT) (2 files)
├── scripts/          # Processing utilities
└── examples/         # Example files and demos
```

## 💡 Usage Examples

### For AI Content Pipeline
```bash
# Use existing pipeline configurations
python -m ai_content_pipeline run-chain --config input/pipelines/tts_simple_test.yaml
python -m ai_content_pipeline run-chain --config input/pipelines/video_budget_hailuo.yaml

# Create your own pipeline config
input/pipelines/my_custom_pipeline.yaml
```

### For FAL AI Services
```bash
# Use existing test images
input/images/portraits/anime_girl.jpeg
input/images/scenes/lily_squid_game.png
input/videos/sample_video.mp4

# Use processed images ready for generation
input/images/processed/woman_with_blonde_hair_singing.jpeg
```

### For Text-to-Speech
```bash
# Use existing prompts
input/prompts/default_prompt.txt

# Add your own text files
input/text/my_speech_content.txt
```

### For Video Tools
```bash
# Use sample files for testing
input/videos/sample_video.mp4
input/subtitles/sample_video.srt
input/audio/sample-0.mp3
```

## ⚠️ Important Notes

- **Files in this directory are NOT tracked by git**
- **Don't put sensitive API keys or credentials here**
- **Large files (>100MB) should be stored elsewhere**
- **Consider using relative paths when referencing these files**

---

This input directory provides a convenient workspace for all your AI content generation needs across the entire monorepo!