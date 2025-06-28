"""
FAL AI Image-to-Image Generator with Multi-Model Support

This module provides a Python interface for modifying images using multiple FAL AI models:
1. Luma Photon Flash - Creative image modification and personalization
2. FLUX Kontext Dev - Contextual image editing with precise control
3. ByteDance SeedEdit v3 - Accurate editing with content preservation

Features:
- Multi-model support for different editing needs
- Image modification with text prompts
- Adjustable parameters per model
- Multiple aspect ratio support (Photon only)
- Fast processing with high-quality results
- Support for both local and remote images

API Endpoints:
- fal-ai/luma-photon/flash/modify (Photon Flash)
- fal-ai/flux-kontext/dev (FLUX Kontext)
- fal-ai/bytedance/seededit/v3/edit-image (SeedEdit v3)

Author: AI Assistant
Date: 2024
"""

import os
import requests
import time
from typing import Dict, Any, Optional, List, Literal
import fal_client
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Supported models
ModelType = Literal["photon", "photon_base", "kontext", "seededit"]

# Supported aspect ratios (Photon Flash only)
AspectRatio = Literal["1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21"]

ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21"]
SUPPORTED_MODELS = ["photon", "photon_base", "kontext", "kontext_multi", "seededit"]

# Supported aspect ratios for FLUX Kontext Multi
KONTEXT_MULTI_ASPECT_RATIOS = ["21:9", "16:9", "4:3", "3:2", "1:1", "2:3", "3:4", "9:16", "9:21"]

