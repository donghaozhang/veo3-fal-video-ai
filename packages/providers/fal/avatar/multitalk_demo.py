#!/usr/bin/env python3
"""
Replicate MultiTalk Demo

This script demonstrates how to use the MultiTalk generator for creating
multi-person conversational videos. It includes examples for both single
and multi-person scenarios.

Usage:
    python multitalk_demo.py [--single] [--conversation] [--test]
    
Examples:
    python multitalk_demo.py --test              # Test connection only
    python multitalk_demo.py --single            # Single person video
    python multitalk_demo.py --conversation      # Multi-person conversation
"""

import os
import argparse
from typing import Optional
from replicate_multitalk_generator import ReplicateMultiTalkGenerator

def demo_single_person(generator: ReplicateMultiTalkGenerator, output_dir: str = "output"):
    """Demonstrate single person video generation"""
    print("\n🎭 Demo: Single Person Video Generation")
    print("=" * 50)
    
    # Example parameters (users should replace with actual files)
    image_url = "https://via.placeholder.com/512x512/DDDDDD/FFFFFF?text=Your+Photo+Here"
    audio_url = "https://via.placeholder.com/1x1/DDDDDD/FFFFFF?text=your_audio.mp3"
    
    print("📋 Parameters:")
    print(f"   • Image: {image_url}")
    print(f"   • Audio: {audio_url}")
    print(f"   • Prompt: A person speaking naturally")
    print(f"   • Frames: 81")
    print(f"   • Turbo: True")
    
    print("\n⚠️ Note: This demo uses placeholder URLs.")
    print("   Replace with actual image and audio file paths for real generation.")
    
    # Uncomment below to run actual generation
    # output_path = os.path.join(output_dir, "multitalk_single_demo.mp4")
    # result = generator.generate_single_person_video(
    #     image_url=image_url,
    #     audio_url=audio_url,
    #     prompt="A person speaking naturally with clear expressions",
    #     num_frames=81,
    #     turbo=True,
    #     output_path=output_path
    # )
    # print(f"✅ Video generated: {result['video']['url']}")
    # print(f"⏱️ Generation time: {result['generation_time']:.2f} seconds")

def demo_conversation(generator: ReplicateMultiTalkGenerator, output_dir: str = "output"):
    """Demonstrate multi-person conversation generation"""
    print("\n🗣️ Demo: Multi-Person Conversation Generation")
    print("=" * 50)
    
    # Example parameters (users should replace with actual files)
    image_url = "https://via.placeholder.com/512x512/DDDDDD/FFFFFF?text=Two+People+Photo"
    first_audio_url = "https://via.placeholder.com/1x1/DDDDDD/FFFFFF?text=person1_audio.mp3"
    second_audio_url = "https://via.placeholder.com/1x1/DDDDDD/FFFFFF?text=person2_audio.mp3"
    
    print("📋 Parameters:")
    print(f"   • Image: {image_url}")
    print(f"   • First audio: {first_audio_url}")
    print(f"   • Second audio: {second_audio_url}")
    print(f"   • Prompt: A smiling man and woman hosting a podcast")
    print(f"   • Frames: 120")
    print(f"   • Turbo: True")
    
    print("\n⚠️ Note: This demo uses placeholder URLs.")
    print("   Replace with actual image and audio file paths for real generation.")
    print("   The image should contain two people for best results.")
    
    # Uncomment below to run actual generation
    # output_path = os.path.join(output_dir, "multitalk_conversation_demo.mp4")
    # result = generator.generate_conversation_video(
    #     image_url=image_url,
    #     first_audio_url=first_audio_url,
    #     second_audio_url=second_audio_url,
    #     prompt="A smiling man and woman hosting a podcast",
    #     num_frames=120,
    #     turbo=True,
    #     output_path=output_path
    # )
    # print(f"✅ Video generated: {result['video']['url']}")
    # print(f"⏱️ Generation time: {result['generation_time']:.2f} seconds")

