#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "elevenlabs",
#     "python-dotenv",
#     "pyaudio",
#     "numpy",
# ]
# ///

import os
import sys
import wave
import tempfile
import time
import threading
from pathlib import Path
from dotenv import load_dotenv

def main():
    """
    ElevenLabs Speech-to-Text Script
    
    Records audio from microphone and converts it to text using ElevenLabs STT API.
    Accepts optional recording duration as command-line argument.
    
    Usage:
    - ./elevenlabs_stt.py                    # Records for 5 seconds (default)
    - ./elevenlabs_stt.py 10                 # Records for 10 seconds
    - ./elevenlabs_stt.py --file audio.wav   # Transcribes existing audio file
    
    Features:
    - Real-time audio recording from microphone
    - High-quality speech-to-text via ElevenLabs Scribe v1
    - Multi-speaker support and language detection
    - Outputs clean transcribed text to stdout
    """
    
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        print("❌ Error: ELEVENLABS_API_KEY not found in environment variables", file=sys.stderr)
        print("Please add your ElevenLabs API key to .env file:", file=sys.stderr)
        print("ELEVENLABS_API_KEY=your_api_key_here", file=sys.stderr)
        sys.exit(1)
    
    try:
        from elevenlabs.client import ElevenLabs
        import pyaudio
        import numpy as np
        
        # Initialize client
        elevenlabs = ElevenLabs(api_key=api_key)
        
        # Parse command line arguments
        file_mode = False
        audio_file_path = None
        duration = 5  # Default 5 seconds
        
        if len(sys.argv) > 1:
            if sys.argv[1] == "--file" and len(sys.argv) > 2:
                file_mode = True
                audio_file_path = sys.argv[2]
            else:
                try:
                    duration = int(sys.argv[1])
                except ValueError:
                    print("❌ Error: Duration must be a number", file=sys.stderr)
                    sys.exit(1)
        
        if file_mode:
            # Transcribe existing file
            if not os.path.exists(audio_file_path):
                print(f"❌ Error: Audio file not found: {audio_file_path}", file=sys.stderr)
                sys.exit(1)
            
            print(f"🎯 Transcribing file: {audio_file_path}", file=sys.stderr)
            transcribe_file(elevenlabs, audio_file_path)
        else:
            # Record and transcribe
            print(f"🎙️  ElevenLabs Speech-to-Text", file=sys.stderr)
            print("=" * 40, file=sys.stderr)
            print(f"🎯 Recording for {duration} seconds...", file=sys.stderr)
            print("🔊 Speak now!", file=sys.stderr)
            
            # Record audio
            audio_data = record_audio(duration)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                temp_path = tmp_file.name
                save_audio(audio_data, temp_path)
            
            try:
                print("🤖 Transcribing...", file=sys.stderr)
                transcribe_file(elevenlabs, temp_path)
            finally:
                # Clean up temporary file
                os.unlink(temp_path)
                
    except ImportError as e:
        if "pyaudio" in str(e):
            print("❌ Error: PyAudio not available", file=sys.stderr)
            print("This script uses UV to auto-install dependencies.", file=sys.stderr)
            print("PyAudio may need system-level installation:", file=sys.stderr)
            print("  macOS: brew install portaudio", file=sys.stderr)
            print("  Ubuntu: sudo apt-get install portaudio19-dev", file=sys.stderr)
        else:
            print(f"❌ Error: Missing dependency: {e}", file=sys.stderr)
            print("This script uses UV to auto-install dependencies.", file=sys.stderr)
            print("Make sure UV is installed: https://docs.astral.sh/uv/", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

def record_audio(duration):
    """Record audio from microphone for specified duration."""
    import pyaudio
    import numpy as np
    
    # Audio recording parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # 16kHz as recommended by ElevenLabs
    
    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        
        frames = []
        
        # Record with visual feedback
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
            
            # Simple progress indicator
            if i % (RATE // CHUNK // 4) == 0:  # Update 4 times per second
                elapsed = i * CHUNK / RATE
                remaining = duration - elapsed
                print(f"\r🎙️  Recording... {remaining:.1f}s remaining", end="", file=sys.stderr)
        
        print("\r🎙️  Recording complete!                    ", file=sys.stderr)
        
        stream.stop_stream()
        stream.close()
        
        return b''.join(frames)
        
    finally:
        p.terminate()

def save_audio(audio_data, filename):
    """Save recorded audio data to WAV file."""
    CHANNELS = 1
    RATE = 16000
    SAMPLE_WIDTH = 2  # 16-bit
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPLE_WIDTH)
        wf.setframerate(RATE)
        wf.writeframes(audio_data)

def transcribe_file(elevenlabs, file_path):
    """Transcribe audio file using ElevenLabs STT API."""
    try:
        with open(file_path, 'rb') as audio_file:
            response = elevenlabs.speech_to_text.convert(
                model_id="scribe_v1",
                file=audio_file,
                # Optional parameters for better results
                language_code="en",  # Auto-detect if not specified
                diarize=False,  # Set to True if multiple speakers expected
            )
        
        # Extract transcribed text from response
        if hasattr(response, 'text'):
            transcribed_text = response.text.strip()
        elif isinstance(response, dict) and 'text' in response:
            transcribed_text = response['text'].strip()
        else:
            # Handle different response formats
            transcribed_text = str(response).strip()
        
        if transcribed_text:
            # Output only the transcribed text to stdout (for piping)
            print(transcribed_text)
        else:
            print("❌ No speech detected in audio", file=sys.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Transcription error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()