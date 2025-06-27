"""
Input Validation Utilities

Validation functions for user inputs and API parameters.
"""

from typing import Union, List, Dict, Any
from ..models.common import VoiceSettings, ElevenLabsModel, AudioFormat


def validate_voice_settings(settings: VoiceSettings) -> tuple[bool, str]:
    """
    Validate voice settings parameters.
    
    Args:
        settings: VoiceSettings object to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(settings, VoiceSettings):
        return False, "Settings must be a VoiceSettings object"
    
    # Validate stability (0.0 - 1.0)
    if not (0.0 <= settings.stability <= 1.0):
        return False, "Stability must be between 0.0 and 1.0"
    
    # Validate similarity_boost (0.0 - 1.0)
    if not (0.0 <= settings.similarity_boost <= 1.0):
        return False, "Similarity boost must be between 0.0 and 1.0"
    
    # Validate style (0.0 - 1.0)
    if not (0.0 <= settings.style <= 1.0):
        return False, "Style must be between 0.0 and 1.0"
    
    # Validate use_speaker_boost (boolean)
    if not isinstance(settings.use_speaker_boost, bool):
        return False, "Use speaker boost must be a boolean"
    
    return True, ""


def validate_text_input(text: str, max_length: int = 40000) -> tuple[bool, str]:
    """
    Validate text input for TTS.
    
    Args:
        text: Text to validate
        max_length: Maximum allowed text length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(text, str):
        return False, "Text must be a string"
    
    if not text.strip():
        return False, "Text cannot be empty"
    
    if len(text) > max_length:
        return False, f"Text length ({len(text)}) exceeds maximum ({max_length})"
    
    return True, ""


def validate_speed(speed: float) -> tuple[bool, str]:
    """
    Validate speed parameter.
    
    Args:
        speed: Speed multiplier to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(speed, (int, float)):
        return False, "Speed must be a number"
    
    if not (0.25 <= speed <= 4.0):
        return False, "Speed must be between 0.25 and 4.0"
    
    return True, ""


def validate_model(model: Union[str, ElevenLabsModel]) -> tuple[bool, str]:
    """
    Validate model parameter.
    
    Args:
        model: Model to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if isinstance(model, str):
        # Check if string matches any enum value
        valid_models = [m.value for m in ElevenLabsModel]
        if model not in valid_models:
            return False, f"Invalid model '{model}'. Valid models: {valid_models}"
    elif isinstance(model, ElevenLabsModel):
        # Enum is always valid
        pass
    else:
        return False, "Model must be a string or ElevenLabsModel enum"
    
    return True, ""


def validate_audio_format(audio_format: Union[str, AudioFormat]) -> tuple[bool, str]:
    """
    Validate audio format parameter.
    
    Args:
        audio_format: Audio format to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if isinstance(audio_format, str):
        # Check if string matches any enum value
        valid_formats = [f.value for f in AudioFormat]
        if audio_format not in valid_formats:
            return False, f"Invalid audio format '{audio_format}'. Valid formats: {valid_formats}"
    elif isinstance(audio_format, AudioFormat):
        # Enum is always valid
        pass
    else:
        return False, "Audio format must be a string or AudioFormat enum"
    
    return True, ""


def validate_voice_id(voice_id: str) -> tuple[bool, str]:
    """
    Validate voice ID parameter.
    
    Args:
        voice_id: Voice ID to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(voice_id, str):
        return False, "Voice ID must be a string"
    
    if not voice_id.strip():
        return False, "Voice ID cannot be empty"
    
    # Basic format check - ElevenLabs voice IDs are typically 20 characters
    if len(voice_id) < 10:
        return False, "Voice ID appears to be invalid (too short)"
    
    return True, ""


def validate_dialogue_inputs(inputs: List[Dict[str, Any]]) -> tuple[bool, str]:
    """
    Validate dialogue inputs for multi-speaker generation.
    
    Args:
        inputs: List of dialogue inputs to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(inputs, list):
        return False, "Inputs must be a list"
    
    if not inputs:
        return False, "Inputs list cannot be empty"
    
    for i, input_item in enumerate(inputs):
        if not isinstance(input_item, dict):
            return False, f"Input {i} must be a dictionary"
        
        # Required fields
        if "text" not in input_item:
            return False, f"Input {i} missing required 'text' field"
        
        if "voice_id" not in input_item:
            return False, f"Input {i} missing required 'voice_id' field"
        
        # Validate text
        is_valid, error = validate_text_input(input_item["text"])
        if not is_valid:
            return False, f"Input {i} text validation failed: {error}"
        
        # Validate voice_id
        is_valid, error = validate_voice_id(input_item["voice_id"])
        if not is_valid:
            return False, f"Input {i} voice_id validation failed: {error}"
    
    return True, ""