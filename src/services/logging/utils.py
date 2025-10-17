"""Enhanced Logging Utilities for Agno Agent System

Provides structured logging with context, filtering, and formatting
capabilities that can be used across all agent types and services.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from logging.handlers import RotatingFileHandler


# Custom log levels
TRACE = 5  # More detailed than DEBUG
logging.addLevelName(TRACE, "TRACE")


class ContextFilter(logging.Filter):
    """Add context information to log records."""
    
    def __init__(self, context: Optional[Dict[str, Any]] = None):
        """Initialize context filter.
        
        Args:
            context: Context dictionary to add to logs
        """
        super().__init__()
        self.context = context or {}
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add context to record."""
        for key, value in self.context.items():
            setattr(record, key, value)
        return True


class AgentLogger(logging.LoggerAdapter):
    """Logger adapter with agent-specific context."""
    
    def __init__(
        self,
        logger: logging.Logger,
        agent_type: Optional[str] = None,
        agent_id: Optional[str] = None,
        team_id: Optional[str] = None
    ):
        """Initialize agent logger.
        
        Args:
            logger: Base logger
            agent_type: Type of agent (e.g., 'basic', 'multi_agent', 'reasoning')
            agent_id: Optional agent identifier
            team_id: Optional team identifier (for multi-agent systems)
        """
        extra = {}
        if agent_type:
            extra['agent_type'] = agent_type
        if agent_id:
            extra['agent_id'] = agent_id
        if team_id:
            extra['team_id'] = team_id
        
        super().__init__(logger, extra)
    
    def trace(self, msg: str, *args, **kwargs):
        """Log at TRACE level."""
        self.log(TRACE, msg, *args, **kwargs)


