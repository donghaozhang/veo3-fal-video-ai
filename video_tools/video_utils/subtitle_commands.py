"""
Subtitle processing command implementations.

Contains commands for generating and burning subtitles into videos.
"""

from pathlib import Path

from .core import get_video_info
from .file_utils import find_video_files
from .subtitle_generator import (
    generate_subtitle_for_video,
    add_text_subtitles_to_video
)


def cmd_generate_subtitles():
    """Generate subtitle files for videos (loadable by video players)."""
    print("📝 GENERATE SUBTITLE FILES FOR VIDEOS")
    print("=" * 50)
    print("💡 Creates .srt/.vtt files that video players can load")
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print(f"❌ Input directory '{input_dir}' does not exist")
        print("💡 Please create the 'input' directory and place your video files there")
        return
    
    video_files = find_video_files(input_dir)
    
    if not video_files:
        print(f"📁 No video files found in '{input_dir}' directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s):")
    for video in video_files:
        info = get_video_info(video)
        duration_str = f"{info['duration']:.1f}s" if info['duration'] else "unknown"
        print(f"   - {video.name} ({duration_str})")
    
    # Get subtitle text from user
    print("\n📝 Enter subtitle text (press Enter twice to finish):")
    subtitle_lines = []
    empty_line_count = 0
    
    try:
        while empty_line_count < 2:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
            else:
                empty_line_count = 0
                subtitle_lines.append(line)
        
        subtitle_text = '\n'.join(subtitle_lines)
        
        if not subtitle_text.strip():
            print("❌ No subtitle text provided")
            return
        
        print(f"\n📝 Subtitle text ({len(subtitle_text.split())} words):")
        print(f"'{subtitle_text[:100]}{'...' if len(subtitle_text) > 100 else ''}'")
        
        # Get subtitle options
        try:
            words_per_second = float(input(f"\n⏱️  Words per second (default: 2.0): ").strip() or "2.0")
            format_choice = input(f"📄 Format - 1) SRT (default), 2) WebVTT: ").strip()
            format_type = "vtt" if format_choice == "2" else "srt"
        except ValueError:
            print("⚠️  Using default values")
            words_per_second = 2.0
            format_type = "srt"
        
        print(f"\n🎯 Generating {format_type.upper()} subtitle files...")
        
        successful = 0
        failed = 0
        
        for video_path in video_files:
            print(f"\n📺 Processing: {video_path.name}")
            
            # Generate subtitle file with same name as video in output directory
            output_subtitle_path = output_dir / f"{video_path.stem}.{format_type}"
            subtitle_path = generate_subtitle_for_video(video_path, subtitle_text, format_type, words_per_second, output_subtitle_path)
            
            if subtitle_path:
                successful += 1
                print(f"✅ Created: {subtitle_path.name}")
                print(f"💡 Load this file in your video player alongside {video_path.name}")
            else:
                failed += 1
        
        print(f"\n📊 Results: {successful} successful | {failed} failed")
        
        if successful > 0:
            print(f"\n🎉 Generated {successful} subtitle file(s)!")
            print("💡 How to use:")
            print("   1. Open your video in any player (VLC, Media Player, etc.)")
            print(f"   2. Load the .{format_type} file as subtitles")
            print("   3. Most players auto-load files with the same name")
        
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")


def cmd_burn_subtitles():
    """Burn subtitles directly into video files (creates new video files)."""
    print("🔥 BURN SUBTITLES INTO VIDEOS")
    print("=" * 50)
    print("⚠️  Creates new video files with subtitles permanently embedded")
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print(f"❌ Input directory '{input_dir}' does not exist")
        print("💡 Please create the 'input' directory and place your video files there")
        return
    
    video_files = find_video_files(input_dir)
    
    if not video_files:
        print(f"📁 No video files found in '{input_dir}' directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s):")
    for video in video_files:
        print(f"   - {video.name}")
    
    # Get subtitle text from user
    print("\n📝 Enter subtitle text (press Enter twice to finish):")
    subtitle_lines = []
    empty_line_count = 0
    
    try:
        while empty_line_count < 2:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
            else:
                empty_line_count = 0
                subtitle_lines.append(line)
        
        subtitle_text = '\n'.join(subtitle_lines)
        
        if not subtitle_text.strip():
            print("❌ No subtitle text provided")
            return
        
        print(f"\n📝 Subtitle text ({len(subtitle_text.split())} words):")
        print(f"'{subtitle_text[:100]}{'...' if len(subtitle_text) > 100 else ''}'")
        
        # Get subtitle options
        try:
            words_per_second = float(input(f"\n⏱️  Words per second (default: 2.0): ").strip() or "2.0")
            font_size = int(input(f"🔤 Font size (default: 24): ").strip() or "24")
            font_color = input(f"🎨 Font color (default: white): ").strip() or "white"
        except ValueError:
            print("⚠️  Using default values")
            words_per_second = 2.0
            font_size = 24
            font_color = "white"
        
        successful = 0
        failed = 0
        
        for video_path in video_files:
            print(f"\n📺 Processing: {video_path.name}")
            
            # Create output filename in output directory
            stem = video_path.stem
            suffix = video_path.suffix
            output_path = output_dir / f"{stem}_with_subtitles{suffix}"
            
            # Skip if output already exists
            if output_path.exists():
                print(f"⏭️  Skipping: {output_path.name} already exists")
                continue
            
            # Burn subtitles into video
            if add_text_subtitles_to_video(video_path, subtitle_text, output_path, 
                                         font_size, font_color, "black", words_per_second):
                successful += 1
            else:
                failed += 1
        
        print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")
        
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")