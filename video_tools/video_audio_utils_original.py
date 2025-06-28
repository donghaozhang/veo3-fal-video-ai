#!/usr/bin/env python3
"""
Video & Audio Utilities Script

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
    python video_audio_utils.py cut [duration]      # Cut first N seconds (default: 5)
    python video_audio_utils.py add-audio           # Add audio to silent videos
    python video_audio_utils.py replace-audio       # Replace existing audio
    python video_audio_utils.py extract-audio       # Extract audio from videos
    python video_audio_utils.py mix-audio           # Mix multiple audio files and add to videos
    python video_audio_utils.py concat-audio        # Concatenate multiple audio files and add to videos
    python video_audio_utils.py generate-subtitles  # Generate .srt/.vtt subtitle files for video players
    python video_audio_utils.py burn-subtitles      # Burn subtitles permanently into video files
    python video_audio_utils.py --help              # Show help

Author: AI Assistant
Date: 2024
"""

import subprocess
import sys
import argparse
from pathlib import Path
from typing import List, Optional

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

def mix_multiple_audio_files(audio_files: List[Path], output_path: Path, 
                           normalize: bool = True) -> bool:
    """Mix multiple audio files together using ffmpeg."""
    if len(audio_files) < 2:
        print("❌ Need at least 2 audio files to mix")
        return False
    
    try:
        # Build ffmpeg command for mixing multiple audio files
        cmd = ['ffmpeg']
        
        # Add input files
        for audio_file in audio_files:
            cmd.extend(['-i', str(audio_file)])
        
        # Build filter complex for mixing
        if normalize:
            # Normalize each input and then mix them
            filter_parts = []
            for i in range(len(audio_files)):
                filter_parts.append(f"[{i}:a]volume=1.0/{len(audio_files)}[a{i}]")
            
            # Mix all normalized inputs
            mix_inputs = ";".join(filter_parts)
            mix_part = "".join([f"[a{i}]" for i in range(len(audio_files))])
            filter_complex = f"{mix_inputs};{mix_part}amix=inputs={len(audio_files)}:duration=longest[out]"
        else:
            # Simple mix without normalization
            mix_part = "".join([f"[{i}:a]" for i in range(len(audio_files))])
            filter_complex = f"{mix_part}amix=inputs={len(audio_files)}:duration=longest[out]"
        
        cmd.extend([
            '-filter_complex', filter_complex,
            '-map', '[out]',
            '-c:a', 'mp3',
            '-ab', '192k',
            str(output_path),
            '-y'
        ])
        
        print(f"🎵 Mixing {len(audio_files)} audio files...")
        for audio in audio_files:
            print(f"   - {audio.name}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Mixed audio saved: {output_path.name}")
            return True
        else:
            print(f"❌ Error mixing audio files:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception mixing audio files: {e}")
        return False

def generate_srt_subtitle_file(text: str, output_path: Path, duration: Optional[float] = None, 
                             start_time: float = 0.0, words_per_second: float = 2.0) -> bool:
    """Generate SRT subtitle file from text for video players to load."""
    try:
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        subtitle_lines = []
        
        if duration is None:
            word_count = len(text.split())
            total_duration = word_count / words_per_second
        else:
            total_duration = duration
        
        time_per_line = total_duration / len(lines) if lines else 1.0
        
        for i, line in enumerate(lines):
            start = start_time + (i * time_per_line)
            end = start + time_per_line
            
            start_time_str = f"{int(start//3600):02d}:{int((start%3600)//60):02d}:{start%60:06.3f}".replace('.', ',')
            end_time_str = f"{int(end//3600):02d}:{int((end%3600)//60):02d}:{end%60:06.3f}".replace('.', ',')
            
            subtitle_lines.append(f"{i+1}")
            subtitle_lines.append(f"{start_time_str} --> {end_time_str}")
            subtitle_lines.append(line)
            subtitle_lines.append("")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(subtitle_lines))
        
        print(f"✅ SRT subtitle file created: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating SRT subtitle file: {e}")
        return False

def generate_vtt_subtitle_file(text: str, output_path: Path, duration: Optional[float] = None,
                             start_time: float = 0.0, words_per_second: float = 2.0) -> bool:
    """Generate WebVTT subtitle file from text for web players."""
    try:
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        subtitle_lines = ["WEBVTT", ""]
        
        if duration is None:
            word_count = len(text.split())
            total_duration = word_count / words_per_second
        else:
            total_duration = duration
        
        time_per_line = total_duration / len(lines) if lines else 1.0
        
        for i, line in enumerate(lines):
            start = start_time + (i * time_per_line)
            end = start + time_per_line
            
            start_time_str = f"{int(start//3600):02d}:{int((start%3600)//60):02d}:{start%60:06.3f}"
            end_time_str = f"{int(end//3600):02d}:{int((end%3600)//60):02d}:{end%60:06.3f}"
            
            subtitle_lines.append(f"{start_time_str} --> {end_time_str}")
            subtitle_lines.append(line)
            subtitle_lines.append("")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(subtitle_lines))
        
        print(f"✅ WebVTT subtitle file created: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating WebVTT subtitle file: {e}")
        return False

