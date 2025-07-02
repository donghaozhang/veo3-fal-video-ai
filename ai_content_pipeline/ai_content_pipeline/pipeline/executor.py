"""
Chain executor for AI Content Pipeline

Handles the sequential execution of pipeline steps with file management.
"""

import time
import json
import requests
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from .chain import ContentCreationChain, ChainResult, PipelineStep, StepType
from ..models.text_to_image import UnifiedTextToImageGenerator
from ..models.image_understanding import UnifiedImageUnderstandingGenerator
from ..models.prompt_generation import UnifiedPromptGenerator
from ..models.image_to_image import UnifiedImageToImageGenerator
from ..models.text_to_speech import UnifiedTextToSpeechGenerator
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
        self.image_understanding = UnifiedImageUnderstandingGenerator()
        self.prompt_generation = UnifiedPromptGenerator()
        self.image_to_image = UnifiedImageToImageGenerator()
        self.text_to_speech = UnifiedTextToSpeechGenerator()
        
        # TODO: Initialize other generators when implemented
        # self.image_to_video = UnifiedImageToVideoGenerator()
        # self.audio_generator = UnifiedAudioGenerator()
        # self.video_upscaler = UnifiedVideoUpscaler()
    
    def execute(
        self,
        chain: ContentCreationChain,
        input_data: str,
        **kwargs
    ) -> ChainResult:
        """
        Execute a complete content creation chain.
        
        Args:
            chain: ContentCreationChain to execute
            input_data: Initial input data (text, image path, or video path)
            **kwargs: Additional execution parameters
            
        Returns:
            ChainResult with execution results
        """
        start_time = time.time()
        step_results = []
        outputs = {}
        total_cost = 0.0
        current_data = input_data
        current_type = chain.get_initial_input_type()
        # Track additional context from previous steps
        step_context = {}
        
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
                    step_context=step_context,
                    **kwargs
                )
                
                step_results.append(step_result)
                total_cost += step_result.get("cost", 0.0)
                
                if not step_result.get("success", False):
                    # Step failed
                    error_msg = step_result.get("error", "Unknown error")
                    print(f"❌ Step failed: {error_msg}")
                    
                    # Save failure report
                    total_time = time.time() - start_time
                    execution_report = self._create_execution_report(
                        chain=chain,
                        input_data=input_data,
                        step_results=step_results,
                        outputs=outputs,
                        total_cost=total_cost,
                        total_time=total_time,
                        success=False,
                        error=f"Step {i+1} failed: {error_msg}"
                    )
                    
                    # Save report to file
                    report_path = self._save_execution_report(execution_report, chain.config)
                    if report_path:
                        print(f"📄 Failure report saved: {report_path}")
                    
                    return ChainResult(
                        success=False,
                        steps_completed=i,
                        total_steps=len(enabled_steps),
                        total_cost=total_cost,
                        total_time=total_time,
                        outputs=outputs,
                        error=f"Step {i+1} failed: {error_msg}",
                        step_results=step_results
                    )
                
                # Update current data for next step
                # Special handling for PROMPT_GENERATION - keep image data
                if step.step_type == StepType.PROMPT_GENERATION:
                    # Store the generated prompt in context but keep the image as current_data
                    step_context["generated_prompt"] = step_result.get("extracted_prompt") or step_result.get("output_text")
                    # Don't update current_data - keep the image from previous step
                    print(f"💡 Stored generated prompt, keeping image data for next step")
                else:
                    # Normal data flow for other steps
                    current_data = (step_result.get("output_path") or 
                                   step_result.get("output_url") or 
                                   step_result.get("output_text"))
                    current_type = self._get_step_output_type(step.step_type)
                
                # Store intermediate output
                step_name = f"step_{i+1}_{step.step_type.value}"
                outputs[step_name] = {
                    "path": step_result.get("output_path"),
                    "url": step_result.get("output_url"),
                    "text": step_result.get("output_text"),
                    "model": step.model,
                    "metadata": step_result.get("metadata", {})
                }
                
                # Special handling for prompt generation - include extracted prompt
                if step.step_type == StepType.PROMPT_GENERATION:
                    outputs[step_name]["optimized_prompt"] = step_result.get("extracted_prompt")
                    outputs[step_name]["full_analysis"] = step_result.get("output_text")
                
                # Save intermediate results if enabled
                if chain.save_intermediates:
                    # Download intermediate image if only URL is available
                    if step_result.get("output_url") and not step_result.get("output_path"):
                        local_path = self._download_intermediate_image(
                            image_url=step_result["output_url"],
                            step_name=step_name,
                            config=chain.config,
                            step_number=i+1
                        )
                        if local_path:
                            # Update the step result and outputs with local path
                            step_result["output_path"] = local_path
                            outputs[step_name]["path"] = local_path
                    
                    intermediate_report = self._create_intermediate_report(
                        chain=chain,
                        input_data=input_data,
                        step_results=step_results[:i+1],  # Only include completed steps
                        outputs=outputs,
                        total_cost=total_cost,
                        current_step=i+1,
                        total_steps=len(enabled_steps)
                    )
                    # Save intermediate report
                    intermediate_path = self._save_intermediate_report(
                        intermediate_report, 
                        chain.config, 
                        step_number=i+1
                    )
                    if intermediate_path:
                        print(f"💾 Intermediate results saved: {intermediate_path}")
                
                print(f"✅ Step completed in {step_result.get('processing_time', 0):.1f}s")
            
            # Chain completed successfully
            total_time = time.time() - start_time
            
            print(f"\n🎉 Chain completed successfully!")
            print(f"⏱️  Total time: {total_time:.1f}s")
            print(f"💰 Total cost: ${total_cost:.3f}")
            
            # Save detailed execution report
            execution_report = self._create_execution_report(
                chain=chain,
                input_data=input_data,
                step_results=step_results,
                outputs=outputs,
                total_cost=total_cost,
                total_time=total_time,
                success=True
            )
            
            # Save report to file
            report_path = self._save_execution_report(execution_report, chain.config)
            if report_path:
                print(f"📄 Execution report saved: {report_path}")
            
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
            
            # Save error report
            total_time = time.time() - start_time
            execution_report = self._create_execution_report(
                chain=chain,
                input_data=input_data,
                step_results=step_results,
                outputs=outputs,
                total_cost=total_cost,
                total_time=total_time,
                success=False,
                error=f"Execution error: {str(e)}"
            )
            
            # Save report to file
            report_path = self._save_execution_report(execution_report, chain.config)
            if report_path:
                print(f"📄 Error report saved: {report_path}")
            
            return ChainResult(
                success=False,
                steps_completed=len(step_results),
                total_steps=len(enabled_steps),
                total_cost=total_cost,
                total_time=total_time,
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
        step_context: Dict[str, Any] = None,
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
            if step_context is None:
                step_context = {}
                
            if step.step_type == StepType.TEXT_TO_IMAGE:
                return self._execute_text_to_image(step, input_data, chain_config, step_context, **kwargs)
            elif step.step_type == StepType.IMAGE_UNDERSTANDING:
                return self._execute_image_understanding(step, input_data, chain_config, step_context, **kwargs)
            elif step.step_type == StepType.PROMPT_GENERATION:
                return self._execute_prompt_generation(step, input_data, chain_config, step_context, **kwargs)
            elif step.step_type == StepType.IMAGE_TO_IMAGE:
                return self._execute_image_to_image(step, input_data, chain_config, step_context, **kwargs)
            elif step.step_type == StepType.IMAGE_TO_VIDEO:
                return self._execute_image_to_video(step, input_data, chain_config, step_context, **kwargs)
            elif step.step_type == StepType.TEXT_TO_SPEECH:
                return self._execute_text_to_speech(step, input_data, chain_config, step_context, **kwargs)
            elif step.step_type == StepType.ADD_AUDIO:
                return self._execute_add_audio(step, input_data, chain_config, step_context, **kwargs)
            elif step.step_type == StepType.UPSCALE_VIDEO:
                return self._execute_upscale_video(step, input_data, chain_config, step_context, **kwargs)
            elif step.step_type == StepType.GENERATE_SUBTITLES:
                return self._execute_generate_subtitles(step, input_data, chain_config, step_context, **kwargs)
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
        step_context: Dict[str, Any] = None,
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
    
    def _execute_image_understanding(
        self,
        step: PipelineStep,
        image_input: str,
        chain_config: Dict[str, Any],
        step_context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute image understanding step."""
        # Get analysis prompt from step params or kwargs
        analysis_prompt = step.params.get("prompt", kwargs.get("prompt", None))
        question = step.params.get("question", kwargs.get("question", None))
        
        # Merge step params with chain config and kwargs
        params = {
            **{k: v for k, v in step.params.items() if k not in ["prompt", "question"]},
            **{k: v for k, v in kwargs.items() if k not in ["prompt", "question"]},
        }
        
        # Add analysis prompt or question if provided
        if analysis_prompt:
            params["analysis_prompt"] = analysis_prompt
        if question:
            params["question"] = question
        
        result = self.image_understanding.analyze(
            image_path=image_input,
            model=step.model,
            **params
        )
        
        return {
            "success": result.success,
            "output_text": result.output_text,
            "processing_time": result.processing_time,
            "cost": result.cost_estimate,
            "model": result.model_used,
            "metadata": result.metadata,
            "error": result.error
        }
    
    def _execute_prompt_generation(
        self,
        step: PipelineStep,
        image_input: str,
        chain_config: Dict[str, Any],
        step_context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute prompt generation step."""
        # Get background context from step params or kwargs
        background_context = step.params.get("background_context", kwargs.get("background_context", ""))
        video_style = step.params.get("video_style", kwargs.get("video_style", ""))
        duration_preference = step.params.get("duration_preference", kwargs.get("duration_preference", ""))
        
        # Merge step params with chain config and kwargs
        params = {
            **{k: v for k, v in step.params.items() if k not in ["background_context", "video_style", "duration_preference"]},
            **{k: v for k, v in kwargs.items() if k not in ["background_context", "video_style", "duration_preference"]},
        }
        
        # Add specific parameters if provided
        if background_context:
            params["background_context"] = background_context
        if video_style:
            params["video_style"] = video_style
        if duration_preference:
            params["duration_preference"] = duration_preference
        
        result = self.prompt_generation.generate(
            image_path=image_input,
            model=step.model,
            **params
        )
        
        return {
            "success": result.success,
            "output_text": result.output_text,
            "extracted_prompt": result.extracted_prompt,
            "processing_time": result.processing_time,
            "cost": result.cost_estimate,
            "model": result.model_used,
            "metadata": result.metadata,
            "error": result.error
        }
    
    def _execute_text_to_speech(
        self,
        step: PipelineStep,
        text_input: str,
        chain_config: Dict[str, Any],
        step_context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute text-to-speech step."""
        try:
            # Get text to use - either from text_override param or input
            actual_text = step.params.get("text_override", text_input)
            
            # Get voice and other parameters from step params or kwargs
            voice = step.params.get("voice", kwargs.get("voice", "rachel"))
            speed = step.params.get("speed", kwargs.get("speed", 1.0))
            stability = step.params.get("stability", kwargs.get("stability", 0.5))
            similarity_boost = step.params.get("similarity_boost", kwargs.get("similarity_boost", 0.8))
            style = step.params.get("style", kwargs.get("style", 0.2))
            output_file = step.params.get("output_file", kwargs.get("output_file", None))
            
            # Merge step params with chain config and kwargs
            params = {
                **step.params,
                **kwargs,
                "output_dir": chain_config.get("output_dir", "output")
            }
            
            # Generate speech using the TTS generator
            success, result = self.text_to_speech.generate(
                prompt=actual_text,
                model=step.model,
                voice=voice,
                speed=speed,
                stability=stability,
                similarity_boost=similarity_boost,
                style=style,
                output_file=output_file
            )
            
            if success:
                return {
                    "success": True,
                    "output_path": result["output_file"],
                    "output_url": None,  # TTS generates local files
                    "processing_time": result.get("processing_time", 15),
                    "cost": result.get("cost", 0.05),  # Default cost estimate
                    "model": result["model"],
                    "metadata": {
                        "voice_used": result["voice_used"],
                        "text_length": result["text_length"],
                        "settings": result["settings"]
                    },
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "output_path": None,
                    "output_url": None,
                    "processing_time": 0,
                    "cost": 0,
                    "model": step.model,
                    "metadata": {},
                    "error": result.get("error", "TTS generation failed")
                }
                
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "output_url": None,
                "processing_time": 0,
                "cost": 0,
                "model": step.model,
                "metadata": {},
                "error": f"TTS execution failed: {str(e)}"
            }
    
    def _execute_image_to_image(
        self,
        step: PipelineStep,
        source_image: str,
        chain_config: Dict[str, Any],
        step_context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute image-to-image step."""
        # Get prompt from step params or kwargs
        prompt = step.params.get("prompt", kwargs.get("prompt", "modify this image"))
        
        # Merge step params with chain config and kwargs, but exclude prompt to avoid duplication
        params = {
            **{k: v for k, v in step.params.items() if k != "prompt"},
            **{k: v for k, v in kwargs.items() if k != "prompt"},
            "output_dir": chain_config.get("output_dir", "output")
        }
        
        result = self.image_to_image.generate(
            source_image=source_image,
            prompt=prompt,
            model=step.model,
            **params
        )
        
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
        step_context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute image-to-video step."""
        try:
            # Try to import and use existing video generation modules
            if step.model == "hailuo":
                return self._execute_hailuo_video(image_path, step, chain_config, step_context, **kwargs)
            elif step.model in ["veo2", "veo3"]:
                return self._execute_veo_video(image_path, step, chain_config, step_context, **kwargs)
            elif step.model == "kling":
                return self._execute_kling_video(image_path, step, chain_config, step_context, **kwargs)
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
        step_context: Dict[str, Any] = None,
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
            # Use generated prompt from previous step if available
            default_prompt = "Create a cinematic video from this image"
            if step_context and "generated_prompt" in step_context:
                prompt = step_context["generated_prompt"]
                print(f"📝 Using generated prompt: {prompt[:100]}...")
            else:
                prompt = step.params.get("prompt", default_prompt)
                
            params = {
                "prompt": prompt,
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
            
            # Get the local path from result
            local_path = result.get("local_path") if result else None
                
            return {
                "success": result is not None,
                "output_path": local_path,
                "output_url": result.get("video", {}).get("url") if result else None,
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
        step_context: Dict[str, Any] = None,
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
        step_context: Dict[str, Any] = None,
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
        step_context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute add-audio step."""
        try:
            print(f"🎵 Debug: video_path received = {video_path}")
            print(f"🎵 Debug: video_path type = {type(video_path)}")
            
            if video_path is None:
                return {
                    "success": False,
                    "error": "Video path is None - video from previous step not available"
                }
                
            # Try to import video-to-video module
            import sys
            from pathlib import Path
            fal_video_path = Path(__file__).parent.parent.parent.parent / "fal_video_to_video"
            sys.path.insert(0, str(fal_video_path))
            from fal_video_to_video.generator import FALVideoToVideoGenerator
            
            generator = FALVideoToVideoGenerator()
            
            # Prepare parameters
            params = {
                **step.params,
                "output_dir": chain_config.get("output_dir", "output")
            }
            
            print(f"🎵 Debug: Calling add_audio_to_local_video with path: {video_path}")
            
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
        step_context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute video upscaling step."""
        import sys
        import os
        from pathlib import Path
        
        try:
            # Try multiple import paths for fal_video_to_video
            current_dir = os.getcwd()
            possible_paths = [
                os.path.join(os.path.dirname(current_dir), 'fal_video_to_video'),
                os.path.join(current_dir, '..', 'fal_video_to_video'),
                '/home/zdhpe/veo3-video-generation/fal_video_to_video'
            ]
            
            imported = False
            for fal_video_path in possible_paths:
                try:
                    print(f"🔍 Trying to import from: {fal_video_path}")
                    if os.path.exists(fal_video_path) and fal_video_path not in sys.path:
                        sys.path.insert(0, fal_video_path)
                    
                    from fal_video_to_video.generator import FALVideoToVideoGenerator
                    imported = True
                    break
                except ImportError:
                    continue
            
            if not imported:
                # Try alternative import structure
                sys.path.insert(0, '/home/zdhpe/veo3-video-generation/fal_video_to_video')
                from fal_video_to_video.fal_video_to_video.generator import FALVideoToVideoGenerator
            print("✅ FAL Video-to-Video upscaler imported successfully")
            
            # Initialize upscaler
            upscaler = FALVideoToVideoGenerator()
            
            # Get parameters
            upscale_factor = step.params.get("upscale_factor", 2)
            target_fps = step.params.get("target_fps", None)
            
            print(f"🔍 Starting video upscaling...")
            print(f"📹 Input video: {video_path}")
            print(f"📈 Upscale factor: {upscale_factor}x")
            if target_fps:
                print(f"🎬 Target FPS: {target_fps}")
            
            # Check if video file exists
            if not os.path.exists(video_path):
                return {
                    "success": False,
                    "error": f"Video file not found: {video_path}"
                }
            
            # Execute upscaling
            start_time = time.time()
            
            result = upscaler.upscale_local_video(
                video_path=video_path,
                upscale_factor=upscale_factor,
                target_fps=target_fps,
                output_dir=chain_config.get("output_dir", "output")
            )
            
            processing_time = time.time() - start_time
            
            if result.get("success"):
                print(f"✅ Video upscaling completed successfully!")
                print(f"📁 Output: {result.get('local_path')}")
                print(f"⏱️  Processing time: {processing_time:.1f} seconds")
                
                return {
                    "success": True,
                    "output_path": result.get("local_path"),
                    "output_url": result.get("video_url"),
                    "processing_time": processing_time,
                    "cost": result.get("cost", 1.50),  # Default Topaz cost
                    "model": step.model,
                    "metadata": {
                        "upscale_factor": upscale_factor,
                        "target_fps": target_fps,
                        "original_path": video_path,
                        "model_response": result
                    },
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "error": f"Video upscaling failed: {result.get('error', 'Unknown error')}",
                    "processing_time": processing_time
                }
                
        except ImportError as e:
            return {
                "success": False,
                "error": f"Could not import video upscaling module: {e}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Video upscaling failed: {str(e)}"
            }
    
    def _execute_generate_subtitles(
        self,
        step: PipelineStep,
        video_path: str,
        chain_config: Dict[str, Any],
        step_context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute subtitle generation step.
        
        Args:
            step: PipelineStep configuration
            video_path: Path to input video file
            chain_config: Chain configuration
            step_context: Context from previous steps
            **kwargs: Additional parameters
            
        Returns:
            Dictionary with execution results
        """
        import time
        import os
        import sys
        from pathlib import Path
        
        try:
            # Import video tools subtitle generator
            try:
                # Try multiple import paths
                video_tools_path = "/home/zdhpe/veo3-video-generation/video_tools"
                if video_tools_path not in sys.path:
                    sys.path.append(video_tools_path)
                
                from video_utils.subtitle_generator import generate_subtitle_for_video
                
            except ImportError as e:
                return {
                    "success": False,
                    "error": f"Could not import subtitle generation module: {e}"
                }
            
            # Get parameters
            subtitle_text = step.params.get("subtitle_text", "")
            format_type = step.params.get("format", "srt")  # srt or vtt
            words_per_second = step.params.get("words_per_second", 2.0)
            output_dir = step.params.get("output_dir", chain_config.get("output_dir", "output"))
            
            # Use subtitle text from context if available and not explicitly set
            if not subtitle_text and step_context:
                subtitle_text = step_context.get("generated_prompt") or step_context.get("subtitle_text", "")
            
            if not subtitle_text:
                return {
                    "success": False,
                    "error": "No subtitle text provided. Use 'subtitle_text' parameter or generate from previous prompt step."
                }
            
            print(f"📝 Starting subtitle generation...")
            print(f"📹 Input video: {video_path}")
            print(f"📄 Format: {format_type.upper()}")
            print(f"⏱️  Words per second: {words_per_second}")
            print(f"📝 Subtitle text: {subtitle_text[:100]}{'...' if len(subtitle_text) > 100 else ''}")
            
            # Check if video file exists
            if not os.path.exists(video_path):
                return {
                    "success": False,
                    "error": f"Video file not found: {video_path}"
                }
            
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate output filename
            video_name = Path(video_path).stem
            output_subtitle_path = output_path / f"{video_name}.{format_type}"
            
            # Execute subtitle generation
            start_time = time.time()
            
            subtitle_path = generate_subtitle_for_video(
                video_path=Path(video_path),
                text=subtitle_text,
                format_type=format_type,
                words_per_second=words_per_second,
                output_path=output_subtitle_path
            )
            
            processing_time = time.time() - start_time
            
            if subtitle_path and os.path.exists(subtitle_path):
                print(f"✅ Subtitle generation completed successfully!")
                print(f"📁 Subtitle file: {subtitle_path}")
                print(f"⏱️  Processing time: {processing_time:.1f} seconds")
                
                # Copy the video file to output directory if not already there
                output_video_path = output_path / Path(video_path).name
                if not output_video_path.exists():
                    import shutil
                    shutil.copy2(video_path, output_video_path)
                    print(f"📁 Video copied to: {output_video_path}")
                
                return {
                    "success": True,
                    "output_path": str(output_video_path),  # Return video path as main output
                    "subtitle_path": str(subtitle_path),
                    "processing_time": processing_time,
                    "cost": 0.0,  # Subtitle generation is free
                    "model": step.model,
                    "metadata": {
                        "format": format_type,
                        "words_per_second": words_per_second,
                        "subtitle_text": subtitle_text,
                        "subtitle_file": str(subtitle_path),
                        "video_file": str(output_video_path),
                        "subtitle_length": len(subtitle_text)
                    },
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "error": f"Subtitle generation failed: No output file created",
                    "processing_time": processing_time
                }
                
        except ImportError as e:
            return {
                "success": False,
                "error": f"Could not import subtitle generation module: {e}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Subtitle generation failed: {str(e)}"
            }
    
    def _get_step_output_type(self, step_type: StepType) -> str:
        """Get the output type for a step."""
        output_types = {
            StepType.TEXT_TO_IMAGE: "image",
            StepType.IMAGE_UNDERSTANDING: "text",
            StepType.PROMPT_GENERATION: "text",
            StepType.IMAGE_TO_IMAGE: "image",
            StepType.IMAGE_TO_VIDEO: "video",
            StepType.ADD_AUDIO: "video",
            StepType.UPSCALE_VIDEO: "video",
            StepType.GENERATE_SUBTITLES: "video"
        }
        return output_types.get(step_type, "unknown")
    
    def _create_execution_report(
        self,
        chain,
        input_data: str,
        step_results: list,
        outputs: dict,
        total_cost: float,
        total_time: float,
        success: bool,
        error: str = None
    ) -> dict:
        """Create detailed execution report with all step information."""
        import time
        from datetime import datetime
        
        # Create step details with status and download links
        step_details = []
        for i, step_result in enumerate(step_results):
            step = chain.get_enabled_steps()[i]
            
            step_detail = {
                "step_number": i + 1,
                "step_name": f"step_{i+1}_{step.step_type.value}",
                "step_type": step.step_type.value,
                "model": step.model,
                "status": "success" if step_result.get("success", False) else "failed",
                "processing_time": step_result.get("processing_time", 0),
                "cost": step_result.get("cost", 0),
                "output_files": {},
                "download_links": {},
                "metadata": step_result.get("metadata", {}),
                "error": step_result.get("error") if not step_result.get("success", False) else None
            }
            
            # Add output file information
            if step_result.get("output_path"):
                step_detail["output_files"]["local_path"] = step_result["output_path"]
            
            if step_result.get("output_url"):
                step_detail["download_links"]["direct_url"] = step_result["output_url"]
            
            # Add step-specific details
            if step.step_type == StepType.TEXT_TO_IMAGE:
                step_detail["input_prompt"] = input_data
                step_detail["generation_params"] = step.params
            elif step.step_type == StepType.PROMPT_GENERATION:
                step_detail["optimized_prompt"] = step_result.get("extracted_prompt")
                step_detail["full_analysis"] = step_result.get("output_text")
                step_detail["generation_params"] = step.params
                step_detail["input_image_url"] = step_results[i-1].get("output_url") if i > 0 else None
            elif step.step_type == StepType.IMAGE_TO_VIDEO:
                step_detail["input_image_url"] = step_results[i-1].get("output_url") if i > 0 else None
                step_detail["video_params"] = step.params
            
            step_details.append(step_detail)
        
        # Get final outputs for easy access
        final_outputs = {}
        download_links = {}
        
        for step_name, output in outputs.items():
            if output.get("path"):
                final_outputs[step_name] = output["path"]
            if output.get("url"):
                download_links[step_name] = output["url"]
        
        # Create comprehensive report
        report = {
            "execution_summary": {
                "chain_name": chain.name,
                "execution_id": f"exec_{int(time.time())}",
                "timestamp": datetime.now().isoformat(),
                "status": "success" if success else "failed",
                "input_data": input_data,
                "input_type": chain.get_initial_input_type(),
                "total_steps": len(chain.get_enabled_steps()),
                "completed_steps": len([s for s in step_results if s.get("success", False)]),
                "total_cost_usd": round(total_cost, 4),
                "total_processing_time_seconds": round(total_time, 2),
                "error": error
            },
            "step_execution_details": step_details,
            "final_outputs": {
                "local_files": final_outputs,
                "download_links": download_links
            },
            "cost_breakdown": {
                "by_step": [
                    {
                        "step": f"{i+1}_{step.step_type.value}",
                        "model": step.model,
                        "cost_usd": step_result.get("cost", 0)
                    }
                    for i, (step, step_result) in enumerate(zip(chain.get_enabled_steps(), step_results))
                ],
                "total_cost_usd": round(total_cost, 4)
            },
            "performance_metrics": {
                "by_step": [
                    {
                        "step": f"{i+1}_{step.step_type.value}",
                        "processing_time_seconds": step_result.get("processing_time", 0),
                        "status": "success" if step_result.get("success", False) else "failed"
                    }
                    for i, (step, step_result) in enumerate(zip(chain.get_enabled_steps(), step_results))
                ],
                "total_time_seconds": round(total_time, 2),
                "average_time_per_step": round(total_time / len(step_results) if step_results else 0, 2)
            },
            "metadata": {
                "chain_config": chain.to_config(),
                "pipeline_version": "1.0.0",
                "models_used": [step.model for step in chain.get_enabled_steps()]
            }
        }
        
        return report
    
    def _save_execution_report(self, report: dict, chain_config: dict) -> str:
        """Save execution report to JSON file."""
        
        try:
            # Create reports directory
            output_dir = Path(chain_config.get("output_dir", "output"))
            reports_dir = output_dir / "reports"
            reports_dir.mkdir(exist_ok=True)
            
            # Generate report filename
            execution_id = report["execution_summary"]["execution_id"]
            chain_name = report["execution_summary"]["chain_name"]
            filename = f"{chain_name}_{execution_id}_report.json"
            report_path = reports_dir / filename
            
            # Save report
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            return str(report_path)
            
        except Exception as e:
            print(f"⚠️  Failed to save execution report: {e}")
            return None
    
    def _create_intermediate_report(
        self,
        chain: 'ContentCreationChain',
        input_data: str,
        step_results: List[Dict[str, Any]],
        outputs: Dict[str, Any],
        total_cost: float,
        current_step: int,
        total_steps: int
    ) -> Dict[str, Any]:
        """Create an intermediate execution report."""
        execution_id = f"intermediate_{int(time.time())}"
        
        return {
            "report_type": "intermediate",
            "execution_summary": {
                "chain_name": chain.name,
                "execution_id": execution_id,
                "timestamp": datetime.now().isoformat(),
                "status": "in_progress",
                "input_data": input_data,
                "input_type": chain.get_initial_input_type(),
                "total_steps": total_steps,
                "completed_steps": current_step,
                "total_cost_usd": total_cost,
                "current_step": current_step
            },
            "completed_steps": [
                {
                    "step_number": i + 1,
                    "step_type": chain.steps[i].step_type.value,
                    "model": chain.steps[i].model,
                    "status": "completed" if result.get("success") else "failed",
                    "cost": result.get("cost", 0),
                    "output": {
                        "path": result.get("output_path"),
                        "url": result.get("output_url"),
                        "text": result.get("output_text"),
                        # Add prompt generation specific fields
                        **({"optimized_prompt": result.get("extracted_prompt"), "full_analysis": result.get("output_text")} 
                           if chain.steps[i].step_type == StepType.PROMPT_GENERATION else {})
                    }
                }
                for i, result in enumerate(step_results)
            ],
            "intermediate_outputs": outputs,
            "metadata": {
                "chain_config": chain.to_config(),
                "save_intermediates": chain.save_intermediates
            }
        }
    
    def _save_intermediate_report(
        self, 
        report: Dict[str, Any], 
        config: Dict[str, Any],
        step_number: int
    ) -> Optional[str]:
        """Save intermediate report to file."""
        try:
            # Create reports directory
            output_dir = Path(config.get("output_dir", "output"))
            reports_dir = output_dir / "reports"
            reports_dir.mkdir(exist_ok=True)
            
            # Generate filename with step number
            chain_name = report["execution_summary"]["chain_name"]
            timestamp = int(time.time())
            filename = f"{chain_name}_step{step_number}_intermediate_{timestamp}.json"
            filepath = reports_dir / filename
            
            # Save report
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            return str(filepath)
        except Exception as e:
            print(f"⚠️  Failed to save intermediate report: {str(e)}")
            return None
    
    def _download_intermediate_image(
        self, 
        image_url: str, 
        step_name: str, 
        config: Dict[str, Any],
        step_number: int
    ) -> Optional[str]:
        """
        Download intermediate image for save_intermediates functionality.
        
        Args:
            image_url: URL of the image to download
            step_name: Name of the step (e.g., "step_1_text_to_image")
            config: Chain configuration containing output_dir
            step_number: Step number for filename generation
            
        Returns:
            Local file path if successful, None if failed
        """
        try:
            # Create intermediates directory
            output_dir = Path(config.get("output_dir", "output"))
            intermediates_dir = output_dir / "intermediates"
            intermediates_dir.mkdir(exist_ok=True)
            
            # Generate filename
            timestamp = int(time.time())
            file_extension = Path(image_url).suffix or ".png"
            filename = f"{step_name}_{timestamp}{file_extension}"
            filepath = intermediates_dir / filename
            
            # Download image
            print(f"📥 Downloading intermediate image: {step_name}")
            response = requests.get(image_url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save to file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"💾 Intermediate image saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"⚠️  Failed to download intermediate image: {str(e)}")
            return None