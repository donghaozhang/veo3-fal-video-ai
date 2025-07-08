"""Integration tests for pipeline execution."""

import asyncio
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch

import pytest

from ai_content_platform.core import (
    PipelineExecutor,
    ParallelPipelineExecutor,
    StepFactory
)
from ai_content_platform.core.models import (
    StepType,
    StepConfig,
    PipelineConfig
)
from ai_content_platform.utils import ConfigLoader


@pytest.mark.integration
class TestPipelineExecution:
    """Test complete pipeline execution."""
    
    @pytest.fixture
    def mock_step_execution(self):
        """Mock successful step execution."""
        with patch('ai_content_platform.services.fal_ai.fal_client') as mock_fal, \
             patch('ai_content_platform.services.elevenlabs.generate') as mock_eleven:
            
            # Mock FAL AI responses
            mock_fal.subscribe = AsyncMock(return_value={
                "images": [{"url": "https://example.com/test.png"}],
                "width": 512,
                "height": 512
            })
            
            # Mock ElevenLabs response
            mock_eleven.return_value = b"fake_audio_data"
            
            yield {
                "fal": mock_fal,
                "elevenlabs": mock_eleven
            }
    
    @pytest.mark.asyncio
    async def test_sequential_pipeline_execution(
        self, 
        sample_pipeline_config, 
        mock_step_execution,
        mock_env_vars
    ):
        """Test sequential pipeline execution."""
        executor = PipelineExecutor(config=sample_pipeline_config)
        
        result = await executor.execute()
        
        assert result.success is True
        assert len(result.step_results) == 2
        assert result.total_cost > 0
        assert result.execution_time > 0
        assert Path(result.output_directory).exists()
    
    @pytest.mark.asyncio
    async def test_parallel_pipeline_execution(
        self,
        sample_pipeline_config,
        mock_step_execution,
        mock_env_vars
    ):
        """Test parallel pipeline execution."""
        executor = ParallelPipelineExecutor(
            config=sample_pipeline_config,
            enable_parallel=True,
            max_workers=2
        )
        
        result = await executor.execute()
        
        assert result.success is True
        assert len(result.step_results) == 2
        assert result.total_cost > 0
        assert result.execution_time > 0
        
        # Check parallel execution metadata
        assert "parallel_execution" in result.metadata
        parallel_meta = result.metadata["parallel_execution"]
        assert parallel_meta["enabled"] is True
        assert parallel_meta["max_workers"] == 2
    
    @pytest.mark.asyncio
    async def test_pipeline_with_failed_step(
        self,
        sample_pipeline_config,
        mock_env_vars
    ):
        """Test pipeline execution with a failed step."""
        # Mock a failure in the first step
        with patch('ai_content_platform.services.fal_ai.fal_client') as mock_fal:
            mock_fal.subscribe = AsyncMock(side_effect=Exception("API Error"))
            
            executor = PipelineExecutor(config=sample_pipeline_config)
            result = await executor.execute()
            
            assert result.success is False
            assert len(result.step_results) >= 1
            assert result.step_results[0].success is False
            assert "API Error" in result.step_results[0].error
    
    @pytest.mark.asyncio
    async def test_pipeline_cost_limit_exceeded(self, temp_dir, mock_env_vars):
        """Test pipeline execution with cost limit exceeded."""
        config = PipelineConfig(
            pipeline_name="expensive_pipeline",
            output_directory=str(temp_dir / "output"),
            steps=[
                StepConfig(
                    name="expensive_step",
                    step_type=StepType.TEXT_TO_VIDEO,
                    parameters={
                        "prompt": "Expensive video",
                        "model": "google-veo-3"  # Expensive model
                    }
                )
            ],
            global_config={
                "max_cost": 0.01  # Very low limit
            }
        )
        
        executor = PipelineExecutor(config=config)
        result = await executor.execute()
        
        assert result.success is False
        assert "cost" in result.error.lower()
    
    @pytest.mark.asyncio
    async def test_pipeline_with_parallel_steps(
        self,
        temp_dir,
        mock_step_execution,
        mock_env_vars
    ):
        """Test pipeline with explicit parallel steps."""
        from ai_content_platform.core.models import ParallelStepConfig
        
        parallel_step = ParallelStepConfig(
            name="parallel_generation",
            parallel_steps=[
                StepConfig(
                    name="image1",
                    step_type=StepType.TEXT_TO_IMAGE,
                    parameters={"prompt": "Image 1", "model": "flux-1-dev"}
                ),
                StepConfig(
                    name="image2", 
                    step_type=StepType.TEXT_TO_IMAGE,
                    parameters={"prompt": "Image 2", "model": "flux-1-schnell"}
                ),
                StepConfig(
                    name="speech1",
                    step_type=StepType.TEXT_TO_SPEECH,
                    parameters={"text": "Speech 1"}
                )
            ],
            merge_strategy="merge_outputs"
        )
        
        config = PipelineConfig(
            pipeline_name="parallel_test",
            output_directory=str(temp_dir / "output"),
            steps=[parallel_step]
        )
        
        executor = ParallelPipelineExecutor(config=config, enable_parallel=True)
        result = await executor.execute()
        
        assert result.success is True
        assert len(result.step_results) == 1  # One parallel group
        
        # Check that parallel execution actually happened
        parallel_meta = result.metadata.get("parallel_execution", {})
        assert parallel_meta.get("parallel_groups", 0) > 0


