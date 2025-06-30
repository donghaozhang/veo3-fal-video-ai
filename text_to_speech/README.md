# ElevenLabs Text-to-Speech Package

A comprehensive, modular Python package for ElevenLabs text-to-speech with advanced voice control, timing features, dialogue generation, and OpenRouter AI integration.

## ✨ New! Refactored Modular Architecture

This package has been completely refactored from monolithic files into a well-organized, modular structure:

- **🏗️ Modular Design**: Clean separation of concerns across multiple focused modules
- **🔧 Enhanced Maintainability**: Smaller files (150-300 lines each) that are easier to understand and modify  
- **🧪 Better Testing**: Isolated components for comprehensive unit testing
- **📦 Proper Package Structure**: Professional Python package with setup.py and proper imports
- **🔄 Backward Compatibility**: Existing code works with minimal import changes

> **Migration Note**: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for help transitioning from the old structure.

## Features

### 🎤 Voice Control
- **3000+ voices** from ElevenLabs voice library
- **Popular voice presets** (Rachel, Drew, Bella, Antoni, etc.)
- **Custom voice cloning** from audio files
- **Multi-speaker dialogue** generation
- **Voice categorization** and filtering

### ⏱️ Timing Control
- **Speed control** (0.7x to 1.2x speed)
- **Pause insertion** with `<break>` tags
- **Custom timing patterns** for natural speech
- **Multi-segment audio** with precise timing

### 🎭 Text-to-Dialogue (NEW!)
- **Multi-speaker conversations** with Eleven v3
- **Emotional context tags** ([cheerfully], [stuttering], etc.)
- **Natural dialogue flow** with automatic timing
- **Immersive conversation generation**

### 🎛️ Advanced Settings
- **Stability control** (0.0-1.0)
- **Similarity boost** (0.0-1.0)
- **Style exaggeration** (0.0-1.0)
- **Speaker boost** for clarity

### 🎵 Audio Formats
- **MP3** (22.05kHz-44.1kHz, 32-192kbps)
- **PCM** (16kHz-44.1kHz, 16-bit)
- **Opus** (48kHz, 32-192kbps)
- **μ-law/A-law** (8kHz, telephony)

### 🌍 Multi-Language Support
- **32 languages** with Flash v2.5
- **29 languages** with Multilingual v2
- **70+ languages** with Eleven v3 (alpha)

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

#### Option A: Using the Activation Script (Recommended)
```bash
# Navigate to the text_to_speech directory
cd text_to_speech

# Run the environment activation script
source activate_env.sh
```

The activation script will:
- ✅ Activate the virtual environment (`tts_env/bin/activate`)
- ✅ Set the proper PYTHONPATH for imports
- ✅ Display ready-to-run commands

#### Option B: Manual Setup
```bash
# Activate virtual environment
source tts_env/bin/activate

# Set PYTHONPATH for proper imports
export PYTHONPATH=/home/zdhpe/veo3-video-generation:$PYTHONPATH

# Set API key
export ELEVENLABS_API_KEY="your_api_key_here"
```

### 3. Get API Key

