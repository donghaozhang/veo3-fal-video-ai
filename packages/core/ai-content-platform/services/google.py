"""Google Vertex AI service integration."""

import asyncio
import time
import json
from pathlib import Path
from typing import Any, Dict, Optional

import google.generativeai as genai
from google.cloud import storage

from ai_content_platform.core.step import BaseStep
from ai_content_platform.core.models import StepConfig, StepResult
from ai_content_platform.core.exceptions import StepExecutionError
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.utils.file_manager import FileManager


class GoogleVeoStep(BaseStep):
    """Google Veo video generation step."""
    
    def __init__(self, config: StepConfig):
        super().__init__(config)
        self.logger = get_logger(__name__)
        self.file_manager = FileManager()
        
        # Initialize Google AI client
        api_key = self.config.parameters.get("api_key") or self._get_api_key_from_env()
        if api_key:
            genai.configure(api_key=api_key)
        
        # Setup Google Cloud Storage if needed
        self.project_id = self.config.parameters.get("project_id") or self._get_project_id_from_env()
        self.bucket_name = self.config.parameters.get("bucket_name")
        
        if self.project_id and self.bucket_name:
            self.storage_client = storage.Client(project=self.project_id)
            self.bucket = self.storage_client.bucket(self.bucket_name)
        else:
            self.storage_client = None
            self.bucket = None
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables."""
        import os
        return os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    def _get_project_id_from_env(self) -> Optional[str]:
        """Get project ID from environment variables."""
        import os
        return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("PROJECT_ID")
    
    def validate_config(self) -> bool:
        """Validate Google Veo configuration."""
        required_params = ["prompt"]
        
        for param in required_params:
            if param not in self.config.parameters:
                self.logger.error(f"Missing required parameter: {param}")
                return False
        
        return True
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute Google Veo video generation."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating video with Google Veo: {self.config.name}")
            
            # Get parameters
            prompt = self.config.parameters["prompt"]
            model_name = self.config.parameters.get("model", "veo-3")
            duration = self.config.parameters.get("duration", 5)
            
            # Check if we have an image input
            image_path = self.config.parameters.get("image_path")
            
            if image_path:
                # Image-to-video generation
                result = await self._generate_video_from_image(prompt, image_path, model_name, duration)
            else:
                # Text-to-video generation
                result = await self._generate_video_from_text(prompt, model_name, duration)
            
            # Download result if it's a GCS URL
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            if result.startswith("gs://"):
                output_path = await self._download_from_gcs(result, output_dir)
            else:
                output_path = await self.file_manager.download_file(
                    result, 
                    output_dir, 
                    f"{self.config.name}_{int(time.time())}.mp4"
                )
            
            self.logger.success(f"Video generated: {output_path}")
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "prompt": prompt,
                    "model": model_name,
                    "duration": duration,
                    "video_url": result,
                    "provider": "google_veo"
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"Google Veo video generation failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    async def _generate_video_from_text(
        self, 
        prompt: str, 
        model_name: str, 
        duration: int
    ) -> str:
        """Generate video from text prompt."""
        try:
            # Use the Gemini API for video generation
            model = genai.GenerativeModel(model_name)
            
            # Create generation config
            generation_config = {
                "temperature": self.config.parameters.get("temperature", 0.7),
                "max_output_tokens": self.config.parameters.get("max_tokens", 1000)
            }
            
            # For now, simulate video generation since actual Veo API access is limited
            # In real implementation, this would use the actual Veo API
            self.logger.info("Simulating Veo video generation (actual API requires allowlist)")
            
            # Simulate processing time
            await asyncio.sleep(2)
            
            # Return a placeholder or mock result
            # In actual implementation, this would return the real video URL
            return "gs://mock-bucket/generated-video.mp4"
            
        except Exception as e:
            raise StepExecutionError(f"Failed to generate video from text: {str(e)}") from e
    
    async def _generate_video_from_image(
        self, 
        prompt: str, 
        image_path: str, 
        model_name: str, 
        duration: int
    ) -> str:
        """Generate video from image and text prompt."""
        try:
            # Load image
            if image_path.startswith("http"):
                # Download image first
                temp_dir = Path("/tmp/ai_platform")
                temp_dir.mkdir(parents=True, exist_ok=True)
                local_image = await self.file_manager.download_file(image_path, temp_dir)
            else:
                local_image = Path(image_path)
            
            # Use the Gemini API for video generation
            model = genai.GenerativeModel(model_name)
            
            # Simulate image-to-video generation
            self.logger.info("Simulating Veo image-to-video generation")
            await asyncio.sleep(3)
            
            return "gs://mock-bucket/generated-video-from-image.mp4"
            
        except Exception as e:
            raise StepExecutionError(f"Failed to generate video from image: {str(e)}") from e
    
    async def _download_from_gcs(self, gcs_url: str, output_dir: Path) -> Path:
        """Download file from Google Cloud Storage."""
        try:
            if not self.storage_client:
                raise StepExecutionError("Google Cloud Storage not configured")
            
            # Parse GCS URL
            if not gcs_url.startswith("gs://"):
                raise StepExecutionError(f"Invalid GCS URL: {gcs_url}")
            
            url_parts = gcs_url[5:].split("/", 1)
            bucket_name = url_parts[0]
            blob_name = url_parts[1]
            
            # Download blob
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            output_path = output_dir / f"{self.config.name}_{int(time.time())}.mp4"
            
            await asyncio.to_thread(blob.download_to_filename, str(output_path))
            
            return output_path
            
        except Exception as e:
            raise StepExecutionError(f"Failed to download from GCS: {str(e)}") from e
    
    def estimate_cost(self) -> float:
        """Estimate cost for Google Veo generation."""
        duration = self.config.parameters.get("duration", 5)
        model = self.config.parameters.get("model", "veo-3")
        
        # Google Veo pricing (approximate)
        if "veo-3" in model.lower():
            return 6.0  # Base cost for Veo 3
        else:
            return 4.0  # Default cost


class GoogleGeminiStep(BaseStep):
    """Google Gemini text generation step."""
    
    def __init__(self, config: StepConfig):
        super().__init__(config)
        self.logger = get_logger(__name__)
        
        # Initialize Google AI client
        api_key = self.config.parameters.get("api_key") or self._get_api_key_from_env()
        if api_key:
            genai.configure(api_key=api_key)
        else:
            raise StepExecutionError("Google API key not found")
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables."""
        import os
        return os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    def validate_config(self) -> bool:
        """Validate Gemini configuration."""
        required_params = ["prompt"]
        
        for param in required_params:
            if param not in self.config.parameters:
                self.logger.error(f"Missing required parameter: {param}")
                return False
        
        return True
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute Gemini text generation."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating text with Gemini: {self.config.name}")
            
            # Get parameters
            prompt = self.config.parameters["prompt"]
            model_name = self.config.parameters.get("model", "gemini-1.5-pro")
            
            # Initialize model
            model = genai.GenerativeModel(model_name)
            
            # Generation config
            generation_config = genai.types.GenerationConfig(
                temperature=self.config.parameters.get("temperature", 0.7),
                max_output_tokens=self.config.parameters.get("max_tokens", 1000),
                top_p=self.config.parameters.get("top_p", 0.8),
                top_k=self.config.parameters.get("top_k", 40)
            )
            
            # Generate content
            response = await asyncio.to_thread(
                model.generate_content,
                prompt,
                generation_config=generation_config
            )
            
            generated_text = response.text
            
            # Save text file
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"{self.config.name}_{int(time.time())}.txt"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(generated_text)
            
            self.logger.success(f"Text generated: {output_path}")
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "prompt": prompt,
                    "model": model_name,
                    "generated_text": generated_text,
                    "provider": "google_gemini"
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"Gemini text generation failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    def estimate_cost(self) -> float:
        """Estimate cost for Gemini generation."""
        prompt = self.config.parameters.get("prompt", "")
        max_tokens = self.config.parameters.get("max_tokens", 1000)
        
        # Gemini pricing (approximate)
        input_tokens = len(prompt) / 4  # Rough estimate
        total_tokens = input_tokens + max_tokens
        
        return max(0.001, (total_tokens / 1000) * 0.001)  # $0.001 per 1k tokens