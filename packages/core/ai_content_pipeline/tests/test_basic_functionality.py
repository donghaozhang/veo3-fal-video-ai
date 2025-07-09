#!/usr/bin/env python3
"""
Basic functionality tests for AI Content Pipeline

Tests core components without requiring API calls.
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ai_content_pipeline.pipeline.manager import AIPipelineManager
from ai_content_pipeline.pipeline.chain import ContentCreationChain, PipelineStep, StepType
from ai_content_pipeline.models.text_to_image import UnifiedTextToImageGenerator
from ai_content_pipeline.utils.file_manager import FileManager
from ai_content_pipeline.utils.validators import (
    validate_prompt, validate_file_path, validate_aspect_ratio,
    validate_model_name, validate_chain_config
)


class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality without API calls."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = AIPipelineManager(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_pipeline_manager_initialization(self):
        """Test pipeline manager initialization."""
        self.assertIsInstance(self.manager, AIPipelineManager)
        self.assertTrue(Path(self.manager.output_dir).exists())
        self.assertTrue(Path(self.manager.temp_dir).exists())
    
    def test_text_to_image_generator_initialization(self):
        """Test text-to-image generator initialization."""
        generator = UnifiedTextToImageGenerator()
        self.assertIsInstance(generator, UnifiedTextToImageGenerator)
        self.assertEqual(generator.model_type, "text_to_image")
    
    def test_file_manager_initialization(self):
        """Test file manager initialization."""
        file_manager = FileManager(self.temp_dir)
        self.assertIsInstance(file_manager, FileManager)
        self.assertTrue(file_manager.output_dir.exists())
        self.assertTrue(file_manager.temp_dir.exists())
    
    def test_pipeline_step_creation(self):
        """Test pipeline step creation."""
        step = PipelineStep(
            step_type=StepType.TEXT_TO_IMAGE,
            model="flux_dev",
            params={"aspect_ratio": "16:9"}
        )
        
        self.assertEqual(step.step_type, StepType.TEXT_TO_IMAGE)
        self.assertEqual(step.model, "flux_dev")
        self.assertEqual(step.params["aspect_ratio"], "16:9")
        self.assertTrue(step.enabled)
    
    def test_pipeline_step_from_dict(self):
        """Test pipeline step creation from dictionary."""
        step_data = {
            "type": "text_to_image",
            "model": "flux_dev",
            "params": {"aspect_ratio": "16:9"},
            "enabled": True
        }
        
        step = PipelineStep.from_dict(step_data)
        self.assertEqual(step.step_type, StepType.TEXT_TO_IMAGE)
        self.assertEqual(step.model, "flux_dev")
        self.assertTrue(step.enabled)
    
    def test_chain_creation(self):
        """Test content creation chain creation."""
        steps = [
            PipelineStep(StepType.TEXT_TO_IMAGE, "flux_dev", {}),
            PipelineStep(StepType.IMAGE_TO_VIDEO, "veo3", {})
        ]
        
        chain = ContentCreationChain("test_chain", steps)
        self.assertEqual(chain.name, "test_chain")
        self.assertEqual(len(chain.steps), 2)
        self.assertEqual(len(chain.get_enabled_steps()), 2)
    
    def test_chain_validation_success(self):
        """Test successful chain validation."""
        steps = [
            PipelineStep(StepType.TEXT_TO_IMAGE, "flux_dev", {}),
            PipelineStep(StepType.IMAGE_TO_VIDEO, "veo3", {})
        ]
        
        chain = ContentCreationChain("test_chain", steps)
        errors = chain.validate()
        self.assertEqual(len(errors), 0)
    
    def test_chain_validation_failure(self):
        """Test chain validation with invalid sequence."""
        # Invalid: image-to-video first (should be text-to-image)
        steps = [
            PipelineStep(StepType.IMAGE_TO_VIDEO, "veo3", {}),
            PipelineStep(StepType.TEXT_TO_IMAGE, "flux_dev", {})
        ]
        
        chain = ContentCreationChain("invalid_chain", steps)
        errors = chain.validate()
        self.assertGreater(len(errors), 0)
    
    def test_simple_chain_creation(self):
        """Test simple chain creation via manager."""
        chain = self.manager.create_simple_chain(
            steps=["text_to_image"],
            models={"text_to_image": "flux_dev"},
            name="simple_test"
        )
        
        self.assertEqual(chain.name, "simple_test")
        self.assertEqual(len(chain.steps), 1)
        self.assertEqual(chain.steps[0].model, "flux_dev")
    
    def test_cost_estimation(self):
        """Test cost estimation for chains."""
        chain = self.manager.create_simple_chain(
            steps=["text_to_image"],
            models={"text_to_image": "flux_dev"}
        )
        
        cost_info = self.manager.estimate_chain_cost(chain)
        self.assertIn("total_cost", cost_info)
        self.assertIn("step_costs", cost_info)
        self.assertIsInstance(cost_info["total_cost"], float)
    
    def test_available_models(self):
        """Test getting available models."""
        available = self.manager.get_available_models()
        self.assertIn("text_to_image", available)
        self.assertIsInstance(available["text_to_image"], list)
    
    def test_file_manager_temp_file(self):
        """Test temporary file creation."""
        temp_file = self.manager.file_manager.create_temp_file(".txt", "test_")
        self.assertTrue(os.path.exists(temp_file))
        self.assertTrue(temp_file.endswith(".txt"))
        self.assertTrue("test_" in os.path.basename(temp_file))
    
    def test_file_manager_output_path(self):
        """Test output path creation."""
        output_path = self.manager.file_manager.create_output_path(
            "test.jpg", "step_1"
        )
        self.assertTrue(output_path.endswith("test.jpg"))
        self.assertTrue("step_1" in output_path)


class TestValidators(unittest.TestCase):
    """Test validation functions."""
    
    def test_prompt_validation_success(self):
        """Test successful prompt validation."""
        valid, error = validate_prompt("A beautiful landscape with mountains")
        self.assertTrue(valid)
        self.assertEqual(error, "")
    
    def test_prompt_validation_empty(self):
        """Test prompt validation with empty string."""
        valid, error = validate_prompt("")
        self.assertFalse(valid)
        self.assertIn("empty", error.lower())
    
    def test_prompt_validation_too_long(self):
        """Test prompt validation with too long string."""
        long_prompt = "x" * 1001
        valid, error = validate_prompt(long_prompt, max_length=1000)
        self.assertFalse(valid)
        self.assertIn("too long", error.lower())
    
    def test_aspect_ratio_validation_success(self):
        """Test successful aspect ratio validation."""
        valid_ratios = ["1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21"]
        
        for ratio in valid_ratios:
            valid, error = validate_aspect_ratio(ratio)
            self.assertTrue(valid, f"Ratio {ratio} should be valid")
            self.assertEqual(error, "")
    
    def test_aspect_ratio_validation_failure(self):
        """Test aspect ratio validation failure."""
        invalid_ratios = ["1:2", "5:4", "invalid", "16/9"]
        
        for ratio in invalid_ratios:
            valid, error = validate_aspect_ratio(ratio)
            self.assertFalse(valid, f"Ratio {ratio} should be invalid")
            self.assertNotEqual(error, "")
    
    def test_model_name_validation_success(self):
        """Test successful model name validation."""
        available_models = ["flux_dev", "flux_schnell", "imagen4"]
        
        # Valid model
        valid, error = validate_model_name("flux_dev", available_models)
        self.assertTrue(valid)
        self.assertEqual(error, "")
        
        # Auto selection
        valid, error = validate_model_name("auto", available_models)
        self.assertTrue(valid)
        self.assertEqual(error, "")
    
    def test_model_name_validation_failure(self):
        """Test model name validation failure."""
        available_models = ["flux_dev", "flux_schnell"]
        
        valid, error = validate_model_name("nonexistent_model", available_models)
        self.assertFalse(valid)
        self.assertIn("not available", error.lower())
    
    def test_chain_config_validation_success(self):
        """Test successful chain configuration validation."""
        config = {
            "name": "test_chain",
            "steps": [
                {
                    "type": "text_to_image",
                    "model": "flux_dev",
                    "params": {"aspect_ratio": "16:9"}
                }
            ]
        }
        
        valid, errors = validate_chain_config(config)
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
    
    def test_chain_config_validation_missing_steps(self):
        """Test chain configuration validation with missing steps."""
        config = {"name": "test_chain"}  # Missing steps
        
        valid, errors = validate_chain_config(config)
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)
    
    def test_chain_config_validation_invalid_step(self):
        """Test chain configuration validation with invalid step."""
        config = {
            "steps": [
                {
                    "type": "invalid_type",  # Invalid step type
                    "model": "flux_dev"
                }
            ]
        }
        
        valid, errors = validate_chain_config(config)
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)


def run_tests():
    """Run all tests."""
    print("🧪 Running AI Content Pipeline Tests")
    print("=" * 40)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBasicFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestValidators))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   • {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"   • {test}: {traceback.split('Exception:')[-1].strip()}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed!'}")
    
    return success


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)