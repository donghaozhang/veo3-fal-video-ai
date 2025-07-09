"""ElevenLabs text-to-speech service integration."""

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, Optional

from elevenlabs import Voice, VoiceSettings, generate, save
from elevenlabs.client import ElevenLabs

from ai_content_platform.core.step import BaseStep
from ai_content_platform.core.models import StepConfig, StepResult
from ai_content_platform.core.exceptions import StepExecutionError
from ai_content_platform.utils.logger import get_logger


class ElevenLabsTTSStep(BaseStep):
    """ElevenLabs text-to-speech generation step."""
    
    def __init__(self, config: StepConfig):
        super().__init__(config)
        self.logger = get_logger(__name__)
        
        # Initialize ElevenLabs client
        api_key = self.config.parameters.get("api_key") or self._get_api_key_from_env()
        if api_key:
            self.client = ElevenLabs(api_key=api_key)
        else:
            raise StepExecutionError("ElevenLabs API key not found")
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variables."""
        import os
        return os.getenv("ELEVENLABS_API_KEY") or os.getenv("ELEVEN_API_KEY")
    
    def validate_config(self) -> bool:
        """Validate ElevenLabs TTS configuration."""
        required_params = ["text"]
        
        for param in required_params:
            if param not in self.config.parameters:
                self.logger.error(f"Missing required parameter: {param}")
                return False
        
        # Validate voice settings if provided
        if "voice_settings" in self.config.parameters:
            settings = self.config.parameters["voice_settings"]
            if not isinstance(settings, dict):
                self.logger.error("voice_settings must be a dictionary")
                return False
        
        return True
    
    async def execute(self, context: Dict[str, Any]) -> StepResult:
        """Execute text-to-speech generation."""
        start_time = time.time()
        
        try:
            self.logger.step(f"Generating speech: {self.config.name}")
            
            # Get parameters
            text = self.config.parameters["text"]
            voice_id = self.config.parameters.get("voice_id", "EXAVITQu4vr4xnSDxMaL")  # Default Bella voice
            
            # Voice settings
            voice_settings = self.config.parameters.get("voice_settings", {})
            settings = VoiceSettings(
                stability=voice_settings.get("stability", 0.5),
                similarity_boost=voice_settings.get("similarity_boost", 0.5),
                style=voice_settings.get("style", 0.0),
                use_speaker_boost=voice_settings.get("use_speaker_boost", True)
            )
            
            # Generate audio
            self.logger.info(f"Generating speech with voice: {voice_id}")
            
            audio = await asyncio.to_thread(
                generate,
                text=text,
                voice=Voice(voice_id=voice_id, settings=settings),
                model=self.config.parameters.get("model", "eleven_monolingual_v1")
            )
            
            # Save audio file
            output_dir = context["output_directory"] / self.config.name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"{self.config.name}_{int(time.time())}.mp3"
            
            await asyncio.to_thread(save, audio, str(output_path))
            
            self.logger.success(f"Speech generated: {output_path}")
            
            return self._create_result(
                success=True,
                output_path=str(output_path),
                metadata={
                    "text": text,
                    "voice_id": voice_id,
                    "voice_settings": voice_settings,
                    "model": self.config.parameters.get("model", "eleven_monolingual_v1"),
                    "character_count": len(text),
                    "audio_format": "mp3"
                },
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"Text-to-speech generation failed: {str(e)}"
            self.logger.error(error_msg)
            return self._create_result(
                success=False,
                error=error_msg,
                execution_time=time.time() - start_time
            )
    
    def estimate_cost(self) -> float:
        """Estimate cost for text-to-speech generation."""
        text = self.config.parameters.get("text", "")
        character_count = len(text)
        
        # ElevenLabs pricing is approximately $0.18 per 1000 characters
        return max(0.001, (character_count / 1000) * 0.18)
    
    def get_available_voices(self) -> Dict[str, Any]:
        """Get list of available voices."""
        try:
            voices = self.client.voices.get_all()
            return {
                voice.voice_id: {
                    "name": voice.name,
                    "category": voice.category,
                    "description": getattr(voice, "description", ""),
                    "language": getattr(voice, "language", "en"),
                    "gender": getattr(voice, "gender", "unknown")
                }
                for voice in voices.voices
            }
        except Exception as e:
            self.logger.error(f"Failed to get voices: {str(e)}")
            return {}
    
    @classmethod
    def get_popular_voices(cls) -> Dict[str, str]:
        """Get popular voice IDs and names."""
        return {
            "EXAVITQu4vr4xnSDxMaL": "Bella (Female, Young)",
            "21m00Tcm4TlvDq8ikWAM": "Rachel (Female, Young)",
            "AZnzlk1XvdvUeBnXmlld": "Domi (Female, Young)", 
            "ErXwobaYiN019PkySvjV": "Antoni (Male, Young)",
            "VR6AewLTigWG4xSOukaG": "Arnold (Male, Middle-aged)",
            "pNInz6obpgDQGcFmaJgB": "Adam (Male, Deep)",
            "yoZ06aMxZJJ28mfd3POQ": "Sam (Male, Young)",
            "2EiwWnXFnvU5JabPnv8n": "Clyde (Male, Middle-aged)",
            "CYw3kZ02Hs0563khs1Fj": "Dave (Male, British)",
            "JBFqnCBsd6RMkjVDRZzb": "George (Male, British)"
        }