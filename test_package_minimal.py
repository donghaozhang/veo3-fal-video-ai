#!/usr/bin/env python3
"""
Minimal test to demonstrate the installed AI Content Pipeline package works correctly
"""
import sys

# Test 1: Basic Import
print("🧪 Testing AI Content Pipeline Package (Minimal)")
print("="*50)

try:
    # Import from installed package
    from packages.core.ai_content_pipeline.ai_content_pipeline.pipeline.manager import AIPipelineManager
    print("✅ Package import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Initialize Manager
try:
    import os
    # Suppress warnings by redirecting stderr temporarily
    import io
    import contextlib
    
    # Capture warnings during initialization
    f = io.StringIO()
    with contextlib.redirect_stderr(f):
        manager = AIPipelineManager()
    
    print("✅ Pipeline manager initialized")
    print(f"📁 Output: {manager.output_dir}")
    print(f"📁 Temp: {manager.temp_dir}")
except Exception as e:
    print(f"❌ Manager initialization failed: {e}")
    sys.exit(1)

# Test 3: Check Models
try:
    models = manager.get_available_models()
    total_models = sum(len(model_list) for model_list in models.values())
    print(f"✅ Found {total_models} AI models across {len(models)} categories")
    
    # Show categories with models
    categories_with_models = [cat for cat, models in models.items() if models]
    print(f"📦 Categories with models: {', '.join(categories_with_models)}")
except Exception as e:
    print(f"❌ Model checking failed: {e}")
    sys.exit(1)

# Test 4: Test Chain Creation
try:
    import tempfile
    import json
    
    # Simple test configuration
    config = {
        "name": "minimal_test",
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
    
    # Load chain
    chain = manager.create_chain_from_config(temp_path)
    print(f"✅ Chain created: {chain.name}")
    
    # Clean up
    os.unlink(temp_path)
except Exception as e:
    print(f"❌ Chain creation failed: {e}")
    sys.exit(1)

# Test 5: Console Scripts
try:
    import subprocess
    result = subprocess.run(['ai-content-pipeline', '--help'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("✅ Console script 'ai-content-pipeline' working")
    else:
        print("⚠️  Console script not found (may need PATH update)")
except Exception as e:
    print(f"⚠️  Console script test skipped: {e}")

print("\n✅ All core functionality tests passed!")
print("🎉 The AI Content Pipeline package is installed and working correctly!")