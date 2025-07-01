#!/bin/bash
# Comprehensive FAL Text-to-Image Test Suite

echo "🧪 FAL Text-to-Image Comprehensive Test Suite"
echo "============================================="

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory
cd fal_text_to_image

# Test 1: Setup (FREE)
echo -e "\n📋 Test 1: Setup Validation (FREE)"
python test/test_setup_new.py

# Test 2: Individual Models (PAID)
echo -e "\n🎨 Test 2: Individual Model Tests"

echo -e "\n   Testing Imagen 4..."
python test/test_imagen4.py --yes

echo -e "\n   Testing FLUX Schnell..."
python test/test_flux_schnell.py --yes

echo -e "\n   Testing Seedream v3..."
python test/test_seedream.py --yes

# Test 3: Model Comparison (PAID)
echo -e "\n🆚 Test 3: Model Comparison"
python test/test_model_comparison.py --yes

echo -e "\n✅ All tests completed!"
echo "📁 Check the output/ directory for generated images"