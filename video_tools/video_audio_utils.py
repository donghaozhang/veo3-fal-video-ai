#!/usr/bin/env python3
"""
Video & Audio Utilities Script - Enhanced Version with CLI Parameters

This script provides multiple video and audio manipulation utilities with enhanced
command-line parameter support, specifically for the describe-videos command.

New Features:
- Support for -i, -o, -f parameters in describe-videos command
- Backward compatibility with existing commands
- Enhanced argument parsing for specific commands

Usage:
    python video_audio_utils.py describe-videos -i video_input_path -o output_path -f describe-video
    python video_audio_utils.py cut [duration]         # Cut first N seconds (default: 5)
    python video_audio_utils.py add-audio             # Add audio to silent videos
    python video_audio_utils.py replace-audio         # Replace existing audio
    python video_audio_utils.py extract-audio         # Extract audio from videos
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

# Add video_utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

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


def cmd_describe_videos_enhanced(input_path=None, output_path=None, format_type=None):
    """Enhanced describe-videos command with parameter support."""
    from video_utils.ai_analysis_commands import cmd_describe_videos_with_params
    return cmd_describe_videos_with_params(input_path, output_path, format_type)


def cmd_transcribe_videos_enhanced(input_path=None, output_path=None, format_type=None):
    """Enhanced transcribe-videos command with parameter support."""
    from video_utils.ai_analysis_commands import cmd_transcribe_videos_with_params
    return cmd_transcribe_videos_with_params(input_path, output_path, format_type)


def cmd_generate_subtitles_enhanced(input_path=None, output_path=None, format_type=None):
    """Enhanced generate-subtitles command with parameter support."""
    from video_utils.subtitle_commands import cmd_generate_subtitles_with_params
    return cmd_generate_subtitles_with_params(input_path, output_path, format_type)


def cmd_analyze_audio_enhanced(input_path=None, output_path=None, format_type=None):
    """Enhanced analyze-audio command with parameter support."""
    from video_utils.ai_analysis_commands import cmd_analyze_audio_with_params
    return cmd_analyze_audio_with_params(input_path, output_path, format_type)


def create_parser():
    """Create argument parser with enhanced support for describe-videos."""
    parser = argparse.ArgumentParser(
        description="Video & Audio Utilities - Multiple video/audio manipulation tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Enhanced describe-videos with parameters
  python video_audio_utils.py describe-videos -i video.mp4 -o output.json -f describe-video
  python video_audio_utils.py describe-videos -i /path/to/video.mp4 -o /path/to/output.json
  python video_audio_utils.py describe-videos -i input_dir/ -o output_dir/
  
  # Enhanced generate-subtitles with parameters
  python video_audio_utils.py generate-subtitles -i video.mp4 -o subtitle.srt
  python video_audio_utils.py generate-subtitles -i video.mp4 -o output/ -f vtt
  python video_audio_utils.py generate-subtitles -i input_dir/ -o output_dir/ -f srt
  
  # Enhanced analyze-audio with parameters
  python video_audio_utils.py analyze-audio -i audio.mp3 -o analysis.json
  python video_audio_utils.py analyze-audio -i audio.mp3 -o output/ -f txt
  python video_audio_utils.py analyze-audio -i input_dir/ -o output_dir/ -f json
  
  # Traditional commands
  python video_audio_utils.py cut              # Cut first 5 seconds from all videos
  python video_audio_utils.py cut 10           # Cut first 10 seconds from all videos
  python video_audio_utils.py add-audio        # Add audio to silent videos
  python video_audio_utils.py replace-audio    # Replace audio in videos
  python video_audio_utils.py extract-audio    # Extract audio from videos
  python video_audio_utils.py analyze-videos   # AI-powered video analysis with Google Gemini
  python video_audio_utils.py transcribe-videos # AI transcription of video audio
  python video_audio_utils.py describe-videos  # AI description (traditional mode - all files in input/)
  python video_audio_utils.py generate-subtitles # Subtitle generation (traditional mode - all files in input/)

Requirements:
  - ffmpeg must be installed and available in PATH
  - For AI commands: GEMINI_API_KEY environment variable required
  - Video files, audio files, and image files accessible
        """
    )
    
    # Define the command choices
    command_choices = [
        'cut', 'add-audio', 'replace-audio', 'extract-audio', 'mix-audio', 
        'concat-audio', 'generate-subtitles', 'burn-subtitles', 'analyze-videos', 
        'transcribe-videos', 'describe-videos', 'analyze-audio', 'transcribe-audio', 
        'describe-audio', 'analyze-images', 'describe-images', 'extract-text', 
        'whisper-transcribe', 'whisper-compare', 'whisper-batch'
    ]
    
    parser.add_argument('command', choices=command_choices, help='Command to execute')
    parser.add_argument('duration', type=int, nargs='?', default=5,
                       help='Duration in seconds for cut command (default: 5)')
    
    # Enhanced parameters for describe-videos, transcribe-videos, generate-subtitles, and analyze-audio commands
    parser.add_argument('-i', '--input', type=str,
                       help='Input video/audio file or directory path (for describe-videos, transcribe-videos, generate-subtitles, analyze-audio)')
    parser.add_argument('-o', '--output', type=str,
                       help='Output file or directory path (for describe-videos, transcribe-videos, generate-subtitles, analyze-audio)')
    parser.add_argument('-f', '--format', type=str, choices=['describe-video', 'json', 'txt', 'srt', 'vtt'],
                       default='describe-video',
                       help='Output format: describe-video/json/txt (for AI commands) or srt/vtt (for generate-subtitles)')
    
    return parser


