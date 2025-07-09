"""
Google Gemini AI analyzer for video, audio, and image understanding.

Provides AI-powered multimodal analysis using Google's Gemini model including:
- Video description, transcription, and scene analysis
- Audio transcription, content analysis, and event detection
- Image description, classification, and object detection
- OCR text extraction from images
- Question answering about any media content
- Composition and technical analysis
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
    """Google Gemini video, audio, and image understanding analyzer."""
    
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
    
    def upload_image(self, image_path: Path) -> str:
        """Upload image to Gemini and return file ID."""
        try:
            print(f"📤 Uploading image: {image_path.name}")
            
            # Check file size
            file_size = image_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.1f} MB")
            
            # Upload file
            image_file = genai.upload_file(str(image_path))
            print(f"✅ Upload complete. File ID: {image_file.name}")
            
            # Images don't need processing time like videos
            print("🎯 Image ready for analysis")
            return image_file.name
            
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
        """Answer specific questions about the video."""
        try:
            file_id = self.upload_video(video_path)
            video_file = genai.get_file(file_id)
            
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            prompt = f"""Analyze this video and answer the following questions:

{questions_text}

Provide detailed, accurate answers based on what you observe in the video. If a question cannot be answered from the video content, please state that clearly."""
            
            print("❓ Answering questions about video...")
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
        """Analyze video scenes and create timeline breakdown."""
        try:
            file_id = self.upload_video(video_path)
            video_file = genai.get_file(file_id)
            
            prompt = """Analyze this video and break it down into distinct scenes or segments. For each scene, provide:
1. Start and end timestamps (approximate)
2. Scene description and main content
3. Key visual elements and actions
4. Audio content (speech, music, effects)
5. Scene transitions and cuts

Create a detailed timeline of the video content."""
            
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
        """Extract key information and insights from video."""
        try:
            file_id = self.upload_video(video_path)
            video_file = genai.get_file(file_id)
            
            prompt = """Extract key information from this video including:
1. Main topics and themes
2. Important facts or data mentioned
3. Key people, places, or objects
4. Notable quotes or statements
5. Action items or conclusions
6. Technical specifications if relevant
7. Timestamps for important moments

Provide structured, actionable information."""
            
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
        """Generate audio description and summary."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            if detailed:
                prompt = """Analyze this audio file in detail and provide:
1. Overall content summary and type
2. Speech content (if any) - transcription and analysis
3. Music analysis (genre, style, instruments, mood)
4. Sound effects and environmental audio
5. Audio quality and technical characteristics
6. Emotional tone and atmosphere
7. Notable segments with timestamps

Provide comprehensive audio analysis."""
            else:
                prompt = """Provide a concise description of this audio including:
- Type of audio content (speech, music, sounds, etc.)
- Main characteristics and quality
- Brief summary of content
- Duration and overall impression"""
            
            print("🤖 Generating audio description...")
            response = self.model.generate_content([audio_file, prompt])
            
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
            print(f"❌ Audio description failed: {e}")
            raise
    
    def transcribe_audio(self, audio_path: Path, include_timestamps: bool = True, 
                        speaker_identification: bool = True) -> Dict[str, Any]:
        """Transcribe spoken content from audio."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            prompt_parts = ["Transcribe all spoken content in this audio file."]
            
            if include_timestamps:
                prompt_parts.append("Include approximate timestamps for each segment.")
            
            if speaker_identification:
                prompt_parts.append("Identify different speakers and label them consistently.")
            
            prompt_parts.extend([
                "Note any non-speech audio (music, sound effects, silence).",
                "Format as a clean, readable transcript."
            ])
            
            prompt = " ".join(prompt_parts)
            
            print("🎤 Transcribing audio...")
            response = self.model.generate_content([audio_file, prompt])
            
            result = {
                'file_id': file_id,
                'transcription': response.text,
                'include_timestamps': include_timestamps,
                'speaker_identification': speaker_identification,
                'analysis_type': 'transcription'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Audio transcription failed: {e}")
            raise
    
    def analyze_audio_content(self, audio_path: Path) -> Dict[str, Any]:
        """Analyze audio content for type, genre, mood, etc."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            prompt = """Analyze the content and characteristics of this audio:
1. Content type (speech, music, podcast, etc.)
2. If music: genre, style, instruments, tempo, mood
3. If speech: language, accent, speaking style, emotion
4. Audio quality and production characteristics
5. Background sounds or effects
6. Overall mood and atmosphere
7. Technical observations (compression, recording quality)

Provide detailed content analysis."""
            
            print("🎵 Analyzing audio content...")
            response = self.model.generate_content([audio_file, prompt])
            
            result = {
                'file_id': file_id,
                'content_analysis': response.text,
                'analysis_type': 'content_analysis'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Audio content analysis failed: {e}")
            raise
    
    def answer_audio_questions(self, audio_path: Path, questions: List[str]) -> Dict[str, Any]:
        """Answer specific questions about the audio."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            prompt = f"""Listen to this audio and answer the following questions:

{questions_text}

Provide detailed, accurate answers based on what you hear in the audio. If a question cannot be answered from the audio content, please state that clearly."""
            
            print("❓ Answering questions about audio...")
            response = self.model.generate_content([audio_file, prompt])
            
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
            print(f"❌ Audio Q&A failed: {e}")
            raise
    
    def detect_audio_events(self, audio_path: Path) -> Dict[str, Any]:
        """Detect and analyze specific events in audio."""
        try:
            file_id = self.upload_audio(audio_path)
            audio_file = genai.get_file(file_id)
            
            prompt = """Analyze this audio and detect specific events or segments:
