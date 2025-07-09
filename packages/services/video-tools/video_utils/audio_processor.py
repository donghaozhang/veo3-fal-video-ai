"""
Audio processing utilities.

Provides functions for audio manipulation, mixing, and video-audio operations.
"""

import subprocess
from pathlib import Path
from typing import List


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