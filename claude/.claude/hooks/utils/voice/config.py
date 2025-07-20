#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyyaml",
#     "python-dotenv",
# ]
# ///

import os
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv

class VoiceConfig:
    """Configuration manager for voice commands."""
    
    DEFAULT_CONFIG = {
        'audio': {
            'sample_rate': 16000,
            'channels': 1,
            'chunk_size': 1024,
            'format_bits': 16,
        },
        'recording': {
            'default_duration': 5,
            'max_duration': 30,
            'silence_threshold': 0.01,
            'silence_duration': 2.0,
        },
        'stt': {
            'model_id': 'scribe_v1',
            'language_code': 'en',
            'diarize': False,
            'num_speakers': 1,
        },
        'preprocessing': {
            'remove_artifacts': True,
            'transform_natural_language': True,
            'validate_commands': True,
            'suggest_corrections': True,
        },
        'listening': {
            'wake_word': 'claude',
            'max_session_minutes': 30,
            'silence_timeout': 2,
            'wake_word_sensitivity': 0.7,
        },
        'feedback': {
            'visual_recording_indicator': True,
            'audio_feedback': False,
            'verbose_logging': False,
            'show_transcription': True,
            'show_preprocessing': True,
        }
    }
    
    def __init__(self, config_file=None):
        """
        Initialize voice configuration.
        
        Args:
            config_file: Optional path to configuration file
        """
        load_dotenv()
        
        self.config_file = config_file or self._get_default_config_path()
        self.config = self._load_config()
    
    def _get_default_config_path(self):
        """Get the default configuration file path."""
        # Try multiple locations
        possible_paths = [
            Path.home() / '.claude' / 'voice_config.yaml',
            Path.cwd() / '.claude' / 'voice_config.yaml',
            Path(__file__).parent / 'voice_config.yaml',
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        # Return the first option as default
        return str(possible_paths[0])
    
    def _load_config(self):
        """Load configuration from file or create default."""
        config_path = Path(self.config_file)
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                
                # Merge with defaults
                config = self._deep_merge(self.DEFAULT_CONFIG.copy(), user_config)
                return config
                
            except Exception as e:
                print(f"Warning: Failed to load config from {config_path}: {e}", file=sys.stderr)
                print("Using default configuration", file=sys.stderr)
        
        return self.DEFAULT_CONFIG.copy()
    
    def _deep_merge(self, base, update):
        """Deep merge two dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
    
    def save_config(self):
        """Save current configuration to file."""
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            print(f"Configuration saved to {config_path}")
        except Exception as e:
            print(f"Error saving config to {config_path}: {e}", file=sys.stderr)
    
    def get(self, path, default=None):
        """
        Get configuration value using dot notation.
        
        Args:
            path: Dot-separated path (e.g., 'audio.sample_rate')
            default: Default value if path not found
            
        Returns:
            Configuration value or default
        """
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, path, value):
        """
        Set configuration value using dot notation.
        
        Args:
            path: Dot-separated path (e.g., 'audio.sample_rate')
            value: Value to set
        """
        keys = path.split('.')
        config = self.config
        
        # Navigate to the parent dict
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the final value
        config[keys[-1]] = value
    
    def get_audio_config(self):
        """Get audio recording configuration."""
        return self.config['audio']
    
    def get_recording_config(self):
        """Get recording behavior configuration."""
        return self.config['recording']
    
    def get_stt_config(self):
        """Get speech-to-text configuration."""
        return self.config['stt']
    
    def get_preprocessing_config(self):
        """Get preprocessing configuration."""
        return self.config['preprocessing']
    
    def get_listening_config(self):
        """Get continuous listening configuration."""
        return self.config['listening']
    
    def get_feedback_config(self):
        """Get user feedback configuration."""
        return self.config['feedback']
    
    def validate_config(self):
        """
        Validate configuration values.
        
        Returns:
            tuple: (is_valid, error_messages)
        """
        errors = []
        
        # Validate audio settings
        audio = self.config['audio']
        if audio['sample_rate'] not in [8000, 16000, 22050, 44100, 48000]:
            errors.append(f"Invalid sample_rate: {audio['sample_rate']}")
        
        if audio['channels'] not in [1, 2]:
            errors.append(f"Invalid channels: {audio['channels']}")
        
        if audio['format_bits'] not in [16, 24, 32]:
            errors.append(f"Invalid format_bits: {audio['format_bits']}")
        
        # Validate recording settings
        recording = self.config['recording']
        if recording['default_duration'] <= 0 or recording['default_duration'] > 300:
            errors.append(f"Invalid default_duration: {recording['default_duration']}")
        
        if recording['silence_threshold'] < 0 or recording['silence_threshold'] > 1:
            errors.append(f"Invalid silence_threshold: {recording['silence_threshold']}")
        
        # Validate listening settings
        listening = self.config['listening']
        if listening['max_session_minutes'] <= 0 or listening['max_session_minutes'] > 480:
            errors.append(f"Invalid max_session_minutes: {listening['max_session_minutes']}")
        
        return len(errors) == 0, errors

def main():
    """Command-line interface for voice configuration."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Voice configuration manager')
    parser.add_argument('--config', type=str, help='Configuration file path')
    parser.add_argument('--show', action='store_true', help='Show current configuration')
    parser.add_argument('--validate', action='store_true', help='Validate configuration')
    parser.add_argument('--create-default', action='store_true', help='Create default configuration file')
    parser.add_argument('--get', type=str, help='Get configuration value (dot notation)')
    parser.add_argument('--set', type=str, nargs=2, metavar=('PATH', 'VALUE'),
                        help='Set configuration value (path value)')
    
    args = parser.parse_args()
    
    config = VoiceConfig(args.config)
    
    if args.create_default:
        config.save_config()
        print("Default configuration created")
        return
    
    if args.validate:
        is_valid, errors = config.validate_config()
        if is_valid:
            print("✅ Configuration is valid")
        else:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        return
    
    if args.get:
        value = config.get(args.get)
        if value is not None:
            print(value)
        else:
            print(f"Configuration path '{args.get}' not found", file=sys.stderr)
            sys.exit(1)
        return
    
    if args.set:
        path, value = args.set
        # Try to parse value as YAML
        try:
            parsed_value = yaml.safe_load(value)
        except:
            parsed_value = value
        
        config.set(path, parsed_value)
        config.save_config()
        print(f"Set {path} = {parsed_value}")
        return
    
    if args.show:
        print(yaml.dump(config.config, default_flow_style=False, indent=2))
        return
    
    # Default: show help
    parser.print_help()

if __name__ == "__main__":
    main()