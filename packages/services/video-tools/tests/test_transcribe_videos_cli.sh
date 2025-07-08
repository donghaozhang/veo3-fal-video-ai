#!/bin/bash
# Simple test for video_audio_utils.py transcribe-videos CLI - 4 usage examples
source ../../venv/bin/activate
cd ..
echo "Testing video_audio_utils.py transcribe-videos CLI with parameters..."
python3 video_audio_utils.py transcribe-videos -i input/sample_video.mp4 -o output/transcription1.json -f describe-video
python3 video_audio_utils.py transcribe-videos -i input/sample_video.mp4 -o output/transcription2.json
python3 video_audio_utils.py transcribe-videos -i input/ -o output/
python3 video_audio_utils.py transcribe-videos -i input/sample_video.mp4 -o output/transcription.txt -f txt
echo "Test completed. Check for output files."