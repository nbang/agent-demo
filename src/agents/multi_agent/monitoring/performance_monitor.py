"""Performance Monitoring for Multi-Agent Teams

Tracks and reports performance metrics for multi-agent team operations including:
- Execution time
- Memory usage
- API calls
- Agent activity
- Resource utilization
"""

import time
import psutil
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict


logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of performance metrics."""
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    API_CALLS = "api_calls"
    AGENT_ACTIVITY = "agent_activity"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"


class PerformanceLevel(Enum):
    """Performance level indicators."""
    EXCELLENT = "excellent"  # > 90% of target
    GOOD = "good"  # 70-90% of target
    ACCEPTABLE = "acceptable"  # 50-70% of target
    POOR = "poor"  # < 50% of target


@dataclass
class MetricSnapshot:
    """A single point-in-time metric measurement."""
    
    timestamp: datetime
    metric_type: MetricType
    value: float
    unit: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "metric_type": self.metric_type.value,
            "value": self.value,
            "unit": self.unit,
            "metadata": self.metadata
        }


@dataclass
class PerformanceWindow:
    """Performance metrics over a time window."""
    
    start_time: datetime
    end_time: datetime
    metrics: List[MetricSnapshot] = field(default_factory=list)
    
    def duration_seconds(self) -> float:
        """Get window duration in seconds."""
        return (self.end_time - self.start_time).total_seconds()
    
    def get_metrics_by_type(self, metric_type: MetricType) -> List[MetricSnapshot]:
        """Get all metrics of a specific type."""
        return [m for m in self.metrics if m.metric_type == metric_type]
    
    def get_average(self, metric_type: MetricType) -> Optional[float]:
        """Get average value for a metric type."""
        metrics = self.get_metrics_by_type(metric_type)
        if not metrics:
            return None
        return sum(m.value for m in metrics) / len(metrics)
    
    def get_max(self, metric_type: MetricType) -> Optional[float]:
        """Get maximum value for a metric type."""
        metrics = self.get_metrics_by_type(metric_type)
        if not metrics:
            return None
        return max(m.value for m in metrics)
    
    def get_min(self, metric_type: MetricType) -> Optional[float]:
        """Get minimum value for a metric type."""
        metrics = self.get_metrics_by_type(metric_type)
        if not metrics:
            return None
        return min(m.value for m in metrics)


@dataclass
class AgentPerformanceMetrics:
    """Performance metrics for a specific agent."""
    
    agent_id: str
    agent_name: str
    total_executions: int = 0
    total_time_seconds: float = 0.0
    successful_executions: int = 0
    failed_executions: int = 0
    average_time_seconds: float = 0.0
    api_calls_made: int = 0
    
    def update_from_execution(self, execution_time: float, success: bool, api_calls: int = 0):
        """Update metrics from an execution."""
        self.total_executions += 1
        self.total_time_seconds += execution_time
        self.api_calls_made += api_calls
        
        if success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1
        
        self.average_time_seconds = self.total_time_seconds / self.total_executions
    
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_executions == 0:
            return 0.0
        return self.successful_executions / self.total_executions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "total_executions": self.total_executions,
            "total_time_seconds": self.total_time_seconds,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "average_time_seconds": self.average_time_seconds,
            "success_rate": self.success_rate(),
            "api_calls_made": self.api_calls_made
        }


class PerformanceMonitor:
    """Monitors and tracks performance metrics for multi-agent teams."""
    
    def __init__(
        self,
        team_id: str,
        enable_memory_tracking: bool = True,
        enable_api_tracking: bool = True,
        snapshot_interval_seconds: float = 5.0
    ):
        """Initialize performance monitor.
        
        Args:
            team_id: Unique identifier for the team being monitored
            enable_memory_tracking: Track memory usage metrics
            enable_api_tracking: Track API call metrics
            snapshot_interval_seconds: Interval for automatic metric snapshots
        """
        self.team_id = team_id
        self.enable_memory_tracking = enable_memory_tracking
        self.enable_api_tracking = enable_api_tracking
        self.snapshot_interval = snapshot_interval_seconds
        
        # Tracking data
        self.start_time = datetime.now()
        self.metrics: List[MetricSnapshot] = []
        self.agent_metrics: Dict[str, AgentPerformanceMetrics] = {}
        self.api_call_count = 0
        self.error_count = 0
        self.operation_count = 0
        
        # Process tracking
        self.process = psutil.Process()
        self.initial_memory_mb = self._get_memory_usage_mb()
        
        # Execution tracking
        self.active_operations: Dict[str, float] = {}  # operation_id -> start_time
        
        logger.info(f"Performance monitoring initialized for team: {team_id}")
    
    def _get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB."""
        try:
            return self.process.memory_info().rss / 1024 / 1024
        except Exception as e:
            logger.warning(f"Could not get memory usage: {e}")
            return 0.0
    
    def _get_cpu_percent(self) -> float:
        """Get current CPU usage percentage."""
        try:
            return self.process.cpu_percent(interval=0.1)
        except Exception as e:
            logger.warning(f"Could not get CPU usage: {e}")
            return 0.0
    
    def start_operation(self, operation_id: str, agent_id: Optional[str] = None) -> float:
        """Start tracking an operation.
        
        Args:
            operation_id: Unique identifier for the operation
            agent_id: Optional agent identifier
        
        Returns:
            Start timestamp
        """
        start_time = time.time()
        self.active_operations[operation_id] = start_time
        self.operation_count += 1
        
        # Ensure agent exists in metrics
        if agent_id and agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentPerformanceMetrics(
                agent_id=agent_id,
                agent_name=agent_id  # Can be updated later
            )
        
        return start_time
    
    def end_operation(
        self,
        operation_id: str,
        agent_id: Optional[str] = None,
        success: bool = True,
        api_calls: int = 0
    ) -> float:
        """End tracking an operation and record metrics.
        
        Args:
            operation_id: Unique identifier for the operation
            agent_id: Optional agent identifier
            success: Whether operation was successful
            api_calls: Number of API calls made during operation
        
        Returns:
            Execution time in seconds
        """
        if operation_id not in self.active_operations:
            logger.warning(f"Operation {operation_id} was not started")
            return 0.0
        
        start_time = self.active_operations.pop(operation_id)
        execution_time = time.time() - start_time
        
        # Record execution time metric
        self.record_metric(
            MetricType.EXECUTION_TIME,
            execution_time,
            "seconds",
            {"operation_id": operation_id, "agent_id": agent_id}
        )
        
        # Update agent metrics
        if agent_id and agent_id in self.agent_metrics:
            self.agent_metrics[agent_id].update_from_execution(
                execution_time, success, api_calls
            )
        
        # Update API call count
        if api_calls > 0:
            self.api_call_count += api_calls
            if self.enable_api_tracking:
                self.record_metric(
                    MetricType.API_CALLS,
                    api_calls,
                    "calls",
                    {"operation_id": operation_id}
                )
        
        # Update error count
        if not success:
            self.error_count += 1
        
        return execution_time
    
    def record_metric(
        self,
        metric_type: MetricType,
        value: float,
        unit: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record a performance metric.
        
        Args:
            metric_type: Type of metric
            value: Metric value
            unit: Unit of measurement
            metadata: Additional metadata
        """
        snapshot = MetricSnapshot(
            timestamp=datetime.now(),
            metric_type=metric_type,
            value=value,
            unit=unit,
            metadata=metadata or {}
        )
        self.metrics.append(snapshot)
    
    def record_memory_snapshot(self):
        """Record current memory usage."""
        if not self.enable_memory_tracking:
            return
        
        memory_mb = self._get_memory_usage_mb()
        self.record_metric(
            MetricType.MEMORY_USAGE,
            memory_mb,
            "MB"
        )
    
    def record_agent_activity(self, agent_id: str, activity_type: str):
        """Record agent activity.
        
        Args:
            agent_id: Agent identifier
            activity_type: Type of activity (e.g., 'message_sent', 'task_completed')
        """
        self.record_metric(
            MetricType.AGENT_ACTIVITY,
            1.0,
            "count",
            {"agent_id": agent_id, "activity_type": activity_type}
        )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary.
        
        Returns:
            Dictionary with performance summary
        """
        now = datetime.now()
        total_time = (now - self.start_time).total_seconds()
        
        # Calculate memory stats
        current_memory = self._get_memory_usage_mb()
        memory_increase = current_memory - self.initial_memory_mb
        
        # Calculate execution time stats
        execution_times = [
            m.value for m in self.metrics 
            if m.metric_type == MetricType.EXECUTION_TIME
        ]
        
        # Calculate error rate
        error_rate = (self.error_count / self.operation_count * 100) if self.operation_count > 0 else 0.0
        
        # Calculate throughput
        throughput = self.operation_count / total_time if total_time > 0 else 0.0
        
        summary = {
            "team_id": self.team_id,
            "monitoring_duration_seconds": total_time,
            "start_time": self.start_time.isoformat(),
            "end_time": now.isoformat(),
            
            # Operations
            "total_operations": self.operation_count,
            "active_operations": len(self.active_operations),
            "completed_operations": self.operation_count - len(self.active_operations),
            
            # Execution times
            "execution_times": {
                "average_seconds": sum(execution_times) / len(execution_times) if execution_times else 0.0,
                "min_seconds": min(execution_times) if execution_times else 0.0,
                "max_seconds": max(execution_times) if execution_times else 0.0,
                "total_seconds": sum(execution_times)
            } if execution_times else None,
            
            # Memory
            "memory": {
                "initial_mb": self.initial_memory_mb,
                "current_mb": current_memory,
                "increase_mb": memory_increase,
                "increase_percent": (memory_increase / self.initial_memory_mb * 100) if self.initial_memory_mb > 0 else 0.0
            },
            
            # API calls
            "api_calls": {
                "total": self.api_call_count,
                "average_per_operation": self.api_call_count / self.operation_count if self.operation_count > 0 else 0.0
            },
            
            # Errors
            "errors": {
                "total": self.error_count,
                "rate_percent": error_rate
            },
            
            # Throughput
            "throughput": {
                "operations_per_second": throughput
            },
            
            # Agent metrics
            "agents": {
                agent_id: metrics.to_dict()
                for agent_id, metrics in self.agent_metrics.items()
            },
            
            # Performance level
            "performance_level": self._assess_performance_level(
                error_rate, throughput, memory_increase
            ).value
        }
        
        return summary
    
    def _assess_performance_level(
        self,
        error_rate: float,
        throughput: float,
        memory_increase_mb: float
    ) -> PerformanceLevel:
        """Assess overall performance level.
        
        Args:
            error_rate: Error rate percentage
            throughput: Operations per second
            memory_increase_mb: Memory increase in MB
        
        Returns:
            Performance level assessment
        """
        # Simple scoring heuristic
        score = 100.0
        
        # Penalize high error rates
        if error_rate > 10:
            score -= 30
        elif error_rate > 5:
            score -= 20
        elif error_rate > 2:
            score -= 10
        
        # Penalize low throughput (below 0.1 ops/sec)
        if throughput < 0.01:
            score -= 20
        elif throughput < 0.05:
            score -= 10
        
        # Penalize high memory increase (above 500MB)
        if memory_increase_mb > 1000:
            score -= 20
        elif memory_increase_mb > 500:
            score -= 10
        
        # Determine performance level
        if score >= 90:
            return PerformanceLevel.EXCELLENT
        elif score >= 70:
            return PerformanceLevel.GOOD
        elif score >= 50:
            return PerformanceLevel.ACCEPTABLE
        else:
            return PerformanceLevel.POOR
    
    def get_performance_window(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> PerformanceWindow:
        """Get performance metrics for a time window.
        
        Args:
            start_time: Window start time (defaults to monitor start time)
            end_time: Window end time (defaults to now)
        
        Returns:
            Performance window with metrics
        """
        start = start_time or self.start_time
        end = end_time or datetime.now()
        
        # Filter metrics in window
        window_metrics = [
            m for m in self.metrics
            if start <= m.timestamp <= end
        ]
        
        return PerformanceWindow(
            start_time=start,
            end_time=end,
            metrics=window_metrics
        )
    
    def print_summary(self):
        """Print performance summary to console."""
        summary = self.get_performance_summary()
        
        print("\n" + "="*70)
        print(f"📊 PERFORMANCE SUMMARY - Team: {self.team_id}")
        print("="*70)
        
        print(f"\n⏱️  Monitoring Duration: {summary['monitoring_duration_seconds']:.2f}s")
        print(f"\n🔄 Operations:")
        print(f"   Total: {summary['total_operations']}")
        print(f"   Active: {summary['active_operations']}")
        print(f"   Completed: {summary['completed_operations']}")
        
        if summary['execution_times']:
            print(f"\n⚡ Execution Times:")
            print(f"   Average: {summary['execution_times']['average_seconds']:.3f}s")
            print(f"   Min: {summary['execution_times']['min_seconds']:.3f}s")
            print(f"   Max: {summary['execution_times']['max_seconds']:.3f}s")
        
        print(f"\n💾 Memory:")
        print(f"   Initial: {summary['memory']['initial_mb']:.2f} MB")
        print(f"   Current: {summary['memory']['current_mb']:.2f} MB")
        print(f"   Increase: {summary['memory']['increase_mb']:.2f} MB ({summary['memory']['increase_percent']:.1f}%)")
        
        print(f"\n📞 API Calls:")
        print(f"   Total: {summary['api_calls']['total']}")
        print(f"   Average/Operation: {summary['api_calls']['average_per_operation']:.2f}")
        
        print(f"\n❌ Errors:")
        print(f"   Total: {summary['errors']['total']}")
        print(f"   Rate: {summary['errors']['rate_percent']:.2f}%")
        
        print(f"\n🚀 Throughput:")
        print(f"   {summary['throughput']['operations_per_second']:.3f} operations/second")
        
        print(f"\n📈 Performance Level: {summary['performance_level'].upper()}")
        
        if summary['agents']:
            print(f"\n👥 Agent Performance:")
            for agent_id, metrics in summary['agents'].items():
                print(f"   • {metrics['agent_name']}:")
                print(f"     - Executions: {metrics['total_executions']} (Success rate: {metrics['success_rate']*100:.1f}%)")
                print(f"     - Avg time: {metrics['average_time_seconds']:.3f}s")
                print(f"     - API calls: {metrics['api_calls_made']}")
        
        print("\n" + "="*70)
    
    def reset(self):
        """Reset all performance metrics."""
        self.start_time = datetime.now()
        self.metrics.clear()
        self.agent_metrics.clear()
        self.api_call_count = 0
        self.error_count = 0
        self.operation_count = 0
        self.active_operations.clear()
        self.initial_memory_mb = self._get_memory_usage_mb()
        
        logger.info(f"Performance monitor reset for team: {self.team_id}")


# Context manager for operation tracking
class PerformanceContext:
    """Context manager for tracking operation performance."""
    
    def __init__(
        self,
        monitor: PerformanceMonitor,
        operation_id: str,
        agent_id: Optional[str] = None
    ):
        """Initialize performance context.
        
        Args:
            monitor: Performance monitor instance
            operation_id: Unique operation identifier
            agent_id: Optional agent identifier
        """
        self.monitor = monitor
        self.operation_id = operation_id
        self.agent_id = agent_id
        self.success = True
        self.api_calls = 0
    
    def __enter__(self):
        """Enter context - start tracking."""
        self.monitor.start_operation(self.operation_id, self.agent_id)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - end tracking."""
        if exc_type is not None:
            self.success = False
        
        self.monitor.end_operation(
            self.operation_id,
            self.agent_id,
            self.success,
            self.api_calls
        )
        return False  # Don't suppress exceptions
    
    def record_api_call(self):
        """Record an API call during this operation."""
        self.api_calls += 1


# Convenience function
def create_performance_monitor(
    team_id: str,
    **kwargs
) -> PerformanceMonitor:
    """Create and initialize a performance monitor.
    
    Args:
        team_id: Team identifier
        **kwargs: Additional arguments for PerformanceMonitor
    
    Returns:
        Initialized PerformanceMonitor
    """
    return PerformanceMonitor(team_id, **kwargs)
