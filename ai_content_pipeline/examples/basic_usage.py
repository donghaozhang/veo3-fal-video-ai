#!/usr/bin/env python3
"""
Basic usage examples for AI Content Pipeline

Demonstrates how to use the pipeline for common content creation tasks.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to Python path to allow imports
sys.path.append(str(Path(__file__).parent.parent))

from ai_content_pipeline import AIPipelineManager


def example_text_to_image():
    """Example: Generate image from text prompt."""
    print("🎨 Example 1: Text-to-Image Generation")
    print("=" * 40)
    
    # Initialize pipeline manager
    manager = AIPipelineManager()
    
    # Generate image
    result = manager.text_to_image.generate(
        prompt="A serene mountain lake at sunset with vibrant colors reflecting in the water",
        model="auto",  # Let the system choose the best model
        aspect_ratio="16:9"
    )
    
    if result.success:
        print(f"✅ Image generated successfully!")
        print(f"📦 Model used: {result.model_used}")
        print(f"📁 Output path: {result.output_path}")
        print(f"💰 Cost: ${result.cost_estimate:.3f}")
        print(f"⏱️  Time: {result.processing_time:.1f}s")
    else:
        print(f"❌ Generation failed: {result.error}")
    
    return result


def example_quick_video_creation():
    """Example: Quick video creation from text."""
    print("\n🎬 Example 2: Quick Video Creation (Text → Image → Video)")
    print("=" * 60)
    
    # Initialize pipeline manager
    manager = AIPipelineManager()
    
    # Create video from text
    result = manager.quick_create_video(
        text="Epic space battle with starships and laser beams in deep space",
        image_model="flux_dev",
        video_model="veo3"  # Note: This will fail until video models are integrated
    )
    
    print(f"📋 Chain: {result.steps_completed}/{result.total_steps} steps completed")
    print(f"💰 Total cost: ${result.total_cost:.3f}")
    print(f"⏱️  Total time: {result.total_time:.1f}s")
    
    if result.success:
        print(f"✅ Video creation successful!")
        for step_name, output in result.outputs.items():
            print(f"   {step_name}: {output.get('path', 'No output path')}")
    else:
        print(f"❌ Video creation failed: {result.error}")
    
    return result


def example_model_comparison():
    """Example: Compare different text-to-image models."""
    print("\n🔍 Example 3: Model Comparison")
    print("=" * 35)
    
    # Initialize pipeline manager
    manager = AIPipelineManager()
    
    # Get available models
    available_models = manager.text_to_image.get_available_models()
    print(f"📦 Available models: {', '.join(available_models)}")
    
    # Compare models for a specific prompt
    prompt = "A futuristic city skyline with flying cars"
    comparison = manager.text_to_image.compare_models(prompt, available_models[:3])
    
    print(f"\n💡 Model comparison for: '{prompt}'")
    for model, info in comparison.items():
        print(f"\n   {model}:")
        print(f"     • Name: {info.get('name', 'N/A')}")
        print(f"     • Provider: {info.get('provider', 'N/A')}")
        print(f"     • Best for: {info.get('best_for', 'N/A')}")
        print(f"     • Cost: {info.get('cost_per_image', 'N/A')}")
        print(f"     • Available: {'Yes' if info.get('available') else 'No'}")


def example_cost_estimation():
    """Example: Estimate costs for different chains."""
    print("\n💰 Example 4: Cost Estimation")
    print("=" * 30)
    
    # Initialize pipeline manager
    manager = AIPipelineManager()
    
    # Create different chain configurations
    chains = [
        # Simple image generation
        manager.create_simple_chain(
            steps=["text_to_image"],
            models={"text_to_image": "flux_schnell"},
            name="quick_image"
        ),
        # High-quality image generation  
        manager.create_simple_chain(
            steps=["text_to_image"],
            models={"text_to_image": "flux_dev"},
            name="quality_image"
        ),
        # Full content creation (will show errors for unimplemented steps)
        manager.create_simple_chain(
            steps=["text_to_image", "image_to_video", "add_audio"],
            name="full_content"
        )
    ]
    
    print("📊 Cost estimates for different workflows:")
    for chain in chains:
        cost_info = manager.estimate_chain_cost(chain)
        print(f"\n   {chain.name}:")
        print(f"     • Total cost: ${cost_info['total_cost']:.3f}")
        print(f"     • Steps: {len(chain.steps)}")
        for step_cost in cost_info['step_costs']:
            print(f"       - {step_cost['step']} ({step_cost['model']}): ${step_cost['cost']:.3f}")


def example_storage_usage():
    """Example: Check storage usage."""
    print("\n💾 Example 5: Storage Usage")
    print("=" * 25)
    
    # Initialize pipeline manager
    manager = AIPipelineManager()
    
    # Get storage usage
    usage = manager.file_manager.get_storage_usage()
    
    print("📁 Storage usage:")
    for dir_name, dir_info in usage.items():
        if dir_name != "total_mb":
            print(f"   {dir_name}: {dir_info['size_mb']:.1f} MB ({dir_info['path']})")
    print(f"   Total: {usage['total_mb']:.1f} MB")


def main():
    """Run all examples."""
    print("🚀 AI Content Pipeline - Basic Usage Examples")
    print("=" * 50)
    print("This script demonstrates basic usage of the AI Content Pipeline.")
    print("Note: Some examples may fail if models are not yet integrated.\n")
    
    try:
        # Run examples
        example_text_to_image()
        example_model_comparison()
        example_cost_estimation()
        example_storage_usage()
        
        # Video creation example (may fail)
        print("\n" + "⚠️ " * 20)
        print("WARNING: The following example may fail because")
        print("video generation models are not yet integrated.")
        print("⚠️ " * 20)
        
        example_quick_video_creation()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Examples interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ Examples completed!")
    print("\nNext steps:")
    print("• Try: python -m ai_content_pipeline list-models")
    print("• Try: python -m ai_content_pipeline generate-image --text 'your prompt here'")
    print("• Try: python -m ai_content_pipeline create-examples")


if __name__ == "__main__":
    main()