"""
Pipeline-specific Data Models

Data models and configurations specific to the OpenRouter TTS pipeline.
"""

from typing import Dict, List, Optional, Union, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class OpenRouterModel(Enum):
    """Top OpenRouter models based on performance"""
    CLAUDE_SONNET_4 = "anthropic/claude-3.5-sonnet"
    GEMINI_2_FLASH = "google/gemini-2.0-flash-exp"
    GEMINI_25_FLASH_PREVIEW = "google/gemini-2.5-flash-preview"
    GEMINI_2_FLASH_LITE = "google/gemini-2.0-flash-lite"
    DEEPSEEK_V3_FREE = "deepseek/deepseek-v3-0324-free"
    DEEPSEEK_V3 = "deepseek/deepseek-v3-0324"
    GEMINI_25_FLASH_LITE = "google/gemini-2.5-flash-lite-preview"
    CLAUDE_37_SONNET = "anthropic/claude-3.7-sonnet"
    GEMINI_25_FLASH = "google/gemini-2.5-flash"
    GEMINI_25_PRO = "google/gemini-2.5-pro"


class ContentType(Enum):
    """Content types for pipeline generation"""
    CONVERSATION = "conversation"
    PRESENTATION = "presentation"
    INTERVIEW = "interview"
    STORY = "story"
    DIALOGUE = "dialogue"
    MONOLOGUE = "monologue"


class VoiceStyle(Enum):
    """Voice style presets for different scenarios"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    DRAMATIC = "dramatic"
    AUTHORITATIVE = "authoritative"
    CONVERSATIONAL = "conversational"


@dataclass
class PipelineInput:
    """Input configuration for the pipeline"""
    description: str  # Description of person(s)
    num_people: int = 1  # Number of speakers
    length_minutes: float = 1.0  # Desired length in minutes
    content_type: ContentType = ContentType.CONVERSATION
    voice_style: VoiceStyle = VoiceStyle.CONVERSATIONAL
    model: OpenRouterModel = OpenRouterModel.CLAUDE_SONNET_4
    
    def __post_init__(self):
        """Validate inputs after initialization"""
        if self.num_people < 1:
            raise ValueError("Number of people must be at least 1")
        if self.length_minutes <= 0:
            raise ValueError("Length must be positive")


@dataclass
class GeneratedContent:
    """Container for generated content from LLM"""
    title: str
    content: str
    speakers: List[str]
    estimated_duration: float
    word_count: int
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        """Calculate word count if not provided"""
        if self.word_count == 0:
            self.word_count = len(self.content.split())


@dataclass
class PipelineResult:
    """Complete pipeline result"""
    input_config: PipelineInput
    generated_content: GeneratedContent
    audio_file: Optional[str]
    processing_time: float
    success: bool
    error_message: Optional[str] = None


@dataclass
class LengthCalculation:
    """Length estimation for content generation"""
    target_minutes: float
    estimated_words: int
    estimated_tokens: int
    speaking_rate_wpm: int = 150  # Words per minute
    
    def __post_init__(self):
        """Calculate estimates based on target minutes"""
        self.estimated_words = int(self.target_minutes * self.speaking_rate_wpm)
        # Rough estimate: 1 token ≈ 0.75 words
        self.estimated_tokens = int(self.estimated_words / 0.75)


# Model performance characteristics
MODEL_CHARACTERISTICS = {
    OpenRouterModel.CLAUDE_SONNET_4: {
        "quality": "highest",
        "speed": "medium",
        "cost": "high",
        "context_length": 200000,
        "strengths": ["reasoning", "analysis", "creative_writing"],
        "best_for": ["complex_dialogues", "analytical_content", "creative_stories"]
    },
    OpenRouterModel.GEMINI_2_FLASH: {
        "quality": "high",
        "speed": "fast", 
        "cost": "medium",
        "context_length": 1000000,
        "strengths": ["speed", "multimodal", "long_context"],
        "best_for": ["real_time_content", "long_form_content", "presentations"]
    },
    OpenRouterModel.DEEPSEEK_V3_FREE: {
        "quality": "good",
        "speed": "fast",
        "cost": "free",
        "context_length": 64000,
        "strengths": ["cost_effective", "coding", "reasoning"],
        "best_for": ["technical_content", "cost_conscious_projects", "prototyping"]
    }
}


# Content type templates and configurations
CONTENT_TYPE_CONFIGS = {
    ContentType.CONVERSATION: {
        "structure": "natural_dialogue",
        "turn_length": "medium",
        "formality": "casual_to_medium",
        "interaction_style": "back_and_forth"
    },
    ContentType.PRESENTATION: {
        "structure": "structured_points",
        "turn_length": "long",
        "formality": "formal_to_medium",
        "interaction_style": "monologue_with_q_and_a"
    },
    ContentType.INTERVIEW: {
        "structure": "question_answer",
        "turn_length": "varied",
        "formality": "medium",
        "interaction_style": "guided_conversation"
    },
    ContentType.STORY: {
        "structure": "narrative",
        "turn_length": "long",
        "formality": "varied",
        "interaction_style": "storytelling"
    }
}


# Voice style configurations
VOICE_STYLE_CONFIGS = {
    VoiceStyle.PROFESSIONAL: {
        "primary_voices": ["rachel", "drew"],
        "tone": "formal",
        "pace": "measured",
        "emotion": "neutral_positive"
    },
    VoiceStyle.CASUAL: {
        "primary_voices": ["bella", "antoni"],
        "tone": "friendly",
        "pace": "natural",
        "emotion": "warm"
    },
    VoiceStyle.DRAMATIC: {
        "primary_voices": ["elli", "josh"],
        "tone": "expressive",
        "pace": "varied",
        "emotion": "dynamic"
    },
    VoiceStyle.AUTHORITATIVE: {
        "primary_voices": ["arnold", "clyde"],
        "tone": "commanding",
        "pace": "deliberate",
        "emotion": "confident"
    },
    VoiceStyle.CONVERSATIONAL: {
        "primary_voices": ["sam", "adam"],
        "tone": "natural",
        "pace": "comfortable",
        "emotion": "engaging"
    }
}


def get_model_info(model: OpenRouterModel) -> Dict[str, Any]:
    """Get detailed information about a model"""
    return MODEL_CHARACTERISTICS.get(model, {})


def get_content_type_config(content_type: ContentType) -> Dict[str, str]:
    """Get configuration for a content type"""
    return CONTENT_TYPE_CONFIGS.get(content_type, {})


def get_voice_style_config(voice_style: VoiceStyle) -> Dict[str, Any]:
    """Get configuration for a voice style"""
    return VOICE_STYLE_CONFIGS.get(voice_style, {})