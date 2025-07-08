# Repository Organization Guide for Multiple Packages

## 🎯 Current Situation

You have multiple implementations that could each become packages:
- `ai_content_pipeline` - Original unified pipeline
- `ai_content_platform` - New comprehensive platform
- `veo3_video_generation` - Google Veo implementation
- `fal_video_generation` - FAL AI video generation
- `fal_text_to_video` - FAL AI text-to-video
- `fal_avatar_generation` - FAL AI avatar generation
- `fal_text_to_image` - FAL AI text-to-image
- `fal_image_to_image` - FAL AI image-to-image
- `fal_video_to_video` - FAL AI video-to-video
- `text_to_speech` - ElevenLabs TTS package
- `video_tools` - Video processing utilities

## 📊 Organization Options

### Option 1: Monorepo with Multiple Packages (Recommended)

```
ai-content-generation/
├── README.md                          # Main repository documentation
├── .gitignore                         # Repository-wide gitignore
├── .github/                           # GitHub Actions for all packages
│   └── workflows/
│       ├── test-all.yml              # Test all packages
│       └── release.yml               # Release automation
├── docs/                             # Shared documentation
│   ├── architecture.md
│   └── contributing.md
├── scripts/                          # Shared scripts
│   ├── test-all.sh
│   └── build-all.sh
├── packages/                         # All packages organized here
│   ├── core/                         # Core/shared packages
│   │   ├── ai-content-platform/      # Main platform package
│   │   │   ├── setup.py
│   │   │   ├── pyproject.toml
│   │   │   └── ai_content_platform/
│   │   └── ai-content-pipeline/      # Pipeline package
│   │       ├── setup.py
│   │       └── ai_content_pipeline/
│   ├── providers/                    # Provider-specific packages
│   │   ├── google-veo/              # Google Veo package
│   │   │   ├── setup.py
│   │   │   └── google_veo/
│   │   └── fal-ai/                  # FAL AI packages
│   │       ├── fal-video/           # Video generation
│   │       ├── fal-text-to-video/   # Text to video
│   │       ├── fal-avatar/          # Avatar generation
│   │       ├── fal-text-to-image/   # Text to image
│   │       ├── fal-image-to-image/  # Image to image
│   │       └── fal-video-to-video/  # Video to video
│   ├── services/                    # Service packages
│   │   ├── text-to-speech/          # TTS package
│   │   │   ├── setup.py
│   │   │   └── text_to_speech/
│   │   └── video-tools/             # Video tools package
│   │       ├── setup.py
│   │       └── video_tools/
│   └── examples/                    # Example projects
│       ├── simple-pipeline/
│       └── enterprise-setup/
├── requirements/                    # Shared requirements
│   ├── base.txt
│   ├── dev.txt
│   └── test.txt
└── Makefile                        # Common operations
```

### Option 2: Namespace Packages

```
ai-content-generation/
├── packages/
│   ├── aicp-core/                  # Core platform
│   │   ├── setup.py (name="aicp-core")
│   │   └── aicp/
│   │       └── core/
│   ├── aicp-fal-video/            # FAL video plugin
│   │   ├── setup.py (name="aicp-fal-video")
│   │   └── aicp/
│   │       └── fal/
│   │           └── video/
│   └── aicp-google-veo/           # Google Veo plugin
│       ├── setup.py (name="aicp-google-veo")
│       └── aicp/
│           └── google/
│               └── veo/
```

Usage with namespace packages:
```python
from aicp.core import Pipeline
from aicp.fal.video import VideoGenerator
from aicp.google.veo import VeoGenerator
```

### Option 3: Plugin Architecture

```
ai-content-generation/
├── core/                           # Main platform
│   ├── ai-content-platform/
│   │   ├── setup.py
│   │   └── ai_content_platform/
│   │       └── plugins/           # Plugin system
├── plugins/                       # Installable plugins
│   ├── plugin-fal-video/
│   │   ├── setup.py
│   │   └── aicp_fal_video/
│   ├── plugin-google-veo/
│   └── plugin-elevenlabs/
└── standalone/                    # Standalone packages
    ├── video-tools/
    └── legacy-pipeline/
```

## 🚀 Recommended Approach: Monorepo with Categories

### Step 1: Create New Directory Structure

```bash
# Create the new structure
mkdir -p ai-content-generation/{packages/{core,providers,services},docs,scripts,tests}

# Move existing packages
mv ai_content_platform ai-content-generation/packages/core/
mv ai_content_pipeline ai-content-generation/packages/core/
mv veo3_video_generation ai-content-generation/packages/providers/google-veo/
mv fal_* ai-content-generation/packages/providers/fal-ai/
mv text_to_speech ai-content-generation/packages/services/
mv video_tools ai-content-generation/packages/services/
```

### Step 2: Create Root Configuration Files

#### Root `pyproject.toml` (for workspace)
```toml
# pyproject.toml
[tool.poetry]
name = "ai-content-generation"
version = "1.0.0"
description = "AI Content Generation Suite"

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "^22.0.0"
isort = "^5.12.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# Workspace members
[tool.poetry.packages]
include = [
    { path = "packages/core/ai-content-platform" },
    { path = "packages/core/ai-content-pipeline" },
    { path = "packages/providers/google-veo" },
    { path = "packages/providers/fal-ai/*" },
    { path = "packages/services/*" }
]
```

