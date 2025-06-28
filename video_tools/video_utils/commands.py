"""
Command implementations for video and audio utilities.

Provides command-line interface implementations for all video/audio operations.
"""

from pathlib import Path
from typing import List

from .core import get_video_info
from .file_utils import find_video_files, find_audio_files
from .video_processor import cut_video_duration
from .audio_processor import (
    add_audio_to_video, 
    extract_audio_from_video, 
    mix_multiple_audio_files, 
    concatenate_multiple_audio_files
)
from .subtitle_generator import (
    generate_subtitle_for_video,
    add_text_subtitles_to_video
)
from .interactive import interactive_audio_selection, interactive_multiple_audio_selection
from .video_understanding import (
    check_gemini_requirements,
    analyze_video_file,
    analyze_audio_file,
    save_analysis_result,
    GeminiVideoAnalyzer
)


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


def cmd_add_audio():
    """Add audio to silent videos."""
    print("🎵 ADD AUDIO TO SILENT VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    audio_files = find_audio_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    if not audio_files:
        print("📁 No audio files found in current directory")
        print("💡 Add some audio files (.mp3, .wav, .aac, etc.) to the current directory")
        return
    
    # Find silent videos
    silent_videos = []
    for video in video_files:
        info = get_video_info(video)
        if not info['has_audio']:
            silent_videos.append(video)
    
    if not silent_videos:
        print("📹 No silent videos found")
        print("💡 All videos already have audio. Use 'replace-audio' to replace existing audio")
        return
    
    print(f"🔇 Found {len(silent_videos)} silent video(s):")
    for video in silent_videos:
        print(f"   - {video.name}")
    
    # Select audio file
    selected_audio = interactive_audio_selection(audio_files)
    if not selected_audio:
        return
    
    print(f"\n🎵 Using audio: {selected_audio.name}")
    
    successful = 0
    failed = 0
    
    for video_path in silent_videos:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_with_audio{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Add audio to video
        if add_audio_to_video(video_path, selected_audio, output_path, replace_audio=False):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")


def cmd_replace_audio():
    """Replace audio in videos."""
    print("🔄 REPLACE AUDIO IN VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    audio_files = find_audio_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    if not audio_files:
        print("📁 No audio files found in current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s)")
    
    # Select audio file
    selected_audio = interactive_audio_selection(audio_files)
    if not selected_audio:
        return
    
    print(f"\n🎵 Using audio: {selected_audio.name}")
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_new_audio{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Replace audio in video
        if add_audio_to_video(video_path, selected_audio, output_path, replace_audio=True):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")


def cmd_extract_audio():
    """Extract audio from videos."""
    print("🎵 EXTRACT AUDIO FROM VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    # Find videos with audio
    videos_with_audio = []
    for video in video_files:
        info = get_video_info(video)
        if info['has_audio']:
            videos_with_audio.append(video)
    
    if not videos_with_audio:
        print("📹 No videos with audio found")
        return
    
    print(f"🎵 Found {len(videos_with_audio)} video(s) with audio:")
    for video in videos_with_audio:
        print(f"   - {video.name}")
    
    successful = 0
    failed = 0
    
    for video_path in videos_with_audio:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        output_path = video_path.parent / f"{stem}_audio.mp3"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Extract audio from video
        if extract_audio_from_video(video_path, output_path):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")


def cmd_mix_audio():
    """Mix multiple audio files and add to videos."""
    print("🎵 MIX MULTIPLE AUDIO FILES AND ADD TO VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    audio_files = find_audio_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    if len(audio_files) < 2:
        print("📁 Need at least 2 audio files to mix")
        print("💡 Add more audio files (.mp3, .wav, .aac, etc.) to the current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s)")
    print(f"🎵 Found {len(audio_files)} audio file(s)")
    
    # Select multiple audio files to mix
    selected_audio_files = interactive_multiple_audio_selection(audio_files)
    if not selected_audio_files:
        return
    
    # Create mixed audio file
    mixed_audio_path = current_dir / "mixed_audio.mp3"
    print(f"\n🎵 Creating mixed audio file: {mixed_audio_path.name}")
    
    if not mix_multiple_audio_files(selected_audio_files, mixed_audio_path):
        return
    
    print(f"\n📺 Adding mixed audio to videos...")
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_mixed_audio{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Add mixed audio to video
        if add_audio_to_video(video_path, mixed_audio_path, output_path, replace_audio=True):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")
    
    # Ask if user wants to keep the mixed audio file
    try:
        keep_mixed = input(f"\n🗂️  Keep mixed audio file '{mixed_audio_path.name}'? (y/N): ").strip().lower()
        if keep_mixed != 'y':
            mixed_audio_path.unlink()
            print(f"🗑️  Deleted temporary file: {mixed_audio_path.name}")
    except KeyboardInterrupt:
        print(f"\n🗂️  Mixed audio file saved: {mixed_audio_path.name}")


def cmd_concat_audio():
    """Concatenate multiple audio files and add to videos."""
    print("🎵 CONCATENATE MULTIPLE AUDIO FILES AND ADD TO VIDEOS")
    print("=" * 50)
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    audio_files = find_audio_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    if len(audio_files) < 2:
        print("📁 Need at least 2 audio files to concatenate")
        print("💡 Add more audio files (.mp3, .wav, .aac, etc.) to the current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s)")
    print(f"🎵 Found {len(audio_files)} audio file(s)")
    
    # Select multiple audio files to concatenate
    selected_audio_files = interactive_multiple_audio_selection(audio_files)
    if not selected_audio_files:
        return
    
    # Create concatenated audio file
    concat_audio_path = current_dir / "concatenated_audio.mp3"
    print(f"\n🎵 Creating concatenated audio file: {concat_audio_path.name}")
    
    if not concatenate_multiple_audio_files(selected_audio_files, concat_audio_path):
        return
    
    print(f"\n📺 Adding concatenated audio to videos...")
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Processing: {video_path.name}")
        
        # Create output filename
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_concat_audio{suffix}"
        
        # Skip if output already exists
        if output_path.exists():
            print(f"⏭️  Skipping: {output_path.name} already exists")
            continue
        
        # Add concatenated audio to video
        if add_audio_to_video(video_path, concat_audio_path, output_path, replace_audio=True):
            successful += 1
        else:
            failed += 1
    
    print(f"\n✅ Successful: {successful} | ❌ Failed: {failed}")
    
    # Ask if user wants to keep the concatenated audio file
    try:
        keep_concat = input(f"\n🗂️  Keep concatenated audio file '{concat_audio_path.name}'? (y/N): ").strip().lower()
        if keep_concat != 'y':
            concat_audio_path.unlink()
            print(f"🗑️  Deleted temporary file: {concat_audio_path.name}")
    except KeyboardInterrupt:
        print(f"\n🗂️  Concatenated audio file saved: {concat_audio_path.name}")


def cmd_generate_subtitles():
    """Generate subtitle files for videos (loadable by video players)."""
    print("📝 GENERATE SUBTITLE FILES FOR VIDEOS")
    print("=" * 50)
    print("💡 Creates .srt/.vtt files that video players can load")
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
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
            
            # Generate subtitle file with same name as video
            subtitle_path = generate_subtitle_for_video(video_path, subtitle_text, format_type, words_per_second)
            
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
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
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
            
            # Create output filename
            stem = video_path.stem
            suffix = video_path.suffix
            output_path = video_path.parent / f"{stem}_with_subtitles{suffix}"
            
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


def cmd_analyze_videos():
    """Analyze videos using Google Gemini AI."""
    print("🤖 AI VIDEO ANALYSIS - Google Gemini")
    print("=" * 50)
    print("💡 Analyze video content with AI-powered understanding")
    
    # Check requirements
    gemini_ready, message = check_gemini_requirements()
    if not gemini_ready:
        print(f"❌ Gemini not available: {message}")
        if "not installed" in message:
            print("📥 Install with: pip install google-generativeai")
        if "not set" in message:
            print("🔑 Set API key: export GEMINI_API_KEY=your_api_key")
            print("🌐 Get API key: https://aistudio.google.com/app/apikey")
        return
    
    print("✅ Gemini API ready")
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s):")
    for video in video_files:
        info = get_video_info(video)
        duration_str = f"{info['duration']:.1f}s" if info['duration'] else "unknown"
        file_size = video.stat().st_size / (1024 * 1024)  # MB
        print(f"   - {video.name} ({duration_str}, {file_size:.1f}MB)")
    
    # Select analysis type
    print("\n🎯 Select analysis type:")
    print("   1. Video Description (summary and overview)")
    print("   2. Audio Transcription (speech to text)")
    print("   3. Scene Analysis (timeline breakdown)")
    print("   4. Key Information Extraction")
    print("   5. Custom Q&A (ask specific questions)")
    
    try:
        choice = input("\n🔢 Enter choice (1-5): ").strip()
        
        analysis_type = {
            '1': 'description',
            '2': 'transcription', 
            '3': 'scenes',
            '4': 'extraction',
            '5': 'qa'
        }.get(choice)
        
        if not analysis_type:
            print("❌ Invalid choice")
            return
        
        # Get additional options
        detailed = False
        questions = None
        
        if analysis_type == 'description':
            detailed_choice = input("📊 Detailed analysis? (y/N): ").strip().lower()
            detailed = detailed_choice == 'y'
        elif analysis_type == 'qa':
            print("\n❓ Enter your questions (press Enter twice to finish):")
            questions = []
            empty_count = 0
            while empty_count < 2:
                question = input()
                if question.strip():
                    questions.append(question.strip())
                    empty_count = 0
                else:
                    empty_count += 1
            
            if not questions:
                print("❌ No questions provided")
                return
        
        print(f"\n🚀 Starting {analysis_type} analysis...")
        
        successful = 0
        failed = 0
        
        for video_path in video_files:
            print(f"\n📺 Analyzing: {video_path.name}")
            
            try:
                # Perform analysis
                result = analyze_video_file(
                    video_path, 
                    analysis_type, 
                    questions=questions,
                    detailed=detailed
                )
                
                if result:
                    # Save result
                    output_file = video_path.parent / f"{video_path.stem}_{analysis_type}_analysis.json"
                    if save_analysis_result(result, output_file):
                        successful += 1
                        
                        # Show preview of result
                        print(f"\n📋 Analysis Preview:")
                        if analysis_type == 'description':
                            preview = result['description'][:200] + "..." if len(result['description']) > 200 else result['description']
                            print(f"'{preview}'")
                        elif analysis_type == 'transcription':
                            preview = result['transcription'][:200] + "..." if len(result['transcription']) > 200 else result['transcription']
                            print(f"'{preview}'")
                        else:
                            content_key = {'scenes': 'scene_analysis', 'extraction': 'key_info', 'qa': 'answers'}[analysis_type]
                            preview = result[content_key][:200] + "..." if len(result[content_key]) > 200 else result[content_key]
                            print(f"'{preview}'")
                else:
                    failed += 1
                    
            except Exception as e:
                print(f"❌ Analysis failed: {e}")
                failed += 1
        
        print(f"\n📊 Results: {successful} successful | {failed} failed")
        
        if successful > 0:
            print(f"\n🎉 Analysis complete! Check JSON files for full results.")
            print("💡 JSON files contain structured data for further processing")
            
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")


def cmd_transcribe_videos():
    """Quick transcription of video audio using Gemini."""
    print("🎤 VIDEO TRANSCRIPTION - Google Gemini")
    print("=" * 50)
    
    # Check requirements
    gemini_ready, message = check_gemini_requirements()
    if not gemini_ready:
        print(f"❌ Gemini not available: {message}")
        return
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s)")
    
    include_timestamps = input("⏰ Include timestamps? (Y/n): ").strip().lower() != 'n'
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Transcribing: {video_path.name}")
        
        try:
            analyzer = GeminiVideoAnalyzer()
            result = analyzer.transcribe_video(video_path, include_timestamps)
            
            if result:
                # Save as both JSON and text
                json_file = video_path.parent / f"{video_path.stem}_transcription.json"
                txt_file = video_path.parent / f"{video_path.stem}_transcription.txt"
                
                save_analysis_result(result, json_file)
                
                # Save text version
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(result['transcription'])
                
                print(f"📄 Transcription saved: {txt_file.name}")
                successful += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            failed += 1
    
    print(f"\n📊 Results: {successful} successful | {failed} failed")


def cmd_describe_videos():
    """Quick description of videos using Gemini."""
    print("📝 VIDEO DESCRIPTION - Google Gemini")
    print("=" * 50)
    
    # Check requirements
    gemini_ready, message = check_gemini_requirements()
    if not gemini_ready:
        print(f"❌ Gemini not available: {message}")
        return
    
    current_dir = Path('.')
    video_files = find_video_files(current_dir)
    
    if not video_files:
        print("📁 No video files found in current directory")
        return
    
    print(f"📹 Found {len(video_files)} video file(s)")
    
    detailed = input("📊 Detailed analysis? (y/N): ").strip().lower() == 'y'
    
    successful = 0
    failed = 0
    
    for video_path in video_files:
        print(f"\n📺 Describing: {video_path.name}")
        
        try:
            analyzer = GeminiVideoAnalyzer()
            result = analyzer.describe_video(video_path, detailed)
            
            if result:
                # Save result
                json_file = video_path.parent / f"{video_path.stem}_description.json"
                txt_file = video_path.parent / f"{video_path.stem}_description.txt"
                
                save_analysis_result(result, json_file)
                
                # Save text version
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(result['description'])
                
                print(f"📄 Description saved: {txt_file.name}")
                print(f"📋 Preview: {result['description'][:150]}...")
                successful += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ Description failed: {e}")
            failed += 1
    
    print(f"\n📊 Results: {successful} successful | {failed} failed")


def cmd_analyze_audio():
    """Comprehensive audio analysis using Gemini."""
    print("🔊 AUDIO ANALYSIS - Google Gemini")
    print("=" * 50)
    
    # Check requirements
    gemini_ready, message = check_gemini_requirements()
    if not gemini_ready:
        print(f"❌ Gemini not available: {message}")
        return
    
    current_dir = Path('.')
    audio_files = find_audio_files(current_dir)
    
    if not audio_files:
        print("📁 No audio files found in current directory")
        return
    
    print(f"🎵 Found {len(audio_files)} audio file(s)")
    
    # Analysis type selection
    analysis_types = {
        '1': ('description', 'Audio description and characteristics'),
        '2': ('transcription', 'Speech-to-text transcription'),
        '3': ('content_analysis', 'Comprehensive content analysis'),
        '4': ('events', 'Audio event and segment detection'),
        '5': ('qa', 'Question and answer analysis')
    }
    
    print("\n🎯 Available analysis types:")
    for key, (type_name, description) in analysis_types.items():
        print(f"   {key}. {description}")
    
    try:
        choice = input("\n📝 Select analysis type (1-5): ").strip()
        if choice not in analysis_types:
            print("❌ Invalid selection")
            return
        
        analysis_type, _ = analysis_types[choice]
        
        # Additional options
        detailed = False
        speaker_identification = True
        questions = None
        
        if analysis_type == 'description':
            detailed = input("📖 Detailed analysis? (y/N): ").strip().lower() == 'y'
        elif analysis_type == 'transcription':
            speaker_identification = input("👥 Speaker identification? (Y/n): ").strip().lower() != 'n'
        elif analysis_type == 'qa':
            print("\n❓ Enter questions (one per line, empty line to finish):")
            questions = []
            while True:
                q = input("   Question: ").strip()
                if not q:
                    break
                questions.append(q)
            if not questions:
                questions = ["What is the main topic of this audio?", "Who is speaking and what are they discussing?"]
        
        successful = 0
        failed = 0
        
        for audio_path in audio_files:
            print(f"\n🎵 Analyzing: {audio_path.name}")
            
            try:
                result = analyze_audio_file(
                    audio_path, 
                    analysis_type, 
                    questions=questions,
                    detailed=detailed,
                    speaker_identification=speaker_identification
                )
                
                if result:
                    # Save result
                    output_file = audio_path.parent / f"{audio_path.stem}_{analysis_type}_analysis.json"
                    if save_analysis_result(result, output_file):
                        successful += 1
                        
                        # Show preview of result
                        print(f"\n📋 Analysis Preview:")
                        if analysis_type == 'description':
                            preview = result['description'][:200] + "..." if len(result['description']) > 200 else result['description']
                            print(f"'{preview}'")
                        elif analysis_type == 'transcription':
                            preview = result['transcription'][:200] + "..." if len(result['transcription']) > 200 else result['transcription']
                            print(f"'{preview}'")
                        elif analysis_type == 'content_analysis':
                            preview = result['analysis'][:200] + "..." if len(result['analysis']) > 200 else result['analysis']
                            print(f"'{preview}'")
                        elif analysis_type == 'events':
                            preview = result['events'][:200] + "..." if len(result['events']) > 200 else result['events']
                            print(f"'{preview}'")
                        elif analysis_type == 'qa':
                            preview = result['answers'][:200] + "..." if len(result['answers']) > 200 else result['answers']
                            print(f"'{preview}'")
                else:
                    failed += 1
                    
            except Exception as e:
                print(f"❌ Analysis failed: {e}")
                failed += 1
        
        print(f"\n📊 Results: {successful} successful | {failed} failed")
        
        if successful > 0:
            print(f"\n🎉 Analysis complete! Check JSON files for full results.")
            print("💡 JSON files contain structured data for further processing")
            
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")


def cmd_transcribe_audio():
    """Quick transcription of audio files using Gemini."""
    print("🎤 AUDIO TRANSCRIPTION - Google Gemini")
    print("=" * 50)
    
    # Check requirements
    gemini_ready, message = check_gemini_requirements()
    if not gemini_ready:
        print(f"❌ Gemini not available: {message}")
        return
    
    current_dir = Path('.')
    audio_files = find_audio_files(current_dir)
    
    if not audio_files:
        print("📁 No audio files found in current directory")
        return
    
    print(f"🎵 Found {len(audio_files)} audio file(s)")
    
    include_timestamps = input("⏰ Include timestamps? (Y/n): ").strip().lower() != 'n'
    speaker_identification = input("👥 Speaker identification? (Y/n): ").strip().lower() != 'n'
    
    successful = 0
    failed = 0
    
    for audio_path in audio_files:
        print(f"\n🎵 Transcribing: {audio_path.name}")
        
        try:
            analyzer = GeminiVideoAnalyzer()
            result = analyzer.transcribe_audio(audio_path, include_timestamps, speaker_identification)
            
            if result:
                # Save as both JSON and text
                json_file = audio_path.parent / f"{audio_path.stem}_transcription.json"
                txt_file = audio_path.parent / f"{audio_path.stem}_transcription.txt"
                
                save_analysis_result(result, json_file)
                
                # Save text version
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(result['transcription'])
                
                print(f"📄 Transcription saved: {txt_file.name}")
                successful += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            failed += 1
    
    print(f"\n📊 Results: {successful} successful | {failed} failed")


def cmd_describe_audio():
    """Quick description of audio files using Gemini."""
    print("📝 AUDIO DESCRIPTION - Google Gemini")
    print("=" * 50)
    
    # Check requirements
    gemini_ready, message = check_gemini_requirements()
    if not gemini_ready:
        print(f"❌ Gemini not available: {message}")
        return
    
    current_dir = Path('.')
    audio_files = find_audio_files(current_dir)
    
    if not audio_files:
        print("📁 No audio files found in current directory")
        return
    
    print(f"🎵 Found {len(audio_files)} audio file(s)")
    
    detailed = input("📖 Generate detailed description? (y/N): ").strip().lower() == 'y'
    
    successful = 0
    failed = 0
    
    for audio_path in audio_files:
        print(f"\n🎵 Describing: {audio_path.name}")
        
        try:
            analyzer = GeminiVideoAnalyzer()
            result = analyzer.describe_audio(audio_path, detailed)
            
            if result:
                # Save result
                json_file = audio_path.parent / f"{audio_path.stem}_description.json"
                txt_file = audio_path.parent / f"{audio_path.stem}_description.txt"
                
                save_analysis_result(result, json_file)
                
                # Save text version
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(result['description'])
                
                print(f"📄 Description saved: {txt_file.name}")
                print(f"📋 Preview: {result['description'][:150]}...")
                successful += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ Description failed: {e}")
            failed += 1
    
    print(f"\n📊 Results: {successful} successful | {failed} failed")