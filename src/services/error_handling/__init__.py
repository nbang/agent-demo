"""Error Handling Services for Agno Agent System

Provides robust error handling, retry logic, and recovery strategies
that can be used across all agent types and services.
"""

from .handler import (
    ErrorHandler,
    ErrorContext,
    RetryConfig,
    RecoveryConfig,
    ErrorSeverity,
    ErrorCategory,
    RecoveryStrategy,
    create_team_error_handler,
    default_error_handler
)

__all__ = [
    'ErrorHandler',
    'ErrorContext',
    'RetryConfig',
    'RecoveryConfig',
    'ErrorSeverity',
    'ErrorCategory',
    'RecoveryStrategy',
    'create_team_error_handler',
    'default_error_handler'
]