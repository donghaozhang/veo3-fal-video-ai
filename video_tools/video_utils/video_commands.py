"""
Video processing command implementations.

Contains commands for video-specific operations like cutting duration.
"""

from pathlib import Path

from .core import get_video_info
from .file_utils import find_video_files
from .video_processor import cut_video_duration


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