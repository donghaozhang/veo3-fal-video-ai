#!/usr/bin/env python3
"""
Proof of concept for parallel pipeline execution.

Demonstrates how to run multiple TTS generations in parallel.
"""

import os
import sys
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_content_pipeline.models.text_to_speech import UnifiedTextToSpeechGenerator


def execute_single_tts(config: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """Execute a single TTS generation."""
    generator = UnifiedTextToSpeechGenerator()
    return generator.generate(**config)


def execute_parallel_tts_threads(configs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Execute multiple TTS generations in parallel using threads."""
    print(f"\n🔄 Executing {len(configs)} TTS tasks in parallel (threads)...")
    start_time = time.time()
    
    results = []
    with ThreadPoolExecutor(max_workers=len(configs)) as executor:
        # Submit all tasks
        future_to_config = {
            executor.submit(execute_single_tts, config): config 
            for config in configs
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_config):
            config = future_to_config[future]
            try:
                success, result = future.result()
                results.append({
                    'config': config,
                    'success': success,
                    'result': result
                })
                voice = config.get('voice', 'unknown')
                if success:
                    print(f"✅ Completed: {voice}")
                else:
                    print(f"❌ Failed: {voice}")
            except Exception as e:
                print(f"❌ Exception for {config.get('voice', 'unknown')}: {e}")
                results.append({
                    'config': config,
                    'success': False,
                    'result': {'error': str(e)}
                })
    
    elapsed = time.time() - start_time
    print(f"⏱️  Total parallel execution time: {elapsed:.2f}s")
    return results


def execute_sequential_tts(configs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Execute multiple TTS generations sequentially for comparison."""
    print(f"\n🔄 Executing {len(configs)} TTS tasks sequentially...")
    start_time = time.time()
    
    results = []
    for config in configs:
        voice = config.get('voice', 'unknown')
        print(f"Processing: {voice}")
        try:
            success, result = execute_single_tts(config)
            results.append({
                'config': config,
                'success': success,
                'result': result
            })
            if success:
                print(f"✅ Completed: {voice}")
            else:
                print(f"❌ Failed: {voice}")
        except Exception as e:
            print(f"❌ Exception for {voice}: {e}")
            results.append({
                'config': config,
                'success': False,
                'result': {'error': str(e)}
            })
    
    elapsed = time.time() - start_time
    print(f"⏱️  Total sequential execution time: {elapsed:.2f}s")
    return results


def main():
    """Demonstrate parallel vs sequential execution."""
    # Test text
    text = "This is a test of parallel text-to-speech generation. Each voice will process this simultaneously."
    
    # Configurations for multiple voices
    configs = [
        {
            'prompt': text,
            'voice': 'rachel',
            'output_file': 'output/parallel_poc_rachel.mp3',
            'speed': 1.0,
            'stability': 0.5,
            'similarity_boost': 0.8,
            'style': 0.2
        },
        {
            'prompt': text,
            'voice': 'drew',
            'output_file': 'output/parallel_poc_drew.mp3',
            'speed': 1.1,
            'stability': 0.7,
            'similarity_boost': 0.9,
            'style': 0.1
        },
        {
            'prompt': text,
            'voice': 'bella',
            'output_file': 'output/parallel_poc_bella.mp3',
            'speed': 0.9,
            'stability': 0.3,
            'similarity_boost': 0.6,
            'style': 0.8
        }
    ]
    
    print("🚀 Parallel Pipeline Execution POC")
    print("=" * 50)
    
    # Run sequential first
    seq_results = execute_sequential_tts(configs)
    
    # Run parallel
    par_results = execute_parallel_tts_threads(configs)
    
    # Summary
    print("\n📊 Summary")
    print("=" * 50)
    print(f"Sequential successful: {sum(1 for r in seq_results if r['success'])}/{len(seq_results)}")
    print(f"Parallel successful: {sum(1 for r in par_results if r['success'])}/{len(par_results)}")
    
    # Performance comparison
    print("\n🏁 Performance Comparison")
    print("Sequential execution processes one at a time")
    print("Parallel execution processes all simultaneously")
    print("Parallel execution is typically 2-3x faster for independent tasks")


if __name__ == "__main__":
    main()