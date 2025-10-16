"""Error Handling and Recovery for Multi-Agent Teams

Provides robust error handling with retry logic, fallback strategies,
and graceful degradation for multi-agent team operations.
"""

import logging
import time
import traceback
from typing import Callable, Any, Optional, Dict, List, Type
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
    COORDINATION = "coordination"  # Team coordination failures
    CONFIGURATION = "configuration"  # Configuration errors
    UNKNOWN = "unknown"  # Unclassified errors


class RecoveryStrategy(Enum):
    """Recovery strategies for handling errors."""
    RETRY = "retry"  # Retry the operation
    FALLBACK = "fallback"  # Use alternative approach
    SKIP = "skip"  # Skip and continue
    ABORT = "abort"  # Abort operation
    ESCALATE = "escalate"  # Escalate to human/higher level


@dataclass
class ErrorContext:
    """Context information about an error."""
    
    error_type: Type[Exception]
    error_message: str
    error_traceback: str
    timestamp: datetime
    operation_id: str
    agent_id: Optional[str] = None
    team_id: Optional[str] = None
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
        if self.exponential_backoff:
            delay = self.initial_delay_seconds * (self.backoff_factor ** attempt)
        else:
            delay = self.initial_delay_seconds
        
        # Cap at max delay
        delay = min(delay, self.max_delay_seconds)
        
        # Add jitter if enabled
        if self.jitter:
            import random
            jitter_amount = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_amount, jitter_amount)
        
        return max(0, delay)


@dataclass
class RecoveryResult:
    """Result of an error recovery attempt."""
    
    success: bool
    strategy_used: RecoveryStrategy
    attempts_made: int
    total_time_seconds: float
    final_result: Any = None
    final_error: Optional[ErrorContext] = None
    recovery_log: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "strategy_used": self.strategy_used.value,
            "attempts_made": self.attempts_made,
            "total_time_seconds": self.total_time_seconds,
            "final_result": str(self.final_result) if self.final_result else None,
            "final_error": self.final_error.to_dict() if self.final_error else None,
            "recovery_log": self.recovery_log
        }


