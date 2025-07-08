#!/usr/bin/env python3
"""Script to reorganize repository into proper package structure."""

import os
import shutil
from pathlib import Path

def create_package_structure():
    """Create the new package directory structure."""
    base_dir = Path(".")
    
    # Create main structure
    package_dirs = [
        "packages/core",
        "packages/providers/google", 
        "packages/providers/fal",
        "packages/services",
        "shared/docs",
        "shared/scripts", 
        "shared/examples",
        "shared/requirements"
    ]
    
    for directory in package_dirs:
        (base_dir / directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def move_packages():
    """Move existing packages to new structure."""
    moves = [
        # Core packages
        ("ai_content_platform", "packages/core/ai-content-platform"),
        ("ai_content_pipeline", "packages/core/ai-content-pipeline"),
        
        # Google providers
        ("veo3_video_generation", "packages/providers/google/veo"),
        
        # FAL providers
        ("fal_video_generation", "packages/providers/fal/video"),
        ("fal_text_to_video", "packages/providers/fal/text-to-video"),
        ("fal_avatar_generation", "packages/providers/fal/avatar"),
        ("fal_text_to_image", "packages/providers/fal/text-to-image"),
        ("fal_image_to_image", "packages/providers/fal/image-to-image"),
        ("fal_video_to_video", "packages/providers/fal/video-to-video"),
        ("fal_image_to_video", "packages/providers/fal/image-to-video"),
        
        # Services
        ("text_to_speech", "packages/services/text-to-speech"),
        ("video_tools", "packages/services/video-tools"),
        
        # Shared resources
        ("docs", "shared/docs"),
        ("requirements", "shared/requirements"),
    ]
    
    for source, destination in moves:
        source_path = Path(source)
        dest_path = Path(destination)
        
        if source_path.exists():
            # Create parent directory
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"📦 Moving {source} → {destination}")
            shutil.move(str(source_path), str(dest_path))
        else:
            print(f"⚠️  Source not found: {source}")

def create_root_files():
    """Create root configuration files."""
    
    # Root README.md
    readme_content = """# AI Content Generation Suite

A comprehensive monorepo containing multiple AI content generation packages.

## 📦 Packages

### Core Packages
- **[ai-content-platform](packages/core/ai-content-platform/)** - Main platform with CLI
- **[ai-content-pipeline](packages/core/ai-content-pipeline/)** - Legacy pipeline implementation

### Provider Packages

#### Google Services
- **[google-veo](packages/providers/google/veo/)** - Google Veo video generation

#### FAL AI Services  
- **[fal-video](packages/providers/fal/video/)** - Video generation
- **[fal-text-to-video](packages/providers/fal/text-to-video/)** - Text-to-video
- **[fal-avatar](packages/providers/fal/avatar/)** - Avatar generation
- **[fal-text-to-image](packages/providers/fal/text-to-image/)** - Text-to-image
- **[fal-image-to-image](packages/providers/fal/image-to-image/)** - Image transformation
- **[fal-video-to-video](packages/providers/fal/video-to-video/)** - Video processing

### Service Packages
- **[text-to-speech](packages/services/text-to-speech/)** - TTS services
- **[video-tools](packages/services/video-tools/)** - Video processing utilities

## 🚀 Quick Start

```bash
# Install all packages in development mode
make install-dev

# Run tests for all packages
make test-all

# Build all packages
make build-all
```

## 📚 Documentation

See [shared/docs/](shared/docs/) for comprehensive documentation.
"""
    
    # Root Makefile
    makefile_content = """# AI Content Generation Suite Makefile

.PHONY: install-dev test-all build-all clean format lint

# Install all packages in development mode
install-dev:
	@echo "🔧 Installing all packages in development mode..."
	@find packages -name "setup.py" -exec dirname {} \\; | while read dir; do \\
		echo "Installing $$dir..."; \\
		pip install -e $$dir; \\
	done

# Run tests for all packages
test-all:
	@echo "🧪 Running tests for all packages..."
	@find packages -name "tests" -type d | while read testdir; do \\
		echo "Testing $$testdir..."; \\
		cd "$$(dirname $$testdir)" && python -m pytest tests/; \\
	done

# Build all packages
build-all:
	@echo "📦 Building all packages..."
	@find packages -name "setup.py" -exec dirname {} \\; | while read dir; do \\
		echo "Building $$dir..."; \\
		cd $$dir && python -m build; \\
	done

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true

# Format code
format:
	@echo "🎨 Formatting code..."
	@black packages/
	@isort packages/

# Lint code
lint:
	@echo "🔍 Linting code..."
	@flake8 packages/
	@black --check packages/
	@isort --check-only packages/
"""
    
    # Root pyproject.toml
    pyproject_content = """[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\\.pyi?$'
extend-exclude = '''
/(
  \\.eggs
  | \\.git
  | \\.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88

[tool.pytest.ini_options]
testpaths = ["packages"]
python_files = ["test_*.py", "*_test.py"]
addopts = [
    "--strict-markers",
    "--strict-config",
]
"""
    
    # Write files
    Path("README.md").write_text(readme_content)
    Path("Makefile").write_text(makefile_content)
    Path("pyproject.toml").write_text(pyproject_content)
    
    print("✅ Created root configuration files")

def create_package_init_files():
    """Create __init__.py files for each package."""
    package_dirs = [
        "packages/core/ai-content-platform/ai_content_platform",
        "packages/core/ai-content-pipeline/ai_content_pipeline", 
        "packages/providers/google/veo/google_veo",
        "packages/providers/fal/video/fal_video",
        "packages/providers/fal/text-to-video/fal_text_to_video",
        "packages/providers/fal/avatar/fal_avatar",
        "packages/providers/fal/text-to-image/fal_text_to_image",
        "packages/providers/fal/image-to-image/fal_image_to_image",
        "packages/providers/fal/video-to-video/fal_video_to_video",
        "packages/services/text-to-speech/text_to_speech",
        "packages/services/video-tools/video_tools",
    ]
    
    for package_dir in package_dirs:
        init_file = Path(package_dir) / "__init__.py"
        if not init_file.exists():
            init_file.parent.mkdir(parents=True, exist_ok=True)
            init_file.touch()
            print(f"✅ Created {init_file}")

def main():
    """Main reorganization function."""
    print("🚀 Starting repository reorganization...")
    
    # Create structure
    create_package_structure()
    
    # Move packages
    move_packages()
    
    # Create root files
    create_root_files()
    
    # Create package init files
    create_package_init_files()
    
    print("✅ Repository reorganization complete!")
    print("\n📋 Next steps:")
    print("1. Run: make install-dev")
    print("2. Run: make test-all")
    print("3. Review and update package configurations")

if __name__ == "__main__":
    main()