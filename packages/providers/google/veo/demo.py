#!/usr/bin/env python3
"""
Google Veo Video Generation Demo

This demo script showcases all the capabilities of the Google Veo video generation implementation.
It provides an interactive menu to test different generation modes and models.

Features demonstrated:
- Text-to-video generation (Veo 2.0 and 3.0)
- Image-to-video generation (from local and GCS images)
- Model comparison
- Custom parameter configuration

Usage:
    python demo.py
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from veo_video_generation import (
        generate_video_from_text,
        generate_video_from_image,
        generate_video_from_local_image,
        generate_video_with_veo3_preview
    )
except ImportError as e:
    print(f"Error importing video generation functions: {e}")
    print("Make sure veo_video_generation.py is in the same directory.")
    sys.exit(1)

# Configuration from environment variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
OUTPUT_BUCKET_PATH = os.getenv("OUTPUT_BUCKET_PATH", "gs://your-bucket-name/veo_output/")

def get_user_choice(prompt, options):
    """Get user choice from a list of options."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (number): "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")

def demo_text_to_video():
    """Demonstrate text-to-video generation."""
    print("\n" + "="*60)
    print("TEXT-TO-VIDEO GENERATION DEMO")
    print("="*60)
    
    # Sample prompts
    sample_prompts = [
        "A serene mountain landscape with a flowing river and colorful sunset. Camera slowly pans across the scene.",
        "A futuristic cityscape with flying vehicles and neon lights, cinematic style with dramatic lighting.",
        "A peaceful garden with blooming flowers swaying in a gentle breeze, butterflies dancing in the air.",
        "A cozy coffee shop interior with warm lighting, steam rising from a cup, soft jazz ambiance.",
        "Custom prompt (enter your own)"
    ]
    
    print("Choose a text prompt:")
    choice = get_user_choice("Select a prompt:", sample_prompts)
    
    if choice == len(sample_prompts) - 1:  # Custom prompt
        prompt = input("\nEnter your custom prompt: ").strip()
        if not prompt:
            print("Empty prompt entered. Using default.")
            prompt = sample_prompts[0]
    else:
        prompt = sample_prompts[choice]
    
    print(f"\nSelected prompt: {prompt}")
    
    # Model selection
    models = ["Veo 2.0 (Stable)", "Veo 3.0 (Preview)"]
    model_choice = get_user_choice("Choose model:", models)
    
    print(f"\n🎬 Generating video with {models[model_choice]}...")
    print(f"📝 Prompt: {prompt}")
    print("⏳ This may take 2-10 minutes...")
    
    try:
        if model_choice == 0:  # Veo 2.0
            video_uri = generate_video_from_text(
                project_id=PROJECT_ID,
                prompt=prompt,
                output_bucket_path=OUTPUT_BUCKET_PATH,
                model_id="veo-2.0-generate-001"
            )
        else:  # Veo 3.0
            video_uri = generate_video_with_veo3_preview(
                project_id=PROJECT_ID,
                prompt=prompt,
                output_bucket_path=OUTPUT_BUCKET_PATH
            )
        
        if video_uri:
            print(f"\n✅ Success! Video generated: {video_uri}")
            print("📁 Video also downloaded to ./result_folder/")
        else:
            print("\n❌ Video generation failed. Check the logs above for details.")
            
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")

