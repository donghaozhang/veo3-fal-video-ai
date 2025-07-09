#!/usr/bin/env python3
"""
FAL AI Avatar Generation - Video Generation Test (PAID)

This script tests actual avatar video generation using FAL AI.
⚠️ WARNING: This script generates real avatar videos and costs money!

Each avatar video generation costs approximately $0.02-0.05 depending on frame count.

Test scenarios:
- Basic avatar generation with default settings (text-to-speech)
- Audio-to-avatar generation with custom audio files
- Multi-audio conversation generation (two-person dialogue)
- Custom voice testing
- Different frame counts
- Multi-avatar comparison (multiple voices)

Usage:
    python test_generation.py [options]
    
Options:
    --quick         Quick test with minimal frames (81 frames)
    --standard      Standard test with default frames (136 frames)
    --audio         Test audio-to-avatar generation
    --multi         Test multi-audio conversation generation
    --compare       Compare multiple voices (costs more - generates multiple videos)
    --voice NAME    Test specific voice (e.g., --voice Sarah)
    --frames N      Custom frame count (81-129)
    --no-turbo      Disable turbo mode
"""

import os
import sys
import time
import argparse
from pathlib import Path
from fal_avatar_generator import FALAvatarGenerator

def get_user_confirmation(test_name: str, cost_estimate: str, details: str = "") -> bool:
    """Get user confirmation for paid operations"""
    print(f"\n⚠️ WARNING: {test_name} will generate real avatar videos and cost money!")
    print(f"💰 Estimated cost: {cost_estimate}")
    print(f"💳 This will charge your FAL AI account.")
    if details:
        print(f"📋 Details: {details}")
    
    while True:
        response = input("\nDo you want to proceed? (yes/no): ").lower().strip()
        if response in ['yes', 'y', 'proceed', 'run']:
            return True
        elif response in ['no', 'n', 'cancel', 'stop']:
            return False
        else:
            print("Please enter 'yes' or 'no'")

def get_test_image() -> str:
    """Get a test image URL or local file"""
    # Official test image from FAL AI documentation
    official_image = "https://v3.fal.media/files/panda/HuM21CXMf0q7OO2zbvwhV_c4533aada79a495b90e50e32dc9b83a8.png"
    
    # Check for local test images first
    test_images = [
        "images/test_avatar.jpg",
        "images/person.jpg",
        "../veo3_video_generation/images/smiling_woman.jpg",
        "test_image.jpg"
    ]
    
    for img_path in test_images:
        if os.path.isfile(img_path):
            print(f"📷 Using local test image: {img_path}")
            return img_path
    
    print(f"📷 Using official FAL AI example image")
    return official_image

def test_basic_generation(generator: FALAvatarGenerator, args) -> bool:
    """Test basic avatar generation"""
    print("\n🎭 Testing Basic Avatar Generation")
    print("-" * 40)
    
    # Cost estimation
    base_cost = 0.03
    cost_multiplier = 1.25 if args.frames > 81 else 1.0
    estimated_cost = f"~${base_cost * cost_multiplier:.3f}"
    
    details = f"1 video, {args.frames} frames, voice: {args.voice}"
    if not get_user_confirmation("Basic Avatar Test", estimated_cost, details):
        print("❌ Basic generation test cancelled")
        return False
    
    try:
        # Test parameters
        image_url = get_test_image()
        # Official text from FAL AI documentation
        text_input = "Spend more time with people who make you feel alive, and less with things that drain your soul."
        
        print(f"🚀 Starting basic avatar generation...")
        print(f"   Image: {image_url}")
        print(f"   Text: {text_input[:50]}...")
        print(f"   Voice: {args.voice}")
        print(f"   Frames: {args.frames}")
        print(f"   Turbo: {not args.no_turbo}")
        
        # Generate output path
        timestamp = int(time.time())
        output_path = f"output/basic_avatar_{timestamp}.mp4"
        
        # Generate avatar video
        result = generator.generate_avatar_video(
            image_url=image_url,
            text_input=text_input,
            voice=args.voice,
            prompt="An elderly man with a white beard and headphones records audio with a microphone. He appears engaged and expressive, suggesting a podcast or voiceover.",
            num_frames=args.frames,
            turbo=not args.no_turbo,
            output_path=output_path
        )
        
        if result and 'video' in result:
            print(f"✅ Basic avatar generation successful!")
            print(f"📁 Saved to: {output_path}")
            print(f"⏱️ Generation time: {result.get('generation_time', 0):.2f} seconds")
            
            video_info = result['video']
            print(f"📊 File size: {video_info.get('file_size', 0) / (1024*1024):.2f} MB")
            return True
        else:
            print(f"❌ Basic avatar generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in basic generation test: {str(e)}")
        return False

