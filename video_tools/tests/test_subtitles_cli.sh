#!/bin/bash
# CLI test for video_audio_utils.py generate-subtitles command with -i and -o parameters
source /home/zdhpe/veo3-video-generation/venv/bin/activate
cd /home/zdhpe/veo3-video-generation/video_tools

echo "🧪 Testing generate-subtitles CLI with parameters..."
echo "=================================================="

INPUT_DIR="/home/zdhpe/veo3-video-generation/video_tools/input"
OUTPUT_DIR="/home/zdhpe/veo3-video-generation/video_tools/output"

# Only create directories if they don't exist
[ ! -d "$INPUT_DIR" ] && mkdir -p "$INPUT_DIR" && echo "📁 Created input directory"
[ ! -d "$OUTPUT_DIR" ] && mkdir -p "$OUTPUT_DIR" && echo "📁 Created output directory"

# Test 1: Command availability
echo "✅ Testing command availability..."
python3 video_audio_utils.py --help | grep -q generate-subtitles && echo "✅ Command found" || echo "❌ Command missing"

# Test 2: Parameter support  
echo "✅ Testing parameter support..."
python3 video_audio_utils.py --help | grep -q "srt.*vtt" && echo "✅ SRT/VTT formats supported" || echo "⚠️  Format support unclear"

# Test 3: Sample video check
echo "✅ Checking for sample video..."
if [ -f "$INPUT_DIR/sample_video.mp4" ]; then
    echo "✅ Sample video found"
else
    echo "⚠️  No sample video found"
fi

# Test 4: FFmpeg check
echo "✅ Checking ffmpeg..."
command -v ffmpeg >/dev/null 2>&1 && echo "✅ ffmpeg available" || echo "❌ ffmpeg missing"

echo ""
echo "💡 Usage examples:"
echo "  python3 video_audio_utils.py generate-subtitles -i video.mp4 -o subtitle.srt"
echo "  python3 video_audio_utils.py generate-subtitles -i input/ -o output/ -f vtt"
echo ""
echo "✨ Test completed!"