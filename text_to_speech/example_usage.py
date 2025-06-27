#!/usr/bin/env python3
"""
Simple usage examples for ElevenLabs TTS Controller
Run this script to test different voice and timing configurations
"""

import os
from elevenlabs_tts_controller import ElevenLabsTTSController, ElevenLabsModel, VoiceSettings

def main():
    """Main example function"""
    
    # Set up API key (get from https://elevenlabs.io/app/speech-synthesis/text-to-speech)
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        print("Please set your ELEVENLABS_API_KEY environment variable")
        print("Get your API key from: https://elevenlabs.io/app/speech-synthesis/text-to-speech")
        return
    
    # Initialize the TTS controller
    tts = ElevenLabsTTSController(api_key)
    
    print("ElevenLabs TTS Controller - Voice and Timing Examples")
    print("=" * 60)
    
    # Example 1: Different voices with same text
    example_1_different_voices()
    
    # Example 2: Same voice with different speeds
    example_2_speed_control()
    
    # Example 3: Voice settings comparison
    example_3_voice_settings()
    
    # Example 4: Multi-speaker dialogue
    example_4_multi_speaker()
    
    # Example 5: Model comparison
    example_5_model_comparison()

def example_1_different_voices():
    """Example 1: Different voices saying the same text"""
    print("\n1. Different Voices Example")
    print("-" * 30)
    
    text = "Hello! This is a demonstration of different voices available in ElevenLabs."
    
    # List of popular voices to try
    voices_to_try = ["rachel", "drew", "bella", "antoni", "elli"]
    
    tts = ElevenLabsTTSController(os.getenv("ELEVENLABS_API_KEY"))
    
    for voice_name in voices_to_try:
        print(f"Generating with voice: {voice_name}")
        
        success = tts.text_to_speech_with_timing_control(
            text=text,
            voice_name=voice_name,
            speed=1.0,
            output_file=f"voice_example_{voice_name}.mp3"
        )
        
        if success:
            print(f"✓ Generated: voice_example_{voice_name}.mp3")
        else:
            print(f"✗ Failed to generate audio for {voice_name}")

def example_2_speed_control():
    """Example 2: Same voice with different speeds"""
    print("\n2. Speed Control Example")
    print("-" * 30)
    
    text = "This sentence will be spoken at different speeds to demonstrate timing control capabilities."
    
    # Test different speeds
    speeds = [0.7, 1.0, 1.2]
    speed_names = ["slow", "normal", "fast"]
    
    tts = ElevenLabsTTSController(os.getenv("ELEVENLABS_API_KEY"))
    
    for speed, name in zip(speeds, speed_names):
        print(f"Generating at {name} speed ({speed}x)")
        
        success = tts.text_to_speech_with_timing_control(
            text=text,
            voice_name="rachel",
            speed=speed,
            pause_duration=0.5,
            output_file=f"speed_example_{name}.mp3"
        )
        
        if success:
            print(f"✓ Generated: speed_example_{name}.mp3")

def example_3_voice_settings():
    """Example 3: Voice settings comparison"""
    print("\n3. Voice Settings Example")
    print("-" * 30)
    
    text = "Voice settings can dramatically change how the same voice sounds and behaves."
    
    tts = ElevenLabsTTSController(os.getenv("ELEVENLABS_API_KEY"))
    voice_id = tts.get_popular_voice_id("bella")
    
    # Conservative settings (stable, consistent)
    conservative_settings = VoiceSettings(
        stability=0.9,
        similarity_boost=0.8,
        style=0.1,
        use_speaker_boost=True
    )
    
    print("Generating with conservative settings (stable, consistent)")
    success = tts.text_to_speech(
        text=text,
        voice_id=voice_id,
        voice_settings=conservative_settings,
        speed=1.0,
        output_file="settings_conservative.mp3"
    )
    
    if success:
        print("✓ Generated: settings_conservative.mp3")
    
    # Creative settings (variable, expressive)
    creative_settings = VoiceSettings(
        stability=0.3,
        similarity_boost=0.6,
        style=0.8,
        use_speaker_boost=True
    )
    
    print("Generating with creative settings (variable, expressive)")
    success = tts.text_to_speech(
        text=text,
        voice_id=voice_id,
        voice_settings=creative_settings,
        speed=1.0,
        output_file="settings_creative.mp3"
    )
    
    if success:
        print("✓ Generated: settings_creative.mp3")

def example_4_multi_speaker():
    """Example 4: Multi-speaker dialogue"""
    print("\n4. Multi-Speaker Dialogue Example")
    print("-" * 30)
    
    # Create a conversation script
    dialogue = [
        {"speaker": "rachel", "text": "Good morning! How can I help you today?"},
        {"speaker": "drew", "text": "Hi there! I'm looking for information about your services."},
        {"speaker": "rachel", "text": "Of course! We offer text-to-speech solutions with multiple voice options."},
        {"speaker": "drew", "text": "That sounds perfect! Can you show me some examples?"},
        {"speaker": "rachel", "text": "Absolutely! Let me demonstrate different voices and timing controls."}
    ]
    
    tts = ElevenLabsTTSController(os.getenv("ELEVENLABS_API_KEY"))
    
    print("Generating multi-speaker conversation...")
    success = tts.multi_voice_generation(
        script=dialogue,
        output_file="multi_speaker_dialogue.wav",
        model=ElevenLabsModel.MULTILINGUAL_V2
    )
    
    if success:
        print("✓ Generated: multi_speaker_dialogue.wav")

def example_5_model_comparison():
    """Example 5: Different models comparison"""
    print("\n5. Model Comparison Example")
    print("-" * 30)
    
    text = "This text will be generated using different ElevenLabs models to showcase their unique characteristics."
    
    tts = ElevenLabsTTSController(os.getenv("ELEVENLABS_API_KEY"))
    voice_id = tts.get_popular_voice_id("antoni")
    
    # Test different models
    models_to_test = [
        (ElevenLabsModel.MULTILINGUAL_V2, "multilingual_v2", "Highest quality, most stable"),
        (ElevenLabsModel.FLASH_V2_5, "flash_v2_5", "Ultra-low latency, fast"),
        (ElevenLabsModel.TURBO_V2_5, "turbo_v2_5", "Balanced quality and speed")
    ]
    
    for model, filename, description in models_to_test:
        print(f"Generating with {model.value} ({description})")
        
        success = tts.text_to_speech(
            text=text,
            voice_id=voice_id,
            model=model,
            speed=1.0,
            output_file=f"model_{filename}.mp3"
        )
        
        if success:
            print(f"✓ Generated: model_{filename}.mp3")

def setup_environment():
    """Help users set up their environment"""
    print("\nEnvironment Setup:")
    print("=" * 20)
    print("1. Get your API key from: https://elevenlabs.io/app/speech-synthesis/text-to-speech")
    print("2. Set environment variable:")
    print("   export ELEVENLABS_API_KEY='your_api_key_here'")
    print("3. Install requirements:")
    print("   pip install -r requirements.txt")
    print("4. Run this script:")
    print("   python example_usage.py")

if __name__ == "__main__":
    if not os.getenv("ELEVENLABS_API_KEY"):
        setup_environment()
    else:
        main()
        print("\n" + "=" * 60)
        print("Examples completed! Check the generated audio files.")
        print("Compare the different voices, speeds, settings, and models.")
        print("=" * 60) 