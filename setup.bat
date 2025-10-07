@echo off
REM Voice Assistant Setup Script for Windows
REM Run this script to automatically install dependencies

echo ============================================================
echo Voice Recognition Assistant - Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo pip found:
pip --version
echo.

REM Install dependencies
echo Installing Python dependencies...
echo This may take several minutes, please be patient...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check the error messages above
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Dependencies installed successfully!
echo ============================================================
echo.

REM Download SymSpell dictionary
echo Downloading SymSpell dictionary for text correction...
python setup_symspell.py

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo To run the application:
echo   python voice_assistant.py
echo.
echo To build a Windows executable:
echo   1. pip install pyinstaller
echo   2. python build_exe.py
echo.
echo For custom wake words, set PORCUPINE_ACCESS_KEY environment variable
echo Visit: https://console.picovoice.ai/
echo.
pause
