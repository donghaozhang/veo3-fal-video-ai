"""Step type registry for automatic registration of service implementations."""

from ai_content_platform.core.models import StepType
from ai_content_platform.core.step import StepFactory
from ai_content_platform.utils.logger import get_logger


def register_all_steps():
    """Register all available step implementations with the StepFactory."""
    logger = get_logger(__name__)
    
    try:
        # Import service implementations
        from ai_content_platform.services.fal_ai import (
            FALTextToImageStep,
            FALImageToImageStep,
            FALTextToVideoStep,
            FALVideoGenerationStep,
            FALAvatarGenerationStep
        )
        from ai_content_platform.services.elevenlabs import ElevenLabsTTSStep
        from ai_content_platform.services.google import GoogleVeoStep, GoogleGeminiStep
        from ai_content_platform.services.openrouter import OpenRouterTTSStep, OpenRouterChatStep
        
        # Register FAL AI steps
        StepFactory.register_step(StepType.TEXT_TO_IMAGE, FALTextToImageStep)
        StepFactory.register_step(StepType.IMAGE_TO_IMAGE, FALImageToImageStep)
        StepFactory.register_step(StepType.TEXT_TO_VIDEO, FALTextToVideoStep)
        StepFactory.register_step(StepType.VIDEO_GENERATION, FALVideoGenerationStep)
        StepFactory.register_step(StepType.AVATAR_GENERATION, FALAvatarGenerationStep)
        
        # Register TTS steps (default to ElevenLabs, can be overridden)
        StepFactory.register_step(StepType.TEXT_TO_SPEECH, ElevenLabsTTSStep)
        
        # Register Google steps
        StepFactory.register_step(StepType.VIDEO_GENERATION_VEO, GoogleVeoStep)
        StepFactory.register_step(StepType.TEXT_GENERATION, GoogleGeminiStep)
        
        # Log successful registration
        registered_types = StepFactory.get_available_steps()
        logger.success(f"Registered {len(registered_types)} step types: {[t.value for t in registered_types]}")
        
    except ImportError as e:
        logger.warning(f"Some service modules not available: {e}")
    except Exception as e:
        logger.error(f"Failed to register steps: {e}")


def register_step_provider_variant(step_type: StepType, provider: str, step_class):
    """Register a provider-specific variant of a step type.
    
    This allows multiple implementations of the same step type from different providers.
    """
    logger = get_logger(__name__)
    
    try:
        # Create a provider-specific step type variant
        variant_key = f"{step_type.value}_{provider}"
        StepFactory._step_registry[variant_key] = step_class
        
        logger.info(f"Registered {provider} variant for {step_type.value}")
        
    except Exception as e:
        logger.error(f"Failed to register {provider} variant for {step_type.value}: {e}")


def get_step_providers(step_type: StepType) -> list:
    """Get list of available providers for a step type.
    
    Args:
        step_type: The step type to check
        
    Returns:
        List of available provider names
    """
    providers = []
    
    # Check for provider variants in registry
    for key in StepFactory._step_registry.keys():
        if isinstance(key, str) and key.startswith(f"{step_type.value}_"):
            provider = key.replace(f"{step_type.value}_", "")
            providers.append(provider)
        elif key == step_type:
            providers.append("default")
    
    return providers


def create_step_with_provider(step_config, provider: str = None):
    """Create step instance with specific provider.
    
    Args:
        step_config: Step configuration
        provider: Optional provider name (e.g., 'elevenlabs', 'openrouter')
        
    Returns:
        Step instance
    """
    if provider:
        # Try provider-specific variant first
        variant_key = f"{step_config.step_type.value}_{provider}"
        if variant_key in StepFactory._step_registry:
            step_class = StepFactory._step_registry[variant_key]
            return step_class(step_config)
    
    # Fall back to default
    return StepFactory.create_step(step_config)


# Register alternative providers for flexible step creation
def register_alternative_providers():
    """Register alternative providers for step types."""
    logger = get_logger(__name__)
    
    try:
        from ai_content_platform.services.openrouter import OpenRouterTTSStep, OpenRouterChatStep
        
        # Register OpenRouter as alternative TTS provider
        register_step_provider_variant(StepType.TEXT_TO_SPEECH, "openrouter", OpenRouterTTSStep)
        register_step_provider_variant(StepType.TEXT_GENERATION, "openrouter", OpenRouterChatStep)
        
        logger.info("Registered alternative providers successfully")
        
    except ImportError as e:
        logger.warning(f"Alternative providers not available: {e}")
    except Exception as e:
        logger.error(f"Failed to register alternative providers: {e}")


def initialize_registry():
    """Initialize the complete step registry."""
    logger = get_logger(__name__)
    
    logger.info("Initializing AI Content Platform step registry...")
    
    # Register all main step implementations
    register_all_steps()
    
    # Register alternative providers
    register_alternative_providers()
    
    logger.success("Step registry initialization completed")