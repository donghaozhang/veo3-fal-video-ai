"""
Subtitle generation and overlay utilities.

Provides functions for creating SRT/VTT subtitle files and burning subtitles into videos.
"""

import subprocess
from pathlib import Path
from typing import Optional

from .core import get_video_info


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