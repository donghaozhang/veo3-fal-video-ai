"""Enhanced logging system with Rich support."""

import logging
import sys
from pathlib import Path
from typing import Optional, Union

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install


class PlatformLogger:
    """Enhanced logger with Rich formatting."""
    
    def __init__(self, name: str, level: str = "INFO"):
        self.name = name
        self.level = level
        self.console = Console()
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger with Rich handler."""
        logger = logging.getLogger(self.name)
        logger.setLevel(getattr(logging, self.level.upper()))
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Add Rich handler
        rich_handler = RichHandler(
            console=self.console,
            show_time=True,
            show_path=True,
            markup=True,
            rich_tracebacks=True
        )
        rich_handler.setFormatter(
            logging.Formatter(
                fmt="%(message)s",
                datefmt="[%X]"
            )
        )
        logger.addHandler(rich_handler)
        
        return logger
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(f"[yellow]{message}[/yellow]", **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(f"[red]{message}[/red]", **kwargs)
    
    def success(self, message: str, **kwargs):
        """Log success message."""
        self.logger.info(f"[green]✓ {message}[/green]", **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(f"[dim]{message}[/dim]", **kwargs)
    
    def step(self, message: str, **kwargs):
        """Log step message with special formatting."""
        self.logger.info(f"[bold blue]→ {message}[/bold blue]", **kwargs)
    
    def cost(self, amount: float, currency: str = "USD", **kwargs):
        """Log cost information."""
        self.logger.info(f"[yellow]💰 Cost: ${amount:.4f} {currency}[/yellow]", **kwargs)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Union[str, Path]] = None,
    rich_tracebacks: bool = True
) -> None:
    """Setup global logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file to write logs to
        rich_tracebacks: Enable Rich traceback formatting
    """
    if rich_tracebacks:
        install(show_locals=True)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Add console handler with Rich
    console_handler = RichHandler(
        console=Console(),
        show_time=True,
        show_path=True,
        markup=True,
        rich_tracebacks=rich_tracebacks
    )
    console_handler.setFormatter(
        logging.Formatter(fmt="%(message)s", datefmt="[%X]")
    )
    root_logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        file_path = Path(log_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        root_logger.addHandler(file_handler)


def get_logger(name: str, level: str = "INFO") -> PlatformLogger:
    """Get a configured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level
        
    Returns:
        Configured PlatformLogger instance
    """
    return PlatformLogger(name, level)