"""
Parameter validation utilities for FAL Image-to-Image models
"""

from typing import Union
from ..config.constants import (
    SUPPORTED_MODELS, ASPECT_RATIOS, KONTEXT_MULTI_ASPECT_RATIOS,
    PHOTON_STRENGTH_RANGE, KONTEXT_INFERENCE_STEPS_RANGE, 
    KONTEXT_GUIDANCE_SCALE_RANGE, SEEDEDIT_GUIDANCE_SCALE_RANGE
)


def validate_model(model: str) -> str:
    """
    Validate and return the model type.
    
    Args:
        model: Model type string
        
    Returns:
        Validated model type
        
    Raises:
        ValueError: If model is not supported
    """
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model: {model}. Supported models: {SUPPORTED_MODELS}")
    return model


def validate_aspect_ratio(aspect_ratio: str, model: str = "photon") -> str:
    """
    Validate and return the aspect ratio.
    
    Args:
        aspect_ratio: Aspect ratio string
        model: Model type ("photon", "kontext", etc.)
        
    Returns:
        Validated aspect ratio
        
    Raises:
        ValueError: If aspect ratio is not supported for the model
    """
    if model in ["photon", "photon_base"]:
        if aspect_ratio not in ASPECT_RATIOS:
            raise ValueError(f"Unsupported aspect ratio for Photon models: {aspect_ratio}. Supported ratios: {ASPECT_RATIOS}")
    elif model == "kontext":
        # Kontext uses resolution_mode instead of aspect_ratio
        valid_modes = ["auto", "match_input"]
        if aspect_ratio not in valid_modes:
            raise ValueError(f"Unsupported resolution mode for Kontext: {aspect_ratio}. Supported modes: {valid_modes}")
    elif model == "kontext_multi":
        if aspect_ratio not in KONTEXT_MULTI_ASPECT_RATIOS:
            raise ValueError(f"Unsupported aspect ratio for Kontext Multi: {aspect_ratio}. Supported ratios: {KONTEXT_MULTI_ASPECT_RATIOS}")
    
    return aspect_ratio


def validate_strength(strength: float) -> float:
    """
    Validate and return the modification strength (Photon only).
    
    Args:
        strength: Modification strength (0-1)
        
    Returns:
        Validated strength value
        
    Raises:
        ValueError: If strength is not in valid range
    """
    min_val, max_val = PHOTON_STRENGTH_RANGE
    if not min_val <= strength <= max_val:
        raise ValueError(f"Strength must be between {min_val} and {max_val}, got: {strength}")
    return strength


def validate_inference_steps(steps: int) -> int:
    """
    Validate and return inference steps (Kontext only).
    
    Args:
        steps: Number of inference steps (1-50)
        
    Returns:
        Validated steps value
        
    Raises:
        ValueError: If steps is not in valid range
    """
    min_val, max_val = KONTEXT_INFERENCE_STEPS_RANGE
    if not min_val <= steps <= max_val:
        raise ValueError(f"Inference steps must be between {min_val} and {max_val}, got: {steps}")
    return steps


def validate_guidance_scale(scale: float, model: str = "kontext") -> float:
    """
    Validate and return guidance scale.
    
    Args:
        scale: Guidance scale value
        model: Model type to determine valid range
        
    Returns:
        Validated scale value
        
    Raises:
        ValueError: If scale is not in valid range
    """
    if model == "seededit":
        min_val, max_val = SEEDEDIT_GUIDANCE_SCALE_RANGE
    else:  # kontext
        min_val, max_val = KONTEXT_GUIDANCE_SCALE_RANGE
    
    if not min_val <= scale <= max_val:
        raise ValueError(f"Guidance scale for {model} must be between {min_val} and {max_val}, got: {scale}")
    return scale


def validate_num_images(num_images: int, max_images: int = 10) -> int:
    """
    Validate number of images to generate.
    
    Args:
        num_images: Number of images to generate
        max_images: Maximum allowed images
        
    Returns:
        Validated number
        
    Raises:
        ValueError: If number is not in valid range
    """
    if not 1 <= num_images <= max_images:
        raise ValueError(f"Number of images must be between 1 and {max_images}, got: {num_images}")
    return num_images


def validate_safety_tolerance(tolerance: int) -> int:
    """
    Validate safety tolerance level.
    
    Args:
        tolerance: Safety tolerance level (1-6)
        
    Returns:
        Validated tolerance level
        
    Raises:
        ValueError: If tolerance is not in valid range
    """
    if not 1 <= tolerance <= 6:
        raise ValueError(f"Safety tolerance must be between 1 and 6, got: {tolerance}")
    return tolerance


def validate_output_format(format_str: str) -> str:
    """
    Validate output format.
    
    Args:
        format_str: Output format ("jpeg" or "png")
        
    Returns:
        Validated format string
        
    Raises:
        ValueError: If format is not supported
    """
    valid_formats = ["jpeg", "png"]
    if format_str not in valid_formats:
        raise ValueError(f"Output format must be one of {valid_formats}, got: {format_str}")
    return format_str