1. Speech segments with speaker changes
2. Music segments and style changes
3. Sound effects and environmental sounds
4. Silence or quiet periods
5. Volume or intensity changes
6. Notable audio events with timestamps
7. Transitions between different types of content

Create a detailed timeline of audio events."""
            
            print("🔍 Detecting audio events...")
            response = self.model.generate_content([audio_file, prompt])
            
            result = {
                'file_id': file_id,
                'event_detection': response.text,
                'analysis_type': 'event_detection'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Audio event detection failed: {e}")
            raise
    
    def describe_image(self, image_path: Path, detailed: bool = False) -> Dict[str, Any]:
        """Generate image description and summary."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            if detailed:
                prompt = """Analyze this image in detail and provide:
1. Overall description and main subject
2. Objects, people, and animals present
3. Setting, location, and environment
4. Colors, lighting, and composition
5. Style, mood, and atmosphere
6. Technical qualities (resolution, clarity, etc.)
7. Any text or writing visible
8. Notable details and interesting elements

Provide comprehensive visual analysis."""
            else:
                prompt = """Provide a concise description of this image including:
- Main subject and content
- Key visual elements
- Setting or location
- Overall impression and style"""
            
            print("🤖 Generating image description...")
            response = self.model.generate_content([image_file, prompt])
            
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
            print(f"❌ Image description failed: {e}")
            raise
    
    def classify_image(self, image_path: Path) -> Dict[str, Any]:
        """Classify image content and categorize."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            prompt = """Classify and categorize this image:
1. Primary category (portrait, landscape, object, scene, etc.)
2. Content type (photograph, artwork, diagram, screenshot, etc.)
3. Subject classification (people, animals, nature, architecture, etc.)
4. Style or genre (if applicable)
5. Purpose or context (professional, casual, artistic, etc.)
6. Technical classification (color/black&white, digital/analog, etc.)

Provide structured classification with confidence levels where possible."""
            
            print("🏷️ Classifying image...")
            response = self.model.generate_content([image_file, prompt])
            
            result = {
                'file_id': file_id,
                'classification': response.text,
                'analysis_type': 'classification'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Image classification failed: {e}")
            raise
    
    def detect_objects(self, image_path: Path, detailed: bool = False) -> Dict[str, Any]:
        """Detect and identify objects in the image."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            if detailed:
                prompt = """Detect and analyze all objects in this image:
1. List all identifiable objects with locations
2. Count quantities where applicable
3. Describe object relationships and interactions
4. Note object conditions, colors, and characteristics
5. Identify brands, text, or labels on objects
6. Describe spatial arrangement and composition
7. Note any unusual or noteworthy objects

Provide comprehensive object detection analysis."""
            else:
                prompt = """Identify the main objects visible in this image:
- List primary objects and items
- Note their general locations
- Include approximate counts
- Mention any notable characteristics"""
            
            print("🔍 Detecting objects in image...")
            response = self.model.generate_content([image_file, prompt])
            
            result = {
                'file_id': file_id,
                'object_detection': response.text,
                'detailed': detailed,
                'analysis_type': 'object_detection'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Object detection failed: {e}")
            raise
    
    def answer_image_questions(self, image_path: Path, questions: List[str]) -> Dict[str, Any]:
        """Answer specific questions about the image."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            prompt = f"""Examine this image carefully and answer the following questions:

{questions_text}

Provide detailed, accurate answers based on what you can see in the image. If a question cannot be answered from the visual content, please state that clearly."""
            
            print("❓ Answering questions about image...")
            response = self.model.generate_content([image_file, prompt])
            
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
            print(f"❌ Image Q&A failed: {e}")
            raise
    
    def extract_text_from_image(self, image_path: Path) -> Dict[str, Any]:
        """Extract and transcribe text from image (OCR)."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            prompt = """Extract all text visible in this image:
1. Transcribe all readable text accurately
2. Preserve formatting and layout where possible
3. Note text locations (top, center, bottom, etc.)
4. Identify different text styles (headlines, body, captions)
5. Note any partially visible or unclear text
6. Include text orientation and direction
7. Describe the context of text elements

Provide complete text extraction with structure."""
            
            print("📝 Extracting text from image...")
            response = self.model.generate_content([image_file, prompt])
            
            result = {
                'file_id': file_id,
                'extracted_text': response.text,
                'analysis_type': 'text_extraction'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Text extraction failed: {e}")
            raise
    
    def analyze_image_composition(self, image_path: Path) -> Dict[str, Any]:
        """Analyze image composition, style, and technical aspects."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            prompt = """Analyze the composition and technical aspects of this image:
1. Composition techniques (rule of thirds, symmetry, leading lines, etc.)
2. Lighting analysis (natural/artificial, direction, quality, mood)
3. Color palette and color harmony
4. Depth of field and focus areas
5. Perspective and viewpoint
6. Visual balance and weight distribution
7. Style and artistic elements
8. Technical quality and characteristics

Provide detailed photographic/artistic analysis."""
            
            print("🎨 Analyzing image composition...")
            response = self.model.generate_content([image_file, prompt])
            
            result = {
                'file_id': file_id,
                'composition_analysis': response.text,
                'analysis_type': 'composition'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Composition analysis failed: {e}")
            raise


def check_gemini_requirements() -> tuple[bool, str]:
    """Check if Gemini requirements are met."""
    if not GEMINI_AVAILABLE:
        return False, "Google GenerativeAI library not installed"
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return False, "GEMINI_API_KEY environment variable not set"
    
    try:
        # Test API connection
        genai.configure(api_key=api_key)
        models = list(genai.list_models())
        return True, "Gemini API ready"
    except Exception as e:
        return False, f"Gemini API error: {str(e)}"