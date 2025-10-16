"""Multi-Agent Team Error Handling Module

Provides robust error handling, retry logic, and recovery strategies
for multi-agent team operations.
"""

from .team_error_handler import (
    TeamErrorHandler,
    ErrorContext,
    ErrorSeverity,
    ErrorCategory,
    RecoveryStrategy,
    RetryConfig,
    RecoveryResult,
    with_retry,
    create_error_handler
)

__all__ = [
    "TeamErrorHandler",
    "ErrorContext",
    "ErrorSeverity",
    "ErrorCategory",
    "RecoveryStrategy",
    "RetryConfig",
    "RecoveryResult",
    "with_retry",
    "create_error_handler"
]
