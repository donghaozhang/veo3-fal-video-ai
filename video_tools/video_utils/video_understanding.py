"""
Google Gemini video, audio, and image understanding utilities.

Provides AI-powered multimodal analysis including:
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

try:
    from openai import OpenAI
    OPENAI_WHISPER_API_AVAILABLE = True
except ImportError:
    OPENAI_WHISPER_API_AVAILABLE = False

try:
    import whisper
    WHISPER_LOCAL_AVAILABLE = True
except ImportError:
    WHISPER_LOCAL_AVAILABLE = False


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
    
    def upload_image(self, image_path: Path) -> str:
        """Upload image to Gemini and return file ID."""
        try:
            print(f"📤 Uploading image: {image_path.name}")
            
            # Check file size (20MB limit for inline)
            file_size = image_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.1f} MB")
            
            if file_size > 20:
                print("📁 Large file detected, using File API...")
            
            # Upload file
            image_file = genai.upload_file(str(image_path))
            print(f"✅ Upload complete. File ID: {image_file.name}")
            
            # Wait for processing
            while image_file.state.name == "PROCESSING":
                print("⏳ Processing image...")
                time.sleep(1)
                image_file = genai.get_file(image_file.name)
            
            if image_file.state.name == "FAILED":
                raise Exception(f"Image processing failed: {image_file.state}")
            
            print("🎯 Image ready for analysis")
            return image_file.name
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            raise
    
    def describe_image(self, image_path: Path, detailed: bool = False) -> Dict[str, Any]:
        """Generate comprehensive image description and analysis."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            if detailed:
                prompt = """Analyze this image in detail and provide:
1. Overall description and main subject
2. Visual composition (layout, colors, lighting, style)
3. Objects and people (detailed descriptions and positions)
4. Setting and environment (location, background, context)
5. Activities and actions (what's happening)
6. Mood and atmosphere (emotional tone, feeling)
7. Technical aspects (quality, perspective, artistic elements)
8. Notable details and interesting features

Provide structured analysis with clear sections and specific details."""
            else:
                prompt = """Describe this image including:
- Main subject and content
- Key visual elements and objects
- Setting and environment
- Overall composition and style
- Notable details or interesting aspects

Provide a clear, concise description."""
            
            print("🤖 Generating image description...")
            response = self.model.generate_content([image_file, prompt])
            
            result = {
                'file_id': file_id,
                'description': response.text,
                'detailed': detailed,
                'analysis_type': 'image_description'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Image description failed: {e}")
            raise
    
    def classify_image(self, image_path: Path) -> Dict[str, Any]:
        """Classify and categorize image content."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            prompt = """Analyze and classify this image:

1. Primary Category:
   - Determine the main type/category of this image
   - Examples: photograph, artwork, diagram, screenshot, document, etc.

2. Content Classification:
   - Subject matter (people, animals, objects, landscapes, etc.)
   - Scene type (indoor/outdoor, urban/natural, etc.)
   - Activity or event depicted

3. Style and Format:
   - Artistic style or photographic type
   - Color scheme and visual characteristics
   - Technical format observations

4. Context and Purpose:
   - Likely purpose or use case
   - Professional vs casual context
   - Informational vs artistic intent

5. Key Features:
   - Most prominent elements
   - Distinctive characteristics
   - Quality and technical aspects

Provide clear categorization with confidence levels where appropriate."""
            
            print("🏷️ Classifying image content...")
            response = self.model.generate_content([image_file, prompt])
            
            result = {
                'file_id': file_id,
                'classification': response.text,
                'analysis_type': 'image_classification'
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
                prompt = """Perform detailed object detection on this image:

1. Object Identification:
   - List all visible objects with precise names
   - Include size estimates (small, medium, large)
   - Note object conditions and states

2. Location and Positioning:
   - Describe where each object is located in the image
   - Spatial relationships between objects
   - Approximate positions (left, right, center, foreground, background)

3. Object Characteristics:
   - Colors, textures, materials
   - Shapes and forms
   - Notable features or details

4. People and Faces:
   - Number of people visible
   - Approximate ages, genders if discernible
   - Clothing and appearance
   - Actions and poses

5. Text and Signage:
   - Any visible text or writing
   - Signs, labels, or captions
   - Readable information

6. Contextual Elements:
   - Setting and environment objects
   - Architectural elements
   - Natural features

Provide systematic object-by-object analysis with specific details."""
            else:
                prompt = """Identify and list the main objects visible in this image:

- Primary objects and subjects
- People (if any) with basic descriptions
- Notable items and elements
- Text or signage (if readable)
- Environmental objects and features

Provide a clear list with brief descriptions of each detected object."""
            
            print("🔍 Detecting objects in image...")
            response = self.model.generate_content([image_file, prompt])
            
            result = {
                'file_id': file_id,
                'objects': response.text,
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
        """Answer specific questions about the image content."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            prompt = f"""Examine this image carefully and answer the following questions with specific details:

{questions_text}

For each question, provide:
- A direct, specific answer based on what you can see
- Supporting visual evidence from the image
- Location details if relevant (where in the image)
- Confidence level in your answer
- Any additional relevant context

Base your answers only on what is clearly visible in the image."""
            
            print(f"❓ Answering {len(questions)} questions about image...")
            response = self.model.generate_content([image_file, prompt])
            
            result = {
                'file_id': file_id,
                'questions': questions,
                'answers': response.text,
                'analysis_type': 'image_qa'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Image Q&A failed: {e}")
            raise
    
    def extract_text_from_image(self, image_path: Path) -> Dict[str, Any]:
        """Extract and transcribe text visible in the image (OCR)."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            prompt = """Extract all text visible in this image:

1. Text Content:
   - Transcribe all readable text exactly as it appears
   - Include headers, body text, captions, labels
   - Preserve formatting and structure where possible

2. Text Location and Context:
   - Describe where each text element is located
   - Note the type of text (sign, document, label, etc.)
   - Identify different text sections or groupings

3. Text Characteristics:
   - Font styles and sizes (if notable)
   - Colors and formatting
   - Language(s) used

4. Readability Assessment:
   - Which text is clearly readable
   - Which text is partially obscured or unclear
   - Overall text quality and clarity

5. Contextual Information:
   - Purpose of the text (informational, decorative, etc.)
   - Relationship to other image elements
   - Any important semantic meaning

If no text is visible, clearly state that no readable text was found."""
            
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
        """Analyze artistic and technical composition of the image."""
        try:
            file_id = self.upload_image(image_path)
            image_file = genai.get_file(file_id)
            
            prompt = """Analyze the artistic and technical composition of this image:

1. Visual Composition:
   - Rule of thirds and compositional guidelines
   - Balance and symmetry
   - Leading lines and focal points
   - Depth and perspective

2. Color Analysis:
   - Color palette and scheme
   - Dominant colors and accents
   - Color harmony and contrast
   - Mood created by colors

3. Lighting and Exposure:
   - Light source and direction
   - Shadows and highlights
   - Overall exposure quality
   - Mood created by lighting

4. Technical Quality:
   - Sharpness and focus
   - Image resolution and clarity
   - Noise or artifacts
   - Professional vs amateur quality

5. Artistic Elements:
   - Style and aesthetic approach
   - Framing and cropping
   - Artistic techniques used
   - Overall visual impact

6. Mood and Atmosphere:
   - Emotional tone conveyed
   - Atmosphere and feeling
   - Artistic intent or message

Provide detailed analysis focusing on both technical and artistic aspects."""
            
            print("🎨 Analyzing image composition...")
            response = self.model.generate_content([image_file, prompt])
            
            result = {
                'file_id': file_id,
                'composition_analysis': response.text,
                'analysis_type': 'composition_analysis'
            }
            
            # Clean up uploaded file
            genai.delete_file(file_id)
            print("🗑️ Cleaned up uploaded file")
            
            return result
            
        except Exception as e:
            print(f"❌ Composition analysis failed: {e}")
            raise


class WhisperTranscriber:
    """OpenAI Whisper speech-to-text transcriber supporting both API and local models."""
    
    def __init__(self, api_key: Optional[str] = None, use_local: bool = False):
        """Initialize Whisper transcriber with API key or local model."""
        self.use_local = use_local
        
        if use_local:
            if not WHISPER_LOCAL_AVAILABLE:
                raise ImportError(
                    "Local Whisper not installed. Run: pip install openai-whisper"
                )
            self.model = None  # Will be loaded on first use
        else:
            if not OPENAI_WHISPER_API_AVAILABLE:
                raise ImportError(
                    "OpenAI package not installed. Run: pip install openai"
                )
            
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError(
                    "OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter"
                )
            
            self.client = OpenAI(api_key=self.api_key)
    
    def _load_local_model(self, model_size: str = "turbo"):
        """Load local Whisper model on demand."""
        if self.model is None:
            print(f"🔄 Loading Whisper {model_size} model...")
            self.model = whisper.load_model(model_size)
            print(f"✅ Whisper {model_size} model loaded")
        return self.model
    
    def transcribe_audio_file(self, audio_path: Path, 
                             language: Optional[str] = None,
                             model_size: str = "turbo",
                             include_timestamps: bool = True,
                             response_format: str = "json") -> Dict[str, Any]:
        """Transcribe audio file using Whisper API or local model."""
        try:
            print(f"🎤 Transcribing: {audio_path.name}")
            
            # Check file size (25MB limit for API)
            file_size = audio_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.1f} MB")
            
            if not self.use_local and file_size > 25:
                print("⚠️  File exceeds 25MB API limit, switching to local model...")
                if not WHISPER_LOCAL_AVAILABLE:
                    raise Exception("File too large for API and local Whisper not available")
                self.use_local = True
            
            if self.use_local:
                return self._transcribe_local(audio_path, model_size, include_timestamps)
            else:
                return self._transcribe_api(audio_path, language, response_format)
                
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
            raise
    
    def _transcribe_api(self, audio_path: Path, language: Optional[str], response_format: str) -> Dict[str, Any]:
        """Transcribe using OpenAI API."""
        try:
            print("🌐 Using OpenAI Whisper API...")
            
            with open(audio_path, "rb") as audio_file:
                kwargs = {
                    "model": "whisper-1",
                    "file": audio_file,
                    "response_format": response_format
                }
                
                if language:
                    kwargs["language"] = language
                
                if response_format == "verbose_json":
                    kwargs["timestamp_granularities"] = ["word", "segment"]
                
                transcription = self.client.audio.transcriptions.create(**kwargs)
            
            # Process response based on format
            if response_format == "json" or response_format == "verbose_json":
                if hasattr(transcription, 'text'):
                    result = {
                        'text': transcription.text,
                        'method': 'openai_api',
                        'model': 'whisper-1',
                        'language': getattr(transcription, 'language', language),
                        'duration': getattr(transcription, 'duration', None)
                    }
                    
                    # Add segments and words if available
                    if hasattr(transcription, 'segments'):
                        result['segments'] = transcription.segments
                    if hasattr(transcription, 'words'):
                        result['words'] = transcription.words
                else:
                    # Handle string response
                    result = {
                        'text': str(transcription),
                        'method': 'openai_api',
                        'model': 'whisper-1',
                        'language': language
                    }
            else:
                # Handle other formats (srt, vtt, etc.)
                result = {
                    'text': str(transcription),
                    'method': 'openai_api',
                    'model': 'whisper-1',
                    'format': response_format,
                    'language': language
                }
            
            print("✅ API transcription complete")
            return result
            
        except Exception as e:
            print(f"❌ API transcription failed: {e}")
            raise
    
    def _transcribe_local(self, audio_path: Path, model_size: str, include_timestamps: bool) -> Dict[str, Any]:
        """Transcribe using local Whisper model."""
        try:
            print(f"💻 Using local Whisper {model_size} model...")
            
            model = self._load_local_model(model_size)
            
            # Transcribe with options
            options = {
                "fp16": False,  # Use fp32 for better compatibility
                "language": None,  # Auto-detect language
            }
            
            result = model.transcribe(str(audio_path), **options)
            
            # Structure the response
            transcription_result = {
                'text': result['text'],
                'method': 'local_whisper',
                'model': model_size,
                'language': result.get('language'),
                'duration': None
            }
            
            if include_timestamps and 'segments' in result:
                transcription_result['segments'] = [
                    {
                        'start': seg['start'],
                        'end': seg['end'],
                        'text': seg['text']
                    }
                    for seg in result['segments']
                ]
                
                # Calculate total duration from segments
                if result['segments']:
                    transcription_result['duration'] = result['segments'][-1]['end']
            
            print("✅ Local transcription complete")
            return transcription_result
            
        except Exception as e:
            print(f"❌ Local transcription failed: {e}")
            raise
    
    def transcribe_video_audio(self, video_path: Path, 
                              extract_audio: bool = True,
                              **kwargs) -> Dict[str, Any]:
        """Transcribe audio from video file."""
        try:
            if extract_audio:
                # Extract audio from video first
                audio_path = self._extract_audio_from_video(video_path)
                result = self.transcribe_audio_file(audio_path, **kwargs)
                
                # Clean up temporary audio file
                if audio_path.exists():
                    audio_path.unlink()
                    print("🗑️ Cleaned up temporary audio file")
                
                result['source'] = 'video'
                result['video_file'] = str(video_path)
                return result
            else:
                # Try to transcribe video directly (API only)
                if self.use_local:
                    raise ValueError("Local Whisper requires audio extraction from video")
                
                return self.transcribe_audio_file(video_path, **kwargs)
                
        except Exception as e:
            print(f"❌ Video transcription failed: {e}")
            raise
    
    def _extract_audio_from_video(self, video_path: Path) -> Path:
        """Extract audio from video using ffmpeg."""
        import subprocess
        
        audio_path = video_path.parent / f"{video_path.stem}_temp_audio.wav"
        
        try:
            print(f"🎵 Extracting audio from video...")
            
            cmd = [
                'ffmpeg', '-i', str(video_path), 
                '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                '-y', str(audio_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"ffmpeg failed: {result.stderr}")
            
            print(f"✅ Audio extracted to: {audio_path.name}")
            return audio_path
            
        except Exception as e:
            print(f"❌ Audio extraction failed: {e}")
            raise


def check_whisper_requirements(check_api: bool = True, check_local: bool = True) -> Dict[str, tuple[bool, str]]:
    """Check if Whisper requirements are met."""
    results = {}
    
    if check_api:
        if not OPENAI_WHISPER_API_AVAILABLE:
            results['api'] = (False, "openai package not installed")
        else:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                results['api'] = (False, "OPENAI_API_KEY environment variable not set")
            else:
                results['api'] = (True, "OpenAI Whisper API ready")
    
    if check_local:
        if not WHISPER_LOCAL_AVAILABLE:
            results['local'] = (False, "whisper package not installed")
        else:
            results['local'] = (True, "Local Whisper ready")
    
    return results


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


def analyze_image_file(image_path: Path, analysis_type: str = "description", 
                      questions: Optional[List[str]] = None, 
                      detailed: bool = False) -> Optional[Dict[str, Any]]:
    """Convenience function to analyze an image file."""
    try:
        analyzer = GeminiVideoAnalyzer()
        
        if analysis_type == "description":
            return analyzer.describe_image(image_path, detailed)
        elif analysis_type == "classification":
            return analyzer.classify_image(image_path)
        elif analysis_type == "objects":
            return analyzer.detect_objects(image_path, detailed)
        elif analysis_type == "qa":
            if not questions:
                questions = ["What is the main subject of this image?", 
                           "What can you tell me about this image?"]
            return analyzer.answer_image_questions(image_path, questions)
        elif analysis_type == "text":
            return analyzer.extract_text_from_image(image_path)
        elif analysis_type == "composition":
            return analyzer.analyze_image_composition(image_path)
        else:
            raise ValueError(f"Unknown image analysis type: {analysis_type}")
            
    except Exception as e:
        print(f"❌ Image analysis failed: {e}")
        return None


def transcribe_with_whisper(file_path: Path, 
                           use_local: bool = False,
                           model_size: str = "turbo",
                           language: Optional[str] = None,
                           include_timestamps: bool = True) -> Optional[Dict[str, Any]]:
    """Convenience function to transcribe audio or video using Whisper."""
    try:
        transcriber = WhisperTranscriber(use_local=use_local)
        
        # Check if it's a video file
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}
        if file_path.suffix.lower() in video_extensions:
            result = transcriber.transcribe_video_audio(
                file_path,
                model_size=model_size,
                language=language,
                include_timestamps=include_timestamps
            )
        else:
            result = transcriber.transcribe_audio_file(
                file_path,
                model_size=model_size,
                language=language,
                include_timestamps=include_timestamps
            )
        
        return result
        
    except Exception as e:
        print(f"❌ Whisper transcription failed: {e}")
        return None


def batch_transcribe_whisper(file_paths: List[Path],
                            use_local: bool = False,
                            model_size: str = "turbo",
                            language: Optional[str] = None,
                            save_results: bool = True) -> List[Dict[str, Any]]:
    """Batch transcribe multiple files with Whisper."""
    results = []
    
    try:
        transcriber = WhisperTranscriber(use_local=use_local)
        
        for i, file_path in enumerate(file_paths, 1):
            print(f"\n📁 Processing file {i}/{len(file_paths)}: {file_path.name}")
            
            try:
                # Check if it's a video file
                video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}
                if file_path.suffix.lower() in video_extensions:
                    result = transcriber.transcribe_video_audio(
                        file_path,
                        model_size=model_size,
                        language=language,
                        include_timestamps=True
                    )
                else:
                    result = transcriber.transcribe_audio_file(
                        file_path,
                        model_size=model_size,
                        language=language,
                        include_timestamps=True
                    )
                
                result['file_path'] = str(file_path)
                results.append(result)
                
                # Save individual result if requested
                if save_results:
                    output_file = file_path.parent / f"{file_path.stem}_whisper_transcription.json"
                    save_analysis_result(result, output_file)
                    
                    # Also save text version
                    txt_file = file_path.parent / f"{file_path.stem}_whisper_transcription.txt"
                    with open(txt_file, 'w', encoding='utf-8') as f:
                        f.write(result['text'])
                
                print(f"✅ Successfully transcribed: {file_path.name}")
                
            except Exception as e:
                print(f"❌ Failed to transcribe {file_path.name}: {e}")
                results.append({
                    'file_path': str(file_path),
                    'error': str(e),
                    'text': None
                })
        
        return results
        
    except Exception as e:
        print(f"❌ Batch transcription failed: {e}")
        return results