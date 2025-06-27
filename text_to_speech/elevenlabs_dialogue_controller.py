#!/usr/bin/env python3
"""
ElevenLabs Text-to-Dialogue Controller
Advanced dialogue generation with multiple speakers and emotional control
Based on ElevenLabs Text to Dialogue API documentation
"""

import os
import json
import time
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play, save
    ELEVENLABS_SDK_AVAILABLE = True
except ImportError:
    ELEVENLABS_SDK_AVAILABLE = False
    print("ElevenLabs SDK not available. Install with: pip install elevenlabs")

from elevenlabs_tts_controller import ElevenLabsTTSController, VoiceInfo


class DialogueModel(Enum):
    """Available dialogue models"""
    ELEVEN_V3 = "eleven_v3"  # Default evergreen model
    ELEVEN_V3_PREVIEW = "eleven_v3_preview_2025_06_03"  # Latest preview features


@dataclass
class DialogueInput:
    """Single dialogue input with voice and emotional context"""
    text: str
    voice_id: str
    emotional_context: Optional[str] = None
    speaker_name: Optional[str] = None
    pause_before: Optional[float] = None  # Pause before this line in seconds
    pause_after: Optional[float] = None   # Pause after this line in seconds


@dataclass
class DialogueSettings:
    """Settings for dialogue generation"""
    model: DialogueModel = DialogueModel.ELEVEN_V3
    normalize_audio: bool = True
    add_speaker_pauses: bool = True
    default_pause_duration: float = 0.5
    cross_fade_duration: float = 0.1


