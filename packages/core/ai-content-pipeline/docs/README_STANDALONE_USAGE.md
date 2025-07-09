# Standalone Image Analysis and Understanding Usage Guide

This guide demonstrates how to use the AI Content Pipeline's image analysis capabilities directly, without going through the full pipeline chain validation.

## Available Approaches

### 1. **AI Content Pipeline Models** (Recommended)
Use the unified models from the AI Content Pipeline with built-in cost estimation and error handling.

**Files:**
- `standalone_image_analysis.py` - Complete examples with all available models
- `test_prompt_generation_standalone.py` - Focus on prompt generation

**Models Available:**
- **Image Understanding:** `gemini_describe`, `gemini_detailed`, `gemini_classify`, `gemini_objects`, `gemini_ocr`, `gemini_composition`, `gemini_qa`
- **Prompt Generation:** `openrouter_video_prompt`, `openrouter_video_cinematic`, `openrouter_video_realistic`, `openrouter_video_artistic`, `openrouter_video_dramatic`

### 2. **Direct Video Tools Integration** (Advanced)
Use the underlying Gemini and OpenRouter analyzers directly, bypassing all pipeline overhead.

**Files:**
- `direct_gemini_analysis.py` - Direct Gemini image analysis
- `direct_openrouter_prompts.py` - Direct OpenRouter prompt generation

**Benefits:** Maximum performance, no validation overhead, direct access to raw results.

### 3. **Existing Examples**
The pipeline already includes working examples:

**Files:**
- `basic_usage.py` - Pipeline-based image generation examples
- `run_example_workflow.py` - Complete workflow demonstrations

## Quick Start Examples

### Image Analysis with AI Content Pipeline Models

```python
from ai_content_pipeline.models.image_understanding import UnifiedImageUnderstandingGenerator

# Initialize analyzer
analyzer = UnifiedImageUnderstandingGenerator()

# Analyze image
result = analyzer.analyze(
    image_path="https://example.com/image.jpg",  # or local path
    model="gemini_detailed"
)

if result.success:
    print(f"Analysis: {result.output_text}")
    print(f"Cost: ${result.cost_estimate:.3f}")
    print(f"Time: {result.processing_time:.2f}s")
```

### Video Prompt Generation

```python
from ai_content_pipeline.models.prompt_generation import UnifiedPromptGenerator

# Initialize generator
generator = UnifiedPromptGenerator()

# Generate video prompt
result = generator.generate(
    image_path="path/to/image.jpg",
    model="openrouter_video_cinematic",
    background_context="Create a dramatic movie-style sequence"
)

if result.success:
    print(f"Generated Prompt: {result.extracted_prompt}")
```

### Direct Gemini Analysis (Advanced)

```python
import sys
from pathlib import Path

# Add video_tools to path
video_tools_path = Path(__file__).parent.parent.parent / "video_tools"
sys.path.insert(0, str(video_tools_path))

from video_utils.gemini_analyzer import GeminiVideoAnalyzer

# Direct usage
analyzer = GeminiVideoAnalyzer()
result = analyzer.describe_image(Path("image.jpg"), detailed=True)
```

### Direct OpenRouter Prompts (Advanced)

```python
import sys
from pathlib import Path

# Add video_tools to path
video_tools_path = Path(__file__).parent.parent.parent / "video_tools"
sys.path.insert(0, str(video_tools_path))

from video_utils.openrouter_analyzer import OpenRouterAnalyzer

# Direct usage
analyzer = OpenRouterAnalyzer(model="google/gemini-2.0-flash-001")
result = analyzer.generate_video_prompt(
    Path("image.jpg"),
    background_context="Create cinematic video",
    video_style="cinematic",
    duration_preference="medium"
)
```

## Environment Setup

### Required API Keys

```bash
# For Gemini image analysis
export GEMINI_API_KEY="your_gemini_api_key"

# For OpenRouter prompt generation  
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

### Virtual Environment

```bash
# Always activate the virtual environment first
source venv/bin/activate
```

## Running the Examples

### 1. Comprehensive Standalone Examples

```bash
# Activate environment
source venv/bin/activate

# Run comprehensive standalone examples
python ai_content_pipeline/examples/standalone_image_analysis.py

# Run prompt generation examples
python ai_content_pipeline/examples/test_prompt_generation_standalone.py
```

### 2. Direct Integration Examples

```bash
# Direct Gemini analysis
python ai_content_pipeline/examples/direct_gemini_analysis.py

# Direct OpenRouter prompts
python ai_content_pipeline/examples/direct_openrouter_prompts.py
```

### 3. Basic Pipeline Examples

```bash
# Basic usage examples
python ai_content_pipeline/examples/basic_usage.py

