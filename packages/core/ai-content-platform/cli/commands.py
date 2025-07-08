"""CLI commands for AI Content Platform."""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.tree import Tree

from ai_content_platform.core import (
    PipelineExecutor,
    ParallelPipelineExecutor,
    StepFactory
)
from ai_content_platform.utils import (
    ConfigLoader,
    ConfigValidator,
    CostCalculator,
    get_logger
)
from ai_content_platform.core.exceptions import (
    ConfigurationError,
    ValidationError,
    PipelineExecutionError
)


console = Console()


@click.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--parallel/--no-parallel",
    default=True,
    help="Enable/disable parallel execution"
)
@click.option(
    "--max-workers",
    type=int,
    help="Maximum number of worker threads"
)
@click.option(
    "--output-dir",
    type=click.Path(),
    help="Override output directory"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Validate and estimate costs without execution"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Verbose output"
)
@click.pass_context
def run(ctx, config_file, parallel, max_workers, output_dir, dry_run, verbose):
    """Run an AI content generation pipeline."""
    logger = get_logger(__name__)
    
    try:
        # Load configuration
        config_loader = ConfigLoader()
        config = config_loader.load_pipeline_config(config_file)
        
        # Override output directory if specified
        if output_dir:
            config.output_directory = output_dir
        
        # Display pipeline info
        display_pipeline_info(config, dry_run)
        
        # Estimate costs
        cost_calculator = CostCalculator()
        cost_summary = cost_calculator.estimate_pipeline_cost(
            _flatten_steps(config.steps)
        )
        
        display_cost_summary(cost_summary)
        
        # Check if dry run
        if dry_run:
            console.print("[yellow]Dry run completed. No pipeline execution.[/yellow]")
            return
        
        # Confirm execution if cost is significant
        if cost_summary.total_estimated_cost > 1.0:
            if not click.confirm(f"Proceed with estimated cost of ${cost_summary.total_estimated_cost:.2f}?"):
                console.print("Pipeline execution cancelled.")
                return
        
        # Create executor
        if parallel:
            executor = ParallelPipelineExecutor(
                config=config,
                max_workers=max_workers,
                enable_parallel=True
            )
            console.print("[green]Using parallel execution[/green]")
        else:
            executor = PipelineExecutor(config=config)
            console.print("[yellow]Using sequential execution[/yellow]")
        
        # Execute pipeline
        console.print("\n[bold]Starting pipeline execution...[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            transient=False
        ) as progress:
            
            task = progress.add_task("Executing pipeline...", total=len(config.steps))
            
            # Run pipeline
            result = await executor.execute()
            
            progress.update(task, completed=len(config.steps))
        
        # Display results
        display_pipeline_results(result)
        
        if result.success:
            console.print(f"\n[green]✓ Pipeline completed successfully![/green]")
            console.print(f"Output directory: {result.output_directory}")
        else:
            console.print(f"\n[red]✗ Pipeline failed![/red]")
            if result.error:
                console.print(f"Error: {result.error}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        console.print(f"[red]✗ Execution failed: {e}[/red]")
        sys.exit(1)


@click.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--strict",
    is_flag=True,
    help="Enable strict validation mode"
)
def validate(config_file, strict):
    """Validate a pipeline configuration file."""
    logger = get_logger(__name__)
    
    try:
        console.print(f"[blue]Validating configuration: {config_file}[/blue]")
        
        # Load and validate configuration
        config_loader = ConfigLoader()
        config = config_loader.load_pipeline_config(config_file)
        
        validator = ConfigValidator()
        is_valid = validator.validate_pipeline_config(config)
        
        if is_valid:
            console.print("[green]✓ Configuration is valid[/green]")
            
            # Display configuration summary
            display_config_summary(config)
            
            # Check service availability
            check_service_requirements(config)
            
        else:
            console.print("[red]✗ Configuration validation failed[/red]")
            sys.exit(1)
            
    except (ConfigurationError, ValidationError) as e:
        console.print(f"[red]✗ Validation failed: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Validation error: {e}")
        console.print(f"[red]✗ Unexpected error: {e}[/red]")
        sys.exit(1)


@click.command()
@click.argument("config_file", type=click.Path(exists=True))
@click.option(
    "--detailed",
    is_flag=True,
    help="Show detailed cost breakdown"
)
@click.option(
    "--format",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format"
)
def cost(config_file, detailed, format):
    """Estimate costs for a pipeline configuration."""
    try:
        # Load configuration
        config_loader = ConfigLoader()
        config = config_loader.load_pipeline_config(config_file)
        
        # Calculate costs
        cost_calculator = CostCalculator()
        cost_summary = cost_calculator.estimate_pipeline_cost(
            _flatten_steps(config.steps)
        )
        
        if format == "json":
            # JSON output
            output = {
                "pipeline_name": config.pipeline_name,
                "total_cost": cost_summary.total_estimated_cost,
                "currency": cost_summary.currency,
                "by_service": {k.value: v for k, v in cost_summary.by_service.items()},
                "by_step_type": {k.value: v for k, v in cost_summary.by_step_type.items()},
                "estimates": [
                    {
                        "service": est.service.value,
                        "step_type": est.step_type.value,
                        "cost": est.estimated_cost,
                        "confidence": est.confidence,
                        "details": est.details
                    }
                    for est in cost_summary.estimates
                ]
            }
            click.echo(json.dumps(output, indent=2))
        else:
            # Table output
            display_cost_summary(cost_summary, detailed)
            
    except Exception as e:
        console.print(f"[red]✗ Cost estimation failed: {e}[/red]")
        sys.exit(1)


