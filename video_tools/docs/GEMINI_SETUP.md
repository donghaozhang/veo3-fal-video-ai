# Google Gemini Video Understanding Setup

This guide shows how to configure Google Gemini AI for video analysis in video_tools.

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install google-generativeai
```

### 2. Get API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 3. Set Environment Variable
```bash
# Linux/macOS
export GEMINI_API_KEY="your_api_key_here"

# Windows
set GEMINI_API_KEY=your_api_key_here

# Or add to .env file
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

### 4. Test Setup
```bash
python video_audio_utils.py analyze-videos
```

## 🎯 Features

### Video Analysis Commands
- `analyze-videos` - Full AI analysis with multiple options
- `transcribe-videos` - Quick audio transcription
- `describe-videos` - Video description and summarization

### Analysis Types
1. **Video Description** - Summary and visual analysis
2. **Audio Transcription** - Speech-to-text with timestamps
3. **Scene Analysis** - Timeline breakdown and key moments
4. **Key Information Extraction** - Facts, people, locations
5. **Custom Q&A** - Ask specific questions about content

## 📋 Requirements

### Supported Video Formats
- MP4, MOV, AVI, WebM, MKV, FLV, WMV, 3GPP

### File Size Limits
- **Inline upload**: Up to 20MB
- **File API**: Larger files (recommended)
- **Max duration**: 2 hours

### API Quotas
- **Free tier**: 8 hours of video per day
- **Paid tier**: No length limit
- Processing: ~1 frame per second
- Token usage: ~300 tokens per second of video

## 💡 Usage Examples

### Basic Description
```bash
python video_audio_utils.py describe-videos
```

### Detailed Transcription
```bash
python video_audio_utils.py transcribe-videos
```

### Custom Analysis
```bash
python video_audio_utils.py analyze-videos
# Choose option 5 for Q&A
# Enter questions like:
# "What is the main topic?"
# "Who are the speakers?"
# "What are the key points?"
```

## 🗂️ Output Files

Analysis results are saved as:
- `video_name_description.json` - Structured analysis data
- `video_name_description.txt` - Human-readable text
- `video_name_transcription.json` - Full transcription data
- `video_name_transcription.txt` - Clean transcript

## 🔧 Troubleshooting

### Import Error
```
ImportError: No module named 'google.generativeai'
```
**Solution**: `pip install google-generativeai`

### API Key Error
```
ValueError: Gemini API key required
```
**Solution**: Set `GEMINI_API_KEY` environment variable

### Upload Failed
```
Upload failed: File too large
```
**Solution**: Use smaller files or ensure good internet connection

### Processing Failed
```
Video processing failed
```
**Solution**: Check video format and try a different file

## 🌐 Getting Help

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs/video-understanding)
- [Google AI Studio](https://aistudio.google.com/)
- [API Key Management](https://aistudio.google.com/app/apikey)

## 🔐 Security Notes

- Never commit API keys to version control
- Use environment variables or .env files
- Keep API keys secure and rotate regularly
- Monitor usage in Google AI Studio