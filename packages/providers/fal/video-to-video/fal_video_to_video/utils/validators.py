"""
Parameter validation utilities for FAL Video to Video models
"""

import os
from typing import Optional, Union
from urllib.parse import urlparse
from ..config.constants import (
    SUPPORTED_MODELS, MAX_VIDEO_SIZE_MB, MAX_VIDEO_DURATION_SECONDS
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


def validate_video_url(video_url: str) -> str:
    """
    Validate video URL.
    
    Args:
        video_url: URL of the video
        
    Returns:
        Validated video URL
        
    Raises:
        ValueError: If URL is invalid
    """
    try:
        result = urlparse(video_url)
        if not all([result.scheme, result.netloc]):
            raise ValueError("Invalid URL format")
        if result.scheme not in ['http', 'https']:
            raise ValueError("URL must use HTTP or HTTPS protocol")
        return video_url
    except Exception as e:
        raise ValueError(f"Invalid video URL: {e}")


def validate_video_path(video_path: str) -> str:
    """
    Validate local video file path.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Validated video path
        
    Raises:
        ValueError: If path is invalid or file doesn't exist
    """
    if not os.path.exists(video_path):
        raise ValueError(f"Video file not found: {video_path}")
    
    if not os.path.isfile(video_path):
        raise ValueError(f"Path is not a file: {video_path}")
    
    # Check file extension
    valid_extensions = ['.mp4', '.mov', '.avi', '.webm']
    ext = os.path.splitext(video_path)[1].lower()
    if ext not in valid_extensions:
        raise ValueError(f"Unsupported video format: {ext}. Supported: {valid_extensions}")
    
    # Check file size
    file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
    if file_size_mb > MAX_VIDEO_SIZE_MB:
        raise ValueError(f"Video file too large: {file_size_mb:.1f}MB. Maximum: {MAX_VIDEO_SIZE_MB}MB")
    
    return video_path


def validate_prompt(prompt: Optional[str]) -> Optional[str]:
    """
    Validate and return the prompt.
    
    Args:
        prompt: Text prompt for audio generation
        
    Returns:
        Validated prompt or None
        
    Raises:
        ValueError: If prompt is invalid
    """
    if prompt is None:
        return None
    
    if not isinstance(prompt, str):
        raise ValueError("Prompt must be a string")
    
    prompt = prompt.strip()
    if len(prompt) == 0:
        return None
    
    if len(prompt) > 1000:
        raise ValueError("Prompt too long. Maximum 1000 characters")
    
    return prompt


def validate_seed(seed: Optional[int]) -> Optional[int]:
    """
    Validate random seed.
    
    Args:
        seed: Random seed value
        
    Returns:
        Validated seed or None
        
    Raises:
        ValueError: If seed is invalid
    """
    if seed is None:
        return None
    
    try:
        seed = int(seed)
        if seed < 0:
            raise ValueError("Seed must be non-negative")
        return seed
    except (ValueError, TypeError):
        raise ValueError("Seed must be an integer")


def validate_upscale_factor(upscale_factor: Union[int, float]) -> Union[int, float]:
    """
    Validate upscale factor for Topaz.
    
    Args:
        upscale_factor: Upscaling factor (1-4)
        
    Returns:
        Validated upscale factor
        
    Raises:
        ValueError: If factor is invalid
    """
    try:
        upscale_factor = float(upscale_factor)
        if not 1 <= upscale_factor <= 4:
            raise ValueError("Upscale factor must be between 1 and 4")
        return upscale_factor
    except (ValueError, TypeError):
        raise ValueError("Upscale factor must be a number")


def validate_target_fps(target_fps: Optional[int]) -> Optional[int]:
    """
    Validate target FPS for Topaz frame interpolation.
    
    Args:
        target_fps: Target frames per second
        
    Returns:
        Validated target FPS or None
        
    Raises:
        ValueError: If FPS is invalid
    """
    if target_fps is None:
        return None
    
    try:
        target_fps = int(target_fps)
        if not 1 <= target_fps <= 120:
            raise ValueError("Target FPS must be between 1 and 120")
        return target_fps
    except (ValueError, TypeError):
        raise ValueError("Target FPS must be an integer")