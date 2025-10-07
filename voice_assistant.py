#!/usr/bin/env python3
"""
Offline Voice Recognition Assistant with Wake Word Detection
Uses Porcupine for wake word, Whisper for ASR, and SymSpell for correction
"""

import os
import sys
import json
import wave
import struct
import threading
import queue
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pyaudio
import pvporcupine
import whisper
from symspellpy import SymSpell, Verbosity

import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class VoiceAssistant:
    """Main voice assistant class with wake word detection and speech recognition"""
    
    def __init__(self, config_path="config.json"):
        """Initialize the voice assistant with configuration"""
        self.load_config(config_path)
        
        # Audio setup
        self.audio = pyaudio.PyAudio()
        self.sample_rate = self.config['audio_sample_rate']
        self.chunk_size = 512
        
        # State management
        self.is_running = False
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        # Initialize models
        self.init_porcupine()
        self.init_whisper()
        self.init_symspell()
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            print("Using default configuration")
            self.config = {
                "wake_word": "susie",
                "porcupine_sensitivity": 0.5,
                "whisper_model": "tiny",
                "audio_sample_rate": 16000,
                "recording_duration": 5,
                "output_file": "output.txt",
                "symspell_max_edit_distance": 2,
                "symspell_prefix_length": 7
            }
    
    def init_porcupine(self):
        """Initialize Porcupine wake word detection"""
        try:
            # Get access key from environment or use default
            access_key = os.environ.get('PORCUPINE_ACCESS_KEY', '')
            
            # For built-in wake words like "porcupine", "picovoice", etc.
            # We'll use the built-in keyword detection
            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=['porcupine']  # Using built-in keyword
            )
            self.porcupine_sample_rate = self.porcupine.sample_rate
            self.porcupine_frame_length = self.porcupine.frame_length
            print(f"Porcupine initialized (using 'porcupine' as wake word)")
        except Exception as e:
            print(f"Failed to initialize Porcupine: {e}")
            print("Note: For custom wake word 'susie', you need a Porcupine access key")
            print("Set PORCUPINE_ACCESS_KEY environment variable")
            self.porcupine = None
    
    def init_whisper(self):
        """Initialize Whisper speech recognition model"""
        try:
            model_name = self.config.get('whisper_model', 'tiny')
            print(f"Loading Whisper {model_name} model...")
            self.whisper_model = whisper.load_model(model_name)
            print("Whisper model loaded successfully")
        except Exception as e:
            print(f"Failed to initialize Whisper: {e}")
            self.whisper_model = None
    
    def init_symspell(self):
        """Initialize SymSpell for text correction"""
        try:
            self.sym_spell = SymSpell(
                max_dictionary_edit_distance=self.config.get('symspell_max_edit_distance', 2),
                prefix_length=self.config.get('symspell_prefix_length', 7)
            )
            
            # Try to load dictionary
            dictionary_path = "frequency_dictionary_en_82_765.txt"
            if os.path.exists(dictionary_path):
                self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
                print("SymSpell dictionary loaded")
            else:
                print("SymSpell dictionary not found, text correction disabled")
                self.sym_spell = None
        except Exception as e:
            print(f"Failed to initialize SymSpell: {e}")
            self.sym_spell = None
    
    def correct_text(self, text):
        """Correct text using SymSpell"""
        if not self.sym_spell or not text:
            return text
        
        try:
            suggestions = self.sym_spell.lookup_compound(
                text, 
                max_edit_distance=2
            )
            if suggestions:
                return suggestions[0].term
        except Exception as e:
            print(f"Text correction error: {e}")
        
        return text
    
    def detect_wake_word(self, audio_data):
        """Detect wake word in audio data"""
        if not self.porcupine:
            return False
        
        try:
            # Convert audio data to int16 array
            pcm = struct.unpack_from("h" * self.porcupine_frame_length, audio_data)
            keyword_index = self.porcupine.process(pcm)
            return keyword_index >= 0
        except Exception as e:
            print(f"Wake word detection error: {e}")
            return False
    
    def record_audio(self, duration):
        """Record audio for specified duration"""
        print(f"Recording for {duration} seconds...")
        
        frames = []
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        num_chunks = int(self.sample_rate / self.chunk_size * duration)
        
        for i in range(num_chunks):
            try:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                print(f"Audio read error: {e}")
                break
        
        stream.stop_stream()
        stream.close()
        
        # Convert to numpy array
        audio_data = b''.join(frames)
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        
        return audio_np
    
    def transcribe_audio(self, audio_data):
        """Transcribe audio using Whisper"""
        if not self.whisper_model:
            return None
        
        try:
            print("Transcribing audio...")
            result = self.whisper_model.transcribe(
                audio_data,
                language='en',
                fp16=False
            )
            text = result['text'].strip()
            print(f"Transcribed: {text}")
            return text
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
    
    def save_output(self, text):
        """Save transcribed and corrected text to output file"""
        output_file = self.config.get('output_file', 'output.txt')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {text}\n")
            print(f"Saved to {output_file}")
        except Exception as e:
            print(f"Failed to save output: {e}")
    
    def audio_monitoring_thread(self):
        """Thread for continuous audio monitoring and wake word detection"""
        if not self.porcupine:
            print("Porcupine not initialized, wake word detection disabled")
            return
        
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.porcupine_sample_rate,
            input=True,
            frames_per_buffer=self.porcupine_frame_length
        )
        
        print("Listening for wake word...")
        
        while self.is_running:
            try:
                audio_data = stream.read(self.porcupine_frame_length, exception_on_overflow=False)
                
                # Send audio data to GUI for visualization
                self.audio_queue.put(audio_data)
                
                # Check for wake word
                if self.detect_wake_word(audio_data):
                    print("Wake word detected!")
                    self.result_queue.put(("wake_word", "Wake word detected"))
                    
                    # Close monitoring stream
                    stream.stop_stream()
                    stream.close()
                    
                    # Record and process command
                    self.process_voice_command()
                    
                    # Reopen monitoring stream
                    stream = self.audio.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=self.porcupine_sample_rate,
                        input=True,
                        frames_per_buffer=self.porcupine_frame_length
                    )
                    print("Listening for wake word...")
                    
            except Exception as e:
                print(f"Audio monitoring error: {e}")
                time.sleep(0.1)
        
        stream.stop_stream()
        stream.close()
    
    def process_voice_command(self):
        """Process voice command after wake word detection"""
        self.result_queue.put(("status", "Recording command..."))
        
        # Record audio
        duration = self.config.get('recording_duration', 5)
        audio_data = self.record_audio(duration)
        
        # Transcribe
        self.result_queue.put(("status", "Transcribing..."))
        text = self.transcribe_audio(audio_data)
        
        if text:
            # Correct text
            self.result_queue.put(("status", "Correcting text..."))
            corrected_text = self.correct_text(text)
            
            # Display and save result
            self.result_queue.put(("transcription", f"Original: {text}"))
            if corrected_text != text:
                self.result_queue.put(("transcription", f"Corrected: {corrected_text}"))
            
            self.save_output(corrected_text)
            self.result_queue.put(("status", "Ready"))
        else:
            self.result_queue.put(("status", "Transcription failed"))
    
    def start(self):
        """Start the voice assistant"""
        self.is_running = True
        
        # Start audio monitoring thread
        self.monitor_thread = threading.Thread(target=self.audio_monitoring_thread, daemon=True)
        self.monitor_thread.start()
    
    def stop(self):
        """Stop the voice assistant"""
        self.is_running = False
        
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
        
        if self.porcupine:
            self.porcupine.delete()
        
        self.audio.terminate()


