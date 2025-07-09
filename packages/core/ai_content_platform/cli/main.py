"""Main CLI entry point for AI Content Platform."""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from ai_content_platform import __version__, __description__
from ai_content_platform.utils.logger import setup_logging, get_logger


# Global console for Rich output
console = Console()


@click.group(invoke_without_command=True)
@click.option(
    "--version", 
    is_flag=True, 
    help="Show version information"
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="INFO",
    help="Set logging level"
)
@click.option(
    "--log-file",
    type=click.Path(),
    help="Log file path"
)
@click.option(
    "--config-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Configuration directory"
)
@click.pass_context
def cli(ctx, version, log_level, log_file, config_dir):
    """
    AI Content Platform - Comprehensive AI content generation framework.
    
    Generate images, videos, audio, and avatars using multiple AI services
    with parallel execution and cost-conscious design.
    """
    # Setup logging
    setup_logging(level=log_level, log_file=log_file)
    
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Store global options in context
    ctx.obj["log_level"] = log_level
    ctx.obj["log_file"] = log_file
    ctx.obj["config_dir"] = config_dir
    
    if version:
        show_version_info()
        return
    
    # If no command provided, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


def show_version_info():
    """Display detailed version information."""
    table = Table(title="AI Content Platform", show_header=False)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Version", __version__)
    table.add_row("Description", __description__)
    table.add_row("Python", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    table.add_row("Platform", sys.platform)
    
    # Check service availability
    services = check_service_availability()
    for service, available in services.items():
        status = "[green]✓ Available[/green]" if available else "[red]✗ Not Available[/red]"
        table.add_row(f"{service} Service", status)
    
    console.print(table)


def check_service_availability():
    """Check availability of AI services."""
    services = {
        "FAL AI": False,
        "ElevenLabs": False,
        "Google Vertex AI": False,
        "OpenRouter": False
    }
    
    # Check environment variables for API keys
    env_vars = os.environ
    
    if env_vars.get("FAL_KEY") or env_vars.get("FAL_API_KEY"):
        services["FAL AI"] = True
    
    if env_vars.get("ELEVENLABS_API_KEY") or env_vars.get("ELEVEN_API_KEY"):
        services["ElevenLabs"] = True
    
    if env_vars.get("GOOGLE_API_KEY") or env_vars.get("GEMINI_API_KEY"):
        services["Google Vertex AI"] = True
    
    if env_vars.get("OPENROUTER_API_KEY") or env_vars.get("OPENAI_API_KEY"):
        services["OpenRouter"] = True
    
    return services


@cli.command()
@click.option(
    "--output", 
    type=click.Path(),
    help="Output directory for generated files"
)
def init(output):
    """Initialize a new AI Content Platform project."""
    logger = get_logger(__name__)
    
    if not output:
        output = Path.cwd() / "ai_content_project"
    else:
        output = Path(output)
    
    try:
        logger.info(f"Initializing project at {output}")
        
        # Create project structure
        output.mkdir(parents=True, exist_ok=True)
        
        # Create directories
        (output / "configs").mkdir(exist_ok=True)
        (output / "output").mkdir(exist_ok=True)
        (output / "logs").mkdir(exist_ok=True)
        
        # Create sample configuration
        create_sample_config(output / "configs" / "sample_pipeline.yaml")
        
        # Create .env template
        create_env_template(output / ".env.template")
        
        # Create README
        create_project_readme(output / "README.md")
        
        console.print(f"[green]✓[/green] Project initialized at {output}")
        console.print("\nNext steps:")
        console.print("1. Copy .env.template to .env and add your API keys")
        console.print("2. Edit configs/sample_pipeline.yaml for your needs")
        console.print(f"3. Run: ai-content run {output}/configs/sample_pipeline.yaml")
        
    except Exception as e:
        logger.error(f"Failed to initialize project: {e}")
        console.print(f"[red]✗[/red] Initialization failed: {e}")
        sys.exit(1)


def create_sample_config(config_path: Path):
    """Create a sample pipeline configuration."""
    config_content = """pipeline_name: "sample_content_pipeline"
description: "Sample AI content generation pipeline"
output_directory: "output"

global_config:
  max_cost: 5.0
  timeout: 300

steps:
  - name: "generate_image"
    step_type: "text_to_image"
    parameters:
      prompt: "A beautiful sunset over mountains, digital art style"
      model: "flux-1-dev"
      width: 1024
      height: 1024
  
  - name: "generate_speech"
    step_type: "text_to_speech" 
    parameters:
      text: "Welcome to AI Content Platform. This is a sample generated speech."
      voice_id: "EXAVITQu4vr4xnSDxMaL"
      voice_settings:
        stability: 0.5
        similarity_boost: 0.5
"""
    
    with open(config_path, 'w') as f:
        f.write(config_content)


def create_env_template(env_path: Path):
    """Create environment template."""
    env_content = """# AI Content Platform Environment Configuration

# FAL AI (for image/video/avatar generation)
FAL_KEY=your_fal_api_key_here

# ElevenLabs (for text-to-speech)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Google Vertex AI (for Veo video generation)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CLOUD_PROJECT=your_project_id_here

# OpenRouter (alternative AI services)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Custom configuration
# PIPELINE_PARALLEL_ENABLED=true
# PIPELINE_MAX_WORKERS=4
"""
    
    with open(env_path, 'w') as f:
        f.write(env_content)


def create_project_readme(readme_path: Path):
    """Create project README."""
    readme_content = f"""# AI Content Platform Project

Generated with AI Content Platform v{__version__}

## Quick Start

1. **Setup Environment**
   ```bash
   cp .env.template .env
   # Edit .env with your API keys
   ```

2. **Run Sample Pipeline**
   ```bash
   ai-content run configs/sample_pipeline.yaml
   ```

3. **View Results**
   Check the `output/` directory for generated content.

## Configuration

Edit `configs/sample_pipeline.yaml` to customize your pipeline:
- Add/remove generation steps
- Configure AI models and parameters
- Set cost limits and timeouts

## Available Step Types

- `text_to_image`: Generate images from text prompts
- `image_to_image`: Transform existing images
- `text_to_video`: Create videos from text descriptions  
- `text_to_speech`: Convert text to audio
- `avatar_generation`: Create talking avatar videos

## Documentation

For complete documentation, visit: https://github.com/your-repo/ai-content-platform

## Support

- Check logs in `logs/` directory for troubleshooting
- Use `ai-content validate` to check configurations
- Use `ai-content cost` to estimate pipeline costs
"""
    
    with open(readme_path, 'w') as f:
        f.write(readme_content)


# Register commands
from .commands import run, validate, cost, config, info

cli.add_command(run)
cli.add_command(validate)
cli.add_command(cost)
cli.add_command(config)
cli.add_command(info)


if __name__ == "__main__":
    cli()