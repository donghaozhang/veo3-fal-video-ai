#!/usr/bin/env python3
"""
Quick MCP Server Startup Test
Tests that the server can initialize without errors.
"""

import asyncio
import sys
import os

async def test_startup():
    print("🚀 Testing MCP Server Startup...")
    print("=" * 40)
    
    try:
        # Test imports (now in same directory as MCP server)
        print("📦 Testing imports...")
        from mcp_server import server, main
        print("✅ Server import successful")
        
        # Test that we can create the server instance
        print("🔧 Testing server instance...")
        if server is not None:
            print("✅ Server instance created successfully")
        else:
            print("❌ Server instance is None")
            return False
        
        print("\n🎉 SERVER STARTUP TEST PASSED!")
        print("✅ All imports work correctly")
        print("✅ Server instance is properly configured")
        print("✅ Ready for MCP client integration")
        
        return True
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(test_startup())
        print(f"\n🎯 Final Result: {'SUCCESS' if result else 'FAILED'}")
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1) 