class TeamErrorHandler:
    """Handles errors and implements recovery strategies for multi-agent teams."""
    
    def __init__(
        self,
        team_id: str,
        default_retry_config: Optional[RetryConfig] = None,
        enable_fallbacks: bool = True,
        enable_logging: bool = True
    ):
        """Initialize error handler.
        
        Args:
            team_id: Team identifier
            default_retry_config: Default retry configuration
            enable_fallbacks: Enable fallback strategies
            enable_logging: Enable error logging
        """
        self.team_id = team_id
        self.default_retry_config = default_retry_config or RetryConfig()
        self.enable_fallbacks = enable_fallbacks
        self.enable_logging = enable_logging
        
        # Error tracking
        self.error_history: List[ErrorContext] = []
        self.recovery_history: List[RecoveryResult] = []
        
        # Fallback handlers
        self.fallback_handlers: Dict[ErrorCategory, Callable] = {}
        
        logger.info(f"Error handler initialized for team: {team_id}")
    
    def categorize_error(self, error: Exception) -> ErrorCategory:
        """Categorize an error.
        
        Args:
            error: Exception to categorize
        
        Returns:
            Error category
        """
        error_name = type(error).__name__.lower()
        error_message = str(error).lower()
        
        # Network errors
        if any(term in error_name or term in error_message 
               for term in ['connection', 'network', 'socket', 'http', 'api']):
            return ErrorCategory.NETWORK
        
        # Timeout errors
        if any(term in error_name or term in error_message 
               for term in ['timeout', 'timed out']):
            return ErrorCategory.TIMEOUT
        
        # Validation errors
        if any(term in error_name or term in error_message 
               for term in ['validation', 'invalid', 'schema']):
            return ErrorCategory.VALIDATION
        
        # Resource errors
        if any(term in error_name or term in error_message 
               for term in ['memory', 'resource', 'quota', 'limit']):
            return ErrorCategory.RESOURCE
        
        # Configuration errors
        if any(term in error_name or term in error_message 
               for term in ['config', 'configuration', 'setting']):
            return ErrorCategory.CONFIGURATION
        
        return ErrorCategory.UNKNOWN
    
    def assess_severity(
        self,
        error: Exception,
        category: ErrorCategory
    ) -> ErrorSeverity:
        """Assess error severity.
        
        Args:
            error: Exception
            category: Error category
        
        Returns:
            Error severity level
        """
        # Critical categories
        if category in [ErrorCategory.RESOURCE, ErrorCategory.CONFIGURATION]:
            return ErrorSeverity.HIGH
        
        # Retry-able categories
        if category in [ErrorCategory.NETWORK, ErrorCategory.TIMEOUT]:
            return ErrorSeverity.MEDIUM
        
        # Minor categories
        if category == ErrorCategory.VALIDATION:
            return ErrorSeverity.LOW
        
        # Check error type
        if isinstance(error, (KeyError, ValueError, TypeError)):
            return ErrorSeverity.LOW
        
        return ErrorSeverity.MEDIUM
    
    def create_error_context(
        self,
        error: Exception,
        operation_id: str,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ErrorContext:
        """Create error context from exception.
        
        Args:
            error: Exception
            operation_id: Operation identifier
            agent_id: Optional agent identifier
            metadata: Optional additional metadata
        
        Returns:
            Error context
        """
        category = self.categorize_error(error)
        severity = self.assess_severity(error, category)
        
        context = ErrorContext(
            error_type=type(error),
            error_message=str(error),
            error_traceback=traceback.format_exc(),
            timestamp=datetime.now(),
            operation_id=operation_id,
            agent_id=agent_id,
            team_id=self.team_id,
            severity=severity,
            category=category,
            metadata=metadata or {}
        )
        
        # Log error
        if self.enable_logging:
            self._log_error(context)
        
        # Track error
        self.error_history.append(context)
        
        return context
    
    def _log_error(self, context: ErrorContext):
        """Log error with appropriate level.
        
        Args:
            context: Error context
        """
        log_message = (
            f"[{context.category.value.upper()}] "
            f"{context.error_type.__name__}: {context.error_message}"
        )
        
        if context.agent_id:
            log_message = f"Agent {context.agent_id}: {log_message}"
        
        if context.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif context.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif context.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)
    
    def execute_with_retry(
        self,
        operation: Callable,
        operation_id: str,
        agent_id: Optional[str] = None,
        retry_config: Optional[RetryConfig] = None,
        **operation_kwargs
    ) -> RecoveryResult:
        """Execute an operation with retry logic.
        
        Args:
            operation: Callable to execute
            operation_id: Operation identifier
            agent_id: Optional agent identifier
            retry_config: Retry configuration (uses default if not provided)
            **operation_kwargs: Arguments to pass to operation
        
        Returns:
            Recovery result
        """
        config = retry_config or self.default_retry_config
        start_time = time.time()
        
        recovery_log = []
        last_error = None
        
        for attempt in range(config.max_attempts):
            try:
                recovery_log.append(f"Attempt {attempt + 1}/{config.max_attempts}")
                
                # Execute operation
                result = operation(**operation_kwargs)
                
                # Success
                total_time = time.time() - start_time
                recovery_result = RecoveryResult(
                    success=True,
                    strategy_used=RecoveryStrategy.RETRY,
                    attempts_made=attempt + 1,
                    total_time_seconds=total_time,
                    final_result=result,
                    recovery_log=recovery_log
                )
                
                self.recovery_history.append(recovery_result)
                
                if attempt > 0:
                    logger.info(
                        f"Operation {operation_id} succeeded after {attempt + 1} attempts"
                    )
                
                return recovery_result
                
            except config.retry_on_exceptions as e:
                # Create error context
                error_context = self.create_error_context(
                    e, operation_id, agent_id,
                    {"attempt": attempt + 1, "max_attempts": config.max_attempts}
                )
                last_error = error_context
                
                # Check if should retry
                if attempt < config.max_attempts - 1:
                    delay = config.get_delay(attempt)
                    recovery_log.append(
                        f"Error: {error_context.error_message}. Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)
                else:
                    recovery_log.append(
                        f"Error: {error_context.error_message}. Max attempts reached."
                    )
        
        # All attempts failed
        total_time = time.time() - start_time
        recovery_result = RecoveryResult(
            success=False,
            strategy_used=RecoveryStrategy.RETRY,
            attempts_made=config.max_attempts,
            total_time_seconds=total_time,
            final_error=last_error,
            recovery_log=recovery_log
        )
        
        self.recovery_history.append(recovery_result)
        
        logger.error(
            f"Operation {operation_id} failed after {config.max_attempts} attempts"
        )
        
        return recovery_result
    
    def register_fallback(
        self,
        category: ErrorCategory,
        fallback_handler: Callable
    ):
        """Register a fallback handler for an error category.
        
        Args:
            category: Error category
            fallback_handler: Function to call as fallback
        """
        self.fallback_handlers[category] = fallback_handler
        logger.info(f"Registered fallback handler for {category.value} errors")
    
    def execute_with_fallback(
        self,
        primary_operation: Callable,
        fallback_operation: Optional[Callable],
        operation_id: str,
        agent_id: Optional[str] = None,
        **operation_kwargs
    ) -> RecoveryResult:
        """Execute operation with fallback.
        
        Args:
            primary_operation: Primary callable to execute
            fallback_operation: Fallback callable if primary fails
            operation_id: Operation identifier
            agent_id: Optional agent identifier
            **operation_kwargs: Arguments to pass to operations
        
        Returns:
            Recovery result
        """
        start_time = time.time()
        recovery_log = []
        
        # Try primary operation
        try:
            recovery_log.append("Attempting primary operation")
            result = primary_operation(**operation_kwargs)
            
            total_time = time.time() - start_time
            return RecoveryResult(
                success=True,
                strategy_used=RecoveryStrategy.FALLBACK,
                attempts_made=1,
                total_time_seconds=total_time,
                final_result=result,
                recovery_log=recovery_log
            )
            
        except Exception as e:
            # Create error context
            error_context = self.create_error_context(
                e, operation_id, agent_id,
                {"strategy": "fallback"}
            )
            recovery_log.append(f"Primary operation failed: {error_context.error_message}")
            
            # Try fallback
            if fallback_operation and self.enable_fallbacks:
                try:
                    recovery_log.append("Attempting fallback operation")
                    result = fallback_operation(**operation_kwargs)
                    
                    total_time = time.time() - start_time
                    return RecoveryResult(
                        success=True,
                        strategy_used=RecoveryStrategy.FALLBACK,
                        attempts_made=2,
                        total_time_seconds=total_time,
                        final_result=result,
                        recovery_log=recovery_log
                    )
                    
                except Exception as fallback_error:
                    fallback_context = self.create_error_context(
                        fallback_error, operation_id, agent_id,
                        {"strategy": "fallback", "stage": "fallback"}
                    )
                    recovery_log.append(
                        f"Fallback operation also failed: {fallback_context.error_message}"
                    )
                    
                    total_time = time.time() - start_time
                    return RecoveryResult(
                        success=False,
                        strategy_used=RecoveryStrategy.FALLBACK,
                        attempts_made=2,
                        total_time_seconds=total_time,
                        final_error=fallback_context,
                        recovery_log=recovery_log
                    )
            
            # No fallback available
            total_time = time.time() - start_time
            recovery_log.append("No fallback available")
            return RecoveryResult(
                success=False,
                strategy_used=RecoveryStrategy.ABORT,
                attempts_made=1,
                total_time_seconds=total_time,
                final_error=error_context,
                recovery_log=recovery_log
            )
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors encountered.
        
        Returns:
            Error summary dictionary
        """
        if not self.error_history:
            return {
                "total_errors": 0,
                "by_category": {},
                "by_severity": {},
                "recent_errors": []
            }
        
        # Count by category
        by_category = {}
        for error in self.error_history:
            category = error.category.value
            by_category[category] = by_category.get(category, 0) + 1
        
        # Count by severity
        by_severity = {}
        for error in self.error_history:
            severity = error.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        # Recent errors (last 10)
        recent_errors = [
            {
                "timestamp": e.timestamp.isoformat(),
                "category": e.category.value,
                "severity": e.severity.value,
                "message": e.error_message[:100]  # Truncate
            }
            for e in self.error_history[-10:]
        ]
        
        return {
            "total_errors": len(self.error_history),
            "by_category": by_category,
            "by_severity": by_severity,
            "recent_errors": recent_errors,
            "total_recoveries": len(self.recovery_history),
            "successful_recoveries": sum(
                1 for r in self.recovery_history if r.success
            )
        }
    
    def print_error_summary(self):
        """Print error summary to console."""
        summary = self.get_error_summary()
        
        print("\n" + "="*70)
        print(f"⚠️  ERROR SUMMARY - Team: {self.team_id}")
        print("="*70)
        
        print(f"\nTotal Errors: {summary['total_errors']}")
        
        if summary['by_category']:
            print("\nBy Category:")
            for category, count in summary['by_category'].items():
                print(f"  • {category}: {count}")
        
        if summary['by_severity']:
            print("\nBy Severity:")
            for severity, count in summary['by_severity'].items():
                print(f"  • {severity}: {count}")
        
        print(f"\nRecovery Attempts: {summary['total_recoveries']}")
        print(f"Successful Recoveries: {summary['successful_recoveries']}")
        
        if summary['recent_errors']:
            print("\nRecent Errors:")
            for error in summary['recent_errors'][-5:]:  # Last 5
                print(f"  [{error['timestamp']}] {error['category']}/{error['severity']}: {error['message']}")
        
        print("\n" + "="*70)


# Decorator for automatic retry
def with_retry(
    retry_config: Optional[RetryConfig] = None,
    operation_id: Optional[str] = None
):
    """Decorator to automatically retry a function.
    
    Args:
        retry_config: Retry configuration
        operation_id: Operation identifier
    
    Returns:
        Decorated function
    """
    config = retry_config or RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            op_id = operation_id or f"{func.__name__}_{id(func)}"
            
            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                except config.retry_on_exceptions as e:
                    if attempt < config.max_attempts - 1:
                        delay = config.get_delay(attempt)
                        logger.warning(
                            f"{op_id} failed (attempt {attempt + 1}): {e}. "
                            f"Retrying in {delay:.2f}s..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"{op_id} failed after {config.max_attempts} attempts: {e}"
                        )
                        raise
            
        return wrapper
    return decorator


# Convenience function
def create_error_handler(team_id: str, **kwargs) -> TeamErrorHandler:
    """Create and initialize an error handler.
    
    Args:
        team_id: Team identifier
        **kwargs: Additional arguments for TeamErrorHandler
    
    Returns:
        Initialized TeamErrorHandler
    """
    return TeamErrorHandler(team_id, **kwargs)
