#!/usr/bin/env python3
"""
FAL AI Text-to-Image Setup Test

This script tests ONLY the setup and environment configuration.
NO IMAGE GENERATION - COMPLETELY FREE!

Usage:
    python test_setup_new.py

Author: AI Assistant
Date: 2024
"""

import os
import sys

# Add parent directory to path to import the generator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fal_text_to_image_generator import FALTextToImageGenerator

def print_banner():
    """Print the test banner."""
    print("=" * 60)
    print("🔧 FAL AI TEXT-TO-IMAGE SETUP TEST")
    print("=" * 60)
    print("✅ This test is COMPLETELY FREE")
    print("✅ No image generation - only setup validation")
    print("✅ Safe to run anytime for troubleshooting")
    print("=" * 60)

def test_environment_setup() -> bool:
    """Test environment setup and API key validation (FREE)."""
    print("\n🔍 Testing Environment Setup...")
    
    try:
        # Check if .env file exists
        env_file = ".env"
        if os.path.exists(env_file):
            print(f"✅ Found {env_file}")
        else:
            print(f"⚠️  No {env_file} file found")
            print("💡 Create a .env file with your FAL_KEY")
        
        # Try to initialize generator
        generator = FALTextToImageGenerator()
        print("✅ FAL AI Text-to-Image Generator initialized successfully")
        
        # Test API key presence
        if generator.api_key:
            print("✅ FAL_KEY found in environment")
            # Mask the key for security
            masked_key = f"{generator.api_key[:8]}...{generator.api_key[-4:]}"
            print(f"🔑 API Key: {masked_key}")
        else:
            print("❌ FAL_KEY not found in environment")
            return False
        
        # Test model information
        model_info = generator.get_model_info()
        print(f"✅ Found {len(model_info)} supported models:")
        for model_name, info in model_info.items():
            print(f"   • {info.get('name', model_name)}")
        
        print("✅ Generator setup completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print_banner()
    
    success = test_environment_setup()
    
    print("\n" + "=" * 60)
    print("📊 SETUP TEST RESULTS")
    print("-" * 25)
    
    if success:
        print("✅ Setup test: PASSED")
        print("🎉 Environment is correctly configured!")
        print("\n💡 Next steps:")
        print("   • Run individual model tests (cost applies)")
        print("   • Try: python test_imagen4.py")
        print("   • Try: python test_flux_schnell.py")
    else:
        print("❌ Setup test: FAILED")
        print("🔧 Please check:")
        print("   • FAL_KEY is set in .env file")
        print("   • Virtual environment is activated")
        print("   • Dependencies are installed")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()