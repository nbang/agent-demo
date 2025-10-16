"""Collaboration Metrics for Multi-Agent Teams

Tracks and analyzes team coordination, communication patterns, and
collaborative effectiveness metrics.
"""

import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict


logger = logging.getLogger(__name__)


class InteractionType(Enum):
    """Types of agent interactions."""
    MESSAGE = "message"
    TASK_HANDOFF = "task_handoff"
    FEEDBACK = "feedback"
    COLLABORATION = "collaboration"
    COORDINATION = "coordination"
    CONFLICT = "conflict"
    CONSENSUS = "consensus"


class CollaborationPattern(Enum):
    """Patterns of collaboration observed."""
    SEQUENTIAL = "sequential"  # Linear task flow
    PARALLEL = "parallel"  # Simultaneous work
    HIERARCHICAL = "hierarchical"  # Leader-follower
    PEER_TO_PEER = "peer_to_peer"  # Equal collaboration
    HUB_AND_SPOKE = "hub_and_spoke"  # Central coordinator
    MESH = "mesh"  # Fully connected


@dataclass
class AgentInteraction:
    """Record of an interaction between agents."""
    
    timestamp: datetime
    from_agent_id: str
    to_agent_id: Optional[str]  # None for broadcast
    interaction_type: InteractionType
    content_summary: str
    duration_seconds: float = 0.0
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
            "metadata": self.metadata
        }


@dataclass
class AgentCollaborationMetrics:
    """Collaboration metrics for a specific agent."""
    
    agent_id: str
    agent_name: str
    
    # Communication metrics
    messages_sent: int = 0
    messages_received: int = 0
    direct_interactions: int = 0
    broadcast_interactions: int = 0
    
    # Collaboration metrics
    tasks_initiated: int = 0
    tasks_completed: int = 0
    tasks_handed_off: int = 0
    tasks_received: int = 0
    
    # Feedback metrics
    feedback_given: int = 0
    feedback_received: int = 0
    
    # Network metrics
    unique_collaborators: Set[str] = field(default_factory=set)
    interaction_frequency: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    # Timing metrics
    average_response_time_seconds: float = 0.0
    total_collaboration_time_seconds: float = 0.0
    
    def collaboration_score(self) -> float:
        """Calculate overall collaboration score (0-100).
        
        Returns:
            Collaboration score
        """
        score = 0.0
        
        # Communication score (30 points)
        total_messages = self.messages_sent + self.messages_received
        if total_messages > 0:
            score += min(30, total_messages * 3)
        
        # Task completion score (30 points)
        if self.tasks_initiated > 0:
            completion_rate = self.tasks_completed / self.tasks_initiated
            score += completion_rate * 30
        
        # Network diversity score (20 points)
        if len(self.unique_collaborators) > 0:
            score += min(20, len(self.unique_collaborators) * 5)
        
        # Feedback engagement score (20 points)
        total_feedback = self.feedback_given + self.feedback_received
        if total_feedback > 0:
            score += min(20, total_feedback * 4)
        
        return min(100.0, score)
    
    def responsiveness_score(self) -> float:
        """Calculate responsiveness score (0-100).
        
        Returns:
            Responsiveness score
        """
        if self.average_response_time_seconds == 0:
            return 100.0
        
        # Score inversely proportional to response time
        # Target: < 1 second = 100, > 10 seconds = 0
        if self.average_response_time_seconds <= 1.0:
            return 100.0
        elif self.average_response_time_seconds >= 10.0:
            return 0.0
        else:
            return 100.0 - ((self.average_response_time_seconds - 1.0) / 9.0) * 100.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "direct_interactions": self.direct_interactions,
            "broadcast_interactions": self.broadcast_interactions,
            "tasks_initiated": self.tasks_initiated,
            "tasks_completed": self.tasks_completed,
            "tasks_handed_off": self.tasks_handed_off,
            "tasks_received": self.tasks_received,
            "feedback_given": self.feedback_given,
            "feedback_received": self.feedback_received,
            "unique_collaborators": list(self.unique_collaborators),
            "collaboration_score": self.collaboration_score(),
            "responsiveness_score": self.responsiveness_score(),
            "average_response_time_seconds": self.average_response_time_seconds,
            "total_collaboration_time_seconds": self.total_collaboration_time_seconds
        }


