#!/usr/bin/env python3
"""
FAL AI Text-to-Image Interactive Demo

This demo showcases all four text-to-image models:
1. Imagen 4 Preview Fast - Cost-effective Google model
2. Seedream v3 - Bilingual text-to-image model  
3. FLUX.1 Schnell - Fastest FLUX model
4. FLUX.1 Dev - High-quality FLUX model

⚠️ WARNING: Each image generation costs approximately $0.01-0.02
Please be mindful of costs when using this demo.

Author: AI Assistant
Date: 2024
"""

import os
import sys
from typing import Optional
from fal_text_to_image_generator import FALTextToImageGenerator

def print_banner():
    """Print the demo banner with cost warning."""
    print("=" * 70)
    print("🎨 FAL AI TEXT-TO-IMAGE GENERATOR DEMO")
    print("=" * 70)
    print("📋 Supported Models:")
    print("   1. Imagen 4 Preview Fast - Cost-effective Google model")
    print("   2. Seedream v3 - Bilingual (Chinese/English) model")
    print("   3. FLUX.1 Schnell - Fastest FLUX model")  
    print("   4. FLUX.1 Dev - High-quality 12B parameter model")
    print()
    print("⚠️  COST WARNING:")
    print("   💰 Each image generation costs ~$0.01-0.02")
    print("   💰 Model comparison generates 4 images (~$0.04-0.08)")
    print("   💰 You will be asked for confirmation before any paid operation")
    print("=" * 70)

def get_user_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def confirm_generation(cost_estimate: str) -> bool:
    """Ask user to confirm paid operation."""
    print(f"\n⚠️  COST WARNING: This operation will cost approximately {cost_estimate}")
    confirm = input("💰 Do you want to proceed? This will charge your account (y/N): ").strip().lower()
    return confirm in ['y', 'yes']

def display_model_menu():
    """Display the model selection menu."""
    print("\n🎨 Select a model:")
    print("1. Imagen 4 Preview Fast (Cost-effective, ~$0.01)")
    print("2. Seedream v3 (Bilingual support, ~$0.01)")
    print("3. FLUX.1 Schnell (Fastest, ~$0.01)")
    print("4. FLUX.1 Dev (Highest quality, ~$0.02)")
    print("5. Batch generate (select models) (~$0.01-0.08)")
    print("6. Compare all models (~$0.04-0.08)")
    print("7. Show model information")
    print("0. Exit")

