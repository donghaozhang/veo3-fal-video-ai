"""OpenRouter AI service integration for TTS and other services."""

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, Optional

import openai
import aiofiles
import aiohttp

from ai_content_platform.core.step import BaseStep
from ai_content_platform.core.models import StepConfig, StepResult
from ai_content_platform.core.exceptions import StepExecutionError
from ai_content_platform.utils.logger import get_logger


class OpenRouterTTSStep(BaseStep):
    """OpenRouter text-to-speech generation step."""
    
    def __init__(self, config: StepConfig):
        super().__init__(config)
        self.logger = get_logger(__name__)
        
        # Initialize OpenRouter client
        api_key = self.config.parameters.get("api_key") or self._get_api_key_from_env()
        if api_key:
            self.client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )
        else:
            raise StepExecutionError("OpenRouter API key not found")
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables."""
        import os
        return os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    def validate_config(self) -> bool:
        """Validate OpenRouter TTS configuration."""
        required_params = ["text"]
        
        for param in required_params:
            if param not in self.config.parameters:
                self.logger.error(f"Missing required parameter: {param}")
                return False
        
        return True
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute text-to-speech generation via OpenRouter."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating speech via OpenRouter: {self.config.name}")
            
            # Get parameters
            text = self.config.parameters["text"]
            model = self.config.parameters.get("model", "openai/tts-1")
            voice = self.config.parameters.get("voice", "alloy")
            
            # Generate audio using OpenRouter
            self.logger.info(f"Generating speech with model: {model}, voice: {voice}")
            
            response = await asyncio.to_thread(
                self.client.audio.speech.create,
                model=model,
                voice=voice,
                input=text,
                response_format=self.config.parameters.get("format", "mp3")
            )
            
            # Save audio file
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            audio_format = self.config.parameters.get("format", "mp3")
            output_path = output_dir / f"{self.config.name}_{int(time.time())}.{audio_format}"
            
            # Write audio data
            async with aiofiles.open(output_path, 'wb') as f:
                await f.write(response.content)
            
            self.logger.success(f"Speech generated: {output_path}")
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "text": text,
                    "model": model,
                    "voice": voice,
                    "format": audio_format,
                    "character_count": len(text),
                    "provider": "openrouter"
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"OpenRouter TTS generation failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    def estimate_cost(self) -> float:
        """Estimate cost for OpenRouter TTS generation."""
        text = self.config.parameters.get("text", "")
        character_count = len(text)
        
        # OpenRouter pricing varies, approximate $0.10 per request
        return max(0.05, 0.10)
    
    @classmethod
    def get_available_models(cls) -> Dict[str, Dict[str, Any]]:
        """Get available TTS models on OpenRouter."""
        return {
            "openai/tts-1": {
                "name": "OpenAI TTS-1",
                "description": "OpenAI's text-to-speech model",
                "voices": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                "formats": ["mp3", "opus", "aac", "flac"]
            },
            "openai/tts-1-hd": {
                "name": "OpenAI TTS-1 HD",
                "description": "Higher quality OpenAI text-to-speech",
                "voices": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                "formats": ["mp3", "opus", "aac", "flac"]
            }
        }


class OpenRouterChatStep(BaseStep):
    """OpenRouter chat/completion step for text generation."""
    
    def __init__(self, config: StepConfig):
        super().__init__(config)
        self.logger = get_logger(__name__)
        
        # Initialize OpenRouter client
        api_key = self.config.parameters.get("api_key") or self._get_api_key_from_env()
        if api_key:
            self.client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
            )
        else:
            raise StepExecutionError("OpenRouter API key not found")
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables."""
        import os
        return os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    def validate_config(self) -> bool:
        """Validate OpenRouter chat configuration."""
        required_params = ["prompt"]
        
        for param in required_params:
            if param not in self.config.parameters:
                self.logger.error(f"Missing required parameter: {param}")
                return False
        
        return True
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute chat completion via OpenRouter."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating text via OpenRouter: {self.config.name}")
            
            # Get parameters
            prompt = self.config.parameters["prompt"]
            model = self.config.parameters.get("model", "openai/gpt-3.5-turbo")
            max_tokens = self.config.parameters.get("max_tokens", 1000)
            temperature = self.config.parameters.get("temperature", 0.7)
            
            # Create messages
            messages = [{"role": "user", "content": prompt}]
            
            # Add system message if provided
            if "system_prompt" in self.config.parameters:
                messages.insert(0, {
                    "role": "system", 
                    "content": self.config.parameters["system_prompt"]
                })
            
            # Generate completion
            self.logger.info(f"Generating completion with model: {model}")
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract generated text
            generated_text = response.choices[0].message.content
            
            # Save text file
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"{self.config.name}_{int(time.time())}.txt"
            
            async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
                await f.write(generated_text)
            
            self.logger.success(f"Text generated: {output_path}")
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "prompt": prompt,
                    "model": model,
                    "generated_text": generated_text,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "token_usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    },
                    "provider": "openrouter"
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"OpenRouter chat completion failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    def estimate_cost(self) -> float:
        """Estimate cost for OpenRouter chat completion."""
        prompt = self.config.parameters.get("prompt", "")
        max_tokens = self.config.parameters.get("max_tokens", 1000)
        
        # Rough estimation based on token count
        # Approximate 4 characters per token, $0.002 per 1000 tokens
        estimated_tokens = len(prompt) / 4 + max_tokens
        return max(0.001, (estimated_tokens / 1000) * 0.002)