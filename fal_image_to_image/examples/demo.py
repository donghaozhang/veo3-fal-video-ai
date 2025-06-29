#!/usr/bin/env python3
"""
FAL AI Image-to-Image Interactive Demo

This script provides an interactive command-line interface for modifying images
using FAL AI's dual-model system:
- Luma Photon Flash: Creative, personalizable modifications
- FLUX Kontext: High-quality, detailed transformations

⚠️ WARNING: This script WILL INCUR COSTS when generating images!
Estimated cost: ~$0.01-0.05 per image modification

Usage:
    python demo.py

Features:
- Interactive prompts for all parameters
- Dual-model support (Photon Flash & FLUX Kontext)
- Support for both URL and local images
- Cost warnings and confirmations
- Model comparison functionality
- Multiple aspect ratios and resolution modes
- Model-specific parameter tuning
- Batch processing capabilities

Author: AI Assistant
Date: 2024
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional, List

def print_banner():
    """Print the demo banner."""
    print("=" * 70)
    print("🎨 FAL AI IMAGE-TO-IMAGE DEMO")
    print("=" * 70)
    print("Transform your images with AI-powered modifications!")
    print("🔸 Luma Photon Flash - Creative, personalizable, intelligent")
    print("🔸 Luma Photon Base - Most creative visual model")
    print("🔸 FLUX Kontext - High-quality, detailed transformations")
    print("=" * 70)

def print_cost_warning():
    """Print cost warning."""
    print("\n💰 COST WARNING:")
    print("   • Each image modification costs approximately $0.01-0.05")
    print("   • Costs depend on image size and processing complexity")
    print("   • Make sure you have sufficient credits in your FAL AI account")
    print("   • You will be prompted before each paid operation")

def print_model_info():
    """Print model information."""
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        all_models = generator.get_model_info()
        
        print("\n🤖 MODEL INFORMATION:")
        
        for model_key, model_info in all_models.items():
            print(f"\n   🔹 {model_key.upper()}: {model_info['model_name']}")
            print(f"      • Description: {model_info['description']}")
            print(f"      • Endpoint: {model_info['endpoint']}")
            
            if model_key == "photon":
                print(f"      • Strength Range: {model_info['strength_range']}")
                print(f"      • Aspect Ratios: {', '.join(model_info['supported_aspect_ratios'])}")
            else:  # kontext
                print(f"      • Inference Steps: {model_info['inference_steps_range']}")
                print(f"      • Guidance Scale: {model_info['guidance_scale_range']}")
                print(f"      • Resolution Modes: {', '.join(model_info['supported_aspect_ratios'])}")
            
            print(f"      • Features: {', '.join(model_info['features'])}")
        
    except Exception as e:
        print(f"\n❌ Could not load model info: {e}")

def get_user_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("❌ This field is required. Please enter a value.")

def get_float_input(prompt: str, min_val: float, max_val: float, default: float) -> float:
    """Get float input within range."""
    while True:
        try:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                return default
            
            value = float(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"❌ Value must be between {min_val} and {max_val}")
        except ValueError:
            print("❌ Please enter a valid number")

def choose_model() -> str:
    """Let user choose between models."""
    print("\n🤖 Available Models:")
    print("   1. Photon Flash (Luma) - Creative, personalizable")
    print("   2. Photon Base (Luma) - Most creative visual model")
    print("   3. FLUX Kontext - High-quality, detailed modifications")
    print("   4. FLUX Kontext Multi - Multi-image experimental generation")
    
    while True:
        choice = input("\nChoose model (1-4) [1]: ").strip()
        if not choice or choice == '1':
            return 'photon'
        elif choice == '2':
            return 'photon_base'
        elif choice == '3':
            return 'kontext'
        elif choice == '4':
            return 'kontext_multi'
        else:
            print("❌ Please choose 1, 2, 3, or 4")

def choose_aspect_ratio(model: str = 'photon') -> str:
    """Let user choose aspect ratio."""
    try:
        from fal_image_to_image_generator import ASPECT_RATIOS, RESOLUTION_MODES
        
        if model == 'photon':
            options = ASPECT_RATIOS
            title = "📐 Available Aspect Ratios:"
        else:  # kontext
            options = RESOLUTION_MODES
            title = "📐 Available Resolution Modes:"
        
        print(f"\n{title}")
        for i, option in enumerate(options, 1):
            print(f"   {i}. {option}")
        
        while True:
            try:
                choice = input(f"\nChoose option (1-{len(options)}) [1]: ").strip()
                if not choice:
                    return options[0]  # Default to first option
                
                index = int(choice) - 1
                if 0 <= index < len(options):
                    return options[index]
                else:
                    print(f"❌ Please choose a number between 1 and {len(options)}")
            except ValueError:
                print("❌ Please enter a valid number")
                
    except ImportError:
        return "1:1" if model == 'photon' else "auto"  # Fallback

def get_kontext_parameters():
    """Get FLUX Kontext-specific parameters."""
    print("\n⚙️  FLUX Kontext Parameters:")
    
    # Inference steps
    steps = get_float_input("   Inference steps (1-50)", 1, 50, 28)
    
    # Guidance scale
    guidance = get_float_input("   Guidance scale (1.0-20.0)", 1.0, 20.0, 2.5)
    
    return int(steps), guidance

def confirm_generation(cost_estimate: str = "$0.01-0.05") -> bool:
    """Get user confirmation for paid operation."""
    print(f"\n💰 This operation will cost approximately {cost_estimate}")
    while True:
        confirm = input("❓ Do you want to proceed? (yes/no) [no]: ").strip().lower()
        if confirm in ['yes', 'y']:
            return True
        elif confirm in ['no', 'n', '']:
            return False
        else:
            print("❌ Please answer 'yes' or 'no'")

def single_image_demo():
    """Demo for single image modification."""
    print("\n🖼️  SINGLE IMAGE MODIFICATION")
    print("-" * 40)
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Get image input
        print("\n📥 Image Input:")
        input_type = input("   Use local file or URL? (local/url) [url]: ").strip().lower()
        
        if input_type == 'local':
            image_path = get_user_input("   Enter path to local image file")
            if not Path(image_path).exists():
                print(f"❌ File not found: {image_path}")
                return
        else:
            image_url = get_user_input("   Enter image URL", "https://picsum.photos/512/512")
        
        # Choose model
        model = choose_model()
        
        # Get modification prompt
        print("\n✏️  Modification:")
        prompt = get_user_input("   Describe how to modify the image", 
                               "Convert this image to a watercolor painting style")
        
        # Get model-specific parameters
        if model in ['photon', 'photon_base']:
            model_display = "Photon Flash" if model == 'photon' else "Photon Base"
            print(f"\n⚙️  {model_display} Parameters:")
            strength = get_float_input("   Modification strength (0.0-1.0)", 0.0, 1.0, 0.7)
            aspect_ratio = choose_aspect_ratio(model)
            
            # Get output directory
            output_dir = get_user_input("   Output directory", "output")
            
            # Confirm generation
            if not confirm_generation():
                print("❌ Operation cancelled")
                return
            
            print(f"\n🚀 Starting {model_display} modification...")
            
            # Generate with appropriate Photon model
            if input_type == 'local':
                if model == 'photon':
                    result = generator.modify_local_image_photon(
                        prompt=prompt,
                        image_path=image_path,
                        strength=strength,
                        aspect_ratio=aspect_ratio,
                        output_dir=output_dir
                    )
                else:  # photon_base
                    result = generator.modify_local_image_photon_base(
                        prompt=prompt,
                        image_path=image_path,
                        strength=strength,
                        aspect_ratio=aspect_ratio,
                        output_dir=output_dir
                    )
            else:
                if model == 'photon':
                    result = generator.modify_image_photon(
                        prompt=prompt,
                        image_url=image_url,
                        strength=strength,
                        aspect_ratio=aspect_ratio,
                        output_dir=output_dir
                    )
                else:  # photon_base
                    result = generator.modify_image_photon_base(
                        prompt=prompt,
                        image_url=image_url,
                        strength=strength,
                        aspect_ratio=aspect_ratio,
                        output_dir=output_dir
                    )
        elif model == 'kontext':  # Regular FLUX Kontext
            num_inference_steps, guidance_scale = get_kontext_parameters()
            resolution_mode = choose_aspect_ratio(model)
            
            # Get output directory
            output_dir = get_user_input("   Output directory", "output")
            
            # Confirm generation
            if not confirm_generation():
                print("❌ Operation cancelled")
                return
            
            print("\n🚀 Starting FLUX Kontext modification...")
            
            # Generate with Kontext
            if input_type == 'local':
                result = generator.modify_local_image_kontext(
                    prompt=prompt,
                    image_path=image_path,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    resolution_mode=resolution_mode,
                    output_dir=output_dir
                )
            else:
                result = generator.modify_image_kontext(
                    prompt=prompt,
                    image_url=image_url,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    resolution_mode=resolution_mode,
                    output_dir=output_dir
                )
        else:  # kontext_multi
            print("❌ FLUX Kontext Multi requires multiple images. Use 'Multi-Image Generation' menu option instead.")
            return
        
        # Show results
        if result['success']:
            print("\n✅ Image modification completed!")
            print(f"   Processing time: {result['processing_time']:.2f} seconds")
            print(f"   Output files: {len(result['downloaded_files'])}")
            for file_path in result['downloaded_files']:
                print(f"   📁 {file_path}")
        else:
            print(f"\n❌ Image modification failed: {result.get('error', 'Unknown error')}")
            
    except ImportError as e:
        print(f"❌ Failed to import generator: {e}")
        print("💡 Make sure fal_image_to_image_generator.py is in the same directory")
    except Exception as e:
        print(f"❌ Demo error: {e}")

def multi_image_demo():
    """Demo for multi-image FLUX Kontext generation."""
    print("\n🔢 MULTI-IMAGE GENERATION")
    print("-" * 40)
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from fal_image_to_image_generator import FALImageToImageGenerator, KONTEXT_MULTI_ASPECT_RATIOS
        
        generator = FALImageToImageGenerator()
        
        # Get number of input images
        while True:
            try:
                count = int(input("   How many input images? (2-5) [2]: ") or "2")
                if 2 <= count <= 5:
                    break
                else:
                    print("❌ Please enter a number between 2 and 5")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Get image inputs
        image_urls = []
        image_paths = []
        input_type = input("   Use local files or URLs? (local/url) [url]: ").strip().lower()
        
        print(f"\n📥 Enter {count} image sources:")
        for i in range(count):
            if input_type == 'local':
                path = get_user_input(f"   Image {i+1} path")
                if not Path(path).exists():
                    print(f"❌ File not found: {path}")
                    return
                image_paths.append(path)
            else:
                url = get_user_input(f"   Image {i+1} URL", f"https://picsum.photos/512/512?random={i+1}")
                image_urls.append(url)
        
        # Get generation prompt
        print("\n✏️  Generation:")
        prompt = get_user_input("   Describe the desired generation", 
                               "Put the little duckling on top of the woman's t-shirt.")
        
        # Get Kontext Multi parameters
        print("\n⚙️  FLUX Kontext Multi Parameters:")
        guidance_scale = get_float_input("   Guidance scale (1.0-20.0)", 1.0, 20.0, 3.5)
        num_images = int(get_float_input("   Number of output images (1-10)", 1, 10, 1))
        
        # Choose aspect ratio
        print("\n📐 Available Aspect Ratios:")
        for i, ratio in enumerate(KONTEXT_MULTI_ASPECT_RATIOS, 1):
            print(f"   {i}. {ratio}")
        
        while True:
            try:
                choice = input(f"\nChoose aspect ratio (1-{len(KONTEXT_MULTI_ASPECT_RATIOS)}) [5]: ").strip()
                if not choice:
                    aspect_ratio = KONTEXT_MULTI_ASPECT_RATIOS[4]  # Default to "1:1"
                    break
                
                index = int(choice) - 1
                if 0 <= index < len(KONTEXT_MULTI_ASPECT_RATIOS):
                    aspect_ratio = KONTEXT_MULTI_ASPECT_RATIOS[index]
                    break
                else:
                    print(f"❌ Please choose a number between 1 and {len(KONTEXT_MULTI_ASPECT_RATIOS)}")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Get output directory
        output_dir = get_user_input("   Output directory", "output")
        
        # Estimate cost
        estimated_cost = f"${0.02 * num_images:.2f}-${0.05 * num_images:.2f}"
        
        # Confirm generation
        if not confirm_generation(estimated_cost):
            print("❌ Multi-image generation cancelled")
            return
        
        print(f"\n🚀 Starting FLUX Kontext Multi generation with {count} input images...")
        
        # Generate
        if input_type == 'local':
            result = generator.modify_multi_local_images_kontext(
                prompt=prompt,
                image_paths=image_paths,
                guidance_scale=guidance_scale,
                num_images=num_images,
                aspect_ratio=aspect_ratio,
                output_dir=output_dir
            )
        else:
            result = generator.modify_multi_images_kontext(
                prompt=prompt,
                image_urls=image_urls,
                guidance_scale=guidance_scale,
                num_images=num_images,
                aspect_ratio=aspect_ratio,
                output_dir=output_dir
            )
        
        # Show results
        if result['success']:
            print("\n✅ Multi-image generation completed!")
            print(f"   Processing time: {result['processing_time']:.2f} seconds")
            print(f"   Input images: {result['input_images']}")
            print(f"   Output images: {result['output_images']}")
            for file_path in result['downloaded_files']:
                print(f"   📁 {file_path}")
        else:
            print(f"\n❌ Multi-image generation failed: {result.get('error', 'Unknown error')}")
            
    except ImportError as e:
        print(f"❌ Failed to import generator: {e}")
    except Exception as e:
        print(f"❌ Multi-image demo error: {e}")

def batch_demo():
    """Demo for batch image processing."""
    print("\n📦 BATCH IMAGE MODIFICATION")
    print("-" * 40)
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Get number of images
        while True:
            try:
                count = int(input("   How many images to process? [3]: ") or "3")
                if count > 0:
                    break
                else:
                    print("❌ Please enter a positive number")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Get image URLs and prompts
        image_urls = []
        prompts = []
        
        print(f"\n📥 Enter {count} image URLs and prompts:")
        for i in range(count):
            print(f"\n   Image {i+1}:")
            url = get_user_input(f"   URL", f"https://picsum.photos/512/512?random={i+1}")
            prompt = get_user_input(f"   Modification prompt", f"Apply artistic style {i+1}")
            
            image_urls.append(url)
            prompts.append(prompt)
        
        # Choose model
        model = choose_model()
        
        # Get model-specific parameters
        output_dir = get_user_input("   Output directory", "output")
        
        if model == 'photon':
            print("\n⚙️  Photon Flash Parameters:")
            strength = get_float_input("   Modification strength (0.0-1.0)", 0.0, 1.0, 0.7)
            aspect_ratio = choose_aspect_ratio(model)
        else:  # kontext
            num_inference_steps, guidance_scale = get_kontext_parameters()
            resolution_mode = choose_aspect_ratio(model)
        
        # Estimate cost
        estimated_cost = f"${0.01 * count:.2f}-${0.05 * count:.2f}"
        
        # Confirm batch generation
        if not confirm_generation(estimated_cost):
            print("❌ Batch operation cancelled")
            return
        
        print(f"\n🚀 Starting batch modification of {count} images with {model.upper()}...")
        
        # Generate batch
        if model == 'photon':
            results = generator.batch_modify_images_photon(
                prompts=prompts,
                image_urls=image_urls,
                strength=strength,
                aspect_ratio=aspect_ratio,
                output_dir=output_dir
            )
        else:  # kontext
            results = generator.batch_modify_images_kontext(
                prompts=prompts,
                image_urls=image_urls,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                resolution_mode=resolution_mode,
                output_dir=output_dir
            )
        
        # Show results
        successful = sum(1 for r in results if r['success'])
        print(f"\n📊 Batch processing completed: {successful}/{count} successful")
        
        for i, result in enumerate(results, 1):
            if result['success']:
                print(f"   ✅ Image {i}: Success ({result['processing_time']:.2f}s)")
                for file_path in result['downloaded_files']:
                    print(f"      📁 {file_path}")
            else:
                print(f"   ❌ Image {i}: Failed - {result.get('error', 'Unknown')}")
                
    except ImportError as e:
        print(f"❌ Failed to import generator: {e}")
    except Exception as e:
        print(f"❌ Batch demo error: {e}")

def show_help():
    """Show help information."""
    print("\n📖 HELP - FAL AI Image-to-Image Demo")
    print("-" * 50)
    print("This demo allows you to modify images using AI with text prompts.")
    print("\n🤖 Available Models:")
    print("   • Photon Flash (Luma): Creative, personalizable modifications")
    print("   • Photon Base (Luma): Most creative visual model for creatives")
    print("   • FLUX Kontext: High-quality, detailed transformations")
    print("   • FLUX Kontext Multi: Experimental multi-image generation")
    print("\n✏️  Prompt Examples:")
    print("   • 'Convert to watercolor painting style'")
    print("   • 'Make it look like a vintage photograph'")
    print("   • 'Transform into cyberpunk aesthetic'")
    print("   • 'Apply oil painting effect'")
    print("   • 'Convert to pencil sketch'")
    print("\n⚙️  Parameter Guidelines:")
    print("   Photon Flash - Strength:")
    print("      • 0.0-0.3: Subtle modifications")
    print("      • 0.4-0.6: Moderate changes")
    print("      • 0.7-1.0: Strong transformations")
    print("   FLUX Kontext - Inference Steps:")
    print("      • 1-15: Fast but lower quality")
    print("      • 16-35: Balanced speed and quality")
    print("      • 36-50: High quality but slower")
    print("   FLUX Kontext - Guidance Scale:")
    print("      • 1.0-2.0: More creative freedom")
    print("      • 2.1-5.0: Balanced adherence to prompt")
    print("      • 5.1-20.0: Strict prompt following")
    print("   FLUX Kontext Multi - Guidance Scale:")
    print("      • 1.0-5.0: Balanced multi-image blending")
    print("      • 5.1-10.0: Strong prompt adherence")
    print("      • 10.1-20.0: Very strict control")
    print("\n💡 Tips:")
    print("   • Be specific in your prompts for better results")
    print("   • Choose Photon Flash for creative, personalizable modifications")
    print("   • Choose Photon Base for the most creative visual transformations")
    print("   • Choose FLUX Kontext for detailed, high-quality changes")
    print("   • Choose FLUX Kontext Multi for experimental multi-image generation")
    print("   • Multi-image generation works best with 2-3 related images")
    print("   • Test with free setup validation first: python test_setup.py")

def model_comparison_demo():
    """Demo comparing both models with the same image and prompt."""
    print("\n🆚 MODEL COMPARISON")
    print("-" * 40)
    
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from fal_image_to_image_generator import FALImageToImageGenerator
        
        generator = FALImageToImageGenerator()
        
        # Get image input
        print("\n📥 Image Input:")
        input_type = input("   Use local file or URL? (local/url) [url]: ").strip().lower()
        
        if input_type == 'local':
            image_path = get_user_input("   Enter path to local image file")
            if not Path(image_path).exists():
                print(f"❌ File not found: {image_path}")
                return
            image_url = None
        else:
            image_url = get_user_input("   Enter image URL", "https://picsum.photos/512/512")
            image_path = None
        
        # Get modification prompt
        print("\n✏️  Modification:")
        prompt = get_user_input("   Describe how to modify the image", 
                               "Transform this into an artistic painting")
        
        # Get output directory
        output_dir = get_user_input("   Output directory", "output")
        
        # Confirm comparison (costs ~$0.02-0.10 for both models)
        if not confirm_generation("$0.02-0.10 (both models)"):
            print("❌ Model comparison cancelled")
            return
        
        print("\n🚀 Starting model comparison...")
        
        # Test both models
        results = {}
        
        # Photon Flash
        print("\n   🔸 Testing Photon Flash...")
        if image_path:
            photon_result = generator.modify_local_image_photon(
                prompt=prompt,
                image_path=image_path,
                strength=0.7,
                aspect_ratio="1:1",
                output_dir=output_dir
            )
        else:
            photon_result = generator.modify_image_photon(
                prompt=prompt,
                image_url=image_url,
                strength=0.7,
                aspect_ratio="1:1",
                output_dir=output_dir
            )
        results['photon'] = photon_result
        
        # Brief pause between models
        time.sleep(3)
        
        # FLUX Kontext
        print("   🔸 Testing FLUX Kontext...")
        if image_path:
            kontext_result = generator.modify_local_image_kontext(
                prompt=prompt,
                image_path=image_path,
                num_inference_steps=28,
                guidance_scale=2.5,
                resolution_mode="auto",
                output_dir=output_dir
            )
        else:
            kontext_result = generator.modify_image_kontext(
                prompt=prompt,
                image_url=image_url,
                num_inference_steps=28,
                guidance_scale=2.5,
                resolution_mode="auto",
                output_dir=output_dir
            )
        results['kontext'] = kontext_result
        
        # Show comparison results
        print(f"\n📊 Model Comparison Results:")
        print("-" * 40)
        
        for model_name, result in results.items():
            model_display = "Photon Flash" if model_name == 'photon' else "FLUX Kontext"
            if result['success']:
                print(f"   ✅ {model_display}: Success ({result['processing_time']:.2f}s)")
                for file_path in result['downloaded_files']:
                    print(f"      📁 {file_path}")
            else:
                print(f"   ❌ {model_display}: Failed - {result.get('error', 'Unknown')}")
        
        # Performance comparison
        if results['photon']['success'] and results['kontext']['success']:
            photon_time = results['photon']['processing_time']
            kontext_time = results['kontext']['processing_time']
            faster_model = "Photon Flash" if photon_time < kontext_time else "FLUX Kontext"
            time_diff = abs(photon_time - kontext_time)
            print(f"\n⚡ {faster_model} was {time_diff:.1f}s faster")
            
    except ImportError as e:
        print(f"❌ Failed to import generator: {e}")
    except Exception as e:
        print(f"❌ Comparison demo error: {e}")

def main_menu():
    """Show main menu and handle user choice."""
    while True:
        print("\n🎨 MAIN MENU")
        print("-" * 20)
        print("1. Single Image Modification")
        print("2. Multi-Image Generation (FLUX Kontext)")
        print("3. Batch Image Processing")
        print("4. Model Comparison")
        print("5. Model Information")
        print("6. Help")
        print("7. Exit")
        
        choice = input("\nChoose an option (1-7): ").strip()
        
        if choice == '1':
            single_image_demo()
        elif choice == '2':
            multi_image_demo()
        elif choice == '3':
            batch_demo()
        elif choice == '4':
            model_comparison_demo()
        elif choice == '5':
            print_model_info()
        elif choice == '6':
            show_help()
        elif choice == '7':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please choose 1-7.")

def main():
    """Main demo function."""
    try:
        print_banner()
        print_cost_warning()
        
        # Quick setup check
        try:
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from fal_image_to_image_generator import FALImageToImageGenerator
            generator = FALImageToImageGenerator()
            print("\n✅ Setup validated - ready to generate!")
        except Exception as e:
            print(f"\n❌ Setup issue: {e}")
            print("💡 Run 'python test_setup.py' first to validate your setup")
            return
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
        print(f"📁 Output directory: {Path('output').absolute()}")
        
        # Show main menu
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main()