#!/usr/bin/env bash

# Test Python CLI for Text-to-Speech
# Quick test script to verify CLI functionality

echo "🎤 Testing Python CLI for Text-to-Speech"
echo "========================================"

cd /home/zdhpe/veo3-video-generation/text_to_speech

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_TOTAL=0

# Function to run test
run_test() {
    local test_name="$1"
    local command="$2"
    local expected_exit_code="${3:-0}"
    
    echo ""
    echo -e "${BLUE}🧪 Test: $test_name${NC}"
    echo "Command: $command"
    echo "----------------------------------------"
    
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    
    # Run command and capture output and exit code
    if eval "$command" > /tmp/test_output.log 2>&1; then
        actual_exit_code=0
    else
        actual_exit_code=$?
    fi
    
    # Show output
    cat /tmp/test_output.log
    
    # Check result
    if [ $actual_exit_code -eq $expected_exit_code ]; then
        echo -e "${GREEN}✅ PASS${NC} (exit code: $actual_exit_code)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}❌ FAIL${NC} (expected: $expected_exit_code, got: $actual_exit_code)"
    fi
    
    echo ""
}

# Test 1: Help command
run_test "Help Command" "python examples/basic_usage.py --help"

# Test 2: List voices
run_test "List Voices" "python examples/basic_usage.py --list-voices"

# Test 3: CLI Wrapper help
run_test "CLI Wrapper Help" "python examples/tts_cli_wrapper.py --help"

# Test 4: CLI Wrapper list voices with JSON
run_test "CLI Wrapper List Voices (JSON)" "python examples/tts_cli_wrapper.py --list-voices --json"

# Test 5: Voice validation
run_test "Voice Validation (Valid)" "python examples/tts_cli_wrapper.py --validate-voice rachel --json"

# Test 6: Voice validation (Invalid)
run_test "Voice Validation (Invalid)" "python examples/tts_cli_wrapper.py --validate-voice invalid_voice --json" 1

# Test 7: Basic text generation (placeholder mode due to import issues)
run_test "Basic Text Generation" "python examples/basic_usage.py --text 'CLI test message' --voice rachel --output test_cli.mp3 --quiet"

# Test 8: CLI Wrapper text generation
run_test "CLI Wrapper Generation" "python examples/tts_cli_wrapper.py 'Wrapper test message' rachel test_wrapper.mp3 --json"

# Test 9: Speed parameter validation (invalid)
run_test "Speed Validation (Invalid)" "python examples/basic_usage.py --text 'Test' --speed 2.0" 1

# Test 10: Speed parameter validation (valid)
run_test "Speed Validation (Valid)" "python examples/basic_usage.py --text 'Test' --speed 1.1 --quiet"

# Results summary
echo ""
echo "========================================="
echo -e "${BLUE}📊 Test Results Summary${NC}"
echo "========================================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}/$TESTS_TOTAL"

if [ $TESTS_PASSED -eq $TESTS_TOTAL ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo -e "${GREEN}✅ Python CLI is working correctly${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed${NC}"
    echo -e "${YELLOW}📝 Check output above for details${NC}"
fi

# Check generated files
echo ""
echo -e "${BLUE}📁 Generated Files Check${NC}"
echo "----------------------------------------"
if [ -d "output" ]; then
    echo -e "${GREEN}✅ Output folder exists${NC}"
    file_count=$(ls -1 output/*.mp3 2>/dev/null | wc -l)
    if [ $file_count -gt 0 ]; then
        echo -e "${GREEN}✅ Found $file_count audio files in output/${NC}"
        echo "Files:"
        ls -la output/*.mp3 2>/dev/null | tail -5
    else
        echo -e "${YELLOW}⚠️  No audio files found in output/${NC}"
    fi
else
    echo -e "${RED}❌ Output folder missing${NC}"
fi

# Cleanup
rm -f /tmp/test_output.log

echo ""
echo -e "${BLUE}🏁 CLI Test Complete!${NC}"

# Exit with appropriate code
if [ $TESTS_PASSED -eq $TESTS_TOTAL ]; then
    exit 0
else
    exit 1
fi