"""
Configuration management module for Gesture AI Agent
Centralized configuration for all modules and settings
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
import json
import os
from pathlib import Path


@dataclass
class CameraConfig:
    """Camera settings"""
    width: int = 1280
    height: int = 720
    fps: int = 30
    device_id: int = 0
    retry_count: int = 3
    retry_delay: float = 1.0


@dataclass
class GestureConfig:
    """Gesture detection settings"""
    enable_hand_gestures: bool = True
    enable_body_gestures: bool = True
    hand_confidence_threshold: float = 0.7
    body_confidence_threshold: float = 0.7
    gesture_buffer_size: int = 5
    min_hold_frames: int = 3
    gesture_cooldown: float = 2.0


@dataclass
class FacialConfig:
    """Facial detection settings"""
    enable_facial_detection: bool = True
    enable_mood_detection: bool = True
    enable_blink_detection: bool = True
    blink_cooldown: float = 3.0
    mood_cooldown: float = 5.0
    mood_confidence_threshold: float = 0.6


@dataclass
class VoiceConfig:
    """Voice command settings"""
    enable_voice_commands: bool = True
    recognition_language: str = "en-US"
    voice_enabled_by_default: bool = False
    microphone_device_index: Optional[int] = None
    timeout: float = 10.0
    phrase_time_limit: float = 5.0


@dataclass
class AudioConfig:
    """Audio output settings"""
    enable_text_to_speech: bool = False
    speech_rate: int = 150
    speech_volume: float = 0.9
    enable_mood_music: bool = True
    music_base_path: str = "music_library"


@dataclass
class LoggingConfig:
    """Logging settings"""
    level: str = "INFO"
    log_file: str = "gesture_ai.log"
    max_bytes: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    log_to_console: bool = True
    log_to_file: bool = True


@dataclass
class ActionConfig:
    """Action execution settings"""
    max_log_size: int = 100
    action_log_file: str = "action_log.json"
    mood_log_file: str = "mood_log.txt"
    notes_directory: str = "notes"
    screenshot_directory: str = "screenshots"


class Config:
    """Global configuration manager"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration

        Args:
            config_path: Path to custom config file (optional)
        """
        self.camera = CameraConfig()
        self.gesture = GestureConfig()
        self.facial = FacialConfig()
        self.voice = VoiceConfig()
        self.audio = AudioConfig()
        self.logging = LoggingConfig()
        self.action = ActionConfig()

        # Load custom config if provided
        if config_path and os.path.exists(config_path):
            self.load_from_file(config_path)

    def load_from_file(self, config_path: str) -> None:
        """Load configuration from JSON file"""
        try:
            with open(config_path, "r") as f:
                data = json.load(f)

            for section, config_obj in [
                ("camera", self.camera),
                ("gesture", self.gesture),
                ("facial", self.facial),
                ("voice", self.voice),
                ("audio", self.audio),
                ("logging", self.logging),
                ("action", self.action),
            ]:
                if section in data:
                    for key, value in data[section].items():
                        if hasattr(config_obj, key):
                            setattr(config_obj, key, value)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")

    def save_to_file(self, config_path: str) -> None:
        """Save configuration to JSON file"""
        try:
            data = {
                "camera": asdict(self.camera),
                "gesture": asdict(self.gesture),
                "facial": asdict(self.facial),
                "voice": asdict(self.voice),
                "audio": asdict(self.audio),
                "logging": asdict(self.logging),
                "action": asdict(self.action),
            }
            with open(config_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "camera": asdict(self.camera),
            "gesture": asdict(self.gesture),
            "facial": asdict(self.facial),
            "voice": asdict(self.voice),
            "audio": asdict(self.audio),
            "logging": asdict(self.logging),
            "action": asdict(self.action),
        }


# Global config instance
_config = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or create global config instance"""
    global _config
    if _config is None:
        _config = Config(config_path)
    return _config


def reset_config() -> None:
    """Reset global config (useful for testing)"""
    global _config
    _config = None