@click.group()
def config():
    """Configuration management commands."""
    pass


@config.command("create")
@click.option(
    "--template",
    type=click.Choice(["basic", "image", "video", "tts", "comprehensive"]),
    default="basic",
    help="Configuration template type"
)
@click.option(
    "--output",
    type=click.Path(),
    default="pipeline.yaml",
    help="Output file path"
)
def config_create(template, output):
    """Create a new pipeline configuration from template."""
    try:
        config_loader = ConfigLoader()
        
        # Define template step types
        template_steps = {
            "basic": ["text_to_image", "text_to_speech"],
            "image": ["text_to_image", "image_to_image"],
            "video": ["text_to_video", "video_generation"],
            "tts": ["text_to_speech"],
            "comprehensive": ["text_to_image", "image_to_image", "text_to_video", "text_to_speech", "avatar_generation"]
        }
        
        # Generate template
        template_config = config_loader.get_config_template(template_steps[template])
        
        # Save configuration
        output_path = config_loader.save_pipeline_config(
            template_config, 
            output, 
            format="yaml"
        )
        
        console.print(f"[green]✓[/green] Configuration template created: {output_path}")
        console.print("Edit the file to customize your pipeline.")
        
    except Exception as e:
        console.print(f"[red]✗ Template creation failed: {e}[/red]")
        sys.exit(1)


@config.command("validate")
@click.argument("config_file", type=click.Path(exists=True))
def config_validate(config_file):
    """Validate a configuration file."""
    # Reuse the main validate command
    ctx = click.get_current_context()
    ctx.invoke(validate, config_file=config_file)


@click.command()
@click.option(
    "--services",
    is_flag=True,
    help="Show available services and their status"
)
@click.option(
    "--steps",
    is_flag=True,
    help="Show available step types"
)
@click.option(
    "--models",
    is_flag=True,
    help="Show available AI models"
)
def info(services, steps, models):
    """Display platform information and capabilities."""
    if not any([services, steps, models]):
        # Show all information by default
        services = steps = models = True
    
    if services:
        display_service_info()
    
    if steps:
        display_step_info()
    
    if models:
        display_model_info()


def display_pipeline_info(config, is_dry_run=False):
    """Display pipeline information."""
    title = f"Pipeline: {config.pipeline_name}"
    if is_dry_run:
        title += " [DRY RUN]"
    
    panel_content = f"""
[bold]Description:[/bold] {config.description or 'No description'}
[bold]Steps:[/bold] {len(config.steps)}
[bold]Output Directory:[/bold] {config.output_directory}
"""
    
    if config.global_config:
        if "max_cost" in config.global_config:
            panel_content += f"\n[bold]Max Cost:[/bold] ${config.global_config['max_cost']:.2f}"
        if "timeout" in config.global_config:
            panel_content += f"\n[bold]Timeout:[/bold] {config.global_config['timeout']}s"
    
    console.print(Panel(panel_content, title=title, border_style="blue"))


def display_cost_summary(cost_summary, detailed=False):
    """Display cost estimation summary."""
    # Main cost table
    table = Table(title="Cost Estimation", show_header=True, header_style="bold magenta")
    table.add_column("Category")
    table.add_column("Cost (USD)", justify="right")
    
    table.add_row("Total Estimated Cost", f"${cost_summary.total_estimated_cost:.4f}")
    
    # By service
    for service, cost in cost_summary.by_service.items():
        table.add_row(f"  {service.value}", f"${cost:.4f}")
    
    console.print(table)
    
    if detailed:
        # Detailed breakdown
        detail_table = Table(title="Detailed Cost Breakdown")
        detail_table.add_column("Step Type")
        detail_table.add_column("Service") 
        detail_table.add_column("Cost", justify="right")
        detail_table.add_column("Confidence", justify="right")
        
        for est in cost_summary.estimates:
            detail_table.add_row(
                est.step_type.value,
                est.service.value,
                f"${est.estimated_cost:.4f}",
                f"{est.confidence:.0%}"
            )
        
        console.print(detail_table)


