# AI Content Generation Platform - Package Creation Guide (Part 5)

## 🎯 Phase 5: CLI Implementation, Testing, and Packaging

### Step 5.1: CLI Structure and Framework

Create the CLI structure using Click framework:
```bash
# Create CLI directory
mkdir -p ai_content_platform/cli

# Create CLI modules
touch ai_content_platform/cli/__init__.py
touch ai_content_platform/cli/main.py
touch ai_content_platform/cli/pipeline.py
touch ai_content_platform/cli/config.py
touch ai_content_platform/cli/utils.py
```

### Step 5.2: Main CLI Entry Point

Create `ai_content_platform/cli/main.py`:
```python
"""Main CLI entry point for AI Content Platform."""

import click
import os
from pathlib import Path
from typing import Optional

from ai_content_platform.__version__ import __version__
from ai_content_platform.utils.logger import setup_logging, get_logger
from ai_content_platform.cli.pipeline import pipeline_group
from ai_content_platform.cli.config import config_group
from ai_content_platform.services import check_service_dependencies


logger = get_logger(__name__)


@click.group()
@click.version_option(version=__version__, prog_name="ai-content-platform")
@click.option(
    "--debug", 
    is_flag=True, 
    help="Enable debug logging"
)
@click.option(
    "--quiet", 
    is_flag=True, 
    help="Suppress output except errors"
)
@click.option(
    "--log-file", 
    type=click.Path(), 
    help="Log to file"
)
@click.pass_context
def cli(ctx, debug: bool, quiet: bool, log_file: Optional[str]):
    """AI Content Platform - Unified content generation pipeline.
    
    A comprehensive platform for generating AI content using multiple services
    with parallel execution capabilities and cost-conscious design.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Setup logging
    if quiet:
        log_level = "WARNING"
    elif debug:
        log_level = "DEBUG"
    else:
        log_level = "INFO"
    
    setup_logging(level=log_level, log_file=log_file)
    
    # Store context
    ctx.obj['debug'] = debug
    ctx.obj['quiet'] = quiet
    ctx.obj['log_file'] = log_file


@cli.command()
@click.pass_context
def info(ctx):
    """Show platform information and service status."""
    click.echo(f"🚀 AI Content Platform v{__version__}")
    click.echo("=" * 50)
    
    # Check service dependencies
    deps = check_service_dependencies()
    
    click.echo("\n📦 Service Dependencies:")
    for service, available in deps.items():
        status = "✅ Available" if available else "❌ Not installed"
        click.echo(f"  {service}: {status}")
    
    # Show available steps
    from ai_content_platform.services import get_available_services
    available_steps = get_available_services()
    
    click.echo(f"\n🔧 Available Steps: {len(available_steps)}")
    for step in available_steps:
        click.echo(f"  • {step.value}")


@cli.command()
@click.option(
    "--output", "-o",
    type=click.Path(),
    default="example_pipeline.yaml",
    help="Output file path for example configuration"
)
def init(output: str):
    """Initialize a new pipeline configuration file."""
    from ai_content_platform.utils.config_loader import create_example_config
    
    try:
        create_example_config(output)
        click.echo(f"✅ Example configuration created: {output}")
        click.echo("\n📝 Next steps:")
        click.echo(f"  1. Edit {output} to customize your pipeline")
        click.echo(f"  2. Run: ai-content-platform pipeline run --config {output}")
        
    except Exception as e:
        click.echo(f"❌ Error creating configuration: {e}", err=True)
        raise click.ClickException(str(e))


@cli.command()
@click.option(
    "--config-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory to check for configuration files"
)
def doctor(config_dir: Optional[str]):
    """Run diagnostic checks on the platform setup."""
    click.echo("🔍 Running diagnostic checks...")
    
    issues = []
    warnings = []
    
    # Check Python version
    import sys
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ required")
    else:
        click.echo(f"✅ Python version: {sys.version}")
    
    # Check dependencies
    deps = check_service_dependencies()
    missing_deps = [name for name, available in deps.items() if not available]
    
    if missing_deps:
        warnings.append(f"Missing optional dependencies: {', '.join(missing_deps)}")
    else:
        click.echo("✅ All service dependencies available")
    
    # Check environment variables
    required_env_vars = {
        'FAL_KEY': 'FAL AI services',
        'ELEVENLABS_API_KEY': 'ElevenLabs TTS',
        'OPENROUTER_API_KEY': 'OpenRouter AI',
        'GOOGLE_API_KEY': 'Google services'
    }
    
    missing_env_vars = []
    for var, description in required_env_vars.items():
        if not os.getenv(var):
            missing_env_vars.append(f"{var} ({description})")
    
    if missing_env_vars:
        warnings.append("Missing environment variables:")
        for var in missing_env_vars:
            warnings.append(f"  • {var}")
    
    # Check configuration files
    if config_dir:
        config_path = Path(config_dir)
        yaml_files = list(config_path.glob("*.yaml")) + list(config_path.glob("*.yml"))
        json_files = list(config_path.glob("*.json"))
        
        if not yaml_files and not json_files:
            warnings.append(f"No configuration files found in {config_dir}")
        else:
            click.echo(f"✅ Found {len(yaml_files + json_files)} configuration files")
    
    # Show results
    if issues:
        click.echo("\n❌ Issues found:")
        for issue in issues:
            click.echo(f"  • {issue}")
    
    if warnings:
        click.echo("\n⚠️  Warnings:")
        for warning in warnings:
            click.echo(f"  • {warning}")
    
    if not issues and not warnings:
        click.echo("\n🎉 All checks passed! Platform is ready to use.")


# Add command groups
cli.add_command(pipeline_group)
cli.add_command(config_group)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
```

