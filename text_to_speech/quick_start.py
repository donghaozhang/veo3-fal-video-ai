#!/usr/bin/env python3
"""
Quick Start Demo for OpenRouter + ElevenLabs Pipeline

This script demonstrates the complete pipeline with several examples.
No user interaction required - just run and watch!
"""

import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_setup():
    """Check if the system is properly configured"""
    
    print("🔧 Checking system setup...")
    
    # Check API keys
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not openrouter_key:
        print("❌ Missing OPENROUTER_API_KEY")
        print("   Get your key from: https://openrouter.ai/")
        print("   Set: export OPENROUTER_API_KEY='your_key'")
        return False
    
    if not elevenlabs_key:
        print("❌ Missing ELEVENLABS_API_KEY")
        print("   Get your key from: https://elevenlabs.io/")
        print("   Set: export ELEVENLABS_API_KEY='your_key'")
        return False
    
    # Check dependencies
    try:
        import requests
        from openrouter_tts_pipeline import OpenRouterTTSPipeline, OpenRouterModel
        print("✅ All dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        return False


def run_demo_examples():
    """Run demonstration examples of the pipeline"""
    
    if not check_setup():
        return
    
    # Get API keys
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    # Import pipeline
    from openrouter_tts_pipeline import OpenRouterTTSPipeline, OpenRouterModel
    
    # Initialize pipeline
    print("\n🚀 Initializing OpenRouter + ElevenLabs Pipeline")
    pipeline = OpenRouterTTSPipeline(openrouter_key, elevenlabs_key)
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Define demo scenarios
    demo_scenarios = [
        {
            "name": "Tech Startup Pitch",
            "description": "a young entrepreneur pitching a revolutionary AI app",
            "num_people": 1,
            "length_minutes": 1.0,
            "content_type": "presentation",
            "voice_style": "professional",
            "model": OpenRouterModel.CLAUDE_SONNET_4,
            "output_file": "tech_pitch_demo.mp3"
        },
        {
            "name": "Coffee Shop Debate",
            "description": "two friends arguing about whether pineapple belongs on pizza",
            "num_people": 2,
            "length_minutes": 1.2,
            "content_type": "conversation",
            "voice_style": "casual",
            "model": OpenRouterModel.DEEPSEEK_V3_FREE,  # Free model for demo
            "output_file": "pizza_debate_demo.mp3"
        },
        {
            "name": "Job Interview",
            "description": "a software engineer interviewing for a senior position",
            "num_people": 2,
            "length_minutes": 1.5,
            "content_type": "interview",
            "voice_style": "professional",
            "model": OpenRouterModel.GEMINI_2_FLASH,
            "output_file": "job_interview_demo.mp3"
        },
        {
            "name": "Ghost Story",
            "description": "a mysterious storyteller narrating a haunted house tale",
            "num_people": 1,
            "length_minutes": 2.0,
            "content_type": "story",
            "voice_style": "dramatic",
            "model": OpenRouterModel.GEMINI_25_FLASH,
            "output_file": "ghost_story_demo.mp3"
        }
    ]
    
    print(f"\n🎯 Running {len(demo_scenarios)} demo scenarios...")
    print("=" * 60)
    
    results = []
    total_start_time = time.time()
    
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"\n🎬 Demo {i}/{len(demo_scenarios)}: {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        print(f"   People: {scenario['num_people']}")
        print(f"   Length: {scenario['length_minutes']} minutes")
        print(f"   Model: {scenario['model'].value}")
        
        try:
            result = pipeline.run_complete_pipeline(
                description=scenario["description"],
                num_people=scenario["num_people"],
                length_minutes=scenario["length_minutes"],
                content_type=scenario["content_type"],
                voice_style=scenario["voice_style"],
                model=scenario["model"],
                output_file=scenario["output_file"]
            )
            
            if result["success"]:
                print(f"   ✅ Success! Generated: {result['output_file']}")
                print(f"   ⏱️ Time: {result['total_time']:.2f}s")
                results.append(result)
            else:
                print(f"   ❌ Failed to generate {scenario['name']}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Small delay between demos
        if i < len(demo_scenarios):
            print("   ⏳ Waiting 2 seconds before next demo...")
            time.sleep(2)
    
    total_time = time.time() - total_start_time
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print(f"⏱️ Total time: {total_time:.2f} seconds")
    print(f"✅ Successful generations: {len(results)}/{len(demo_scenarios)}")
    
    if results:
        print("\n🎵 Generated files:")
        for result in results:
            print(f"   📁 {result['output_file']}")
            print(f"      Duration: {result['generated_content'].estimated_duration:.2f} min")
        
        print("\n🎧 You can now play these audio files to hear the results!")
        print("💡 Try different descriptions and settings using interactive_pipeline.py")
    
    else:
        print("\n❌ No files were generated successfully")
        print("   Check your API keys and internet connection")


def show_pipeline_info():
    """Show information about the pipeline capabilities"""
    
    print("\n🎙️ OpenRouter + ElevenLabs Text-to-Speech Pipeline")
    print("=" * 60)
    print("Complete AI-to-Speech pipeline with 5 steps:")
    print()
    print("1️⃣ Input: Describe person(s) and desired length")
    print("2️⃣ Length Calculation: Estimate content requirements")
    print("3️⃣ LLM Generation: Create content using top AI models")
    print("4️⃣ Content Processing: Structure for text-to-speech")
    print("5️⃣ Speech Generation: Convert to audio with ElevenLabs")
    print()
    print("🤖 Supported AI Models (10 total):")
    print("   • Claude Sonnet 4 (Anthropic)")
    print("   • Gemini 2.0/2.5 Flash (Google)")
    print("   • DeepSeek V3 (Free & Paid)")
    print("   • And 6 more top models...")
    print()
    print("🎭 Content Types:")
    print("   • Conversation (natural dialogue)")
    print("   • Presentation (informative speech)")
    print("   • Interview (Q&A format)")
    print("   • Story (narrative content)")
    print()
    print("🎤 Voice Styles:")
    print("   • Professional (business, formal)")
    print("   • Casual (friendly, relaxed)")
    print("   • Dramatic (expressive, theatrical)")
    print()
    print("👥 Speaker Options:")
    print("   • Single speaker (monologue)")
    print("   • Two speakers (dialogue)")
    print()
    print("⏱️ Length: 0.5 - 10 minutes (recommended: 1-3 minutes)")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--info":
            show_pipeline_info()
        elif sys.argv[1] == "--check":
            check_setup()
        else:
            print("Usage:")
            print("  python quick_start.py       # Run demo")
            print("  python quick_start.py --info   # Show pipeline info")
            print("  python quick_start.py --check  # Check setup")
    else:
        show_pipeline_info()
        print("\n🚀 Starting demo in 3 seconds...")
        time.sleep(3)
        run_demo_examples() 