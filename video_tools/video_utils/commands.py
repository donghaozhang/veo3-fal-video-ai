"""Command implementations for video and audio utilities.

This module serves as a central hub importing all command implementations
from specialized modules for better organization and maintainability.
"""

# Import all commands from specialized modules
from .video_commands import cmd_cut_videos
from .audio_commands import (
    cmd_add_audio,
    cmd_replace_audio,
    cmd_extract_audio,
    cmd_mix_audio,
    cmd_concat_audio
)
from .subtitle_commands import (
    cmd_generate_subtitles,
    cmd_burn_subtitles
)
from .ai_analysis_commands import (
    cmd_analyze_videos,
    cmd_transcribe_videos,
    cmd_describe_videos,
    cmd_analyze_audio,
    cmd_transcribe_audio,
    cmd_describe_audio,
    cmd_analyze_images,
    cmd_describe_images,
    cmd_extract_text
)
from .whisper_commands import (
    cmd_whisper_transcribe,
    cmd_whisper_compare,
    cmd_whisper_batch
)

# All command functions are now imported from their respective modules
# This file serves as a central import hub for backward compatibility