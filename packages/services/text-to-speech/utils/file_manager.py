"""
File Management Utilities

File operations and management utilities for the text-to-speech package.
"""

import os
import io
from pathlib import Path
from typing import Union, Optional


def ensure_output_dir(output_path: Union[str, Path]) -> Path:
    """
    Ensure the output directory exists for the given file path.
    
    Args:
        output_path: Path to the output file
        
    Returns:
        Path object for the output file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def save_audio_file(audio_data: bytes, output_path: Union[str, Path]) -> bool:
    """
    Save audio data to file.
    
    Args:
        audio_data: Audio data bytes
        output_path: Path to save the audio file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        output_path = ensure_output_dir(output_path)
        
        with open(output_path, 'wb') as f:
            f.write(audio_data)
        
        return True
    except Exception as e:
        print(f"Error saving audio file: {e}")
        return False


def get_output_path(base_dir: str = "output", filename: str = "output.mp3") -> Path:
    """
    Get a standardized output path for audio files.
    
    Args:
        base_dir: Base directory for output files
        filename: Name of the output file
        
    Returns:
        Path object for the output file
    """
    return Path(base_dir) / filename


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """
    Validate that a filename has an allowed extension.
    
    Args:
        filename: Name of the file to validate
        allowed_extensions: List of allowed extensions (e.g., ['.mp3', '.wav'])
        
    Returns:
        True if extension is allowed, False otherwise
    """
    file_path = Path(filename)
    return file_path.suffix.lower() in [ext.lower() for ext in allowed_extensions]


def get_file_size(file_path: Union[str, Path]) -> Optional[int]:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes, or None if file doesn't exist
    """
    try:
        return Path(file_path).stat().st_size
    except (OSError, FileNotFoundError):
        return None