class FALImageToImageGenerator:
    """
    FAL AI Image-to-Image Generator with Multi-Model Support
    
    This class provides methods to modify existing images using text prompts
    with multiple FAL AI models:
    - Luma Photon Flash: Creative modifications with aspect ratio control
    - FLUX Kontext Dev: Contextual editing with precise control
    - ByteDance SeedEdit v3: Accurate editing with content preservation
    """
    
    MODEL_ENDPOINTS = {
        "photon": "fal-ai/luma-photon/flash/modify",
        "photon_base": "fal-ai/luma-photon/modify",
        "kontext": "fal-ai/flux-kontext/dev",
        "kontext_multi": "fal-ai/flux-pro/kontext/max/multi",
        "seededit": "fal-ai/bytedance/seededit/v3/edit-image"
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FAL Image-to-Image Generator.
        
        Args:
            api_key: FAL AI API key. If not provided, will try to load from environment.
        """
        # Set API key
        if api_key:
            fal_client.api_key = api_key
        else:
            api_key = os.getenv('FAL_KEY')
            if not api_key:
                raise ValueError("FAL_KEY environment variable is not set. Please set it or provide api_key parameter.")
            fal_client.api_key = api_key
        
        # Create output directories
        self.output_dir = Path("output")
        self.test_output_dir = Path("test_output")
        self.output_dir.mkdir(exist_ok=True)
        self.test_output_dir.mkdir(exist_ok=True)
    
    def get_model_info(self, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about supported models.
        
        Args:
            model: Specific model to get info for ("photon" or "kontext"). If None, returns all models.
        
        Returns:
            Dictionary containing model information
        """
        photon_info = {
            "model_name": "Luma Photon Flash",
            "endpoint": self.MODEL_ENDPOINTS["photon"],
            "description": "Creative, personalizable, and intelligent image modification model",
            "supported_aspect_ratios": ASPECT_RATIOS,
            "strength_range": "0.0 - 1.0",
            "features": [
                "Fast processing",
                "High-quality results",
                "Creative modifications",
                "Personalizable outputs",
                "Aspect ratio control"
            ]
        }
        
        photon_base_info = {
            "model_name": "Luma Photon Base",
            "endpoint": self.MODEL_ENDPOINTS["photon_base"],
            "description": "Most creative, personalizable, and intelligent visual model for creatives",
            "supported_aspect_ratios": ASPECT_RATIOS,
            "strength_range": "0.0 - 1.0",
            "cost_per_megapixel": "$0.019",
            "features": [
                "Step-function change in cost",
                "High-quality image generation",
                "Creative image editing",
                "Prompt-based modifications",
                "Commercial use ready"
            ]
        }
        
        kontext_info = {
            "model_name": "FLUX Kontext Dev",
            "endpoint": self.MODEL_ENDPOINTS["kontext"],
            "description": "Frontier image editing model focused on contextual understanding",
            "supported_aspect_ratios": ["auto", "match_input"],
            "inference_steps_range": "1 - 50 (default: 28)",
            "guidance_scale_range": "1.0 - 20.0 (default: 2.5)",
            "features": [
                "Contextual understanding",
                "Nuanced modifications",
                "Style preservation",
                "Iterative editing",
                "Precise control"
            ]
        }
        
        kontext_multi_info = {
            "model_name": "FLUX Kontext [max] Multi",
            "endpoint": self.MODEL_ENDPOINTS["kontext_multi"],
            "description": "Experimental multi-image version of FLUX Kontext [max] with advanced capabilities",
            "supported_aspect_ratios": KONTEXT_MULTI_ASPECT_RATIOS,
            "guidance_scale_range": "1.0 - 20.0 (default: 3.5)",
            "num_images_range": "1 - 10 (default: 1)",
            "features": [
                "Multi-image input support",
                "Advanced contextual understanding",
                "Experimental capabilities",
                "High-quality results",
                "Safety tolerance control",
                "Multiple output formats"
            ]
        }
        
        seededit_info = {
            "model_name": "ByteDance SeedEdit v3",
            "endpoint": self.MODEL_ENDPOINTS["seededit"],
            "description": "Accurate image editing model with excellent content preservation",
            "guidance_scale_range": "0.0 - 1.0 (default: 0.5)",
            "seed_support": "Yes (optional)",
            "features": [
                "Accurate editing instruction following",
                "Effective content preservation",
                "Commercial use ready",
                "Simple parameter set",
                "High-quality results",
                "ByteDance developed"
            ]
        }
        
        if model == "photon":
            return photon_info
        elif model == "photon_base":
            return photon_base_info
        elif model == "kontext":
            return kontext_info
        elif model == "kontext_multi":
            return kontext_multi_info
        elif model == "seededit":
            return seededit_info
        else:
            return {
                "photon": photon_info,
                "photon_base": photon_base_info,
                "kontext": kontext_info,
                "kontext_multi": kontext_multi_info,
                "seededit": seededit_info
            }
    
    def validate_model(self, model: str) -> str:
        """
        Validate and return the model type.
        
        Args:
            model: Model type string ("photon" or "kontext")
            
        Returns:
            Validated model type
            
        Raises:
            ValueError: If model is not supported
        """
        if model not in SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model: {model}. Supported models: {SUPPORTED_MODELS}")
        return model
    
    def validate_aspect_ratio(self, aspect_ratio: str, model: str = "photon") -> str:
        """
        Validate and return the aspect ratio.
        
        Args:
            aspect_ratio: Aspect ratio string
            model: Model type ("photon" or "kontext")
            
        Returns:
            Validated aspect ratio
            
        Raises:
            ValueError: If aspect ratio is not supported for the model
        """
        if model in ["photon", "photon_base"]:
            if aspect_ratio not in ASPECT_RATIOS:
                raise ValueError(f"Unsupported aspect ratio for Photon models: {aspect_ratio}. Supported ratios: {ASPECT_RATIOS}")
        elif model == "kontext":
            # Kontext uses resolution_mode instead of aspect_ratio
            valid_modes = ["auto", "match_input"]
            if aspect_ratio not in valid_modes:
                raise ValueError(f"Unsupported resolution mode for Kontext: {aspect_ratio}. Supported modes: {valid_modes}")
        return aspect_ratio
    
    def validate_strength(self, strength: float) -> float:
        """
        Validate and return the modification strength (Photon only).
        
        Args:
            strength: Modification strength (0-1)
            
        Returns:
            Validated strength value
            
        Raises:
            ValueError: If strength is not in valid range
        """
        if not 0.0 <= strength <= 1.0:
            raise ValueError(f"Strength must be between 0.0 and 1.0, got: {strength}")
        return strength
    
    def validate_inference_steps(self, steps: int) -> int:
        """
        Validate and return inference steps (Kontext only).
        
        Args:
            steps: Number of inference steps (1-50)
            
        Returns:
            Validated steps value
            
        Raises:
            ValueError: If steps is not in valid range
        """
        if not 1 <= steps <= 50:
            raise ValueError(f"Inference steps must be between 1 and 50, got: {steps}")
        return steps
    
    def validate_guidance_scale(self, scale: float) -> float:
        """
        Validate and return guidance scale (Kontext only).
        
        Args:
            scale: Guidance scale (1.0-20.0)
            
        Returns:
            Validated scale value
            
        Raises:
            ValueError: If scale is not in valid range
        """
        if not 1.0 <= scale <= 20.0:
            raise ValueError(f"Guidance scale must be between 1.0 and 20.0, got: {scale}")
        return scale
    
    def upload_local_image(self, image_path: str) -> str:
        """
        Upload a local image to FAL AI and return the URL.
        
        Args:
            image_path: Path to local image file
            
        Returns:
            URL of uploaded image
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            Exception: If upload fails
        """
        image_file = Path(image_path)
        if not image_file.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            # Upload file to FAL AI
            url = fal_client.upload_file(str(image_file))
            print(f"✅ Image uploaded successfully: {url}")
            return url
        except Exception as e:
            raise Exception(f"Failed to upload image: {e}")
    
    def modify_image(
        self,
        prompt: str,
        image_url: str,
        model: ModelType = "photon",
        strength: Optional[float] = None,
        aspect_ratio: Optional[str] = None,
        num_inference_steps: int = 28,
        guidance_scale: float = 2.5,
        seed: Optional[int] = None,
        resolution_mode: str = "auto",
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Modify an image using text prompt with multiple model options.
        
        Args:
            prompt: Text instruction for modifying the image
            image_url: URL of the input image
            model: Model to use ("photon", "kontext", "seededit", default: "photon")
            strength: Modification intensity for Photon (0-1, default: 0.8)
            aspect_ratio: Output aspect ratio for Photon (default: "1:1")
            num_inference_steps: Inference steps for Kontext (1-50, default: 28)
            guidance_scale: Guidance scale for Kontext (1.0-20.0, default: 2.5) or SeedEdit (0.0-1.0, default: 0.5)
            seed: Random seed for reproducible results (Kontext and SeedEdit)
            resolution_mode: Resolution mode for Kontext ("auto" or "match_input")
            output_dir: Custom output directory (optional)
            
        Returns:
            Dictionary containing generation results and file paths
        """
        # Validate model
        self.validate_model(model)
        
        # Set defaults based on model
        if model in ["photon", "photon_base"]:
            if strength is None:
                strength = 0.8
            if aspect_ratio is None:
                aspect_ratio = "1:1"
            
            # Validate Photon parameters
            self.validate_strength(strength)
            self.validate_aspect_ratio(aspect_ratio, model)
            
            # Prepare Photon arguments
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "strength": strength,
                "aspect_ratio": aspect_ratio
            }
            
            model_name = "Luma Photon Flash" if model == "photon" else "Luma Photon Base"
            print(f"🎨 Modifying image with {model_name}...")
            print(f"   Prompt: {prompt}")
            print(f"   Strength: {strength}")
            print(f"   Aspect Ratio: {aspect_ratio}")
            
        elif model == "seededit":
            # Set SeedEdit defaults
            if guidance_scale == 2.5:  # Default Kontext value, change for SeedEdit
                guidance_scale = 0.5
            
            # Validate SeedEdit parameters
            if not 0.0 <= guidance_scale <= 1.0:
                raise ValueError(f"SeedEdit guidance scale must be between 0.0 and 1.0, got: {guidance_scale}")
            
            # Prepare SeedEdit arguments
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "guidance_scale": guidance_scale
            }
            
            if seed is not None:
                arguments["seed"] = seed
            
            print(f"🎨 Modifying image with ByteDance SeedEdit v3...")
            print(f"   Prompt: {prompt}")
            print(f"   Guidance Scale: {guidance_scale}")
            if seed is not None:
                print(f"   Seed: {seed}")
            
        else:  # kontext
            # Validate Kontext parameters
            self.validate_inference_steps(num_inference_steps)
            self.validate_guidance_scale(guidance_scale)
            self.validate_aspect_ratio(resolution_mode, model)
            
            # Prepare Kontext arguments
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "resolution_mode": resolution_mode
            }
            
            if seed is not None:
                arguments["seed"] = seed
            
            print(f"🎨 Modifying image with FLUX Kontext Dev...")
            print(f"   Prompt: {prompt}")
            print(f"   Inference Steps: {num_inference_steps}")
            print(f"   Guidance Scale: {guidance_scale}")
            print(f"   Resolution Mode: {resolution_mode}")
        
        try:
            # Generate image
            start_time = time.time()
            result = fal_client.subscribe(
                self.MODEL_ENDPOINTS[model],
                arguments=arguments
            )
            end_time = time.time()
            
            processing_time = end_time - start_time
            print(f"✅ Generation completed in {processing_time:.2f} seconds")
            
            # Process results - handle different response formats
            images = []
            if "images" in result:
                # Standard format (Photon, Kontext)
                images = result.get("images", [])
            elif "image" in result:
                # SeedEdit v3 format (single image object)
                images = [result["image"]]
            
            if not images:
                raise Exception("No images generated")
            
            # Download images
            output_directory = Path(output_dir) if output_dir else self.output_dir
            output_directory.mkdir(exist_ok=True)
            
            downloaded_files = []
            for i, image_info in enumerate(images):
                image_url = image_info.get("url")
                if image_url:
                    # Generate filename
                    timestamp = int(time.time())
                    filename = f"modified_image_{timestamp}_{i+1}.png"
                    file_path = output_directory / filename
                    
                    # Download image
                    response = requests.get(image_url)
                    response.raise_for_status()
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    downloaded_files.append(str(file_path))
                    print(f"✅ Image saved: {file_path}")
            
            # Build result dictionary based on model
            model_display_name = {
                "photon": "Luma Photon Flash",
                "photon_base": "Luma Photon Base",
                "kontext": "FLUX Kontext Dev",
                "seededit": "ByteDance SeedEdit v3"
            }.get(model, model)
            
            result_dict = {
                "success": True,
                "model": model_display_name,
                "prompt": prompt,
                "processing_time": processing_time,
                "images": images,
                "downloaded_files": downloaded_files,
                "output_directory": str(output_directory)
            }
            
            # Add model-specific parameters
            if model in ["photon", "photon_base"]:
                result_dict.update({
                    "strength": strength,
                    "aspect_ratio": aspect_ratio
                })
            elif model == "seededit":
                result_dict.update({
                    "guidance_scale": guidance_scale
                })
                if seed is not None:
                    result_dict["seed"] = seed
            else:  # kontext
                result_dict.update({
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale,
                    "resolution_mode": resolution_mode
                })
                if seed is not None:
                    result_dict["seed"] = seed
            
            return result_dict
            
        except Exception as e:
            print(f"❌ Error during image modification: {e}")
            model_display_name = {
                "photon": "Luma Photon Flash",
                "photon_base": "Luma Photon Base",
                "kontext": "FLUX Kontext Dev",
                "seededit": "ByteDance SeedEdit v3"
            }.get(model, model)
            
            error_dict = {
                "success": False,
                "error": str(e),
                "model": model_display_name,
                "prompt": prompt
            }
            
            # Add model-specific parameters to error response
            if model in ["photon", "photon_base"]:
                error_dict.update({
                    "strength": strength,
                    "aspect_ratio": aspect_ratio
                })
            elif model == "seededit":
                error_dict.update({
                    "guidance_scale": guidance_scale
                })
            else:  # kontext
                error_dict.update({
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale,
                    "resolution_mode": resolution_mode
                })
            
            return error_dict
    
    def modify_image_photon(
        self,
        prompt: str,
        image_url: str,
        strength: float = 0.8,
        aspect_ratio: AspectRatio = "1:1",
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convenience method for Luma Photon Flash modifications.
        
        Args:
            prompt: Text instruction for modifying the image
            image_url: URL of the input image
            strength: Modification intensity (0-1, default: 0.8)
            aspect_ratio: Output aspect ratio (default: "1:1")
            output_dir: Custom output directory (optional)
            
        Returns:
            Dictionary containing generation results and file paths
        """
        return self.modify_image(
            prompt=prompt,
            image_url=image_url,
            model="photon",
            strength=strength,
            aspect_ratio=aspect_ratio,
            output_dir=output_dir
        )
    
    def modify_image_photon_base(
        self,
        prompt: str,
        image_url: str,
        strength: float = 0.8,
        aspect_ratio: AspectRatio = "1:1",
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convenience method for Luma Photon Base modifications.
        
        Args:
            prompt: Text instruction for modifying the image
            image_url: URL of the input image
            strength: Modification intensity (0-1, default: 0.8)
            aspect_ratio: Output aspect ratio (default: "1:1")
            output_dir: Custom output directory (optional)
            
        Returns:
            Dictionary containing generation results and file paths
        """
        return self.modify_image(
            prompt=prompt,
            image_url=image_url,
            model="photon_base",
            strength=strength,
            aspect_ratio=aspect_ratio,
            output_dir=output_dir
        )
    
    def modify_local_image_photon_base(
        self,
        prompt: str,
        image_path: str,
        strength: float = 0.8,
        aspect_ratio: AspectRatio = "1:1",
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convenience method for Luma Photon Base local image modifications.
        
        Args:
            prompt: Text instruction for modifying the image
            image_path: Path to local image file
            strength: Modification intensity (0-1, default: 0.8)
            aspect_ratio: Output aspect ratio (default: "1:1")
            output_dir: Custom output directory (optional)
            
        Returns:
            Dictionary containing generation results and file paths
        """
        return self.modify_local_image(
            prompt=prompt,
            image_path=image_path,
            model="photon_base",
            strength=strength,
            aspect_ratio=aspect_ratio,
            output_dir=output_dir
        )
    
    def modify_image_kontext(
        self,
        prompt: str,
        image_url: str,
        num_inference_steps: int = 28,
        guidance_scale: float = 2.5,
        seed: Optional[int] = None,
        resolution_mode: str = "auto",
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convenience method for FLUX Kontext Dev modifications.
        
        Args:
            prompt: Text instruction for modifying the image
            image_url: URL of the input image
            num_inference_steps: Inference steps (1-50, default: 28)
            guidance_scale: Guidance scale (1.0-20.0, default: 2.5)
            seed: Random seed for reproducible results (optional)
            resolution_mode: Resolution mode ("auto" or "match_input")
            output_dir: Custom output directory (optional)
            
        Returns:
            Dictionary containing generation results and file paths
        """
        return self.modify_image(
            prompt=prompt,
            image_url=image_url,
            model="kontext",
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            seed=seed,
            resolution_mode=resolution_mode,
            output_dir=output_dir
        )
    
    def modify_image_seededit(
        self,
        prompt: str,
        image_url: str,
        guidance_scale: float = 0.5,
        seed: Optional[int] = None,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convenience method for ByteDance SeedEdit v3 modifications.
        
        Args:
            prompt: Text instruction for modifying the image
            image_url: URL of the input image
            guidance_scale: Guidance scale (0.0-1.0, default: 0.5)
            seed: Random seed for reproducible results (optional)
            output_dir: Custom output directory (optional)
            
        Returns:
            Dictionary containing generation results and file paths
        """
        return self.modify_image(
            prompt=prompt,
            image_url=image_url,
            model="seededit",
            guidance_scale=guidance_scale,
            seed=seed,
            output_dir=output_dir
        )
    
    def modify_multi_images_kontext(
        self,
        prompt: str,
        image_urls: List[str],
        guidance_scale: float = 3.5,
        num_images: int = 1,
        aspect_ratio: str = "1:1",
        seed: Optional[int] = None,
        safety_tolerance: int = 2,
        output_format: str = "jpeg",
        sync_mode: bool = True,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate new image from multiple input images using FLUX Kontext [max] Multi model.
        
        Args:
            prompt: Text description of desired transformation
            image_urls: List of image URLs to use as input
            guidance_scale: CFG guidance scale (1.0-20.0, default: 3.5)
            num_images: Number of images to generate (1-10, default: 1)
            aspect_ratio: Output aspect ratio (from KONTEXT_MULTI_ASPECT_RATIOS)
            seed: Random seed for reproducibility
            safety_tolerance: Safety tolerance level (1-6, default: 2)
            output_format: Output format ("jpeg" or "png")
            sync_mode: Wait for completion before returning
            output_dir: Output directory path
            
        Returns:
            Dictionary containing success status, processing info, and downloaded files
        """
        start_time = time.time()
        
        try:
            # Validate inputs
            if not image_urls or len(image_urls) == 0:
                raise ValueError("At least one image URL is required")
            
            if aspect_ratio not in KONTEXT_MULTI_ASPECT_RATIOS:
                raise ValueError(f"Unsupported aspect ratio: {aspect_ratio}. Supported: {KONTEXT_MULTI_ASPECT_RATIOS}")
            
            if not 1.0 <= guidance_scale <= 20.0:
                raise ValueError(f"Guidance scale must be between 1.0 and 20.0, got: {guidance_scale}")
            
            if not 1 <= num_images <= 10:
                raise ValueError(f"Number of images must be between 1 and 10, got: {num_images}")
            
            if not 1 <= safety_tolerance <= 6:
                raise ValueError(f"Safety tolerance must be between 1 and 6, got: {safety_tolerance}")
            
            if output_format not in ["jpeg", "png"]:
                raise ValueError(f"Output format must be 'jpeg' or 'png', got: {output_format}")
            
            # Prepare request parameters
            request_data = {
                "prompt": prompt,
                "image_urls": image_urls,
                "guidance_scale": guidance_scale,
                "num_images": num_images,
                "aspect_ratio": aspect_ratio,
                "safety_tolerance": str(safety_tolerance),
                "output_format": output_format,
                "sync_mode": sync_mode
            }
            
            if seed is not None:
                request_data["seed"] = seed
            
            print(f"🚀 Starting FLUX Kontext Multi generation with {len(image_urls)} input images...")
            print(f"   Prompt: {prompt}")
            print(f"   Guidance Scale: {guidance_scale}")
            print(f"   Aspect Ratio: {aspect_ratio}")
            print(f"   Number of Images: {num_images}")
            
            # Submit to FAL AI
            result = fal_client.subscribe(
                self.MODEL_ENDPOINTS["kontext_multi"],
                arguments=request_data
            )
            
            processing_time = time.time() - start_time
            print(f"✅ Generation completed in {processing_time:.2f} seconds")
            
            # Handle the result
            if not result or 'images' not in result:
                return {
                    "success": False,
                    "error": "No images returned from API",
                    "processing_time": processing_time,
                    "downloaded_files": []
                }
            
            # Download generated images
            output_path = Path(output_dir) if output_dir else self.output_dir
            output_path.mkdir(exist_ok=True)
            
            downloaded_files = []
            for i, image in enumerate(result['images']):
                if 'url' in image:
                    # Generate filename
                    timestamp = int(time.time())
                    filename = f"kontext_multi_{timestamp}_{i+1}.{output_format}"
                    file_path = output_path / filename
                    
                    # Download image
                    response = requests.get(image['url'])
                    response.raise_for_status()
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    downloaded_files.append(str(file_path))
                    print(f"📁 Downloaded: {file_path}")
            
            return {
                "success": True,
                "result": result,
                "processing_time": processing_time,
                "downloaded_files": downloaded_files,
                "model": "kontext_multi",
                "input_images": len(image_urls),
                "output_images": len(downloaded_files)
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"FLUX Kontext Multi generation failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "processing_time": processing_time,
                "downloaded_files": []
            }
    
    def modify_multi_local_images_kontext(
        self,
        prompt: str,
        image_paths: List[str],
        guidance_scale: float = 3.5,
        num_images: int = 1,
        aspect_ratio: str = "1:1",
        seed: Optional[int] = None,
        safety_tolerance: int = 2,
        output_format: str = "jpeg",
        sync_mode: bool = True,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate new image from multiple local images using FLUX Kontext [max] Multi model.
        
        Args:
            prompt: Text description of desired transformation
            image_paths: List of local image file paths
            guidance_scale: CFG guidance scale (1.0-20.0, default: 3.5)
            num_images: Number of images to generate (1-10, default: 1)
            aspect_ratio: Output aspect ratio (from KONTEXT_MULTI_ASPECT_RATIOS)
            seed: Random seed for reproducibility
            safety_tolerance: Safety tolerance level (1-6, default: 2)
            output_format: Output format ("jpeg" or "png")
            sync_mode: Wait for completion before returning
            output_dir: Output directory path
            
        Returns:
            Dictionary containing success status, processing info, and downloaded files
        """
        try:
            # Upload all local images first
            print(f"📤 Uploading {len(image_paths)} local images...")
            image_urls = []
            for i, image_path in enumerate(image_paths):
                if not Path(image_path).exists():
                    raise ValueError(f"Image file not found: {image_path}")
                
                print(f"   Uploading image {i+1}/{len(image_paths)}: {image_path}")
                image_url = self.upload_local_image(image_path)
                image_urls.append(image_url)
            
            print("✅ All images uploaded successfully")
            
            # Then generate using the uploaded URLs
            return self.modify_multi_images_kontext(
                prompt=prompt,
                image_urls=image_urls,
                guidance_scale=guidance_scale,
                num_images=num_images,
                aspect_ratio=aspect_ratio,
                seed=seed,
                safety_tolerance=safety_tolerance,
                output_format=output_format,
                sync_mode=sync_mode,
                output_dir=output_dir
            )
            
        except Exception as e:
            error_msg = f"Multi-image local upload failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "processing_time": 0,
                "downloaded_files": []
            }
    
    def modify_local_image_seededit(
        self,
        prompt: str,
        image_path: str,
        guidance_scale: float = 0.5,
        seed: Optional[int] = None,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Convenience method for ByteDance SeedEdit v3 local image modifications.
        
        Args:
            prompt: Text instruction for modifying the image
            image_path: Path to local image file
            guidance_scale: Guidance scale (0.0-1.0, default: 0.5)
            seed: Random seed for reproducible results (optional)
            output_dir: Custom output directory (optional)
            
        Returns:
            Dictionary containing generation results and file paths
        """
        return self.modify_local_image(
            prompt=prompt,
            image_path=image_path,
            model="seededit",
            guidance_scale=guidance_scale,
            seed=seed,
            output_dir=output_dir
        )
    
    def modify_local_image(
        self,
        prompt: str,
        image_path: str,
        model: ModelType = "photon",
        strength: Optional[float] = None,
        aspect_ratio: Optional[str] = None,
        num_inference_steps: int = 28,
        guidance_scale: float = 2.5,
        seed: Optional[int] = None,
        resolution_mode: str = "auto",
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Modify a local image file using text prompt with either model.
        
        Args:
            prompt: Text instruction for modifying the image
            image_path: Path to local image file
            model: Model to use ("photon" or "kontext", default: "photon")
            strength: Modification intensity for Photon (0-1)
            aspect_ratio: Output aspect ratio for Photon
            num_inference_steps: Inference steps for Kontext (1-50, default: 28)
            guidance_scale: Guidance scale for Kontext (1.0-20.0, default: 2.5)
            seed: Random seed for Kontext (optional)
            resolution_mode: Resolution mode for Kontext ("auto" or "match_input")
            output_dir: Custom output directory (optional)
            
        Returns:
            Dictionary containing generation results and file paths
        """
        try:
            # Upload local image
            print(f"📤 Uploading local image: {image_path}")
            image_url = self.upload_local_image(image_path)
            
            # Modify image using the main method
            return self.modify_image(
                prompt=prompt,
                image_url=image_url,
                model=model,
                strength=strength,
                aspect_ratio=aspect_ratio,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                seed=seed,
                resolution_mode=resolution_mode,
                output_dir=output_dir
            )
            
        except Exception as e:
            print(f"❌ Error processing local image: {e}")
            model_display_name = {
                "photon": "Luma Photon Flash",
                "photon_base": "Luma Photon Base",
                "kontext": "FLUX Kontext Dev",
                "seededit": "ByteDance SeedEdit v3"
            }.get(model, model)
            
            error_dict = {
                "success": False,
                "error": str(e),
                "model": model_display_name,
                "prompt": prompt,
                "image_path": image_path
            }
            
            # Add model-specific parameters to error response
            if model in ["photon", "photon_base"]:
                error_dict.update({
                    "strength": strength,
                    "aspect_ratio": aspect_ratio
                })
            elif model == "seededit":
                error_dict.update({
                    "guidance_scale": guidance_scale
                })
            else:  # kontext
                error_dict.update({
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale,
                    "resolution_mode": resolution_mode
                })
            
            return error_dict
    
    def batch_modify_images(
        self,
        prompts: List[str],
        image_urls: List[str],
        strength: float = 0.8,
        aspect_ratio: AspectRatio = "1:1",
        output_dir: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Modify multiple images with different prompts.
        
        Args:
            prompts: List of text instructions
            image_urls: List of image URLs
            strength: Modification intensity (0-1, default: 0.8)
            aspect_ratio: Output aspect ratio (default: "1:1")
            output_dir: Custom output directory (optional)
            
        Returns:
            List of generation results for each image
        """
        if len(prompts) != len(image_urls):
            raise ValueError("Number of prompts must match number of image URLs")
        
        results = []
        total_images = len(prompts)
        
        print(f"🎨 Starting batch modification of {total_images} images...")
        
        for i, (prompt, image_url) in enumerate(zip(prompts, image_urls), 1):
            print(f"\n📸 Processing image {i}/{total_images}")
            
            result = self.modify_image_photon(
                prompt=prompt,
                image_url=image_url,
                strength=strength,
                aspect_ratio=aspect_ratio,
                output_dir=output_dir
            )
            results.append(result)
            
            # Brief pause between requests
            if i < total_images:
                time.sleep(1)
        
        successful = sum(1 for r in results if r.get("success", False))
        print(f"\n✅ Batch processing completed: {successful}/{total_images} successful")
        
        return results
    
    def get_supported_models(self) -> List[str]:
        """
        Get list of supported models.
        
        Returns:
            List of supported model strings
        """
        return SUPPORTED_MODELS.copy()
    
    def get_supported_aspect_ratios(self, model: str = "photon") -> List[str]:
        """
        Get list of supported aspect ratios for a specific model.
        
        Args:
            model: Model type ("photon" or "kontext")
        
        Returns:
            List of supported aspect ratio/resolution mode strings
        """
        if model == "photon":
            return ASPECT_RATIOS.copy()
        elif model == "kontext":
            return ["auto", "match_input"]
        else:
            raise ValueError(f"Unsupported model: {model}. Supported models: {SUPPORTED_MODELS}")
    
    def get_model_endpoints(self) -> Dict[str, str]:
        """
        Get mapping of model names to their API endpoints.
        
        Returns:
            Dictionary mapping model names to endpoints
        """
        return self.MODEL_ENDPOINTS.copy()