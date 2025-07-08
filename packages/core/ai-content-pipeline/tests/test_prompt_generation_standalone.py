#!/usr/bin/env python3
"""
Test script for standalone prompt generation functionality
Demonstrates how to use the prompt generation feature independently
"""

import sys
from pathlib import Path

# Add the ai_content_pipeline to the Python path
pipeline_path = Path(__file__).parent.parent
sys.path.insert(0, str(pipeline_path))

from ai_content_pipeline.models.prompt_generation import UnifiedPromptGenerator

def test_standalone_prompt_generation():
    """Test standalone prompt generation with different models."""
    
    print("🧪 Testing Standalone Prompt Generation")
    print("=" * 50)
    
    # Initialize the generator
    generator = UnifiedPromptGenerator()
    
    if not generator.analyzer:
        print("❌ OpenRouter analyzer not available - check OPENROUTER_API_KEY")
        return False
    
    # Test with a sample image URL (using a publicly available test image)
    test_image_url = "https://picsum.photos/1920/1080"
    
    # Test different prompt generation models
    models_to_test = [
        ("openrouter_video_prompt", "General video prompt generation"),
        ("openrouter_video_cinematic", "Cinematic style prompts"),
        ("openrouter_video_realistic", "Documentary-style prompts"),
        ("openrouter_video_artistic", "Creative artistic prompts"),
        ("openrouter_video_dramatic", "High-emotion dramatic prompts")
    ]
    
    results = []
    
    for model, description in models_to_test:
        print(f"\n🎬 Testing {model}")
        print(f"📝 Description: {description}")
        print("-" * 40)
        
        # Generate prompt with background context
        background_context = f"Transform this image into a compelling video using {description.lower()}"
        
        result = generator.generate(
            image_path=test_image_url,
            model=model,
            background_context=background_context
        )
        
        if result.success:
            print(f"✅ Success! Processing time: {result.processing_time:.2f}s")
            print(f"💰 Cost estimate: ${result.cost_estimate:.3f}")
            print(f"🎯 Extracted prompt: {result.extracted_prompt[:100]}...")
            results.append((model, True, result.processing_time, result.cost_estimate))
        else:
            print(f"❌ Failed: {result.error}")
            results.append((model, False, 0, 0))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    successful_tests = sum(1 for _, success, _, _ in results if success)
    total_cost = sum(cost for _, success, _, cost in results if success)
    total_time = sum(time for _, success, time, _ in results if success)
    
    print(f"✅ Successful tests: {successful_tests}/{len(results)}")
    print(f"⏱️  Total processing time: {total_time:.2f}s")
    print(f"💰 Total cost estimate: ${total_cost:.3f}")
    
    if successful_tests > 0:
        print(f"📈 Average time per generation: {total_time/successful_tests:.2f}s")
        print(f"📊 Average cost per generation: ${total_cost/successful_tests:.3f}")
    
    return successful_tests == len(results)

def test_with_local_image():
    """Test with a local image file (if available)."""
    
    print("\n🖼️  Testing with Local Image")
    print("=" * 50)
    
    # Look for sample images in common locations
    possible_image_paths = [
        "/home/zdhpe/veo3-video-generation/ai_content_pipeline/output",
        "/home/zdhpe/veo3-video-generation/fal_text_to_image/output",
        "/home/zdhpe/veo3-video-generation/veo3_video_generation/images"
    ]
    
    sample_image = None
    for path in possible_image_paths:
        image_dir = Path(path)
        if image_dir.exists():
            # Find first image file
            for ext in ['.jpg', '.jpeg', '.png', '.webp']:
                images = list(image_dir.glob(f"*{ext}"))
                if images:
                    sample_image = images[0]
                    break
            if sample_image:
                break
    
    if not sample_image:
        print("📁 No local images found for testing")
        return True
    
    print(f"🖼️  Using sample image: {sample_image}")
    
    generator = UnifiedPromptGenerator()
    
    result = generator.generate(
        image_path=str(sample_image),
        model="openrouter_video_cinematic",
        background_context="Create a beautiful cinematic sequence from this image"
    )
    
    if result.success:
        print(f"✅ Local image test successful!")
        print(f"⏱️  Processing time: {result.processing_time:.2f}s")
        print(f"🎯 Generated prompt: {result.extracted_prompt}")
        return True
    else:
        print(f"❌ Local image test failed: {result.error}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Prompt Generation Tests")
    print("=" * 60)
    
    # Test standalone functionality
    standalone_success = test_standalone_prompt_generation()
    
    # Test with local image
    local_success = test_with_local_image()
    
    print("\n" + "=" * 60)
    print("🏁 FINAL RESULTS")
    print("=" * 60)
    print(f"📡 Standalone tests: {'✅ PASSED' if standalone_success else '❌ FAILED'}")
    print(f"🖼️  Local image tests: {'✅ PASSED' if local_success else '❌ FAILED'}")
    
    overall_success = standalone_success and local_success
    print(f"\n🎯 Overall: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    sys.exit(0 if overall_success else 1)