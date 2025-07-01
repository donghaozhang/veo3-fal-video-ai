#!/bin/bash
# Test FAL Text-to-Image Imagen 4 Model

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory
cd fal_text_to_image

# Generate image with Imagen 4 model
python test/test_imagen4.py --yes