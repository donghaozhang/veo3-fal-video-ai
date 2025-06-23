#!/usr/bin/env python3
"""
MCP Dragon Generation Test
Uses MCP server tools to generate a dragon image
"""

import asyncio
import json
from mcp_server import app

async def test_mcp_dragon_generation():
    """Test MCP generate_image tool with dragon prompt"""
    
    print("🐲 MCP Dragon Image Generation")
    print("=" * 50)
    print("🔧 Using MCP generate_image tool")
    print("⚠️ Cost Warning: This will cost approximately $0.015")
    print("🎨 Model: FLUX Schnell (fast generation)")
    print()
    
    # Prepare MCP tool call arguments
    dragon_prompt = (
        "A majestic dragon with red scales, breathing fire, "
        "fantasy art style, detailed and epic, cinematic lighting, "
        "digital art masterpiece, 4k resolution"
    )
    
    # MCP tool call arguments
    mcp_args = {
        "prompt": dragon_prompt,
        "model": "flux_schnell",
        "negative_prompt": "blurry, low quality, distorted, ugly",
        "num_inference_steps": 4,
        "seed": None,
        "image_size": "square_hd",
        "num_images": 1,
        "enable_safety_checker": True,
        "sync_mode": True,
        "output_format": "png"
    }
    
    print(f"🎯 Prompt: {dragon_prompt}")
    print(f"🚫 Negative: {mcp_args['negative_prompt']}")
    print(f"⚡ Steps: {mcp_args['num_inference_steps']}")
    print()
    
    try:
        # Get the MCP server's generate_image handler
        from mcp_server import handle_generate_image
        
        print("🚀 Calling MCP generate_image tool...")
        
        # Call the MCP tool handler
        result = await handle_generate_image(mcp_args)
        
        print("✅ MCP call completed!")
        print()
        
        # Parse the result
        if isinstance(result, str):
            # If result is a string, parse it
            print("📄 MCP Response:")
            print(result)
        else:
            # If result is a dict, format it nicely
            print("📊 Generation Result:")
            if result.get('success'):
                print(f"✅ Status: Success")
                print(f"🔗 Image URL: {result.get('image_url', 'Not provided')}")
                print(f"📁 Local Path: {result.get('local_path', 'Not saved locally')}")
                print(f"⏱️ Time: {result.get('generation_time', 'Unknown')} seconds")
                print(f"💰 Cost: ${result.get('cost_estimate', 0.015):.3f}")
            else:
                print(f"❌ Status: Failed")
                print(f"🚨 Error: {result.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"❌ MCP call failed: {str(e)}")
        print("💡 Make sure the MCP server is running correctly")
        return False
    
    print()
    print("🎉 MCP dragon generation test completed!")
    return True

if __name__ == "__main__":
    asyncio.run(test_mcp_dragon_generation()) 