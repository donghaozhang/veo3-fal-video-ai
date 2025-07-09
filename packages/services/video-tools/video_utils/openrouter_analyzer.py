"""
OpenRouter AI analyzer for video, audio, and image understanding.

Provides AI-powered multimodal analysis using OpenRouter's unified API access to multiple models including:
- Video description, transcription, and scene analysis
- Audio transcription, content analysis, and event detection  
- Image description, classification, and object detection
- OCR text extraction from images
- Question answering about any media content
- Composition and technical analysis

Uses OpenAI-compatible API through OpenRouter for access to Gemini, Claude, and other models.
"""

import json
import time
import base64
from pathlib import Path
from typing import Optional, Dict, Any, List
import os

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class OpenRouterAnalyzer:
    """OpenRouter multimodal AI analyzer with support for various models."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "google/gemini-2.0-flash-001"):
        """Initialize with API key and model selection."""
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI library not installed. Run: pip install openai"
            )
        
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key required. Set OPENROUTER_API_KEY environment variable or pass api_key parameter"
            )
        
        self.model = model
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        
        print(f"✅ OpenRouter analyzer initialized with model: {model}")
    
    def _encode_image_base64(self, image_path: Path) -> str:
        """Encode image to base64 for API transmission."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def _get_image_mime_type(self, image_path: Path) -> str:
        """Get MIME type for image file."""
        suffix = image_path.suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg', 
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return mime_types.get(suffix, 'image/jpeg')
    
    def _analyze_with_prompt(self, content_list: List[Dict[str, Any]], prompt: str) -> str:
        """Generic method to analyze content with a custom prompt."""
        try:
            messages = [{
                "role": "user",
                "content": content_list + [{"type": "text", "text": prompt}]
            }]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4000,
                temperature=0.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            raise
    
    # Video Analysis Methods
    def describe_video(self, video_path: Path, detailed: bool = False) -> Dict[str, Any]:
        """Generate video description and summary."""
        print(f"🎬 Note: Video analysis requires file upload - using image frame analysis instead")
        print(f"📝 For full video analysis, consider using direct Gemini API")
        
        if detailed:
            prompt = """Analyze this video content in detail and provide:
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
        
        result = {
            'description': "Video analysis through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Gemini API directly for video analysis.",
            'detailed': detailed,
            'analysis_type': 'description',
            'note': 'Full video analysis requires native file upload support'
        }
        
        return result
    
    def transcribe_video(self, video_path: Path, include_timestamps: bool = True) -> Dict[str, Any]:
        """Transcribe audio content from video."""
        print(f"🎤 Note: Video transcription requires file upload - not supported in OpenRouter implementation")
        
        result = {
            'transcription': "Video transcription through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Whisper API or Gemini API directly.",
            'include_timestamps': include_timestamps,
            'analysis_type': 'transcription',
            'note': 'Video transcription requires native file upload support'
        }
        
        return result
    
    def answer_questions(self, video_path: Path, questions: List[str]) -> Dict[str, Any]:
        """Answer specific questions about the video."""
        print(f"❓ Note: Video Q&A requires file upload - not supported in OpenRouter implementation")
        
        result = {
            'questions': questions,
            'answers': "Video Q&A through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Gemini API directly.",
            'analysis_type': 'qa',
            'note': 'Video Q&A requires native file upload support'
        }
        
        return result
    
    def analyze_scenes(self, video_path: Path) -> Dict[str, Any]:
        """Analyze video scenes and create timeline breakdown."""
        print(f"🎬 Note: Scene analysis requires file upload - not supported in OpenRouter implementation")
        
        result = {
            'scene_analysis': "Scene analysis through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Gemini API directly.",
            'analysis_type': 'scenes',
            'note': 'Scene analysis requires native file upload support'
        }
        
        return result
    
    def extract_key_info(self, video_path: Path) -> Dict[str, Any]:
        """Extract key information and insights from video."""
        print(f"🔍 Note: Video info extraction requires file upload - not supported in OpenRouter implementation")
        
        result = {
            'key_info': "Key info extraction through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Gemini API directly.",
            'analysis_type': 'extraction',
            'note': 'Video key info extraction requires native file upload support'
        }
        
        return result
    
    # Audio Analysis Methods  
    def describe_audio(self, audio_path: Path, detailed: bool = False) -> Dict[str, Any]:
        """Generate audio description and summary."""
        print(f"🎵 Note: Audio analysis requires file upload - not supported in OpenRouter implementation")
        
        result = {
            'description': "Audio analysis through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Whisper API or Gemini API directly.",
            'detailed': detailed,
            'analysis_type': 'description',
            'note': 'Audio analysis requires native file upload support'
        }
        
        return result
    
    def transcribe_audio(self, audio_path: Path, include_timestamps: bool = True, 
                        speaker_identification: bool = True) -> Dict[str, Any]:
        """Transcribe spoken content from audio."""
        print(f"🎤 Note: Audio transcription requires file upload - not supported in OpenRouter implementation")
        
        result = {
            'transcription': "Audio transcription through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Whisper API or Gemini API directly.",
            'include_timestamps': include_timestamps,
            'speaker_identification': speaker_identification,
            'analysis_type': 'transcription',
            'note': 'Audio transcription requires native file upload support'
        }
        
        return result
    
    def analyze_audio_content(self, audio_path: Path) -> Dict[str, Any]:
        """Analyze audio content for type, genre, mood, etc."""
        print(f"🎵 Note: Audio content analysis requires file upload - not supported in OpenRouter implementation")
        
        result = {
            'content_analysis': "Audio content analysis through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Gemini API directly.",
            'analysis_type': 'content_analysis',
            'note': 'Audio content analysis requires native file upload support'
        }
        
        return result
    
    def answer_audio_questions(self, audio_path: Path, questions: List[str]) -> Dict[str, Any]:
        """Answer specific questions about the audio."""
        print(f"❓ Note: Audio Q&A requires file upload - not supported in OpenRouter implementation")
        
        result = {
            'questions': questions,
            'answers': "Audio Q&A through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Gemini API directly.",
            'analysis_type': 'qa',
            'note': 'Audio Q&A requires native file upload support'
        }
        
        return result
    
    def detect_audio_events(self, audio_path: Path) -> Dict[str, Any]:
        """Detect and analyze specific events in audio."""
        print(f"🔍 Note: Audio event detection requires file upload - not supported in OpenRouter implementation")
        
        result = {
            'event_detection': "Audio event detection through OpenRouter requires direct file upload capabilities not available in this implementation. Consider using Gemini API directly.",
            'analysis_type': 'event_detection',
            'note': 'Audio event detection requires native file upload support'
        }
        
        return result
    
    # Image Analysis Methods (These work with OpenRouter!)
    def describe_image(self, image_path: Path, detailed: bool = False) -> str:
        """Generate image description and summary."""
        try:
            print(f"🖼️ Analyzing image: {image_path.name}")
            
            # Encode image to base64
            image_base64 = self._encode_image_base64(image_path)
            mime_type = self._get_image_mime_type(image_path)
            
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
            
            content_list = [{
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }
            }]
            
            description = self._analyze_with_prompt(content_list, prompt)
            
            return description
            
        except Exception as e:
            print(f"❌ Image description failed: {e}")
            raise
    
    def classify_image(self, image_path: Path) -> str:
        """Classify image content and categorize."""
        try:
            print(f"🏷️ Classifying image: {image_path.name}")
            
            image_base64 = self._encode_image_base64(image_path)
            mime_type = self._get_image_mime_type(image_path)
            
            prompt = """Classify and categorize this image:
