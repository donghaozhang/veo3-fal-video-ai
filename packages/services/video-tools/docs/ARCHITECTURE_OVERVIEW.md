# Enhanced Class-Based Architecture Overview

This document provides a comprehensive overview of the new enhanced class-based architecture for video tools.

## Architecture Diagram

```
video_tools/
├── enhanced_cli.py                    # New enhanced CLI entry point
├── test_enhanced_architecture.py      # Architecture validation tests
├── MIGRATION_GUIDE.md                 # Migration documentation
├── ARCHITECTURE_OVERVIEW.md           # This document
│
└── video_utils/                       # Main package
    ├── __init__.py                    # Updated exports (backward compatible)
    │
    ├── # LEGACY MODULES (preserved for compatibility)
    ├── core.py                        # Basic ffmpeg utilities
    ├── file_utils.py                  # File discovery functions
    ├── video_processor.py             # Original video processing
    ├── audio_processor.py             # Original audio processing
    ├── subtitle_generator.py          # Subtitle functionality
    ├── interactive.py                 # User interaction helpers
    ├── commands.py                    # Legacy command imports
    ├── *_commands.py                  # Original command modules
    ├── video_understanding.py         # Original large module (1,363 lines)
    │
    ├── # ENHANCED CLASS-BASED MODULES
    ├── enhanced_video_processor.py    # VideoProcessor class
    ├── enhanced_audio_processor.py    # AudioProcessor class
    ├── base_controller.py             # BaseController abstract class
    ├── media_processing_controller.py # MediaProcessingController class
    ├── command_dispatcher.py          # CommandDispatcher + main CLI
    │
    └── # AI ANALYSIS MODULES (split from video_understanding.py)
        ├── gemini_analyzer.py          # GeminiVideoAnalyzer class
        ├── whisper_transcriber.py      # WhisperTranscriber class
        └── ai_utils.py                 # AI convenience functions
```

## Core Design Principles

### 1. Backward Compatibility
- All existing function-based code continues to work
- No breaking changes to existing APIs
- Legacy modules preserved alongside new classes

### 2. Single Responsibility Principle
- Each class has a focused, well-defined purpose
- Large monolithic files split into logical modules
- Clear separation between different types of operations

### 3. Dependency Injection
- Classes accept configuration parameters
- Dependencies can be mocked for testing
- Runtime behavior can be customized

### 4. Consistent Interfaces
- All controllers inherit from BaseController
- Common patterns for error handling and user interaction
- Unified approach to file operations and validation

## Class Hierarchy

```
BaseController (abstract)
├── MediaProcessingController
└── CommandDispatcher
    └── Uses MediaProcessingController

VideoProcessor (standalone)
AudioProcessor (standalone)

GeminiVideoAnalyzer (standalone)
WhisperTranscriber (standalone)
```

## Module Organization

### Core Processing Classes

#### VideoProcessor (`enhanced_video_processor.py`)
```python
class VideoProcessor:
    def __init__(self, verbose: bool = True)
    
    # Core functionality
    def cut_duration(input_path, output_path, duration, start_time=0)
    def get_video_info(video_path) -> Dict[str, Any]
    
    # Enhanced functionality  
    def resize_video(input_path, output_path, width, height)
    def convert_format(input_path, output_path, target_codec)
    def extract_frames(input_path, output_dir, frame_rate)
    def get_thumbnail(input_path, output_path, timestamp)
    
    # Utility methods
    def validate_video(video_path) -> bool
    def check_dependencies() -> Dict[str, bool]
    def batch_process(input_dir, output_dir, operation, **kwargs)
```

#### AudioProcessor (`enhanced_audio_processor.py`)
```python
class AudioProcessor:
    def __init__(self, verbose: bool = True)
    
    # Core functionality
    def extract_from_video(video_path, output_path)
    def add_to_video(video_path, audio_path, output_path)
    
    # Enhanced functionality
    def mix_files(audio_files, output_path, normalize=True)
    def concatenate_files(audio_files, output_path, crossfade_duration=0)
    def adjust_volume(input_path, output_path, volume_factor)
    def trim_audio(input_path, output_path, start_time, duration)
    def convert_format(input_path, output_path, target_format)
    
    # Utility methods
    def get_audio_info(audio_path) -> Dict[str, Any]
    def validate_audio(audio_path) -> bool
    def check_dependencies() -> Dict[str, bool]
    def batch_process(input_dir, output_dir, operation, **kwargs)
```

### Controller Classes

#### BaseController (`base_controller.py`)
```python
class BaseController(ABC):
    def __init__(self, input_dir, output_dir, verbose=True)
    
    # Directory management
    def setup_directories() -> bool
    def print_header(title, width=50)
    def print_file_info(files, file_type)
    
    # User interaction
    def get_user_choice(prompt, options, default=None)
    def get_user_input(prompt, default=None)
    def get_yes_no(prompt, default=False)
    
    # Progress and results
    def show_progress(current, total, item_name)
    def show_summary(successful, failed, total)
    def save_results(results, filename)
    def save_text_results(content, filename)
    
    # Utility methods
    def check_skip_existing(output_path) -> bool
    def get_safe_filename(base_name, suffix, extension)
    def validate_dependencies() -> Dict[str, bool]
    
    @abstractmethod
    def run() -> bool
```