def test_voice_comparison(generator: FALAvatarGenerator, args) -> bool:
    """Test multiple voices for comparison"""
    print("\n🎤 Testing Voice Comparison")
    print("-" * 40)
    
    # Select test voices
    all_voices = generator.get_available_voices()
    test_voices = ["Sarah", "Roger", "Bill", "Alice"]
    
    # Filter available voices
    available_test_voices = [v for v in test_voices if v in all_voices]
    if len(available_test_voices) < 2:
        available_test_voices = all_voices[:3]  # Use first 3 if test voices not available
    
    num_videos = len(available_test_voices)
    base_cost = 0.03
    cost_multiplier = 1.25 if args.frames > 81 else 1.0
    total_cost = base_cost * cost_multiplier * num_videos
    estimated_cost = f"~${total_cost:.3f}"
    
    details = f"{num_videos} videos, {args.frames} frames each, voices: {', '.join(available_test_voices)}"
    if not get_user_confirmation("Voice Comparison Test", estimated_cost, details):
        print("❌ Voice comparison test cancelled")
        return False
    
    try:
        image_url = get_test_image()
        # Use official text from FAL AI documentation for consistency
        text_input = "Spend more time with people who make you feel alive, and less with things that drain your soul."
        
        results = []
        timestamp = int(time.time())
        
        for i, voice in enumerate(available_test_voices):
            print(f"\n🎤 Generating avatar {i+1}/{num_videos} with voice: {voice}")
            
            output_path = f"output/voice_comparison_{voice.lower()}_{timestamp}.mp4"
            
            result = generator.generate_avatar_video(
                image_url=image_url,
                text_input=text_input,
                voice=voice,
                prompt="An elderly man with a white beard and headphones records audio with a microphone. He appears engaged and expressive, suggesting a podcast or voiceover.",
                num_frames=args.frames,
                turbo=not args.no_turbo,
                output_path=output_path
            )
            
            if result and 'video' in result:
                results.append({
                    'voice': voice,
                    'path': output_path,
                    'result': result
                })
                print(f"✅ Voice {voice} generation successful!")
            else:
                print(f"❌ Voice {voice} generation failed")
        
        if results:
            print(f"\n🎉 Voice comparison test completed!")
            print(f"📊 Generated {len(results)}/{num_videos} videos:")
            
            for r in results:
                video_info = r['result']['video']
                size_mb = video_info.get('file_size', 0) / (1024*1024)
                gen_time = r['result'].get('generation_time', 0)
                print(f"   🎤 {r['voice']}: {r['path']} ({size_mb:.2f} MB, {gen_time:.1f}s)")
            
            return len(results) > 0
        else:
            print(f"❌ All voice generations failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in voice comparison test: {str(e)}")
        return False

def test_custom_scenarios(generator: FALAvatarGenerator, args) -> bool:
    """Test custom avatar scenarios"""
    print("\n🎬 Testing Custom Avatar Scenarios")
    print("-" * 40)
    
    scenarios = [
        {
            "name": "Professional Presentation",
            "text": "Good morning everyone. Today I'll be presenting our quarterly results and discussing our strategic initiatives for the upcoming fiscal year.",
            "prompt": "A professional person in business attire presenting to an audience with confident and engaging expressions."
        },
        {
            "name": "Educational Content",
            "text": "Welcome to today's lesson on artificial intelligence. We'll explore how machine learning algorithms can generate realistic avatar videos with synchronized speech.",
            "prompt": "An educator or teacher explaining concepts with clear articulation and engaging facial expressions."
        }
    ]
    
    num_videos = len(scenarios)
    base_cost = 0.03
    cost_multiplier = 1.25 if args.frames > 81 else 1.0
    total_cost = base_cost * cost_multiplier * num_videos
    estimated_cost = f"~${total_cost:.3f}"
    
    details = f"{num_videos} scenario videos, {args.frames} frames each"
    if not get_user_confirmation("Custom Scenarios Test", estimated_cost, details):
        print("❌ Custom scenarios test cancelled")
        return False
    
    try:
        image_url = get_test_image()
        results = []
        timestamp = int(time.time())
        
        for i, scenario in enumerate(scenarios):
            print(f"\n🎬 Generating scenario {i+1}/{num_videos}: {scenario['name']}")
            
            output_path = f"output/scenario_{scenario['name'].lower().replace(' ', '_')}_{timestamp}.mp4"
            
            result = generator.generate_avatar_video(
                image_url=image_url,
                text_input=scenario['text'],
                voice=args.voice,
                prompt=scenario['prompt'],
                num_frames=args.frames,
                turbo=not args.no_turbo,
                output_path=output_path
            )
            
            if result and 'video' in result:
                results.append({
                    'scenario': scenario['name'],
                    'path': output_path,
                    'result': result
                })
                print(f"✅ Scenario '{scenario['name']}' generation successful!")
            else:
                print(f"❌ Scenario '{scenario['name']}' generation failed")
        
        if results:
            print(f"\n🎉 Custom scenarios test completed!")
            print(f"📊 Generated {len(results)}/{num_videos} videos:")
            
            for r in results:
                video_info = r['result']['video']
                size_mb = video_info.get('file_size', 0) / (1024*1024)
                gen_time = r['result'].get('generation_time', 0)
                print(f"   🎬 {r['scenario']}: {r['path']} ({size_mb:.2f} MB, {gen_time:.1f}s)")
            
            return len(results) > 0
        else:
            print(f"❌ All scenario generations failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in custom scenarios test: {str(e)}")
        return False

