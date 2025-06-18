#!/usr/bin/env python3
"""
Test script to verify FAL AI setup without making actual API calls
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import fal_client
        print("✅ fal_client imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import fal_client: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        from fal_video_generator import FALVideoGenerator
        print("✅ FALVideoGenerator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import FALVideoGenerator: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment...")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check for FAL_KEY
        fal_key = os.getenv('FAL_KEY')
        if fal_key:
            if fal_key.startswith('fal-'):
                print("✅ FAL_KEY found and appears to be valid format")
            else:
                print("⚠️  FAL_KEY found but may not be in correct format (should start with 'fal-')")
        else:
            print("❌ FAL_KEY not found in environment")
            return False
    else:
        print("⚠️  .env file not found")
        print("💡 Create a .env file with your FAL_KEY to test API functionality")
        return False
    
    return True

def test_generator_initialization():
    """Test FAL Video Generator initialization"""
    print("\n🎬 Testing FAL Video Generator initialization...")
    
    try:
        from fal_video_generator import FALVideoGenerator
        
        # Try to initialize (this will check for API key)
        generator = FALVideoGenerator()
        print("✅ FALVideoGenerator initialized successfully")
        
        # Check if the endpoint is set
        if hasattr(generator, 'model_endpoint'):
            print(f"✅ Model endpoint: {generator.model_endpoint}")
        
        return True
        
    except ValueError as e:
        print(f"❌ Failed to initialize FALVideoGenerator: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during initialization: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 FAL AI Setup Test")
    print("=" * 30)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test environment
    if not test_environment():
        all_passed = False
    
    # Test generator initialization
    if not test_generator_initialization():
        all_passed = False
    
    # Summary
    print("\n" + "=" * 30)
    if all_passed:
        print("🎉 All tests passed! Setup is ready.")
        print("💡 You can now run 'python demo.py' to test video generation")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("💡 Make sure to:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Create .env file with your FAL_KEY")
        print("   3. Verify your FAL AI API key is correct")

if __name__ == "__main__":
    main() 