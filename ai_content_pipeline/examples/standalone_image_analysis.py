#!/usr/bin/env python3
"""
Standalone Image Analysis Examples

This script demonstrates how to use the AI Content Pipeline's image analysis 
capabilities directly without going through the full pipeline chain validation.

Examples include:
1. Direct image understanding/analysis using Gemini
2. Standalone prompt generation for video content
3. Individual model usage without pipeline overhead
"""

import sys
import os
from pathlib import Path

# Add the ai_content_pipeline to the Python path
pipeline_path = Path(__file__).parent.parent
sys.path.insert(0, str(pipeline_path))

# Import the standalone models
from ai_content_pipeline.models.image_understanding import UnifiedImageUnderstandingGenerator
from ai_content_pipeline.models.prompt_generation import UnifiedPromptGenerator


def example_standalone_image_analysis():
    """Example: Direct image analysis without pipeline validation."""
    print("🔍 Example 1: Standalone Image Analysis")
    print("=" * 50)
    
    # Initialize the image understanding generator directly
    analyzer = UnifiedImageUnderstandingGenerator()
    
    # Check if analyzer is available
    if not analyzer.analyzer:
        print("❌ Gemini analyzer not available. Please check GEMINI_API_KEY environment variable.")
        print("💡 Set up Gemini API key: export GEMINI_API_KEY='your_api_key_here'")
        return False
    
    # Test image URL (using a publicly available test image)
    test_image_url = "https://picsum.photos/1920/1080"
    
    print(f"📸 Analyzing image: {test_image_url}")
    print("\n🎯 Available analysis models:")
    available_models = analyzer.get_available_models()
    for i, model in enumerate(available_models, 1):
        info = analyzer.get_model_info(model)
        print(f"   {i}. {model} - {info['best_for'] if info else 'No description'}")
    
    # Run different types of analysis
    analysis_results = []
    
    # 1. Basic description
    print("\n📝 1. Basic Image Description:")
    result = analyzer.analyze(test_image_url, model="gemini_describe")
    if result.success:
        print(f"   ✅ Success: {result.output_text}")
        print(f"   ⏱️ Time: {result.processing_time:.2f}s | 💰 Cost: ${result.cost_estimate:.3f}")
        analysis_results.append(("Basic Description", True))
    else:
        print(f"   ❌ Failed: {result.error}")
        analysis_results.append(("Basic Description", False))
    
    # 2. Detailed analysis
    print("\n🔍 2. Detailed Image Analysis:")
    result = analyzer.analyze(test_image_url, model="gemini_detailed")
    if result.success:
        output_preview = str(result.output_text)[:100] + "..." if len(str(result.output_text)) > 100 else str(result.output_text)
        print(f"   ✅ Success: {output_preview}")
        print(f"   ⏱️ Time: {result.processing_time:.2f}s | 💰 Cost: ${result.cost_estimate:.3f}")
        analysis_results.append(("Detailed Analysis", True))
    else:
        print(f"   ❌ Failed: {result.error}")
        analysis_results.append(("Detailed Analysis", False))
    
    # 3. Object detection
    print("\n🎯 3. Object Detection:")
    result = analyzer.analyze(test_image_url, model="gemini_objects")
    if result.success:
        print(f"   ✅ Success: {result.output_text}")
        print(f"   ⏱️ Time: {result.processing_time:.2f}s | 💰 Cost: ${result.cost_estimate:.3f}")
        analysis_results.append(("Object Detection", True))
    else:
        print(f"   ❌ Failed: {result.error}")
        analysis_results.append(("Object Detection", False))
    
    # 4. Composition analysis
    print("\n🎨 4. Composition Analysis:")
    result = analyzer.analyze(test_image_url, model="gemini_composition")
    if result.success:
        print(f"   ✅ Success: {result.output_text}")
        print(f"   ⏱️ Time: {result.processing_time:.2f}s | 💰 Cost: ${result.cost_estimate:.3f}")
        analysis_results.append(("Composition Analysis", True))
    else:
        print(f"   ❌ Failed: {result.error}")
        analysis_results.append(("Composition Analysis", False))
    
    # Summary
    successful = sum(1 for _, success in analysis_results if success)
    print(f"\n📊 Analysis Summary: {successful}/{len(analysis_results)} successful")
    
    return successful > 0


