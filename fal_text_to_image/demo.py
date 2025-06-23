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
    print("5. Compare all models (~$0.04-0.08)")
    print("6. Show model information")
    print("0. Exit")

def generate_single_image(generator: FALTextToImageGenerator):
    """Generate a single image with selected model."""
    display_model_menu()
    
    try:
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == "0":
            return False
        elif choice == "6":
            show_model_info(generator)
            return True
        elif choice == "5":
            return compare_all_models(generator)
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
            print("2. Show model information")
            print("0. Exit")
            
            choice = input("\nEnter your choice (0-2): ").strip()
            
            if choice == "0":
                print("\n👋 Thank you for using FAL AI Text-to-Image Generator!")
                break
            elif choice == "1":
                if not generate_single_image(generator):
                    break
            elif choice == "2":
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