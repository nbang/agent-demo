#!/usr/bin/env python3
"""
Performance Monitoring Module

Provides performance monitoring, metrics collection, and alerting
for the Agno Agent Demo project.
"""

import time
import psutil
import logging
from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from contextlib import contextmanager
from collections import deque

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Data class for storing performance metrics."""
    response_time: float
    memory_usage_mb: float
    cpu_usage_percent: float
    timestamp: datetime
    operation: str
    success: bool = True
    error_message: Optional[str] = None

@dataclass
class PerformanceThresholds:
    """Performance thresholds for alerting."""
    max_response_time: float = 5.0  # seconds
    max_memory_usage: float = 500.0  # MB
    max_cpu_usage: float = 80.0  # percent
    alert_enabled: bool = True

class PerformanceMonitor:
    """Performance monitoring and metrics collection."""
    
    def __init__(self, max_history: int = 100):
        self.metrics_history: deque = deque(maxlen=max_history)
        self.thresholds = PerformanceThresholds()
        self.start_time = datetime.now()
        self.total_operations = 0
        self.successful_operations = 0
        
    @contextmanager
    def monitor_operation(self, operation_name: str):
        """
        Context manager to monitor the performance of an operation.
        
        Args:
            operation_name: Name of the operation being monitored
        """
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        start_cpu = psutil.cpu_percent()
        
        success = True
        error_message = None
        
        try:
            yield
        except Exception as e:
            success = False
            error_message = str(e)
            raise
        finally:
            # Calculate metrics
            end_time = time.time()
            response_time = end_time - start_time
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            end_cpu = psutil.cpu_percent()
            
            # Create metrics record
            metrics = PerformanceMetrics(
                response_time=response_time,
                memory_usage_mb=end_memory,
                cpu_usage_percent=end_cpu,
                timestamp=datetime.now(),
                operation=operation_name,
                success=success,
                error_message=error_message
            )
            
            # Store metrics
            self.metrics_history.append(metrics)
            self.total_operations += 1
            if success:
                self.successful_operations += 1
            
            # Log metrics
            logger.info(f"Operation '{operation_name}' completed in {response_time:.2f}s "
                       f"(Memory: {end_memory:.1f}MB, CPU: {end_cpu:.1f}%)")
            
            # Check for performance alerts
            self._check_performance_alerts(metrics)
    
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
        
        for alert in alerts:
            logger.warning(f"Performance Alert: {alert}")
            if len(alerts) == 1:  # Only print first alert to avoid spam
                print(f"⚠️  Performance Alert: {alert}")
    
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
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }
    
    def print_performance_report(self):
        """Print a formatted performance report."""
        stats = self.get_summary_stats()
        uptime_minutes = stats["uptime_seconds"] / 60
        
        print("\n📊 Performance Report")
        print("=" * 40)
        print(f"Uptime: {uptime_minutes:.1f} minutes")
        print(f"Total Operations: {stats['total_operations']}")
        print(f"Successful Operations: {stats['successful_operations']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        
        if stats['successful_operations'] > 0:
            print(f"Avg Response Time: {stats['avg_response_time']:.2f}s")
            print(f"Max Response Time: {stats['max_response_time']:.2f}s")
            print(f"Min Response Time: {stats['min_response_time']:.2f}s")
        
        print(f"Avg Memory Usage: {stats['avg_memory_usage']:.1f}MB")
        print(f"Avg CPU Usage: {stats['avg_cpu_usage']:.1f}%")
        print("=" * 40)
    
    def get_recent_failures(self, minutes: int = 5) -> List[PerformanceMetrics]:
        """Get recent failed operations within the specified time window."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        return [
            m for m in self.metrics_history 
            if not m.success and m.timestamp > cutoff_time
        ]
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health and resource usage."""
        # Get current system metrics
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Calculate health scores (0-100, where 100 is perfect)
        memory_health = max(0, 100 - memory.percent)
        disk_health = max(0, 100 - disk.percent)
        cpu_health = max(0, 100 - cpu_percent)
        
        # Overall health score
        overall_health = (memory_health + disk_health + cpu_health) / 3
        
        health_status = {
            "overall_health": overall_health,
            "status": "healthy" if overall_health > 80 else "warning" if overall_health > 60 else "critical",
            "memory": {
                "health_score": memory_health,
                "total_gb": memory.total / (1024**3),
                "available_gb": memory.available / (1024**3),
                "percent_used": memory.percent
            },
            "disk": {
                "health_score": disk_health,
                "total_gb": disk.total / (1024**3),
                "free_gb": disk.free / (1024**3),
                "percent_used": disk.percent
            },
            "cpu": {
                "health_score": cpu_health,
                "percent_used": cpu_percent,
                "core_count": psutil.cpu_count()
            }
        }
        
        return health_status
    
    def print_system_health(self):
        """Print system health information."""
        health = self.check_system_health()
        
        # Status emoji
        status_emoji = "🟢" if health["status"] == "healthy" else "🟡" if health["status"] == "warning" else "🔴"
        
        print(f"\n{status_emoji} System Health: {health['status'].title()} ({health['overall_health']:.1f}/100)")
        print("=" * 40)
        print(f"Memory: {health['memory']['available_gb']:.1f}GB free of {health['memory']['total_gb']:.1f}GB "
              f"({100-health['memory']['percent_used']:.1f}% available)")
        print(f"Disk: {health['disk']['free_gb']:.1f}GB free of {health['disk']['total_gb']:.1f}GB "
              f"({100-health['disk']['percent_used']:.1f}% available)")
        print(f"CPU: {health['cpu']['core_count']} cores, {100-health['cpu']['percent_used']:.1f}% available")
        print("=" * 40)

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    return performance_monitor

def monitor_agent_response(func):
    """Decorator to monitor agent response performance."""
    def wrapper(*args, **kwargs):
        with performance_monitor.monitor_operation("agent_response"):
            return func(*args, **kwargs)
    return wrapper