"""
Comprehensive logging module for Gesture AI Agent
Provides structured logging with file and console output
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional
from config import get_config


class LoggerManager:
    """Centralized logger management"""

    _loggers: dict = {}
    _configured: bool = False

    @classmethod
    def setup(cls, config=None) -> None:
        """
        Setup logging configuration

        Args:
            config: Configuration object (uses global config if None)
        """
        if cls._configured:
            return

        if config is None:
            config = get_config()

        log_config = config.logging

        # Create logs directory if needed
        log_dir = os.path.dirname(log_config.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_config.level, logging.INFO))

        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File handler
        if log_config.log_to_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_config.log_file,
                maxBytes=log_config.max_bytes,
                backupCount=log_config.backup_count,
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        # Console handler
        if log_config.log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        cls._configured = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get logger instance for a module

        Args:
            name: Logger name (typically __name__)

        Returns:
            Logger instance
        """
        if not cls._configured:
            cls.setup()

        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)

        return cls._loggers[name]


# Convenience function
def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return LoggerManager.get_logger(name)
