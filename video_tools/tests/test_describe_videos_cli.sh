#!/bin/bash
# Simple test for video_audio_utils.py CLI - 4 usage examples

# Activate virtual environment
source ../../venv/bin/activate

# Navigate to video_tools directory for .env access
cd ..

echo "Testing video_audio_utils.py CLI..."
python3 video_audio_utils.py describe-videos -i input/sample_video.mp4 -o output/output1.json -f describe-video
python3 video_audio_utils.py describe-videos -i input/sample_video.mp4 -o output/output2.json
python3 video_audio_utils.py describe-videos -i input/ -o output/
python3 video_audio_utils.py describe-videos -i input/sample_video.mp4 -o output/result.txt -f txt
echo "Test completed. Check for output files."