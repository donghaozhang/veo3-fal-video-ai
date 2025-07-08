"""
OpenAI Whisper transcriber for audio and video files.

Provides speech-to-text transcription using both OpenAI's API and local Whisper models.
Supports multiple audio formats and languages with timestamp extraction.
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List
import os

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


class WhisperTranscriber:
    """OpenAI Whisper transcriber for audio and video files."""
    
    def __init__(self, api_key: Optional[str] = None, use_local: bool = False):
        """Initialize the transcriber.
        
        Args:
            api_key: OpenAI API key (if using API)
            use_local: Whether to use local Whisper model by default
        """
        self.use_local = use_local
        self.local_model = None
        
        # Setup API client if available and requested
        if not use_local and OPENAI_WHISPER_API_AVAILABLE:
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            if self.api_key:
                self.client = OpenAI(api_key=self.api_key)
            else:
                self.client = None
        else:
            self.client = None
            
        # Setup local model if requested
        if use_local and WHISPER_LOCAL_AVAILABLE:
            self._load_local_model()
    
    def _load_local_model(self, model_size: str = "turbo"):
        """Load local Whisper model."""
        if not WHISPER_LOCAL_AVAILABLE:
            raise ImportError("whisper package not installed. Run: pip install openai-whisper")
        
        try:
            print(f"🤖 Loading Whisper model: {model_size}")
            self.local_model = whisper.load_model(model_size)
            print("✅ Local Whisper model loaded")
        except Exception as e:
            print(f"❌ Failed to load local model: {e}")
            self.local_model = None
    
    def transcribe_audio_file(self, audio_path: Path, language: Optional[str] = None,
                             model_size: str = "turbo", include_timestamps: bool = True,
                             response_format: str = "json") -> Dict[str, Any]:
        """Transcribe audio file using Whisper.
        
        Args:
            audio_path: Path to audio file
            language: Language code (e.g., 'en', 'es', 'fr')
            model_size: Model size for local transcription
            include_timestamps: Whether to include timestamps
            response_format: Response format ('json', 'text', 'srt', 'vtt')
            
        Returns:
            Transcription result dictionary
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"🎤 Transcribing: {audio_path.name}")
        
        # Determine which method to use
        if self.use_local or not self.client:
            return self._transcribe_local(audio_path, model_size, include_timestamps)
        else:
            return self._transcribe_api(audio_path, language, response_format)
    
    def _transcribe_api(self, audio_path: Path, language: Optional[str],
                       response_format: str) -> Dict[str, Any]:
        """Transcribe using OpenAI API."""
        if not self.client:
            raise ValueError("OpenAI API client not available")
        
        try:
            # Check file size (25MB limit for API)
            file_size = audio_path.stat().st_size / (1024 * 1024)  # MB
            if file_size > 25:
                raise ValueError(f"File too large for API: {file_size:.1f}MB (max 25MB)")
            
            print(f"📤 Uploading to OpenAI API ({file_size:.1f}MB)")
            
            with open(audio_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format=response_format
                )
            
            if response_format == "json":
                result = {
                    'text': transcript.text,
                    'language': language,
                    'method': 'api',
                    'model': 'whisper-1',
                    'file_size_mb': file_size
                }
            else:
                result = {
                    'text': str(transcript),
                    'language': language,
                    'method': 'api',
                    'model': 'whisper-1',
                    'format': response_format,
                    'file_size_mb': file_size
                }
            
            print("✅ API transcription complete")
            return result
            
        except Exception as e:
            print(f"❌ API transcription failed: {e}")
            raise
    
    def _transcribe_local(self, audio_path: Path, model_size: str,
                         include_timestamps: bool) -> Dict[str, Any]:
        """Transcribe using local Whisper model."""
        if not self.local_model or self.local_model.dims.n_vocab != whisper.load_model(model_size).dims.n_vocab:
            self._load_local_model(model_size)
        
        if not self.local_model:
            raise RuntimeError("Local Whisper model not available")
        
        try:
            print(f"🤖 Processing with local model: {model_size}")
            
            # Transcribe with options
            options = {
                "verbose": False,
                "task": "transcribe"
            }
            
            if include_timestamps:
                options["word_timestamps"] = True
            
            result_whisper = self.local_model.transcribe(str(audio_path), **options)
            
            # Format result
            result = {
                'text': result_whisper['text'],
                'language': result_whisper.get('language', 'unknown'),
                'method': 'local',
                'model': model_size,
                'segments': []
            }
            
            # Include segments with timestamps if available
            if 'segments' in result_whisper and include_timestamps:
                for segment in result_whisper['segments']:
                    segment_info = {
                        'start': segment.get('start', 0),
                        'end': segment.get('end', 0),
                        'text': segment.get('text', '').strip()
                    }
                    
                    # Include word-level timestamps if available
                    if 'words' in segment:
                        segment_info['words'] = [
                            {
                                'word': word.get('word', ''),
                                'start': word.get('start', 0),
                                'end': word.get('end', 0),
                                'probability': word.get('probability', 0)
                            }
                            for word in segment['words']
                        ]
                    
                    result['segments'].append(segment_info)
            
            print("✅ Local transcription complete")
            return result
            
        except Exception as e:
            print(f"❌ Local transcription failed: {e}")
            raise
    
    def transcribe_video_audio(self, video_path: Path, extract_audio: bool = True,
                              **kwargs) -> Dict[str, Any]:
        """Transcribe audio from video file.
        
        Args:
            video_path: Path to video file
            extract_audio: Whether to extract audio first
            **kwargs: Arguments passed to transcribe_audio_file
            
        Returns:
            Transcription result dictionary
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if extract_audio:
            # Extract audio to temporary file
            audio_path = self._extract_audio_from_video(video_path)
            try:
                result = self.transcribe_audio_file(audio_path, **kwargs)
                result['source_video'] = str(video_path)
                result['extracted_audio'] = True
                return result
            finally:
                # Clean up temporary audio file
                if audio_path.exists():
                    audio_path.unlink()
        else:
            # Try to transcribe video directly (may not work with all methods)
            result = self.transcribe_audio_file(video_path, **kwargs)
            result['source_video'] = str(video_path)
            result['extracted_audio'] = False
            return result
    
    def _extract_audio_from_video(self, video_path: Path) -> Path:
        """Extract audio from video to temporary file."""
        try:
            # Create temporary audio file
            temp_dir = Path(tempfile.gettempdir())
            temp_audio = temp_dir / f"{video_path.stem}_temp_audio.wav"
            
            print(f"🎵 Extracting audio from: {video_path.name}")
            
            # Use ffmpeg to extract audio
            cmd = [
                'ffmpeg', '-i', str(video_path),
                '-vn',  # No video
                '-acodec', 'pcm_s16le',  # PCM format for compatibility
                '-ar', '16000',  # 16kHz sample rate (good for speech)
                '-ac', '1',  # Mono channel
                str(temp_audio),
                '-y'  # Overwrite if exists
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"ffmpeg failed: {result.stderr}")
            
            if not temp_audio.exists():
                raise RuntimeError("Audio extraction failed - no output file")
            
            print(f"✅ Audio extracted: {temp_audio.name}")
            return temp_audio
            
        except Exception as e:
            print(f"❌ Audio extraction failed: {e}")
            raise
    
    def batch_transcribe(self, file_paths: List[Path], save_results: bool = True,
                        output_dir: Optional[Path] = None, **kwargs) -> List[Dict[str, Any]]:
        """Transcribe multiple files in batch.
        
        Args:
            file_paths: List of audio/video file paths
            save_results: Whether to save results to files
            output_dir: Directory to save results (default: current directory)
            **kwargs: Arguments passed to transcribe methods
            
        Returns:
            List of transcription results
        """
        if output_dir is None:
            output_dir = Path.cwd()
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        print(f"🎤 Starting batch transcription of {len(file_paths)} files")
        
        for i, file_path in enumerate(file_paths, 1):
            print(f"\n📊 Processing file {i}/{len(file_paths)}: {file_path.name}")
            
            try:
                # Determine if it's a video or audio file
                video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
                is_video = file_path.suffix.lower() in video_extensions
                
                if is_video:
                    result = self.transcribe_video_audio(file_path, **kwargs)
                else:
                    result = self.transcribe_audio_file(file_path, **kwargs)
                
                result['source_file'] = str(file_path)
                result['batch_index'] = i
                results.append(result)
                
                # Save individual result if requested
                if save_results:
                    result_file = output_dir / f"{file_path.stem}_transcription.json"
                    with open(result_file, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    print(f"💾 Saved: {result_file.name}")
                
            except Exception as e:
                print(f"❌ Failed to transcribe {file_path.name}: {e}")
                error_result = {
                    'source_file': str(file_path),
                    'batch_index': i,
                    'error': str(e),
                    'success': False
                }
                results.append(error_result)
        
        # Save batch summary
        if save_results:
            summary_file = output_dir / "batch_transcription_summary.json"
            summary = {
                'total_files': len(file_paths),
                'successful': len([r for r in results if 'error' not in r]),
                'failed': len([r for r in results if 'error' in r]),
                'results': results
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            print(f"\n📋 Batch summary saved: {summary_file.name}")
        
        successful = len([r for r in results if 'error' not in r])
        failed = len(results) - successful
        print(f"\n📊 Batch complete: {successful} successful, {failed} failed")
        
        return results


def check_whisper_requirements(check_api: bool = True, check_local: bool = True) -> Dict[str, tuple[bool, str]]:
    """Check Whisper requirements.
    
    Args:
        check_api: Whether to check API requirements
        check_local: Whether to check local requirements
        
    Returns:
        Dictionary with requirement check results
    """
    results = {}
    
    if check_api:
        # Check OpenAI API availability
        if OPENAI_WHISPER_API_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                try:
                    # Test API connection
                    client = OpenAI(api_key=api_key)
                    # Simple test - this won't actually use credits
                    models = client.models.list()
                    results['api'] = (True, "OpenAI API ready")
                except Exception as e:
                    results['api'] = (False, f"OpenAI API error: {str(e)}")
            else:
                results['api'] = (False, "OPENAI_API_KEY environment variable not set")
        else:
            results['api'] = (False, "OpenAI library not installed")
    
    if check_local:
        # Check local Whisper availability
        if WHISPER_LOCAL_AVAILABLE:
            try:
                # Try to load the smallest model to test
                import whisper
                model = whisper.load_model("tiny")
                results['local'] = (True, "Local Whisper ready")
            except Exception as e:
                results['local'] = (False, f"Local Whisper error: {str(e)}")
        else:
            results['local'] = (False, "whisper package not installed")
    
    # Check ffmpeg for video audio extraction
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        results['ffmpeg'] = (True, "ffmpeg available")
    except (subprocess.CalledProcessError, FileNotFoundError):
        results['ffmpeg'] = (False, "ffmpeg not available")
    
    return results