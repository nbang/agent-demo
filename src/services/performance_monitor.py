"""Services for Agno Agent System

This module has been restructured. The performance monitoring functionality
has been moved to src.services.monitoring.

For backward compatibility, import from the new location:
    from src.services.monitoring import PerformanceMonitor

The old performance_monitor.py is deprecated.
"""

# Backward compatibility imports
try:
    from .monitoring import (
        PerformanceMonitor,
        PerformanceMetrics,
        PerformanceThresholds,
        default_performance_monitor
    )
    
    # Issue deprecation warning
    import warnings
    warnings.warn(
        "Importing from src.services.performance_monitor is deprecated. "
        "Use 'from src.services.monitoring import PerformanceMonitor' instead.",
        DeprecationWarning,
        stacklevel=2
    )
    
except ImportError:
    # Fallback for if monitoring module isn't available
    pass

__all__ = [
    'PerformanceMonitor',
    'PerformanceMetrics', 
    'PerformanceThresholds',
    'default_performance_monitor'
]