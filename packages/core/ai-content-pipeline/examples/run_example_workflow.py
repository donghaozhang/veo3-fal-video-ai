#!/usr/bin/env python3
"""
Script to run example workflows demonstrating the complete image→prompt→video pipeline
"""

import sys
import os
from pathlib import Path

# Add the ai_content_pipeline to the Python path
pipeline_path = Path(__file__).parent.parent
sys.path.insert(0, str(pipeline_path))

from ai_content_pipeline.pipeline.manager import AIPipelineManager

def run_workflow_example(workflow_name: str, input_text: str):
    """Run a specific workflow example."""
    
    print(f"\n🎬 Running Workflow: {workflow_name}")
    print("=" * 60)
    print(f"📝 Input: {input_text}")
    print("-" * 40)
    
    # Initialize pipeline manager
    manager = AIPipelineManager(base_dir=str(Path(__file__).parent.parent))
    
    # Load workflow configuration
    config_path = Path(__file__).parent / f"{workflow_name}.yaml"
    
    if not config_path.exists():
        print(f"❌ Workflow config not found: {config_path}")
        return False
    
    try:
        # Create chain from configuration
        chain = manager.create_chain_from_config(str(config_path))
        
        # Estimate costs before execution
        cost_breakdown = manager.estimate_chain_cost(chain)
        print(f"💰 Estimated total cost: ${cost_breakdown['total_cost']:.3f}")
        
        # Show step breakdown
        for step_cost in cost_breakdown['step_costs']:
            print(f"   • {step_cost['step']} ({step_cost['model']}): ${step_cost['cost']:.3f}")
        
        print("\n🚀 Starting execution...")
        
        # Execute the chain
        result = manager.execute_chain(chain, input_text)
        
        # Display results
        if result.success:
            print(f"\n✅ Workflow completed successfully!")
            print(f"⏱️  Total time: {result.total_time:.1f}s")
            print(f"💰 Total cost: ${result.total_cost:.3f}")
            print(f"📊 Steps completed: {result.steps_completed}/{result.total_steps}")
            
            # Show final outputs
            print("\n📁 Final Outputs:")
            for step_name, output in result.outputs.items():
                if output.get('path'):
                    print(f"   • {step_name}: {output['path']}")
                if output.get('url'):
                    print(f"   • {step_name} (URL): {output['url']}")
                if output.get('text'):
                    preview = output['text'][:100] + "..." if len(output['text']) > 100 else output['text']
                    print(f"   • {step_name} (text): {preview}")
            
            return True
        else:
            print(f"\n❌ Workflow failed: {result.error}")
            print(f"📊 Steps completed: {result.steps_completed}/{result.total_steps}")
            return False
            
    except Exception as e:
        print(f"❌ Error running workflow: {str(e)}")
        return False

def main():
    """Run example workflows."""
    
    print("🎯 AI Content Pipeline - Example Workflows")
    print("=" * 60)
    
    # Define example workflows to run
    workflows = [
        {
            "name": "image_prompt_video_workflow",
            "input": "A majestic mountain landscape at sunrise with golden light illuminating snow-capped peaks",
            "description": "Image analysis → Prompt optimization → Video creation"
        },
        {
            "name": "text_to_video_with_smart_prompts", 
            "input": "A futuristic cityscape with flying cars and neon lights",
            "description": "Text to image → Smart prompts → Dramatic video"
        },
        {
            "name": "artistic_video_creation",
            "input": "Abstract geometric shapes floating in a dreamlike space with vibrant colors",
            "description": "Artistic image → Composition analysis → Creative video"
        },
        {
            "name": "realistic_documentary_style",
            "input": "A peaceful forest clearing with sunlight filtering through ancient trees",
            "description": "Photorealistic image → Natural prompts → Documentary video"
        }
    ]
    
    # Check if user wants to run a specific workflow
    if len(sys.argv) > 1:
        workflow_name = sys.argv[1]
        custom_input = sys.argv[2] if len(sys.argv) > 2 else None
        
        # Find the workflow
        selected_workflow = None
        for wf in workflows:
            if wf["name"] == workflow_name:
                selected_workflow = wf
                break
        
        if selected_workflow:
            input_text = custom_input or selected_workflow["input"]
            success = run_workflow_example(workflow_name, input_text)
            sys.exit(0 if success else 1)
        else:
            print(f"❌ Workflow '{workflow_name}' not found")
            print("Available workflows:")
            for wf in workflows:
                print(f"   • {wf['name']}: {wf['description']}")
            sys.exit(1)
    
    # Run all workflows
    print("🔄 Running all example workflows...")
    results = []
    
    for workflow in workflows:
        print(f"\n{'='*60}")
        success = run_workflow_example(workflow["name"], workflow["input"])
        results.append((workflow["name"], success))
        
        if not success:
            print(f"⚠️  Workflow {workflow['name']} failed - continuing with next workflow")
    
    # Final summary
    print(f"\n{'='*60}")
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"✅ Successful workflows: {successful}/{total}")
    
    for workflow_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   • {workflow_name}: {status}")
    
    if successful == total:
        print(f"\n🎉 All workflows completed successfully!")
    else:
        print(f"\n⚠️  {total - successful} workflow(s) failed")
    
    sys.exit(0 if successful == total else 1)

if __name__ == "__main__":
    main()