def demo_real_files_example(generator: ReplicateMultiTalkGenerator, output_dir: str = "output"):
    """Show example with real file paths (commented out)"""
    print("\n📁 Demo: Real Files Example (Template)")
    print("=" * 50)
    
    print("📝 To use with real files, replace the paths below:")
    print("""
# Example with real local files:
result = generator.generate_conversation_video(
    image_url="./input/my_photo.jpg",           # Local image file
    first_audio_url="./input/person1_speech.mp3",   # First person's audio
    second_audio_url="./input/person2_speech.mp3",  # Second person's audio
    prompt="Two friends having a casual conversation",
    num_frames=150,
    seed=42,
    turbo=True,
    output_path="./output/my_conversation.mp4"
)

# Example with remote URLs:
result = generator.generate_single_person_video(
    image_url="https://your-domain.com/images/portrait.jpg",
    audio_url="https://your-domain.com/audio/speech.mp3",
    prompt="A professional presenter giving a speech",
    num_frames=100,
    turbo=True,
    output_path="./output/presentation.mp4"
)
""")
    
    print("🎯 Tips for best results:")
    print("   • Use high-quality portrait images (512x512 or larger)")
    print("   • Ensure clear audio with minimal background noise")
    print("   • For conversations, use images with 2 clearly visible faces")
    print("   • Audio length affects generation time and cost")
    print("   • Start with shorter audio clips (10-30 seconds) for testing")

def show_model_capabilities(generator: ReplicateMultiTalkGenerator):
    """Display model capabilities and features"""
    print("\n📋 MultiTalk Model Capabilities")
    print("=" * 50)
    
    model_info = generator.get_model_info()
    
    print(f"🏷️ Model: {model_info['name']}")
    print(f"🏢 Provider: {model_info['provider']}")
    print(f"🆔 ID: {model_info['model_id']}")
    print(f"📝 Description: {model_info['description']}")
    
    print(f"\n✨ Features:")
    for feature in model_info['features']:
        print(f"   • {feature}")
    
    print(f"\n📥 Input Parameters:")
    for param, description in model_info['input_formats'].items():
        print(f"   • {param}: {description}")
    
    print(f"\n📤 Output: {model_info['output_format']}")
    print(f"💻 Hardware: {model_info['hardware']}")
    print(f"💰 Cost: {model_info['cost_estimate']}")
    
    print(f"\n🔗 Documentation: https://replicate.com/zsxkib/multitalk")

def main():
    """Main demo function"""
    parser = argparse.ArgumentParser(description="MultiTalk Demo")
    parser.add_argument("--single", action="store_true", help="Demo single person video")
    parser.add_argument("--conversation", action="store_true", help="Demo multi-person conversation")
    parser.add_argument("--test", action="store_true", help="Test connection only")
    parser.add_argument("--output-dir", default="output", help="Output directory for videos")
    
    args = parser.parse_args()
    
    # If no specific demo selected, run all
    if not any([args.single, args.conversation, args.test]):
        args.single = True
        args.conversation = True
        args.test = True
    
    print("🗣️ Replicate MultiTalk Demo")
    print("=" * 70)
    
    try:
        # Initialize generator
        print("🔧 Initializing MultiTalk generator...")
        generator = ReplicateMultiTalkGenerator()
        
        # Test connection if requested
        if args.test:
            print("\n🔍 Testing Connection")
            print("-" * 30)
            if generator.test_connection():
                print("✅ Connection successful!")
            else:
                print("❌ Connection failed. Please check your REPLICATE_API_TOKEN.")
                return
        
        # Show model capabilities
        show_model_capabilities(generator)
        
        # Create output directory
        os.makedirs(args.output_dir, exist_ok=True)
        
        # Run demos
        if args.single:
            demo_single_person(generator, args.output_dir)
        
        if args.conversation:
            demo_conversation(generator, args.output_dir)
        
        # Show real files example
        demo_real_files_example(generator, args.output_dir)
        
        print("\n🎉 Demo completed!")
        print(f"\n📁 Output directory: {args.output_dir}")
        print("💡 To run actual generation, replace placeholder URLs with real files.")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Make sure REPLICATE_API_TOKEN is set in your environment or .env file")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()