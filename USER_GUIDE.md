# Voice Assistant User Guide

Complete guide for using the Voice Recognition Assistant.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Using the Application](#using-the-application)
3. [Understanding the Interface](#understanding-the-interface)
4. [Configuration](#configuration)
5. [Tips for Best Results](#tips-for-best-results)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

## Getting Started

### First Launch

1. **Start the application**:
   - Double-click `run.bat` or
   - Run `python voice_assistant.py` in the command prompt

2. **Wait for initialization**:
   - First launch may take 30-60 seconds while loading the Whisper model
   - Subsequent launches are faster (~5-10 seconds)
   - Watch the status bar for initialization progress

3. **Ready to use**:
   - When you see "Status: Listening for wake word...", the app is ready
   - The audio spectrum should show real-time visualization

### Basic Workflow

```
1. Wait for "Listening for wake word..."
   ↓
2. Say wake word ("porcupine")
   ↓
3. Wait for "Recording command..." (you'll hear a beep)
   ↓
4. Speak your message (within 5 seconds)
   ↓
5. Application transcribes automatically
   ↓
6. View result in the output area
   ↓
7. Text saved to output.txt
   ↓
8. Return to step 1
```

## Using the Application

### Activating with Wake Word

**Default Wake Word: "porcupine"**

1. Speak clearly: "Hey porcupine" or just "porcupine"
2. Wait for confirmation (status changes to "Recording command...")
3. Start speaking immediately after confirmation

**Tips for wake word detection:**
- Speak at normal volume
- Avoid background noise when saying the wake word
- If not detected, wait 1 second and try again
- Adjust `porcupine_sensitivity` in config.json if needed

### Speaking Your Command

After the wake word is detected:

1. **Timing**: You have 5 seconds to speak (configurable)
2. **Speaking**: Speak clearly at a normal pace
3. **Distance**: Stay 1-2 feet from the microphone
4. **Noise**: Minimize background noise for best results

**Good practices:**
- ✓ Speak at normal conversation volume
- ✓ Enunciate clearly
- ✓ Pause briefly between sentences
- ✓ Speak directly toward the microphone

**Avoid:**
- ✗ Speaking too fast or too slow
- ✗ Whispering or shouting
- ✗ Being too far from the microphone
- ✗ Background music or TV noise

### Viewing Results

Transcriptions appear in the output area with:
- Timestamp
- Original transcription
- Corrected text (if different from original)

All transcriptions are automatically saved to `output.txt`.

## Understanding the Interface

### Main Window Components

```
┌─────────────────────────────────────────────────────┐
│ Status: Listening for wake word...                  │ ← Status Bar
├─────────────────────────────────────────────────────┤
│ ┌─Audio Spectrum─────────────────────────────────┐ │
│ │                                                  │ │ ← Audio Visualization
│ │  [real-time audio spectrum graph]               │ │
│ └──────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ ┌─Transcriptions──────────────────────────────────┐ │
│ │                                                  │ │
│ │ [2025-01-10 14:30:15] Hello world               │ │ ← Transcription Log
│ │ [2025-01-10 14:31:42] This is a test           │ │
│ │                                                  │ │
│ └──────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│        [Clear Output]  [Quit]                       │ ← Control Buttons
└─────────────────────────────────────────────────────┘
```

### Status Messages

| Status | Meaning |
|--------|---------|
| "Listening for wake word..." | Ready, waiting for activation |
| "Wake word detected" | Activation successful, preparing to record |
| "Recording command..." | Currently recording your speech |
| "Transcribing..." | Processing audio with Whisper |
| "Correcting text..." | Applying SymSpell correction |
| "Ready" | Command processed, returning to listening mode |
| "Transcription failed" | Error occurred, try again |

### Audio Spectrum

The spectrum display shows:
- **Height**: Audio volume/amplitude
- **Movement**: Real-time audio activity
- **Purpose**: Confirm microphone is working and detecting sound

**What to look for:**
- Small activity when silent (background noise)
- Large spikes when speaking
- If completely flat, check microphone connection

## Configuration

Edit `config.json` to customize behavior:

### Wake Word Settings

```json
"wake_word": "susie",           // Wake word name (needs access key for custom)
"porcupine_sensitivity": 0.5    // Detection sensitivity (0.0 to 1.0)
```

**Sensitivity Guide:**
- `0.3` - Less sensitive, fewer false positives
- `0.5` - Balanced (recommended)
- `0.7` - More sensitive, may have false positives

### Speech Recognition

```json
"whisper_model": "tiny",        // Model size: tiny, base, small, medium, large
"recording_duration": 5         // Recording time in seconds
```

**Model Comparison:**

| Model | Speed | Accuracy | Memory | Best For |
|-------|-------|----------|--------|----------|
| tiny | Very Fast | Good | ~200MB | Quick commands |
| base | Fast | Better | ~300MB | Balanced use |
| small | Moderate | Great | ~800MB | Longer speech |
| medium | Slow | Excellent | ~1.5GB | Maximum accuracy |
| large | Very Slow | Best | ~3GB | Professional use |

### Audio Settings

```json
"audio_sample_rate": 16000      // Sample rate in Hz (16000 recommended)
```

**Sample Rate Guide:**
- `8000` - Phone quality (not recommended)
- `16000` - Standard for speech (recommended)
- `22050` - Higher quality
- `44100` - CD quality (unnecessary for speech)

### Output Settings

```json
"output_file": "output.txt"     // Where to save transcriptions
```

You can change this to any file path, e.g.:
- `"output.txt"` - Current directory
- `"C:\\Users\\YourName\\Documents\\transcriptions.txt"` - Absolute path
- `"logs/output.txt"` - Subdirectory (must exist)

### GUI Settings

```json
"gui_width": 600,               // Window width in pixels
"gui_height": 400,              // Window height in pixels
"spectrum_update_interval": 50  // Refresh rate in milliseconds
```

## Tips for Best Results

### Optimal Environment

1. **Quiet space**: Minimize background noise
2. **Good microphone**: Use a quality microphone if possible
3. **Proper distance**: 1-2 feet from microphone
4. **Stable position**: Keep microphone in fixed location

### Speaking Tips

1. **Clear pronunciation**: Enunciate words clearly
2. **Normal pace**: Don't speak too fast or slow
3. **Natural volume**: Use conversational voice level
4. **Sentence structure**: Use complete sentences
5. **Pause briefly**: Between sentences or thoughts

### Technical Tips

1. **Close other apps**: Free up CPU/memory for better performance
2. **Use smaller model**: Start with "tiny" model, upgrade if needed
3. **Adjust sensitivity**: Tune wake word detection to your environment
4. **Regular restarts**: Restart app occasionally to clear memory
5. **Update software**: Keep Python and dependencies updated

## Troubleshooting

### Wake Word Not Detected

**Problem**: Application doesn't respond to wake word

**Solutions:**
1. Check microphone is connected and enabled
2. Verify microphone is selected as default recording device
3. Speak louder or closer to microphone
4. Increase `porcupine_sensitivity` in config.json
5. Try alternative pronunciation (e.g., "porcu-pine")
6. Check status bar confirms "Listening for wake word..."

### Poor Transcription Quality

**Problem**: Transcriptions are inaccurate or incomplete

**Solutions:**
1. Speak more clearly and at normal pace
2. Reduce background noise
3. Move closer to microphone
4. Increase `recording_duration` for longer speech
5. Use larger Whisper model (base or small)
6. Check microphone quality and settings
7. Test microphone in Windows Sound Settings

### Application Runs Slowly

**Problem**: Long delays or high CPU usage

**Solutions:**
1. Use "tiny" Whisper model
2. Close other resource-intensive applications
3. Reduce `recording_duration`
4. Restart the application
5. Restart your computer
6. Check for CPU-intensive background processes

### No Text Correction

**Problem**: Spelling errors not corrected

**Solutions:**
1. Run `python setup_symspell.py`
2. Verify `frequency_dictionary_en_82_765.txt` exists
3. Check file is ~6MB in size
4. Re-download if corrupted
5. Check file is in same folder as application

### Audio Spectrum Not Moving

**Problem**: Spectrum display is flat/not responding

**Solutions:**
1. Check microphone is plugged in
2. Verify microphone permissions in Windows
3. Test microphone in Sound Settings
4. Try different USB port (if USB microphone)
5. Restart application
6. Check Windows Privacy settings allow microphone access

## Advanced Usage

### Multiple Output Files

Create different output files for different purposes:

1. Edit `config.json` before launching
2. Change `output_file` to desired filename
3. Launch application
4. Transcriptions save to new file

Example uses:
- `meeting_notes.txt` - For meetings
- `dictation.txt` - For writing
- `commands.txt` - For command logging

### Custom Wake Words

To use custom wake words like "susie":

1. Get Porcupine access key from [Picovoice Console](https://console.picovoice.ai/)
2. Create custom wake word in the console
3. Download wake word model file (`.ppn`)
4. Update your code to use the custom model
5. Set `PORCUPINE_ACCESS_KEY` environment variable

### Running in Background

To run minimized:

1. Start the application
2. Minimize the window
3. Application continues listening
4. Bring window forward to view transcriptions

### Batch Processing

For transcribing audio files (requires modification):

1. Disable wake word detection
2. Load audio file
3. Process through Whisper
4. Apply text correction
5. Save to output file

### Integration with Other Tools

The `output.txt` file can be:
- Monitored by other scripts
- Imported into note-taking apps
- Processed by automation tools
- Backed up to cloud storage

Example PowerShell monitoring:
```powershell
Get-Content output.txt -Wait -Tail 10
```

### Performance Monitoring

Monitor resource usage:

1. Open Task Manager (Ctrl+Shift+Esc)
2. Find Python process
3. Watch CPU and Memory columns
4. Adjust settings if usage is too high

Typical resource usage:
- **Idle**: 5-10% CPU, 200MB RAM
- **Processing**: 50-100% CPU (1 core), 800MB RAM

### Keyboard Shortcuts

While the GUI window has focus:

- **Ctrl+C**: Copy selected text from output area
- **Ctrl+A**: Select all text in output area
- **Alt+F4**: Close application
- **Tab**: Navigate between controls

## Best Practices

### Daily Use

1. Start application at beginning of work session
2. Keep running in background
3. Use wake word to activate when needed
4. Review `output.txt` periodically
5. Clear output display if it gets too long
6. Restart application at end of day

### For Accuracy

1. Train yourself to speak consistently
2. Use the same microphone position
3. Minimize environmental changes
4. Review and correct important transcriptions manually
5. Adjust settings based on results

### For Performance

1. Use smallest model that meets your needs
2. Close unnecessary browser tabs and apps
3. Disable visual effects if on older hardware
4. Consider GPU acceleration for larger models
5. Keep recording duration as short as practical

### For Privacy

1. Disable when not needed
2. Review what's saved to `output.txt`
3. Clear sensitive transcriptions regularly
4. Secure `output.txt` with file permissions
5. Remember: no data leaves your computer

## Getting Help

If you need assistance:

1. Review this guide thoroughly
2. Check [README.md](README.md) for technical details
3. See [INSTALL.md](INSTALL.md) for setup issues
4. Search existing GitHub issues
5. Create new issue with details:
   - What you're trying to do
   - What's happening instead
   - Error messages
   - Your configuration
   - System specifications

## Updates and Maintenance

### Updating Dependencies

Periodically update Python packages:

```bash
pip install --upgrade pvporcupine openai-whisper torch symspellpy
```

### Backing Up Configuration

Save your `config.json`:

```bash
copy config.json config_backup.json
```

### Clearing Cache

To reset Whisper model cache:

1. Close application
2. Delete `~/.cache/whisper` folder
3. Restart application

## Glossary

- **Wake Word**: Trigger word that activates listening
- **ASR**: Automatic Speech Recognition
- **Whisper**: OpenAI's speech recognition model
- **Porcupine**: Wake word detection engine
- **SymSpell**: Spelling correction algorithm
- **Transcription**: Converting speech to text
- **FFT**: Fast Fourier Transform (for spectrum)
- **PCM**: Pulse Code Modulation (audio format)

## Additional Resources

- [OpenAI Whisper Documentation](https://github.com/openai/whisper)
- [Picovoice Porcupine Documentation](https://picovoice.ai/docs/porcupine/)
- [SymSpellPy Documentation](https://github.com/mammothb/symspellpy)
- [PyAudio Documentation](https://people.csail.mit.edu/hubert/pyaudio/)

---

**Version**: 1.0  
**Last Updated**: 2025  
**For**: Voice Recognition Assistant
