#!/usr/bin/env python3
"""
TTS CLI Wrapper for AI Pipeline Integration

Simplified interface specifically designed for integration with AI content pipelines.
Provides JSON output and standardized return codes for automation.

Usage:
    python tts_cli_wrapper.py "Hello world" rachel output.mp3
    python tts_cli_wrapper.py "Text" voice_name output_file --speed 1.2 --json
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Force SimpleTTS implementation for reliability
from examples.simple_tts import SimpleTTS
USE_BASIC_USAGE = False


def tts_pipeline_generate(text, voice_name="rachel", output_file=None, **kwargs):
    """
    Generate speech optimized for pipeline integration
    
    Args:
        text (str): Text to convert to speech
        voice_name (str): Voice name
        output_file (str): Output file path
        **kwargs: Additional parameters
    
    Returns:
        dict: Result with status, output_file, and metadata
    """
    try:
        # Validate inputs
        if not text or not text.strip():
            return {
                "success": False,
                "error": "Empty text provided",
                "output_file": None
            }
        
        if USE_BASIC_USAGE:
            if not validate_voice(voice_name):
                return {
                    "success": False,
                    "error": f"Invalid voice: {voice_name}. Available: {list_available_voices()}",
                    "output_file": None
            }
        
        # Auto-generate output file if not provided
        if not output_file:
            import time
            timestamp = int(time.time())
            output_file = f"output/pipeline_tts_{timestamp}.mp3"
        elif not output_file.startswith(('output/', '/')):
            # Ensure files go to output folder unless absolute path is specified
            output_file = f"output/{output_file}"
        
        # Initialize TTS
        if USE_BASIC_USAGE:
            tts = TTSBasicUsage()
            # Generate speech
            result_file = tts.generate_speech(
                text=text,
                voice_name=voice_name,
                output_file=output_file,
                **kwargs
            )
            
            if result_file:
                return {
                    "success": True,
                    "output_file": result_file,
                    "voice_used": voice_name,
                    "text_length": len(text),
                    "settings": kwargs
                }
            else:
                return {
                    "success": False,
                    "error": "Speech generation failed",
                    "output_file": None
                }
        else:
            # Use SimpleTTS fallback
            tts = SimpleTTS()
            result = tts.generate_speech(
                text=text,
                voice_name=voice_name,
                output_file=output_file,
                **kwargs
            )
            return result
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output_file": None
        }


def main():
    """Main function for CLI wrapper"""
    parser = argparse.ArgumentParser(
        description="TTS CLI Wrapper for AI Pipeline Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Hello world" rachel output.mp3
  %(prog)s "Test speech" drew custom.mp3 --speed 1.2 --json
  %(prog)s "Sample text" bella --json
        """
    )
    
    # Positional arguments (optional for utility commands)
    parser.add_argument("text", nargs="?", help="Text to convert to speech")
    parser.add_argument("voice", nargs="?", default="rachel", help="Voice name (default: rachel)")
    parser.add_argument("output", nargs="?", help="Output file path (optional)")
    
    # Optional parameters
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (0.7-1.2)")
    parser.add_argument("--stability", type=float, default=0.5, help="Voice stability (0.0-1.0)")
    parser.add_argument("--similarity-boost", type=float, default=0.8, help="Similarity boost (0.0-1.0)")
    parser.add_argument("--style", type=float, default=0.2, help="Style exaggeration (0.0-1.0)")
    
    # Output options
    parser.add_argument("--json", action="store_true", help="Output JSON result")
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose output")
    
    # Utility options
    parser.add_argument("--list-voices", action="store_true", help="List available voices and exit")
    parser.add_argument("--validate-voice", help="Validate a voice name and exit")
    
    args = parser.parse_args()
    
    try:
        # Handle utility commands
        if args.list_voices:
            if USE_BASIC_USAGE:
                voices = list_available_voices()
            else:
                # Fallback to SimpleTTS voice list
                tts = SimpleTTS()
                voices = list(tts.voice_map.keys())
            
            if args.json:
                print(json.dumps({"voices": voices}))
            else:
                print("Available voices:")
                for voice in voices:
                    print(f"  - {voice}")
            return 0
        
        if args.validate_voice:
            if USE_BASIC_USAGE:
                is_valid = validate_voice(args.validate_voice)
            else:
                # Fallback to SimpleTTS voice validation
                tts = SimpleTTS()
                is_valid = args.validate_voice.lower() in tts.voice_map
            
            if args.json:
                print(json.dumps({"voice": args.validate_voice, "valid": is_valid}))
            else:
                print(f"Voice '{args.validate_voice}' is {'valid' if is_valid else 'invalid'}")
            return 0 if is_valid else 1
        
        # Check if text is provided for generation
        if not args.text:
            error_msg = "Text is required for speech generation"
            if args.json:
                print(json.dumps({"success": False, "error": error_msg}))
            else:
                print(f"❌ {error_msg}")
                print("Use --help for usage information")
            return 1
        
        # Main generation
        if not args.quiet and not args.json:
            print("🎤 TTS Pipeline Wrapper")
            print("=" * 25)
        
        # Validate parameters
        if not 0.7 <= args.speed <= 1.2:
            error_msg = "Speed must be between 0.7 and 1.2"
            if args.json:
                print(json.dumps({"success": False, "error": error_msg}))
            else:
                print(f"❌ {error_msg}")
            return 1
        
        # Generate speech
        result = tts_pipeline_generate(
            text=args.text,
            voice_name=args.voice,
            output_file=args.output,
            speed=args.speed,
            stability=args.stability,
            similarity_boost=args.similarity_boost,
            style=args.style
        )
        
        # Output result
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                if not args.quiet:
                    print(f"✅ Speech generated successfully!")
                    print(f"📁 Output: {result['output_file']}")
                    print(f"🎤 Voice: {result['voice_used']}")
            else:
                print(f"❌ Generation failed: {result['error']}")
        
        return 0 if result["success"] else 1
        
    except KeyboardInterrupt:
        if args.json:
            print(json.dumps({"success": False, "error": "Interrupted by user"}))
        else:
            print("\n👋 Interrupted by user")
        return 1
    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}))
        else:
            print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())