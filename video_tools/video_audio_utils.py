#!/usr/bin/env python3
"""
Video & Audio Utilities Script

This script provides multiple video and audio manipulation utilities:
1. Extract first N seconds from videos
2. Add audio to videos without audio (silent videos)
3. Replace audio in existing videos
4. Extract audio from videos

Requirements:
- ffmpeg must be installed and available in PATH
- Supports common video formats: .mp4, .avi, .mov, .mkv, .webm
- Supports common audio formats: .mp3, .wav, .aac, .ogg, .m4a

Usage:
    python video_audio_utils.py cut [duration]      # Cut first N seconds (default: 5)
    python video_audio_utils.py add-audio           # Add audio to silent videos
    python video_audio_utils.py replace-audio       # Replace existing audio
    python video_audio_utils.py extract-audio       # Extract audio from videos
    python video_audio_utils.py --help              # Show help

Author: AI Assistant
Date: 2024
"""

import os
import subprocess
import sys
import argparse
from pathlib import Path
from typing import List, Optional, Tuple

def check_ffmpeg():
    """Check if ffmpeg is available."""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_ffprobe():
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

def cut_video_duration(input_path: Path, output_path: Path, duration: int) -> bool:
    """Cut first N seconds from video using ffmpeg."""
    try:
        cmd = [
            'ffmpeg', '-i', str(input_path),
            '-t', str(duration),  # Duration in seconds
            '-c', 'copy',  # Copy streams without re-encoding (faster)
            '-avoid_negative_ts', 'make_zero',
            str(output_path),
            '-y'  # Overwrite output file if exists
        ]
        
        print(f"🎬 Processing: {input_path.name}")
        print(f"⏱️  Extracting first {duration} seconds...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success: {output_path.name}")
            return True
        else:
            print(f"❌ Error processing {input_path.name}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception processing {input_path.name}: {e}")
        return False

def add_audio_to_video(video_path: Path, audio_path: Path, output_path: Path, 
                      replace_audio: bool = False) -> bool:
    """Add audio to video using ffmpeg."""
    try:
        if replace_audio:
            # Replace existing audio
            cmd = [
                'ffmpeg', '-i', str(video_path), '-i', str(audio_path),
                '-c:v', 'copy',  # Copy video stream
                '-c:a', 'aac',   # Re-encode audio to AAC
                '-map', '0:v:0', # Map video from first input
                '-map', '1:a:0', # Map audio from second input
                '-shortest',     # Stop when shortest stream ends
                str(output_path),
                '-y'
            ]
        else:
            # Add audio to silent video
            cmd = [
                'ffmpeg', '-i', str(video_path), '-i', str(audio_path),
                '-c:v', 'copy',  # Copy video stream
                '-c:a', 'aac',   # Encode audio to AAC
                '-shortest',     # Stop when shortest stream ends
                str(output_path),
                '-y'
            ]
        
        action = "Replacing" if replace_audio else "Adding"
        print(f"🎵 {action} audio: {audio_path.name} → {video_path.name}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success: {output_path.name}")
            return True
        else:
            print(f"❌ Error processing {video_path.name}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception processing {video_path.name}: {e}")
        return False

def extract_audio_from_video(video_path: Path, output_path: Path) -> bool:
    """Extract audio from video using ffmpeg."""
    try:
        cmd = [
            'ffmpeg', '-i', str(video_path),
            '-vn',           # No video
            '-c:a', 'mp3',   # Audio codec MP3
            '-ab', '192k',   # Audio bitrate
            str(output_path),
            '-y'
        ]
        
        print(f"🎵 Extracting audio: {video_path.name} → {output_path.name}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success: {output_path.name}")
            return True
        else:
            print(f"❌ Error extracting audio from {video_path.name}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception processing {video_path.name}: {e}")
        return False

