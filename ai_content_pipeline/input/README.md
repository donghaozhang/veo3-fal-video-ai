# AI Content Pipeline Workflows

This directory contains 8 organized workflow templates for the AI content pipeline.

## Video Generation Workflows

### `video_budget_hailuo.yaml`
- **Purpose**: Budget-friendly video generation using Hailuo model
- **Cost**: ~$0.08 per video
- **Features**: Fast, cost-effective video creation
- **Best for**: Testing, prototyping, high-volume generation

### `video_documentary_realistic.yaml`
- **Purpose**: Documentary-style realistic video creation
- **Models**: Imagen 4 (photorealistic) + Hailuo (subtle motion)
- **Features**: Natural movements, authentic feel
- **Best for**: Documentary content, realistic scenes

### `video_smart_prompts_kling.yaml`
- **Purpose**: Enhanced video with AI-optimized prompts using Kling
- **Features**: AI prompt enhancement, high-quality Kling model
- **Best for**: Creative content with optimized prompts

### `video_premium_complete.yaml`
- **Purpose**: Full premium pipeline with advanced features
- **Models**: Premium models with analysis and audio support
- **Features**: Complete production pipeline
- **Best for**: High-quality commercial content

## Image Processing Workflows

### `image_artistic_transform.yaml`
- **Purpose**: Multi-step artistic image transformations
- **Features**: Text→Image→Oil painting→Lighting effects
- **Models**: FLUX Dev, Photon Base, SeedEdit v3
- **Best for**: Artistic image creation with multiple styles

### `image_enhance_to_video.yaml`
- **Purpose**: Image enhancement followed by video conversion
- **Features**: Enhancement + video generation pipeline
- **Best for**: Creating videos from enhanced static images

## Analysis Workflows

### `analysis_detailed_gemini.yaml`
- **Purpose**: Comprehensive image analysis with Gemini
- **Features**: Detailed image understanding and description
- **Best for**: Content analysis, metadata generation

### `analysis_ocr_extraction.yaml`
- **Purpose**: Text extraction from generated images
- **Features**: OCR analysis of visual content
- **Best for**: Document processing, text extraction

## Usage

```bash
cd ai_content_pipeline

# Run any workflow:
python -m ai_content_pipeline run-chain --config input/video_budget_hailuo.yaml --input-text "Your prompt here" --no-confirm

# With custom input file:
python -m ai_content_pipeline run-chain --config input/video_documentary_realistic.yaml --prompt-file my_prompt.txt --no-confirm
```

## Notes

- All workflows have `save_intermediates: true` by default
- Intermediate results are saved even if pipelines are interrupted
- Reports are saved in `output/reports/` directory
- Generated content is saved in `output/` directory