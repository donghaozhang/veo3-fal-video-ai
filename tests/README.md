# AI Content Pipeline Tests

This folder contains various test scripts to validate the AI Content Pipeline package functionality.

## Test Files

### 📋 test_package_basic.py
**Purpose**: Basic functionality test for the AI Content Pipeline package
- Tests package imports using installed package structure
- Validates pipeline manager initialization
- Tests chain creation and validation
- Tests YAML configuration loading
- Shows available models across all categories

**Run**: `python tests/test_package_basic.py`

### 🚀 test_simple_pipeline.py
**Purpose**: Simple pipeline functionality test
- Tests basic pipeline manager functionality
- Creates and validates simple chains
- Uses proper installed package imports
- Tests chain creation from configuration

**Run**: `python tests/test_simple_pipeline.py`

### 🎯 test_package_minimal.py
**Purpose**: Minimal test with clean output
- Tests core functionality without verbose output
- Validates package imports
- Checks model availability
- Tests console script functionality
- Suppresses warnings for cleaner output

**Run**: `python tests/test_package_minimal.py`

### 🎬 test_package_demo.py
**Purpose**: Comprehensive demonstration of package capabilities
- Shows all available AI models
- Demonstrates configuration loading
- Displays package structure
- Shows console script commands
- Provides usage examples

**Run**: `python tests/test_package_demo.py`

### ✅ test_package_final.py
**Purpose**: Final comprehensive test suite
- Tests package installation
- Validates console scripts (ai-content-pipeline, aicp)
- Tests YAML configuration loading
- Tests parallel execution feature
- Tests output directory management
- Provides complete test summary

**Run**: `python tests/test_package_final.py`

## Running All Tests

To run all tests, activate the virtual environment first:

```bash
# Activate virtual environment
source venv/bin/activate

# Run individual tests
python tests/test_package_basic.py
python tests/test_simple_pipeline.py
python tests/test_package_minimal.py
python tests/test_package_demo.py
python tests/test_package_final.py
```

## Test Results

All tests should pass successfully, confirming:
- ✅ Package installation works correctly
- ✅ All 28+ AI models are available
- ✅ Console scripts function properly
- ✅ YAML configuration loading works
- ✅ Chain creation and validation succeeds
- ✅ Cost estimation functions correctly
- ✅ Parallel execution can be enabled
- ✅ Output management works as expected

## Notes

- All tests use the installed package structure (no sys.path manipulation)
- Tests validate the consolidated package after reorganization
- Console scripts `ai-content-pipeline` and `aicp` are tested
- The package supports 28 AI models across 7 categories:
  - Text-to-Image (4 models)
  - Image Understanding (7 models)
  - Prompt Generation (5 models)
  - Image-to-Image (6 models)
  - Image-to-Video (4 models)
  - Add Audio (1 model)
  - Upscale Video (1 model)