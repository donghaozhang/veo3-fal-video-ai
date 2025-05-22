import os
import time
import traceback
from google import genai
from google.genai.types import GenerateVideosConfig

def generate_video_from_text(project_id, prompt, output_bucket_path, model_id="veo-2.0-generate-001", location="us-central1"):
    """
    Generate a video from a text prompt using Google's Veo API.
    
    Args:
        project_id (str): Google Cloud project ID
        prompt (str): Text description for video generation
        output_bucket_path (str): GCS path for storing the output (e.g., "gs://dh_learn/veo_output/")
        model_id (str): Veo model ID to use
        location (str): Google Cloud region
    
    Returns:
        str: The GCS URI of the generated video, or None if an error occurred
    """
    # Set environment variables for the genai SDK
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["GOOGLE_CLOUD_LOCATION"] = location
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    
    # Remove GOOGLE_APPLICATION_CREDENTIALS if it's set
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    
    # Initialize the client
    print("Initializing Google GenAI client...")
    client = genai.Client()
    print(f"Client initialized for project: {project_id}")
    
    try:
        # Start the video generation operation
        print(f"Starting video generation with prompt: '{prompt}'")
        
        operation = client.models.generate_videos(
            model=model_id,
            prompt=prompt,
            config=GenerateVideosConfig(
                aspect_ratio="16:9",
                output_gcs_uri=output_bucket_path,
                # Optional: you can add more parameters here
                # duration_seconds=5,  # Video duration (seconds)
                # fps=24,             # Frames per second
            ),
        )
        
        print(f"Video generation operation started. Operation name: {operation.name}")
        print("Polling for completion...")
        
        # Poll for completion
        while not operation.done:
            time.sleep(15)  # Check every 15 seconds
            operation = client.operations.get(operation)
            print(f"Operation status: {operation.metadata.state if operation.metadata else 'Processing...'}")
        
        # Check the result
        if operation.response and operation.result.generated_videos:
            video_uri = operation.result.generated_videos[0].video.uri
            print(f"Video generated successfully: {video_uri}")
            return video_uri
        elif operation.error:
            print(f"Error during video generation: {str(operation.error)}")
            return None
        else:
            print("Operation finished but no video URI found or an unknown error occurred.")
            return None
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Full error details:")
        traceback.print_exc()
        return None

def generate_video_from_image(project_id, image_path, output_bucket_path, prompt=None, model_id="veo-2.0-generate-001", location="us-central1"):
    """
    Generate a video from an image using Google's Veo API.
    
    Args:
        project_id (str): Google Cloud project ID
        image_path (str): GCS path to the image file (e.g., "gs://bucket/image.jpg") or local file path
        output_bucket_path (str): GCS path for storing the output (e.g., "gs://dh_learn/veo_output/")
        prompt (str, optional): Optional text prompt to guide the video generation
        model_id (str): Veo model ID to use
        location (str): Google Cloud region
    
    Returns:
        str: The GCS URI of the generated video, or None if an error occurred
    """
    # Set environment variables for the genai SDK
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["GOOGLE_CLOUD_LOCATION"] = location
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
    
    # Remove GOOGLE_APPLICATION_CREDENTIALS if it's set
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    
    # Initialize the client
    print("Initializing Google GenAI client...")
    client = genai.Client()
    print(f"Client initialized for project: {project_id}")
    
    try:
        # Check if the image is a local file or GCS URI
        if image_path.startswith("gs://"):
            # GCS URI
            from google.genai.types import Image
            image = Image(gcs_uri=image_path)
        else:
            # Local file
            image = genai.upload_file(path=image_path)
        
        # Start the video generation operation
        print(f"Starting image-to-video generation with image: '{image_path}'")
        
        # Create operation based on whether a prompt is provided
        if prompt:
            print(f"Using additional prompt: '{prompt}'")
            operation = client.models.generate_videos(
                model=model_id,
                image=image,
                prompt=prompt,
                config=GenerateVideosConfig(
                    aspect_ratio="16:9",
                    output_gcs_uri=output_bucket_path,
                ),
            )
        else:
            operation = client.models.generate_videos(
                model=model_id,
                image=image,
                config=GenerateVideosConfig(
                    aspect_ratio="16:9",
                    output_gcs_uri=output_bucket_path,
                ),
            )
        
        print(f"Video generation operation started. Operation name: {operation.name}")
        print("Polling for completion...")
        
        # Poll for completion
        while not operation.done:
            time.sleep(15)  # Check every 15 seconds
            operation = client.operations.get(operation)
            print(f"Operation status: {operation.metadata.state if operation.metadata else 'Processing...'}")
        
        # Check the result
        if operation.response and operation.result.generated_videos:
            video_uri = operation.result.generated_videos[0].video.uri
            print(f"Video generated successfully: {video_uri}")
            return video_uri
        elif operation.error:
            print(f"Error during video generation: {str(operation.error)}")
            return None
        else:
            print("Operation finished but no video URI found or an unknown error occurred.")
            return None
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Full error details:")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # You need to install the Google genai SDK first:
    # pip install --upgrade google-genai
    
    # Set your project ID and output path
    PROJECT_ID = "speedy-sunspot-460603-p7"
    OUTPUT_BUCKET_PATH = "gs://test_dh/veo_output/"
    
    # Example 1: Generate video from text
    prompt = "A serene mountain landscape with a flowing river and colorful sunset. Camera slowly pans across the scene."
    video_uri = generate_video_from_text(
        project_id=PROJECT_ID,
        prompt=prompt,
        output_bucket_path=OUTPUT_BUCKET_PATH
    )
    
    if video_uri:
        print(f"Video is available at: {video_uri}")
    
    # Example 2: Generate video from image (uncomment to use)
    # Note: Replace with your image path (can be a GCS URI or local file)
    """
    image_path = "gs://dh_learn/input_images/landscape.jpg"  # or a local path like "C:/path/to/image.jpg"
    image_prompt = "The landscape comes alive with gentle movements and birds flying in the distance"
    
    video_uri = generate_video_from_image(
        project_id=PROJECT_ID,
        image_path=image_path,
        output_bucket_path=OUTPUT_BUCKET_PATH,
        prompt=image_prompt  # Optional
    )
    
    if video_uri:
        print(f"Image-to-video is available at: {video_uri}")
    """ 