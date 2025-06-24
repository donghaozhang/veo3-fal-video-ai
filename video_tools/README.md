# Video Tools

A collection of Python scripts for video processing and manipulation using FFmpeg.

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
# Navigate to folder with videos
cd /path/to/videos

# Run the script
python /path/to/video_tools/cut_video_first_5_seconds.py
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