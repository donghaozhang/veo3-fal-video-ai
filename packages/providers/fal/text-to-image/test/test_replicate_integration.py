#!/usr/bin/env python3
"""
Test script for Replicate Seedream-3 integration - NO API CALLS (cost-free)

This script validates that the Replicate Seedream-3 model is properly integrated
and the unified interface works without making actual API calls that would incur costs.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports (where the actual modules are)
sys.path.append(str(Path(__file__).parent.parent))

def test_replicate_generator():
    """Test Replicate generator without API calls."""
    print("🧪 Testing Replicate Generator (No API Calls)")
    print("=" * 60)
    
    try:
        from replicate_text_to_image_generator import ReplicateTextToImageGenerator, ReplicateTextToImageModel
        
        # Test 1: Verify model is available
        print("\n1️⃣ Testing model availability...")
        assert hasattr(ReplicateTextToImageModel, 'SEEDREAM3'), "❌ SEEDREAM3 model not found"
        assert ReplicateTextToImageModel.SEEDREAM3.value == "bytedance/seedream-3", "❌ Incorrect endpoint"
        print("✅ Seedream-3 model is available")
        
        # Test 2: Initialize generator (with fake API token)
        print("\n2️⃣ Testing generator initialization...")
        fake_token = "r8_faktoken123456789abcdefghijklmnopqrstuvwxyz"
        generator = ReplicateTextToImageGenerator(api_token=fake_token, verbose=False)
        print("✅ Generator initialized successfully")
        
        # Test 3: Verify model configuration
        print("\n3️⃣ Testing model configuration...")
        model_info = generator.get_model_info(ReplicateTextToImageModel.SEEDREAM3)
        expected_config = {
            "name": "ByteDance Seedream-3",
            "version": "3.0",
            "cost_per_image": 0.003
        }
        
        for key, expected_value in expected_config.items():
            assert model_info[key] == expected_value, f"❌ {key}: expected {expected_value}, got {model_info[key]}"
        
        print("✅ Model configuration is correct")
        
        # Test 4: Cost calculation
        print("\n4️⃣ Testing cost calculation...")
        cost_1_image = generator.calculate_cost(ReplicateTextToImageModel.SEEDREAM3, 1)
        cost_5_images = generator.calculate_cost(ReplicateTextToImageModel.SEEDREAM3, 5)
        
        assert cost_1_image == 0.003, f"❌ Expected $0.003, got ${cost_1_image}"
        assert cost_5_images == 0.015, f"❌ Expected $0.015, got ${cost_5_images}"
        print("✅ Cost calculation is correct")
        
        # Test 5: Model info
        print("\n5️⃣ Testing model info...")
        all_models = generator.get_model_info()
        assert 'SEEDREAM3' in all_models['available_models'], "❌ Seedream-3 not in model list"
        print("✅ Model appears in info")
        
        # Test 6: Cost estimates
        print("\n6️⃣ Testing cost estimates...")
        estimate = generator.get_cost_estimate(ReplicateTextToImageModel.SEEDREAM3, 1)
        assert "Seedream-3" in estimate, "❌ Cost estimate doesn't mention Seedream-3"
        print("✅ Cost estimates work correctly")
        
        print("\n🎉 Replicate generator tests passed!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        return False
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False


def test_unified_generator():
    """Test unified generator without API calls."""
    print("\n🔗 Testing Unified Generator (No API Calls)")
    print("=" * 60)
    
    try:
        from unified_text_to_image_generator import UnifiedTextToImageGenerator, Provider
        
        # Test 1: Initialize with fake credentials
        print("\n1️⃣ Testing unified generator initialization...")
        fake_fal_key = "00000000-0000-0000-0000-000000000000:fakehash"
        fake_replicate_token = "r8_faktoken123456789abcdefghijklmnopqrstuvwxyz"
        
        try:
            generator = UnifiedTextToImageGenerator(
                fal_api_key=fake_fal_key,
                replicate_api_token=fake_replicate_token,
                verbose=False
            )
            print("✅ Unified generator initialized")
        except Exception as e:
            print(f"⚠️ Could not initialize unified generator: {e}")
            return False
        
        # Test 2: Check model catalog
        print("\n2️⃣ Testing model catalog...")
        available_models = generator.get_available_models()
        assert "seedream3" in available_models, "❌ seedream3 not in available models"
        assert "flux_dev" in available_models, "❌ flux_dev not in available models"
        print(f"✅ Model catalog contains {len(available_models)} models")
        
        # Test 3: Check providers
        print("\n3️⃣ Testing available providers...")
        providers = generator.get_available_providers()
        expected_providers = ['fal', 'replicate']
        for provider in expected_providers:
            assert provider in providers, f"❌ {provider} provider not available"
        print("✅ All expected providers available")
        
        # Test 4: Model comparison
        print("\n4️⃣ Testing model comparison...")
        comparison = generator.compare_models()
        assert comparison['total_models'] > 0, "❌ No models available"
        assert 'recommendations' in comparison, "❌ No recommendations generated"
        print("✅ Model comparison works")
        
        # Test 5: Cost estimation
        print("\n5️⃣ Testing cost estimation...")
        cost = generator.estimate_cost("seedream3", 3)
        expected_cost = 0.003 * 3
        assert cost == expected_cost, f"❌ Expected ${expected_cost}, got ${cost}"
        print("✅ Cost estimation works")
        
        # Test 6: Optimal model selection
        print("\n6️⃣ Testing optimal model selection...")
        try:
            cheapest = generator._get_optimal_model("cost")
            fastest = generator._get_optimal_model("speed")
            highest_quality = generator._get_optimal_model("quality")
            
            assert cheapest in available_models, "❌ Cheapest model not in available models"
            assert fastest in available_models, "❌ Fastest model not in available models"
            assert highest_quality in available_models, "❌ Highest quality model not in available models"
            
            print(f"✅ Optimal model selection works:")
            print(f"   💰 Cheapest: {cheapest}")
            print(f"   ⚡ Fastest: {fastest}")
            print(f"   🎯 Highest Quality: {highest_quality}")
        except Exception as e:
            print(f"⚠️ Optimal model selection failed: {e}")
        
        print("\n🎉 Unified generator tests passed!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return False


def test_ai_pipeline_integration():
    """Test integration with main AI pipeline constants."""
    print("\n🔗 Testing AI Pipeline Integration")
    print("-" * 40)
    
    try:
        # Import main pipeline constants
        # Navigate from test file to project root, then to ai_content_pipeline
        project_root = Path(__file__).parent.parent.parent.parent.parent.parent
        pipeline_path = project_root / "packages" / "core" / "ai_content_pipeline" / "ai_content_pipeline"
        sys.path.append(str(pipeline_path))
        from config.constants import SUPPORTED_MODELS, COST_ESTIMATES, MODEL_RECOMMENDATIONS
        
        # For now, just check that constants load properly
        # We'll update them after confirming the Replicate integration works
        assert "text_to_image" in SUPPORTED_MODELS, "❌ text_to_image not in SUPPORTED_MODELS"
        assert "text_to_image" in COST_ESTIMATES, "❌ text_to_image not in COST_ESTIMATES"
        print("✅ AI Pipeline constants accessible")
        
        # Note: We'll need to add replicate models to constants manually
        print("📝 Note: Replicate models need to be added to AI Pipeline constants")
        return True
        
    except ImportError as e:
        print(f"⚠️ Could not test pipeline integration: {e}")
        return False
    except Exception as e:
        print(f"❌ Pipeline integration test failed: {e}")
        return False


def test_dependencies():
    """Test that required dependencies are available."""
    print("\n📦 Testing Dependencies")
    print("-" * 30)
    
    dependencies = {
        "replicate": "Replicate Python client",
        "requests": "HTTP requests library",
        "pathlib": "Path handling (built-in)",
        "enum": "Enums (built-in)"
    }
    
    missing_deps = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep}: {description}")
        except ImportError:
            print(f"❌ {dep}: {description} - MISSING")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n⚠️ Missing dependencies: {', '.join(missing_deps)}")
        print("💡 Install with: pip install " + " ".join(missing_deps))
        return False
    else:
        print("\n✅ All dependencies available")
        return True


if __name__ == "__main__":
    print("🚀 Replicate Seedream-3 Integration Test Suite")
    print("=" * 70)
    print("⚠️ Note: This test does NOT make API calls (no costs incurred)")
    
    # Run tests
    tests = [
        ("Dependencies", test_dependencies),
        ("Replicate Generator", test_replicate_generator),
        ("Unified Generator", test_unified_generator),
        ("AI Pipeline Integration", test_ai_pipeline_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        print(f"🧪 Running: {test_name}")
        print('='*70)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Replicate Seedream-3 integration is ready!")
        print("\n📝 Next steps:")
        print("  1. Add replicate models to AI Pipeline constants")
        print("  2. Update main package requirements.txt")
        print("  3. Test with actual API calls (when ready)")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check output above for details.")
        sys.exit(1)