### Step 5.3: Pipeline Commands

Create `ai_content_platform/cli/pipeline.py`:
```python
"""Pipeline management CLI commands."""

import click
import asyncio
import time
from pathlib import Path
from typing import Optional

from ai_content_platform.core.executor import PipelineExecutor
from ai_content_platform.utils.config_loader import ConfigLoader
from ai_content_platform.utils.cost_calculator import CostCalculator
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.core.exceptions import PipelineConfigurationError


logger = get_logger(__name__)


@click.group(name="pipeline")
def pipeline_group():
    """Pipeline execution and management commands."""
    pass


@pipeline_group.command(name="run")
@click.option(
    "--config", "-c",
    required=True,
    type=click.Path(exists=True),
    help="Pipeline configuration file (YAML or JSON)"
)
@click.option(
    "--parallel", "-p",
    is_flag=True,
    help="Enable parallel execution"
)
@click.option(
    "--no-confirm",
    is_flag=True,
    help="Skip cost confirmation prompt"
)
@click.option(
    "--output-dir", "-o",
    type=click.Path(),
    help="Override output directory"
)
@click.option(
    "--cost-limit",
    type=float,
    help="Maximum cost limit in USD"
)
@click.pass_context
def run_pipeline(
    ctx,
    config: str,
    parallel: bool,
    no_confirm: bool,
    output_dir: Optional[str],
    cost_limit: Optional[float]
):
    """Run a pipeline from configuration file."""
    try:
        # Load configuration
        pipeline_config = ConfigLoader.load_from_file(config)
        
        # Override output directory if specified
        if output_dir:
            pipeline_config.output_directory = output_dir
        
        # Check parallel execution environment variable
        if not parallel:
            parallel = os.getenv('PIPELINE_PARALLEL_ENABLED', '').lower() == 'true'
        
        click.echo(f"🚀 Running pipeline: {pipeline_config.pipeline_name}")
        if parallel:
            click.echo("⚡ Parallel execution enabled")
        
        # Estimate cost
        if not no_confirm:
            estimate = CostCalculator.estimate_pipeline_cost(pipeline_config.steps)
            
            # Check cost limit
            limit = cost_limit or pipeline_config.global_config.get('cost_limit', 10.0)
            
            if estimate.total_cost > limit:
                click.echo(f"💰 Estimated cost: ${estimate.total_cost:.3f}")
                click.echo(f"⚠️  Cost exceeds limit: ${limit:.2f}")
                
                if not click.confirm("Continue anyway?"):
                    click.echo("❌ Pipeline execution cancelled")
                    return
            else:
                click.echo(f"💰 Estimated cost: ${estimate.total_cost:.3f}")
                
                if estimate.total_cost > 0.10:  # Only confirm for costs > 10 cents
                    if not click.confirm("Proceed with pipeline execution?"):
                        click.echo("❌ Pipeline execution cancelled")
                        return
        
        # Execute pipeline
        executor = PipelineExecutor(pipeline_config, parallel_enabled=parallel)
        
        start_time = time.time()
        result = asyncio.run(executor.execute())
        execution_time = time.time() - start_time
        
        # Show results
        if result.success:
            click.echo(f"✅ Pipeline completed successfully!")
            click.echo(f"⏱️  Total time: {execution_time:.2f}s")
            click.echo(f"📊 Steps: {result.successful_steps}/{result.total_steps} successful")
            click.echo(f"💰 Total cost: ${result.total_cost:.3f}")
            click.echo(f"📁 Output: {result.output_directory}")
        else:
            click.echo(f"❌ Pipeline failed!")
            click.echo(f"📊 Steps: {result.successful_steps}/{result.total_steps} successful")
            
            # Show failed steps
            failed_steps = [step for step in result.step_results if not step.success]
            if failed_steps:
                click.echo("\n💥 Failed steps:")
                for step in failed_steps:
                    click.echo(f"  • {step.step_type}: {step.error}")
        
    except PipelineConfigurationError as e:
        click.echo(f"❌ Configuration error: {e}", err=True)
        raise click.ClickException(str(e))
    except Exception as e:
        logger.exception("Pipeline execution failed")
        click.echo(f"❌ Execution error: {e}", err=True)
        raise click.ClickException(str(e))


@pipeline_group.command(name="validate")
@click.option(
    "--config", "-c",
    required=True,
    type=click.Path(exists=True),
    help="Pipeline configuration file to validate"
)
def validate_pipeline(config: str):
    """Validate a pipeline configuration file."""
    try:
        pipeline_config = ConfigLoader.load_from_file(config)
        
        click.echo(f"✅ Configuration is valid!")
        click.echo(f"📝 Pipeline: {pipeline_config.pipeline_name}")
        click.echo(f"📊 Steps: {len(pipeline_config.steps)}")
        
        # Show step breakdown
        from collections import Counter
        step_types = [step.step_type for step in pipeline_config.steps]
        step_counts = Counter(step_types)
        
        click.echo("\n📋 Step breakdown:")
        for step_type, count in step_counts.items():
            click.echo(f"  • {step_type}: {count}")
        
        # Estimate cost
        estimate = CostCalculator.estimate_pipeline_cost(pipeline_config.steps)
        click.echo(f"\n💰 Estimated cost: ${estimate.total_cost:.3f}")
        
    except Exception as e:
        click.echo(f"❌ Validation failed: {e}", err=True)
        raise click.ClickException(str(e))


@pipeline_group.command(name="estimate")
@click.option(
    "--config", "-c",
    required=True,
    type=click.Path(exists=True),
    help="Pipeline configuration file"
)
@click.option(
    "--detailed",
    is_flag=True,
    help="Show detailed cost breakdown"
)
def estimate_cost(config: str, detailed: bool):
    """Estimate cost for pipeline execution."""
    try:
        pipeline_config = ConfigLoader.load_from_file(config)
        estimate = CostCalculator.estimate_pipeline_cost(pipeline_config.steps)
        
        click.echo(f"💰 Cost Estimate for: {pipeline_config.pipeline_name}")
        click.echo("=" * 50)
        click.echo(f"Total Cost: ${estimate.total_cost:.3f} {estimate.currency}")
        click.echo(f"Confidence: {estimate.confidence}")
        
        if detailed:
            click.echo("\n📊 Step Breakdown:")
            for step_name, cost in estimate.step_costs.items():
                click.echo(f"  • {step_name}: ${cost:.3f}")
        
        # Cost warnings
        limit = pipeline_config.global_config.get('cost_limit', 10.0)
        warning = CostCalculator.get_cost_warning_message(estimate, limit)
        if warning:
            click.echo(f"\n⚠️  {warning}")
        
    except Exception as e:
        click.echo(f"❌ Cost estimation failed: {e}", err=True)
        raise click.ClickException(str(e))


@pipeline_group.command(name="list")
@click.option(
    "--directory", "-d",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=".",
    help="Directory to search for pipeline configurations"
)
def list_pipelines(directory: str):
    """List available pipeline configurations."""
    config_dir = Path(directory)
    
    # Find configuration files
    yaml_files = list(config_dir.glob("*.yaml")) + list(config_dir.glob("*.yml"))
    json_files = list(config_dir.glob("*.json"))
    
    all_configs = yaml_files + json_files
    
    if not all_configs:
        click.echo(f"No pipeline configurations found in {directory}")
        return
    
    click.echo(f"📁 Pipeline configurations in {directory}:")
    click.echo("=" * 50)
    
    for config_file in all_configs:
        try:
            pipeline_config = ConfigLoader.load_from_file(config_file)
            
            click.echo(f"📝 {config_file.name}")
            click.echo(f"   Name: {pipeline_config.pipeline_name}")
            click.echo(f"   Steps: {len(pipeline_config.steps)}")
            
            if pipeline_config.description:
                click.echo(f"   Description: {pipeline_config.description}")
            
            # Quick cost estimate
            estimate = CostCalculator.estimate_pipeline_cost(pipeline_config.steps)
            click.echo(f"   Estimated cost: ${estimate.total_cost:.3f}")
            click.echo()
            
        except Exception as e:
            click.echo(f"⚠️  {config_file.name}: Error loading - {e}")
            click.echo()
```

