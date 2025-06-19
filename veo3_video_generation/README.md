# Google Veo Video Generation

This project provides a Python implementation for generating videos using Google's Veo API on Vertex AI. The implementation supports both text-to-video and image-to-video generation with multiple Veo model versions.

## Features

- **Text-to-Video Generation**: Create videos from descriptive text prompts
- **Image-to-Video Generation**: Animate static images with optional text guidance
- **Multiple Model Support**: Veo 2.0 (stable) and Veo 3.0 (preview) models
- **Flexible Configuration**: Customizable video parameters (aspect ratio, duration, fps)
- **Local Image Support**: Direct upload and processing of local image files
- **Automatic Download**: Generated videos downloaded to local storage
- **Built with Official SDK**: Uses the official Google GenAI SDK

## Prerequisites

1. **Google Cloud Project**: With Vertex AI API enabled
2. **Google Cloud Storage Bucket**: To store generated videos
3. **Authentication**: Proper gcloud CLI authentication setup
4. **Python 3.8+**: Compatible Python version
5. **API Access**: Veo model access (Veo 3.0 requires allowlist approval)

## Step-by-Step Setup Guide

### 1. Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Set up Google Cloud SDK

Ensure Google Cloud SDK is properly installed and accessible:
```powershell
# On Windows, add to PATH if needed:
$env:PATH += ";C:\Users\<username>\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
```

### 3. Authenticate with Google Cloud

```powershell
# Login with your Google account
gcloud auth login your-email@gmail.com

# Set up application default credentials
gcloud auth application-default login

# Set your project ID
gcloud config set project your-project-id
```

### 4. Grant Storage Permissions

Grant necessary permissions to the Veo service account:
```powershell
# For Veo 2.0 model
gcloud storage buckets add-iam-policy-binding gs://your-bucket \
  --member="user:cloud-lvm-video-server@prod.google.com" \
  --role=roles/storage.objectCreator

gcloud storage buckets add-iam-policy-binding gs://your-bucket \
  --member="user:cloud-lvm-video-server@prod.google.com" \
  --role=roles/storage.objectAdmin
```

### 5. Configure Environment Variables

Copy the example configuration file and update with your values:
```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your actual values
# Update these two key variables:
GOOGLE_CLOUD_PROJECT=your-actual-project-id
OUTPUT_BUCKET_PATH=gs://your-actual-bucket/veo_output/
```

### 6. Quick Permission Fix (Automated)

Run the automated permission fix tool:
```bash
# This fixes 90% of permission issues automatically
python fix_permissions.py

# Or specify your project/bucket manually
python fix_permissions.py --project-id your-project-id --bucket-name your-bucket
```

### 7. Test Your Setup

```bash
# Quick test (text-to-video with Veo 2.0 only)
python test_veo.py --text-only

# Full test (both models, text and image)
python test_veo.py --full

# Interactive demo
python demo.py
```

### 8. Download Generated Videos

Videos are automatically downloaded to the `result_folder/` directory. You can also manually download from GCS:
```bash
gcloud storage cp gs://your-bucket/veo_output/<generation-id>/sample_0.mp4 ./result_folder/
```

## Usage Examples

### Text-to-Video Generation

```python
import os
from veo_video_generation import generate_video_from_text

# Configuration is loaded from .env file automatically
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
OUTPUT_BUCKET_PATH = os.getenv("OUTPUT_BUCKET_PATH")

# Basic text-to-video
video_uri = generate_video_from_text(
    project_id=PROJECT_ID,
    prompt="A serene mountain landscape with a flowing river and colorful sunset. Camera slowly pans across the scene.",
    output_bucket_path=OUTPUT_BUCKET_PATH
)

# Using Veo 3.0 Preview model
video_uri = generate_video_with_veo3_preview(
    project_id=PROJECT_ID,
    prompt="A futuristic cityscape with flying vehicles and neon lights, cinematic style.",
    output_bucket_path=OUTPUT_BUCKET_PATH
)
```

### Image-to-Video Generation

```python
import os
from veo_video_generation import generate_video_from_image, generate_video_from_local_image

# Configuration from environment
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
OUTPUT_BUCKET_PATH = os.getenv("OUTPUT_BUCKET_PATH")

# From GCS-hosted image
video_uri = generate_video_from_image(
    project_id=PROJECT_ID,
    image_path="gs://your-bucket/images/landscape.jpg",
    output_bucket_path=OUTPUT_BUCKET_PATH,
    prompt="The landscape comes alive with gentle movements"  # Optional
)

# From local image file
video_uri = generate_video_from_local_image(
    project_id=PROJECT_ID,
    image_filename="smiling_woman.jpg",  # File in ./images/ folder
    output_bucket_path=OUTPUT_BUCKET_PATH,
    prompt="The person comes to life, smiling and looking around with a happy expression"
)
```

## Available Functions

### Core Functions

- `generate_video_from_text()` - Generate video from text prompt
- `generate_video_from_image()` - Generate video from image (GCS or local)
- `generate_video_from_local_image()` - Generate video from local image file
- `generate_video_with_veo3_preview()` - Generate video using Veo 3.0 model
- `download_gcs_file()` - Download generated videos from GCS

### Function Parameters

All generation functions support these common parameters:
- `project_id` (str): Your Google Cloud project ID
- `output_bucket_path` (str): GCS path for storing outputs
- `model_id` (str): Veo model to use (default: "veo-2.0-generate-001")
- `location` (str): Google Cloud region (default: "us-central1")