def generate_single_image(generator: FALTextToImageGenerator):
    """Generate a single image with selected model."""
    display_model_menu()
    
    try:
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "0":
            return False
        elif choice == "7":
            show_model_info(generator)
            return True
        elif choice == "6":
            return compare_all_models(generator)
        elif choice == "5":
            return batch_generate_models(generator)
        elif choice not in ["1", "2", "3", "4"]:
            print("❌ Invalid choice. Please try again.")
            return True
        
        # Map choice to model
        model_map = {
            "1": ("imagen4", "Imagen 4 Preview Fast", "~$0.01"),
            "2": ("seedream", "Seedream v3", "~$0.01"),
            "3": ("flux_schnell", "FLUX.1 Schnell", "~$0.01"),
            "4": ("flux_dev", "FLUX.1 Dev", "~$0.02")
        }
        
        model_key, model_name, cost = model_map[choice]
        
        print(f"\n🎨 Selected: {model_name}")
        
        # Get prompt
        prompt = get_user_input("📝 Enter your image description")
        if not prompt:
            print("❌ Prompt cannot be empty.")
            return True
        
        # Get negative prompt for supported models
        negative_prompt = None
        if model_key in ["seedream", "flux_dev"]:
            negative_prompt = get_user_input("❌ Enter negative prompt (optional, what to avoid)", "")
            if not negative_prompt:
                negative_prompt = None
        
        # Confirm generation
        if not confirm_generation(cost):
            print("❌ Generation cancelled.")
            return True
        
        print(f"\n🚀 Generating image with {model_name}...")
        
        # Generate image
        result = generator.generate_image(
            prompt=prompt,
            model=model_key,
            negative_prompt=negative_prompt
        )
        
        if result['success']:
            print(f"✅ Image generated successfully!")
            print(f"🔗 Image URL: {result['image_url']}")
            
            # Ask if user wants to download
            download = input("\n💾 Download image locally? (Y/n): ").strip().lower()
            if download != 'n':
                try:
                    filename = f"{model_key}_{int(time.time())}.png"
                    local_path = generator.download_image(
                        result['image_url'],
                        "output",
                        filename
                    )
                    print(f"📁 Image saved to: {local_path}")
                except Exception as e:
                    print(f"❌ Download failed: {e}")
        else:
            print(f"❌ Generation failed: {result['error']}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return True

def compare_all_models(generator: FALTextToImageGenerator) -> bool:
    """Compare all models with the same prompt."""
    print("\n🔄 Model Comparison Mode")
    print("This will generate images with all 4 models for comparison.")
    
    # Get prompt
    prompt = get_user_input("📝 Enter your image description")
    if not prompt:
        print("❌ Prompt cannot be empty.")
        return True
    
    # Get negative prompt
    negative_prompt = get_user_input("❌ Enter negative prompt (optional, for compatible models)", "")
    if not negative_prompt:
        negative_prompt = None
    
    # Confirm expensive operation
    if not confirm_generation("~$0.04-0.08 (4 images)"):
        print("❌ Comparison cancelled.")
        return True
    
    try:
        results = generator.compare_models(
            prompt=prompt,
            negative_prompt=negative_prompt,
            output_folder="output"
        )
        
        if results.get('cancelled'):
            return True
        
        # Display results summary
        print("\n📊 Comparison Results:")
        print("-" * 50)
        
        for model, result in results.items():
            if result.get('success'):
                print(f"✅ {model}: {result['image_url']}")
                if 'local_path' in result:
                    print(f"   📁 Saved: {result['local_path']}")
            else:
                print(f"❌ {model}: {result.get('error', 'Unknown error')}")
        
        successful = sum(1 for r in results.values() if r.get('success', False))
        print(f"\n🎯 Success rate: {successful}/{len(results)} models")
        
    except Exception as e:
        print(f"❌ Comparison failed: {e}")
    
    return True

def batch_generate_models(generator: FALTextToImageGenerator) -> bool:
    """Batch generate images with selected models."""
    print("\n🔄 Batch Generation Mode")
    print("Select which models you want to use for batch generation.")
    
    # Display available models for selection
    available_models = {
        "1": ("imagen4", "Imagen 4 Preview Fast", "~$0.01"),
        "2": ("seedream", "Seedream v3", "~$0.01"),
        "3": ("flux_schnell", "FLUX.1 Schnell", "~$0.01"),
        "4": ("flux_dev", "FLUX.1 Dev", "~$0.02")
    }
    
    print("\n📋 Available Models:")
    for key, (model_key, name, cost) in available_models.items():
        print(f"{key}. {name} ({cost})")
    
    # Get model selection
    print("\nSelect models (e.g., '1,3,4' for Imagen4, FLUX Schnell, and FLUX Dev):")
    selection = input("Models to use: ").strip()
    
    if not selection:
        print("❌ No models selected.")
        return True
    
    # Parse selection
    selected_models = []
    try:
        for choice in selection.split(','):
            choice = choice.strip()
            if choice in available_models:
                model_key, name, cost = available_models[choice]
                selected_models.append(model_key)
            else:
                print(f"❌ Invalid choice: {choice}")
                return True
    except Exception as e:
        print(f"❌ Invalid selection format: {e}")
        return True
    
    if not selected_models:
        print("❌ No valid models selected.")
        return True
    
    print(f"\n✅ Selected models: {', '.join(selected_models)}")
    
    # Get prompt
    prompt = get_user_input("📝 Enter your image description")
    if not prompt:
        print("❌ Prompt cannot be empty.")
        return True
    
    # Get negative prompt
    compatible_models = [m for m in selected_models if m in ["seedream", "flux_dev"]]
    negative_prompt = None
    if compatible_models:
        negative_prompt = get_user_input(f"❌ Enter negative prompt (optional, for {', '.join(compatible_models)})", "")
        if not negative_prompt:
            negative_prompt = None
    
    # Estimate cost
    estimated_cost = len(selected_models) * 0.015
    cost_str = f"~${estimated_cost:.3f} ({len(selected_models)} images)"
    
    # Confirm batch operation
    if not confirm_generation(cost_str):
        print("❌ Batch generation cancelled.")
        return True
    
    try:
        # Use the new batch_generate method
        result = generator.batch_generate(
            prompt=prompt,
            models=selected_models,
            negative_prompt=negative_prompt,
            output_folder="output",
            download_images=True,
            auto_confirm=True  # We already confirmed above
        )
        
        if result.get('cancelled'):
            return True
        
        # Display results summary
        print("\n📊 Batch Generation Results:")
        print("-" * 60)
        
        results = result['results']
        summary = result['summary']
        
        for model, model_result in results.items():
            if model_result.get('success'):
                time_taken = model_result.get('generation_time', 0)
                print(f"✅ {model}: SUCCESS ({time_taken:.2f}s)")
                print(f"   🔗 URL: {model_result['image_url']}")
                if 'local_path' in model_result:
                    print(f"   📁 File: {model_result['local_path']}")
            else:
                print(f"❌ {model}: FAILED - {model_result.get('error', 'Unknown error')}")
        
        print(f"\n🎯 Summary:")
        print(f"   ✅ Successful: {summary['successful']}/{summary['total_models']}")
        print(f"   ⏱️ Total time: {summary['total_time']:.2f}s")
        print(f"   💰 Estimated cost: ~${summary['estimated_cost']:.3f}")
        
        if summary['successful'] > 0:
            avg_time = summary['total_time'] / summary['successful']
            print(f"   ⚡ Avg generation time: {avg_time:.2f}s")
        
    except Exception as e:
        print(f"❌ Batch generation failed: {e}")
    
    return True

def show_model_info(generator: FALTextToImageGenerator):
    """Display detailed information about all models."""
    model_info = generator.get_model_info()
    
    print("\n📚 MODEL INFORMATION")
    print("=" * 60)
    
    for model_key, info in model_info.items():
        print(f"\n🎨 {info['name']}")
        print(f"   Endpoint: {info['endpoint']}")
        print(f"   Description: {info['description']}")
        print(f"   Strengths: {', '.join(info['strengths'])}")
        print(f"   Max Steps: {info['max_steps']}")
        print(f"   Negative Prompts: {'✅' if info['supports_negative_prompt'] else '❌'}")
        print(f"   Features: {', '.join(info['supported_features'])}")

def main():
    """Main demo function."""
    print_banner()
    
    try:
        # Initialize generator
        print("🔧 Initializing FAL AI Text-to-Image Generator...")
        generator = FALTextToImageGenerator()
        print("✅ Generator initialized successfully!")
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
        
        # Main demo loop
        while True:
            print("\n" + "=" * 50)
            print("🎨 MAIN MENU")
            print("=" * 50)
            print("1. Generate single image")
            print("2. Batch generate with multiple models")
            print("3. Show model information")
            print("0. Exit")
            
            choice = input("\nEnter your choice (0-3): ").strip()
            
            if choice == "0":
                print("\n👋 Thank you for using FAL AI Text-to-Image Generator!")
                break
            elif choice == "1":
                if not generate_single_image(generator):
                    break
            elif choice == "2":
                batch_generate_models(generator)
            elif choice == "3":
                show_model_info(generator)
            else:
                print("❌ Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("Please check your FAL_KEY in the .env file and try again.")
    
    print("\n🎨 Demo ended.")

if __name__ == "__main__":
    import time
    main() 