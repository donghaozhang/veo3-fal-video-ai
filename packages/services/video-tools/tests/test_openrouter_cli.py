#!/usr/bin/env python3
"""
Quick CLI test for OpenRouter integration.

Tests OpenRouter info command and basic functionality.
"""

import sys
from pathlib import Path

# Add video_utils to path
sys.path.insert(0, str(Path(__file__).parent / "video_utils"))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from video_utils.openrouter_commands import cmd_openrouter_info, check_openrouter_requirements
from video_utils.openrouter_analyzer import OpenRouterAnalyzer


def test_openrouter_info():
    """Test OpenRouter info command."""
    print("🧪 Testing OpenRouter Info Command")
    print("-" * 40)
    
    try:
        cmd_openrouter_info()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_openrouter_analyzer():
    """Test OpenRouter analyzer basic functionality."""
    print("\n🧪 Testing OpenRouter Analyzer")
    print("-" * 40)
    
    # Check requirements
    ready, message = check_openrouter_requirements()
    if not ready:
        print(f"❌ Requirements not met: {message}")
        return False
    
    print(f"✅ Requirements met: {message}")
    
    # Test analyzer creation
    try:
        analyzer = OpenRouterAnalyzer(model="google/gemini-2.0-flash-001")
        print("✅ Analyzer created successfully")
        
        # Check available methods
        methods = [
            'describe_image',
            'classify_image', 
            'detect_objects',
            'extract_text_from_image',
            'analyze_image_composition',
            'answer_image_questions'
        ]
        
        print("\n📋 Available methods:")
        for method in methods:
            if hasattr(analyzer, method):
                print(f"   ✅ {method}")
            else:
                print(f"   ❌ {method} (missing)")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Analyzer test failed: {e}")
        return False


def main():
    """Run all CLI tests."""
    print("🌐 OPENROUTER CLI TESTS")
    print("=" * 50)
    
    tests = [
        ("OpenRouter Info", test_openrouter_info),
        ("OpenRouter Analyzer", test_openrouter_analyzer)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
            print(f"\n✅ {test_name} PASSED")
        else:
            print(f"\n❌ {test_name} FAILED")
    
    print(f"\n📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All CLI tests passed! OpenRouter is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)