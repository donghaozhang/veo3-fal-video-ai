"""
File discovery and management utilities.

Provides functions for finding video and audio files in directories.
"""

from pathlib import Path
from typing import List


def find_video_files(directory: Path) -> List[Path]:
    """Find all video files in directory."""
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}
    video_files = []
    
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            video_files.append(file_path)
    
    return sorted(video_files)


def find_audio_files(directory: Path) -> List[Path]:
    """Find all audio files in directory."""
    audio_extensions = {'.mp3', '.wav', '.aac', '.ogg', '.m4a', '.flac'}
    audio_files = []
    
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
            audio_files.append(file_path)
    
    return sorted(audio_files)