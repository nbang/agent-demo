"""
Service Layer

This module contains various services for the agent system including
performance monitoring, health checks, and other supporting services.
"""

"""Common Services for Agno Agent System

Provides centralized services that can be used across all agent types:
- Logging: Structured logging with context and formatting
- Error Handling: Robust error handling with retry logic and recovery
- Monitoring: Performance monitoring and metrics collection
- Metrics: Agent metrics and collaboration analysis

Usage:
    from src.services.logging import get_agent_logger, setup_logging
    from src.services.error_handling import ErrorHandler
    from src.services.monitoring import PerformanceMonitor
    from src.services.metrics import AgentMetricsCollector
"""

# Import main service classes
from .logging import (
    setup_logging,
    get_agent_logger,
    setup_advanced_logging,
    LoggedOperation,
    logger
)

from .error_handling import (
    ErrorHandler,
    ErrorSeverity,
    ErrorCategory,
    RecoveryStrategy,
    default_error_handler
)

from .monitoring import (
    PerformanceMonitor,
    PerformanceMetrics,
    MetricType,
    default_performance_monitor
)

from .metrics import (
    AgentMetricsCollector,
    AgentMetrics,
    InteractionType,
    CollaborationPattern,
    default_metrics_collector
)

# Backward compatibility
try:
    from .monitoring import (
        PerformanceMonitor as LegacyPerformanceMonitor,
        default_performance_monitor as performance_monitor
    )
except ImportError:
    pass

__all__ = [
    # Logging
    'setup_logging',
    'get_agent_logger', 
    'setup_advanced_logging',
    'LoggedOperation',
    'logger',
    
    # Error Handling
    'ErrorHandler',
    'ErrorSeverity',
    'ErrorCategory', 
    'RecoveryStrategy',
    'default_error_handler',
    
    # Monitoring
    'PerformanceMonitor',
    'PerformanceMetrics',
    'MetricType',
    'default_performance_monitor',
    
    # Metrics
    'AgentMetricsCollector',
    'AgentMetrics',
    'InteractionType',
    'CollaborationPattern',
    'default_metrics_collector',
    
    # Backward compatibility
    'performance_monitor'
]

__all__ = ['PerformanceMonitor']