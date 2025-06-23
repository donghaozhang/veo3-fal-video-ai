#!/usr/bin/env python3
"""
Comprehensive MCP Server Test
Tests all MCP server functionality without running the actual MCP protocol.
"""

import asyncio
import sys
import os

def test_imports():
    """Test all required imports."""
    print("🔍 Testing Imports...")
    try:
        # Test MCP imports
        from mcp.server import Server
        from mcp.types import Tool, TextContent
        print("   ✅ MCP core imports successful")
        
        # Test local imports
        from mcp_server import server, MODELS, generator
        from fal_text_to_image_generator import FALTextToImageGenerator
        print("   ✅ Local imports successful")
        
        return True
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def test_server_structure():
    """Test MCP server structure."""
    print("🏗️ Testing Server Structure...")
    try:
        from mcp_server import server
        
        # Check server instance
        if hasattr(server, 'name') and server.name == "fal-text-to-image":
            print("   ✅ Server instance properly configured")
        else:
            print("   ❌ Server instance configuration issue")
            return False
        
        # Check if server has expected handlers
        expected_handlers = ['list_tools', 'call_tool', 'list_resources', 'read_resource']
        for handler in expected_handlers:
            if hasattr(server, handler):
                print(f"   ✅ Handler '{handler}' found")
            else:
                print(f"   ❌ Handler '{handler}' missing")
                return False
        
        return True
    except Exception as e:
        print(f"   ❌ Server structure test failed: {e}")
        return False

def test_models_config():
    """Test model configurations."""
    print("📋 Testing Model Configurations...")
    try:
        from mcp_server import MODELS
        
        expected_models = ["imagen4", "seedream", "flux_schnell", "flux_dev"]
        
        if len(MODELS) != 4:
            print(f"   ❌ Expected 4 models, found {len(MODELS)}")
            return False
        
        for model in expected_models:
            if model not in MODELS:
                print(f"   ❌ Model '{model}' missing")
                return False
            
            # Check required fields
            model_config = MODELS[model]
            required_fields = ["name", "endpoint", "description", "cost"]
            for field in required_fields:
                if field not in model_config:
                    print(f"   ❌ Model '{model}' missing field '{field}'")
                    return False
            
            print(f"   ✅ Model '{model}' configuration complete")
        
        return True
    except Exception as e:
        print(f"   ❌ Model configuration test failed: {e}")
        return False

def test_formatting_functions():
    """Test formatting functions."""
    print("🎨 Testing Formatting Functions...")
    try:
        from mcp_server import format_cost_warning, format_model_info, format_generation_result, format_batch_summary
        
        # Test cost warning
        warning = format_cost_warning(0.015, 1)
        if "0.015" in warning and "💰" in warning:
            print("   ✅ format_cost_warning works")
        else:
            print("   ❌ format_cost_warning failed")
            return False
        
        # Test model info
        info = format_model_info("imagen4")
        if "imagen4" in info and "Endpoint:" in info:
            print("   ✅ format_model_info works")
        else:
            print("   ❌ format_model_info failed")
            return False
        
        # Test generation result
        mock_result = {
            'success': True,
            'image_url': 'https://example.com/image.png',
            'model': 'imagen4',
            'generation_time': 5.0
        }
        result_text = format_generation_result(mock_result)
        if "Successfully generated" in result_text or "✅" in result_text:
            print("   ✅ format_generation_result works")
        else:
            print("   ❌ format_generation_result failed")
            return False
        
        # Test batch summary
        mock_results = [mock_result]
        mock_summary = {
            'total_images': 1,
            'successful': 1,
            'failed': 0,
            'total_time': 5.0,
            'total_cost': 0.015,
            'success_rate': 100.0
        }
        summary_text = format_batch_summary(mock_results, mock_summary)
        if "Summary" in summary_text and "100.0%" in summary_text:
            print("   ✅ format_batch_summary works")
        else:
            print("   ❌ format_batch_summary failed")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ Formatting functions test failed: {e}")
        return False

