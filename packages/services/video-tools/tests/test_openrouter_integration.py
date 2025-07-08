"""
Test OpenRouter integration in video_tools.

Tests the OpenRouter analyzer functionality and CLI integration.
"""

import os
import sys
from pathlib import Path

# Add video_utils to path
sys.path.insert(0, str(Path(__file__).parent.parent / "video_utils"))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    print("💡 Note: python-dotenv not installed, using system environment variables")

from video_utils.openrouter_analyzer import check_openrouter_requirements, OpenRouterAnalyzer


def test_openrouter_requirements():
    """Test OpenRouter requirements checking."""
    print("🧪 Testing OpenRouter requirements...")
    
    ready, message = check_openrouter_requirements()
    
    if ready:
        print("✅ OpenRouter requirements met!")
        print(f"   Status: {message}")
        return True
    else:
        print("❌ OpenRouter requirements not met")
        print(f"   Reason: {message}")
        
        if "not installed" in message:
            print("💡 Install with: pip install openai")
        if "not set" in message:
            print("💡 Set API key: export OPENROUTER_API_KEY=your_api_key")
            print("🌐 Get API key: https://openrouter.ai/keys")
        
        return False


def test_openrouter_analyzer_init():
    """Test OpenRouter analyzer initialization."""
    print("\n🧪 Testing OpenRouter analyzer initialization...")
    
    ready, _ = check_openrouter_requirements()
    if not ready:
        print("⏭️ Skipping - requirements not met")
        return False
    
    try:
        # Test with different models
        models_to_test = [
            "google/gemini-2.0-flash-001",
            "google/gemini-pro-1.5",
            "anthropic/claude-3.5-sonnet"
        ]
        
        for model in models_to_test:
            print(f"   Testing model: {model}")
            analyzer = OpenRouterAnalyzer(model=model)
            print(f"   ✅ {model} initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Analyzer initialization failed: {e}")
        return False


def test_openrouter_commands_import():
    """Test importing OpenRouter commands."""
    print("\n🧪 Testing OpenRouter commands import...")
    
    try:
        from video_utils.openrouter_commands import (
            cmd_analyze_images_openrouter,
            cmd_openrouter_info,
            cmd_compare_providers
        )
        print("✅ OpenRouter commands imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Command import failed: {e}")
        return False


def test_cli_integration():
    """Test CLI integration."""
    print("\n🧪 Testing CLI integration...")
    
    try:
        from video_utils.command_dispatcher import CommandDispatcher
        
        # Create dispatcher
        dispatcher = CommandDispatcher(verbose=False)
        
        # Test that OpenRouter methods exist
        methods_to_check = [
            '_analyze_images_openrouter',
            '_compare_providers',
            '_openrouter_info'
        ]
        
        for method_name in methods_to_check:
            if hasattr(dispatcher, method_name):
                print(f"   ✅ Method {method_name} exists")
            else:
                print(f"   ❌ Method {method_name} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ CLI integration test failed: {e}")
        return False


def test_image_analysis_flow():
    """Test image analysis flow (dry run)."""
    print("\n🧪 Testing image analysis flow (dry run)...")
    
    ready, _ = check_openrouter_requirements()
    if not ready:
        print("⏭️ Skipping - OpenRouter not available")
        return False
    
    # Check for test images
    input_dir = Path("input")
    if not input_dir.exists():
        print("⏭️ Skipping - no input directory found")
        return False
    
    from video_utils.file_utils import find_image_files
    image_files = find_image_files(input_dir)
    
    if not image_files:
        print("⏭️ Skipping - no image files found")
        return False
    
    print(f"   Found {len(image_files)} image file(s)")
    
    try:
        # Test analyzer creation (don't actually analyze)
        analyzer = OpenRouterAnalyzer(model="google/gemini-2.0-flash-001")
        print("   ✅ Analyzer created successfully")
        
        # Test method availability
        methods_to_check = [
            'describe_image',
            'classify_image',
            'detect_objects',
            'extract_text_from_image',
            'analyze_image_composition',
            'answer_image_questions'
        ]
        
        for method in methods_to_check:
            if hasattr(analyzer, method):
                print(f"   ✅ Method {method} available")
            else:
                print(f"   ❌ Method {method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Image analysis flow test failed: {e}")
        return False


def main():
    """Run all OpenRouter integration tests."""
    print("🌐 OPENROUTER INTEGRATION TESTS")
    print("=" * 50)
    
    tests = [
        ("Requirements Check", test_openrouter_requirements),
        ("Analyzer Initialization", test_openrouter_analyzer_init),
        ("Commands Import", test_openrouter_commands_import),
        ("CLI Integration", test_cli_integration),
        ("Image Analysis Flow", test_image_analysis_flow)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"💥 {test_name} ERROR: {e}")
    
    print(f"\n📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! OpenRouter integration is working.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    # Show setup info if needed
    if passed < total:
        print("\n💡 Setup Instructions:")
        print("   1. Install OpenAI library: pip install openai")
        print("   2. Get OpenRouter API key: https://openrouter.ai/keys")
        print("   3. Set environment variable: export OPENROUTER_API_KEY=your_key")
        print("   4. Add image files to input/ directory for testing")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)