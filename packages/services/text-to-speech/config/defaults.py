"""
Default Configuration Settings

Default values and settings for the text-to-speech package.
"""

try:
    from ..models.common import VoiceSettings, AudioFormat, ElevenLabsModel
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models.common import VoiceSettings, AudioFormat, ElevenLabsModel


# Default voice settings
DEFAULT_VOICE_SETTINGS = VoiceSettings(
    stability=0.5,
    similarity_boost=0.5,
    style=0.3,
    use_speaker_boost=True
)

# Default audio format
DEFAULT_AUDIO_FORMAT = AudioFormat.MP3

# Default model
DEFAULT_MODEL = ElevenLabsModel.TURBO_V2_5

# Default API settings
DEFAULT_API_BASE_URL = "https://api.elevenlabs.io/v1"
DEFAULT_REQUEST_TIMEOUT = 60
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1.0

# Default output settings
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_OUTPUT_FORMAT = "mp3"

# Default text processing settings
DEFAULT_MAX_TEXT_LENGTH = 40000
DEFAULT_SPEED_RANGE = (0.25, 4.0)
DEFAULT_PAUSE_DURATION = 0.5

# Default voice cloning settings
DEFAULT_VOICE_CLONE_DESCRIPTION = "A clear, natural speaking voice"
DEFAULT_VOICE_CLONE_LABELS = ["english", "american", "male", "middle_aged"]

# File validation settings
ALLOWED_AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
MAX_FILE_SIZE_MB = 100

# API rate limiting
DEFAULT_RATE_LIMIT_REQUESTS = 50
DEFAULT_RATE_LIMIT_WINDOW = 60  # seconds

# Pipeline settings
DEFAULT_CONTENT_TYPES = ["conversation", "presentation", "interview", "story"]
DEFAULT_VOICE_STYLES = ["professional", "casual", "dramatic", "authoritative", "conversational"]

# Environment variable names
ENV_API_KEY = "ELEVENLABS_API_KEY"
ENV_OPENROUTER_KEY = "OPENROUTER_API_KEY"