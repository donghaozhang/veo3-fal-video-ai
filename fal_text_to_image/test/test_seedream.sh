#!/bin/bash
# Test FAL Text-to-Image Seedream v3 Model

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory
cd fal_text_to_image

# Run the Seedream test
python test/test_seedream.py --yes