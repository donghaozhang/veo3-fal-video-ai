"""
Media processing controller for video and audio operations.

Consolidates commands for video cutting, audio manipulation, and media processing tasks.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional

from .base_controller import BaseController
from .enhanced_video_processor import VideoProcessor
from .enhanced_audio_processor import AudioProcessor
from .file_utils import find_video_files, find_audio_files
from .interactive import interactive_audio_selection, interactive_multiple_audio_selection


class MediaProcessingController(BaseController):
    """Controller for media processing operations."""
    
    def __init__(self, input_dir: str = 'input', output_dir: str = 'output', 
                 verbose: bool = True):
        """Initialize the media processing controller.
        
        Args:
            input_dir: Directory containing input files
            output_dir: Directory for output files
            verbose: Whether to print operation details
        """
        super().__init__(input_dir, output_dir, verbose)
        self.video_processor = VideoProcessor(verbose=verbose)
        self.audio_processor = AudioProcessor(verbose=verbose)
    
    def validate_dependencies(self) -> Dict[str, bool]:
        """Validate required dependencies for media processing.
        
        Returns:
            Dictionary mapping dependency names to availability status
        """
        video_deps = self.video_processor.check_dependencies()
        audio_deps = self.audio_processor.check_dependencies()
        
        # Combine dependencies
        deps = {}
        deps.update(video_deps)
        deps.update(audio_deps)
        
        return deps
    
    def run(self) -> bool:
        """Run the media processing controller (interactive menu).
        
        Returns:
            True if successful, False otherwise
        """
        if not self.setup_directories():
            return False
        
        # Check dependencies
        deps = self.validate_dependencies()
        if not self.print_dependency_status(deps):
            return False
        
        # Show menu
        return self._show_menu()
    
    def _show_menu(self) -> bool:
        """Show interactive menu for media processing options."""
        options = {
            '1': 'Cut videos to duration',
            '2': 'Add audio to silent videos',
            '3': 'Replace audio in videos',
            '4': 'Extract audio from videos',
            '5': 'Mix multiple audio files',
            '6': 'Concatenate audio files',
            '7': 'Resize videos',
            '8': 'Convert video formats',
            '9': 'Extract video thumbnails',
            '10': 'Batch process videos',
            'q': 'Quit'
        }
        
        choice = self.get_user_choice("🎬 Select media processing operation:", options)
        
        if choice == '1':
            return self.cmd_cut_videos()
        elif choice == '2':
            return self.cmd_add_audio()
        elif choice == '3':
            return self.cmd_replace_audio()
        elif choice == '4':
            return self.cmd_extract_audio()
        elif choice == '5':
            return self.cmd_mix_audio()
        elif choice == '6':
            return self.cmd_concat_audio()
        elif choice == '7':
            return self.cmd_resize_videos()
        elif choice == '8':
            return self.cmd_convert_videos()
        elif choice == '9':
            return self.cmd_extract_thumbnails()
        elif choice == '10':
            return self.cmd_batch_process()
        elif choice == 'q':
            return True
        else:
            if self.verbose:
                print("❌ Invalid choice")
            return False
    
    def cmd_cut_videos(self) -> bool:
        """Cut first N seconds from all videos."""
        self.print_header("✂️  VIDEO CUTTER - Duration Extractor")
        
        if not self.setup_directories():
            return False
        
        video_files = find_video_files(self.input_dir)
        if not video_files:
            if self.verbose:
                print("📁 No video files found in input folder")
            return False
        
        self.print_file_info(video_files, "video file")
        
        # Get duration
        duration_str = self.get_user_input("⏱️  Duration to extract (seconds)", "3")
        try:
            duration = int(duration_str)
        except ValueError:
            if self.verbose:
                print("❌ Invalid duration")
            return False
        
        if duration <= 0:
            if self.verbose:
                print("❌ Duration must be positive")
            return False
        
        # Get start time
        start_time_str = self.get_user_input("⏱️  Start time (seconds)", "0")
        try:
            start_time = int(start_time_str)
        except ValueError:
            start_time = 0
        
        successful = 0
        failed = 0
        
        for i, video_path in enumerate(video_files, 1):
            self.show_progress(i, len(video_files), "video")
            
            # Check video info
            info = self.video_processor.get_video_info(video_path)
            if info['duration'] is None:
                if self.verbose:
                    print(f"⚠️  Warning: Could not determine duration of {video_path.name}")
            elif info['duration'] < duration + start_time:
                if self.verbose:
                    print(f"⚠️  Warning: Video is only {info['duration']:.1f}s long")
            
            # Create output filename
            output_path = self.output_dir / f"{video_path.stem}_cut_{duration}s{video_path.suffix}"
            
            if self.check_skip_existing(output_path):
                continue
            
            # Cut the video
            if self.video_processor.cut_duration(video_path, output_path, duration, start_time):
                successful += 1
                
                # Show file sizes
                if self.verbose:
                    input_size = video_path.stat().st_size / (1024 * 1024)  # MB
                    output_size = output_path.stat().st_size / (1024 * 1024)  # MB
                    print(f"📊 Input: {input_size:.1f} MB → Output: {output_size:.1f} MB")
            else:
                failed += 1
        
        self.show_summary(successful, failed, len(video_files))
        return successful > 0
    
    def cmd_add_audio(self) -> bool:
        """Add audio to silent videos."""
        self.print_header("🎵 ADD AUDIO TO SILENT VIDEOS")
        
        if not self.setup_directories():
            return False
        
        video_files = find_video_files(self.input_dir)
        audio_files = find_audio_files(self.input_dir)
        
        if not video_files:
            if self.verbose:
                print("📁 No video files found in input folder")
            return False
        
        if not audio_files:
            if self.verbose:
                print("📁 No audio files found in input folder")
                print("💡 Add some audio files (.mp3, .wav, .aac, etc.) to the input folder")
            return False
        
        # Find silent videos
        silent_videos = []
        for video in video_files:
            info = self.video_processor.get_video_info(video)
            if not info['has_audio']:
                silent_videos.append(video)
        
        if not silent_videos:
            if self.verbose:
                print("📹 No silent videos found")
                print("💡 All videos already have audio. Use 'replace-audio' to replace existing audio")
            return False
        
        self.print_file_info(silent_videos, "silent video")
        
        # Select audio file
        if self.verbose:
            selected_audio = interactive_audio_selection(audio_files)
        else:
            selected_audio = audio_files[0]  # Use first audio file in non-verbose mode
        
        if not selected_audio:
            return False
        
        if self.verbose:
            print(f"\n🎵 Using audio: {selected_audio.name}")
        
        successful = 0
        failed = 0
        
        for i, video_path in enumerate(silent_videos, 1):
            self.show_progress(i, len(silent_videos), "video")
            
            # Create output filename
            output_path = self.output_dir / f"{video_path.stem}_with_audio{video_path.suffix}"
            
            if self.check_skip_existing(output_path):
                continue
            
            # Add audio to video
            if self.audio_processor.add_to_video(video_path, selected_audio, output_path, 
                                               replace_audio=False):
                successful += 1
            else:
                failed += 1
        
        self.show_summary(successful, failed, len(silent_videos))
        return successful > 0
    
    def cmd_replace_audio(self) -> bool:
        """Replace audio in videos."""
        self.print_header("🔄 REPLACE AUDIO IN VIDEOS")
        
        if not self.setup_directories():
            return False
        
        video_files = find_video_files(self.input_dir)
        audio_files = find_audio_files(self.input_dir)
        
        if not video_files:
            if self.verbose:
                print("📁 No video files found in input folder")
            return False
        
        if not audio_files:
            if self.verbose:
                print("📁 No audio files found in input folder")
            return False
        
        self.print_file_info(video_files, "video file")
        
        # Select audio file
        if self.verbose:
            selected_audio = interactive_audio_selection(audio_files)
        else:
            selected_audio = audio_files[0]
        
        if not selected_audio:
            return False
        
        successful = 0
        failed = 0
        
        for i, video_path in enumerate(video_files, 1):
            self.show_progress(i, len(video_files), "video")
            
            output_path = self.output_dir / f"{video_path.stem}_new_audio{video_path.suffix}"
            
            if self.check_skip_existing(output_path):
                continue
            
            if self.audio_processor.add_to_video(video_path, selected_audio, output_path, 
                                               replace_audio=True):
                successful += 1
            else:
                failed += 1
        
        self.show_summary(successful, failed, len(video_files))
        return successful > 0
    
    def cmd_extract_audio(self) -> bool:
        """Extract audio from videos."""
        self.print_header("🎵 EXTRACT AUDIO FROM VIDEOS")
        
        if not self.setup_directories():
            return False
        
        video_files = find_video_files(self.input_dir)
        
        if not video_files:
            if self.verbose:
                print("📁 No video files found in input folder")
            return False
        
        # Filter videos with audio
        videos_with_audio = []
        for video in video_files:
            info = self.video_processor.get_video_info(video)
            if info['has_audio']:
                videos_with_audio.append(video)
        
        if not videos_with_audio:
            if self.verbose:
                print("📹 No videos with audio found")
            return False
        
        self.print_file_info(videos_with_audio, "video with audio")
        
        # Get audio format
        audio_format = self.get_user_input("🎵 Audio format (mp3/wav/aac)", "mp3")
        quality = self.get_user_input("🎵 Audio quality (192k/256k/320k)", "192k")
        
        successful = 0
        failed = 0
        
        for i, video_path in enumerate(videos_with_audio, 1):
            self.show_progress(i, len(videos_with_audio), "video")
            
            output_path = self.output_dir / f"{video_path.stem}_audio.{audio_format}"
            
            if self.check_skip_existing(output_path):
                continue
            
            if self.audio_processor.extract_from_video(video_path, output_path, 
                                                     audio_format, quality):
                successful += 1
            else:
                failed += 1
        
        self.show_summary(successful, failed, len(videos_with_audio))
        return successful > 0
    
    def cmd_mix_audio(self) -> bool:
        """Mix multiple audio files together."""
        self.print_header("🎵 MIX MULTIPLE AUDIO FILES")
        
        if not self.setup_directories():
            return False
        
        audio_files = find_audio_files(self.input_dir)
        
        if len(audio_files) < 2:
            if self.verbose:
                print("📁 Need at least 2 audio files to mix")
            return False
        
        self.print_file_info(audio_files, "audio file")
        
        # Select audio files to mix
        if self.verbose:
            selected_files = interactive_multiple_audio_selection(audio_files)
        else:
            selected_files = audio_files[:2]  # Use first 2 files in non-verbose mode
        
        if len(selected_files) < 2:
            if self.verbose:
                print("❌ Need at least 2 files to mix")
            return False
        
        # Get mixing options
        normalize = self.get_yes_no("🔊 Normalize volume levels?", True)
        method = self.get_user_choice("🎵 Mixing method:", 
                                    {'1': 'Overlay (blend)', '2': 'Sum (add)'}, '1')
        method_name = 'overlay' if method == '1' else 'sum'
        
        output_path = self.output_dir / "mixed_audio.mp3"
        
        if self.audio_processor.mix_files(selected_files, output_path, normalize, method_name):
            if self.verbose:
                print("✅ Audio mixing completed successfully")
            return True
        else:
            if self.verbose:
                print("❌ Audio mixing failed")
            return False
    
    def cmd_concat_audio(self) -> bool:
        """Concatenate multiple audio files in sequence."""
        self.print_header("🎵 CONCATENATE AUDIO FILES")
        
        if not self.setup_directories():
            return False
        
        audio_files = find_audio_files(self.input_dir)
        
        if len(audio_files) < 2:
            if self.verbose:
                print("📁 Need at least 2 audio files to concatenate")
            return False
        
        self.print_file_info(audio_files, "audio file")
        
        # Select audio files to concatenate
        if self.verbose:
            selected_files = interactive_multiple_audio_selection(audio_files)
        else:
            selected_files = audio_files
        
        if len(selected_files) < 2:
            if self.verbose:
                print("❌ Need at least 2 files to concatenate")
            return False
        
        # Get crossfade option
        crossfade = self.get_yes_no("🎵 Add crossfade between files?", False)
        crossfade_duration = 0.0
        
        if crossfade:
            duration_str = self.get_user_input("⏱️  Crossfade duration (seconds)", "1.0")
            try:
                crossfade_duration = float(duration_str)
            except ValueError:
                crossfade_duration = 1.0
        
        output_path = self.output_dir / "concatenated_audio.mp3"
        
        if self.audio_processor.concatenate_files(selected_files, output_path, crossfade_duration):
            if self.verbose:
                print("✅ Audio concatenation completed successfully")
            return True
        else:
            if self.verbose:
                print("❌ Audio concatenation failed")
            return False
    
    def cmd_resize_videos(self) -> bool:
        """Resize videos to specified dimensions."""
        self.print_header("📐 RESIZE VIDEOS")
        
        if not self.setup_directories():
            return False
        
        video_files = find_video_files(self.input_dir)
        if not video_files:
            if self.verbose:
                print("📁 No video files found")
            return False
        
        # Get target dimensions
        width_str = self.get_user_input("📐 Target width (pixels)", "1920")
        height_str = self.get_user_input("📐 Target height (pixels)", "1080")
        
        try:
            width = int(width_str)
            height = int(height_str)
        except ValueError:
            if self.verbose:
                print("❌ Invalid dimensions")
            return False
        
        maintain_aspect = self.get_yes_no("📐 Maintain aspect ratio?", True)
        
        successful = 0
        failed = 0
        
        for i, video_path in enumerate(video_files, 1):
            self.show_progress(i, len(video_files), "video")
            
            output_path = self.output_dir / f"{video_path.stem}_resized{video_path.suffix}"
            
            if self.check_skip_existing(output_path):
                continue
            
            if self.video_processor.resize_video(video_path, output_path, 
                                               width, height, maintain_aspect):
                successful += 1
            else:
                failed += 1
        
        self.show_summary(successful, failed, len(video_files))
        return successful > 0
    
    def cmd_convert_videos(self) -> bool:
        """Convert videos to different format."""
        self.print_header("🔄 CONVERT VIDEO FORMATS")
        
        if not self.setup_directories():
            return False
        
        video_files = find_video_files(self.input_dir)
        if not video_files:
            if self.verbose:
                print("📁 No video files found")
            return False
        
        # Get target codec
        codec_options = {
            '1': 'libx264 (H.264)',
            '2': 'libx265 (H.265/HEVC)',
            '3': 'libvpx-vp9 (VP9)',
            '4': 'copy (no re-encoding)'
        }
        
        codec_choice = self.get_user_choice("🔄 Select target codec:", codec_options, '1')
        codec_map = {
            '1': 'libx264',
            '2': 'libx265', 
            '3': 'libvpx-vp9',
            '4': 'copy'
        }
        
        target_codec = codec_map.get(codec_choice, 'libx264')
        
        successful = 0
        failed = 0
        
        for i, video_path in enumerate(video_files, 1):
            self.show_progress(i, len(video_files), "video")
            
            output_path = self.output_dir / f"{video_path.stem}_converted.mp4"
            
            if self.check_skip_existing(output_path):
                continue
            
            if self.video_processor.convert_format(video_path, output_path, target_codec):
                successful += 1
            else:
                failed += 1
        
        self.show_summary(successful, failed, len(video_files))
        return successful > 0
    
    def cmd_extract_thumbnails(self) -> bool:
        """Extract thumbnails from videos."""
        self.print_header("📸 EXTRACT VIDEO THUMBNAILS")
        
        if not self.setup_directories():
            return False
        
        video_files = find_video_files(self.input_dir)
        if not video_files:
            if self.verbose:
                print("📁 No video files found")
            return False
        
        # Get timestamp
        timestamp = self.get_user_input("⏱️  Timestamp for thumbnail (HH:MM:SS)", "00:00:01")
        
        successful = 0
        failed = 0
        
        for i, video_path in enumerate(video_files, 1):
            self.show_progress(i, len(video_files), "video")
            
            output_path = self.output_dir / f"{video_path.stem}_thumbnail.jpg"
            
            if self.check_skip_existing(output_path):
                continue
            
            if self.video_processor.get_thumbnail(video_path, output_path, timestamp):
                successful += 1
            else:
                failed += 1
        
        self.show_summary(successful, failed, len(video_files))
        return successful > 0
    
    def cmd_batch_process(self) -> bool:
        """Batch process videos with multiple operations."""
        self.print_header("⚡ BATCH PROCESS VIDEOS")
        
        if not self.setup_directories():
            return False
        
        video_files = find_video_files(self.input_dir)
        if not video_files:
            if self.verbose:
                print("📁 No video files found")
            return False
        
        batch_options = {
            '1': 'Cut duration from all videos',
            '2': 'Resize all videos',
            '3': 'Convert all videos',
            '4': 'Extract thumbnails from all'
        }
        
        operation_choice = self.get_user_choice("⚡ Select batch operation:", batch_options)
        
        if operation_choice == '1':
            duration = int(self.get_user_input("⏱️  Duration (seconds)", "5"))
            results = self.video_processor.batch_process(
                self.input_dir, self.output_dir, 'cut_duration', duration=duration)
        elif operation_choice == '2':
            width = int(self.get_user_input("📐 Width", "1920"))
            height = int(self.get_user_input("📐 Height", "1080"))
            results = self.video_processor.batch_process(
                self.input_dir, self.output_dir, 'resize', width=width, height=height)
        elif operation_choice == '3':
            codec = self.get_user_input("🔄 Codec", "libx264")
            results = self.video_processor.batch_process(
                self.input_dir, self.output_dir, 'convert', target_codec=codec)
        elif operation_choice == '4':
            timestamp = self.get_user_input("⏱️  Timestamp", "00:00:01")
            results = self.video_processor.batch_process(
                self.input_dir, self.output_dir, 'thumbnail', timestamp=timestamp)
        else:
            if self.verbose:
                print("❌ Invalid choice")
            return False
        
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        self.show_summary(successful, failed, len(results))
        
        # Save batch results
        self.save_results(results, "batch_processing_results.json")
        
        return successful > 0