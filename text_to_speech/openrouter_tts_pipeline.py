#!/usr/bin/env python3
"""
OpenRouter + ElevenLabs Text-to-Speech Pipeline
Complete pipeline: Description → LLM Generation → Text-to-Speech/Dialogue
Uses top 10 OpenRouter models for content generation
"""

import os
import json
import time
import requests
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our existing TTS controllers
from elevenlabs_tts_controller import ElevenLabsTTSController, ElevenLabsModel, VoiceSettings
from text_to_dialogue_script import create_dialogue_example

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import save, play
    ELEVENLABS_SDK_AVAILABLE = True
except ImportError:
    ELEVENLABS_SDK_AVAILABLE = False


class OpenRouterModel(Enum):
    """Top 10 OpenRouter models based on performance"""
    CLAUDE_SONNET_4 = "anthropic/claude-3.5-sonnet"
    GEMINI_2_FLASH = "google/gemini-2.0-flash-exp"
    GEMINI_25_FLASH_PREVIEW = "google/gemini-2.5-flash-preview"
    GEMINI_2_FLASH_LITE = "google/gemini-2.0-flash-lite"
    DEEPSEEK_V3_FREE = "deepseek/deepseek-v3-0324-free"
    DEEPSEEK_V3 = "deepseek/deepseek-v3-0324"
    GEMINI_25_FLASH_LITE = "google/gemini-2.5-flash-lite-preview"
    CLAUDE_37_SONNET = "anthropic/claude-3.7-sonnet"
    GEMINI_25_FLASH = "google/gemini-2.5-flash"
    GEMINI_25_PRO = "google/gemini-2.5-pro"


@dataclass
class PipelineInput:
    """Input configuration for the pipeline"""
    description: str  # Description of person(s)
    num_people: int   # 1 or 2 people
    length_minutes: float  # Desired length in minutes
    content_type: str = "conversation"  # Type of content to generate
    voice_style: str = "professional"   # Voice style for TTS
    model_preference: Optional[OpenRouterModel] = None


@dataclass
class GeneratedContent:
    """Generated content from LLM"""
    raw_text: str
    processed_content: List[Dict[str, str]]  # For dialogue: [{"speaker": "A", "text": "...", "emotion": "..."}]
    estimated_duration: float
    model_used: str
    token_count: int


