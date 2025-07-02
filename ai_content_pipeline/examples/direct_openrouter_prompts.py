#!/usr/bin/env python3
"""
Direct OpenRouter Prompt Generation Example

This script demonstrates how to use the OpenRouter analyzer directly 
for video prompt generation without any pipeline overhead or validation.

This bypasses the AI Content Pipeline entirely and uses the underlying
video_tools OpenRouter analyzer directly.
"""

import sys
import os
from pathlib import Path

# Add the video_tools directory to Python path
video_tools_path = Path(__file__).parent.parent.parent / "video_tools"
if video_tools_path.exists():
    sys.path.insert(0, str(video_tools_path))
    from video_utils.openrouter_analyzer import OpenRouterAnalyzer
else:
    print("❌ Video tools directory not found")
    sys.exit(1)


def test_direct_openrouter_prompts():
    """Test direct usage of OpenRouterAnalyzer for video prompt generation."""
    print("🧪 Direct OpenRouter Prompt Generation Test")
    print("=" * 50)
    
    # Check if OpenRouter API key is available
    if not os.getenv('OPENROUTER_API_KEY'):
        print("❌ OPENROUTER_API_KEY environment variable not set")
        print("💡 Set up your API key: export OPENROUTER_API_KEY='your_api_key_here'")
        print("💡 Get your key from: https://openrouter.ai/")
        return False
    
    try:
        # Initialize OpenRouter analyzer directly
        print("🚀 Initializing OpenRouter Analyzer...")
        # Using Gemini 2.0 Flash for fast and high-quality prompt generation
        analyzer = OpenRouterAnalyzer(model="google/gemini-2.0-flash-001")
        print("✅ OpenRouter analyzer initialized successfully")
        
        # Test with a sample image URL
        test_image_url = "https://picsum.photos/1920/1080"
        print(f"\n📸 Testing with image: {test_image_url}")
        
        # Download the image to a temporary location for testing
        import requests
        import tempfile
        
        print("📥 Downloading test image...")
        response = requests.get(test_image_url, timeout=30)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file.write(response.content)
            temp_image_path = Path(temp_file.name)
        
        print(f"✅ Image downloaded to: {temp_image_path}")
        
        # Test different prompt generation methods directly
        print("\n" + "="*60)
        print("🎬 RUNNING DIRECT PROMPT GENERATION METHODS")
        print("="*60)
        
        # 1. General video prompt generation
        print("\n🎬 1. General Video Prompt Generation:")
        try:
            result = analyzer.generate_video_prompt(
                temp_image_path,
                background_context="Transform this image into a compelling video sequence",
                video_style="cinematic",
                duration_preference="medium"
            )
            print(f"   ✅ Success!")
            print(f"   📋 Result type: {type(result)}")
            print(f"   📄 Generated Analysis: {str(result)[:300]}...")
            
            # Extract optimized prompt
            optimized_prompt = analyzer.extract_optimized_prompt(result)
            print(f"   🎯 Optimized Prompt: {optimized_prompt}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 2. Cinematic style video prompt
        print("\n🎭 2. Cinematic Style Video Prompt:")
        try:
            result = analyzer.generate_video_prompt(
                temp_image_path,
                background_context="Create a dramatic, movie-style video sequence with professional cinematography",
                video_style="cinematic",
                duration_preference="long"
            )
            print(f"   ✅ Success!")
            print(f"   📄 Generated Analysis: {str(result)[:300]}...")
            
            # Extract optimized prompt
            optimized_prompt = analyzer.extract_optimized_prompt(result)
            print(f"   🎯 Optimized Prompt: {optimized_prompt}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 3. Realistic documentary style
        print("\n📹 3. Realistic Documentary Style:")
        try:
            result = analyzer.generate_video_prompt(
                temp_image_path,
                background_context="Create a natural, documentary-style video with realistic movements",
                video_style="realistic",
                duration_preference="medium"
            )
            print(f"   ✅ Success!")
            print(f"   📄 Generated Analysis: {str(result)[:300]}...")
            
            # Extract optimized prompt
            optimized_prompt = analyzer.extract_optimized_prompt(result)
            print(f"   🎯 Optimized Prompt: {optimized_prompt}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 4. Artistic creative style
        print("\n🎨 4. Artistic Creative Style:")
        try:
            result = analyzer.generate_video_prompt(
                temp_image_path,
                background_context="Create an abstract, artistic video with creative visual effects and transformations",
                video_style="artistic",
                duration_preference="long"
            )
            print(f"   ✅ Success!")
            print(f"   📄 Generated Analysis: {str(result)[:300]}...")
            
            # Extract optimized prompt
            optimized_prompt = analyzer.extract_optimized_prompt(result)
            print(f"   🎯 Optimized Prompt: {optimized_prompt}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 5. Dramatic high-emotion style
        print("\n⚡ 5. Dramatic High-Emotion Style:")
        try:
            result = analyzer.generate_video_prompt(
                temp_image_path,
                background_context="Create an intense, dramatic video with powerful emotional impact",
                video_style="dramatic",
                duration_preference="medium"
            )
            print(f"   ✅ Success!")
            print(f"   📄 Generated Analysis: {str(result)[:300]}...")
            
            # Extract optimized prompt
            optimized_prompt = analyzer.extract_optimized_prompt(result)
            print(f"   🎯 Optimized Prompt: {optimized_prompt}")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # Clean up temporary file
        try:
            os.unlink(temp_image_path)
            print(f"\n🗑️ Cleaned up temporary file: {temp_image_path}")
        except:
            pass
        
        print("\n✅ Direct OpenRouter prompt generation test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize or test OpenRouter analyzer: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_local_image():
    """Test prompt generation with a local image if available."""
    print("\n🖼️ Testing with Local Image")
    print("=" * 35)
    
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
        return True
    
    print(f"🖼️ Found local image: {sample_image}")
    
    try:
        # Initialize analyzer
        analyzer = OpenRouterAnalyzer(model="google/gemini-2.0-flash-001")
        
        # Test prompt generation
        print("\n🎬 Generating video prompt from local image...")
        result = analyzer.generate_video_prompt(
            sample_image,
            background_context="Transform this local image into a compelling cinematic video",
            video_style="cinematic",
            duration_preference="medium"
        )
        
        print(f"✅ Local image prompt generation successful!")
        print(f"📄 Generated Analysis: {str(result)[:400]}...")
        
        # Extract optimized prompt
        optimized_prompt = analyzer.extract_optimized_prompt(result)
        print(f"🎯 Optimized Prompt: {optimized_prompt}")
        
        return True
        
    except Exception as e:
        print(f"❌ Local image prompt generation failed: {e}")
        return False


def test_different_models():
    """Test prompt generation with different OpenRouter models."""
    print("\n🤖 Testing Different OpenRouter Models")
    print("=" * 45)
    
    # List of models to test
    models_to_test = [
        ("google/gemini-2.0-flash-001", "Google Gemini 2.0 Flash - Fast and efficient"),
        ("anthropic/claude-3-sonnet", "Anthropic Claude 3 Sonnet - High quality"),
        ("openai/gpt-4o", "OpenAI GPT-4o - Multimodal capabilities")
    ]
    
    test_image_url = "https://picsum.photos/1920/1080"
    
    # Download test image once
    import requests
    import tempfile
    
    try:
        print("📥 Downloading test image...")
        response = requests.get(test_image_url, timeout=30)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file.write(response.content)
            temp_image_path = Path(temp_file.name)
        
        print(f"✅ Image downloaded to: {temp_image_path}")
        
        for model_name, description in models_to_test:
            print(f"\n🤖 Testing {model_name}")
            print(f"📝 Description: {description}")
            print("-" * 40)
            
            try:
                # Initialize analyzer with specific model
                analyzer = OpenRouterAnalyzer(model=model_name)
                
                # Generate prompt
                result = analyzer.generate_video_prompt(
                    temp_image_path,
                    background_context=f"Create a video using {model_name} analysis",
                    video_style="cinematic",
                    duration_preference="medium"
                )
                
                print(f"   ✅ Success with {model_name}!")
                
                # Extract optimized prompt
                optimized_prompt = analyzer.extract_optimized_prompt(result)
                print(f"   🎯 Prompt: {optimized_prompt[:200]}...")
                
            except Exception as e:
                print(f"   ❌ Failed with {model_name}: {e}")
        
        # Clean up
        try:
            os.unlink(temp_image_path)
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Model testing failed: {e}")
        return False


def main():
    """Run the direct OpenRouter prompt generation tests."""
    print("🚀 Direct OpenRouter Prompt Generation Examples")
    print("=" * 55)
    print("This bypasses the AI Content Pipeline and uses")
    print("the underlying OpenRouter analyzer directly.\n")
    
    # Check environment
    print("🔧 Environment Check:")
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    print(f"   OPENROUTER_API_KEY: {'✅ Set' if openrouter_key else '❌ Not set'}")
    
    if not openrouter_key:
        print("\n💡 To enable direct OpenRouter analysis:")
        print("   export OPENROUTER_API_KEY='your_openrouter_api_key_here'")
        print("   Get your key from: https://openrouter.ai/")
        return
    
    print("\n" + "="*55)
    
    try:
        # Test direct prompt generation
        success1 = test_direct_openrouter_prompts()
        
        # Test with local image
        success2 = test_with_local_image()
        
        # Test different models (may fail due to availability/cost)
        print("\n⚠️ " * 15)
        print("WARNING: The following test may fail due to")
        print("model availability or API rate limits.")
        print("⚠️ " * 15)
        success3 = test_different_models()
        
        # Summary
        print("\n" + "="*55)
        print("📊 FINAL SUMMARY")
        print("="*55)
        
        results = [
            ("Direct Prompt Generation", success1),
            ("Local Image Test", success2),
            ("Multiple Models Test", success3)
        ]
        
        successful = sum(1 for _, success in results if success)
        total = len(results)
        
        print(f"✅ Successful tests: {successful}/{total}")
        
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"   • {test_name}: {status}")
        
        print(f"\n🎯 Overall Result: {'✅ SUCCESS' if successful > 0 else '❌ ALL FAILED'}")
        
        if successful > 0:
            print("\n💡 Key Insights:")
            print("• OpenRouter analyzer can be used directly without pipeline overhead")
            print("• Multiple video styles supported: cinematic, realistic, artistic, dramatic")
            print("• Different models can be specified for different capabilities")
            print("• Background context helps generate more targeted prompts")
            print("• Extract_optimized_prompt() provides clean, usable video prompts")
        
        print("\n📚 Related Examples:")
        print("• ai_content_pipeline/examples/standalone_image_analysis.py")
        print("• ai_content_pipeline/examples/direct_gemini_analysis.py")
        print("• ai_content_pipeline/examples/test_prompt_generation_standalone.py")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()