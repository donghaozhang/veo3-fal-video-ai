"""
Audio Processing Module

Audio format handling, processing, and utility functions.
"""

import os
import io
import time
from typing import Dict, Optional, Union, Any
from pathlib import Path
from ..models.common import AudioFormat
from ..utils.file_manager import save_audio_file, ensure_output_dir


class AudioProcessor:
    """
    Handles audio format processing, conversion, and file operations.
    """
    
    def __init__(self):
        """Initialize the audio processor."""
        self.supported_formats = {
            AudioFormat.MP3: {"mime": "audio/mpeg", "extension": ".mp3"},
            AudioFormat.MP3_HIGH: {"mime": "audio/mpeg", "extension": ".mp3"},
            AudioFormat.MP3_LOW: {"mime": "audio/mpeg", "extension": ".mp3"},
            AudioFormat.PCM: {"mime": "audio/wav", "extension": ".wav"},
            AudioFormat.PCM_HIGH: {"mime": "audio/wav", "extension": ".wav"},
            AudioFormat.ULAW: {"mime": "audio/wav", "extension": ".wav"},
            AudioFormat.OPUS: {"mime": "audio/opus", "extension": ".opus"}
        }
    
    def get_mime_type(self, audio_format: AudioFormat) -> str:
        """
        Get MIME type for an audio format.
        
        Args:
            audio_format: AudioFormat enum
            
        Returns:
            MIME type string
        """
        return self.supported_formats.get(audio_format, {}).get("mime", "audio/mpeg")
    
    def get_file_extension(self, audio_format: AudioFormat) -> str:
        """
        Get file extension for an audio format.
        
        Args:
            audio_format: AudioFormat enum
            
        Returns:
            File extension string (including dot)
        """
        return self.supported_formats.get(audio_format, {}).get("extension", ".mp3")
    
    def build_headers_for_format(self, base_headers: Dict[str, str], audio_format: AudioFormat) -> Dict[str, str]:
        """
        Build request headers for a specific audio format.
        
        Args:
            base_headers: Base headers dictionary
            audio_format: Desired audio format
            
        Returns:
            Updated headers dictionary
        """
        headers = base_headers.copy()
        headers["Accept"] = self.get_mime_type(audio_format)
        return headers
    
    def save_audio(self, audio_data: bytes, output_path: Union[str, Path], audio_format: Optional[AudioFormat] = None) -> bool:
        """
        Save audio data to file with appropriate extension.
        
        Args:
            audio_data: Audio data bytes
            output_path: Path to save the audio file
            audio_format: Audio format (used to determine extension if not in path)
            
        Returns:
            True if successful, False otherwise
        """
        output_path = Path(output_path)
        
        # Add appropriate extension if not present
        if audio_format and not output_path.suffix:
            extension = self.get_file_extension(audio_format)
            output_path = output_path.with_suffix(extension)
        
        return save_audio_file(audio_data, output_path)
    
    def process_streaming_response(self, response, output_file: Optional[str] = None) -> Union[bytes, bool]:
        """
        Process a streaming HTTP response for audio data.
        
        Args:
            response: Streaming HTTP response object
            output_file: Optional output file path
            
        Returns:
            Audio bytes if no output file, success status if output file provided
        """
        try:
            if output_file:
                # Save streaming data to file
                output_path = ensure_output_dir(output_file)
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                return True
            else:
                # Collect streaming data in memory
                content = b""
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        content += chunk
                return content
        except Exception as e:
            print(f"Error processing streaming response: {e}")
            return False
    
    def process_regular_response(self, response, output_file: Optional[str] = None) -> Union[bytes, bool]:
        """
        Process a regular HTTP response for audio data.
        
        Args:
            response: HTTP response object
            output_file: Optional output file path
            
        Returns:
            Audio bytes if no output file, success status if output file provided
        """
        try:
            audio_content = response.content
            
            if output_file:
                # Save to file
                success = self.save_audio(audio_content, output_file)
                return success
            else:
                # Return audio bytes
                return audio_content
        except Exception as e:
            print(f"Error processing response: {e}")
            return False
    
    def add_timing_breaks(self, text: str, pause_duration: float = 0.5) -> str:
        """
        Add timing breaks to text for natural speech pacing.
        
        Args:
            text: Input text
            pause_duration: Duration of pauses in seconds
            
        Returns:
            Text with timing breaks added
        """
        import re
        
        # Add breaks after sentences
        text = re.sub(r'([.!?])\s+', f'\\1 <break time="{pause_duration}s" /> ', text)
        
        # Add shorter breaks after commas
        short_pause = pause_duration * 0.5
        text = re.sub(r'(,)\s+', f'\\1 <break time="{short_pause}s" /> ', text)
        
        return text
    
    def split_long_text(self, text: str, max_length: int = 5000) -> List[str]:
        """
        Split long text into smaller chunks for processing.
        
        Args:
            text: Input text to split
            max_length: Maximum length per chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by sentences first
        sentences = text.split('. ')
        
        for sentence in sentences:
            # If adding this sentence would exceed the limit
            if len(current_chunk) + len(sentence) + 2 > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence + ". "
                else:
                    # Single sentence is too long, split by words
                    words = sentence.split()
                    for word in words:
                        if len(current_chunk) + len(word) + 1 > max_length:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                                current_chunk = word + " "
                            else:
                                # Single word is too long, just add it
                                chunks.append(word)
                        else:
                            current_chunk += word + " "
            else:
                current_chunk += sentence + ". "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def combine_audio_files(self, file_paths: List[str], output_path: str) -> bool:
        """
        Combine multiple audio files into one.
        
        Note: This is a basic implementation. For production use,
        consider using audio processing libraries like pydub.
        
        Args:
            file_paths: List of audio file paths to combine
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            combined_data = b""
            
            for file_path in file_paths:
                with open(file_path, 'rb') as f:
                    combined_data += f.read()
            
            return self.save_audio(combined_data, output_path)
        except Exception as e:
            print(f"Error combining audio files: {e}")
            return False
    
    def get_audio_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get basic information about an audio file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with audio file information
        """
        file_path = Path(file_path)
        
        info = {
            "exists": file_path.exists(),
            "size_bytes": file_path.stat().st_size if file_path.exists() else 0,
            "extension": file_path.suffix,
            "name": file_path.name
        }
        
        if info["size_bytes"] > 0:
            info["size_mb"] = round(info["size_bytes"] / (1024 * 1024), 2)
        
        return info