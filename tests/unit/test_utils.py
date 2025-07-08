"""Unit tests for utility modules."""

import asyncio
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

import pytest
import yaml

from ai_content_platform.utils import (
    get_logger,
    setup_logging,
    FileManager,
    ConfigLoader,
    CostCalculator,
    ConfigValidator,
    InputValidator
)
from ai_content_platform.core.models import StepType, StepConfig, PipelineConfig
from ai_content_platform.core.exceptions import (
    ValidationError,
    ConfigurationError,
    FileOperationError,
    CostCalculationError
)


@pytest.mark.unit
class TestLogger:
    """Test logging utilities."""
    
    def test_get_logger(self):
        """Test logger creation."""
        logger = get_logger("test_logger")
        assert logger.name == "test_logger"
        assert logger.level == "INFO"
    
    def test_logger_with_custom_level(self):
        """Test logger with custom level."""
        logger = get_logger("debug_logger", level="DEBUG")
        assert logger.level == "DEBUG"
    
    def test_setup_logging(self, temp_dir):
        """Test logging setup."""
        log_file = temp_dir / "test.log"
        setup_logging(level="WARNING", log_file=log_file)
        
        # Test that log file is created
        logger = get_logger("setup_test")
        logger.logger.warning("Test warning message")
        
        # File should be created (though content testing is complex with Rich)
        assert log_file.exists()


@pytest.mark.unit
class TestFileManager:
    """Test FileManager utilities."""
    
    def test_file_manager_initialization(self, temp_dir):
        """Test FileManager initialization."""
        fm = FileManager(base_dir=temp_dir)
        assert fm.base_dir == temp_dir
        assert temp_dir.exists()
    
    @pytest.mark.asyncio
    async def test_copy_file(self, file_manager, temp_dir, create_test_file):
        """Test file copying."""
        source = temp_dir / "source.txt"
        destination = temp_dir / "destination.txt"
        
        create_test_file(source, "test content")
        
        result = await file_manager.copy_file(source, destination)
        
        assert result == destination
        assert destination.exists()
        assert destination.read_text() == "test content"
    
    @pytest.mark.asyncio
    async def test_copy_nonexistent_file(self, file_manager, temp_dir):
        """Test copying nonexistent file."""
        source = temp_dir / "nonexistent.txt"
        destination = temp_dir / "destination.txt"
        
        with pytest.raises(FileOperationError):
            await file_manager.copy_file(source, destination)
    
    @pytest.mark.asyncio
    async def test_move_file(self, file_manager, temp_dir, create_test_file):
        """Test file moving."""
        source = temp_dir / "source.txt"
        destination = temp_dir / "destination.txt"
        
        create_test_file(source, "move test")
        
        result = await file_manager.move_file(source, destination)
        
        assert result == destination
        assert destination.exists()
        assert not source.exists()
        assert destination.read_text() == "move test"
    
    @pytest.mark.asyncio
    async def test_delete_file(self, file_manager, temp_dir, create_test_file):
        """Test file deletion."""
        test_file = temp_dir / "delete_me.txt"
        create_test_file(test_file, "delete this")
        
        result = await file_manager.delete_file(test_file)
        
        assert result is True
        assert not test_file.exists()
    
    @pytest.mark.asyncio
    async def test_delete_nonexistent_file(self, file_manager, temp_dir):
        """Test deleting nonexistent file."""
        nonexistent = temp_dir / "nonexistent.txt"
        
        result = await file_manager.delete_file(nonexistent)
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_file_hash(self, file_manager, temp_dir, create_test_file):
        """Test file hash calculation."""
        test_file = temp_dir / "hash_test.txt"
        create_test_file(test_file, "content for hashing")
        
        hash_md5 = await file_manager.get_file_hash(test_file, "md5")
        hash_sha256 = await file_manager.get_file_hash(test_file, "sha256")
        
        assert isinstance(hash_md5, str)
        assert isinstance(hash_sha256, str)
        assert len(hash_md5) == 32  # MD5 hex length
        assert len(hash_sha256) == 64  # SHA256 hex length
    
    @pytest.mark.asyncio
    async def test_get_file_info(self, file_manager, temp_dir, create_test_file):
        """Test file information retrieval."""
        test_file = temp_dir / "info_test.txt"
        content = "file info test content"
        create_test_file(test_file, content)
        
        info = await file_manager.get_file_info(test_file)
        
        assert info["name"] == "info_test.txt"
        assert info["size"] == len(content)
        assert info["is_file"] is True
        assert info["is_dir"] is False
        assert info["suffix"] == ".txt"
    
    @pytest.mark.asyncio
    async def test_list_files(self, file_manager, temp_dir, create_test_file):
        """Test file listing."""
        # Create test files
        create_test_file(temp_dir / "file1.txt", "content1")
        create_test_file(temp_dir / "file2.txt", "content2")
        create_test_file(temp_dir / "file3.py", "python content")
        create_test_file(temp_dir / "subdir" / "file4.txt", "subdir content")
        
        # List all files
        all_files = await file_manager.list_files(temp_dir, "*")
        txt_files = await file_manager.list_files(temp_dir, "*.txt")
        recursive_files = await file_manager.list_files(temp_dir, "*.txt", recursive=True)
        
        assert len(all_files) == 3  # file1.txt, file2.txt, file3.py
        assert len(txt_files) == 2  # file1.txt, file2.txt
        assert len(recursive_files) == 3  # includes subdir/file4.txt


