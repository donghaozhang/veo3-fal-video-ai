"""
OpenRouter TTS Pipeline Core

Main pipeline orchestration for AI content generation and text-to-speech conversion.
"""

import os
import json
import time
import requests
from typing import Dict, List, Optional, Union, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from ..models.pipeline import (
        OpenRouterModel, 
        ContentType, 
        VoiceStyle, 
        PipelineInput, 
        GeneratedContent, 
        PipelineResult,
        LengthCalculation
    )
    from ..tts.controller import ElevenLabsTTSController
    from ..models.common import ElevenLabsModel, VoiceSettings
    from ..config.voices import get_voice_style_preset
    from ..utils.validators import validate_text_input
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models.pipeline import (
        OpenRouterModel, 
        ContentType, 
        VoiceStyle, 
        PipelineInput, 
        GeneratedContent, 
        PipelineResult,
        LengthCalculation
    )
    from tts.controller import ElevenLabsTTSController
    from models.common import ElevenLabsModel, VoiceSettings
    from config.voices import get_voice_style_preset
    from utils.validators import validate_text_input


class OpenRouterTTSPipeline:
    """
    Complete AI content generation pipeline from description to speech using OpenRouter models.
    """
    
    def __init__(self, openrouter_key: str, elevenlabs_key: str):
        """
        Initialize the pipeline.
        
        Args:
            openrouter_key: OpenRouter API key
            elevenlabs_key: ElevenLabs API key
        """
        self.openrouter_key = openrouter_key
        self.elevenlabs_key = elevenlabs_key
        
        # Initialize TTS controller
        self.tts_controller = ElevenLabsTTSController(elevenlabs_key)
        
        # OpenRouter API configuration
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        self.openrouter_headers = {
            "Authorization": f"Bearer {openrouter_key}",
            "HTTP-Referer": "https://github.com/your-repo",
            "X-Title": "ElevenLabs TTS Pipeline",
            "Content-Type": "application/json"
        }
    
    def calculate_length_requirements(self, target_minutes: float, num_people: int = 1) -> LengthCalculation:
        """
        Calculate content requirements for target length.
        
        Args:
            target_minutes: Target duration in minutes
            num_people: Number of speakers
            
        Returns:
            LengthCalculation object with estimates
        """
        # Adjust speaking rate based on number of people (dialogue is typically slower)
        speaking_rate = 150 if num_people == 1 else 130
        return LengthCalculation(target_minutes, 0, 0, speaking_rate)
    
    def generate_content_with_llm(
        self,
        pipeline_input: PipelineInput,
        model: OpenRouterModel = OpenRouterModel.CLAUDE_SONNET_4
    ) -> Optional[GeneratedContent]:
        """
        Generate content using OpenRouter LLM.
        
        Args:
            pipeline_input: Pipeline input configuration
            model: OpenRouter model to use
            
        Returns:
            GeneratedContent object if successful, None otherwise
        """
        # Calculate length requirements
        length_calc = self.calculate_length_requirements(
            pipeline_input.length_minutes, 
            pipeline_input.num_people
        )
        
        # Build prompt based on content type and requirements
        prompt = self._build_content_prompt(pipeline_input, length_calc)
        
        try:
            # Make request to OpenRouter
            response = requests.post(
                f"{self.openrouter_base_url}/chat/completions",
                headers=self.openrouter_headers,
                json={
                    "model": model.value,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": length_calc.estimated_tokens + 500,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                return GeneratedContent(
                    title=f"{pipeline_input.content_type.value.title()} - {pipeline_input.description}",
                    content=content,
                    speakers=self._extract_speakers(content, pipeline_input.num_people),
                    estimated_duration=pipeline_input.length_minutes,
                    word_count=0,  # Will be calculated in __post_init__
                    metadata={
                        "model": model.value,
                        "content_type": pipeline_input.content_type.value,
                        "voice_style": pipeline_input.voice_style.value
                    }
                )
            else:
                print(f"OpenRouter API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
    
    def convert_to_speech(
        self,
        generated_content: GeneratedContent,
        pipeline_input: PipelineInput,
        output_file: str
    ) -> bool:
        """
        Convert generated content to speech.
        
        Args:
            generated_content: Generated content to convert
            pipeline_input: Original pipeline input
            output_file: Output audio file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if pipeline_input.num_people == 1:
                # Single speaker
                voice_config = get_voice_style_preset(pipeline_input.voice_style.value)
                if voice_config:
                    voice_name = voice_config.get("primary", "rachel")
                else:
                    voice_name = "rachel"
                
                return self.tts_controller.text_to_speech_with_timing_control(
                    text=generated_content.content,
                    voice_name=voice_name,
                    output_file=output_file
                )
            else:
                # Multi-speaker
                script = self._parse_dialogue_content(generated_content.content, pipeline_input)
                return self.tts_controller.multi_voice_generation(
                    script=script,
                    output_file=output_file
                )
                
        except Exception as e:
            print(f"Error converting to speech: {e}")
            return False
    
    def run_complete_pipeline(
        self,
        description: str,
        num_people: int = 1,
        length_minutes: float = 1.0,
        content_type: Union[str, ContentType] = ContentType.CONVERSATION,
        voice_style: Union[str, VoiceStyle] = VoiceStyle.CONVERSATIONAL,
        model: OpenRouterModel = OpenRouterModel.CLAUDE_SONNET_4,
        output_file: Optional[str] = None
    ) -> PipelineResult:
        """
        Run the complete pipeline from description to speech.
        
        Args:
            description: Description of content to generate
            num_people: Number of speakers
            length_minutes: Target length in minutes
            content_type: Type of content to generate
            voice_style: Voice style to use
            model: OpenRouter model to use
            output_file: Output audio file path
            
        Returns:
            PipelineResult with complete results
        """
        start_time = time.time()
        
        # Convert string enums to enum objects
        if isinstance(content_type, str):
            content_type = ContentType(content_type)
        if isinstance(voice_style, str):
            voice_style = VoiceStyle(voice_style)
        
        # Create pipeline input
        pipeline_input = PipelineInput(
            description=description,
            num_people=num_people,
            length_minutes=length_minutes,
            content_type=content_type,
            voice_style=voice_style,
            model=model
        )
        
        # Generate default output filename if not provided
        if not output_file:
            timestamp = int(time.time())
            output_file = f"output/pipeline_{timestamp}.mp3"
        
        try:
            # Step 1: Generate content
            generated_content = self.generate_content_with_llm(pipeline_input, model)
            if not generated_content:
                return PipelineResult(
                    input_config=pipeline_input,
                    generated_content=None,
                    audio_file=None,
                    processing_time=time.time() - start_time,
                    success=False,
                    error_message="Failed to generate content"
                )
            
            # Step 2: Convert to speech
            speech_success = self.convert_to_speech(generated_content, pipeline_input, output_file)
            
            processing_time = time.time() - start_time
            
            return PipelineResult(
                input_config=pipeline_input,
                generated_content=generated_content,
                audio_file=output_file if speech_success else None,
                processing_time=processing_time,
                success=speech_success,
                error_message=None if speech_success else "Failed to convert to speech"
            )
            
        except Exception as e:
            return PipelineResult(
                input_config=pipeline_input,
                generated_content=None,
                audio_file=None,
                processing_time=time.time() - start_time,
                success=False,
                error_message=str(e)
            )
    
    def _build_content_prompt(self, pipeline_input: PipelineInput, length_calc: LengthCalculation) -> str:
        """Build prompt for content generation"""
        base_prompt = f"""Generate a {pipeline_input.content_type.value} about {pipeline_input.description}.

Requirements:
- Number of speakers: {pipeline_input.num_people}
- Target length: ~{length_calc.estimated_words} words (approximately {pipeline_input.length_minutes} minutes)
- Style: {pipeline_input.voice_style.value}
- Content type: {pipeline_input.content_type.value}

Please generate natural, engaging content that fits these requirements."""
        
        if pipeline_input.num_people > 1:
            base_prompt += "\n\nFormat as a dialogue with clear speaker labels (Speaker 1:, Speaker 2:, etc.)"
        
        return base_prompt
    
    def _extract_speakers(self, content: str, num_people: int) -> List[str]:
        """Extract speaker names from content"""
        if num_people == 1:
            return ["Narrator"]
        else:
            return [f"Speaker {i+1}" for i in range(num_people)]
    
    def _parse_dialogue_content(self, content: str, pipeline_input: PipelineInput) -> List[Dict[str, str]]:
        """Parse dialogue content into script format"""
        # Simple parsing - can be enhanced
        lines = content.split('\n')
        script = []
        
        voice_config = get_voice_style_preset(pipeline_input.voice_style.value)
        voices = voice_config.get("primary_voices", ["rachel", "drew"]) if voice_config else ["rachel", "drew"]
        
        current_speaker = 0
        for line in lines:
            line = line.strip()
            if line and ':' in line:
                # Extract speaker and text
                parts = line.split(':', 1)
                if len(parts) == 2:
                    text = parts[1].strip()
                    if text:
                        voice = voices[current_speaker % len(voices)]
                        script.append({
                            "speaker": voice,
                            "text": text
                        })
                        current_speaker += 1
        
        return script