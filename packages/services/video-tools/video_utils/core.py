"""
Core utilities for video and audio processing.

Provides basic functionality like ffmpeg checks and video information extraction.
"""

import subprocess
from pathlib import Path


def check_ffmpeg() -> bool:
    """Check if ffmpeg is available."""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_ffprobe() -> bool:
    """Check if ffprobe is available."""
    try:
        subprocess.run(['ffprobe', '-version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_video_info(video_path: Path) -> dict:
    """Get video information using ffprobe."""
    try:
        # Get general info
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 
            'format=duration', '-of', 'csv=p=0', str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        
        # Check for audio stream
        cmd_audio = [
            'ffprobe', '-v', 'error', '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', str(video_path)
        ]
        result_audio = subprocess.run(cmd_audio, capture_output=True, text=True)
        has_audio = bool(result_audio.stdout.strip())
        
        return {
            'duration': duration,
            'has_audio': has_audio,
            'audio_codec': result_audio.stdout.strip() if has_audio else None
        }
    except (subprocess.CalledProcessError, ValueError):
        return {'duration': None, 'has_audio': False, 'audio_codec': None}