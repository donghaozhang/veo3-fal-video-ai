"""
Enhanced audio processing class.

Provides a comprehensive class-based approach for audio operations including:
- Audio extraction from video
- Audio addition to video
- Audio mixing and concatenation
- Audio format conversion
- Audio analysis and manipulation
"""

import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import json
import tempfile


class AudioProcessor:
    """Enhanced audio processor with comprehensive audio manipulation capabilities."""
    
    def __init__(self, verbose: bool = True):
        """Initialize the audio processor.
        
        Args:
            verbose: Whether to print operation details
        """
        self.verbose = verbose
        
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if required audio processing tools are available.
        
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
            
        return deps
    
    def get_audio_info(self, audio_path: Path) -> Dict[str, Any]:
        """Get comprehensive audio information using ffprobe.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary with audio information
        """
        try:
            # Get format info
            cmd = [
                'ffprobe', '-v', 'error', '-show_entries',
                'format=duration,size,bit_rate', '-of', 'csv=p=0', str(audio_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            format_info = result.stdout.strip().split(',')
            
            duration = float(format_info[0]) if format_info[0] else None
            size = int(format_info[1]) if format_info[1] else None
            bit_rate = int(format_info[2]) if format_info[2] else None
            
            # Get stream info
            cmd_stream = [
                'ffprobe', '-v', 'error', '-select_streams', 'a:0',
                '-show_entries', 'stream=codec_name,sample_rate,channels,bit_rate',
                '-of', 'csv=p=0', str(audio_path)
            ]
            result_stream = subprocess.run(cmd_stream, capture_output=True, text=True)
            stream_info = result_stream.stdout.strip().split(',') if result_stream.stdout.strip() else []
            
            return {
                'duration': duration,
                'file_size': size,
                'format_bit_rate': bit_rate,
                'codec': stream_info[0] if len(stream_info) > 0 else None,
                'sample_rate': int(stream_info[1]) if len(stream_info) > 1 and stream_info[1] else None,
                'channels': int(stream_info[2]) if len(stream_info) > 2 and stream_info[2] else None,
                'stream_bit_rate': int(stream_info[3]) if len(stream_info) > 3 and stream_info[3] else None,
            }
        except (subprocess.CalledProcessError, ValueError, IndexError) as e:
            if self.verbose:
                print(f"❌ Error getting audio info for {audio_path.name}: {e}")
            return {
                'duration': None, 'file_size': None, 'format_bit_rate': None,
                'codec': None, 'sample_rate': None, 'channels': None, 'stream_bit_rate': None
            }
    
    def extract_from_video(self, video_path: Path, output_path: Path, 
                          audio_format: str = 'mp3', quality: str = '192k') -> bool:
        """Extract audio from video file.
        
        Args:
            video_path: Path to input video file
            output_path: Path for output audio file
            audio_format: Output audio format (mp3, wav, aac, etc.)
            quality: Audio quality/bitrate
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                'ffmpeg', '-i', str(video_path),
                '-vn',  # No video
                '-c:a', audio_format,
                '-ab', quality,
                str(output_path),
                '-y'
            ]
            
            if self.verbose:
                print(f"🎵 Extracting audio: {video_path.name} → {output_path.name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Success: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error extracting audio from {video_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception extracting audio from {video_path.name}: {e}")
            return False
    
    def add_to_video(self, video_path: Path, audio_path: Path, output_path: Path, 
                    replace_audio: bool = False, sync_to_video: bool = True) -> bool:
        """Add or replace audio in video file.
        
        Args:
            video_path: Path to input video file
            audio_path: Path to audio file to add
            output_path: Path for output video file
            replace_audio: Whether to replace existing audio or mix with it
            sync_to_video: Whether to sync audio duration to video duration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if replace_audio:
                # Replace existing audio completely
                cmd = [
                    'ffmpeg', '-i', str(video_path), '-i', str(audio_path),
                    '-c:v', 'copy',  # Copy video stream
                    '-c:a', 'aac',   # Re-encode audio to AAC
                    '-map', '0:v:0', # Map video from first input
                    '-map', '1:a:0', # Map audio from second input
                ]
                
                if sync_to_video:
                    cmd.append('-shortest')  # Stop when shortest stream ends
                    
                cmd.extend([str(output_path), '-y'])
                
            else:
                # Add audio to silent video or mix with existing
                cmd = [
                    'ffmpeg', '-i', str(video_path), '-i', str(audio_path),
                    '-c:v', 'copy',  # Copy video stream
                    '-c:a', 'aac',   # Encode audio to AAC
                ]
                
                if sync_to_video:
                    cmd.append('-shortest')
                    
                cmd.extend([str(output_path), '-y'])
            
            action = "Replacing" if replace_audio else "Adding"
            if self.verbose:
                print(f"🎵 {action} audio: {audio_path.name} → {video_path.name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Success: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error processing {video_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception processing {video_path.name}: {e}")
            return False
    
    def mix_files(self, audio_files: List[Path], output_path: Path, 
                 normalize: bool = True, method: str = 'overlay') -> bool:
        """Mix multiple audio files together.
        
        Args:
            audio_files: List of paths to audio files to mix
            output_path: Path for output mixed audio file
            normalize: Whether to normalize volume levels
            method: Mixing method ('overlay' or 'sum')
            
        Returns:
            True if successful, False otherwise
        """
        if len(audio_files) < 2:
            if self.verbose:
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
                    volume = 1.0 / len(audio_files) if method == 'overlay' else 1.0
                    filter_parts.append(f"[{i}:a]volume={volume}[a{i}]")
                
                # Mix all normalized inputs
                mix_inputs = ";".join(filter_parts)
                mix_part = "".join([f"[a{i}]" for i in range(len(audio_files))])
                
                if method == 'overlay':
                    filter_complex = f"{mix_inputs};{mix_part}amix=inputs={len(audio_files)}:duration=longest[out]"
                else:
                    filter_complex = f"{mix_inputs};{mix_part}amix=inputs={len(audio_files)}:duration=longest:dropout_transition=0[out]"
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
            
            if self.verbose:
                print(f"🎵 Mixing {len(audio_files)} audio files using {method} method...")
                for audio in audio_files:
                    print(f"   - {audio.name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Mixed audio saved: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error mixing audio files:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception mixing audio files: {e}")
            return False
    
    def concatenate_files(self, audio_files: List[Path], output_path: Path, 
                         crossfade_duration: float = 0.0) -> bool:
        """Concatenate multiple audio files in sequence.
        
        Args:
            audio_files: List of paths to audio files to concatenate
            output_path: Path for output concatenated audio file
            crossfade_duration: Duration of crossfade between files in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if len(audio_files) < 2:
            if self.verbose:
                print("❌ Need at least 2 audio files to concatenate")
            return False
        
        try:
            if crossfade_duration > 0:
                # Use complex filter for crossfading
                return self._concatenate_with_crossfade(audio_files, output_path, crossfade_duration)
            else:
                # Simple concatenation using file list
                return self._concatenate_simple(audio_files, output_path)
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception concatenating audio files: {e}")
            return False
    
    def _concatenate_simple(self, audio_files: List[Path], output_path: Path) -> bool:
        """Simple concatenation without crossfade."""
        temp_list_file = None
        try:
            # Create a temporary file list for ffmpeg concat
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                temp_list_file = Path(f.name)
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
            
            if self.verbose:
                print(f"🎵 Concatenating {len(audio_files)} audio files in sequence...")
                for i, audio in enumerate(audio_files, 1):
                    print(f"   {i}. {audio.name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Concatenated audio saved: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error concatenating audio files:")
                    print(result.stderr)
                return False
                
        finally:
            # Clean up temp file
            if temp_list_file and temp_list_file.exists():
                temp_list_file.unlink()
    
    def _concatenate_with_crossfade(self, audio_files: List[Path], output_path: Path, 
                                   crossfade_duration: float) -> bool:
        """Concatenation with crossfade effect."""
        cmd = ['ffmpeg']
        
        # Add all input files
        for audio_file in audio_files:
            cmd.extend(['-i', str(audio_file)])
        
        # Build complex filter for crossfading
        filter_parts = []
        current_label = "[0:a]"
        
        for i in range(1, len(audio_files)):
            crossfade_filter = f"{current_label}[{i}:a]acrossfade=d={crossfade_duration}[cf{i}]"
            filter_parts.append(crossfade_filter)
            current_label = f"[cf{i}]"
        
        filter_complex = ";".join(filter_parts)
        
        cmd.extend([
            '-filter_complex', filter_complex,
            '-map', current_label,
            '-c:a', 'mp3',
            '-ab', '192k',
            str(output_path),
            '-y'
        ])
        
        if self.verbose:
            print(f"🎵 Concatenating {len(audio_files)} files with {crossfade_duration}s crossfade...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            if self.verbose:
                print(f"✅ Crossfaded concatenation saved: {output_path.name}")
            return True
        else:
            if self.verbose:
                print(f"❌ Error in crossfade concatenation:")
                print(result.stderr)
            return False
    
    def convert_format(self, input_path: Path, output_path: Path, 
                      target_format: str = 'mp3', quality: str = '192k',
                      sample_rate: Optional[int] = None) -> bool:
        """Convert audio to different format.
        
        Args:
            input_path: Input audio file path
            output_path: Output audio file path
            target_format: Target audio format (mp3, wav, aac, flac, etc.)
            quality: Audio quality/bitrate
            sample_rate: Target sample rate (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-c:a', target_format,
                '-ab', quality
            ]
            
            if sample_rate:
                cmd.extend(['-ar', str(sample_rate)])
            
            cmd.extend([str(output_path), '-y'])
            
            if self.verbose:
                print(f"🎵 Converting: {input_path.name}")
                print(f"🔄 Target format: {target_format} @ {quality}")
            
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
    
    def adjust_volume(self, input_path: Path, output_path: Path, 
                     volume_factor: float = 1.0, normalize: bool = False) -> bool:
        """Adjust audio volume.
        
        Args:
            input_path: Input audio file path
            output_path: Output audio file path
            volume_factor: Volume multiplication factor (1.0 = no change, 2.0 = double)
            normalize: Whether to normalize audio levels
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if normalize:
                filter_str = f"volume={volume_factor},loudnorm"
            else:
                filter_str = f"volume={volume_factor}"
            
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-af', filter_str,
                '-c:a', 'mp3',
                '-ab', '192k',
                str(output_path),
                '-y'
            ]
            
            if self.verbose:
                print(f"🎵 Adjusting volume: {input_path.name}")
                print(f"🔊 Volume factor: {volume_factor}, Normalize: {normalize}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Success: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error adjusting volume for {input_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception adjusting volume for {input_path.name}: {e}")
            return False
    
    def trim_audio(self, input_path: Path, output_path: Path, 
                  start_time: str, duration: Optional[str] = None, 
                  end_time: Optional[str] = None) -> bool:
        """Trim audio file to specified time range.
        
        Args:
            input_path: Input audio file path
            output_path: Output audio file path
            start_time: Start time (HH:MM:SS format)
            duration: Duration to keep (HH:MM:SS format, optional)
            end_time: End time (HH:MM:SS format, optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-ss', start_time
            ]
            
            if duration:
                cmd.extend(['-t', duration])
            elif end_time:
                cmd.extend(['-to', end_time])
            
            cmd.extend([
                '-c:a', 'mp3',
                '-ab', '192k',
                str(output_path),
                '-y'
            ])
            
            if self.verbose:
                print(f"🎵 Trimming audio: {input_path.name}")
                print(f"⏱️  From {start_time} for {duration or 'to ' + end_time}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Success: {output_path.name}")
                return True
            else:
                if self.verbose:
                    print(f"❌ Error trimming {input_path.name}:")
                    print(result.stderr)
                return False
                
        except Exception as e:
            if self.verbose:
                print(f"❌ Exception trimming {input_path.name}: {e}")
            return False
    
    def validate_audio(self, audio_path: Path) -> bool:
        """Validate if file is a valid audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            True if valid audio, False otherwise
        """
        if not audio_path.exists():
            return False
            
        info = self.get_audio_info(audio_path)
        return info.get('duration', 0) > 0 and info.get('codec') is not None
    
    def batch_process(self, input_dir: Path, output_dir: Path, 
                     operation: str, **kwargs) -> Dict[str, bool]:
        """Process multiple audio files with the same operation.
        
        Args:
            input_dir: Directory containing input audio files
            output_dir: Directory for output audio files
            operation: Operation to perform
            **kwargs: Arguments for the operation
            
        Returns:
            Dictionary mapping input filenames to success status
        """
        results = {}
        
        # Common audio extensions
        audio_extensions = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'}
        
        # Find all audio files
        audio_files = [f for f in input_dir.iterdir() 
                      if f.is_file() and f.suffix.lower() in audio_extensions]
        
        if not audio_files:
            if self.verbose:
                print(f"❌ No audio files found in {input_dir}")
            return results
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.verbose:
            print(f"🎵 Starting batch {operation} on {len(audio_files)} audio files")
        
        for audio_file in audio_files:
            output_file = output_dir / f"{audio_file.stem}_processed.mp3"
            
            try:
                if operation == 'convert':
                    success = self.convert_format(audio_file, output_file, **kwargs)
                elif operation == 'volume':
                    success = self.adjust_volume(audio_file, output_file, **kwargs)
                elif operation == 'trim':
                    success = self.trim_audio(audio_file, output_file, **kwargs)
                else:
                    if self.verbose:
                        print(f"❌ Unknown operation: {operation}")
                    success = False
                    
                results[audio_file.name] = success
                
            except Exception as e:
                if self.verbose:
                    print(f"❌ Error processing {audio_file.name}: {e}")
                results[audio_file.name] = False
        
        # Summary
        if self.verbose:
            successful = sum(1 for success in results.values() if success)
            print(f"🎵 Batch processing complete: {successful}/{len(results)} successful")
        
        return results