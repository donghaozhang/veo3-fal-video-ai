"""
Text-to-speech generation models for AI Content Pipeline

Provides unified interface for text-to-speech generation using ElevenLabs API.
"""

import os
import sys
import subprocess
import json
import time
from typing import Dict, Any, Optional, Tuple
from pathlib import Path


class UnifiedTextToSpeechGenerator:
    """
    Unified text-to-speech generator supporting multiple ElevenLabs models.
    
    Integrates with the existing text-to-speech CLI system for consistent
    voice generation and pipeline compatibility.
    """
    
    def __init__(self):
        """Initialize the TTS generator."""
        self.tts_path = Path("/home/zdhpe/veo3-video-generation/text_to_speech")
        self.supported_models = ["elevenlabs", "elevenlabs_turbo", "elevenlabs_v3"]
        self.supported_voices = [
            "rachel", "drew", "bella", "antoni", "elli", 
            "josh", "arnold", "adam", "sam", "clyde"
        ]
        
    def generate(
        self,
        prompt: str,
        model: str = "elevenlabs",
        voice: str = "rachel",
        speed: float = 1.0,
        stability: float = 0.5,
        similarity_boost: float = 0.8,
        style: float = 0.2,
        output_file: Optional[str] = None,
        **kwargs
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Generate speech from text using ElevenLabs TTS.
        
        Args:
            prompt: Text to convert to speech
            model: TTS model to use (elevenlabs, elevenlabs_turbo, elevenlabs_v3)
            voice: Voice name to use
            speed: Speech speed (0.7-1.2)
            stability: Voice stability (0.0-1.0)
            similarity_boost: Voice similarity boost (0.0-1.0)
            style: Style exaggeration (0.0-1.0)
            output_file: Output filename (optional)
            **kwargs: Additional parameters
            
        Returns:
            Tuple of (success, result_dict)
        """
        try:
            # Validate inputs
            if not prompt or not prompt.strip():
                return False, {"error": "Empty prompt provided"}
                
            if model not in self.supported_models:
                return False, {"error": f"Unsupported model: {model}. Supported: {self.supported_models}"}
                
            if voice not in self.supported_voices:
                return False, {"error": f"Unsupported voice: {voice}. Supported: {self.supported_voices}"}
                
            # Validate parameter ranges
            if not 0.7 <= speed <= 1.2:
                return False, {"error": "Speed must be between 0.7 and 1.2"}
                
            for param, name in [
                (stability, "stability"), (similarity_boost, "similarity_boost"), (style, "style")
            ]:
                if not 0.0 <= param <= 1.0:
                    return False, {"error": f"{name} must be between 0.0 and 1.0"}
            
            # Generate output filename if not provided
            if not output_file:
                timestamp = int(time.time())
                output_file = f"pipeline_tts_{voice}_{timestamp}.mp3"
            
            # Use CLI wrapper for generation (ensures consistency)
            result = self._call_tts_cli(
                text=prompt,
                voice=voice,
                output_file=output_file,
                speed=speed,
                stability=stability,
                similarity_boost=similarity_boost,
                style=style
            )
            
            if result["success"]:
                return True, {
                    "output_file": result["output_file"],
                    "voice_used": result["voice_used"],
                    "text_length": result["text_length"],
                    "model": model,
                    "settings": result["settings"],
                    "processing_time": result.get("processing_time", 15)
                }
            else:
                return False, {"error": result.get("error", "TTS generation failed")}
                
        except Exception as e:
            return False, {"error": f"TTS generation error: {str(e)}"}
    
    def _call_tts_cli(
        self,
        text: str,
        voice: str,
        output_file: str,
        speed: float,
        stability: float,
        similarity_boost: float,
        style: float
    ) -> Dict[str, Any]:
        """
        Call the TTS CLI wrapper for speech generation.
        
        Args:
            text: Text to convert
            voice: Voice name
            output_file: Output filename
            speed: Speech speed
            stability: Voice stability
            similarity_boost: Similarity boost
            style: Style exaggeration
            
        Returns:
            Result dictionary from CLI
        """
        try:
            # Build command for CLI wrapper
            cmd = [
                "python", "examples/tts_cli_wrapper.py",
                text, voice, output_file,
                "--speed", str(speed),
                "--stability", str(stability),
                "--similarity-boost", str(similarity_boost),
                "--style", str(style),
                "--json"
            ]
            
            # Execute CLI command
            start_time = time.time()
            result = subprocess.run(
                cmd,
                cwd=str(self.tts_path),
                capture_output=True,
                text=True,
                timeout=60
            )
            processing_time = time.time() - start_time
            
            if result.returncode == 0:
                # Parse JSON response - extract only the JSON part
                stdout_text = result.stdout.strip()
                
                # Find JSON block - look for opening brace and matching closing brace
                json_start_pos = stdout_text.find('{')
                if json_start_pos >= 0:
                    # Count braces to find the matching close
                    brace_count = 0
                    json_end_pos = -1
                    
                    for i in range(json_start_pos, len(stdout_text)):
                        if stdout_text[i] == '{':
                            brace_count += 1
                        elif stdout_text[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                json_end_pos = i
                                break
                    
                    if json_end_pos > json_start_pos:
                        json_text = stdout_text[json_start_pos:json_end_pos+1]
                        
                        try:
                            response = json.loads(json_text)
                            response["processing_time"] = processing_time
                            return response
                        except json.JSONDecodeError as e:
                            return {
                                "success": False,
                                "error": f"JSON parse error: {str(e)}. JSON: '{json_text[:100]}'"
                            }
                
                return {
                    "success": False,
                    "error": f"No valid JSON found in output: {result.stdout[:200]}"
                }
            else:
                # Handle CLI errors
                try:
                    # Try to find JSON in stdout even for non-zero exit codes
                    stdout_text = result.stdout.strip()
                    
                    # Find JSON block - look for opening brace and matching closing brace
                    json_start_pos = stdout_text.find('{')
                    if json_start_pos >= 0:
                        # Count braces to find the matching close
                        brace_count = 0
                        json_end_pos = -1
                        
                        for i in range(json_start_pos, len(stdout_text)):
                            if stdout_text[i] == '{':
                                brace_count += 1
                            elif stdout_text[i] == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    json_end_pos = i
                                    break
                        
                        if json_end_pos > json_start_pos:
                            json_text = stdout_text[json_start_pos:json_end_pos+1]
                            return json.loads(json_text)
                    
                    # No JSON found, return error
                    return {
                        "success": False,
                        "error": f"CLI error (exit {result.returncode}): {result.stderr or result.stdout}"
                    }
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": f"CLI error: {result.stderr or 'Unknown error'}"
                    }
                    
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "TTS generation timeout"}
        except Exception as e:
            return {"success": False, "error": f"CLI execution error: {str(e)}"}
    
    def validate_voice(self, voice: str) -> bool:
        """
        Validate if a voice is supported.
        
        Args:
            voice: Voice name to validate
            
        Returns:
            True if voice is supported
        """
        try:
            cmd = [
                "python", "examples/tts_cli_wrapper.py",
                "--validate-voice", voice, "--json"
            ]
            
            result = subprocess.run(
                cmd,
                cwd=str(self.tts_path),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode in [0, 1]:  # Both success and validation failure are valid responses
                response = json.loads(result.stdout)
                return response.get("valid", False)
            else:
                return False
                
        except Exception:
            return voice in self.supported_voices  # Fallback to static list
    
    def list_voices(self) -> Dict[str, Any]:
        """
        Get list of available voices.
        
        Returns:
            Dictionary with voice information
        """
        try:
            cmd = [
                "python", "examples/tts_cli_wrapper.py",
                "--list-voices", "--json"
            ]
            
            result = subprocess.run(
                cmd,
                cwd=str(self.tts_path),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                response = json.loads(result.stdout)
                return {
                    "success": True,
                    "voices": response.get("voices", self.supported_voices)
                }
            else:
                return {
                    "success": False,
                    "voices": self.supported_voices  # Fallback
                }
                
        except Exception:
            return {
                "success": False,
                "voices": self.supported_voices  # Fallback
            }
    
    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model: Model name
            
        Returns:
            Model information dictionary
        """
        model_info = {
            "elevenlabs": {
                "name": "ElevenLabs Standard",
                "description": "High-quality text-to-speech with natural voices",
                "cost_per_generation": 0.05,
                "processing_time": 15,
                "quality": "high"
            },
            "elevenlabs_turbo": {
                "name": "ElevenLabs Turbo",
                "description": "Fast text-to-speech for quick generation",
                "cost_per_generation": 0.03,
                "processing_time": 8,
                "quality": "medium"
            },
            "elevenlabs_v3": {
                "name": "ElevenLabs v3",
                "description": "Latest model with enhanced quality and expressiveness",
                "cost_per_generation": 0.08,
                "processing_time": 20,
                "quality": "premium"
            }
        }
        
        return model_info.get(model, {
            "name": "Unknown Model",
            "description": "Model information not available",
            "cost_per_generation": 0.05,
            "processing_time": 15,
            "quality": "unknown"
        })