import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging
def setup_logging():
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    console_handler = logging.StreamHandler()

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger