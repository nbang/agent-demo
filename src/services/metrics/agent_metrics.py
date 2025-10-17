"""Agent Metrics for Agno Agent System

Provides comprehensive metrics tracking for agents including collaboration,
performance, and interaction patterns. Can be used for all agent types.
"""

import logging
from typing import Dict, List, Any, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict


logger = logging.getLogger(__name__)


class InteractionType(Enum):
    """Types of agent interactions."""
    MESSAGE = "message"
    TASK_HANDOFF = "task_handoff"
    TASK_REQUEST = "task_request"
    FEEDBACK = "feedback"
    COLLABORATION = "collaboration"
    COORDINATION = "coordination"
    CONFLICT = "conflict"
    CONSENSUS = "consensus"
    API_CALL = "api_call"
    USER_INTERACTION = "user_interaction"
    SYSTEM_EVENT = "system_event"


class CollaborationPattern(Enum):
    """Patterns of collaboration observed."""
    SEQUENTIAL = "sequential"  # Linear task flow
    PARALLEL = "parallel"  # Simultaneous work
    HIERARCHICAL = "hierarchical"  # Leader-follower
    PEER_TO_PEER = "peer_to_peer"  # Equal collaboration
    HUB_AND_SPOKE = "hub_and_spoke"  # Central coordinator
    MESH = "mesh"  # Fully connected
    SINGLE_AGENT = "single_agent"  # No collaboration


class MetricCategory(Enum):
    """Categories of metrics."""
    PERFORMANCE = "performance"
    COLLABORATION = "collaboration"
    COMMUNICATION = "communication"
    QUALITY = "quality"
    EFFICIENCY = "efficiency"
    RELIABILITY = "reliability"


@dataclass
class AgentInteraction:
    """Record of an interaction involving an agent."""
    
    timestamp: datetime
    from_agent_id: str
    to_agent_id: Optional[str]  # None for broadcast or system interactions
    interaction_type: InteractionType
    content_summary: str
    duration_seconds: float = 0.0
    success: bool = True
    agent_type: Optional[str] = None
    team_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "from_agent_id": self.from_agent_id,
            "to_agent_id": self.to_agent_id,
            "interaction_type": self.interaction_type.value,
            "content_summary": self.content_summary,
            "duration_seconds": self.duration_seconds,
            "success": self.success,
            "agent_type": self.agent_type,
            "team_id": self.team_id,
            "metadata": self.metadata
        }


