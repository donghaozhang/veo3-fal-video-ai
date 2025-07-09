#!/usr/bin/env python3
"""
Enhanced command line interface for video tools.

Uses the new class-based architecture for improved maintainability and functionality.
Provides both interactive menu and direct command execution modes.
"""

import sys
from pathlib import Path

# Add video_utils to Python path
sys.path.insert(0, str(Path(__file__).parent / "video_utils"))

from video_utils.command_dispatcher import main

if __name__ == "__main__":
    main()