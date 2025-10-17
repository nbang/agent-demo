"""Logging Services for Agno Agent System

Provides centralized logging configuration and utilities that can be used
across all agent types and services.
"""

from .config import (
    setup_logging,
    get_logger,
    setup_multi_agent_logging,  # backward compatibility
    get_multi_agent_logger,     # backward compatibility
    logger,
    multi_agent_logger
)

from .utils import (
    setup_advanced_logging,
    get_agent_logger,
    get_team_logger,           # backward compatibility
    log_operation_start,
    log_operation_end,
    log_metric,
    log_interaction,
    log_error_with_context,
    LoggedOperation,
    AgentLogger,
    ContextFilter,
    ColoredFormatter,
    TRACE
)

__all__ = [
    # Config functions
    'setup_logging',
    'get_logger',
    'setup_multi_agent_logging',
    'get_multi_agent_logger',
    'logger',
    'multi_agent_logger',
    
    # Utils functions and classes
    'setup_advanced_logging',
    'get_agent_logger',
    'get_team_logger',
    'log_operation_start',
    'log_operation_end',
    'log_metric',
    'log_interaction',
    'log_error_with_context',
    'LoggedOperation',
    'AgentLogger',
    'ContextFilter',
    'ColoredFormatter',
    'TRACE'
]