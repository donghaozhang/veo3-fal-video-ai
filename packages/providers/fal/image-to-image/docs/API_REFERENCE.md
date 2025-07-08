# API Reference

Complete API reference for the FAL Image-to-Image package.

## Main Classes

### FALImageToImageGenerator

The main generator class providing unified access to all models.

#### Constructor

```python
FALImageToImageGenerator(api_key: Optional[str] = None)
```

**Parameters:**
- `api_key`: FAL AI API key. If not provided, loads from `FAL_KEY` environment variable.

**Raises:**
- `ValueError`: If no API key is provided or found in environment.

#### Core Methods

##### modify_image()

```python
modify_image(
    prompt: str,
    image_url: str,
    model: ModelType = "photon",
    output_dir: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]
```

Modify an image using the specified model.

**Parameters:**
- `prompt`: Text instruction for image modification
- `image_url`: URL of input image
- `model`: Model to use ("photon", "photon_base", "kontext", "kontext_multi", "seededit")
- `output_dir`: Custom output directory
- `**kwargs`: Model-specific parameters

**Returns:**
Dictionary with:
- `success`: Boolean indicating success/failure
- `model`: Model display name used
- `prompt`: Original prompt
- `processing_time`: Time taken in seconds
- `images`: List of image metadata from API
- `downloaded_files`: List of local file paths
- `output_directory`: Output directory path
- Additional model-specific parameters

##### modify_local_image()

```python
modify_local_image(
    prompt: str,
    image_path: str,
    model: ModelType = "photon",
    output_dir: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]
```

Modify a local image file (uploads automatically).

**Parameters:**
- `prompt`: Text instruction for image modification
- `image_path`: Path to local image file
- `model`: Model to use
- `output_dir`: Custom output directory
- `**kwargs`: Model-specific parameters

**Returns:**
Same as `modify_image()`

#### Convenience Methods

##### SeedEdit v3

```python
modify_image_seededit(
    prompt: str,
    image_url: str,
    guidance_scale: float = 0.5,
    seed: Optional[int] = None,
    output_dir: Optional[str] = None
) -> Dict[str, Any]
```

```python
modify_local_image_seededit(
    prompt: str,
    image_path: str,
    guidance_scale: float = 0.5,
    seed: Optional[int] = None,
    output_dir: Optional[str] = None
) -> Dict[str, Any]
```

**SeedEdit Parameters:**
- `guidance_scale`: 0.0-1.0, controls adherence to prompt (default: 0.5)
- `seed`: Optional integer for reproducible results

##### Photon Flash

```python
modify_image_photon(
    prompt: str,
    image_url: str,
    strength: float = 0.8,
    aspect_ratio: str = "1:1",
    output_dir: Optional[str] = None
) -> Dict[str, Any]
```

**Photon Parameters:**
- `strength`: 0.0-1.0, modification intensity (default: 0.8)
- `aspect_ratio`: Output aspect ratio ("1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21")

#### Information Methods

##### get_model_info()

```python
get_model_info(model: Optional[str] = None) -> Dict[str, Any]
```

Get information about models.

**Parameters:**
- `model`: Specific model name, or None for all models

**Returns:**
Model information dictionary or dictionary of all models

##### get_supported_models()

```python
get_supported_models() -> List[str]
```

**Returns:**
List of supported model names

##### get_supported_aspect_ratios()

```python
get_supported_aspect_ratios(model: str = "photon") -> List[str]
```

**Parameters:**
- `model`: Model name to get aspect ratios for

**Returns:**
List of supported aspect ratios for the model

#### Batch Processing

##### batch_modify_images()

```python
batch_modify_images(
    prompts: List[str],
    image_urls: List[str],
    model: ModelType = "photon",
    output_dir: Optional[str] = None,
    **kwargs
) -> List[Dict[str, Any]]
```

Process multiple images with different prompts.

**Parameters:**
- `prompts`: List of text instructions (must match image_urls length)
- `image_urls`: List of image URLs
- `model`: Model to use for all images
- `output_dir`: Custom output directory
- `**kwargs`: Model-specific parameters

**Returns:**
List of result dictionaries (one per image)

## Model-Specific Parameters

### SeedEdit v3 Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `guidance_scale` | float | 0.0-1.0 | 0.5 | Controls adherence to prompt |
| `seed` | int | - | None | Random seed for reproducibility |

### Photon Parameters

| Parameter | Type | Options | Default | Description |
|-----------|------|---------|---------|-------------|
| `strength` | float | 0.0-1.0 | 0.8 | Modification intensity |
| `aspect_ratio` | str | 1:1, 16:9, 9:16, 4:3, 3:4, 21:9, 9:21 | "1:1" | Output aspect ratio |

### Kontext Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `num_inference_steps` | int | 1-50 | 28 | Number of inference steps |
| `guidance_scale` | float | 1.0-20.0 | 2.5 | Guidance scale |
| `resolution_mode` | str | "auto", "match_input" | "auto" | Resolution handling |
| `seed` | int | - | None | Random seed for reproducibility |

## Type Definitions

### ModelType

```python
ModelType = Literal["photon", "photon_base", "kontext", "kontext_multi", "seededit"]
```

### AspectRatio

```python
AspectRatio = Literal["1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21"]
```

## Error Handling

All methods return a result dictionary with a `success` field:

```python
if result['success']:
    print(f"Generated: {result['downloaded_files']}")
else:
    print(f"Error: {result['error']}")
```

Common error scenarios:
- Invalid API key: `ValueError` during initialization
- Invalid parameters: `ValueError` with specific parameter issue
- Network/API errors: `success: False` with error message in result
- File not found: `FileNotFoundError` for local images

## Constants

### SUPPORTED_MODELS

```python
SUPPORTED_MODELS = ["photon", "photon_base", "kontext", "kontext_multi", "seededit"]
```

### MODEL_ENDPOINTS

```python
MODEL_ENDPOINTS = {
    "photon": "fal-ai/luma-photon/flash/modify",
    "photon_base": "fal-ai/luma-photon/modify",
    "kontext": "fal-ai/flux-kontext/dev",
    "kontext_multi": "fal-ai/flux-pro/kontext/max/multi",
    "seededit": "fal-ai/bytedance/seededit/v3/edit-image"
}
```