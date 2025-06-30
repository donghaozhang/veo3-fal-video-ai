#!/usr/bin/env python3
"""
FAL Text-to-Video Setup Test (FREE - No API costs)

This script tests the setup and environment without generating any videos,
so it won't incur any API costs. Use this to validate your configuration
before running actual video generation.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def test_environment():
    """Test environment setup and dependencies."""
    print("🔍 Testing Environment Setup")
    print("=" * 50)
    
    # Test Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version compatible")
    
    # Test required imports
    print("\n📦 Testing Dependencies...")
    
    try:
        import fal_client
        print("✅ fal_client imported successfully")
        print(f"   Version: {getattr(fal_client, '__version__', 'unknown')}")
    except ImportError as e:
        print(f"❌ fal_client import failed: {e}")
        print("💡 Install with: pip install fal-client")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
        print(f"   Version: {requests.__version__}")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        print("💡 Install with: pip install requests")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        print("💡 Install with: pip install python-dotenv")
        return False
    
    return True

def test_environment_variables():
    """Test environment variable configuration."""
    print("\n🔧 Testing Environment Variables...")
    
    # Load .env file if it exists
    env_file = Path(".env")
    if env_file.exists():
        load_dotenv()
        print("✅ .env file found and loaded")
    else:
        print("ℹ️ No .env file found (using system environment)")
    
    # Check FAL_KEY
    fal_key = os.getenv('FAL_KEY')
    if fal_key:
        # Check API key format (FAL keys have format: uuid:hash)
        if ':' in fal_key and len(fal_key.split(':')) == 2:
            uuid_part, hash_part = fal_key.split(':')
            if len(uuid_part) >= 30 and len(hash_part) >= 30:
                # Mask the key for security
                masked_key = uuid_part[:8] + '*' * (len(uuid_part) - 8) + ':' + hash_part[:4] + '*' * (len(hash_part) - 8) + hash_part[-4:]
                print(f"✅ FAL_KEY found: {masked_key}")
                print("✅ API key format appears valid")
                return True
        
        print("❌ FAL_KEY found but format appears invalid (should be uuid:hash format)")
        return False
    else:
        print("❌ FAL_KEY not found")
        print("💡 Set your API key:")
        print("   export FAL_KEY='your_api_key_here'")
        print("   Or create a .env file with: FAL_KEY=your_api_key_here")
        print("   Get your key from: https://fal.ai/dashboard/keys")
        return False

def test_directory_structure():
    """Test directory structure and permissions."""
    print("\n📁 Testing Directory Structure...")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📂 Current directory: {current_dir}")
    
    # Test output directory creation
    output_dir = Path("output")
    try:
        output_dir.mkdir(exist_ok=True)
        print(f"✅ Output directory ready: {output_dir.absolute()}")
        
        # Test write permissions
        test_file = output_dir / "test_write.tmp"
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Write permissions confirmed")
        
    except Exception as e:
        print(f"❌ Directory/permission error: {e}")
        return False
    
    return True

def test_module_import():
    """Test importing the FAL Text-to-Video module."""
    print("\n🎬 Testing Module Import...")
    
    try:
        from fal_text_to_video_generator import FALTextToVideoGenerator, TextToVideoModel
        print("✅ FALTextToVideoGenerator imported successfully")
        print("✅ TextToVideoModel enum imported successfully")
        
        # Test model info (no API call)
        generator = FALTextToVideoGenerator(api_key="dummy:dummy", verbose=False)
        all_models_info = generator.get_model_info()
        print(f"✅ Model info retrieved: {len(all_models_info['available_models'])} models available")
        
        # Test cost calculations
        minimax_cost = generator.calculate_cost(TextToVideoModel.MINIMAX_HAILUO)
        veo3_cost = generator.calculate_cost(TextToVideoModel.GOOGLE_VEO3, "8s", True)
        print(f"✅ Cost calculation working: MiniMax ${minimax_cost:.2f}, Veo3 ${veo3_cost:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        return False

def test_api_key_validation():
    """Test API key validation without making API calls."""
    print("\n🔑 Testing API Key Validation...")
    
    fal_key = os.getenv('FAL_KEY')
    if not fal_key:
        print("❌ No API key to validate")
        return False
    
    try:
        # Import and test initialization (no API calls)
        from fal_text_to_video_generator import FALTextToVideoGenerator
        
        generator = FALTextToVideoGenerator(verbose=False)
        print("✅ Generator initialized successfully")
        
        # Test connection method (validates format only, no API call)
        connection_ok = generator.test_connection()
        if connection_ok:
            print("✅ API key format validation passed")
            return True
        else:
            print("❌ API key format validation failed")
            return False
            
    except Exception as e:
        print(f"❌ API key validation error: {e}")
        return False

def main():
    """Run all setup tests."""
    print("🧪 FAL Text-to-Video Setup Test")
    print("💡 This test is completely FREE - no API calls are made")
    print("=" * 60)
    
    tests = [
        ("Environment", test_environment),
        ("Environment Variables", test_environment_variables),
        ("Directory Structure", test_directory_structure),
        ("Module Import", test_module_import),
        ("API Key Validation", test_api_key_validation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Setup Test Summary")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready for video generation.")
        print("💡 Next steps:")
        print("   1. Run test_generation.py to test actual video generation (costs ~$0.08)")
        print("   2. Use demo.py for interactive video generation")
        print("   3. Use the FALTextToVideoGenerator class in your own code")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please fix the issues above.")
        print("💡 Common fixes:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - Set your API key: export FAL_KEY='your_api_key_here'")
        print("   - Get API key from: https://fal.ai/dashboard/keys")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)