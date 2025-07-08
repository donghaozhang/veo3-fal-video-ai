"""
Image Understanding model integration for AI Content Pipeline
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
class ImageUnderstandingResult:
    """Result from image understanding analysis."""
    success: bool
    output_text: Optional[str] = None
    model_used: Optional[str] = None
    cost_estimate: float = 0.0
    processing_time: float = 0.0
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UnifiedImageUnderstandingGenerator:
    """
    Unified image understanding generator for the AI Content Pipeline.
    
    Integrates with the existing Gemini-based image analysis from video_tools.
    """
    
    def __init__(self):
        """Initialize the image understanding generator."""
        self.analyzer = None
        self._initialize_analyzer()
    
    def _initialize_analyzer(self):
        """Initialize the Gemini video analyzer for image understanding."""
        try:
            # Add the video_tools directory to Python path
            video_tools_path = Path(__file__).parent.parent.parent.parent / "video_tools"
            if video_tools_path.exists():
                sys.path.insert(0, str(video_tools_path))
                from video_utils.gemini_analyzer import GeminiVideoAnalyzer
                self.analyzer = GeminiVideoAnalyzer()
                print("✅ Gemini Image Understanding analyzer initialized")
            else:
                print("❌ Video tools directory not found")
                self.analyzer = None
        except Exception as e:
            print(f"❌ Failed to initialize Gemini analyzer: {e}")
            self.analyzer = None
    
    def get_available_models(self) -> list:
        """Get list of available models."""
        return [
            "gemini_describe",
            "gemini_detailed",
            "gemini_classify",
            "gemini_objects",
            "gemini_ocr",
            "gemini_composition",
            "gemini_qa"
        ]
    
    def analyze(self, 
                image_path: str,
                model: str = "gemini_describe",
                analysis_prompt: str = None,
                **kwargs) -> ImageUnderstandingResult:
        """
        Analyze image and return text description.
        
        Args:
            image_path: Path to image file or URL
            model: Analysis model to use
            analysis_prompt: Optional custom prompt for analysis
            **kwargs: Additional model-specific parameters
            
        Returns:
            ImageUnderstandingResult with analysis results
        """
        start_time = time.time()
        
        if not self.analyzer:
            return ImageUnderstandingResult(
                success=False,
                error="Gemini analyzer not available. Please check GEMINI_API_KEY."
            )
        
        try:
            print(f"🔍 Analyzing image with {model} model...")
            print(f"🖼️ Image: {image_path}")
            
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
                    return ImageUnderstandingResult(
                        success=False,
                        error=f"Failed to download image: {str(e)}"
                    )
            else:
                # Convert string path to Path object
                actual_image_path = Path(image_path)
            
            # Map model names to analyzer methods
            if model == "gemini_describe":
                result_text = self.analyzer.describe_image(actual_image_path, detailed=False)
            elif model == "gemini_detailed":
                result_text = self.analyzer.describe_image(actual_image_path, detailed=True)
            elif model == "gemini_classify":
                result_text = self.analyzer.classify_image(actual_image_path)
            elif model == "gemini_objects":
                result_text = self.analyzer.detect_objects(actual_image_path, detailed=True)
            elif model == "gemini_ocr":
                result_text = self.analyzer.extract_text_from_image(actual_image_path)
            elif model == "gemini_composition":
                result_text = self.analyzer.analyze_image_composition(actual_image_path)
            elif model == "gemini_qa":
                # Use custom prompt or default question
                question = analysis_prompt or kwargs.get("question", "What do you see in this image?")
                result_text = self.analyzer.answer_image_questions(actual_image_path, [question])
            else:
                return ImageUnderstandingResult(
                    success=False,
                    error=f"Unsupported model: {model}"
                )
            
            # Clean up temporary file if created
            if temp_file:
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            
            processing_time = time.time() - start_time
            
            if result_text:
                return ImageUnderstandingResult(
                    success=True,
                    output_text=result_text,
                    model_used=model,
                    cost_estimate=self._get_cost_estimate(model),
                    processing_time=processing_time,
                    metadata={
                        "model": model,
                        "image_path": image_path,
                        "analysis_type": self._get_analysis_type(model)
                    }
                )
            else:
                return ImageUnderstandingResult(
                    success=False,
                    error="Analysis returned empty result",
                    processing_time=processing_time
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            return ImageUnderstandingResult(
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    def _get_cost_estimate(self, model: str) -> float:
        """Get cost estimate for the model."""
        cost_mapping = {
            "gemini_describe": 0.001,
            "gemini_detailed": 0.002,
            "gemini_classify": 0.001,
            "gemini_objects": 0.002,
            "gemini_ocr": 0.001,
            "gemini_composition": 0.002,
            "gemini_qa": 0.001,
        }
        return cost_mapping.get(model, 0.001)
    
    def _get_analysis_type(self, model: str) -> str:
        """Get human-readable analysis type."""
        type_mapping = {
            "gemini_describe": "Basic Image Description",
            "gemini_detailed": "Detailed Image Analysis",
            "gemini_classify": "Image Classification",
            "gemini_objects": "Object Detection",
            "gemini_ocr": "Text Extraction (OCR)",
            "gemini_composition": "Composition Analysis",
            "gemini_qa": "Question & Answer",
        }
        return type_mapping.get(model, "Unknown Analysis")
    
    def get_model_info(self, model: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model."""
        model_info = {
            "gemini_describe": {
                "name": "Gemini Image Description",
                "provider": "Google Gemini",
                "best_for": "Basic image descriptions and summaries",
                "cost_per_analysis": "$0.001"
            },
            "gemini_detailed": {
                "name": "Gemini Detailed Analysis",
                "provider": "Google Gemini",
                "best_for": "Comprehensive image analysis with composition details",
                "cost_per_analysis": "$0.002"
            },
            "gemini_classify": {
                "name": "Gemini Image Classification",
                "provider": "Google Gemini",
                "best_for": "Categorizing and classifying image content",
                "cost_per_analysis": "$0.001"
            },
            "gemini_objects": {
                "name": "Gemini Object Detection",
                "provider": "Google Gemini",
                "best_for": "Identifying and locating objects in images",
                "cost_per_analysis": "$0.002"
            },
            "gemini_ocr": {
                "name": "Gemini OCR",
                "provider": "Google Gemini",
                "best_for": "Extracting text from images",
                "cost_per_analysis": "$0.001"
            },
            "gemini_composition": {
                "name": "Gemini Composition Analysis",
                "provider": "Google Gemini",
                "best_for": "Analyzing artistic and technical composition",
                "cost_per_analysis": "$0.002"
            },
            "gemini_qa": {
                "name": "Gemini Q&A",
                "provider": "Google Gemini",
                "best_for": "Answering specific questions about images",
                "cost_per_analysis": "$0.001"
            }
        }
        
        return model_info.get(model)