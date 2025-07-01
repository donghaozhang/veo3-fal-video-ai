#!/bin/bash
# Simple test for video_audio_utils.py analyze-videos CLI - 4 usage examples

# Activate virtual environment
source ../../venv/bin/activate

# Navigate to video_tools directory for .env access
cd ..

echo "Testing video_audio_utils.py analyze-videos CLI..."
python3 video_audio_utils.py analyze-videos -i input/sample_video.mp4 -o output/analysis1.json -f describe-video
python3 video_audio_utils.py analyze-videos -i input/sample_video.mp4 -o output/analysis2.json
python3 video_audio_utils.py analyze-videos -i input/ -o output/
python3 video_audio_utils.py analyze-videos -i input/sample_video.mp4 -o output/analysis.txt -f txt
echo "Test completed. Check for output files."