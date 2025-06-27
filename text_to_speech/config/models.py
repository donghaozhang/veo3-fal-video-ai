"""
Model Configuration Settings

Configuration settings and presets for different ElevenLabs models.
"""

from typing import Dict, Any
from ..models.common import ElevenLabsModel, VoiceSettings


# Default settings for each model type
DEFAULT_MODEL_SETTINGS = {
    ElevenLabsModel.ELEVEN_V3: {
        "max_characters": 10000,
        "languages": 70,
        "latency": "high",
        "quality": "highest",
        "features": ["dialogue", "emotional_range", "multi_speaker"],
        "recommended_for": ["audiobooks", "dramatic_content", "dialogue"]
    },
    ElevenLabsModel.MULTILINGUAL_V2: {
        "max_characters": 10000,
        "languages": 29,
        "latency": "medium",
        "quality": "highest",
        "features": ["multilingual", "high_quality", "stability"],
        "recommended_for": ["professional_narration", "multilingual_projects"]
    },
    ElevenLabsModel.FLASH_V2_5: {
        "max_characters": 40000,
        "languages": 32,
        "latency": "ultra_low",
        "quality": "good",
        "features": ["real_time", "cost_effective", "long_form"],
        "recommended_for": ["real_time_applications", "conversational_ai"]
    },
    ElevenLabsModel.TURBO_V2_5: {
        "max_characters": 40000,
        "languages": 32,
        "latency": "low",
        "quality": "high",
        "features": ["balanced", "streaming", "cost_effective"],
        "recommended_for": ["streaming_applications", "cost_effective_projects"]
    }
}


# Recommended voice settings for different use cases
VOICE_SETTINGS_PRESETS = {
    "conservative": VoiceSettings(
        stability=0.9,
        similarity_boost=0.8,
        style=0.1,
        use_speaker_boost=True
    ),
    "balanced": VoiceSettings(
        stability=0.5,
        similarity_boost=0.5,
        style=0.3,
        use_speaker_boost=True
    ),
    "creative": VoiceSettings(
        stability=0.3,
        similarity_boost=0.6,
        style=0.8,
        use_speaker_boost=True
    ),
    "expressive": VoiceSettings(
        stability=0.2,
        similarity_boost=0.4,
        style=0.9,
        use_speaker_boost=True
    ),
    "stable": VoiceSettings(
        stability=1.0,
        similarity_boost=0.9,
        style=0.0,
        use_speaker_boost=True
    )
}


def get_model_info(model: ElevenLabsModel) -> Dict[str, Any]:
    """
    Get detailed information about a specific model.
    
    Args:
        model: ElevenLabs model enum
        
    Returns:
        Dictionary with model information
    """
    return DEFAULT_MODEL_SETTINGS.get(model, {})


def get_recommended_model(use_case: str) -> ElevenLabsModel:
    """
    Get recommended model for a specific use case.
    
    Args:
        use_case: Use case description
        
    Returns:
        Recommended ElevenLabs model
    """
    use_case_lower = use_case.lower()
    
    if any(keyword in use_case_lower for keyword in ["real_time", "streaming", "fast", "low_latency"]):
        return ElevenLabsModel.FLASH_V2_5
    elif any(keyword in use_case_lower for keyword in ["dialogue", "conversation", "emotional", "dramatic"]):
        return ElevenLabsModel.ELEVEN_V3
    elif any(keyword in use_case_lower for keyword in ["multilingual", "professional", "high_quality"]):
        return ElevenLabsModel.MULTILINGUAL_V2
    else:
        return ElevenLabsModel.TURBO_V2_5  # Balanced default


def get_voice_settings_preset(preset_name: str) -> VoiceSettings:
    """
    Get voice settings for a specific preset.
    
    Args:
        preset_name: Name of the preset
        
    Returns:
        VoiceSettings object
    """
    return VOICE_SETTINGS_PRESETS.get(preset_name.lower(), VOICE_SETTINGS_PRESETS["balanced"])


def list_voice_settings_presets() -> list[str]:
    """
    Get list of available voice settings presets.
    
    Returns:
        List of preset names
    """
    return list(VOICE_SETTINGS_PRESETS.keys())


def get_model_character_limit(model: ElevenLabsModel) -> int:
    """
    Get character limit for a specific model.
    
    Args:
        model: ElevenLabs model enum
        
    Returns:
        Maximum character limit for the model
    """
    model_info = get_model_info(model)
    return model_info.get("max_characters", 10000)