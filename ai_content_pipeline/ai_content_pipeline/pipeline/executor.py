"""
Chain executor for AI Content Pipeline

Handles the sequential execution of pipeline steps with file management.
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .chain import ContentCreationChain, ChainResult, PipelineStep, StepType
from ..models.text_to_image import UnifiedTextToImageGenerator
from ..utils.file_manager import FileManager


class ChainExecutor:
    """
    Executes content creation chains step by step.
    
    Manages file flow between steps and handles errors gracefully.
    """
    
    def __init__(self, file_manager: FileManager):
        """
        Initialize chain executor.
        
        Args:
            file_manager: FileManager instance for handling files
        """
        self.file_manager = file_manager
        
        # Initialize model generators
        self.text_to_image = UnifiedTextToImageGenerator()
        
        # TODO: Initialize other generators when implemented
        # self.image_to_video = UnifiedImageToVideoGenerator()
        # self.audio_generator = UnifiedAudioGenerator()
        # self.video_upscaler = UnifiedVideoUpscaler()
    
    def execute(
        self,
        chain: ContentCreationChain,
        input_text: str,
        **kwargs
    ) -> ChainResult:
        """
        Execute a complete content creation chain.
        
        Args:
            chain: ContentCreationChain to execute
            input_text: Initial text input
            **kwargs: Additional execution parameters
            
        Returns:
            ChainResult with execution results
        """
        start_time = time.time()
        step_results = []
        outputs = {}
        total_cost = 0.0
        current_data = input_text
        current_type = "text"
        
        enabled_steps = chain.get_enabled_steps()
        
        print(f"🎬 Starting chain execution: {len(enabled_steps)} steps")
        
        try:
            for i, step in enumerate(enabled_steps):
                print(f"\n📍 Step {i+1}/{len(enabled_steps)}: {step.step_type.value} ({step.model})")
                
                # Execute step
                step_result = self._execute_step(
                    step=step,
                    input_data=current_data,
                    input_type=current_type,
                    chain_config=chain.config,
                    **kwargs
                )
                
                step_results.append(step_result)
                total_cost += step_result.get("cost", 0.0)
                
                if not step_result.get("success", False):
                    # Step failed
                    error_msg = step_result.get("error", "Unknown error")
                    print(f"❌ Step failed: {error_msg}")
                    
                    return ChainResult(
                        success=False,
                        steps_completed=i,
                        total_steps=len(enabled_steps),
                        total_cost=total_cost,
                        total_time=time.time() - start_time,
                        outputs=outputs,
                        error=f"Step {i+1} failed: {error_msg}",
                        step_results=step_results
                    )
                
                # Update current data for next step
                current_data = step_result.get("output_path") or step_result.get("output_url")
                current_type = self._get_step_output_type(step.step_type)
                
                # Store intermediate output
                step_name = f"step_{i+1}_{step.step_type.value}"
                outputs[step_name] = {
                    "path": step_result.get("output_path"),
                    "url": step_result.get("output_url"),
                    "model": step.model,
                    "metadata": step_result.get("metadata", {})
                }
                
                print(f"✅ Step completed in {step_result.get('processing_time', 0):.1f}s")
            
            # Chain completed successfully
            total_time = time.time() - start_time
            
            print(f"\n🎉 Chain completed successfully!")
            print(f"⏱️  Total time: {total_time:.1f}s")
            print(f"💰 Total cost: ${total_cost:.3f}")
            
            return ChainResult(
                success=True,
                steps_completed=len(enabled_steps),
                total_steps=len(enabled_steps),
                total_cost=total_cost,
                total_time=total_time,
                outputs=outputs,
                step_results=step_results
            )
            
        except Exception as e:
            print(f"❌ Chain execution failed: {str(e)}")
            
            return ChainResult(
                success=False,
                steps_completed=len(step_results),
                total_steps=len(enabled_steps),
                total_cost=total_cost,
                total_time=time.time() - start_time,
                outputs=outputs,
                error=f"Execution error: {str(e)}",
                step_results=step_results
            )
    
    def _execute_step(
        self,
        step: PipelineStep,
        input_data: Any,
        input_type: str,
        chain_config: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a single pipeline step.
        
        Args:
            step: PipelineStep to execute
            input_data: Input data for the step
            input_type: Type of input data ("text", "image", "video")
            chain_config: Chain configuration
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with step execution results
        """
        try:
            if step.step_type == StepType.TEXT_TO_IMAGE:
                return self._execute_text_to_image(step, input_data, chain_config, **kwargs)
            elif step.step_type == StepType.IMAGE_TO_VIDEO:
                return self._execute_image_to_video(step, input_data, chain_config, **kwargs)
            elif step.step_type == StepType.ADD_AUDIO:
                return self._execute_add_audio(step, input_data, chain_config, **kwargs)
            elif step.step_type == StepType.UPSCALE_VIDEO:
                return self._execute_upscale_video(step, input_data, chain_config, **kwargs)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported step type: {step.step_type.value}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Step execution failed: {str(e)}"
            }
    
    def _execute_text_to_image(
        self,
        step: PipelineStep,
        prompt: str,
        chain_config: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Execute text-to-image step."""
        # Merge step params with chain config and kwargs
        params = {
            **step.params,
            **kwargs,
            "output_dir": chain_config.get("output_dir", "output")
        }
        
        result = self.text_to_image.generate(prompt, step.model, **params)
        
        return {
            "success": result.success,
            "output_path": result.output_path,
            "output_url": result.output_url,
            "processing_time": result.processing_time,
            "cost": result.cost_estimate,
            "model": result.model_used,
            "metadata": result.metadata,
            "error": result.error
        }
    
    def _execute_image_to_video(
        self,
        step: PipelineStep,
        image_path: str,
        chain_config: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Execute image-to-video step."""
        try:
            # Try to import and use existing video generation modules
            if step.model == "hailuo":
                return self._execute_hailuo_video(image_path, step, chain_config, **kwargs)
            elif step.model in ["veo2", "veo3"]:
                return self._execute_veo_video(image_path, step, chain_config, **kwargs)
            elif step.model == "kling":
                return self._execute_kling_video(image_path, step, chain_config, **kwargs)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported image-to-video model: {step.model}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Image-to-video execution failed: {str(e)}"
            }
    
    def _execute_hailuo_video(
        self,
        image_path: str,
        step: PipelineStep,
        chain_config: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Execute Hailuo image-to-video generation."""
        try:
            # Try to import FAL image-to-video generation
            import sys
            from pathlib import Path
            import_path = "/home/zdhpe/veo3-video-generation/fal_image_to_video"
            print(f"🔍 Trying to import from: {import_path}")
            sys.path.insert(0, import_path)
            from fal_image_to_video_generator import FALImageToVideoGenerator
            print("✅ FAL Image-to-Video generator imported successfully")
            
            generator = FALImageToVideoGenerator()
            
            # Prepare parameters
            params = {
                "prompt": "Create a cinematic video from this image",  # Default prompt
                "image_url": image_path,  # This is actually a URL from the previous step
                "output_folder": chain_config.get("output_dir", "output"),
                "duration": str(step.params.get("duration", 6)),
                "model": "hailuo"
            }
            
            # Generate video from image URL
            result = generator.generate_video_from_image(**params)
            
            if result is None:
                return {
                    "success": False,
                    "error": "Video generation returned None"
                }
            
            return {
                "success": result is not None,
                "output_path": result.get("local_video_path") if result else None,
                "output_url": result.get("video_url") if result else None,
                "processing_time": result.get("processing_time", 0) if result else 0,
                "cost": 0.08,  # Approximate Hailuo cost
                "model": "hailuo",
                "metadata": result if result else {},
                "error": result.get("error") if result else "Unknown error"
            }
            
        except ImportError:
            return {
                "success": False,
                "error": "FAL video generation module not available"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Hailuo video generation failed: {str(e)}"
            }
    
    def _execute_veo_video(
        self,
        image_path: str,
        step: PipelineStep,
        chain_config: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Execute Veo image-to-video generation."""
        # TODO: Implement Veo integration
        return {
            "success": False,
            "error": "Veo video generation integration not yet implemented"
        }
    
    def _execute_kling_video(
        self,
        image_path: str,
        step: PipelineStep,
        chain_config: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Execute Kling image-to-video generation."""
        try:
            # Try to import FAL image-to-video generation
            import sys
            from pathlib import Path
            sys.path.insert(0, "/home/zdhpe/veo3-video-generation/fal_image_to_video")
            from fal_image_to_video_generator import FALImageToVideoGenerator
            
            generator = FALImageToVideoGenerator()
            
            # Prepare parameters
            params = {
                **step.params,
                "output_dir": chain_config.get("output_dir", "output")
            }
            
            # Generate video from image
            result = generator.generate_video_from_local_image(
                image_path=image_path,
                model="kling",
                **params
            )
            
            return {
                "success": result.get("success", False),
                "output_path": result.get("local_path"),
                "output_url": result.get("video_url"),
                "processing_time": result.get("processing_time", 0),
                "cost": 0.10,  # Approximate Kling cost
                "model": "kling",
                "metadata": result.get("response", {}),
                "error": result.get("error")
            }
            
        except ImportError:
            return {
                "success": False,
                "error": "FAL video generation module not available"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Kling video generation failed: {str(e)}"
            }
    
    def _execute_add_audio(
        self,
        step: PipelineStep,
        video_path: str,
        chain_config: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Execute add-audio step."""
        try:
            # Try to import video-to-video module
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent / "fal_video_to_video"))
            from fal_video_to_video import FALVideoToVideoGenerator
            
            generator = FALVideoToVideoGenerator()
            
            # Prepare parameters
            params = {
                **step.params,
                "output_dir": chain_config.get("output_dir", "output")
            }
            
            # Add audio to video
            result = generator.add_audio_to_local_video(
                video_path=video_path,
                model="thinksound",
                **params
            )
            
            return {
                "success": result.get("success", False),
                "output_path": result.get("local_path"),
                "output_url": result.get("video_url"),
                "processing_time": result.get("processing_time", 0),
                "cost": 0.05,  # Approximate ThinksSound cost
                "model": "thinksound",
                "metadata": result.get("response", {}),
                "error": result.get("error")
            }
            
        except ImportError:
            return {
                "success": False,
                "error": "Video-to-video module not available"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Audio generation failed: {str(e)}"
            }
    
    def _execute_upscale_video(
        self,
        step: PipelineStep,
        video_path: str,
        chain_config: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Execute video upscaling step (placeholder)."""
        # TODO: Implement when video upscaling models are integrated
        return {
            "success": False,
            "error": "Video upscaling integration not yet implemented"
        }
    
    def _get_step_output_type(self, step_type: StepType) -> str:
        """Get the output type for a step."""
        output_types = {
            StepType.TEXT_TO_IMAGE: "image",
            StepType.IMAGE_TO_VIDEO: "video",
            StepType.ADD_AUDIO: "video",
            StepType.UPSCALE_VIDEO: "video"
        }
        return output_types.get(step_type, "unknown")