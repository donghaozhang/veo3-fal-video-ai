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

### `cut_video_first_5_seconds.py`
Extracts the first 5 seconds from video files in the current directory.

**Features:**
- 🎬 Automatically finds all video files in current directory
- ⏱️ Extracts first 5 seconds from each video
- 📁 Creates output with `_first_5s` suffix
- 🔍 Checks video duration before processing
- ⚡ Fast processing using stream copy (no re-encoding)
- 📊 Shows file size comparison and processing summary

**Usage:**
```bash
# Navigate to video_tools directory
cd video_tools

# Process files in samples/ directory
python video_audio_utils.py cut 5

# Or process files in any other directory
cd /path/to/your/videos
python /path/to/video_tools/video_audio_utils.py cut 5
```

**Supported Formats:**
- `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.flv`, `.wmv`

**Requirements:**
- Python 3.6+
- FFmpeg installed and in PATH

**Example Output:**
```
Original: video.mp4 (7.5 MB, 110.4 seconds)
Output:   video_first_5s.mp4 (0.4 MB, 5 seconds)
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