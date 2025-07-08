"""
Main TTS Controller

Core text-to-speech functionality with voice control, timing, and audio generation.
"""

import os
import time
import requests
from typing import Dict, List, Optional, Union
from ..models.common import ElevenLabsModel, AudioFormat, VoiceSettings, VoiceInfo
from ..config.defaults import DEFAULT_VOICE_SETTINGS, DEFAULT_MODEL, DEFAULT_API_BASE_URL
from ..utils.api_helpers import make_request_with_retry, build_headers, validate_api_key
from ..utils.validators import validate_text_input, validate_voice_settings, validate_speed
from .voice_manager import VoiceManager
from .audio_processor import AudioProcessor


class ElevenLabsTTSController:
    """
    ElevenLabs Text-to-Speech Controller
    
    Features:
    - Multiple model support (v3, Multilingual v2, Flash v2.5, Turbo v2.5)
    - Voice control and selection
    - Timing and speed control
    - Audio format selection
    - Streaming support
    - Professional voice cloning
    """
    
    def __init__(self, api_key: str, base_url: str = DEFAULT_API_BASE_URL):
        """
        Initialize the TTS controller
        
        Args:
            api_key: ElevenLabs API key
            base_url: API base URL
        """
        if not validate_api_key(api_key):
            raise ValueError("Invalid API key format")
        
        self.api_key = api_key
        self.base_url = base_url
        self.headers = build_headers(api_key)
        
        # Initialize managers
        self.voice_manager = VoiceManager(api_key, base_url)
        self.audio_processor = AudioProcessor()
    
    def text_to_speech(
        self,
        text: str,
        voice_id: str,
        model: ElevenLabsModel = DEFAULT_MODEL,
        voice_settings: Optional[VoiceSettings] = None,
        audio_format: AudioFormat = AudioFormat.MP3,
        speed: float = 1.0,
        output_file: Optional[str] = None,
        stream: bool = False
    ) -> Union[bytes, bool]:
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            voice_id: Voice ID to use
            model: TTS model to use
            voice_settings: Voice configuration
            audio_format: Output audio format
            speed: Speech speed (0.25-4.0)
            output_file: Output file path (optional)
            stream: Whether to stream the audio
            
        Returns:
            Audio bytes or success status
        """
        # Validate inputs
        is_valid, error = validate_text_input(text)
        if not is_valid:
            print(f"Invalid text input: {error}")
            return False
        
        is_valid, error = validate_speed(speed)
        if not is_valid:
            print(f"Invalid speed setting: {error}")
            return False
        
        if voice_settings is None:
            voice_settings = DEFAULT_VOICE_SETTINGS
        
        is_valid, error = validate_voice_settings(voice_settings)
        if not is_valid:
            print(f"Invalid voice settings: {error}")
            return False
        
        # Prepare payload
        payload = {
            "text": text,
            "model_id": model.value,
            "voice_settings": voice_settings.to_dict()
        }
        
        # Add speed if model supports it
        if model in [ElevenLabsModel.TURBO_V2_5, ElevenLabsModel.FLASH_V2_5]:
            payload["voice_settings"]["speed"] = speed
        
        # Prepare headers for audio format
        headers = self.audio_processor.build_headers_for_format(self.headers, audio_format)
        
        try:
            # Build URL
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            if stream:
                url += "/stream"
            
            # Make API request
            response = make_request_with_retry(
                url=url,
                headers=headers,
                data=payload,
                method="POST"
            )
            
            if not response:
                return False
            
            # Process response
            if stream:
                return self.audio_processor.process_streaming_response(response, output_file)
            else:
                return self.audio_processor.process_regular_response(response, output_file)
                
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")
            return False
    
    def text_to_speech_with_timing_control(
        self,
        text: str,
        voice_name: str,
        speed: float = 1.0,
        pause_duration: float = 0.5,
        model: ElevenLabsModel = DEFAULT_MODEL,
        voice_settings: Optional[VoiceSettings] = None,
        output_file: Optional[str] = None
    ) -> bool:
        """
        Convert text to speech with enhanced timing control
        
        Args:
            text: Text to convert
            voice_name: Name of the voice to use
            speed: Speech speed multiplier
            pause_duration: Duration of pauses after sentences
            model: TTS model to use
            voice_settings: Voice configuration
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        # Get voice ID from name
        voice_id = self.voice_manager.get_popular_voice_id(voice_name)
        if not voice_id:
            # Try to find voice by name in full voice list
            voice_info = self.voice_manager.get_voice_by_name(voice_name)
            if voice_info:
                voice_id = voice_info.voice_id
            else:
                print(f"Voice '{voice_name}' not found")
                return False
        
        # Add timing breaks to text
        enhanced_text = self.audio_processor.add_timing_breaks(text, pause_duration)
        
        # Generate speech
        result = self.text_to_speech(
            text=enhanced_text,
            voice_id=voice_id,
            model=model,
            voice_settings=voice_settings,
            speed=speed,
            output_file=output_file
        )
        
        return isinstance(result, bool) and result
    
    def multi_voice_generation(
        self,
        script: List[Dict[str, str]],
        model: ElevenLabsModel = DEFAULT_MODEL,
        voice_settings: Optional[VoiceSettings] = None,
        output_file: Optional[str] = None,
        pause_between_speakers: float = 0.3
    ) -> bool:
        """
        Generate multi-voice audio from a script
        
        Args:
            script: List of {"speaker": "voice_name", "text": "content"} dictionaries
            model: TTS model to use
            voice_settings: Voice configuration
            output_file: Output file path
            pause_between_speakers: Pause duration between speakers
            
        Returns:
            True if successful, False otherwise
        """
        if not script:
            print("Script cannot be empty")
            return False
        
        audio_segments = []
        temp_files = []
        
        try:
            for i, segment in enumerate(script):
                speaker = segment.get("speaker", "")
                text = segment.get("text", "")
                
                if not speaker or not text:
                    print(f"Invalid script segment {i}: missing speaker or text")
                    continue
                
                # Get voice ID
                voice_id = self.voice_manager.get_popular_voice_id(speaker)
                if not voice_id:
                    voice_info = self.voice_manager.get_voice_by_name(speaker)
                    if voice_info:
                        voice_id = voice_info.voice_id
                    else:
                        print(f"Voice '{speaker}' not found, skipping segment")
                        continue
                
                # Generate audio for this segment
                temp_file = f"temp_segment_{i}.mp3"
                success = self.text_to_speech(
                    text=text,
                    voice_id=voice_id,
                    model=model,
                    voice_settings=voice_settings,
                    output_file=temp_file
                )
                
                if success:
                    temp_files.append(temp_file)
                else:
                    print(f"Failed to generate audio for segment {i}")
            
            # Combine audio files
            if temp_files and output_file:
                success = self.audio_processor.combine_audio_files(temp_files, output_file)
                
                # Cleanup temp files
                for temp_file in temp_files:
                    try:
                        os.remove(temp_file)
                    except OSError:
                        pass
                
                return success
            
        except Exception as e:
            print(f"Error in multi-voice generation: {e}")
            
            # Cleanup temp files on error
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except OSError:
                    pass
            
            return False
        
        return False
    
    def clone_voice_from_file(
        self,
        audio_file: str,
        voice_name: str,
        description: str = "Custom cloned voice"
    ) -> Optional[str]:
        """
        Clone a voice from an audio file
        
        Args:
            audio_file: Path to audio file for cloning
            voice_name: Name for the new voice
            description: Description of the voice
            
        Returns:
            Voice ID if successful, None otherwise
        """
        try:
            url = f"{self.base_url}/voices/add"
            
            # Prepare files and data
            with open(audio_file, 'rb') as f:
                files = {'files': (os.path.basename(audio_file), f, 'audio/mpeg')}
                data = {
                    'name': voice_name,
                    'description': description
                }
                
                response = make_request_with_retry(
                    url=url,
                    headers=self.headers,
                    data=data,
                    files=files,
                    method="POST"
                )
            
            if response and response.status_code in [200, 201]:
                result = response.json()
                voice_id = result.get('voice_id')
                if voice_id:
                    print(f"Voice cloned successfully: {voice_name} ({voice_id})")
                    return voice_id
            
            print("Failed to clone voice")
            return None
            
        except Exception as e:
            print(f"Error cloning voice: {e}")
            return None
    
    # Delegate methods to voice manager
    def get_voices(self, refresh_cache: bool = False) -> List[VoiceInfo]:
        """Get all available voices"""
        return self.voice_manager.get_voices(refresh_cache)
    
    def get_voice_by_name(self, name: str) -> Optional[VoiceInfo]:
        """Get voice by name"""
        return self.voice_manager.get_voice_by_name(name)
    
    def get_popular_voice_id(self, name: str) -> Optional[str]:
        """Get popular voice ID by name"""
        return self.voice_manager.get_popular_voice_id(name)
    
    def print_voices(self, category: Optional[str] = None, limit: int = 20):
        """Print available voices"""
        self.voice_manager.print_voices(category, limit)
    
    def search_voices(self, query: str, category: Optional[str] = None, gender: Optional[str] = None) -> List[VoiceInfo]:
        """Search for voices"""
        return self.voice_manager.search_voices(query, category, gender)