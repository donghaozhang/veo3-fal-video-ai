#!/usr/bin/env python3
"""Test the reframe endpoint for aspect ratio changes"""

import os
from dotenv import load_dotenv
import fal_client

# Load environment variables
load_dotenv()
fal_client.api_key = os.getenv("FAL_KEY")

# Test the reframe endpoint
print("Testing reframe endpoint with 16:9 aspect ratio")
result = fal_client.subscribe(
    "fal-ai/luma-photon/reframe",
    arguments={
        "image_url": "https://v3.fal.media/files/elephant/d6-CDsEvQTKDj4NIxoLgK_anime_girl.jpeg",
        "aspect_ratio": "16:9"
    }
)
print(f"Result: {result}")

# Download and check
if result.get('images'):
    import requests
    url = result['images'][0]['url']
    response = requests.get(url)
    with open('reframe_16_9_output.jpg', 'wb') as f:
        f.write(response.content)
    print("Image saved as reframe_16_9_output.jpg")