@echo off
REM Quick launcher for Voice Assistant

echo Starting Voice Recognition Assistant...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Run the application
python voice_assistant.py

if errorlevel 1 (
    echo.
    echo Application exited with an error
    echo Please check the error messages above
    pause
)
