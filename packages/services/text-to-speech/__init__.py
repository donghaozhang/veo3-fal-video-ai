"""
ElevenLabs Text-to-Speech Package

A comprehensive Python package for ElevenLabs text-to-speech with advanced voice control,
timing features, dialogue generation, and OpenRouter AI integration.

Main components:
- tts: Core text-to-speech functionality
- dialogue: Multi-speaker dialogue generation
- pipeline: Complete AI content generation pipeline
- models: Data models and configurations
- utils: Utility functions and helpers
- config: Configuration and presets
"""

from .tts.controller import ElevenLabsTTSController
from .models.common import ElevenLabsModel, AudioFormat, VoiceSettings, VoiceInfo

__version__ = "1.0.0"
__author__ = "Text-to-Speech Team"

# Main exports for backwards compatibility
__all__ = [
    "ElevenLabsTTSController",
    "ElevenLabsModel", 
    "AudioFormat",
    "VoiceSettings",
    "VoiceInfo"
]