def example_standalone_prompt_generation():
    """Example: Direct prompt generation without pipeline validation."""
    print("\n🎬 Example 2: Standalone Video Prompt Generation")
    print("=" * 55)
    
    # Initialize the prompt generator directly
    generator = UnifiedPromptGenerator()
    
    # Check if generator is available
    if not generator.analyzer:
        print("❌ OpenRouter analyzer not available. Please check OPENROUTER_API_KEY environment variable.")
        print("💡 Set up OpenRouter API key: export OPENROUTER_API_KEY='your_api_key_here'")
        return False
    
    # Test image URL
    test_image_url = "https://picsum.photos/1920/1080"
    
    print(f"📸 Generating video prompts for: {test_image_url}")
    print("\n🎯 Available prompt models:")
    available_models = generator.get_available_models()
    for i, model in enumerate(available_models, 1):
        info = generator.get_model_info(model)
        print(f"   {i}. {model} - {info['best_for'] if info else 'No description'}")
    
    # Generate different types of video prompts
    prompt_results = []
    
    # 1. General video prompt
    print("\n🎬 1. General Video Prompt:")
    result = generator.generate(
        test_image_url, 
        model="openrouter_video_prompt",
        background_context="Transform this image into a compelling video sequence"
    )
    if result.success:
        print(f"   ✅ Success!")
        print(f"   🎯 Extracted Prompt: {result.extracted_prompt}")
        print(f"   ⏱️ Time: {result.processing_time:.2f}s | 💰 Cost: ${result.cost_estimate:.3f}")
        prompt_results.append(("General Video", True))
    else:
        print(f"   ❌ Failed: {result.error}")
        prompt_results.append(("General Video", False))
    
    # 2. Cinematic style
    print("\n🎭 2. Cinematic Style Prompt:")
    result = generator.generate(
        test_image_url, 
        model="openrouter_video_cinematic",
        background_context="Create a dramatic, movie-style video sequence"
    )
    if result.success:
        print(f"   ✅ Success!")
        print(f"   🎯 Extracted Prompt: {result.extracted_prompt}")
        print(f"   ⏱️ Time: {result.processing_time:.2f}s | 💰 Cost: ${result.cost_estimate:.3f}")
        prompt_results.append(("Cinematic Style", True))
    else:
        print(f"   ❌ Failed: {result.error}")
        prompt_results.append(("Cinematic Style", False))
    
    # 3. Artistic style
    print("\n🎨 3. Artistic Style Prompt:")
    result = generator.generate(
        test_image_url, 
        model="openrouter_video_artistic",
        background_context="Create an abstract, artistic video with creative visual effects"
    )
    if result.success:
        print(f"   ✅ Success!")
        print(f"   🎯 Extracted Prompt: {result.extracted_prompt}")
        print(f"   ⏱️ Time: {result.processing_time:.2f}s | 💰 Cost: ${result.cost_estimate:.3f}")
        prompt_results.append(("Artistic Style", True))
    else:
        print(f"   ❌ Failed: {result.error}")
        prompt_results.append(("Artistic Style", False))
    
    # Summary
    successful = sum(1 for _, success in prompt_results if success)
    print(f"\n📊 Prompt Generation Summary: {successful}/{len(prompt_results)} successful")
    
    return successful > 0


