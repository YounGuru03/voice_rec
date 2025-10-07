"""
Build script for creating Windows executable using PyInstaller
"""

import os
import sys
import subprocess

def build_executable():
    """Build the Windows executable"""
    print("Building Voice Assistant executable...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=VoiceAssistant',
        '--add-data=config.json;.',
        '--hidden-import=pvporcupine',
        '--hidden-import=whisper',
        '--hidden-import=symspellpy',
        '--hidden-import=tkinter',
        '--hidden-import=matplotlib',
        '--hidden-import=numpy',
        '--hidden-import=pyaudio',
        '--collect-all=whisper',
        '--collect-all=torch',
        '--collect-all=torchaudio',
        '--icon=NONE',
        'voice_assistant.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild completed successfully!")
        print("Executable can be found in the 'dist' folder")
        print("\nIMPORTANT:")
        print("- Copy config.json to the same folder as the executable")
        print("- Set PORCUPINE_ACCESS_KEY environment variable for custom wake word")
        print("- Optional: Add frequency_dictionary_en_82_765.txt for spell correction")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("PyInstaller not found. Install it with: pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()
