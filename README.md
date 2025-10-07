# Voice Recognition Assistant

A fully offline Windows voice recognition system with wake word detection, speech recognition, and text correction. The application runs continuously with low resource usage, activating only when the wake word is detected.

## Features

- **Wake Word Detection**: Uses Porcupine for efficient, low-resource wake word detection
- **Speech Recognition**: Whisper Tiny model for fast, accurate offline transcription
- **Text Correction**: SymSpell for automatic spelling and grammar correction
- **Real-time Audio Visualization**: Live audio spectrum display
- **Offline Processing**: All processing done locally, no internet required
- **Low Resource Usage**: Optimized for continuous operation with minimal CPU/memory
- **Native Windows UI**: Clean, responsive interface using tkinter
- **Auto-save**: Transcriptions automatically saved to `output.txt`

## System Requirements

- Windows 10 or later
- Python 3.8 or later
- Microphone
- ~500MB disk space for models
- ~1GB RAM during active transcription

## Installation

### Option 1: Run from Source (Recommended for Development)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YounGuru03/voice_rec.git
   cd voice_rec
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download SymSpell dictionary** (optional, for text correction):
   ```bash
   python setup_symspell.py
   ```

5. **Set Porcupine access key** (required for custom wake word):
   
   The application uses Porcupine's built-in "porcupine" wake word by default. To use a custom wake word like "susie", you need to:
   
   - Sign up for a free account at [Picovoice Console](https://console.picovoice.ai/)
   - Get your AccessKey
   - Set the environment variable:
     ```bash
     set PORCUPINE_ACCESS_KEY=your_access_key_here
     ```
   
   Or add it to your system environment variables for persistence.

6. **Run the application**:
   ```bash
   python voice_assistant.py
   ```

### Option 2: Build Windows Executable

1. Follow steps 1-4 from Option 1

2. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

3. **Build the executable**:
   ```bash
   python build_exe.py
   ```

4. **Run the executable**:
   - Navigate to the `dist` folder
   - Copy `config.json` to the same folder
   - (Optional) Copy `frequency_dictionary_en_82_765.txt` for spell correction
   - Double-click `VoiceAssistant.exe`

## Usage

1. **Start the application**:
   - Run `python voice_assistant.py` or launch the executable

2. **Wait for initialization**:
   - The application will load the Whisper model (takes a few seconds)
   - Status will show "Listening for wake word..."

3. **Activate with wake word**:
   - Say the wake word ("porcupine" by default)
   - The application will beep and start recording

4. **Speak your command**:
   - Speak clearly within 5 seconds (configurable)
   - Recording will stop automatically

5. **View transcription**:
   - Transcribed text appears in the output area
   - If correction is enabled, both original and corrected text are shown
   - Text is automatically saved to `output.txt`

6. **Continue using**:
   - The application returns to listening for the wake word
   - Repeat steps 3-5 as needed

## Configuration

Edit `config.json` to customize the application:

```json
{
  "wake_word": "susie",                // Wake word name (requires access key)
  "porcupine_sensitivity": 0.5,        // 0.0 to 1.0, higher = more sensitive
  "whisper_model": "tiny",             // tiny, base, small, medium, large
  "audio_sample_rate": 16000,          // Audio sample rate in Hz
  "recording_duration": 5,             // Recording duration in seconds
  "output_file": "output.txt",         // Output file path
  "symspell_max_edit_distance": 2,     // Max edit distance for correction
  "gui_width": 600,                    // GUI window width
  "gui_height": 400                    // GUI window height
}
```

### Whisper Model Selection

- **tiny**: Fastest, lowest resource usage, good accuracy (~75MB)
- **base**: Balanced speed and accuracy (~150MB)
- **small**: Better accuracy, moderate speed (~500MB)
- **medium**: High accuracy, slower (~1.5GB)
- **large**: Best accuracy, slowest (~3GB)

For offline real-time use, **tiny** or **base** is recommended.

## Performance

Typical performance on a modern PC:

- **Wake word detection**: <50ms latency, ~5% CPU
- **Transcription**: 1-3 seconds for 5 seconds of audio
- **Memory usage**: 
  - Idle (listening): ~200MB
  - During transcription: ~800MB (tiny model)
- **Disk space**: ~500MB with tiny model

## Troubleshooting

### "Porcupine not initialized" error
- Set the `PORCUPINE_ACCESS_KEY` environment variable
- Or use the default "porcupine" wake word without a key

### "No module named 'whisper'" error
- Install dependencies: `pip install -r requirements.txt`

### Audio device errors
- Check that your microphone is connected and enabled
- Try running as administrator
- Check Windows audio settings

### Slow transcription
- Use a smaller Whisper model (tiny or base)
- Ensure the application is running on the GPU (if available)
- Close other resource-intensive applications

### No text correction
- Run `python setup_symspell.py` to download the dictionary
- Ensure `frequency_dictionary_en_82_765.txt` is in the same folder

## Building from Source

Requirements for building:
- All runtime dependencies from `requirements.txt`
- PyInstaller: `pip install pyinstaller`

Build command:
```bash
python build_exe.py
```

The executable will be created in the `dist` folder.

## Technical Details

### Architecture

```
┌─────────────────────────────────────────┐
│           Voice Assistant GUI           │
│  (Tkinter + Matplotlib visualization)  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Audio Monitoring Thread            │
│  (Continuous wake word detection)       │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────────┐    ┌───────▼──────┐
│ Porcupine  │    │   Whisper    │
│  (Wake)    │    │    (ASR)     │
└────────────┘    └───────┬──────┘
                          │
                  ┌───────▼──────┐
                  │   SymSpell   │
                  │ (Correction) │
                  └───────┬──────┘
                          │
                  ┌───────▼──────┐
                  │  output.txt  │
                  └──────────────┘
```

### Models Used

1. **Porcupine**: Efficient on-device wake word detection
   - Low latency (<50ms)
   - Low false positive rate
   - Minimal CPU/memory footprint

2. **Whisper Tiny**: Lightweight speech recognition
   - 39M parameters
   - English language optimized
   - Fast inference on CPU

3. **SymSpell**: Fast spelling correction
   - Symmetric delete algorithm
   - 1M+ word dictionary
   - Sub-millisecond correction

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

- [Picovoice Porcupine](https://github.com/Picovoice/porcupine) for wake word detection
- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [SymSpellPy](https://github.com/mammothb/symspellpy) for text correction
