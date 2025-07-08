# AI Content Generation Platform - Package Creation Guide (Part 6)

## 🧪 Phase 6: Testing, Documentation, CI/CD, and Distribution

### Step 6.1: Testing Framework Structure

Create comprehensive testing structure:
```bash
# Create testing directory structure
mkdir -p tests/{unit,integration,fixtures,mocks}

# Create test files
touch tests/__init__.py
touch tests/conftest.py
touch tests/test_utils.py

# Unit tests
touch tests/unit/__init__.py
touch tests/unit/test_core_models.py
touch tests/unit/test_pipeline_executor.py
touch tests/unit/test_step_factory.py
touch tests/unit/test_validators.py
touch tests/unit/test_cost_calculator.py
touch tests/unit/test_config_loader.py
touch tests/unit/test_file_manager.py

# Integration tests
touch tests/integration/__init__.py
touch tests/integration/test_pipeline_integration.py
touch tests/integration/test_service_integration.py
touch tests/integration/test_cli_integration.py

# Test fixtures and mocks
touch tests/fixtures/__init__.py
touch tests/fixtures/sample_configs.py
touch tests/mocks/__init__.py
touch tests/mocks/service_mocks.py
```

### Step 6.2: Test Configuration and Fixtures

Create `tests/conftest.py`:
```python
"""Test configuration and fixtures for AI Content Platform."""

import pytest
import tempfile
import os
from pathlib import Path
from typing import Dict, Any
from unittest.mock import MagicMock, patch

from ai_content_platform.core.models import PipelineConfig, StepConfig, StepType
from ai_content_platform.utils.logger import setup_logging


# Setup test logging
setup_logging(level="DEBUG")


@pytest.fixture(scope="session")
def temp_dir():
    """Create temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_text_to_speech_config():
    """Sample text-to-speech step configuration."""
    return StepConfig(
        step_type=StepType.TEXT_TO_SPEECH,
        config={
            "text": "Hello, this is a test message",
            "voice": "Rachel",
            "model": "eleven_monolingual_v1"
        },
        output_filename="test_speech.mp3"
    )


@pytest.fixture
def sample_text_to_image_config():
    """Sample text-to-image step configuration."""
    return StepConfig(
        step_type=StepType.TEXT_TO_IMAGE,
        config={
            "prompt": "A beautiful sunset over mountains",
            "model": "flux-dev",
            "image_size": "landscape_16_9",
            "num_images": 1
        },
        output_filename="test_image.png"
    )


@pytest.fixture
def sample_pipeline_config(sample_text_to_speech_config, sample_text_to_image_config):
    """Sample pipeline configuration."""
    return PipelineConfig(
        pipeline_name="test_pipeline",
        description="Test pipeline for unit tests",
        output_directory="test_output",
        steps=[sample_text_to_speech_config, sample_text_to_image_config],
        global_config={
            "parallel_enabled": False,
            "cost_limit": 5.0,
            "timeout": 300
        }
    )


@pytest.fixture
def sample_parallel_pipeline_config():
    """Sample parallel pipeline configuration."""
    from ai_content_platform.core.models import ParallelStepConfig, ParallelConfig, MergeStrategy
    
    parallel_step = ParallelStepConfig(
        parallel_config=ParallelConfig(
            merge_strategy=MergeStrategy.COLLECT_ALL,
            max_workers=2
        ),
        steps=[
            StepConfig(
                step_type=StepType.TEXT_TO_SPEECH,
                config={"text": "First voice", "voice": "Adam"},
                output_filename="voice1.mp3"
            ),
            StepConfig(
                step_type=StepType.TEXT_TO_SPEECH,
                config={"text": "Second voice", "voice": "Rachel"},
                output_filename="voice2.mp3"
            )
        ]
    )
    
    return PipelineConfig(
        pipeline_name="parallel_test_pipeline",
        description="Parallel execution test pipeline",
        output_directory="parallel_output",
        steps=[parallel_step]
    )


@pytest.fixture
def mock_fal_client():
    """Mock FAL client for testing."""
    with patch('fal_client.submit') as mock_submit:
        mock_handler = MagicMock()
        mock_handler.get.return_value = {
            'images': [{'url': 'http://example.com/test.png'}],
            'video': {'url': 'http://example.com/test.mp4'}
        }
        mock_submit.return_value = mock_handler
        yield mock_submit


@pytest.fixture
def mock_elevenlabs():
    """Mock ElevenLabs for testing."""
    with patch('elevenlabs.generate') as mock_generate, \
         patch('elevenlabs.save') as mock_save:
        mock_generate.return_value = b"fake_audio_data"
        yield mock_generate, mock_save


@pytest.fixture
def mock_aiohttp_session():
    """Mock aiohttp session for file downloads."""
    with patch('aiohttp.ClientSession') as mock_session:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.content.iter_chunked.return_value = [b"chunk1", b"chunk2"]
        
        mock_context = MagicMock()
        mock_context.__aenter__.return_value = mock_response
        mock_context.__aexit__.return_value = None
        
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_context
        mock_session_instance.__aenter__.return_value = mock_session_instance
        mock_session_instance.__aexit__.return_value = None
        
        mock_session.return_value = mock_session_instance
        yield mock_session


@pytest.fixture
def environment_variables():
    """Set up test environment variables."""
    test_env = {
        'FAL_KEY': 'test_fal_key_12345',
        'ELEVENLABS_API_KEY': 'test_elevenlabs_key_67890',
        'OPENROUTER_API_KEY': 'test_openrouter_key_abcdef',
        'PIPELINE_PARALLEL_ENABLED': 'false'
    }
    
    original_env = {}
    for key, value in test_env.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value
    
    yield test_env
    
    # Restore original environment
    for key, original_value in original_env.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value


@pytest.fixture
def sample_yaml_config(temp_dir):
    """Create sample YAML configuration file."""
    config_content = """
pipeline_name: "test_yaml_pipeline"
description: "Test YAML configuration"
output_directory: "yaml_output"
global_config:
  parallel_enabled: false
  cost_limit: 3.0
steps:
  - step_type: "text_to_speech"
    config:
      text: "YAML test message"
      voice: "Rachel"
    output_filename: "yaml_test.mp3"
"""
    
    config_file = temp_dir / "test_config.yaml"
    config_file.write_text(config_content.strip())
    return config_file


@pytest.fixture
def sample_json_config(temp_dir):
    """Create sample JSON configuration file."""
    import json
    
    config_data = {
        "pipeline_name": "test_json_pipeline",
        "description": "Test JSON configuration",
        "output_directory": "json_output",
        "global_config": {
            "parallel_enabled": False,
            "cost_limit": 4.0
        },
        "steps": [
            {
                "step_type": "text_to_image",
                "config": {
                    "prompt": "JSON test image",
                    "model": "flux-dev"
                },
                "output_filename": "json_test.png"
            }
        ]
    }
    
    config_file = temp_dir / "test_config.json"
    config_file.write_text(json.dumps(config_data, indent=2))
    return config_file


# Pytest markers for test categories
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.slow = pytest.mark.slow
```

