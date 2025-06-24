#!/usr/bin/env python3
"""
FAL AI Avatar Generation Demo

Interactive demonstration of the FAL AI Avatar Video Generator.
This script provides a user-friendly interface to generate talking avatar videos
from images and text with various voice options.

⚠️ WARNING: This demo generates real avatar videos and costs money!
Each avatar video generation costs approximately $0.02-0.05 depending on frame count.

Usage:
    python demo.py
"""

import os
import sys
from pathlib import Path
from fal_avatar_generator import FALAvatarGenerator

def get_user_confirmation(cost_estimate: str) -> bool:
    """Get user confirmation for paid operations"""
    print(f"\n⚠️ WARNING: This will generate a real avatar video and cost money!")
    print(f"💰 Estimated cost: {cost_estimate}")
    print(f"💳 This will charge your FAL AI account.")
    
    while True:
        response = input("\nDo you want to proceed? (yes/no): ").lower().strip()
        if response in ['yes', 'y', 'proceed', 'run']:
            return True
        elif response in ['no', 'n', 'cancel', 'stop']:
            return False
        else:
            print("Please enter 'yes' or 'no'")

def display_voices(voices: list):
    """Display available voices in a formatted list"""
    print("\n🎤 Available Voices:")
    print("=" * 50)
    
    # Display in columns for better readability
    for i in range(0, len(voices), 4):
        row = voices[i:i+4]
        formatted_row = []
        for j, voice in enumerate(row):
            formatted_row.append(f"{i+j+1:2d}. {voice:<12}")
        print("  ".join(formatted_row))

def get_voice_choice(voices: list) -> str:
    """Get voice selection from user"""
    while True:
        try:
            choice = input(f"\nSelect voice (1-{len(voices)} or name): ").strip()
            
            # Check if it's a number
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(voices):
                    return voices[index]
                else:
                    print(f"Please enter a number between 1 and {len(voices)}")
            
            # Check if it's a voice name
            elif choice in voices:
                return choice
            
            # Check case-insensitive match
            else:
                for voice in voices:
                    if voice.lower() == choice.lower():
                        return voice
                
                print(f"Voice '{choice}' not found. Please try again.")
                
        except ValueError:
            print("Invalid input. Please enter a number or voice name.")

def get_sample_images():
    """Get list of available sample images"""
    sample_images = []
    
    # Check for images in common locations
    image_dirs = [
        "images",
        "../veo3_video_generation/images",
        "../fal_video_generation/output",
        "samples"
    ]
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
    
    for img_dir in image_dirs:
        if os.path.exists(img_dir):
            for file in os.listdir(img_dir):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    sample_images.append(os.path.join(img_dir, file))
    
    return sample_images

def get_image_input() -> str:
    """Get image input from user (URL or local file)"""
    print("\n🖼️ Image Input Options:")
    print("1. Use image URL")
    print("2. Use local image file")
    
    sample_images = get_sample_images()
    if sample_images:
        print("3. Use sample image")
    
    while True:
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            url = input("Enter image URL: ").strip()
            if url:
                return url
            else:
                print("Please enter a valid URL")
        
        elif choice == "2":
            path = input("Enter local image path: ").strip()
            if os.path.isfile(path):
                return path
            else:
                print("File not found. Please enter a valid path.")
        
        elif choice == "3" and sample_images:
            print("\n📁 Available sample images:")
            for i, img in enumerate(sample_images[:10], 1):  # Show max 10
                print(f"  {i}. {os.path.basename(img)} ({img})")
            
            try:
                img_choice = int(input(f"Select image (1-{min(len(sample_images), 10)}): ")) - 1
                if 0 <= img_choice < len(sample_images):
                    return sample_images[img_choice]
                else:
                    print("Invalid selection")
            except ValueError:
                print("Please enter a number")
        
        else:
            print("Invalid option. Please try again.")

def get_text_input() -> str:
    """Get text input from user"""
    print("\n📝 Text Input:")
    print("Enter the text that the avatar should speak.")
    print("(Press Enter twice to finish, or Ctrl+C to cancel)")
    
    lines = []
    empty_lines = 0
    
    try:
        while True:
            line = input()
            if line.strip() == "":
                empty_lines += 1
                if empty_lines >= 2:
                    break
            else:
                empty_lines = 0
                lines.append(line)
        
        text = "\n".join(lines).strip()
        if not text:
            # Provide default text if none entered
            text = "Hello! This is a demonstration of AI-generated avatar video with lip-sync technology."
            print(f"Using default text: {text}")
        
        return text
        
    except KeyboardInterrupt:
        print("\n❌ Text input cancelled")
        sys.exit(0)

def get_audio_input() -> str:
    """Get audio input from user (URL or local file)"""
    print("\n🎵 Audio Input Options:")
    print("1. Use audio URL")
    print("2. Use local audio file")
    
    # Check for sample audio files
    audio_extensions = ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac']
    sample_audio = []
    
    audio_dirs = ["audio", "samples", "../audio"]
    for audio_dir in audio_dirs:
        if os.path.exists(audio_dir):
            for file in os.listdir(audio_dir):
                if any(file.lower().endswith(ext) for ext in audio_extensions):
                    sample_audio.append(os.path.join(audio_dir, file))
    
    if sample_audio:
        print("3. Use sample audio")
    
    while True:
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            url = input("Enter audio URL: ").strip()
            if url:
                return url
            else:
                print("Please enter a valid URL")
        
        elif choice == "2":
            path = input("Enter local audio path: ").strip()
            if os.path.isfile(path):
                return path
            else:
                print("File not found. Please enter a valid path.")
        
        elif choice == "3" and sample_audio:
            print("\n📁 Available sample audio files:")
            for i, audio in enumerate(sample_audio[:10], 1):  # Show max 10
                print(f"  {i}. {os.path.basename(audio)} ({audio})")
            
            try:
                audio_choice = int(input(f"Select audio (1-{min(len(sample_audio), 10)}): ")) - 1
                if 0 <= audio_choice < len(sample_audio):
                    return sample_audio[audio_choice]
                else:
                    print("Invalid selection")
            except ValueError:
                print("Please enter a number")
        
        else:
            print("Invalid option. Please try again.")

