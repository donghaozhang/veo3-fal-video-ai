#!/bin/bash

# AI Content Pipeline Quick Test Script
# Activate virtual environment and run basic commands

set -e  # Exit on error

# Activate virtual environment
source venv/bin/activate

echo "🚀 AI Content Pipeline Quick Test"
echo "================================="

# List all available models
echo "📋 Listing available models..."
ai-content-pipeline list-models

# Run pipeline from YAML config
echo -e "\n📄 Running pipeline from YAML config..."
ai-content-pipeline run-chain --config input/pipelines/tts_single_voice_test.yaml --no-confirm

# Run with parallel execution (2-3x speedup)
# echo -e "\n⚡ Running with parallel execution..."
# PIPELINE_PARALLEL_ENABLED=true ai-content-pipeline run-chain --config input/pipelines/tts_single_voice_test.yaml --no-confirm

# Generate single image
echo -e "\n🎨 Generating single image..."
ai-content-pipeline generate-image --text "A beautiful sunset" --model flux_dev
ai-content-pipeline generate-image --text "A beautiful supermodel in the rock" --model seedream_v3
ai-content-pipeline generate-image --text "A beautiful supermodel in the rock" --model imagen4

# Create video from text (text → image → video)
echo -e "\n🎬 Creating video from text..."
ai-content-pipeline create-video --text "A beautiful sunset"

echo -e "\n✅ All tests completed successfully!"