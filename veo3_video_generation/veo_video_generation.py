import os
import time
import traceback
from google import genai
from google.genai.types import GenerateVideosConfig
from google.cloud import storage

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
            
            # Download the video
            local_video_path = download_gcs_file(video_uri, "result_folder", project_id)
            if local_video_path:
                print(f"Video also available locally at: {local_video_path}")
            
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
            # For local files, upload to GCS first
            
            # Create a temporary file name in GCS
            timestamp = int(time.time())
            file_name = os.path.basename(image_path)
            # Extract bucket name and blob path from the GCS URI
            bucket_name = output_bucket_path.replace("gs://", "").split("/")[0]
            blob_path = "/".join(output_bucket_path.replace("gs://", "").split("/")[1:])
            if blob_path and not blob_path.endswith("/"):
                blob_path += "/"
            blob_path += f"{timestamp}_{file_name}"
            
            # Full GCS URI for the uploaded image
            gcs_uri = f"gs://{bucket_name}/{blob_path}"
            
            print(f"Uploading local image to GCS: {gcs_uri}")
            
            # Determine content type based on file extension
            content_type = None
            if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
                content_type = 'image/jpeg'
            elif image_path.lower().endswith('.png'):
                content_type = 'image/png'
            elif image_path.lower().endswith('.gif'):
                content_type = 'image/gif'
            elif image_path.lower().endswith('.webp'):
                content_type = 'image/webp'
            else:
                # Default to jpeg if we can't determine
                content_type = 'image/jpeg'
                
            print(f"Using content type: {content_type}")
            
            # Upload file to GCS
            storage_client = storage.Client(project=project_id)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_path)
            
            # Set content type and upload
            blob.upload_from_filename(image_path, content_type=content_type)
            
            # Now use the GCS URI and explicitly set the mime_type for the genai.Image object
            from google.genai.types import Image
            image = Image(gcs_uri=gcs_uri, mime_type=content_type)
        
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
            
            # Download the video
            local_video_path = download_gcs_file(video_uri, "result_folder", project_id)
            if local_video_path:
                print(f"Video also available locally at: {local_video_path}")
            
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

def generate_video_from_local_image(project_id, image_filename, output_bucket_path, prompt=None, model_id="veo-2.0-generate-001", location="us-central1"):
    """
    Generate a video from a local image in the video_analyzer/images folder.
    
    Args:
        project_id (str): Google Cloud project ID
        image_filename (str): Filename of the image in the video_analyzer/images folder
        output_bucket_path (str): GCS path for storing the output (e.g., "gs://dh_learn/veo_output/")
        prompt (str, optional): Optional text prompt to guide the video generation
        model_id (str): Veo model ID to use
        location (str): Google Cloud region
    
    Returns:
        str: The GCS URI of the generated video, or None if an error occurred
    """
    # Get the absolute path to the image file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "images", image_filename)
    
    # Verify the image exists
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None
    
    # Call the existing generate_video_from_image function
    return generate_video_from_image(
        project_id=project_id,
        image_path=image_path,
        output_bucket_path=output_bucket_path,
        prompt=prompt,
        model_id=model_id,
        location=location
    )

def generate_video_with_veo3_preview(project_id, prompt, output_bucket_path, location="us-central1"):
    """
    Generate a video from a text prompt using Google's Veo 3 Preview model.
    
    Args:
        project_id (str): Google Cloud project ID
        prompt (str): Text description for video generation
        output_bucket_path (str): GCS path for storing the output (e.g., "gs://dh_learn/veo_output/")
        location (str): Google Cloud region
    
    Returns:
        str: The GCS URI of the generated video, or None if an error occurred
    """
    print("Using Veo 3 Preview model (veo-3.0-generate-preview).")
    return generate_video_from_text(
        project_id=project_id,
        prompt=prompt,
        output_bucket_path=output_bucket_path,
        model_id="veo-3.0-generate-preview",
        location=location
    )

def download_gcs_file(gcs_uri: str, local_folder_path: str, project_id: str):
    """
    Downloads a file from GCS to a local folder.

    Args:
        gcs_uri (str): The GCS URI of the file to download (e.g., "gs://bucket/file.mp4").
        local_folder_path (str): The local directory to save the file to.
        project_id (str): Google Cloud project ID.

    Returns:
        str: The local path to the downloaded file, or None if an error occurred.
    """
    try:
        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)
            print(f"Created directory: {local_folder_path}")

        storage_client = storage.Client(project=project_id)
        
        if not gcs_uri.startswith("gs://"):
            print(f"Invalid GCS URI: {gcs_uri}")
            return None
        
        path_parts = gcs_uri.replace("gs://", "").split("/")
        bucket_name = path_parts[0]
        blob_name = "/".join(path_parts[1:])
        
        # Ensure blob_name is not empty, which can happen if URI is just "gs://bucketname/"
        if not blob_name:
            print(f"Invalid GCS URI - no object name specified: {gcs_uri}")
            return None

        file_name = blob_name.split("/")[-1]
        if not file_name: # Handle cases like "gs://bucket/folder/"
             print(f"Invalid GCS URI - URI points to a folder or has a trailing slash: {gcs_uri}")
             return None
        local_file_path = os.path.join(local_folder_path, file_name)
        
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        print(f"Downloading {gcs_uri} to {local_file_path}...")
        blob.download_to_filename(local_file_path)
        print(f"Successfully downloaded to {local_file_path}")
        return local_file_path
    except Exception as e:
        print(f"Error downloading {gcs_uri}: {e}")
        print("Full download error details:")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # You need to install the Google genai SDK first:
    # pip install --upgrade google-genai
    
    # Set your project ID and output path
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    OUTPUT_BUCKET_PATH = os.getenv("OUTPUT_BUCKET_PATH", "gs://your-bucket-name/veo_output/")
    
    # Example 1: Generate video from text
    # prompt = "A serene mountain landscape with a flowing river and colorful sunset. Camera slowly pans across the scene."
    # video_uri = generate_video_from_text(
    #     project_id=PROJECT_ID,
    #     prompt=prompt,
    #     output_bucket_path=OUTPUT_BUCKET_PATH
    # )
    
    # if video_uri:
    #     print(f"Video is available at: {video_uri}")
    
    # Example 2: Generate video from a local image in the images folder
    # Use the new simplified function for local images
    # image_prompt = "The man comes to life, smiling and looking around with a happy expression"
    
    # video_uri = generate_video_from_local_image(
    #     project_id=PROJECT_ID,
    #     image_filename="smiling_woman.jpg",
    #     output_bucket_path=OUTPUT_BUCKET_PATH,
    #     prompt=image_prompt  # Optional but recommended for better results
    # )
    
    # if video_uri:
    #     print(f"Image-to-video is available at: {video_uri}")

    # Example 3: Generate video with Veo 3 Preview model (uncomment to use)
    # Make sure your project is allowlisted for veo-3.0-generate-preview
    # """
    veo3_prompt = "A futuristic cityscape with flying vehicles and neon lights, cinematic style."
    video_uri_veo3 = generate_video_with_veo3_preview(
        project_id=PROJECT_ID,
        prompt=veo3_prompt,
        output_bucket_path=OUTPUT_BUCKET_PATH
    )
    
    if video_uri_veo3:
        print(f"Veo 3 Preview video is available at: {video_uri_veo3}")
    # """ 