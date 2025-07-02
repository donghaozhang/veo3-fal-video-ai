#!/bin/bash

# TTS CLI Demo Test Script
# Based on tts_cli_demo.yaml workflow

echo "🎤 TTS CLI Demo Test Script"
echo "=========================="

cd /home/zdhpe/veo3-video-generation/text_to_speech

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}1. Testing voice listing...${NC}"
python examples/basic_usage.py --list-voices

echo -e "\n${BLUE}2. Testing basic generation...${NC}"
python examples/basic_usage.py --text "This is a demonstration of our text-to-speech capabilities." --voice rachel --output demo_basic.mp3 --quiet

echo -e "\n${BLUE}3. Testing CLI wrapper with JSON...${NC}"
python examples/tts_cli_wrapper.py "The system supports multiple voices with customizable settings." rachel demo_wrapper.mp3 --json

echo -e "\n${BLUE}4. Testing voice validation...${NC}"
echo "Valid voice:"
python examples/tts_cli_wrapper.py --validate-voice rachel --json
echo "Invalid voice:"
python examples/tts_cli_wrapper.py --validate-voice invalid_voice --json

echo -e "\n${BLUE}5. Testing different voices...${NC}"
python examples/tts_cli_wrapper.py "Professional audio with Drew voice." drew demo_drew.mp3 --json
python examples/tts_cli_wrapper.py "Creative audio with Bella voice." bella demo_bella.mp3 --json

echo -e "\n${BLUE}6. Testing custom settings...${NC}"
echo "Slow and stable:"
python examples/basic_usage.py --text "This is slow and stable speech." --voice rachel --speed 0.8 --stability 0.9 --output demo_slow_stable.mp3 --quiet

echo "Fast and creative:"
python examples/basic_usage.py --text "This is fast and creative speech!" --voice bella --speed 1.2 --stability 0.3 --style 0.8 --output demo_fast_creative.mp3 --quiet

echo -e "\n${BLUE}7. Checking generated files...${NC}"
echo "Files in output directory:"
ls -la output/demo_*.mp3 2>/dev/null | while read line; do
    echo -e "${GREEN}✅${NC} $line"
done

# Count generated files
file_count=$(ls output/demo_*.mp3 2>/dev/null | wc -l)
echo -e "\n${YELLOW}📊 Generated $file_count demo audio files${NC}"

echo -e "\n${GREEN}✅ TTS CLI Demo Complete!${NC}"
echo ""
echo "Demo files created:"
echo "  - output/demo_basic.mp3 (Rachel voice, default settings)"
echo "  - output/demo_wrapper.mp3 (Rachel voice, CLI wrapper)"  
echo "  - output/demo_drew.mp3 (Drew voice)"
echo "  - output/demo_bella.mp3 (Bella voice)"
echo "  - output/demo_slow_stable.mp3 (Slow, stable speech)"
echo "  - output/demo_fast_creative.mp3 (Fast, creative speech)"
echo ""
echo "🚀 Ready for AI pipeline integration!"