### Step 5.4: Configuration Management Commands

Create `ai_content_platform/cli/config.py`:
```python
"""Configuration management CLI commands."""

import click
import yaml
import json
from pathlib import Path
from typing import Dict, Any

from ai_content_platform.utils.config_loader import ConfigLoader, create_example_config
from ai_content_platform.utils.logger import get_logger
from ai_content_platform.services import get_available_services


logger = get_logger(__name__)


@click.group(name="config")
def config_group():
    """Configuration management commands."""
    pass


@config_group.command(name="create")
@click.option(
    "--output", "-o",
    type=click.Path(),
    default="pipeline.yaml",
    help="Output configuration file"
)
@click.option(
    "--template",
    type=click.Choice(['basic', 'tts', 'image', 'video', 'parallel']),
    default='basic',
    help="Configuration template to use"
)
@click.option(
    "--interactive", "-i",
    is_flag=True,
    help="Interactive configuration creation"
)
def create_config(output: str, template: str, interactive: bool):
    """Create a new pipeline configuration."""
    
    if interactive:
        config = _create_interactive_config()
    else:
        config = _get_template_config(template)
    
    # Save configuration
    output_path = Path(output)
    
    try:
        with open(output_path, 'w') as f:
            if output_path.suffix.lower() in ['.yaml', '.yml']:
                yaml.dump(config, f, default_flow_style=False, indent=2)
            else:
                json.dump(config, f, indent=2)
        
        click.echo(f"✅ Configuration created: {output}")
        click.echo(f"📝 Template: {template}")
        click.echo(f"🚀 Run with: ai-content-platform pipeline run --config {output}")
        
    except Exception as e:
        click.echo(f"❌ Error creating configuration: {e}", err=True)
        raise click.ClickException(str(e))


@config_group.command(name="validate")
@click.argument("config_file", type=click.Path(exists=True))
def validate_config(config_file: str):
    """Validate a configuration file."""
    try:
        config = ConfigLoader.load_from_file(config_file)
        click.echo(f"✅ Configuration is valid!")
        click.echo(f"📝 Pipeline: {config.pipeline_name}")
        click.echo(f"📊 Steps: {len(config.steps)}")
        
    except Exception as e:
        click.echo(f"❌ Validation failed: {e}", err=True)
        raise click.ClickException(str(e))


@config_group.command(name="convert")
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def convert_config(input_file: str, output_file: str):
    """Convert configuration between YAML and JSON formats."""
    try:
        # Load configuration
        config = ConfigLoader.load_from_file(input_file)
        
        # Save in new format
        ConfigLoader.save_to_file(config, output_file)
        
        click.echo(f"✅ Configuration converted:")
        click.echo(f"   From: {input_file}")
        click.echo(f"   To: {output_file}")
        
    except Exception as e:
        click.echo(f"❌ Conversion failed: {e}", err=True)
        raise click.ClickException(str(e))


@config_group.command(name="merge")
@click.argument("base_config", type=click.Path(exists=True))
@click.argument("override_config", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def merge_configs(base_config: str, override_config: str, output_file: str):
    """Merge two configuration files."""
    try:
        # Load configurations
        base = ConfigLoader.load_from_file(base_config)
        override = ConfigLoader.load_from_file(override_config)
        
        # Merge configurations
        base_dict = base.dict()
        override_dict = override.dict()
        merged_dict = ConfigLoader.merge_configs(base_dict, override_dict)
        
        # Create merged config
        merged_config = ConfigLoader.load_from_dict(merged_dict)
        
        # Save merged configuration
        ConfigLoader.save_to_file(merged_config, output_file)
        
        click.echo(f"✅ Configurations merged:")
        click.echo(f"   Base: {base_config}")
        click.echo(f"   Override: {override_config}")
        click.echo(f"   Output: {output_file}")
        
    except Exception as e:
        click.echo(f"❌ Merge failed: {e}", err=True)
        raise click.ClickException(str(e))


def _create_interactive_config() -> Dict[str, Any]:
    """Create configuration interactively."""
    click.echo("🛠️  Interactive Configuration Creator")
    click.echo("=" * 40)
    
    # Basic information
    name = click.prompt("Pipeline name", default="my_pipeline")
    description = click.prompt("Description (optional)", default="", show_default=False)
    output_dir = click.prompt("Output directory", default="output")
    
    config = {
        "pipeline_name": name,
        "description": description or None,
        "output_directory": output_dir,
        "global_config": {
            "parallel_enabled": click.confirm("Enable parallel execution?", default=False),
            "cost_limit": click.prompt("Cost limit (USD)", type=float, default=10.0)
        },
        "steps": []
    }
    
    # Add steps
    available_steps = get_available_services()
    step_choices = [step.value for step in available_steps]
    
    while True:
        if config["steps"]:
            click.echo(f"\nCurrent steps: {len(config['steps'])}")
            for i, step in enumerate(config["steps"], 1):
                click.echo(f"  {i}. {step['step_type']}")
        
        if not click.confirm("\nAdd a step?", default=True):
            break
        
        step_type = click.prompt(
            "Step type",
            type=click.Choice(step_choices),
            show_choices=True
        )
        
        step_config = _create_step_config(step_type)
        config["steps"].append(step_config)
    
    return config


def _create_step_config(step_type: str) -> Dict[str, Any]:
    """Create configuration for a specific step type."""
    step_config = {
        "step_type": step_type,
        "config": {}
    }
    
    # Step-specific configuration
    if step_type == "text_to_speech":
        step_config["config"]["text"] = click.prompt("Text to speak")
        step_config["config"]["voice"] = click.prompt("Voice name", default="Rachel")
        step_config["output_filename"] = click.prompt("Output filename", default=f"{step_type}.mp3")
    
    elif step_type == "text_to_image":
        step_config["config"]["prompt"] = click.prompt("Image prompt")
        step_config["config"]["model"] = click.prompt(
            "Model",
            type=click.Choice(['flux-dev', 'flux-schnell', 'imagen-4']),
            default='flux-dev'
        )
        step_config["output_filename"] = click.prompt("Output filename", default=f"{step_type}.png")
    
    elif step_type == "text_to_video":
        step_config["config"]["prompt"] = click.prompt("Video prompt")
        step_config["config"]["model"] = click.prompt(
            "Model",
            type=click.Choice(['minimax-hailuo-pro', 'google-veo-3']),
            default='minimax-hailuo-pro'
        )
        step_config["config"]["duration"] = click.prompt("Duration (seconds)", type=int, default=6)
        step_config["output_filename"] = click.prompt("Output filename", default=f"{step_type}.mp4")
    
    return step_config


def _get_template_config(template: str) -> Dict[str, Any]:
    """Get predefined template configuration."""
    templates = {
        'basic': {
            "pipeline_name": "basic_pipeline",
            "description": "Basic pipeline template",
            "output_directory": "output",
            "steps": []
        },
        'tts': {
            "pipeline_name": "text_to_speech_pipeline",
            "description": "Text-to-speech generation pipeline",
            "output_directory": "output",
            "steps": [
                {
                    "step_type": "text_to_speech",
                    "config": {
                        "text": "Hello, this is AI-generated speech!",
                        "voice": "Rachel"
                    },
                    "output_filename": "speech.mp3"
                }
            ]
        },
        'image': {
            "pipeline_name": "image_generation_pipeline",
            "description": "Image generation pipeline",
            "output_directory": "output",
            "steps": [
                {
                    "step_type": "text_to_image",
                    "config": {
                        "prompt": "A beautiful landscape with mountains and lakes",
                        "model": "flux-dev",
                        "image_size": "landscape_16_9"
                    },
                    "output_filename": "landscape.png"
                }
            ]
        },
        'video': {
            "pipeline_name": "video_generation_pipeline",
            "description": "Video generation pipeline",
            "output_directory": "output",
            "steps": [
                {
                    "step_type": "text_to_video",
                    "config": {
                        "prompt": "A serene mountain lake at sunset",
                        "model": "minimax-hailuo-pro",
                        "duration": 6
                    },
                    "output_filename": "mountain_lake.mp4"
                }
            ]
        },
        'parallel': {
            "pipeline_name": "parallel_pipeline",
            "description": "Parallel execution example",
            "output_directory": "output",
            "global_config": {
                "parallel_enabled": True
            },
            "steps": [
                {
                    "step_type": "parallel_group",
                    "parallel_config": {
                        "merge_strategy": "collect_all"
                    },
                    "steps": [
                        {
                            "step_type": "text_to_speech",
                            "config": {
                                "text": "First voice saying hello",
                                "voice": "Adam"
                            },
                            "output_filename": "voice1.mp3"
                        },
                        {
                            "step_type": "text_to_speech",
                            "config": {
                                "text": "Second voice saying hello",
                                "voice": "Rachel"
                            },
                            "output_filename": "voice2.mp3"
                        }
                    ]
                }
            ]
        }
    }
    
    return templates.get(template, templates['basic'])
```

