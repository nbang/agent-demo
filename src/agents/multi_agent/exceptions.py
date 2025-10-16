"""Multi-Agent System Exceptions

Custom exception classes for multi-agent collaboration system errors.
"""

from typing import Optional, Dict, Any

class MultiAgentError(Exception):
    """Base exception for multi-agent system errors."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}


class TeamError(MultiAgentError):
    """Exception raised for team-related errors."""
    
    def __init__(self, message: str, team_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.team_id = team_id


class AgentRoleError(MultiAgentError):
    """Exception raised for agent role-related errors."""
    
    def __init__(self, message: str, role_name: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.role_name = role_name


class WorkflowError(MultiAgentError):
    """Exception raised for workflow orchestration errors."""
    
    def __init__(self, message: str, workflow_id: Optional[str] = None, step_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.workflow_id = workflow_id
        self.step_id = step_id


class CommunicationError(MultiAgentError):
    """Exception raised for agent communication errors."""
    
    def __init__(self, message: str, sender_id: Optional[str] = None, recipient_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.sender_id = sender_id
        self.recipient_id = recipient_id


class TaskAssignmentError(MultiAgentError):
    """Exception raised for task assignment errors."""
    
    def __init__(self, message: str, task_id: Optional[str] = None, agent_id: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.task_id = task_id
        self.agent_id = agent_id


class QualityGateError(MultiAgentError):
    """Exception raised when quality gates are not met."""
    
    def __init__(self, message: str, quality_score: Optional[float] = None, threshold: Optional[float] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.quality_score = quality_score
        self.threshold = threshold


class ResourceError(MultiAgentError):
    """Exception raised for resource-related errors."""
    
    def __init__(self, message: str, resource_type: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.resource_type = resource_type