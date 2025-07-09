#!/usr/bin/env bash

# Quick Text-to-Speech CLI Test
# Fast check for basic functionality

echo "⚡ Quick TTS CLI Test"
echo "==================="

cd /home/zdhpe/veo3-video-generation/text_to_speech

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "🔍 Basic Checks:"

# Check directory structure
echo -n "   File structure: "
if [ -f "cli/quick_start.py" ] && [ -f "config/voices.py" ] && [ -f ".env" ]; then
    echo -e "${GREEN}✅ OK${NC}"
else
    echo -e "${RED}❌ Missing files${NC}"
fi

# Check API keys
echo -n "   API configuration: "
if [ -f ".env" ]; then
    API_CHECK=$(python3 -c "
from dotenv import load_dotenv; import os; load_dotenv()
print('OK' if os.getenv('ELEVENLABS_API_KEY') else 'MISSING')
" 2>/dev/null)
    
    if [ "$API_CHECK" = "OK" ]; then
        echo -e "${GREEN}✅ API keys loaded${NC}"
    else
        echo -e "${YELLOW}⚠️  API keys missing${NC}"
    fi
else
    echo -e "${RED}❌ No .env file${NC}"
fi

# Check voice system
echo -n "   Voice system: "
VOICE_CHECK=$(python3 -c "
from config.voices import POPULAR_VOICES
print(len(POPULAR_VOICES))
" 2>/dev/null)

if [ "$VOICE_CHECK" -gt 0 ] 2>/dev/null; then
    echo -e "${GREEN}✅ $VOICE_CHECK voices available${NC}"
else
    echo -e "${RED}❌ Voice system error${NC}"
fi

# Check output directory
echo -n "   Output directory: "
if [ -d "output" ]; then
    file_count=$(ls -1 output/*.mp3 2>/dev/null | wc -l)
    echo -e "${GREEN}✅ Ready ($file_count existing files)${NC}"
else
    echo -e "${YELLOW}⚠️  Will be created${NC}"
fi

echo ""
echo "🎯 Quick Tests:"

# Test CLI accessibility
echo -n "   CLI scripts: "
if python3 cli/quick_start.py --help >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Import issues${NC}"
fi

# Test voice lookup
echo -n "   Voice lookup: "
VOICE_TEST=$(python3 -c "
from dotenv import load_dotenv; load_dotenv()
from config.voices import POPULAR_VOICES
voice = POPULAR_VOICES.get('rachel')
print('OK' if voice else 'FAIL')
" 2>/dev/null)

if [ "$VOICE_TEST" = "OK" ]; then
    echo -e "${GREEN}✅ Working${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
fi

echo ""
echo "🚀 Status Summary:"

# Calculate overall status
CHECKS_PASSED=0
[ -f "cli/quick_start.py" ] && CHECKS_PASSED=$((CHECKS_PASSED + 1))
[ -f ".env" ] && CHECKS_PASSED=$((CHECKS_PASSED + 1))
[ "$VOICE_CHECK" -gt 0 ] 2>/dev/null && CHECKS_PASSED=$((CHECKS_PASSED + 1))
[ "$API_CHECK" = "OK" ] && CHECKS_PASSED=$((CHECKS_PASSED + 1))

if [ $CHECKS_PASSED -ge 4 ]; then
    echo -e "   ${GREEN}✅ READY FOR USE${NC} - All systems operational"
    echo ""
    echo "   Quick commands:"
    echo "   python3 cli/quick_start.py --info"
    echo "   python3 -c \"from dotenv import load_dotenv; load_dotenv(); from config.voices import POPULAR_VOICES; print(list(POPULAR_VOICES.keys()))\""
elif [ $CHECKS_PASSED -ge 2 ]; then
    echo -e "   ${YELLOW}⚠️  PARTIALLY READY${NC} - Some features may not work"
    echo "   Check API configuration and dependencies"
else
    echo -e "   ${RED}❌ NOT READY${NC} - Needs setup"
    echo "   Run comprehensive test for detailed diagnosis"
fi

echo ""
echo "📋 For detailed testing: bash tests/comprehensive_cli_test.sh"
echo ""
echo "⚡ Quick test completed!"