# AI Content Pipeline Test Suite

This directory contains the consolidated test suite for the AI Content Pipeline package.

## Test Files Overview

### 🧪 `test_core.py`
**Quick smoke tests** for essential functionality validation.

**Purpose**: Fast validation that the package is working correctly  
**Runtime**: ~30 seconds  
**Use when**: Quick sanity checks, CI/CD pipelines, after installation

**Tests**:
- Package import validation
- Pipeline manager initialization
- Model availability check
- Basic chain creation and validation
- Cost estimation functionality
- Console script availability

```bash
python tests/test_core.py
```

### 🔧 `test_integration.py`
**Comprehensive integration tests** for all package features.

**Purpose**: Thorough testing of all components and integrations  
**Runtime**: ~2-3 minutes  
**Use when**: Full validation, before releases, troubleshooting

**Tests**:
- Package installation verification
- Console script functionality (`ai-content-pipeline`, `aicp`)
- YAML configuration loading
- Parallel execution features
- Output directory management
- Model availability across all categories

```bash
python tests/test_integration.py
```

### 🎬 `demo.py`
**Interactive demonstration** of package capabilities.

**Purpose**: Showcase features, onboarding, documentation  
**Runtime**: Interactive (user-controlled)  
**Use when**: Learning the package, demonstrating to others

**Features**:
- Package initialization walkthrough
- Model showcase with examples
- Configuration examples
- YAML loading demonstration
- Parallel execution explanation
- Console command examples
- Package structure overview
- Cost management features

```bash
# Interactive mode (recommended)
python tests/demo.py --interactive

# Non-interactive mode (full demo)
python tests/demo.py
```

## Migration from Old Test Files

The following redundant test files have been consolidated:

| Old File | Consolidated Into | Notes |
|----------|------------------|-------|
| `test_package_basic.py` | `test_core.py` | Basic functionality preserved |
| `test_simple_pipeline.py` | `test_core.py` | Merged with basic tests |
| `test_package_minimal.py` | `test_core.py` | Clean output style preserved |
| `test_package_final.py` | `test_integration.py` | Comprehensive tests enhanced |
| `test_package_demo.py` | `demo.py` | Converted to proper demo script |

## Usage Recommendations

### Development Workflow
1. **After code changes**: Run `python tests/test_core.py`
2. **Before committing**: Run `python tests/test_integration.py`
3. **For demonstrations**: Use `python tests/demo.py --interactive`

### CI/CD Integration
```yaml
# Example GitHub Actions
- name: Quick Tests
  run: python tests/test_core.py

- name: Integration Tests
  run: python tests/test_integration.py
```

### New User Onboarding
1. Start with: `python tests/demo.py --interactive`
2. Validate setup: `python tests/test_core.py`
3. Full verification: `python tests/test_integration.py`

## Test Structure Benefits

### ✅ Reduced Redundancy
- Eliminated 5 similar test files
- Consolidated duplicate functionality
- Cleaner test directory

### ✅ Clear Purpose Separation
- **Core**: Fast validation
- **Integration**: Comprehensive testing
- **Demo**: Interactive exploration

### ✅ Better Maintainability
- Single source of truth for each test type
- Easier to update and extend
- Clear documentation of what each test does

### ✅ Improved User Experience
- Faster feedback with core tests
- Comprehensive validation when needed
- Interactive learning with demo mode

## Adding New Tests

### For Core Functionality
Add to `test_core.py` if the test is:
- Essential for basic operation
- Fast to execute (< 10 seconds)
- Validates core imports/initialization

### For Integration Features
Add to `test_integration.py` if the test:
- Requires external dependencies
- Tests complex interactions
- Validates full workflows

### For Demonstrations
Add to `demo.py` if the feature:
- Showcases package capabilities
- Helps users understand usage
- Provides interactive examples

## Environment Requirements

All tests require:
- Python 3.8+
- Virtual environment activated
- Dependencies installed: `pip install -r requirements.txt`
- Environment variables loaded (`.env` files)

Optional for full functionality:
- FAL API key for model tests
- ElevenLabs API key for TTS tests
- Google Cloud credentials for Veo tests