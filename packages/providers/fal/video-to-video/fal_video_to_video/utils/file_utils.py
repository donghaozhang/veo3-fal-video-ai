"""
File handling utilities for FAL Video to Video
"""

import os
import time
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse


def ensure_output_directory(output_dir: Optional[str] = None) -> Path:
    """
    Ensure output directory exists.
    
    Args:
        output_dir: Custom output directory path
        
    Returns:
        Path object for output directory
    """
    if output_dir:
        out_path = Path(output_dir)
    else:
        out_path = Path("output")
    
    out_path.mkdir(parents=True, exist_ok=True)
    return out_path


def download_video(video_url: str, output_dir: Path, filename: Optional[str] = None) -> str:
    """
    Download video from URL.
    
    Args:
        video_url: URL of the video
        output_dir: Directory to save video
        filename: Optional custom filename
        
    Returns:
        Path to downloaded video
    """
    if not filename:
        # Generate filename from timestamp
        timestamp = int(time.time())
        ext = os.path.splitext(urlparse(video_url).path)[1] or '.mp4'
        filename = f"video_{timestamp}{ext}"
    
    output_path = output_dir / filename
    
    print(f"📥 Downloading video...")
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size:
                    progress = (downloaded / total_size) * 100
                    print(f"   Progress: {progress:.1f}%", end='\r')
    
    print(f"\n✅ Video saved: {output_path}")
    return str(output_path)


def upload_video(video_path: str) -> str:
    """
    Upload local video to FAL storage.
    
    Args:
        video_path: Path to local video file
        
    Returns:
        URL of uploaded video
    """
    import fal_client
    
    print(f"📤 Uploading video: {video_path}")
    
    # Upload the video file
    video_url = fal_client.upload_file(video_path)
    
    print(f"✅ Video uploaded successfully: {video_url}")
    return video_url


def get_video_info(video_path: str) -> Dict[str, Any]:
    """
    Get video information using moviepy.
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dictionary with video information
    """
    try:
        from moviepy.editor import VideoFileClip
        
        with VideoFileClip(video_path) as video:
            info = {
                "duration": video.duration,
                "fps": video.fps,
                "size": video.size,
                "width": video.w,
                "height": video.h,
                "has_audio": video.audio is not None
            }
        return info
    except Exception as e:
        print(f"⚠️  Could not get video info: {e}")
        return {}


def cleanup_temp_files(file_paths: List[str]) -> None:
    """
    Clean up temporary files.
    
    Args:
        file_paths: List of file paths to delete
    """
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"🗑️  Cleaned up: {path}")
        except Exception as e:
            print(f"⚠️  Failed to clean up {path}: {e}")