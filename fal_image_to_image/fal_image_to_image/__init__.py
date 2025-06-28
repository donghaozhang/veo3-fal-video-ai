"""
FAL AI Image-to-Image Generator Package

A comprehensive Python interface for modifying images using multiple FAL AI models.

Main Features:
- Multi-model support (Photon, Kontext, SeedEdit v3)
- Unified API interface
- Parameter validation
- Batch processing
- Local and remote image support

Quick Start:
    from fal_image_to_image import FALImageToImageGenerator
    
    generator = FALImageToImageGenerator()
    
    result = generator.modify_image_seededit(
        prompt="Make it more photorealistic",
        image_url="https://example.com/image.jpg"
    )
"""

from .generator import FALImageToImageGenerator
from .config.constants import ModelType, AspectRatio, SUPPORTED_MODELS

__version__ = "2.0.0"
__author__ = "AI Assistant"

# Main exports
__all__ = [
    "FALImageToImageGenerator",
    "ModelType",
    "AspectRatio", 
    "SUPPORTED_MODELS"
]