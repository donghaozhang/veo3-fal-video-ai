# Text-to-Speech Examples - Enhanced CLI Version

Enhanced examples supporting both Python usage and command-line interfaces for AI pipeline integration.

## 📁 Available Examples

### 🎤 `basic_usage.py` - Enhanced CLI & Python API
**Complete text-to-speech interface with dual usage modes**

#### Python API Usage:
```python
from examples.basic_usage import generate_speech, list_available_voices

# Simple generation
output_file = generate_speech("Hello world", "rachel", "output.mp3")

# With custom settings
output_file = generate_speech(
    text="Custom speech",
    voice_name="drew", 
    output_file="custom.mp3",
    speed=1.2,
    stability=0.8
)

# Utility functions
voices = list_available_voices()
is_valid = validate_voice("rachel")
```

#### CLI Usage:
```bash
# Basic speech generation
python basic_usage.py --text "Hello world" --voice rachel --output output.mp3

# With custom settings
python basic_usage.py --text "Test speech" --voice drew --speed 1.2 --stability 0.8

# Run examples
python basic_usage.py --example basic
python basic_usage.py --example all

# List available voices
python basic_usage.py --list-voices

# Quiet mode for automation
python basic_usage.py --text "Hello" --voice rachel --quiet
```

### 🔗 `tts_cli_wrapper.py` - AI Pipeline Integration
**Optimized CLI wrapper for automation and pipeline integration**

#### Features:
- ✅ **JSON output** for programmatic parsing
- ✅ **Standardized return codes** (0=success, 1=failure)
- ✅ **Simplified interface** for automation
- ✅ **Pipeline-friendly** error handling

#### CLI Usage:
```bash
# Simple generation
python tts_cli_wrapper.py "Hello world" rachel output.mp3

# With JSON output for pipelines
python tts_cli_wrapper.py "Test speech" drew --json

# Custom settings
python tts_cli_wrapper.py "Custom text" bella output.mp3 --speed 1.2 --json

# Utility commands
python tts_cli_wrapper.py --list-voices --json
python tts_cli_wrapper.py --validate-voice rachel --json
```

#### JSON Output Format:
```json
{
  "success": true,
  "output_file": "output.mp3",
  "voice_used": "rachel",
  "text_length": 26,
  "settings": {
    "speed": 1.0,
    "stability": 0.5,
    "similarity_boost": 0.8,
    "style": 0.2
  }
}
```

## 🚀 AI Pipeline Integration

### Direct Integration Example:
```python
import subprocess
import json

# Call TTS wrapper from AI pipeline
result = subprocess.run([
    "python", "examples/tts_cli_wrapper.py",
    "Generated AI content text",
    "rachel",
    "output/ai_speech.mp3",
    "--json"
], capture_output=True, text=True)

# Parse JSON result
if result.returncode == 0:
    output_data = json.loads(result.stdout)
    print(f"TTS Success: {output_data['output_file']}")
else:
    error_data = json.loads(result.stdout)
    print(f"TTS Failed: {error_data['error']}")
```

### Pipeline Integration with Error Handling:
```python
def generate_ai_speech(text, voice="rachel", output_file=None):
    """Generate speech for AI pipeline with proper error handling"""
    import subprocess
    import json
    
    cmd = [
        "python", "examples/tts_cli_wrapper.py",
        text, voice, "--json"
    ]
    if output_file:
        cmd.insert(-1, output_file)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        data = json.loads(result.stdout)
        
        if result.returncode == 0 and data["success"]:
            return {
                "success": True,
                "output_file": data["output_file"],
                "metadata": data
            }
        else:
            return {
                "success": False,
                "error": data.get("error", "Unknown error")
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Pipeline error: {str(e)}"
        }

# Usage in AI pipeline
result = generate_ai_speech("AI generated content", "drew", "ai_output.mp3")
if result["success"]:
    print(f"✅ Audio generated: {result['output_file']}")
else:
    print(f"❌ Failed: {result['error']}")
```

## 📊 Available Parameters

### Voice Options:
- **rachel** - Versatile, clear female voice
- **drew** - Warm, professional male voice  
- **bella** - Friendly, expressive female voice
- **antoni** - Deep, authoritative male voice
- **elli** - Young, energetic female voice
- **josh** - Casual, conversational male voice
- **arnold** - Strong, confident male voice
- **adam** - Neutral, reliable male voice
- **sam** - Smooth, professional male voice
- **clyde** - Mature, distinguished male voice

### Audio Controls:
- **speed**: 0.7-1.2 (speech rate)
- **stability**: 0.0-1.0 (voice consistency)
- **similarity_boost**: 0.0-1.0 (voice similarity)
- **style**: 0.0-1.0 (expressiveness)

## 🔧 Environment Setup

### Requirements:
```bash
# Ensure you're in the text_to_speech directory
cd /home/zdhpe/veo3-video-generation/text_to_speech

# Load environment variables
source .env  # or ensure ELEVENLABS_API_KEY is set

# Test basic functionality
python examples/basic_usage.py --list-voices
```

### API Key Configuration:
```bash
# Set API key in environment
export ELEVENLABS_API_KEY="your_api_key_here"

# Or use .env file
echo "ELEVENLABS_API_KEY=your_api_key_here" >> .env
```

## 📋 Examples by Use Case

### For Development and Testing:
```bash
# Interactive examples
python examples/basic_usage.py --example all

# Quick voice test
python examples/basic_usage.py --text "Test voice" --voice rachel
```

### For AI Pipeline Integration:
```bash
# JSON output for parsing
python examples/tts_cli_wrapper.py "AI content" rachel --json

# Quiet mode for automation
python examples/basic_usage.py --text "Silent generation" --quiet
```

### For Custom Voice Settings:
```bash
# Conservative (stable) voice
python examples/basic_usage.py --text "Professional speech" --voice drew --stability 0.9 --style 0.1

# Creative (expressive) voice  
python examples/basic_usage.py --text "Dynamic content" --voice bella --stability 0.3 --style 0.8
```

## 🧪 Testing

### Quick Test:
```bash
# Test CLI functionality
python examples/basic_usage.py --list-voices
python examples/tts_cli_wrapper.py --list-voices --json
```

### Full Test:
```bash
# Test speech generation
python examples/basic_usage.py --text "CLI test" --voice rachel --output test.mp3
python examples/tts_cli_wrapper.py "Wrapper test" drew test2.mp3 --json
```

## 🔗 Integration with AI Content Pipeline

These enhanced examples are designed for seamless integration with the AI Content Pipeline:

1. **Standardized Interfaces**: Consistent CLI patterns
2. **JSON Output**: Machine-readable results
3. **Error Handling**: Proper exit codes and error messages
4. **Automation Ready**: Silent/quiet modes for scripts
5. **Flexible Parameters**: Full control over voice settings

### Pipeline Workflow Example:
```
AI Content Generation → Text Processing → TTS CLI Wrapper → Audio Output
                                           ↓
                                     JSON Response
                                           ↓
                                  Pipeline Continues
```

This makes the text-to-speech system ready for production use in automated AI content creation workflows! 🎉