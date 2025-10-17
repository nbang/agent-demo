"""Error Handling and Recovery for Agno Agent System

Provides robust error handling with retry logic, fallback strategies,
and graceful degradation for agent operations across all agent types.
"""

import logging
import time
import traceback
import random
from typing import Callable, Any, Optional, Dict, List, Type, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from functools import wraps


logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Severity levels for errors."""
    LOW = "low"  # Minor issue, can continue
    MEDIUM = "medium"  # Significant issue, may need retry
    HIGH = "high"  # Critical issue, requires intervention
    CRITICAL = "critical"  # System-threatening, immediate action needed


class ErrorCategory(Enum):
    """Categories of errors that can occur."""
    NETWORK = "network"  # Network/API connectivity issues
    TIMEOUT = "timeout"  # Operation timeout
    VALIDATION = "validation"  # Data validation errors
    RESOURCE = "resource"  # Resource exhaustion (memory, CPU)
    AGENT = "agent"  # Agent-specific errors
    COORDINATION = "coordination"  # Multi-agent coordination failures
    CONFIGURATION = "configuration"  # Configuration errors
    API = "api"  # External API errors
    AUTHENTICATION = "authentication"  # Auth/permission errors
    DATA = "data"  # Data processing errors
    UNKNOWN = "unknown"  # Unclassified errors


class RecoveryStrategy(Enum):
    """Recovery strategies for handling errors."""
    RETRY = "retry"  # Retry the operation
    FALLBACK = "fallback"  # Use alternative approach
    SKIP = "skip"  # Skip and continue
    ABORT = "abort"  # Abort operation
    ESCALATE = "escalate"  # Escalate to human/higher level
    IGNORE = "ignore"  # Ignore and log only


@dataclass
class ErrorContext:
    """Context information about an error."""
    
    error_type: Type[Exception]
    error_message: str
    error_traceback: str
    timestamp: datetime
    operation_id: str
    agent_type: Optional[str] = None
    agent_id: Optional[str] = None
    team_id: Optional[str] = None  # For multi-agent systems
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.UNKNOWN
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "error_type": self.error_type.__name__,
            "error_message": self.error_message,
            "error_traceback": self.error_traceback,
            "timestamp": self.timestamp.isoformat(),
            "operation_id": self.operation_id,
            "agent_type": self.agent_type,
            "agent_id": self.agent_id,
            "team_id": self.team_id,
            "severity": self.severity.value,
            "category": self.category.value,
            "metadata": self.metadata
        }


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    
    max_attempts: int = 3
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    exponential_backoff: bool = True
    backoff_factor: float = 2.0
    jitter: bool = True  # Add random jitter to delays
    retry_on_exceptions: tuple = (Exception,)
    
    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number.
        
        Args:
            attempt: Attempt number (0-indexed)
        
        Returns:
            Delay in seconds
        """
        if attempt == 0:
            return 0.0
        
        if self.exponential_backoff:
            delay = self.initial_delay_seconds * (self.backoff_factor ** (attempt - 1))
        else:
            delay = self.initial_delay_seconds
        
        # Apply maximum delay
        delay = min(delay, self.max_delay_seconds)
        
        # Add jitter
        if self.jitter:
            delay = delay * (0.5 + random.random() * 0.5)
        
        return delay


@dataclass
class RecoveryConfig:
    """Configuration for error recovery."""
    
    strategy: RecoveryStrategy = RecoveryStrategy.RETRY
    fallback_function: Optional[Callable] = None
    escalation_handler: Optional[Callable] = None
    max_escalations: int = 1
    auto_recovery: bool = True
    recovery_timeout_seconds: float = 300.0  # 5 minutes
    
    def should_retry(self, error: Exception, attempt: int, max_attempts: int) -> bool:
        """Determine if operation should be retried.
        
        Args:
            error: The error that occurred
            attempt: Current attempt number (0-indexed)
            max_attempts: Maximum number of attempts
        
        Returns:
            Whether to retry
        """
        if self.strategy != RecoveryStrategy.RETRY:
            return False
        
        if attempt >= max_attempts - 1:
            return False
        
        # Add custom logic here based on error type
        return True