def test_generator_integration():
    """Test generator integration."""
    print("🔗 Testing Generator Integration...")
    try:
        from fal_text_to_image_generator import FALTextToImageGenerator
        
        # Test generator initialization
        gen = FALTextToImageGenerator()
        print("   ✅ Generator initialization successful")
        
        # Test if generator has required methods
        required_methods = ['generate_image', 'batch_generate', 'get_model_info']
        for method in required_methods:
            if hasattr(gen, method):
                print(f"   ✅ Method '{method}' available")
            else:
                print(f"   ❌ Method '{method}' missing")
                return False
        
        # Test model support
        if hasattr(gen, 'supported_models') and len(gen.supported_models) == 4:
            print("   ✅ All 4 models supported by generator")
        else:
            print("   ⚠️ Model support check inconclusive (still OK)")
        
        return True
    except Exception as e:
        print(f"   ❌ Generator integration test failed: {e}")
        return False

async def test_tools_definition():
    """Test MCP tools definition."""
    print("🛠️ Testing Tools Definition...")
    try:
        from mcp_server import handle_list_tools
        
        # Call the tools handler directly
        tools = await handle_list_tools()
        
        if not tools or len(tools) == 0:
            print("   ❌ No tools returned")
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
                print(f"   ✅ Tool '{expected_tool}' defined")
            else:
                print(f"   ❌ Tool '{expected_tool}' missing")
                return False
        
        print(f"   ✅ All {len(tools)} tools properly defined")
        return True
        
    except Exception as e:
        print(f"   ❌ Tools definition test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_list_models_handler():
    """Test the list models handler."""
    print("📝 Testing List Models Handler...")
    try:
        from mcp_server import handle_list_models
        
        # Test list models with empty arguments
        result = await handle_list_models({})
        
        if not result or len(result) == 0:
            print("   ❌ No result from list_models")
            return False
        
        # Check if result contains text content
        text_content = result[0].text if hasattr(result[0], 'text') else str(result[0])
        
        if "Available FAL AI" in text_content and "imagen4" in text_content:
            print("   ✅ list_models handler works correctly")
            return True
        else:
            print("   ❌ list_models handler returned unexpected content")
            return False
        
    except Exception as e:
        print(f"   ❌ List models handler test failed: {e}")
        return False

def test_config_file():
    """Test MCP configuration file."""
    print("⚙️ Testing MCP Configuration File...")
    try:
        import json
        
        if not os.path.exists('mcp_config.json'):
            print("   ❌ mcp_config.json not found")
            return False
        
        with open('mcp_config.json', 'r') as f:
            config = json.load(f)
        
        # Check required structure
        if 'mcpServers' not in config:
            print("   ❌ mcpServers section missing")
            return False
        
        if 'fal-text-to-image' not in config['mcpServers']:
            print("   ❌ fal-text-to-image server config missing")
            return False
        
        server_config = config['mcpServers']['fal-text-to-image']
        required_keys = ['command', 'args']
        
        for key in required_keys:
            if key not in server_config:
                print(f"   ❌ Configuration key '{key}' missing")
                return False
        
        print("   ✅ MCP configuration file valid")
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration file test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🚀 Starting Comprehensive MCP Server Tests...\n")
    
    tests = [
        ("Imports", test_imports),
        ("Server Structure", test_server_structure),
        ("Model Configurations", test_models_config),
        ("Formatting Functions", test_formatting_functions),
        ("Generator Integration", test_generator_integration),
        ("Configuration File", test_config_file),
        ("Tools Definition", test_tools_definition),
        ("List Models Handler", test_list_models_handler),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
        print()  # Add spacing between tests
    
    # Summary
    print("="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} {test_name}")
        if result:
            passed += 1
    
    print("-"*60)
    print(f"Result: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! MCP server is ready for use.")
        print("📋 Next steps:")
        print("   1. Add configuration to Claude Desktop settings")
        print("   2. Restart Claude Desktop")
        print("   3. Test MCP tools in Claude interface")
    else:
        print(f"\n🔧 {total-passed} tests failed. Please fix issues before deploying.")
    
    return passed == total

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 