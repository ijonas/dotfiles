#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyaudio",
#     "numpy",
# ]
# ///

import os
import sys
import wave
import time
import threading
import tempfile
from pathlib import Path

class AudioRecorder:
    """Cross-platform audio recorder with real-time feedback."""
    
    def __init__(self, 
                 sample_rate=16000,
                 channels=1,
                 chunk_size=1024,
                 format_bits=16):
        """
        Initialize audio recorder with configurable parameters.
        
        Args:
            sample_rate: Sample rate in Hz (16000 recommended for STT)
            channels: Number of audio channels (1 for mono, 2 for stereo)
            chunk_size: Buffer size for recording
            format_bits: Audio bit depth (16 recommended)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.format_bits = format_bits
        
        # Import and configure PyAudio
        try:
            import pyaudio
            self.pyaudio = pyaudio
            
            if format_bits == 16:
                self.format = pyaudio.paInt16
                self.sample_width = 2
            elif format_bits == 24:
                self.format = pyaudio.paInt24
                self.sample_width = 3
            elif format_bits == 32:
                self.format = pyaudio.paInt32
                self.sample_width = 4
            else:
                raise ValueError(f"Unsupported bit depth: {format_bits}")
                
        except ImportError:
            print("❌ Error: PyAudio not available", file=sys.stderr)
            print("Please install system dependencies:", file=sys.stderr)
            print("  macOS: brew install portaudio", file=sys.stderr)
            print("  Ubuntu: sudo apt-get install portaudio19-dev", file=sys.stderr)
            sys.exit(1)
    
    def record(self, duration=5, show_progress=True, output_file=None):
        """
        Record audio for specified duration.
        
        Args:
            duration: Recording duration in seconds
            show_progress: Whether to show recording progress
            output_file: Optional file path to save recording
            
        Returns:
            tuple: (audio_data_bytes, temp_file_path or output_file)
        """
        p = self.pyaudio.PyAudio()
        
        try:
            # Check for available input devices
            self._check_input_devices(p)
            
            stream = p.open(format=self.format,
                           channels=self.channels,
                           rate=self.sample_rate,
                           input=True,
                           frames_per_buffer=self.chunk_size)
            
            if show_progress:
                print(f"🎙️  Recording for {duration} seconds...", file=sys.stderr)
                print("🔊 Speak now!", file=sys.stderr)
            
            frames = []
            start_time = time.time()
            
            # Record with progress feedback
            for i in range(0, int(self.sample_rate / self.chunk_size * duration)):
                try:
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    frames.append(data)
                    
                    if show_progress and i % (self.sample_rate // self.chunk_size // 4) == 0:
                        elapsed = time.time() - start_time
                        remaining = max(0, duration - elapsed)
                        print(f"\r🎙️  Recording... {remaining:.1f}s remaining", 
                              end="", file=sys.stderr)
                        
                except Exception as e:
                    print(f"\r❌ Recording error: {e}", file=sys.stderr)
                    break
            
            if show_progress:
                print("\r🎙️  Recording complete!                    ", file=sys.stderr)
            
            stream.stop_stream()
            stream.close()
            
            audio_data = b''.join(frames)
            
            # Save to file
            if output_file:
                file_path = output_file
            else:
                # Create temporary file
                fd, file_path = tempfile.mkstemp(suffix='.wav')
                os.close(fd)
            
            self._save_wav(audio_data, file_path)
            
            return audio_data, file_path
            
        finally:
            p.terminate()
    
    def record_until_silence(self, max_duration=30, silence_threshold=0.01, 
                           silence_duration=2.0, show_progress=True):
        """
        Record audio until silence is detected.
        
        Args:
            max_duration: Maximum recording duration
            silence_threshold: Volume threshold for silence detection
            silence_duration: Duration of silence before stopping
            show_progress: Whether to show recording progress
            
        Returns:
            tuple: (audio_data_bytes, temp_file_path)
        """
        import numpy as np
        
        p = self.pyaudio.PyAudio()
        
        try:
            stream = p.open(format=self.format,
                           channels=self.channels,
                           rate=self.sample_rate,
                           input=True,
                           frames_per_buffer=self.chunk_size)
            
            if show_progress:
                print("🎙️  Recording until silence detected...", file=sys.stderr)
                print("🔊 Speak now! (will stop after 2s of silence)", file=sys.stderr)
            
            frames = []
            silent_chunks = 0
            silent_threshold_chunks = int(silence_duration * self.sample_rate / self.chunk_size)
            start_time = time.time()
            
            while True:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)
                
                # Check for silence
                audio_array = np.frombuffer(data, dtype=np.int16)
                volume = np.sqrt(np.mean(audio_array**2))
                normalized_volume = volume / 32768  # Normalize for 16-bit audio
                
                if normalized_volume < silence_threshold:
                    silent_chunks += 1
                else:
                    silent_chunks = 0
                
                elapsed = time.time() - start_time
                
                # Stop conditions
                if silent_chunks >= silent_threshold_chunks:
                    if show_progress:
                        print("\r🔇 Silence detected, stopping...                ", file=sys.stderr)
                    break
                elif elapsed >= max_duration:
                    if show_progress:
                        print("\r⏰ Max duration reached, stopping...            ", file=sys.stderr)
                    break
                
                if show_progress:
                    print(f"\r🎙️  Recording... {elapsed:.1f}s (volume: {'▊' * int(normalized_volume * 10)})", 
                          end="", file=sys.stderr)
            
            stream.stop_stream()
            stream.close()
            
            audio_data = b''.join(frames)
            
            # Save to temporary file
            fd, file_path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)
            self._save_wav(audio_data, file_path)
            
            return audio_data, file_path
            
        finally:
            p.terminate()
    
    def _check_input_devices(self, p):
        """Check for available input devices and provide helpful error messages."""
        try:
            device_count = p.get_device_count()
            input_devices = []
            
            for i in range(device_count):
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    input_devices.append(device_info)
            
            if not input_devices:
                print("❌ No input devices found!", file=sys.stderr)
                print("Please check your microphone connection.", file=sys.stderr)
                sys.exit(1)
                
        except Exception as e:
            print(f"⚠️  Warning: Could not check input devices: {e}", file=sys.stderr)
    
    def _save_wav(self, audio_data, filename):
        """Save audio data to WAV file."""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.sample_width)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data)

def main():
    """Command-line interface for audio recorder."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Cross-platform audio recorder')
    parser.add_argument('duration', type=float, nargs='?', default=5.0,
                        help='Recording duration in seconds (default: 5)')
    parser.add_argument('-o', '--output', type=str,
                        help='Output file path (default: temporary file)')
    parser.add_argument('--auto-stop', action='store_true',
                        help='Stop recording automatically when silence detected')
    parser.add_argument('--sample-rate', type=int, default=16000,
                        help='Sample rate in Hz (default: 16000)')
    parser.add_argument('--channels', type=int, default=1,
                        help='Number of channels (default: 1)')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress progress output')
    
    args = parser.parse_args()
    
    try:
        recorder = AudioRecorder(
            sample_rate=args.sample_rate,
            channels=args.channels
        )
        
        if args.auto_stop:
            audio_data, file_path = recorder.record_until_silence(
                max_duration=args.duration,
                show_progress=not args.quiet
            )
        else:
            audio_data, file_path = recorder.record(
                duration=args.duration,
                show_progress=not args.quiet,
                output_file=args.output
            )
        
        # Output the file path for use in scripts
        print(file_path)
        
    except KeyboardInterrupt:
        print("\n🛑 Recording cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()