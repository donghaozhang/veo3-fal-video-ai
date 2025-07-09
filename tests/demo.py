#!/usr/bin/env python3
"""
Interactive demo script for the AI Content Pipeline package.
Showcases package features and provides guided examples.
"""
import sys
import os
import json
import tempfile
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def show_header():
    """Display demo header"""
    print("🎬 AI Content Pipeline Package - Interactive Demo")
    print("="*60)
    print("This demo showcases the AI Content Pipeline package capabilities.")
    print("Follow along to see how to use the package features!")
    print()

def demo_initialization():
    """Demo: Package initialization"""
    print("🚀 DEMO 1: Package Initialization")
    print("-" * 40)
    
    try:
        # Import and initialize
        from packages.core.ai_content_pipeline.ai_content_pipeline.pipeline.manager import AIPipelineManager
        
        print("📦 Initializing AI Content Pipeline Manager...")
        manager = AIPipelineManager()
        
        print("✅ Manager initialized successfully!")
        print(f"📁 Output directory: {manager.output_dir}")
        print(f"📁 Temp directory: {manager.temp_dir}")
        
        return manager
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return None

def demo_model_showcase(manager):
    """Demo: Available models showcase"""
    print("\n🎯 DEMO 2: Available AI Models")
    print("-" * 40)
    
    try:
        models = manager.get_available_models()
        total_models = sum(len(model_list) for model_list in models.values())
        
        print(f"📊 Total models available: {total_models}")
        print("\n🔍 Model Categories:")
        
        for step_type, model_list in models.items():
            if model_list:
                print(f"\n📦 {step_type.replace('_', ' ').title()} ({len(model_list)} models):")
                for model in model_list:
                    print(f"   ✓ {model}")
            else:
                print(f"\n📦 {step_type.replace('_', ' ').title()}: No models configured")
        
        return models
        
    except Exception as e:
        print(f"❌ Model showcase failed: {e}")
        return {}