def main():
    """Main demo function"""
    print("🎭 FAL AI Avatar Video Generation Demo")
    print("=" * 50)
    print("Generate talking avatar videos from images!")
    print("Features: Text-to-speech (20 voices) OR custom audio with lip-sync")
    
    try:
        # Initialize generator
        print("\n🔧 Initializing FAL Avatar Generator...")
        generator = FALAvatarGenerator()
        
        # Choose generation mode
        print("\n🎬 Generation Mode:")
        print("1. Text-to-Speech (choose from 20 voices)")
        print("2. Audio-to-Avatar (use your own audio file)")
        
        while True:
            mode_choice = input("\nSelect mode (1-2): ").strip()
            if mode_choice in ["1", "2"]:
                break
            print("Please enter 1 or 2")
        
        # Get user inputs
        print("\n" + "=" * 50)
        print("📋 Setup Avatar Generation")
        
        # Get image
        image_input = get_image_input()
        print(f"✅ Image selected: {image_input}")
        
        # Get text or audio based on mode
        if mode_choice == "1":
            # Text-to-speech mode
            # Get available voices
            voices = generator.get_available_voices()
            display_voices(voices)
            
            # Get text
            text_input = get_text_input()
            print(f"✅ Text entered: {text_input[:50]}{'...' if len(text_input) > 50 else ''}")
            
            # Get voice
            voice = get_voice_choice(voices)
            print(f"✅ Voice selected: {voice}")
            
            # Default frame count for text mode
            default_frames = 136
            
        else:
            # Audio-to-avatar mode
            audio_input = get_audio_input()
            print(f"✅ Audio selected: {audio_input}")
            
            # No voice selection needed for audio mode
            text_input = None
            voice = None
            
            # Default frame count for audio mode
            default_frames = 145
        
        # Get additional parameters
        print(f"\n⚙️ Additional Parameters:")
        
        # Frame count
        while True:
            try:
                frames_input = input(f"Number of frames (81-129, default {default_frames}): ").strip()
                if not frames_input:
                    num_frames = default_frames
                    break
                
                num_frames = int(frames_input)
                if 81 <= num_frames <= 129:
                    break
                else:
                    print("Frame count must be between 81 and 129")
            except ValueError:
                print("Please enter a valid number")
        
        # Turbo mode
        turbo_input = input("Use turbo mode for faster generation? (Y/n): ").strip().lower()
        turbo = turbo_input != 'n'
        
        # Custom prompt
        custom_prompt = input("Custom prompt (optional, press Enter for default): ").strip()
        if not custom_prompt:
            custom_prompt = "A person speaking naturally with clear lip-sync and natural expressions."
        
        # Cost estimation
        base_cost = 0.03  # Approximate cost per generation
        if num_frames > 81:
            cost_multiplier = 1.25
        else:
            cost_multiplier = 1.0
        
        estimated_cost = f"~${base_cost * cost_multiplier:.3f}"
        
        # Get confirmation
        if not get_user_confirmation(estimated_cost):
            print("❌ Avatar generation cancelled by user")
            return
        
        # Prepare output path
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        import time
        timestamp = int(time.time())
        mode_suffix = "text" if mode_choice == "1" else "audio"
        output_filename = f"avatar_{mode_suffix}_{timestamp}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"\n🚀 Starting avatar video generation...")
        print(f"📊 Parameters:")
        print(f"   - Mode: {'Text-to-Speech' if mode_choice == '1' else 'Audio-to-Avatar'}")
        print(f"   - Image: {os.path.basename(image_input) if os.path.isfile(image_input) else image_input}")
        
        if mode_choice == "1":
            print(f"   - Text length: {len(text_input)} characters")
            print(f"   - Voice: {voice}")
        else:
            print(f"   - Audio: {os.path.basename(audio_input) if os.path.isfile(audio_input) else audio_input}")
        
        print(f"   - Frames: {num_frames}")
        print(f"   - Turbo: {turbo}")
        print(f"   - Output: {output_path}")
        
        # Generate avatar video based on mode
        if mode_choice == "1":
            # Text-to-speech mode
            result = generator.generate_avatar_video(
                image_url=image_input,
                text_input=text_input,
                voice=voice,
                prompt=custom_prompt,
                num_frames=num_frames,
                turbo=turbo,
                output_path=output_path
            )
        else:
            # Audio-to-avatar mode
            result = generator.generate_avatar_from_audio(
                image_url=image_input,
                audio_url=audio_input,
                prompt=custom_prompt,
                num_frames=num_frames,
                turbo=turbo,
                output_path=output_path
            )
        
        print(f"\n🎉 Avatar video generation completed!")
        print(f"📁 Saved to: {output_path}")
        print(f"⏱️ Generation time: {result.get('generation_time', 0):.2f} seconds")
        
        if 'video' in result:
            video_info = result['video']
            print(f"📊 File size: {video_info.get('file_size', 0) / (1024*1024):.2f} MB")
            print(f"🔗 Online URL: {video_info['url']}")
        
        print(f"\n✨ Demo completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n❌ Demo cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 