@pytest.mark.unit
class TestConfigLoader:
    """Test ConfigLoader utilities."""
    
    def test_config_loader_initialization(self):
        """Test ConfigLoader initialization."""
        loader = ConfigLoader()
        assert loader.validator is not None
    
    def test_load_yaml_config(self, config_loader, test_config_yaml):
        """Test loading YAML configuration."""
        config = config_loader.load_pipeline_config(test_config_yaml)
        
        assert config.pipeline_name == "yaml_test_pipeline"
        assert config.description == "Test pipeline from YAML"
        assert len(config.steps) == 2
        assert config.global_config["max_cost"] == 10.0
    
    def test_load_json_config(self, config_loader, test_config_json):
        """Test loading JSON configuration."""
        config = config_loader.load_pipeline_config(test_config_json)
        
        assert config.pipeline_name == "json_test_pipeline"
        assert config.description == "Test pipeline from JSON"
        assert len(config.steps) == 1
        assert config.global_config["max_cost"] == 10.0
    
    def test_load_invalid_config(self, config_loader, invalid_config_yaml):
        """Test loading invalid configuration."""
        with pytest.raises(ConfigurationError):
            config_loader.load_pipeline_config(invalid_config_yaml)
    
    def test_load_nonexistent_config(self, config_loader, temp_dir):
        """Test loading nonexistent configuration."""
        nonexistent = temp_dir / "nonexistent.yaml"
        
        with pytest.raises(ConfigurationError):
            config_loader.load_pipeline_config(nonexistent)
    
    def test_save_yaml_config(self, config_loader, sample_pipeline_config, temp_dir):
        """Test saving YAML configuration."""
        output_path = temp_dir / "saved_config.yaml"
        
        result_path = config_loader.save_pipeline_config(
            sample_pipeline_config, 
            output_path, 
            format="yaml"
        )
        
        assert result_path == output_path
        assert output_path.exists()
        
        # Verify content
        with open(output_path) as f:
            data = yaml.safe_load(f)
        
        assert data["pipeline_name"] == sample_pipeline_config.pipeline_name
    
    def test_save_json_config(self, config_loader, sample_pipeline_config, temp_dir):
        """Test saving JSON configuration."""
        output_path = temp_dir / "saved_config.json"
        
        result_path = config_loader.save_pipeline_config(
            sample_pipeline_config,
            output_path,
            format="json"
        )
        
        assert result_path == output_path
        assert output_path.exists()
        
        # Verify content
        with open(output_path) as f:
            data = json.load(f)
        
        assert data["pipeline_name"] == sample_pipeline_config.pipeline_name
    
    def test_environment_variable_substitution(self, config_loader, temp_dir, monkeypatch):
        """Test environment variable substitution."""
        monkeypatch.setenv("TEST_PROMPT", "Environment prompt")
        monkeypatch.setenv("TEST_MODEL", "env-model")
        
        config_content = """
pipeline_name: "env_test"
steps:
  - name: "env_step"
    step_type: "text_to_image"
    parameters:
      prompt: "${TEST_PROMPT}"
      model: "$TEST_MODEL"
"""
        
        config_path = temp_dir / "env_config.yaml"
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        config = config_loader.load_pipeline_config(config_path)
        
        assert config.steps[0].parameters["prompt"] == "Environment prompt"
        assert config.steps[0].parameters["model"] == "env-model"
    
    def test_get_config_template(self, config_loader):
        """Test configuration template generation."""
        template = config_loader.get_config_template(["text_to_image", "text_to_speech"])
        
        assert template["pipeline_name"] == "example_pipeline"
        assert len(template["steps"]) == 2
        assert template["steps"][0]["step_type"] == "text_to_image"
        assert template["steps"][1]["step_type"] == "text_to_speech"


