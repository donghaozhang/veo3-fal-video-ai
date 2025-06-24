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

def main():
    """Main demo function"""
    print("🎭 FAL AI Avatar Video Generation Demo")
    print("=" * 50)
    print("Generate talking avatar videos from images and text!")
    print("Features: 20 voice options, lip-sync, natural expressions")
    
    try:
        # Initialize generator
        print("\n🔧 Initializing FAL Avatar Generator...")
        generator = FALAvatarGenerator()
        
        # Get available voices
        voices = generator.get_available_voices()
        display_voices(voices)
        
        # Get user inputs
        print("\n" + "=" * 50)
        print("📋 Setup Avatar Generation")
        
        # Get image
        image_input = get_image_input()
        print(f"✅ Image selected: {image_input}")
        
        # Get text
        text_input = get_text_input()
        print(f"✅ Text entered: {text_input[:50]}{'...' if len(text_input) > 50 else ''}")
        
        # Get voice
        voice = get_voice_choice(voices)
        print(f"✅ Voice selected: {voice}")
        
        # Get additional parameters
        print(f"\n⚙️ Additional Parameters:")
        
        # Frame count
        while True:
            try:
                frames_input = input("Number of frames (81-129, default 136): ").strip()
                if not frames_input:
                    num_frames = 136
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
        output_filename = f"avatar_video_{timestamp}.mp4"
        output_path = os.path.join(output_dir, output_filename)
        
        print(f"\n🚀 Starting avatar video generation...")
        print(f"📊 Parameters:")
        print(f"   - Image: {os.path.basename(image_input) if os.path.isfile(image_input) else image_input}")
        print(f"   - Text length: {len(text_input)} characters")
        print(f"   - Voice: {voice}")
        print(f"   - Frames: {num_frames}")
        print(f"   - Turbo: {turbo}")
        print(f"   - Output: {output_path}")
        
        # Generate avatar video
        result = generator.generate_avatar_video(
            image_url=image_input,
            text_input=text_input,
            voice=voice,
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