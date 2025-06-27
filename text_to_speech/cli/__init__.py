"""
Command Line Interface Module

Interactive command line tools and quick start utilities.

Components:
- interactive: Interactive pipeline interface (moved from interactive_pipeline.py)
- quick_start: Quick demo runner (moved from quick_start.py)
"""

# Import main functions for easy access
try:
    from .interactive import main as interactive_main
    from .quick_start import main as quick_start_main
    __all__ = ["interactive_main", "quick_start_main"]
except ImportError:
    # Graceful fallback if imports fail
    __all__ = []