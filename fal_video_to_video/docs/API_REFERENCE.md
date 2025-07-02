# API Reference

Complete API reference for FAL Video to Video.

## FALVideoToVideoGenerator

Main class for video audio generation.

### Constructor

```python
FALVideoToVideoGenerator(api_key: Optional[str] = None)
```

**Parameters:**
- `api_key` (str, optional): FAL API key. If not provided, looks for `FAL_KEY` environment variable.

**Raises:**
- `ValueError`: If no API key is found

### Methods

#### add_audio_to_video

```python
add_audio_to_video(
    video_url: str,
    model: str = "thinksound",
    prompt: Optional[str] = None,
    seed: Optional[int] = None,
    output_dir: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]
```

Add AI-generated audio to a video from URL.

**Parameters:**
- `video_url` (str): URL of the input video
- `model` (str): Model to use (default: "thinksound")
- `prompt` (str, optional): Text prompt to guide audio generation
- `seed` (int, optional): Random seed for reproducibility
- `output_dir` (str, optional): Custom output directory
- `**kwargs`: Additional model-specific parameters

**Returns:**
- Dictionary containing:
  - `success` (bool): Whether generation was successful
  - `model` (str): Model used
  - `local_path` (str): Path to downloaded video with audio
  - `response` (dict): Full API response
  - `processing_time` (float): Time taken for generation
  - `prompt` (str): Prompt used (if provided)
  - `seed` (int): Seed used (if provided)

**Raises:**
- `ValueError`: If video_url is invalid or model is not supported

#### add_audio_to_local_video

```python
add_audio_to_local_video(
    video_path: str,
    model: str = "thinksound",
    prompt: Optional[str] = None,
    seed: Optional[int] = None,
    output_dir: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]
```

Add AI-generated audio to a local video file.

**Parameters:**
- `video_path` (str): Path to local video file
- `model` (str): Model to use (default: "thinksound")
- `prompt` (str, optional): Text prompt to guide audio generation
- `seed` (int, optional): Random seed for reproducibility
- `output_dir` (str, optional): Custom output directory
- `**kwargs`: Additional model-specific parameters

**Returns:**
- Same as `add_audio_to_video()`

**Raises:**
- `ValueError`: If video file doesn't exist, is too large, or has unsupported format

#### get_model_info

```python
get_model_info(model: Optional[str] = None) -> Dict[str, Any]
```

Get information about available models.

**Parameters:**
- `model` (str, optional): Specific model to get info for. If None, returns info for all models.

**Returns:**
- Dictionary containing model information including features, pricing, and capabilities

#### list_models

```python
list_models() -> List[str]
```

List all available models.

**Returns:**
- List of available model names

## Models

### ThinkSoundModel

Implementation of the ThinkSound model for AI audio generation.

#### Methods

##### validate_parameters

```python
validate_parameters(**kwargs) -> Dict[str, Any]
```

Validate ThinkSound-specific parameters.

**Parameters:**
- `prompt` (str, optional): Text prompt for audio generation (max 1000 characters)
- `seed` (int, optional): Random seed (must be non-negative)

**Returns:**
- Dictionary of validated parameters

**Raises:**
- `ValueError`: If parameters are invalid

##### prepare_arguments

```python
prepare_arguments(video_url: str, **kwargs) -> Dict[str, Any]
```

Prepare API arguments for ThinkSound.

**Parameters:**
- `video_url` (str): URL of input video
- `**kwargs`: Validated parameters

**Returns:**
- Dictionary of API arguments

##### get_model_info

```python
get_model_info() -> Dict[str, Any]
```

Get ThinkSound model information.

**Returns:**
- Dictionary with model details

## Utilities

### Validators

#### validate_model

```python
validate_model(model: str) -> str
```

Validate model type.

**Parameters:**
- `model` (str): Model type string

**Returns:**
- Validated model type

**Raises:**
- `ValueError`: If model is not supported

#### validate_video_url

```python
validate_video_url(video_url: str) -> str
```

Validate video URL.

**Parameters:**
- `video_url` (str): URL of the video

**Returns:**
- Validated video URL

**Raises:**
- `ValueError`: If URL is invalid

#### validate_video_path