def example_local_image_analysis():
    """Example: Analyze local images if available."""
    print("\n🖼️ Example 3: Local Image Analysis")
    print("=" * 40)
    
    # Look for sample images in the project
    possible_image_paths = [
        "/home/zdhpe/veo3-video-generation/ai_content_pipeline/output",
        "/home/zdhpe/veo3-video-generation/fal_text_to_image/output",
        "/home/zdhpe/veo3-video-generation/veo3_video_generation/images",
        "/home/zdhpe/veo3-video-generation/ai_content_pipeline/input"
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
        print("💡 Try generating an image first with:")
        print("   cd /home/zdhpe/veo3-video-generation && python ai_content_pipeline/examples/basic_usage.py")
        return True
    
    print(f"🖼️ Found local image: {sample_image}")
    
    # Initialize analyzers
    analyzer = UnifiedImageUnderstandingGenerator()
    generator = UnifiedPromptGenerator()
    
    results = []
    
    # Image analysis
    if analyzer.analyzer:
        print("\n🔍 Analyzing local image...")
        result = analyzer.analyze(str(sample_image), model="gemini_detailed")
        if result.success:
            output_preview = str(result.output_text)[:150] + "..." if len(str(result.output_text)) > 150 else str(result.output_text)
            print(f"   ✅ Analysis: {output_preview}")
            results.append(("Local Image Analysis", True))
        else:
            print(f"   ❌ Analysis failed: {result.error}")
            results.append(("Local Image Analysis", False))
    
    # Prompt generation
    if generator.analyzer:
        print("\n🎬 Generating video prompt from local image...")
        result = generator.generate(
            str(sample_image), 
            model="openrouter_video_cinematic",
            background_context="Transform this local image into a cinematic video sequence"
        )
        if result.success:
            print(f"   ✅ Prompt: {result.extracted_prompt}")
            results.append(("Local Prompt Generation", True))
        else:
            print(f"   ❌ Prompt generation failed: {result.error}")
            results.append(("Local Prompt Generation", False))
    
    successful = sum(1 for _, success in results if success)
    print(f"\n📊 Local Image Summary: {successful}/{len(results)} successful")
    
    return len(results) == 0 or successful > 0


def example_custom_qa_analysis():
    """Example: Custom question-answer analysis."""
    print("\n❓ Example 4: Custom Q&A Image Analysis")
    print("=" * 45)
    
    analyzer = UnifiedImageUnderstandingGenerator()
    
    if not analyzer.analyzer:
        print("❌ Gemini analyzer not available for Q&A analysis")
        return False
    
    # Test image
    test_image_url = "https://picsum.photos/1920/1080"
    
    # Custom questions to ask about the image
    custom_questions = [
        "What is the dominant color in this image?",
        "What mood or emotion does this image convey?",
        "What time of day does this appear to be?",
        "What would be a good title for this image?"
    ]
    
    print(f"📸 Asking custom questions about: {test_image_url}")
    
    for i, question in enumerate(custom_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        
        result = analyzer.analyze(
            test_image_url, 
            model="gemini_qa",
            analysis_prompt=question
        )
        
        if result.success:
            print(f"   ✅ Answer: {result.output_text}")
        else:
            print(f"   ❌ Failed: {result.error}")
    
    return True


def main():
    """Run all standalone examples."""
    print("🚀 AI Content Pipeline - Standalone Image Analysis Examples")
    print("=" * 65)
    print("This script demonstrates direct usage of image analysis models")
    print("without going through the full pipeline chain validation.\n")
    
    # Check environment setup
    print("🔧 Environment Check:")
    gemini_key = os.getenv('GEMINI_API_KEY')
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    
    print(f"   GEMINI_API_KEY: {'✅ Set' if gemini_key else '❌ Not set'}")
    print(f"   OPENROUTER_API_KEY: {'✅ Set' if openrouter_key else '❌ Not set'}")
    
    if not gemini_key:
        print("\n💡 To enable Gemini image analysis:")
        print("   export GEMINI_API_KEY='your_gemini_api_key_here'")
    
    if not openrouter_key:
        print("\n💡 To enable OpenRouter prompt generation:")
        print("   export OPENROUTER_API_KEY='your_openrouter_api_key_here'")
    
    print("\n" + "="*65)
    
    # Run examples
    results = []
    
    try:
        # Example 1: Standalone image analysis
        result1 = example_standalone_image_analysis()
        results.append(("Image Analysis", result1))
        
        # Example 2: Standalone prompt generation
        result2 = example_standalone_prompt_generation()
        results.append(("Prompt Generation", result2))
        
        # Example 3: Local image analysis
        result3 = example_local_image_analysis()
        results.append(("Local Images", result3))
        
        # Example 4: Custom Q&A
        result4 = example_custom_qa_analysis()
        results.append(("Custom Q&A", result4))
        
    except KeyboardInterrupt:
        print("\n\n🛑 Examples interrupted by user.")
        return
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Final summary
    print("\n" + "="*65)
    print("📊 FINAL SUMMARY")
    print("="*65)
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"✅ Successful examples: {successful}/{total}")
    
    for example_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   • {example_name}: {status}")
    
    print(f"\n🎯 Overall Result: {'✅ SUCCESS' if successful > 0 else '❌ ALL FAILED'}")
    
    if successful > 0:
        print("\n💡 Key Takeaways:")
        print("• Image analysis models can be used directly without pipeline validation")
        print("• Both Gemini (image analysis) and OpenRouter (prompt generation) are available")
        print("• Models support both URLs and local file paths")
        print("• Cost estimates and processing times are provided for each operation")
        print("• Different analysis types are available for different use cases")
    
    print("\n📚 Next Steps:")
    print("• Try: python ai_content_pipeline/examples/basic_usage.py")
    print("• Try: python ai_content_pipeline/examples/test_prompt_generation_standalone.py")
    print("• Try: python -m ai_content_pipeline generate-image --text 'your prompt here'")


if __name__ == "__main__":
    main()