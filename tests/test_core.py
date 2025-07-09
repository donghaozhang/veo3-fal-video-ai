#!/usr/bin/env python3
"""
Core AI Content Pipeline Package Tests

Fast smoke tests for essential functionality validation.
Recommended for quick development checks and CI/CD.
"""
import sys
import os
import tempfile
import json
from dotenv import load_dotenv

# Use the installed package directly
from packages.core.ai_content_pipeline.ai_content_pipeline.pipeline.manager import AIPipelineManager

# Load environment variables
load_dotenv()

def test_package_import():
    """Test that the package can be imported correctly"""
    print("🧪 Testing Package Import...")
    try:
        # Test is already done by importing above
        print("✅ Package import successful")
        return True
    except Exception as e:
        print(f"❌ Package import failed: {e}")
        return False

def test_manager_initialization():
    """Test pipeline manager initialization"""
    print("🧪 Testing Manager Initialization...")
    try:
        manager = AIPipelineManager()
        print("✅ Pipeline manager initialized")
        print(f"📁 Output: {manager.output_dir}")
        print(f"📁 Temp: {manager.temp_dir}")
        return True, manager
    except Exception as e:
        print(f"❌ Manager initialization failed: {e}")
        return False, None

def test_model_availability():
    """Test that AI models are available"""
    print("🧪 Testing Model Availability...")
    try:
        manager = AIPipelineManager()
        models = manager.get_available_models()
        total_models = sum(len(model_list) for model_list in models.values())
        
        print(f"✅ Found {total_models} AI models across {len(models)} categories")
        
        # Show categories with models
        categories_with_models = [cat for cat, model_list in models.items() if model_list]
        print(f"📦 Categories: {', '.join(categories_with_models)}")
        
        return total_models > 0
    except Exception as e:
        print(f"❌ Model availability test failed: {e}")
        return False

def test_chain_creation():
    """Test basic chain creation"""
    print("🧪 Testing Chain Creation...")
    try:
        manager = AIPipelineManager()
        
        # Simple test configuration
        config = {
            "name": "core_test_chain",
            "steps": [{
                "type": "image_to_video",
                "model": "kling",
                "params": {"duration": 5}
            }]
        }
        
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            chain = manager.create_chain_from_config(temp_path)
            print(f"✅ Chain created: {chain.name}")
            
            # Test validation
            errors = chain.validate()
            if errors:
                print(f"⚠️  Validation issues: {errors}")
            else:
                print("✅ Chain validation passed")
            
            return True
        finally:
            os.unlink(temp_path)
            
    except Exception as e:
        print(f"❌ Chain creation failed: {e}")
        return False

def main():
    """Run core tests"""
    print("🚀 AI Content Pipeline - Core Tests")
    print("="*50)
    
    tests = [
        ("Package Import", test_package_import),
        ("Manager Initialization", test_manager_initialization),
        ("Model Availability", test_model_availability),
        ("Chain Creation", test_chain_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if isinstance(result, tuple):
                result = result[0]  # Handle manager initialization return
            
            if result:
                passed += 1
                print(f"✅ {test_name} - PASSED\n")
            else:
                print(f"❌ {test_name} - FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}\n")
    
    # Summary
    print("="*50)
    print(f"📊 CORE TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core tests passed!")
        print("✅ Package is ready for use")
        return 0
    else:
        print("⚠️  Some core tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())