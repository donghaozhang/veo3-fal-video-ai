#!/bin/bash
# Test FAL Text-to-Image FLUX Dev Model

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_text_to_image directory
cd fal_text_to_image

# Create test_flux_dev.py if it doesn't exist
if [ ! -f "test/test_flux_dev.py" ]; then
    echo "Creating test_flux_dev.py..."
    cp test/test_flux_schnell.py test/test_flux_dev.py
    sed -i 's/flux_schnell/flux_dev/g' test/test_flux_dev.py
    sed -i 's/FLUX Schnell/FLUX Dev/g' test/test_flux_dev.py
fi

# Generate image with FLUX Dev model
python test/test_flux_dev.py --yes