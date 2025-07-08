"""Test configuration and fixtures for AI Content Platform."""

import asyncio
import tempfile
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, AsyncMock

import pytest
from pydantic import BaseModel

from ai_content_platform.core.models import (
    StepType,
    StepConfig,
    ParallelStepConfig,
    PipelineConfig,
    StepResult,
    PipelineResult
)
from ai_content_platform.utils import (
    get_logger,
    setup_logging,
    FileManager,
    ConfigLoader,
    CostCalculator,
    ConfigValidator
)


# Test configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def logger():
    """Configure test logger."""
    setup_logging(level="DEBUG")
    return get_logger("test")


@pytest.fixture
def file_manager(temp_dir):
    """Create FileManager instance with temporary directory."""
    return FileManager(base_dir=temp_dir)


@pytest.fixture
def config_loader():
    """Create ConfigLoader instance."""
    return ConfigLoader()


@pytest.fixture
def cost_calculator():
    """Create CostCalculator instance."""
    return CostCalculator()


@pytest.fixture
def config_validator():
    """Create ConfigValidator instance."""
    return ConfigValidator()


# Sample configurations
@pytest.fixture
def sample_step_config():
    """Create a sample step configuration."""
    return StepConfig(
        name="test_step",
        step_type=StepType.TEXT_TO_IMAGE,
        parameters={
            "prompt": "A test image",
            "model": "flux-1-dev",
            "width": 512,
            "height": 512
        }
    )


@pytest.fixture
def sample_parallel_step_config():
    """Create a sample parallel step configuration."""
    return ParallelStepConfig(
        name="test_parallel",
        parallel_steps=[
            StepConfig(
                name="step1",
                step_type=StepType.TEXT_TO_IMAGE,
                parameters={"prompt": "Image 1"}
            ),
            StepConfig(
                name="step2", 
                step_type=StepType.TEXT_TO_SPEECH,
                parameters={"text": "Hello world"}
            )
        ],
        merge_strategy="merge_outputs"
    )


@pytest.fixture
def sample_pipeline_config(temp_dir):
    """Create a sample pipeline configuration."""
    return PipelineConfig(
        pipeline_name="test_pipeline",
        description="A test pipeline",
        output_directory=str(temp_dir / "output"),
        steps=[
            StepConfig(
                name="generate_image",
                step_type=StepType.TEXT_TO_IMAGE,
                parameters={
                    "prompt": "A beautiful landscape",
                    "model": "flux-1-dev"
                }
            ),
            StepConfig(
                name="generate_speech",
                step_type=StepType.TEXT_TO_SPEECH,
                parameters={
                    "text": "This is a test.",
                    "voice_id": "test_voice"
                }
            )
        ],
        global_config={
            "max_cost": 5.0,
            "timeout": 300
        }
    )


@pytest.fixture
def sample_step_result():
    """Create a sample step result."""
    return StepResult(
        step_id="test_step_123",
        step_type=StepType.TEXT_TO_IMAGE,
        success=True,
        output_path="/tmp/test_output.png",
        metadata={
            "model": "flux-1-dev",
            "prompt": "A test image",
            "width": 512,
            "height": 512
        },
        execution_time=2.5,
        cost=0.002
    )


@pytest.fixture
def sample_pipeline_result(sample_step_result, temp_dir):
    """Create a sample pipeline result."""
    return PipelineResult(
        pipeline_name="test_pipeline",
        success=True,
        step_results=[sample_step_result],
        total_cost=0.002,
        execution_time=3.0,
        output_directory=str(temp_dir / "output"),
        metadata={
            "steps_executed": 1,
            "successful_steps": 1,
            "failed_steps": 0
        }
    )


# Mock fixtures
@pytest.fixture
def mock_fal_client():
    """Mock FAL client for testing."""
    mock = Mock()
    mock.subscribe = AsyncMock(return_value={
        "images": [{"url": "https://example.com/test_image.png"}],
        "width": 512,
        "height": 512
    })
    return mock


@pytest.fixture
def mock_elevenlabs_client():
    """Mock ElevenLabs client for testing."""
    mock = Mock()
    mock.generate = Mock(return_value=b"fake_audio_data")
    return mock


