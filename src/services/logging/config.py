"""Logging Configuration for Agno Agent System

Provides centralized logging configuration that can be used across all agent types
and services in the Agno framework.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    logger_name: str = "agno",
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """Set up logging for the Agno agent system.
    
    Args:
        logger_name: Base name for the logger (default: "agno")
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        log_format: Optional custom log format string
        
    Returns:
        Configured logger instance
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str, base_name: str = "agno") -> logging.Logger:
    """Get a logger instance for components.
    
    Args:
        name: Name for the logger (e.g., 'agent', 'workflow', 'multi_agent')
        base_name: Base logger name (default: "agno")
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"{base_name}.{name}")


def setup_multi_agent_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """Set up logging for multi-agent system (backward compatibility).
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        log_format: Optional custom log format string
        
    Returns:
        Configured logger instance
    """
    return setup_logging("multi_agent", log_level, log_file, log_format)


def get_multi_agent_logger(name: str) -> logging.Logger:
    """Get a logger instance for multi-agent components (backward compatibility).
    
    Args:
        name: Name for the logger (e.g., 'team_manager', 'workflow')
        
    Returns:
        Logger instance
    """
    return get_logger(name, "multi_agent")


# Default logger instances
logger = get_logger("core")
multi_agent_logger = get_multi_agent_logger("core")