def test_audio_generation(generator: FALAvatarGenerator, args) -> bool:
    """Test audio-to-avatar generation"""
    print("\n🎵 Testing Audio-to-Avatar Generation")
    print("-" * 40)
    
    # Cost estimation
    base_cost = 0.03
    cost_multiplier = 1.25 if args.frames > 81 else 1.0
    estimated_cost = f"~${base_cost * cost_multiplier:.3f}"
    
    details = f"1 video, {args.frames} frames, audio-to-avatar mode"
    if not get_user_confirmation("Audio-to-Avatar Test", estimated_cost, details):
        print("❌ Audio generation test cancelled")
        return False
    
    try:
        # Test parameters
        image_url = get_test_image()
        
        # Use a sample audio URL or create a simple test audio
        # For demo purposes, we'll use a placeholder audio URL
        # In real usage, users would provide their own audio files
        audio_url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"  # Sample audio
        
        print(f"🚀 Starting audio-to-avatar generation...")
        print(f"   Image: {image_url}")
        print(f"   Audio: {audio_url}")
        print(f"   Frames: {args.frames}")
        print(f"   Turbo: {not args.no_turbo}")
        
        # Generate output path
        timestamp = int(time.time())
        output_path = f"output/audio_avatar_{timestamp}.mp4"
        
        # Generate avatar video from audio
        result = generator.generate_avatar_from_audio(
            image_url=image_url,
            audio_url=audio_url,
            prompt="A person speaking naturally with clear lip-sync matching the provided audio.",
            num_frames=args.frames,
            turbo=not args.no_turbo,
            output_path=output_path
        )
        
        if result and 'video' in result:
            print(f"✅ Audio-to-avatar generation successful!")
            print(f"📁 Saved to: {output_path}")
            print(f"⏱️ Generation time: {result.get('generation_time', 0):.2f} seconds")
            
            video_info = result['video']
            print(f"📊 File size: {video_info.get('file_size', 0) / (1024*1024):.2f} MB")
            return True
        else:
            print(f"❌ Audio-to-avatar generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in audio generation test: {str(e)}")
        return False

def test_multi_audio_generation(generator: FALAvatarGenerator, args) -> bool:
    """Test multi-audio conversation generation"""
    print("\n🎭 Testing Multi-Audio Conversation Generation")
    print("-" * 40)
    
    # Cost estimation
    base_cost = 0.03
    cost_multiplier = 1.25 if args.frames > 81 else 1.0
    estimated_cost = f"~${base_cost * cost_multiplier:.3f}"
    
    details = f"1 conversation video, {args.frames} frames, two-person conversation"
    if not get_user_confirmation("Multi-Audio Conversation Test", estimated_cost, details):
        print("❌ Multi-audio generation test cancelled")
        return False
    
    try:
        # Test parameters
        image_url = get_test_image()
        
        # Use sample audio URLs for demonstration
        # In real usage, users would provide their own conversation audio files
        first_audio_url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"  # Sample audio 1
        second_audio_url = "https://www2.cs.uic.edu/~i101/SoundFiles/CantinaBand60.wav"  # Sample audio 2
        
        print(f"🚀 Starting multi-audio conversation generation...")
        print(f"   Image: {image_url}")
        print(f"   First audio: {first_audio_url}")
        print(f"   Second audio: {second_audio_url}")
        print(f"   Frames: {args.frames}")
        print(f"   Turbo: {not args.no_turbo}")
        
        # Generate output path
        timestamp = int(time.time())
        output_path = f"output/multi_conversation_{timestamp}.mp4"
        
        # Generate multi-avatar conversation video
        result = generator.generate_multi_avatar_conversation(
            image_url=image_url,
            first_audio_url=first_audio_url,
            second_audio_url=second_audio_url,
            prompt="Two people engaged in a natural conversation, speaking in sequence with clear lip-sync and natural expressions. The scene captures a lively conversational exchange between both speakers.",
            num_frames=args.frames,
            turbo=not args.no_turbo,
            output_path=output_path
        )
        
        if result and 'video' in result:
            print(f"✅ Multi-audio conversation generation successful!")
            print(f"📁 Saved to: {output_path}")
            print(f"⏱️ Generation time: {result.get('generation_time', 0):.2f} seconds")
            
            video_info = result['video']
            print(f"📊 File size: {video_info.get('file_size', 0) / (1024*1024):.2f} MB")
            return True
        else:
            print(f"❌ Multi-audio conversation generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in multi-audio generation test: {str(e)}")
        return False

