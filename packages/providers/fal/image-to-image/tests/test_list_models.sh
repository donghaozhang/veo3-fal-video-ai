#!/bin/bash
# List all available models

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_image_to_image directory
cd fal_image_to_image

# Run the test
python -m fal_image_to_image list-models