## Model Versions

### Veo 2.0 (Stable)
- **Model ID**: `veo-2.0-generate-001`
- **Status**: Generally available
- **Quality**: High-quality, reliable results
- **Access**: Standard API access

### Veo 3.0 (Preview)
- **Model ID**: `veo-3.0-generate-preview`
- **Status**: Preview/Beta
- **Quality**: Enhanced quality and capabilities
- **Access**: Requires allowlist approval from Google Cloud

## Configuration Options

Customize video generation with `GenerateVideosConfig`:

```python
from google.genai.types import GenerateVideosConfig

config = GenerateVideosConfig(
    aspect_ratio="16:9",        # "16:9", "4:3", "1:1", "9:16"
    output_gcs_uri="gs://your-bucket/output/",
    duration_seconds=5,         # Video length in seconds
    fps=24                      # Frames per second
)
```

## Troubleshooting

### Veo 3.0 Access Issues

**Error**: "Text to video is not allowlisted for project"
**Solutions**:
1. **Use Veo 2.0**: Change model_id to `"veo-2.0-generate-001"`
2. **Request Access**: Apply for Veo 3.0 allowlist through Google Cloud Console

### Storage Permission Issues

**Error**: "Permission 'storage.objects.create' denied"
**Solution**:
```bash
gcloud storage buckets add-iam-policy-binding gs://your-bucket \
  --member="user:cloud-lvm-video-server@prod.google.com" \
  --role=roles/storage.objectAdmin
```

### Authentication Issues

**Problem**: Invalid or missing credentials
**Solutions**:
1. Check active account: `gcloud auth list`
2. Re-authenticate: `gcloud auth application-default login`
3. Verify project: `gcloud config get project`

### Image Upload Failures

**Problem**: Cannot process local images
**Solutions**:
1. Verify image format (JPEG, PNG, GIF, WebP supported)
2. Check file permissions and path accessibility
3. Ensure GCS bucket exists and is writable
4. Verify content-type detection

## Best Practices for Prompts

For optimal results with Veo, include detailed descriptions:

### Text-to-Video Prompts
1. **Subjects and Actions**: Clearly describe what/who and their actions
2. **Setting and Environment**: Specify location and context
3. **Cinematic Elements**: Camera movements, lighting, mood
4. **Technical Details**: Shot type, style, atmosphere

**Example**:
```
A medium shot, historical adventure setting: Warm lamplight illuminates a cartographer in a cluttered study, poring over an ancient, sprawling map spread across a large table. The cartographer looks up excitedly and declares: "According to this old sea chart, the lost island isn't myth! We must prepare an expedition immediately!" Camera slowly zooms in on the detailed map.
```

### Image-to-Video Prompts
1. **Movement Description**: How the scene should animate
2. **Consistency**: Maintain the original image's style and content
3. **Subtle Changes**: Avoid dramatic transformations
4. **Natural Motion**: Describe realistic, believable movements

**Example**:
```
The person comes to life with a gentle, warm smile spreading across their face. Their eyes light up with joy as they turn slightly toward the camera, hair moving softly as if in a gentle breeze.
```

## Project Structure

```
veo3_video_generation/
├── veo_video_generation.py     # Main video generation functions
├── demo.py                     # Interactive demo with menu system
├── test_veo.py                # Comprehensive test suite with CLI options
├── fix_permissions.py         # 🔧 Automated Google Cloud permission fix tool
├── README.md                  # This documentation
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration (copy from .env.example)
├── .env.example              # Template with dummy values for all variables
├── images/                    # Input images for image-to-video generation
│   ├── smiling_woman.jpg     # Sample portrait image
│   └── bet.png               # Sample landscape image
└── result_folder/            # Downloaded video outputs
```

### Key Files Explained

- **`.env.example`**: Template showing all required environment variables with dummy values
- **`.env`**: Your actual configuration (copy from .env.example and update with real values)
- **`fix_permissions.py`**: Automated tool that fixes 90% of Google Cloud permission issues
- **`demo.py`**: Interactive menu-driven demo for testing all features
- **`test_veo.py`**: Command-line test suite with options like `--text-only`, `--compare`, `--full`

## Dependencies

- `google-genai>=0.1.0` - Official Google GenAI SDK
- `google-cloud-aiplatform>=1.38.0` - Vertex AI client
- `google-cloud-storage>=2.10.0` - Cloud Storage operations
- `google-auth>=2.23.0` - Authentication
- `requests>=2.31.0` - HTTP requests
- `python-dotenv>=1.0.0` - Environment variable management
- `pillow>=10.0.0` - Image processing

## Performance Considerations

- **Generation Time**: Videos typically take 2-10 minutes to generate
- **Model Differences**: Veo 3.0 may take longer but produces higher quality
- **Concurrent Requests**: Respect API rate limits and quotas
- **Storage Costs**: Consider GCS storage costs for large video files

## Resources

- [Veo API Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation)
- [Google GenAI SDK](https://github.com/google/generative-ai-python)
- [Vertex AI Console](https://console.cloud.google.com/vertex-ai)
- [Google Cloud Storage](https://console.cloud.google.com/storage)

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Google Cloud documentation
3. Verify API quotas and permissions
4. Test with simpler prompts first 