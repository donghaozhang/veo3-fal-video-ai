#!/usr/bin/env python3
"""
Test FAL Video to Video setup and environment
Run this first to validate your setup before incurring API costs
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
import fal_client
from fal_video_to_video.config.constants import SUPPORTED_MODELS, MODEL_INFO


def test_environment():
    """Test environment setup."""
    print("🔧 Testing environment setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("FAL_KEY")
    if not api_key:
        print("❌ FAL_KEY not found in environment variables")
        print("   Please set FAL_KEY in .env file")
        return False
    else:
        print("✅ FAL_KEY found")
        # Set masked key for testing
        fal_client.api_key = api_key[:10] + "..." if len(api_key) > 10 else api_key
    
    return True


def test_imports():
    """Test that all modules can be imported."""
    print("\n📦 Testing imports...")
    
    try:
        from fal_video_to_video import FALVideoToVideoGenerator
        print("✅ FALVideoToVideoGenerator imported successfully")
        
        from fal_video_to_video.models.thinksound import ThinkSoundModel
        print("✅ ThinkSoundModel imported successfully")
        
        from fal_video_to_video.utils.validators import validate_model, validate_video_url
        print("✅ Validators imported successfully")
        
        from fal_video_to_video.utils.file_utils import ensure_output_directory
        print("✅ File utils imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_model_info():
    """Test model information retrieval."""
    print("\n📋 Testing model information...")
    
    try:
        for model in SUPPORTED_MODELS:
            info = MODEL_INFO.get(model)
            if info:
                print(f"✅ {model}: {info['model_name']}")
                print(f"   Features: {len(info.get('features', []))} listed")
                print(f"   Pricing: {info.get('pricing', 'N/A')}")
            else:
                print(f"❌ No info found for model: {model}")
                return False
        return True
    except Exception as e:
        print(f"❌ Error testing model info: {e}")
        return False


def test_directories():
    """Test directory structure."""
    print("\n📁 Testing directory structure...")
    
    required_dirs = [
        "input",
        "output", 
        "test_output",
        "fal_video_to_video",
        "fal_video_to_video/config",
        "fal_video_to_video/models",
        "fal_video_to_video/utils"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ Missing: {dir_path}/")
            all_exist = False
    
    return all_exist


def test_dependencies():
    """Test required dependencies."""
    print("\n📚 Testing dependencies...")
    
    required_packages = [
        "fal_client",
        "dotenv",
        "requests"
    ]
    
    all_available = True
    for package in required_packages:
        try:
            __import__(package.replace("_", "-").replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ Missing: {package}")
            all_available = False
    
    # Test optional dependencies
    optional_packages = [
        "moviepy"
    ]
    
    print("\nOptional dependencies:")
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} (for video info)")
        except ImportError:
            print(f"⚠️  {package} (optional - for video info)")
    
    return all_available


def main():
    """Run all setup tests."""
    print("🎵 FAL Video to Video Setup Test")
    print("=" * 40)
    
    tests = [
        ("Environment", test_environment),
        ("Imports", test_imports),
        ("Model Info", test_model_info), 
        ("Directories", test_directories),
        ("Dependencies", test_dependencies)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print(f"\n📊 Setup Test Summary")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! You're ready to use FAL Video to Video")
        print("\nNext steps:")
        print("1. Add a test video to the input/ folder")
        print("2. Run: python tests/test_generation.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()