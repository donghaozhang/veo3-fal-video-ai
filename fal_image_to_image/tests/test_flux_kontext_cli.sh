#!/bin/bash
# Test FLUX Kontext via CLI

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_image_to_image directory
cd fal_image_to_image

# Run the test
python -m fal_image_to_image modify -i input/flux_kontext_death_1751335665.png -p "Remove text and symbol at top left of image" -m kontext