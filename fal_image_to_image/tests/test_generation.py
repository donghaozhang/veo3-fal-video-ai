#!/usr/bin/env python3
"""
FAL AI Image-to-Image Generation Test

This script tests the actual image modification functionality.
⚠️ WARNING: This script WILL INCUR COSTS when run!

Test costs approximately $0.01-0.05 per image modification.

Usage:
    python test_generation.py              # Basic test (1 image)
    python test_generation.py --quick      # Quick test with minimal parameters
    python test_generation.py --batch      # Test batch processing
    python test_generation.py --all        # Test all aspect ratios
    python test_generation.py --help       # Show help

Author: AI Assistant
Date: 2024
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

def print_cost_warning():
    """Print cost warning and get user confirmation."""
    print("⚠️" * 20)
    print("💰 COST WARNING: This script will incur charges!")
    print("💰 Estimated cost: $0.01-0.05 per image modification")
    print("💰 Make sure you have credits in your FAL AI account")
    print("⚠️" * 20)
    
    response = input("\n❓ Do you want to continue and incur charges? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Test cancelled by user")
        sys.exit(0)
    
    print("✅ Proceeding with paid tests...")

def test_basic_modification() -> Dict[str, Any]:
    """Test basic image modification."""
    print("\n🎨 Testing Basic Image Modification...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Test with a simple modification
        prompt = "Convert this image to a watercolor painting style"
        # Using a public test image URL
        image_url = "https://picsum.photos/512/512"
        
        result = generator.modify_image_photon(
            prompt=prompt,
            image_url=image_url,
            strength=0.7,
            aspect_ratio="1:1",
            output_dir="output"
        )
        
        print(f"✅ Basic Photon modification test: {'PASSED' if result['success'] else 'FAILED'}")
        if result['success']:
            print(f"   Model: {result['model']}")
            print(f"   Processing time: {result['processing_time']:.2f}s")
            print(f"   Output files: {len(result['downloaded_files'])}")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Basic modification test failed: {e}")
        return {"success": False, "error": str(e)}

def test_kontext_modification() -> Dict[str, Any]:
    """Test FLUX Kontext image modification."""
    print("\n🎨 Testing FLUX Kontext Modification...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Test with contextual editing prompt
        prompt = "Change the setting to nighttime, add street lights"
        # Using a public test image URL
        image_url = "https://picsum.photos/512/512"
        
        result = generator.modify_image_kontext(
            prompt=prompt,
            image_url=image_url,
            num_inference_steps=25,
            guidance_scale=3.0,
            resolution_mode="auto",
            output_dir="output"
        )
        
        print(f"✅ Kontext modification test: {'PASSED' if result['success'] else 'FAILED'}")
        if result['success']:
            print(f"   Model: {result['model']}")
            print(f"   Processing time: {result['processing_time']:.2f}s")
            print(f"   Output files: {len(result['downloaded_files'])}")
            print(f"   Inference steps: {result['num_inference_steps']}")
            print(f"   Guidance scale: {result['guidance_scale']}")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Kontext modification test failed: {e}")
        return {"success": False, "error": str(e)}

def test_strength_variations() -> List[Dict[str, Any]]:
    """Test different strength values."""
    print("\n🎯 Testing Strength Variations...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Test different strength values
        strengths = [0.3, 0.5, 0.8]
        prompt = "Make this image look like a vintage photograph"
        image_url = "https://picsum.photos/512/512"
        
        results = []
        
        for strength in strengths:
            print(f"   Testing strength: {strength}")
            
            result = generator.modify_image(
                prompt=prompt,
                image_url=image_url,
                strength=strength,
                aspect_ratio="1:1",
                output_dir="output"
            )
            
            results.append(result)
            
            if result['success']:
                print(f"   ✅ Strength {strength}: Success ({result['processing_time']:.2f}s)")
            else:
                print(f"   ❌ Strength {strength}: Failed - {result.get('error', 'Unknown')}")
            
            # Brief pause between requests
            time.sleep(2)
        
        successful = sum(1 for r in results if r['success'])
        print(f"✅ Strength variations test: {successful}/{len(strengths)} successful")
        
        return results
        
    except Exception as e:
        print(f"❌ Strength variations test failed: {e}")
        return [{"success": False, "error": str(e)}]

def test_aspect_ratios() -> List[Dict[str, Any]]:
    """Test different aspect ratios."""
    print("\n📐 Testing Aspect Ratios...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator, ASPECT_RATIOS
        
        generator = FALImageToImageGenerator()
        
        # Test a few key aspect ratios
        test_ratios = ["1:1", "16:9", "4:3"]
        prompt = "Transform this into a digital art piece"
        image_url = "https://picsum.photos/512/512"
        
        results = []
        
        for ratio in test_ratios:
            print(f"   Testing aspect ratio: {ratio}")
            
            result = generator.modify_image(
                prompt=prompt,
                image_url=image_url,
                strength=0.6,
                aspect_ratio=ratio,
                output_dir="output"
            )
            
            results.append(result)
            
            if result['success']:
                print(f"   ✅ Aspect ratio {ratio}: Success ({result['processing_time']:.2f}s)")
            else:
                print(f"   ❌ Aspect ratio {ratio}: Failed - {result.get('error', 'Unknown')}")
            
            # Brief pause between requests
            time.sleep(2)
        
        successful = sum(1 for r in results if r['success'])
        print(f"✅ Aspect ratios test: {successful}/{len(test_ratios)} successful")
        
        return results
        
    except Exception as e:
        print(f"❌ Aspect ratios test failed: {e}")
        return [{"success": False, "error": str(e)}]

def test_batch_processing() -> Dict[str, Any]:
    """Test batch image processing."""
    print("\n📦 Testing Batch Processing...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Test batch processing with multiple prompts
        prompts = [
            "Convert to oil painting style",
            "Make it look like a pencil sketch",
            "Transform into cyberpunk style"
        ]
        
        # Use different test images
        image_urls = [
            "https://picsum.photos/512/512?random=1",
            "https://picsum.photos/512/512?random=2", 
            "https://picsum.photos/512/512?random=3"
        ]
        
        results = generator.batch_modify_images(
            prompts=prompts,
            image_urls=image_urls,
            strength=0.7,
            aspect_ratio="1:1",
            output_dir="output"
        )
        
        successful = sum(1 for r in results if r['success'])
        print(f"✅ Batch processing test: {successful}/{len(prompts)} successful")
        
        return {
            "success": successful == len(prompts),
            "total": len(prompts),
            "successful": successful,
            "results": results
        }
        
    except Exception as e:
        print(f"❌ Batch processing test failed: {e}")
        return {"success": False, "error": str(e)}

def test_quick_generation() -> Dict[str, Any]:
    """Quick test with minimal cost."""
    print("\n⚡ Running Quick Test...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Single quick test
        result = generator.modify_image(
            prompt="Add a slight artistic filter",
            image_url="https://picsum.photos/512/512",
            strength=0.4,  # Lower strength for subtle changes
            aspect_ratio="1:1",
            output_dir="output"
        )
        
        if result['success']:
            print(f"✅ Quick test passed in {result['processing_time']:.2f}s")
        else:
            print(f"❌ Quick test failed: {result.get('error', 'Unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return {"success": False, "error": str(e)}

def print_summary(results: Dict[str, Any]):
    """Print test summary."""
    print("\n" + "=" * 60)
    print("📊 IMAGE-TO-IMAGE GENERATION TEST SUMMARY")
    print("=" * 60)
    
    total_tests = 0
    passed_tests = 0
    
    for test_name, result in results.items():
        if isinstance(result, dict):
            success = result.get('success', False)
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {test_name}")
            
            total_tests += 1
            if success:
                passed_tests += 1
                
        elif isinstance(result, list):
            successful = sum(1 for r in result if r.get('success', False))
            total = len(result)
            status = "✅ PASS" if successful == total else f"⚠️  PARTIAL ({successful}/{total})"
            print(f"{status} {test_name}")
            
            total_tests += 1
            if successful == total:
                passed_tests += 1
    
    print("-" * 60)
    print(f"🎯 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Image-to-image generation is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

def test_model_comparison() -> Dict[str, Any]:
    """Test both models with the same prompt for comparison."""
    print("\n🆚 Testing Model Comparison...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Use the same prompt and image for both models
        prompt = "Transform this into an artistic painting"
        image_url = "https://picsum.photos/512/512"
        
        print("   Testing Photon Flash...")
        photon_result = generator.modify_image_photon(
            prompt=prompt,
            image_url=image_url,
            strength=0.7,
            aspect_ratio="1:1",
            output_dir="output"
        )
        
        # Brief pause between models
        time.sleep(3)
        
        print("   Testing FLUX Kontext...")
        kontext_result = generator.modify_image_kontext(
            prompt=prompt,
            image_url=image_url,
            num_inference_steps=28,
            guidance_scale=2.5,
            resolution_mode="auto",
            output_dir="output"
        )
        
        # Compare results
        photon_success = photon_result.get('success', False)
        kontext_success = kontext_result.get('success', False)
        
        print(f"\n📊 Model Comparison Results:")
        print(f"   Photon Flash: {'PASSED' if photon_success else 'FAILED'}")
        if photon_success:
            print(f"      Time: {photon_result['processing_time']:.2f}s")
        
        print(f"   FLUX Kontext: {'PASSED' if kontext_success else 'FAILED'}")
        if kontext_success:
            print(f"      Time: {kontext_result['processing_time']:.2f}s")
        
            return {
        "success": photon_success and kontext_success,
        "photon_result": photon_result,
        "kontext_result": kontext_result,
        "comparison": {
            "photon_time": photon_result.get('processing_time', 0),
            "kontext_time": kontext_result.get('processing_time', 0)
        }
    }

def test_photon_base() -> Dict[str, Any]:
    """Test Luma Photon Base model."""
    print("\n🎨 Testing Luma Photon Base...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        result = generator.modify_image_photon_base(
            prompt="Transform this into a watercolor painting",
            image_url="https://picsum.photos/512/512?random=photon_base",
            strength=0.8,
            aspect_ratio="1:1",
            output_dir="output"
        )
        
        if result.get('success'):
            print(f"✅ Photon Base test passed!")
            print(f"   Processing time: {result['processing_time']:.2f}s")
            for file_path in result['downloaded_files']:
                print(f"   📁 {file_path}")
        else:
            print(f"❌ Photon Base test failed: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Photon Base test failed: {e}")
        return {"success": False, "error": str(e)}

def test_kontext_multi() -> Dict[str, Any]:
    """Test FLUX Kontext Multi model with multiple input images."""
    print("\n🔢 Testing FLUX Kontext Multi...")
    
    try:
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Use multiple test images
        image_urls = [
            "https://picsum.photos/512/512?random=1",
            "https://picsum.photos/512/512?random=2"
        ]
        
        result = generator.modify_multi_images_kontext(
            prompt="Put the little duckling on top of the woman's t-shirt.",
            image_urls=image_urls,
            guidance_scale=3.5,
            num_images=1,
            aspect_ratio="1:1",
            output_dir="output"
        )
        
        if result.get('success'):
            print(f"✅ Kontext Multi test passed!")
            print(f"   Processing time: {result['processing_time']:.2f}s")
            print(f"   Input images: {result['input_images']}")
            print(f"   Output images: {result['output_images']}")
            for file_path in result['downloaded_files']:
                print(f"   📁 {file_path}")
        else:
            print(f"❌ Kontext Multi test failed: {result.get('error', 'Unknown error')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Kontext Multi test failed: {e}")
        return {"success": False, "error": str(e)}
        
    except Exception as e:
        print(f"❌ Model comparison test failed: {e}")
        return {"success": False, "error": str(e)}

def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description="FAL AI Image-to-Image Generation Tests")
    parser.add_argument('--quick', action='store_true', help='Run quick test only')
    parser.add_argument('--batch', action='store_true', help='Test batch processing')
    parser.add_argument('--all', action='store_true', help='Test all aspect ratios')
    parser.add_argument('--kontext', action='store_true', help='Test FLUX Kontext only')
    parser.add_argument('--kontext-multi', action='store_true', help='Test FLUX Kontext Multi only')
    parser.add_argument('--photon-base', action='store_true', help='Test Luma Photon Base only')
    parser.add_argument('--compare', action='store_true', help='Compare both models')
    parser.add_argument('--no-confirm', action='store_true', help='Skip cost warning')
    
    args = parser.parse_args()
    
    # Cost warning
    if not args.no_confirm:
        print_cost_warning()
    
    # Setup output directory
    os.makedirs("output", exist_ok=True)
    
    print("\n🚀 Starting FAL AI Image-to-Image Generation Tests...")
    print(f"📁 Output directory: {Path('output').absolute()}")
    
    results = {}
    
    try:
        if args.quick:
            # Quick test only
            results["Quick Test"] = test_quick_generation()
        elif args.batch:
            # Batch processing test
            results["Batch Processing"] = test_batch_processing()
        elif args.all:
            # All aspect ratios test
            results["Aspect Ratios"] = test_aspect_ratios()
        elif args.kontext:
            # FLUX Kontext only
            results["Kontext Modification"] = test_kontext_modification()
        elif getattr(args, 'kontext_multi', False):
            # FLUX Kontext Multi only
            results["Kontext Multi"] = test_kontext_multi()
        elif getattr(args, 'photon_base', False):
            # Luma Photon Base only
            results["Photon Base"] = test_photon_base()
        elif args.compare:
            # Model comparison
            results["Model Comparison"] = test_model_comparison()
        else:
            # Default: basic tests for both models
            results["Basic Photon Modification"] = test_basic_modification()
            results["FLUX Kontext Modification"] = test_kontext_modification()
        
        print_summary(results)
        
        # Check if any tests failed
        failed_tests = []
        for test_name, result in results.items():
            if isinstance(result, dict) and not result.get('success', False):
                failed_tests.append(test_name)
            elif isinstance(result, list) and not all(r.get('success', False) for r in result):
                failed_tests.append(test_name)
        
        if failed_tests:
            print(f"\n❌ Failed tests: {', '.join(failed_tests)}")
            sys.exit(1)
        else:
            print("\n✅ All tests completed successfully!")
            
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()