def generate_subtitle_for_video(video_path: Path, text: str, format_type: str = "srt",
                              words_per_second: float = 2.0) -> Optional[Path]:
    """Generate subtitle file for a specific video."""
    try:
        info = get_video_info(video_path)
        video_duration = info.get('duration', 10.0)
        
        if format_type.lower() == "vtt":
            subtitle_path = video_path.with_suffix('.vtt')
            success = generate_vtt_subtitle_file(text, subtitle_path, video_duration, 0.0, words_per_second)
        else:  # Default to SRT
            subtitle_path = video_path.with_suffix('.srt')
            success = generate_srt_subtitle_file(text, subtitle_path, video_duration, 0.0, words_per_second)
        
        if success:
            print(f"📝 Subtitle file for {video_path.name}: {subtitle_path.name}")
            return subtitle_path
        return None
        
    except Exception as e:
        print(f"❌ Error generating subtitle for {video_path.name}: {e}")
        return None

def add_subtitles_to_video(video_path: Path, subtitle_path: Path, output_path: Path,
                          font_size: int = 24, font_color: str = "white",
                          bg_color: str = "black") -> bool:
    """Add subtitles to video using ffmpeg."""
    try:
        cmd = [
            'ffmpeg', '-i', str(video_path),
            '-vf', f"subtitles={subtitle_path}:force_style='FontSize={font_size},PrimaryColour=&H{font_color.replace('#', '')},BackColour=&H{bg_color.replace('#', '')},BorderStyle=3,Outline=1,Shadow=1'",
            '-c:a', 'copy',
            str(output_path),
            '-y'
        ]
        
        print(f"📝 Adding subtitles: {subtitle_path.name} → {video_path.name}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success: {output_path.name}")
            return True
        else:
            print(f"❌ Error adding subtitles to {video_path.name}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception adding subtitles to {video_path.name}: {e}")
        return False

def add_text_subtitles_to_video(video_path: Path, text: str, output_path: Path,
                               font_size: int = 24, font_color: str = "white",
                               bg_color: str = "black", words_per_second: float = 2.0) -> bool:
    """Burn subtitles from text directly into video (creates new video file)."""
    try:
        info = get_video_info(video_path)
        video_duration = info.get('duration', 10.0)
        
        subtitle_path = video_path.parent / f"{video_path.stem}_subtitles.srt"
        
        if not generate_srt_subtitle_file(text, subtitle_path, video_duration, 0.0, words_per_second):
            return False
        
        success = add_subtitles_to_video(video_path, subtitle_path, output_path, 
                                       font_size, font_color, bg_color)
        
        subtitle_path.unlink()
        
        return success
        
    except Exception as e:
        print(f"❌ Exception processing {video_path.name}: {e}")
        return False