class OpenRouterTTSPipeline:
    """
    Complete pipeline from description to speech
    
    Pipeline Steps:
    1. Input: Description + Parameters
    2. Length Calculation: Estimate content requirements
    3. LLM Generation: Use OpenRouter models
    4. Content Processing: Structure for TTS
    5. Speech Generation: ElevenLabs TTS/Dialogue
    """
    
    def __init__(self, openrouter_api_key: str, elevenlabs_api_key: str):
        """
        Initialize the pipeline
        
        Args:
            openrouter_api_key: OpenRouter API key
            elevenlabs_api_key: ElevenLabs API key
        """
        self.openrouter_api_key = openrouter_api_key
        self.elevenlabs_api_key = elevenlabs_api_key
        
        # Ensure output directory exists
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize ElevenLabs controllers
        self.tts_controller = ElevenLabsTTSController(elevenlabs_api_key)
        
        if ELEVENLABS_SDK_AVAILABLE:
            self.elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)
        else:
            self.elevenlabs_client = None
        
        # OpenRouter configuration
        self.openrouter_base_url = "https://openrouter.ai/api/v1"
        self.openrouter_headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/donghaozhang/veo3-video-generation",
            "X-Title": "Text-to-Speech Pipeline"
        }
        
        # Voice configurations for different scenarios
        self.voice_configurations = {
            "professional": {
                "single": {"voice_id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel"},  # Professional female
                "dual": [
                    {"voice_id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel", "speaker": "speaker_1"},
                    {"voice_id": "29vD33N1CtxCmqQRPOHJ", "name": "Drew", "speaker": "speaker_2"}
                ]
            },
            "casual": {
                "single": {"voice_id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella"},  # Friendly female
                "dual": [
                    {"voice_id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella", "speaker": "speaker_1"},
                    {"voice_id": "ErXwobaYiN019PkySvjV", "name": "Antoni", "speaker": "speaker_2"}
                ]
            },
            "dramatic": {
                "single": {"voice_id": "MF3mGyEYCl7XYWbV9V6O", "name": "Elli"},  # Expressive female
                "dual": [
                    {"voice_id": "MF3mGyEYCl7XYWbV9V6O", "name": "Elli", "speaker": "speaker_1"},
                    {"voice_id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh", "speaker": "speaker_2"}
                ]
            }
        }
        
        # Content type templates
        self.content_templates = {
            "conversation": {
                "single": "Create a {length_minutes}-minute monologue for {description}. Make it engaging and natural.",
                "dual": "Create a {length_minutes}-minute conversation between two people: {description}. Include natural dialogue with emotions."
            },
            "presentation": {
                "single": "Create a {length_minutes}-minute presentation by {description}. Make it informative and engaging.",
                "dual": "Create a {length_minutes}-minute discussion between two presenters: {description}. Include Q&A style dialogue."
            },
            "interview": {
                "single": "Create a {length_minutes}-minute self-introduction by {description}. Make it personal and interesting.",
                "dual": "Create a {length_minutes}-minute interview between an interviewer and {description}. Include thoughtful questions and answers."
            },
            "story": {
                "single": "Create a {length_minutes}-minute story narrated by {description}. Make it engaging and immersive.",
                "dual": "Create a {length_minutes}-minute story with dialogue between {description}. Include character interactions."
            }
        }
    
    def _get_output_path(self, filename: str) -> str:
        """
        Get the full output path for a file
        
        Args:
            filename: The filename (e.g., "test.mp3")
            
        Returns:
            Full path in the output directory
        """
        return os.path.join(self.output_dir, filename)
    
    def calculate_content_length(self, length_minutes: float, num_people: int) -> Dict[str, int]:
        """
        Step 2: Calculate content requirements based on desired length
        
        Args:
            length_minutes: Desired audio length in minutes
            num_people: Number of speakers
            
        Returns:
            Dictionary with content specifications
        """
        # Speech rate: approximately 150-200 words per minute
        base_words_per_minute = 175
        
        # Adjust for multiple speakers (includes pauses, turn-taking)
        if num_people == 2:
            effective_wpm = base_words_per_minute * 0.8  # Account for dialogue pauses
        else:
            effective_wpm = base_words_per_minute
        
        target_words = int(length_minutes * effective_wpm)
        
        # Estimate tokens (approximately 1.3 tokens per word)
        estimated_tokens = int(target_words * 1.3)
        
        # Estimate sentences (approximately 15-20 words per sentence)
        estimated_sentences = max(int(target_words / 17), 1)
        
        # For dialogue, estimate exchanges
        if num_people == 2:
            estimated_exchanges = max(int(estimated_sentences / 2), 1)
        else:
            estimated_exchanges = 1
        
        return {
            "target_words": target_words,
            "estimated_tokens": estimated_tokens,
            "estimated_sentences": estimated_sentences,
            "estimated_exchanges": estimated_exchanges,
            "effective_wpm": effective_wpm
        }
    
    def generate_content_with_llm(
        self,
        pipeline_input: PipelineInput,
        content_specs: Dict[str, int],
        model: OpenRouterModel = OpenRouterModel.CLAUDE_SONNET_4
    ) -> GeneratedContent:
        """
        Step 3: Generate content using OpenRouter LLM
        
        Args:
            pipeline_input: Input configuration
            content_specs: Content specifications from calculate_content_length
            model: OpenRouter model to use
            
        Returns:
            Generated content
        """
        # Select appropriate template
        template_key = "dual" if pipeline_input.num_people == 2 else "single"
        template = self.content_templates[pipeline_input.content_type][template_key]
        
        # Create the prompt
        base_prompt = template.format(
            length_minutes=pipeline_input.length_minutes,
            description=pipeline_input.description
        )
        
        # Add specific instructions based on number of people
        if pipeline_input.num_people == 2:
            additional_instructions = f"""
            
IMPORTANT FORMATTING INSTRUCTIONS:
- Format as a structured dialogue
- Use clear speaker labels (Speaker A: and Speaker B:)
- Include emotional context in square brackets: [cheerfully], [curiously], [excitedly], etc.
- Target approximately {content_specs['target_words']} words total
- Create {content_specs['estimated_exchanges']} natural exchanges
- Make the conversation flow naturally with realistic timing
- Include appropriate emotions and reactions

Example format:
Speaker A: [cheerfully] Hello! How are you doing today?
Speaker B: [enthusiastically] I'm doing great, thanks for asking!
"""
        else:
            additional_instructions = f"""
            
IMPORTANT FORMATTING INSTRUCTIONS:
- Create a natural monologue or presentation
- Include emotional cues in square brackets: [confidently], [thoughtfully], [passionately], etc.
- Target approximately {content_specs['target_words']} words total
- Structure with clear topics or sections
- Make it engaging and natural-sounding
- Include appropriate pacing and emphasis

Example format:
[confidently] Welcome everyone to today's presentation...
[thoughtfully] When we consider the implications...
"""
        
        full_prompt = base_prompt + additional_instructions
        
        try:
            # Make request to OpenRouter
            response = requests.post(
                f"{self.openrouter_base_url}/chat/completions",
                headers=self.openrouter_headers,
                json={
                    "model": model.value,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert content creator specializing in natural, engaging dialogue and monologues for text-to-speech conversion. Create content that sounds natural when spoken aloud."
                        },
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ],
                    "max_tokens": min(content_specs['estimated_tokens'] + 500, 4000),
                    "temperature": 0.7,
                    "top_p": 0.9
                },
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            generated_text = result['choices'][0]['message']['content']
            token_count = result.get('usage', {}).get('total_tokens', 0)
            
            # Estimate actual duration based on generated content
            word_count = len(generated_text.split())
            estimated_duration = word_count / content_specs['effective_wpm']
            
            return GeneratedContent(
                raw_text=generated_text,
                processed_content=[],  # Will be filled in step 4
                estimated_duration=estimated_duration,
                model_used=model.value,
                token_count=token_count
            )
            
        except Exception as e:
            print(f"Error generating content with {model.value}: {e}")
            raise
    
    def process_generated_content(
        self,
        generated_content: GeneratedContent,
        num_people: int
    ) -> GeneratedContent:
        """
        Step 4: Process LLM output into structured format for TTS
        
        Args:
            generated_content: Raw generated content
            num_people: Number of speakers
            
        Returns:
            Processed content ready for TTS
        """
        text = generated_content.raw_text
        processed_content = []
        
        if num_people == 2:
            # Parse dialogue format
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Look for speaker patterns
                speaker_patterns = [
                    r'^(Speaker\s*[A-B]|Person\s*[1-2]|[A-Z][a-z]*)\s*:\s*(.+)$',
                    r'^([A-B])\s*:\s*(.+)$',
                    r'^\*\*([^*]+)\*\*\s*:\s*(.+)$'
                ]
                
                speaker_found = False
                for pattern in speaker_patterns:
                    match = re.match(pattern, line, re.IGNORECASE)
                    if match:
                        speaker_label = match.group(1).strip()
                        content = match.group(2).strip()
                        
                        # Normalize speaker labels
                        if any(x in speaker_label.lower() for x in ['a', '1', 'first']):
                            speaker = "speaker_1"
                        else:
                            speaker = "speaker_2"
                        
                        # Extract emotion if present
                        emotion_match = re.search(r'\[([^\]]+)\]', content)
                        emotion = emotion_match.group(1) if emotion_match else None
                        
                        # Clean content (remove emotion tags)
                        clean_content = re.sub(r'\[([^\]]+)\]', '', content).strip()
                        
                        if clean_content:
                            processed_content.append({
                                "speaker": speaker,
                                "text": clean_content,
                                "emotion": emotion
                            })
                        
                        speaker_found = True
                        break
                
                # If no speaker pattern found, treat as continuation
                if not speaker_found and processed_content:
                    # Add to last speaker's content
                    emotion_match = re.search(r'\[([^\]]+)\]', line)
                    emotion = emotion_match.group(1) if emotion_match else None
                    clean_content = re.sub(r'\[([^\]]+)\]', '', line).strip()
                    
                    if clean_content:
                        last_entry = processed_content[-1]
                        last_entry["text"] += " " + clean_content
                        if emotion and not last_entry["emotion"]:
                            last_entry["emotion"] = emotion
        
        else:
            # Single speaker: split into logical segments
            # Extract emotions and clean text
            emotion_pattern = r'\[([^\]]+)\]'
            segments = re.split(r'(?<=[.!?])\s+(?=\[)', text)
            
            for segment in segments:
                segment = segment.strip()
                if not segment:
                    continue
                
                # Extract emotion
                emotion_match = re.search(emotion_pattern, segment)
                emotion = emotion_match.group(1) if emotion_match else None
                
                # Clean content
                clean_content = re.sub(emotion_pattern, '', segment).strip()
                
                if clean_content:
                    processed_content.append({
                        "speaker": "speaker_1",
                        "text": clean_content,
                        "emotion": emotion
                    })
        
        # Update the generated content with processed data
        generated_content.processed_content = processed_content
        return generated_content
    
    def convert_to_speech(
        self,
        processed_content: GeneratedContent,
        pipeline_input: PipelineInput,
        output_file: str
    ) -> bool:
        """
        Step 5: Convert processed content to speech using ElevenLabs
        
        Args:
            processed_content: Processed content from step 4
            pipeline_input: Original input configuration
            output_file: Output audio file path
            
        Returns:
            Success status
        """
        try:
            voice_config = self.voice_configurations[pipeline_input.voice_style]
            
            if pipeline_input.num_people == 1:
                # Single speaker TTS
                voice = voice_config["single"]
                
                # Combine all text with emotional tags
                full_text = ""
                for segment in processed_content.processed_content:
                    emotion_tag = f"[{segment['emotion']}] " if segment['emotion'] else ""
                    full_text += emotion_tag + segment['text'] + " "
                
                success = self.tts_controller.text_to_speech(
                    text=full_text.strip(),
                    voice_id=voice["voice_id"],
                    model=ElevenLabsModel.MULTILINGUAL_V2,
                    speed=1.0,
                    output_file=output_file
                )
                
                return success
            
            else:
                # Multi-speaker dialogue
                if ELEVENLABS_SDK_AVAILABLE and self.elevenlabs_client:
                    # Use Text-to-Dialogue API if available
                    voices = voice_config["dual"]
                    
                    # Prepare dialogue inputs
                    dialogue_inputs = []
                    for segment in processed_content.processed_content:
                        # Map speaker to voice
                        voice_data = voices[0] if segment["speaker"] == "speaker_1" else voices[1]
                        
                        # Add emotional context
                        emotion_tag = f"[{segment['emotion']}] " if segment['emotion'] else ""
                        text_with_emotion = emotion_tag + segment['text']
                        
                        dialogue_inputs.append({
                            "text": text_with_emotion,
                            "voice_id": voice_data["voice_id"]
                        })
                    
                    # Generate dialogue
                    audio = self.elevenlabs_client.text_to_dialogue.convert(
                        inputs=dialogue_inputs
                    )
                    
                    # Save audio
                    from elevenlabs import save
                    save(audio, output_file)
                    return True
                
                else:
                    # Fallback: Use multi-voice generation
                    conversation_data = []
                    for segment in processed_content.processed_content:
                        conversation_data.append({
                            "speaker": segment["speaker"],
                            "text": segment["text"],
                            "emotion": segment["emotion"]
                        })
                    
                    success = self.tts_controller.multi_voice_generation(
                        script=conversation_data,
                        output_file=output_file
                    )
                    
                    return success
        
        except Exception as e:
            print(f"Error converting to speech: {e}")
            return False
    
    def run_complete_pipeline(
        self,
        description: str,
        num_people: int,
        length_minutes: float,
        content_type: str = "conversation",
        voice_style: str = "professional",
        model: OpenRouterModel = OpenRouterModel.CLAUDE_SONNET_4,
        output_file: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Run the complete pipeline from description to speech
        
        Args:
            description: Description of person(s)
            num_people: 1 or 2 people
            length_minutes: Desired length in minutes
            content_type: Type of content (conversation, presentation, interview, story)
            voice_style: Voice style (professional, casual, dramatic)
            model: OpenRouter model to use
            output_file: Output file (auto-generated if None)
            
        Returns:
            Pipeline results
        """
        print("🚀 Starting OpenRouter + ElevenLabs TTS Pipeline")
        print("=" * 60)
        
        # Step 1: Create pipeline input
        pipeline_input = PipelineInput(
            description=description,
            num_people=num_people,
            length_minutes=length_minutes,
            content_type=content_type,
            voice_style=voice_style,
            model_preference=model
        )
        
        print(f"📝 Input: {description}")
        print(f"👥 People: {num_people}")
        print(f"⏱️ Length: {length_minutes} minutes")
        print(f"🎭 Style: {voice_style} {content_type}")
        print(f"🤖 Model: {model.value}")
        
        # Step 2: Calculate content length
        print("\n📊 Step 2: Calculating content requirements...")
        content_specs = self.calculate_content_length(length_minutes, num_people)
        print(f"Target words: {content_specs['target_words']}")
        print(f"Estimated tokens: {content_specs['estimated_tokens']}")
        print(f"Estimated exchanges: {content_specs['estimated_exchanges']}")
        
        # Step 3: Generate content with LLM
        print(f"\n🧠 Step 3: Generating content with {model.value}...")
        start_time = time.time()
        generated_content = self.generate_content_with_llm(
            pipeline_input, content_specs, model
        )
        generation_time = time.time() - start_time
        print(f"✅ Content generated in {generation_time:.2f}s")
        print(f"Tokens used: {generated_content.token_count}")
        print(f"Estimated duration: {generated_content.estimated_duration:.2f} minutes")
        
        # Step 4: Process content
        print("\n🔄 Step 4: Processing content for TTS...")
        processed_content = self.process_generated_content(
            generated_content, num_people
        )
        print(f"Processed {len(processed_content.processed_content)} segments")
        
        # Step 5: Convert to speech
        if output_file is None:
            timestamp = int(time.time())
            output_file = f"pipeline_output_{timestamp}.mp3"
        
        # Ensure output file is in the output directory
        output_file = self._get_output_path(output_file)
        
        print(f"\n🎤 Step 5: Converting to speech...")
        print(f"Output file: {output_file}")
        
        start_time = time.time()
        success = self.convert_to_speech(
            processed_content, pipeline_input, output_file
        )
        conversion_time = time.time() - start_time
        
        if success:
            print(f"✅ Speech generated in {conversion_time:.2f}s")
            print(f"🎵 Audio saved: {output_file}")
        else:
            print("❌ Speech generation failed")
        
        # Return results
        results = {
            "success": success,
            "output_file": output_file if success else None,
            "generated_content": processed_content,
            "content_specs": content_specs,
            "generation_time": generation_time,
            "conversion_time": conversion_time,
            "total_time": generation_time + conversion_time
        }
        
        print("\n" + "=" * 60)
        print("🎯 Pipeline completed!")
        if success:
            print(f"🎵 Total time: {results['total_time']:.2f}s")
            print(f"📁 Output: {output_file}")
        
        return results


def demo_pipeline():
    """Demonstrate the complete pipeline with multiple examples"""
    
    # Check API keys
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not openrouter_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        print("Get your API key from: https://openrouter.ai/")
        return
    
    if not elevenlabs_key:
        print("❌ ELEVENLABS_API_KEY environment variable not set")
        print("Get your API key from: https://elevenlabs.io/")
        return
    
    # Initialize pipeline
    pipeline = OpenRouterTTSPipeline(openrouter_key, elevenlabs_key)
    
    # Example 1: Single person presentation
    print("\n🎯 Example 1: Single Person Presentation")
    pipeline.run_complete_pipeline(
        description="a tech entrepreneur explaining AI innovation",
        num_people=1,
        length_minutes=1.5,
        content_type="presentation",
        voice_style="professional",
        model=OpenRouterModel.CLAUDE_SONNET_4,
        output_file="ai_presentation.mp3"
    )
    
    # Example 2: Two-person interview
    print("\n🎯 Example 2: Two-Person Interview")
    pipeline.run_complete_pipeline(
        description="a job candidate and HR manager discussing career goals",
        num_people=2,
        length_minutes=2.0,
        content_type="interview",
        voice_style="professional",
        model=OpenRouterModel.GEMINI_2_FLASH,
        output_file="job_interview.mp3"
    )
    
    # Example 3: Casual conversation
    print("\n🎯 Example 3: Casual Conversation")
    pipeline.run_complete_pipeline(
        description="two friends discussing their weekend plans",
        num_people=2,
        length_minutes=1.0,
        content_type="conversation",
        voice_style="casual",
        model=OpenRouterModel.DEEPSEEK_V3_FREE,
        output_file="weekend_plans.mp3"
    )
    
    # Example 4: Dramatic story
    print("\n🎯 Example 4: Dramatic Story")
    pipeline.run_complete_pipeline(
        description="a storyteller narrating a mysterious adventure",
        num_people=1,
        length_minutes=2.5,
        content_type="story",
        voice_style="dramatic",
        model=OpenRouterModel.GEMINI_25_FLASH,
        output_file="mystery_story.mp3"
    )
    
    print("\n🎉 All examples completed!")
    print("Generated files:")
    print("- ai_presentation.mp3")
    print("- job_interview.mp3") 
    print("- weekend_plans.mp3")
    print("- mystery_story.mp3")


if __name__ == "__main__":
    demo_pipeline() 