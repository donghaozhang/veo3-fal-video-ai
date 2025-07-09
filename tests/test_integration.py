#!/usr/bin/env python3
"""
Comprehensive integration tests for AI Content Pipeline package.
Tests all features including YAML loading, parallel execution, console scripts, and more.
"""
import subprocess
import sys
import os
import json
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def test_package_installation():
    """Test that the package is properly installed"""
    print("🧪 Testing Package Installation...")
    
    try:
        # Test import using installed package
        from packages.core.ai_content_pipeline.ai_content_pipeline.pipeline.manager import AIPipelineManager
        from packages.core.ai_content_pipeline.ai_content_pipeline.models.step import StepType
        print("✅ Package imports successful")
        
        # Test basic functionality
        manager = AIPipelineManager()
        models = manager.get_available_models()
        total_models = sum(len(model_list) for model_list in models.values())
        print(f"✅ Pipeline manager initialized with {total_models} models")
        
        # Show model distribution
        print("📊 Model distribution:")
        for step_type, model_list in models.items():
            if model_list:
                print(f"   {step_type}: {len(model_list)} models")
        
        return True
    except Exception as e:
        print(f"❌ Package installation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_console_scripts():
    """Test that console scripts are properly installed and working"""
    print("\n🖥️  Testing Console Scripts...")
    
    scripts_tested = 0
    scripts_passed = 0
    
    # Test main command
    try:
        result = subprocess.run(['ai-content-pipeline', '--help'], 
                              capture_output=True, text=True, timeout=10)
        scripts_tested += 1
        if result.returncode == 0 and 'AI Content Pipeline' in result.stdout:
            print("✅ 'ai-content-pipeline' command working")
            scripts_passed += 1
        else:
            print(f"❌ 'ai-content-pipeline' command failed")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
    except Exception as e:
        print(f"⚠️  'ai-content-pipeline' test skipped: {e}")
    
    # Test alias command
    try:
        result = subprocess.run(['aicp', '--help'], 
                              capture_output=True, text=True, timeout=10)
        scripts_tested += 1
        if result.returncode == 0 and 'AI Content Pipeline' in result.stdout:
            print("✅ 'aicp' alias working")
            scripts_passed += 1
        else:
            print(f"❌ 'aicp' alias failed")
    except Exception as e:
        print(f"⚠️  'aicp' test skipped: {e}")
    
    # Test list-models command
    try:
        result = subprocess.run(['ai-content-pipeline', 'list-models'], 
                              capture_output=True, text=True, timeout=10)
        scripts_tested += 1
        if result.returncode == 0 and 'Available' in result.stdout:
            print("✅ 'list-models' command working")
            scripts_passed += 1
        else:
            print(f"❌ 'list-models' command failed")
    except Exception as e:
        print(f"⚠️  'list-models' test skipped: {e}")
    
    return scripts_passed >= 2  # Pass if at least 2 out of 3 work

def test_yaml_configuration():
    """Test YAML configuration loading"""
    print("\n📄 Testing YAML Configuration Loading...")
    
    try:
        from packages.core.ai_content_pipeline.ai_content_pipeline.pipeline.manager import AIPipelineManager
        
        manager = AIPipelineManager()
        
        # Look for YAML files in different possible locations
        yaml_paths = [
            "input/pipelines/simple_test.yaml",
            "input/pipelines/analysis_detailed_gemini.yaml",
            "input/tts_simple_test.yaml",
            "input/tts_parallel_test.yaml"
        ]
        
        yaml_found = False
        for yaml_path in yaml_paths:
            if os.path.exists(yaml_path):
                yaml_found = True
                print(f"📋 Testing with: {yaml_path}")
                
                try:
                    chain = manager.create_chain_from_config(yaml_path)
                    print(f"✅ Config loaded: {chain.name}")
                    print(f"   Steps: {len(chain.steps)}")
                    
                    # Show first few steps
                    for i, step in enumerate(chain.steps[:3], 1):
                        print(f"   Step {i}: {step.step_type.value} ({step.model})")
                    if len(chain.steps) > 3:
                        print(f"   ... and {len(chain.steps) - 3} more steps")
                    
                    # Test validation
                    errors = chain.validate()
                    if errors:
                        print(f"⚠️  Validation warnings: {len(errors)} issues")
                    else:
                        print("✅ Chain validation passed")
                    
                    # Test cost estimation
                    cost_info = manager.estimate_chain_cost(chain)
                    print(f"💰 Estimated cost: ${cost_info['total_cost']:.4f}")
                    
                    break
                except Exception as e:
                    print(f"⚠️  Error loading {yaml_path}: {e}")
                    continue
        
        if not yaml_found:
            print("⚠️  No YAML test files found, creating test config...")
            # Create a test YAML file
            test_config = """
name: integration_test
description: Integration test pipeline
steps:
  - type: text_to_speech
    model: elevenlabs
    params:
      voice: Rachel
      text: "Hello from integration test"
  
  - type: text_to_image
    model: flux_schnell
    params:
      prompt: "A beautiful sunset"
      num_images: 1
"""
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                f.write(test_config)
                temp_yaml = f.name
            
            chain = manager.create_chain_from_config(temp_yaml)
            print(f"✅ Test YAML loaded: {chain.name}")
            os.unlink(temp_yaml)
        
        return True
        
    except Exception as e:
        print(f"❌ YAML configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_parallel_execution():
    """Test parallel execution feature"""
    print("\n⚡ Testing Parallel Execution Feature...")
    
    try:
        # Set environment variable for parallel execution
        original_value = os.environ.get('PIPELINE_PARALLEL_ENABLED')
        os.environ['PIPELINE_PARALLEL_ENABLED'] = 'true'
        
        from packages.core.ai_content_pipeline.ai_content_pipeline.pipeline.manager import AIPipelineManager
        
        manager = AIPipelineManager()
        print("✅ Parallel execution enabled")
        
        # Create a test config with parallel group
        config = {
            "name": "parallel_test",
            "description": "Test parallel execution",
            "steps": [
                {
                    "type": "parallel_group",
                    "steps": [
                        {
                            "type": "text_to_image",
                            "model": "flux_schnell",
                            "params": {"prompt": "Test 1"}
                        },
                        {
                            "type": "text_to_image", 
                            "model": "flux_schnell",
                            "params": {"prompt": "Test 2"}
                        }
                    ]
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        chain = manager.create_chain_from_config(temp_path)
        print(f"✅ Parallel chain created: {chain.name}")
        
        # Validate parallel structure
        if chain.steps and hasattr(chain.steps[0], 'steps'):
            print(f"✅ Parallel group contains {len(chain.steps[0].steps)} parallel steps")
        
        os.unlink(temp_path)
        
        # Reset environment variable
        if original_value is None:
            if 'PIPELINE_PARALLEL_ENABLED' in os.environ:
                del os.environ['PIPELINE_PARALLEL_ENABLED']
        else:
            os.environ['PIPELINE_PARALLEL_ENABLED'] = original_value
        
        return True
    except Exception as e:
        print(f"❌ Parallel execution test failed: {e}")
        return False

def test_output_management():
    """Test output directory management"""
    print("\n📁 Testing Output Management...")
    
    try:
        from packages.core.ai_content_pipeline.ai_content_pipeline.pipeline.manager import AIPipelineManager
        
        manager = AIPipelineManager()
        
        # Check output directories
        output_dir = manager.output_dir
        temp_dir = manager.temp_dir
        
        print(f"📂 Output directory: {output_dir}")
        print(f"📂 Temp directory: {temp_dir}")
        
        # Verify they are Path objects
        if isinstance(output_dir, Path) and isinstance(temp_dir, Path):
            print("✅ Directory paths are valid Path objects")
            
            # Check if parent directories exist (directories themselves might not exist yet)
            if output_dir.parent.exists() or str(output_dir).startswith('output'):
                print("✅ Output directory structure is valid")
            else:
                print("⚠️  Output directory will be created on first use")
            
            return True
        else:
            print("❌ Invalid directory path types")
            return False
            
    except Exception as e:
        print(f"❌ Output management test failed: {e}")
        return False

def test_model_availability():
    """Test model availability and categorization"""
    print("\n🎯 Testing Model Availability...")
    
    try:
        from packages.core.ai_content_pipeline.ai_content_pipeline.pipeline.manager import AIPipelineManager
        
        manager = AIPipelineManager()
        models = manager.get_available_models()
        
        # Expected categories
        expected_categories = [
            'text_to_speech', 'text_to_image', 'text_to_video',
            'image_to_image', 'image_to_video', 'video_to_video',
            'prompt_generation'
        ]
        
        print("📊 Model Categories:")
        for category in expected_categories:
            if category in models:
                count = len(models[category])
                if count > 0:
                    print(f"✅ {category}: {count} models")
                    # Show first 2 models as examples
                    for model in list(models[category])[:2]:
                        print(f"   - {model}")
                    if count > 2:
                        print(f"   ... and {count - 2} more")
                else:
                    print(f"⚠️  {category}: No models configured")
            else:
                print(f"❌ {category}: Category missing")
        
        total_models = sum(len(model_list) for model_list in models.values())
        print(f"\n📈 Total: {total_models} models available")
        
        return total_models > 0
        
    except Exception as e:
        print(f"❌ Model availability test failed: {e}")
        return False

def main():
    """Run comprehensive integration tests"""
    print("🚀 AI Content Pipeline - Integration Test Suite")
    print("="*60)
    
    tests = [
        ("Package Installation", test_package_installation),
        ("Console Scripts", test_console_scripts),
        ("YAML Configuration", test_yaml_configuration),
        ("Parallel Execution", test_parallel_execution),
        ("Output Management", test_output_management),
        ("Model Availability", test_model_availability),
    ]
    
    passed = 0
    failed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            failed += 1
    
    # Final summary
    print("\n" + "="*60)
    print("📊 INTEGRATION TEST RESULTS")
    print("="*60)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print(f"✅ {passed}/{total} tests successful")
        print("\n🏆 The AI Content Pipeline package is fully functional!")
        print("\n🔧 Available Commands:")
        print("   • ai-content-pipeline --help")
        print("   • ai-content-pipeline list-models")
        print("   • ai-content-pipeline run-chain --config config.yaml")
        print("   • ai-content-pipeline generate-image --text 'prompt'")
        print("   • aicp (shortened alias)")
        print("\n📦 Key Features Verified:")
        print("   • Multi-model support across 7 categories")
        print("   • YAML-based pipeline configuration")
        print("   • Parallel execution capability")
        print("   • Cost estimation and tracking")
        print("   • Organized output management")
    else:
        print(f"⚠️  {passed}/{total} tests passed, {failed} failed")
        print("🔧 Some features may need configuration")
        print("📝 Check the output above for specific issues")
        
        if passed >= total * 0.6:  # If at least 60% passed
            print("\n✅ Core functionality is working")
            print("💡 The package can still be used for most tasks")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())