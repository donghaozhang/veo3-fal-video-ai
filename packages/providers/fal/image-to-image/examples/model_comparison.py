#!/usr/bin/env python3
"""
Model comparison examples

This script demonstrates the differences between various models.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fal_image_to_image import FALImageToImageGenerator

def compare_models_for_same_prompt():
    """Compare different models with the same prompt"""
    print("🔄 Model Comparison: Same Prompt, Different Models")
    print("=" * 60)
    
    if not os.getenv('FAL_KEY'):
        print("⚠️  FAL_KEY not set - showing comparison patterns only\n")
    
    # Sample prompt for comparison
    prompt = "Make this image more professional and photorealistic"
    image_url = "https://example.com/test-image.jpg"  # Replace with actual URL
    
    try:
        generator = FALImageToImageGenerator()
        
        # Compare different models
        models_to_test = [
            {
                "name": "SeedEdit v3",
                "model": "seededit",
                "params": {"guidance_scale": 0.5, "seed": 42},
                "best_for": "Content preservation and accuracy"
            },
            {
                "name": "Photon Flash", 
                "model": "photon",
                "params": {"strength": 0.7, "aspect_ratio": "1:1"},
                "best_for": "Creative modifications"
            },
            {
                "name": "Kontext Dev",
                "model": "kontext", 
                "params": {"num_inference_steps": 28, "guidance_scale": 2.5},
                "best_for": "Contextual understanding"
            }
        ]
        
        print(f"Prompt: '{prompt}'\n")
        
        for model_config in models_to_test:
            print(f"🎯 {model_config['name']} ({model_config['model']})")
            print(f"   Best for: {model_config['best_for']}")
            print(f"   Parameters: {model_config['params']}")
            
            # Show what the API call would be
            print(f"   Code:")
            print(f"   result = generator.modify_image(")
            print(f"       prompt=\"{prompt}\",")
            print(f"       image_url=\"{image_url}\",")
            print(f"       model=\"{model_config['model']}\",")
            for key, value in model_config['params'].items():
                print(f"       {key}={repr(value)},")
            print(f"   )")
            
            if os.getenv('FAL_KEY'):
                print("   🔄 Would execute API call...")
                # Uncomment to make real API calls:
                # result = generator.modify_image(
                #     prompt=prompt,
                #     image_url=image_url,
                #     model=model_config['model'],
                #     **model_config['params']
                # )
                # if result['success']:
                #     print(f"   ✅ Generated: {Path(result['downloaded_files'][0]).name}")
            else:
                print("   📋 Set FAL_KEY to execute")
            
            print()

def guidance_scale_comparison():
    """Compare different guidance scales for SeedEdit v3"""
    print("🎛️ SeedEdit v3: Guidance Scale Comparison")
    print("=" * 60)
    
    prompt = "Add dramatic lighting and enhance image quality"
    
    guidance_scales = [
        (0.2, "Minimal changes - Maximum content preservation"),
        (0.5, "Balanced - Good compromise between change and preservation"),
        (0.8, "Strong changes - More dramatic modifications")
    ]
    
    print(f"Prompt: '{prompt}'\n")
    
    for scale, description in guidance_scales:
        print(f"📊 Guidance Scale: {scale}")
        print(f"   Effect: {description}")
        print(f"   Use case: {get_guidance_scale_use_case(scale)}")
        print(f"   Code: generator.modify_image_seededit(..., guidance_scale={scale})")
        print()

def get_guidance_scale_use_case(scale):
    """Get use case recommendation for guidance scale"""
    if scale <= 0.3:
        return "Quality enhancement, noise reduction"
    elif scale <= 0.6:
        return "Style changes, lighting adjustments"
    else:
        return "Creative transformations, major modifications"

def model_selection_guide():
    """Guide for selecting the right model"""
    print("🎯 Model Selection Guide")
    print("=" * 60)
    
    scenarios = [
        {
            "scenario": "Photo Enhancement",
            "description": "Improve photo quality while keeping it realistic",
            "recommended": "SeedEdit v3",
            "params": "guidance_scale=0.3-0.5",
            "reason": "Excellent content preservation with quality improvements"
        },
        {
            "scenario": "Creative Transformation", 
            "description": "Transform image into artistic or stylized version",
            "recommended": "Photon Flash",
            "params": "strength=0.6-0.8",
            "reason": "Creative and personalizable modifications"
        },
        {
            "scenario": "Contextual Editing",
            "description": "Make changes that understand image context",
            "recommended": "Kontext Dev",
            "params": "guidance_scale=2.5, steps=28",
            "reason": "Frontier contextual understanding capabilities"
        },
        {
            "scenario": "Content Preservation Priority",
            "description": "Make changes but keep original structure intact",
            "recommended": "SeedEdit v3",
            "params": "guidance_scale=0.2-0.4", 
            "reason": "Best-in-class content preservation"
        }
    ]
    
    for scenario in scenarios:
        print(f"📝 Scenario: {scenario['scenario']}")
        print(f"   Description: {scenario['description']}")
        print(f"   ✅ Recommended: {scenario['recommended']}")
        print(f"   ⚙️  Parameters: {scenario['params']}")
        print(f"   💡 Reason: {scenario['reason']}")
        print()

def main():
    """Run model comparison examples"""
    print("FAL Image-to-Image Model Comparison Guide")
    print("=" * 70)
    
    compare_models_for_same_prompt()
    guidance_scale_comparison()
    model_selection_guide()
    
    print("=" * 70)
    print("🎉 Model comparison guide completed!")
    print("💡 Use this guide to choose the best model for your use case")

if __name__ == "__main__":
    main()