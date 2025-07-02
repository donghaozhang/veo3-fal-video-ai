#!/usr/bin/env python3
"""Debug script to test reframing parameters"""

import os
from dotenv import load_dotenv
import fal_client

# Load environment variables
load_dotenv()
fal_client.api_key = os.getenv("FAL_KEY")

# Test 1: Only aspect ratio
print("Test 1: Only aspect ratio 16:9")
result1 = fal_client.subscribe(
    "fal-ai/luma-photon/modify",
    arguments={
        "prompt": "enhance colors",
        "image_url": "https://v3.fal.media/files/elephant/d6-CDsEvQTKDj4NIxoLgK_anime_girl.jpeg",
        "strength": 0.7,
        "aspect_ratio": "16:9"
    }
)
print(f"Result 1: {result1}")

# Test 2: With reframing coordinates
print("\nTest 2: Aspect ratio 16:9 with reframing coordinates")
result2 = fal_client.subscribe(
    "fal-ai/luma-photon/modify",
    arguments={
        "prompt": "enhance colors",
        "image_url": "https://v3.fal.media/files/elephant/d6-CDsEvQTKDj4NIxoLgK_anime_girl.jpeg",
        "strength": 0.7,
        "aspect_ratio": "16:9",
        "x_start": 0,
        "y_start": 235,
        "x_end": 1076,
        "y_end": 840
    }
)
print(f"Result 2: {result2}")

# Test 3: Try 1:1 aspect ratio with reframing
print("\nTest 3: Aspect ratio 1:1 with reframing coordinates")
result3 = fal_client.subscribe(
    "fal-ai/luma-photon/modify",
    arguments={
        "prompt": "enhance colors",
        "image_url": "https://v3.fal.media/files/elephant/d6-CDsEvQTKDj4NIxoLgK_anime_girl.jpeg",
        "strength": 0.7,
        "aspect_ratio": "1:1",
        "x_start": 200,
        "y_start": 200,
        "x_end": 876,
        "y_end": 876
    }
)
print(f"Result 3: {result3}")