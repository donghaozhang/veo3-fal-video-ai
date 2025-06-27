#!/usr/bin/env python3
"""
ElevenLabs Text-to-Dialogue Script
Simple script for generating dialogue from text using ElevenLabs API
Based on: https://elevenlabs.io/docs/cookbooks/text-to-dialogue
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play, save
    ELEVENLABS_SDK_AVAILABLE = True
except ImportError:
    ELEVENLABS_SDK_AVAILABLE = False
    print("ElevenLabs SDK not installed. Install with: pip install elevenlabs")
    exit(1)


def create_dialogue_example():
    """Create a simple dialogue example as shown in the official documentation"""
    
    # Get API key
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY environment variable not set")
        print("Get your API key from: https://elevenlabs.io/app/speech-synthesis/text-to-speech")
        return False
    
    # Initialize ElevenLabs client
    client = ElevenLabs(api_key=api_key)
    
    try:
        print("🎭 Generating dialogue with ElevenLabs Text-to-Dialogue API...")
        
        # Generate dialogue using the exact example from documentation
        audio = client.text_to_dialogue.convert(
            # Text to Dialogue defaults to using the evergreen model "eleven_v3",
            # but you can use a preview version to try out
            # the latest features by providing the model ID
            # model_id="eleven_v3_preview_2025_06_03"
            inputs=[
                {
                    "text": "[cheerfully] Hello, how are you?",
                    "voice_id": "9BWtsMINqrJLrRacOk9x",  # Aria (female)
                },
                {
                    "text": "[stuttering] I'm... I'm doing well, thank you",
                    "voice_id": "IKne3meq5aSn9XLyUdCD",  # Paul (male)
                }
            ]
        )
        
        # Save the dialogue
        output_file = "dialogue_example.mp3"
        save(audio, output_file)
        print(f"✅ Dialogue saved to: {output_file}")
        
        # Play the dialogue
        print("🔊 Playing dialogue...")
        play(audio)
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating dialogue: {e}")
        print("\nNote: Eleven v3 API access is currently limited.")
        print("Contact ElevenLabs sales team for access: https://elevenlabs.io/contact")
        return False


def create_custom_dialogue():
    """Create a custom dialogue with multiple speakers and emotions"""
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY environment variable not set")
        return False
    
    client = ElevenLabs(api_key=api_key)
    
    try:
        print("🎭 Generating custom dialogue...")
        
        # Custom dialogue with multiple emotions and speakers
        audio = client.text_to_dialogue.convert(
            inputs=[
                {
                    "text": "[excitedly] Welcome to our new AI dialogue system!",
                    "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel (female)
                },
                {
                    "text": "[curiously] How does it work exactly?",
                    "voice_id": "29vD33N1CtxCmqQRPOHJ",  # Drew (male)
                },
                {
                    "text": "[cheerfully] It uses advanced AI to generate natural conversations with emotional context!",
                    "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel (female)
                },
                {
                    "text": "[amazed] That's incredible! The possibilities are endless.",
                    "voice_id": "29vD33N1CtxCmqQRPOHJ",  # Drew (male)
                },
                {
                    "text": "[mischievously] And we're just getting started!",
                    "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel (female)
                }
            ]
        )
        
        # Save the custom dialogue
        output_file = "custom_dialogue.mp3"
        save(audio, output_file)
        print(f"✅ Custom dialogue saved to: {output_file}")
        
        # Play the dialogue
        print("🔊 Playing custom dialogue...")
        play(audio)
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating custom dialogue: {e}")
        return False


def create_conversation_dialogue():
    """Create a longer conversation dialogue"""
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY environment variable not set")
        return False
    
    client = ElevenLabs(api_key=api_key)
    
    try:
        print("🎭 Generating conversation dialogue...")
        
        # Longer conversation with multiple speakers
        audio = client.text_to_dialogue.convert(
            inputs=[
                {
                    "text": "[cheerfully] Good morning! How can I help you today?",
                    "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella (female, customer service)
                },
                {
                    "text": "[politely] Hi there! I'm interested in learning about text-to-speech technology.",
                    "voice_id": "ErXwobaYiN019PkySvjV",  # Antoni (male, customer)
                },
                {
                    "text": "[enthusiastically] Great choice! Our latest technology can generate incredibly natural-sounding speech.",
                    "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella
                },
                {
                    "text": "[curiously] Can it handle different emotions and speaking styles?",
                    "voice_id": "ErXwobaYiN019PkySvjV",  # Antoni
                },
                {
                    "text": "[confidently] Absolutely! We support emotional tags like cheerful, sad, excited, and many more.",
                    "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella
                },
                {
                    "text": "[impressed] That's amazing! Can you show me an example?",
                    "voice_id": "ErXwobaYiN019PkySvjV",  # Antoni
                },
                {
                    "text": "[playfully] Well, you're listening to one right now!",
                    "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella
                },
                {
                    "text": "[laughing] Ha! That's brilliant. I'm definitely interested.",
                    "voice_id": "ErXwobaYiN019PkySvjV",  # Antoni
                }
            ]
        )
        
        # Save the conversation
        output_file = "conversation_dialogue.mp3"
        save(audio, output_file)
        print(f"✅ Conversation dialogue saved to: {output_file}")
        
        # Play the dialogue
        print("🔊 Playing conversation dialogue...")
        play(audio)
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating conversation dialogue: {e}")
        return False


def list_emotional_tags():
    """List available emotional tags for dialogue"""
    
    print("\n🎭 Available Emotional Tags for Dialogue:")
    print("=" * 50)
    
    emotional_tags = {
        "Positive Emotions": [
            "[cheerfully]", "[excitedly]", "[happily]", "[joyfully]", 
            "[enthusiastically]", "[playfully]", "[confidently]"
        ],
        "Negative Emotions": [
            "[sadly]", "[angrily]", "[frustrated]", "[disappointed]", 
            "[worried]", "[nervously]"
        ],
        "Neutral/Descriptive": [
            "[calmly]", "[quietly]", "[loudly]", "[slowly]", "[quickly]",
            "[politely]", "[curiously]", "[seriously]"
        ],
        "Special Delivery": [
            "[whispering]", "[shouting]", "[stuttering]", "[sarcastically]",
            "[mischievously]", "[amazed]", "[impressed]", "[laughing]"
        ]
    }
    
    for category, tags in emotional_tags.items():
        print(f"\n{category}:")
        for tag in tags:
            print(f"  {tag}")
    
    print("\nUsage: Add emotional tags at the beginning of your text")
    print("Example: '[cheerfully] Hello, how are you today?'")


def list_popular_voices():
    """List popular voice IDs for dialogue"""
    
    print("\n🎤 Popular Voice IDs for Dialogue:")
    print("=" * 50)
    
    voices = {
        "Female Voices": [
            ("Rachel", "21m00Tcm4TlvDq8ikWAM", "Professional, clear"),
            ("Bella", "EXAVITQu4vr4xnSDxMaL", "Friendly, customer service"),
            ("Elli", "MF3mGyEYCl7XYWbV9V6O", "Young, energetic"),
            ("Aria", "9BWtsMINqrJLrRacOk9x", "Expressive, dramatic")
        ],
        "Male Voices": [
            ("Drew", "29vD33N1CtxCmqQRPOHJ", "Warm, professional"),
            ("Antoni", "ErXwobaYiN019PkySvjV", "Casual, friendly"),
            ("Josh", "TxGEqnHWrfWFTfGW9XjX", "Conversational, natural"),
            ("Paul", "IKne3meq5aSn9XLyUdCD", "Mature, authoritative")
        ]
    }
    
    for category, voice_list in voices.items():
        print(f"\n{category}:")
        for name, voice_id, description in voice_list:
            print(f"  {name}: {voice_id} ({description})")
    
    print("\nUsage: Use voice_id in your dialogue inputs")
    print("Example: {'text': '[cheerfully] Hello!', 'voice_id': '21m00Tcm4TlvDq8ikWAM'}")


def main():
    """Main function to run dialogue examples"""
    
    print("ElevenLabs Text-to-Dialogue Script")
    print("=" * 40)
    print("Based on: https://elevenlabs.io/docs/cookbooks/text-to-dialogue")
    
    if not ELEVENLABS_SDK_AVAILABLE:
        print("\n❌ ElevenLabs SDK not available")
        print("Install with: pip install elevenlabs")
        return
    
    # Check for API key
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("\n❌ ELEVENLABS_API_KEY environment variable not set")
        print("1. Get your API key from: https://elevenlabs.io/app/speech-synthesis/text-to-speech")
        print("2. Set environment variable: export ELEVENLABS_API_KEY='your_api_key_here'")
        print("3. Or create a .env file with: ELEVENLABS_API_KEY=your_api_key_here")
        return
    
    # Show available options
    list_emotional_tags()
    list_popular_voices()
    
    # Run examples
    print("\n" + "=" * 50)
    print("Running Dialogue Examples")
    print("=" * 50)
    
    # Example 1: Official documentation example
    print("\n1. Official Documentation Example:")
    create_dialogue_example()
    
    # Example 2: Custom dialogue
    print("\n2. Custom Dialogue Example:")
    create_custom_dialogue()
    
    # Example 3: Conversation dialogue
    print("\n3. Conversation Dialogue Example:")
    create_conversation_dialogue()
    
    print("\n" + "=" * 50)
    print("✅ All examples completed!")
    print("Generated files:")
    print("- dialogue_example.mp3")
    print("- custom_dialogue.mp3")
    print("- conversation_dialogue.mp3")
    print("=" * 50)
    
    print("\n📝 Note: Eleven v3 API access is currently limited.")
    print("If you encounter access errors, contact ElevenLabs sales team:")
    print("https://elevenlabs.io/contact")


if __name__ == "__main__":
    main() 