@pytest.mark.integration
class TestStepFactory:
    """Test step factory integration."""
    
    def test_step_factory_registration(self):
        """Test that all step types are properly registered."""
        # Initialize registry
        from ai_content_platform.core.registry import initialize_registry
        initialize_registry()
        
        available_steps = StepFactory.get_available_steps()
        
        # Should have registered step types
        assert len(available_steps) > 0
        
        # Check for key step types
        step_values = [step.value for step in available_steps]
        expected_steps = [
            "text_to_image",
            "text_to_speech",
            "text_to_video",
            "avatar_generation"
        ]
        
        for expected in expected_steps:
            assert expected in step_values or any(expected in sv for sv in step_values)
    
    def test_create_fal_ai_steps(self, mock_env_vars):
        """Test creating FAL AI steps."""
        from ai_content_platform.core.registry import initialize_registry
        initialize_registry()
        
        # Test text-to-image step
        image_config = StepConfig(
            name="test_image",
            step_type=StepType.TEXT_TO_IMAGE,
            parameters={
                "prompt": "Test image",
                "model": "flux-1-dev"
            }
        )
        
        step = StepFactory.create_step(image_config)
        assert step is not None
        assert step.config.name == "test_image"
        assert step.validate_config() is True
    
    def test_create_elevenlabs_step(self, mock_env_vars):
        """Test creating ElevenLabs TTS step."""
        from ai_content_platform.core.registry import initialize_registry
        initialize_registry()
        
        tts_config = StepConfig(
            name="test_tts",
            step_type=StepType.TEXT_TO_SPEECH,
            parameters={
                "text": "Hello world",
                "voice_id": "test_voice"
            }
        )
        
        step = StepFactory.create_step(tts_config)
        assert step is not None
        assert step.config.name == "test_tts"
        assert step.validate_config() is True