def concatenate_multiple_audio_files(audio_files: List[Path], output_path: Path) -> bool:
    """Concatenate multiple audio files in sequence using ffmpeg."""
    if len(audio_files) < 2:
        print("❌ Need at least 2 audio files to concatenate")
        return False
    
    try:
        # Create a temporary file list for ffmpeg concat
        temp_list_file = output_path.parent / "temp_audio_list.txt"
        
        # Write file list
        with open(temp_list_file, 'w') as f:
            for audio_file in audio_files:
                # Convert to absolute path to avoid issues
                abs_path = audio_file.resolve()
                f.write(f"file '{abs_path}'\n")
        
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(temp_list_file),
            '-c:a', 'mp3',
            '-ab', '192k',
            str(output_path),
            '-y'
        ]
        
        print(f"🎵 Concatenating {len(audio_files)} audio files in sequence...")
        for i, audio in enumerate(audio_files, 1):
            print(f"   {i}. {audio.name}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up temp file
        if temp_list_file.exists():
            temp_list_file.unlink()
        
        if result.returncode == 0:
            print(f"✅ Concatenated audio saved: {output_path.name}")
            return True
        else:
            print(f"❌ Error concatenating audio files:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception concatenating audio files: {e}")
        # Clean up temp file on error
        temp_list_file = output_path.parent / "temp_audio_list.txt"
        if temp_list_file.exists():
            temp_list_file.unlink()
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

def interactive_multiple_audio_selection(audio_files: List[Path]) -> List[Path]:
    """Interactive selection of multiple audio files."""
    if not audio_files:
        print("❌ No audio files found in current directory")
        return []
    
    print("\n🎵 Available audio files:")
    for i, audio in enumerate(audio_files, 1):
        print(f"   {i}. {audio.name}")
    
    selected_files = []
    
    print(f"\n🔢 Select multiple audio files:")
    print("   - Enter numbers separated by commas (e.g., 1,3,5)")
    print("   - Or enter 'all' to select all files")
    print("   - Or enter 'q' to quit")
    
    while True:
        try:
            choice = input(f"\nSelection: ").strip()
            
            if choice.lower() == 'q':
                return []
            
            if choice.lower() == 'all':
                return audio_files
            
            # Parse comma-separated numbers
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            
            # Validate all indices
            valid = True
            for index in indices:
                if index < 0 or index >= len(audio_files):
                    print(f"❌ Invalid choice: {index + 1}. Please enter numbers 1-{len(audio_files)}")
                    valid = False
                    break
            
            if valid and len(indices) >= 2:
                selected_files = [audio_files[i] for i in indices]
                print(f"\n✅ Selected {len(selected_files)} audio files:")
                for i, audio in enumerate(selected_files, 1):
                    print(f"   {i}. {audio.name}")
                return selected_files
            elif valid and len(indices) < 2:
                print("❌ Please select at least 2 audio files")
            
        except ValueError:
            print("❌ Invalid input. Please enter numbers separated by commas")
        except KeyboardInterrupt:
            print("\n👋 Cancelled by user")
            return []

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

def cmd_mix_audio():
    """Mix multiple audio files and add to videos."""
    print("🎵 MIX MULTIPLE AUDIO FILES AND ADD TO VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    audio_files = find_audio_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    if len(audio_files) < 2:
        print("📁 Need at least 2 audio files to mix")
        print("💡 Add more audio files (.mp3, .wav, .aac, etc.) to the current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s)")
    print(f"🎵 Found {len(audio_files)} audio file(s)")
    
    # Select multiple audio files to mix
    selected_audio_files = interactive_multiple_audio_selection(audio_files)
    if not selected_audio_files:
        return
    
    # Create mixed audio file
    mixed_audio_path = current_dir / "mixed_audio.mp3"
    print(f"\n🎵 Creating mixed audio file: {mixed_audio_path.name}")
    
    if not mix_multiple_audio_files(selected_audio_files, mixed_audio_path):
        return
    
    print(f"\n📺 Adding mixed audio to videos...")
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_mixed_audio{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Add mixed audio to video
        if add_audio_to_video(video_path, mixed_audio_path, output_path, replace_audio=True):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")
    
    # Ask if user wants to keep the mixed audio file
    try:
        keep_mixed = input(f"\n🗂️  Keep mixed audio file '{mixed_audio_path.name}'? (y/N): ").strip().lower()
        if keep_mixed != 'y':
            mixed_audio_path.unlink()
            print(f"🗑️  Deleted temporary file: {mixed_audio_path.name}")
    except KeyboardInterrupt:
        print(f"\n🗂️  Mixed audio file saved: {mixed_audio_path.name}")

def cmd_generate_subtitles():
    """Generate subtitle files for videos (loadable by video players)."""
    print("📝 GENERATE SUBTITLE FILES FOR VIDEOS")
    print("=" * 50)
    print("💡 Creates .srt/.vtt files that video players can load")
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s):")
    for video in video_files:
        info = get_video_info(video)
        duration_str = f"{info['duration']:.1f}s" if info['duration'] else "unknown"
        print(f"   - {video.name} ({duration_str})")
    
    # Get subtitle text from user
    print("\n📝 Enter subtitle text (press Enter twice to finish):")
    subtitle_lines = []
    empty_line_count = 0
    
    try:
        while empty_line_count < 2:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
            else:
                empty_line_count = 0
                subtitle_lines.append(line)
        
        subtitle_text = '\n'.join(subtitle_lines)
        
        if not subtitle_text.strip():
            print("❌ No subtitle text provided")
            return
        
        print(f"\n📝 Subtitle text ({len(subtitle_text.split())} words):")
        print(f"'{subtitle_text[:100]}{'...' if len(subtitle_text) > 100 else ''}'")
        
        # Get subtitle options
        try:
            words_per_second = float(input(f"\n⏱️  Words per second (default: 2.0): ").strip() or "2.0")
            format_choice = input(f"📄 Format - 1) SRT (default), 2) WebVTT: ").strip()
            format_type = "vtt" if format_choice == "2" else "srt"
        except ValueError:
            print("⚠️  Using default values")
            words_per_second = 2.0
            format_type = "srt"
        
        print(f"\n🎯 Generating {format_type.upper()} subtitle files...")
        
        successful = 0
        failed = 0
        
        for video_path in video_files:
            print(f"\n📺 Processing: {video_path.name}")
            
            # Generate subtitle file with same name as video
            subtitle_path = generate_subtitle_for_video(video_path, subtitle_text, format_type, words_per_second)
            
            if subtitle_path:
                successful += 1
                print(f"✅ Created: {subtitle_path.name}")
                print(f"💡 Load this file in your video player alongside {video_path.name}")
            else:
                failed += 1
        
        print(f"\n📊 Results: {successful} successful | {failed} failed")
        
        if successful > 0:
            print(f"\n🎉 Generated {successful} subtitle file(s)!")
            print("💡 How to use:")
            print("   1. Open your video in any player (VLC, Media Player, etc.)")
            print(f"   2. Load the .{format_type} file as subtitles")
            print("   3. Most players auto-load files with the same name")
        
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")

def cmd_burn_subtitles():
    """Burn subtitles directly into video files (creates new video files)."""
    print("🔥 BURN SUBTITLES INTO VIDEOS")
    print("=" * 50)
    print("⚠️  Creates new video files with subtitles permanently embedded")
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s):")
    for video in video_files:
        print(f"   - {video.name}")
    
    # Get subtitle text from user
    print("\n📝 Enter subtitle text (press Enter twice to finish):")
    subtitle_lines = []
    empty_line_count = 0
    
    try:
        while empty_line_count < 2:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
            else:
                empty_line_count = 0
                subtitle_lines.append(line)
        
        subtitle_text = '\n'.join(subtitle_lines)
        
        if not subtitle_text.strip():
            print("❌ No subtitle text provided")
            return
        
        print(f"\n📝 Subtitle text ({len(subtitle_text.split())} words):")
        print(f"'{subtitle_text[:100]}{'...' if len(subtitle_text) > 100 else ''}'")
        
        # Get subtitle options
        try:
            words_per_second = float(input(f"\n⏱️  Words per second (default: 2.0): ").strip() or "2.0")
            font_size = int(input(f"🔤 Font size (default: 24): ").strip() or "24")
            font_color = input(f"🎨 Font color (default: white): ").strip() or "white"
        except ValueError:
            print("⚠️  Using default values")
            words_per_second = 2.0
            font_size = 24
            font_color = "white"
        
        successful = 0
        failed = 0
        
        for video_path in video_files:
            print(f"\n📺 Processing: {video_path.name}")
            
            # Create output filename
            stem = video_path.stem
            suffix = video_path.suffix
            output_path = video_path.parent / f"{stem}_with_subtitles{suffix}"
            
            # Skip if output already exists
            if output_path.exists():
                print(f"⏭️  Skipping: {output_path.name} already exists")
                continue
            
            # Burn subtitles into video
            if add_text_subtitles_to_video(video_path, subtitle_text, output_path, 
                                         font_size, font_color, "black", words_per_second):
                successful += 1
            else:
                failed += 1
        
        print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")
        
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")

def cmd_concat_audio():
    """Concatenate multiple audio files and add to videos."""
    print("🎵 CONCATENATE MULTIPLE AUDIO FILES AND ADD TO VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    audio_files = find_audio_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    if len(audio_files) < 2:
        print("📁 Need at least 2 audio files to concatenate")
        print("💡 Add more audio files (.mp3, .wav, .aac, etc.) to the current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s)")
    print(f"🎵 Found {len(audio_files)} audio file(s)")
    
    # Select multiple audio files to concatenate
    selected_audio_files = interactive_multiple_audio_selection(audio_files)
    if not selected_audio_files:
        return
    
    # Create concatenated audio file
    concat_audio_path = current_dir / "concatenated_audio.mp3"
    print(f"\n🎵 Creating concatenated audio file: {concat_audio_path.name}")
    
    if not concatenate_multiple_audio_files(selected_audio_files, concat_audio_path):
        return
    
    print(f"\n📺 Adding concatenated audio to videos...")
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_concat_audio{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Add concatenated audio to video
        if add_audio_to_video(video_path, concat_audio_path, output_path, replace_audio=True):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")
    
    # Ask if user wants to keep the concatenated audio file
    try:
        keep_concat = input(f"\n🗂️  Keep concatenated audio file '{concat_audio_path.name}'? (y/N): ").strip().lower()
        if keep_concat != 'y':
            concat_audio_path.unlink()
            print(f"🗑️  Deleted temporary file: {concat_audio_path.name}")
    except KeyboardInterrupt:
        print(f"\n🗂️  Concatenated audio file saved: {concat_audio_path.name}")

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