@dataclass
class TeamCollaborationMetrics:
    """Overall team collaboration metrics."""
    
    team_id: str
    team_size: int
    start_time: datetime
    
    # Interaction metrics
    total_interactions: int = 0
    interaction_types: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    # Pattern metrics
    detected_patterns: List[CollaborationPattern] = field(default_factory=list)
    
    # Network metrics
    interaction_graph: Dict[str, Dict[str, int]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(int)))
    
    # Efficiency metrics
    average_task_completion_time: float = 0.0
    coordination_overhead_ratio: float = 0.0
    
    # Quality metrics
    consensus_rate: float = 0.0
    conflict_resolution_rate: float = 0.0
    
    def network_density(self) -> float:
        """Calculate network density (0-1).
        
        Returns:
            Network density score
        """
        if self.team_size <= 1:
            return 0.0
        
        # Count actual connections
        actual_connections = sum(
            len(targets) for targets in self.interaction_graph.values()
        )
        
        # Maximum possible connections (n * (n-1) for directed graph)
        max_connections = self.team_size * (self.team_size - 1)
        
        if max_connections == 0:
            return 0.0
        
        return actual_connections / max_connections
    
    def collaboration_efficiency(self) -> float:
        """Calculate collaboration efficiency score (0-100).
        
        Returns:
            Efficiency score
        """
        score = 100.0
        
        # Penalize high coordination overhead
        if self.coordination_overhead_ratio > 0.5:
            score -= 30
        elif self.coordination_overhead_ratio > 0.3:
            score -= 15
        
        # Reward high consensus
        if self.consensus_rate > 0.8:
            score += 0  # Already good
        elif self.consensus_rate < 0.5:
            score -= 20
        
        # Penalize unresolved conflicts
        if self.conflict_resolution_rate < 0.7:
            score -= 15
        
        return max(0.0, min(100.0, score))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "team_id": self.team_id,
            "team_size": self.team_size,
            "start_time": self.start_time.isoformat(),
            "total_interactions": self.total_interactions,
            "interaction_types": dict(self.interaction_types),
            "detected_patterns": [p.value for p in self.detected_patterns],
            "network_density": self.network_density(),
            "collaboration_efficiency": self.collaboration_efficiency(),
            "average_task_completion_time": self.average_task_completion_time,
            "coordination_overhead_ratio": self.coordination_overhead_ratio,
            "consensus_rate": self.consensus_rate,
            "conflict_resolution_rate": self.conflict_resolution_rate
        }