### Step 6.3: Unit Tests for Core Models

Create `tests/unit/test_core_models.py`:
```python
"""Unit tests for core models."""

import pytest
from pydantic import ValidationError

from ai_content_platform.core.models import (
    StepType, StepConfig, PipelineConfig, ParallelStepConfig,
    ParallelConfig, MergeStrategy, StepResult, PipelineResult
)


class TestStepConfig:
    """Test StepConfig model."""
    
    def test_valid_step_config(self):
        """Test creating valid step configuration."""
        config = StepConfig(
            step_type=StepType.TEXT_TO_SPEECH,
            config={"text": "Hello world", "voice": "Rachel"},
            output_filename="test.mp3"
        )
        
        assert config.step_type == StepType.TEXT_TO_SPEECH
        assert config.config["text"] == "Hello world"
        assert config.output_filename == "test.mp3"
        assert config.enabled is True
        assert config.retry_count == 0
    
    def test_step_config_defaults(self):
        """Test step configuration defaults."""
        config = StepConfig(
            step_type=StepType.TEXT_TO_IMAGE,
            config={"prompt": "test"}
        )
        
        assert config.enabled is True
        assert config.retry_count == 0
        assert config.timeout is None
        assert config.output_filename is None
    
    def test_invalid_step_type(self):
        """Test invalid step type raises error."""
        with pytest.raises(ValidationError):
            StepConfig(
                step_type="invalid_type",
                config={"test": "value"}
            )


class TestParallelConfig:
    """Test ParallelConfig model."""
    
    def test_valid_parallel_config(self):
        """Test creating valid parallel configuration."""
        config = ParallelConfig(
            merge_strategy=MergeStrategy.COLLECT_ALL,
            max_workers=4,
            timeout=120
        )
        
        assert config.merge_strategy == MergeStrategy.COLLECT_ALL
        assert config.max_workers == 4
        assert config.timeout == 120
    
    def test_parallel_config_defaults(self):
        """Test parallel configuration defaults."""
        config = ParallelConfig()
        
        assert config.merge_strategy == MergeStrategy.COLLECT_ALL
        assert config.max_workers is None
        assert config.timeout is None


class TestPipelineConfig:
    """Test PipelineConfig model."""
    
    def test_valid_pipeline_config(self, sample_text_to_speech_config):
        """Test creating valid pipeline configuration."""
        config = PipelineConfig(
            pipeline_name="test_pipeline",
            description="Test description",
            output_directory="test_output",
            steps=[sample_text_to_speech_config]
        )
        
        assert config.pipeline_name == "test_pipeline"
        assert config.description == "Test description"
        assert config.output_directory == "test_output"
        assert len(config.steps) == 1
        assert config.global_config == {}
    
    def test_pipeline_config_validation(self):
        """Test pipeline configuration validation."""
        # Missing pipeline_name should raise error
        with pytest.raises(ValidationError):
            PipelineConfig(
                output_directory="test",
                steps=[]
            )
        
        # Empty pipeline_name should raise error
        with pytest.raises(ValidationError):
            PipelineConfig(
                pipeline_name="",
                output_directory="test",
                steps=[]
            )


class TestStepResult:
    """Test StepResult model."""
    
    def test_successful_step_result(self):
        """Test creating successful step result."""
        result = StepResult(
            step_id="test_step_123",
            step_type=StepType.TEXT_TO_SPEECH,
            success=True,
            output_path="/path/to/output.mp3",
            execution_time=2.5,
            cost=0.05
        )
        
        assert result.step_id == "test_step_123"
        assert result.step_type == StepType.TEXT_TO_SPEECH
        assert result.success is True
        assert result.output_path == "/path/to/output.mp3"
        assert result.execution_time == 2.5
        assert result.cost == 0.05
        assert result.error is None
    
    def test_failed_step_result(self):
        """Test creating failed step result."""
        result = StepResult(
            step_id="failed_step_456",
            step_type=StepType.TEXT_TO_IMAGE,
            success=False,
            error="API key invalid",
            execution_time=1.0
        )
        
        assert result.success is False
        assert result.error == "API key invalid"
        assert result.output_path is None
        assert result.cost is None


class TestPipelineResult:
    """Test PipelineResult model."""
    
    def test_successful_pipeline_result(self):
        """Test creating successful pipeline result."""
        step_result = StepResult(
            step_id="step1",
            step_type=StepType.TEXT_TO_SPEECH,
            success=True,
            cost=0.05
        )
        
        result = PipelineResult(
            pipeline_name="test_pipeline",
            success=True,
            total_steps=1,
            successful_steps=1,
            failed_steps=0,
            total_execution_time=5.0,
            total_cost=0.05,
            step_results=[step_result],
            output_directory="output"
        )
        
        assert result.pipeline_name == "test_pipeline"
        assert result.success is True
        assert result.total_steps == 1
        assert result.successful_steps == 1
        assert result.failed_steps == 0
        assert result.total_cost == 0.05
        assert len(result.step_results) == 1
    
    def test_failed_pipeline_result(self):
        """Test creating failed pipeline result."""
        failed_step = StepResult(
            step_id="step1",
            step_type=StepType.TEXT_TO_SPEECH,
            success=False,
            error="Service unavailable"
        )
        
        result = PipelineResult(
            pipeline_name="failed_pipeline",
            success=False,
            total_steps=1,
            successful_steps=0,
            failed_steps=1,
            total_execution_time=2.0,
            total_cost=0.0,
            step_results=[failed_step],
            output_directory="output"
        )
        
        assert result.success is False
        assert result.successful_steps == 0
        assert result.failed_steps == 1
        assert result.total_cost == 0.0


@pytest.mark.unit
class TestModelSerialization:
    """Test model serialization and deserialization."""
    
    def test_step_config_serialization(self, sample_text_to_speech_config):
        """Test step config serialization."""
        # Test dict conversion
        config_dict = sample_text_to_speech_config.dict()
        assert isinstance(config_dict, dict)
        assert config_dict["step_type"] == "text_to_speech"
        
        # Test JSON serialization
        json_str = sample_text_to_speech_config.json()
        assert isinstance(json_str, str)
        assert "text_to_speech" in json_str
        
        # Test reconstruction from dict
        reconstructed = StepConfig(**config_dict)
        assert reconstructed.step_type == sample_text_to_speech_config.step_type
        assert reconstructed.config == sample_text_to_speech_config.config
    
    def test_pipeline_config_serialization(self, sample_pipeline_config):
        """Test pipeline config serialization."""
        # Test dict conversion
        config_dict = sample_pipeline_config.dict()
        assert isinstance(config_dict, dict)
        assert config_dict["pipeline_name"] == "test_pipeline"
        assert len(config_dict["steps"]) == 2
        
        # Test reconstruction
        reconstructed = PipelineConfig(**config_dict)
        assert reconstructed.pipeline_name == sample_pipeline_config.pipeline_name
        assert len(reconstructed.steps) == len(sample_pipeline_config.steps)
```