Get your API key from [ElevenLabs Speech Synthesis](https://elevenlabs.io/app/speech-synthesis/text-to-speech)

### 4. Set Environment Variable

```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```

### 5. Basic Usage

```python
from elevenlabs_tts_controller import ElevenLabsTTSController

# Initialize
tts = ElevenLabsTTSController(api_key="your_api_key")

# Simple text-to-speech with timing control
success = tts.text_to_speech_with_timing_control(
    text="Hello! This demonstrates voice and timing control.",
    voice_name="rachel",
    speed=1.0,
    output_file="hello.mp3"
)
```

### 6. Text-to-Dialogue Usage

```python
# Quick dialogue script
python text_to_dialogue_script.py
```

### 7. Quick Start Commands

After running the activation script, you can immediately use:
```bash
# Basic usage examples
python examples/basic_usage.py

# Quick start with interactive CLI
python cli/quick_start.py

# Simple test to verify setup
python test_simple.py
```

### 8. Complete AI Pipeline Usage

```bash
# Quick start with demos
python quick_start.py

# Interactive pipeline (user-friendly)
python interactive_pipeline.py

# Quick demo
python interactive_pipeline.py --demo

# Advanced pipeline usage
python openrouter_tts_pipeline.py
```

## Text-to-Dialogue Examples

Based on the [official ElevenLabs Text-to-Dialogue documentation](https://elevenlabs.io/docs/cookbooks/text-to-dialogue):

### Basic Dialogue
```python
from elevenlabs.client import ElevenLabs
from elevenlabs import save, play

client = ElevenLabs(api_key="your_api_key")

audio = client.text_to_dialogue.convert(
    inputs=[
        {
            "text": "[cheerfully] Hello, how are you?",
            "voice_id": "9BWtsMINqrJLrRacOk9x",  # Aria
        },
        {
            "text": "[stuttering] I'm... I'm doing well, thank you",
            "voice_id": "IKne3meq5aSn9XLyUdCD",  # Paul
        }
    ]
)

save(audio, "dialogue.mp3")
play(audio)
```

### Multi-Speaker Conversation
```python
audio = client.text_to_dialogue.convert(
    inputs=[
        {
            "text": "[excitedly] Welcome to our AI dialogue system!",
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        },
        {
            "text": "[curiously] How does it work exactly?",
            "voice_id": "29vD33N1CtxCmqQRPOHJ",  # Drew
        },
        {
            "text": "[cheerfully] It uses advanced AI to generate natural conversations!",
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        }
    ]
)
```

### Emotional Tags for Dialogue

Available emotional context tags:

**Positive**: `[cheerfully]`, `[excitedly]`, `[happily]`, `[enthusiastically]`, `[playfully]`

**Negative**: `[sadly]`, `[angrily]`, `[frustrated]`, `[disappointed]`, `[worried]`

**Neutral**: `[calmly]`, `[quietly]`, `[loudly]`, `[politely]`, `[curiously]`

**Special**: `[whispering]`, `[shouting]`, `[stuttering]`, `[sarcastically]`, `[mischievously]`

## OpenRouter AI + Text-to-Speech Pipeline

Complete end-to-end pipeline that generates content using top AI models and converts to speech:

### Pipeline Steps:
1. **Input**: Description of person(s) + desired length
2. **Length Calculation**: Estimate content requirements (words, tokens, timing)
3. **LLM Generation**: Use OpenRouter models to create content
4. **Content Processing**: Structure output for text-to-speech
5. **Speech Generation**: Convert to audio using ElevenLabs

### Supported AI Models (Top 10):
1. **Claude Sonnet 4** - Anthropic's latest, most capable
2. **Gemini 2.0 Flash** - Google's fast, high-quality model
3. **Gemini 2.5 Flash Preview** - Latest Google preview
4. **DeepSeek V3 (Free)** - High-quality free model
5. **Gemini 2.5 Flash** - Google's production model
6. **Claude 3.7 Sonnet** - Advanced Anthropic model
7. **Gemini 2.5 Pro** - Google's professional model
8. **DeepSeek V3** - High-performance paid model
9. **Gemini 2.0 Flash Lite** - Lightweight Google model
10. **Gemini 2.5 Flash Lite** - Efficient Google model

### Interactive Pipeline Usage:

```bash
# Setup API keys
export OPENROUTER_API_KEY="your_openrouter_key"
export ELEVENLABS_API_KEY="your_elevenlabs_key"

# Run interactive pipeline
python interactive_pipeline.py
```

### Example Pipeline Workflows:

#### Single Speaker Presentation:
```python
from openrouter_tts_pipeline import OpenRouterTTSPipeline, OpenRouterModel

pipeline = OpenRouterTTSPipeline(openrouter_key, elevenlabs_key)

results = pipeline.run_complete_pipeline(
    description="a tech entrepreneur explaining AI startup strategies",
    num_people=1,
    length_minutes=2.0,
    content_type="presentation",
    voice_style="professional",
    model=OpenRouterModel.CLAUDE_SONNET_4,
    output_file="ai_startup_talk.mp3"
)
```

#### Two-Person Dialogue:
```python
results = pipeline.run_complete_pipeline(
    description="two coffee enthusiasts debating espresso vs drip coffee",
    num_people=2,
    length_minutes=1.5,
    content_type="conversation",
    voice_style="casual",
    model=OpenRouterModel.GEMINI_2_FLASH,
    output_file="coffee_debate.mp3"
)
```

### Content Types:
- **Conversation**: Natural dialogue between speakers
- **Presentation**: Informative speech or talk
- **Interview**: Q&A format discussion
- **Story**: Narrative content with character voices

### Voice Styles:
- **Professional**: Business, formal tone (Rachel + Drew)
- **Casual**: Friendly, relaxed conversation (Bella + Antoni)
- **Dramatic**: Expressive, theatrical delivery (Elli + Josh)

## Usage Examples

### Voice Control Examples

#### Different Voices, Same Text
```python
voices = ["rachel", "drew", "bella", "antoni", "elli"]

for voice in voices:
    tts.text_to_speech_with_timing_control(
        text="Hello from ElevenLabs!",
        voice_name=voice,
        output_file=f"hello_{voice}.mp3"
    )
```

#### Speed Control
```python
speeds = [0.7, 1.0, 1.2]  # slow, normal, fast

for speed in speeds:
    tts.text_to_speech_with_timing_control(
        text="This demonstrates speed control.",
        voice_name="rachel",
        speed=speed,
        output_file=f"speed_{speed}.mp3"
    )
```

### Advanced Voice Settings

```python
from elevenlabs_tts_controller import VoiceSettings

# Conservative settings (stable, consistent)
conservative = VoiceSettings(
    stability=0.9,
    similarity_boost=0.8,
    style=0.1,
    use_speaker_boost=True
)

# Creative settings (variable, expressive)
creative = VoiceSettings(
    stability=0.3,
    similarity_boost=0.6,
    style=0.8,
    use_speaker_boost=True
)

# Use custom settings
tts.text_to_speech(
    text="Custom voice settings example.",
    voice_id=tts.get_popular_voice_id("bella"),
    voice_settings=creative,
    output_file="creative_voice.mp3"
)
```

### Multi-Speaker Dialogue

```python
conversation = [
    {"speaker": "rachel", "text": "Hello! How can I help you?"},
    {"speaker": "drew", "text": "I'd like to learn about voice synthesis."},
    {"speaker": "rachel", "text": "Great! Let me explain the features."}
]

tts.multi_voice_generation(
    script=conversation,
    output_file="conversation.wav"
)
```

### Model Comparison

```python
from elevenlabs_tts_controller import ElevenLabsModel

models = [
    ElevenLabsModel.MULTILINGUAL_V2,  # Highest quality
    ElevenLabsModel.FLASH_V2_5,       # Ultra-low latency
    ElevenLabsModel.TURBO_V2_5        # Balanced
]

for model in models:
    tts.text_to_speech(
        text="Model comparison example.",
        voice_id=tts.get_popular_voice_id("antoni"),
        model=model,
        output_file=f"model_{model.value}.mp3"
    )
```

## ElevenLabs Models

Based on the [official documentation](https://elevenlabs.io/docs/capabilities/text-to-speech), ElevenLabs offers four main models:

### Eleven v3 (Alpha) 🎭
- **Most expressive** and emotionally rich
- **70+ languages** supported
- **10,000 character limit**
- **Multi-speaker dialogue** support
- **Text-to-Dialogue API** available
- **Use cases**: Audiobooks, dramatic content, expressive narration, dialogue

### Eleven Multilingual v2 🌍
- **Highest quality** and most stable
- **29 languages** supported
- **10,000 character limit**
- **Best for long-form** content
- **Use cases**: Professional narration, multilingual projects

### Eleven Flash v2.5 ⚡
- **Ultra-low latency** (~75ms)
- **32 languages** supported
- **40,000 character limit**
- **50% lower cost** per character
- **Use cases**: Real-time applications, conversational AI

### Eleven Turbo v2.5 🚀
- **Balanced quality and speed**
- **Low latency** (~250-300ms)
- **32 languages** supported
- **40,000 character limit**
- **Use cases**: Streaming applications, cost-effective projects

## Voice Options

### Popular Voices (Presets)
- **Rachel**: Female, American (versatile, clear)
- **Drew**: Male, American (warm, professional)
- **Bella**: Female, American (friendly, expressive)
- **Antoni**: Male, American (deep, authoritative)
- **Elli**: Female, American (young, energetic)
- **Josh**: Male, American (casual, conversational)
- **Arnold**: Male, American (strong, confident)
- **Adam**: Male, American (neutral, reliable)
- **Sam**: Male, American (smooth, professional)
- **Clyde**: Male, American (mature, distinguished)

### Voice Library
- **3000+ community voices** available
- **32 languages** supported
- **Multiple accents** per language
- **Gender variety** (male, female, neutral)

### Voice Creation Options
1. **Voice Library**: Choose from existing voices
2. **Instant Voice Cloning**: Quick voice replication from samples
3. **Professional Voice Cloning**: High-fidelity voice replicas
4. **Voice Design**: Generate custom voices from text descriptions

## Audio Quality and Formats

### Supported Output Formats
- **MP3**: 22.05kHz-44.1kHz, 32-192kbps (default: 44.1kHz @ 128kbps)
- **PCM**: 16kHz-44.1kHz, 16-bit depth
- **Opus**: 48kHz, 32-192kbps
- **μ-law**: 8kHz (telephony optimized)
- **A-law**: 8kHz (telephony optimized)

### Quality Recommendations
- **High Quality**: MP3 44.1kHz @ 192kbps or PCM 44.1kHz
- **Balanced**: MP3 44.1kHz @ 128kbps (default)
- **Low Bandwidth**: MP3 22.05kHz @ 32kbps
- **Real-time**: PCM 16kHz for streaming applications
- **Telephony**: μ-law or A-law 8kHz

## Language Support

### Flash v2.5 (32 Languages)
English (US, UK, AU, CA), Japanese, Chinese, German, Hindi, French (FR, CA), Korean, Portuguese (BR, PT), Italian, Spanish (ES, MX), Indonesian, Dutch, Turkish, Filipino, Polish, Swedish, Bulgarian, Romanian, Arabic (SA, UAE), Czech, Greek, Finnish, Croatian, Malay, Slovak, Danish, Tamil, Ukrainian, Russian, **Hungarian, Norwegian, Vietnamese**

### Multilingual v2 (29 Languages)
All Flash v2.5 languages except Hungarian, Norwegian, and Vietnamese

### Usage Tips
- **Match voice accent** to target language/region for best results
- **Use native speakers** when available in voice library
- **Test different voices** for the same language to find the best fit

## Timing and Pacing Control

### Speed Control
```python
# Speed range: 0.7x (slow) to 1.2x (fast)
tts.text_to_speech_with_timing_control(
    text="Speed control demonstration.",
    voice_name="rachel",
    speed=0.8,  # 20% slower than normal
    output_file="slow_speech.mp3"
)
```

### Pause Control
```python
# Automatic pause insertion at punctuation
text = "Hello. This has pauses. How are you?"

tts.text_to_speech_with_timing_control(
    text=text,
    voice_name="rachel",
    pause_duration=0.8,  # 800ms pause after sentences
    output_file="with_pauses.mp3"
)
```

### Manual Break Tags
```python
# Use HTML-like break tags for precise control
text = 'Hello <break time="1.0s" /> there <break time="2.0s" /> friend!'

tts.text_to_speech(
    text=text,
    voice_id=tts.get_popular_voice_id("rachel"),
    output_file="manual_breaks.mp3"
)
```

## File Structure

```
text_to_speech/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── elevenlabs_tts_controller.py       # Main TTS controller class
├── elevenlabs_dialogue_controller.py  # Advanced dialogue controller
├── text_to_dialogue_script.py        # Simple dialogue script
├── openrouter_tts_pipeline.py        # Complete OpenRouter + TTS pipeline
├── interactive_pipeline.py           # User-friendly interactive interface
├── quick_start.py                     # Demo script with examples
├── example_usage.py                   # Simple usage examples
├── eleven_v3_prompting_guide.md      # ElevenLabs v3 guide
├── elevenlabs_controls_guide.md      # Controls and formatting guide
├── .env.example                       # Example environment configuration
└── output/                           # Generated audio files (.mp3) - created automatically
```

## Run Examples

### Quick Test
```bash
python example_usage.py
```

### Text-to-Dialogue
```bash
python text_to_dialogue_script.py
```

### Custom Usage
```python
from elevenlabs_tts_controller import ElevenLabsTTSController

# Your implementation here
```

## Text-to-Dialogue API Access

⚠️ **Important**: The Text-to-Dialogue API (Eleven v3) is currently in limited availability. 

- **Current Status**: Not publicly available yet, but will be soon
- **Access**: Contact ElevenLabs sales team for early access
- **Contact**: [https://elevenlabs.io/contact](https://elevenlabs.io/contact)
- **Documentation**: [Text-to-Dialogue Quickstart](https://elevenlabs.io/docs/cookbooks/text-to-dialogue)

## Troubleshooting

### Common Issues

#### API Key Not Set
```
Error: Please set your ELEVENLABS_API_KEY environment variable
```
**Solution**: Get API key from [ElevenLabs](https://elevenlabs.io/app/speech-synthesis/text-to-speech) and set environment variable

#### Voice Not Found
```
Error: Voice 'unknown_voice' not found
```
**Solution**: Use `tts.print_voices()` to see available voices or use popular voice names

#### Text-to-Dialogue Access Error
```
Error: Eleven v3 API access is currently limited
```
**Solution**: Contact ElevenLabs sales team for access to Text-to-Dialogue API

#### Rate Limiting
```
Error: Rate limit exceeded
```
**Solution**: Add delays between requests or upgrade your ElevenLabs plan

#### Audio Quality Issues
```
Issue: Generated audio sounds distorted
```
**Solution**: 
- Try different voice settings (higher stability)
- Use higher quality audio format
- Reduce text length for complex content

### Best Practices

1. **Voice Selection**: Test multiple voices to find the best fit for your content
2. **Text Length**: Break long texts into smaller segments for better quality
3. **Speed Control**: Use moderate speed adjustments (0.8x-1.2x) for natural results
4. **Voice Settings**: Start with default settings, then fine-tune based on results
5. **Model Selection**: Choose model based on your priorities (quality vs speed vs cost)
6. **Dialogue Emotions**: Use appropriate emotional tags that match the voice character

## API Documentation References

This implementation is based on the official ElevenLabs documentation:

- [Text to Speech Capabilities](https://elevenlabs.io/docs/capabilities/text-to-speech)
- [Text-to-Dialogue Quickstart](https://elevenlabs.io/docs/cookbooks/text-to-dialogue)
- [Eleven v3 Prompting](https://elevenlabs.io/docs/best-practices/prompting/eleven-v3)
- [Controls and Formatting](https://elevenlabs.io/docs/best-practices/prompting/controls)

## License

This project is for educational and demonstration purposes. Please refer to ElevenLabs' terms of service for commercial usage rights.

## Contributing

Feel free to submit issues and enhancement requests! This implementation covers the core ElevenLabs TTS functionality as documented in their official API documentation. 