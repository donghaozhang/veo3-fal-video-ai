#!/usr/bin/env python3
"""
Quick test to debug the video-to-audio pipeline flow issue
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from ai_content_pipeline.pipeline.executor import ChainExecutor
from ai_content_pipeline.pipeline.chain import PipelineStep, StepType
from ai_content_pipeline.utils.file_manager import FileManager

def test_video_audio_flow():
    """Test the flow from image to video to audio."""
    
    # Use existing image URL from previous tests
    image_url = "https://v3.fal.media/files/zebra/hvvs04jBPxpFYM-wKImU4_8f16a3aaaf194e79b80898eb5045d65a.png"
    
    # Initialize executor
    file_manager = FileManager()
    executor = ChainExecutor(file_manager)
    
    # Create test chain config
    chain_config = {
        "output_dir": "output",
        "name": "test_video_audio"
    }
    
    print("🧪 Testing video generation step...")
    
    # Step 1: Image to Video
    video_step = PipelineStep(
        step_type=StepType.IMAGE_TO_VIDEO,
        model="hailuo",
        params={
            "duration": 6,
            "motion_level": "medium"
        }
    )
    
    video_result = executor._execute_image_to_video(
        step=video_step,
        image_path=image_url,  # This is actually a URL
        chain_config=chain_config
    )
    
    print(f"Video result: {video_result}")
    
    if not video_result.get("success"):
        print("❌ Video generation failed")
        return
        
    video_path = video_result.get("output_path")
    print(f"📹 Video path from step: {video_path}")
    
    if not video_path:
        print("❌ No video path returned")
        return
    
    print("\n🧪 Testing audio generation step...")
    
    # Step 2: Add Audio
    audio_step = PipelineStep(
        step_type=StepType.ADD_AUDIO,
        model="thinksound",
        params={
            "prompt": "add ambient nature sounds",
            "audio_style": "calm"
        }
    )
    
    audio_result = executor._execute_add_audio(
        step=audio_step,
        video_path=video_path,
        chain_config=chain_config
    )
    
    print(f"Audio result: {audio_result}")
    
    if audio_result.get("success"):
        print("✅ Full pipeline working!")
        final_path = audio_result.get("output_path")
        print(f"🎬 Final video with audio: {final_path}")
    else:
        print(f"❌ Audio generation failed: {audio_result.get('error')}")

if __name__ == "__main__":
    test_video_audio_flow()