# Installation Guide

This guide will help you install and set up the Voice Recognition Assistant on Windows.

## Prerequisites

Before you begin, ensure you have:

1. **Windows 10 or later**
2. **Python 3.8 or later** - Download from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"
3. **Microphone** - Any working microphone
4. **Internet connection** - For initial setup and downloading models

## Quick Installation (Recommended)

### Step 1: Download the Project

```bash
git clone https://github.com/YounGuru03/voice_rec.git
cd voice_rec
```

Or download and extract the ZIP file from GitHub.

### Step 2: Install Python Dependencies

Open Command Prompt or PowerShell in the project folder and run:

```bash
pip install -r requirements.txt
```

This will install:
- pvporcupine (wake word detection)
- openai-whisper (speech recognition)
- torch & torchaudio (Whisper dependencies)
- numpy (numerical computing)
- pyaudio (audio input)
- symspellpy (text correction)
- matplotlib (audio visualization)

**Note**: Installing Whisper and PyTorch may take several minutes.

### Step 3: Download SymSpell Dictionary (Optional)

For automatic text correction, run:

```bash
python setup_symspell.py
```

This downloads the English frequency dictionary used for spelling correction.

### Step 4: Get Porcupine Access Key (Optional)

The application works with the built-in "porcupine" wake word without any setup.

To use a custom wake word like "susie":

1. Sign up for a free account at [Picovoice Console](https://console.picovoice.ai/)
2. Create a new Porcupine project
3. Copy your AccessKey
4. Set the environment variable:

   **PowerShell:**
   ```powershell
   $env:PORCUPINE_ACCESS_KEY="your_access_key_here"
   ```

   **Command Prompt:**
   ```cmd
   set PORCUPINE_ACCESS_KEY=your_access_key_here
   ```

   **Permanent (System-wide):**
   - Open System Properties → Environment Variables
   - Add new User Variable: `PORCUPINE_ACCESS_KEY` = `your_access_key_here`

### Step 5: Run the Application

```bash
python voice_assistant.py
```

The application will:
1. Load the Whisper model (first run takes longer)
2. Initialize audio devices
3. Start listening for the wake word

## Building Windows Executable

If you want a standalone `.exe` file:

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Build the Executable

```bash
python build_exe.py
```

### Step 3: Prepare Distribution

1. Navigate to the `dist` folder
2. Copy `config.json` to the same folder
3. (Optional) Copy `frequency_dictionary_en_82_765.txt` for spell correction
4. Share the folder or create a ZIP file

### Step 4: Run the Executable

Double-click `VoiceAssistant.exe` to run.

## Troubleshooting

### PyAudio Installation Issues

If PyAudio fails to install, try:

**Option 1: Use precompiled wheel**
```bash
pip install pipwin
pipwin install pyaudio
```

**Option 2: Download wheel manually**
1. Visit https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download the appropriate `.whl` file for your Python version
3. Install: `pip install PyAudio-0.2.14-cpXX-cpXX-win_amd64.whl`

### Torch/Whisper Installation Issues

If Torch installation is slow or fails:

**Option 1: CPU-only version (smaller, faster)**
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**Option 2: GPU version (if you have NVIDIA GPU)**
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### "No audio input device found"

1. Check that your microphone is connected
2. Go to Windows Sound Settings and ensure the microphone is enabled
3. Set the microphone as the default recording device
4. Try running the application as Administrator

### "PORCUPINE_ACCESS_KEY not set"

The application works with the built-in "porcupine" wake word without an access key.

To use custom wake words:
1. Get an access key from [Picovoice Console](https://console.picovoice.ai/)
2. Set it as an environment variable (see Step 4 above)

### Application is slow

1. **Use a smaller Whisper model**: Edit `config.json` and change `"whisper_model": "tiny"`
2. **Close other applications**: Free up CPU and memory
3. **Check CPU usage**: Ensure no background processes are consuming resources
4. **Use GPU acceleration**: Install CUDA-enabled PyTorch if you have an NVIDIA GPU

### No text correction

1. Run `python setup_symspell.py` to download the dictionary
2. Ensure `frequency_dictionary_en_82_765.txt` is in the same folder as the application
3. Check that the file downloaded successfully (should be ~6MB)

## Testing the Installation

Run the basic tests:

```bash
python test_basic.py
```

This will verify:
- All required files are present
- Configuration is valid
- Modules can be imported

## Minimum System Requirements

- **CPU**: Any modern processor (Intel Core i3 or equivalent)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 1GB free space (for models and dependencies)
- **OS**: Windows 10 or later

## Recommended System Specifications

- **CPU**: Intel Core i5 or AMD Ryzen 5 or better
- **RAM**: 8GB or more
- **Disk**: SSD with 2GB free space
- **OS**: Windows 10/11 64-bit

## Next Steps

Once installed, see [README.md](README.md) for:
- Usage instructions
- Configuration options
- Performance tuning
- Advanced features

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the [README.md](README.md) documentation
3. Open an issue on GitHub with:
   - Your Python version (`python --version`)
   - Your OS version
   - Error messages
   - Steps to reproduce the problem

## Uninstallation

To remove the application:

1. Delete the project folder
2. (Optional) Remove the virtual environment if you created one
3. (Optional) Uninstall Python packages:
   ```bash
   pip uninstall pvporcupine openai-whisper torch torchaudio numpy pyaudio symspellpy matplotlib
   ```

## Privacy and Security

This application:
- ✓ Runs completely offline (no internet required after installation)
- ✓ Does not transmit any data
- ✓ Does not collect any information
- ✓ Processes all audio locally on your computer
- ✓ Only saves transcriptions to a local file you control

All your voice data stays on your computer.