@pytest.mark.unit
class TestCostCalculator:
    """Test CostCalculator utilities."""
    
    def test_cost_calculator_initialization(self):
        """Test CostCalculator initialization."""
        calculator = CostCalculator()
        assert calculator._cost_history == []
    
    def test_estimate_step_cost(self, cost_calculator):
        """Test step cost estimation."""
        step_config = StepConfig(
            name="test_step",
            step_type=StepType.TEXT_TO_IMAGE,
            parameters={
                "prompt": "Test image",
                "model": "flux-1-dev"
            }
        )
        
        estimate = cost_calculator.estimate_step_cost(step_config)
        
        assert estimate.service.value == "fal_ai"
        assert estimate.step_type == StepType.TEXT_TO_IMAGE
        assert estimate.estimated_cost > 0
        assert 0 <= estimate.confidence <= 1
    
    def test_estimate_pipeline_cost(self, cost_calculator, sample_pipeline_config):
        """Test pipeline cost estimation."""
        steps = [step for step in sample_pipeline_config.steps]
        summary = cost_calculator.estimate_pipeline_cost(steps)
        
        assert summary.total_estimated_cost > 0
        assert len(summary.estimates) == len(steps)
        assert len(summary.by_service) > 0
        assert len(summary.by_step_type) > 0
    
    def test_check_cost_limit_pass(self, cost_calculator):
        """Test cost limit check passing."""
        result = cost_calculator.check_cost_limit(5.0, 10.0)
        assert result is True
    
    def test_check_cost_limit_fail(self, cost_calculator):
        """Test cost limit check failing."""
        with pytest.raises(CostCalculationError):
            cost_calculator.check_cost_limit(15.0, 10.0)
    
    def test_track_actual_cost(self, cost_calculator):
        """Test actual cost tracking."""
        # Should not raise any exceptions
        cost_calculator.track_actual_cost("test_step", 0.05)
    
    def test_get_cost_report(self, cost_calculator):
        """Test cost report generation."""
        report = cost_calculator.get_cost_report()
        
        assert "cost_history" in report
        assert "total_estimates" in report
        assert "total_estimated_cost" in report
        assert isinstance(report["cost_history"], list)