class VoiceAssistantGUI:
    """GUI for the voice assistant with audio spectrum visualization"""
    
    def __init__(self, root):
        """Initialize the GUI"""
        self.root = root
        self.root.title("Voice Assistant - Say 'porcupine' to activate")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Initialize voice assistant
        self.assistant = VoiceAssistant()
        
        # Setup GUI
        self.setup_gui()
        
        # Start assistant
        self.assistant.start()
        
        # Start GUI update loop
        self.update_gui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        """Setup GUI components"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame, 
            text="Status: Listening for wake word...",
            font=('Segoe UI', 10, 'bold')
        )
        self.status_label.grid(row=0, column=0, pady=5, sticky=tk.W)
        
        # Audio spectrum visualization
        spectrum_frame = ttk.LabelFrame(main_frame, text="Audio Spectrum", padding="5")
        spectrum_frame.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        spectrum_frame.columnconfigure(0, weight=1)
        spectrum_frame.rowconfigure(0, weight=1)
        
        self.figure = Figure(figsize=(6, 2), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_ylim([0, 1])
        self.ax.set_xlim([0, 100])
        self.ax.set_xlabel('Frequency Bins')
        self.ax.set_ylabel('Amplitude')
        self.ax.grid(True, alpha=0.3)
        
        self.canvas = FigureCanvasTkAgg(self.figure, spectrum_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.line, = self.ax.plot([], [], 'b-', linewidth=1)
        
        # Output text area
        output_frame = ttk.LabelFrame(main_frame, text="Transcriptions", padding="5")
        output_frame.grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=70,
            height=10,
            font=('Segoe UI', 9)
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=5)
        
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear Output",
            command=self.clear_output
        )
        self.clear_button.grid(row=0, column=0, padx=5)
        
        self.quit_button = ttk.Button(
            button_frame,
            text="Quit",
            command=self.on_closing
        )
        self.quit_button.grid(row=0, column=1, padx=5)
        
    def update_spectrum(self, audio_data):
        """Update audio spectrum visualization"""
        try:
            # Convert audio data to numpy array
            pcm = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Compute FFT
            fft = np.fft.rfft(pcm)
            spectrum = np.abs(fft)
            
            # Normalize and limit to displayable range
            if len(spectrum) > 0:
                spectrum = spectrum / (np.max(spectrum) + 1e-10)
                
                # Downsample for display
                display_bins = 100
                if len(spectrum) > display_bins:
                    spectrum = np.interp(
                        np.linspace(0, len(spectrum) - 1, display_bins),
                        np.arange(len(spectrum)),
                        spectrum
                    )
                
                # Update plot
                x_data = np.arange(len(spectrum))
                self.line.set_data(x_data, spectrum)
                self.canvas.draw_idle()
        except Exception as e:
            pass  # Silently ignore visualization errors
    
    def update_gui(self):
        """Update GUI with new data from queues"""
        # Update audio spectrum
        try:
            while not self.assistant.audio_queue.empty():
                audio_data = self.assistant.audio_queue.get_nowait()
                self.update_spectrum(audio_data)
        except queue.Empty:
            pass
        
        # Update status and results
        try:
            while not self.assistant.result_queue.empty():
                msg_type, msg = self.assistant.result_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_label.config(text=f"Status: {msg}")
                elif msg_type == "wake_word":
                    self.output_text.insert(tk.END, f"\n=== {msg} ===\n")
                    self.output_text.see(tk.END)
                elif msg_type == "transcription":
                    self.output_text.insert(tk.END, f"{msg}\n")
                    self.output_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Schedule next update
        self.root.after(50, self.update_gui)
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def on_closing(self):
        """Handle window closing"""
        print("Shutting down...")
        self.assistant.stop()
        self.root.destroy()


def main():
    """Main entry point"""
    print("=" * 60)
    print("Voice Assistant with Wake Word Detection")
    print("=" * 60)
    print("Starting application...")
    
    # Create GUI
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    
    # Run main loop
    root.mainloop()
    
    print("Application closed")


if __name__ == "__main__":
    main()
