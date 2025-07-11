#!/usr/bin/env python3
"""
Test script for Veo3 Fast integration - NO API CALLS (cost-free)

This script validates that the Veo3 Fast model is properly integrated
without making actual API calls that would incur costs.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from fal_text_to_video_generator import FALTextToVideoGenerator, TextToVideoModel


def test_veo3_fast_integration():
    """Test Veo3 Fast integration without API calls."""
    print("🧪 Testing Veo3 Fast Integration (No API Calls)")
    print("=" * 60)
    
    try:
        # Test 1: Verify model is available
        print("\n1️⃣ Testing model availability...")
        assert hasattr(TextToVideoModel, 'GOOGLE_VEO3_FAST'), "❌ GOOGLE_VEO3_FAST model not found"
        assert TextToVideoModel.GOOGLE_VEO3_FAST.value == "fal-ai/veo3/fast", "❌ Incorrect endpoint"
        print("✅ Veo3 Fast model is available")
        
        # Test 2: Initialize generator (requires valid API key format)
        print("\n2️⃣ Testing generator initialization...")
        # Use fake but valid format API key for testing
        fake_api_key = "00000000-0000-0000-0000-000000000000:fakehashfortest123456789abcdef"
        generator = FALTextToVideoGenerator(api_key=fake_api_key, verbose=False)
        print("✅ Generator initialized successfully")
        
        # Test 3: Verify model configuration
        print("\n3️⃣ Testing model configuration...")
        model_info = generator.get_model_info(TextToVideoModel.GOOGLE_VEO3_FAST)
        expected_config = {
            "name": "Google Veo 3 Fast",
            "resolution": "720p",
            "cost_per_second_no_audio": 0.25,
            "cost_per_second_with_audio": 0.40
        }
        
        for key, expected_value in expected_config.items():
            assert model_info[key] == expected_value, f"❌ {key}: expected {expected_value}, got {model_info[key]}"
        
        print("✅ Model configuration is correct")
        
        # Test 4: Cost calculation
        print("\n4️⃣ Testing cost calculation...")
        cost_5s_no_audio = generator.calculate_cost(TextToVideoModel.GOOGLE_VEO3_FAST, "5s", False)
        cost_8s_with_audio = generator.calculate_cost(TextToVideoModel.GOOGLE_VEO3_FAST, "8s", True)
        
        assert cost_5s_no_audio == 1.25, f"❌ Expected $1.25, got ${cost_5s_no_audio}"
        assert cost_8s_with_audio == 3.20, f"❌ Expected $3.20, got ${cost_8s_with_audio}"
        print("✅ Cost calculation is correct")
        
        # Test 5: Model comparison
        print("\n5️⃣ Testing model comparison...")
        all_models = generator.get_model_info()
        assert 'GOOGLE_VEO3_FAST' in all_models['available_models'], "❌ Veo3 Fast not in model list"
        print("✅ Model appears in comparison")
        
        # Test 6: Cost estimates
        print("\n6️⃣ Testing cost estimates...")
        estimates = [
            generator.get_cost_estimate(TextToVideoModel.GOOGLE_VEO3_FAST, "5s", True),
            generator.get_cost_estimate(TextToVideoModel.GOOGLE_VEO3_FAST, "8s", False)
        ]
        assert all("Veo 3 Fast" in estimate for estimate in estimates), "❌ Cost estimates don't mention Veo3 Fast"
        print("✅ Cost estimates work correctly")
        
        print("\n🎉 All tests passed! Veo3 Fast is properly integrated.")
        print("\n📊 Summary:")
        print("  • Model endpoint: fal-ai/veo3/fast")
        print("  • Cost: $0.25/s (no audio), $0.40/s (with audio)")
        print("  • Features: 720p, 5-8s duration, faster generation")
        print("  • Integration: Complete ✅")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
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
        sys.path.append(str(Path(__file__).parent.parent.parent.parent / "core" / "ai_content_pipeline" / "ai_content_pipeline"))
        from config.constants import SUPPORTED_MODELS, COST_ESTIMATES, MODEL_RECOMMENDATIONS
        
        # Test model is in supported models
        assert "veo3_fast" in SUPPORTED_MODELS["image_to_video"], "❌ veo3_fast not in SUPPORTED_MODELS"
        print("✅ Model in SUPPORTED_MODELS")
        
        # Test cost estimate exists
        assert "veo3_fast" in COST_ESTIMATES["image_to_video"], "❌ veo3_fast cost not defined"
        assert COST_ESTIMATES["image_to_video"]["veo3_fast"] == 2.00, "❌ Incorrect cost estimate"
        print("✅ Cost estimate configured")
        
        # Test recommendation exists
        assert "balanced" in MODEL_RECOMMENDATIONS["image_to_video"], "❌ balanced recommendation missing"
        assert MODEL_RECOMMENDATIONS["image_to_video"]["balanced"] == "veo3_fast", "❌ veo3_fast not recommended for balanced"
        print("✅ Model recommendation configured")
        
        print("✅ AI Pipeline integration complete!")
        return True
        
    except ImportError as e:
        print(f"⚠️ Could not test pipeline integration: {e}")
        return False
    except AssertionError as e:
        print(f"❌ Pipeline integration failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Veo3 Fast Integration Test Suite")
    print("=" * 60)
    print("⚠️ Note: This test does NOT make API calls (no costs incurred)")
    
    # Run tests
    test1_passed = test_veo3_fast_integration()
    test2_passed = test_ai_pipeline_integration()
    
    # Summary
    print("\n" + "=" * 60)
    if test1_passed and test2_passed:
        print("🎉 ALL TESTS PASSED! Veo3 Fast is ready to use.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check output above.")
        sys.exit(1)