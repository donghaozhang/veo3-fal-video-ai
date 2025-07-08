#!/usr/bin/env python3
"""
Direct OCR analysis test script
"""
import sys
import os

# Add the ai_content_pipeline module to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ai_content_pipeline'))

from ai_content_pipeline.models.image_understanding import UnifiedImageUnderstandingGenerator

def test_direct_ocr():
    """Test direct OCR analysis on existing image"""
    
    # Initialize the image understanding model
    print("🔧 Initializing OCR analyzer...")
    analyzer = UnifiedImageUnderstandingGenerator()
    
    # Path to the test image
    image_path = "input/test_ocr_image.webp"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file not found: {image_path}")
        return
    
    print(f"📁 Analyzing image: {image_path}")
    
    try:
        # Perform OCR analysis
        print("🔍 Starting OCR analysis...")
        result = analyzer.analyze(
            image_path=image_path,
            model="gemini_ocr",
            analysis_prompt="Extract all readable text from this image"
        )
        
        print("✅ OCR Analysis Complete!")
        print(f"💰 Cost: ${result.cost_estimate:.3f}")
        print(f"⏱️  Processing time: {result.processing_time:.1f}s")
        print("\n📝 Extracted Text:")
        print("=" * 50)
        
        # Print the extracted text
        if result.success and result.output_text:
            print(result.output_text)
        else:
            print(f"❌ Analysis failed: {result.error}")
            print("Full result:", result)
            
    except Exception as e:
        print(f"❌ Error during OCR analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_ocr()