### Step 5.5: Setup.py Configuration

Create `setup.py` in the root directory:
```python
"""Setup configuration for AI Content Platform package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read version
version_file = Path(__file__).parent / "ai_content_platform" / "__version__.py"
version_dict = {}
with open(version_file) as f:
    exec(f.read(), version_dict)

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_dir = Path(__file__).parent / "requirements"

def read_requirements(filename):
    """Read requirements from file."""
    req_file = requirements_dir / filename
    if req_file.exists():
        return req_file.read_text().strip().split('\n')
    return []

# Core requirements
install_requires = read_requirements("base.txt")

# Optional requirements
extras_require = {
    "fal": read_requirements("fal.txt"),
    "google": read_requirements("google.txt"),
    "tts": read_requirements("tts.txt"),
    "video": read_requirements("video.txt"),
    "dev": read_requirements("dev.txt"),
    "all": (
        read_requirements("fal.txt") +
        read_requirements("google.txt") +
        read_requirements("tts.txt") +
        read_requirements("video.txt")
    )
}

setup(
    name="ai-content-platform",
    version=version_dict["__version__"],
    author=version_dict["__author__"],
    author_email=version_dict["__email__"],
    description=version_dict["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=version_dict["__url__"],
    
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    include_package_data=True,
    
    python_requires=">=3.8",
    install_requires=install_requires,
    extras_require=extras_require,
    
    entry_points={
        "console_scripts": [
            "ai-content-platform=ai_content_platform.cli.main:main",
            "acp=ai_content_platform.cli.main:main",  # Short alias
        ],
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    
    keywords=[
        "ai", "artificial-intelligence", "content-generation", "pipeline",
        "text-to-speech", "text-to-image", "text-to-video", "image-to-image",
        "fal-ai", "elevenlabs", "google-veo", "parallel-execution"
    ],
    
    project_urls={
        "Bug Reports": f"{version_dict['__url__']}/issues",
        "Source": version_dict["__url__"],
        "Documentation": f"{version_dict['__url__']}/blob/main/README.md",
    },
    
    zip_safe=False,
)
```

