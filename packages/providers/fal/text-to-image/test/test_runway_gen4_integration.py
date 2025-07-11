#!/usr/bin/env python3
"""
Test script for Runway Gen4 integration - NO API CALLS (cost-free)

This script validates that the Runway Gen4 model is properly integrated
and the unified interface works without making actual API calls that would incur costs.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports (where the actual modules are)
sys.path.append(str(Path(__file__).parent.parent))

def test_runway_gen4_generator():
    """Test Runway Gen4 generator without API calls."""
    print("🎬 Testing Runway Gen4 Generator (No API Calls)")
    print("=" * 60)
    
    try:
        from runway_gen4_generator import RunwayGen4Generator, RunwayGen4Model
        
        # Test 1: Verify model is available
        print("\n1️⃣ Testing model availability...")
        assert hasattr(RunwayGen4Model, 'GEN4_IMAGE'), "❌ GEN4_IMAGE model not found"
        assert RunwayGen4Model.GEN4_IMAGE.value == "runwayml/gen4-image", "❌ Incorrect endpoint"
        print("✅ Runway Gen4 model is available")
        
        # Test 2: Initialize generator (with fake API token)
        print("\n2️⃣ Testing generator initialization...")
        fake_token = "r8_faktoken123456789abcdefghijklmnopqrstuvwxyz"
        generator = RunwayGen4Generator(api_token=fake_token, verbose=False)
        print("✅ Generator initialized successfully")
        
        # Test 3: Verify model configuration
        print("\n3️⃣ Testing model configuration...")
        model_info = generator.get_model_info(RunwayGen4Model.GEN4_IMAGE)
        expected_config = {
            "name": "Runway Gen-4 Image",
            "version": "4.0",
            "cost_720p": 0.05,
            "cost_1080p": 0.08
        }
        
        for key, expected_value in expected_config.items():
            assert model_info[key] == expected_value, f"❌ {key}: expected {expected_value}, got {model_info[key]}"
        
        print("✅ Model configuration is correct")
        
        # Test 4: Cost calculation
        print("\n4️⃣ Testing cost calculation...")
        cost_720p = generator.calculate_cost(RunwayGen4Model.GEN4_IMAGE, "720p", 1)
        cost_1080p = generator.calculate_cost(RunwayGen4Model.GEN4_IMAGE, "1080p", 1)
        cost_multiple = generator.calculate_cost(RunwayGen4Model.GEN4_IMAGE, "1080p", 3)
        
        assert cost_720p == 0.05, f"❌ Expected $0.05, got ${cost_720p}"
        assert cost_1080p == 0.08, f"❌ Expected $0.08, got ${cost_1080p}"
        assert cost_multiple == 0.24, f"❌ Expected $0.24, got ${cost_multiple}"
        print("✅ Cost calculation is correct")
        
        # Test 5: Model features validation
        print("\n5️⃣ Testing model features...")
        model_info = generator.get_model_info(RunwayGen4Model.GEN4_IMAGE)
        features = model_info.get("features", [])
        
        expected_features = [
            "Multi-reference image guidance",
            "Reference image tagging",
            "720p and 1080p resolution",
            "Multiple aspect ratio support"
        ]
        
        for feature_check in expected_features:
            found = any(feature_check.lower() in feature.lower() for feature in features)
            assert found, f"❌ Expected feature not found: {feature_check}"
        
        print("✅ Model features validated")
        
        # Test 6: Reference image validation
        print("\n6️⃣ Testing reference image validation...")
        
        # Test valid cases
        generator._validate_reference_images(None, None)  # No references
        generator._validate_reference_images(["url1"], ["tag1"])  # Single reference with tag
        generator._validate_reference_images(["url1", "url2", "url3"], ["tag1", "tag2", "tag3"])  # Max references
        
        # Test invalid cases
        try:
            generator._validate_reference_images(["url1", "url2", "url3", "url4"], None)  # Too many
            assert False, "❌ Should have failed with too many references"
        except ValueError:
            pass  # Expected
        
        try:
            generator._validate_reference_images(["url1", "url2"], ["tag1"])  # Mismatched tags
            assert False, "❌ Should have failed with mismatched tags"
        except ValueError:
            pass  # Expected
        
        print("✅ Reference image validation works correctly")
        
        print("\n🎉 Runway Gen4 generator tests passed!")
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


def test_unified_generator_with_gen4():
    """Test unified generator with Gen4 support."""
    print("\n🔗 Testing Unified Generator with Gen4 (No API Calls)")
    print("=" * 60)
    
    try:
        from unified_text_to_image_generator import UnifiedTextToImageGenerator
        
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
        
        # Test 2: Check model catalog includes Gen4
        print("\n2️⃣ Testing model catalog...")
        available_models = generator.get_available_models()
        assert "gen4" in available_models, "❌ gen4 not in available models"
        print(f"✅ Model catalog contains gen4 (total: {len(available_models)} models)")
        
        # Test 3: Check Gen4 model configuration
        print("\n3️⃣ Testing Gen4 model configuration...")
        model_config = generator.MODEL_CATALOG["gen4"]
        
        expected_gen4_config = {
            "name": "Runway Gen-4 Image",
            "cost_per_image": 0.08,
            "quality": "cinematic",
            "use_case": "Multi-reference guided generation"
        }
        
        for key, expected_value in expected_gen4_config.items():
            assert model_config[key] == expected_value, f"❌ {key}: expected {expected_value}, got {model_config[key]}"
        
        print("✅ Gen4 model configuration is correct")
        
        # Test 4: Check special features
        print("\n4️⃣ Testing Gen4 special features...")
        special_features = model_config.get("special_features", [])
        expected_special = ["Up to 3 reference images", "Reference image tagging"]
        
        for feature in expected_special:
            assert feature in special_features, f"❌ Special feature missing: {feature}"
        
        print("✅ Gen4 special features validated")
        
        # Test 5: Cost estimation for Gen4
        print("\n5️⃣ Testing Gen4 cost estimation...")
        cost_1_image = generator.estimate_cost("gen4", 1)
        cost_3_images = generator.estimate_cost("gen4", 3)
        
        assert cost_1_image == 0.08, f"❌ Expected $0.08, got ${cost_1_image}"
        assert cost_3_images == 0.24, f"❌ Expected $0.24, got ${cost_3_images}"
        print("✅ Gen4 cost estimation works")
        
        # Test 6: Model comparison includes Gen4
        print("\n6️⃣ Testing model comparison...")
        comparison = generator.compare_models()
        models = comparison.get("models", {})
        assert "gen4" in models, "❌ gen4 not in model comparison"
        print("✅ Gen4 appears in model comparison")
        
        print("\n🎉 Unified generator Gen4 tests passed!")
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
        
        # Test 1: Check gen4 in supported models
        assert "text_to_image" in SUPPORTED_MODELS, "❌ text_to_image not in SUPPORTED_MODELS"
        assert "gen4" in SUPPORTED_MODELS["text_to_image"], "❌ gen4 not in text_to_image models"
        print("✅ gen4 model added to supported models")
        
        # Test 2: Check cost estimates
        assert "text_to_image" in COST_ESTIMATES, "❌ text_to_image not in COST_ESTIMATES"
        assert "gen4" in COST_ESTIMATES["text_to_image"], "❌ gen4 not in cost estimates"
        assert COST_ESTIMATES["text_to_image"]["gen4"] == 0.08, "❌ Incorrect gen4 cost estimate"
        print("✅ gen4 cost estimates configured")
        
        # Test 3: Check model recommendations
        assert "text_to_image" in MODEL_RECOMMENDATIONS, "❌ text_to_image not in recommendations"
        recommendations = MODEL_RECOMMENDATIONS["text_to_image"]
        assert "cinematic" in recommendations, "❌ cinematic recommendation not found"
        assert recommendations["cinematic"] == "gen4", "❌ gen4 not recommended for cinematic"
        print("✅ gen4 model recommendations configured")
        
        print("✅ AI Pipeline integration complete")
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
    print("🎬 Runway Gen4 Integration Test Suite")
    print("=" * 70)
    print("⚠️ Note: This test does NOT make API calls (no costs incurred)")
    
    # Run tests
    tests = [
        ("Dependencies", test_dependencies),
        ("Runway Gen4 Generator", test_runway_gen4_generator),
        ("Unified Generator with Gen4", test_unified_generator_with_gen4),
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
        print("🎉 ALL TESTS PASSED! Runway Gen4 integration is ready!")
        print("\n📝 Key Features Validated:")
        print("  ✅ Multi-reference image support (up to 3 images)")
        print("  ✅ Reference image tagging system")
        print("  ✅ Multiple resolution options (720p/1080p)")
        print("  ✅ Cinematic quality generation")
        print("  ✅ Integrated with unified interface")
        print("  ✅ AI Pipeline constants updated")
        print("\n💰 Pricing: $0.05 (720p) / $0.08 (1080p) per image")
        print("⚠️  Note: Actual generation requires valid Replicate API token")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check output above for details.")
        sys.exit(1)