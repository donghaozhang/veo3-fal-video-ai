#!/usr/bin/env python3
"""Test script for running multiple TTS generations with different voices."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_content_pipeline.models.text_to_speech import UnifiedTextToSpeechGenerator

def test_multi_voice_tts():
    """Test TTS with multiple voices."""
    # Initialize generator
    generator = UnifiedTextToSpeechGenerator()
    
    # Main text
    main_text = "Welcome to our advanced AI content creation platform. This demonstration showcases our integrated text-to-speech capabilities with multiple voice options and customizable parameters for professional audio production."
    
    # Test configurations
    tests = [
        {
            "voice": "rachel",
            "text": main_text,
            "speed": 1.0,
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.2,
            "output_file": "output/multi_voice_rachel.mp3"
        },
        {
            "voice": "drew", 
            "text": "This is Drew speaking with professional settings optimized for business presentations and corporate communications.",
            "speed": 1.1,
            "stability": 0.7,
            "similarity_boost": 0.9,
            "style": 0.1,
            "output_file": "output/multi_voice_drew.mp3"
        },
        {
            "voice": "bella",
            "text": "Hello! This is Bella with a creative and expressive voice style perfect for storytelling and engaging content creation.",
            "speed": 0.9,
            "stability": 0.3,
            "similarity_boost": 0.6,
            "style": 0.8,
            "output_file": "output/multi_voice_bella.mp3"
        }
    ]
    
    # Run tests
    for i, test in enumerate(tests, 1):
        print(f"\n🎤 Test {i}: Voice '{test['voice']}'")
        print(f"📝 Text: {test['text'][:100]}...")
        
        success, result = generator.generate(
            prompt=test["text"],
            voice=test["voice"],
            speed=test["speed"],
            stability=test["stability"],
            similarity_boost=test["similarity_boost"],
            style=test["style"],
            output_file=test["output_file"]
        )
        
        if success:
            print(f"✅ Success! Audio saved to: {result.get('output_file', 'unknown')}")
            print(f"📊 Processing time: {result.get('processing_time', 'N/A')}s")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n✨ All tests completed!")

if __name__ == "__main__":
    test_multi_voice_tts()