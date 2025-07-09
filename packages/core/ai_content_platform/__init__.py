"""AI Content Platform - Comprehensive AI content generation framework."""

from .__version__ import (
    __version__,
    __author__, 
    __email__,
    __description__,
    __url__
)

# Core imports
from .core import (
    # Models
    StepType,
    StepConfig,
    ParallelStepConfig, 
    PipelineConfig,
    StepResult,
    PipelineResult,
    
    # Exceptions
    AIPlatformError,
    ConfigurationError,
    ValidationError,
    StepExecutionError,
    PipelineExecutionError,
    
    # Core classes
    BaseStep,
    StepFactory,
    PipelineExecutor,
    ParallelPipelineExecutor
)

# Utility imports
from .utils import (
    get_logger,
    setup_logging,
    FileManager,
    ConfigValidator,
    InputValidator,
    CostCalculator,
    ConfigLoader
)

# Main public API
__all__ = [
    # Package info
    "__version__",
    "__author__",
    "__email__",
    "__description__",
    "__url__",
    
    # Models
    "StepType",
    "StepConfig",
    "ParallelStepConfig", 
    "PipelineConfig",
    "StepResult",
    "PipelineResult",
    
    # Exceptions
    "AIPlatformError",
    "ConfigurationError",
    "ValidationError",
    "StepExecutionError",
    "PipelineExecutionError",
    
    # Core classes
    "BaseStep",
    "StepFactory",
    "PipelineExecutor",
    "ParallelPipelineExecutor",
    
    # Utilities
    "get_logger",
    "setup_logging",
    "FileManager",
    "ConfigValidator",
    "InputValidator",
    "CostCalculator",
    "ConfigLoader"
]

# Initialize step registry on import
def _initialize_platform():
    """Initialize the platform and register all step types."""
    try:
        from .core.registry import initialize_registry
        initialize_registry()
    except Exception:
        # Fail silently during import - registry can be initialized manually
        pass

_initialize_platform()