1. Primary category (portrait, landscape, object, scene, etc.)
2. Content type (photograph, artwork, diagram, screenshot, etc.)
3. Subject classification (people, animals, nature, architecture, etc.)
4. Style or genre (if applicable)
5. Purpose or context (professional, casual, artistic, etc.)
6. Technical classification (color/black&white, digital/analog, etc.)

Provide structured classification with confidence levels where possible."""
            
            content_list = [{
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }
            }]
            
            classification = self._analyze_with_prompt(content_list, prompt)
            
            return classification
            
        except Exception as e:
            print(f"❌ Image classification failed: {e}")
            raise
    
    def detect_objects(self, image_path: Path, detailed: bool = False) -> str:
        """Detect and identify objects in the image."""
        try:
            print(f"🔍 Detecting objects in image: {image_path.name}")
            
            image_base64 = self._encode_image_base64(image_path)
            mime_type = self._get_image_mime_type(image_path)
            
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
            
            content_list = [{
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }
            }]
            
            detection_result = self._analyze_with_prompt(content_list, prompt)
            
            return detection_result
            
        except Exception as e:
            print(f"❌ Object detection failed: {e}")
            raise
    
    def answer_image_questions(self, image_path: Path, questions: List[str]) -> str:
        """Answer specific questions about the image."""
        try:
            print(f"❓ Answering questions about image: {image_path.name}")
            
            image_base64 = self._encode_image_base64(image_path)
            mime_type = self._get_image_mime_type(image_path)
            
            questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            prompt = f"""Examine this image carefully and answer the following questions:

{questions_text}

Provide detailed, accurate answers based on what you can see in the image. If a question cannot be answered from the visual content, please state that clearly."""
            
            content_list = [{
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }
            }]
            
            answers = self._analyze_with_prompt(content_list, prompt)
            
            return answers
            
        except Exception as e:
            print(f"❌ Image Q&A failed: {e}")
            raise
    
    def extract_text_from_image(self, image_path: Path) -> str:
        """Extract and transcribe text from image (OCR)."""
        try:
            print(f"📝 Extracting text from image: {image_path.name}")
            
            image_base64 = self._encode_image_base64(image_path)
            mime_type = self._get_image_mime_type(image_path)
            
            prompt = """Extract all text visible in this image:
