#!/usr/bin/env python3
"""
FAL AI Text-to-Image MCP Server

A Model Context Protocol (MCP) server that provides Claude and other AI assistants 
with access to FAL AI text-to-image generation capabilities.

Features:
- Cost-conscious design with cost warnings
- Support for all four models (imagen4, seedream, flux_schnell, flux_dev)
- Batch processing capabilities
- Rich response formatting with metadata
- Error handling and validation
- Resource support for generated images
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

# MCP imports
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource,
    CallToolRequest, CallToolResult, ListResourcesRequest, ListResourcesResult,
    ListToolsRequest, ListToolsResult, ReadResourceRequest, ReadResourceResult
)
import mcp.types as types

# Local imports
from fal_text_to_image_generator import FALTextToImageGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fal-text-to-image-mcp")

# Initialize the MCP server
server = Server("fal-text-to-image")

# Global generator instance
generator = None

# Model information
MODELS = {
    "imagen4": {
        "name": "Imagen4",
        "endpoint": "fal-ai/google/imagen4/text-to-image",
        "description": "Google's high-quality model with excellent realism",
        "resolution": "High-quality (1024x1024 default)",
        "speed": "6-8 seconds",
        "cost": 0.015,
        "best_for": "Photorealistic content, portraits, professional images"
    },
    "seedream": {
        "name": "Seedream",
        "endpoint": "fal-ai/seedream/text-to-image",
        "description": "Artistic and creative generation with unique style",
        "resolution": "Artistic quality (varies)",
        "speed": "9-15 seconds",
        "cost": 0.015,
        "best_for": "Creative and artistic content, unique aesthetics"
    },
    "flux_schnell": {
        "name": "FLUX Schnell",
        "endpoint": "fal-ai/flux/schnell",
        "description": "Ultra-fast generation (1-2 seconds)",
        "resolution": "Good quality (1024x1024 default)",
        "speed": "1-2 seconds",
        "cost": 0.015,
        "best_for": "Fast iterations, concept development, testing"
    },
    "flux_dev": {
        "name": "FLUX Dev",
        "endpoint": "fal-ai/flux/dev",
        "description": "Balanced speed and quality",
        "resolution": "High quality (1024x1024 default)",
        "speed": "2-3 seconds",
        "cost": 0.015,
        "best_for": "Production content, balanced quality and speed"
    }
}

def format_cost_warning(estimated_cost: float, num_images: int = 1) -> str:
    """Format cost warning message."""
    return (
        f"💰 **COST WARNING**: This will generate {num_images} image(s) "
        f"and cost approximately ${estimated_cost:.3f}. "
        f"This will charge your FAL AI account."
    )

def format_model_info(model_key: str) -> str:
    """Format detailed model information."""
    if model_key not in MODELS:
        return f"Unknown model: {model_key}"
    
    model = MODELS[model_key]
    return (
        f"**{model['name']}** ({model_key})\n"
        f"- Endpoint: {model['endpoint']}\n"
        f"- Description: {model['description']}\n"
        f"- Resolution: {model['resolution']}\n"
        f"- Speed: {model['speed']}\n"
        f"- Cost: ${model['cost']:.3f} per image\n"
        f"- Best for: {model['best_for']}"
    )

def format_generation_result(result: Dict[str, Any]) -> str:
    """Format generation result for display."""
    if not result.get('success', False):
        return f"❌ Generation failed: {result.get('error', 'Unknown error')}"
    
    model = result.get('model', 'unknown')
    time_taken = result.get('generation_time', 0)
    cost = result.get('cost_estimate', 0.015)
    
    output = [
        f"✅ **{MODELS.get(model, {}).get('name', model)} Generation Successful**",
        f"- Time: {time_taken:.2f} seconds",
        f"- Cost: ${cost:.3f}",
        f"- Image URL: {result.get('image_url', 'Not available')}",
    ]
    
    if result.get('local_path'):
        output.append(f"- Local path: {result['local_path']}")
    
    return "\n".join(output)

def format_batch_summary(results: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
    """Format batch generation summary."""
    total = summary.get('total_images', 0)
    successful = summary.get('successful', 0)
    failed = summary.get('failed', 0)
    total_time = summary.get('total_time', 0)
    total_cost = summary.get('total_cost', 0)
    success_rate = summary.get('success_rate', 0)
    
    output = [
        f"📊 **Batch Generation Summary**",
        f"- Total images: {total}",
        f"- Successful: {successful}",
        f"- Failed: {failed}",
        f"- Success rate: {success_rate:.1f}%",
        f"- Total time: {total_time:.2f} seconds",
        f"- Total cost: ${total_cost:.3f}",
        "",
        "**Individual Results:**"
    ]
    
    for i, result in enumerate(results, 1):
        model = result.get('model', 'unknown')
        if result.get('success'):
            time_taken = result.get('generation_time', 0)
            output.append(f"{i}. ✅ {MODELS.get(model, {}).get('name', model)}: {time_taken:.2f}s")
        else:
            error = result.get('error', 'Unknown error')
            output.append(f"{i}. ❌ {MODELS.get(model, {}).get('name', model)}: {error}")
    
    return "\n".join(output)

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="generate_image",
            description="Generate a single image using FAL AI with the specified model",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Text prompt describing the image to generate"
                    },
                    "model": {
                        "type": "string",
                        "enum": ["imagen4", "seedream", "flux_schnell", "flux_dev"],
                        "default": "imagen4",
                        "description": "Model to use for generation"
                    },
                    "negative_prompt": {
                        "type": "string",
                        "description": "Optional negative prompt to avoid certain elements"
                    },
                    "output_folder": {
                        "type": "string",
                        "default": "output",
                        "description": "Folder to save the generated image"
                    },
                    "confirm_cost": {
                        "type": "boolean",
                        "default": True,
                        "description": "Whether to show cost confirmation (set to false for automated workflows)"
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="batch_generate_images",
            description="Generate images with multiple models for comparison",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Text prompt describing the image to generate"
                    },
                    "models": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["imagen4", "seedream", "flux_schnell", "flux_dev"]
                        },
                        "default": ["imagen4", "flux_dev"],
                        "description": "List of models to use for generation"
                    },
                    "negative_prompt": {
                        "type": "string",
                        "description": "Optional negative prompt to avoid certain elements"
                    },
                    "output_folder": {
                        "type": "string",
                        "default": "output",
                        "description": "Folder to save the generated images"
                    },
                    "confirm_cost": {
                        "type": "boolean",
                        "default": True,
                        "description": "Whether to show cost confirmation (set to false for automated workflows)"
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="list_models",
            description="List all available text-to-image models with their specifications",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_model_info",
            description="Get detailed information about a specific model",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {
                        "type": "string",
                        "enum": ["imagen4", "seedream", "flux_schnell", "flux_dev"],
                        "description": "Model to get information about"
                    }
                },
                "required": ["model"]
            }
        ),
        Tool(
            name="download_image",
            description="Download a generated image from URL to local storage",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_url": {
                        "type": "string",
                        "description": "URL of the image to download"
                    },
                    "output_folder": {
                        "type": "string",
                        "default": "output",
                        "description": "Folder to save the downloaded image"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Optional custom filename (with extension)"
                    }
                },
                "required": ["image_url"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    global generator
    
    # Initialize generator if not already done
    if generator is None:
        try:
            generator = FALTextToImageGenerator()
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"❌ **Error**: Failed to initialize FAL AI generator: {str(e)}\n\n"
                     f"Please check your FAL_KEY environment variable and try again."
            )]
    
    try:
        if name == "generate_image":
            return await handle_generate_image(arguments)
        elif name == "batch_generate_images":
            return await handle_batch_generate_images(arguments)
        elif name == "list_models":
            return await handle_list_models(arguments)
        elif name == "get_model_info":
            return await handle_get_model_info(arguments)
        elif name == "download_image":
            return await handle_download_image(arguments)
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ **Error**: Unknown tool '{name}'"
            )]
    
    except Exception as e:
        logger.error(f"Error in tool '{name}': {str(e)}")
        return [types.TextContent(
            type="text",
            text=f"❌ **Error**: Tool '{name}' failed: {str(e)}"
        )]

async def handle_generate_image(arguments: dict) -> list[types.TextContent]:
    """Handle single image generation."""
    # Check if generator is initialized
    if generator is None:
        return [types.TextContent(
            type="text",
            text="❌ **Error**: FAL AI generator not initialized. Please check your configuration and restart the server."
        )]
    
    prompt = arguments.get("prompt")
    model = arguments.get("model", "imagen4")
    negative_prompt = arguments.get("negative_prompt")
    output_folder = arguments.get("output_folder", "output")
    confirm_cost = arguments.get("confirm_cost", True)
    
    # Validate model
    if model not in MODELS:
        return [types.TextContent(
            type="text",
            text=f"❌ **Error**: Invalid model '{model}'. Available models: {', '.join(MODELS.keys())}"
        )]
    
    # Cost warning
    estimated_cost = MODELS[model]["cost"]
    response_parts = []
    
    if confirm_cost:
        response_parts.append(types.TextContent(
            type="text",
            text=format_cost_warning(estimated_cost, 1)
        ))
    
    try:
        # Generate image
        result = generator.generate_image(
            prompt=prompt,
            model=model,
            negative_prompt=negative_prompt,
            output_folder=output_folder
        )
        
        # Format result
        result_text = format_generation_result(result)
        response_parts.append(types.TextContent(
            type="text",
            text=result_text
        ))
        
        return response_parts
    
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ **Generation Failed**: {str(e)}"
        )]

async def handle_batch_generate_images(arguments: dict) -> list[types.TextContent]:
    """Handle batch image generation."""
    # Check if generator is initialized
    if generator is None:
        return [types.TextContent(
            type="text",
            text="❌ **Error**: FAL AI generator not initialized. Please check your configuration and restart the server."
        )]
    
    prompt = arguments.get("prompt")
    models = arguments.get("models", ["imagen4", "flux_dev"])
    negative_prompt = arguments.get("negative_prompt")
    output_folder = arguments.get("output_folder", "output")
    confirm_cost = arguments.get("confirm_cost", True)
    
    # Validate models
    invalid_models = [m for m in models if m not in MODELS]
    if invalid_models:
        return [types.TextContent(
            type="text",
            text=f"❌ **Error**: Invalid models: {', '.join(invalid_models)}. Available models: {', '.join(MODELS.keys())}"
        )]
    
    # Cost warning
    estimated_cost = sum(MODELS[model]["cost"] for model in models)
    response_parts = []
    
    if confirm_cost:
        response_parts.append(types.TextContent(
            type="text",
            text=format_cost_warning(estimated_cost, len(models))
        ))
    
    try:
        # Generate images
        result = generator.batch_generate(
            prompt=prompt,
            models=models,
            negative_prompt=negative_prompt,
            output_folder=output_folder,
            auto_confirm=True,  # Skip confirmation in MCP context
            download_images=True
        )
        
        # Format results
        results = result.get("results", [])
        summary = result.get("summary", {})
        
        summary_text = format_batch_summary(results, summary)
        response_parts.append(types.TextContent(
            type="text",
            text=summary_text
        ))
        
        return response_parts
    
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ **Batch Generation Failed**: {str(e)}"
        )]

async def handle_list_models(arguments: dict) -> list[types.TextContent]:
    """Handle listing available models."""
    output = ["🎨 **Available FAL AI Text-to-Image Models:**", ""]
    
    for model_key, model_info in MODELS.items():
        output.append(format_model_info(model_key))
        output.append("")
    
    output.extend([
        "**Usage Tips:**",
        "- **Imagen4**: Best for photorealistic images and portraits",
        "- **Seedream**: Best for artistic and creative content",
        "- **FLUX Schnell**: Best for fast iterations and testing",
        "- **FLUX Dev**: Best for production content with balanced quality/speed",
        "",
        "💡 Use batch generation to compare multiple models with the same prompt!"
    ])
    
    return [types.TextContent(
        type="text",
        text="\n".join(output)
    )]

async def handle_get_model_info(arguments: dict) -> list[types.TextContent]:
    """Handle getting information about a specific model."""
    model = arguments.get("model")
    
    if model not in MODELS:
        return [types.TextContent(
            type="text",
            text=f"❌ **Error**: Invalid model '{model}'. Available models: {', '.join(MODELS.keys())}"
        )]
    
    info_text = format_model_info(model)
    
    return [types.TextContent(
        type="text",
        text=info_text
    )]

async def handle_download_image(arguments: dict) -> list[types.TextContent]:
    """Handle downloading an image from URL."""
    # Check if generator is initialized
    if generator is None:
        return [types.TextContent(
            type="text",
            text="❌ **Error**: FAL AI generator not initialized. Please check your configuration and restart the server."
        )]
    
    image_url = arguments.get("image_url")
    output_folder = arguments.get("output_folder", "output")
    filename = arguments.get("filename")
    
    try:
        # Use generator's download method
        local_path = generator.download_image(image_url, output_folder, filename)
        
        return [types.TextContent(
            type="text",
            text=f"✅ **Download Successful**\n"
                 f"- Image URL: {image_url}\n"
                 f"- Local path: {local_path}\n"
                 f"- File size: {os.path.getsize(local_path)} bytes"
        )]
    
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ **Download Failed**: {str(e)}"
        )]

@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources (generated images)."""
    resources = []
    
    # Check output directories for generated images
    output_dirs = ["output", "test_output"]
    
    for output_dir in output_dirs:
        if os.path.exists(output_dir):
            for file_path in Path(output_dir).glob("*.png"):
                resources.append(Resource(
                    uri=f"file://{file_path.absolute()}",
                    name=file_path.name,
                    description=f"Generated image from {output_dir}",
                    mimeType="image/png"
                ))
            
            for file_path in Path(output_dir).glob("*.jpg"):
                resources.append(Resource(
                    uri=f"file://{file_path.absolute()}",
                    name=file_path.name,
                    description=f"Generated image from {output_dir}",
                    mimeType="image/jpeg"
                ))
    
    return resources

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a resource (image file)."""
    try:
        if uri.startswith("file://"):
            file_path = uri[7:]  # Remove "file://" prefix
            
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    import base64
                    content = base64.b64encode(f.read()).decode()
                    return content
            else:
                raise FileNotFoundError(f"File not found: {file_path}")
        else:
            raise ValueError(f"Unsupported URI scheme: {uri}")
    
    except Exception as e:
        raise RuntimeError(f"Failed to read resource {uri}: {str(e)}")

async def main():
    """Main entry point for the MCP server."""
    global generator
    
    # Initialize the generator
    try:
        generator = FALTextToImageGenerator()
        logger.info("✅ FAL AI Text-to-Image generator initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize generator: {e}")
        # Continue anyway for testing purposes
        generator = None
    
    # Import here to avoid issues with event loop
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="fal-text-to-image",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main()) 