@pytest.mark.unit
class TestConfigValidator:
    """Test ConfigValidator utilities."""
    
    def test_validator_initialization(self):
        """Test ConfigValidator initialization."""
        validator = ConfigValidator()
        assert validator.logger is not None
    
    def test_validate_valid_config(self, config_validator, sample_pipeline_config):
        """Test validation of valid configuration."""
        result = config_validator.validate_pipeline_config(sample_pipeline_config)
        assert result is True
    
    def test_validate_invalid_pipeline_name(self, config_validator):
        """Test validation with invalid pipeline name."""
        config = PipelineConfig(
            pipeline_name="",  # Invalid: empty
            steps=[
                StepConfig(
                    name="test",
                    step_type=StepType.TEXT_TO_IMAGE,
                    parameters={"prompt": "test"}
                )
            ]
        )
        
        with pytest.raises(ValidationError):
            config_validator.validate_pipeline_config(config)
    
    def test_validate_no_steps(self, config_validator):
        """Test validation with no steps."""
        config = PipelineConfig(
            pipeline_name="no_steps",
            steps=[]  # Invalid: no steps
        )
        
        with pytest.raises(ValidationError):
            config_validator.validate_pipeline_config(config)
    
    def test_validate_invalid_step_name(self, config_validator):
        """Test validation with invalid step name."""
        config = PipelineConfig(
            pipeline_name="test_pipeline",
            steps=[
                StepConfig(
                    name="",  # Invalid: empty name
                    step_type=StepType.TEXT_TO_IMAGE,
                    parameters={"prompt": "test"}
                )
            ]
        )
        
        with pytest.raises(ValidationError):
            config_validator.validate_pipeline_config(config)
    
    def test_validate_missing_required_parameters(self, config_validator):
        """Test validation with missing required parameters."""
        config = PipelineConfig(
            pipeline_name="test_pipeline",
            steps=[
                StepConfig(
                    name="missing_params",
                    step_type=StepType.TEXT_TO_IMAGE,
                    parameters={}  # Missing required 'prompt'
                )
            ]
        )
        
        with pytest.raises(ValidationError):
            config_validator.validate_pipeline_config(config)


@pytest.mark.unit
class TestInputValidator:
    """Test InputValidator utilities."""
    
    def test_input_validator_initialization(self):
        """Test InputValidator initialization."""
        validator = InputValidator()
        assert validator.logger is not None
    
    def test_validate_existing_file_path(self, temp_dir, create_test_file):
        """Test validation of existing file path."""
        validator = InputValidator()
        test_file = temp_dir / "test.txt"
        create_test_file(test_file)
        
        result = validator.validate_file_path(test_file)
        assert result == test_file
    
    def test_validate_nonexistent_file_path(self, temp_dir):
        """Test validation of nonexistent file path."""
        validator = InputValidator()
        nonexistent = temp_dir / "nonexistent.txt"
        
        with pytest.raises(ValidationError):
            validator.validate_file_path(nonexistent)
    
    def test_validate_valid_url(self):
        """Test validation of valid URL."""
        validator = InputValidator()
        valid_url = "https://example.com/test"
        
        result = validator.validate_url(valid_url)
        assert result == valid_url
    
    def test_validate_invalid_url(self):
        """Test validation of invalid URL."""
        validator = InputValidator()
        invalid_url = "not-a-url"
        
        with pytest.raises(ValidationError):
            validator.validate_url(invalid_url)
    
    def test_validate_api_key(self):
        """Test API key validation."""
        validator = InputValidator()
        valid_key = "sk-test-key-1234567890"
        
        result = validator.validate_api_key(valid_key, "TestService")
        assert result == valid_key
    
    def test_validate_empty_api_key(self):
        """Test validation of empty API key."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError):
            validator.validate_api_key("", "TestService")
    
    def test_validate_short_api_key(self):
        """Test validation of too short API key."""
        validator = InputValidator()
        short_key = "short"
        
        with pytest.raises(ValidationError):
            validator.validate_api_key(short_key, "TestService")
    
    def test_validate_positive_number(self):
        """Test positive number validation."""
        validator = InputValidator()
        
        assert validator.validate_positive_number(5.0, "test") == 5.0
        assert validator.validate_positive_number(10, "test") == 10
    
    def test_validate_negative_number(self):
        """Test negative number validation."""
        validator = InputValidator()
        
        with pytest.raises(ValidationError):
            validator.validate_positive_number(-1, "test")
        
        with pytest.raises(ValidationError):
            validator.validate_positive_number(0, "test")
    
    def test_validate_valid_email(self):
        """Test valid email validation."""
        validator = InputValidator()
        valid_email = "test@example.com"
        
        result = validator.validate_email(valid_email)
        assert result == valid_email
    
    def test_validate_invalid_email(self):
        """Test invalid email validation."""
        validator = InputValidator()
        invalid_emails = [
            "not-an-email",
            "@example.com",
            "test@",
            "test.example.com"
        ]
        
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                validator.validate_email(email)