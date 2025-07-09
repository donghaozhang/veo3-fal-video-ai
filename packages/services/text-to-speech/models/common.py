"""
Common Data Models

Shared data models, enums, and dataclasses used across the text-to-speech package.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class ElevenLabsModel(Enum):
    """ElevenLabs TTS Models with their capabilities"""
    ELEVEN_V3 = "eleven_v3"  # Alpha - Most expressive, 70+ languages, 10k chars
    MULTILINGUAL_V2 = "eleven_multilingual_v2"  # Highest quality, 29 languages, 10k chars
    FLASH_V2_5 = "eleven_flash_v2_5"  # Ultra-low latency ~75ms, 32 languages, 40k chars
    TURBO_V2_5 = "eleven_turbo_v2_5"  # Balanced quality/speed, 32 languages, 40k chars


class AudioFormat(Enum):
    """Supported audio formats"""
    MP3 = "mp3_44100_128"  # Default: 44.1kHz @ 128kbps
    MP3_HIGH = "mp3_44100_192"  # High quality: 44.1kHz @ 192kbps
    MP3_LOW = "mp3_22050_32"   # Low quality: 22.05kHz @ 32kbps
    PCM = "pcm_16000"          # PCM 16kHz
    PCM_HIGH = "pcm_44100"     # PCM 44.1kHz
    ULAW = "ulaw_8000"         # μ-law 8kHz (telephony)
    OPUS = "opus_48000"        # Opus 48kHz


@dataclass
class VoiceSettings:
    """Voice configuration settings"""
    stability: float = 0.5      # 0.0-1.0: Higher = more stable, lower = more variable
    similarity_boost: float = 0.5  # 0.0-1.0: Higher = closer to original voice
    style: float = 0.0          # 0.0-1.0: Style exaggeration (v2 models)
    use_speaker_boost: bool = True  # Enhance speaker clarity

    def to_dict(self) -> Dict:
        """Convert to dictionary for API requests"""
        return {
            "stability": self.stability,
            "similarity_boost": self.similarity_boost,
            "style": self.style,
            "use_speaker_boost": self.use_speaker_boost
        }


@dataclass
class VoiceInfo:
    """Voice information structure"""
    voice_id: str
    name: str
    category: str
    description: str = ""
    language: str = "en"
    gender: str = "neutral"

    def __str__(self) -> str:
        return f"{self.name} ({self.voice_id}) - {self.category} - {self.language}"


# Popular voice presets mapping
POPULAR_VOICE_IDS = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",  # Female, American
    "drew": "29vD33N1CtxCmqQRPOHJ",     # Male, American  
    "clyde": "2EiwWnXFnvU5JabPnv8n",    # Male, American
    "bella": "EXAVITQu4vr4xnSDxMaL",    # Female, American
    "antoni": "ErXwobaYiN019PkySvjV",   # Male, American
    "elli": "MF3mGyEYCl7XYWbV9V6O",     # Female, American
    "josh": "TxGEqnHWrfWFTfGW9XjX",     # Male, American
    "arnold": "VR6AewLTigWG4xSOukaG",   # Male, American
    "adam": "pNInz6obpgDQGcFmaJgB",     # Male, American
    "sam": "yoZ06aMxZJJ28mfd3POQ",      # Male, American
}