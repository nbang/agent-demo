"""Team Manager Orchestration

Coordinates multi-agent teams and orchestrates their collaboration.
"""

import time
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

try:
    from agno.agent import Agent
    from agno.team import Team
except ImportError:
    try:
        # Try alternative import
        from agno import agent as agno_agent
        Agent = agno_agent.Agent if hasattr(agno_agent, 'Agent') else None
        Team = None  # Team may not be available in current agno version
    except:
        Agent = None
        Team = None

from .constants import TeamType, TeamStatus, DEFAULT_CONFIG
from .exceptions import TeamError, MultiAgentError
from .agent_roles import RoleDefinition, role_manager
from .shared_context import SharedContext
from .communication import AgentCommunication
from .logging_config import get_multi_agent_logger

logger = get_multi_agent_logger("team_manager")


@dataclass
class TeamConfiguration:
    """Configuration for a multi-agent team."""
    
    team_name: str
    team_type: TeamType
    max_agents: int = DEFAULT_CONFIG["max_agents_per_team"]
    collaboration_timeout: int = DEFAULT_CONFIG["default_collaboration_timeout"]
    quality_threshold: float = DEFAULT_CONFIG["quality_threshold"]
    max_rounds: int = DEFAULT_CONFIG["max_collaboration_rounds"]


