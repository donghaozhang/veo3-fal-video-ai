"""
Constants and configuration for FAL Video to Video models
"""

from typing import Dict, List, Literal

# Model type definitions
ModelType = Literal["thinksound", "topaz"]

# Supported models
SUPPORTED_MODELS = ["thinksound", "topaz"]

# Model endpoints mapping
MODEL_ENDPOINTS = {
    "thinksound": "fal-ai/thinksound",
    "topaz": "fal-ai/topaz/upscale/video"
}

# Model display names
MODEL_DISPLAY_NAMES = {
    "thinksound": "ThinkSound",
    "topaz": "Topaz Video Upscale"
}

# Model information
MODEL_INFO = {
    "thinksound": {
        "model_name": "ThinkSound",
        "description": "AI-powered video audio generation that creates realistic sound effects for any video",
        "features": [
            "Automatic sound effect generation",
            "Text prompt guidance",
            "Video context understanding",
            "High-quality audio synthesis",
            "Commercial use license"
        ],
        "pricing": "$0.001 per second",
        "supported_formats": ["mp4", "mov", "avi", "webm"],
        "max_duration": 300,  # 5 minutes
        "output_format": "mp4"
    },
    "topaz": {
        "model_name": "Topaz Video Upscale",
        "description": "Professional-grade video upscaling using Proteus v4 with optional Apollo v8 frame interpolation",
        "features": [
            "Up to 4x video upscaling",
            "Frame rate enhancement up to 120 FPS",
            "Proteus v4 upscaling engine",
            "Apollo v8 frame interpolation",
            "Professional quality enhancement",
            "Commercial use license"
        ],
        "pricing": "Commercial use pricing",
        "supported_formats": ["mp4", "mov", "avi", "webm"],
        "max_upscale": 4,
        "max_fps": 120,
        "output_format": "mp4"
    }
}

# Default values
DEFAULT_VALUES = {
    "thinksound": {
        "seed": None,
        "prompt": None
    },
    "topaz": {
        "upscale_factor": 2,
        "target_fps": None
    }
}

# File size limits
MAX_VIDEO_SIZE_MB = 100
MAX_VIDEO_DURATION_SECONDS = 300

# Output settings
DEFAULT_OUTPUT_FORMAT = "mp4"
VIDEO_CODECS = {
    "mp4": "libx264",
    "webm": "libvpx",
    "mov": "libx264"
}