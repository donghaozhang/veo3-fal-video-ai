#!/usr/bin/env python3
"""
Real MultiTalk Example Test

This script demonstrates the MultiTalk model using the exact same parameters
from the official Replicate example, including real image and audio assets.

⚠️ WARNING: This script makes actual API calls and will cost money!
Cost estimate: $0.50-2.00 per generation

Usage:
    python test_real_multitalk_example.py [--dry-run]
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from replicate_multitalk_generator import ReplicateMultiTalkGenerator

def test_real_multitalk_example(dry_run=False):
    """Test MultiTalk with real example from Replicate documentation"""
    print("🎬 Real MultiTalk Example Test")
    print("=" * 50)
    
    if dry_run:
        print("🔍 DRY RUN MODE - No actual API calls will be made")
    else:
        print("⚠️ WARNING: This will make actual API calls and cost money!")
        print("💰 Estimated cost: $0.50-2.00")
        
        confirm = input("\nProceed with real generation? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ Test cancelled")
            return False
    
    try:
        # Initialize generator
        print("\n🔧 Initializing MultiTalk generator...")
        generator = ReplicateMultiTalkGenerator()
        
        # Test connection first
        print("\n🔍 Testing connection...")
        if not generator.test_connection():
            print("❌ Connection failed. Check your REPLICATE_API_TOKEN")
            return False
        
        # Real example parameters from Replicate documentation
        print("\n📋 Using real example parameters:")
        
        image_url = "https://replicate.delivery/pbxt/NHF6Y7EeJGK6pp4rDODjJS8m0nk9rj32iuaVQs8IfOl7S4vJ/multi1.png"
        first_audio_url = "https://replicate.delivery/pbxt/NHF6XifveoBBNUVcYdrkqkiLqq2vDI7g322dYXadTtF4BFZ9/1.WAV"
        second_audio_url = "https://replicate.delivery/pbxt/NHF6Y526MirDQ9byxeuIxcnrnW5CeISX11fWxr78FP9d3gut/2.WAV"
        prompt = ("In a casual, intimate setting, a man and a woman are engaged in a heartfelt conversation "
                 "inside a car. The man, sporting a denim jacket over a blue shirt, sits attentively with a "
                 "seatbelt fastened, his gaze fixed on the woman beside him. The woman, wearing a black tank "
                 "top and a denim jacket draped over her shoulders, smiles warmly, her eyes reflecting genuine "
                 "interest and connection. The car's interior, with its beige seats and simple design, provides "
                 "a backdrop that emphasizes their interaction. The scene captures a moment of shared understanding "
                 "and connection, set against the soft, diffused light of an overcast day. A medium shot from a "
                 "slightly angled perspective, focusing on their expressions and body language")
        
        print(f"   • Image: {image_url}")
        print(f"   • First audio: {first_audio_url}")
        print(f"   • Second audio: {second_audio_url}")
        print(f"   • Prompt: {prompt[:100]}...")
        print(f"   • Frames: 81")
        print(f"   • Turbo: True")
        print(f"   • Sampling steps: 10")
        
        if dry_run:
            print("\n✅ DRY RUN: Parameters validated, no API call made")
            print("💡 Remove --dry-run flag to run actual generation")
            return True
        
        # Generate the conversation video
        print(f"\n🚀 Starting MultiTalk generation...")
        output_path = "output/real_multitalk_example.mp4"
        
        result = generator.generate_conversation_video(
            image_url=image_url,
            first_audio_url=first_audio_url,
            second_audio_url=second_audio_url,
            prompt=prompt,
            num_frames=81,
            turbo=True,
            sampling_steps=10,
            output_path=output_path
        )
        
        print(f"\n✅ MultiTalk video generated successfully!")
        print(f"🔗 Video URL: {result['video']['url']}")
        print(f"⏱️ Generation time: {result['generation_time']:.2f} seconds")
        print(f"📁 Local file: {output_path}")
        
        # Show result details
        print(f"\n📊 Generation Details:")
        print(f"   • Model: {generator.model_version}")
        print(f"   • Parameters: {len(result['parameters'])} parameters used")
        print(f"   • Status: Success")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Real MultiTalk Example Test")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Validate parameters without making API calls")
    
    args = parser.parse_args()
    
    print("🗣️ Replicate MultiTalk - Real Example Test")
    print("=" * 70)
    
    if args.dry_run:
        print("🔍 Running in DRY RUN mode (no costs)")
    else:
        print("💰 WARNING: Real API calls - costs money!")
    
    print(f"\n📋 Test Details:")
    print(f"   • Model: zsxkib/multitalk")
    print(f"   • Version: 0bd2390c40618c910ffc345b36c8fd218fd8fa59c9124aa641fea443fa203b44")
    print(f"   • Assets: Real image and audio from Replicate delivery")
    print(f"   • Scene: Car conversation between man and woman")
    
    success = test_real_multitalk_example(dry_run=args.dry_run)
    
    if success:
        print(f"\n🎉 Test completed successfully!")
        if not args.dry_run:
            print(f"📁 Check output/real_multitalk_example.mp4 for the generated video")
    else:
        print(f"\n❌ Test failed")
    
    print(f"\n💡 Usage tips:")
    print(f"   • Use --dry-run for cost-free validation")
    print(f"   • Ensure REPLICATE_API_TOKEN is set in .env")
    print(f"   • Check your Replicate account for usage/billing")

if __name__ == "__main__":
    main()