# Google Veo 3 Video Generation

This project provides a Python script for generating videos using Google's Veo API on Vertex AI. The script supports both text-to-video and image-to-video generation.

## Features

- Generate videos from text prompts
- Generate videos from images (with optional text guidance)
- Configurable video parameters (aspect ratio, duration, etc.)
- Built with the official Google GenAI SDK

## Prerequisites

1. A Google Cloud project with Vertex AI API enabled
2. A Google Cloud Storage bucket to store the generated videos
3. Proper authentication set up (gcloud CLI)
4. Python 3.7+ installed

## Step-by-Step Setup Guide

### 1. Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Set up Google Cloud SDK

First, locate your Google Cloud SDK installation:
```powershell
# On Windows, the SDK is typically located at:
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

If you're using Veo 2.0 model, you'll need to grant permissions to the service account:
```powershell
gcloud storage buckets add-iam-policy-binding gs://your-bucket --member="user:cloud-lvm-video-server@prod.google.com" --role=roles/storage.objectCreator
gcloud storage buckets add-iam-policy-binding gs://your-bucket --member="user:cloud-lvm-video-server@prod.google.com" --role=roles/storage.objectAdmin
```

### 5. Configure the Script

Edit `veo3_video_generation.py` to set your project ID and output bucket path:
```python
PROJECT_ID = "your-project-id"
OUTPUT_BUCKET_PATH = "gs://your-bucket/veo_output/"
```

### 6. Run the Script

```powershell
python veo3_video_generation.py
```

### 7. Download the Generated Video

Once the video is generated, you can download it from the Google Cloud Storage bucket:
```powershell
gcloud storage cp gs://your-bucket/veo_output/<generation-id>/sample_0.mp4 .
```

## Usage

### Basic Usage

1. Edit the script to set your project ID and output bucket path:
   ```python
   PROJECT_ID = "your-project-id"
   OUTPUT_BUCKET_PATH = "gs://your-bucket/output/"
   ```

2. Run the script:
   ```bash
   python veo3_video_generation.py
   ```

### Generating Videos from Text

```python
from veo3_video_generation import generate_video_from_text

video_uri = generate_video_from_text(
    project_id="your-project-id",
    prompt="A serene mountain landscape with a flowing river and colorful sunset. Camera slowly pans across the scene.",
    output_bucket_path="gs://your-bucket/output/"
)
```

### Generating Videos from Images

```python
from veo3_video_generation import generate_video_from_image

video_uri = generate_video_from_image(
    project_id="your-project-id",
    image_path="gs://your-bucket/images/landscape.jpg",  # or a local path
    output_bucket_path="gs://your-bucket/output/",
    prompt="The landscape comes alive with gentle movements"  # Optional
)
```

## Troubleshooting

### Access Issues with Veo 3.0

If you encounter the error "Text to video is not allowlisted for project", you have two options:

1. **Switch to Veo 2.0**: Modify the model_id parameter to "veo-2.0-generate-001" instead of "veo-3.0-generate-preview"
2. **Request Allowlist Access**: For Veo 3.0, you need to request allowlist access from Google Cloud

### Storage Permission Issues

If you encounter permission errors when writing to Google Cloud Storage:
```
ERROR: ('An error occurred while generating the video: Error generating video: 
<_InactiveRpcError of RPC that terminated with: 
status = StatusCode.PERMISSION_DENIED, 
details = "Permission 'storage.objects.create' denied on resource...">')
```

Fix with:
```powershell
gcloud storage buckets add-iam-policy-binding gs://your-bucket --member="user:cloud-lvm-video-server@prod.google.com" --role=roles/storage.objectAdmin
```

## Tips for Better Prompts

For better results with Veo, include details about:

1. **Subjects and actions**: What/who is in the video and what are they doing
2. **Setting and environment**: Where the scene takes place
3. **Cinematic styles**: Camera movements, lighting, etc.
4. **Mood and tone**: The emotional feel of the video

Example of a detailed prompt:
```
A medium shot, historical adventure setting: Warm lamplight illuminates a cartographer in a cluttered study, 
poring over an ancient, sprawling map spread across a large table. Cartographer: "According to this old sea chart, 
the lost island isn't myth! We must prepare an expedition immediately!"
```

## Configuration Options

You can customize video generation with these parameters:

- `aspect_ratio`: The aspect ratio of the video (e.g., "16:9", "4:3", "1:1")
- `duration_seconds`: The length of the video in seconds
- `fps`: Frames per second

Example:
```python
from google.genai.types import GenerateVideosConfig

config = GenerateVideosConfig(
    aspect_ratio="16:9",
    output_gcs_uri="gs://your-bucket/output/",
    duration_seconds=5,
    fps=24
)
```

## Resources

- [Veo API Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation)
- [Google GenAI SDK](https://github.com/google/generative-ai-python)
- [How to Use Google Veo 3 API on Vertex AI](https://apidog.com/blog/google-veo-3-api/) 