### Step 5.6: Modern Packaging with pyproject.toml

Create `pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-content-platform"
description = "Comprehensive AI content generation platform with unified pipeline"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "AI Content Platform Team", email = "contact@aicontentplatform.com"}
]
maintainers = [
    {name = "AI Content Platform Team", email = "contact@aicontentplatform.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
keywords = [
    "ai", "artificial-intelligence", "content-generation", "pipeline",
    "text-to-speech", "text-to-image", "text-to-video", "parallel-execution"
]
requires-python = ">=3.8"
dependencies = [
    "pyyaml>=6.0",
    "requests>=2.28.0",
    "python-dotenv>=0.19.0",
    "typing-extensions>=4.0.0",
    "pydantic>=1.10.0",
    "click>=8.0.0",
    "rich>=12.0.0",
    "tqdm>=4.64.0",
    "aiohttp>=3.8.0",
    "aiofiles>=22.1.0",
]
dynamic = ["version"]

[project.optional-dependencies]
fal = ["fal-client>=0.2.0", "pillow>=9.0.0"]
google = [
    "google-generativeai>=0.3.0",
    "google-cloud-storage>=2.7.0",
    "google-auth>=2.16.0"
]
tts = ["elevenlabs>=0.2.0"]
video = ["ffmpeg-python>=0.2.0", "opencv-python>=4.7.0"]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "pytest-asyncio>=0.21.0",
    "black>=22.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "sphinx>=6.0.0",
    "sphinx-rtd-theme>=1.2.0",
    "twine>=4.0.0",
    "build>=0.10.0",
]
all = [
    "fal-client>=0.2.0",
    "pillow>=9.0.0",
    "google-generativeai>=0.3.0",
    "google-cloud-storage>=2.7.0",
    "google-auth>=2.16.0",
    "elevenlabs>=0.2.0",
    "ffmpeg-python>=0.2.0",
    "opencv-python>=4.7.0",
]

[project.scripts]
ai-content-platform = "ai_content_platform.cli.main:main"
acp = "ai_content_platform.cli.main:main"

[project.urls]
Homepage = "https://github.com/username/ai-content-platform"
Documentation = "https://github.com/username/ai-content-platform/blob/main/README.md"
Repository = "https://github.com/username/ai-content-platform"
"Bug Tracker" = "https://github.com/username/ai-content-platform/issues"

[tool.setuptools.dynamic]
version = {attr = "ai_content_platform.__version__.__version__"}

[tool.setuptools.packages.find]
exclude = ["tests*", "docs*", "examples*"]

[tool.setuptools.package-data]
ai_content_platform = ["py.typed"]

# Development tools configuration
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["ai_content_platform"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = [
    "fal_client.*",
    "elevenlabs.*",
    "google.*",
    "ffmpeg.*",
    "cv2.*",
]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=ai_content_platform",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
asyncio_mode = "auto"
```

---

**Part 5 Complete** - This covers:

1. **Complete CLI Framework** - Professional Click-based CLI with commands for pipeline management
2. **Interactive Configuration** - User-friendly config creation with templates and validation
3. **Modern Packaging Setup** - Both setup.py and pyproject.toml for compatibility
4. **Development Tools Configuration** - Black, isort, mypy, pytest configuration
5. **Entry Points** - Console scripts for easy installation and usage

The next section will cover testing framework, documentation, and deployment. Would you like me to continue with Part 6?