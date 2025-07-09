#!/usr/bin/env python3
"""
Basic test to demonstrate AI Content Pipeline package functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages', 'core', 'ai_content_pipeline'))

from ai_content_pipeline.pipeline.manager import AIPipelineManager
from ai_content_pipeline.pipeline.chain import ContentCreationChain, PipelineStep, StepType
from dotenv import load_dotenv
import tempfile
import json

# Load environment variables
load_dotenv()

def test_basic_functionality():
    """Test basic package functionality"""
    print("🧪 Testing AI Content Pipeline Package Basic Functionality")
    print("="*60)
    
    # Initialize manager
    print("📦 Initializing pipeline manager...")
    manager = AIPipelineManager()
    print(f"✅ Manager initialized")
    print(f"📁 Output directory: {manager.output_dir}")
    print(f"📁 Temp directory: {manager.temp_dir}")
    
    # Check available models
    print("\n📋 Available models:")
    models = manager.get_available_models()
    for step_type, model_list in models.items():
        print(f"  {step_type}: {len(model_list)} models")
        if model_list:
            for model in model_list[:3]:  # Show first 3 models
                print(f"    - {model}")
            if len(model_list) > 3:
                print(f"    ... and {len(model_list) - 3} more")
    
    # Test chain creation
    print("\n🔗 Testing chain creation...")
    test_config = {
        "name": "test_chain",
        "description": "Test chain for package validation",
        "steps": [
            {
                "type": "image_to_video",
                "model": "kling",
                "params": {
                    "duration": 5
                }
            }
        ]
    }
    
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_config, f)
        temp_config_path = f.name
    
    try:
        chain = manager.create_chain_from_config(temp_config_path)
        print(f"✅ Chain created: {chain.name}")
        print(f"📋 Steps: {len(chain.steps)}")
        
        # Test validation
        errors = chain.validate()
        if errors:
            print(f"⚠️  Validation issues: {errors}")
        else:
            print("✅ Chain validation passed")
            
        # Test cost estimation
        cost_info = manager.estimate_chain_cost(chain)
        print(f"💰 Estimated cost: ${cost_info['total_cost']:.4f}")
        
    finally:
        # Clean up
        os.unlink(temp_config_path)
    
    print("\n🎯 Package basic functionality test completed successfully!")
    return True

def test_yaml_config():
    """Test YAML configuration loading"""
    print("\n🧪 Testing YAML configuration loading...")
    
    try:
        manager = AIPipelineManager()
        
        # Test with the existing YAML file
        yaml_path = "input/pipelines/analysis_detailed_gemini.yaml"
        if os.path.exists(yaml_path):
            print(f"📄 Loading config from: {yaml_path}")
            chain = manager.create_chain_from_config(yaml_path)
            print(f"✅ YAML config loaded successfully")
            print(f"📋 Chain: {chain.name}")
            print(f"📝 Description: {chain.description}")
            print(f"🔗 Steps: {len(chain.steps)}")
            
            # Show step details
            for i, step in enumerate(chain.steps, 1):
                print(f"   Step {i}: {step.step_type.value} ({step.model})")
            
            return True
        else:
            print(f"⚠️  YAML file not found: {yaml_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error loading YAML config: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Content Pipeline Package Test Suite")
    print("="*60)
    
    success = True
    
    # Test 1: Basic functionality
    try:
        success &= test_basic_functionality()
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        success = False
    
    # Test 2: YAML config loading
    try:
        success &= test_yaml_config()
    except Exception as e:
        print(f"❌ YAML config test failed: {e}")
        success = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    if success:
        print("✅ All tests passed!")
        print("🎉 The AI Content Pipeline package is working correctly.")
        print("\n💡 The package can:")
        print("   - Initialize pipeline manager")
        print("   - Load YAML configurations")
        print("   - Create and validate chains")
        print("   - Estimate costs")
        print("   - Show available models")
        print("\n🔧 Usage:")
        print("   ai-content-pipeline --help")
        print("   ai-content-pipeline list-models")
        print("   ai-content-pipeline run-chain --config config.yaml")
    else:
        print("❌ Some tests failed!")
        print("⚠️  Check the output above for specific issues.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())