class ErrorHandler:
    """Generic error handler for agent operations."""
    
    def __init__(
        self,
        agent_type: str = "generic",
        agent_id: Optional[str] = None,
        team_id: Optional[str] = None
    ):
        """Initialize error handler.
        
        Args:
            agent_type: Type of agent (e.g., 'basic', 'multi_agent', 'reasoning')
            agent_id: Optional agent identifier
            team_id: Optional team identifier
        """
        self.agent_type = agent_type
        self.agent_id = agent_id
        self.team_id = team_id
        self.error_history: List[ErrorContext] = []
        self.recovery_configs: Dict[Type[Exception], RecoveryConfig] = {}
        self.retry_configs: Dict[str, RetryConfig] = {
            'default': RetryConfig()
        }
        
        # Setup default recovery strategies
        self._setup_default_recovery_strategies()
    
    def _setup_default_recovery_strategies(self):
        """Setup default error recovery strategies."""
        # Network errors - retry with exponential backoff
        self.recovery_configs[ConnectionError] = RecoveryConfig(
            strategy=RecoveryStrategy.RETRY
        )
        
        # Timeout errors - retry with shorter timeout
        self.recovery_configs[TimeoutError] = RecoveryConfig(
            strategy=RecoveryStrategy.RETRY
        )
        
        # Validation errors - usually don't retry
        self.recovery_configs[ValueError] = RecoveryConfig(
            strategy=RecoveryStrategy.ESCALATE
        )
        
        # Permission errors - escalate
        self.recovery_configs[PermissionError] = RecoveryConfig(
            strategy=RecoveryStrategy.ESCALATE
        )
    
    def add_retry_config(self, operation_name: str, config: RetryConfig):
        """Add retry configuration for specific operation.
        
        Args:
            operation_name: Name of the operation
            config: Retry configuration
        """
        self.retry_configs[operation_name] = config
    
    def add_recovery_config(self, exception_type: Type[Exception], config: RecoveryConfig):
        """Add recovery configuration for specific exception type.
        
        Args:
            exception_type: Exception type
            config: Recovery configuration
        """
        self.recovery_configs[exception_type] = config
    
    def handle_error(
        self,
        error: Exception,
        operation_id: str,
        operation_name: str = "unknown",
        metadata: Optional[Dict[str, Any]] = None
    ) -> ErrorContext:
        """Handle an error and create error context.
        
        Args:
            error: The error that occurred
            operation_id: Unique identifier for the operation
            operation_name: Name of the operation
            metadata: Additional metadata
        
        Returns:
            ErrorContext with error details
        """
        error_context = ErrorContext(
            error_type=type(error),
            error_message=str(error),
            error_traceback=traceback.format_exc(),
            timestamp=datetime.now(),
            operation_id=operation_id,
            agent_type=self.agent_type,
            agent_id=self.agent_id,
            team_id=self.team_id,
            severity=self._classify_severity(error),
            category=self._classify_category(error),
            metadata=metadata or {}
        )
        
        # Add to error history
        self.error_history.append(error_context)
        
        # Log error
        logger.error(
            f"Error in {operation_name} (ID: {operation_id}): {error}",
            extra={
                "error_context": error_context.to_dict(),
                "agent_type": self.agent_type,
                "agent_id": self.agent_id,
                "team_id": self.team_id
            },
            exc_info=True
        )
        
        return error_context
    
    def _classify_severity(self, error: Exception) -> ErrorSeverity:
        """Classify error severity.
        
        Args:
            error: The error to classify
        
        Returns:
            Error severity
        """
        # Critical system errors
        if isinstance(error, (SystemExit, KeyboardInterrupt, MemoryError)):
            return ErrorSeverity.CRITICAL
        
        # High severity errors
        if isinstance(error, (PermissionError, FileNotFoundError)):
            return ErrorSeverity.HIGH
        
        # Medium severity errors
        if isinstance(error, (ConnectionError, TimeoutError, ValueError)):
            return ErrorSeverity.MEDIUM
        
        # Default to low for unknown errors
        return ErrorSeverity.LOW
    
    def _classify_category(self, error: Exception) -> ErrorCategory:
        """Classify error category.
        
        Args:
            error: The error to classify
        
        Returns:
            Error category
        """
        if isinstance(error, (ConnectionError, OSError)):
            return ErrorCategory.NETWORK
        
        if isinstance(error, TimeoutError):
            return ErrorCategory.TIMEOUT
        
        if isinstance(error, (ValueError, TypeError)):
            return ErrorCategory.VALIDATION
        
        if isinstance(error, (MemoryError, ResourceWarning)):
            return ErrorCategory.RESOURCE
        
        if isinstance(error, PermissionError):
            return ErrorCategory.AUTHENTICATION
        
        return ErrorCategory.UNKNOWN
    
    def with_retry(
        self,
        operation_name: str = "default",
        operation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Decorator for automatic retry with error handling.
        
        Args:
            operation_name: Name of the operation
            operation_id: Optional operation identifier
            metadata: Additional metadata
        
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                config = self.retry_configs.get(operation_name, self.retry_configs['default'])
                op_id = operation_id or f"{func.__name__}_{int(time.time())}"
                
                for attempt in range(config.max_attempts):
                    try:
                        result = func(*args, **kwargs)
                        if attempt > 0:
                            logger.info(
                                f"Operation {func.__name__} succeeded on attempt {attempt + 1}",
                                extra={
                                    "operation_id": op_id,
                                    "attempt": attempt + 1,
                                    "agent_type": self.agent_type
                                }
                            )
                        return result
                    
                    except Exception as e:
                        error_context = self.handle_error(e, op_id, operation_name, metadata)
                        
                        # Check if we should retry
                        if attempt < config.max_attempts - 1 and isinstance(e, config.retry_on_exceptions):
                            delay = config.get_delay(attempt)
                            logger.warning(
                                f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s",
                                extra={
                                    "operation_id": op_id,
                                    "attempt": attempt + 1,
                                    "delay": delay,
                                    "agent_type": self.agent_type
                                }
                            )
                            if delay > 0:
                                time.sleep(delay)
                            continue
                        
                        # No more retries, handle according to recovery strategy
                        recovery_config = self.recovery_configs.get(type(e))
                        if recovery_config:
                            return self._execute_recovery_strategy(
                                e, error_context, recovery_config, func, args, kwargs
                            )
                        
                        # Re-raise if no recovery strategy
                        raise
                
                # Should not reach here
                raise RuntimeError(f"Retry logic failed for {operation_name}")
            
            return wrapper
        return decorator
    
    def _execute_recovery_strategy(
        self,
        error: Exception,
        error_context: ErrorContext,
        recovery_config: RecoveryConfig,
        func: Callable,
        args: tuple,
        kwargs: dict
    ) -> Any:
        """Execute recovery strategy for an error.
        
        Args:
            error: The original error
            error_context: Error context
            recovery_config: Recovery configuration
            func: Original function
            args: Function arguments
            kwargs: Function keyword arguments
        
        Returns:
            Result from recovery strategy
        """
        strategy = recovery_config.strategy
        
        if strategy == RecoveryStrategy.FALLBACK and recovery_config.fallback_function:
            logger.info(f"Executing fallback for {func.__name__}")
            return recovery_config.fallback_function(*args, **kwargs)
        
        elif strategy == RecoveryStrategy.SKIP:
            logger.warning(f"Skipping operation {func.__name__} due to error")
            return None
        
        elif strategy == RecoveryStrategy.ESCALATE and recovery_config.escalation_handler:
            logger.warning(f"Escalating error for {func.__name__}")
            return recovery_config.escalation_handler(error, error_context)
        
        elif strategy == RecoveryStrategy.IGNORE:
            logger.warning(f"Ignoring error for {func.__name__}: {error}")
            return None
        
        else:  # ABORT or no valid strategy
            logger.error(f"Aborting operation {func.__name__} due to error")
            raise error
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics.
        
        Returns:
            Dictionary with error statistics
        """
        if not self.error_history:
            return {"total_errors": 0}
        
        total_errors = len(self.error_history)
        
        # Count by severity
        severity_counts = {}
        for severity in ErrorSeverity:
            severity_counts[severity.value] = sum(
                1 for ctx in self.error_history if ctx.severity == severity
            )
        
        # Count by category
        category_counts = {}
        for category in ErrorCategory:
            category_counts[category.value] = sum(
                1 for ctx in self.error_history if ctx.category == category
            )
        
        # Recent errors (last hour)
        recent_threshold = datetime.now().timestamp() - 3600
        recent_errors = sum(
            1 for ctx in self.error_history 
            if ctx.timestamp.timestamp() > recent_threshold
        )
        
        return {
            "total_errors": total_errors,
            "recent_errors": recent_errors,
            "severity_breakdown": severity_counts,
            "category_breakdown": category_counts,
            "error_rate": recent_errors / 60 if recent_errors > 0 else 0.0  # per minute
        }
    
    def clear_error_history(self):
        """Clear error history."""
        self.error_history.clear()
        logger.info("Error history cleared")


# Convenience functions for backward compatibility
def create_team_error_handler(team_id: str, agent_id: Optional[str] = None) -> ErrorHandler:
    """Create error handler for multi-agent team (backward compatibility).
    
    Args:
        team_id: Team identifier
        agent_id: Optional agent identifier
    
    Returns:
        ErrorHandler instance
    """
    return ErrorHandler("multi_agent", agent_id, team_id)


# Global error handler instance
default_error_handler = ErrorHandler()