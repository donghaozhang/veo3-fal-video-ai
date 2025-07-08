#!/bin/bash
# Test Photon Flash via CLI with auto-centering feature

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_image_to_image directory
cd fal_image_to_image

# echo "🎨 Test 1: Basic Photon modification"
# echo "=================================="
# python -m fal_image_to_image modify -i input/death.jpeg -p "transform into cyberpunk style with neon lights" -m photon --strength 0.8

echo -e "\n\n🎨 Test 2: Auto-center anime_girl.jpeg to 16:9 aspect ratio"
echo "========================================================="
echo "Input image: 1076x1076 (square)"
echo "Output aspect: 16:9 (landscape)"
echo "Expected: Image will be centered with vertical cropping"
python -m fal_image_to_image modify -i input/anime_girl.jpeg -p "enhance colors and make it more vibrant" -m photon --aspect-ratio "16:9" --auto-center --input-width 1076 --input-height 1076 --strength 0.7

# echo -e "\n\n🎨 Test 3: Auto-center to 9:16 aspect ratio (portrait)"
# echo "===================================================="
# echo "Input image: 1076x1076 (square)"
# echo "Output aspect: 9:16 (portrait)"
# echo "Expected: Image will be centered with horizontal cropping"
# python -m fal_image_to_image modify -i input/anime_girl.jpeg -p "apply artistic style" -m photon --aspect-ratio "9:16" --auto-center --input-width 1076 --input-height 1076 --strength 0.5

# echo -e "\n\n🎨 Test 4: Manual reframing with specific coordinates"
# echo "==================================================="
# echo "Manually crop center region (200,200) to (876,876)"
# python -m fal_image_to_image modify -i input/anime_girl.jpeg -p "transform into oil painting style" -m photon --x-start 200 --y-start 200 --x-end 876 --y-end 876 --aspect-ratio "1:1" --strength 0.8

# echo -e "\n\n🎨 Test 5: Auto-center without dimensions (should skip auto-center)"
# echo "================================================================"
# echo "Testing auto-center flag without input dimensions"
# python -m fal_image_to_image modify -i input/anime_girl.jpeg -p "make it look vintage" -m photon --aspect-ratio "21:9" --auto-center --strength 0.6

echo -e "\n\n✅ All tests completed!"
echo "Check the output directory for generated images"