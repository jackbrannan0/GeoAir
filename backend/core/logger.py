"""Centralized logging configuration"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Create and configure a logger with console output.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already done
    if not logger.handlers:
        logger.setLevel(getattr(logging, level))
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level))
        
        # Formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger


# Global logger instance
logger = get_logger("geoair")
