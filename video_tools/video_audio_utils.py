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
7. AI-powered video understanding with Google Gemini

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
import os
from pathlib import Path

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    # Load .env from the script's directory
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, environment variables can still be set manually
    pass

from video_utils.core import check_ffmpeg, check_ffprobe
from video_utils.commands import (
    cmd_cut_videos,
    cmd_add_audio,
    cmd_replace_audio,
    cmd_extract_audio,
    cmd_mix_audio,
    cmd_concat_audio,
    cmd_generate_subtitles,
    cmd_burn_subtitles,
    cmd_analyze_videos,
    cmd_transcribe_videos,
    cmd_describe_videos,
    cmd_analyze_audio,
    cmd_transcribe_audio,
    cmd_describe_audio,
    cmd_analyze_images,
    cmd_describe_images,
    cmd_extract_text,
    cmd_whisper_transcribe,
    cmd_whisper_compare,
    cmd_whisper_batch
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
  python video_audio_utils.py analyze-videos      # AI-powered video analysis with Google Gemini
  python video_audio_utils.py transcribe-videos   # AI transcription of video audio
  python video_audio_utils.py describe-videos     # AI description and summarization
  python video_audio_utils.py analyze-audio       # AI-powered audio analysis with Google Gemini
  python video_audio_utils.py transcribe-audio    # AI transcription of audio files
  python video_audio_utils.py describe-audio      # AI description of audio content
  python video_audio_utils.py analyze-images      # AI-powered image analysis with Google Gemini
  python video_audio_utils.py describe-images     # AI description of images
  python video_audio_utils.py extract-text        # Extract text from images (OCR)
  python video_audio_utils.py whisper-transcribe  # Transcribe with OpenAI Whisper (API or local)
  python video_audio_utils.py whisper-compare     # Compare Whisper vs Gemini transcription
  python video_audio_utils.py whisper-batch       # Batch Whisper transcription with advanced options

Requirements:
  - ffmpeg must be installed and available in PATH
  - Video files, audio files, and image files in current directory
  - For mix-audio and concat-audio: at least 2 audio files needed
        """
    )
    
    parser.add_argument('command', 
                       choices=['cut', 'add-audio', 'replace-audio', 'extract-audio', 'mix-audio', 'concat-audio', 'generate-subtitles', 'burn-subtitles', 'analyze-videos', 'transcribe-videos', 'describe-videos', 'analyze-audio', 'transcribe-audio', 'describe-audio', 'analyze-images', 'describe-images', 'extract-text', 'whisper-transcribe', 'whisper-compare', 'whisper-batch'],
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
        elif args.command == 'analyze-videos':
            cmd_analyze_videos()
        elif args.command == 'transcribe-videos':
            cmd_transcribe_videos()
        elif args.command == 'describe-videos':
            cmd_describe_videos()
        elif args.command == 'analyze-audio':
            cmd_analyze_audio()
        elif args.command == 'transcribe-audio':
            cmd_transcribe_audio()
        elif args.command == 'describe-audio':
            cmd_describe_audio()
        elif args.command == 'analyze-images':
            cmd_analyze_images()
        elif args.command == 'describe-images':
            cmd_describe_images()
        elif args.command == 'extract-text':
            cmd_extract_text()
        elif args.command == 'whisper-transcribe':
            cmd_whisper_transcribe()
        elif args.command == 'whisper-compare':
            cmd_whisper_compare()
        elif args.command == 'whisper-batch':
            cmd_whisper_batch()
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()