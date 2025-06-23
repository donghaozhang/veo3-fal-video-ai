#!/usr/bin/env python3
"""
Script to help update Cursor MCP configuration for FAL AI Text-to-Image
"""

import json
import os
from pathlib import Path

def main():
    print("🔧 CURSOR MCP CONFIGURATION UPDATER")
    print("=" * 50)
    
    # MCP config path
    mcp_config_path = Path("c:/Users/zdhpe/.cursor/mcp.json")
    
    print(f"📁 MCP Config Location: {mcp_config_path}")
    
    if not mcp_config_path.exists():
        print("❌ MCP config file not found!")
        return
    
    # Read current config
    try:
        with open(mcp_config_path, 'r') as f:
            config = json.load(f)
        print("✅ Current MCP config loaded")
    except Exception as e:
        print(f"❌ Error reading MCP config: {e}")
        return
    
    # FAL AI configuration
    fal_config = {
        "command": "python",
        "args": [
            "D:\\AI_play\\AI_Code\\veo3\\fal_text_to_image\\mcp_server.py"
        ],
        "env": {
            "FAL_KEY": "be79b36b-d802-435d-9637-f0a0d717f08b:855e8483913d73412b16dc00593d8f1d"
        }
    }
    
    # Check if already exists
    if "fal-text-to-image" in config.get("mcpServers", {}):
        print("⚠️ FAL text-to-image server already exists in config")
        print("🔄 Updating existing configuration...")
    else:
        print("➕ Adding new FAL text-to-image server to config...")
    
    # Add/update the configuration
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    config["mcpServers"]["fal-text-to-image"] = fal_config
    
    # Create backup
    backup_path = mcp_config_path.with_suffix('.json.backup')
    try:
        with open(backup_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"💾 Backup created: {backup_path}")
    except Exception as e:
        print(f"⚠️ Could not create backup: {e}")
    
    # Print the configuration to add
    print("\n📋 CONFIGURATION TO ADD:")
    print("=" * 30)
    print('"fal-text-to-image": {')
    print('  "command": "python",')
    print('  "args": [')
    print('    "D:\\\\AI_play\\\\AI_Code\\\\veo3\\\\fal_text_to_image\\\\mcp_server.py"')
    print('  ],')
    print('  "env": {')
    print('    "FAL_KEY": "be79b36b-d802-435d-9637-f0a0d717f08b:855e8483913d73412b16dc00593d8f1d"')
    print('  }')
    print('}')
    
    print("\n🎯 NEXT STEPS:")
    print("1. Add the above configuration to your mcp.json file")
    print("2. Save the file")
    print("3. Restart Cursor completely")
    print("4. The FAL text-to-image tools should appear in MCP tools")
    
    print("\n⚠️ IMPORTANT:")
    print("• Each image generation costs ~$0.015")
    print("• Test with cost-conscious prompts")
    print("• Use batch generation carefully")
    
    print("\n🧪 ALTERNATIVE TESTING:")
    print("• python demo.py - Interactive demo with cost controls")
    print("• python test_cursor_mcp.py - Direct tool testing")

if __name__ == "__main__":
    main() 