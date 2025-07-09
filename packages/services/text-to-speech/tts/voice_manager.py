"""
Voice Management Module

Voice selection, management, and retrieval functionality.
"""

import requests
from typing import Dict, List, Optional, Union

try:
    from ..models.common import VoiceInfo, POPULAR_VOICE_IDS
    from ..config.voices import POPULAR_VOICES, get_voice_preset
    from ..utils.api_helpers import make_request_with_retry, build_headers
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models.common import VoiceInfo, POPULAR_VOICE_IDS
    from config.voices import POPULAR_VOICES, get_voice_preset
    from utils.api_helpers import make_request_with_retry, build_headers


class VoiceManager:
    """
    Manages voice selection, retrieval, and caching for TTS operations.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.elevenlabs.io/v1"):
        """
        Initialize the voice manager.
        
        Args:
            api_key: ElevenLabs API key
            base_url: API base URL
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = build_headers(api_key)
        
        # Cache for voices
        self._voices_cache: Optional[List[VoiceInfo]] = None
    
    def get_voices(self, refresh_cache: bool = False) -> List[VoiceInfo]:
        """
        Get all available voices from the API.
        
        Args:
            refresh_cache: Whether to refresh the cached voices
            
        Returns:
            List of VoiceInfo objects
        """
        if self._voices_cache is None or refresh_cache:
            try:
                url = f"{self.base_url}/voices"
                response = make_request_with_retry(url, self.headers, method="GET")
                
                if response and response.status_code == 200:
                    voices_data = response.json()
                    self._voices_cache = []
                    
                    for voice_data in voices_data.get("voices", []):
                        voice_info = VoiceInfo(
                            voice_id=voice_data.get("voice_id", ""),
                            name=voice_data.get("name", ""),
                            category=voice_data.get("category", ""),
                            description=voice_data.get("description", ""),
                            language=voice_data.get("language", "en"),
                            gender=voice_data.get("gender", "neutral")
                        )
                        self._voices_cache.append(voice_info)
                else:
                    print("Failed to retrieve voices from API, using popular voices as fallback")
                    self._voices_cache = list(POPULAR_VOICES.values())
                    
            except Exception as e:
                print(f"Error retrieving voices: {e}")
                self._voices_cache = list(POPULAR_VOICES.values())
        
        return self._voices_cache or []
    
    def get_voice_by_id(self, voice_id: str) -> Optional[VoiceInfo]:
        """
        Get voice information by voice ID.
        
        Args:
            voice_id: Voice ID to look up
            
        Returns:
            VoiceInfo object if found, None otherwise
        """
        voices = self.get_voices()
        for voice in voices:
            if voice.voice_id == voice_id:
                return voice
        return None
    
    def get_voice_by_name(self, voice_name: str) -> Optional[VoiceInfo]:
        """
        Get voice information by voice name.
        
        Args:
            voice_name: Voice name to look up
            
        Returns:
            VoiceInfo object if found, None otherwise
        """
        # First check popular voices
        voice_info = get_voice_preset(voice_name)
        if voice_info:
            return voice_info
        
        # Then check all voices
        voices = self.get_voices()
        for voice in voices:
            if voice.name.lower() == voice_name.lower():
                return voice
        
        return None
    
    def get_popular_voice_id(self, voice_name: str) -> Optional[str]:
        """
        Get voice ID for a popular voice preset.
        
        Args:
            voice_name: Name of the popular voice
            
        Returns:
            Voice ID string if found, None otherwise
        """
        return POPULAR_VOICE_IDS.get(voice_name.lower())
    
    def search_voices(self, query: str, category: Optional[str] = None, gender: Optional[str] = None) -> List[VoiceInfo]:
        """
        Search for voices by name, description, or other criteria.
        
        Args:
            query: Search query
            category: Voice category filter
            gender: Gender filter
            
        Returns:
            List of matching VoiceInfo objects
        """
        voices = self.get_voices()
        results = []
        
        query_lower = query.lower()
        
        for voice in voices:
            # Check if query matches name or description
            name_match = query_lower in voice.name.lower()
            desc_match = query_lower in voice.description.lower()
            
            # Apply filters
            category_match = category is None or voice.category == category
            gender_match = gender is None or voice.gender == gender
            
            if (name_match or desc_match) and category_match and gender_match:
                results.append(voice)
        
        return results
    
    def get_voices_by_category(self, category: str) -> List[VoiceInfo]:
        """
        Get all voices in a specific category.
        
        Args:
            category: Voice category
            
        Returns:
            List of VoiceInfo objects
        """
        voices = self.get_voices()
        return [voice for voice in voices if voice.category == category]
    
    def get_voices_by_gender(self, gender: str) -> List[VoiceInfo]:
        """
        Get all voices of a specific gender.
        
        Args:
            gender: Gender filter ("male", "female", "neutral")
            
        Returns:
            List of VoiceInfo objects
        """
        voices = self.get_voices()
        return [voice for voice in voices if voice.gender == gender.lower()]
    
    def print_voices(self, category: Optional[str] = None, limit: int = 20):
        """
        Print available voices in a formatted way.
        
        Args:
            category: Optional category filter
            limit: Maximum number of voices to display
        """
        voices = self.get_voices()
        
        if category:
            voices = [v for v in voices if v.category == category]
        
        print(f"\nAvailable Voices ({len(voices)} total):")
        print("-" * 80)
        
        for i, voice in enumerate(voices[:limit]):
            print(f"{i+1:2d}. {voice.name:15} | {voice.voice_id:25} | {voice.category:10} | {voice.gender:8}")
        
        if len(voices) > limit:
            print(f"... and {len(voices) - limit} more voices")
    
    def validate_voice_id(self, voice_id: str) -> bool:
        """
        Validate that a voice ID exists.
        
        Args:
            voice_id: Voice ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        return self.get_voice_by_id(voice_id) is not None
    
    def get_random_voice(self, category: Optional[str] = None, gender: Optional[str] = None) -> Optional[VoiceInfo]:
        """
        Get a random voice matching the specified criteria.
        
        Args:
            category: Optional category filter
            gender: Optional gender filter
            
        Returns:
            Random VoiceInfo object if found, None otherwise
        """
        import random
        
        voices = self.get_voices()
        
        # Apply filters
        if category:
            voices = [v for v in voices if v.category == category]
        if gender:
            voices = [v for v in voices if v.gender == gender]
        
        return random.choice(voices) if voices else None