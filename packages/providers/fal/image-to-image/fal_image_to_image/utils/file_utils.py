"""
File and image handling utilities
"""

import os
import time
import requests
from pathlib import Path
from typing import List, Optional
import fal_client


def upload_local_image(image_path: str) -> str:
    """
    Upload a local image to FAL AI and return the URL.
    
    Args:
        image_path: Path to local image file
        
    Returns:
        URL of uploaded image
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        Exception: If upload fails
    """
    image_file = Path(image_path)
    if not image_file.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        # Upload file to FAL AI
        url = fal_client.upload_file(str(image_file))
        print(f"✅ Image uploaded successfully: {url}")
        return url
    except Exception as e:
        raise Exception(f"Failed to upload image: {e}")


def download_image(image_url: str, output_path: Path) -> str:
    """
    Download an image from URL to local file.
    
    Args:
        image_url: URL of the image to download
        output_path: Local path to save the image
        
    Returns:
        Path to downloaded file
        
    Raises:
        Exception: If download fails
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return str(output_path)
    except Exception as e:
        raise Exception(f"Failed to download image from {image_url}: {e}")


def download_images(images: List[dict], output_dir: Path, prefix: str = "modified_image") -> List[str]:
    """
    Download multiple images from API response.
    
    Args:
        images: List of image dictionaries from API response
        output_dir: Directory to save images
        prefix: Filename prefix for saved images
        
    Returns:
        List of downloaded file paths
    """
    output_dir.mkdir(exist_ok=True)
    downloaded_files = []
    
    for i, image_info in enumerate(images):
        image_url = image_info.get("url")
        if image_url:
            # Generate filename
            timestamp = int(time.time())
            filename = f"{prefix}_{timestamp}_{i+1}.png"
            file_path = output_dir / filename
            
            # Download image
            try:
                download_image(image_url, file_path)
                downloaded_files.append(str(file_path))
                print(f"✅ Image saved: {file_path}")
            except Exception as e:
                print(f"❌ Failed to download image {i+1}: {e}")
    
    return downloaded_files


def ensure_output_directory(output_dir: Optional[str] = None) -> Path:
    """
    Ensure output directory exists and return Path object.
    
    Args:
        output_dir: Custom output directory path
        
    Returns:
        Path object for output directory
    """
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = Path("output")
    
    output_path.mkdir(exist_ok=True)
    return output_path


def get_file_size_kb(file_path: str) -> float:
    """
    Get file size in kilobytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in KB
    """
    return Path(file_path).stat().st_size / 1024