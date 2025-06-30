"""
AI analysis command implementations using Google Gemini.

Contains commands for AI-powered video, audio, and image analysis.
"""

from pathlib import Path

from .core import get_video_info
from .file_utils import find_video_files, find_audio_files, find_image_files
from .video_understanding import (
    check_gemini_requirements,
    analyze_video_file,
    analyze_audio_file,
    analyze_image_file,
    save_analysis_result,
    GeminiVideoAnalyzer
)


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
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("📁 Input directory 'input' not found")
        print("💡 Create an 'input' directory and place your video files there")
        return
    
    video_files = find_video_files(input_dir)
    
    if not video_files:
        print("📁 No video files found in input directory")
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
                    output_file = output_dir / f"{video_path.stem}_{analysis_type}_analysis.json"
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
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("📁 Input directory 'input' not found")
        print("💡 Create an 'input' directory and place your video files there")
        return
    
    video_files = find_video_files(input_dir)
    
    if not video_files:
        print("📁 No video files found in input directory")
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
                json_file = output_dir / f"{video_path.stem}_transcription.json"
                txt_file = output_dir / f"{video_path.stem}_transcription.txt"
                
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
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("📁 Input directory 'input' not found")
        print("💡 Create an 'input' directory and place your video files there")
        return
    
    video_files = find_video_files(input_dir)
    
    if not video_files:
        print("📁 No video files found in input directory")
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
                json_file = output_dir / f"{video_path.stem}_description.json"
                txt_file = output_dir / f"{video_path.stem}_description.txt"
                
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
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("📁 Input directory 'input' not found")
        print("💡 Create an 'input' directory and place your audio files there")
        return
    
    audio_files = find_audio_files(input_dir)
    
    if not audio_files:
        print("📁 No audio files found in input directory")
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
                    output_file = output_dir / f"{audio_path.stem}_{analysis_type}_analysis.json"
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
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("📁 Input directory 'input' not found")
        print("💡 Create an 'input' directory and place your audio files there")
        return
    
    audio_files = find_audio_files(input_dir)
    
    if not audio_files:
        print("📁 No audio files found in input directory")
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
                json_file = output_dir / f"{audio_path.stem}_transcription.json"
                txt_file = output_dir / f"{audio_path.stem}_transcription.txt"
                
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
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("📁 Input directory 'input' not found")
        print("💡 Create an 'input' directory and place your audio files there")
        return
    
    audio_files = find_audio_files(input_dir)
    
    if not audio_files:
        print("📁 No audio files found in input directory")
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
                json_file = output_dir / f"{audio_path.stem}_description.json"
                txt_file = output_dir / f"{audio_path.stem}_description.txt"
                
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


def cmd_analyze_images():
    """Comprehensive image analysis using Gemini."""
    print("🖼️ IMAGE ANALYSIS - Google Gemini")
    print("=" * 50)
    
    # Check requirements
    gemini_ready, message = check_gemini_requirements()
    if not gemini_ready:
        print(f"❌ Gemini not available: {message}")
        return
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("📁 Input directory 'input' not found")
        print("💡 Create an 'input' directory and place your image files there")
        return
    
    image_files = find_image_files(input_dir)
    
    if not image_files:
        print("📁 No image files found in input directory")
        return
    
    print(f"🖼️ Found {len(image_files)} image file(s)")
    
    # Analysis type selection
    analysis_types = {
        '1': ('description', 'Image description and visual analysis'),
        '2': ('classification', 'Image classification and categorization'),
        '3': ('objects', 'Object detection and identification'),
        '4': ('text', 'Text extraction (OCR) from images'),
        '5': ('composition', 'Artistic and technical composition analysis'),
        '6': ('qa', 'Question and answer analysis')
    }
    
    print("\n🎯 Available analysis types:")
    for key, (type_name, description) in analysis_types.items():
        print(f"   {key}. {description}")
    
    try:
        choice = input("\n📝 Select analysis type (1-6): ").strip()
        if choice not in analysis_types:
            print("❌ Invalid selection")
            return
        
        analysis_type, _ = analysis_types[choice]
        
        # Additional options
        detailed = False
        questions = None
        
        if analysis_type in ['description', 'objects']:
            detailed = input("📖 Detailed analysis? (y/N): ").strip().lower() == 'y'
        elif analysis_type == 'qa':
            print("\n❓ Enter questions (one per line, empty line to finish):")
            questions = []
            while True:
                q = input("   Question: ").strip()
                if not q:
                    break
                questions.append(q)
            if not questions:
                questions = ["What is the main subject of this image?", "What can you tell me about this image?"]
        
        successful = 0
        failed = 0
        
        for image_path in image_files:
            print(f"\n🖼️ Analyzing: {image_path.name}")
            
            try:
                result = analyze_image_file(
                    image_path, 
                    analysis_type, 
                    questions=questions,
                    detailed=detailed
                )
                
                if result:
                    # Save result
                    output_file = output_dir / f"{image_path.stem}_{analysis_type}_analysis.json"
                    if save_analysis_result(result, output_file):
                        successful += 1
                        
                        # Show preview of result
                        print(f"\n📋 Analysis Preview:")
                        if analysis_type == 'description':
                            preview = result['description'][:200] + "..." if len(result['description']) > 200 else result['description']
                            print(f"'{preview}'")
                        elif analysis_type == 'classification':
                            preview = result['classification'][:200] + "..." if len(result['classification']) > 200 else result['classification']
                            print(f"'{preview}'")
                        elif analysis_type == 'objects':
                            preview = result['objects'][:200] + "..." if len(result['objects']) > 200 else result['objects']
                            print(f"'{preview}'")
                        elif analysis_type == 'text':
                            preview = result['extracted_text'][:200] + "..." if len(result['extracted_text']) > 200 else result['extracted_text']
                            print(f"'{preview}'")
                        elif analysis_type == 'composition':
                            preview = result['composition_analysis'][:200] + "..." if len(result['composition_analysis']) > 200 else result['composition_analysis']
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