@dataclass
class TaskMetric:
    """Metrics for a specific task or operation."""
    
    task_id: str
    task_type: str
    agent_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    success: bool = False
    quality_score: float = 0.0  # 0-100
    complexity_score: float = 0.0  # 0-100
    resource_usage: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def duration_seconds(self) -> float:
        """Calculate task duration in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "agent_id": self.agent_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "success": self.success,
            "quality_score": self.quality_score,
            "complexity_score": self.complexity_score,
            "duration_seconds": self.duration_seconds(),
            "resource_usage": self.resource_usage,
            "metadata": self.metadata
        }


@dataclass
class AgentMetrics:
    """Comprehensive metrics for an agent."""
    
    agent_id: str
    agent_type: str
    agent_name: Optional[str] = None
    team_id: Optional[str] = None
    
    # Task metrics
    tasks_initiated: int = 0
    tasks_completed: int = 0
    tasks_failed: int = 0
    average_task_duration_seconds: float = 0.0
    average_quality_score: float = 0.0
    
    # Communication metrics (for multi-agent systems)
    messages_sent: int = 0
    messages_received: int = 0
    direct_interactions: int = 0
    broadcast_interactions: int = 0
    
    # Collaboration metrics (for multi-agent systems)
    tasks_handed_off: int = 0
    tasks_received: int = 0
    feedback_given: int = 0
    feedback_received: int = 0
    
    # Performance metrics
    api_calls_made: int = 0
    total_execution_time_seconds: float = 0.0
    average_response_time_seconds: float = 0.0
    error_count: int = 0
    
    # Network metrics (for multi-agent systems)
    unique_collaborators: Set[str] = field(default_factory=set)
    interaction_frequency: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    # Quality metrics
    user_satisfaction_scores: List[float] = field(default_factory=list)
    peer_feedback_scores: List[float] = field(default_factory=list)
    
    # Efficiency metrics
    resource_utilization: Dict[str, float] = field(default_factory=dict)
    
    def success_rate(self) -> float:
        """Calculate task success rate."""
        total_tasks = self.tasks_completed + self.tasks_failed
        if total_tasks == 0:
            return 0.0
        return self.tasks_completed / total_tasks
    
    def error_rate(self) -> float:
        """Calculate error rate."""
        total_operations = self.tasks_completed + self.tasks_failed + self.error_count
        if total_operations == 0:
            return 0.0
        return self.error_count / total_operations
    
    def collaboration_score(self) -> float:
        """Calculate collaboration effectiveness score (0-100)."""
        if self.agent_type == "single_agent" or not self.unique_collaborators:
            return 0.0  # Single agents don't collaborate
        
        # Base score on various collaboration factors
        score = 0.0
        
        # Communication effectiveness (0-25 points)
        if self.messages_sent + self.messages_received > 0:
            communication_balance = min(self.messages_sent, self.messages_received) / max(self.messages_sent, self.messages_received, 1)
            score += communication_balance * 25
        
        # Collaboration breadth (0-25 points)
        collaboration_breadth = min(len(self.unique_collaborators) / 5, 1.0)  # Normalize to 5 collaborators
        score += collaboration_breadth * 25
        
        # Task handoff effectiveness (0-25 points)
        if self.tasks_handed_off + self.tasks_received > 0:
            handoff_balance = min(self.tasks_handed_off, self.tasks_received) / max(self.tasks_handed_off, self.tasks_received, 1)
            score += handoff_balance * 25
        
        # Feedback participation (0-25 points)
        if self.feedback_given + self.feedback_received > 0:
            feedback_balance = min(self.feedback_given, self.feedback_received) / max(self.feedback_given, self.feedback_received, 1)
            score += feedback_balance * 25
        
        return score
    
    def overall_score(self) -> float:
        """Calculate overall agent performance score (0-100)."""
        # Weighted combination of different metrics
        success_weight = 0.3
        quality_weight = 0.25
        efficiency_weight = 0.2
        collaboration_weight = 0.15 if self.agent_type == "multi_agent" else 0.0
        reliability_weight = 0.1 if self.agent_type == "multi_agent" else 0.45
        
        success_score = self.success_rate() * 100
        quality_score = self.average_quality_score
        efficiency_score = max(0, 100 - (self.average_response_time_seconds * 10))  # Penalize slow response
        collaboration_score = self.collaboration_score()
        reliability_score = max(0, 100 - (self.error_rate() * 100))
        
        overall = (
            success_score * success_weight +
            quality_score * quality_weight +
            efficiency_score * efficiency_weight +
            collaboration_score * collaboration_weight +
            reliability_score * reliability_weight
        )
        
        return min(100.0, overall)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "agent_name": self.agent_name,
            "team_id": self.team_id,
            "tasks_initiated": self.tasks_initiated,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "success_rate": self.success_rate(),
            "average_task_duration_seconds": self.average_task_duration_seconds,
            "average_quality_score": self.average_quality_score,
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "direct_interactions": self.direct_interactions,
            "broadcast_interactions": self.broadcast_interactions,
            "tasks_handed_off": self.tasks_handed_off,
            "tasks_received": self.tasks_received,
            "feedback_given": self.feedback_given,
            "feedback_received": self.feedback_received,
            "api_calls_made": self.api_calls_made,
            "total_execution_time_seconds": self.total_execution_time_seconds,
            "average_response_time_seconds": self.average_response_time_seconds,
            "error_count": self.error_count,
            "error_rate": self.error_rate(),
            "unique_collaborators_count": len(self.unique_collaborators),
            "collaboration_score": self.collaboration_score(),
            "overall_score": self.overall_score(),
            "resource_utilization": self.resource_utilization
        }


class AgentMetricsCollector:
    """Collects and analyzes metrics for agents."""
    
    def __init__(self, agent_type: str = "generic", team_id: Optional[str] = None):
        """Initialize metrics collector.
        
        Args:
            agent_type: Type of agent (e.g., 'basic', 'multi_agent', 'reasoning')
            team_id: Optional team identifier for multi-agent systems
        """
        self.agent_type = agent_type
        self.team_id = team_id
        
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.interactions: List[AgentInteraction] = []
        self.tasks: Dict[str, TaskMetric] = {}
        self.start_time = datetime.now()
        
        # Pattern detection
        self.detected_patterns: Set[CollaborationPattern] = set()
        self.pattern_confidence: Dict[CollaborationPattern, float] = {}
    
    def get_or_create_agent_metrics(self, agent_id: str, agent_name: Optional[str] = None) -> AgentMetrics:
        """Get or create metrics for an agent."""
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentMetrics(
                agent_id=agent_id,
                agent_type=self.agent_type,
                agent_name=agent_name,
                team_id=self.team_id
            )
        return self.agent_metrics[agent_id]
    
    def record_interaction(self, interaction: AgentInteraction):
        """Record an agent interaction."""
        self.interactions.append(interaction)
        
        # Update agent metrics
        from_agent = self.get_or_create_agent_metrics(interaction.from_agent_id)
        from_agent.messages_sent += 1
        
        if interaction.to_agent_id:
            to_agent = self.get_or_create_agent_metrics(interaction.to_agent_id)
            to_agent.messages_received += 1
            from_agent.direct_interactions += 1
            from_agent.unique_collaborators.add(interaction.to_agent_id)
            from_agent.interaction_frequency[interaction.to_agent_id] += 1
        else:
            from_agent.broadcast_interactions += 1
        
        # Update interaction type counters
        if interaction.interaction_type == InteractionType.FEEDBACK:
            from_agent.feedback_given += 1
            if interaction.to_agent_id:
                to_agent = self.get_or_create_agent_metrics(interaction.to_agent_id)
                to_agent.feedback_received += 1
        
        elif interaction.interaction_type == InteractionType.TASK_HANDOFF:
            from_agent.tasks_handed_off += 1
            if interaction.to_agent_id:
                to_agent = self.get_or_create_agent_metrics(interaction.to_agent_id)
                to_agent.tasks_received += 1
    
    def start_task(self, task_id: str, task_type: str, agent_id: str, complexity_score: float = 0.0) -> TaskMetric:
        """Start tracking a task."""
        task = TaskMetric(
            task_id=task_id,
            task_type=task_type,
            agent_id=agent_id,
            start_time=datetime.now(),
            complexity_score=complexity_score
        )
        
        self.tasks[task_id] = task
        
        # Update agent metrics
        agent_metrics = self.get_or_create_agent_metrics(agent_id)
        agent_metrics.tasks_initiated += 1
        
        return task
    
    def complete_task(self, task_id: str, success: bool = True, quality_score: float = 0.0, resource_usage: Optional[Dict[str, float]] = None):
        """Mark a task as completed."""
        if task_id not in self.tasks:
            logger.warning(f"Task {task_id} not found in metrics")
            return
        
        task = self.tasks[task_id]
        task.end_time = datetime.now()
        task.success = success
        task.quality_score = quality_score
        if resource_usage:
            task.resource_usage.update(resource_usage)
        
        # Update agent metrics
        agent_metrics = self.get_or_create_agent_metrics(task.agent_id)
        
        if success:
            agent_metrics.tasks_completed += 1
        else:
            agent_metrics.tasks_failed += 1
        
        # Update averages
        completed_tasks = [t for t in self.tasks.values() if t.end_time and t.success]
        if completed_tasks:
            total_duration = sum(t.duration_seconds() for t in completed_tasks)
            agent_metrics.average_task_duration_seconds = total_duration / len(completed_tasks)
            
            total_quality = sum(t.quality_score for t in completed_tasks if t.quality_score > 0)
            quality_tasks = [t for t in completed_tasks if t.quality_score > 0]
            if quality_tasks:
                agent_metrics.average_quality_score = total_quality / len(quality_tasks)
    
    def record_api_call(self, agent_id: str, response_time_seconds: float, success: bool = True):
        """Record an API call made by an agent."""
        agent_metrics = self.get_or_create_agent_metrics(agent_id)
        agent_metrics.api_calls_made += 1
        
        if not success:
            agent_metrics.error_count += 1
        
        # Update average response time
        total_response_time = agent_metrics.average_response_time_seconds * (agent_metrics.api_calls_made - 1) + response_time_seconds
        agent_metrics.average_response_time_seconds = total_response_time / agent_metrics.api_calls_made
    
    def record_user_satisfaction(self, agent_id: str, satisfaction_score: float):
        """Record user satisfaction score for an agent (0-100)."""
        agent_metrics = self.get_or_create_agent_metrics(agent_id)
        agent_metrics.user_satisfaction_scores.append(satisfaction_score)
    
    def detect_collaboration_patterns(self) -> Dict[CollaborationPattern, float]:
        """Detect collaboration patterns from interaction data."""
        if not self.interactions:
            self.detected_patterns.add(CollaborationPattern.SINGLE_AGENT)
            self.pattern_confidence[CollaborationPattern.SINGLE_AGENT] = 1.0
            return self.pattern_confidence
        
        # Analyze interaction patterns
        agent_connections = defaultdict(set)
        interaction_matrix = defaultdict(lambda: defaultdict(int))
        
        for interaction in self.interactions:
            if interaction.to_agent_id:
                agent_connections[interaction.from_agent_id].add(interaction.to_agent_id)
                interaction_matrix[interaction.from_agent_id][interaction.to_agent_id] += 1
        
        agents = set(self.agent_metrics.keys())
        num_agents = len(agents)
        
        if num_agents <= 1:
            self.pattern_confidence[CollaborationPattern.SINGLE_AGENT] = 1.0
            return self.pattern_confidence
        
        # Sequential pattern: linear chain of interactions
        sequential_score = self._calculate_sequential_pattern_score(interaction_matrix, agents)
        if sequential_score > 0.7:
            self.pattern_confidence[CollaborationPattern.SEQUENTIAL] = sequential_score
        
        # Hierarchical pattern: one central coordinator
        hierarchical_score = self._calculate_hierarchical_pattern_score(interaction_matrix, agents)
        if hierarchical_score > 0.7:
            self.pattern_confidence[CollaborationPattern.HIERARCHICAL] = hierarchical_score
        
        # Hub and spoke pattern
        hub_spoke_score = self._calculate_hub_spoke_pattern_score(interaction_matrix, agents)
        if hub_spoke_score > 0.7:
            self.pattern_confidence[CollaborationPattern.HUB_AND_SPOKE] = hub_spoke_score
        
        # Mesh pattern: everyone talks to everyone
        mesh_score = self._calculate_mesh_pattern_score(agent_connections, agents)
        if mesh_score > 0.7:
            self.pattern_confidence[CollaborationPattern.MESH] = mesh_score
        
        # Peer-to-peer: balanced interactions
        p2p_score = self._calculate_p2p_pattern_score(interaction_matrix, agents)
        if p2p_score > 0.7:
            self.pattern_confidence[CollaborationPattern.PEER_TO_PEER] = p2p_score
        
        return self.pattern_confidence
    
    def _calculate_sequential_pattern_score(self, interaction_matrix: Dict, agents: Set[str]) -> float:
        """Calculate score for sequential collaboration pattern."""
        # Sequential means mostly linear chains of interaction
        # Implementation would analyze the interaction flow
        return 0.0  # Placeholder
    
    def _calculate_hierarchical_pattern_score(self, interaction_matrix: Dict, agents: Set[str]) -> float:
        """Calculate score for hierarchical collaboration pattern."""
        # Look for one agent that sends many messages and receives few
        return 0.0  # Placeholder
    
    def _calculate_hub_spoke_pattern_score(self, interaction_matrix: Dict, agents: Set[str]) -> float:
        """Calculate score for hub-and-spoke collaboration pattern."""
        # One central hub connected to all others, others don't connect to each other
        return 0.0  # Placeholder
    
    def _calculate_mesh_pattern_score(self, agent_connections: Dict, agents: Set[str]) -> float:
        """Calculate score for mesh collaboration pattern."""
        if len(agents) <= 1:
            return 0.0
        
        total_possible_connections = len(agents) * (len(agents) - 1)
        actual_connections = sum(len(connections) for connections in agent_connections.values())
        
        return actual_connections / total_possible_connections if total_possible_connections > 0 else 0.0
    
    def _calculate_p2p_pattern_score(self, interaction_matrix: Dict, agents: Set[str]) -> float:
        """Calculate score for peer-to-peer collaboration pattern."""
        # Balanced interactions between agents
        return 0.0  # Placeholder
    
    def get_team_summary(self) -> Dict[str, Any]:
        """Get summary metrics for the entire team/system."""
        if not self.agent_metrics:
            return {"total_agents": 0}
        
        total_tasks = sum(m.tasks_completed + m.tasks_failed for m in self.agent_metrics.values())
        total_successful = sum(m.tasks_completed for m in self.agent_metrics.values())
        total_interactions = len(self.interactions)
        
        # Calculate averages
        avg_quality = sum(m.average_quality_score for m in self.agent_metrics.values()) / len(self.agent_metrics)
        avg_response_time = sum(m.average_response_time_seconds for m in self.agent_metrics.values()) / len(self.agent_metrics)
        avg_collaboration_score = sum(m.collaboration_score() for m in self.agent_metrics.values()) / len(self.agent_metrics)
        
        return {
            "total_agents": len(self.agent_metrics),
            "total_tasks": total_tasks,
            "total_successful_tasks": total_successful,
            "overall_success_rate": total_successful / total_tasks if total_tasks > 0 else 0.0,
            "total_interactions": total_interactions,
            "average_quality_score": avg_quality,
            "average_response_time_seconds": avg_response_time,
            "average_collaboration_score": avg_collaboration_score,
            "detected_patterns": [pattern.value for pattern in self.detected_patterns],
            "pattern_confidence": {pattern.value: score for pattern, score in self.pattern_confidence.items()},
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "agent_type": self.agent_type,
            "team_id": self.team_id
        }
    
    def get_agent_summary(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get summary for a specific agent."""
        if agent_id not in self.agent_metrics:
            return None
        
        return self.agent_metrics[agent_id].to_dict()
    
    def get_all_agents_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary for all agents."""
        return {
            agent_id: metrics.to_dict()
            for agent_id, metrics in self.agent_metrics.items()
        }
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics for persistence or analysis."""
        return {
            "team_summary": self.get_team_summary(),
            "agent_metrics": self.get_all_agents_summary(),
            "interactions": [interaction.to_dict() for interaction in self.interactions],
            "tasks": {task_id: task.to_dict() for task_id, task in self.tasks.items()},
            "collaboration_patterns": {
                pattern.value: score for pattern, score in self.pattern_confidence.items()
            }
        }
    
    def reset_metrics(self):
        """Reset all metrics."""
        self.agent_metrics.clear()
        self.interactions.clear()
        self.tasks.clear()
        self.detected_patterns.clear()
        self.pattern_confidence.clear()
        self.start_time = datetime.now()
        logger.info("Agent metrics reset")


# Global metrics collector
default_metrics_collector = AgentMetricsCollector()


# Convenience functions for backward compatibility
def create_collaboration_metrics_collector(team_id: str) -> AgentMetricsCollector:
    """Create metrics collector for multi-agent collaboration (backward compatibility).
    
    Args:
        team_id: Team identifier
    
    Returns:
        AgentMetricsCollector instance
    """
    return AgentMetricsCollector("multi_agent", team_id)