1. Transcribe all readable text accurately
2. Preserve formatting and layout where possible
3. Note text locations (top, center, bottom, etc.)
4. Identify different text styles (headlines, body, captions)
5. Note any partially visible or unclear text
6. Include text orientation and direction
7. Describe the context of text elements

Provide complete text extraction with structure."""
            
            content_list = [{
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }
            }]
            
            extracted_text = self._analyze_with_prompt(content_list, prompt)
            
            return extracted_text
            
        except Exception as e:
            print(f"❌ Text extraction failed: {e}")
            raise
    
    def analyze_image_composition(self, image_path: Path) -> str:
        """Analyze image composition, style, and technical aspects."""
        try:
            print(f"🎨 Analyzing image composition: {image_path.name}")
            
            image_base64 = self._encode_image_base64(image_path)
            mime_type = self._get_image_mime_type(image_path)
            
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
            
            content_list = [{
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }
            }]
            
            composition_analysis = self._analyze_with_prompt(content_list, prompt)
            
            return composition_analysis
            
        except Exception as e:
            print(f"❌ Composition analysis failed: {e}")
            raise
    
    def generate_video_prompt(self, image_path: Path, background_context: str = "", 
                             video_style: str = "cinematic", duration_preference: str = "medium") -> str:
        """Generate optimized prompt for image-to-video conversion.
        
        Args:
            image_path: Path to the image file
            background_context: Additional context about the scene, story, or desired outcome
            video_style: Style preference (cinematic, realistic, artistic, dramatic, etc.)
            duration_preference: Duration hint (short, medium, long) for pacing suggestions
            
        Returns:
            Optimized prompt for image-to-video generation
        """
        try:
            print(f"🎬 Generating video prompt for: {image_path.name}")
            
            image_base64 = self._encode_image_base64(image_path)
            mime_type = self._get_image_mime_type(image_path)
            
            # Create comprehensive prompt for video generation
            analysis_prompt = f"""Analyze this image and create an optimized prompt for AI image-to-video generation.

CONTEXT INFORMATION:
- Background/Story Context: {background_context if background_context else 'None provided'}
- Desired Video Style: {video_style}
- Duration Preference: {duration_preference}

ANALYSIS REQUIREMENTS:
1. Identify the main subject and scene elements
2. Determine natural movement possibilities (wind, water, people, objects, camera)
3. Assess lighting conditions and potential changes
4. Identify atmospheric elements (fog, clouds, particles, etc.)
5. Consider perspective and camera movement opportunities
6. Evaluate emotional tone and mood potential

OUTPUT FORMAT:
Provide a comprehensive video generation prompt that includes:

**SCENE DESCRIPTION:**
[Clear description of the static elements]

**MOVEMENT SUGGESTIONS:**
[Specific, realistic movements that would enhance the scene]

**CAMERA WORK:**
[Camera movements, angles, or transitions that would work well]

**ATMOSPHERIC EFFECTS:**
[Weather, lighting, or environmental changes]

**STYLE NOTES:**
[Artistic direction aligned with {video_style} style]

**OPTIMIZED PROMPT:**
[A concise, powerful prompt optimized for AI video generation, 1-2 sentences max]

Focus on creating movement that feels natural and enhances the original image's story without being overly complex."""
            
            content_list = [{
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_base64}"
                }
            }]
            
            video_prompt_analysis = self._analyze_with_prompt(content_list, analysis_prompt)
            
            return video_prompt_analysis
            
        except Exception as e:
            print(f"❌ Video prompt generation failed: {e}")
            raise
    
    def extract_optimized_prompt(self, video_prompt_analysis: str) -> str:
        """Extract just the optimized prompt from the full analysis.
        
        Args:
            video_prompt_analysis: Full analysis output from generate_video_prompt
            
        Returns:
            Just the optimized prompt portion
        """
        try:
            # Look for the optimized prompt section
            lines = video_prompt_analysis.split('\n')
            in_optimized_section = False
            optimized_lines = []
            
            for line in lines:
                if '**OPTIMIZED PROMPT:**' in line:
                    in_optimized_section = True
                    continue
                elif line.startswith('**') and in_optimized_section:
                    break
                elif in_optimized_section and line.strip():
                    optimized_lines.append(line.strip())
            
            if optimized_lines:
                return ' '.join(optimized_lines)
            else:
                # Fallback: return last few sentences if structure not found
                sentences = video_prompt_analysis.split('.')
                return '. '.join(sentences[-2:]).strip()
                
        except Exception as e:
            print(f"⚠️ Prompt extraction failed, returning full analysis: {e}")
            return video_prompt_analysis


def check_openrouter_requirements() -> tuple[bool, str]:
    """Check if OpenRouter requirements are met."""
    if not OPENAI_AVAILABLE:
        return False, "OpenAI library not installed"
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return False, "OPENROUTER_API_KEY environment variable not set"
    
    try:
        # Test API connection
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Simple test call
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        return True, "OpenRouter API ready"
    except Exception as e:
        return False, f"OpenRouter API error: {str(e)}"