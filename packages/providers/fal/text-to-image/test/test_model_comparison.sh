#!/bin/bash
# Test FAL Text-to-Image Model Comparison (ALL MODELS) using CLI

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory for .env access
cd fal_text_to_image

echo "🧪 Testing all models comparison via CLI..."
echo "⚠️  This will incur costs (~$0.08 total for 4 models)"

# Compare all models with same prompt using CLI
python __main__.py compare -p "A majestic phoenix rising from flames, detailed fantasy art, vibrant colors" -o output --save-json comparison_results.json

echo "✅ Model comparison CLI test completed!"