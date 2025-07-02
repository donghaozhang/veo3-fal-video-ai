#!/usr/bin/env python3
"""
Quick test to verify the audio step works with an existing video
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from ai_content_pipeline.pipeline.executor import ChainExecutor
from ai_content_pipeline.pipeline.chain import PipelineStep, StepType
from ai_content_pipeline.utils.file_manager import FileManager

def test_audio_step():
    """Test the audio step with an existing video."""
    
    # Use existing video file
    video_path = "output/generated_95f810c6.mp4"
    
    # Check if file exists
    if not Path(video_path).exists():
        print(f"❌ Video file not found: {video_path}")
        return
    
    print(f"✅ Found video file: {video_path}")
    
    # Initialize executor
    file_manager = FileManager()
    executor = ChainExecutor(file_manager)
    
    # Create test chain config
    chain_config = {
        "output_dir": "output",
        "name": "test_audio"
    }
    
    print("🧪 Testing audio generation step...")
    
    # Create audio step
    audio_step = PipelineStep(
        step_type=StepType.ADD_AUDIO,
        model="thinksound",
        params={
            "prompt": "add ambient nature sounds and gentle music",
            "audio_style": "calm"
        }
    )
    
    # Execute audio step
    audio_result = executor._execute_add_audio(
        step=audio_step,
        video_path=video_path,
        chain_config=chain_config
    )
    
    print(f"Audio result: {audio_result}")
    
    if audio_result.get("success"):
        print("✅ Audio step working!")
        final_path = audio_result.get("output_path")
        print(f"🎬 Final video with audio: {final_path}")
    else:
        print(f"❌ Audio generation failed: {audio_result.get('error')}")

if __name__ == "__main__":
    test_audio_step()