#### MediaProcessingController (`media_processing_controller.py`)
```python
class MediaProcessingController(BaseController):
    def __init__(self, input_dir, output_dir, verbose=True)
    
    # Implements BaseController.run() with media processing menu
    def run() -> bool
    
    # Video operations
    def cmd_cut_videos() -> bool
    def cmd_resize_videos() -> bool
    def cmd_convert_videos() -> bool
    def cmd_extract_thumbnails() -> bool
    
    # Audio operations
    def cmd_add_audio() -> bool
    def cmd_replace_audio() -> bool
    def cmd_extract_audio() -> bool
    def cmd_mix_audio() -> bool
    def cmd_concat_audio() -> bool
    
    # Batch operations
    def cmd_batch_process() -> bool
```

#### CommandDispatcher (`command_dispatcher.py`)
```python
class CommandDispatcher(BaseController):
    def __init__(self, input_dir, output_dir, verbose=True)
    
    # Main entry point
    def run() -> bool
    
    # Category handlers
    def _handle_media_processing() -> bool
    def _handle_ai_analysis() -> bool  
    def _handle_transcription() -> bool
    def _handle_batch_operations() -> bool
    def _handle_system_status() -> bool
    def _handle_settings() -> bool
    
    # AI analysis submenu
    def _analyze_videos() -> bool
    def _analyze_audio() -> bool
    def _analyze_images() -> bool
    def _comprehensive_analysis() -> bool
    
    # Transcription submenu
    def _transcribe_individual() -> bool
    def _transcribe_batch() -> bool
    
    # CLI entry point
    def main()  # Command-line argument parsing and execution
```

### AI Analysis Classes

#### GeminiVideoAnalyzer (`gemini_analyzer.py`)
```python
class GeminiVideoAnalyzer:
    def __init__(self, api_key: Optional[str] = None)
    
    # Upload methods
    def upload_video(video_path) -> str
    def upload_audio(audio_path) -> str
    def upload_image(image_path) -> str
    
    # Video analysis
    def describe_video(video_path, detailed=False)
    def transcribe_video(video_path, include_timestamps=True)
    def answer_questions(video_path, questions)
    def analyze_scenes(video_path)
    def extract_key_info(video_path)
    
    # Audio analysis
    def describe_audio(audio_path, detailed=False)
    def transcribe_audio(audio_path, include_timestamps=True)
    def analyze_audio_content(audio_path)
    def detect_audio_events(audio_path)
    def answer_audio_questions(audio_path, questions)
    
    # Image analysis
    def describe_image(image_path, detailed=False)
    def classify_image(image_path)
    def detect_objects(image_path, detailed=False)
    def extract_text_from_image(image_path)
    def analyze_image_composition(image_path)
    def answer_image_questions(image_path, questions)
```

#### WhisperTranscriber (`whisper_transcriber.py`)
```python
class WhisperTranscriber:
    def __init__(self, api_key: Optional[str] = None, use_local: bool = False)
    
    # Core transcription
    def transcribe_audio_file(audio_path, language=None, model_size="turbo")
    def transcribe_video_audio(video_path, extract_audio=True, **kwargs)
    
    # Batch processing
    def batch_transcribe(file_paths, save_results=True, **kwargs)
    
    # Private methods
    def _load_local_model(model_size="turbo")
    def _transcribe_api(audio_path, language, response_format)
    def _transcribe_local(audio_path, model_size, include_timestamps)
    def _extract_audio_from_video(video_path) -> Path
```

### Utility Modules

#### AI Utils (`ai_utils.py`)
```python
# Convenience functions
def analyze_video_file(video_path, analysis_type, questions=None, detailed=False)
def analyze_audio_file(audio_path, analysis_type, questions=None, detailed=False)
def analyze_image_file(image_path, analysis_type, questions=None, detailed=False)
def transcribe_with_whisper(file_path, use_local=False, model_size="turbo")
def batch_transcribe_whisper(file_paths, use_local=False, **kwargs)

# Comprehensive analysis
def analyze_media_comprehensively(file_path, output_dir=None, save_results=True)

# System utilities
def save_analysis_result(result, output_path) -> bool
def check_ai_requirements() -> Dict[str, Dict[str, tuple[bool, str]]]
def print_ai_status()
```

## Data Flow

### 1. CLI Entry Point
```
enhanced_cli.py
    └── CommandDispatcher.main()
        └── CommandDispatcher.run()
            └── Shows main menu
                ├── Media Processing → MediaProcessingController
                ├── AI Analysis → AI analysis submenu
                ├── Transcription → Transcription submenu
                └── Other options
```

