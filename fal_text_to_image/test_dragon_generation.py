#!/usr/bin/env python3
"""
Dragon Image Generation Test
Uses FAL AI text-to-image generator to create a dragon image
"""

import asyncio
from fal_text_to_image_generator import FALTextToImageGenerator

async def generate_dragon_image():
    """Generate a dragon image using FAL AI"""
    
    print("🐲 Dragon Image Generation Test")
    print("=" * 50)
    print("⚠️ Cost Warning: This will cost approximately $0.015")
    print("🎨 Using FLUX Schnell for fast generation")
    print("🔥 Generating majestic dragon...")
    print()
    
    # Initialize generator
    generator = FALTextToImageGenerator()
    
    # Dragon prompt
    dragon_prompt = (
        "A majestic dragon with red scales, breathing fire, "
        "fantasy art style, detailed and epic, cinematic lighting, "
        "digital art, 4k resolution"
    )
    
    try:
        # Generate the dragon image
        result = generator.generate_image(
            prompt=dragon_prompt,
            model='flux_schnell',
            output_folder='output'
        )
        
        if result.get('success'):
            print("✅ Dragon image generated successfully!")
            print(f"🔗 Image URL: {result['image']['url']}")
            print(f"📁 Local path: {result['local_path']}")
            print(f"⏱️ Generation time: {result.get('generation_time', 'unknown')} seconds")
            print(f"💰 Estimated cost: ${result.get('cost_estimate', 0.015):.3f}")
            print()
            print("🎉 Your dragon awaits! Check the output folder.")
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during generation: {str(e)}")
        return False
    
    return result.get('success', False)

if __name__ == "__main__":
    asyncio.run(generate_dragon_image()) 