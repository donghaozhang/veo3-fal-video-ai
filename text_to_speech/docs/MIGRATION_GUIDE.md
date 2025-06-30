# Migration Guide: Refactored Text-to-Speech Package

This guide helps you migrate from the original monolithic structure to the new modular package structure.

## What Changed?

### Before (Monolithic Structure)
```
text_to_speech/
├── elevenlabs_tts_controller.py      (632 lines)
├── openrouter_tts_pipeline.py        (705 lines) 
├── elevenlabs_dialogue_controller.py (618 lines)
├── example_usage.py
├── interactive_pipeline.py
├── quick_start.py
└── text_to_dialogue_script.py
```

### After (Modular Package Structure)
```
text_to_speech/
├── __init__.py                    # Main package interface
├── models/                        # Data models and enums
│   ├── common.py                  # Shared models
│   └── pipeline.py                # Pipeline-specific models
├── tts/                          # Core TTS functionality
│   ├── controller.py             # Main TTS controller
│   ├── voice_manager.py          # Voice management
│   └── audio_processor.py        # Audio processing
├── pipeline/                     # OpenRouter pipeline
│   └── core.py                   # Pipeline orchestration
├── utils/                        # Utilities
│   ├── file_manager.py           # File operations
│   ├── api_helpers.py            # API utilities
│   └── validators.py             # Input validation
├── config/                       # Configuration
│   ├── voices.py                 # Voice presets
│   ├── models.py                 # Model configurations
│   └── defaults.py               # Default settings
└── examples/                     # Usage examples
    └── basic_usage.py            # Basic examples
```

## Import Changes

### Old Imports
```python
# Before
from elevenlabs_tts_controller import ElevenLabsTTSController, ElevenLabsModel, VoiceSettings
from openrouter_tts_pipeline import OpenRouterTTSPipeline, OpenRouterModel
```

### New Imports
```python
# After - Main package interface (recommended)
from text_to_speech import ElevenLabsTTSController, ElevenLabsModel, VoiceSettings

# After - Direct module imports
from text_to_speech.tts.controller import ElevenLabsTTSController
from text_to_speech.models.common import ElevenLabsModel, VoiceSettings
from text_to_speech.pipeline.core import OpenRouterTTSPipeline
from text_to_speech.models.pipeline import OpenRouterModel
```

## Code Migration Examples

### Basic TTS Usage

#### Before
```python
from elevenlabs_tts_controller import ElevenLabsTTSController, VoiceSettings

tts = ElevenLabsTTSController(api_key)
success = tts.text_to_speech(
    text="Hello world",
    voice_id=tts.get_popular_voice_id("rachel"),
    output_file="output.mp3"
)
```

#### After
```python
from text_to_speech import ElevenLabsTTSController, VoiceSettings

tts = ElevenLabsTTSController(api_key)
success = tts.text_to_speech(
    text="Hello world", 
    voice_id=tts.get_popular_voice_id("rachel"),
    output_file="output.mp3"
)
```

### Pipeline Usage

#### Before
```python
from openrouter_tts_pipeline import OpenRouterTTSPipeline, OpenRouterModel

pipeline = OpenRouterTTSPipeline(openrouter_key, elevenlabs_key)
result = pipeline.run_complete_pipeline(
    description="tech startup discussion",
    num_people=2,
    length_minutes=1.5
)
```

#### After
```python
from text_to_speech.pipeline.core import OpenRouterTTSPipeline
from text_to_speech.models.pipeline import OpenRouterModel

pipeline = OpenRouterTTSPipeline(openrouter_key, elevenlabs_key)
result = pipeline.run_complete_pipeline(
    description="tech startup discussion",
    num_people=2,
    length_minutes=1.5
)
```

## Key Benefits of New Structure

### 1. Modularity
- Smaller, focused files (150-300 lines each)
- Clear separation of concerns
- Easier to understand and maintain

### 2. Reusability
- Shared utilities and models
- Pluggable components
- Better code organization

### 3. Testing
- Isolated modules for unit testing
- Easier to mock dependencies
- Better test coverage

### 4. Documentation
- Clearer module purposes
- Better API documentation
- Easier onboarding

## Migration Steps

### Step 1: Update Your Imports
Replace old imports with new package imports as shown above.

### Step 2: Test Your Code
Run your existing code with the new imports to ensure compatibility.

### Step 3: Leverage New Features
Consider using the new modular components for enhanced functionality:

```python
# Use voice manager directly
from text_to_speech.tts.voice_manager import VoiceManager
voice_manager = VoiceManager(api_key)
voices = voice_manager.search_voices("female")

# Use audio processor for advanced features
from text_to_speech.tts.audio_processor import AudioProcessor
processor = AudioProcessor()
info = processor.get_audio_info("output.mp3")

# Use configuration presets
from text_to_speech.config.voices import get_voice_style_preset
style = get_voice_style_preset("professional")
```

### Step 4: Update Dependencies
If you have a requirements.txt, ensure you have the latest version:

```txt
requests>=2.31.0
python-dotenv>=1.0.0
elevenlabs>=1.0.0
```

## Backward Compatibility

The main public APIs remain the same, so most existing code will work with minimal changes:

- `ElevenLabsTTSController` class interface unchanged
- `OpenRouterTTSPipeline` class interface unchanged
- All method signatures preserved
- Same environment variable requirements

## New Features Available

### Enhanced Voice Management
```python
from text_to_speech.tts.voice_manager import VoiceManager

voice_manager = VoiceManager(api_key)
# Search voices by criteria
female_voices = voice_manager.get_voices_by_gender("female")
# Get random voice
random_voice = voice_manager.get_random_voice(category="premade")
```

### Better Error Handling
```python
from text_to_speech.utils.validators import validate_text_input

is_valid, error = validate_text_input(text)
if not is_valid:
    print(f"Validation error: {error}")
```

### Configuration Management
```python
from text_to_speech.config.models import get_voice_settings_preset

# Use predefined voice settings
creative_settings = get_voice_settings_preset("creative")
```

## Getting Help

If you encounter issues during migration:

1. Check the examples in `examples/basic_usage.py`
2. Review the new package structure
3. Ensure all imports are updated correctly
4. Test with a simple example first

The refactored package maintains all original functionality while providing better organization and new features for enhanced development experience.