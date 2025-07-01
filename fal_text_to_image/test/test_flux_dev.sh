#!/bin/bash
# Test FAL Text-to-Image FLUX Dev Model using CLI

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory for .env access
cd fal_text_to_image

echo "🧪 Testing FLUX Dev model via CLI..."
echo "⚠️  This will incur costs (~$0.01-0.02 per image)"

# Generate image with FLUX Dev model using CLI (single line to avoid issues)
python __main__.py generate -p "A surreal landscape with floating islands and waterfalls in the sky, masterpiece quality, detailed 8K art" -m flux_dev -o output --image-size landscape_16_9 --guidance-scale 4.0 --num-inference-steps 28 --save-json flux_dev_result.json

echo "✅ FLUX Dev CLI test completed!"