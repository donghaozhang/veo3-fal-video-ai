# YAML Configuration Guide

This document provides a complete reference for configuring AI Content Pipeline workflows using YAML files.

## 📋 Basic Structure

Every pipeline configuration follows this basic structure:

```yaml
name: "pipeline_identifier"
description: "Human-readable description"
prompt: "Main input text or description"

steps:
  - type: "step_type"
    model: "model_name"
    params:
      key: value
    enabled: true

output_dir: "output"
temp_dir: "temp"
cleanup_temp: true
save_intermediates: true
```

## 🔧 Configuration Fields

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✅ | Unique identifier for the pipeline |
| `description` | string | ❌ | Human-readable description |
| `prompt` | string | ✅ | Main input text for the pipeline |
| `steps` | array | ✅ | List of processing steps |
| `output_dir` | string | ❌ | Output directory (default: "output") |
| `temp_dir` | string | ❌ | Temporary files directory (default: "temp") |
| `cleanup_temp` | boolean | ❌ | Clean temporary files after execution |
| `save_intermediates` | boolean | ❌ | Save intermediate step results |

### Step Configuration

Each step in the `steps` array has these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Step type (see [Step Types](#step-types)) |
| `model` | string | ✅ | Model/service to use |
| `params` | object | ❌ | Step-specific parameters |
| `enabled` | boolean | ❌ | Whether to execute this step (default: true) |

## 🎯 Step Types

### Text-to-Speech (`text_to_speech`)

Convert text to audio using voice synthesis.

**Models:** `elevenlabs`, `elevenlabs_turbo`, `elevenlabs_v3`

```yaml
- type: "text_to_speech"
  model: "elevenlabs"
  params:
    voice: "rachel"              # Voice to use
    speed: 1.0                   # Speech speed (0.25-4.0)
    stability: 0.5               # Voice stability (0.0-1.0)
    similarity_boost: 0.8        # Voice similarity (0.0-1.0)
    style: 0.2                   # Style exaggeration (0.0-1.0)
    output_file: "audio.mp3"     # Output filename
```

**Available Voices:**
- `rachel`, `drew`, `bella`, `antoni`, `elli`
- `josh`, `arnold`, `adam`, `sam`, `clyde`

### Text-to-Image (`text_to_image`)

Generate images from text descriptions.

**Models:** `imagen4`, `flux`, `seedream`

```yaml
- type: "text_to_image"
  model: "imagen4"
  params:
    aspect_ratio: "16:9"         # Image aspect ratio
    style: "photorealistic"      # Image style
    quality: "high"              # Generation quality
    output_file: "image.png"     # Output filename
```

**Aspect Ratios:**
- `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9`, `9:21`

### Image Understanding (`image_understanding`)

Analyze and describe images.

**Models:** `gemini`, `openrouter`

```yaml
- type: "image_understanding"
  model: "gemini"
  params:
    analysis_type: "detailed"    # Analysis depth
    focus_areas: ["objects", "scene", "text"]  # What to analyze
```

### Prompt Generation (`prompt_generation`)

Generate optimized prompts for other AI models.

**Models:** `openrouter_video_realistic`, `openrouter_image_creative`

```yaml
- type: "prompt_generation"
  model: "openrouter_video_realistic"
  params:
    background_context: "documentary style"
    video_style: "realistic"
    duration_preference: "medium"
```

### Image-to-Image (`image_to_image`)

Modify or transform existing images.

**Models:** `luma_photon`

```yaml
- type: "image_to_image"
  model: "luma_photon"
  params:
    strength: 0.8                # Modification strength (0.0-1.0)
    aspect_ratio: "16:9"         # Output aspect ratio
    input_image: "input.jpg"     # Input image path
```

### Parallel Group (`parallel_group`)

Execute multiple steps simultaneously.

**Model:** `parallel` (dummy model name)

```yaml
- type: "parallel_group"
  model: "parallel"
  params:
    max_workers: 3               # Maximum concurrent executions
    merge_strategy: "collect_all" # How to combine results
    parallel_steps:              # Steps to run in parallel
      - type: "text_to_speech"
        model: "elevenlabs"
        params: {voice: "rachel"}
      - type: "text_to_speech"
        model: "elevenlabs"
        params: {voice: "drew"}
```

**Merge Strategies:**
- `collect_all` - Return all results as a collection
- `first_success` - Return the first successful result
- `best_quality` - Return the highest quality result (future)

## 📝 Complete Examples

### Simple Text-to-Speech
```yaml
name: "simple_tts"
description: "Basic text-to-speech conversion"
prompt: "Hello, welcome to our AI platform!"

steps:
  - type: "text_to_speech"
    model: "elevenlabs"
    params:
      voice: "rachel"
      speed: 1.0
      stability: 0.5
      similarity_boost: 0.8
      style: 0.2
      output_file: "welcome_message.mp3"

output_dir: "output"
save_intermediates: true
```

### Multi-Voice Parallel Generation
```yaml
name: "multi_voice_parallel"
description: "Generate multiple voice versions simultaneously"
prompt: "This message will be generated in multiple voices for comparison."

steps:
  - type: "parallel_group"
    model: "parallel"
    params:
      max_workers: 3
      merge_strategy: "collect_all"
      parallel_steps:
        - type: "text_to_speech"
          model: "elevenlabs"
          params:
            voice: "rachel"
            speed: 1.0
            output_file: "version_rachel.mp3"
        
        - type: "text_to_speech"
          model: "elevenlabs"
          params:
            voice: "drew"
            speed: 1.1
            stability: 0.7
            output_file: "version_drew.mp3"
        
        - type: "text_to_speech"
          model: "elevenlabs"
          params:
            voice: "bella"
            speed: 0.9
            style: 0.8
            output_file: "version_bella.mp3"

output_dir: "output"
cleanup_temp: true
save_intermediates: true
```

### Image Generation and Analysis
```yaml
name: "image_creation_analysis"
description: "Generate image then analyze it"
prompt: "A futuristic cityscape at sunset with flying cars"

steps:
  - type: "text_to_image"
    model: "imagen4"
    params:
      aspect_ratio: "16:9"
      style: "photorealistic"
      quality: "high"
      output_file: "cityscape.png"
  
  - type: "image_understanding"
    model: "gemini"
    params:
      analysis_type: "detailed"
      focus_areas: ["architecture", "lighting", "vehicles"]

output_dir: "output"
```

### Multi-Model Image Comparison
```yaml
name: "image_model_comparison"
description: "Generate same image with different models for comparison"
prompt: "A serene mountain lake reflecting snow-capped peaks"

steps:
  - type: "parallel_group"
    model: "parallel"
    params:
      max_workers: 3
      merge_strategy: "collect_all"
      parallel_steps:
        - type: "text_to_image"
          model: "imagen4"
          params:
            aspect_ratio: "16:9"
            output_file: "lake_imagen4.png"
        
        - type: "text_to_image"
          model: "flux"
          params:
            aspect_ratio: "16:9"
            output_file: "lake_flux.png"
        
        - type: "text_to_image"
          model: "seedream"
          params:
            aspect_ratio: "16:9"
            output_file: "lake_seedream.png"

output_dir: "comparison_results"
save_intermediates: true
```

## 🔧 Advanced Configuration

### Environment Variables in YAML

You can reference environment variables in YAML using the `${VAR_NAME}` syntax:

```yaml
name: "dynamic_config"
prompt: "${CUSTOM_PROMPT}"

steps:
  - type: "text_to_speech"
    model: "elevenlabs"
    params:
      voice: "${PREFERRED_VOICE}"
      output_file: "${OUTPUT_FILENAME}.mp3"
```

### Conditional Steps

Disable steps conditionally:

```yaml
steps:
  - type: "text_to_speech"
    model: "elevenlabs"
    enabled: true                # Always enabled
    params:
      voice: "rachel"
  
  - type: "text_to_speech"
    model: "elevenlabs"
    enabled: false               # Disabled (skip this step)
    params:
      voice: "drew"
```

### Step Dependencies

For complex workflows, you can reference outputs from previous steps:

```yaml
steps:
  - type: "prompt_generation"
    model: "openrouter_video_realistic"
    params:
      style: "documentary"
  
  - type: "text_to_image"
    model: "imagen4"
    # This step will use the enhanced prompt from the previous step
    params:
      aspect_ratio: "16:9"
```

## ⚠️ Common Pitfalls

### YAML Syntax Issues

❌ **Incorrect indentation:**
```yaml
steps:
- type: "text_to_speech"
model: "elevenlabs"  # Wrong indentation
```

✅ **Correct indentation:**
```yaml
steps:
  - type: "text_to_speech"
    model: "elevenlabs"  # Proper indentation
```

❌ **Missing quotes for special characters:**
```yaml
prompt: This won't work: colons cause issues
```

✅ **Proper quoting:**
```yaml
prompt: "This works: colons are safe in quotes"
```

### Configuration Errors

❌ **Invalid step type:**
```yaml
- type: "speech_to_text"  # Not supported
```

✅ **Valid step type:**
```yaml
- type: "text_to_speech"  # Supported
```

❌ **Missing required fields:**
```yaml
- type: "text_to_speech"
  # Missing model field
```

✅ **All required fields:**
```yaml
- type: "text_to_speech"
  model: "elevenlabs"
```

## 🧪 Testing Your Configuration

### Validation
The pipeline automatically validates your configuration. Common validation errors:

- Missing required fields
- Invalid step types
- Incompatible input/output types between steps
- Invalid parameter values

### Dry Run
Test your configuration without executing:

```bash
python -m ai_content_pipeline run-chain --config your_config.yaml --debug
```

### Cost Estimation
Check estimated costs before running:

```bash
python -m ai_content_pipeline run-chain --config your_config.yaml
# Review the cost estimate before confirming
```

## 📊 Performance Optimization

### Parallel Execution Guidelines

1. **Use parallel groups** for independent tasks
2. **Limit max_workers** to avoid rate limits (typically 2-4)
3. **Group similar operations** (e.g., multiple TTS with same model)
4. **Consider API costs** when running parallel operations

### Resource Management

```yaml
# Efficient parallel configuration
- type: "parallel_group"
  model: "parallel"
  params:
    max_workers: 3              # Don't exceed API limits
    merge_strategy: "collect_all"
    parallel_steps:
      # Group similar operations for better resource usage
      - type: "text_to_speech"
        model: "elevenlabs"
        params: {voice: "rachel"}
      - type: "text_to_speech"
        model: "elevenlabs"
        params: {voice: "drew"}
```

## 🔍 Debugging Configuration

### Enable Debug Mode
```bash
python -m ai_content_pipeline run-chain --config config.yaml --debug
```

### Check Execution Reports
All executions generate detailed reports in `output/reports/`:
- `*_exec_*.json` - Full execution report
- `*_intermediate_*.json` - Step-by-step results

### Common Debug Information
- Step validation results
- Input/output type checking
- Parameter validation
- Cost calculations
- Execution timing

---

*For more advanced usage patterns, see [PARALLEL_WORKFLOWS.md](PARALLEL_WORKFLOWS.md) and [API_REFERENCE.md](API_REFERENCE.md).*