#### Root `Makefile`
```makefile
# Makefile
.PHONY: install test lint format clean

install:
	@echo "Installing all packages in development mode..."
	@for pkg in packages/*/*/setup.py; do \
		dir=$$(dirname $$pkg); \
		echo "Installing $$dir..."; \
		pip install -e $$dir; \
	done

test:
	@echo "Running tests for all packages..."
	pytest packages/

lint:
	@echo "Linting all packages..."
	black --check packages/
	isort --check-only packages/
	flake8 packages/

format:
	@echo "Formatting all packages..."
	black packages/
	isort packages/

build:
	@echo "Building all packages..."
	@for pkg in packages/*/*/setup.py; do \
		dir=$$(dirname $$pkg); \
		echo "Building $$dir..."; \
		cd $$dir && python -m build; \
	done

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
```

### Step 3: Package Naming Convention

```python
# Package names on PyPI
ai-content-platform      # Main platform
ai-content-pipeline      # Pipeline implementation
aicp-google-veo         # Google Veo provider
aicp-fal-video          # FAL video provider
aicp-fal-text-to-video  # FAL text-to-video
aicp-fal-avatar         # FAL avatar
aicp-text-to-speech     # TTS service
aicp-video-tools        # Video tools

# Import names
import ai_content_platform
import ai_content_pipeline
import aicp_google_veo
import aicp_fal_video
```

### Step 4: Dependency Management

#### For Core Platform (`packages/core/ai-content-platform/setup.py`)
```python
setup(
    name="ai-content-platform",
    install_requires=[
        # Core dependencies only
        "click>=8.0.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "fal": ["aicp-fal-video>=1.0.0", "aicp-fal-text-to-video>=1.0.0"],
        "google": ["aicp-google-veo>=1.0.0"],
        "tts": ["aicp-text-to-speech>=1.0.0"],
        "all": ["aicp-fal-video>=1.0.0", "aicp-google-veo>=1.0.0", ...],
    }
)
```

#### For Provider Packages
```python
# packages/providers/fal-ai/fal-video/setup.py
setup(
    name="aicp-fal-video",
    install_requires=[
        "ai-content-platform>=1.0.0",  # Depends on core
        "fal-client>=0.4.0",
    ]
)
```

### Step 5: Create Shared Documentation

#### `docs/README.md`
```markdown
# AI Content Generation Suite

A comprehensive suite of AI content generation tools.

## Packages

### Core Packages
- **ai-content-platform**: Main platform with CLI and orchestration
- **ai-content-pipeline**: Legacy pipeline implementation

### Provider Packages
- **aicp-google-veo**: Google Veo video generation
- **aicp-fal-video**: FAL AI video generation
- **aicp-fal-text-to-video**: FAL AI text-to-video
- **aicp-fal-avatar**: FAL AI avatar generation

### Service Packages
- **aicp-text-to-speech**: Text-to-speech service
- **aicp-video-tools**: Video processing utilities

## Installation

```bash
# Install core platform
pip install ai-content-platform

# Install with all providers
pip install ai-content-platform[all]

# Install specific providers
pip install ai-content-platform[fal,google]
```

## Development

```bash
# Clone repository
git clone https://github.com/yourusername/ai-content-generation
cd ai-content-generation

# Install all packages in development mode
make install

# Run tests
make test

# Format code
make format
```
```

### Step 6: CI/CD Configuration

#### `.github/workflows/test-all.yml`
```yaml
name: Test All Packages

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package:
          - packages/core/ai-content-platform
          - packages/core/ai-content-pipeline
          - packages/providers/google-veo
          - packages/providers/fal-ai/fal-video
          - packages/services/text-to-speech
          - packages/services/video-tools
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -e ${{ matrix.package }}[dev]
    
    - name: Run tests
      run: |
        cd ${{ matrix.package }}
        pytest
```

## 🎯 Benefits of This Approach

1. **Clear Organization**: Packages grouped by type (core, providers, services)
2. **Independent Versioning**: Each package can have its own version
3. **Selective Installation**: Users only install what they need
4. **Shared Infrastructure**: Common CI/CD, documentation, scripts
5. **Easy Development**: Single repo for all development
6. **Dependency Management**: Clear dependency hierarchy

## 🔄 Migration Path

1. **Phase 1**: Reorganize into monorepo structure
2. **Phase 2**: Update imports and dependencies
3. **Phase 3**: Add proper packaging to each component
4. **Phase 4**: Set up CI/CD and documentation
5. **Phase 5**: Publish to PyPI (optional)

## 📝 Summary

The monorepo approach with categorized packages provides:
- **Organization**: Clear structure with core/providers/services
- **Flexibility**: Each package can evolve independently
- **Usability**: Users can install only what they need
- **Maintainability**: Shared tooling and infrastructure
- **Scalability**: Easy to add new providers or services

This structure supports both the current development needs and future growth while maintaining clean separation of concerns.