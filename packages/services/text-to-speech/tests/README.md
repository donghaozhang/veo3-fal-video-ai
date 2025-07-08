# Text-to-Speech CLI Test Suite

This directory contains comprehensive test scripts for the Text-to-Speech CLI functionality.

## 📋 Available Tests

### 🚀 Quick Tests (Recommended for daily use)

#### `quick_test.sh`
**Fast check for basic functionality**
- ⚡ Runs in ~5 seconds
- ✅ No API calls (free)
- 🔍 Checks file structure, API config, voice system
- 💡 Perfect for daily verification

```bash
cd /home/zdhpe/veo3-video-generation/text_to_speech
bash tests/quick_test.sh
```

### 🧪 Comprehensive Tests

#### `comprehensive_cli_test.sh`
**Complete system testing (35+ tests)**
- 🔬 Thorough testing of all components
- ✅ No API calls (free)
- 📊 Detailed pass/fail reporting
- 🎯 Best for troubleshooting and setup verification

```bash
bash tests/comprehensive_cli_test.sh
```

### 🔌 API Tests (Uses API calls - costs apply)

#### `api_functionality_test.sh`
**Tests actual API connectivity**
- ⚠️  Makes real API calls (costs may apply)
- 🔑 Requires valid API keys
- 🧪 Tests TTS controller initialization
- 🎤 Validates voice system with API context

```bash
bash tests/api_functionality_test.sh
```

## 🎯 Test Suite Philosophy

This streamlined test suite eliminates redundancy while providing comprehensive coverage:

- **Quick Test**: Fast daily verification
- **Comprehensive Test**: Complete system validation  
- **API Test**: Real-world functionality testing
- **Test Runner**: User-friendly interface

## 🎯 Usage Recommendations

### For Daily Development
```bash
# Quick health check
bash tests/quick_test.sh
```

### For Setup/Troubleshooting
```bash
# Comprehensive diagnosis
bash tests/comprehensive_cli_test.sh
```

### For API Testing
```bash
# Test actual API functionality (costs apply)
bash tests/api_functionality_test.sh
```

## 📊 Test Results Interpretation

### Success Rates
- **90-100%**: ✅ Ready for production use
- **75-89%**: ⚠️  Mostly ready, minor issues
- **50-74%**: ⚠️  Partial functionality
- **<50%**: ❌ Significant issues, needs setup

### Common Issues and Solutions

#### Import Errors
```
ImportError: attempted relative import beyond top-level package
```
**Solution**: This is expected for some package imports without API keys. Core functionality still works.

#### Missing API Keys
```
ELEVENLABS_API_KEY not set
```
**Solution**: Set API key in `.env` file or environment variable.

#### Voice System Errors
```
Voice configuration failed
```
**Solution**: Check `config/voices.py` and ensure imports work.

## 🔧 Test Environment

### Requirements
- Python 3.12+
- Virtual environment activated
- Dependencies installed (`pip install -r requirements.txt`)
- `.env` file with API keys (for API tests)

### Setup
```bash
# Ensure you're in the text_to_speech directory
cd /home/zdhpe/veo3-video-generation/text_to_speech

# Activate virtual environment
source tts_env/bin/activate

# Run desired test
bash tests/quick_test.sh
```

## 🎯 Integration Testing

These tests verify the TTS system is ready for integration with:
- ✅ AI Content Pipeline
- ✅ Video generation workflows
- ✅ Automated content creation
- ✅ Multi-speaker dialogue systems

## 📈 Continuous Testing

For automated testing in CI/CD pipelines:

```bash
# Non-interactive comprehensive test
bash tests/comprehensive_cli_test.sh | tee test_results.log

# Check exit code
if [ $? -eq 0 ]; then
    echo "Tests passed"
else
    echo "Tests failed"
fi
```

## 🔍 Debugging

For detailed debugging output:
```bash
# Enable verbose mode
set -x
bash tests/comprehensive_cli_test.sh
set +x
```

## 🚀 Next Steps

After tests pass:
1. Run actual TTS generation: `python3 examples/basic_usage.py`
2. Try interactive CLI: `python3 cli/interactive.py`
3. Integrate with AI Content Pipeline
4. Set up automated workflows

---

**Test Suite Version**: 1.0  
**Last Updated**: July 2025  
**Compatibility**: Python 3.12+, ElevenLabs API v2.5+