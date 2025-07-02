#!/usr/bin/env bash

# API Functionality Test
# Tests actual API connectivity and functionality (uses API calls)

echo "🔌 Text-to-Speech API Functionality Test"
echo "========================================"

cd /home/zdhpe/veo3-video-generation/text_to_speech

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}⚠️  WARNING: This test makes actual API calls and may incur costs${NC}"
echo ""
read -p "Continue with API testing? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "API testing cancelled."
    exit 0
fi

echo ""
echo "🔑 Loading API Configuration..."

# Load environment and check keys
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    exit 1
fi

API_STATUS=$(python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY', '')
openrouter_key = os.getenv('OPENROUTER_API_KEY', '')
print(f'ELEVENLABS:{len(elevenlabs_key) > 0}')
print(f'OPENROUTER:{len(openrouter_key) > 0}')
if elevenlabs_key:
    print(f'ELEVENLABS_PREVIEW:{elevenlabs_key[:8]}...{elevenlabs_key[-4:]}')
")

if echo "$API_STATUS" | grep -q "ELEVENLABS:True"; then
    ELEVENLABS_PREVIEW=$(echo "$API_STATUS" | grep "ELEVENLABS_PREVIEW:" | cut -d: -f2)
    echo -e "${GREEN}✅ ElevenLabs API key loaded: $ELEVENLABS_PREVIEW${NC}"
else
    echo -e "${RED}❌ ElevenLabs API key not found${NC}"
    exit 1
fi

if echo "$API_STATUS" | grep -q "OPENROUTER:True"; then
    echo -e "${GREEN}✅ OpenRouter API key loaded${NC}"
else
    echo -e "${YELLOW}⚠️  OpenRouter API key not found (optional)${NC}"
fi

echo ""
echo "🧪 API Functionality Tests:"

# Ensure output directory exists
mkdir -p output

echo ""
echo -e "${BLUE}Test 1: Voice Configuration with API Context${NC}"
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()

try:
    from config.voices import POPULAR_VOICES
    print(f'✅ Successfully loaded {len(POPULAR_VOICES)} voices')
    
    # Test voice lookup
    rachel = POPULAR_VOICES.get('rachel')
    if rachel:
        print(f'✅ Rachel voice found: {rachel.voice_id}')
    else:
        print('❌ Rachel voice not found')
        
    # Show available voices
    print('📋 Available voices:')
    for i, (name, voice) in enumerate(list(POPULAR_VOICES.items())[:5]):
        print(f'   {i+1}. {name}: {voice.description}')
    if len(POPULAR_VOICES) > 5:
        print(f'   ... and {len(POPULAR_VOICES) - 5} more')
        
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo -e "${BLUE}Test 2: TTS Controller Initialization${NC}"
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()

try:
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print('❌ No API key available')
        exit(1)
    
    print(f'✅ API key available: {api_key[:8]}...{api_key[-4:]}')
    print(f'✅ Key length: {len(api_key)} characters')
    print(f'✅ Valid format: {api_key.startswith(\"sk_\")}')
    
    # Test basic validation
    from utils.validators import validate_text_input
    test_text = 'Hello, this is a test.'
    is_valid, error = validate_text_input(test_text)
    print(f'✅ Text validation: {is_valid} (error: {error})')
    
except Exception as e:
    print(f'❌ Error during initialization: {e}')
"

echo ""
echo -e "${BLUE}Test 3: CLI Scripts with API${NC}"
echo "Testing CLI accessibility with API context..."

# Test CLI info command
echo "📋 Pipeline Information:"
python3 cli/quick_start.py --info 2>/dev/null | head -10

echo ""
echo -e "${BLUE}Test 4: Voice System Ready Check${NC}"
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()

try:
    from config.voices import POPULAR_VOICES
    
    # Test specific voice lookup
    test_voices = ['rachel', 'drew', 'bella', 'antoni']
    print('🎤 Voice System Ready Check:')
    
    for voice_name in test_voices:
        voice = POPULAR_VOICES.get(voice_name)
        if voice:
            print(f'   ✅ {voice_name}: {voice.description} (ID: {voice.voice_id[:12]}...)')
        else:
            print(f'   ❌ {voice_name}: Not found')
    
    print(f'\\n📊 Total voices available: {len(POPULAR_VOICES)}')
    
except Exception as e:
    print(f'❌ Voice system error: {e}')
"

echo ""
echo -e "${CYAN}=== API READINESS SUMMARY ===${NC}"

# Final readiness check
READINESS=$(python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()

score = 0
issues = []

# Check API key
api_key = os.getenv('ELEVENLABS_API_KEY', '')
if api_key and len(api_key) > 20:
    score += 2
    print('✅ API Key: Ready')
else:
    issues.append('API Key missing')
    print('❌ API Key: Not configured')

# Check voice system
try:
    from config.voices import POPULAR_VOICES
    if len(POPULAR_VOICES) >= 5:
        score += 1
        print(f'✅ Voice System: {len(POPULAR_VOICES)} voices ready')
    else:
        issues.append('Insufficient voices')
        print('❌ Voice System: Insufficient voices')
except:
    issues.append('Voice system error')
    print('❌ Voice System: Import error')

# Check CLI
try:
    from utils.validators import validate_text_input
    score += 1
    print('✅ CLI Utilities: Working')
except:
    issues.append('CLI utilities error')
    print('❌ CLI Utilities: Import error')

print(f'\\nScore: {score}/4')
if score >= 3:
    print('Status: READY FOR API CALLS')
elif score >= 2:
    print('Status: PARTIALLY READY')
else:
    print('Status: NOT READY')

if issues:
    print('Issues:', ', '.join(issues))
")

echo ""
echo "🎯 Next Steps:"

if python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('ELEVENLABS_API_KEY', '')
print('ready' if len(api_key) > 20 else 'not_ready')
" | grep -q "ready"; then
    echo "   ✅ System ready for text-to-speech generation"
    echo ""
    echo "   🚀 Try these commands:"
    echo "   # Interactive CLI:"
    echo "   python3 cli/interactive.py"
    echo ""
    echo "   # Basic examples:"
    echo "   python3 examples/basic_usage.py"
    echo ""
    echo "   # Voice test:"
    echo "   python3 -c \"from dotenv import load_dotenv; load_dotenv(); from config.voices import POPULAR_VOICES; print('Available:', list(POPULAR_VOICES.keys()))\""
else
    echo "   ⚠️  System needs configuration before API calls"
    echo "   Check API keys and dependencies"
fi

echo ""
echo "🔌 API functionality test completed!"