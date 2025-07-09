#!/usr/bin/env python3
"""
FAL AI Image-to-Image Setup and API Test

This script tests ONLY the setup, environment, and API connection.
NO IMAGE GENERATION - COMPLETELY FREE!

This is the recommended first step for troubleshooting setup issues.

Usage:
    python test_setup.py

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
    print("🔧 FAL AI IMAGE-TO-IMAGE SETUP TEST")
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

def test_generator_initialization() -> bool:
    """Test image-to-image generator initialization."""
    print("\n🎨 Testing Generator Initialization...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        print("✅ FALImageToImageGenerator imported successfully")
        
        # Try to initialize (this should not make any API calls)
        generator = FALImageToImageGenerator()
        print("✅ Generator initialized successfully")
        
        # Test model information (local operation)
        all_models = generator.get_model_info()
        print(f"✅ Model Info Retrieved for both models:")
        
        for model_key, model_info in all_models.items():
            print(f"   • {model_key.upper()}: {model_info['model_name']}")
            print(f"     - Endpoint: {model_info['endpoint']}")
            print(f"     - Features: {len(model_info['features'])} features")
        
        # Test individual model info
        photon_info = generator.get_model_info("photon")
        kontext_info = generator.get_model_info("kontext")
        print(f"✅ Individual model info retrieval successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import generator: {e}")
        print("💡 Make sure fal_image_to_image_generator.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Generator initialization failed: {e}")
        return False

def test_model_validation() -> bool:
    """Test model parameter validation."""
    print("\n🔗 Testing Model Validation...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator, ASPECT_RATIOS, SUPPORTED_MODELS
        
        generator = FALImageToImageGenerator()
        
        # Test model validation
        for model in SUPPORTED_MODELS:
            try:
                validated = generator.validate_model(model)
                print(f"✅ Model {model}: Valid")
            except Exception as e:
                print(f"❌ Model {model}: {e}")
                return False
        
        # Test Photon aspect ratio validation
        print("   Testing Photon aspect ratios...")
        for aspect_ratio in ASPECT_RATIOS:
            try:
                validated = generator.validate_aspect_ratio(aspect_ratio, "photon")
                print(f"✅ Photon aspect ratio {aspect_ratio}: Valid")
            except Exception as e:
                print(f"❌ Photon aspect ratio {aspect_ratio}: {e}")
                return False
        
        # Test Kontext resolution modes
        print("   Testing Kontext resolution modes...")
        kontext_modes = ["auto", "match_input"]
        for mode in kontext_modes:
            try:
                validated = generator.validate_aspect_ratio(mode, "kontext")
                print(f"✅ Kontext resolution mode {mode}: Valid")
            except Exception as e:
                print(f"❌ Kontext resolution mode {mode}: {e}")
                return False
        
        # Test Photon strength validation
        print("   Testing Photon strength values...")
        test_strengths = [0.0, 0.5, 1.0]
        for strength in test_strengths:
            try:
                validated = generator.validate_strength(strength)
                print(f"✅ Photon strength {strength}: Valid")
            except Exception as e:
                print(f"❌ Photon strength {strength}: {e}")
                return False
        
        # Test Kontext inference steps validation
        print("   Testing Kontext inference steps...")
        test_steps = [1, 28, 50]
        for steps in test_steps:
            try:
                validated = generator.validate_inference_steps(steps)
                print(f"✅ Kontext inference steps {steps}: Valid")
            except Exception as e:
                print(f"❌ Kontext inference steps {steps}: {e}")
                return False
        
        # Test Kontext guidance scale validation
        print("   Testing Kontext guidance scale...")
        test_scales = [1.0, 2.5, 20.0]
        for scale in test_scales:
            try:
                validated = generator.validate_guidance_scale(scale)
                print(f"✅ Kontext guidance scale {scale}: Valid")
            except Exception as e:
                print(f"❌ Kontext guidance scale {scale}: {e}")
                return False
        
        # Test invalid values
        print("   Testing invalid parameter rejection...")
        
        try:
            generator.validate_model("invalid")
            print("❌ Invalid model validation failed")
            return False
        except ValueError:
            print("✅ Invalid model correctly rejected")
        
        try:
            generator.validate_aspect_ratio("invalid", "photon")
            print("❌ Invalid aspect ratio validation failed")
            return False
        except ValueError:
            print("✅ Invalid aspect ratio correctly rejected")
        
        try:
            generator.validate_strength(1.5)
            print("❌ Invalid strength validation failed")
            return False
        except ValueError:
            print("✅ Invalid strength correctly rejected")
        
        try:
            generator.validate_inference_steps(100)
            print("❌ Invalid inference steps validation failed")
            return False
        except ValueError:
            print("✅ Invalid inference steps correctly rejected")
        
        try:
            generator.validate_guidance_scale(25.0)
            print("❌ Invalid guidance scale validation failed")
            return False
        except ValueError:
            print("✅ Invalid guidance scale correctly rejected")
        
        return True
        
    except Exception as e:
        print(f"❌ Model validation test failed: {e}")
        return False

def test_output_directories() -> bool:
    """Test output directory creation."""
    print("\n📁 Testing Output Directories...")
    
    try:
        directories = ["output"]
        
        for output_dir in directories:
            os.makedirs(output_dir, exist_ok=True)
            
            if os.path.exists(output_dir) and os.path.isdir(output_dir):
                print(f"✅ Directory '{output_dir}' ready")
            else:
                print(f"❌ Could not create directory '{output_dir}'")
                return False
        
        return True
            
    except Exception as e:
        print(f"❌ Output directory test failed: {e}")
        return False

def test_model_endpoints() -> bool:
    """Test model endpoint configuration."""
    print("\n🔗 Testing Model Endpoints...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        endpoints = generator.get_model_endpoints()
        
        expected_endpoints = {
            "photon": "fal-ai/luma-photon/flash/modify",
            "kontext": "fal-ai/flux-kontext/dev"
        }
        
        for model, expected_endpoint in expected_endpoints.items():
            actual_endpoint = endpoints.get(model)
            if actual_endpoint == expected_endpoint:
                print(f"✅ {model.title()} endpoint correct: {actual_endpoint}")
            else:
                print(f"❌ {model.title()} endpoint mismatch:")
                print(f"   Expected: {expected_endpoint}")
                print(f"   Actual: {actual_endpoint}")
                return False
        
        # Test supported models list
        supported_models = generator.get_supported_models()
        expected_models = ["photon", "kontext"]
        
        if set(supported_models) == set(expected_models):
            print(f"✅ Supported models correct: {supported_models}")
        else:
            print(f"❌ Supported models mismatch:")
            print(f"   Expected: {expected_models}")
            print(f"   Actual: {supported_models}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Model endpoints test failed: {e}")
        return False

def run_comprehensive_test() -> Dict[str, bool]:
    """Run all tests and return results."""
    print_banner()
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Dependencies", test_dependencies),
        ("Generator Initialization", test_generator_initialization),
        ("Model Validation", test_model_validation),
        ("Output Directories", test_output_directories),
        ("Model Endpoints", test_model_endpoints)
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
    print("📊 SETUP TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 50)
    print(f"🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All setup tests passed! Your environment is ready.")
        print("💡 Next steps:")
        print("   • python test_generation.py --help - See image modification options")
        print("   • python demo.py - Interactive demo with cost controls")
        print("   • Remember: Image modification costs money (~$0.01-0.05 per image)")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("💡 Common fixes:")
        print("   • Add FAL_KEY to .env file")
        print("   • Install missing dependencies: pip install -r requirements.txt")
        print("   • Check file permissions")

def main():
    """Main test function."""
    try:
        results = run_comprehensive_test()
        print_summary(results)
        
        # Exit with error code if any critical tests failed
        critical_tests = ["Environment Variables", "Dependencies", "Generator Initialization"]
        critical_passed = all(results.get(test, False) for test in critical_tests)
        
        if not critical_passed:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()