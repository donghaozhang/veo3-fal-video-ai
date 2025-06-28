# Video Tools

A collection of Python scripts for video processing and manipulation using FFmpeg.

## 📁 Directory Structure

```
video_tools/
├── video_audio_utils.py    # Main utility script
├── README.md               # This documentation
├── .gitignore             # Git ignore rules
├── samples/               # Original sample videos/audio (tracked in git)
│   └── sample_video.mp4   # Main sample video for testing
├── processed/             # Manual processing outputs (ignored by git)
└── test_output/           # Test-generated files (ignored by git)
    ├── sample_video_first_1s.mp4
    ├── sample_video_first_3s.mp4
    ├── sample_video_first_5s.mp4
    ├── sample_video_audio.mp3
    └── ... (other test outputs)
```

**Organization Notes:**
- `samples/` - Contains original input files that serve as test samples
- `processed/` - For manually processed outputs and production files  
- `test_output/` - Auto-generated test files (ignored by git to keep repo clean)

## 📁 Scripts

### `video_audio_utils.py`
Comprehensive video and audio manipulation utility supporting multiple operations:

#### **Video Cutting**
Extracts the first N seconds from video files in the current directory.

**Features:**
- ✂️ **Video Cutting**: Extract first N seconds from videos
- 🎵 **Audio Addition**: Add audio to silent videos
- 🔄 **Audio Replacement**: Replace existing audio in videos
- 🎵 **Audio Extraction**: Extract audio tracks from videos
- 🎛️ **Audio Mixing**: Mix multiple audio files together and add to videos
- 🔗 **Audio Concatenation**: Join multiple audio files in sequence and add to videos
- 🎬 Automatically finds all video/audio files in current directory
- ⚡ Fast processing using FFmpeg stream copy when possible
- 📊 Progress tracking and detailed output information
- 🛡️ Safe processing with existing file checks

**Usage:**
```bash
# Navigate to video_tools directory
cd video_tools

# Video cutting - extract first N seconds
python video_audio_utils.py cut 5          # Extract first 5 seconds
python video_audio_utils.py cut 10         # Extract first 10 seconds

# Audio operations  
python video_audio_utils.py add-audio      # Add audio to silent videos
python video_audio_utils.py replace-audio  # Replace existing audio
python video_audio_utils.py extract-audio  # Extract audio from videos

# Advanced audio operations (NEW!)
python video_audio_utils.py mix-audio      # Mix multiple audio files and add to videos
python video_audio_utils.py concat-audio   # Concatenate multiple audio files and add to videos

# Or process files in any other directory
cd /path/to/your/videos
python /path/to/video_tools/video_audio_utils.py [command]
```

**Supported Video Formats:**
- `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.flv`, `.wmv`

**Supported Audio Formats:**
- `.mp3`, `.wav`, `.aac`, `.ogg`, `.m4a`, `.flac`

## 🎛️ Advanced Audio Features

### **Audio Mixing**
Combines multiple audio files by layering them together (playing simultaneously):
- Automatically normalizes volume levels to prevent distortion
- Creates a single mixed audio track from multiple sources
- Perfect for adding background music, sound effects, etc.
- Interactive selection: choose specific files or mix all available audio

### **Audio Concatenation** 
Joins multiple audio files in sequence (playing one after another):
- Maintains original audio quality and timing
- Creates a single continuous audio track
- Perfect for creating playlists, joining speech segments, etc.
- Interactive selection with custom ordering

**Example Workflow:**
```bash
# Mix 3 audio files and add to all videos
python video_audio_utils.py mix-audio
# → Select files: music.mp3, effects.wav, voice.mp3
# → Creates: mixed_audio.mp3 
# → Applies to: video1_mixed_audio.mp4, video2_mixed_audio.mp4

# Concatenate audio files in sequence and add to videos  
python video_audio_utils.py concat-audio
# → Select files: intro.mp3, main.mp3, outro.mp3
# → Creates: concatenated_audio.mp3
# → Applies to: video1_concat_audio.mp4, video2_concat_audio.mp4
```

**Requirements:**
- Python 3.6+
- FFmpeg installed and in PATH
- For mixing/concatenation: at least 2 audio files

**Example Output:**
```
🎬 Video Cutting:
Original: video.mp4 (7.5 MB, 110.4 seconds)
Output:   video_first_5s.mp4 (0.4 MB, 5 seconds)

🎵 Audio Mixing:
Selected: music.mp3, effects.wav, voice.mp3
Mixed:    mixed_audio.mp3 (all tracks layered)
Applied:  video_mixed_audio.mp4
```

## 🔧 Requirements

### FFmpeg Installation

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract and add to PATH
3. Or use: `winget install FFmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
```

## 📝 Usage Tips

1. **Always backup original videos** before processing
2. **Test on a single file first** before batch processing
3. **Check available disk space** for output files
4. **Use stream copy** (`-c copy`) when possible for faster processing
5. **Monitor file sizes** to ensure expected results

## 🎯 Future Tools

Planned additions to this toolkit:
- Video trimming by time range
- Video format conversion
- Video compression/quality adjustment
- Audio extraction from videos
- Video concatenation
- Batch video processing
- Video metadata extraction

## 📊 Performance Notes

- **Stream Copy**: Fastest method, preserves quality, limited editing options
- **Re-encoding**: Slower but allows format changes and quality adjustments
- **File Sizes**: Typically 5-second clips are 5-10% of original file size

## 🚨 Important Notes

- Scripts use FFmpeg's stream copy by default for speed
- Output files will overwrite existing files with same name
- Some video formats may require re-encoding for certain operations
- Always verify output quality matches expectations 