"""Unified Performance Monitoring for Agno Agent System

Provides comprehensive performance monitoring, metrics collection, and alerting
that can be used across all agent types and services in the Agno framework.
"""

import time
import psutil
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from contextlib import contextmanager
from collections import deque, defaultdict
from enum import Enum

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of performance metrics."""
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    API_CALLS = "api_calls"
    AGENT_ACTIVITY = "agent_activity"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    RESPONSE_TIME = "response_time"


class PerformanceLevel(Enum):
    """Performance level indicators."""
    EXCELLENT = "excellent"  # > 90% of target
    GOOD = "good"  # 70-90% of target
    ACCEPTABLE = "acceptable"  # 50-70% of target
    POOR = "poor"  # < 50% of target


@dataclass
class PerformanceMetrics:
    """Data class for storing performance metrics."""
    response_time: float
    memory_usage_mb: float
    cpu_usage_percent: float
    timestamp: datetime
    operation: str
    agent_type: Optional[str] = None
    agent_id: Optional[str] = None
    team_id: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    api_calls: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "response_time": self.response_time,
            "memory_usage_mb": self.memory_usage_mb,
            "cpu_usage_percent": self.cpu_usage_percent,
            "timestamp": self.timestamp.isoformat(),
            "operation": self.operation,
            "agent_type": self.agent_type,
            "agent_id": self.agent_id,
            "team_id": self.team_id,
            "success": self.success,
            "error_message": self.error_message,
            "api_calls": self.api_calls,
            "metadata": self.metadata
        }


@dataclass
class MetricSnapshot:
    """A single point-in-time metric measurement."""
    
    timestamp: datetime
    metric_type: MetricType
    value: float
    unit: str
    agent_id: Optional[str] = None
    team_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "metric_type": self.metric_type.value,
            "value": self.value,
            "unit": self.unit,
            "agent_id": self.agent_id,
            "team_id": self.team_id,
            "metadata": self.metadata
        }


@dataclass
class PerformanceThresholds:
    """Performance thresholds for alerting."""
    max_response_time: float = 5.0  # seconds
    max_memory_usage: float = 500.0  # MB
    max_cpu_usage: float = 80.0  # percent
    min_success_rate: float = 0.95  # 95%
    max_error_rate: float = 0.05  # 5%
    alert_enabled: bool = True


@dataclass
class AgentPerformanceMetrics:
    """Performance metrics for a specific agent."""
    
    agent_id: str
    agent_type: str
    agent_name: Optional[str] = None
    team_id: Optional[str] = None
    total_executions: int = 0
    total_time_seconds: float = 0.0
    successful_executions: int = 0
    failed_executions: int = 0
    average_time_seconds: float = 0.0
    api_calls_made: int = 0
    memory_peak_mb: float = 0.0
    
    def update_from_execution(self, execution_time: float, success: bool, api_calls: int = 0, memory_mb: float = 0.0):
        """Update metrics from an execution."""
        self.total_executions += 1
        self.total_time_seconds += execution_time
        self.api_calls_made += api_calls
        
        if memory_mb > self.memory_peak_mb:
            self.memory_peak_mb = memory_mb
        
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
    
    def error_rate(self) -> float:
        """Calculate error rate."""
        if self.total_executions == 0:
            return 0.0
        return self.failed_executions / self.total_executions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "agent_name": self.agent_name,
            "team_id": self.team_id,
            "total_executions": self.total_executions,
            "total_time_seconds": self.total_time_seconds,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "average_time_seconds": self.average_time_seconds,
            "success_rate": self.success_rate(),
            "error_rate": self.error_rate(),
            "api_calls_made": self.api_calls_made,
            "memory_peak_mb": self.memory_peak_mb
        }


class PerformanceMonitor:
    """Unified performance monitoring and metrics collection."""
    
    def __init__(self, max_history: int = 1000, agent_type: str = "generic", agent_id: Optional[str] = None, team_id: Optional[str] = None):
        """Initialize performance monitor.
        
        Args:
            max_history: Maximum number of metrics to keep in history
            agent_type: Type of agent being monitored
            agent_id: Optional agent identifier
            team_id: Optional team identifier
        """
        self.agent_type = agent_type
        self.agent_id = agent_id
        self.team_id = team_id
        
        self.metrics_history: deque = deque(maxlen=max_history)
        self.snapshots_history: deque = deque(maxlen=max_history)
        self.agent_metrics: Dict[str, AgentPerformanceMetrics] = {}
        self.thresholds = PerformanceThresholds()
        self.start_time = datetime.now()
        self.total_operations = 0
        self.successful_operations = 0
        
        # Performance tracking
        self.operation_counts = defaultdict(int)
        self.operation_times = defaultdict(list)
        self.recent_metrics: Dict[MetricType, List[MetricSnapshot]] = defaultdict(list)
        
    @contextmanager
    def monitor_operation(self, operation_name: str, agent_id: Optional[str] = None):
        """
        Context manager to monitor the performance of an operation.
        
        Args:
            operation_name: Name of the operation being monitored
            agent_id: Optional specific agent ID for this operation
        """
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        start_cpu = psutil.cpu_percent(interval=None)
        
        success = True
        error_message = None
        api_calls = 0
        
        try:
            yield self
        except Exception as e:
            success = False
            error_message = str(e)
            raise
        finally:
            # Calculate metrics
            end_time = time.time()
            response_time = end_time - start_time
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            end_cpu = psutil.cpu_percent(interval=None)
            
            # Create metrics record
            metrics = PerformanceMetrics(
                response_time=response_time,
                memory_usage_mb=end_memory,
                cpu_usage_percent=end_cpu,
                timestamp=datetime.now(),
                operation=operation_name,
                agent_type=self.agent_type,
                agent_id=agent_id or self.agent_id,
                team_id=self.team_id,
                success=success,
                error_message=error_message,
                api_calls=api_calls
            )
            
            # Store metrics
            self.record_metrics(metrics)
            
            # Update agent-specific metrics
            target_agent_id = agent_id or self.agent_id
            if target_agent_id:
                self.update_agent_metrics(
                    target_agent_id,
                    response_time,
                    success,
                    api_calls,
                    end_memory
                )
            
            # Log metrics
            status = "✅" if success else "❌"
            logger.info(
                f"{status} Operation '{operation_name}' completed in {response_time:.2f}s "
                f"(Memory: {end_memory:.1f}MB, CPU: {end_cpu:.1f}%)",
                extra={
                    "operation": operation_name,
                    "response_time": response_time,
                    "memory_mb": end_memory,
                    "cpu_percent": end_cpu,
                    "success": success,
                    "agent_type": self.agent_type,
                    "agent_id": agent_id or self.agent_id,
                    "team_id": self.team_id
                }
            )
            
            # Check for performance alerts
            self._check_performance_alerts(metrics)
    
    def record_metrics(self, metrics: PerformanceMetrics):
        """Record performance metrics."""
        self.metrics_history.append(metrics)
        self.total_operations += 1
        if metrics.success:
            self.successful_operations += 1
        
        # Track operation-specific metrics
        self.operation_counts[metrics.operation] += 1
        self.operation_times[metrics.operation].append(metrics.response_time)
        
        # Record individual metric snapshots
        self.record_snapshot(MetricType.EXECUTION_TIME, metrics.response_time, "seconds", metrics.agent_id)
        self.record_snapshot(MetricType.MEMORY_USAGE, metrics.memory_usage_mb, "MB", metrics.agent_id)
        self.record_snapshot(MetricType.CPU_USAGE, metrics.cpu_usage_percent, "percent", metrics.agent_id)
        if metrics.api_calls > 0:
            self.record_snapshot(MetricType.API_CALLS, metrics.api_calls, "calls", metrics.agent_id)
    
    def record_snapshot(self, metric_type: MetricType, value: float, unit: str, agent_id: Optional[str] = None):
        """Record a metric snapshot."""
        snapshot = MetricSnapshot(
            timestamp=datetime.now(),
            metric_type=metric_type,
            value=value,
            unit=unit,
            agent_id=agent_id or self.agent_id,
            team_id=self.team_id
        )
        
        self.snapshots_history.append(snapshot)
        self.recent_metrics[metric_type].append(snapshot)
        
        # Keep only recent metrics (last hour)
        cutoff = datetime.now() - timedelta(hours=1)
        self.recent_metrics[metric_type] = [
            s for s in self.recent_metrics[metric_type]
            if s.timestamp > cutoff
        ]
    
    def update_agent_metrics(self, agent_id: str, execution_time: float, success: bool, api_calls: int = 0, memory_mb: float = 0.0):
        """Update agent-specific metrics."""
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentPerformanceMetrics(
                agent_id=agent_id,
                agent_type=self.agent_type,
                team_id=self.team_id
            )
        
        self.agent_metrics[agent_id].update_from_execution(execution_time, success, api_calls, memory_mb)
    
    def _check_performance_alerts(self, metrics: PerformanceMetrics):
        """Check metrics against thresholds and issue alerts if needed."""
        if not self.thresholds.alert_enabled:
            return
        
        alerts = []
        
        if metrics.response_time > self.thresholds.max_response_time:
            alerts.append(f"Slow response time: {metrics.response_time:.2f}s "
                         f"(threshold: {self.thresholds.max_response_time}s)")
        
        if metrics.memory_usage_mb > self.thresholds.max_memory_usage:
            alerts.append(f"High memory usage: {metrics.memory_usage_mb:.1f}MB "
                         f"(threshold: {self.thresholds.max_memory_usage}MB)")
        
        if metrics.cpu_usage_percent > self.thresholds.max_cpu_usage:
            alerts.append(f"High CPU usage: {metrics.cpu_usage_percent:.1f}% "
                         f"(threshold: {self.thresholds.max_cpu_usage}%)")
        
        # Check success rate
        if self.total_operations >= 10:  # Only check after some operations
            current_success_rate = self.successful_operations / self.total_operations
            if current_success_rate < self.thresholds.min_success_rate:
                alerts.append(f"Low success rate: {current_success_rate:.1%} "
                             f"(threshold: {self.thresholds.min_success_rate:.1%})")
        
        for alert in alerts:
            logger.warning(
                f"Performance Alert: {alert}",
                extra={
                    "alert_type": "performance",
                    "agent_type": self.agent_type,
                    "agent_id": self.agent_id,
                    "team_id": self.team_id
                }
            )
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary performance statistics."""
        if not self.metrics_history:
            return {
                "total_operations": 0,
                "successful_operations": 0,
                "success_rate": 0.0,
                "avg_response_time": 0.0,
                "avg_memory_usage": 0.0,
                "avg_cpu_usage": 0.0,
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
            }
        
        successful_metrics = [m for m in self.metrics_history if m.success]
        
        return {
            "total_operations": self.total_operations,
            "successful_operations": self.successful_operations,
            "success_rate": (self.successful_operations / self.total_operations * 100) if self.total_operations > 0 else 0.0,
            "avg_response_time": sum(m.response_time for m in successful_metrics) / len(successful_metrics) if successful_metrics else 0.0,
            "avg_memory_usage": sum(m.memory_usage_mb for m in self.metrics_history) / len(self.metrics_history),
            "avg_cpu_usage": sum(m.cpu_usage_percent for m in self.metrics_history) / len(self.metrics_history),
            "max_response_time": max(m.response_time for m in successful_metrics) if successful_metrics else 0.0,
            "min_response_time": min(m.response_time for m in successful_metrics) if successful_metrics else 0.0,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "agent_type": self.agent_type,
            "agent_id": self.agent_id,
            "team_id": self.team_id
        }
    
    def get_agent_stats(self, agent_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get performance statistics for a specific agent."""
        target_agent = agent_id or self.agent_id
        if not target_agent or target_agent not in self.agent_metrics:
            return None
        
        return self.agent_metrics[target_agent].to_dict()
    
    def get_all_agent_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get performance statistics for all agents."""
        return {
            agent_id: metrics.to_dict()
            for agent_id, metrics in self.agent_metrics.items()
        }
    
    def get_operation_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics by operation type."""
        stats = {}
        
        for operation, times in self.operation_times.items():
            if times:
                stats[operation] = {
                    "count": self.operation_counts[operation],
                    "avg_time": sum(times) / len(times),
                    "min_time": min(times),
                    "max_time": max(times),
                    "total_time": sum(times)
                }
        
        return stats
    
    def get_recent_metrics(self, metric_type: MetricType, minutes: int = 60) -> List[MetricSnapshot]:
        """Get recent metrics of a specific type."""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return [
            m for m in self.recent_metrics.get(metric_type, [])
            if m.timestamp > cutoff
        ]
    
    def reset_metrics(self):
        """Reset all metrics and counters."""
        self.metrics_history.clear()
        self.snapshots_history.clear()
        self.agent_metrics.clear()
        self.operation_counts.clear()
        self.operation_times.clear()
        self.recent_metrics.clear()
        self.total_operations = 0
        self.successful_operations = 0
        self.start_time = datetime.now()
        logger.info("Performance metrics reset")
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics for persistence or analysis."""
        return {
            "summary": self.get_summary_stats(),
            "agent_stats": self.get_all_agent_stats(),
            "operation_stats": self.get_operation_stats(),
            "recent_metrics": {
                metric_type.value: [s.to_dict() for s in snapshots]
                for metric_type, snapshots in self.recent_metrics.items()
            },
            "thresholds": {
                "max_response_time": self.thresholds.max_response_time,
                "max_memory_usage": self.thresholds.max_memory_usage,
                "max_cpu_usage": self.thresholds.max_cpu_usage,
                "min_success_rate": self.thresholds.min_success_rate,
                "alert_enabled": self.thresholds.alert_enabled
            }
        }


# Global performance monitor instance
default_performance_monitor = PerformanceMonitor()


# Convenience functions for backward compatibility
def create_team_performance_monitor(team_id: str, agent_id: Optional[str] = None) -> PerformanceMonitor:
    """Create performance monitor for multi-agent team (backward compatibility).
    
    Args:
        team_id: Team identifier
        agent_id: Optional agent identifier
    
    Returns:
        PerformanceMonitor instance
    """
    return PerformanceMonitor(agent_type="multi_agent", agent_id=agent_id, team_id=team_id)