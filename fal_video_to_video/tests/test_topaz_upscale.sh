#!/bin/bash

# Test script for Topaz Video Upscale with final_multitalk_6112.mp4
# Usage: bash test_topaz_upscale.sh

echo "🚀 Testing Topaz Video Upscale with final_multitalk_6112.mp4"
echo "============================================================"

# Set paths
VIDEO_FILE="input/final_multitalk_6112.mp4"
OUTPUT_DIR="output"

# Check if video file exists
if [ ! -f "$VIDEO_FILE" ]; then
    echo "❌ Error: Video file not found: $VIDEO_FILE"
    exit 1
fi

# Check if output directory exists, create if not
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "📁 Creating output directory: $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
fi

# Get video info before processing
echo "📹 Input video information:"
if command -v ffprobe &> /dev/null; then
    ffprobe -v quiet -print_format json -show_format -show_streams "$VIDEO_FILE" | grep -E '"width"|"height"|"duration"|"bit_rate"' | head -4
else
    ls -lh "$VIDEO_FILE"
fi

echo ""
echo "🔍 Starting Topaz 2x upscaling..."
echo "⏱️  Start time: $(date)"

# Run the upscale command
python -m fal_video_to_video upscale \
    -i "$VIDEO_FILE" \
    --upscale-factor 2 \
    -o "$OUTPUT_DIR" \
    --save-json "topaz_result.json"

# Check if command was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Upscaling completed successfully!"
    echo "⏱️  End time: $(date)"
    
    # Show output files
    echo ""
    echo "📁 Output directory contents:"
    ls -lah "$OUTPUT_DIR"
    
    # Show result JSON if it exists
    if [ -f "topaz_result.json" ]; then
        echo ""
        echo "📄 Result summary:"
        cat topaz_result.json | grep -E '"success"|"model"|"processing_time"|"local_path"' | head -4
    fi
else
    echo ""
    echo "❌ Upscaling failed!"
    exit 1
fi

echo ""
echo "🎉 Test completed!"