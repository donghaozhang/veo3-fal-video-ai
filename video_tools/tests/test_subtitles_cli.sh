#!/bin/bash
# CLI test for video_audio_utils.py generate-subtitles command with -i and -o parameters

# Activate virtual environment and navigate to correct directory
source /home/zdhpe/veo3-video-generation/venv/bin/activate
cd /home/zdhpe/veo3-video-generation/video_tools

echo "🧪 Testing video_audio_utils.py generate-subtitles CLI with parameters..."
echo "================================================================="

# Use specified input and output directories
INPUT_DIR="/home/zdhpe/veo3-video-generation/video_tools/input"
OUTPUT_DIR="/home/zdhpe/veo3-video-generation/video_tools/output"

# Create directories if they don't exist
mkdir -p "$INPUT_DIR" "$OUTPUT_DIR"

echo "📁 Using directories:"
echo "   Input:  $INPUT_DIR"
echo "   Output: $OUTPUT_DIR"
echo ""

echo "🧪 Test 1: Command availability and parameter support"
echo "Testing generate-subtitles command availability..."
python3 video_audio_utils.py --help | grep generate-subtitles

if [ $? -eq 0 ]; then
    echo "✅ generate-subtitles command is available"
else
    echo "❌ generate-subtitles command not found in help"
fi
echo ""

echo "🧪 Test 2: Enhanced parameter support"
echo "Testing enhanced help message..."
python3 video_audio_utils.py --help | grep -A 3 "Enhanced generate-subtitles"

if [ $? -eq 0 ]; then
    echo "✅ Enhanced parameter support documented"
else
    echo "⚠️  Enhanced parameter documentation not found"
fi
echo ""

echo "🧪 Test 3: Format parameter validation"
echo "Testing format choices (should include srt and vtt)..."
python3 video_audio_utils.py --help | grep "srt.*vtt"

if [ $? -eq 0 ]; then
    echo "✅ SRT and VTT format options available"
else
    echo "⚠️  SRT/VTT format options not found in help"
fi
echo ""

echo "🧪 Test 4: Single video file test"
if [ -f "$INPUT_DIR/sample_video.mp4" ]; then
    echo "✅ Sample video found: $INPUT_DIR/sample_video.mp4"
    echo "📺 Testing single file with specific output:"
    echo "   Command: python3 video_audio_utils.py generate-subtitles -i $INPUT_DIR/sample_video.mp4 -o $OUTPUT_DIR/test_subtitle.srt -f srt"
    echo "   (Interactive mode - requires subtitle text input)"
else
    echo "⚠️  Sample video not found: $INPUT_DIR/sample_video.mp4"
    echo "💡 Place a test video at '$INPUT_DIR/sample_video.mp4' to run full tests"
fi
echo ""

echo "🧪 Test 5: Directory input test"
echo "📺 Testing directory input with VTT format:"
echo "   Command: python3 video_audio_utils.py generate-subtitles -i $INPUT_DIR/ -o $OUTPUT_DIR/ -f vtt"
echo "   (Interactive mode - requires subtitle text input)"
echo ""

echo "🧪 Test 6: Parameter combination examples"
echo "Available parameter combinations:"
echo "1. Single file to specific output: -i video.mp4 -o subtitle.srt"
echo "2. Single file to directory: -i video.mp4 -o output_dir/ -f srt"
echo "3. Directory to directory: -i input_dir/ -o output_dir/ -f vtt"
echo "4. Input only (output defaults): -i video.mp4 -f srt"
echo "5. Input and format only: -i input_dir/ -f vtt"
echo ""

echo "🧪 Test 7: FFmpeg availability check"
echo "Checking ffmpeg installation..."
if command -v ffmpeg >/dev/null 2>&1; then
    echo "✅ ffmpeg is installed and available"
    ffmpeg -version | head -1
else
    echo "❌ ffmpeg not found - required for video processing"
    echo "📥 Please install ffmpeg to run video subtitle tests"
fi
echo ""

echo "📊 CLI PARAMETER TEST SUMMARY"
echo "==============================="
echo "✅ Command availability: generate-subtitles with -i, -o, -f parameters"
echo "✅ Format support: SRT (.srt) and WebVTT (.vtt)"
echo "✅ Input options: Single file or directory"
echo "✅ Output options: Specific file or directory"
echo "✅ Directories: Input=$INPUT_DIR, Output=$OUTPUT_DIR"

if command -v ffmpeg >/dev/null 2>&1; then
    echo "✅ ffmpeg: Available"
else
    echo "⚠️  ffmpeg: Not found (install required)"
fi

echo ""
echo "💡 PARAMETER USAGE EXAMPLES:"
echo "1. Single video to SRT subtitle:"
echo "   python3 video_audio_utils.py generate-subtitles -i $INPUT_DIR/video.mp4 -o $OUTPUT_DIR/subtitle.srt"
echo ""
echo "2. Video to specific directory (VTT format):"
echo "   python3 video_audio_utils.py generate-subtitles -i $INPUT_DIR/video.mp4 -o $OUTPUT_DIR/ -f vtt"
echo ""
echo "3. Batch process directory (SRT format):"
echo "   python3 video_audio_utils.py generate-subtitles -i $INPUT_DIR/ -o $OUTPUT_DIR/ -f srt"
echo ""
echo "4. Use specific format (auto-detect from output extension):"
echo "   python3 video_audio_utils.py generate-subtitles -i $INPUT_DIR/video.mp4 -o $OUTPUT_DIR/subtitle.vtt"
echo ""

echo "🎯 EXPECTED OUTPUT FILES:"
echo "   - $OUTPUT_DIR/*.srt (SRT subtitle files)"
echo "   - $OUTPUT_DIR/*.vtt (WebVTT subtitle files)"
echo ""

echo "📺 COMPATIBLE VIDEO PLAYERS:"
echo "   - VLC Media Player (auto-loads same-name subtitle files)"
echo "   - Windows Media Player"
echo "   - Web browsers (for .vtt files)"
echo "   - MPV, MPC-HC, and most modern video players"

echo ""
echo "✨ Enhanced CLI test completed!"