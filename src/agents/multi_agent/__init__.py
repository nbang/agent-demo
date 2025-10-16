"""Multi-Agent Collaboration System

This module provides capabilities for creating and managing teams of AI agents
that collaborate on complex tasks like research, content creation, and problem-solving.

The system leverages the Agno framework's Agent and Team classes to coordinate
multiple agents with distinct roles, shared context, and workflow orchestration.
"""

from .team_manager import MultiAgentTeam, TeamConfiguration
from .agent_roles import AgentRole, RoleDefinition
from .shared_context import SharedContext
from .communication import AgentCommunication
from .exceptions import MultiAgentError, TeamError, WorkflowError

__version__ = "1.0.0"
__all__ = [
    "MultiAgentTeam",
    "TeamConfiguration",
    "AgentRole", 
    "RoleDefinition",
    "SharedContext",
    "AgentCommunication",
    "MultiAgentError",
    "TeamError", 
    "WorkflowError"
]