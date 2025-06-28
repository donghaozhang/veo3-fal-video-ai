#!/usr/bin/env python3
"""
Video & Audio Utilities Script - Refactored Version

This script provides multiple video and audio manipulation utilities:
1. Extract first N seconds from videos
2. Add audio to videos without audio (silent videos)
3. Replace audio in existing videos
4. Extract audio from videos
5. Generate subtitle files (.srt/.vtt) for video players
6. Burn subtitles permanently into video files

Requirements:
- ffmpeg must be installed and available in PATH
- Supports common video formats: .mp4, .avi, .mov, .mkv, .webm
- Supports common audio formats: .mp3, .wav, .aac, .ogg, .m4a

Usage:
    python video_audio_utils.py cut [duration]         # Cut first N seconds (default: 5)
    python video_audio_utils.py add-audio             # Add audio to silent videos
    python video_audio_utils.py replace-audio         # Replace existing audio
    python video_audio_utils.py extract-audio         # Extract audio from videos
    python video_audio_utils.py mix-audio             # Mix multiple audio files and add to videos
    python video_audio_utils.py concat-audio          # Concatenate multiple audio files and add to videos
    python video_audio_utils.py generate-subtitles    # Generate .srt/.vtt subtitle files for video players
    python video_audio_utils.py burn-subtitles        # Burn subtitles permanently into video files
    python video_audio_utils.py --help                # Show help

Author: AI Assistant
Date: 2024
"""

import argparse
import sys

from video_utils.core import check_ffmpeg, check_ffprobe
from video_utils.commands import (
    cmd_cut_videos,
    cmd_add_audio,
    cmd_replace_audio,
    cmd_extract_audio,
    cmd_mix_audio,
    cmd_concat_audio,
    cmd_generate_subtitles,
    cmd_burn_subtitles
)


def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Video & Audio Utilities - Multiple video/audio manipulation tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python video_audio_utils.py cut              # Cut first 5 seconds from all videos
  python video_audio_utils.py cut 10           # Cut first 10 seconds from all videos
  python video_audio_utils.py add-audio        # Add audio to silent videos
  python video_audio_utils.py replace-audio    # Replace audio in videos
  python video_audio_utils.py extract-audio    # Extract audio from videos
  python video_audio_utils.py mix-audio           # Mix multiple audio files and add to videos
  python video_audio_utils.py concat-audio        # Concatenate multiple audio files and add to videos
  python video_audio_utils.py generate-subtitles  # Generate .srt/.vtt subtitle files for video players
  python video_audio_utils.py burn-subtitles      # Burn subtitles permanently into video files

Requirements:
  - ffmpeg must be installed and available in PATH
  - Video files and audio files in current directory
  - For mix-audio and concat-audio: at least 2 audio files needed
        """
    )
    
    parser.add_argument('command', 
                       choices=['cut', 'add-audio', 'replace-audio', 'extract-audio', 'mix-audio', 'concat-audio', 'generate-subtitles', 'burn-subtitles'],
                       help='Command to execute')
    parser.add_argument('duration', type=int, nargs='?', default=5,
                       help='Duration in seconds for cut command (default: 5)')
    
    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Check ffmpeg availability
    print("🔧 Checking requirements...")
    if not check_ffmpeg():
        print("❌ Error: ffmpeg is not installed or not in PATH")
        print("📥 Please install ffmpeg:")
        print("   - Windows: Download from https://ffmpeg.org/download.html")
        print("   - macOS: brew install ffmpeg")
        print("   - Linux: sudo apt install ffmpeg (Ubuntu/Debian)")
        sys.exit(1)
    
    if not check_ffprobe():
        print("❌ Error: ffprobe is not installed or not in PATH")
        print("📥 ffprobe is usually included with ffmpeg installation")
        sys.exit(1)
    
    print("✅ ffmpeg and ffprobe found")
    print()
    
    # Execute command
    try:
        if args.command == 'cut':
            cmd_cut_videos(args.duration)
        elif args.command == 'add-audio':
            cmd_add_audio()
        elif args.command == 'replace-audio':
            cmd_replace_audio()
        elif args.command == 'extract-audio':
            cmd_extract_audio()
        elif args.command == 'mix-audio':
            cmd_mix_audio()
        elif args.command == 'concat-audio':
            cmd_concat_audio()
        elif args.command == 'generate-subtitles':
            cmd_generate_subtitles()
        elif args.command == 'burn-subtitles':
            cmd_burn_subtitles()
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()