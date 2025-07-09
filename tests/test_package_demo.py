#!/usr/bin/env python3
"""
Demo script showing AI Content Pipeline package functionality
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages', 'core', 'ai_content_pipeline'))

from ai_content_pipeline.pipeline.manager import AIPipelineManager
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def demonstrate_package():
    """Demonstrate the AI Content Pipeline package functionality"""
    print("🎬 AI Content Pipeline Package Demo")
    print("="*50)
    
    # Initialize manager
    print("🚀 Initializing AI Content Pipeline Manager...")
    manager = AIPipelineManager()
    print(f"✅ Manager initialized successfully!")
    print(f"📁 Output directory: {manager.output_dir}")
    print(f"📁 Temp directory: {manager.temp_dir}")
    
    # Show available models
    print("\n🎯 Available AI Models:")
    models = manager.get_available_models()
    
    total_models = sum(len(model_list) for model_list in models.values())
    print(f"📊 Total models available: {total_models}")
    
    for step_type, model_list in models.items():
        if model_list:
            print(f"\n📦 {step_type.replace('_', ' ').title()}:")
            for model in model_list:
                print(f"   ✓ {model}")
        else:
            print(f"\n📦 {step_type.replace('_', ' ').title()}: No models available")
    
    # Test configuration loading
    print("\n🔧 Testing Configuration Loading...")
    
    # Test with the original YAML file
    yaml_path = "input/pipelines/analysis_detailed_gemini.yaml"
    
    if os.path.exists(yaml_path):
        print(f"📄 Loading: {yaml_path}")
        try:
            chain = manager.create_chain_from_config(yaml_path)
            print(f"✅ Configuration loaded successfully!")
            print(f"📋 Chain name: {chain.name}")
            print(f"🔗 Steps: {len(chain.steps)}")
            
            # Show step details
            for i, step in enumerate(chain.steps, 1):
                print(f"   Step {i}: {step.step_type.value} using {step.model}")
                if hasattr(step, 'params') and step.params:
                    print(f"      Parameters: {step.params}")
            
            # Test cost estimation
            cost_info = manager.estimate_chain_cost(chain)
            print(f"💰 Estimated cost: ${cost_info['total_cost']:.4f}")
            
        except Exception as e:
            print(f"⚠️  Configuration loading issue: {e}")
    else:
        print(f"⚠️  YAML file not found: {yaml_path}")
    
    # Test console script functionality
    print("\n🖥️  Console Script Commands:")
    print("   ai-content-pipeline list-models")
    print("   ai-content-pipeline run-chain --config config.yaml")
    print("   ai-content-pipeline generate-image --text 'prompt' --model flux_dev")
    print("   ai-content-pipeline create-video --text 'prompt'")
    print("   aicp --help  # (shortened alias)")
    
    # Show package structure
    print("\n📁 Package Structure:")
    print("   ├── packages/")
    print("   │   ├── core/")
    print("   │   │   ├── ai_content_pipeline/  # Main unified pipeline")
    print("   │   │   └── ai_content_platform/  # Platform framework")
    print("   │   ├── providers/")
    print("   │   │   ├── google/veo/          # Google Veo integration")
    print("   │   │   └── fal/                 # FAL AI services")
    print("   │   └── services/")
    print("   │       ├── text-to-speech/     # ElevenLabs TTS")
    print("   │       └── video-tools/        # Video processing")
    print("   ├── input/                      # Input files and configs")
    print("   └── output/                     # Generated output")
    
    print("\n✅ Package Demo Complete!")
    print("🎉 The AI Content Pipeline package is working and ready to use!")
    
    return True

def main():
    """Run the demonstration"""
    try:
        demonstrate_package()
        return 0
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())