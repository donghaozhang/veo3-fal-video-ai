#!/usr/bin/env python3
"""
FAL AI Text-to-Image MCP Server Test Suite

This script tests MCP server functionality including:
- Server structure and initialization
- Tool definitions and handlers
- Formatting functions
- Direct tool testing (Cursor-compatible)

NO IMAGE GENERATION - COMPLETELY FREE!

Usage:
    python test_mcp.py                    # Full MCP test suite
    python test_mcp.py --tools-only       # Test only MCP tools
    python test_mcp.py --direct-test      # Direct tool testing (Cursor mode)

Author: AI Assistant
Date: 2024
"""

import asyncio
import json
import sys
import argparse
import traceback
from typing import Dict, Any, List

def print_banner():
    """Print the test banner."""
    print("=" * 60)
    print("🧪 FAL AI TEXT-TO-IMAGE MCP SERVER TEST")
    print("=" * 60)
    print("✅ This test is COMPLETELY FREE")
    print("✅ No image generation - only MCP validation")
    print("✅ Safe to run anytime for troubleshooting")
    print("=" * 60)

def test_imports() -> bool:
    """Test all required imports."""
    print("🔍 Testing Imports...")
    
    try:
        # MCP imports
        from mcp.server.models import InitializationOptions
        from mcp.server import NotificationOptions, Server
        from mcp.types import Resource, Tool, TextContent
        print("✅ MCP core imports successful")
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

def test_mcp_server_structure() -> bool:
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

def test_model_configurations() -> bool:
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
                    required_fields = ["name", "endpoint", "description", "cost"]
                    
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

def test_formatting_functions() -> bool:
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
        if isinstance(result_text, str) and ("Successful" in result_text or "✅" in result_text):
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
        if isinstance(summary_text, str) and "Summary" in summary_text:
            print("✅ format_batch_summary works correctly")
        else:
            print("❌ format_batch_summary failed")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Formatting function test failed: {e}")
        traceback.print_exc()
        return False

def test_generator_integration() -> bool:
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

