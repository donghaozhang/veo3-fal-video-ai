#!/usr/bin/env python3
"""
Interactive OpenRouter + ElevenLabs Pipeline
User-friendly interface for generating speech from descriptions
"""

import os
import sys
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from ..pipeline.core import OpenRouterTTSPipeline
    from ..models.pipeline import OpenRouterModel
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False
    print("❌ Pipeline not available. Ensure all dependencies are installed.")


def get_user_input() -> dict:
    """Get user input for the pipeline"""
    
    print("\n🎙️ OpenRouter + ElevenLabs Text-to-Speech Pipeline")
    print("=" * 60)
    print("Generate speech from your descriptions using AI models!")
    
    # Get description
    print("\n📝 Step 1: Describe the person(s)")
    print("Examples:")
    print("  - 'a tech entrepreneur explaining startup strategies'")
    print("  - 'two friends discussing their favorite movies'")
    print("  - 'a teacher explaining quantum physics'")
    description = input("\nEnter description: ").strip()
    
    if not description:
        print("❌ Description cannot be empty")
        return None
    
    # Get number of people
    print("\n👥 Step 2: Number of speakers")
    print("1 = Single speaker (monologue/presentation)")
    print("2 = Two speakers (dialogue/conversation)")
    
    while True:
        try:
            num_people = int(input("\nNumber of people (1 or 2): "))
            if num_people in [1, 2]:
                break
            else:
                print("Please enter 1 or 2")
        except ValueError:
            print("Please enter a valid number")
    
    # Get length
    print("\n⏱️ Step 3: Audio length")
    print("Recommended: 0.5-3.0 minutes for best quality")
    
    while True:
        try:
            length = float(input("\nLength in minutes: "))
            if 0.1 <= length <= 10.0:
                break
            else:
                print("Please enter a length between 0.1 and 10.0 minutes")
        except ValueError:
            print("Please enter a valid number")
    
    # Get content type
    print("\n🎭 Step 4: Content type")
    content_types = {
        "1": "conversation",
        "2": "presentation", 
        "3": "interview",
        "4": "story"
    }
    
    print("1. Conversation (natural dialogue)")
    print("2. Presentation (informative speech)")
    print("3. Interview (Q&A format)")
    print("4. Story (narrative content)")
    
    while True:
        choice = input("\nSelect content type (1-4): ").strip()
        if choice in content_types:
            content_type = content_types[choice]
            break
        else:
            print("Please enter 1, 2, 3, or 4")
    
    # Get voice style
    print("\n🎤 Step 5: Voice style")
    voice_styles = {
        "1": "professional",
        "2": "casual",
        "3": "dramatic"
    }
    
    print("1. Professional (business, formal)")
    print("2. Casual (friendly, relaxed)")
    print("3. Dramatic (expressive, theatrical)")
    
    while True:
        choice = input("\nSelect voice style (1-3): ").strip()
        if choice in voice_styles:
            voice_style = voice_styles[choice]
            break
        else:
            print("Please enter 1, 2, or 3")
    
    # Get AI model
    print("\n🤖 Step 6: AI Model")
    models = {
        "1": ("Claude Sonnet 4", OpenRouterModel.CLAUDE_SONNET_4),
        "2": ("Gemini 2.0 Flash", OpenRouterModel.GEMINI_2_FLASH),
        "3": ("Gemini 2.5 Flash Preview", OpenRouterModel.GEMINI_25_FLASH_PREVIEW),
        "4": ("DeepSeek V3 (Free)", OpenRouterModel.DEEPSEEK_V3_FREE),
        "5": ("Gemini 2.5 Flash", OpenRouterModel.GEMINI_25_FLASH),
        "6": ("Claude 3.7 Sonnet", OpenRouterModel.CLAUDE_37_SONNET),
        "7": ("Gemini 2.5 Pro", OpenRouterModel.GEMINI_25_PRO),
        "8": ("DeepSeek V3", OpenRouterModel.DEEPSEEK_V3),
        "9": ("Gemini 2.0 Flash Lite", OpenRouterModel.GEMINI_2_FLASH_LITE),
        "10": ("Gemini 2.5 Flash Lite", OpenRouterModel.GEMINI_25_FLASH_LITE)
    }
    
    print("Top 10 AI Models:")
    for key, (name, _) in models.items():
        print(f"{key:2}. {name}")
    
    while True:
        choice = input("\nSelect AI model (1-10): ").strip()
        if choice in models:
            model_name, model_enum = models[choice]
            break
        else:
            print("Please enter a number between 1-10")
    
    return {
        "description": description,
        "num_people": num_people,
        "length_minutes": length,
        "content_type": content_type,
        "voice_style": voice_style,
        "model": model_enum,
        "model_name": model_name
    }


def check_api_keys() -> tuple:
    """Check if required API keys are available"""
    
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not openrouter_key:
        print("\n❌ Missing OpenRouter API Key")
        print("1. Get your API key from: https://openrouter.ai/")
        print("2. Set environment variable: export OPENROUTER_API_KEY='your_key'")
        print("3. Or add to .env file: OPENROUTER_API_KEY=your_key")
        return False, None, None
    
    if not elevenlabs_key:
        print("\n❌ Missing ElevenLabs API Key")
        print("1. Get your API key from: https://elevenlabs.io/")
        print("2. Set environment variable: export ELEVENLABS_API_KEY='your_key'")
        print("3. Or add to .env file: ELEVENLABS_API_KEY=your_key")
        return False, None, None
    
    return True, openrouter_key, elevenlabs_key


