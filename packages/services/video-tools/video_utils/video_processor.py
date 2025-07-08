"""
Video processing utilities.

Provides functions for video cutting and manipulation.
"""

import subprocess
from pathlib import Path


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