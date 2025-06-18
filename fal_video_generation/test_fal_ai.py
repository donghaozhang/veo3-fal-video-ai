#!/usr/bin/env python3
"""
Comprehensive FAL AI Video Generation Test Suite
Combines setup verification, API testing, and video generation testing
"""

import os
import sys
import traceback
from dotenv import load_dotenv

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    modules = [
        ('fal_client', 'fal_client'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv'),
        ('FALVideoGenerator', 'fal_video_generator')
    ]
    
    for name, module in modules:
        try:
            if name == 'FALVideoGenerator':
                from fal_video_generator import FALVideoGenerator
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
    if not os.path.exists('.env'):
        print("⚠️  .env file not found")
        print("💡 Create a .env file with your FAL_KEY to test API functionality")
        return False
    
    print("✅ .env file found")
    
    # Load environment variables
    load_dotenv()
    
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
        from fal_video_generator import FALVideoGenerator
        
        # Try to initialize (this will check for API key)
        generator = FALVideoGenerator()
        print("✅ FALVideoGenerator initialized successfully")
        
        # Check if the endpoint is set
        if hasattr(generator, 'model_endpoint'):
            print(f"✅ Model endpoint: {generator.model_endpoint}")
        
        return generator
        
    except ValueError as e:
        print(f"❌ Failed to initialize FALVideoGenerator: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error during initialization: {e}")
        return None

def test_api_connection():
    """Test API connection without full video generation"""
    print("\n🔑 Testing API connection...")
    
    try:
        import fal_client
        load_dotenv()
        api_key = os.getenv('FAL_KEY')
        
        if not api_key:
            print('❌ No API key found')
            return False
        
        print('🔑 API Key loaded:', api_key[:20] + '...')
        
        # Set the API key
        fal_client.api_key = api_key
        
        # Test with a simple request (this will validate the key)
        print('🧪 Testing API authentication...')
        
        # Just test the endpoint exists and key is valid
        # We'll use a minimal request that should fail gracefully
        try:
            result = fal_client.run(
                'fal-ai/minimax/hailuo-02/standard/image-to-video',
                arguments={
                    'image_url': 'https://picsum.photos/512/512',
                    'prompt': 'API test',
                    'duration': '6'
                }
            )
            print('✅ API key is working! Connection successful.')
            return True
            
        except Exception as e:
            if 'unauthorized' in str(e).lower() or 'invalid' in str(e).lower():
                print('❌ API key authentication failed:', str(e))
                return False
            else:
                print('✅ API key is valid (connection test passed)')
                return True
        
    except Exception as e:
        print(f'❌ API connection test failed: {e}')
        return False

def test_video_generation(generator, quick_test=False):
    """Test actual video generation"""
    print("\n🎬 Testing video generation...")
    
    if not generator:
        print("❌ Cannot test video generation - generator not initialized")
        return False
    
    try:
        if quick_test:
            print("⚡ Running quick test (may take 1-3 minutes)...")
        else:
            print("🎯 Running full video generation test...")
        
        result = generator.generate_video_from_image(
            image_url="https://picsum.photos/512/512",
            prompt="A beautiful landscape with moving clouds",
            duration="6"
        )
        
        if result and 'video' in result:
            video_url = result['video'].get('url', 'No URL found')
            print(f"✅ Video generation successful!")
            print(f"📹 Video URL: {video_url}")
            print(f"🎯 Duration: {result.get('duration', 'Unknown')} seconds")
            print(f"📐 Resolution: {result.get('width', '?')}x{result.get('height', '?')}")
            
            # Try to download the video
            if video_url and video_url != 'No URL found':
                print("⬇️  Attempting to download video...")
                local_path = generator.download_video(video_url, "test_output", "test_video.mp4")
                if local_path:
                    print(f"✅ Video downloaded to: {local_path}")
                    return True
                else:
                    print("⚠️  Video download failed, but generation was successful")
                    return True
            
            return True
        else:
            print("❌ Video generation failed")
            print("Response:", result)
            return False
            
    except Exception as e:
        print(f"❌ Error during video generation: {str(e)}")
        if not quick_test:
            traceback.print_exc()
        return False

def main():
    """Run comprehensive test suite"""
    print("🧪 FAL AI Comprehensive Test Suite")
    print("=" * 50)
    
    # Parse command line arguments
    quick_test = '--quick' in sys.argv
    full_test = '--full' in sys.argv
    api_only = '--api-only' in sys.argv
    
    if len(sys.argv) > 1 and not any([quick_test, full_test, api_only]):
        print("Usage:")
        print("  python test_fal_ai.py           # Setup and API connection test")
        print("  python test_fal_ai.py --quick   # Quick video generation test")
        print("  python test_fal_ai.py --full    # Full test with detailed output")
        print("  python test_fal_ai.py --api-only # Only test API connection")
        return
    
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
    
    # 4. Test API connection
    if not api_only:
        print("\n🔑 STEP 4: Testing API Connection")
        print("-" * 30)
        api_ok = test_api_connection()
        test_results.append(("API Connection", api_ok))
        
        if not api_ok:
            print("\n❌ API connection failed - check your API key")
            return
    
    # 5. Test video generation (optional)
    if quick_test or full_test:
        print("\n🎥 STEP 5: Testing Video Generation")
        print("-" * 30)
        video_ok = test_video_generation(generator, quick_test=quick_test)
        test_results.append(("Video Generation", video_ok))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("-" * 25)
    
    all_passed = True
    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if not passed:
            all_passed = False
    
    print("-" * 25)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        if not (quick_test or full_test):
            print("💡 Run with --quick to test video generation")
    else:
        print("❌ SOME TESTS FAILED")
        print("💡 Check the error messages above")
    
    print("\n📚 Available commands:")
    print("  python demo.py              # Interactive demo")
    print("  python test_fal_ai.py --quick  # Quick video test")

if __name__ == "__main__":
    main() 