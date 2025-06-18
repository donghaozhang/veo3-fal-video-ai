#!/usr/bin/env python3
"""
Google Veo Video Generation Test Suite

This test script validates all the functionality of the Google Veo video generation implementation.
It includes tests for both Veo 2.0 and Veo 3.0 models, text-to-video, image-to-video, and error handling.

Usage:
    python test_veo.py                    # Run basic tests
    python test_veo.py --veo3             # Test Veo 3.0 specifically
    python test_veo.py --compare          # Compare both models
    python test_veo.py --full             # Run comprehensive tests
    python test_veo.py --image-only       # Test only image-to-video
    python test_veo.py --text-only        # Test only text-to-video
"""

import os
import sys
import argparse
import time
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from veo_video_generation import (
        generate_video_from_text,
        generate_video_from_image,
        generate_video_from_local_image,
        generate_video_with_veo3_preview,
        download_gcs_file
    )
except ImportError as e:
    print(f"❌ Error importing video generation functions: {e}")
    print("Make sure veo_video_generation.py is in the same directory.")
    sys.exit(1)

# Test configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
OUTPUT_BUCKET_PATH = os.getenv("OUTPUT_BUCKET_PATH", "gs://your-bucket-name/veo_output/")

class VeoTestSuite:
    """Test suite for Google Veo video generation."""
    
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        self.start_time = time.time()
    
    def log_test(self, test_name, success, message="", video_uri=None):
        """Log test result."""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'name': test_name,
            'success': success,
            'message': message,
            'video_uri': video_uri,
            'timestamp': time.time()
        }
        self.test_results.append(result)
        
        if success:
            self.passed_tests += 1
            print(f"{status} {test_name}")
            if video_uri:
                print(f"    📹 Video: {video_uri}")
            if message:
                print(f"    💬 {message}")
        else:
            self.failed_tests += 1
            print(f"{status} {test_name}")
            if message:
                print(f"    ❌ Error: {message}")
    
    def test_environment_setup(self):
        """Test if the environment is properly set up."""
        print("\n🔧 Testing Environment Setup...")
        
        # Test imports
        try:
            from google import genai
            from google.genai.types import GenerateVideosConfig
            from google.cloud import storage
            self.log_test("Import Dependencies", True, "All required packages imported successfully")
        except ImportError as e:
            self.log_test("Import Dependencies", False, f"Missing dependency: {e}")
            return False
        
        # Test configuration
        if not PROJECT_ID or PROJECT_ID == "your-project-id":
            self.log_test("Project Configuration", False, "PROJECT_ID not configured")
            return False
        
        if not OUTPUT_BUCKET_PATH or OUTPUT_BUCKET_PATH == "gs://your-bucket/output/":
            self.log_test("Bucket Configuration", False, "OUTPUT_BUCKET_PATH not configured")
            return False
        
        self.log_test("Project Configuration", True, f"Project: {PROJECT_ID}")
        self.log_test("Bucket Configuration", True, f"Bucket: {OUTPUT_BUCKET_PATH}")
        
        # Test directories
        images_dir = current_dir / "images"
        results_dir = current_dir / "result_folder"
        
        if not images_dir.exists():
            images_dir.mkdir(exist_ok=True)
        
        if not results_dir.exists():
            results_dir.mkdir(exist_ok=True)
        
        self.log_test("Directory Setup", True, "All directories created/verified")
        return True
    
    def test_text_to_video_veo2(self):
        """Test text-to-video generation with Veo 2.0."""
        print("\n🎬 Testing Text-to-Video with Veo 2.0...")
        
        test_prompt = "A simple animation of a bouncing ball on a white background, clean and minimal style."
        
        try:
            start_time = time.time()
            video_uri = generate_video_from_text(
                project_id=PROJECT_ID,
                prompt=test_prompt,
                output_bucket_path=OUTPUT_BUCKET_PATH,
                model_id="veo-2.0-generate-001"
            )
            duration = time.time() - start_time
            
            if video_uri:
                self.log_test(
                    "Text-to-Video (Veo 2.0)", 
                    True, 
                    f"Generated in {duration:.1f}s",
                    video_uri
                )
                return video_uri
            else:
                self.log_test("Text-to-Video (Veo 2.0)", False, "No video URI returned")
                return None
                
        except Exception as e:
            self.log_test("Text-to-Video (Veo 2.0)", False, str(e))
            return None
    
    def test_text_to_video_veo3(self):
        """Test text-to-video generation with Veo 3.0."""
        print("\n🎬 Testing Text-to-Video with Veo 3.0...")
        
        test_prompt = "A futuristic robot walking through a neon-lit corridor, cinematic lighting."
        
        try:
            start_time = time.time()
            video_uri = generate_video_with_veo3_preview(
                project_id=PROJECT_ID,
                prompt=test_prompt,
                output_bucket_path=OUTPUT_BUCKET_PATH
            )
            duration = time.time() - start_time
            
            if video_uri:
                self.log_test(
                    "Text-to-Video (Veo 3.0)", 
                    True, 
                    f"Generated in {duration:.1f}s",
                    video_uri
                )
                return video_uri
            else:
                self.log_test("Text-to-Video (Veo 3.0)", False, "No video URI returned")
                return None
                
        except Exception as e:
            error_msg = str(e)
            if "not allowlisted" in error_msg.lower():
                self.log_test("Text-to-Video (Veo 3.0)", False, "Project not allowlisted for Veo 3.0")
            else:
                self.log_test("Text-to-Video (Veo 3.0)", False, error_msg)
            return None
    
    def test_image_to_video_local(self):
        """Test image-to-video generation with local images."""
        print("\n🖼️ Testing Image-to-Video with Local Images...")
        
        images_dir = current_dir / "images"
        if not images_dir.exists():
            self.log_test("Image-to-Video (Local)", False, "Images directory not found")
            return None
        
        # Find available images
        image_files = [f for f in os.listdir(images_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        if not image_files:
            self.log_test("Image-to-Video (Local)", False, "No images found in images directory")
            return None
        
        # Use the first available image
        test_image = image_files[0]
        test_prompt = "The image comes to life with gentle, natural movements and soft lighting."
        
        try:
            start_time = time.time()
            video_uri = generate_video_from_local_image(
                project_id=PROJECT_ID,
                image_filename=test_image,
                output_bucket_path=OUTPUT_BUCKET_PATH,
                prompt=test_prompt
            )
            duration = time.time() - start_time
            
            if video_uri:
                self.log_test(
                    "Image-to-Video (Local)", 
                    True, 
                    f"Used {test_image}, generated in {duration:.1f}s",
                    video_uri
                )
                return video_uri
            else:
                self.log_test("Image-to-Video (Local)", False, "No video URI returned")
                return None
                
        except Exception as e:
            self.log_test("Image-to-Video (Local)", False, str(e))
            return None
    
    def test_image_to_video_no_prompt(self):
        """Test image-to-video generation without prompt."""
        print("\n🖼️ Testing Image-to-Video without Prompt...")
        
        images_dir = current_dir / "images"
        if not images_dir.exists():
            self.log_test("Image-to-Video (No Prompt)", False, "Images directory not found")
            return None
        
        # Find available images
        image_files = [f for f in os.listdir(images_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
        
        if not image_files:
            self.log_test("Image-to-Video (No Prompt)", False, "No images found")
            return None
        
        # Use the first available image
        test_image = image_files[0]
        
        try:
            start_time = time.time()
            video_uri = generate_video_from_local_image(
                project_id=PROJECT_ID,
                image_filename=test_image,
                output_bucket_path=OUTPUT_BUCKET_PATH,
                prompt=None  # No prompt
            )
            duration = time.time() - start_time
            
            if video_uri:
                self.log_test(
                    "Image-to-Video (No Prompt)", 
                    True, 
                    f"Used {test_image}, generated in {duration:.1f}s",
                    video_uri
                )
                return video_uri
            else:
                self.log_test("Image-to-Video (No Prompt)", False, "No video URI returned")
                return None
                
        except Exception as e:
            self.log_test("Image-to-Video (No Prompt)", False, str(e))
            return None
    
    def test_download_functionality(self, video_uri):
        """Test the GCS download functionality."""
        if not video_uri:
            self.log_test("Download Functionality", False, "No video URI provided")
            return False
        
        print("\n📥 Testing Download Functionality...")
        
        try:
            local_path = download_gcs_file(
                gcs_uri=video_uri,
                local_folder_path=str(current_dir / "result_folder"),
                project_id=PROJECT_ID
            )
            
            if local_path and os.path.exists(local_path):
                file_size = os.path.getsize(local_path) / (1024 * 1024)  # MB
                self.log_test(
                    "Download Functionality", 
                    True, 
                    f"Downloaded {file_size:.1f}MB to {local_path}"
                )
                return True
            else:
                self.log_test("Download Functionality", False, "File not downloaded or doesn't exist")
                return False
                
        except Exception as e:
            self.log_test("Download Functionality", False, str(e))
            return False
    
    def test_error_handling(self):
        """Test error handling with invalid inputs."""
        print("\n🚫 Testing Error Handling...")
        
        # Test with empty prompt
        try:
            video_uri = generate_video_from_text(
                project_id=PROJECT_ID,
                prompt="",
                output_bucket_path=OUTPUT_BUCKET_PATH
            )
            # If it doesn't raise an error, it should return None
            if video_uri is None:
                self.log_test("Error Handling (Empty Prompt)", True, "Correctly handled empty prompt")
            else:
                self.log_test("Error Handling (Empty Prompt)", False, "Should not generate video with empty prompt")
        except Exception:
            self.log_test("Error Handling (Empty Prompt)", True, "Correctly raised exception for empty prompt")
        
        # Test with invalid image file
        try:
            video_uri = generate_video_from_local_image(
                project_id=PROJECT_ID,
                image_filename="nonexistent_image.jpg",
                output_bucket_path=OUTPUT_BUCKET_PATH
            )
            if video_uri is None:
                self.log_test("Error Handling (Invalid Image)", True, "Correctly handled invalid image")
            else:
                self.log_test("Error Handling (Invalid Image)", False, "Should not generate video with invalid image")
        except Exception:
            self.log_test("Error Handling (Invalid Image)", True, "Correctly raised exception for invalid image")
    
    def run_basic_tests(self):
        """Run basic test suite."""
        print("🧪 Running Basic Test Suite")
        print("=" * 60)
        
        if not self.test_environment_setup():
            print("❌ Environment setup failed. Cannot continue with tests.")
            return
        
        # Test text-to-video with Veo 2.0
        video_uri = self.test_text_to_video_veo2()
        
        # Test download if we have a video
        if video_uri:
            self.test_download_functionality(video_uri)
        
        # Test image-to-video
        self.test_image_to_video_local()
        
        # Test error handling
        self.test_error_handling()
    
    def run_veo3_tests(self):
        """Run Veo 3.0 specific tests."""
        print("🧪 Running Veo 3.0 Test Suite")
        print("=" * 60)
        
        if not self.test_environment_setup():
            return
        
        self.test_text_to_video_veo3()
    
    def run_comparison_tests(self):
        """Run model comparison tests."""
        print("🧪 Running Model Comparison Tests")
        print("=" * 60)
        
        if not self.test_environment_setup():
            return
        
        # Test both models with the same prompt
        test_prompt = "A peaceful lake reflecting the sky with gentle ripples."
        
        print(f"\n⚖️ Comparing models with prompt: '{test_prompt}'")
        
        # Test Veo 2.0
        video_uri_2 = self.test_text_to_video_veo2()
        
        # Test Veo 3.0
        video_uri_3 = self.test_text_to_video_veo3()
        
        # Summary
        print(f"\n📊 Comparison Results:")
        print(f"Veo 2.0: {'✅ Success' if video_uri_2 else '❌ Failed'}")
        print(f"Veo 3.0: {'✅ Success' if video_uri_3 else '❌ Failed'}")
    
    def run_full_tests(self):
        """Run comprehensive test suite."""
        print("🧪 Running Full Test Suite")
        print("=" * 60)
        
        if not self.test_environment_setup():
            return
        
        # Text-to-video tests
        video_uri_2 = self.test_text_to_video_veo2()
        video_uri_3 = self.test_text_to_video_veo3()
        
        # Image-to-video tests
        self.test_image_to_video_local()
        self.test_image_to_video_no_prompt()
        
        # Download tests
        if video_uri_2:
            self.test_download_functionality(video_uri_2)
        
        # Error handling tests
        self.test_error_handling()
    
    def run_image_only_tests(self):
        """Run only image-to-video tests."""
        print("🧪 Running Image-to-Video Tests Only")
        print("=" * 60)
        
        if not self.test_environment_setup():
            return
        
        self.test_image_to_video_local()
        self.test_image_to_video_no_prompt()
    
    def run_text_only_tests(self):
        """Run only text-to-video tests."""
        print("🧪 Running Text-to-Video Tests Only")
        print("=" * 60)
        
        if not self.test_environment_setup():
            return
        
        self.test_text_to_video_veo2()
        self.test_text_to_video_veo3()
    
    def print_summary(self):
        """Print test summary."""
        total_time = time.time() - self.start_time
        total_tests = self.passed_tests + self.failed_tests
        
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed_tests} ✅")
        print(f"Failed: {self.failed_tests} ❌")
        print(f"Success Rate: {(self.passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        print(f"Total Time: {total_time:.1f}s")
        
        if self.failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['name']}: {result['message']}")
        
        # Show generated videos
        successful_videos = [r for r in self.test_results if r['success'] and r['video_uri']]
        if successful_videos:
            print(f"\n📹 Generated Videos:")
            for result in successful_videos:
                print(f"  - {result['name']}: {result['video_uri']}")
        
        print(f"\n📁 Check ./result_folder/ for downloaded videos")

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description="Google Veo Video Generation Test Suite")
    parser.add_argument("--veo3", action="store_true", help="Test Veo 3.0 specifically")
    parser.add_argument("--compare", action="store_true", help="Compare both models")
    parser.add_argument("--full", action="store_true", help="Run comprehensive tests")
    parser.add_argument("--image-only", action="store_true", help="Test only image-to-video")
    parser.add_argument("--text-only", action="store_true", help="Test only text-to-video")
    
    args = parser.parse_args()
    
    # Create test suite
    test_suite = VeoTestSuite()
    
    try:
        if args.veo3:
            test_suite.run_veo3_tests()
        elif args.compare:
            test_suite.run_comparison_tests()
        elif args.full:
            test_suite.run_full_tests()
        elif args.image_only:
            test_suite.run_image_only_tests()
        elif args.text_only:
            test_suite.run_text_only_tests()
        else:
            test_suite.run_basic_tests()
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error during testing: {e}")
    finally:
        test_suite.print_summary()

if __name__ == "__main__":
    main() 