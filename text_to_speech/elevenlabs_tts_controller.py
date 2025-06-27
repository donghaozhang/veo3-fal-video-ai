#!/usr/bin/env python3
"""
ElevenLabs Text-to-Speech Controller
Comprehensive Python implementation for controlling voices, timing, and audio generation
Based on ElevenLabs official API documentation
"""

import os
import time
import requests
import json
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
import io


class ElevenLabsModel(Enum):
    """ElevenLabs TTS Models with their capabilities"""
    ELEVEN_V3 = "eleven_v3"  # Alpha - Most expressive, 70+ languages, 10k chars
    MULTILINGUAL_V2 = "eleven_multilingual_v2"  # Highest quality, 29 languages, 10k chars
    FLASH_V2_5 = "eleven_flash_v2_5"  # Ultra-low latency ~75ms, 32 languages, 40k chars
    TURBO_V2_5 = "eleven_turbo_v2_5"  # Balanced quality/speed, 32 languages, 40k chars


class AudioFormat(Enum):
    """Supported audio formats"""
    MP3 = "mp3_44100_128"  # Default: 44.1kHz @ 128kbps
    MP3_HIGH = "mp3_44100_192"  # High quality: 44.1kHz @ 192kbps
    MP3_LOW = "mp3_22050_32"   # Low quality: 22.05kHz @ 32kbps
    PCM = "pcm_16000"          # PCM 16kHz
    PCM_HIGH = "pcm_44100"     # PCM 44.1kHz
    ULAW = "ulaw_8000"         # μ-law 8kHz (telephony)
    OPUS = "opus_48000"        # Opus 48kHz


@dataclass
class VoiceSettings:
    """Voice configuration settings"""
    stability: float = 0.5      # 0.0-1.0: Higher = more stable, lower = more variable
    similarity_boost: float = 0.5  # 0.0-1.0: Higher = closer to original voice
    style: float = 0.0          # 0.0-1.0: Style exaggeration (v2 models)
    use_speaker_boost: bool = True  # Enhance speaker clarity


