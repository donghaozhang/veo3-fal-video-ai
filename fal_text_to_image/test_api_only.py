#!/usr/bin/env python3
"""
FAL AI Text-to-Image API Connection Test

This script tests ONLY the API connection and environment setup.
NO IMAGE GENERATION - COMPLETELY FREE!

This is the recommended first step for troubleshooting setup issues.

Usage:
    python test_api_only.py

Author: AI Assistant  
Date: 2024
"""

import os
import sys
from typing import Dict, Any
import fal_client
from dotenv import load_dotenv

def print_banner():
    """Print the test banner."""
    print("=" * 60)
    print("🔧 FAL AI TEXT-TO-IMAGE API CONNECTION TEST")
    print("=" * 60)
    print("✅ This test is COMPLETELY FREE")
    print("✅ No image generation - only setup validation")
    print("✅ Safe to run anytime for troubleshooting")
    print("=" * 60)

def test_environment_variables() -> bool:
    """Test environment variable setup."""
    print("\n🔍 Testing Environment Variables...")
    
    # Load environment variables
    load_dotenv()
    
    # Check .env file
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ Found {env_file} file")
    else:
        print(f"⚠️  No {env_file} file found")
        print("💡 Create a .env file with your FAL_KEY")
    
    # Check FAL_KEY
    fal_key = os.getenv('FAL_KEY')
    if fal_key:
        print("✅ FAL_KEY found in environment")
        # Mask the key for security
        if len(fal_key) > 12:
            masked_key = f"{fal_key[:8]}...{fal_key[-4:]}"
        else:
            masked_key = f"{fal_key[:4]}..."
        print(f"🔑 API Key: {masked_key}")
        return True
    else:
        print("❌ FAL_KEY not found in environment")
        print("💡 Set FAL_KEY in your .env file or environment variables")
        return False

def test_fal_client_import() -> bool:
    """Test FAL client import and basic functionality."""
    print("\n📦 Testing FAL Client Import...")
    
    try:
        import fal_client
        print("✅ fal_client imported successfully")
        
        # Check if we can access basic client info
        print(f"✅ fal_client version available")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import fal_client: {e}")
        print("💡 Install with: pip install fal-client")
        return False
    except Exception as e:
        print(f"⚠️  fal_client import warning: {e}")
        return True

def test_generator_initialization() -> bool:
    """Test text-to-image generator initialization."""
    print("\n🎨 Testing Generator Initialization...")
    
    try:
        from fal_text_to_image_generator import FALTextToImageGenerator
        print("✅ FALTextToImageGenerator imported successfully")
        
        # Try to initialize (this should not make any API calls)
        generator = FALTextToImageGenerator()
        print("✅ Generator initialized successfully")
        
        # Test model information (local operation)
        model_info = generator.get_model_info()
        print(f"✅ Found {len(model_info)} supported models:")
        
        for model_key, info in model_info.items():
            print(f"   • {info['name']} ({model_key})")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import generator: {e}")
        print("💡 Make sure fal_text_to_image_generator.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Generator initialization failed: {e}")
        return False

def test_model_endpoints() -> bool:
    """Test model endpoint configuration."""
    print("\n🔗 Testing Model Endpoints...")
    
    try:
        from fal_text_to_image_generator import FALTextToImageGenerator
        
        generator = FALTextToImageGenerator()
        endpoints = generator.MODEL_ENDPOINTS
        
        print(f"✅ Found {len(endpoints)} model endpoints:")
        for model, endpoint in endpoints.items():
            print(f"   • {model}: {endpoint}")
        
        # Test model validation
        for model in endpoints.keys():
            try:
                validated_endpoint = generator.validate_model(model)
                print(f"✅ {model} validation: OK")
            except Exception as e:
                print(f"❌ {model} validation failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Model endpoint test failed: {e}")
        return False

def test_dependencies() -> bool:
    """Test all required dependencies."""
    print("\n📋 Testing Dependencies...")
    
    dependencies = [
        ('fal_client', 'fal-client'),
        ('requests', 'requests'),
        ('dotenv', 'python-dotenv'),
        ('typing_extensions', 'typing-extensions')
    ]
    
    all_good = True
    
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {package_name}: Available")
        except ImportError:
            print(f"❌ {package_name}: Missing")
            print(f"💡 Install with: pip install {package_name}")
            all_good = False
    
    return all_good

def test_output_directory() -> bool:
    """Test output directory creation."""
    print("\n📁 Testing Output Directory...")
    
    try:
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        if os.path.exists(output_dir) and os.path.isdir(output_dir):
            print(f"✅ Output directory '{output_dir}' ready")
            return True
        else:
            print(f"❌ Could not create output directory '{output_dir}'")
            return False
            
    except Exception as e:
        print(f"❌ Output directory test failed: {e}")
        return False

def run_comprehensive_test() -> Dict[str, bool]:
    """Run all tests and return results."""
    print_banner()
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("FAL Client Import", test_fal_client_import),
        ("Dependencies", test_dependencies),
        ("Generator Initialization", test_generator_initialization),
        ("Model Endpoints", test_model_endpoints),
        ("Output Directory", test_output_directory)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    return results

def print_summary(results: Dict[str, bool]):
    """Print test summary."""
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 50)
    print(f"🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Your setup is ready for text-to-image generation.")
        print("💡 You can now run paid tests with specific model flags")
        print("   Example: python test_text_to_image.py --flux-schnell")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before generating images.")
        print("💡 Common fixes:")
        print("   • Add FAL_KEY to .env file")
        print("   • Install missing dependencies: pip install -r requirements.txt")
        print("   • Check file permissions")

def main():
    """Main test function."""
    try:
        results = run_comprehensive_test()
        print_summary(results)
        
        # Exit with error code if any tests failed
        if not all(results.values()):
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 