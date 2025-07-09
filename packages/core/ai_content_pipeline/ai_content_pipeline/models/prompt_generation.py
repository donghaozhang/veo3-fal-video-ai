"""
Prompt Generation model integration for AI Content Pipeline
"""

import os
import sys
import time
import requests
import tempfile
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class PromptGenerationResult:
    """Result from prompt generation analysis."""
    success: bool
    output_text: Optional[str] = None
    extracted_prompt: Optional[str] = None
    model_used: Optional[str] = None
    cost_estimate: float = 0.0
    processing_time: float = 0.0
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UnifiedPromptGenerator:
    """
    Unified prompt generator for the AI Content Pipeline.
    
    Specializes in creating optimized prompts for image-to-video generation
    using OpenRouter's multi-model capabilities.
    """
    
    def __init__(self):
        """Initialize the prompt generator."""
        self.analyzer = None
        self._initialize_analyzer()
    
    def _initialize_analyzer(self):
        """Initialize the OpenRouter analyzer for prompt generation."""
        try:
            # Add the video_tools directory to Python path
            video_tools_path = Path(__file__).parent.parent.parent.parent / "video_tools"
            if video_tools_path.exists():
                sys.path.insert(0, str(video_tools_path))
                from video_utils.openrouter_analyzer import OpenRouterAnalyzer
                
                # Use Gemini 2.0 Flash for fast and high-quality prompt generation
                self.analyzer = OpenRouterAnalyzer(model="google/gemini-2.0-flash-001")
                print("✅ OpenRouter Prompt Generator initialized")
            else:
                print("❌ Video tools directory not found")
                self.analyzer = None
        except Exception as e:
            print(f"❌ Failed to initialize OpenRouter analyzer: {e}")
            self.analyzer = None
    
    def get_available_models(self) -> list:
        """Get list of available models."""
        return [
            "openrouter_video_prompt",
            "openrouter_video_cinematic",
            "openrouter_video_realistic",
            "openrouter_video_artistic",
            "openrouter_video_dramatic"
        ]
    
    def generate(self, 
                image_path: str,
                model: str = "openrouter_video_prompt",
                background_context: str = "",
                **kwargs) -> PromptGenerationResult:
        """
        Generate optimized video prompt from image and context.
        
        Args:
            image_path: Path to image file or URL
            model: Prompt generation model to use
            background_context: Additional context about the scene or desired outcome
            **kwargs: Additional model-specific parameters
            
        Returns:
            PromptGenerationResult with generated prompt
        """
        start_time = time.time()
        
        if not self.analyzer:
            return PromptGenerationResult(
                success=False,
                error="OpenRouter analyzer not available. Please check OPENROUTER_API_KEY."
            )
        
        try:
            print(f"🎬 Generating video prompt with {model} model...")
            print(f"🖼️ Image: {image_path}")
            if background_context:
                print(f"📝 Context: {background_context}")
            
            # Handle both URLs and local file paths
            temp_file = None
            actual_image_path = image_path
            
            if isinstance(image_path, str) and image_path.startswith(('http://', 'https://')):
                # Download image from URL to temporary file
                print(f"📥 Downloading image from URL...")
                try:
                    response = requests.get(image_path, timeout=30)
                    response.raise_for_status()
                    
                    # Create temporary file with appropriate extension
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                    temp_file.write(response.content)
                    temp_file.close()
                    actual_image_path = Path(temp_file.name)
                    print(f"✅ Image downloaded to: {actual_image_path}")
                except Exception as e:
                    return PromptGenerationResult(
                        success=False,
                        error=f"Failed to download image: {str(e)}"
                    )
            else:
                # Convert string path to Path object
                actual_image_path = Path(image_path)
            
            # Map model names to video styles and parameters
            style_mapping = {
                "openrouter_video_prompt": ("cinematic", "medium"),
                "openrouter_video_cinematic": ("cinematic", "medium"),
                "openrouter_video_realistic": ("realistic", "medium"),
                "openrouter_video_artistic": ("artistic", "long"),
                "openrouter_video_dramatic": ("dramatic", "medium"),
            }
            
            video_style, duration_preference = style_mapping.get(model, ("cinematic", "medium"))
            
            # Override with kwargs if provided
            video_style = kwargs.get("video_style", video_style)
            duration_preference = kwargs.get("duration_preference", duration_preference)
            
            # Generate comprehensive video prompt analysis
            result_analysis = self.analyzer.generate_video_prompt(
                actual_image_path,
                background_context=background_context,
                video_style=video_style,
                duration_preference=duration_preference
            )
            
            # Extract the optimized prompt
            extracted_prompt = self.analyzer.extract_optimized_prompt(result_analysis)
            
            # Clean up temporary file if created
            if temp_file:
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            
            processing_time = time.time() - start_time
            
            if result_analysis:
                return PromptGenerationResult(
                    success=True,
                    output_text=result_analysis,
                    extracted_prompt=extracted_prompt,
                    model_used=model,
                    cost_estimate=self._get_cost_estimate(model),
                    processing_time=processing_time,
                    metadata={
                        "model": model,
                        "image_path": image_path,
                        "background_context": background_context,
                        "video_style": video_style,
                        "duration_preference": duration_preference,
                        "openrouter_model": "google/gemini-2.0-flash-001"
                    }
                )
            else:
                return PromptGenerationResult(
                    success=False,
                    error="Prompt generation returned empty result",
                    processing_time=processing_time
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            return PromptGenerationResult(
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    def _get_cost_estimate(self, model: str) -> float:
        """Get cost estimate for the model."""
        cost_mapping = {
            "openrouter_video_prompt": 0.002,
            "openrouter_video_cinematic": 0.002,
            "openrouter_video_realistic": 0.002,
            "openrouter_video_artistic": 0.002,
            "openrouter_video_dramatic": 0.002,
        }
        return cost_mapping.get(model, 0.002)
    
    def get_model_info(self, model: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model."""
        model_info = {
            "openrouter_video_prompt": {
                "name": "OpenRouter Video Prompt Generator",
                "provider": "OpenRouter (Gemini 2.0 Flash)",
                "best_for": "General purpose video prompt generation",
                "style": "Cinematic",
                "cost_per_generation": "$0.002"
            },
            "openrouter_video_cinematic": {
                "name": "OpenRouter Cinematic Video Prompts",
                "provider": "OpenRouter (Gemini 2.0 Flash)",
                "best_for": "Movie-style, cinematic video sequences",
                "style": "Cinematic",
                "cost_per_generation": "$0.002"
            },
            "openrouter_video_realistic": {
                "name": "OpenRouter Realistic Video Prompts",
                "provider": "OpenRouter (Gemini 2.0 Flash)",
                "best_for": "Natural, documentary-style video content",
                "style": "Realistic",
                "cost_per_generation": "$0.002"
            },
            "openrouter_video_artistic": {
                "name": "OpenRouter Artistic Video Prompts",
                "provider": "OpenRouter (Gemini 2.0 Flash)",
                "best_for": "Creative, abstract, and artistic video sequences",
                "style": "Artistic",
                "cost_per_generation": "$0.002"
            },
            "openrouter_video_dramatic": {
                "name": "OpenRouter Dramatic Video Prompts",
                "provider": "OpenRouter (Gemini 2.0 Flash)",
                "best_for": "High-emotion, dramatic video sequences",
                "style": "Dramatic",
                "cost_per_generation": "$0.002"
            }
        }
        
        return model_info.get(model)


def test_prompt_generation():
    """Test function for prompt generation."""
    generator = UnifiedPromptGenerator()
    
    if not generator.analyzer:
        print("❌ OpenRouter not available for testing")
        return False
    
    print("✅ Prompt generator ready for testing")
    return True


if __name__ == "__main__":
    # Basic test
    success = test_prompt_generation()
    print(f"🧪 Test result: {'PASSED' if success else 'FAILED'}")