```python
validate_video_path(video_path: str) -> str
```

Validate local video file path.

**Parameters:**
- `video_path` (str): Path to video file

**Returns:**
- Validated video path

**Raises:**
- `ValueError`: If path is invalid, file doesn't exist, or file is too large

#### validate_prompt

```python
validate_prompt(prompt: Optional[str]) -> Optional[str]
```

Validate text prompt.

**Parameters:**
- `prompt` (str, optional): Text prompt for audio generation

**Returns:**
- Validated prompt or None

**Raises:**
- `ValueError`: If prompt is too long (>1000 characters)

#### validate_seed

```python
validate_seed(seed: Optional[int]) -> Optional[int]
```

Validate random seed.

**Parameters:**
- `seed` (int, optional): Random seed value

**Returns:**
- Validated seed or None

**Raises:**
- `ValueError`: If seed is not an integer or is negative

### File Utils

#### ensure_output_directory

```python
ensure_output_directory(output_dir: Optional[str] = None) -> Path
```

Ensure output directory exists.

**Parameters:**
- `output_dir` (str, optional): Custom output directory path

**Returns:**
- Path object for output directory

#### download_video

```python
download_video(
    video_url: str, 
    output_dir: Path, 
    filename: Optional[str] = None
) -> str
```

Download video from URL.

**Parameters:**
- `video_url` (str): URL of the video
- `output_dir` (Path): Directory to save video
- `filename` (str, optional): Custom filename

**Returns:**
- Path to downloaded video

#### upload_video

```python
upload_video(video_path: str) -> str
```

Upload local video to FAL storage.

**Parameters:**
- `video_path` (str): Path to local video file

**Returns:**
- URL of uploaded video

#### get_video_info

```python
get_video_info(video_path: str) -> Dict[str, Any]
```

Get video information using moviepy.

**Parameters:**
- `video_path` (str): Path to video file

**Returns:**
- Dictionary with video information (duration, fps, size, etc.)

## Constants

### Models

```python
SUPPORTED_MODELS = ["thinksound"]
MODEL_ENDPOINTS = {
    "thinksound": "fal-ai/thinksound"
}
MODEL_DISPLAY_NAMES = {
    "thinksound": "ThinkSound"
}
```

### Limits

```python
MAX_VIDEO_SIZE_MB = 100
MAX_VIDEO_DURATION_SECONDS = 300
```

### Defaults

```python
DEFAULT_VALUES = {
    "thinksound": {
        "seed": None,
        "prompt": None
    }
}
```

## Error Handling

All methods return dictionaries with `success` boolean. On failure:

```python
{
    "success": False,
    "error": "Error description",
    "model": "Model name",
    "video_url": "Input URL"
}
```

Common error types:
- **Authentication**: Invalid API key
- **Validation**: Invalid parameters or file formats
- **Network**: Connection or upload/download issues
- **API**: Service errors or rate limits
- **File**: Missing files or permission issues

## CLI Interface

The package provides a command-line interface via `python -m fal_video_to_video`.

### Commands

#### list-models

```bash
python -m fal_video_to_video list-models
```

List all available models.

#### add-audio

```bash
python -m fal_video_to_video add-audio [options]
```

Add audio to a single video.

**Options:**
- `-i, --video-path`: Path to local video file
- `-u, --video-url`: URL of video (mutually exclusive with `-i`)
- `-m, --model`: Model to use (default: thinksound)
- `-p, --prompt`: Text prompt to guide audio generation
- `--seed`: Random seed for reproducibility
- `-o, --output-dir`: Output directory
- `--save-json`: Save full result as JSON
- `--debug`: Enable debug output

#### batch

```bash
python -m fal_video_to_video batch [options]
```

Batch process multiple videos.

**Options:**
- `-f, --batch-file`: JSON file with batch data (required)
- `-m, --model`: Default model (can be overridden per video)
- `--save-json`: Save results as JSON
- `--debug`: Enable debug output

### Batch File Format

```json
[
  {
    "video_url": "https://example.com/video1.mp4",
    "prompt": "add dramatic music",
    "model": "thinksound",
    "seed": 42
  },
  {
    "video_path": "input/video2.mp4",
    "prompt": "add nature sounds"
  }
]
```