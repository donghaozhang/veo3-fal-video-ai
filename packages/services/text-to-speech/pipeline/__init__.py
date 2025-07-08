"""
OpenRouter Pipeline Module

Complete AI content generation pipeline from description to speech using OpenRouter models.

Components:
- core: Main pipeline orchestration
- content_generator: LLM integration for content generation
- content_processor: Content processing for TTS
- templates: Content templates and configurations
"""

from .core import OpenRouterTTSPipeline

__all__ = ["OpenRouterTTSPipeline"]