class MultiAgentTeam:
    """Manages a team of AI agents working collaboratively."""
    
    def __init__(self, config: TeamConfiguration):
        self.team_id = f"team_{int(time.time())}_{str(uuid.uuid4())[:8]}"
        self.config = config
        self.status = TeamStatus.INACTIVE
        self.created_at = time.time()
        
        # Core components
        self.shared_context = SharedContext(self.team_id)
        self.communication = AgentCommunication(self.team_id)
        
        # Team composition
        self.agents: Dict[str, Agent] = {}
        self.agent_roles: Dict[str, RoleDefinition] = {}
        self.agno_team: Optional[Team] = None
        
        # Collaboration state
        self.current_task: Optional[str] = None
        self.collaboration_start_time: Optional[float] = None
        self.collaboration_results: Optional[Dict[str, Any]] = None
        
        logger.info(f"Created multi-agent team {self.team_id} of type {config.team_type.value}")
    
    def add_agent(self, agent_id: str, role_id: str, agent_config: Optional[Dict[str, Any]] = None) -> Agent:
        """Add an agent to the team with a specific role.
        
        Args:
            agent_id: Unique identifier for the agent
            role_id: Role identifier from role manager
            agent_config: Optional agent configuration overrides
            
        Returns:
            The created Agent instance
            
        Raises:
            TeamError: If team is full, role is duplicate, or agent creation fails
        """
        if len(self.agents) >= self.config.max_agents:
            raise TeamError(f"Team cannot have more than {self.config.max_agents} agents", self.team_id)
        
        if role_id in self.agent_roles:
            raise TeamError(f"Role {role_id} already assigned in team", self.team_id)
        
        # Get role definition
        try:
            role_def = role_manager.get_role(role_id)
        except Exception as e:
            raise TeamError(f"Failed to get role definition for {role_id}: {e}", self.team_id)
        
        # Create agent configuration
        agent_config = agent_config or {}
        agent_config.setdefault("instructions", role_def.instructions)
        agent_config.setdefault("tools", role_def.tools)
        
        # Create Agno agent
        try:
            agent = Agent(
                name=f"{role_def.name}_{agent_id}",
                role=role_id,
                **agent_config
            )
        except Exception as e:
            raise TeamError(f"Failed to create agent {agent_id}: {e}", self.team_id)
        
        # Add to team
        self.agents[agent_id] = agent
        self.agent_roles[agent_id] = role_def
        
        # Register for communication
        self.communication.register_agent(agent_id)
        
        # Update shared context
        self.shared_context.set(
            f"agent_{agent_id}_role",
            role_id,
            updated_by="team_manager"
        )
        
        logger.info(f"Added agent {agent_id} with role {role_id} to team {self.team_id}")
        return agent
    
    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent from the team.
        
        Args:
            agent_id: ID of agent to remove
            
        Raises:
            TeamError: If agent not found or team becomes too small
        """
        if agent_id not in self.agents:
            raise TeamError(f"Agent {agent_id} not found in team", self.team_id)
        
        if len(self.agents) <= DEFAULT_CONFIG["min_agents_per_team"]:
            raise TeamError("Cannot remove agent - team would be too small", self.team_id)
        
        # Remove from collections
        del self.agents[agent_id]
        del self.agent_roles[agent_id]
        
        # Update shared context
        self.shared_context.delete(f"agent_{agent_id}_role", updated_by="team_manager")
        
        logger.info(f"Removed agent {agent_id} from team {self.team_id}")
    
    def initialize_team(self) -> None:
        """Initialize the team for collaboration.
        
        Raises:
            TeamError: If team cannot be initialized
        """
        if len(self.agents) < DEFAULT_CONFIG["min_agents_per_team"]:
            raise TeamError(f"Team must have at least {DEFAULT_CONFIG['min_agents_per_team']} agents", self.team_id)
        
        if len(self.agents) > self.config.max_agents:
            raise TeamError(f"Team cannot have more than {self.config.max_agents} agents", self.team_id)
        
        # Create Agno Team instance
        try:
            agent_list = list(self.agents.values())
            self.agno_team = Team(agent_list)
        except Exception as e:
            raise TeamError(f"Failed to create Agno team: {e}", self.team_id)
        
        # Update status and context
        self.status = TeamStatus.ACTIVE
        self.shared_context.set("team_status", self.status.value, updated_by="team_manager")
        self.shared_context.set("team_initialized_at", time.time(), updated_by="team_manager")
        
        logger.info(f"Initialized team {self.team_id} with {len(self.agents)} agents")
    
    def start_collaboration(
        self,
        task_description: str,
        expected_output: str,
        context: Optional[Dict[str, Any]] = None,
        constraints: Optional[Dict[str, Any]] = None
    ) -> str:
        """Start collaborative work on a specific task.
        
        Args:
            task_description: Detailed task description
            expected_output: Description of expected deliverable
            context: Initial shared context
            constraints: Task constraints and limits
            
        Returns:
            Collaboration session ID
            
        Raises:
            TeamError: If collaboration cannot be started
        """
        if self.status != TeamStatus.ACTIVE:
            raise TeamError("Team must be active to start collaboration", self.team_id)
        
        if self.current_task:
            raise TeamError("Team is already working on a task", self.team_id)
        
        # Set up collaboration
        collaboration_id = f"collab_{self.team_id}_{int(time.time())}"
        self.current_task = task_description
        self.collaboration_start_time = time.time()
        
        # Update shared context
        if context:
            for key, value in context.items():
                self.shared_context.set(key, value, updated_by="team_manager")
        
        self.shared_context.set("collaboration_id", collaboration_id, updated_by="team_manager")
        self.shared_context.set("task_description", task_description, updated_by="team_manager")
        self.shared_context.set("expected_output", expected_output, updated_by="team_manager")
        self.shared_context.set("constraints", constraints or {}, updated_by="team_manager")
        self.shared_context.set("collaboration_start_time", self.collaboration_start_time, updated_by="team_manager")
        
        # Broadcast task to all agents
        self.communication.broadcast_update(
            sender_agent_id="team_manager",
            update_type="task_assignment",
            content={
                "summary": f"New collaboration task: {task_description}",
                "details": f"Expected output: {expected_output}",
                "action_required": True
            },
            urgency="attention"
        )
        
        logger.info(f"Started collaboration {collaboration_id} for team {self.team_id}")
        return collaboration_id
    
    def execute_collaboration(self, workflow_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the collaborative task using the Agno team.
        
        Args:
            workflow_config: Optional workflow configuration
            
        Returns:
            Collaboration results
            
        Raises:
            TeamError: If execution fails
        """
        if not self.current_task:
            raise TeamError("No active task to execute", self.team_id)
        
        if not self.agno_team:
            raise TeamError("Team not initialized", self.team_id)
        
        try:
            # Use Agno Team to run the collaborative task
            workflow_config = workflow_config or {}
            workflow_config.setdefault("max_rounds", self.config.max_rounds)
            
            # Execute collaboration
            results = self.agno_team.run(
                task=self.current_task,
                **workflow_config
            )
            
            # Store results
            self.collaboration_results = {
                "task": self.current_task,
                "results": results,
                "execution_time": time.time() - (self.collaboration_start_time or time.time()),
                "agents_involved": list(self.agents.keys()),
                "success": True
            }
            
            # Update shared context
            self.shared_context.set("collaboration_results", self.collaboration_results, updated_by="team_manager")
            
            # Broadcast completion
            self.communication.broadcast_update(
                sender_agent_id="team_manager",
                update_type="completion",
                content={
                    "summary": "Task completed successfully",
                    "details": f"Collaboration finished in {self.collaboration_results['execution_time']:.2f} seconds"
                },
                urgency="info"
            )
            
            logger.info(f"Completed collaboration for team {self.team_id}")
            return self.collaboration_results
            
        except Exception as e:
            error_results = {
                "task": self.current_task,
                "error": str(e),
                "execution_time": time.time() - (self.collaboration_start_time or time.time()),
                "agents_involved": list(self.agents.keys()),
                "success": False
            }
            
            self.collaboration_results = error_results
            
            # Broadcast failure
            self.communication.broadcast_update(
                sender_agent_id="team_manager",
                update_type="issue",
                content={
                    "summary": "Task execution failed",
                    "details": str(e)
                },
                urgency="critical"
            )
            
            logger.error(f"Collaboration failed for team {self.team_id}: {e}")
            raise TeamError(f"Collaboration execution failed: {e}", self.team_id)
    
    def stop_collaboration(self, force_stop: bool = False) -> Dict[str, Any]:
        """Stop ongoing collaboration and retrieve results.
        
        Args:
            force_stop: Whether to stop immediately
            
        Returns:
            Final collaboration results
        """
        if not self.current_task:
            raise TeamError("No active collaboration to stop", self.team_id)
        
        # Finalize results
        final_results = self.collaboration_results or {
            "task": self.current_task,
            "results": None,
            "execution_time": time.time() - (self.collaboration_start_time or time.time()),
            "agents_involved": list(self.agents.keys()),
            "success": False,
            "stopped": True,
            "force_stopped": force_stop
        }
        
        # Clean up collaboration state
        self.current_task = None
        self.collaboration_start_time = None
        
        # Update shared context
        self.shared_context.set("collaboration_completed", True, updated_by="team_manager")
        self.shared_context.set("final_results", final_results, updated_by="team_manager")
        
        logger.info(f"Stopped collaboration for team {self.team_id}")
        return final_results
    
    def get_team_status(self) -> Dict[str, Any]:
        """Get current team status and metrics.
        
        Returns:
            Team status information
        """
        return {
            "team_id": self.team_id,
            "status": self.status.value,
            "team_type": self.config.team_type.value,
            "agent_count": len(self.agents),
            "agents": {
                agent_id: {
                    "role": self.agent_roles[agent_id].name,
                    "role_id": self.agent_roles[agent_id].role_id
                }
                for agent_id in self.agents.keys()
            },
            "current_task": self.current_task,
            "collaboration_active": self.current_task is not None,
            "created_at": self.created_at,
            "context_version": self.shared_context.get_version(),
            "communication_stats": self.communication.get_communication_stats()
        }
    
    def pause_collaboration(self) -> None:
        """Pause the current collaboration."""
        if self.status == TeamStatus.ACTIVE:
            self.status = TeamStatus.PAUSED
            self.shared_context.set("team_status", self.status.value, updated_by="team_manager")
            logger.info(f"Paused collaboration for team {self.team_id}")
    
    def resume_collaboration(self) -> None:
        """Resume a paused collaboration."""
        if self.status == TeamStatus.PAUSED:
            self.status = TeamStatus.ACTIVE
            self.shared_context.set("team_status", self.status.value, updated_by="team_manager")
            logger.info(f"Resumed collaboration for team {self.team_id}")
    
    def cleanup(self) -> None:
        """Clean up team resources."""
        self.status = TeamStatus.COMPLETED
        self.shared_context.set("team_status", self.status.value, updated_by="team_manager")
        logger.info(f"Cleaned up team {self.team_id}")