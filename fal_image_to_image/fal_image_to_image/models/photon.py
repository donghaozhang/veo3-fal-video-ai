"""
Luma Photon model implementations
"""

from typing import Dict, Any, Optional
from .base import BaseModel
from ..utils.validators import validate_strength, validate_aspect_ratio
from ..config.constants import MODEL_INFO, DEFAULT_VALUES, ASPECT_RATIOS


class PhotonModel(BaseModel):
    """Luma Photon Flash model for creative image modifications."""
    
    def __init__(self):
        super().__init__("photon")
    
    def validate_parameters(self, **kwargs) -> Dict[str, Any]:
        """Validate Photon Flash parameters."""
        defaults = DEFAULT_VALUES["photon"]
        
        strength = kwargs.get("strength", defaults["strength"])
        aspect_ratio = kwargs.get("aspect_ratio", defaults["aspect_ratio"])
        
        strength = validate_strength(strength)
        aspect_ratio = validate_aspect_ratio(aspect_ratio, "photon")
        
        return {
            "strength": strength,
            "aspect_ratio": aspect_ratio
        }
    
    def prepare_arguments(self, prompt: str, image_url: str, **kwargs) -> Dict[str, Any]:
        """Prepare API arguments for Photon Flash."""
        return {
            "prompt": prompt,
            "image_url": image_url,
            "strength": kwargs["strength"],
            "aspect_ratio": kwargs["aspect_ratio"]
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get Photon Flash model information."""
        return {
            **MODEL_INFO["photon"],
            "endpoint": self.endpoint
        }


class PhotonBaseModel(BaseModel):
    """Luma Photon Base model for high-quality creative modifications."""
    
    def __init__(self):
        super().__init__("photon_base")
    
    def validate_parameters(self, **kwargs) -> Dict[str, Any]:
        """Validate Photon Base parameters."""
        defaults = DEFAULT_VALUES["photon"]
        
        strength = kwargs.get("strength", defaults["strength"])
        aspect_ratio = kwargs.get("aspect_ratio", defaults["aspect_ratio"])
        
        strength = validate_strength(strength)
        aspect_ratio = validate_aspect_ratio(aspect_ratio, "photon_base")
        
        return {
            "strength": strength,
            "aspect_ratio": aspect_ratio
        }
    
    def prepare_arguments(self, prompt: str, image_url: str, **kwargs) -> Dict[str, Any]:
        """Prepare API arguments for Photon Base."""
        return {
            "prompt": prompt,
            "image_url": image_url,
            "strength": kwargs["strength"],
            "aspect_ratio": kwargs["aspect_ratio"]
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get Photon Base model information."""
        return {
            **MODEL_INFO["photon_base"],
            "endpoint": self.endpoint
        }