def main():
    """Main function with enhanced command line argument parsing."""
    parser = create_parser()
    
    # Handle no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Special handling for describe-videos command with parameters
    if args.command == 'describe-videos' and (args.input or args.output or args.format != 'describe-video'):
        print("🎬 Enhanced describe-videos mode with parameters")
        print(f"📁 Input: {args.input or 'current directory/input'}")
        print(f"📁 Output: {args.output or 'current directory/output'}")
        print(f"📋 Format: {args.format}")
        print()
        
        try:
            return cmd_describe_videos_enhanced(args.input, args.output, args.format)
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled by user")
        except Exception as e:
            print(f"\n❌ Error in enhanced describe-videos: {e}")
            sys.exit(1)
    
    # Special handling for transcribe-videos command with parameters
    if args.command == 'transcribe-videos' and (args.input or args.output or args.format != 'describe-video'):
        print("🎤 Enhanced transcribe-videos mode with parameters")
        print(f"📁 Input: {args.input or 'current directory/input'}")
        print(f"📁 Output: {args.output or 'current directory/output'}")
        print(f"📋 Format: {args.format}")
        print()
        
        try:
            return cmd_transcribe_videos_enhanced(args.input, args.output, args.format)
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled by user")
        except Exception as e:
            print(f"\n❌ Error in enhanced transcribe-videos: {e}")
            sys.exit(1)
    
    # Special handling for generate-subtitles command with parameters
    if args.command == 'generate-subtitles' and (args.input or args.output or args.format):
        print("📝 Enhanced generate-subtitles mode with parameters")
        print(f"📁 Input: {args.input or 'current directory/input'}")
        print(f"📁 Output: {args.output or 'current directory/output'}")
        if args.format in ['srt', 'vtt']:
            print(f"📋 Format: {args.format}")
        else:
            print("📋 Format: interactive selection")
        print()
        
        try:
            # Map format parameter for subtitles (srt/vtt instead of describe-video/json/txt)
            subtitle_format = args.format if args.format in ['srt', 'vtt'] else None
            return cmd_generate_subtitles_enhanced(args.input, args.output, subtitle_format)
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled by user")
        except Exception as e:
            print(f"\n❌ Error in enhanced generate-subtitles: {e}")
            sys.exit(1)
    
    # Special handling for analyze-audio command with parameters
    if args.command == 'analyze-audio' and (args.input or args.output or args.format != 'describe-video'):
        print("🔊 Enhanced analyze-audio mode with parameters")
        print(f"📁 Input: {args.input or 'current directory/input'}")
        print(f"📁 Output: {args.output or 'current directory/output'}")
        if args.format in ['json', 'txt']:
            print(f"📋 Format: {args.format}")
        else:
            print("📋 Format: interactive selection")
        print()
        
        try:
            # Map format parameter for audio analysis (json/txt instead of describe-video)
            audio_format = args.format if args.format in ['json', 'txt'] else 'json'
            return cmd_analyze_audio_enhanced(args.input, args.output, audio_format)
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled by user")
        except Exception as e:
            print(f"\n❌ Error in enhanced analyze-audio: {e}")
            sys.exit(1)
    
    # Check ffmpeg availability for commands that need it
    ffmpeg_commands = ['cut', 'add-audio', 'replace-audio', 'extract-audio', 'mix-audio', 
                      'concat-audio', 'generate-subtitles', 'burn-subtitles']
    
    if args.command in ffmpeg_commands:
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
            # Traditional mode - no parameters provided
            from video_utils.ai_analysis_commands import cmd_describe_videos
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