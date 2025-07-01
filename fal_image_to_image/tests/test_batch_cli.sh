#!/bin/bash
# Test batch processing via CLI

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_image_to_image directory
cd fal_image_to_image

# Create a sample batch file
cat > test_batch.json << 'EOF'
[
  {
    "image_path": "input/death.jpeg",
    "model": "clarity",
    "scale": 2,
    "enable_enhancement": true,
    "prompt": "enhance details"
  },
  {
    "image_path": "input/death.jpeg", 
    "model": "photon",
    "prompt": "transform to anime style",
    "strength": 0.9,
    "aspect_ratio": "1:1"
  }
]
EOF

# Run batch processing
python -m fal_image_to_image batch -f test_batch.json --save-json batch_results.json

# Clean up
rm test_batch.json