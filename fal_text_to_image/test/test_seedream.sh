#!/bin/bash
# Test FAL Text-to-Image Seedream v3 Model

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory
cd fal_text_to_image

# Generate image with Seedream model (supports bilingual)
python test/test_seedream.py --yes