### Step 6.4: Integration Tests

Create `tests/integration/test_pipeline_integration.py`:
```python
"""Integration tests for pipeline execution."""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock

from ai_content_platform.core.executor import PipelineExecutor
from ai_content_platform.core.models import PipelineResult
from ai_content_platform.utils.config_loader import ConfigLoader


@pytest.mark.integration
class TestPipelineIntegration:
    """Integration tests for complete pipeline execution."""
    
    @pytest.mark.asyncio
    async def test_simple_pipeline_execution(
        self, 
        sample_pipeline_config, 
        temp_dir,
        mock_elevenlabs,
        mock_fal_client,
        mock_aiohttp_session
    ):
        """Test simple pipeline execution with mocked services."""
        # Update output directory to temp directory
        sample_pipeline_config.output_directory = str(temp_dir)
        
        # Create executor
        executor = PipelineExecutor(sample_pipeline_config, parallel_enabled=False)
        
        # Execute pipeline
        result = await executor.execute()
        
        # Verify result
        assert isinstance(result, PipelineResult)
        assert result.pipeline_name == "test_pipeline"
        assert result.total_steps == 2
        assert len(result.step_results) == 2
        
        # Check that output directory was created
        assert Path(temp_dir).exists()
    
    @pytest.mark.asyncio
    async def test_parallel_pipeline_execution(
        self,
        sample_parallel_pipeline_config,
        temp_dir,
        mock_elevenlabs,
        environment_variables
    ):
        """Test parallel pipeline execution."""
        # Update output directory
        sample_parallel_pipeline_config.output_directory = str(temp_dir)
        
        # Create executor with parallel enabled
        executor = PipelineExecutor(sample_parallel_pipeline_config, parallel_enabled=True)
        
        # Execute pipeline
        result = await executor.execute()
        
        # Verify result
        assert isinstance(result, PipelineResult)
        assert result.pipeline_name == "parallel_test_pipeline"
        # Should have 2 steps from the parallel group
        assert len(result.step_results) == 2
    
    @pytest.mark.asyncio
    async def test_pipeline_with_step_failure(
        self,
        sample_pipeline_config,
        temp_dir
    ):
        """Test pipeline behavior when steps fail."""
        # Update output directory
        sample_pipeline_config.output_directory = str(temp_dir)
        
        # Mock service to fail
        with patch('ai_content_platform.services.elevenlabs.tts.ElevenLabsTTSStep.execute') as mock_execute:
            # Make TTS step fail
            from ai_content_platform.core.models import StepResult, StepType
            mock_execute.return_value = StepResult(
                step_id="failed_tts",
                step_type=StepType.TEXT_TO_SPEECH,
                success=False,
                error="Service unavailable"
            )
            
            executor = PipelineExecutor(sample_pipeline_config, parallel_enabled=False)
            result = await executor.execute()
            
            # Pipeline should report partial failure
            assert result.success is False
            assert result.failed_steps > 0
            assert any(not step.success for step in result.step_results)
    
    def test_config_file_loading_and_execution(
        self,
        sample_yaml_config,
        temp_dir,
        mock_elevenlabs
    ):
        """Test loading config from file and executing."""
        # Load config from YAML file
        config = ConfigLoader.load_from_file(sample_yaml_config)
        
        # Verify loaded config
        assert config.pipeline_name == "test_yaml_pipeline"
        assert len(config.steps) == 1
        
        # Update output directory
        config.output_directory = str(temp_dir)
        
        # Execute pipeline
        executor = PipelineExecutor(config, parallel_enabled=False)
        result = asyncio.run(executor.execute())
        
        assert isinstance(result, PipelineResult)
        assert result.pipeline_name == "test_yaml_pipeline"


@pytest.mark.integration 
class TestServiceIntegration:
    """Integration tests for AI service implementations."""
    
    def test_service_dependency_checking(self):
        """Test service dependency checking."""
        from ai_content_platform.services import check_service_dependencies
        
        deps = check_service_dependencies()
        
        assert isinstance(deps, dict)
        assert 'fal_ai' in deps
        assert 'elevenlabs' in deps
        assert 'google' in deps
        
        # Dependencies should be boolean
        for service, available in deps.items():
            assert isinstance(available, bool)
    
    def test_service_registration(self):
        """Test that services are properly registered."""
        from ai_content_platform.services import get_available_services
        from ai_content_platform.core.step import StepFactory
        
        available_services = get_available_services()
        registered_steps = StepFactory.get_available_steps()
        
        # Should have some services registered
        assert len(available_services) > 0
        assert len(registered_steps) > 0
        
        # All available services should be registered
        for service in available_services:
            assert service in registered_steps
    
    @pytest.mark.slow
    def test_step_factory_creation(self, sample_text_to_speech_config):
        """Test step factory can create steps."""
        from ai_content_platform.core.step import StepFactory
        
        # This should work if dependencies are available
        try:
            step = StepFactory.create_step(sample_text_to_speech_config)
            assert step is not None
            assert step.config == sample_text_to_speech_config
        except Exception as e:
            # If dependencies aren't available, should get meaningful error
            assert "not installed" in str(e) or "API key" in str(e)


@pytest.mark.integration
class TestCLIIntegration:
    """Integration tests for CLI functionality."""
    
    def test_cli_import(self):
        """Test that CLI can be imported."""
        from ai_content_platform.cli.main import cli
        assert callable(cli)
    
    def test_cli_version(self):
        """Test CLI version display."""
        from click.testing import CliRunner
        from ai_content_platform.cli.main import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        
        assert result.exit_code == 0
        assert "ai-content-platform" in result.output
    
    def test_cli_info_command(self):
        """Test CLI info command."""
        from click.testing import CliRunner
        from ai_content_platform.cli.main import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['info'])
        
        assert result.exit_code == 0
        assert "AI Content Platform" in result.output
        assert "Service Dependencies" in result.output
    
    def test_cli_init_command(self, temp_dir):
        """Test CLI init command."""
        from click.testing import CliRunner
        from ai_content_platform.cli.main import cli
        
        runner = CliRunner()
        config_file = temp_dir / "init_test.yaml"
        
        result = runner.invoke(cli, ['init', '--output', str(config_file)])
        
        assert result.exit_code == 0
        assert config_file.exists()
        assert "Example configuration created" in result.output
    
    def test_cli_config_validate(self, sample_yaml_config):
        """Test CLI config validation."""
        from click.testing import CliRunner
        from ai_content_platform.cli.main import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['config', 'validate', str(sample_yaml_config)])
        
        assert result.exit_code == 0
        assert "Configuration is valid" in result.output
```

