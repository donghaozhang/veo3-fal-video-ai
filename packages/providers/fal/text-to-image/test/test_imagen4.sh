#!/bin/bash
# Test FAL Text-to-Image Imagen 4 Model using CLI

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory for .env access
cd fal_text_to_image

echo "🧪 Testing Imagen 4 model via CLI..."
echo "⚠️  This will incur costs (~$0.015 per image)"

# Generate image with Imagen 4 model using CLI
python __main__.py generate -p "A majestic dragon soaring through cloudy skies, detailed digital art, fantasy style" -m imagen4 -o output --image-size landscape_4_3 --guidance-scale 3.0 --num-inference-steps 4 --save-json imagen4_result.json

echo "✅ Imagen 4 CLI test completed!"