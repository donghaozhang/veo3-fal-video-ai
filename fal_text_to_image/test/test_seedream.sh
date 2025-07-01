#!/bin/bash
# Test FAL Text-to-Image Seedream v3 Model using CLI

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory for .env access
cd fal_text_to_image

echo "🧪 Testing Seedream v3 model via CLI..."
echo "⚠️  This will incur costs (~$0.01-0.02 per image)"

# Generate image with Seedream model using CLI (supports bilingual prompts)
python __main__.py generate -p "一条威严的中国龙在云雾中飞翔，传统水墨画风格 (A majestic Chinese dragon flying through clouds, traditional ink painting style)" -m seedream -o output --image-size 1024x1024 --guidance-scale 7.5 --num-inference-steps 20 --seed 42 --save-json seedream_result.json

echo "✅ Seedream v3 CLI test completed!"