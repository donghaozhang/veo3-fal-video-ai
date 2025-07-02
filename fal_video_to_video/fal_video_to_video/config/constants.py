"""
Constants and configuration for FAL Video to Video models
"""

from typing import Dict, List, Literal

# Model type definitions
ModelType = Literal["thinksound"]

# Supported models
SUPPORTED_MODELS = ["thinksound"]

# Model endpoints mapping
MODEL_ENDPOINTS = {
    "thinksound": "fal-ai/thinksound"
}

# Model display names
MODEL_DISPLAY_NAMES = {
    "thinksound": "ThinkSound"
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
    }
}

# Default values
DEFAULT_VALUES = {
    "thinksound": {
        "seed": None,
        "prompt": None
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