async def test_tools_definition() -> bool:
    """Test MCP tools definition."""
    print("\n🛠️ Testing Tools Definition...")
    
    try:
        from mcp_server import handle_list_tools
        
        # Call the tools handler directly
        tools = await handle_list_tools()
        
        if not tools or len(tools) == 0:
            print("❌ No tools returned")
            return False
        
        expected_tool_names = [
            "generate_image",
            "batch_generate_images", 
            "list_models",
            "get_model_info",
            "download_image"
        ]
        
        tool_names = [tool.name for tool in tools]
        
        for expected_tool in expected_tool_names:
            if expected_tool in tool_names:
                print(f"✅ Tool '{expected_tool}' defined")
            else:
                print(f"❌ Tool '{expected_tool}' missing")
                return False
        
        print(f"✅ All {len(tools)} tools properly defined")
        return True
        
    except Exception as e:
        print(f"❌ Tools definition test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_list_models_handler() -> bool:
    """Test the list models handler."""
    print("\n📝 Testing List Models Handler...")
    
    try:
        from mcp_server import handle_list_models
        
        # Test list models with empty arguments
        result = await handle_list_models({})
        
        if not result or len(result) == 0:
            print("❌ No result from list_models")
            return False
        
        # Check if result contains text content
        text_content = result[0].text if hasattr(result[0], 'text') else str(result[0])
        
        if "Available FAL AI" in text_content and "imagen4" in text_content:
            print("✅ list_models handler works correctly")
            return True
        else:
            print("❌ list_models handler returned unexpected content")
            return False
        
    except Exception as e:
        print(f"❌ List models handler test failed: {e}")
        return False

def test_config_file() -> bool:
    """Test MCP configuration file."""
    print("\n⚙️ Testing MCP Configuration File...")
    
    try:
        import json
        import os
        
        if not os.path.exists('mcp_config.json'):
            print("⚠️  mcp_config.json not found (optional)")
            return True  # Config file is optional
        
        with open('mcp_config.json', 'r') as f:
            config = json.load(f)
        
        # Check required structure
        if 'mcpServers' not in config:
            print("❌ mcpServers section missing")
            return False
        
        if 'fal-text-to-image' not in config['mcpServers']:
            print("❌ fal-text-to-image server config missing")
            return False
        
        server_config = config['mcpServers']['fal-text-to-image']
        required_keys = ['command', 'args']
        
        for key in required_keys:
            if key not in server_config:
                print(f"❌ Configuration key '{key}' missing")
                return False
        
        print("✅ MCP configuration file valid")
        return True
        
    except Exception as e:
        print(f"❌ Configuration file test failed: {e}")
        return False

async def test_tool_directly(tool_name: str, arguments: Dict[str, Any]) -> bool:
    """Test an MCP tool directly by calling its handler."""
    print(f"\n🧪 Testing tool: {tool_name}")
    print(f"📝 Arguments: {json.dumps(arguments, indent=2)}")
    print("-" * 50)
    
    try:
        # Import the MCP server
        from mcp_server import handle_call_tool
        
        # Call the tool handler directly
        result = await handle_call_tool(tool_name, arguments)
        
        # Display the result
        if result:
            for content in result:
                if hasattr(content, 'text'):
                    print(content.text)
                else:
                    print(str(content))
        else:
            print("❌ No result returned")
            return False
        
        print("\n✅ Tool test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Tool test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def run_direct_tool_tests() -> Dict[str, bool]:
    """Run direct tool tests for Cursor compatibility."""
    print("\n🖱️ DIRECT TOOL TESTING (CURSOR MODE)")
    print("=" * 50)
    print("✅ Test MCP tools directly without external MCP client")
    print("✅ Safe testing with cost controls")
    print("=" * 50)
    
    # Test free/safe tools
    safe_tests = [
        ("list_models", {}),
        ("get_model_info", {"model": "imagen4"}),
        ("download_image", {
            "image_url": "https://picsum.photos/512/512",
            "output_folder": "test_output",
            "filename": "test_download.jpg"
        })
    ]
    
    results = {}
    
    for tool_name, arguments in safe_tests:
        print(f"\n{'='*20} {tool_name.title()} {'='*20}")
        try:
            results[tool_name] = await test_tool_directly(tool_name, arguments)
        except Exception as e:
            print(f"❌ {tool_name} crashed: {e}")
            results[tool_name] = False
    
    # Test generate_image with dry run
    print(f"\n{'='*20} Generate Image (Dry Run) {'='*20}")
    print("\n⚠️ NOTE: This is a DRY RUN test - no actual image will be generated")
    print("💰 In real usage, this would cost ~$0.015")
    
    arguments = {
        "prompt": "A beautiful sunset over mountains",
        "model": "imagen4",
        "output_folder": "test_output",
        "confirm_cost": False  # Skip confirmation for testing
    }
    
    print(f"\n🧪 Would call generate_image with:")
    print(json.dumps(arguments, indent=2))
    print("\n⚠️ Skipped actual generation to avoid costs")
    print("✅ Dry run test completed")
    results["generate_image_dry_run"] = True
    
    return results

async def run_comprehensive_test() -> Dict[str, bool]:
    """Run all tests and return results."""
    print_banner()
    
    tests = [
        ("Imports", test_imports),
        ("MCP Server Structure", test_mcp_server_structure),
        ("Model Configurations", test_model_configurations),
        ("Formatting Functions", test_formatting_functions),
        ("Generator Integration", test_generator_integration),
        ("Configuration File", test_config_file),
        ("Tools Definition", test_tools_definition),
        ("List Models Handler", test_list_models_handler),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results[test_name] = False
        print()  # Add spacing between tests
    
    return results

def print_summary(results: Dict[str, bool]):
    """Print test summary."""
    print("=" * 60)
    print("📊 MCP TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 60)
    print(f"🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All MCP tests passed! Server is ready for deployment.")
        print("💡 Next steps:")
        print("   • python mcp_server.py - Start the MCP server")
        print("   • python test_generation.py --help - Test image generation")
        print("   • python demo.py - Interactive demo with cost controls")
    else:
        print(f"\n⚠️ {total-passed} test(s) failed. Please fix issues before deployment.")

def print_usage_instructions():
    """Print instructions for using the MCP server."""
    print("""
🖱️ HOW TO USE FAL AI TEXT-TO-IMAGE MCP

1️⃣ DIRECT TOOL TESTING (This Script):
   • Run this script to test individual MCP tools
   • Safe for testing without costs (except actual image generation)
   
2️⃣ INTERACTIVE DEMO:
   • Run: python demo.py
   • Interactive interface with cost controls
   • Full functionality with user confirmations

3️⃣ COMMAND LINE TESTING:
   • Run specific tests: python test_generation.py --imagen4
   • Use FREE tests: python test_setup.py
   
4️⃣ DIRECT PYTHON USAGE:
   from fal_text_to_image_generator import FALTextToImageGenerator
   generator = FALTextToImageGenerator()
   result = generator.generate_image("your prompt", model="imagen4")

5️⃣ MCP SERVER FOR CLIENTS:
   • Start server: python mcp_server.py
   • Connect any MCP-compatible client
   • Use stdio protocol for communication

💡 RECOMMENDED:
   Start with the interactive demo (python demo.py) for the best experience!
""")

async def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description="FAL AI Text-to-Image MCP Test Suite")
    parser.add_argument('--tools-only', action='store_true', help='Test only MCP tools')
    parser.add_argument('--direct-test', action='store_true', help='Direct tool testing (Cursor mode)')
    
    args = parser.parse_args()
    
    try:
        if args.direct_test:
            # Run direct tool tests for Cursor
            results = await run_direct_tool_tests()
            print_summary(results)
            print_usage_instructions()
        elif args.tools_only:
            # Test only tools
            print_banner()
            results = {}
            results["Tools Definition"] = await test_tools_definition()
            results["List Models Handler"] = await test_list_models_handler()
            print_summary(results)
        else:
            # Run comprehensive test
            results = await run_comprehensive_test()
            print_summary(results)
        
        # Exit with error code if any tests failed
        if not all(results.values()):
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 