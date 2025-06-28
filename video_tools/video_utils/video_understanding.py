"""
Google Gemini video understanding utilities.

Provides AI-powered video analysis including:
- Video description and summarization
- Audio transcription and extraction
- Visual content analysis
- Question answering about video content
- Scene detection and timestamps
"""

import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
import os

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class GeminiVideoAnalyzer:
    """Google Gemini video and audio understanding analyzer."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with API key."""
        if not GEMINI_AVAILABLE:
            raise ImportError(
                "Google GenerativeAI not installed. Run: pip install google-generativeai"
            )
        
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Gemini API key required. Set GEMINI_API_KEY environment variable or pass api_key parameter"
            )
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def upload_video(self, video_path: Path) -> str:
        """Upload video to Gemini and return file ID."""
        try:
            print(f"📤 Uploading video: {video_path.name}")
            
            # Check file size (20MB limit for inline)
            file_size = video_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.1f} MB")
            
            if file_size > 20:
                print("📁 Large file detected, using File API...")
            
            # Upload file
            video_file = genai.upload_file(str(video_path))
            print(f"✅ Upload complete. File ID: {video_file.name}")
            
            # Wait for processing
            while video_file.state.name == "PROCESSING":
                print("⏳ Processing video...")
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise Exception(f"Video processing failed: {video_file.state}")
            
            print("🎯 Video ready for analysis")
            return video_file.name
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            raise
    
    def upload_audio(self, audio_path: Path) -> str:
        """Upload audio to Gemini and return file ID."""
        try:
            print(f"📤 Uploading audio: {audio_path.name}")
            
            # Check file size (20MB limit for inline)
            file_size = audio_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.1f} MB")
            
            if file_size > 20:
                print("📁 Large file detected, using File API...")
            
            # Upload file
            audio_file = genai.upload_file(str(audio_path))
            print(f"✅ Upload complete. File ID: {audio_file.name}")
            
            # Wait for processing
            while audio_file.state.name == "PROCESSING":
                print("⏳ Processing audio...")
                time.sleep(2)
                audio_file = genai.get_file(audio_file.name)
            
            if audio_file.state.name == "FAILED":
                raise Exception(f"Audio processing failed: {audio_file.state}")
            
            print("🎯 Audio ready for analysis")
            return audio_file.name
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            raise
    
    def describe_video(self, video_path: Path, detailed: bool = False) -> Dict[str, Any]:
        """Generate video description and summary."""
        try:
            file_id = self.upload_video(video_path)
            video_file = genai.get_file(file_id)
            
            if detailed:
                prompt = """Analyze this video in detail and provide:
1. Overall summary and main topic
2. Key scenes and their timestamps
3. Visual elements (objects, people, settings, actions)
4. Audio content (speech, music, sounds)
5. Mood and tone
6. Technical observations (quality, style, etc.)

Provide structured analysis with clear sections."""
            else:
                prompt = """Provide a concise description of this video including:
- Main content and topic
- Key visual elements
- Brief summary of what happens
- Duration and pacing"""
            
            print("🤖 Generating video description...")
            response = self.model.generate_content([video_file, prompt])
            
            result = {
                'file_id': file_id,
                'description': response.text,
                'detailed': detailed,
                'analysis_type': 'description'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Description failed: {e}")
            raise
    
    def transcribe_video(self, video_path: Path, include_timestamps: bool = True) -> Dict[str, Any]:
        """Transcribe audio content from video."""
        try:
            file_id = self.upload_video(video_path)
            video_file = genai.get_file(file_id)
            
            if include_timestamps:
                prompt = """Transcribe all spoken content in this video. Include:
1. Complete transcription of all speech
2. Speaker identification if multiple speakers
3. Approximate timestamps for each segment
4. Note any non-speech audio (music, sound effects, silence)

Format as a clean, readable transcript with timestamps."""
            else:
                prompt = """Provide a complete transcription of all spoken content in this video. 
Focus on accuracy and readability. Include speaker changes if multiple people speak."""
            
            print("🎤 Transcribing video audio...")
            response = self.model.generate_content([video_file, prompt])
            
            result = {
                'file_id': file_id,
                'transcription': response.text,
                'include_timestamps': include_timestamps,
                'analysis_type': 'transcription'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            raise
    
    def answer_questions(self, video_path: Path, questions: List[str]) -> Dict[str, Any]:
        """Answer specific questions about video content."""
        try:
            file_id = self.upload_video(video_path)
            video_file = genai.get_file(file_id)
            
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            prompt = f"""Analyze this video and answer the following questions with specific details and timestamps when relevant:

{questions_text}

For each question, provide:
- A direct answer
- Supporting evidence from the video
- Relevant timestamps if applicable
- Confidence level in your answer"""
            
            print(f"❓ Answering {len(questions)} questions about video...")
            response = self.model.generate_content([video_file, prompt])
            
            result = {
                'file_id': file_id,
                'questions': questions,
                'answers': response.text,
                'analysis_type': 'qa'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Q&A failed: {e}")
            raise
    
    def analyze_scenes(self, video_path: Path) -> Dict[str, Any]:
        """Analyze video scenes and detect key moments."""
        try:
            file_id = self.upload_video(video_path)
            video_file = genai.get_file(file_id)
            
            prompt = """Analyze this video and identify key scenes/segments. For each scene provide:
1. Start and end timestamps
2. Description of what happens
3. Key visual elements
4. Important dialogue or audio
5. Scene transitions and changes

Format as a structured breakdown of the video timeline."""
            
            print("🎬 Analyzing video scenes...")
            response = self.model.generate_content([video_file, prompt])
            
            result = {
                'file_id': file_id,
                'scene_analysis': response.text,
                'analysis_type': 'scenes'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Scene analysis failed: {e}")
            raise
    
    def extract_key_info(self, video_path: Path) -> Dict[str, Any]:
        """Extract key information and metadata from video."""
        try:
            file_id = self.upload_video(video_path)
            video_file = genai.get_file(file_id)
            
            prompt = """Extract and summarize key information from this video:
1. Main topic/subject
2. Key people mentioned or shown
3. Important dates, numbers, or facts
4. Locations mentioned or shown
5. Main takeaways or conclusions
6. Notable quotes or statements
7. Technical terms or concepts

Present as a structured summary with clear categories."""
            
            print("🔍 Extracting key information...")
            response = self.model.generate_content([video_file, prompt])
            
            result = {
                'file_id': file_id,
                'key_info': response.text,
                'analysis_type': 'extraction'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Key info extraction failed: {e}")
            raise
    
    def describe_audio(self, audio_path: Path, detailed: bool = False) -> Dict[str, Any]:
        """Generate audio description and analysis."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            if detailed:
                prompt = """Analyze this audio file in detail and provide:
1. Overall content summary and main topics
2. Audio quality and technical characteristics
3. Speech analysis (speakers, language, tone, pace)
4. Background sounds and music description
5. Emotional tone and mood
6. Key timestamps and segments
7. Notable acoustic features

Provide structured analysis with clear sections."""
            else:
                prompt = """Describe this audio file including:
- Main content and topic
- Type of audio (speech, music, sounds, etc.)
- Number of speakers if applicable
- Overall quality and characteristics
- Brief summary of what you hear"""
            
            print("🤖 Generating audio description...")
            response = self.model.generate_content([audio_file, prompt])
            
            result = {
                'file_id': file_id,
                'description': response.text,
                'detailed': detailed,
                'analysis_type': 'audio_description'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Audio description failed: {e}")
            raise
    
    def transcribe_audio(self, audio_path: Path, include_timestamps: bool = True, 
                        speaker_identification: bool = True) -> Dict[str, Any]:
        """Transcribe audio content with enhanced features."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            prompt_parts = ["Transcribe this audio file with high accuracy."]
            
            if include_timestamps:
                prompt_parts.append("Include precise timestamps for each segment.")
            
            if speaker_identification:
                prompt_parts.append("Identify and label different speakers if multiple people speak.")
            
            prompt_parts.extend([
                "Note any background sounds, music, or audio effects.",
                "Indicate pauses, emphasis, or emotional tone where relevant.",
                "Format as a clean, professional transcript."
            ])
            
            prompt = " ".join(prompt_parts)
            
            print("🎤 Transcribing audio with enhanced features...")
            response = self.model.generate_content([audio_file, prompt])
            
            result = {
                'file_id': file_id,
                'transcription': response.text,
                'include_timestamps': include_timestamps,
                'speaker_identification': speaker_identification,
                'analysis_type': 'audio_transcription'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Audio transcription failed: {e}")
            raise
    
    def analyze_audio_content(self, audio_path: Path) -> Dict[str, Any]:
        """Analyze audio for content, quality, and acoustic features."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            prompt = """Analyze this audio file comprehensively and provide:

1. Content Analysis:
   - Main topics and themes
   - Type of content (conversation, lecture, music, etc.)
   - Key messages or information

2. Technical Analysis:
   - Audio quality assessment
   - Recording environment characteristics
   - Noise levels and clarity

3. Speaker Analysis (if applicable):
   - Number of speakers
   - Gender and approximate age
   - Speaking style and tone
   - Language and accent characteristics

4. Acoustic Features:
   - Background sounds or music
   - Audio effects or processing
   - Dynamic range and volume levels
   - Notable acoustic events

5. Temporal Analysis:
   - Duration and pacing
   - Silent periods or pauses
   - Key timestamps for important segments

Provide detailed insights with specific examples and timestamps."""
            
            print("🔍 Analyzing audio content and features...")
            response = self.model.generate_content([audio_file, prompt])
            
            result = {
                'file_id': file_id,
                'analysis': response.text,
                'analysis_type': 'audio_content_analysis'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Audio analysis failed: {e}")
            raise
    
    def answer_audio_questions(self, audio_path: Path, questions: List[str]) -> Dict[str, Any]:
        """Answer specific questions about audio content."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            prompt = f"""Listen to this audio file and answer the following questions with specific details and timestamps when relevant:

{questions_text}

For each question, provide:
- A direct answer
- Supporting evidence from the audio
- Relevant timestamps if applicable
- Confidence level in your answer
- Any additional context that might be helpful"""
            
            print(f"❓ Answering {len(questions)} questions about audio...")
            response = self.model.generate_content([audio_file, prompt])
            
            result = {
                'file_id': file_id,
                'questions': questions,
                'answers': response.text,
                'analysis_type': 'audio_qa'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Audio Q&A failed: {e}")
            raise
    
    def detect_audio_events(self, audio_path: Path) -> Dict[str, Any]:
        """Detect and catalog specific events, sounds, or segments in audio."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            prompt = """Analyze this audio file and detect specific events, sounds, and segments. Provide:

1. Speech Events:
   - When people start/stop speaking
   - Changes in speakers
   - Emotional changes in speech

2. Non-Speech Sounds:
   - Background music or noise
   - Sound effects or environmental sounds
   - Technical sounds (phone rings, notifications, etc.)

3. Audio Quality Events:
   - Volume changes
   - Audio dropouts or glitches
   - Echo or reverb changes

4. Content Markers:
   - Topic changes
   - Important statements or quotes
   - Questions being asked

5. Temporal Segments:
   - Natural break points
   - Distinct sections or chapters
   - Key moments for indexing

Format as a timeline with precise timestamps and descriptions."""
            
            print("🕵️ Detecting audio events and segments...")
            response = self.model.generate_content([audio_file, prompt])
            
            result = {
                'file_id': file_id,
                'events': response.text,
                'analysis_type': 'audio_event_detection'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Audio event detection failed: {e}")
            raise


def check_gemini_requirements() -> tuple[bool, str]:
    """Check if Gemini API requirements are met."""
    if not GEMINI_AVAILABLE:
        return False, "google-generativeai package not installed"
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return False, "GEMINI_API_KEY environment variable not set"
    
    return True, "Gemini API ready"


def save_analysis_result(result: Dict[str, Any], output_path: Path) -> bool:
    """Save analysis result to JSON file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"💾 Analysis saved to: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to save analysis: {e}")
        return False


def analyze_video_file(video_path: Path, analysis_type: str = "description", 
                      questions: Optional[List[str]] = None, 
                      detailed: bool = False) -> Optional[Dict[str, Any]]:
    """Convenience function to analyze a video file."""
    try:
        analyzer = GeminiVideoAnalyzer()
        
        if analysis_type == "description":
            return analyzer.describe_video(video_path, detailed)
        elif analysis_type == "transcription":
            return analyzer.transcribe_video(video_path, include_timestamps=True)
        elif analysis_type == "qa":
            if not questions:
                questions = ["What is the main topic of this video?", 
                           "What are the key points discussed?"]
            return analyzer.answer_questions(video_path, questions)
        elif analysis_type == "scenes":
            return analyzer.analyze_scenes(video_path)
        elif analysis_type == "extraction":
            return analyzer.extract_key_info(video_path)
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
            
    except Exception as e:
        print(f"❌ Video analysis failed: {e}")
        return None


def analyze_audio_file(audio_path: Path, analysis_type: str = "description", 
                      questions: Optional[List[str]] = None, 
                      detailed: bool = False,
                      speaker_identification: bool = True) -> Optional[Dict[str, Any]]:
    """Convenience function to analyze an audio file."""
    try:
        analyzer = GeminiVideoAnalyzer()
        
        if analysis_type == "description":
            return analyzer.describe_audio(audio_path, detailed)
        elif analysis_type == "transcription":
            return analyzer.transcribe_audio(audio_path, include_timestamps=True, 
                                           speaker_identification=speaker_identification)
        elif analysis_type == "content_analysis":
            return analyzer.analyze_audio_content(audio_path)
        elif analysis_type == "qa":
            if not questions:
                questions = ["What is the main topic of this audio?", 
                           "Who is speaking and what are they discussing?"]
            return analyzer.answer_audio_questions(audio_path, questions)
        elif analysis_type == "events":
            return analyzer.detect_audio_events(audio_path)
        else:
            raise ValueError(f"Unknown audio analysis type: {analysis_type}")
            
    except Exception as e:
        print(f"❌ Audio analysis failed: {e}")
        return None