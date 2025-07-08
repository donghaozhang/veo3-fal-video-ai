#\!/bin/bash
# CLI test for video_audio_utils.py analyze-images command
cd /home/zdhpe/veo3-video-generation
source venv/bin/activate
cd video_tools

echo "🧪 Testing analyze-images CLI with parameters..."
echo "================================================="

INPUT_DIR="/home/zdhpe/veo3-video-generation/video_tools/input"
OUTPUT_DIR="/home/zdhpe/veo3-video-generation/video_tools/output"

# Only create directories if they do not exist
[ \! -d "$INPUT_DIR" ] && mkdir -p "$INPUT_DIR" && echo "📁 Created input directory"
[ \! -d "$OUTPUT_DIR" ] && mkdir -p "$OUTPUT_DIR" && echo "📁 Created output directory"

# Test 1: Command availability
echo "✅ Testing command availability..."
python3 video_audio_utils.py --help < /dev/null  < /dev/null |  grep -q analyze-images && echo "✅ Command found" || echo "❌ Command missing"

# Test 2: Parameter support
echo "✅ Testing parameter support..."
python3 video_audio_utils.py --help | grep -q "json.*txt" && echo "✅ JSON/TXT formats supported" || echo "⚠️  Format support unclear"

# Test 3: Sample image check
echo "✅ Checking for sample images..."
if [ -f "$INPUT_DIR/sample_image.jpg" ] || [ -f "$INPUT_DIR/sample_image.png" ] || [ -f "$INPUT_DIR/sample_image.jpeg" ]; then
    echo "✅ Sample image found"
else
    echo "⚠️  No sample image found"
fi

# Test 4: Gemini API check (optional)
echo "✅ Checking Gemini API..."
if [ -n "$GEMINI_API_KEY" ]; then
    echo "✅ GEMINI_API_KEY is set"
else
    echo "⚠️  GEMINI_API_KEY not set (optional for AI analysis)"
fi

echo ""
echo "💡 Usage examples:"
echo "  python3 video_audio_utils.py analyze-images -i image.jpg -o analysis.json"
echo "  python3 video_audio_utils.py analyze-images -i input/ -o output/ -f txt"
echo ""
echo "✨ Test completed!"
