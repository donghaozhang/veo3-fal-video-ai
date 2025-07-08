#!/usr/bin/env python3
"""
FAL AI Text-to-Image Model Comparison Test

Compares all models with the same prompt to evaluate differences.
⚠️ WARNING: This script WILL INCUR SIGNIFICANT COSTS!

Usage:
    python test_model_comparison.py
    python test_model_comparison.py --yes  # Skip confirmation

Author: AI Assistant
Date: 2024
"""

import os
import sys
import time
from typing import Dict, Any, List

# Add parent directory to path to import the generator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fal_text_to_image_generator import FALTextToImageGenerator

def print_cost_warning():
    """Print cost warning and get user confirmation."""
    print("⚠️" * 25)
    print("💰 HIGH COST WARNING: This script will incur significant charges!")
    print("💰 Tests: All 4 models (Imagen4, Seedream, FLUX Schnell, FLUX Dev)")
    print("💰 Estimated cost: ~$0.060 (4 images)")
    print("💰 Make sure you have sufficient credits in your FAL AI account")
    print("⚠️" * 25)
    
    # Check for --yes flag to skip confirmation
    if '--yes' in sys.argv:
        print("\n✅ Auto-confirmed with --yes flag")
        print("✅ Proceeding with model comparison test...")
        return
    
    response = input("\n❓ Do you want to continue and incur charges? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("❌ Test cancelled by user")
        sys.exit(0)
    
    print("✅ Proceeding with model comparison test...")

def test_model_comparison() -> Dict[str, Any]:
    """Test all models with the same prompt for comparison."""
    print("\n🆚 Testing Model Comparison...")
    
    try:
        # Initialize generator
        generator = FALTextToImageGenerator()
        
        # Common test prompt
        prompt = "A majestic phoenix rising from flames, detailed fantasy art, vibrant colors"
        print(f"📝 Shared Prompt: {prompt}")
        
        # Test all models
        models = ["imagen4", "seedream", "flux_schnell", "flux_dev"]
        results = {}
        
        for i, model in enumerate(models, 1):
            print(f"\n🎨 Testing Model {i}/{len(models)}: {model}")
            
            try:
                start_time = time.time()
                
                if model == "imagen4":
                    result = generator.generate_imagen4(prompt=prompt, output_dir="output")
                elif model == "seedream":
                    result = generator.generate_seedream(prompt=prompt, output_dir="output")
                elif model == "flux_schnell":
                    result = generator.generate_flux_schnell(prompt=prompt, output_dir="output")
                elif model == "flux_dev":
                    result = generator.generate_flux_dev(prompt=prompt, output_dir="output")
                
                processing_time = time.time() - start_time
                result['processing_time'] = processing_time
                
                if result.get("success"):
                    print(f"   ✅ {model}: SUCCESS ({processing_time:.2f}s)")
                    print(f"   📁 Files: {len(result.get('downloaded_files', []))}")
                else:
                    print(f"   ❌ {model}: FAILED - {result.get('error', 'Unknown error')}")
                
                results[model] = result
                
                # Brief pause between requests
                if i < len(models):
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ❌ {model}: ERROR - {e}")
                results[model] = {"success": False, "error": str(e)}
        
        return {
            "success": True,
            "prompt": prompt,
            "results": results,
            "total_models": len(models),
            "successful_models": sum(1 for r in results.values() if r.get("success", False))
        }
        
    except Exception as e:
        print(f"\n❌ Error during model comparison: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def print_comparison_summary(results: Dict[str, Any]):
    """Print detailed comparison summary."""
    if not results.get("success"):
        return
    
    print("\n" + "=" * 70)
    print("📊 MODEL COMPARISON SUMMARY")
    print("=" * 70)
    print(f"📝 Prompt: {results.get('prompt', 'N/A')}")
    print(f"🎯 Models tested: {results.get('total_models', 0)}")
    print(f"✅ Successful: {results.get('successful_models', 0)}")
    print()
    
    model_results = results.get("results", {})
    
    for model, result in model_results.items():
        print(f"🤖 {model.upper()}:")
        if result.get("success"):
            print(f"   ✅ Status: SUCCESS")
            print(f"   ⏱️  Time: {result.get('processing_time', 'N/A'):.2f}s")
            print(f"   📁 Files: {len(result.get('downloaded_files', []))}")
            
            # Show file details
            for file_path in result.get('downloaded_files', []):
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"      🖼️  {os.path.basename(file_path)} ({file_size:,} bytes)")
        else:
            print(f"   ❌ Status: FAILED")
            print(f"   💥 Error: {result.get('error', 'Unknown error')}")
        print()

def main():
    """Main test function."""
    print("🧪 FAL AI Text-to-Image Model Comparison")
    print("=" * 60)
    
    # Print cost warning and get confirmation
    print_cost_warning()
    
    # Run comparison test
    results = test_model_comparison()
    
    # Print detailed summary
    print_comparison_summary(results)
    
    # Final results
    print("=" * 70)
    if results.get("success"):
        successful = results.get("successful_models", 0)
        total = results.get("total_models", 0)
        print(f"🎉 Model comparison completed: {successful}/{total} models successful")
        
        if successful == total:
            print("✅ All models working perfectly!")
        elif successful > 0:
            print("⚠️  Some models failed - check individual results above")
        else:
            print("❌ All models failed - check your setup and API credits")
    else:
        print("❌ Model comparison failed")
        print(f"💥 Error: {results.get('error', 'Unknown error')}")
    
    print("\n💡 Comparison completed!")

if __name__ == "__main__":
    main()