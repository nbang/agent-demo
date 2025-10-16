"""Constants and Enums for Multi-Agent System

Shared constants, enumerations, and configuration values used across
the multi-agent collaboration system.
"""

from enum import Enum
from typing import Dict, Any


class TeamType(Enum):
    """Types of multi-agent team collaborations."""
    RESEARCH = "research"
    CONTENT_CREATION = "content_creation"
    PROBLEM_SOLVING = "problem_solving"


class TeamStatus(Enum):
    """Status of multi-agent team."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class WorkflowType(Enum):
    """Types of workflow orchestration patterns."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"


class WorkflowStatus(Enum):
    """Status of workflow execution."""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class TaskStatus(Enum):
    """Status of individual tasks."""
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class MessageType(Enum):
    """Types of agent-to-agent messages."""
    INFORMATION = "information"
    REQUEST = "request"
    RESPONSE = "response"
    COORDINATION = "coordination"
    BROADCAST = "broadcast"


class MessagePriority(Enum):
    """Priority levels for agent messages."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class AgentRole(Enum):
    """Standard agent roles for collaboration."""
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    SYNTHESIZER = "synthesizer"
    WRITER = "writer"
    EDITOR = "editor"
    REVIEWER = "reviewer"
    PROBLEM_ANALYZER = "problem_analyzer"
    SOLUTION_STRATEGIST = "solution_strategist"
    IMPLEMENTATION_SPECIALIST = "implementation_specialist"


# Configuration Constants
DEFAULT_CONFIG: Dict[str, Any] = {
    "max_agents_per_team": 5,
    "min_agents_per_team": 2,
    "default_collaboration_timeout": 300,  # 5 minutes in seconds
    "quality_threshold": 0.8,
    "max_collaboration_rounds": 10,
    "coordination_overhead_limit": 0.2,  # 20%
    "success_rate_target": 0.9,  # 90%
}

# Performance Targets
PERFORMANCE_TARGETS: Dict[str, Any] = {
    "research_task_completion_time": 300,  # 5 minutes in seconds
    "coordination_overhead_max": 0.2,  # 20%
    "success_rate_min": 0.9,  # 90%
    "quality_score_min": 0.8,  # 80%
}

# Error Messages
ERROR_MESSAGES: Dict[str, str] = {
    "team_too_small": "Team must have at least {min_agents} agents",
    "team_too_large": "Team cannot have more than {max_agents} agents",
    "duplicate_roles": "Agent roles must be unique within a team",
    "invalid_team_type": "Team type must be one of: {valid_types}",
    "workflow_timeout": "Workflow execution exceeded timeout of {timeout} seconds",
    "quality_gate_failed": "Output quality score {score} below threshold {threshold}",
    "agent_communication_failed": "Failed to communicate with agent {agent_id}",
    "task_assignment_failed": "Failed to assign task {task_id} to agent {agent_id}",
}

# Default Agent Instructions
DEFAULT_AGENT_INSTRUCTIONS: Dict[str, str] = {
    AgentRole.RESEARCHER.value: "You are a research specialist. Gather comprehensive information on the given topic using available tools and sources. Focus on accuracy, relevance, and credible sources.",
    AgentRole.ANALYST.value: "You are a data analyst. Examine research findings, identify patterns, validate information, and provide analytical insights. Focus on accuracy and logical reasoning.",
    AgentRole.SYNTHESIZER.value: "You are a synthesis specialist. Combine findings from multiple sources into coherent, well-structured conclusions. Focus on clarity and comprehensive coverage.",
    AgentRole.WRITER.value: "You are a content writer. Create engaging, well-structured content based on research and requirements. Focus on clarity, readability, and audience engagement.",
    AgentRole.EDITOR.value: "You are a content editor. Review, refine, and improve content quality, structure, and style. Focus on accuracy, consistency, and readability.",
    AgentRole.REVIEWER.value: "You are a quality reviewer. Ensure content meets standards and requirements. Focus on quality assurance and constructive feedback.",
    AgentRole.PROBLEM_ANALYZER.value: "You are a problem analysis specialist. Break down complex problems into manageable components and identify key factors. Focus on systematic analysis.",
    AgentRole.SOLUTION_STRATEGIST.value: "You are a solution strategist. Develop strategic approaches and solution alternatives. Focus on feasibility and strategic thinking.",
    AgentRole.IMPLEMENTATION_SPECIALIST.value: "You are an implementation specialist. Create actionable plans and implementation strategies. Focus on practicality and execution details.",
}

# Tool Configurations by Role
DEFAULT_ROLE_TOOLS: Dict[str, list] = {
    AgentRole.RESEARCHER.value: ["web_search", "academic_search", "document_analysis"],
    AgentRole.ANALYST.value: ["data_analysis", "pattern_recognition", "validation_tools"],
    AgentRole.SYNTHESIZER.value: ["document_generation", "structure_analysis", "summary_tools"],
    AgentRole.WRITER.value: ["writing_tools", "style_guide", "content_templates"],
    AgentRole.EDITOR.value: ["editing_tools", "grammar_check", "style_analysis"],
    AgentRole.REVIEWER.value: ["quality_assessment", "review_templates", "feedback_tools"],
    AgentRole.PROBLEM_ANALYZER.value: ["analysis_frameworks", "decomposition_tools", "root_cause_analysis"],
    AgentRole.SOLUTION_STRATEGIST.value: ["strategy_frameworks", "decision_matrices", "scenario_analysis"],
    AgentRole.IMPLEMENTATION_SPECIALIST.value: ["project_planning", "task_breakdown", "resource_planning"],
}