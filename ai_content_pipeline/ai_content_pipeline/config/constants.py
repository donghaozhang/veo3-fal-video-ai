"""
Configuration constants for AI Content Pipeline
"""

# Supported models for each pipeline step
SUPPORTED_MODELS = {
    "text_to_image": [
        "flux_dev",           # FLUX.1 Dev (high quality)
        "flux_schnell",       # FLUX.1 Schnell (fast)
        "imagen4",            # Google Imagen 4
        "seedream_v3",        # Seedream v3 (bilingual)
        "dalle3",             # OpenAI DALL-E 3 (planned)
        "stable_diffusion",   # Stability AI (planned)
    ],
    "image_to_video": [
        "veo3",               # Google Veo 3.0
        "veo2",               # Google Veo 2.0  
        "hailuo",             # MiniMax Hailuo-02
        "kling",              # Kling Video 2.1
    ],
    "add_audio": [
        "thinksound",         # ThinksSound AI audio generation
    ],
    "upscale_video": [
        "topaz",              # Topaz Video Upscale
    ]
}

# Pipeline step types
PIPELINE_STEPS = [
    "text_to_image",
    "image_to_video", 
    "add_audio",
    "upscale_video"
]

# Model recommendations based on use case
MODEL_RECOMMENDATIONS = {
    "text_to_image": {
        "quality": "flux_dev",
        "speed": "flux_schnell", 
        "cost_effective": "seedream_v3",
        "photorealistic": "imagen4"
    },
    "image_to_video": {
        "quality": "veo3",
        "speed": "hailuo",
        "cost_effective": "hailuo",
        "cinematic": "veo3"
    }
}

# Cost estimates (USD)
COST_ESTIMATES = {
    "text_to_image": {
        "flux_dev": 0.003,
        "flux_schnell": 0.001,
        "imagen4": 0.004,
        "seedream_v3": 0.002,
    },
    "image_to_video": {
        "veo3": 3.00,
        "veo2": 2.50,
        "hailuo": 0.08,
        "kling": 0.10,
    },
    "add_audio": {
        "thinksound": 0.05,
    },
    "upscale_video": {
        "topaz": 1.50,
    }
}

# Processing time estimates (seconds)
PROCESSING_TIME_ESTIMATES = {
    "text_to_image": {
        "flux_dev": 15,
        "flux_schnell": 5,
        "imagen4": 20,
        "seedream_v3": 10,
    },
    "image_to_video": {
        "veo3": 300,
        "veo2": 240,
        "hailuo": 60,
        "kling": 90,
    },
    "add_audio": {
        "thinksound": 45,
    },
    "upscale_video": {
        "topaz": 120,
    }
}

# File format mappings
SUPPORTED_FORMATS = {
    "image": [".jpg", ".jpeg", ".png", ".webp"],
    "video": [".mp4", ".mov", ".avi", ".webm"]
}

# Default configuration
DEFAULT_CHAIN_CONFIG = {
    "steps": [
        {
            "type": "text_to_image",
            "model": "flux_dev",
            "params": {
                "aspect_ratio": "16:9",
                "style": "cinematic"
            }
        },
        {
            "type": "image_to_video", 
            "model": "veo3",
            "params": {
                "duration": 8,
                "motion_level": "medium"
            }
        }
    ],
    "output_dir": "output",
    "temp_dir": "temp",
    "cleanup_temp": True
}