def main():
    """Main test function"""
    parser = argparse.ArgumentParser(description="FAL AI Avatar Generation Tests (PAID)")
    parser.add_argument('--quick', action='store_true', help='Quick test with minimal frames (81)')
    parser.add_argument('--standard', action='store_true', help='Standard test with default frames (136)')
    parser.add_argument('--audio', action='store_true', help='Test audio-to-avatar generation')
    parser.add_argument('--multi', action='store_true', help='Test multi-audio conversation generation')
    parser.add_argument('--compare', action='store_true', help='Compare multiple voices (costs more)')
    parser.add_argument('--scenarios', action='store_true', help='Test custom scenarios')
    parser.add_argument('--voice', default='Bill', help='Voice to use for testing (default: Bill - from official example)')
    parser.add_argument('--frames', type=int, help='Custom frame count (81-129)')
    parser.add_argument('--no-turbo', action='store_true', help='Disable turbo mode')
    
    args = parser.parse_args()
    
    # Set frame count based on options
    if args.quick:
        args.frames = 81
    elif args.standard:
        args.frames = 136
    elif not args.frames:
        args.frames = 136  # Default
    
    # Validate frame count
    if not (81 <= args.frames <= 129):
        print(f"❌ Frame count must be between 81 and 129, got {args.frames}")
        sys.exit(1)
    
    print("🧪 FAL AI Avatar Generation - Video Generation Tests (PAID)")
    print("=" * 70)
    print("⚠️ WARNING: These tests generate real videos and cost money!")
    print(f"💰 Each video costs approximately $0.02-0.05")
    
    try:
        # Initialize generator
        print(f"\n🔧 Initializing FAL Avatar Generator...")
        generator = FALAvatarGenerator()
        
        # Create test output directory
        os.makedirs("output", exist_ok=True)
        
        # Run tests based on arguments
        tests_run = []
        tests_passed = []
        
        if not any([args.audio, args.multi, args.compare, args.scenarios]):
            # Default: run basic test
            tests_run.append("Basic Generation")
            if test_basic_generation(generator, args):
                tests_passed.append("Basic Generation")
        
        if args.audio:
            tests_run.append("Audio-to-Avatar")
            if test_audio_generation(generator, args):
                tests_passed.append("Audio-to-Avatar")
        
        if args.multi:
            tests_run.append("Multi-Audio Conversation")
            if test_multi_audio_generation(generator, args):
                tests_passed.append("Multi-Audio Conversation")
        
        if args.compare:
            tests_run.append("Voice Comparison")
            if test_voice_comparison(generator, args):
                tests_passed.append("Voice Comparison")
        
        if args.scenarios:
            tests_run.append("Custom Scenarios")
            if test_custom_scenarios(generator, args):
                tests_passed.append("Custom Scenarios")
        
        # Summary
        print(f"\n" + "=" * 70)
        print(f"📊 Test Results Summary:")
        print(f"   Tests run: {len(tests_run)}")
        print(f"   Tests passed: {len(tests_passed)}")
        
        for test in tests_run:
            status = "✅ PASS" if test in tests_passed else "❌ FAIL"
            print(f"   {status} {test}")
        
        if len(tests_passed) == len(tests_run):
            print(f"\n🎉 All tests passed! Avatar generation is working correctly.")
        else:
            print(f"\n⚠️ Some tests failed. Check the output above for details.")
        
        print(f"\n📁 Generated videos saved in: output/")
        
    except KeyboardInterrupt:
        print(f"\n❌ Tests cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during tests: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 