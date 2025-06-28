"""
Interactive utilities for user input and selection.

Provides functions for interactive audio file selection and user input.
"""

from pathlib import Path
from typing import List, Optional


def interactive_audio_selection(audio_files: List[Path]) -> Optional[Path]:
    """Interactive audio file selection."""
    if not audio_files:
        print("❌ No audio files found in current directory")
        return None
    
    print("\n🎵 Available audio files:")
    for i, audio in enumerate(audio_files, 1):
        print(f"   {i}. {audio.name}")
    
    while True:
        try:
            choice = input(f"\n🔢 Select audio file (1-{len(audio_files)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(audio_files):
                return audio_files[index]
            else:
                print(f"❌ Invalid choice. Please enter 1-{len(audio_files)}")
        except ValueError:
            print("❌ Invalid input. Please enter a number")
        except KeyboardInterrupt:
            print("\n👋 Cancelled by user")
            return None


def interactive_multiple_audio_selection(audio_files: List[Path]) -> List[Path]:
    """Interactive selection of multiple audio files."""
    if not audio_files:
        print("❌ No audio files found in current directory")
        return []
    
    print("\n🎵 Available audio files:")
    for i, audio in enumerate(audio_files, 1):
        print(f"   {i}. {audio.name}")
    
    selected_files = []
    
    print(f"\n🔢 Select multiple audio files:")
    print("   - Enter numbers separated by commas (e.g., 1,3,5)")
    print("   - Or enter 'all' to select all files")
    print("   - Or enter 'q' to quit")
    
    while True:
        try:
            choice = input(f"\nSelection: ").strip()
            
            if choice.lower() == 'q':
                return []
            
            if choice.lower() == 'all':
                return audio_files
            
            # Parse comma-separated numbers
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            
            # Validate all indices
            valid = True
            for index in indices:
                if index < 0 or index >= len(audio_files):
                    print(f"❌ Invalid choice: {index + 1}. Please enter numbers 1-{len(audio_files)}")
                    valid = False
                    break
            
            if valid and len(indices) >= 2:
                selected_files = [audio_files[i] for i in indices]
                print(f"\n✅ Selected {len(selected_files)} audio files:")
                for i, audio in enumerate(selected_files, 1):
                    print(f"   {i}. {audio.name}")
                return selected_files
            elif valid and len(indices) < 2:
                print("❌ Please select at least 2 audio files")
            
        except ValueError:
            print("❌ Invalid input. Please enter numbers separated by commas")
        except KeyboardInterrupt:
            print("\n👋 Cancelled by user")
            return []