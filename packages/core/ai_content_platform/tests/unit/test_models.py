"""Unit tests for core models."""

import pytest
from pydantic import ValidationError

from ai_content_platform.core.models import (
    StepType,
    StepConfig,
    ParallelStepConfig,
    PipelineConfig,
    StepResult,
    PipelineResult
)


@pytest.mark.unit
class TestStepType:
    """Test StepType enum."""
    
    def test_step_type_values(self):
        """Test that all expected step types exist."""
        expected_types = [
            "text_to_image",
            "image_to_image", 
            "text_to_video",
            "video_generation",
            "text_to_speech",
            "avatar_generation",
            "parallel_group"
        ]
        
        for expected in expected_types:
            assert hasattr(StepType, expected.upper())
            assert getattr(StepType, expected.upper()).value == expected


@pytest.mark.unit
class TestStepConfig:
    """Test StepConfig model."""
    
    def test_valid_step_config(self):
        """Test creating a valid step configuration."""
        config = StepConfig(
            name="test_step",
            step_type=StepType.TEXT_TO_IMAGE,
            parameters={
                "prompt": "A test image",
                "model": "flux-1-dev"
            }
        )
        
        assert config.name == "test_step"
        assert config.step_type == StepType.TEXT_TO_IMAGE
        assert config.parameters["prompt"] == "A test image"
        assert config.required is True  # Default value
    
    def test_step_config_with_optional_fields(self):
        """Test step configuration with optional fields."""
        config = StepConfig(
            name="optional_step",
            step_type=StepType.TEXT_TO_SPEECH,
            parameters={"text": "Hello world"},
            required=False,
            description="Optional test step"
        )
        
        assert config.required is False
        assert config.description == "Optional test step"
    
    def test_invalid_step_config(self):
        """Test invalid step configuration."""
        # Missing required fields
        with pytest.raises(ValidationError):
            StepConfig()
        
        # Invalid step type
        with pytest.raises(ValidationError):
            StepConfig(
                name="invalid",
                step_type="invalid_type",
                parameters={}
            )
    
    def test_step_config_serialization(self):
        """Test step configuration serialization."""
        config = StepConfig(
            name="serialize_test",
            step_type=StepType.TEXT_TO_IMAGE,
            parameters={"prompt": "Test"}
        )
        
        # Test dict conversion
        config_dict = config.dict()
        assert config_dict["name"] == "serialize_test"
        assert config_dict["step_type"] == "text_to_image"
        
        # Test JSON serialization
        config_json = config.json()
        assert "serialize_test" in config_json
        assert "text_to_image" in config_json


@pytest.mark.unit
class TestParallelStepConfig:
    """Test ParallelStepConfig model."""
    
    def test_valid_parallel_step_config(self):
        """Test creating a valid parallel step configuration."""
        steps = [
            StepConfig(
                name="step1",
                step_type=StepType.TEXT_TO_IMAGE,
                parameters={"prompt": "Image 1"}
            ),
            StepConfig(
                name="step2",
                step_type=StepType.TEXT_TO_SPEECH,
                parameters={"text": "Speech 1"}
            )
        ]
        
        parallel_config = ParallelStepConfig(
            name="parallel_test",
            parallel_steps=steps,
            merge_strategy="merge_outputs"
        )
        
        assert parallel_config.name == "parallel_test"
        assert len(parallel_config.parallel_steps) == 2
        assert parallel_config.merge_strategy == "merge_outputs"
    
    def test_invalid_merge_strategy(self):
        """Test invalid merge strategy."""
        steps = [
            StepConfig(
                name="step1",
                step_type=StepType.TEXT_TO_IMAGE,
                parameters={"prompt": "Test"}
            )
        ]
        
        with pytest.raises(ValidationError):
            ParallelStepConfig(
                name="invalid_merge",
                parallel_steps=steps,
                merge_strategy="invalid_strategy"
            )
    
    def test_empty_parallel_steps(self):
        """Test parallel config with empty steps list."""
        with pytest.raises(ValidationError):
            ParallelStepConfig(
                name="empty_parallel",
                parallel_steps=[],
                merge_strategy="merge_outputs"
            )


@pytest.mark.unit
class TestPipelineConfig:
    """Test PipelineConfig model."""
    
    def test_valid_pipeline_config(self, sample_step_config):
        """Test creating a valid pipeline configuration."""
        config = PipelineConfig(
            pipeline_name="test_pipeline",
            description="A test pipeline",
            output_directory="output",
            steps=[sample_step_config],
            global_config={"max_cost": 5.0}
        )
        
        assert config.pipeline_name == "test_pipeline"
        assert config.description == "A test pipeline"
        assert config.output_directory == "output"
        assert len(config.steps) == 1
        assert config.global_config["max_cost"] == 5.0
    
    def test_minimal_pipeline_config(self, sample_step_config):
        """Test pipeline config with minimal required fields."""
        config = PipelineConfig(
            pipeline_name="minimal",
            steps=[sample_step_config]
        )
        
        assert config.pipeline_name == "minimal"
        assert config.description is None
        assert config.output_directory == "output"  # Default value
        assert config.global_config == {}  # Default value
    
    def test_invalid_pipeline_config(self):
        """Test invalid pipeline configuration."""
        # Missing required fields
        with pytest.raises(ValidationError):
            PipelineConfig()
        
        # Empty pipeline name
        with pytest.raises(ValidationError):
            PipelineConfig(
                pipeline_name="",
                steps=[]
            )


