#!/usr/bin/env python3
"""
Test script to verify .env configuration and API key setup.
"""

import os
from pathlib import Path

def test_env_setup():
    """Test environment variable loading."""
    print("🔧 Video Tools Environment Setup Test")
    print("=" * 50)
    
    # Check for .env file
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        print("✅ .env file found")
        
        # Try to load dotenv if available
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print("✅ python-dotenv loaded successfully")
        except ImportError:
            print("⚠️  python-dotenv not installed (optional)")
            print("   You can install it with: pip install python-dotenv")
    else:
        print("❌ .env file not found")
        print("   Create one by copying .env.example: cp .env.example .env")
        return False
    
    # Check API keys
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print(f"✅ GEMINI_API_KEY found: {gemini_key[:10]}...{gemini_key[-4:]}")
        if len(gemini_key) == 39 and gemini_key.startswith('AIzaSy'):
            print("✅ GEMINI_API_KEY format looks correct")
        else:
            print("⚠️  GEMINI_API_KEY format may be incorrect")
    else:
        print("❌ GEMINI_API_KEY not found in environment")
        return False
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print(f"✅ OPENAI_API_KEY found: {openai_key[:8]}...{openai_key[-4:]}")
    else:
        print("ℹ️  OPENAI_API_KEY not set (optional for Whisper API)")
    
    # Test Gemini package availability
    try:
        import google.generativeai as genai
        print("✅ google-generativeai package installed")
        
        # Try to configure with API key
        try:
            genai.configure(api_key=gemini_key)
            print("✅ Gemini API key configured successfully")
        except Exception as e:
            print(f"⚠️  Gemini API configuration issue: {e}")
            
    except ImportError:
        print("❌ google-generativeai package not installed")
        print("   Install with: pip install google-generativeai")
        return False
    
    print("\n🎉 Environment setup complete!")
    print("📖 You can now use AI analysis features in video_audio_utils.py")
    return True

if __name__ == "__main__":
    test_env_setup()