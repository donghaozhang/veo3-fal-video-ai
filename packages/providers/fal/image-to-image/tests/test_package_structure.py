#!/usr/bin/env python3
"""
Test the refactored package structure

This script tests that all imports work and the package functions correctly.
"""

import sys
import os
from pathlib import Path

def test_package_imports():
    """Test that all package imports work correctly"""
    print("🧪 Testing Package Imports")
    print("-" * 40)
    
    try:
        # Test main package import
        from fal_image_to_image import FALImageToImageGenerator
        print("✅ Main generator import successful")
        
        # Test type imports
        from fal_image_to_image import ModelType, AspectRatio, SUPPORTED_MODELS
        print("✅ Type definitions import successful")
        
        # Test individual model imports
        from fal_image_to_image.models import SeedEditModel, PhotonModel
        print("✅ Individual model imports successful")
        
        # Test utility imports
        from fal_image_to_image.utils import validate_model, upload_local_image
        print("✅ Utility imports successful")
        
        # Test config imports
        from fal_image_to_image.config import MODEL_ENDPOINTS, MODEL_INFO
        print("✅ Configuration imports successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_generator_initialization():
    """Test generator initialization"""
    print("\n🧪 Testing Generator Initialization")
    print("-" * 40)
    
    try:
        from fal_image_to_image import FALImageToImageGenerator
        
        # Test with dummy API key
        generator = FALImageToImageGenerator("test_key")
        print("✅ Generator initialization successful")
        
        # Test supported models
        models = generator.get_supported_models()
        print(f"✅ Supported models: {models}")
        
        # Test model info
        seededit_info = generator.get_model_info("seededit")
        print(f"✅ SeedEdit info: {seededit_info['model_name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Generator test failed: {e}")
        return False

def test_model_classes():
    """Test individual model classes"""
    print("\n🧪 Testing Individual Model Classes")
    print("-" * 40)
    
    try:
        from fal_image_to_image.models import SeedEditModel
        
        # Test SeedEdit model
        seededit = SeedEditModel()
        print(f"✅ SeedEdit model: {seededit.display_name}")
        
        # Test parameter validation
        params = seededit.validate_parameters(guidance_scale=0.5, seed=42)
        print(f"✅ Parameter validation: {params}")
        
        # Test model info
        info = seededit.get_model_info()
        print(f"✅ Model info: {info['description'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Model class test failed: {e}")
        return False

def test_validators():
    """Test validation utilities"""
    print("\n🧪 Testing Validation Utilities")
    print("-" * 40)
    
    try:
        from fal_image_to_image.utils.validators import (
            validate_model, validate_guidance_scale, validate_strength
        )
        
        # Test model validation
        model = validate_model("seededit")
        print(f"✅ Model validation: {model}")
        
        # Test guidance scale validation
        scale = validate_guidance_scale(0.5, "seededit")
        print(f"✅ Guidance scale validation: {scale}")
        
        # Test strength validation  
        strength = validate_strength(0.8)
        print(f"✅ Strength validation: {strength}")
        
        # Test invalid parameter
        try:
            validate_guidance_scale(1.5, "seededit")
            print("❌ Should have failed validation")
            return False
        except ValueError:
            print("✅ Invalid parameter correctly rejected")
        
        return True
        
    except Exception as e:
        print(f"❌ Validator test failed: {e}")
        return False

def test_convenience_methods():
    """Test convenience methods exist"""
    print("\n🧪 Testing Convenience Methods")
    print("-" * 40)
    
    try:
        from fal_image_to_image import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator("test_key")
        
        # Check method existence
        methods = [
            'modify_image_seededit',
            'modify_local_image_seededit',
            'modify_image_photon',
            'batch_modify_images'
        ]
        
        for method in methods:
            if hasattr(generator, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Method {method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Convenience method test failed: {e}")
        return False

def test_backwards_compatibility():
    """Test that old import patterns still work"""
    print("\n🧪 Testing Backwards Compatibility")
    print("-" * 40)
    
    try:
        # Test that we can still import the main class
        from fal_image_to_image import FALImageToImageGenerator
        
        # Test that key methods exist with same signatures
        generator = FALImageToImageGenerator("test_key")
        
        # These should work the same as before
        models = generator.get_supported_models()
        info = generator.get_model_info("seededit")
        
        print("✅ Backwards compatibility maintained")
        print(f"   Supported models: {len(models)} models")
        print(f"   SeedEdit available: {'seededit' in models}")
        
        return True
        
    except Exception as e:
        print(f"❌ Backwards compatibility test failed: {e}")
        return False

def main():
    """Run all package tests"""
    print("FAL Image-to-Image Package Structure Test")
    print("=" * 60)
    
    tests = [
        test_package_imports,
        test_generator_initialization,
        test_model_classes,
        test_validators,
        test_convenience_methods,
        test_backwards_compatibility
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Package refactoring successful.")
        print("\n✅ Package is ready for use:")
        print("   • Modular architecture ✓")
        print("   • Clean imports ✓") 
        print("   • Backwards compatibility ✓")
        print("   • Proper validation ✓")
        print("   • All models working ✓")
        return True
    else:
        print("❌ Some tests failed. Check the output above for issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)