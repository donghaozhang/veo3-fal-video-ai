# AI Content Pipeline Documentation - Table of Contents

## 🚀 Getting Started

1. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Your first pipeline
   - Prerequisites and setup
   - Simple TTS example
   - Parallel execution introduction
   - Troubleshooting common issues

2. **[YAML_CONFIGURATION.md](YAML_CONFIGURATION.md)** - Complete configuration reference
   - Basic YAML structure
   - All step types and parameters
   - Complete examples
   - Advanced configuration patterns

## 🔧 Technical Documentation

### Parallel Execution
3. **[parallel_pipeline_design.md](parallel_pipeline_design.md)** - Design concepts
   - Current limitations
   - Proposed solutions
   - Data flow patterns
   - Use cases and benefits

4. **[PARALLEL_IMPLEMENTATION_PLAN.md](PARALLEL_IMPLEMENTATION_PLAN.md)** - Technical implementation
   - Phase-by-phase implementation plan
   - Core data structures
   - Executor implementation
   - Testing strategy

5. **[BACKWARD_COMPATIBLE_PARALLEL_PLAN.md](BACKWARD_COMPATIBLE_PARALLEL_PLAN.md)** - Zero-breaking-change strategy
   - Compatibility principles
   - Feature flags and gradual rollout
   - Migration path
   - Rollback strategies

## 📋 Quick Reference

### Step Types
- `text_to_speech` - Convert text to audio
- `text_to_image` - Generate images from text
- `image_understanding` - Analyze images
- `prompt_generation` - Generate optimized prompts
- `image_to_image` - Modify existing images
- `parallel_group` - Execute steps in parallel

### Models
- **TTS**: `elevenlabs`, `elevenlabs_turbo`, `elevenlabs_v3`
- **Images**: `imagen4`, `flux`, `seedream`
- **Analysis**: `gemini`, `openrouter`

### Commands
```bash
# Run pipeline
python -m ai_content_pipeline run-chain --config config.yaml

# Enable parallel execution
PIPELINE_PARALLEL_ENABLED=true python -m ai_content_pipeline run-chain --config config.yaml

# Debug mode
python -m ai_content_pipeline run-chain --config config.yaml --debug
```

## 📁 File Structure

```
docs/
├── README.md                              # Documentation index
├── TABLE_OF_CONTENTS.md                   # This file
├── GETTING_STARTED.md                     # Quick start guide
├── YAML_CONFIGURATION.md                  # Configuration reference
├── parallel_pipeline_design.md            # Design concepts
├── PARALLEL_IMPLEMENTATION_PLAN.md        # Technical plan
└── BACKWARD_COMPATIBLE_PARALLEL_PLAN.md   # Compatibility strategy
```

## 🎯 By Use Case

### New Users
1. [GETTING_STARTED.md](GETTING_STARTED.md) - Basic setup
2. [YAML_CONFIGURATION.md](YAML_CONFIGURATION.md) - Learn syntax

### Content Creators
1. [YAML_CONFIGURATION.md](YAML_CONFIGURATION.md) - Configuration guide
2. [GETTING_STARTED.md](GETTING_STARTED.md) - Examples and workflows

### Developers
1. [parallel_pipeline_design.md](parallel_pipeline_design.md) - Architecture
2. [PARALLEL_IMPLEMENTATION_PLAN.md](PARALLEL_IMPLEMENTATION_PLAN.md) - Implementation
3. [BACKWARD_COMPATIBLE_PARALLEL_PLAN.md](BACKWARD_COMPATIBLE_PARALLEL_PLAN.md) - Compatibility

### Performance Optimization
1. [parallel_pipeline_design.md](parallel_pipeline_design.md) - Parallel concepts
2. [YAML_CONFIGURATION.md](YAML_CONFIGURATION.md) - Optimization tips

## 📖 Reading Order Recommendations

### For Beginners
1. Start with [GETTING_STARTED.md](GETTING_STARTED.md)
2. Try the simple examples
3. Read [YAML_CONFIGURATION.md](YAML_CONFIGURATION.md) for more options
4. Experiment with parallel execution

### For Advanced Users
1. Review [parallel_pipeline_design.md](parallel_pipeline_design.md) for concepts
2. Check [YAML_CONFIGURATION.md](YAML_CONFIGURATION.md) for all options
3. Design complex workflows with parallel execution

### For Contributors
1. Understand the system with [parallel_pipeline_design.md](parallel_pipeline_design.md)
2. Review implementation details in [PARALLEL_IMPLEMENTATION_PLAN.md](PARALLEL_IMPLEMENTATION_PLAN.md)
3. Check compatibility strategy in [BACKWARD_COMPATIBLE_PARALLEL_PLAN.md](BACKWARD_COMPATIBLE_PARALLEL_PLAN.md)

---

*Choose your starting point based on your role and experience level!*