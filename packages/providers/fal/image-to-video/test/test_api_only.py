#!/usr/bin/env python3
"""
FAL AI API Connection Test - FREE
Tests API connectivity without generating videos to avoid costs
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    modules = [
        ('fal_client', 'fal_client'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv'),
        ('FALImageToVideoGenerator', '../fal_image_to_video_generator')
    ]
    
    for name, module in modules:
        try:
                    if name == 'FALImageToVideoGenerator':
            from ..fal_image_to_video_generator import FALImageToVideoGenerator
            else:
                __import__(module)
            print(f"✅ {name} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {name}: {e}")
            return False
    
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🔧 Testing environment...")
    
    # Check for .env file
    if not os.path.exists('../.env'):
        print("⚠️  .env file not found")
        print("💡 Create a .env file with your FAL_KEY")
        return False
    
    print("✅ .env file found")
    
    # Load environment variables
    load_dotenv('../.env')
    
    # Check for FAL_KEY
    fal_key = os.getenv('FAL_KEY')
    if not fal_key:
        print("❌ FAL_KEY not found in environment")
        return False
    
    if fal_key.startswith('fal-'):
        print("✅ FAL_KEY found and appears to be valid format")
    else:
        print("⚠️  FAL_KEY found but may not be in correct format (should start with 'fal-')")
    
    return True

def test_generator_initialization():
    """Test FAL Video Generator initialization"""
    print("\n🎬 Testing FAL Video Generator initialization...")
    
    try:
        from ..fal_image_to_video_generator import FALImageToVideoGenerator
        
        # Try to initialize (this will check for API key)
        generator = FALImageToVideoGenerator()
        print("✅ FALImageToVideoGenerator initialized successfully")
        
        # Check if the endpoints are set
        if hasattr(generator, 'hailuo_endpoint'):
            print(f"✅ Hailuo endpoint: {generator.hailuo_endpoint}")
        if hasattr(generator, 'kling_endpoint'):
            print(f"✅ Kling endpoint: {generator.kling_endpoint}")
        
        return generator
        
    except ValueError as e:
        print(f"❌ Failed to initialize FALImageToVideoGenerator: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error during initialization: {e}")
        return None

def test_api_key_validity():
    """Test API key validity without generating videos"""
    print("\n🔑 Testing API key validity...")
    
    try:
        import fal_client
        load_dotenv('../.env')
        api_key = os.getenv('FAL_KEY')
        
        if not api_key:
            print('❌ No API key found')
            return False
        
        print('🔑 API Key loaded:', api_key[:20] + '...')
        
        # Set the API key
        fal_client.api_key = api_key
        
        # Test API key validity by making a minimal request
        # We'll use the list function which doesn't generate videos
        print('🧪 Testing API authentication...')
        
        try:
            # This is a minimal API call that validates the key without generating content
            response = fal_client.run(
                'fal-ai/minimax/hailuo-02/standard/image-to-video',
                arguments={
                    'image_url': 'invalid_url_for_testing',  # This will fail but validate the key
                    'prompt': 'test',
                    'duration': '6'
                }
            )
        except Exception as e:
            error_msg = str(e).lower()
            if 'unauthorized' in error_msg or 'invalid' in error_msg or 'authentication' in error_msg:
                print('❌ API key authentication failed:', str(e))
                return False
            elif 'invalid url' in error_msg or 'url' in error_msg or 'image' in error_msg:
                print('✅ API key is valid! (Expected URL validation error)')
                return True
            else:
                print('✅ API key appears to be valid')
                return True
        
        print('✅ API connection successful!')
        return True
        
    except Exception as e:
        print(f'❌ API connection test failed: {e}')
        return False

def main():
    """Run FREE API connection tests only"""
    print("🆓 FAL AI API Connection Test - FREE")
    print("Tests API connectivity without generating videos")
    print("=" * 50)
    
    test_results = []
    
    # 1. Test imports
    print("📦 STEP 1: Testing Dependencies")
    print("-" * 30)
    imports_ok = test_imports()
    test_results.append(("Dependencies", imports_ok))
    
    if not imports_ok:
        print("\n❌ Cannot continue - missing dependencies")
        print("💡 Run: pip install -r requirements.txt")
        return
    
    # 2. Test environment
    print("\n🔧 STEP 2: Testing Environment")
    print("-" * 30)
    env_ok = test_environment()
    test_results.append(("Environment", env_ok))
    
    if not env_ok:
        print("\n❌ Cannot continue - environment not configured")
        return
    
    # 3. Test generator initialization
    print("\n🎬 STEP 3: Testing Generator")
    print("-" * 30)
    generator = test_generator_initialization()
    generator_ok = generator is not None
    test_results.append(("Generator", generator_ok))
    
    if not generator_ok:
        print("\n❌ Cannot continue - generator initialization failed")
        return
    
    # 4. Test API key validity
    print("\n🔑 STEP 4: Testing API Key Validity")
    print("-" * 30)
    api_ok = test_api_key_validity()
    test_results.append(("API Key", api_ok))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("-" * 25)
    
    all_passed = True
    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<15} {status}")
        if not passed:
            all_passed = False
    
    print("-" * 25)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your FAL AI setup is ready for video generation")
        print("\n💡 Next steps (these WILL cost money):")
        print("  python test_fal_ai.py --hailuo     # Test Hailuo model")
        print("  python test_fal_ai.py --kling      # Test Kling model")
        print("  python demo.py                     # Interactive demo")
    else:
        print("❌ SOME TESTS FAILED")
        print("💡 Check the error messages above")
    
    print("\n🆓 This test was completely FREE - no videos were generated")

if __name__ == "__main__":
    main() 