def demo_configuration_examples(manager):
    """Demo: Configuration examples"""
    print("\n🔧 DEMO 3: Configuration Examples")
    print("-" * 40)
    
    examples = [
        {
            "name": "Simple Text-to-Speech",
            "config": {
                "name": "simple_tts",
                "description": "Convert text to speech",
                "steps": [
                    {
                        "type": "text_to_speech",
                        "model": "elevenlabs",
                        "params": {
                            "voice": "Rachel",
                            "text": "Hello from the AI Content Pipeline!"
                        }
                    }
                ]
            }
        },
        {
            "name": "Text-to-Image Generation",
            "config": {
                "name": "text_to_image",
                "description": "Generate image from text",
                "steps": [
                    {
                        "type": "text_to_image",
                        "model": "flux_schnell",
                        "params": {
                            "prompt": "A beautiful sunset over mountains",
                            "num_images": 1
                        }
                    }
                ]
            }
        },
        {
            "name": "Multi-step Pipeline",
            "config": {
                "name": "multi_step",
                "description": "Multiple AI operations in sequence",
                "steps": [
                    {
                        "type": "prompt_generation",
                        "model": "openrouter_video_cinematic",
                        "params": {
                            "base_prompt": "A robot in a futuristic city",
                            "style": "cinematic"
                        }
                    },
                    {
                        "type": "text_to_image",
                        "model": "flux_dev",
                        "params": {
                            "prompt": "{{step_1.output}}",
                            "num_images": 2
                        }
                    }
                ]
            }
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n📋 Example {i}: {example['name']}")
        print(f"   Description: {example['config']['description']}")
        print(f"   Steps: {len(example['config']['steps'])}")
        
        # Show step details
        for j, step in enumerate(example['config']['steps'], 1):
            print(f"   Step {j}: {step['type']} using {step['model']}")
        
        # Test configuration loading
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(example['config'], f)
                temp_path = f.name
            
            chain = manager.create_chain_from_config(temp_path)
            cost_info = manager.estimate_chain_cost(chain)
            print(f"   💰 Estimated cost: ${cost_info['total_cost']:.4f}")
            
            os.unlink(temp_path)
            
        except Exception as e:
            print(f"   ⚠️  Configuration test failed: {e}")

def demo_yaml_loading(manager):
    """Demo: YAML configuration loading"""
    print("\n📄 DEMO 4: YAML Configuration Loading")
    print("-" * 40)
    
    # Look for existing YAML files
    yaml_search_paths = [
        "input/pipelines/",
        "input/",
        ".",
        "examples/"
    ]
    
    yaml_files = []
    for search_path in yaml_search_paths:
        if os.path.exists(search_path):
            for file in os.listdir(search_path):
                if file.endswith('.yaml') or file.endswith('.yml'):
                    yaml_files.append(os.path.join(search_path, file))
    
    if yaml_files:
        print(f"📂 Found {len(yaml_files)} YAML configuration files:")
        for yaml_file in yaml_files[:5]:  # Show first 5
            print(f"   - {yaml_file}")
        
        # Try to load the first one
        try:
            test_file = yaml_files[0]
            print(f"\n📋 Loading example: {test_file}")
            
            chain = manager.create_chain_from_config(test_file)
            print(f"✅ Loaded '{chain.name}' with {len(chain.steps)} steps")
            
            # Show step overview
            for i, step in enumerate(chain.steps[:3], 1):
                print(f"   Step {i}: {step.step_type.value} ({step.model})")
            if len(chain.steps) > 3:
                print(f"   ... and {len(chain.steps) - 3} more steps")
            
        except Exception as e:
            print(f"⚠️  YAML loading demo failed: {e}")
    else:
        print("⚠️  No YAML files found for demo")
        print("💡 You can create YAML configs like this:")
        print("""
   Example pipeline.yaml:
   
   name: my_pipeline
   description: Example pipeline
   steps:
     - type: text_to_speech
       model: elevenlabs
       params:
         voice: Rachel
         text: "Hello world"
        """)

def demo_parallel_execution():
    """Demo: Parallel execution explanation"""
    print("\n⚡ DEMO 5: Parallel Execution")
    print("-" * 40)
    
    print("🚀 The AI Content Pipeline supports parallel execution!")
    print("   This can speed up pipelines by 2-3x when processing multiple items.")
    print()
    print("🔧 To enable parallel execution:")
    print("   export PIPELINE_PARALLEL_ENABLED=true")
    print("   # or")
    print("   PIPELINE_PARALLEL_ENABLED=true ai-content-pipeline run-chain --config config.yaml")
    print()
    print("📋 Example parallel configuration:")
    print("""
   steps:
     - type: parallel_group
       steps:
         - type: text_to_image
           model: flux_schnell
           params:
             prompt: "A cat"
         - type: text_to_image
           model: flux_schnell
           params:
             prompt: "A dog"
         - type: text_to_image
           model: flux_schnell
           params:
             prompt: "A bird"
    """)

def demo_console_commands():
    """Demo: Console command examples"""
    print("\n🖥️  DEMO 6: Console Commands")
    print("-" * 40)
    
    print("🔧 Available console commands:")
    print()
    
    commands = [
        ("ai-content-pipeline --help", "Show help and all available commands"),
        ("ai-content-pipeline list-models", "List all available AI models"),
        ("ai-content-pipeline run-chain --config pipeline.yaml", "Run a pipeline from YAML config"),
        ("ai-content-pipeline generate-image --text 'prompt' --model flux_dev", "Generate single image"),
        ("ai-content-pipeline create-speech --text 'Hello' --voice Rachel", "Create speech audio"),
        ("aicp --help", "Shortened alias for ai-content-pipeline"),
    ]
    
    for cmd, description in commands:
        print(f"   {cmd}")
        print(f"   └─ {description}")
        print()

def demo_package_structure():
    """Demo: Package structure explanation"""
    print("\n📁 DEMO 7: Package Structure")
    print("-" * 40)
    
    print("🏗️  The AI Content Pipeline is organized as follows:")
    print()
    print("📦 packages/")
    print("├── core/")
    print("│   ├── ai_content_pipeline/     # Main unified pipeline")
    print("│   │   ├── pipeline/            # Pipeline management")
    print("│   │   ├── models/              # AI model integrations")
    print("│   │   └── utils/               # Utilities and helpers")
    print("│   └── ai_content_platform/     # Platform framework")
    print("├── providers/")
    print("│   ├── google/veo/              # Google Veo integration")
    print("│   └── fal/                     # FAL AI services")
    print("│       ├── text-to-image/       # Image generation")
    print("│       ├── image-to-image/      # Image transformation")
    print("│       ├── text-to-video/       # Video generation")
    print("│       └── avatar-generation/   # Avatar creation")
    print("└── services/")
    print("    ├── text-to-speech/          # ElevenLabs TTS")
    print("    └── video-tools/             # Video processing")
    print()
    print("📂 Project directories:")
    print("├── input/                       # Input files and configs")
    print("├── output/                      # Generated output")
    print("└── tests/                       # Test suites")

def demo_cost_management():
    """Demo: Cost management features"""
    print("\n💰 DEMO 8: Cost Management")
    print("-" * 40)
    
    print("💡 The AI Content Pipeline includes cost estimation features:")
    print()
    print("🔍 Cost estimation is available for:")
    print("   ✓ Text-to-Speech (ElevenLabs)")
    print("   ✓ Text-to-Image (FAL models)")
    print("   ✓ Text-to-Video (FAL models)")
    print("   ✓ Image-to-Image (FAL models)")
    print("   ✓ Avatar generation (FAL models)")
    print()
    print("📊 Cost estimates are shown:")
    print("   - Before pipeline execution")
    print("   - Per-step breakdown")
    print("   - Total pipeline cost")
    print()
    print("⚠️  Always run cost estimation before executing pipelines!")

def interactive_demo():
    """Run interactive demonstration"""
    show_header()
    
    print("🎮 Interactive Demo Mode")
    print("Press Enter to continue through each demo, or 'q' to quit...")
    
    demos = [
        ("Package Initialization", demo_initialization),
        ("Available Models", demo_model_showcase),
        ("Configuration Examples", demo_configuration_examples),
        ("YAML Loading", demo_yaml_loading),
        ("Parallel Execution", demo_parallel_execution),
        ("Console Commands", demo_console_commands),
        ("Package Structure", demo_package_structure),
        ("Cost Management", demo_cost_management),
    ]
    
    manager = None
    models = {}
    
    for i, (title, demo_func) in enumerate(demos, 1):
        print(f"\n{'='*60}")
        print(f"Demo {i}/{len(demos)}: {title}")
        print(f"{'='*60}")
        
        response = input(f"Ready to see '{title}' demo? (Enter to continue, 'q' to quit): ").strip().lower()
        if response == 'q':
            print("👋 Demo ended by user. Thanks for exploring!")
            break
        
        try:
            if title == "Package Initialization":
                manager = demo_func()
            elif title == "Available Models" and manager:
                models = demo_func(manager)
            elif title == "Configuration Examples" and manager:
                demo_func(manager)
            elif title == "YAML Loading" and manager:
                demo_func(manager)
            else:
                demo_func()
                
        except Exception as e:
            print(f"❌ Demo section failed: {e}")
            continue
    
    print(f"\n{'='*60}")
    print("🎉 Demo Complete!")
    print(f"{'='*60}")
    print("Thank you for exploring the AI Content Pipeline!")
    print()
    print("🚀 Ready to get started? Try these commands:")
    print("   ai-content-pipeline --help")
    print("   ai-content-pipeline list-models")
    print("   ai-content-pipeline run-chain --config your_pipeline.yaml")
    print()
    print("📚 For more information, check the documentation and examples.")

def main():
    """Main demo function"""
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_demo()
    else:
        # Non-interactive mode - run all demos
        show_header()
        
        print("🎬 Running full demonstration...")
        manager = demo_initialization()
        
        if manager:
            models = demo_model_showcase(manager)
            demo_configuration_examples(manager)
            demo_yaml_loading(manager)
        
        demo_parallel_execution()
        demo_console_commands()
        demo_package_structure()
        demo_cost_management()
        
        print(f"\n{'='*60}")
        print("🎉 Full Demo Complete!")
        print(f"{'='*60}")
        print("💡 Run with --interactive for step-by-step exploration")

if __name__ == "__main__":
    main()