### Step 6.5: Documentation Setup with Sphinx

Create documentation structure:
```bash
# Create docs directory
mkdir -p docs/{source,_static,_templates}

# Create Sphinx configuration files
touch docs/source/conf.py
touch docs/source/index.rst
touch docs/source/installation.rst
touch docs/source/quickstart.rst
touch docs/source/api.rst
touch docs/source/cli.rst
touch docs/source/examples.rst
touch docs/Makefile
```

Create `docs/source/conf.py`:
```python
"""Sphinx configuration for AI Content Platform documentation."""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import version
from ai_content_platform.__version__ import __version__

# Project information
project = 'AI Content Platform'
copyright = '2024, AI Content Platform Team'
author = 'AI Content Platform Team'
release = __version__
version = __version__

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

# Source file suffixes
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser',
}

# HTML output options
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = f"{project} v{version}"

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'special-members': '__init__',
}

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pydantic': ('https://pydantic-docs.helpmanual.io/', None),
    'click': ('https://click.palletsprojects.com/', None),
}

# Auto-generate API documentation
autosummary_generate = True
```

Create `docs/source/index.rst`:
```rst
AI Content Platform Documentation
=================================

Welcome to the AI Content Platform documentation! This comprehensive platform provides 
Python implementations for generating content using multiple AI services and models.

Features
--------

* **Unified Pipeline**: Single interface for all AI services
* **Parallel Execution**: 2-3x performance improvement
* **Cost Management**: Built-in cost estimation and limits
* **Multiple AI Services**: FAL AI, ElevenLabs, Google Veo, and more
* **Professional CLI**: Command-line interface with rich output
* **Type Safety**: Full type hints and validation

Quick Start
-----------

Install the package:

.. code-block:: bash

   pip install ai-content-platform[all]

Create a simple pipeline:

.. code-block:: bash

   acp init --template tts
   acp pipeline run --config pipeline.yaml

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   cli
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

Create `docs/Makefile`:
```makefile
# Makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD  ?= sphinx-build
SOURCEDIR    = source
BUILDDIR     = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx-build
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets
clean:
	rm -rf $(BUILDDIR)/*

livehtml:
	sphinx-autobuild $(SOURCEDIR) $(BUILDDIR)/html

deploy:
	@echo "Building documentation..."
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "Documentation built successfully!"
```

### Step 6.6: CI/CD with GitHub Actions

Create `.github/workflows/ci.yml`:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.8, 3.9, '3.10', 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements/*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
    
    - name: Lint with flake8
      run: |
        flake8 ai_content_platform tests --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 ai_content_platform tests --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
    
    - name: Format check with black
      run: |
        black --check ai_content_platform tests
    
    - name: Import sort check with isort
      run: |
        isort --check-only ai_content_platform tests
    
    - name: Type check with mypy
      run: |
        mypy ai_content_platform
    
    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=ai_content_platform --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.9'
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install safety bandit
    
    - name: Security check with safety
      run: |
        safety check
    
    - name: Security check with bandit
      run: |
        bandit -r ai_content_platform

  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
    
    - name: Build documentation
      run: |
        cd docs
        make html
    
    - name: Deploy to GitHub Pages
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/build/html

  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: |
        python -m build
    
    - name: Check package
      run: |
        twine check dist/*
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  publish:
    runs-on: ubuntu-latest
    needs: [build]
    if: github.event_name == 'release' && github.event.action == 'published'
    environment:
      name: pypi
      url: https://pypi.org/p/ai-content-platform
    permissions:
      id-token: write
    
    steps:
    - name: Download build artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist
        path: dist/
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
```

### Step 6.7: Docker Support

Create `Dockerfile`:
```dockerfile
# Multi-stage build for AI Content Platform
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements/ /tmp/requirements/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements/base.txt && \
    pip install -r /tmp/requirements/fal.txt && \
    pip install -r /tmp/requirements/tts.txt

# Production stage
FROM python:3.9-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user
RUN useradd --create-home --shell /bin/bash acp
USER acp
WORKDIR /home/acp

# Copy application code
COPY --chown=acp:acp . /home/acp/ai-content-platform/
WORKDIR /home/acp/ai-content-platform

# Install package
RUN pip install -e .

# Create directories
RUN mkdir -p /home/acp/workspace/{input,output,configs}

# Set working directory for user
WORKDIR /home/acp/workspace

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD acp info || exit 1

# Default command
CMD ["acp", "--help"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  ai-content-platform:
    build: .
    container_name: acp
    volumes:
      - ./workspace:/home/acp/workspace
      - ./configs:/home/acp/workspace/configs
    environment:
      - FAL_KEY=${FAL_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - PIPELINE_PARALLEL_ENABLED=true
    working_dir: /home/acp/workspace
    command: acp pipeline run --config configs/pipeline.yaml

  # Development service with mounted source code
  ai-content-platform-dev:
    build:
      context: .
      target: builder
    container_name: acp-dev
    volumes:
      - .:/home/acp/ai-content-platform
      - ./workspace:/home/acp/workspace
    environment:
      - FAL_KEY=${FAL_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - PIPELINE_PARALLEL_ENABLED=true
    working_dir: /home/acp/ai-content-platform
    command: tail -f /dev/null
```

---

**Part 6 Complete** - This covers:

1. **Comprehensive Testing Framework** - Unit tests, integration tests, fixtures, and mocks
2. **Documentation with Sphinx** - Professional documentation generation with RTD theme
3. **CI/CD Pipeline** - GitHub Actions for testing, security, and automated deployment
4. **Docker Support** - Multi-stage builds and development/production containers
5. **PyPI Distribution** - Automated publishing on releases

The package is now production-ready with professional testing, documentation, and deployment infrastructure! Would you like me to create a final Part 7 covering deployment guides and project management?