#!/usr/bin/env python3
"""
FAL AI Text-to-Image Test Suite

This test suite provides cost-conscious testing for all four text-to-image models.

⚠️ COST WARNING: 
- FREE tests: API connection and setup validation (no image generation)
- PAID tests: Actual image generation (~$0.01-0.02 per image)

Usage:
    python test_text_to_image.py                    # FREE - Setup test only
    python test_text_to_image.py --imagen4          # PAID - Test Imagen 4 only
    python test_text_to_image.py --seedream         # PAID - Test Seedream only  
    python test_text_to_image.py --flux-schnell     # PAID - Test FLUX Schnell only
    python test_text_to_image.py --flux-dev         # PAID - Test FLUX Dev only
    python test_text_to_image.py --compare          # PAID - Test all models (~$0.04-0.08)
    python test_text_to_image.py --full             # PAID - Full test with downloads

Author: AI Assistant
Date: 2024
"""

import os
import sys
import argparse
import time
from typing import Dict, Any, List
from fal_text_to_image_generator import FALTextToImageGenerator

def print_banner():
    """Print the test banner with cost information."""
    print("=" * 70)
    print("🧪 FAL AI TEXT-TO-IMAGE TEST SUITE")
    print("=" * 70)
    print("📋 Available Models:")
    print("   • Imagen 4 Preview Fast - Cost-effective Google model")
    print("   • Seedream v3 - Bilingual (Chinese/English) model")
    print("   • FLUX.1 Schnell - Fastest FLUX model")
    print("   • FLUX.1 Dev - High-quality 12B parameter model")
    print()
    print("💰 COST INFORMATION:")
    print("   • FREE tests: Setup and API validation only")
    print("   • PAID tests: ~$0.01-0.02 per image generated")
    print("   • Comparison tests: ~$0.04-0.08 (4 images)")
    print("=" * 70)

def test_environment_setup() -> bool:
    """Test environment setup and API key validation (FREE)."""
    print("\n🔧 Testing Environment Setup...")
    
    try:
        # Check if .env file exists
        env_file = ".env"
        if os.path.exists(env_file):
            print(f"✅ Found {env_file}")
        else:
            print(f"⚠️  No {env_file} file found")
        
        # Try to initialize generator
        generator = FALTextToImageGenerator()
        print("✅ FAL AI Text-to-Image Generator initialized successfully")
        
        # Test API key presence
        if generator.api_key:
            print("✅ FAL_KEY found in environment")
            # Mask the key for security
            masked_key = f"{generator.api_key[:8]}...{generator.api_key[-4:]}"
            print(f"🔑 API Key: {masked_key}")
        else:
            print("❌ FAL_KEY not found in environment")
            return False
        
        # Test model information
        model_info = generator.get_model_info()
        print(f"✅ Found {len(model_info)} supported models")
        
        return True
        
    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        return False

def confirm_paid_test(test_description: str, cost_estimate: str) -> bool:
    """Confirm paid test with user."""
    print(f"\n⚠️  COST WARNING: {test_description}")
    print(f"💰 Estimated cost: {cost_estimate}")
    print("💳 This will charge your FAL AI account.")
    
    confirm = input("\n🤔 Do you want to proceed? (y/N): ").strip().lower()
    return confirm in ['y', 'yes']

def test_single_model(generator: FALTextToImageGenerator, model: str, download: bool = False) -> Dict[str, Any]:
    """Test a single model with image generation (PAID)."""
    print(f"\n🎨 Testing {model} model...")
    
    # Test prompts for different models
    test_prompts = {
        "imagen4": "A beautiful landscape with mountains and a lake, digital art style",
        "seedream": "一个美丽的风景，有山和湖，数字艺术风格",  # Chinese prompt for Seedream
        "flux_schnell": "A cute robot in a futuristic city, cartoon style",
        "flux_dev": "A professional portrait of a person in business attire, photorealistic"
    }
    
    prompt = test_prompts.get(model, "A beautiful sunset over the ocean, artistic style")
    
    try:
        print(f"📝 Using prompt: {prompt}")
        
        # Add negative prompt for supported models
        negative_prompt = None
        if model in ["seedream", "flux_dev"]:
            negative_prompt = "blur, distortion, low quality, artifacts"
            print(f"❌ Using negative prompt: {negative_prompt}")
        
        # Generate image
        start_time = time.time()
        result = generator.generate_image(
            prompt=prompt,
            model=model,
            negative_prompt=negative_prompt
        )
        generation_time = time.time() - start_time
        
        if result['success']:
            print(f"✅ {model} generation successful!")
            print(f"⏱️  Generation time: {generation_time:.2f} seconds")
            print(f"🔗 Image URL: {result['image_url']}")
            print(f"📏 Image size: {result.get('image_size', 'unknown')}")
            
            # Download if requested
            if download:
                try:
                    filename = f"test_{model}_{int(time.time())}.png"
                    local_path = generator.download_image(
                        result['image_url'],
                        "test_output",
                        filename
                    )
                    result['local_path'] = local_path
                    print(f"📁 Downloaded to: {local_path}")
                except Exception as e:
                    print(f"⚠️  Download failed: {e}")
            
            return {
                'success': True,
                'model': model,
                'generation_time': generation_time,
                'result': result
            }
        else:
            print(f"❌ {model} generation failed: {result['error']}")
            return {
                'success': False,
                'model': model,
                'error': result['error']
            }
    
    except Exception as e:
        print(f"❌ {model} test failed: {e}")
        return {
            'success': False,
            'model': model,
            'error': str(e)
        }

