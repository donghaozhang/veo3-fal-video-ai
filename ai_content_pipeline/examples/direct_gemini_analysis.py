#!/usr/bin/env python3
"""
Direct Gemini Image Analysis Example

This script demonstrates how to use the Gemini video analyzer directly 
for image analysis without any pipeline overhead or validation.

This bypasses the AI Content Pipeline entirely and uses the underlying
video_tools Gemini analyzer directly.
"""

import sys
import os
from pathlib import Path

# Add the video_tools directory to Python path
video_tools_path = Path(__file__).parent.parent.parent / "video_tools"
if video_tools_path.exists():
    sys.path.insert(0, str(video_tools_path))
    from video_utils.gemini_analyzer import GeminiVideoAnalyzer
else:
    print("❌ Video tools directory not found")
    sys.exit(1)


def test_direct_gemini_analysis():
    """Test direct usage of GeminiVideoAnalyzer for image analysis."""
    print("🧪 Direct Gemini Image Analysis Test")
    print("=" * 45)
    
    # Check if Gemini API key is available
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY environment variable not set")
        print("💡 Set up your API key: export GEMINI_API_KEY='your_api_key_here'")
        return False
    
    try:
        # Initialize Gemini analyzer directly
        print("🚀 Initializing Gemini Video Analyzer...")
        analyzer = GeminiVideoAnalyzer()
        print("✅ Gemini analyzer initialized successfully")
        
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
        
        # Test different analysis methods directly
        print("\n" + "="*50)
        print("🔍 RUNNING DIRECT ANALYSIS METHODS")
        print("="*50)
        
        # 1. Basic image description
        print("\n📝 1. Basic Image Description:")
        try:
            result = analyzer.describe_image(temp_image_path, detailed=False)
            print(f"   ✅ Success!")
            print(f"   📋 Result type: {type(result)}")
            if isinstance(result, dict):
                description = result.get('description', 'No description found')
                print(f"   📄 Description: {description[:200]}...")
            else:
                print(f"   📄 Raw result: {str(result)[:200]}...")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 2. Detailed image analysis
        print("\n🔍 2. Detailed Image Analysis:")
        try:
            result = analyzer.describe_image(temp_image_path, detailed=True)
            print(f"   ✅ Success!")
            print(f"   📋 Result type: {type(result)}")
            if isinstance(result, dict):
                description = result.get('description', 'No description found')
                print(f"   📄 Description: {description[:200]}...")
            else:
                print(f"   📄 Raw result: {str(result)[:200]}...")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 3. Object detection
        print("\n🎯 3. Object Detection:")
        try:
            result = analyzer.detect_objects(temp_image_path, detailed=True)
            print(f"   ✅ Success!")
            print(f"   📋 Result type: {type(result)}")
            if isinstance(result, dict):
                objects = result.get('objects', 'No objects found')
                print(f"   🎯 Objects: {str(objects)[:200]}...")
            else:
                print(f"   🎯 Raw result: {str(result)[:200]}...")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 4. Image classification
        print("\n🏷️ 4. Image Classification:")
        try:
            result = analyzer.classify_image(temp_image_path)
            print(f"   ✅ Success!")
            print(f"   📋 Result type: {type(result)}")
            if isinstance(result, dict):
                classification = result.get('classification', 'No classification found')
                print(f"   🏷️ Classification: {str(classification)[:200]}...")
            else:
                print(f"   🏷️ Raw result: {str(result)[:200]}...")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 5. Composition analysis
        print("\n🎨 5. Composition Analysis:")
        try:
            result = analyzer.analyze_image_composition(temp_image_path)
            print(f"   ✅ Success!")
            print(f"   📋 Result type: {type(result)}")
            if isinstance(result, dict):
                composition = result.get('composition', 'No composition analysis found')
                print(f"   🎨 Composition: {str(composition)[:200]}...")
            else:
                print(f"   🎨 Raw result: {str(result)[:200]}...")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 6. Question and Answer
        print("\n❓ 6. Question & Answer:")
        try:
            questions = [
                "What is the main subject of this image?",
                "What colors are prominent in this image?",
                "What mood does this image convey?"
            ]
            result = analyzer.answer_image_questions(temp_image_path, questions)
            print(f"   ✅ Success!")
            print(f"   📋 Result type: {type(result)}")
            if isinstance(result, dict):
                answers = result.get('answers', 'No answers found')
                print(f"   ❓ Answers: {str(answers)[:200]}...")
            else:
                print(f"   ❓ Raw result: {str(result)[:200]}...")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # 7. OCR (Text Extraction)
        print("\n📝 7. OCR Text Extraction:")
        try:
            result = analyzer.extract_text_from_image(temp_image_path)
            print(f"   ✅ Success!")
            print(f"   📋 Result type: {type(result)}")
            if isinstance(result, dict):
                text = result.get('text', 'No text found')
                print(f"   📝 Extracted text: {str(text)[:200]}...")
            else:
                print(f"   📝 Raw result: {str(result)[:200]}...")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # Clean up temporary file
        try:
            os.unlink(temp_image_path)
            print(f"\n🗑️ Cleaned up temporary file: {temp_image_path}")
        except:
            pass
        
        print("\n✅ Direct Gemini analysis test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize or test Gemini analyzer: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_local_image():
    """Test with a local image if available."""
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
        analyzer = GeminiVideoAnalyzer()
        
        # Test basic description
        print("\n📝 Analyzing local image...")
        result = analyzer.describe_image(sample_image, detailed=True)
        
        print(f"✅ Local image analysis successful!")
        print(f"📋 Result type: {type(result)}")
        
        if isinstance(result, dict):
            description = result.get('description', 'No description found')
            print(f"📄 Description: {description[:300]}...")
        else:
            print(f"📄 Raw result: {str(result)[:300]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Local image analysis failed: {e}")
        return False


def main():
    """Run the direct Gemini analysis tests."""
    print("🚀 Direct Gemini Image Analysis Examples")
    print("=" * 50)
    print("This bypasses the AI Content Pipeline and uses")
    print("the underlying Gemini analyzer directly.\n")
    
    # Check environment
    print("🔧 Environment Check:")
    gemini_key = os.getenv('GEMINI_API_KEY')
    print(f"   GEMINI_API_KEY: {'✅ Set' if gemini_key else '❌ Not set'}")
    
    if not gemini_key:
        print("\n💡 To enable direct Gemini analysis:")
        print("   export GEMINI_API_KEY='your_gemini_api_key_here'")
        print("   Get your key from: https://aistudio.google.com/app/apikey")
        return
    
    print("\n" + "="*50)
    
    try:
        # Test direct analysis
        success1 = test_direct_gemini_analysis()
        
        # Test with local image
        success2 = test_with_local_image()
        
        # Summary
        print("\n" + "="*50)
        print("📊 FINAL SUMMARY")
        print("="*50)
        
        results = [
            ("Direct Gemini Analysis", success1),
            ("Local Image Test", success2)
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
            print("• Gemini analyzer can be used directly without any pipeline overhead")
            print("• Multiple analysis methods are available: describe, classify, detect, etc.")
            print("• Results are returned as dictionaries with structured data")
            print("• Both URL and local file paths are supported")
            print("• Direct usage bypasses all cost estimation and validation layers")
        
        print("\n📚 Related Examples:")
        print("• ai_content_pipeline/examples/standalone_image_analysis.py")
        print("• ai_content_pipeline/examples/test_prompt_generation_standalone.py")
        print("• video_tools/tests/test_image_workflow.py")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()