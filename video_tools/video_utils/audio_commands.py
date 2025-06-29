"""
Audio processing command implementations.

Contains commands for audio operations like adding, replacing, extracting, 
mixing, and concatenating audio files with videos.
"""

from pathlib import Path

from .core import get_video_info
from .file_utils import find_video_files, find_audio_files
from .audio_processor import (
    add_audio_to_video, 
    extract_audio_from_video, 
    mix_multiple_audio_files, 
    concatenate_multiple_audio_files
)
from .interactive import interactive_audio_selection, interactive_multiple_audio_selection


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