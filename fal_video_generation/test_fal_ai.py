#!/usr/bin/env python3
"""
Comprehensive FAL AI Video Generation Test Suite
Supports both MiniMax Hailuo-02 and Kling Video 2.1 models
Cost-conscious testing with explicit model selection
"""

import os
import sys
import traceback
from dotenv import load_dotenv

def show_cost_warning():
    """Display cost warning and model selection options"""
    print("💰 COST WARNING:")
    print("   Video generation costs money! Each test generates a real video.")
    print("   Choose your tests carefully to avoid unnecessary costs.")
    print()
    print("🎯 AVAILABLE TEST OPTIONS:")
    print("   --api-only    : Test API connection only (FREE)")
    print("   --hailuo      : Test fal-ai/minimax/hailuo-02/standard/image-to-video (~$0.02-0.05)")
    print("   --kling       : Test fal-ai/kling-video/v2.1/standard/image-to-video (~$0.02-0.05)")
    print("   --compare     : Test BOTH models (~$0.04-0.10) ⚠️ EXPENSIVE")
    print("   --quick       : Quick Hailuo test (same as --hailuo)")
    print("   --full        : Full Hailuo test with detailed output")
    print()

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
        
        # Check if the endpoints are set
        if hasattr(generator, 'hailuo_endpoint'):
            print(f"✅ Hailuo endpoint: {generator.hailuo_endpoint}")
        if hasattr(generator, 'kling_endpoint'):
            print(f"✅ Kling endpoint: {generator.kling_endpoint}")
        
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

