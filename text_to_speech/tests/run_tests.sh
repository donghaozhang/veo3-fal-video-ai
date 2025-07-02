#!/usr/bin/env bash

# Test Runner for Text-to-Speech CLI
# Provides easy access to all test scripts

echo "🧪 Text-to-Speech CLI Test Runner"
echo "================================="

cd /home/zdhpe/veo3-video-generation/text_to_speech

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to show usage
show_usage() {
    echo ""
    echo "Usage: $0 [test_type]"
    echo ""
    echo "Available test types:"
    echo -e "  ${GREEN}quick${NC}          - Quick functionality test (~5 seconds, no API calls)"
    echo -e "  ${BLUE}comprehensive${NC}  - Complete system test (35+ tests, no API calls)" 
    echo -e "  ${YELLOW}api${NC}            - API functionality test (uses API calls, costs apply)"
    echo -e "  ${CYAN}all${NC}            - Run quick + comprehensive tests"
    echo -e "  ${CYAN}list${NC}           - List all available test scripts"
    echo ""
    echo "Examples:"
    echo "  $0 quick              # Fast daily check"
    echo "  $0 comprehensive      # Thorough testing"
    echo "  $0 api               # Test with actual API calls"
    echo "  $0 all               # Run multiple tests"
    echo ""
}

# Function to list available tests
list_tests() {
    echo ""
    echo "📋 Available Test Scripts:"
    echo ""
    echo "🚀 Available Tests:"
    ls -la tests/*.sh | grep -E "(quick_test|comprehensive|api_functionality|run_tests)" | awk '{print "   " $9 " (" $5 " bytes)"}'
    echo ""
    echo "📖 Documentation:"
    [ -f tests/README.md ] && echo "   tests/README.md ($(wc -c < tests/README.md) bytes)"
    echo ""
}

# Function to run a specific test
run_test() {
    local test_name="$1"
    local test_file="$2"
    
    echo ""
    echo -e "${BLUE}🏃 Running: $test_name${NC}"
    echo "=================================================="
    
    if [ -f "$test_file" ]; then
        bash "$test_file"
        local exit_code=$?
        
        echo ""
        if [ $exit_code -eq 0 ]; then
            echo -e "${GREEN}✅ $test_name completed successfully${NC}"
        else
            echo -e "${YELLOW}⚠️  $test_name completed with issues (exit code: $exit_code)${NC}"
        fi
        return $exit_code
    else
        echo -e "${RED}❌ Test file not found: $test_file${NC}"
        return 1
    fi
}

# Main logic
case "${1:-}" in
    "quick")
        run_test "Quick Test" "tests/quick_test.sh"
        ;;
    
    "comprehensive")
        run_test "Comprehensive Test" "tests/comprehensive_cli_test.sh"
        ;;
    
    "api")
        echo ""
        echo -e "${YELLOW}⚠️  Warning: API test will make actual API calls${NC}"
        echo "This may incur costs on your ElevenLabs account."
        echo ""
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            run_test "API Functionality Test" "tests/api_functionality_test.sh"
        else
            echo "API test cancelled."
        fi
        ;;
    
    "all")
        echo -e "${CYAN}Running multiple tests...${NC}"
        
        run_test "Quick Test" "tests/quick_test.sh"
        echo ""
        echo "===================="
        
        run_test "Comprehensive Test" "tests/comprehensive_cli_test.sh"
        
        echo ""
        echo -e "${CYAN}📊 All Tests Summary:${NC}"
        echo "✅ Quick test and comprehensive test completed"
        echo "💡 Run 'bash tests/run_tests.sh api' to test API functionality"
        ;;
    
    "list")
        list_tests
        ;;
    
    "help"|"-h"|"--help")
        show_usage
        ;;
    
    "")
        echo "🎯 No test specified. Available options:"
        echo ""
        echo -e "  ${GREEN}Quick Test${NC}        - Fast daily check"
        echo -e "  ${BLUE}Comprehensive${NC}     - Complete system verification"
        echo -e "  ${YELLOW}API Test${NC}          - Test with actual API calls (costs apply)"
        echo ""
        echo "Choose your test:"
        echo "  1) Quick test (recommended)"
        echo "  2) Comprehensive test"
        echo "  3) API test"
        echo "  4) List all tests"
        echo "  5) Help"
        echo ""
        read -p "Enter choice (1-5): " -n 1 -r
        echo ""
        
        case $REPLY in
            1) run_test "Quick Test" "tests/quick_test.sh" ;;
            2) run_test "Comprehensive Test" "tests/comprehensive_cli_test.sh" ;;
            3) 
                echo ""
                echo -e "${YELLOW}⚠️  API test will make actual API calls and may incur costs${NC}"
                read -p "Continue? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    run_test "API Functionality Test" "tests/api_functionality_test.sh"
                else
                    echo "API test cancelled."
                fi
                ;;
            4) list_tests ;;
            5) show_usage ;;
            *) echo "Invalid choice. Use --help for usage information." ;;
        esac
        ;;
    
    *)
        echo "❌ Unknown test type: $1"
        show_usage
        exit 1
        ;;
esac

echo ""
echo "🏁 Test runner finished!"