class ElevenLabsDialogueController:
    """
    ElevenLabs Text-to-Dialogue Controller
    
    Features:
    - Multi-speaker dialogue generation
    - Emotional context tags ([cheerfully], [stuttering], etc.)
    - Advanced timing control
    - Speaker identification and management
    - Conversation flow optimization
    - Integration with existing TTS controller
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the dialogue controller
        
        Args:
            api_key: ElevenLabs API key
        """
        self.api_key = api_key
        
        # Initialize ElevenLabs client if SDK is available
        if ELEVENLABS_SDK_AVAILABLE:
            self.client = ElevenLabs(api_key=api_key)
        else:
            self.client = None
            print("Warning: ElevenLabs SDK not available. Some features may be limited.")
        
        # Initialize TTS controller for fallback and additional features
        self.tts_controller = ElevenLabsTTSController(api_key)
        
        # Popular voice combinations for dialogue
        self.dialogue_voice_pairs = {
            "professional": {
                "speaker_1": ("rachel", "21m00Tcm4TlvDq8ikWAM"),  # Female, professional
                "speaker_2": ("drew", "29vD33N1CtxCmqQRPOHJ")     # Male, warm
            },
            "casual": {
                "speaker_1": ("bella", "EXAVITQu4vr4xnSDxMaL"),   # Female, friendly
                "speaker_2": ("antoni", "ErXwobaYiN019PkySvjV")   # Male, casual
            },
            "dramatic": {
                "speaker_1": ("elli", "MF3mGyEYCl7XYWbV9V6O"),    # Female, expressive
                "speaker_2": ("josh", "TxGEqnHWrfWFTfGW9XjX")     # Male, dramatic
            },
            "authoritative": {
                "speaker_1": ("arnold", "VR6AewLTigWG4xSOukaG"),  # Male, strong
                "speaker_2": ("sam", "yoZ06aMxZJJ28mfd3POQ")      # Male, professional
            }
        }
        
        # Emotional context tags for dialogue
        self.emotional_tags = {
            # Positive emotions
            "cheerfully": "[cheerfully]",
            "excitedly": "[excitedly]",
            "happily": "[happily]",
            "joyfully": "[joyfully]",
            "enthusiastically": "[enthusiastically]",
            
            # Negative emotions
            "sadly": "[sadly]",
            "angrily": "[angrily]",
            "frustrated": "[frustrated]",
            "disappointed": "[disappointed]",
            "worried": "[worried]",
            
            # Neutral/descriptive
            "calmly": "[calmly]",
            "quietly": "[quietly]",
            "loudly": "[loudly]",
            "slowly": "[slowly]",
            "quickly": "[quickly]",
            
            # Special delivery
            "whispering": "[whispering]",
            "shouting": "[shouting]",
            "stuttering": "[stuttering]",
            "sarcastically": "[sarcastically]",
            "curiously": "[curiously]",
            "mischievously": "[mischievously]"
        }
    
    def create_dialogue_input(
        self,
        text: str,
        voice_id: str,
        emotional_context: Optional[str] = None,
        speaker_name: Optional[str] = None
    ) -> DialogueInput:
        """
        Create a dialogue input with optional emotional context
        
        Args:
            text: The text to be spoken
            voice_id: Voice ID for this speaker
            emotional_context: Emotional context (e.g., "cheerfully", "stuttering")
            speaker_name: Optional speaker name for reference
            
        Returns:
            DialogueInput object
        """
        # Add emotional context to text if provided
        if emotional_context and emotional_context in self.emotional_tags:
            enhanced_text = f"{self.emotional_tags[emotional_context]} {text}"
        elif emotional_context and emotional_context.startswith("[") and emotional_context.endswith("]"):
            # Allow custom emotional tags
            enhanced_text = f"{emotional_context} {text}"
        else:
            enhanced_text = text
        
        return DialogueInput(
            text=enhanced_text,
            voice_id=voice_id,
            emotional_context=emotional_context,
            speaker_name=speaker_name
        )
    
    def generate_dialogue(
        self,
        dialogue_inputs: List[DialogueInput],
        settings: Optional[DialogueSettings] = None,
        output_file: Optional[str] = None
    ) -> Union[bytes, bool]:
        """
        Generate dialogue from multiple speakers
        
        Args:
            dialogue_inputs: List of dialogue inputs
            settings: Dialogue generation settings
            output_file: Optional output file path
            
        Returns:
            Audio bytes or success status
        """
        if settings is None:
            settings = DialogueSettings()
        
        if not ELEVENLABS_SDK_AVAILABLE or not self.client:
            print("Warning: Using fallback method. Install elevenlabs SDK for best results.")
            return self._generate_dialogue_fallback(dialogue_inputs, settings, output_file)
        
        try:
            # Prepare inputs for the API
            api_inputs = []
            for dialogue_input in dialogue_inputs:
                api_inputs.append({
                    "text": dialogue_input.text,
                    "voice_id": dialogue_input.voice_id
                })
            
            # Generate dialogue using ElevenLabs Text to Dialogue API
            audio = self.client.text_to_dialogue.convert(
                model_id=settings.model.value,
                inputs=api_inputs
            )
            
            if output_file:
                save(audio, output_file)
                return True
            
            return audio
            
        except Exception as e:
            print(f"Error generating dialogue: {e}")
            print("Falling back to alternative method...")
            return self._generate_dialogue_fallback(dialogue_inputs, settings, output_file)
    
    def _generate_dialogue_fallback(
        self,
        dialogue_inputs: List[DialogueInput],
        settings: DialogueSettings,
        output_file: Optional[str]
    ) -> bool:
        """
        Fallback method using individual TTS calls
        
        Args:
            dialogue_inputs: List of dialogue inputs
            settings: Dialogue generation settings
            output_file: Optional output file path
            
        Returns:
            Success status
        """
        try:
            import wave
            import struct
            
            audio_segments = []
            sample_rate = 22050  # Standard sample rate
            
            for i, dialogue_input in enumerate(dialogue_inputs):
                print(f"Generating segment {i+1}/{len(dialogue_inputs)}: {dialogue_input.speaker_name or 'Speaker'}")
                
                # Generate audio for this segment
                audio_data = self.tts_controller.text_to_speech(
                    text=dialogue_input.text,
                    voice_id=dialogue_input.voice_id,
                    audio_format=self.tts_controller.AudioFormat.PCM,
                    speed=1.0
                )
                
                if audio_data:
                    # Add pause before if specified
                    if dialogue_input.pause_before:
                        pause_samples = int(sample_rate * dialogue_input.pause_before)
                        pause_audio = b'\x00\x00' * pause_samples
                        audio_segments.append(pause_audio)
                    
                    audio_segments.append(audio_data)
                    
                    # Add pause after if specified
                    if dialogue_input.pause_after:
                        pause_samples = int(sample_rate * dialogue_input.pause_after)
                        pause_audio = b'\x00\x00' * pause_samples
                        audio_segments.append(pause_audio)
                    
                    # Add default pause between speakers
                    elif settings.add_speaker_pauses and i < len(dialogue_inputs) - 1:
                        pause_samples = int(sample_rate * settings.default_pause_duration)
                        pause_audio = b'\x00\x00' * pause_samples
                        audio_segments.append(pause_audio)
            
            # Combine all segments
            if audio_segments and output_file:
                combined_audio = b''.join(audio_segments)
                
                # Save as WAV file
                with wave.open(output_file, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(combined_audio)
                
                return True
            
        except Exception as e:
            print(f"Error in fallback dialogue generation: {e}")
        
        return False
    
    def create_conversation_script(
        self,
        conversation_data: List[Dict[str, str]],
        voice_pair: str = "professional"
    ) -> List[DialogueInput]:
        """
        Create dialogue inputs from conversation data
        
        Args:
            conversation_data: List of {"speaker": "name", "text": "content", "emotion": "context"}
            voice_pair: Voice pair preset to use
            
        Returns:
            List of DialogueInput objects
        """
        if voice_pair not in self.dialogue_voice_pairs:
            print(f"Unknown voice pair '{voice_pair}', using 'professional'")
            voice_pair = "professional"
        
        voices = self.dialogue_voice_pairs[voice_pair]
        dialogue_inputs = []
        
        for entry in conversation_data:
            speaker = entry.get("speaker", "speaker_1")
            text = entry.get("text", "")
            emotion = entry.get("emotion", None)
            
            # Map speaker to voice
            if speaker in voices:
                voice_name, voice_id = voices[speaker]
            elif speaker == "speaker_1" or speaker.lower() in ["speaker1", "person1", "a"]:
                voice_name, voice_id = voices["speaker_1"]
            elif speaker == "speaker_2" or speaker.lower() in ["speaker2", "person2", "b"]:
                voice_name, voice_id = voices["speaker_2"]
            else:
                # Default to speaker_1
                voice_name, voice_id = voices["speaker_1"]
            
            dialogue_input = self.create_dialogue_input(
                text=text,
                voice_id=voice_id,
                emotional_context=emotion,
                speaker_name=f"{speaker} ({voice_name})"
            )
            
            dialogue_inputs.append(dialogue_input)
        
        return dialogue_inputs
    
    def generate_conversation(
        self,
        conversation_data: List[Dict[str, str]],
        voice_pair: str = "professional",
        output_file: str = "conversation.wav",
        settings: Optional[DialogueSettings] = None
    ) -> bool:
        """
        Generate a complete conversation from structured data
        
        Args:
            conversation_data: List of conversation entries
            voice_pair: Voice pair preset to use
            output_file: Output file path
            settings: Optional dialogue settings
            
        Returns:
            Success status
        """
        print(f"Generating conversation with {voice_pair} voices...")
        print(f"Conversation has {len(conversation_data)} exchanges")
        
        # Create dialogue inputs
        dialogue_inputs = self.create_conversation_script(conversation_data, voice_pair)
        
        # Generate dialogue
        success = self.generate_dialogue(
            dialogue_inputs=dialogue_inputs,
            settings=settings,
            output_file=output_file
        )
        
        if success:
            print(f"✓ Conversation generated: {output_file}")
        else:
            print("✗ Failed to generate conversation")
        
        return success
    
    def play_dialogue(self, audio_data: bytes) -> bool:
        """
        Play generated dialogue audio
        
        Args:
            audio_data: Audio data to play
            
        Returns:
            Success status
        """
        if ELEVENLABS_SDK_AVAILABLE:
            try:
                play(audio_data)
                return True
            except Exception as e:
                print(f"Error playing audio: {e}")
        else:
            print("Audio playback requires elevenlabs SDK")
        
        return False
    
    def get_available_voice_pairs(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """Get available voice pair presets"""
        return self.dialogue_voice_pairs
    
    def get_emotional_tags(self) -> Dict[str, str]:
        """Get available emotional context tags"""
        return self.emotional_tags
    
    def print_voice_pairs(self):
        """Print available voice pair presets"""
        print("\nAvailable Voice Pairs:")
        print("=" * 40)
        
        for pair_name, voices in self.dialogue_voice_pairs.items():
            print(f"\n{pair_name.title()}:")
            for speaker, (voice_name, voice_id) in voices.items():
                print(f"  {speaker}: {voice_name} ({voice_id[:8]}...)")
    
    def print_emotional_tags(self):
        """Print available emotional context tags"""
        print("\nAvailable Emotional Tags:")
        print("=" * 40)
        
        categories = {
            "Positive": ["cheerfully", "excitedly", "happily", "joyfully", "enthusiastically"],
            "Negative": ["sadly", "angrily", "frustrated", "disappointed", "worried"],
            "Neutral": ["calmly", "quietly", "loudly", "slowly", "quickly"],
            "Special": ["whispering", "shouting", "stuttering", "sarcastically", "curiously", "mischievously"]
        }
        
        for category, tags in categories.items():
            print(f"\n{category}:")
            for tag in tags:
                print(f"  {tag}: {self.emotional_tags[tag]}")


def demo_dialogue_generation():
    """Demonstrate dialogue generation capabilities"""
    
    # Get API key
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("Please set ELEVENLABS_API_KEY environment variable")
        return
    
    print("ElevenLabs Text-to-Dialogue Demo")
    print("=" * 50)
    
    # Initialize controller
    dialogue_controller = ElevenLabsDialogueController(api_key)
    
    # Show available options
    dialogue_controller.print_voice_pairs()
    dialogue_controller.print_emotional_tags()
    
    # Example 1: Simple professional conversation
    print("\n" + "=" * 50)
    print("Example 1: Professional Conversation")
    print("=" * 50)
    
    professional_conversation = [
        {
            "speaker": "speaker_1",
            "text": "Good morning! Thank you for joining us today.",
            "emotion": "cheerfully"
        },
        {
            "speaker": "speaker_2",
            "text": "Good morning! I'm excited to be here.",
            "emotion": "enthusiastically"
        },
        {
            "speaker": "speaker_1",
            "text": "Let's start with an overview of our new text-to-speech capabilities.",
            "emotion": "calmly"
        },
        {
            "speaker": "speaker_2",
            "text": "That sounds fascinating! I'd love to learn more about the technology.",
            "emotion": "curiously"
        }
    ]
    
    success = dialogue_controller.generate_conversation(
        conversation_data=professional_conversation,
        voice_pair="professional",
        output_file="professional_conversation.wav"
    )
    
    # Example 2: Casual conversation with emotions
    print("\n" + "=" * 50)
    print("Example 2: Casual Emotional Conversation")
    print("=" * 50)
    
    casual_conversation = [
        {
            "speaker": "speaker_1",
            "text": "Hey! Did you hear about the new AI features?",
            "emotion": "excitedly"
        },
        {
            "speaker": "speaker_2",
            "text": "No, what happened? Tell me everything!",
            "emotion": "curiously"
        },
        {
            "speaker": "speaker_1",
            "text": "They can now generate entire conversations with different emotions!",
            "emotion": "enthusiastically"
        },
        {
            "speaker": "speaker_2",
            "text": "That's... that's incredible! How does it work?",
            "emotion": "stuttering"
        },
        {
            "speaker": "speaker_1",
            "text": "Well, you just provide the text and emotional context tags.",
            "emotion": "calmly"
        }
    ]
    
    success = dialogue_controller.generate_conversation(
        conversation_data=casual_conversation,
        voice_pair="casual",
        output_file="casual_conversation.wav"
    )
    
    # Example 3: Dramatic dialogue
    print("\n" + "=" * 50)
    print("Example 3: Dramatic Dialogue")
    print("=" * 50)
    
    dramatic_conversation = [
        {
            "speaker": "speaker_1",
            "text": "I can't believe you would do this to me!",
            "emotion": "angrily"
        },
        {
            "speaker": "speaker_2",
            "text": "I... I'm sorry. I never meant for it to happen this way.",
            "emotion": "sadly"
        },
        {
            "speaker": "speaker_1",
            "text": "Sorry? Sorry doesn't fix what you've broken!",
            "emotion": "frustrated"
        },
        {
            "speaker": "speaker_2",
            "text": "Please, just give me a chance to explain.",
            "emotion": "quietly"
        },
        {
            "speaker": "speaker_1",
            "text": "Fine. But this better be good.",
            "emotion": "sarcastically"
        }
    ]
    
    success = dialogue_controller.generate_conversation(
        conversation_data=dramatic_conversation,
        voice_pair="dramatic",
        output_file="dramatic_conversation.wav"
    )
    
    # Example 4: Custom dialogue using API directly
    if ELEVENLABS_SDK_AVAILABLE:
        print("\n" + "=" * 50)
        print("Example 4: Direct API Usage")
        print("=" * 50)
        
        # Create custom dialogue inputs
        custom_inputs = [
            dialogue_controller.create_dialogue_input(
                text="Welcome to our advanced dialogue system!",
                voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
                emotional_context="cheerfully",
                speaker_name="Host"
            ),
            dialogue_controller.create_dialogue_input(
                text="This is amazing! The voices sound so natural.",
                voice_id="29vD33N1CtxCmqQRPOHJ",  # Drew
                emotional_context="excitedly",
                speaker_name="Guest"
            ),
            dialogue_controller.create_dialogue_input(
                text="And we can control emotions and timing perfectly.",
                voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
                emotional_context="calmly",
                speaker_name="Host"
            )
        ]
        
        success = dialogue_controller.generate_dialogue(
            dialogue_inputs=custom_inputs,
            output_file="custom_dialogue.wav"
        )
        
        if success:
            print("✓ Custom dialogue generated: custom_dialogue.wav")
    
    print("\n" + "=" * 50)
    print("Demo completed! Check the generated audio files:")
    print("- professional_conversation.wav")
    print("- casual_conversation.wav") 
    print("- dramatic_conversation.wav")
    if ELEVENLABS_SDK_AVAILABLE:
        print("- custom_dialogue.wav")
    print("=" * 50)


if __name__ == "__main__":
    demo_dialogue_generation() 