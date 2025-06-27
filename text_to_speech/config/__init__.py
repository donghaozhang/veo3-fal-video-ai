"""
Configuration Module

Configuration settings, presets, and defaults for the text-to-speech package.

Components:
- voices: Voice presets and configurations
- models: Model configurations and settings
- defaults: Default values and settings
"""

from .voices import POPULAR_VOICES, get_voice_preset
from .models import DEFAULT_MODEL_SETTINGS
from .defaults import DEFAULT_VOICE_SETTINGS, DEFAULT_AUDIO_FORMAT

__all__ = [
    "POPULAR_VOICES",
    "get_voice_preset",
    "DEFAULT_MODEL_SETTINGS", 
    "DEFAULT_VOICE_SETTINGS",
    "DEFAULT_AUDIO_FORMAT"
]