class CollaborationMetricsCollector:
    """Collects and analyzes collaboration metrics for multi-agent teams."""
    
    def __init__(self, team_id: str, team_size: int):
        """Initialize collaboration metrics collector.
        
        Args:
            team_id: Team identifier
            team_size: Number of agents in team
        """
        self.team_id = team_id
        self.team_size = team_size
        self.start_time = datetime.now()
        
        # Agent metrics
        self.agent_metrics: Dict[str, AgentCollaborationMetrics] = {}
        
        # Team metrics
        self.team_metrics = TeamCollaborationMetrics(
            team_id=team_id,
            team_size=team_size,
            start_time=self.start_time
        )
        
        # Interaction history
        self.interactions: List[AgentInteraction] = []
        
        # Response time tracking
        self.pending_responses: Dict[str, Tuple[str, datetime]] = {}  # message_id -> (to_agent, timestamp)
        
        logger.info(f"Collaboration metrics collector initialized for team: {team_id}")
    
    def register_agent(self, agent_id: str, agent_name: str):
        """Register an agent for metrics tracking.
        
        Args:
            agent_id: Agent identifier
            agent_name: Agent name
        """
        if agent_id not in self.agent_metrics:
            self.agent_metrics[agent_id] = AgentCollaborationMetrics(
                agent_id=agent_id,
                agent_name=agent_name
            )
            logger.debug(f"Registered agent for metrics: {agent_name}")
    
    def record_interaction(
        self,
        from_agent_id: str,
        to_agent_id: Optional[str],
        interaction_type: InteractionType,
        content_summary: str = "",
        duration_seconds: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record an interaction between agents.
        
        Args:
            from_agent_id: Source agent ID
            to_agent_id: Target agent ID (None for broadcast)
            interaction_type: Type of interaction
            content_summary: Brief description of interaction
            duration_seconds: Duration of interaction
            metadata: Additional metadata
        """
        # Ensure agents are registered
        if from_agent_id not in self.agent_metrics:
            self.register_agent(from_agent_id, from_agent_id)
        
        if to_agent_id and to_agent_id not in self.agent_metrics:
            self.register_agent(to_agent_id, to_agent_id)
        
        # Create interaction record
        interaction = AgentInteraction(
            timestamp=datetime.now(),
            from_agent_id=from_agent_id,
            to_agent_id=to_agent_id,
            interaction_type=interaction_type,
            content_summary=content_summary,
            duration_seconds=duration_seconds,
            metadata=metadata or {}
        )
        self.interactions.append(interaction)
        
        # Update team metrics
        self.team_metrics.total_interactions += 1
        self.team_metrics.interaction_types[interaction_type.value] += 1
        
        # Update interaction graph
        if to_agent_id:
            self.team_metrics.interaction_graph[from_agent_id][to_agent_id] += 1
        
        # Update agent metrics
        from_metrics = self.agent_metrics[from_agent_id]
        
        if interaction_type == InteractionType.MESSAGE:
            from_metrics.messages_sent += 1
            if to_agent_id:
                from_metrics.direct_interactions += 1
                self.agent_metrics[to_agent_id].messages_received += 1
            else:
                from_metrics.broadcast_interactions += 1
        
        elif interaction_type == InteractionType.TASK_HANDOFF:
            from_metrics.tasks_handed_off += 1
            if to_agent_id:
                self.agent_metrics[to_agent_id].tasks_received += 1
        
        elif interaction_type == InteractionType.FEEDBACK:
            from_metrics.feedback_given += 1
            if to_agent_id:
                self.agent_metrics[to_agent_id].feedback_received += 1
        
        # Update collaborators
        if to_agent_id:
            from_metrics.unique_collaborators.add(to_agent_id)
            from_metrics.interaction_frequency[to_agent_id] += 1
            
            to_metrics = self.agent_metrics[to_agent_id]
            to_metrics.unique_collaborators.add(from_agent_id)
            to_metrics.interaction_frequency[from_agent_id] += 1
        
        # Update collaboration time
        if duration_seconds > 0:
            from_metrics.total_collaboration_time_seconds += duration_seconds
    
    def record_task_start(self, agent_id: str, task_id: str):
        """Record task initiation by an agent.
        
        Args:
            agent_id: Agent identifier
            task_id: Task identifier
        """
        if agent_id in self.agent_metrics:
            self.agent_metrics[agent_id].tasks_initiated += 1
    
    def record_task_completion(self, agent_id: str, task_id: str, duration_seconds: float = 0.0):
        """Record task completion by an agent.
        
        Args:
            agent_id: Agent identifier
            task_id: Task identifier
            duration_seconds: Task duration
        """
        if agent_id in self.agent_metrics:
            self.agent_metrics[agent_id].tasks_completed += 1
            
            # Update team average
            if duration_seconds > 0:
                current_avg = self.team_metrics.average_task_completion_time
                total_tasks = sum(m.tasks_completed for m in self.agent_metrics.values())
                
                if total_tasks > 0:
                    self.team_metrics.average_task_completion_time = (
                        (current_avg * (total_tasks - 1) + duration_seconds) / total_tasks
                    )
    
    def record_response(
        self,
        message_id: str,
        from_agent_id: str,
        to_agent_id: str
    ):
        """Record a response to track response times.
        
        Args:
            message_id: Message identifier
            from_agent_id: Responding agent
            to_agent_id: Original sender
        """
        if message_id in self.pending_responses:
            original_to, timestamp = self.pending_responses.pop(message_id)
            
            if original_to == from_agent_id:
                response_time = (datetime.now() - timestamp).total_seconds()
                
                # Update agent metrics
                if from_agent_id in self.agent_metrics:
                    metrics = self.agent_metrics[from_agent_id]
                    
                    # Update average response time
                    if metrics.average_response_time_seconds == 0:
                        metrics.average_response_time_seconds = response_time
                    else:
                        # Moving average
                        metrics.average_response_time_seconds = (
                            metrics.average_response_time_seconds * 0.8 + response_time * 0.2
                        )
    
    def track_message_for_response(
        self,
        message_id: str,
        to_agent_id: str
    ):
        """Start tracking a message for response time.
        
        Args:
            message_id: Message identifier
            to_agent_id: Expected responder
        """
        self.pending_responses[message_id] = (to_agent_id, datetime.now())
    
    def detect_collaboration_patterns(self) -> List[CollaborationPattern]:
        """Detect collaboration patterns in team interactions.
        
        Returns:
            List of detected patterns
        """
        patterns = []
        
        if len(self.interactions) < 5:
            return patterns
        
        # Analyze interaction graph
        graph = self.team_metrics.interaction_graph
        
        # Check for hub-and-spoke (one agent interacts with all others)
        for agent_id, targets in graph.items():
            if len(targets) >= self.team_size - 1:
                if CollaborationPattern.HUB_AND_SPOKE not in patterns:
                    patterns.append(CollaborationPattern.HUB_AND_SPOKE)
                break
        
        # Check for mesh (all agents interact with each other)
        network_density = self.team_metrics.network_density()
        if network_density > 0.8:
            patterns.append(CollaborationPattern.MESH)
        
        # Check for sequential (linear task flow)
        # Look for task handoffs in sequence
        task_handoffs = [
            i for i in self.interactions
            if i.interaction_type == InteractionType.TASK_HANDOFF
        ]
        if len(task_handoffs) >= 3:
            patterns.append(CollaborationPattern.SEQUENTIAL)
        
        # Check for parallel (simultaneous work)
        # Look for overlapping activities
        time_buckets = defaultdict(set)
        for interaction in self.interactions[-20:]:  # Last 20 interactions
            bucket = interaction.timestamp.replace(second=0, microsecond=0)
            time_buckets[bucket].add(interaction.from_agent_id)
        
        for bucket, agents in time_buckets.items():
            if len(agents) >= max(2, self.team_size // 2):
                if CollaborationPattern.PARALLEL not in patterns:
                    patterns.append(CollaborationPattern.PARALLEL)
                break
        
        # Check for peer-to-peer (balanced interactions)
        if network_density > 0.4:
            # Check if interactions are relatively balanced
            interaction_counts = defaultdict(int)
            for agent_id, targets in graph.items():
                for target_id, count in targets.items():
                    interaction_counts[agent_id] += count
            
            if interaction_counts:
                values = list(interaction_counts.values())
                avg = sum(values) / len(values)
                variance = sum((v - avg) ** 2 for v in values) / len(values)
                
                if variance < avg:  # Low variance = balanced
                    patterns.append(CollaborationPattern.PEER_TO_PEER)
        
        self.team_metrics.detected_patterns = patterns
        return patterns
    
    def calculate_coordination_overhead(self) -> float:
        """Calculate coordination overhead ratio.
        
        Returns:
            Coordination overhead ratio (0-1)
        """
        if self.team_metrics.total_interactions == 0:
            return 0.0
        
        # Count coordination interactions
        coordination_types = [
            InteractionType.COORDINATION,
            InteractionType.CONSENSUS,
            InteractionType.CONFLICT
        ]
        
        coordination_count = sum(
            self.team_metrics.interaction_types.get(ct.value, 0)
            for ct in coordination_types
        )
        
        # Calculate ratio
        overhead = coordination_count / self.team_metrics.total_interactions
        self.team_metrics.coordination_overhead_ratio = overhead
        
        return overhead
    
    def calculate_consensus_rate(self) -> float:
        """Calculate consensus achievement rate.
        
        Returns:
            Consensus rate (0-1)
        """
        consensus_count = self.team_metrics.interaction_types.get(
            InteractionType.CONSENSUS.value, 0
        )
        coordination_count = self.team_metrics.interaction_types.get(
            InteractionType.COORDINATION.value, 0
        )
        
        if coordination_count == 0:
            return 1.0  # No coordination needed = perfect consensus
        
        rate = consensus_count / coordination_count if coordination_count > 0 else 0.0
        self.team_metrics.consensus_rate = rate
        
        return rate
    
    def get_collaboration_summary(self) -> Dict[str, Any]:
        """Get comprehensive collaboration summary.
        
        Returns:
            Collaboration summary dictionary
        """
        # Update calculated metrics
        self.detect_collaboration_patterns()
        self.calculate_coordination_overhead()
        self.calculate_consensus_rate()
        
        # Calculate team-level scores
        agent_scores = [
            m.collaboration_score()
            for m in self.agent_metrics.values()
        ]
        
        avg_collaboration_score = (
            sum(agent_scores) / len(agent_scores)
            if agent_scores else 0.0
        )
        
        return {
            "team_metrics": self.team_metrics.to_dict(),
            "agent_metrics": {
                agent_id: metrics.to_dict()
                for agent_id, metrics in self.agent_metrics.items()
            },
            "average_collaboration_score": avg_collaboration_score,
            "total_agents": len(self.agent_metrics),
            "total_interactions": len(self.interactions),
            "monitoring_duration_seconds": (
                datetime.now() - self.start_time
            ).total_seconds()
        }
    
    def print_collaboration_summary(self):
        """Print collaboration summary to console."""
        summary = self.get_collaboration_summary()
        
        print("\n" + "="*70)
        print(f"🤝 COLLABORATION SUMMARY - Team: {self.team_id}")
        print("="*70)
        
        team = summary["team_metrics"]
        print(f"\n👥 Team Size: {team['team_size']}")
        print(f"📊 Total Interactions: {team['total_interactions']}")
        print(f"🔗 Network Density: {team['network_density']:.2%}")
        print(f"⚡ Collaboration Efficiency: {team['collaboration_efficiency']:.1f}/100")
        
        if team['detected_patterns']:
            print(f"\n🔍 Detected Patterns:")
            for pattern in team['detected_patterns']:
                print(f"   • {pattern.replace('_', ' ').title()}")
        
        print(f"\n📈 Team Metrics:")
        print(f"   Coordination Overhead: {team['coordination_overhead_ratio']:.1%}")
        print(f"   Consensus Rate: {team['consensus_rate']:.1%}")
        if team['average_task_completion_time'] > 0:
            print(f"   Avg Task Completion: {team['average_task_completion_time']:.2f}s")
        
        print(f"\n🌟 Average Collaboration Score: {summary['average_collaboration_score']:.1f}/100")
        
        if summary['agent_metrics']:
            print(f"\n👤 Top Collaborators:")
            # Sort by collaboration score
            sorted_agents = sorted(
                summary['agent_metrics'].items(),
                key=lambda x: x[1]['collaboration_score'],
                reverse=True
            )
            
            for i, (agent_id, metrics) in enumerate(sorted_agents[:5], 1):
                print(f"   {i}. {metrics['agent_name']}:")
                print(f"      Score: {metrics['collaboration_score']:.1f}/100")
                print(f"      Messages: {metrics['messages_sent']}↑ {metrics['messages_received']}↓")
                print(f"      Collaborators: {len(metrics['unique_collaborators'])}")
        
        print("\n" + "="*70)
    
    def export_network_graph(self) -> Dict[str, Any]:
        """Export interaction network as graph data.
        
        Returns:
            Graph data in node-link format
        """
        nodes = [
            {
                "id": agent_id,
                "name": metrics.agent_name,
                "collaboration_score": metrics.collaboration_score(),
                "messages_sent": metrics.messages_sent,
                "messages_received": metrics.messages_received
            }
            for agent_id, metrics in self.agent_metrics.items()
        ]
        
        links = []
        for from_id, targets in self.team_metrics.interaction_graph.items():
            for to_id, count in targets.items():
                links.append({
                    "source": from_id,
                    "target": to_id,
                    "weight": count
                })
        
        return {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "team_id": self.team_id,
                "network_density": self.team_metrics.network_density(),
                "patterns": [p.value for p in self.team_metrics.detected_patterns]
            }
        }


# Convenience function
def create_collaboration_metrics(
    team_id: str,
    team_size: int
) -> CollaborationMetricsCollector:
    """Create and initialize a collaboration metrics collector.
    
    Args:
        team_id: Team identifier
        team_size: Number of agents in team
    
    Returns:
        Initialized CollaborationMetricsCollector
    """
    return CollaborationMetricsCollector(team_id, team_size)
