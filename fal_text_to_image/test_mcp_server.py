#!/usr/bin/env python3
"""
Test script for FAL AI Text-to-Image MCP Server

This script validates the MCP server structure and functionality without 
actually running the server or generating images.

Features:
- Validates MCP server structure
- Tests tool definitions
- Checks import dependencies
- Validates model configurations
- Tests formatting functions
"""

import sys
import traceback
from typing import Dict, Any

def test_imports():
    """Test all required imports."""
    print("🔍 Testing Imports...")
    
    try:
        # MCP imports
        from mcp.server.models import InitializationOptions
        from mcp.server import NotificationOptions, Server
        from mcp.types import Resource, Tool, TextContent
        print("✅ MCP imports successful")
    except ImportError as e:
        print(f"❌ MCP import failed: {e}")
        return False
    
    try:
        # Local imports
        from fal_text_to_image_generator import FALTextToImageGenerator
        print("✅ FAL generator import successful")
    except ImportError as e:
        print(f"❌ FAL generator import failed: {e}")
        return False
    
    try:
        # Standard library imports
        import asyncio
        import json
        import logging
        import os
        from pathlib import Path
        print("✅ Standard library imports successful")
    except ImportError as e:
        print(f"❌ Standard library import failed: {e}")
        return False
    
    return True

def test_mcp_server_structure():
    """Test MCP server structure and initialization."""
    print("\n🏗️ Testing MCP Server Structure...")
    
    try:
        # Import the server module
        import mcp_server
        
        # Check if server is initialized
        if hasattr(mcp_server, 'server'):
            print("✅ MCP server instance found")
        else:
            print("❌ MCP server instance not found")
            return False
        
        # Check if required functions exist
        required_functions = [
            'format_cost_warning',
            'format_model_info', 
            'format_generation_result',
            'format_batch_summary'
        ]
        
        for func_name in required_functions:
            if hasattr(mcp_server, func_name):
                print(f"✅ Function {func_name} found")
            else:
                print(f"❌ Function {func_name} not found")
                return False
        
        return True
    
    except Exception as e:
        print(f"❌ MCP server structure test failed: {e}")
        return False

def test_model_configurations():
    """Test model configurations."""
    print("\n📋 Testing Model Configurations...")
    
    try:
        import mcp_server
        
        # Check if MODELS dictionary exists
        if hasattr(mcp_server, 'MODELS'):
            models = mcp_server.MODELS
            print(f"✅ Found {len(models)} model configurations")
            
            expected_models = ["imagen4", "seedream", "flux_schnell", "flux_dev"]
            for model_key in expected_models:
                if model_key in models:
                    model = models[model_key]
                    required_fields = ["name", "endpoint", "description", "cost", "best_for"]
                    
                    all_fields_present = all(field in model for field in required_fields)
                    if all_fields_present:
                        print(f"✅ Model {model_key}: Complete configuration")
                    else:
                        missing_fields = [field for field in required_fields if field not in model]
                        print(f"❌ Model {model_key}: Missing fields: {missing_fields}")
                        return False
                else:
                    print(f"❌ Model {model_key} not found")
                    return False
        else:
            print("❌ MODELS dictionary not found")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Model configuration test failed: {e}")
        return False

def test_formatting_functions():
    """Test formatting functions."""
    print("\n🎨 Testing Formatting Functions...")
    
    try:
        import mcp_server
        
        # Test cost warning formatting
        cost_warning = mcp_server.format_cost_warning(0.015, 1)
        if isinstance(cost_warning, str) and "$0.015" in cost_warning:
            print("✅ format_cost_warning works correctly")
        else:
            print("❌ format_cost_warning failed")
            return False
        
        # Test model info formatting
        model_info = mcp_server.format_model_info("imagen4")
        if isinstance(model_info, str) and "Imagen4" in model_info:
            print("✅ format_model_info works correctly")
        else:
            print("❌ format_model_info failed")
            return False
        
        # Test generation result formatting
        test_result = {
            'success': True,
            'model': 'imagen4',
            'generation_time': 6.42,
            'cost_estimate': 0.015,
            'image_url': 'https://example.com/image.png',
            'local_path': 'output/test.png'
        }
        result_text = mcp_server.format_generation_result(test_result)
        if isinstance(result_text, str) and "Successful" in result_text:
            print("✅ format_generation_result works correctly")
        else:
            print("❌ format_generation_result failed")
            return False
        
        # Test batch summary formatting
        test_results = [
            {'model': 'imagen4', 'success': True, 'generation_time': 6.42},
            {'model': 'flux_dev', 'success': True, 'generation_time': 2.18}
        ]
        test_summary = {
            'total_images': 2,
            'successful': 2,
            'failed': 0,
            'total_time': 8.60,
            'total_cost': 0.030,
            'success_rate': 100.0
        }
        summary_text = mcp_server.format_batch_summary(test_results, test_summary)
        if isinstance(summary_text, str) and "Batch Generation Summary" in summary_text:
            print("✅ format_batch_summary works correctly")
        else:
            print("❌ format_batch_summary failed")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Formatting function test failed: {e}")
        traceback.print_exc()
        return False

def test_generator_integration():
    """Test generator integration."""
    print("\n🔗 Testing Generator Integration...")
    
    try:
        from fal_text_to_image_generator import FALTextToImageGenerator
        
        # Test generator initialization
        generator = FALTextToImageGenerator()
        print("✅ Generator initialization successful")
        
        # Test generator methods exist
        required_methods = [
            'generate_image',
            'batch_generate',
            'get_model_info',
            'download_image'
        ]
        
        for method_name in required_methods:
            if hasattr(generator, method_name):
                print(f"✅ Method {method_name} found")
            else:
                print(f"❌ Method {method_name} not found")
                return False
        
        return True
    
    except Exception as e:
        print(f"❌ Generator integration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 FAL AI TEXT-TO-IMAGE MCP SERVER VALIDATION")
    print("=" * 60)
    print("✅ This test is COMPLETELY FREE")
    print("✅ No image generation - only structure validation")
    print("✅ Safe to run anytime for troubleshooting")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("MCP Server Structure", test_mcp_server_structure),
        ("Model Configurations", test_model_configurations),
        ("Formatting Functions", test_formatting_functions),
        ("Generator Integration", test_generator_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_function in tests:
        try:
            if test_function():
                passed += 1
            else:
                print(f"\n❌ {test_name} test failed")
        except Exception as e:
            print(f"\n❌ {test_name} test failed with exception: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if i < passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 50)
    success_rate = (passed / total) * 100
    print(f"🎯 Overall: {passed}/{total} tests passed ({success_rate:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! MCP server is ready for deployment.")
        print("💡 Next steps:")
        print("   1. Configure MCP client (Claude Desktop, etc.)")
        print("   2. Test with actual MCP client")
        print("   3. Use cost-conscious generation tools")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please fix issues before deployment.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
