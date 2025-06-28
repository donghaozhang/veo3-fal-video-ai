#!/bin/bash
# Activation script for text_to_speech environment

# Activate virtual environment
source tts_env/bin/activate

# Set PYTHONPATH for proper imports
export PYTHONPATH=/home/zdhpe/veo3-video-generation:$PYTHONPATH

echo "✅ Text-to-Speech environment activated"
echo "📁 Working directory: $(pwd)"
echo "🐍 Python path includes: $PYTHONPATH"
echo ""
echo "Ready to run:"
echo "  python examples/basic_usage.py"
echo "  python cli/quick_start.py"
echo "  python test_simple.py"