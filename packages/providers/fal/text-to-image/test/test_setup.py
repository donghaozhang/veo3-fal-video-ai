#!/usr/bin/env python3
"""
FAL AI Text-to-Image Setup and API Test

This script tests ONLY the setup, environment, and API connection.
NO IMAGE GENERATION - COMPLETELY FREE!

This is the recommended first step for troubleshooting setup issues.

Usage:
    python test_setup.py

Author: AI Assistant  
Date: 2024
"""

import os
import sys
from typing import Dict, Any
import fal_client
from dotenv import load_dotenv

def print_banner():
    """Print the test banner."""
    print("=" * 60)
    print("🔧 FAL AI TEXT-TO-IMAGE SETUP TEST")
    print("=" * 60)
    print("✅ This test is COMPLETELY FREE")
    print("✅ No image generation - only setup validation")
    print("✅ Safe to run anytime for troubleshooting")
    print("=" * 60)

def test_environment_variables() -> bool:
    """Test environment variable setup."""
    print("\n🔍 Testing Environment Variables...")
    
    # Load environment variables from parent directory
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(parent_dir, ".env")
    load_dotenv(env_file)
    
    # Check .env file
    if os.path.exists(env_file):
        print(f"✅ Found {env_file} file")
    else:
        print(f"⚠️  No {env_file} file found")
        print("💡 Create a .env file with your FAL_KEY")
    
    # Check FAL_KEY
    fal_key = os.getenv('FAL_KEY')
    if fal_key:
        print("✅ FAL_KEY found in environment")
        # Mask the key for security
        if len(fal_key) > 12:
            masked_key = f"{fal_key[:8]}...{fal_key[-4:]}"
        else:
            masked_key = f"{fal_key[:4]}..."
        print(f"🔑 API Key: {masked_key}")
        return True
    else:
        print("❌ FAL_KEY not found in environment")
        print("💡 Set FAL_KEY in your .env file or environment variables")
        return False

def test_dependencies() -> bool:
    """Test all required dependencies."""
    print("\n📋 Testing Dependencies...")
    
    dependencies = [
        ('fal_client', 'fal-client'),
        ('requests', 'requests'),
        ('dotenv', 'python-dotenv'),
        ('typing_extensions', 'typing-extensions'),
        ('mcp', 'mcp')
    ]
    
    all_good = True
    
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {package_name}: Available")
        except ImportError:
            print(f"❌ {package_name}: Missing")
            print(f"💡 Install with: pip install {package_name}")
            all_good = False
    
    return all_good

def test_generator_initialization() -> bool:
    """Test text-to-image generator initialization."""
    print("\n🎨 Testing Generator Initialization...")
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from fal_text_to_image_generator import FALTextToImageGenerator
        print("✅ FALTextToImageGenerator imported successfully")
        
        # Try to initialize (this should not make any API calls)
        generator = FALTextToImageGenerator()
        print("✅ Generator initialized successfully")
        
        # Test model information (local operation)
        model_info = generator.get_model_info()
        print(f"✅ Found {len(model_info)} supported models:")
        
        for model_key, info in model_info.items():
            print(f"   • {info['name']} ({model_key})")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import generator: {e}")
        print("💡 Make sure fal_text_to_image_generator.py is in the same directory")
        return False
    except Exception as e:
        print(f"❌ Generator initialization failed: {e}")
        return False

def test_model_endpoints() -> bool:
    """Test model endpoint configuration."""
    print("\n🔗 Testing Model Endpoints...")
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from fal_text_to_image_generator import FALTextToImageGenerator
        
        generator = FALTextToImageGenerator()
        endpoints = generator.MODEL_ENDPOINTS
        
        print(f"✅ Found {len(endpoints)} model endpoints:")
        for model, endpoint in endpoints.items():
            print(f"   • {model}: {endpoint}")
        
        # Test model validation
        for model in endpoints.keys():
            try:
                validated_endpoint = generator.validate_model(model)
                print(f"✅ {model} validation: OK")
            except Exception as e:
                print(f"❌ {model} validation failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Model endpoint test failed: {e}")
        return False

def test_output_directories() -> bool:
    """Test output directory creation."""
    print("\n📁 Testing Output Directories...")
    
    try:
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        directories = ["output", "input"]
        
        for dir_name in directories:
            full_path = os.path.join(parent_dir, dir_name)
            os.makedirs(full_path, exist_ok=True)
            
            if os.path.exists(full_path) and os.path.isdir(full_path):
                print(f"✅ Directory '{dir_name}' ready")
            else:
                print(f"❌ Could not create directory '{dir_name}'")
                return False
        
        return True
            
    except Exception as e:
        print(f"❌ Output directory test failed: {e}")
        return False

def test_mcp_server_availability() -> bool:
    """Test if MCP server components are available."""
    print("\n🔧 Testing MCP Server Availability...")
    
    try:
        # Test MCP server import
        import mcp_server
        print("✅ MCP server module available")
        
        # Test if server has required components
        if hasattr(mcp_server, 'server'):
            print("✅ MCP server instance found")
        else:
            print("⚠️  MCP server instance not found (optional)")
        
        # Test formatting functions
        required_functions = [
            'format_cost_warning',
            'format_model_info', 
            'format_generation_result',
            'format_batch_summary'
        ]
        
        for func_name in required_functions:
            if hasattr(mcp_server, func_name):
                print(f"✅ Function {func_name} available")
            else:
                print(f"⚠️  Function {func_name} not found (optional)")
        
        return True
        
    except ImportError:
        print("⚠️  MCP server not available (optional)")
        return True  # MCP is optional
    except Exception as e:
        print(f"⚠️  MCP server test failed: {e} (optional)")
        return True  # MCP is optional

def run_comprehensive_test() -> Dict[str, bool]:
    """Run all tests and return results."""
    print_banner()
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Dependencies", test_dependencies),
        ("Generator Initialization", test_generator_initialization),
        ("Model Endpoints", test_model_endpoints),
        ("Output Directories", test_output_directories),
        ("MCP Server Availability", test_mcp_server_availability)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    return results

def print_summary(results: Dict[str, bool]):
    """Print test summary."""
    print("\n" + "=" * 50)
    print("📊 SETUP TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print("-" * 50)
    print(f"🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All setup tests passed! Your environment is ready.")
        print("💡 Next steps:")
        print("   • python test_mcp.py - Test MCP server functionality")
        print("   • python test_generation.py --help - See image generation options")
        print("   • python demo.py - Interactive demo with cost controls")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("💡 Common fixes:")
        print("   • Add FAL_KEY to .env file")
        print("   • Install missing dependencies: pip install -r requirements.txt")
        print("   • Check file permissions")

def main():
    """Main test function."""
    try:
        results = run_comprehensive_test()
        print_summary(results)
        
        # Exit with error code if any critical tests failed
        critical_tests = ["Environment Variables", "Dependencies", "Generator Initialization"]
        critical_passed = all(results.get(test, False) for test in critical_tests)
        
        if not critical_passed:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 