# Converting AI Content Pipeline to a Python Package

This guide provides step-by-step instructions for transforming the existing `ai_content_pipeline` implementation into a professional Python package.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Current Structure Analysis](#current-structure-analysis)
3. [Package Structure Design](#package-structure-design)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [CLI Integration](#cli-integration)
6. [Testing Setup](#testing-setup)
7. [Documentation](#documentation)
8. [Distribution](#distribution)

## Overview

The `ai_content_pipeline` is currently a functional implementation that needs to be transformed into a distributable Python package with:
- Professional package structure
- CLI interface
- pip installation support
- Comprehensive testing
- Documentation

## Current Structure Analysis

```
ai_content_pipeline/
├── ai_content_pipeline/
│   ├── __init__.py
│   ├── __main__.py
│   ├── models/
│   │   ├── text_to_speech.py
│   │   ├── text_to_image.py
│   │   ├── image_to_image.py
│   │   └── ...
│   ├── pipeline/
│   │   ├── chain.py
│   │   ├── executor.py
│   │   └── parallel_extension.py
│   ├── config/
│   └── utils/
├── input/
├── output/
├── docs/
├── examples/
└── tests/
```

## Package Structure Design

Transform into this structure:

```
ai_content_pipeline/
├── setup.py                      # Package installation script
├── pyproject.toml               # Modern Python packaging
├── README.md                    # Package documentation
├── LICENSE                      # License file
├── MANIFEST.in                  # Include non-Python files
├── requirements.txt             # Dependencies
├── requirements-dev.txt         # Development dependencies
├── ai_content_pipeline/         # Main package
│   ├── __init__.py             # Package initialization
│   ├── __version__.py          # Version information
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── pipeline.py         # Pipeline execution
│   │   ├── executor.py         # Execution engine
│   │   └── parallel.py         # Parallel processing
│   ├── models/                 # AI model integrations
│   │   ├── __init__.py
│   │   ├── base.py            # Base model interface
│   │   ├── text_to_speech.py
│   │   ├── text_to_image.py
│   │   └── ...
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   ├── loader.py          # Config loading
│   │   └── validator.py       # Config validation
│   ├── utils/                  # Utilities
│   │   ├── __init__.py
│   │   ├── file_manager.py
│   │   └── logger.py
│   └── cli/                    # CLI interface
│       ├── __init__.py
│       └── main.py            # Click commands
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py            # pytest configuration
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── docs/                       # Documentation
│   ├── conf.py                # Sphinx config
│   └── index.rst              # Documentation index
└── examples/                   # Example configurations
    └── sample_pipeline.yaml
```

## Step-by-Step Implementation

### Step 1: Create Package Metadata Files

#### 1.1 Create `__version__.py`

```python
# ai_content_pipeline/__version__.py
__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "Unified AI content generation pipeline with parallel execution"
```

#### 1.2 Update `__init__.py`

```python
# ai_content_pipeline/__init__.py
from .__version__ import __version__, __author__, __email__, __description__

# Import main classes for easy access
from .core.pipeline import Pipeline
from .core.executor import PipelineExecutor
from .config.loader import ConfigLoader

__all__ = [
    "__version__",
    "Pipeline",
    "PipelineExecutor", 
    "ConfigLoader"
]
```

### Step 2: Reorganize Core Modules

#### 2.1 Move and refactor pipeline modules

```bash
# Create new structure
mkdir -p ai_content_pipeline/core
mkdir -p ai_content_pipeline/cli

# Move files with refactoring
mv ai_content_pipeline/pipeline/chain.py ai_content_pipeline/core/pipeline.py
mv ai_content_pipeline/pipeline/executor.py ai_content_pipeline/core/executor.py
mv ai_content_pipeline/pipeline/parallel_extension.py ai_content_pipeline/core/parallel.py
```

#### 2.2 Update imports in moved files

```python
# In ai_content_pipeline/core/pipeline.py
# Change: from ai_content_pipeline.models import ...
# To: from ..models import ...

# In ai_content_pipeline/core/executor.py
# Change: from ai_content_pipeline.pipeline.chain import ...
# To: from .pipeline import ...
```

### Step 3: Create CLI Interface

#### 3.1 Create `cli/main.py`

```python
# ai_content_pipeline/cli/main.py
import click
from pathlib import Path
from ..core.pipeline import Pipeline
from ..core.executor import PipelineExecutor
from ..config.loader import ConfigLoader

@click.group()
@click.version_option()
def cli():
    """AI Content Pipeline - Unified content generation with parallel execution."""
    pass

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--parallel/--no-parallel', default=True, help='Enable parallel execution')
@click.option('--max-workers', type=int, help='Maximum worker threads')
@click.option('--output-dir', type=click.Path(), help='Override output directory')
@click.option('--dry-run', is_flag=True, help='Validate and estimate costs without execution')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--no-confirm', is_flag=True, help='Skip confirmation prompts')
def run(config_file, parallel, max_workers, output_dir, dry_run, verbose, no_confirm):
    """Run a pipeline from configuration file."""
    # Load configuration
    loader = ConfigLoader()
    config = loader.load_config(config_file)
    
    # Override settings if provided
    if output_dir:
        config.output_directory = output_dir
    
    # Create executor
    if parallel:
        from ..core.parallel import ParallelExecutor
        executor = ParallelExecutor(config, max_workers=max_workers)
    else:
        executor = PipelineExecutor(config)
    
    # Execute pipeline
    if dry_run:
        executor.validate()
        click.echo("Validation successful. Estimated cost: $X.XX")
    else:
        if not no_confirm:
            click.confirm("Proceed with pipeline execution?", abort=True)
        result = executor.execute()
        click.echo(f"Pipeline completed: {result}")

@cli.command()
def list_models():
    """List available AI models."""
    from ..models import get_available_models
    models = get_available_models()
    for category, model_list in models.items():
        click.echo(f"\n{category}:")
        for model in model_list:
            click.echo(f"  - {model}")

if __name__ == '__main__':
    cli()
```

### Step 4: Create Setup Files

#### 4.1 Create `setup.py`

```python
# setup.py
from setuptools import setup, find_packages
from pathlib import Path

# Read version
exec(open('ai_content_pipeline/__version__.py').read())

# Read README
long_description = Path('README.md').read_text()

setup(
    name="ai-content-pipeline",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-content-pipeline",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "aiohttp>=3.8.0",
        "aiofiles>=23.0.0",
        "fal-client>=0.4.0",
        "elevenlabs>=0.2.0",
        "google-generativeai>=0.3.0",
        "openai>=1.0.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-pipeline=ai_content_pipeline.cli.main:cli",
            "aipipe=ai_content_pipeline.cli.main:cli",  # Short alias
        ],
    },
    include_package_data=True,
    package_data={
        "ai_content_pipeline": ["examples/*.yaml", "docs/*.md"],
    },
)
```

#### 4.2 Create `pyproject.toml`

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-content-pipeline"
dynamic = ["version"]
description = "Unified AI content generation pipeline with parallel execution"
readme = "README.md"
license = {text = "MIT"}
authors = [{name = "Your Name", email = "your.email@example.com"}]
keywords = ["ai", "content generation", "pipeline", "parallel processing"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
]
requires-python = ">=3.8"

[project.urls]
Homepage = "https://github.com/yourusername/ai-content-pipeline"
Documentation = "https://ai-content-pipeline.readthedocs.io"
Repository = "https://github.com/yourusername/ai-content-pipeline.git"

[project.scripts]
ai-pipeline = "ai_content_pipeline.cli.main:cli"
aipipe = "ai_content_pipeline.cli.main:cli"

[tool.setuptools.dynamic]
version = {attr = "ai_content_pipeline.__version__.__version__"}
```

### Step 5: Create Tests

#### 5.1 Create `tests/conftest.py`

```python
# tests/conftest.py
import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)

@pytest.fixture
def sample_config():
    """Sample pipeline configuration."""
    return {
        "pipeline_name": "test_pipeline",
        "description": "Test pipeline",
        "output_directory": "output",
        "steps": [
            {
                "step_type": "text_to_speech",
                "config": {
                    "text": "Hello world",
                    "voice": "adam"
                }
            }
        ]
    }
```

#### 5.2 Create basic tests

```python
# tests/unit/test_pipeline.py
import pytest
from ai_content_pipeline.core.pipeline import Pipeline

def test_pipeline_creation(sample_config):
    """Test pipeline creation."""
    pipeline = Pipeline(sample_config)
    assert pipeline.name == "test_pipeline"
    assert len(pipeline.steps) == 1

def test_pipeline_validation(sample_config):
    """Test pipeline validation."""
    pipeline = Pipeline(sample_config)
    assert pipeline.validate() is True
```

### Step 6: Update Documentation

#### 6.1 Create proper `README.md`

```markdown
# AI Content Pipeline

A unified AI content generation pipeline with parallel execution support.

## Features

- 🔄 Chain multiple AI operations (text → image → video → audio)
- ⚡ Parallel execution with 2-3x speedup
- 📝 YAML-based configuration
- 💰 Cost estimation and management
- 🎯 Multiple AI service integration

## Installation

```bash
pip install ai-content-pipeline
```

## Quick Start

```bash
# Run a pipeline
ai-pipeline run config.yaml

# With parallel execution
ai-pipeline run config.yaml --parallel

# List available models
ai-pipeline list-models
```

## Configuration Example

```yaml
pipeline_name: "content_generation"
description: "Generate multimedia content"
output_directory: "output"

steps:
  - step_type: "text_to_speech"
    config:
      text: "Welcome to AI Content Pipeline"
      voice: "rachel"
```

## Development

```bash
# Clone repository
git clone https://github.com/yourusername/ai-content-pipeline
cd ai-content-pipeline

# Install in development mode
pip install -e .[dev]

# Run tests
pytest
```
```

### Step 7: Create Additional Files

#### 7.1 Create `MANIFEST.in`

```
# MANIFEST.in
include README.md
include LICENSE
include requirements.txt
recursive-include ai_content_pipeline/examples *.yaml
recursive-include ai_content_pipeline/docs *.md
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

#### 7.2 Create `requirements-dev.txt`

```
# requirements-dev.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-asyncio>=0.21.0
black>=22.0.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.0.0
sphinx>=6.0.0
```

### Step 8: Final Migration Steps

```bash
# 1. Install the package in development mode
pip install -e .

# 2. Run tests
pytest

# 3. Build distribution
python -m build

# 4. Test installation
pip install dist/ai_content_pipeline-1.0.0-py3-none-any.whl

# 5. Test CLI
ai-pipeline --help
ai-pipeline run examples/sample_pipeline.yaml
```

## Summary

This guide transforms the existing `ai_content_pipeline` into a professional Python package with:

1. **Proper package structure** with clear module organization
2. **CLI interface** using Click for easy command-line usage
3. **Setup files** for pip installation
4. **Test framework** for quality assurance
5. **Documentation** for users and developers
6. **Distribution ready** for PyPI publishing

The key differences from the `ai_content_platform` implementation:
- Keeps the existing functionality intact
- Minimal refactoring of existing code
- Focuses on packaging the current implementation
- Simpler structure without full service abstractions

Follow these steps sequentially to convert your working pipeline into a distributable package!