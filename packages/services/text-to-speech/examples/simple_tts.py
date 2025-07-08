#!/usr/bin/env python3
"""
Simple TTS implementation that works without relative imports
"""

import os
import sys
import json
import requests
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleTTS:
    """Simple TTS implementation using ElevenLabs API directly"""
    
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        self.voice_map = {
            "rachel": "21m00Tcm4TlvDq8ikWAM",
            "drew": "29vD33N1CtxCmqQRPOHJ", 
            "bella": "EXAVITQu4vr4xnSDxMaL",
            "antoni": "ErXwobaYiN019PkySvjV",
            "elli": "MF3mGyEYCl7XYWbV9V6O",
            "josh": "TxGEqnHWrfWFTfGW9XjX",
            "arnold": "VR6AewLTigWG4xSOukaG",
            "adam": "pNInz6obpgDQGcFmaJgB",
            "sam": "yoZ06aMxZJJ28mfd3POQ",
            "clyde": "2EiwWnXFnvU5JabPnv8n"
        }
    
    def generate_speech(self, text, voice_name="rachel", output_file=None, 
                       speed=1.0, stability=0.5, similarity_boost=0.8, style=0.2):
        """Generate speech from text using ElevenLabs API"""
        
        try:
            # Get voice ID
            voice_id = self.voice_map.get(voice_name.lower())
            if not voice_id:
                return {
                    "success": False,
                    "error": f"Unknown voice: {voice_name}. Available: {list(self.voice_map.keys())}"
                }
            
            # Prepare output file
            if not output_file:
                timestamp = int(time.time())
                output_file = f"output/tts_{voice_name}_{timestamp}.mp3"
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else "output", exist_ok=True)
            
            # Prepare API request
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": similarity_boost,
                    "style": style,
                    "use_speaker_boost": True
                }
            }
            
            print(f"🎵 Generating speech...")
            print(f"   Text: {text}")
            print(f"   Voice: {voice_name}")
            print(f"   Output: {output_file}")
            print(f"   Settings: speed={speed}, stability={stability}")
            
            # Make API request
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Save audio file
                with open(output_file, "wb") as f:
                    f.write(response.content)
                
                print(f"✅ Speech generated successfully: {output_file}")
                
                return {
                    "success": True,
                    "output_file": output_file,
                    "voice_used": voice_name,
                    "text_length": len(text),
                    "settings": {
                        "speed": speed,
                        "stability": stability,
                        "similarity_boost": similarity_boost,
                        "style": style
                    }
                }
            else:
                error_msg = f"API error {response.status_code}: {response.text}"
                print(f"❌ {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except requests.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"TTS generation error: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }


def main():
    """CLI interface"""
    if len(sys.argv) < 4:
        print("Usage: python simple_tts.py <text> <voice> <output_file> [--json]")
        return
    
    text = sys.argv[1]
    voice = sys.argv[2]
    output_file = sys.argv[3]
    use_json = "--json" in sys.argv
    
    # Get additional parameters
    speed = 1.0
    stability = 0.5
    similarity_boost = 0.8
    style = 0.2
    
    for i, arg in enumerate(sys.argv):
        if arg == "--speed" and i + 1 < len(sys.argv):
            speed = float(sys.argv[i + 1])
        elif arg == "--stability" and i + 1 < len(sys.argv):
            stability = float(sys.argv[i + 1])
        elif arg == "--similarity-boost" and i + 1 < len(sys.argv):
            similarity_boost = float(sys.argv[i + 1])
        elif arg == "--style" and i + 1 < len(sys.argv):
            style = float(sys.argv[i + 1])
    
    try:
        tts = SimpleTTS()
        result = tts.generate_speech(
            text=text,
            voice_name=voice,
            output_file=output_file,
            speed=speed,
            stability=stability,
            similarity_boost=similarity_boost,
            style=style
        )
        
        if use_json:
            print(json.dumps(result, indent=2))
        else:
            if result["success"]:
                print(f"✅ Success: {result['output_file']}")
            else:
                print(f"❌ Error: {result['error']}")
                
    except Exception as e:
        if use_json:
            print(json.dumps({"success": False, "error": str(e)}, indent=2))
        else:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()