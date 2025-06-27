#!/usr/bin/env python3
"""
Basic Usage Examples

Simple examples demonstrating core text-to-speech functionality.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import from refactored package
from text_to_speech.tts.controller import ElevenLabsTTSController
from text_to_speech.models.common import ElevenLabsModel, VoiceSettings, AudioFormat


def basic_text_to_speech_example():
    """Basic text-to-speech example"""
    print("=== Basic Text-to-Speech Example ===")
    
    # Get API key from environment
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Please set ELEVENLABS_API_KEY environment variable")
        return
    
    # Initialize TTS controller
    tts = ElevenLabsTTSController(api_key)
    
    # Simple text-to-speech
    text = "Hello! This is a basic text-to-speech example using the refactored package."
    voice_id = tts.get_popular_voice_id("rachel")
    
    if voice_id:
        success = tts.text_to_speech(
            text=text,
            voice_id=voice_id,
            output_file="output/basic_example.mp3"
        )
        
        if success:
            print("✓ Audio generated successfully: output/basic_example.mp3")
        else:
            print("✗ Failed to generate audio")
    else:
        print("✗ Voice 'rachel' not found")


def voice_comparison_example():
    """Compare different voices"""
    print("\n=== Voice Comparison Example ===")
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Please set ELEVENLABS_API_KEY environment variable")
        return
    
    tts = ElevenLabsTTSController(api_key)
    
    text = "This demonstrates different voice characteristics."
    voices = ["rachel", "drew", "bella", "antoni"]
    
    for voice in voices:
        voice_id = tts.get_popular_voice_id(voice)
        if voice_id:
            output_file = f"output/voice_{voice}.mp3"
            success = tts.text_to_speech(
                text=text,
                voice_id=voice_id,
                output_file=output_file
            )
            
            if success:
                print(f"✓ Generated with {voice}: {output_file}")
            else:
                print(f"✗ Failed to generate with {voice}")


def timing_control_example():
    """Timing and speed control example"""
    print("\n=== Timing Control Example ===")
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Please set ELEVENLABS_API_KEY environment variable")
        return
    
    tts = ElevenLabsTTSController(api_key)
    
    text = "This sentence has timing control. It includes natural pauses. Perfect for presentations!"
    
    # Generate with timing control
    success = tts.text_to_speech_with_timing_control(
        text=text,
        voice_name="rachel",
        speed=1.0,
        pause_duration=0.8,
        output_file="output/timing_example.mp3"
    )
    
    if success:
        print("✓ Audio with timing control generated: output/timing_example.mp3")
    else:
        print("✗ Failed to generate audio with timing control")


def voice_settings_example():
    """Custom voice settings example"""
    print("\n=== Voice Settings Example ===")
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Please set ELEVENLABS_API_KEY environment variable")
        return
    
    tts = ElevenLabsTTSController(api_key)
    
    text = "This demonstrates custom voice settings for different effects."
    voice_id = tts.get_popular_voice_id("bella")
    
    if not voice_id:
        print("✗ Voice 'bella' not found")
        return
    
    # Conservative settings (stable, consistent)
    conservative_settings = VoiceSettings(
        stability=0.9,
        similarity_boost=0.8,
        style=0.1,
        use_speaker_boost=True
    )
    
    # Creative settings (variable, expressive)
    creative_settings = VoiceSettings(
        stability=0.3,
        similarity_boost=0.6,
        style=0.8,
        use_speaker_boost=True
    )
    
    # Generate with different settings
    for name, settings in [("conservative", conservative_settings), ("creative", creative_settings)]:
        output_file = f"output/voice_settings_{name}.mp3"
        success = tts.text_to_speech(
            text=text,
            voice_id=voice_id,
            voice_settings=settings,
            output_file=output_file
        )
        
        if success:
            print(f"✓ Generated with {name} settings: {output_file}")
        else:
            print(f"✗ Failed to generate with {name} settings")


def main():
    """Run all examples"""
    print("Running Basic Usage Examples")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Run examples
    basic_text_to_speech_example()
    voice_comparison_example()
    timing_control_example()
    voice_settings_example()
    
    print("\n" + "=" * 50)
    print("Examples completed! Check the output/ directory for generated audio files.")


if __name__ == "__main__":
    main()