@dataclass
class VoiceInfo:
    """Voice information structure"""
    voice_id: str
    name: str
    category: str
    description: str = ""
    language: str = "en"
    gender: str = "neutral"


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
    
    def __init__(self, api_key: str, base_url: str = "https://api.elevenlabs.io/v1"):
        """
        Initialize the TTS controller
        
        Args:
            api_key: ElevenLabs API key
            base_url: API base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        # Cache for voices
        self._voices_cache: Optional[List[VoiceInfo]] = None
        
        # Popular voice IDs (these are examples - use get_voices() for current list)
        self.popular_voices = {
            "rachel": "21m00Tcm4TlvDq8ikWAM",  # Female, American
            "drew": "29vD33N1CtxCmqQRPOHJ",     # Male, American  
            "clyde": "2EiwWnXFnvU5JabPnv8n",    # Male, American
            "bella": "EXAVITQu4vr4xnSDxMaL",    # Female, American
            "antoni": "ErXwobaYiN019PkySvjV",   # Male, American
            "elli": "MF3mGyEYCl7XYWbV9V6O",     # Female, American
            "josh": "TxGEqnHWrfWFTfGW9XjX",     # Male, American
            "arnold": "VR6AewLTigWG4xSOukaG",   # Male, American
            "adam": "pNInz6obpgDQGcFmaJgB",     # Male, American
            "sam": "yoZ06aMxZJJ28mfd3POQ",      # Male, American
        }
    
    def get_voices(self, refresh_cache: bool = False) -> List[VoiceInfo]:
        """
        Get available voices from ElevenLabs
        
        Args:
            refresh_cache: Force refresh of voice cache
            
        Returns:
            List of available voices
        """
        if self._voices_cache is None or refresh_cache:
            try:
                response = requests.get(f"{self.base_url}/voices", headers=self.headers)
                response.raise_for_status()
                
                data = response.json()
                self._voices_cache = []
                
                for voice_data in data.get("voices", []):
                    voice_info = VoiceInfo(
                        voice_id=voice_data["voice_id"],
                        name=voice_data["name"],
                        category=voice_data.get("category", "cloned"),
                        description=voice_data.get("description", ""),
                        language=voice_data.get("labels", {}).get("language", "en"),
                        gender=voice_data.get("labels", {}).get("gender", "neutral")
                    )
                    self._voices_cache.append(voice_info)
                    
            except Exception as e:
                print(f"Error fetching voices: {e}")
                return []
        
        return self._voices_cache or []
    
    def get_voice_by_name(self, name: str) -> Optional[VoiceInfo]:
        """Get voice by name"""
        voices = self.get_voices()
        for voice in voices:
            if voice.name.lower() == name.lower():
                return voice
        return None
    
    def get_popular_voice_id(self, name: str) -> Optional[str]:
        """Get popular voice ID by name"""
        return self.popular_voices.get(name.lower())
    
    def text_to_speech(
        self,
        text: str,
        voice_id: str,
        model: ElevenLabsModel = ElevenLabsModel.MULTILINGUAL_V2,
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
            speed: Speech speed (0.7-1.2)
            output_file: Output file path (optional)
            stream: Whether to stream the audio
            
        Returns:
            Audio bytes or success status
        """
        if voice_settings is None:
            voice_settings = VoiceSettings()
        
        # Validate speed
        speed = max(0.7, min(1.2, speed))
        
        # Prepare payload
        payload = {
            "text": text,
            "model_id": model.value,
            "voice_settings": {
                "stability": voice_settings.stability,
                "similarity_boost": voice_settings.similarity_boost,
                "style": voice_settings.style,
                "use_speaker_boost": voice_settings.use_speaker_boost,
                "speed": speed
            }
        }
        
        # Set headers for audio format
        headers = self.headers.copy()
        if audio_format == AudioFormat.MP3:
            headers["Accept"] = "audio/mpeg"
        elif "pcm" in audio_format.value:
            headers["Accept"] = "audio/wav"
        elif audio_format == AudioFormat.OPUS:
            headers["Accept"] = "audio/opus"
        
        try:
            # Make API request
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            if stream:
                url += "/stream"
            
            response = requests.post(url, json=payload, headers=headers, stream=stream)
            response.raise_for_status()
            
            if stream:
                # Handle streaming response
                if output_file:
                    with open(output_file, "wb") as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    return True
                else:
                    # Return streaming content
                    content = b""
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            content += chunk
                    return content
            else:
                # Handle regular response
                audio_content = response.content
                
                if output_file:
                    with open(output_file, "wb") as f:
                        f.write(audio_content)
                    return True
                
                return audio_content
                
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")
            return False
    
    def text_to_speech_with_timing_control(
        self,
        text: str,
        voice_name: str,
        speed: float = 1.0,
        pause_duration: float = 0.5,
        model: ElevenLabsModel = ElevenLabsModel.MULTILINGUAL_V2,
        output_file: Optional[str] = None
    ) -> bool:
        """
        Convert text to speech with enhanced timing control
        
        Args:
            text: Text to convert
            voice_name: Voice name (popular voice or custom)
            speed: Speech speed (0.7-1.2)
            pause_duration: Pause duration for breaks in seconds
            model: TTS model to use
            output_file: Output file path
            
        Returns:
            Success status
        """
        # Get voice ID
        voice_id = self.get_popular_voice_id(voice_name)
        if not voice_id:
            voice_info = self.get_voice_by_name(voice_name)
            if voice_info:
                voice_id = voice_info.voice_id
            else:
                print(f"Voice '{voice_name}' not found")
                return False
        
        # Add timing controls to text
        enhanced_text = self._add_timing_controls(text, pause_duration)
        
        # Configure voice settings for timing
        voice_settings = VoiceSettings(
            stability=0.6,  # Slightly more stable for timing consistency
            similarity_boost=0.7,
            style=0.2,
            use_speaker_boost=True
        )
        
        return self.text_to_speech(
            text=enhanced_text,
            voice_id=voice_id,
            model=model,
            voice_settings=voice_settings,
            speed=speed,
            output_file=output_file
        )
    
    def _add_timing_controls(self, text: str, pause_duration: float) -> str:
        """Add timing controls to text"""
        # Add breaks after sentences
        import re
        
        # Add breaks after periods, exclamation marks, and question marks
        text = re.sub(r'([.!?])\s+', f'\\1 <break time="{pause_duration}s" /> ', text)
        
        # Add breaks after commas (shorter pause)
        comma_pause = pause_duration * 0.5
        text = re.sub(r'(,)\s+', f'\\1 <break time="{comma_pause}s" /> ', text)
        
        return text
    
    def multi_voice_generation(
        self,
        script: List[Dict[str, str]],
        output_file: str,
        model: ElevenLabsModel = ElevenLabsModel.MULTILINGUAL_V2
    ) -> bool:
        """
        Generate multi-voice audio from script
        
        Args:
            script: List of {"speaker": "voice_name", "text": "dialogue"}
            output_file: Output file path
            model: TTS model to use
            
        Returns:
            Success status
        """
        try:
            import wave
            import struct
            
            audio_segments = []
            
            for segment in script:
                speaker = segment["speaker"]
                text = segment["text"]
                
                # Get voice ID
                voice_id = self.get_popular_voice_id(speaker)
                if not voice_id:
                    voice_info = self.get_voice_by_name(speaker)
                    if voice_info:
                        voice_id = voice_info.voice_id
                    else:
                        print(f"Voice '{speaker}' not found, using default")
                        voice_id = self.popular_voices["rachel"]
                
                # Generate audio for this segment
                audio_data = self.text_to_speech(
                    text=text,
                    voice_id=voice_id,
                    model=model,
                    audio_format=AudioFormat.PCM
                )
                
                if audio_data:
                    audio_segments.append(audio_data)
                    # Add pause between speakers
                    silence_duration = 0.5  # 500ms pause
                    sample_rate = 16000
                    silence_samples = int(sample_rate * silence_duration)
                    silence = b'\x00\x00' * silence_samples
                    audio_segments.append(silence)
            
            # Combine all segments
            if audio_segments:
                combined_audio = b''.join(audio_segments)
                
                # Save as WAV file
                with wave.open(output_file, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(16000)  # 16kHz
                    wav_file.writeframes(combined_audio)
                
                return True
            
        except Exception as e:
            print(f"Error in multi-voice generation: {e}")
        
        return False
    
    def clone_voice_from_file(
        self,
        audio_file_path: str,
        voice_name: str,
        voice_description: str = ""
    ) -> Optional[str]:
        """
        Clone a voice from audio file (Instant Voice Cloning)
        
        Args:
            audio_file_path: Path to audio file
            voice_name: Name for the cloned voice
            voice_description: Description of the voice
            
        Returns:
            Voice ID of cloned voice or None if failed
        """
        try:
            with open(audio_file_path, 'rb') as audio_file:
                files = {
                    'files': (audio_file_path, audio_file, 'audio/mpeg')
                }
                
                data = {
                    'name': voice_name,
                    'description': voice_description
                }
                
                headers = {"xi-api-key": self.api_key}
                
                response = requests.post(
                    f"{self.base_url}/voices/add",
                    files=files,
                    data=data,
                    headers=headers
                )
                
                response.raise_for_status()
                result = response.json()
                
                return result.get("voice_id")
                
        except Exception as e:
            print(f"Error cloning voice: {e}")
            return None
    
    def get_model_info(self) -> Dict[str, Dict]:
        """Get information about available models"""
        return {
            "eleven_v3": {
                "name": "Eleven v3 (Alpha)",
                "description": "Most emotionally rich, expressive speech synthesis",
                "features": ["Dramatic delivery", "70+ languages", "Multi-speaker dialogue"],
                "character_limit": 10000,
                "latency": "Medium",
                "use_cases": ["Audiobooks", "Dramatic content", "Expressive narration"]
            },
            "eleven_multilingual_v2": {
                "name": "Eleven Multilingual v2",
                "description": "Lifelike, consistent quality speech synthesis",
                "features": ["Natural-sounding", "29 languages", "Most stable"],
                "character_limit": 10000,
                "latency": "Medium",
                "use_cases": ["Long-form content", "Professional narration", "Multilingual projects"]
            },
            "eleven_flash_v2_5": {
                "name": "Eleven Flash v2.5",
                "description": "Fast, affordable speech synthesis",
                "features": ["Ultra-low latency ~75ms", "32 languages", "50% lower cost"],
                "character_limit": 40000,
                "latency": "Ultra-low",
                "use_cases": ["Real-time applications", "Conversational AI", "Interactive systems"]
            },
            "eleven_turbo_v2_5": {
                "name": "Eleven Turbo v2.5",
                "description": "High quality, low-latency balanced model",
                "features": ["Low latency ~250ms", "32 languages", "50% lower cost"],
                "character_limit": 40000,
                "latency": "Low",
                "use_cases": ["Streaming applications", "Real-time synthesis", "Cost-effective projects"]
            }
        }
    
    def print_voices(self, category_filter: Optional[str] = None):
        """Print available voices with details"""
        voices = self.get_voices()
        
        if category_filter:
            voices = [v for v in voices if v.category.lower() == category_filter.lower()]
        
        print(f"\n{'='*60}")
        print(f"Available Voices ({len(voices)} total)")
        print(f"{'='*60}")
        
        for voice in voices:
            print(f"Name: {voice.name}")
            print(f"ID: {voice.voice_id}")
            print(f"Category: {voice.category}")
            print(f"Language: {voice.language}")
            print(f"Gender: {voice.gender}")
            if voice.description:
                print(f"Description: {voice.description}")
            print("-" * 40)


def demo_usage():
    """Demonstrate the TTS controller usage"""
    
    # Initialize controller (replace with your API key)
    api_key = os.getenv("ELEVENLABS_API_KEY", "your_api_key_here")
    
    if api_key == "your_api_key_here":
        print("Please set your ELEVENLABS_API_KEY environment variable")
        return
    
    tts = ElevenLabsTTSController(api_key)
    
    # Print model information
    print("ElevenLabs TTS Models:")
    models = tts.get_model_info()
    for model_id, info in models.items():
        print(f"\n{info['name']}:")
        print(f"  Description: {info['description']}")
        print(f"  Character Limit: {info['character_limit']:,}")
        print(f"  Latency: {info['latency']}")
        print(f"  Use Cases: {', '.join(info['use_cases'])}")
    
    # Example 1: Basic text-to-speech with timing control
    print("\n" + "="*50)
    print("Example 1: Basic TTS with Speed Control")
    print("="*50)
    
    text = "Hello! This is a demonstration of ElevenLabs text-to-speech with speed control. Notice how the timing changes with different speed settings."
    
    # Normal speed
    success = tts.text_to_speech_with_timing_control(
        text=text,
        voice_name="rachel",
        speed=1.0,
        output_file="demo_normal_speed.mp3"
    )
    
    if success:
        print("✓ Generated: demo_normal_speed.mp3")
    
    # Slow speed
    success = tts.text_to_speech_with_timing_control(
        text=text,
        voice_name="rachel",
        speed=0.8,
        output_file="demo_slow_speed.mp3"
    )
    
    if success:
        print("✓ Generated: demo_slow_speed.mp3")
    
    # Fast speed
    success = tts.text_to_speech_with_timing_control(
        text=text,
        voice_name="rachel",
        speed=1.2,
        output_file="demo_fast_speed.mp3"
    )
    
    if success:
        print("✓ Generated: demo_fast_speed.mp3")
    
    # Example 2: Multi-voice conversation
    print("\n" + "="*50)
    print("Example 2: Multi-Voice Conversation")
    print("="*50)
    
    conversation_script = [
        {"speaker": "rachel", "text": "Hello, how are you doing today?"},
        {"speaker": "drew", "text": "I'm doing great, thanks for asking! How about you?"},
        {"speaker": "rachel", "text": "I'm wonderful! The weather is so nice today."},
        {"speaker": "drew", "text": "Yes, it's perfect for a walk in the park."},
        {"speaker": "rachel", "text": "That sounds like a great idea! Let's go together."}
    ]
    
    success = tts.multi_voice_generation(
        script=conversation_script,
        output_file="demo_conversation.wav",
        model=ElevenLabsModel.MULTILINGUAL_V2
    )
    
    if success:
        print("✓ Generated: demo_conversation.wav")
    
    # Example 3: Different models comparison
    print("\n" + "="*50)
    print("Example 3: Model Comparison")
    print("="*50)
    
    comparison_text = "This is a comparison of different ElevenLabs models. Each model has unique characteristics in terms of quality, speed, and expressiveness."
    
    models_to_test = [
        (ElevenLabsModel.MULTILINGUAL_V2, "multilingual_v2"),
        (ElevenLabsModel.FLASH_V2_5, "flash_v2_5"),
        (ElevenLabsModel.TURBO_V2_5, "turbo_v2_5")
    ]
    
    for model, filename in models_to_test:
        success = tts.text_to_speech(
            text=comparison_text,
            voice_id=tts.get_popular_voice_id("rachel"),
            model=model,
            output_file=f"demo_{filename}.mp3"
        )
        
        if success:
            print(f"✓ Generated: demo_{filename}.mp3")
    
    # Example 4: Custom voice settings
    print("\n" + "="*50)
    print("Example 4: Custom Voice Settings")
    print("="*50)
    
    settings_text = "This demonstrates different voice settings. You can control stability, similarity, and style to customize the voice output."
    
    # High stability (more consistent)
    stable_settings = VoiceSettings(stability=0.9, similarity_boost=0.8, style=0.1)
    success = tts.text_to_speech(
        text=settings_text,
        voice_id=tts.get_popular_voice_id("bella"),
        voice_settings=stable_settings,
        output_file="demo_stable_voice.mp3"
    )
    
    if success:
        print("✓ Generated: demo_stable_voice.mp3 (High Stability)")
    
    # Creative settings (more expressive)
    creative_settings = VoiceSettings(stability=0.3, similarity_boost=0.6, style=0.8)
    success = tts.text_to_speech(
        text=settings_text,
        voice_id=tts.get_popular_voice_id("bella"),
        voice_settings=creative_settings,
        output_file="demo_creative_voice.mp3"
    )
    
    if success:
        print("✓ Generated: demo_creative_voice.mp3 (Creative Settings)")
    
    print("\n" + "="*50)
    print("Demo completed! Check the generated audio files.")
    print("="*50)


if __name__ == "__main__":
    demo_usage() 