@pytest.fixture
def mock_google_client():
    """Mock Google client for testing."""
    mock = Mock()
    mock.generate_content = AsyncMock(return_value=Mock(
        text="Generated content",
        candidates=[Mock(content=Mock(parts=[Mock(text="Generated content")]))]
    ))
    return mock


# Test data fixtures
@pytest.fixture
def test_config_yaml(temp_dir):
    """Create a test YAML configuration file."""
    config_content = """
pipeline_name: "yaml_test_pipeline"
description: "Test pipeline from YAML"
output_directory: "output"

global_config:
  max_cost: 10.0
  timeout: 600

steps:
  - name: "test_image"
    step_type: "text_to_image"
    parameters:
      prompt: "A test image from YAML"
      model: "flux-1-dev"
      width: 1024
      height: 1024
  
  - name: "test_speech"
    step_type: "text_to_speech"
    parameters:
      text: "This is a test from YAML configuration."
      voice_id: "test_voice"
"""
    
    config_path = temp_dir / "test_config.yaml"
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    return config_path


@pytest.fixture
def test_config_json(temp_dir):
    """Create a test JSON configuration file."""
    config_content = {
        "pipeline_name": "json_test_pipeline",
        "description": "Test pipeline from JSON",
        "output_directory": "output",
        "global_config": {
            "max_cost": 10.0,
            "timeout": 600
        },
        "steps": [
            {
                "name": "test_image",
                "step_type": "text_to_image",
                "parameters": {
                    "prompt": "A test image from JSON",
                    "model": "flux-1-dev",
                    "width": 1024,
                    "height": 1024
                }
            }
        ]
    }
    
    config_path = temp_dir / "test_config.json"
    import json
    with open(config_path, 'w') as f:
        json.dump(config_content, f, indent=2)
    
    return config_path


@pytest.fixture
def invalid_config_yaml(temp_dir):
    """Create an invalid YAML configuration file."""
    config_content = """
pipeline_name: ""  # Invalid: empty name
description: "Invalid test pipeline"
output_directory: "output"

steps: []  # Invalid: no steps
"""
    
    config_path = temp_dir / "invalid_config.yaml"
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    return config_path


# Environment fixtures
@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    env_vars = {
        "FAL_KEY": "test_fal_key",
        "ELEVENLABS_API_KEY": "test_elevenlabs_key",
        "GOOGLE_API_KEY": "test_google_key",
        "OPENROUTER_API_KEY": "test_openrouter_key"
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    return env_vars


@pytest.fixture
def mock_no_env_vars(monkeypatch):
    """Remove environment variables for testing error cases."""
    env_vars = [
        "FAL_KEY", "FAL_API_KEY",
        "ELEVENLABS_API_KEY", "ELEVEN_API_KEY",
        "GOOGLE_API_KEY", "GEMINI_API_KEY",
        "OPENROUTER_API_KEY", "OPENAI_API_KEY"
    ]
    
    for var in env_vars:
        monkeypatch.delenv(var, raising=False)


# Test helper functions
@pytest.fixture
def create_test_file():
    """Helper function to create test files."""
    def _create_file(path: Path, content: str = "test content"):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return path
    
    return _create_file


@pytest.fixture
def assert_file_exists():
    """Helper function to assert file existence."""
    def _assert_exists(path: Path, should_exist: bool = True):
        if should_exist:
            assert path.exists(), f"File should exist: {path}"
            assert path.is_file(), f"Path should be a file: {path}"
        else:
            assert not path.exists(), f"File should not exist: {path}"
    
    return _assert_exists


# Performance testing fixtures
@pytest.fixture
def performance_config():
    """Configuration for performance testing."""
    return {
        "max_execution_time": 10.0,  # seconds
        "memory_limit": 100 * 1024 * 1024,  # 100MB
        "cpu_limit": 80.0,  # 80% CPU usage
    }


# Integration test fixtures
@pytest.fixture
def integration_test_config():
    """Configuration for integration tests."""
    return {
        "use_real_services": False,  # Set to True for real API testing
        "test_timeout": 30.0,
        "max_cost_per_test": 0.50,  # Maximum cost per integration test
    }


# Markers for different test types
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "api: mark test as requiring API access"
    )
    config.addinivalue_line(
        "markers", "expensive: mark test as potentially expensive"
    )