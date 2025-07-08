#!/bin/bash
# Comprehensive CLI test for all models

echo "🧪 FAL Image-to-Image CLI Test Suite"
echo "===================================="

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_image_to_image directory
cd fal_image_to_image

# Test 1: List models
echo -e "\n📋 Test 1: List all models"
python -m fal_image_to_image list-models

# Test 2: Clarity Upscaler
echo -e "\n📷 Test 2: Clarity Upscaler (2x)"
python -m fal_image_to_image modify \
    -i input/death.jpeg \
    -m clarity \
    --scale 2 \
    --save-json output/clarity_result.json

# Test 3: Photon Flash
echo -e "\n🎨 Test 3: Photon Flash"
python -m fal_image_to_image modify \
    -i input/death.jpeg \
    -p "transform into retro 80s style with neon colors" \
    -m photon \
    --strength 0.8 \
    --aspect-ratio "1:1"

# Test 4: FLUX Kontext (if processed image exists)
if [ -f "input/flux_kontext_death_1751335665.png" ]; then
    echo -e "\n🔧 Test 4: FLUX Kontext"
    python -m fal_image_to_image modify \
        -i input/flux_kontext_death_1751335665.png \
        -p "Remove all text and symbols" \
        -m kontext
else
    echo -e "\n⚠️  Test 4: Skipping FLUX Kontext (input file not found)"
fi

# Test 5: SeedEdit v3
echo -e "\n✏️  Test 5: SeedEdit v3"
python -m fal_image_to_image modify \
    -i input/death.jpeg \
    -p "change background to a sunny beach" \
    -m seededit \
    --guidance-scale 0.5

echo -e "\n✅ All tests completed!"
echo "📁 Check the output/ directory for results"