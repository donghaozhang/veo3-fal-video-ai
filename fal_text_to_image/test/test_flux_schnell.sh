#!/bin/bash
# Test FAL Text-to-Image FLUX Schnell Model using CLI

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory for .env access
cd fal_text_to_image

echo "🧪 Testing FLUX Schnell model via CLI..."
echo "⚠️  This will incur costs (~$0.01-0.02 per image)"

# Generate image with FLUX Schnell model using CLI (optimized for speed)
python __main__.py generate -p "A cyberpunk cityscape at night with neon lights reflecting on wet streets, high detail, digital art" -m flux_schnell -o output --image-size landscape_4_3 --num-inference-steps 4 --save-json flux_schnell_result.json

echo "✅ FLUX Schnell CLI test completed!"