def show_examples():
    """Show example inputs"""
    
    print("\n💡 Example Inputs:")
    print("=" * 40)
    
    examples = [
        {
            "description": "a fitness coach motivating people to exercise",
            "people": 1,
            "length": 1.5,
            "type": "presentation",
            "style": "professional"
        },
        {
            "description": "two coffee shop customers debating their favorite drinks",
            "people": 2,
            "length": 2.0,
            "type": "conversation",
            "style": "casual"
        },
        {
            "description": "a mystery novelist telling a scary story",
            "people": 1,
            "length": 3.0,
            "type": "story",
            "style": "dramatic"
        },
        {
            "description": "a job candidate and interviewer discussing work experience",
            "people": 2,
            "length": 2.5,
            "type": "interview",
            "style": "professional"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(f"  Description: {example['description']}")
        print(f"  People: {example['people']}")
        print(f"  Length: {example['length']} minutes")
        print(f"  Type: {example['type']}")
        print(f"  Style: {example['style']}")


def main():
    """Main interactive function"""
    
    if not PIPELINE_AVAILABLE:
        print("❌ Pipeline dependencies not available")
        print("Run: pip install -r requirements.txt")
        return
    
    print("🚀 Welcome to the AI Speech Generation Pipeline!")
    
    # Show examples
    show_examples()
    
    # Check API keys
    keys_valid, openrouter_key, elevenlabs_key = check_api_keys()
    if not keys_valid:
        return
    
    # Get user input
    user_input = get_user_input()
    if not user_input:
        return
    
    # Initialize pipeline
    print("\n🔧 Initializing pipeline...")
    try:
        pipeline = OpenRouterTTSPipeline(openrouter_key, elevenlabs_key)
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        return
    
    # Generate output filename
    safe_description = "".join(c for c in user_input["description"][:30] if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_description = safe_description.replace(' ', '_')
    output_file = f"{safe_description}_{user_input['num_people']}person_{user_input['length_minutes']}min.mp3"
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Show configuration
    print("\n📋 Configuration Summary:")
    print("=" * 40)
    print(f"Description: {user_input['description']}")
    print(f"People: {user_input['num_people']}")
    print(f"Length: {user_input['length_minutes']} minutes")
    print(f"Content Type: {user_input['content_type']}")
    print(f"Voice Style: {user_input['voice_style']}")
    print(f"AI Model: {user_input['model_name']}")
    print(f"Output File: {output_file}")
    
    # Confirm before proceeding
    print("\n⚠️ This will use API credits from both OpenRouter and ElevenLabs")
    confirm = input("Proceed? (y/N): ").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print("❌ Cancelled by user")
        return
    
    # Run pipeline
    try:
        results = pipeline.run_complete_pipeline(
            description=user_input["description"],
            num_people=user_input["num_people"],
            length_minutes=user_input["length_minutes"],
            content_type=user_input["content_type"],
            voice_style=user_input["voice_style"],
            model=user_input["model"],
            output_file=output_file
        )
        
        if results["success"]:
            print("\n🎉 Success! Your audio has been generated.")
            print(f"📁 File: {results['output_file']}")
            print(f"⏱️ Generation time: {results['total_time']:.2f} seconds")
            print(f"📊 Estimated duration: {results['generated_content'].estimated_duration:.2f} minutes")
            
            # Show generated content preview
            print("\n📝 Generated Content Preview:")
            print("-" * 40)
            content = results['generated_content'].processed_content
            for i, segment in enumerate(content[:3]):  # Show first 3 segments
                speaker = segment.get('speaker', 'Speaker')
                emotion = f"[{segment['emotion']}] " if segment.get('emotion') else ""
                text = segment['text'][:100] + "..." if len(segment['text']) > 100 else segment['text']
                print(f"{speaker}: {emotion}{text}")
            
            if len(content) > 3:
                print(f"... and {len(content) - 3} more segments")
            
        else:
            print("\n❌ Generation failed. Check your API keys and try again.")
            
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
        print("Check your API keys and internet connection.")


def quick_demo():
    """Run a quick demo with predefined inputs"""
    
    # Check API keys
    keys_valid, openrouter_key, elevenlabs_key = check_api_keys()
    if not keys_valid:
        return
    
    print("\n🚀 Running Quick Demo...")
    print("Generating a 30-second conversation between two friends about coffee")
    
    try:
        pipeline = OpenRouterTTSPipeline(openrouter_key, elevenlabs_key)
        
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)
        
        results = pipeline.run_complete_pipeline(
            description="two friends comparing their favorite coffee drinks",
            num_people=2,
            length_minutes=0.5,
            content_type="conversation",
            voice_style="casual",
            model=OpenRouterModel.DEEPSEEK_V3_FREE,  # Use free model for demo
            output_file="coffee_demo.mp3"
        )
        
        if results["success"]:
            print("\n🎉 Demo completed successfully!")
            print(f"📁 Generated: {results['output_file']}")
        else:
            print("\n❌ Demo failed")
            
    except Exception as e:
        print(f"\n❌ Demo error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        quick_demo()
    else:
        main() 