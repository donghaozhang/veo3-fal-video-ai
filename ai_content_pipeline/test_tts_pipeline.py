#!/usr/bin/env python3
"""
Test script for text-to-speech pipeline integration
"""

import sys
import os
import yaml
from pathlib import Path

# Add the ai_content_pipeline to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from ai_content_pipeline.pipeline.manager import AIPipelineManager
from ai_content_pipeline.pipeline.chain import ContentCreationChain, PipelineStep, StepType

def test_tts_pipeline():
    """Test the TTS pipeline integration."""
    
    print("🎤 Testing TTS Pipeline Integration")
    print("=" * 50)
    
    # Initialize pipeline manager
    manager = AIPipelineManager(base_dir=str(Path(__file__).parent))
    
    # Load the TTS workflow
    workflow_path = "input/tts_pipeline_test.yaml"
    
    print(f"📂 Loading workflow: {workflow_path}")
    
    try:
        # Load YAML configuration
        with open(workflow_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"📋 Config loaded: {config['name']}")
        
        # Create pipeline steps from config
        steps = []
        for step_config in config['steps']:
            step = PipelineStep(
                step_type=StepType(step_config['type']),
                model=step_config['model'],
                params=step_config.get('params', {})
            )
            steps.append(step)
        
        # Create content creation chain
        chain = ContentCreationChain(
            name=config['name'],
            steps=steps,
            config={
                "output_dir": config.get('output_dir', 'output'),
                "temp_dir": config.get('temp_dir', 'temp'),
                "cleanup_temp": config.get('cleanup_temp', True),
                "save_intermediates": config.get('save_intermediates', True)
            }
        )
        
        # Execute the TTS workflow
        input_text = config.get('prompt', "Welcome to our advanced AI content creation platform. This demonstration showcases our integrated text-to-speech capabilities with multiple voice options and customizable parameters for professional audio production.")
        
        result = manager.execute_chain(chain, input_text)
        
        if result.success:
            print(f"\n✅ TTS Pipeline executed successfully!")
            print(f"📊 Steps completed: {result.steps_completed}/{result.total_steps}")
            print(f"💰 Total cost: ${result.total_cost:.3f}")
            print(f"⏱️  Total time: {result.total_time:.1f}s")
            
            print("\n📁 Generated outputs:")
            for output_name, output_info in result.outputs.items():
                print(f"  • {output_name}: {output_info}")
                
        else:
            print(f"\n❌ TTS Pipeline failed")
            print(f"📊 Steps completed: {result.steps_completed}/{result.total_steps}")
            if hasattr(result, 'error'):
                print(f"🚨 Error: {result.error}")
                
    except Exception as e:
        print(f"\n❌ Error running TTS pipeline: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tts_pipeline()