@pytest.mark.unit
class TestStepResult:
    """Test StepResult model."""
    
    def test_valid_step_result(self):
        """Test creating a valid step result."""
        result = StepResult(
            step_id="test_123",
            step_type=StepType.TEXT_TO_IMAGE,
            success=True,
            output_path="/tmp/test.png",
            metadata={"model": "flux-1-dev"},
            execution_time=2.5,
            cost=0.002
        )
        
        assert result.step_id == "test_123"
        assert result.step_type == StepType.TEXT_TO_IMAGE
        assert result.success is True
        assert result.output_path == "/tmp/test.png"
        assert result.metadata["model"] == "flux-1-dev"
        assert result.execution_time == 2.5
        assert result.cost == 0.002
        assert result.error is None
    
    def test_failed_step_result(self):
        """Test creating a failed step result."""
        result = StepResult(
            step_id="failed_123",
            step_type=StepType.TEXT_TO_SPEECH,
            success=False,
            error="API timeout",
            execution_time=1.0,
            cost=0.0
        )
        
        assert result.success is False
        assert result.error == "API timeout"
        assert result.output_path is None
    
    def test_step_result_defaults(self):
        """Test step result with default values."""
        result = StepResult(
            step_id="defaults_123",
            step_type=StepType.TEXT_TO_IMAGE,
            success=True
        )
        
        assert result.metadata == {}
        assert result.execution_time == 0.0
        assert result.cost == 0.0


@pytest.mark.unit
class TestPipelineResult:
    """Test PipelineResult model."""
    
    def test_valid_pipeline_result(self, sample_step_result):
        """Test creating a valid pipeline result."""
        result = PipelineResult(
            pipeline_name="test_pipeline",
            success=True,
            step_results=[sample_step_result],
            total_cost=0.002,
            execution_time=3.0,
            output_directory="/tmp/output",
            metadata={"steps_executed": 1}
        )
        
        assert result.pipeline_name == "test_pipeline"
        assert result.success is True
        assert len(result.step_results) == 1
        assert result.total_cost == 0.002
        assert result.execution_time == 3.0
        assert result.output_directory == "/tmp/output"
        assert result.metadata["steps_executed"] == 1
        assert result.error is None
    
    def test_failed_pipeline_result(self):
        """Test creating a failed pipeline result."""
        result = PipelineResult(
            pipeline_name="failed_pipeline",
            success=False,
            step_results=[],
            total_cost=0.0,
            execution_time=1.0,
            output_directory="/tmp/output",
            error="Pipeline validation failed"
        )
        
        assert result.success is False
        assert result.error == "Pipeline validation failed"
        assert len(result.step_results) == 0
    
    def test_pipeline_result_defaults(self):
        """Test pipeline result with default values."""
        result = PipelineResult(
            pipeline_name="defaults_pipeline",
            success=True,
            step_results=[],
            total_cost=0.0,
            execution_time=0.0,
            output_directory="/tmp"
        )
        
        assert result.metadata == {}
        assert result.error is None


@pytest.mark.unit
class TestModelIntegration:
    """Test model integration and relationships."""
    
    def test_pipeline_with_mixed_steps(self):
        """Test pipeline with both regular and parallel steps."""
        regular_step = StepConfig(
            name="regular",
            step_type=StepType.TEXT_TO_IMAGE,
            parameters={"prompt": "Regular step"}
        )
        
        parallel_step = ParallelStepConfig(
            name="parallel",
            parallel_steps=[
                StepConfig(
                    name="parallel_1",
                    step_type=StepType.TEXT_TO_SPEECH,
                    parameters={"text": "Parallel 1"}
                ),
                StepConfig(
                    name="parallel_2", 
                    step_type=StepType.TEXT_TO_IMAGE,
                    parameters={"prompt": "Parallel 2"}
                )
            ],
            merge_strategy="merge_outputs"
        )
        
        pipeline = PipelineConfig(
            pipeline_name="mixed_pipeline",
            steps=[regular_step, parallel_step]
        )
        
        assert len(pipeline.steps) == 2
        assert isinstance(pipeline.steps[0], StepConfig)
        assert isinstance(pipeline.steps[1], ParallelStepConfig)
        assert len(pipeline.steps[1].parallel_steps) == 2
    
    def test_model_json_roundtrip(self, sample_pipeline_config):
        """Test JSON serialization and deserialization."""
        # Serialize to JSON
        json_data = sample_pipeline_config.json()
        
        # Deserialize back to model
        restored_config = PipelineConfig.parse_raw(json_data)
        
        # Verify data integrity
        assert restored_config.pipeline_name == sample_pipeline_config.pipeline_name
        assert restored_config.description == sample_pipeline_config.description
        assert len(restored_config.steps) == len(sample_pipeline_config.steps)
        assert restored_config.global_config == sample_pipeline_config.global_config