def interactive_audio_selection(audio_files: List[Path]) -> Optional[Path]:
    """Interactive audio file selection."""
    if not audio_files:
        print("❌ No audio files found in current directory")
        return None
    
    print("\n🎵 Available audio files:")
    for i, audio in enumerate(audio_files, 1):
        print(f"   {i}. {audio.name}")
    
    while True:
        try:
            choice = input(f"\n🔢 Select audio file (1-{len(audio_files)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(audio_files):
                return audio_files[index]
            else:
                print(f"❌ Invalid choice. Please enter 1-{len(audio_files)}")
        except ValueError:
            print("❌ Invalid input. Please enter a number")
        except KeyboardInterrupt:
            print("\n👋 Cancelled by user")
            return None

def cmd_cut_videos(duration: int):
    """Cut first N seconds from all videos."""
    print(f"✂️  VIDEO CUTTER - First {duration} Seconds Extractor")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s)")
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Check video duration
        info = get_video_info(video_path)
        if info['duration'] is None:
            print(f"⚠️  Warning: Could not determine duration of {video_path.name}")
        elif info['duration'] < duration:
            print(f"⚠️  Warning: Video is only {info['duration']:.1f}s long (less than {duration}s)")
        else:
            print(f"📏 Duration: {info['duration']:.1f} seconds")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_first_{duration}s{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Cut the video
        if cut_video_duration(video_path, output_path, duration):
            successful += 1
            
            # Show file sizes
            input_size = video_path.stat().st_size / (1024 * 1024)  # MB
            output_size = output_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 Input: {input_size:.1f} MB → Output: {output_size:.1f} MB")
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")

def cmd_add_audio():
    """Add audio to silent videos."""
    print("🎵 ADD AUDIO TO SILENT VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    audio_files = find_audio_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    if not audio_files:
        print("📁 No audio files found in current directory")
        print("💡 Add some audio files (.mp3, .wav, .aac, etc.) to the current directory")
        return
    
    # Find silent videos
    silent_videos = []
    for video in video_files:
        info = get_video_info(video)
        if not info['has_audio']:
            silent_videos.append(video)
    
    if not silent_videos:
        print("📹 No silent videos found")
        print("💡 All videos already have audio. Use 'replace-audio' to replace existing audio")
        return
    
    print(f"🔇 Found {len(silent_videos)} silent video(s):")
    for video in silent_videos:
        print(f"   - {video.name}")
    
    # Select audio file
    selected_audio = interactive_audio_selection(audio_files)
    if not selected_audio:
        return
    
    print(f"\n🎵 Using audio: {selected_audio.name}")
    
    successful = 0
    failed = 0
    
    for video_path in silent_videos:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_with_audio{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Add audio to video
        if add_audio_to_video(video_path, selected_audio, output_path, replace_audio=False):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")

def cmd_replace_audio():
    """Replace audio in videos."""
    print("🔄 REPLACE AUDIO IN VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    audio_files = find_audio_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    if not audio_files:
        print("📁 No audio files found in current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s)")
    
    # Select audio file
    selected_audio = interactive_audio_selection(audio_files)
    if not selected_audio:
        return
    
    print(f"\n🎵 Using audio: {selected_audio.name}")
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_new_audio{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Replace audio in video
        if add_audio_to_video(video_path, selected_audio, output_path, replace_audio=True):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")

def cmd_extract_audio():
    """Extract audio from videos."""
    print("🎵 EXTRACT AUDIO FROM VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    # Find videos with audio
    videos_with_audio = []
    for video in video_files:
        info = get_video_info(video)
        if info['has_audio']:
            videos_with_audio.append(video)
    
    if not videos_with_audio:
        print("📹 No videos with audio found")
        return
    
    print(f"🎵 Found {len(videos_with_audio)} video(s) with audio:")
    for video in videos_with_audio:
        print(f"   - {video.name}")
    
    successful = 0
    failed = 0
    
    for video_path in videos_with_audio:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        output_path = video_path.parent / f"{stem}_audio.mp3"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Extract audio from video
        if extract_audio_from_video(video_path, output_path):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")

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

Requirements:
  - ffmpeg must be installed and available in PATH
  - Video files and audio files in current directory
        """
    )
    
    parser.add_argument('command', 
                       choices=['cut', 'add-audio', 'replace-audio', 'extract-audio'],
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
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 