def test_all_models(generator: FALTextToImageGenerator, download: bool = False) -> Dict[str, Any]:
    """Test all models with comparison (PAID - EXPENSIVE)."""
    print("\n🔄 Testing All Models (Comparison Mode)")
    
    models = ["imagen4", "seedream", "flux_schnell", "flux_dev"]
    results = {}
    
    # Common prompt for fair comparison
    prompt = "A majestic eagle soaring over snow-capped mountains at sunset, cinematic style"
    negative_prompt = "blur, distortion, low quality, artifacts"
    
    print(f"📝 Using common prompt: {prompt}")
    print(f"❌ Using negative prompt (where supported): {negative_prompt}")
    
    for i, model in enumerate(models, 1):
        print(f"\n📊 Testing model {i}/{len(models)}: {model}")
        
        try:
            start_time = time.time()
            result = generator.generate_image(
                prompt=prompt,
                model=model,
                negative_prompt=negative_prompt if model in ["seedream", "flux_dev"] else None
            )
            generation_time = time.time() - start_time
            
            if result['success']:
                print(f"✅ {model}: Success ({generation_time:.2f}s)")
                
                # Download for comparison
                if download:
                    try:
                        filename = f"comparison_{model}_{int(time.time())}.png"
                        local_path = generator.download_image(
                            result['image_url'],
                            "test_output",
                            filename
                        )
                        result['local_path'] = local_path
                    except Exception as e:
                        print(f"⚠️  Download failed for {model}: {e}")
                
                results[model] = {
                    'success': True,
                    'generation_time': generation_time,
                    'result': result
                }
            else:
                print(f"❌ {model}: Failed - {result['error']}")
                results[model] = {
                    'success': False,
                    'error': result['error']
                }
        
        except Exception as e:
            print(f"❌ {model}: Exception - {e}")
            results[model] = {
                'success': False,
                'error': str(e)
            }
    
    return results

def print_test_summary(results: Dict[str, Any]):
    """Print a summary of test results."""
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if isinstance(results, dict) and 'model' in results:
        # Single model result
        if results['success']:
            print(f"✅ {results['model']}: SUCCESS")
            print(f"   ⏱️  Time: {results.get('generation_time', 'N/A'):.2f}s")
        else:
            print(f"❌ {results['model']}: FAILED")
            print(f"   Error: {results.get('error', 'Unknown error')}")
    else:
        # Multiple model results
        successful = 0
        total = len(results)
        
        for model, result in results.items():
            if result['success']:
                successful += 1
                print(f"✅ {model}: SUCCESS ({result.get('generation_time', 0):.2f}s)")
            else:
                print(f"❌ {model}: FAILED - {result.get('error', 'Unknown')}")
        
        print(f"\n🎯 Overall Success Rate: {successful}/{total} ({successful/total*100:.1f}%)")
        
        if successful > 0:
            avg_time = sum(r.get('generation_time', 0) for r in results.values() if r['success']) / successful
            print(f"⏱️  Average Generation Time: {avg_time:.2f}s")

def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description="FAL AI Text-to-Image Test Suite")
    
    # Model-specific tests
    parser.add_argument('--imagen4', action='store_true', help='Test Imagen 4 model only (~$0.01)')
    parser.add_argument('--seedream', action='store_true', help='Test Seedream model only (~$0.01)')
    parser.add_argument('--flux-schnell', action='store_true', help='Test FLUX Schnell model only (~$0.01)')
    parser.add_argument('--flux-dev', action='store_true', help='Test FLUX Dev model only (~$0.02)')
    
    # Comparison tests
    parser.add_argument('--compare', action='store_true', help='Test all models for comparison (~$0.04-0.08)')
    parser.add_argument('--full', action='store_true', help='Full test with downloads (~$0.04-0.08)')
    
    # Options
    parser.add_argument('--download', action='store_true', help='Download generated images locally')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Test environment setup (always free)
    if not test_environment_setup():
        print("\n❌ Environment setup failed. Please check your configuration.")
        sys.exit(1)
    
    # If no paid test flags, just do free setup test
    paid_tests = [args.imagen4, args.seedream, getattr(args, 'flux_schnell'), args.flux_dev, args.compare, args.full]
    if not any(paid_tests):
        print("\n✅ FREE setup test completed successfully!")
        print("\n💡 To run paid tests, use flags like --imagen4, --seedream, --flux-schnell, --flux-dev")
        print("   Or use --compare to test all models, --full for complete testing")
        return
    
    try:
        generator = FALTextToImageGenerator()
        
        # Create test output directory
        os.makedirs("test_output", exist_ok=True)
        
        # Run specific tests based on flags
        if args.full or args.compare:
            # Full comparison test
            cost = "~$0.04-0.08 (4 images)"
            if not confirm_paid_test("Full model comparison test", cost):
                print("❌ Test cancelled by user.")
                return
            
            results = test_all_models(generator, download=True)
            print_test_summary(results)
        
        else:
            # Individual model tests
            test_models = []
            if args.imagen4:
                test_models.append(("imagen4", "~$0.01"))
            if args.seedream:
                test_models.append(("seedream", "~$0.01"))
            if getattr(args, 'flux_schnell'):
                test_models.append(("flux_schnell", "~$0.01"))
            if args.flux_dev:
                test_models.append(("flux_dev", "~$0.02"))
            
            for model, cost in test_models:
                if not confirm_paid_test(f"Test {model} model", cost):
                    print(f"❌ {model} test cancelled by user.")
                    continue
                
                result = test_single_model(generator, model, download=args.download)
                print_test_summary(result)
    
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