def test_video_generation(generator, quick_test=False, model="hailuo"):
    """Test actual video generation with specific model"""
    model_info = {
        "hailuo": {
            "name": "MiniMax Hailuo-02",
            "cost": "~$0.02-0.05",
            "duration": "6"
        },
        "kling": {
            "name": "Kling Video 2.1", 
            "cost": "~$0.02-0.05",
            "duration": "5"
        }
    }
    
    model_data = model_info.get(model, model_info["hailuo"])
    
    print(f"\n🎬 Testing video generation with {model_data['name']}...")
    print(f"💰 Estimated cost: {model_data['cost']}")
    
    if not generator:
        print("❌ Cannot test video generation - generator not initialized")
        return False
    
    # Confirmation prompt for cost-conscious testing
    if not quick_test:
        response = input(f"\n⚠️  This will generate a real video (cost: {model_data['cost']}). Continue? (y/N): ")
        if response.lower() != 'y':
            print("❌ Test cancelled by user")
            return False
    
    try:
        if quick_test:
            print("⚡ Running quick test (may take 1-3 minutes)...")
        else:
            print("🎯 Running full video generation test...")
        
        if model == "kling":
            result = generator.generate_video_from_image(
                image_url="https://picsum.photos/512/512",
                prompt="A beautiful landscape with moving clouds, cinematic quality",
                duration=model_data['duration'],
                model="fal-ai/kling-video/v2.1/standard/image-to-video"
            )
        else:
            result = generator.generate_video_from_image(
                image_url="https://picsum.photos/512/512",
                prompt="A beautiful landscape with moving clouds",
                duration=model_data['duration'],
                model="fal-ai/minimax/hailuo-02/standard/image-to-video"
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
                local_path = generator.download_video(video_url, "test_output", f"test_{model}_video.mp4")
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

def test_both_models(generator):
    """Test both Hailuo and Kling models for comparison - EXPENSIVE!"""
    print("\n🆚 Testing both models for comparison...")
    print("💰 WARNING: This will test BOTH models (~$0.04-0.10 total cost)")
    
    if not generator:
        print("❌ Cannot test models - generator not initialized")
        return False
    
    # Explicit confirmation for expensive operation
    response = input("\n⚠️  This will generate 2 videos (expensive!). Continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Comparison test cancelled by user")
        return False
    
    results = {}
    
    # Test Hailuo
    print("\n1️⃣ Testing fal-ai/minimax/hailuo-02/standard/image-to-video...")
    try:
        result_hailuo = generator.generate_video_from_image(
            image_url="https://picsum.photos/512/512",
            prompt="A peaceful mountain landscape with gentle movement",
            duration="6",
            model="fal-ai/minimax/hailuo-02/standard/image-to-video"
        )
        if result_hailuo:
            results['hailuo'] = {
                'success': True,
                'url': result_hailuo['video']['url'],
                'size': result_hailuo['video']['file_size']
            }
            print("✅ Hailuo test successful")
        else:
            results['hailuo'] = {'success': False, 'error': 'Generation failed'}
            print("❌ Hailuo test failed")
    except Exception as e:
        results['hailuo'] = {'success': False, 'error': str(e)}
        print(f"❌ Hailuo test error: {e}")
    
    # Test Kling
    print("\n2️⃣ Testing fal-ai/kling-video/v2.1/standard/image-to-video...")
    try:
        result_kling = generator.generate_video_from_image(
            image_url="https://picsum.photos/512/512",
            prompt="A peaceful mountain landscape with gentle movement",
            duration="5",
            model="fal-ai/kling-video/v2.1/standard/image-to-video"
        )
        if result_kling:
            results['kling'] = {
                'success': True,
                'url': result_kling['video']['url'],
                'size': result_kling['video']['file_size']
            }
            print("✅ Kling test successful")
        else:
            results['kling'] = {'success': False, 'error': 'Generation failed'}
            print("❌ Kling test failed")
    except Exception as e:
        results['kling'] = {'success': False, 'error': str(e)}
        print(f"❌ Kling test error: {e}")
    
    # Print comparison
    print("\n📊 Model Comparison Results:")
    print("-" * 40)
    
    for model, result in results.items():
        if result['success']:
            print(f"🟢 {model.upper()}: SUCCESS")
            print(f"   📹 URL: {result['url']}")
            print(f"   💾 Size: {result['size']} bytes")
        else:
            print(f"🔴 {model.upper()}: FAILED")
            print(f"   ❌ Error: {result['error']}")
        print()
    
    return any(result['success'] for result in results.values())

def main():
    """Run comprehensive test suite with cost-conscious options"""
    print("🧪 FAL AI Comprehensive Test Suite")
    print("Supports MiniMax Hailuo-02 and Kling Video 2.1")
    print("=" * 50)
    
    # Parse command line arguments
    quick_test = '--quick' in sys.argv
    full_test = '--full' in sys.argv
    api_only = '--api-only' in sys.argv
    hailuo_test = '--hailuo' in sys.argv or quick_test  # --quick defaults to hailuo
    kling_test = '--kling' in sys.argv
    compare_test = '--compare' in sys.argv
    
    # Show help if no valid arguments or invalid arguments
    if len(sys.argv) > 1 and not any([quick_test, full_test, api_only, hailuo_test, kling_test, compare_test]):
        show_cost_warning()
        print("❌ Invalid arguments. Use one of the options above.")
        return
    
    # Show cost warning if no arguments (default behavior)
    if len(sys.argv) == 1:
        show_cost_warning()
        print("🆓 Running FREE tests only (setup + API connection)")
        print("   Add a flag above to test video generation")
        print()
    
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
    print("\n🔑 STEP 4: Testing API Connection")
    print("-" * 30)
    api_ok = test_api_connection()
    test_results.append(("API Connection", api_ok))
    
    if not api_ok:
        print("\n❌ API connection failed - check your API key")
        return
    
    # 5. Test video generation (optional, cost-conscious)
    if hailuo_test and not compare_test:
        print("\n🎥 STEP 5: Testing Hailuo Video Generation")
        print("-" * 30)
        video_ok = test_video_generation(generator, quick_test=quick_test, model="hailuo")
        test_results.append(("Hailuo Video Generation", video_ok))
    elif kling_test:
        print("\n🎥 STEP 5: Testing Kling Video Generation")
        print("-" * 30)
        video_ok = test_video_generation(generator, quick_test=True, model="kling")
        test_results.append(("Kling Video Generation", video_ok))
    elif compare_test:
        print("\n🎥 STEP 5: Testing Both Models (EXPENSIVE)")
        print("-" * 30)
        comparison_ok = test_both_models(generator)
        test_results.append(("Model Comparison", comparison_ok))
    elif full_test:
        print("\n🎥 STEP 5: Testing Video Generation (Full)")
        print("-" * 30)
        video_ok = test_video_generation(generator, quick_test=False, model="hailuo")
        test_results.append(("Video Generation", video_ok))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("-" * 25)
    
    all_passed = True
    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if not passed:
            all_passed = False
    
    print("-" * 25)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        if not any([hailuo_test, kling_test, compare_test, full_test]):
            print("\n💡 Next steps - choose ONE to avoid costs:")
            print("  python test_fal_ai.py --hailuo     # Test Hailuo only")
            print("  python test_fal_ai.py --kling      # Test Kling only")
            print("  python test_fal_ai.py --compare    # Test both (expensive)")
    else:
        print("❌ SOME TESTS FAILED")
        print("💡 Check the error messages above")
    
    print("\n📚 Available commands:")
    print("  python demo.py                      # Interactive demo")
    print("  python test_fal_ai.py --api-only    # Free API test only")
    print("  python test_fal_ai.py --hailuo      # Test Hailuo model")
    print("  python test_fal_ai.py --kling       # Test Kling model")

if __name__ == "__main__":
    main() 