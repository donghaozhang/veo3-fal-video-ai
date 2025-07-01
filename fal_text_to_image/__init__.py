"""
FAL AI Text-to-Image Generation Package

A Python interface for generating images using multiple FAL AI text-to-image models.

Models supported:
- Imagen 4 Preview Fast - Cost-effective Google model
- Seedream v3 - Bilingual (Chinese/English) model  
- FLUX.1 Schnell - Fastest FLUX model
- FLUX.1 Dev - High-quality 12B parameter model

Quick Start:
    from fal_text_to_image_generator import FALTextToImageGenerator
    
    generator = FALTextToImageGenerator()
    
    result = generator.generate_flux_schnell(
        prompt="A dragon flying through clouds"
    )
"""

from .fal_text_to_image_generator import FALTextToImageGenerator

__version__ = "1.0.0"
__author__ = "AI Assistant"

# Main exports
__all__ = [
    "FALTextToImageGenerator"
]