def demo_image_to_video():
    """Demonstrate image-to-video generation."""
    print("\n" + "="*60)
    print("IMAGE-TO-VIDEO GENERATION DEMO")
    print("="*60)
    
    # Check available local images
    images_dir = current_dir / "images"
    if images_dir.exists():
        image_files = [f for f in os.listdir(images_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
    else:
        image_files = []
    
    if not image_files:
        print("❌ No images found in ./images/ directory")
        print("Please add some images to test image-to-video generation.")
        return
    
    print("Available images:")
    for i, img in enumerate(image_files, 1):
        print(f"{i}. {img}")
    
    print(f"{len(image_files) + 1}. Use custom GCS URI")
    
    choice = get_user_choice("Select an image:", image_files + ["Custom GCS URI"])
    
    if choice == len(image_files):  # Custom GCS URI
        image_path = input("\nEnter GCS URI (gs://bucket/path/image.jpg): ").strip()
        if not image_path.startswith("gs://"):
            print("Invalid GCS URI. Must start with 'gs://'")
            return
        use_local = False
    else:
        image_filename = image_files[choice]
        image_path = image_filename
        use_local = True
    
    # Sample prompts for image animation
    sample_prompts = [
        "The person comes to life with a gentle, warm smile spreading across their face",
        "The scene comes alive with subtle movements and natural lighting changes",
        "Gentle breeze brings the image to life with soft, natural movements",
        "The subject looks around with curiosity and wonder in their eyes",
        "Custom prompt (enter your own)",
        "No prompt (let AI decide the animation)"
    ]
    
    prompt_choice = get_user_choice("Choose animation prompt:", sample_prompts)
    
    if prompt_choice == len(sample_prompts) - 2:  # Custom prompt
        prompt = input("\nEnter your custom animation prompt: ").strip()
    elif prompt_choice == len(sample_prompts) - 1:  # No prompt
        prompt = None
    else:
        prompt = sample_prompts[prompt_choice]
    
    print(f"\n🎬 Generating video from image...")
    print(f"🖼️  Image: {image_path}")
    if prompt:
        print(f"📝 Animation prompt: {prompt}")
    else:
        print("📝 No specific prompt (AI will decide animation)")
    print("⏳ This may take 2-10 minutes...")
    
    try:
        if use_local:
            video_uri = generate_video_from_local_image(
                project_id=PROJECT_ID,
                image_filename=image_filename,
                output_bucket_path=OUTPUT_BUCKET_PATH,
                prompt=prompt
            )
        else:
            video_uri = generate_video_from_image(
                project_id=PROJECT_ID,
                image_path=image_path,
                output_bucket_path=OUTPUT_BUCKET_PATH,
                prompt=prompt
            )
        
        if video_uri:
            print(f"\n✅ Success! Video generated: {video_uri}")
            print("📁 Video also downloaded to ./result_folder/")
        else:
            print("\n❌ Video generation failed. Check the logs above for details.")
            
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")

def demo_model_comparison():
    """Demonstrate model comparison by generating the same prompt with both models."""
    print("\n" + "="*60)
    print("MODEL COMPARISON DEMO")
    print("="*60)
    
    comparison_prompts = [
        "A beautiful sunset over a calm ocean with gentle waves",
        "A bustling city street at night with neon lights and traffic",
        "A magical forest with glowing fireflies and mystical atmosphere",
        "Custom prompt (enter your own)"
    ]
    
    choice = get_user_choice("Choose a prompt for comparison:", comparison_prompts)
    
    if choice == len(comparison_prompts) - 1:  # Custom prompt
        prompt = input("\nEnter your custom prompt: ").strip()
        if not prompt:
            print("Empty prompt entered. Using default.")
            prompt = comparison_prompts[0]
    else:
        prompt = comparison_prompts[choice]
    
    print(f"\n🎬 Generating videos with both models for comparison...")
    print(f"📝 Prompt: {prompt}")
    print("⏳ This will take 4-20 minutes (both models)...")
    
    results = {}
    
    # Generate with Veo 2.0
    print(f"\n🔄 Generating with Veo 2.0...")
    try:
        video_uri_2 = generate_video_from_text(
            project_id=PROJECT_ID,
            prompt=prompt,
            output_bucket_path=OUTPUT_BUCKET_PATH,
            model_id="veo-2.0-generate-001"
        )
        results["Veo 2.0"] = video_uri_2
        if video_uri_2:
            print(f"✅ Veo 2.0 Success: {video_uri_2}")
        else:
            print("❌ Veo 2.0 Failed")
    except Exception as e:
        print(f"❌ Veo 2.0 Error: {e}")
        results["Veo 2.0"] = None
    
    # Generate with Veo 3.0
    print(f"\n🔄 Generating with Veo 3.0 Preview...")
    try:
        video_uri_3 = generate_video_with_veo3_preview(
            project_id=PROJECT_ID,
            prompt=prompt,
            output_bucket_path=OUTPUT_BUCKET_PATH
        )
        results["Veo 3.0"] = video_uri_3
        if video_uri_3:
            print(f"✅ Veo 3.0 Success: {video_uri_3}")
        else:
            print("❌ Veo 3.0 Failed")
    except Exception as e:
        print(f"❌ Veo 3.0 Error: {e}")
        results["Veo 3.0"] = None
    
    # Summary
    print(f"\n" + "="*60)
    print("COMPARISON RESULTS")
    print("="*60)
    print(f"Prompt: {prompt}")
    print()
    
    for model, uri in results.items():
        if uri:
            print(f"✅ {model}: {uri}")
        else:
            print(f"❌ {model}: Generation failed")
    
    print("\n📁 All generated videos are in ./result_folder/")

def show_configuration():
    """Show current configuration and allow updates."""
    print("\n" + "="*60)
    print("CURRENT CONFIGURATION")
    print("="*60)
    
    # Environment Variables
    print("Environment Variables (from .env file):")
    print(f"  GOOGLE_CLOUD_PROJECT: {PROJECT_ID}")
    print(f"  OUTPUT_BUCKET_PATH: {OUTPUT_BUCKET_PATH}")
    
    # Show if using defaults (dummy values)
    if PROJECT_ID == "your-project-id":
        print("  ⚠️  Using default project ID - update .env file with your actual project ID")
    if OUTPUT_BUCKET_PATH == "gs://your-bucket-name/veo_output/":
        print("  ⚠️  Using default bucket path - update .env file with your actual bucket")
    
    print(f"\nLocal Directories:")
    print(f"  Images Directory: {current_dir / 'images'}")
    print(f"  Results Directory: {current_dir / 'result_folder'}")
    
    # Check if directories exist
    images_dir = current_dir / "images"
    results_dir = current_dir / "result_folder"
    
    print(f"\nDirectory Status:")
    print(f"  Images folder exists: {'✅' if images_dir.exists() else '❌'}")
    print(f"  Results folder exists: {'✅' if results_dir.exists() else '❌'}")
    
    if images_dir.exists():
        image_files = [f for f in os.listdir(images_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        print(f"  Available images: {len(image_files)}")
        if image_files:
            print("    - " + "\n    - ".join(image_files))
    
    if results_dir.exists():
        video_files = [f for f in os.listdir(results_dir) 
                      if f.lower().endswith(('.mp4', '.mov', '.avi'))]
        print(f"  Generated videos: {len(video_files)}")
        if video_files:
            print("    - " + "\n    - ".join(video_files))
    
    print(f"\nConfiguration Help:")
    print(f"  📝 To update configuration, edit the .env file in this directory")
    print(f"  🔧 Run 'python fix_permissions.py' to fix Google Cloud permissions")
    print(f"  🧪 Run 'python test_veo.py' to test your configuration")

def main():
    """Main demo function with interactive menu."""
    print("🎬 Google Veo Video Generation Demo")
    print("=" * 60)
    print("This demo showcases the Google Veo video generation capabilities.")
    print("Make sure you have:")
    print("1. ✅ Google Cloud authentication set up")
    print("2. ✅ Project ID and bucket configured")
    print("3. ✅ Required permissions granted")
    print("4. ✅ Dependencies installed")
    
    while True:
        options = [
            "🎥 Text-to-Video Generation",
            "🖼️  Image-to-Video Generation", 
            "⚖️  Model Comparison (Veo 2.0 vs 3.0)",
            "⚙️  Show Configuration",
            "❌ Exit"
        ]
        
        choice = get_user_choice("Choose a demo option:", options)
        
        if choice == 0:
            demo_text_to_video()
        elif choice == 1:
            demo_image_to_video()
        elif choice == 2:
            demo_model_comparison()
        elif choice == 3:
            show_configuration()
        elif choice == 4:
            print("\n👋 Thanks for using the Google Veo Video Generation Demo!")
            break
        
        # Ask if user wants to continue
        if choice < 4:
            continue_choice = input("\n🔄 Would you like to try another demo? (y/n): ").lower().strip()
            if continue_choice not in ['y', 'yes']:
                print("\n👋 Thanks for using the Google Veo Video Generation Demo!")
                break

if __name__ == "__main__":
    main() 