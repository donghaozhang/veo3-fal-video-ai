"""
FAL AI Image-to-Video Generation
Advanced image-to-video generation using FAL AI's dual models with high-quality output
"""

import os
import time
import traceback
from typing import Optional, Dict, Any
import fal_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FALImageToVideoGenerator:
    """
    FAL AI Image-to-Video Generator supporting multiple models
    
    Supports:
    - MiniMax Hailuo-02: 768p resolution, 6-10 second videos
    - Kling Video 2.1: High-quality image-to-video generation, 5-10 second videos
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FAL Image-to-Video Generator
        
        Args:
            api_key: FAL API key (if not provided, will use FAL_KEY environment variable)
        """
        self.api_key = api_key or os.getenv('FAL_KEY')
        if not self.api_key:
            raise ValueError("FAL API key is required. Set FAL_KEY environment variable or pass api_key parameter.")
        
        # Set the API key for fal_client
        os.environ['FAL_KEY'] = self.api_key
        
        # Model endpoints
        self.hailuo_endpoint = "fal-ai/minimax/hailuo-02/standard/image-to-video"
        self.kling_endpoint = "fal-ai/kling-video/v2.1/standard/image-to-video"
        
    def generate_video_from_image(
        self,
        prompt: str,
        image_url: str,
        duration: str = "6",
        prompt_optimizer: bool = True,
        output_folder: str = "output",
        use_async: bool = False,
        model: str = "fal-ai/minimax/hailuo-02/standard/image-to-video"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate video from image using FAL AI models
        
        Args:
            prompt: Text description for video generation
            image_url: URL of the image to use as the first frame
            duration: Duration in seconds ("6" or "10" for Hailuo, "5" or "10" for Kling)
            prompt_optimizer: Whether to use the model's prompt optimizer (Hailuo only)
            output_folder: Local folder to save the generated video
            use_async: Whether to use async processing
            model: Model to use (full endpoint name):
                   - "fal-ai/minimax/hailuo-02/standard/image-to-video" for MiniMax Hailuo-02
                   - "fal-ai/kling-video/v2.1/standard/image-to-video" for Kling Video 2.1
            
        Returns:
            Dictionary containing the result with video URL and metadata
        """
        try:
            # Select model endpoint
            if model == "fal-ai/kling-video/v2.1/standard/image-to-video":
                endpoint = self.kling_endpoint
                model_name = "Kling Video 2.1"
                # Kling specific parameters
                arguments = {
                    "prompt": prompt,
                    "image_url": image_url,
                    "duration": duration,
                    "negative_prompt": "blur, distort, and low quality",
                    "cfg_scale": 0.5
                }
            else:  # Default to Hailuo
                endpoint = self.hailuo_endpoint
                model_name = "MiniMax Hailuo-02"
                # Hailuo specific parameters
                arguments = {
                    "prompt": prompt,
                    "image_url": image_url,
                    "duration": duration,
                    "prompt_optimizer": prompt_optimizer
                }
            
            print(f"Starting video generation with FAL AI {model_name}...")
            print(f"Prompt: '{prompt}'")
            print(f"Image URL: {image_url}")
            print(f"Duration: {duration} seconds")
            print(f"Model: {model_name}")
            
            # Generate unique task ID
            task_id = str(uuid.uuid4())[:8]
            print(f"Task ID: {task_id}")
            
            # Define queue update handler
            def on_queue_update(update):
                if hasattr(update, 'logs') and update.logs:
                    print("Processing... Logs:")
                    for log in update.logs:
                        print(f"  {log.get('message', str(log))}")
                else:
                    print(f"Processing... Update: {type(update).__name__}")
            
            # Generate video
            print("Submitting request to FAL AI...")
            
            if use_async:
                # Async processing
                handler = fal_client.submit(
                    endpoint,
                    arguments=arguments
                )
                
                request_id = handler.request_id
                print(f"Request submitted with ID: {request_id}")
                
                # Poll for completion
                while True:
                    status = fal_client.status(endpoint, request_id, with_logs=True)
                    print(f"Status: {status.status}")
                    
                    if status.status == "COMPLETED":
                        result = fal_client.result(endpoint, request_id)
                        break
                    elif status.status == "FAILED":
                        print(f"Request failed: {status}")
                        return None
                    
                    time.sleep(5)  # Wait 5 seconds before checking again
                    
            else:
                # Synchronous processing
                result = fal_client.subscribe(
                    endpoint,
                    arguments=arguments,
                    with_logs=True,
                    on_queue_update=on_queue_update,
                )
            
            print("Video generation completed successfully!")
            
            # Process result
            if result and 'video' in result:
                video_info = result['video']
                video_url = video_info['url']
                original_file_name = video_info.get('file_name', 'generated_video.mp4')
                file_size = video_info.get('file_size', 0)
                
                # Generate custom filename: inputname_taskid.mp4
                if input_filename:
                    base_name = os.path.splitext(input_filename)[0]
                    custom_filename = f"{base_name}_{task_id}.mp4"
                else:
                    custom_filename = f"generated_{task_id}.mp4"
                
                print(f"Generated video URL: {video_url}")
                print(f"Original file name: {original_file_name}")
                print(f"Custom file name: {custom_filename}")
                print(f"File size: {file_size} bytes")
                
                # Download video locally with custom filename
                local_path = self.download_video(video_url, output_folder, custom_filename)
                if local_path:
                    result['local_path'] = local_path
                    result['task_id'] = task_id
                    result['custom_filename'] = custom_filename
                
                return result
            else:
                print("No video found in result")
                return None
                
        except Exception as e:
            print(f"Error during video generation: {e}")
            traceback.print_exc()
            return None
    
    def upload_local_image(self, image_path: str) -> Optional[str]:
        """
        Upload a local image file to FAL AI and get the URL
        
        Args:
            image_path: Path to the local image file
            
        Returns:
            URL of the uploaded image or None if failed
        """
        try:
            print(f"Uploading local image: {image_path}")
            
            if not os.path.exists(image_path):
                print(f"Image file not found: {image_path}")
                return None
            
            # Upload file to FAL AI
            url = fal_client.upload_file(image_path)
            print(f"Image uploaded successfully: {url}")
            return url
            
        except Exception as e:
            print(f"Error uploading image: {e}")
            traceback.print_exc()
            return None
    
    def generate_video_from_local_image(
        self,
        prompt: str,
        image_path: str,
        duration: str = "6",
        prompt_optimizer: bool = True,
        output_folder: str = "output",
        use_async: bool = False,
        model: str = "fal-ai/minimax/hailuo-02/standard/image-to-video"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate video from local image file
        
        Args:
            prompt: Text description for video generation
            image_path: Path to the local image file
            duration: Duration in seconds ("6" or "10" for Hailuo, "5" or "10" for Kling)
            prompt_optimizer: Whether to use the model's prompt optimizer (Hailuo only)
            output_folder: Local folder to save the generated video
            use_async: Whether to use async processing
            model: Model to use (full endpoint name):
                   - "fal-ai/minimax/hailuo-02/standard/image-to-video" for MiniMax Hailuo-02
                   - "fal-ai/kling-video/v2.1/standard/image-to-video" for Kling Video 2.1
            
        Returns:
            Dictionary containing the result with video URL and metadata
        """
        # First upload the local image
        image_url = self.upload_local_image(image_path)
        if not image_url:
            return None
        
        # Generate video using the uploaded image URL
        return self.generate_video_from_image(
            prompt=prompt,
            image_url=image_url,
            duration=duration,
            prompt_optimizer=prompt_optimizer,
            output_folder=output_folder,
            use_async=use_async,
            model=model
        )
    
    def generate_video_with_kling(
        self,
        prompt: str,
        image_url: str,
        duration: str = "5",
        negative_prompt: str = "blur, distort, and low quality",
        cfg_scale: float = 0.5,
        output_folder: str = "output",
        use_async: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Generate video using Kling Video 2.1 model specifically
        
        Args:
            prompt: Text description for video generation
            image_url: URL of the image to use as the first frame
            duration: Duration in seconds ("5" or "10")
            negative_prompt: Negative prompt to avoid certain elements
            cfg_scale: CFG scale for guidance (0.5 default)
            output_folder: Local folder to save the generated video
            use_async: Whether to use async processing
            
        Returns:
            Dictionary containing the result with video URL and metadata
        """
        try:
            print(f"Starting video generation with Kling Video 2.1...")
            print(f"Prompt: '{prompt}'")
            print(f"Image URL: {image_url}")
            print(f"Duration: {duration} seconds")
            print(f"CFG Scale: {cfg_scale}")
            
            # Kling specific parameters
            arguments = {
                "prompt": prompt,
                "image_url": image_url,
                "duration": duration,
                "negative_prompt": negative_prompt,
                "cfg_scale": cfg_scale
            }
            
            # Define queue update handler
            def on_queue_update(update):
                if hasattr(update, 'logs') and update.logs:
                    print("Processing... Logs:")
                    for log in update.logs:
                        print(f"  {log.get('message', str(log))}")
                else:
                    print(f"Processing... Update: {type(update).__name__}")
            
            # Generate video
            print("Submitting request to FAL AI Kling...")
            
            if use_async:
                # Async processing
                handler = fal_client.submit(
                    self.kling_endpoint,
                    arguments=arguments
                )
                
                request_id = handler.request_id
                print(f"Request submitted with ID: {request_id}")
                
                # Poll for completion
                while True:
                    status = fal_client.status(self.kling_endpoint, request_id, with_logs=True)
                    print(f"Status: {status.status}")
                    
                    if status.status == "COMPLETED":
                        result = fal_client.result(self.kling_endpoint, request_id)
                        break
                    elif status.status == "FAILED":
                        print(f"Request failed: {status}")
                        return None
                    
                    time.sleep(5)  # Wait 5 seconds before checking again
                    
            else:
                # Synchronous processing
                result = fal_client.subscribe(
                    self.kling_endpoint,
                    arguments=arguments,
                    with_logs=True,
                    on_queue_update=on_queue_update,
                )
            
            print("Video generation completed successfully!")
            
            # Process result
            if result and 'video' in result:
                video_info = result['video']
                video_url = video_info['url']
                original_file_name = video_info.get('file_name', 'kling_video.mp4')
                file_size = video_info.get('file_size', 0)
                
                # Generate custom filename: inputname_taskid.mp4
                if input_filename:
                    base_name = os.path.splitext(input_filename)[0]
                    custom_filename = f"{base_name}_{task_id}.mp4"
                else:
                    custom_filename = f"kling_{task_id}.mp4"
                
                print(f"Generated video URL: {video_url}")
                print(f"Original file name: {original_file_name}")
                print(f"Custom file name: {custom_filename}")
                print(f"File size: {file_size} bytes")
                
                # Download video locally with custom filename
                local_path = self.download_video(video_url, output_folder, custom_filename)
                if local_path:
                    result['local_path'] = local_path
                    result['task_id'] = task_id
                    result['custom_filename'] = custom_filename
                
                return result
            else:
                print("No video found in result")
                return None
                
        except Exception as e:
            print(f"Error during Kling video generation: {e}")
            traceback.print_exc()
            return None
    
    def generate_video_with_hailuo(
        self,
        prompt: str,
        image_url: str,
        duration: str = "6",
        prompt_optimizer: bool = True,
        output_folder: str = "output",
        use_async: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Generate video using MiniMax Hailuo-02 model specifically
        
        Args:
            prompt: Text description for video generation
            image_url: URL of the image to use as the first frame
            duration: Duration in seconds ("6" or "10")
            prompt_optimizer: Whether to use the model's prompt optimizer
            output_folder: Local folder to save the generated video
            use_async: Whether to use async processing
            
        Returns:
            Dictionary containing the result with video URL and metadata
        """
        return self.generate_video_from_image(
            prompt=prompt,
            image_url=image_url,
            duration=duration,
            prompt_optimizer=prompt_optimizer,
            output_folder=output_folder,
            use_async=use_async,
            model="fal-ai/minimax/hailuo-02/standard/image-to-video"
        )
    
    def download_video(self, video_url: str, output_folder: str, filename: str) -> Optional[str]:
        """
        Download video from URL to local folder
        
        Args:
            video_url: URL of the video to download
            output_folder: Local folder to save the video
            filename: Name of the file to save
            
        Returns:
            Local path of the downloaded video or None if failed
        """
        try:
            import requests
            
            # Create output folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)
            
            # Download video
            print(f"Downloading video from: {video_url}")
            response = requests.get(video_url, stream=True)
            response.raise_for_status()
            
            # Save to local file
            local_path = os.path.join(output_folder, filename)
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Video downloaded successfully: {local_path}")
            return local_path
            
        except Exception as e:
            print(f"Error downloading video: {e}")
            traceback.print_exc()
            return None


def main():
    """
    Example usage of FAL Video Generator
    """
    try:
        # Initialize the generator
        generator = FALImageToVideoGenerator()
        
        # Example 1: Generate video from online image URL
        print("=== Example 1: Generate from online image ===")
        result1 = generator.generate_video_from_image(
            prompt="Man walked into winter cave with polar bear",
            image_url="https://storage.googleapis.com/falserverless/model_tests/minimax/1749891352437225630-389852416840474630_1749891352.png",
            duration="6",
            output_folder="output"
        )
        
        if result1:
            print("✅ Video generation successful!")
            print(f"Video URL: {result1['video']['url']}")
            if 'local_path' in result1:
                print(f"Local path: {result1['local_path']}")
        
        # Example 2: Generate video from local image (if available)
        local_image_path = "input/smiling_woman.jpg"
        if os.path.exists(local_image_path):
            print("\n=== Example 2: Generate from local image ===")
            result2 = generator.generate_video_from_local_image(
                prompt="A smiling woman in a beautiful garden, gentle breeze moving her hair",
                image_path=local_image_path,
                duration="6",
                output_folder="output"
            )
            
            if result2:
                print("✅ Local image video generation successful!")
                print(f"Video URL: {result2['video']['url']}")
                if 'local_path' in result2:
                    print(f"Local path: {result2['local_path']}")
        else:
            print(f"\n⚠️ Local image not found: {local_image_path}")
            print("Skipping local image example")
        
    except Exception as e:
        print(f"Error in main: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main() 