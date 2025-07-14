# Input Directory File Index

This file provides a comprehensive index of all files consolidated from various package input directories into this centralized location.

## 📊 Summary Statistics

- **Total Files**: ~41 files consolidated
- **Pipeline Configurations**: 18 YAML files
- **Images**: 7 files across 3 categories
- **Videos**: 2 MP4 files
- **Audio**: 1 MP3 file
- **Text Files**: 5 TXT files
- **Prompts**: 2 prompt files
- **Metadata**: 3 JSON files
- **Subtitles**: 2 files (SRT, VTT)

## 📁 Detailed File Inventory

### `/pipelines/` - Pipeline Configurations (18 files)
**Text-to-Speech Pipelines:**
- `tts_simple_test.yaml` - Basic TTS test
- `tts_pipeline_test.yaml` - TTS pipeline testing
- `tts_single_voice_test.yaml` - Single voice testing
- `parallel_tts_test.yaml` - Parallel TTS processing
- `text_to_speech_test.yaml` - TTS functionality test

**Video Generation Pipelines:**
- `video_budget_hailuo.yaml` - Budget-friendly Hailuo model
- `video_budget_superwomen.yaml` - Budget superwomen theme
- `video_premium_complete.yaml` - Premium complete pipeline
- `video_smart_prompts_kling.yaml` - Smart prompts with Kling
- `video_documentary_realistic.yaml` - Documentary style
- `video_complete_with_subtitles.yaml` - Video with subtitles
- `video_subtitle_generation.yaml` - Subtitle generation
- `video_upscale_topaz.yaml` - Video upscaling with Topaz

**Analysis Pipelines:**
- `analysis_detailed_gemini.yaml` - Detailed Gemini analysis
- `analysis_ocr_direct.yaml` - Direct OCR analysis
- `analysis_ocr_extraction.yaml` - OCR text extraction

**Image Processing:**
- `image_artistic_transform.yaml` - Artistic image transformation

### `/images/` - Image Assets (7 files)

#### `/images/portraits/` (2 files)
- `anime_girl.jpeg` - Anime-style character portrait
- `death.jpeg` - Dark themed character image

#### `/images/scenes/` (2 files)  
- `horror_poster_strart_notext.jpg` - Horror scene without text
- `lily_squid_game.png` - Squid Game themed scene

#### `/images/horror/` (3 files)
- `horror_poster_starter.jpg` - Horror poster base
- `horror_poster_strart_notext.jpg` - Clean horror poster
- `woman_portrait.jpg` - Portrait for horror processing

#### Root images:
- `test_ocr_image.webp` - OCR testing image

> **Note**: Additional folders like `processed/` and `flux_outputs/` may exist locally for user workspace but are not tracked in git to keep the repository clean.

### `/videos/` - Video Files (2 files)
- `final_multitalk_6112.mp4` - Multi-speaker conversation video
- `sample_video.mp4` - General purpose test video

### `/audio/` - Audio Files (1 file)
- `sample-0.mp3` - Sample audio for testing

### `/text/` - Text Content (5 files)
- `sample-0_description.txt` - Audio description text
- `sample-0_transcription.txt` - Audio transcription
- `sample_video_description.txt` - Video description
- `test_input.txt` - General test input
- `test_text.txt` - Text processing test

### `/prompts/` - AI Prompts (2 files)
- `default_prompt.txt` - Default generation prompt
- `horror_poster_starter_nontext.txt` - Horror poster prompt

### `/metadata/` - JSON Metadata (3 files)
- `sample-0_description.json` - Audio metadata
- `sample-0_transcription.json` - Transcription metadata  
- `sample_video_description.json` - Video metadata

### `/subtitles/` - Subtitle Files (2 files)
- `sample_video.srt` - SRT format subtitles
- `sample_video.vtt` - WebVTT format subtitles

## 🔄 Migration Source

Files were consolidated from these original locations:
- `packages/core/ai-content-pipeline/input/`
- `packages/providers/fal/image-to-image/input/`
- `packages/providers/fal/image-to-video/input/`
- `packages/providers/fal/video-to-video/input/`
- `packages/services/video-tools/input/`
- `packages/services/text-to-speech/input/`

## 🎯 Usage Guidelines

1. **Pipeline Configs**: Reference in AI Content Pipeline commands
2. **Images**: Use as input for FAL AI image generation services
3. **Videos**: Test material for video processing tools
4. **Audio**: Sample files for audio analysis and TTS testing
5. **Text/Prompts**: Input for text-based AI generation
6. **Metadata**: Reference data for testing API responses
7. **Subtitles**: Testing subtitle generation and processing

---

This consolidated structure provides easy access to all test materials and configurations across the entire AI Content Generation Suite!