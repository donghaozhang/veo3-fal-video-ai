# Getting Started with AI Content Pipeline

This guide will help you get up and running with the AI Content Pipeline quickly.

## 🏗️ Prerequisites

1. **Python Environment**: Python 3.8+ with virtual environment
2. **API Keys**: Valid API keys for the services you want to use
3. **Dependencies**: All required packages installed

## 🚀 Quick Setup

### 1. Activate Virtual Environment
```bash
cd /home/zdhpe/veo3-video-generation
source venv/bin/activate
```

### 2. Navigate to Pipeline Directory
```bash
cd ai_content_pipeline
```

### 3. Set Up Environment Variables
```bash
# For ElevenLabs TTS
export ELEVENLABS_API_KEY="your_elevenlabs_api_key"

# For FAL AI services
export FAL_KEY="your_fal_api_key"

# Enable parallel execution (optional)
export PIPELINE_PARALLEL_ENABLED=true
```

## 📝 Your First Pipeline

### Simple Text-to-Speech
Create a file `my_first_pipeline.yaml`:

```yaml
name: "my_first_tts"
description: "Convert text to speech"
prompt: "Hello! This is my first AI content pipeline."

steps:
  - type: "text_to_speech"
    model: "elevenlabs"
    params:
      voice: "rachel"
      speed: 1.0
      stability: 0.5
      similarity_boost: 0.8
      style: 0.2
      output_file: "my_first_audio.mp3"

output_dir: "output"
```

### Run the Pipeline
```bash
python -m ai_content_pipeline run-chain --config my_first_pipeline.yaml --no-confirm
```

## 🔄 Parallel Execution Example

### Multi-Voice Generation
Create `parallel_voices.yaml`:

```yaml
name: "parallel_voices"
description: "Generate multiple voices simultaneously"
prompt: "This text will be spoken by multiple voices in parallel."

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
            output_file: "voice_rachel.mp3"
        - type: "text_to_speech"
          model: "elevenlabs"
          params:
            voice: "drew"
            output_file: "voice_drew.mp3"
        - type: "text_to_speech"
          model: "elevenlabs"
          params:
            voice: "bella"
            output_file: "voice_bella.mp3"

output_dir: "output"
```

### Run with Parallel Execution
```bash
PIPELINE_PARALLEL_ENABLED=true python -m ai_content_pipeline run-chain --config parallel_voices.yaml --no-confirm
```

## 📊 Understanding Output

### Success Output
```
✅ Chain execution successful!
📦 Steps completed: 1/1
💰 Total cost: $0.050
⏱️  Total time: 1.1 seconds
```

### Parallel Execution Output
```
🔄 Executing 3 steps in parallel (max_workers=3)
⏱️  Parallel execution completed in 2.28s
📊 Results: 2/3 successful
```

### Generated Files
Check the `output/` directory for:
- Generated audio files (`.mp3`)
- Execution reports (`.json`)
- Intermediate results

## 🛠️ Available Step Types

### Current Step Types
- `text_to_speech` - Convert text to audio
- `text_to_image` - Generate images from text
- `image_understanding` - Analyze images
- `prompt_generation` - Generate optimized prompts
- `image_to_image` - Modify existing images
- `parallel_group` - Execute steps in parallel

### Models Available
- **TTS**: `elevenlabs`, `elevenlabs_turbo`, `elevenlabs_v3`
- **Images**: `imagen4`, `flux`, `seedream`
- **Analysis**: `gemini`, `openrouter`

## 🎛️ Configuration Options

### Basic Configuration
```yaml
name: "pipeline_name"           # Required: Pipeline identifier
description: "What it does"     # Optional: Human description
prompt: "Input text"            # Required: Main input text

steps: [...]                    # Required: Array of processing steps

output_dir: "output"            # Optional: Output directory
temp_dir: "temp"               # Optional: Temporary files
cleanup_temp: true             # Optional: Clean temp files
save_intermediates: true       # Optional: Save step results
```

### Parallel Group Configuration
```yaml
- type: "parallel_group"
  model: "parallel"
  params:
    max_workers: 3              # Max concurrent executions
    merge_strategy: "collect_all"  # How to combine results
    parallel_steps: [...]       # Steps to run in parallel
```

### Merge Strategies
- `collect_all` - Return all results
- `first_success` - Return first successful result
- `best_quality` - Return highest quality result (future)

## 🔧 Troubleshooting

### Common Issues

#### 1. Module Not Found
```bash
# Ensure you're in the right directory and venv is activated
cd ai_content_pipeline
source ../venv/bin/activate
```

#### 2. API Key Errors
```bash
# Check your environment variables
echo $ELEVENLABS_API_KEY
echo $FAL_KEY
```

#### 3. Parallel Not Working
```bash
# Ensure parallel execution is enabled
export PIPELINE_PARALLEL_ENABLED=true
```

#### 4. Permission Errors
```bash
# Check output directory permissions
ls -la output/
mkdir -p output
```

### Validation Errors
If you see validation errors:
- Check YAML syntax (proper indentation)
- Verify all required fields are present
- Ensure step types are spelled correctly
- Check input/output type compatibility

### Cost Monitoring
- Check execution reports for cost breakdown
- Use `--debug` flag for detailed logging
- Monitor API usage in provider dashboards

## 📚 Next Steps

1. **Explore Examples**: Check `input/` directory for more examples
2. **Read Documentation**: See [YAML_CONFIGURATION.md](YAML_CONFIGURATION.md) for complete syntax
3. **Try Parallel Workflows**: Read [PARALLEL_WORKFLOWS.md](PARALLEL_WORKFLOWS.md) for advanced patterns
4. **Optimize Costs**: See [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md) for cost-saving tips

## 🎯 Example Workflows

### Content Creation Workflow
```yaml
# 1. Generate image → 2. Create multiple voice narrations
steps:
  - type: "text_to_image"
    model: "imagen4"
    params:
      aspect_ratio: "16:9"
  
  - type: "parallel_group"
    params:
      parallel_steps:
        - type: "text_to_speech"
          params: {voice: "rachel"}
        - type: "text_to_speech"
          params: {voice: "drew"}
```

### A/B Testing Workflow
```yaml
# Test multiple image generation models
steps:
  - type: "parallel_group"
    params:
      merge_strategy: "collect_all"
      parallel_steps:
        - type: "text_to_image"
          model: "imagen4"
        - type: "text_to_image"
          model: "flux"
        - type: "text_to_image"
          model: "seedream"
```

## 📞 Getting Help

- **Documentation**: Browse the `docs/` directory
- **Examples**: Check `input/` directory for working examples
- **Tests**: Run test suite to see working code
- **Issues**: Create GitHub issues for bugs or questions

Happy content creation! 🎨🎵📹