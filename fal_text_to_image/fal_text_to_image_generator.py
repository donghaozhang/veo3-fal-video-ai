"""
FAL AI Text-to-Image Generator

This module provides a unified interface for generating images using four different
FAL AI text-to-image models:
1. Imagen 4 Preview Fast - Cost-effective Google model
2. Seedream v3 - Bilingual (Chinese/English) text-to-image model  
3. FLUX.1 Schnell - Fastest inference FLUX model
4. FLUX.1 Dev - High-quality 12B parameter FLUX model

Author: AI Assistant
Date: 2024
"""

import os
import requests
import time
from typing import Dict, Any, Optional, List
import fal_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FALTextToImageGenerator:
    """
    A unified text-to-image generator supporting multiple FAL AI models.
    
    Supported models:
    - imagen4: fal-ai/imagen4/preview/fast
    - seedream: fal-ai/bytedance/seedream/v3/text-to-image  
    - flux_schnell: fal-ai/flux-1/schnell
    - flux_dev: fal-ai/flux-1/dev
    """
    
    # Model endpoint mappings
    MODEL_ENDPOINTS = {
        "imagen4": "fal-ai/imagen4/preview/fast",
        "seedream": "fal-ai/bytedance/seedream/v3/text-to-image",
        "flux_schnell": "fal-ai/flux-1/schnell", 
        "flux_dev": "fal-ai/flux-1/dev"
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FAL Text-to-Image Generator.
        
        Args:
            api_key: FAL AI API key. If not provided, will try to load from environment.
        """
        self.api_key = api_key or os.getenv('FAL_KEY')
        if not self.api_key:
            raise ValueError("FAL_KEY not found in environment variables or provided as parameter")
        
        # Set the API key for fal_client
        os.environ['FAL_KEY'] = self.api_key
        
        # Model-specific default parameters
        self.model_defaults = {
            "imagen4": {
                "image_size": "landscape_4_3",  # Options: square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9
                "num_inference_steps": 4,
                "guidance_scale": 3.0,
                "num_images": 1,
                "enable_safety_checker": True
            },
            "seedream": {
                "image_size": "1024x1024",  # Options: 512x512, 768x768, 1024x1024, 1152x896, 896x1152
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "num_images": 1,
                "seed": None  # Random if None
            },
            "flux_schnell": {
                "image_size": "landscape_4_3",  # Options: square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9
                "num_inference_steps": 4,  # Schnell is optimized for 1-4 steps
                "num_images": 1,
                "enable_safety_checker": True
            },
            "flux_dev": {
                "image_size": "landscape_4_3",  # Options: square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9  
                "num_inference_steps": 28,  # Dev typically uses more steps for quality
                "guidance_scale": 3.5,
                "num_images": 1,
                "enable_safety_checker": True
            }
        }
    
    def validate_model(self, model: str) -> str:
        """
        Validate and return the model endpoint.
        
        Args:
            model: Model name (imagen4, seedream, flux_schnell, flux_dev)
            
        Returns:
            Model endpoint string
            
        Raises:
            ValueError: If model is not supported
        """
        if model not in self.MODEL_ENDPOINTS:
            available_models = ", ".join(self.MODEL_ENDPOINTS.keys())
            raise ValueError(f"Model '{model}' not supported. Available models: {available_models}")
        
        return self.MODEL_ENDPOINTS[model]
    
    def generate_image(
        self,
        prompt: str,
        model: str = "flux_schnell",
        negative_prompt: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate an image using the specified model.
        
        Args:
            prompt: Text description of the image to generate
            model: Model to use (imagen4, seedream, flux_schnell, flux_dev)
            negative_prompt: What to avoid in the image (not supported by all models)
            **kwargs: Model-specific parameters
            
        Returns:
            Dictionary containing image URL and metadata
        """
        endpoint = self.validate_model(model)
        
        # Get default parameters for the model
        default_params = self.model_defaults[model].copy()
        
        # Override with provided kwargs
        default_params.update(kwargs)
        
        # Build the request payload
        payload = {
            "prompt": prompt,
            **default_params
        }
        
        # Add negative prompt if supported and provided
        if negative_prompt and model in ["seedream", "flux_dev"]:
            payload["negative_prompt"] = negative_prompt
        
        try:
            print(f"🎨 Generating image with {model} model...")
            print(f"📝 Prompt: {prompt}")
            if negative_prompt and model in ["seedream", "flux_dev"]:
                print(f"❌ Negative prompt: {negative_prompt}")
            
            # Submit the request
            result = fal_client.subscribe(
                endpoint,
                arguments=payload,
                with_logs=True
            )
            
            if result and 'images' in result and len(result['images']) > 0:
                image_data = result['images'][0]
                
                response = {
                    'success': True,
                    'model': model,
                    'endpoint': endpoint,
                    'image_url': image_data['url'],
                    'image_size': str(image_data.get('width', 'unknown')) + 'x' + str(image_data.get('height', 'unknown')) if 'width' in image_data else 'unknown',
                    'prompt': prompt,
                    'negative_prompt': negative_prompt,
                    'parameters': payload,
                    'full_result': result
                }
                
                print(f"✅ Image generated successfully!")
                print(f"🔗 Image URL: {response['image_url']}")
                
                return response
            else:
                raise Exception("No images returned from API")
                
        except Exception as e:
            print(f"❌ Error generating image: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model': model,
                'endpoint': endpoint,
                'prompt': prompt
            }
    
    def generate_with_imagen4(
        self,
        prompt: str,
        image_size: str = "landscape_4_3",
        num_inference_steps: int = 4,
        guidance_scale: float = 3.0,
        num_images: int = 1,
        enable_safety_checker: bool = True
    ) -> Dict[str, Any]:
        """
        Generate image using Imagen 4 Preview Fast model.
        
        Args:
            prompt: Text description
            image_size: Image aspect ratio (square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9)
            num_inference_steps: Number of denoising steps (1-8, default 4)
            guidance_scale: How closely to follow the prompt (1.0-10.0, default 3.0)
            num_images: Number of images to generate (1-4, default 1)
            enable_safety_checker: Enable safety filtering
            
        Returns:
            Generation result dictionary
        """
        return self.generate_image(
            prompt=prompt,
            model="imagen4",
            image_size=image_size,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            num_images=num_images,
            enable_safety_checker=enable_safety_checker
        )
    
    def generate_with_seedream(
        self,
        prompt: str,
        image_size: str = "1024x1024",
        num_inference_steps: int = 20,
        guidance_scale: float = 7.5,
        negative_prompt: Optional[str] = None,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate image using Seedream v3 model (supports Chinese and English).
        
        Args:
            prompt: Text description (Chinese or English)
            image_size: Image dimensions (512x512, 768x768, 1024x1024, 1152x896, 896x1152)
            num_inference_steps: Number of denoising steps (1-50, default 20)
            guidance_scale: How closely to follow the prompt (1.0-20.0, default 7.5)
            negative_prompt: What to avoid in the image
            seed: Random seed for reproducibility
            
        Returns:
            Generation result dictionary
        """
        return self.generate_image(
            prompt=prompt,
            model="seedream",
            image_size=image_size,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            negative_prompt=negative_prompt,
            seed=seed
        )
    
    def generate_with_flux_schnell(
        self,
        prompt: str,
        image_size: str = "landscape_4_3",
        num_inference_steps: int = 4,
        num_images: int = 1,
        enable_safety_checker: bool = True
    ) -> Dict[str, Any]:
        """
        Generate image using FLUX.1 Schnell (fastest) model.
        
        Args:
            prompt: Text description
            image_size: Image aspect ratio (square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9)
            num_inference_steps: Number of denoising steps (1-4 recommended, default 4)
            num_images: Number of images to generate (1-4, default 1)
            enable_safety_checker: Enable safety filtering
            
        Returns:
            Generation result dictionary
        """
        return self.generate_image(
            prompt=prompt,
            model="flux_schnell",
            image_size=image_size,
            num_inference_steps=num_inference_steps,
            num_images=num_images,
            enable_safety_checker=enable_safety_checker
        )
    
    def generate_with_flux_dev(
        self,
        prompt: str,
        image_size: str = "landscape_4_3",
        num_inference_steps: int = 28,
        guidance_scale: float = 3.5,
        negative_prompt: Optional[str] = None,
        num_images: int = 1,
        enable_safety_checker: bool = True
    ) -> Dict[str, Any]:
        """
        Generate image using FLUX.1 Dev (high-quality) model.
        
        Args:
            prompt: Text description
            image_size: Image aspect ratio (square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9)
            num_inference_steps: Number of denoising steps (1-50, default 28)
            guidance_scale: How closely to follow the prompt (1.0-10.0, default 3.5)
            negative_prompt: What to avoid in the image
            num_images: Number of images to generate (1-4, default 1)
            enable_safety_checker: Enable safety filtering
            
        Returns:
            Generation result dictionary
        """
        return self.generate_image(
            prompt=prompt,
            model="flux_dev",
            image_size=image_size,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            negative_prompt=negative_prompt,
            num_images=num_images,
            enable_safety_checker=enable_safety_checker
        )
    
    def download_image(self, image_url: str, output_folder: str = "output", filename: Optional[str] = None) -> str:
        """
        Download an image from URL to local folder.
        
        Args:
            image_url: URL of the image to download
            output_folder: Local folder to save the image
            filename: Custom filename (optional)
            
        Returns:
            Path to the downloaded image
        """
        try:
            # Create output folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)
            
            # Generate filename if not provided
            if not filename:
                timestamp = int(time.time())
                filename = f"generated_image_{timestamp}.png"
            
            # Ensure filename has extension
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                filename += '.png'
            
            filepath = os.path.join(output_folder, filename)
            
            # Download the image
            print(f"⬇️ Downloading image to: {filepath}")
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Image downloaded successfully!")
            return filepath
            
        except Exception as e:
            print(f"❌ Error downloading image: {str(e)}")
            raise
    
    def compare_models(
        self,
        prompt: str,
        models: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
        output_folder: str = "output"
    ) -> Dict[str, Any]:
        """
        Generate images with multiple models for comparison.
        
        Args:
            prompt: Text description
            models: List of models to compare (default: all models)
            negative_prompt: What to avoid (only used for compatible models)
            output_folder: Folder to save comparison images
            
        Returns:
            Dictionary with results from all models
        """
        if models is None:
            models = list(self.MODEL_ENDPOINTS.keys())
        
        print(f"🔄 Comparing {len(models)} models...")
        print(f"💰 Estimated cost: ~${len(models) * 0.01:.2f} (${0.01} per image)")
        
        confirm = input("⚠️ This will generate multiple images and cost money. Continue? (y/N): ")
        if confirm.lower() not in ['y', 'yes']:
            print("❌ Comparison cancelled.")
            return {'cancelled': True}
        
        results = {}
        
        for model in models:
            print(f"\n🎨 Generating with {model}...")
            
            try:
                result = self.generate_image(
                    prompt=prompt,
                    model=model,
                    negative_prompt=negative_prompt
                )
                
                if result['success']:
                    # Download image for comparison
                    filename = f"comparison_{model}_{int(time.time())}.png"
                    local_path = self.download_image(
                        result['image_url'],
                        output_folder,
                        filename
                    )
                    result['local_path'] = local_path
                
                results[model] = result
                
            except Exception as e:
                print(f"❌ Error with {model}: {str(e)}")
                results[model] = {
                    'success': False,
                    'error': str(e),
                    'model': model
                }
        
        # Summary
        successful = sum(1 for r in results.values() if r.get('success', False))
        print(f"\n📊 Comparison complete: {successful}/{len(models)} models succeeded")
        
        return results
    
    def get_model_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all supported models.
        
        Returns:
            Dictionary with model information and capabilities
        """
        return {
            "imagen4": {
                "name": "Imagen 4 Preview Fast",
                "endpoint": self.MODEL_ENDPOINTS["imagen4"],
                "description": "Google's cost-effective text-to-image model",
                "strengths": ["Fast generation", "Cost-effective", "Good quality"],
                "supported_features": ["Safety checker", "Multiple aspect ratios"],
                "max_steps": 8,
                "supports_negative_prompt": False
            },
            "seedream": {
                "name": "Seedream v3",
                "endpoint": self.MODEL_ENDPOINTS["seedream"],
                "description": "Bilingual (Chinese/English) text-to-image model",
                "strengths": ["Bilingual support", "High quality", "Flexible sizing"],
                "supported_features": ["Negative prompts", "Custom seeds", "Multiple sizes"],
                "max_steps": 50,
                "supports_negative_prompt": True
            },
            "flux_schnell": {
                "name": "FLUX.1 Schnell",
                "endpoint": self.MODEL_ENDPOINTS["flux_schnell"],
                "description": "Fastest FLUX model optimized for speed",
                "strengths": ["Ultra-fast generation", "Good quality", "Low cost"],
                "supported_features": ["Safety checker", "Multiple aspect ratios"],
                "max_steps": 4,
                "supports_negative_prompt": False
            },
            "flux_dev": {
                "name": "FLUX.1 Dev",
                "endpoint": self.MODEL_ENDPOINTS["flux_dev"],
                "description": "High-quality 12B parameter FLUX model",
                "strengths": ["Highest quality", "Detailed images", "Professional results"],
                "supported_features": ["Negative prompts", "Guidance scale", "Safety checker"],
                "max_steps": 50,
                "supports_negative_prompt": True
            }
        }


if __name__ == "__main__":
    # Example usage
    try:
        generator = FALTextToImageGenerator()
        
        # Test with FLUX Schnell (fastest)
        result = generator.generate_with_flux_schnell(
            prompt="A beautiful sunset over mountains, digital art style",
            image_size="landscape_4_3"
        )
        
        if result['success']:
            print(f"Generated image: {result['image_url']}")
            # Download the image
            local_path = generator.download_image(result['image_url'])
            print(f"Saved to: {local_path}")
        else:
            print(f"Generation failed: {result['error']}")
            
    except Exception as e:
        print(f"Error: {e}")
