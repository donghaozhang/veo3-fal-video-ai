"""
Dialogue Generation Module

Advanced multi-speaker dialogue generation with emotional context and voice pairing.

Components:
- controller: Main dialogue controller
- emotional_tags: Emotion management and context
- voice_pairs: Voice combination presets
"""

from .controller import ElevenLabsDialogueController

__all__ = ["ElevenLabsDialogueController"]