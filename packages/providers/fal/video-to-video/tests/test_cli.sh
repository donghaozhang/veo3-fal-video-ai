#!/bin/bash
# Test FAL Video to Video CLI interface

# Navigate to project root
cd /home/zdhpe/veo3-video-generation

# Activate virtual environment
source venv/bin/activate

# Navigate to fal_video_to_video directory
cd fal_video_to_video

echo "🎵 Test 1: List available models"
echo "================================="
python -m fal_video_to_video list-models

echo -e "\n\n🎵 Test 2: Add audio to sample video (if available)"
echo "=================================================="
if [ -f "input/sample.mp4" ]; then
    echo "Found sample video, processing..."
    python -m fal_video_to_video add-audio -i input/sample.mp4 -p "add dramatic music and sound effects" -m thinksound
else
    echo "No sample video found in input/sample.mp4"
    echo "To test with a real video, add a video file to input/ and run:"
    echo "python -m fal_video_to_video add-audio -i input/your_video.mp4 -p \"your prompt\""
fi

echo -e "\n\n🎵 Test 3: Test with URL (example)"
echo "=================================="
echo "Example command (commented out to avoid costs):"
echo "# python -m fal_video_to_video add-audio -u \"https://example.com/video.mp4\" -p \"add background music\""

echo -e "\n\n✅ CLI tests completed!"
echo "Note: Actual generation tests require valid video files and will incur API costs"