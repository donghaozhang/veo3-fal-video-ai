"""
Voice Configuration and Presets

Voice presets, configurations, and helper functions for voice selection.
"""

from typing import Dict, List, Optional
from ..models.common import VoiceInfo, POPULAR_VOICE_IDS


# Popular voice configurations with detailed information
POPULAR_VOICES = {
    "rachel": VoiceInfo(
        voice_id="21m00Tcm4TlvDq8ikWAM",
        name="Rachel",
        category="premade",
        description="Versatile, clear female voice",
        language="en",
        gender="female"
    ),
    "drew": VoiceInfo(
        voice_id="29vD33N1CtxCmqQRPOHJ",
        name="Drew",
        category="premade",
        description="Warm, professional male voice",
        language="en",
        gender="male"
    ),
    "clyde": VoiceInfo(
        voice_id="2EiwWnXFnvU5JabPnv8n",
        name="Clyde",
        category="premade",
        description="Mature, distinguished male voice",
        language="en",
        gender="male"
    ),
    "bella": VoiceInfo(
        voice_id="EXAVITQu4vr4xnSDxMaL",
        name="Bella",
        category="premade",
        description="Friendly, expressive female voice",
        language="en",
        gender="female"
    ),
    "antoni": VoiceInfo(
        voice_id="ErXwobaYiN019PkySvjV",
        name="Antoni",
        category="premade",
        description="Deep, authoritative male voice",
        language="en",
        gender="male"
    ),
    "elli": VoiceInfo(
        voice_id="MF3mGyEYCl7XYWbV9V6O",
        name="Elli",
        category="premade",
        description="Young, energetic female voice",
        language="en",
        gender="female"
    ),
    "josh": VoiceInfo(
        voice_id="TxGEqnHWrfWFTfGW9XjX",
        name="Josh",
        category="premade",
        description="Casual, conversational male voice",
        language="en",
        gender="male"
    ),
    "arnold": VoiceInfo(
        voice_id="VR6AewLTigWG4xSOukaG",
        name="Arnold",
        category="premade",
        description="Strong, confident male voice",
        language="en",
        gender="male"
    ),
    "adam": VoiceInfo(
        voice_id="pNInz6obpgDQGcFmaJgB",
        name="Adam",
        category="premade",
        description="Neutral, reliable male voice",
        language="en",
        gender="male"
    ),
    "sam": VoiceInfo(
        voice_id="yoZ06aMxZJJ28mfd3POQ",
        name="Sam",
        category="premade",
        description="Smooth, professional male voice",
        language="en",
        gender="male"
    )
}


# Voice style presets for different use cases
VOICE_STYLE_PRESETS = {
    "professional": {
        "primary": "rachel",
        "secondary": "drew",
        "description": "Business, formal tone"
    },
    "casual": {
        "primary": "bella",
        "secondary": "antoni",
        "description": "Friendly, relaxed conversation"
    },
    "dramatic": {
        "primary": "elli",
        "secondary": "josh",
        "description": "Expressive, theatrical delivery"
    },
    "authoritative": {
        "primary": "arnold",
        "secondary": "clyde",
        "description": "Strong, commanding presence"
    },
    "conversational": {
        "primary": "sam",
        "secondary": "adam",
        "description": "Natural, everyday speech"
    }
}


def get_voice_preset(voice_name: str) -> Optional[VoiceInfo]:
    """
    Get voice information for a popular voice preset.
    
    Args:
        voice_name: Name of the voice preset
        
    Returns:
        VoiceInfo object if found, None otherwise
    """
    return POPULAR_VOICES.get(voice_name.lower())


def get_voice_id(voice_name: str) -> Optional[str]:
    """
    Get voice ID for a popular voice preset.
    
    Args:
        voice_name: Name of the voice preset
        
    Returns:
        Voice ID string if found, None otherwise
    """
    voice_info = get_voice_preset(voice_name)
    return voice_info.voice_id if voice_info else None


def get_voices_by_gender(gender: str) -> List[VoiceInfo]:
    """
    Get all voices of a specific gender.
    
    Args:
        gender: Gender filter ("male", "female", "neutral")
        
    Returns:
        List of VoiceInfo objects matching the gender
    """
    return [voice for voice in POPULAR_VOICES.values() if voice.gender == gender.lower()]


def get_voice_style_preset(style: str) -> Optional[Dict[str, str]]:
    """
    Get voice style preset configuration.
    
    Args:
        style: Style name ("professional", "casual", "dramatic", etc.)
        
    Returns:
        Style configuration dictionary if found, None otherwise
    """
    return VOICE_STYLE_PRESETS.get(style.lower())


def list_available_voices() -> List[str]:
    """
    Get list of all available voice preset names.
    
    Returns:
        List of voice preset names
    """
    return list(POPULAR_VOICES.keys())


def list_voice_styles() -> List[str]:
    """
    Get list of all available voice style presets.
    
    Returns:
        List of voice style names
    """
    return list(VOICE_STYLE_PRESETS.keys())