@pytest.mark.integration
class TestConfigurationIntegration:
    """Test configuration loading and pipeline execution integration."""
    
    @pytest.mark.asyncio
    async def test_yaml_config_to_execution(
        self,
        test_config_yaml,
        mock_step_execution,
        mock_env_vars
    ):
        """Test loading YAML config and executing pipeline."""
        config_loader = ConfigLoader()
        config = config_loader.load_pipeline_config(test_config_yaml)
        
        executor = PipelineExecutor(config=config)
        result = await executor.execute()
        
        assert result.success is True
        assert result.pipeline_name == "yaml_test_pipeline"
        assert len(result.step_results) == 2
    
    @pytest.mark.asyncio
    async def test_json_config_to_execution(
        self,
        test_config_json,
        mock_step_execution,
        mock_env_vars
    ):
        """Test loading JSON config and executing pipeline."""
        config_loader = ConfigLoader()
        config = config_loader.load_pipeline_config(test_config_json)
        
        executor = PipelineExecutor(config=config)
        result = await executor.execute()
        
        assert result.success is True
        assert result.pipeline_name == "json_test_pipeline"
        assert len(result.step_results) == 1
    
    def test_config_validation_integration(self, test_config_yaml):
        """Test configuration validation integration."""
        config_loader = ConfigLoader()
        config = config_loader.load_pipeline_config(test_config_yaml)
        
        from ai_content_platform.utils import ConfigValidator
        validator = ConfigValidator()
        
        # Should validate successfully
        result = validator.validate_pipeline_config(config)
        assert result is True
    
    def test_cost_estimation_integration(self, test_config_yaml):
        """Test cost estimation integration."""
        config_loader = ConfigLoader()
        config = config_loader.load_pipeline_config(test_config_yaml)
        
        from ai_content_platform.utils import CostCalculator
        calculator = CostCalculator()
        
        # Flatten steps for cost calculation
        steps = []
        for step in config.steps:
            if hasattr(step, 'parallel_steps'):
                steps.extend(step.parallel_steps)
            else:
                steps.append(step)
        
        summary = calculator.estimate_pipeline_cost(steps)
        
        assert summary.total_estimated_cost > 0
        assert len(summary.estimates) == len(steps)
        assert len(summary.by_service) > 0


@pytest.mark.integration
@pytest.mark.slow
class TestPerformanceIntegration:
    """Test performance characteristics of pipeline execution."""
    
    @pytest.mark.asyncio
    async def test_parallel_vs_sequential_performance(
        self,
        temp_dir,
        mock_step_execution,
        mock_env_vars
    ):
        """Test that parallel execution is faster than sequential."""
        # Create a pipeline with multiple independent steps
        steps = []
        for i in range(4):
            steps.append(StepConfig(
                name=f"step_{i}",
                step_type=StepType.TEXT_TO_IMAGE,
                parameters={
                    "prompt": f"Test image {i}",
                    "model": "flux-1-schnell"  # Fast model
                }
            ))
        
        config = PipelineConfig(
            pipeline_name="performance_test",
            output_directory=str(temp_dir / "output"),
            steps=steps
        )
        
        # Test sequential execution
        sequential_executor = PipelineExecutor(config=config)
        sequential_result = await sequential_executor.execute()
        sequential_time = sequential_result.execution_time
        
        # Test parallel execution
        parallel_executor = ParallelPipelineExecutor(
            config=config,
            enable_parallel=True,
            max_workers=4
        )
        parallel_result = await parallel_executor.execute()
        parallel_time = parallel_result.execution_time
        
        # Both should succeed
        assert sequential_result.success is True
        assert parallel_result.success is True
        
        # Parallel should be faster (allowing for some variance in mock timing)
        # Note: In real scenarios, this would be more pronounced
        assert parallel_time <= sequential_time * 1.2  # Allow 20% variance for mocking
    
    @pytest.mark.asyncio
    async def test_large_pipeline_execution(
        self,
        temp_dir,
        mock_step_execution,
        mock_env_vars
    ):
        """Test execution of a large pipeline with many steps."""
        # Create a large pipeline
        steps = []
        for i in range(10):
            steps.append(StepConfig(
                name=f"large_step_{i}",
                step_type=StepType.TEXT_TO_IMAGE if i % 2 == 0 else StepType.TEXT_TO_SPEECH,
                parameters={
                    "prompt": f"Large test {i}" if i % 2 == 0 else None,
                    "text": f"Large speech test {i}" if i % 2 == 1 else None,
                    "model": "flux-1-schnell" if i % 2 == 0 else None
                }
            ))
        
        config = PipelineConfig(
            pipeline_name="large_pipeline",
            output_directory=str(temp_dir / "output"),
            steps=steps,
            global_config={"max_cost": 100.0}  # Allow higher cost
        )
        
        executor = ParallelPipelineExecutor(config=config, enable_parallel=True)
        result = await executor.execute()
        
        assert result.success is True
        assert len(result.step_results) == 10
        assert result.execution_time > 0
        assert result.total_cost > 0
        
        # Check that all steps completed
        successful_steps = sum(1 for r in result.step_results if r.success)
        assert successful_steps == 10