### 2. Media Processing Flow
```
MediaProcessingController.run()
    └── Shows media processing menu
        ├── Video operations → VideoProcessor methods
        ├── Audio operations → AudioProcessor methods
        └── Batch operations → Processor.batch_process()
```

### 3. AI Analysis Flow
```
AI Analysis Menu
    ├── Video Analysis → GeminiVideoAnalyzer + ai_utils
    ├── Audio Analysis → GeminiVideoAnalyzer + ai_utils  
    ├── Image Analysis → GeminiVideoAnalyzer + ai_utils
    └── Comprehensive → analyze_media_comprehensively()
```

### 4. Transcription Flow
```
Transcription Menu
    ├── Individual Files → WhisperTranscriber + ai_utils
    ├── Batch Processing → WhisperTranscriber.batch_transcribe()
    └── Model Comparison → (future feature)
```

## Error Handling Strategy

### 1. Graceful Degradation
- Methods return boolean success/failure where appropriate
- Detailed error information available through verbose mode
- Fallback options when primary methods fail

### 2. Dependency Validation
- All processors check their dependencies on startup
- Clear error messages when dependencies are missing
- Graceful handling of optional dependencies

### 3. User-Friendly Errors
- CLI shows helpful error messages and suggestions
- Setup instructions provided for missing components
- Progress indicators for long-running operations

## Testing Strategy

### 1. Unit Tests
- Each class can be tested independently
- Dependencies can be mocked for isolated testing
- Clear separation of concerns enables focused tests

### 2. Integration Tests
- `test_enhanced_architecture.py` validates the overall system
- Tests both import/export and basic functionality
- Ensures backward compatibility is maintained

### 3. Manual Testing
- Enhanced CLI provides interactive testing capabilities
- System status checks validate environment setup
- Comprehensive analysis modes test end-to-end workflows

## Performance Considerations

### 1. Lazy Loading
- AI models and heavy dependencies loaded only when needed
- Optional features don't impact startup time
- Classes instantiated only when required

### 2. Batch Processing
- Efficient handling of multiple files
- Progress tracking for long-running operations
- Memory-conscious processing of large media files

### 3. Resource Management
- Automatic cleanup of temporary files
- Proper handling of uploaded files in AI services
- Memory-efficient processing for large batches

## Extension Points

### 1. Adding New Processors
```python
class CustomProcessor:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
    
    def check_dependencies(self) -> Dict[str, bool]:
        # Validate required tools/libraries
        pass
    
    def process_file(self, input_path, output_path, **kwargs) -> bool:
        # Implement custom processing
        pass
    
    def batch_process(self, input_dir, output_dir, **kwargs):
        # Optional batch processing capability
        pass
```

### 2. Adding New Controllers
```python
class CustomController(BaseController):
    def __init__(self, input_dir, output_dir, verbose=True):
        super().__init__(input_dir, output_dir, verbose)
        self.custom_processor = CustomProcessor(verbose)
    
    def run(self) -> bool:
        # Implement controller logic
        return self._show_custom_menu()
    
    def _show_custom_menu(self) -> bool:
        # Custom menu implementation
        pass
```

### 3. Adding New AI Analyzers
```python
class CustomAIAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        # Initialize custom AI service
        pass
    
    def analyze_media(self, media_path: Path) -> Dict[str, Any]:
        # Implement custom analysis
        pass

# Add to ai_utils.py for convenience functions
def analyze_with_custom_ai(file_path: Path, **kwargs) -> Optional[Dict[str, Any]]:
    try:
        analyzer = CustomAIAnalyzer()
        return analyzer.analyze_media(file_path)
    except Exception as e:
        print(f"❌ Custom AI analysis failed: {e}")
        return None
```

## Future Enhancements

### 1. Plugin System
- Dynamic loading of custom processors and analyzers
- Configuration-based feature enabling/disabling
- Third-party extension support

### 2. Web Interface
- REST API for programmatic access
- Web-based UI for file upload and processing
- Real-time progress monitoring

### 3. Cloud Integration
- Cloud storage integration (AWS S3, Google Cloud Storage)
- Distributed processing capabilities
- API rate limiting and queue management

### 4. Advanced Features
- Real-time processing pipelines
- Custom workflow definition and execution
- Integration with video editing software

## Summary

The enhanced class-based architecture provides:

✅ **Maintainable Code**: Smaller, focused modules instead of monolithic files  
✅ **Extensible Design**: Easy to add new processors and analyzers  
✅ **Better Organization**: Logical grouping of related functionality  
✅ **Improved Testing**: Classes enable better unit and integration testing  
✅ **Backward Compatibility**: All existing code continues to work  
✅ **Enhanced Capabilities**: More features and configuration options  
✅ **Unified Interface**: Single CLI for all operations  
✅ **Professional Structure**: Industry-standard patterns and practices  

This architecture provides a solid foundation for current needs while enabling future growth and enhancements.