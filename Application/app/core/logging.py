"""
Application Logging Configuration

This module configures the application's logging system, including:
- File and console logging handlers
- Log rotation settings
- Log formatting
- Directory structure setup

Author: Marco Alejandro Santiago
Created: February 7, 2025
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

def setup_logging():
    """
    Configure and initialize the application logging system.
    
    Returns:
        logger: Configured logging instance with both file and console handlers
    """
    # Initialize application logger
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    # Configure rotating file handler
    # - Rotates log files when size reaches 1MB
    # - Keeps up to 5 backup files
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    
    # Configure console handler for terminal output
    console_handler = logging.StreamHandler()

    # Define log message format
    # Format: timestamp - logger_name - log_level - message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Apply formatter to both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Attach both handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger