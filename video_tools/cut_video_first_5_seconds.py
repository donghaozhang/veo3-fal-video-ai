#!/usr/bin/env python3
"""
Video Cutter Script - Extract First 5 Seconds

This script finds video files in the current directory and extracts 
the first 5 seconds into separate video files with "_first_5s" suffix.

Requirements:
- ffmpeg must be installed and available in PATH
- Supports common video formats: .mp4, .avi, .mov, .mkv, .webm

Usage:
    python cut_video_first_5_seconds.py

Author: AI Assistant
Date: 2024
"""

import os
import subprocess
import sys
from pathlib import Path

def check_ffmpeg():
    """Check if ffmpeg is available."""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_video_duration(video_path):
    """Get video duration in seconds using ffprobe."""
    try:
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 
            'format=duration', '-of', 'csv=p=0', str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return duration
    except (subprocess.CalledProcessError, ValueError):
        return None

def cut_first_5_seconds(input_path, output_path):
    """Cut first 5 seconds from video using ffmpeg."""
    try:
        cmd = [
            'ffmpeg', '-i', str(input_path),
            '-t', '5',  # Duration: 5 seconds
            '-c', 'copy',  # Copy streams without re-encoding (faster)
            '-avoid_negative_ts', 'make_zero',
            str(output_path),
            '-y'  # Overwrite output file if exists
        ]
        
        print(f"🎬 Processing: {input_path.name}")
        print(f"⏱️  Extracting first 5 seconds...")
        
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

def main():
    """Main function to process all video files."""
    print("🎥 VIDEO CUTTER - First 5 Seconds Extractor")
    print("=" * 50)
    
    # Check if ffmpeg is available
    if not check_ffmpeg():
        print("❌ Error: ffmpeg is not installed or not in PATH")
        print("📥 Please install ffmpeg:")
        print("   - Windows: Download from https://ffmpeg.org/download.html")
        print("   - macOS: brew install ffmpeg")
        print("   - Linux: sudo apt install ffmpeg (Ubuntu/Debian)")
        sys.exit(1)
    
    print("✅ ffmpeg found")
    
    # Supported video formats
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}
    
    # Get current directory (output folder)
    current_dir = Path('.')
    
    # Find all video files
    video_files = []
    for file_path in current_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            video_files.append(file_path)
    
    if not video_files:
        print("📁 No video files found in current directory")
        print(f"🔍 Looked for: {', '.join(video_extensions)}")
        return
    
    print(f"📹 Found {len(video_files)} video file(s):")
    for video in video_files:
        print(f"   - {video.name}")
    
    print("\n🎬 Starting processing...")
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Check video duration
        duration = get_video_duration(video_path)
        if duration is None:
            print(f"⚠️  Warning: Could not determine duration of {video_path.name}")
        elif duration < 5:
            print(f"⚠️  Warning: Video is only {duration:.1f}s long (less than 5s)")
        else:
            print(f"📏 Duration: {duration:.1f} seconds")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_first_5s{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Cut the video
        if cut_first_5_seconds(video_path, output_path):
            successful += 1
            
            # Show file sizes
            input_size = video_path.stat().st_size / (1024 * 1024)  # MB
            output_size = output_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 Input: {input_size:.1f} MB → Output: {output_size:.1f} MB")
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PROCESSING SUMMARY")
    print("=" * 50)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Total processed: {successful + failed}")
    
    if successful > 0:
        print(f"\n🎉 Successfully created {successful} video clip(s)!")
        print("📁 Output files have '_first_5s' suffix")
    
    if failed > 0:
        print(f"\n⚠️  {failed} file(s) failed to process")

if __name__ == "__main__":
    main() 