# Full workflow examples
python ai_content_pipeline/examples/run_example_workflow.py
```

## Available Image Analysis Models

### Gemini Image Understanding Models

| Model | Description | Use Case | Cost |
|-------|-------------|----------|------|
| `gemini_describe` | Basic image description | Quick summaries | $0.001 |
| `gemini_detailed` | Comprehensive analysis | Detailed understanding | $0.002 |
| `gemini_classify` | Image categorization | Content classification | $0.001 |
| `gemini_objects` | Object detection | Identify items in image | $0.002 |
| `gemini_ocr` | Text extraction | Read text from images | $0.001 |
| `gemini_composition` | Artistic analysis | Photography/art critique | $0.002 |
| `gemini_qa` | Question answering | Custom questions | $0.001 |

### OpenRouter Video Prompt Models

| Model | Description | Style | Cost |
|-------|-------------|-------|------|
| `openrouter_video_prompt` | General video prompts | Cinematic | $0.002 |
| `openrouter_video_cinematic` | Movie-style prompts | Cinematic | $0.002 |
| `openrouter_video_realistic` | Documentary style | Realistic | $0.002 |
| `openrouter_video_artistic` | Creative/abstract | Artistic | $0.002 |
| `openrouter_video_dramatic` | High-emotion | Dramatic | $0.002 |

## Input Support

All models support:
- **URLs:** `https://example.com/image.jpg`
- **Local Files:** `/path/to/image.jpg` or `./relative/path.jpg`
- **Formats:** `.jpg`, `.jpeg`, `.png`, `.webp`

## Pipeline vs. Direct Usage

### AI Content Pipeline Models (Recommended)
- ✅ Built-in error handling and validation
- ✅ Cost estimation and tracking
- ✅ Consistent result format
- ✅ Processing time measurement
- ✅ Automatic file handling (URLs, local files)
- ✅ Metadata and context preservation

### Direct Video Tools Usage (Advanced)
- ✅ Maximum performance (no overhead)
- ✅ Direct access to raw model responses
- ✅ Full control over parameters
- ❌ No built-in error handling
- ❌ No cost estimation
- ❌ Manual file path management
- ❌ Raw response format handling required

## Troubleshooting

### Common Issues

1. **"Analyzer not available"**
   - Check API key environment variables
   - Ensure virtual environment is activated
   - Verify video_tools directory exists

2. **"Module not found" errors**
   - Activate virtual environment: `source venv/bin/activate`
   - Check Python path in scripts

3. **API key errors**
   ```bash
   export GEMINI_API_KEY="your_key_here"
   export OPENROUTER_API_KEY="your_key_here"
   ```

4. **Image download failures**
   - Check internet connection
   - Verify image URL accessibility
   - Try with local image files

### Getting API Keys

- **Gemini:** https://aistudio.google.com/app/apikey
- **OpenRouter:** https://openrouter.ai/

## Performance Comparison

| Approach | Setup Time | Execution Time | Error Handling | Cost Tracking |
|----------|------------|----------------|----------------|---------------|
| Pipeline Models | Medium | Medium | Excellent | Yes |
| Direct Tools | Fast | Fast | Manual | No |
| Full Pipeline | Slow | Slow | Excellent | Yes |

## Best Practices

1. **For Development/Testing:** Use AI Content Pipeline models for consistent results and built-in validation.

2. **For Production:** Consider direct tools if maximum performance is needed and you can handle errors manually.

3. **For Learning:** Start with the comprehensive examples in `standalone_image_analysis.py`.

4. **For Integration:** Use the unified model classes to maintain consistency across your application.

5. **For Debugging:** Use direct tools to understand raw model responses and troubleshoot issues.

## Example Outputs

### Image Analysis Result
```python
ImageUnderstandingResult(
    success=True,
    output_text="A scenic mountain landscape with snow-capped peaks...",
    model_used="gemini_detailed",
    cost_estimate=0.002,
    processing_time=3.45,
    error=None,
    metadata={
        "model": "gemini_detailed",
        "image_path": "https://example.com/image.jpg",
        "analysis_type": "Detailed Image Analysis"
    }
)
```

### Prompt Generation Result
```python
PromptGenerationResult(
    success=True,
    output_text="Full analysis of the image for video generation...",
    extracted_prompt="A cinematic aerial shot of snow-capped mountains with golden hour lighting, slow camera movement revealing the vast landscape below",
    model_used="openrouter_video_cinematic",
    cost_estimate=0.002,
    processing_time=2.8,
    error=None,
    metadata={
        "model": "openrouter_video_cinematic",
        "video_style": "cinematic",
        "duration_preference": "medium"
    }
)
```