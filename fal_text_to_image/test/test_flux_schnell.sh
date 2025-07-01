#!/bin/bash
# Test FAL Text-to-Image FLUX Schnell Model

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory
cd fal_text_to_image

# Generate image with FLUX Schnell model
python test/test_flux_schnell.py --yes