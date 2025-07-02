#!/bin/bash

# TTS Basic Test - Based on tts_basic_test.yaml
# Simple text-to-speech testing script

echo "🎤 TTS Basic Test"
echo "================"

# Change to TTS directory
cd /home/zdhpe/veo3-video-generation/text_to_speech

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Step 1: List available voices${NC}"
python examples/basic_usage.py --list-voices

echo -e "\n${BLUE}Step 2: Generate basic TTS sample (Rachel voice)${NC}"
python examples/basic_usage.py \
  --text "Welcome to our AI-powered text-to-speech system. This demonstration showcases natural voice synthesis with customizable parameters for professional audio content creation." \
  --voice rachel \
  --output tts_basic.mp3 \
  --quiet

echo -e "\n${BLUE}Step 3: Generate professional sample (Drew voice)${NC}"
python examples/tts_cli_wrapper.py \
  "This is a professional male voice demonstration with optimized settings for business presentations and corporate communications." \
  drew \
  tts_professional.mp3 \
  --stability 0.7 \
  --similarity-boost 0.9 \
  --style 0.1 \
  --json

echo -e "\n${BLUE}Step 4: Generate creative sample (Bella voice)${NC}"
python examples/basic_usage.py \
  --text "This creative voice sample demonstrates expressive speech with dynamic intonation perfect for storytelling and engaging content." \
  --voice bella \
  --speed 1.1 \
  --stability 0.3 \
  --style 0.8 \
  --output tts_creative.mp3 \
  --quiet

echo -e "\n${BLUE}Step 5: Validate voice availability${NC}"
python examples/tts_cli_wrapper.py --validate-voice rachel --json

echo -e "\n${BLUE}Step 6: Check generated files${NC}"
echo "Generated TTS files:"
for file in output/tts_basic.mp3 output/tts_professional.mp3 output/tts_creative.mp3; do
    if [ -f "$file" ]; then
        size=$(ls -lh "$file" | awk '{print $5}')
        echo -e "${GREEN}✅${NC} $file ($size)"
    else
        echo -e "${YELLOW}⚠️${NC} $file (not found)"
    fi
done

# Count successful generations
success_count=$(ls output/tts_*.mp3 2>/dev/null | wc -l)
echo -e "\n${YELLOW}📊 Generated $success_count/3 TTS files${NC}"

if [ $success_count -eq 3 ]; then
    echo -e "${GREEN}✅ TTS Basic Test PASSED${NC}"
    echo "All voice samples generated successfully!"
else
    echo -e "${YELLOW}⚠️ TTS Basic Test PARTIAL${NC}"
    echo "Some voice samples may have issues."
fi

echo ""
echo "🚀 TTS test complete!"
echo "Files available in: /home/zdhpe/veo3-video-generation/text_to_speech/output/"