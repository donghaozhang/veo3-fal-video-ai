"""
Video utilities package for video and audio manipulation.

This package provides modular utilities for:
- Video processing and cutting
- Audio manipulation and mixing
- Subtitle generation and overlay
- File format support and validation
"""

from .core import check_ffmpeg, check_ffprobe, get_video_info
from .file_utils import find_video_files, find_audio_files
from .video_processor import cut_video_duration
from .audio_processor import (
    add_audio_to_video, 
    extract_audio_from_video, 
    mix_multiple_audio_files, 
    concatenate_multiple_audio_files
)
from .subtitle_generator import (
    generate_srt_subtitle_file,
    generate_vtt_subtitle_file,
    generate_subtitle_for_video,
    add_subtitles_to_video,
    add_text_subtitles_to_video
)
from .interactive import interactive_audio_selection, interactive_multiple_audio_selection
from .video_understanding import (
    check_gemini_requirements,
    analyze_video_file,
    analyze_audio_file,
    save_analysis_result,
    GeminiVideoAnalyzer
)

__all__ = [
    # Core utilities
    'check_ffmpeg', 'check_ffprobe', 'get_video_info',
    # File utilities
    'find_video_files', 'find_audio_files',
    # Video processing
    'cut_video_duration',
    # Audio processing
    'add_audio_to_video', 'extract_audio_from_video', 
    'mix_multiple_audio_files', 'concatenate_multiple_audio_files',
    # Subtitle generation
    'generate_srt_subtitle_file', 'generate_vtt_subtitle_file',
    'generate_subtitle_for_video', 'add_subtitles_to_video', 'add_text_subtitles_to_video',
    # Interactive utilities
    'interactive_audio_selection', 'interactive_multiple_audio_selection',
    # Video understanding
    'check_gemini_requirements', 'analyze_video_file', 'analyze_audio_file', 'save_analysis_result', 'GeminiVideoAnalyzer'
]