def display_pipeline_results(result):
    """Display pipeline execution results."""
    table = Table(title="Pipeline Results")
    table.add_column("Step")
    table.add_column("Status")
    table.add_column("Time", justify="right")
    table.add_column("Cost", justify="right")
    table.add_column("Output")
    
    for step_result in result.step_results:
        status = "[green]✓ Success[/green]" if step_result.success else "[red]✗ Failed[/red]"
        time_str = f"{step_result.execution_time:.1f}s"
        cost_str = f"${step_result.cost:.4f}"
        output = step_result.output_path or step_result.error or "N/A"
        
        table.add_row(
            step_result.step_id,
            status,
            time_str,
            cost_str,
            output
        )
    
    # Summary row
    table.add_section()
    total_time = result.execution_time
    total_cost = result.total_cost
    overall_status = "[green]✓ Success[/green]" if result.success else "[red]✗ Failed[/red]"
    
    table.add_row(
        "[bold]TOTAL[/bold]",
        overall_status,
        f"[bold]{total_time:.1f}s[/bold]",
        f"[bold]${total_cost:.4f}[/bold]",
        f"[bold]{result.output_directory}[/bold]"
    )
    
    console.print(table)


def display_config_summary(config):
    """Display configuration summary."""
    tree = Tree(f"Pipeline: {config.pipeline_name}")
    
    for i, step in enumerate(config.steps):
        if hasattr(step, 'parallel_steps'):
            # Parallel step
            branch = tree.add(f"[yellow]Parallel Group {i+1}[/yellow]")
            for sub_step in step.parallel_steps:
                branch.add(f"{sub_step.name} ({sub_step.step_type.value})")
        else:
            # Regular step
            tree.add(f"{step.name} ({step.step_type.value})")
    
    console.print(tree)


def check_service_requirements(config):
    """Check if required services are available."""
    from ai_content_platform.cli.main import check_service_availability
    
    services = check_service_availability()
    required_services = set()
    
    # Determine required services from steps
    for step in _flatten_steps(config.steps):
        if step.step_type.value in ["text_to_image", "image_to_image", "text_to_video", "video_generation", "avatar_generation"]:
            required_services.add("FAL AI")
        elif step.step_type.value == "text_to_speech":
            required_services.add("ElevenLabs")
    
    # Check availability
    missing_services = []
    for service in required_services:
        if not services.get(service, False):
            missing_services.append(service)
    
    if missing_services:
        console.print(f"[yellow]⚠ Missing API keys for: {', '.join(missing_services)}[/yellow]")
        console.print("Add the required API keys to your environment variables.")
    else:
        console.print("[green]✓ All required services are available[/green]")


def display_service_info():
    """Display available services information."""
    from ai_content_platform.cli.main import check_service_availability
    
    services = check_service_availability()
    
    table = Table(title="Available Services", show_header=True)
    table.add_column("Service")
    table.add_column("Status")
    table.add_column("Capabilities")
    
    service_capabilities = {
        "FAL AI": "Images, Videos, Avatars",
        "ElevenLabs": "Text-to-Speech",
        "Google Vertex AI": "Veo Video Generation",
        "OpenRouter": "Alternative TTS & Chat"
    }
    
    for service, available in services.items():
        status = "[green]✓ Available[/green]" if available else "[red]✗ Not Available[/red]"
        capabilities = service_capabilities.get(service, "Unknown")
        table.add_row(service, status, capabilities)
    
    console.print(table)


def display_step_info():
    """Display available step types."""
    available_steps = StepFactory.get_available_steps()
    
    table = Table(title="Available Step Types")
    table.add_column("Step Type")
    table.add_column("Description")
    
    step_descriptions = {
        "text_to_image": "Generate images from text prompts",
        "image_to_image": "Transform existing images",
        "text_to_video": "Create videos from text descriptions",
        "video_generation": "Generate videos with advanced models",
        "text_to_speech": "Convert text to audio",
        "avatar_generation": "Create talking avatar videos",
        "parallel_group": "Execute multiple steps in parallel"
    }
    
    for step_type in available_steps:
        description = step_descriptions.get(step_type.value, "Advanced AI processing")
        table.add_row(step_type.value, description)
    
    console.print(table)


def display_model_info():
    """Display available AI models."""
    console.print(Panel("AI Models by Service", border_style="green"))
    
    # FAL AI Models
    console.print("\n[bold cyan]FAL AI Models:[/bold cyan]")
    fal_models = {
        "Text-to-Image": ["imagen-4", "seedream-v3", "flux-1-schnell", "flux-1-dev"],
        "Text-to-Video": ["minimax-hailuo-02-pro", "google-veo-3"],
        "Video Generation": ["minimax-hailuo-02", "kling-video-2-1"],
        "Image-to-Image": ["luma-photon-flash"]
    }
    
    for category, models in fal_models.items():
        console.print(f"  {category}: {', '.join(models)}")
    
    # ElevenLabs Voices
    console.print("\n[bold cyan]ElevenLabs Voices:[/bold cyan]")
    from ai_content_platform.services.elevenlabs import ElevenLabsTTSStep
    popular_voices = ElevenLabsTTSStep.get_popular_voices()
    for voice_id, name in list(popular_voices.items())[:5]:
        console.print(f"  {name}")
    console.print(f"  ... and {len(popular_voices) - 5} more voices")


def _flatten_steps(steps):
    """Flatten step configurations for processing."""
    flattened = []
    for step in steps:
        if hasattr(step, 'parallel_steps'):
            flattened.extend(step.parallel_steps)
        else:
            flattened.append(step)
    return flattened