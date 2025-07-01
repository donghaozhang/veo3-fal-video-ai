#!/bin/bash
# Test FAL Text-to-Image Model Comparison (ALL MODELS)

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory
cd fal_text_to_image

# Run the model comparison test
python test/test_model_comparison.py --yes