class ColoredFormatter(logging.Formatter):
    """Colored console output formatter."""
    
    # ANSI color codes
    COLORS = {
        'TRACE': '\033[36m',      # Cyan
        'DEBUG': '\033[34m',      # Blue
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format with colors."""
        # Add color
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            )
        
        # Format message
        result = super().format(record)
        
        # Reset levelname for potential reuse
        record.levelname = levelname
        
        return result


def setup_advanced_logging(
    logger_name: str = "agno",
    log_level: str = "INFO",
    log_to_file: bool = True,
    log_file: str = "logs/agno.log",
    log_to_console: bool = True,
    use_colors: bool = True,
    max_file_size_mb: int = 10,
    backup_count: int = 5,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Setup comprehensive logging for the Agno system.
    
    Args:
        logger_name: Base logger name (default: "agno")
        log_level: Logging level (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Enable file logging
        log_file: Path to log file
        log_to_console: Enable console logging
        use_colors: Use colored output for console
        max_file_size_mb: Maximum log file size in MB
        backup_count: Number of backup log files to keep
        format_string: Custom format string
    
    Returns:
        Configured root logger
    """
    # Get root logger
    root_logger = logging.getLogger(logger_name)
    
    # Set level
    level = getattr(logging, log_level.upper(), logging.INFO)
    root_logger.setLevel(level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Default format
    if format_string is None:
        format_string = (
            "%(asctime)s | %(levelname)-8s | "
            "%(name)s | %(message)s"
        )
    
    # Add agent context if available
    detailed_format = (
        "%(asctime)s | %(levelname)-8s | "
        "%(name)s"
    )
    
    # Add agent_type if present
    if hasattr(logging.LogRecord, 'agent_type'):
        detailed_format += " | Type:%(agent_type)s"
    
    # Add team_id if present
    if hasattr(logging.LogRecord, 'team_id'):
        detailed_format += " | Team:%(team_id)s"
    
    # Add agent_id if present
    if hasattr(logging.LogRecord, 'agent_id'):
        detailed_format += " | Agent:%(agent_id)s"
    
    detailed_format += " | %(message)s"
    
    # File handler
    if log_to_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=max_file_size_mb * 1024 * 1024,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        
        file_formatter = logging.Formatter(
            detailed_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Console handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        if use_colors and sys.stdout.isatty():
            console_formatter = ColoredFormatter(
                format_string,
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            console_formatter = logging.Formatter(
                format_string,
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # Log startup message
    root_logger.info("="*70)
    root_logger.info(f"Agno Agent Logging Initialized - Level: {log_level}")
    root_logger.info(f"Log File: {log_file if log_to_file else 'Disabled'}")
    root_logger.info(f"Console: {'Enabled' if log_to_console else 'Disabled'}")
    root_logger.info("="*70)
    
    return root_logger


def get_agent_logger(
    name: str,
    agent_type: Optional[str] = None,
    agent_id: Optional[str] = None,
    team_id: Optional[str] = None
) -> AgentLogger:
    """Get an agent-specific logger.
    
    Args:
        name: Logger name (usually __name__)
        agent_type: Type of agent (e.g., 'basic', 'multi_agent', 'reasoning')
        agent_id: Optional agent identifier
        team_id: Optional team identifier
    
    Returns:
        AgentLogger instance
    """
    base_logger = logging.getLogger(name)
    return AgentLogger(base_logger, agent_type, agent_id, team_id)


def get_team_logger(
    name: str,
    team_id: Optional[str] = None,
    agent_id: Optional[str] = None
) -> AgentLogger:
    """Get a team-specific logger (backward compatibility for multi-agent).
    
    Args:
        name: Logger name (usually __name__)
        team_id: Optional team identifier
        agent_id: Optional agent identifier
    
    Returns:
        AgentLogger instance
    """
    return get_agent_logger(name, "multi_agent", agent_id, team_id)


def setup_multi_agent_logging(
    log_level: str = "INFO",
    log_to_file: bool = True,
    log_file: str = "logs/multi_agent.log",
    log_to_console: bool = True,
    use_colors: bool = True,
    max_file_size_mb: int = 10,
    backup_count: int = 5,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Setup logging for multi-agent system (backward compatibility).
    
    Args:
        log_level: Logging level (TRACE, DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Enable file logging
        log_file: Path to log file
        log_to_console: Enable console logging
        use_colors: Use colored output for console
        max_file_size_mb: Maximum log file size in MB
        backup_count: Number of backup log files to keep
        format_string: Custom format string
    
    Returns:
        Configured logger
    """
    return setup_advanced_logging(
        "multi_agent", log_level, log_to_file, log_file,
        log_to_console, use_colors, max_file_size_mb,
        backup_count, format_string
    )


def log_operation_start(
    logger: logging.Logger,
    operation: str,
    **kwargs
):
    """Log operation start with context.
    
    Args:
        logger: Logger instance
        operation: Operation name
        **kwargs: Additional context
    """
    context = " | ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.info(f"▶️  START: {operation}" + (f" | {context}" if context else ""))


def log_operation_end(
    logger: logging.Logger,
    operation: str,
    success: bool = True,
    duration_seconds: Optional[float] = None,
    **kwargs
):
    """Log operation end with context.
    
    Args:
        logger: Logger instance
        operation: Operation name
        success: Whether operation succeeded
        duration_seconds: Operation duration
        **kwargs: Additional context
    """
    status = "✅ SUCCESS" if success else "❌ FAILED"
    context_parts = []
    
    if duration_seconds is not None:
        context_parts.append(f"duration={duration_seconds:.2f}s")
    
    for k, v in kwargs.items():
        context_parts.append(f"{k}={v}")
    
    context = " | ".join(context_parts)
    
    log_func = logger.info if success else logger.error
    log_func(f"⏹️  END: {operation} | {status}" + (f" | {context}" if context else ""))


def log_metric(
    logger: logging.Logger,
    metric_name: str,
    metric_value: Any,
    unit: Optional[str] = None
):
    """Log a metric value.
    
    Args:
        logger: Logger instance
        metric_name: Metric name
        metric_value: Metric value
        unit: Optional unit
    """
    value_str = f"{metric_value:.2f}" if isinstance(metric_value, float) else str(metric_value)
    unit_str = f" {unit}" if unit else ""
    logger.debug(f"📊 METRIC: {metric_name} = {value_str}{unit_str}")


def log_interaction(
    logger: logging.Logger,
    from_agent: str,
    to_agent: str,
    interaction_type: str,
    summary: Optional[str] = None
):
    """Log agent interaction.
    
    Args:
        logger: Logger instance
        from_agent: Source agent
        to_agent: Target agent
        interaction_type: Type of interaction
        summary: Optional summary
    """
    message = f"🔄 INTERACTION: {from_agent} → {to_agent} | Type: {interaction_type}"
    if summary:
        message += f" | {summary}"
    logger.debug(message)


def log_error_with_context(
    logger: logging.Logger,
    error: Exception,
    operation: str,
    **context
):
    """Log error with full context.
    
    Args:
        logger: Logger instance
        error: Exception
        operation: Operation that failed
        **context: Additional context
    """
    context_str = " | ".join(f"{k}={v}" for k, v in context.items())
    logger.error(
        f"❌ ERROR in {operation}: {type(error).__name__}: {error}" +
        (f" | Context: {context_str}" if context_str else ""),
        exc_info=True
    )


# Context manager for operation logging
class LoggedOperation:
    """Context manager for logging operations."""
    
    def __init__(
        self,
        logger: logging.Logger,
        operation: str,
        **context
    ):
        """Initialize logged operation.
        
        Args:
            logger: Logger instance
            operation: Operation name
            **context: Additional context
        """
        self.logger = logger
        self.operation = operation
        self.context = context
        self.start_time = None
        self.success = False
    
    def __enter__(self):
        """Enter context - log start."""
        self.start_time = datetime.now()
        log_operation_start(self.logger, self.operation, **self.context)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - log end."""
        duration = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0.0
        self.success = exc_type is None
        
        if exc_val:
            log_error_with_context(
                self.logger,
                exc_val,
                self.operation,
                **self.context
            )
        
        log_operation_end(
            self.logger,
            self.operation,
            self.success,
            duration,
            **self.context
        )
        
        return False  # Don't suppress exceptions