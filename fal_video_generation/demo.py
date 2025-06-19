#!/usr/bin/env python3
"""
Interactive demo script for FAL AI Video Generation
Supports both MiniMax Hailuo-02 and Kling Video 2.1 models
Cost-conscious with user confirmation prompts
"""

import os
import sys
from fal_video_generator import FALVideoGenerator

def show_cost_warning():
    """Display cost warning for video generation"""
    print("\n💰 COST WARNING:")
    print("   Each video generation costs money (~$0.02-0.05 per video)")
    print("   This demo will generate real videos that will be charged to your account")
    print("   Make sure you understand the costs before proceeding")
    print()

def get_user_choice(prompt, options):
    """Get user choice from a list of options"""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")

def confirm_generation(model_name, estimated_cost="~$0.02-0.05"):
    """Ask user to confirm video generation with cost information"""
    print(f"\n⚠️  About to generate video with {model_name}")
    print(f"💰 Estimated cost: {estimated_cost}")
    response = input("Continue with video generation? (y/N): ")
    return response.lower() == 'y'

def main():
    """
    Run an interactive demo of FAL AI video generation
    """
    print("🎬 FAL AI Video Generation Demo")
    print("Supports MiniMax Hailuo-02 and Kling Video 2.1")
    print("=" * 50)
    
    # Show cost warning upfront
    show_cost_warning()
    
    try:
        # Check if API key is available
        api_key = os.getenv('FAL_KEY')
        if not api_key:
            print("❌ Error: FAL_KEY environment variable not set!")
            print("Please set your FAL AI API key in the .env file")
            return
        
        # Initialize generator
        print("🔧 Initializing FAL Video Generator...")
        generator = FALVideoGenerator()
        print("✅ Generator initialized successfully!")
        
        # Model selection with cost info
        models = [
            "MiniMax Hailuo-02 (768p, 6-10s) - ~$0.02-0.05 per video", 
            "Kling Video 2.1 (High quality, 5-10s) - ~$0.02-0.05 per video"
        ]
        model_choice = get_user_choice("\n🎯 Select a model:", models)
        
        if model_choice == 0:
            model_name = "hailuo"
            model_display = "MiniMax Hailuo-02"
            print("\n📋 Selected: MiniMax Hailuo-02")
            print("   • Resolution: 768p")
            print("   • Duration: 6 or 10 seconds")
            print("   • Features: Prompt optimizer")
            print("   • Cost: ~$0.02-0.05 per video")
        else:
            model_name = "kling"
            model_display = "Kling Video 2.1"
            print("\n📋 Selected: Kling Video 2.1")
            print("   • Resolution: High quality")
            print("   • Duration: 5 or 10 seconds")
            print("   • Features: CFG scale, negative prompts")
            print("   • Cost: ~$0.02-0.05 per video")
        
        # Demo options with cost indicators
        demo_options = [
            "Generate from online image (~$0.02-0.05)",
            "Generate from local image (~$0.02-0.05)",
            "Compare both models with same input (~$0.04-0.10) ⚠️ EXPENSIVE",
            "Custom input (enter your own prompt and image) (~$0.02-0.05)"
        ]
        
        demo_choice = get_user_choice("\n🎯 Select demo type:", demo_options)
        
        if demo_choice == 0:
            # Demo 1: Generate from online image
            print("\n🎯 Demo: Generate video from online image")
            print("-" * 40)
            
            if not confirm_generation(model_display):
                print("❌ Demo cancelled by user")
                return
            
            if model_name == "kling":
                result = generator.generate_video_with_kling(
                    prompt="As the sun dips below the horizon, painting the sky in fiery hues of orange and purple, powerful waves relentlessly crash against jagged, dark rocks",
                    image_url="https://v3.fal.media/files/panda/W-_J46zuJDQnUhqkKm9Iv_image.webp",
                    duration="5",
                    output_folder="demo_output"
                )
            else:
                result = generator.generate_video_with_hailuo(
                    prompt="A man walks into a winter cave with a polar bear, cinematic lighting, dramatic atmosphere",
                    image_url="https://storage.googleapis.com/falserverless/model_tests/minimax/1749891352437225630-389852416840474630_1749891352.png",
                    duration="6",
                    output_folder="demo_output"
                )
            
            if result:
                print("🎉 Success! Video generated:")
                print(f"   📹 Video URL: {result['video']['url']}")
                print(f"   💾 File size: {result['video']['file_size']} bytes")
                if 'local_path' in result:
                    print(f"   📁 Local path: {result['local_path']}")
            else:
                print("❌ Failed to generate video from online image")
        
        elif demo_choice == 1:
            # Demo 2: Generate from local image
            local_image_path = "../images/smiling_woman.jpg"
            if os.path.exists(local_image_path):
                print("\n🎯 Demo: Generate video from local image")
                print("-" * 40)
                
                if not confirm_generation(model_display):
                    print("❌ Demo cancelled by user")
                    return
                
                result = generator.generate_video_from_local_image(
                    prompt="A smiling woman in a beautiful garden, gentle breeze moving her hair, warm sunlight",
                    image_path=local_image_path,
                    duration="6" if model_name == "hailuo" else "5",
                    output_folder="demo_output",
                    model=model_name
                )
                
                if result:
                    print("🎉 Success! Video generated from local image:")
                    print(f"   📹 Video URL: {result['video']['url']}")
                    print(f"   💾 File size: {result['video']['file_size']} bytes")
                    if 'local_path' in result:
                        print(f"   📁 Local path: {result['local_path']}")
                else:
                    print("❌ Failed to generate video from local image")
            else:
                print(f"\n⚠️  Local image not found at {local_image_path}")
                print("Please place an image at that location or choose a different demo")
        
        elif demo_choice == 2:
            # Demo 3: Compare both models - EXPENSIVE!
            print("\n🎯 Demo: Compare Hailuo vs Kling with same input")
            print("💰 WARNING: This will generate 2 videos (~$0.04-0.10 total cost)")
            print("-" * 40)
            
            if not confirm_generation("BOTH models", "~$0.04-0.10 (2 videos)"):
                print("❌ Comparison demo cancelled by user")
                return
            
            prompt = "A peaceful landscape with gentle movement, cinematic quality"
            image_url = "https://picsum.photos/512/512"
            
            print("🔄 Generating with MiniMax Hailuo-02...")
            result_hailuo = generator.generate_video_with_hailuo(
                prompt=prompt,
                image_url=image_url,
                duration="6",
                output_folder="demo_output"
            )
            
            print("\n🔄 Generating with Kling Video 2.1...")
            result_kling = generator.generate_video_with_kling(
                prompt=prompt,
                image_url=image_url,
                duration="5",
                output_folder="demo_output"
            )
            
            print("\n📊 Comparison Results:")
            if result_hailuo:
                print(f"   🟢 Hailuo: {result_hailuo['video']['url']}")
                print(f"      Size: {result_hailuo['video']['file_size']} bytes")
            else:
                print("   🔴 Hailuo: Failed")
            
            if result_kling:
                print(f"   🟢 Kling: {result_kling['video']['url']}")
                print(f"      Size: {result_kling['video']['file_size']} bytes")
            else:
                print("   🔴 Kling: Failed")
        
        elif demo_choice == 3:
            # Demo 4: Custom input
            print("\n🎯 Demo: Custom input")
            print("-" * 40)
            
            custom_prompt = input("Enter your prompt: ")
            custom_image_url = input("Enter image URL (or press Enter for default): ")
            
            if not custom_image_url:
                custom_image_url = "https://picsum.photos/512/512"
            
            duration_options = ["5", "6", "10"]
            duration_choice = get_user_choice("Select duration:", [f"{d} seconds" for d in duration_options])
            duration = duration_options[duration_choice]
            
            if not confirm_generation(model_display):
                print("❌ Custom demo cancelled by user")
                return
            
            if model_name == "kling":
                result = generator.generate_video_with_kling(
                    prompt=custom_prompt,
                    image_url=custom_image_url,
                    duration=duration,
                    output_folder="demo_output"
                )
            else:
                result = generator.generate_video_with_hailuo(
                    prompt=custom_prompt,
                    image_url=custom_image_url,
                    duration=duration,
                    output_folder="demo_output"
                )
            
            if result:
                print("🎉 Success! Custom video generated:")
                print(f"   📹 Video URL: {result['video']['url']}")
                print(f"   💾 File size: {result['video']['file_size']} bytes")
                if 'local_path' in result:
                    print(f"   📁 Local path: {result['local_path']}")
            else:
                print("❌ Failed to generate custom video")
        
        print("\n🎉 Demo completed!")
        print("💡 Check the 'demo_output' folder for downloaded videos")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        print("💡 Check your API key and internet connection")

if __name__ == "__main__":
    main() 