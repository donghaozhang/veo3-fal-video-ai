"""
Text-to-Speech Module

Core TTS functionality including voice control, audio processing, and speech generation.

Components:
- controller: Main TTS controller with speech generation
- voice_manager: Voice selection and management
- audio_processor: Audio format handling and processing
"""

from .controller import ElevenLabsTTSController
from .voice_manager import VoiceManager
from .audio_processor import AudioProcessor

__all__ = ["ElevenLabsTTSController", "VoiceManager", "AudioProcessor"]