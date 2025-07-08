"""
Enhanced video processing class.

Provides a comprehensive class-based approach for video operations including:
- Video cutting and trimming
- Video information extraction
- Video format conversion
- Video quality operations
- Integration with audio operations
"""

import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import json


class VideoProcessor:
    """Enhanced video processor with comprehensive video manipulation capabilities."""
    
    def __init__(self, verbose: bool = True):
        """Initialize the video processor.
        
        Args:
            verbose: Whether to print operation details
        """
        self.verbose = verbose
        
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if required video processing tools are available.
        
        Returns:
            Dict with availability status of required tools
        """
        deps = {}
        
        # Check ffmpeg
        try:
            subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, check=True)
            deps['ffmpeg'] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            deps['ffmpeg'] = False
            
        # Check ffprobe
        try:
            subprocess.run(['ffprobe', '-version'], 
                          capture_output=True, check=True)
            deps['ffprobe'] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            deps['ffprobe'] = False
            
        return deps
    
    def get_video_info(self, video_path: Path) -> Dict[str, Any]:
        """Get comprehensive video information using ffprobe.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary with video information
        """
        try:
            # Get general format info
            cmd = [
                'ffprobe', '-v', 'error', '-show_entries', 
                'format=duration,size,bit_rate', '-of', 'csv=p=0', str(video_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            format_info = result.stdout.strip().split(',')
            
            duration = float(format_info[0]) if format_info[0] else None
            size = int(format_info[1]) if format_info[1] else None
            bit_rate = int(format_info[2]) if format_info[2] else None
            
            # Get video stream info
            cmd_video = [
                'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=codec_name,width,height,r_frame_rate',
                '-of', 'csv=p=0', str(video_path)
            ]
            result_video = subprocess.run(cmd_video, capture_output=True, text=True)
            video_info = result_video.stdout.strip().split(',') if result_video.stdout.strip() else []
            
            # Get audio stream info
            cmd_audio = [
                'ffprobe', '-v', 'error', '-select_streams', 'a:0',
                '-show_entries', 'stream=codec_name,sample_rate,channels',
                '-of', 'csv=p=0', str(video_path)
            ]
            result_audio = subprocess.run(cmd_audio, capture_output=True, text=True)
            audio_info = result_audio.stdout.strip().split(',') if result_audio.stdout.strip() else []
            
            return {
                'duration': duration,
                'file_size': size,
                'bit_rate': bit_rate,
                'has_video': bool(video_info),
                'video_codec': video_info[0] if len(video_info) > 0 else None,
                'width': int(video_info[1]) if len(video_info) > 1 and video_info[1] else None,
                'height': int(video_info[2]) if len(video_info) > 2 and video_info[2] else None,
                'frame_rate': video_info[3] if len(video_info) > 3 else None,
                'has_audio': bool(audio_info),
                'audio_codec': audio_info[0] if len(audio_info) > 0 else None,
                'sample_rate': int(audio_info[1]) if len(audio_info) > 1 and audio_info[1] else None,
                'audio_channels': int(audio_info[2]) if len(audio_info) > 2 and audio_info[2] else None,
            }
        except (subprocess.CalledProcessError, ValueError, IndexError) as e:
            if self.verbose:
                print(f"❌ Error getting video info for {video_path.name}: {e}")
            return {
                'duration': None, 'file_size': None, 'bit_rate': None,
                'has_video': False, 'video_codec': None, 'width': None, 'height': None, 'frame_rate': None,
                'has_audio': False, 'audio_codec': None, 'sample_rate': None, 'audio_channels': None
            }
    
    def cut_duration(self, input_path: Path, output_path: Path, duration: int, 
                    start_time: int = 0) -> bool:
        """Cut video to specified duration from start time.
        
        Args:
            input_path: Input video file path
            output_path: Output video file path
            duration: Duration to extract in seconds
            start_time: Start time in seconds (default: 0)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-ss', str(start_time),  # Start time
                '-t', str(duration),     # Duration in seconds
                '-c', 'copy',           # Copy streams without re-encoding (faster)
                '-avoid_negative_ts', 'make_zero',
                str(output_path),
                '-y'  # Overwrite output file if exists
            ]
            
            if self.verbose:
                print(f"🎬 Processing: {input_path.name}")
                print(f"⏱️  Extracting {duration}s from {start_time}s...")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Success: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error processing {input_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception processing {input_path.name}: {e}")
            return False
    
    def cut_timeframe(self, input_path: Path, output_path: Path, 
                     start_time: str, end_time: str) -> bool:
        """Cut video between specific timestamps.
        
        Args:
            input_path: Input video file path
            output_path: Output video file path
            start_time: Start time (HH:MM:SS format)
            end_time: End time (HH:MM:SS format)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-ss', start_time,
                '-to', end_time,
                '-c', 'copy',
                '-avoid_negative_ts', 'make_zero',
                str(output_path),
                '-y'
            ]
            
            if self.verbose:
                print(f"🎬 Processing: {input_path.name}")
                print(f"⏱️  Cutting from {start_time} to {end_time}...")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Success: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error processing {input_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception processing {input_path.name}: {e}")
            return False
    
    def resize_video(self, input_path: Path, output_path: Path, 
                    width: int, height: int, maintain_aspect: bool = True) -> bool:
        """Resize video to specified dimensions.
        
        Args:
            input_path: Input video file path
            output_path: Output video file path
            width: Target width
            height: Target height
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if maintain_aspect:
                scale_filter = f"scale={width}:{height}:force_original_aspect_ratio=decrease"
            else:
                scale_filter = f"scale={width}:{height}"
                
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-vf', scale_filter,
                '-c:a', 'copy',  # Copy audio unchanged
                str(output_path),
                '-y'
            ]
            
            if self.verbose:
                print(f"🎬 Resizing: {input_path.name}")
                print(f"📐 Target dimensions: {width}x{height}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Success: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error resizing {input_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception resizing {input_path.name}: {e}")
            return False
    
    def convert_format(self, input_path: Path, output_path: Path, 
                      target_codec: str = 'libx264') -> bool:
        """Convert video to different format/codec.
        
        Args:
            input_path: Input video file path
            output_path: Output video file path
            target_codec: Target video codec
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-c:v', target_codec,
                '-c:a', 'aac',  # Standard audio codec
                str(output_path),
                '-y'
            ]
            
            if self.verbose:
                print(f"🎬 Converting: {input_path.name}")
                print(f"🔄 Target codec: {target_codec}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Success: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error converting {input_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception converting {input_path.name}: {e}")
            return False
    
    def extract_frames(self, input_path: Path, output_dir: Path, 
                      frame_rate: str = "1/10") -> bool:
        """Extract frames from video at specified rate.
        
        Args:
            input_path: Input video file path
            output_dir: Directory to save frames
            frame_rate: Frame extraction rate (e.g., "1/10" for 1 frame per 10 seconds)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_pattern = output_dir / f"{input_path.stem}_frame_%04d.png"
            
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-vf', f'fps={frame_rate}',
                '-q:v', '2',  # High quality
                str(output_pattern),
                '-y'
            ]
            
            if self.verbose:
                print(f"🎬 Extracting frames: {input_path.name}")
                print(f"📸 Frame rate: {frame_rate}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Frames extracted to: {output_dir}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error extracting frames from {input_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception extracting frames from {input_path.name}: {e}")
            return False
    
    def get_thumbnail(self, input_path: Path, output_path: Path, 
                     timestamp: str = "00:00:01") -> bool:
        """Extract a thumbnail from video at specified timestamp.
        
        Args:
            input_path: Input video file path
            output_path: Output thumbnail file path
            timestamp: Timestamp for thumbnail (HH:MM:SS format)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-ss', timestamp,
                '-vframes', '1',
                '-q:v', '2',  # High quality
                str(output_path),
                '-y'
            ]
            
            if self.verbose:
                print(f"🎬 Extracting thumbnail: {input_path.name}")
                print(f"⏱️  At timestamp: {timestamp}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Thumbnail saved: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error extracting thumbnail from {input_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception extracting thumbnail from {input_path.name}: {e}")
            return False
    
    def validate_video(self, video_path: Path) -> bool:
        """Validate if file is a valid video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            True if valid video, False otherwise
        """
        if not video_path.exists():
            return False
            
        info = self.get_video_info(video_path)
        return info.get('has_video', False) and info.get('duration', 0) > 0
    
    def batch_process(self, input_dir: Path, output_dir: Path, 
                     operation: str, **kwargs) -> Dict[str, bool]:
        """Process multiple videos with the same operation.
        
        Args:
            input_dir: Directory containing input videos
            output_dir: Directory for output videos
            operation: Operation to perform ('cut_duration', 'resize', 'convert', etc.)
            **kwargs: Arguments for the operation
            
        Returns:
            Dictionary mapping input filenames to success status
        """
        results = {}
        
        # Common video extensions
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
        
        # Find all video files
        video_files = [f for f in input_dir.iterdir() 
                      if f.is_file() and f.suffix.lower() in video_extensions]
        
        if not video_files:
            if self.verbose:
                print(f"❌ No video files found in {input_dir}")
            return results
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.verbose:
            print(f"🎬 Starting batch {operation} on {len(video_files)} videos")
        
        for video_file in video_files:
            output_file = output_dir / f"{video_file.stem}_processed{video_file.suffix}"
            
            try:
                if operation == 'cut_duration':
                    success = self.cut_duration(video_file, output_file, **kwargs)
                elif operation == 'resize':
                    success = self.resize_video(video_file, output_file, **kwargs)
                elif operation == 'convert':
                    success = self.convert_format(video_file, output_file, **kwargs)
                elif operation == 'thumbnail':
                    thumb_output = output_dir / f"{video_file.stem}_thumb.jpg"
                    success = self.get_thumbnail(video_file, thumb_output, **kwargs)
                else:
                    if self.verbose:
                        print(f"❌ Unknown operation: {operation}")
                    success = False
                    
                results[video_file.name] = success
                
            except Exception as e:
                if self.verbose:
                    print(f"❌ Error processing {video_file.name}: {e}")
                results[video_file.name] = False
        
        # Summary
        if self.verbose:
            successful = sum(1 for success in results.values() if success)
            print(f"🎬 Batch processing complete: {successful}/{len(results)} successful")
        
        return results