def cmd_describe_images():
    """Quick description of images using Gemini."""
    print("📝 IMAGE DESCRIPTION - Google Gemini")
    print("=" * 50)
    
    # Check requirements
    gemini_ready, message = check_gemini_requirements()
    if not gemini_ready:
        print(f"❌ Gemini not available: {message}")
        return
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("📁 Input directory 'input' not found")
        print("💡 Create an 'input' directory and place your image files there")
        return
    
    image_files = find_image_files(input_dir)
    
    if not image_files:
        print("📁 No image files found in input directory")
        return
    
    print(f"🖼️ Found {len(image_files)} image file(s)")
    
    detailed = input("📖 Generate detailed description? (y/N): ").strip().lower() == 'y'
    
    successful = 0
    failed = 0
    
    for image_path in image_files:
        print(f"\n🖼️ Describing: {image_path.name}")
        
        try:
            analyzer = GeminiVideoAnalyzer()
            result = analyzer.describe_image(image_path, detailed)
            
            if result:
                # Save result
                json_file = output_dir / f"{image_path.stem}_description.json"
                txt_file = output_dir / f"{image_path.stem}_description.txt"
                
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


def cmd_extract_text():
    """Extract text from images using Gemini OCR."""
    print("📝 IMAGE TEXT EXTRACTION - Google Gemini OCR")
    print("=" * 50)
    
    # Check requirements
    gemini_ready, message = check_gemini_requirements()
    if not gemini_ready:
        print(f"❌ Gemini not available: {message}")
        return
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("📁 Input directory 'input' not found")
        print("💡 Create an 'input' directory and place your image files there")
        return
    
    image_files = find_image_files(input_dir)
    
    if not image_files:
        print("📁 No image files found in input directory")
        return
    
    print(f"🖼️ Found {len(image_files)} image file(s)")
    
    successful = 0
    failed = 0
    
    for image_path in image_files:
        print(f"\n🖼️ Extracting text from: {image_path.name}")
        
        try:
            analyzer = GeminiVideoAnalyzer()
            result = analyzer.extract_text_from_image(image_path)
            
            if result:
                # Save result
                json_file = output_dir / f"{image_path.stem}_text.json"
                txt_file = output_dir / f"{image_path.stem}_text.txt"
                
                save_analysis_result(result, json_file)
                
                # Save text version
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(result['extracted_text'])
                
                print(f"📄 Extracted text saved: {txt_file.name}")
                
                # Show preview if text was found
                text_preview = result['extracted_text'][:200]
                if "no readable text" not in text_preview.lower():
                    print(f"📋 Text Preview: {text_preview}...")
                else:
                    print("📋 No readable text found in image")
                
                successful += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ Text extraction failed: {e}")
            failed += 1
    
    print(f"\n📊 Results: {successful} successful | {failed} failed")