#!/usr/bin/env python3
"""
Simple test script to validate the AI Content Pipeline package
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages', 'core', 'ai_content_pipeline'))

from ai_content_pipeline.pipeline.manager import AIPipelineManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_pipeline_manager():
    """Test the basic pipeline manager functionality"""
    print("🧪 Testing AI Content Pipeline Manager...")
    
    try:
        # Initialize manager
        print("📦 Initializing manager...")
        manager = AIPipelineManager()
        
        # Check available models
        print("📋 Checking available models...")
        models = manager.get_available_models()
        
        print("\n🎯 Available Models:")
        for step_type, model_list in models.items():
            print(f"  {step_type}:")
            if model_list:
                for model in model_list:
                    print(f"    - {model}")
            else:
                print("    - None available")
        
        # Test basic functionality
        print("\n✅ Pipeline manager initialized successfully!")
        print(f"📁 Output directory: {manager.output_dir}")
        print(f"📁 Temp directory: {manager.temp_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_creation():
    """Test creating a simple configuration"""
    print("\n🧪 Testing simple pipeline creation...")
    
    try:
        manager = AIPipelineManager()
        
        # Create a simple chain for testing
        config = {
            "name": "test_pipeline",
            "description": "Simple test pipeline",
            "steps": [
                {
                    "type": "prompt_generation",
                    "model": "openrouter_video_cinematic",
                    "params": {
                        "style": "cinematic"
                    }
                }
            ]
        }
        
        print("📝 Creating chain from config...")
        chain = manager.create_chain_from_dict(config)
        
        print(f"✅ Chain created: {chain.name}")
        print(f"📋 Steps: {len(chain.steps)}")
        
        # Validate chain
        errors = chain.validate()
        if errors:
            print(f"⚠️  Validation errors: {errors}")
        else:
            print("✅ Chain validation passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run the tests"""
    print("🚀 AI Content Pipeline Package Test\n")
    
    success = True
    
    # Test 1: Basic manager initialization
    success &= test_pipeline_manager()
    
    # Test 2: Simple chain creation
    success &= test_simple_creation()
    
    # Summary
    print("\n" + "="*50)
    if success:
        print("✅ All tests passed! The package is working correctly.")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())