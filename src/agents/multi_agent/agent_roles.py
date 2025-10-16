"""Agent Role System

Defines agent roles, capabilities, and specializations for multi-agent collaboration.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .constants import AgentRole, DEFAULT_AGENT_INSTRUCTIONS, DEFAULT_ROLE_TOOLS
from .exceptions import AgentRoleError
from .logging_config import get_multi_agent_logger

logger = get_multi_agent_logger("agent_roles")


@dataclass
class RoleDefinition:
    """Definition of an agent role with capabilities and configuration."""
    
    role_id: str
    name: str
    description: str
    capabilities: List[str]
    tools: List[str]
    instructions: str
    expertise_areas: List[str]
    
    def __post_init__(self):
        """Validate role definition after initialization."""
        if not self.capabilities:
            raise AgentRoleError(f"Role {self.name} must have at least one capability")
        
        if not self.instructions:
            raise AgentRoleError(f"Role {self.name} must have instructions")


class AgentRoleManager:
    """Manages agent roles and their definitions."""
    
    def __init__(self):
        self._roles: Dict[str, RoleDefinition] = {}
        self._load_default_roles()
    
    def _load_default_roles(self):
        """Load default role definitions."""
        logger.info("Loading default agent roles")
        
        # Research Team Roles
        self.register_role(RoleDefinition(
            role_id="researcher",
            name="Researcher",
            description="Specialist in gathering and validating information from various sources",
            capabilities=["web_search", "source_validation", "fact_checking"],
            tools=DEFAULT_ROLE_TOOLS[AgentRole.RESEARCHER.value],
            instructions=DEFAULT_AGENT_INSTRUCTIONS[AgentRole.RESEARCHER.value],
            expertise_areas=["research_methodology", "source_analysis", "information_gathering"]
        ))
        
        self.register_role(RoleDefinition(
            role_id="analyst",
            name="Analyst",
            description="Specialist in analyzing data and identifying patterns",
            capabilities=["data_analysis", "pattern_recognition", "statistical_analysis"],
            tools=DEFAULT_ROLE_TOOLS[AgentRole.ANALYST.value],
            instructions=DEFAULT_AGENT_INSTRUCTIONS[AgentRole.ANALYST.value],
            expertise_areas=["data_analysis", "statistical_methods", "trend_identification"]
        ))
        
        self.register_role(RoleDefinition(
            role_id="synthesizer",
            name="Synthesizer",
            description="Specialist in combining information into coherent conclusions",
            capabilities=["information_synthesis", "report_generation", "conclusion_drawing"],
            tools=DEFAULT_ROLE_TOOLS[AgentRole.SYNTHESIZER.value],
            instructions=DEFAULT_AGENT_INSTRUCTIONS[AgentRole.SYNTHESIZER.value],
            expertise_areas=["synthesis", "report_writing", "conclusion_formation"]
        ))
        
        # Content Creation Team Roles
        self.register_role(RoleDefinition(
            role_id="writer",
            name="Writer",
            description="Specialist in creating engaging and well-structured content",
            capabilities=["content_creation", "storytelling", "audience_adaptation"],
            tools=DEFAULT_ROLE_TOOLS[AgentRole.WRITER.value],
            instructions=DEFAULT_AGENT_INSTRUCTIONS[AgentRole.WRITER.value],
            expertise_areas=["writing", "content_strategy", "audience_engagement"]
        ))
        
        self.register_role(RoleDefinition(
            role_id="editor",
            name="Editor",
            description="Specialist in refining and improving content quality",
            capabilities=["content_editing", "style_improvement", "quality_assurance"],
            tools=DEFAULT_ROLE_TOOLS[AgentRole.EDITOR.value],
            instructions=DEFAULT_AGENT_INSTRUCTIONS[AgentRole.EDITOR.value],
            expertise_areas=["editing", "style_guide", "quality_control"]
        ))
        
        self.register_role(RoleDefinition(
            role_id="reviewer",
            name="Reviewer",
            description="Specialist in quality review and feedback",
            capabilities=["quality_assessment", "feedback_generation", "standards_compliance"],
            tools=DEFAULT_ROLE_TOOLS[AgentRole.REVIEWER.value],
            instructions=DEFAULT_AGENT_INSTRUCTIONS[AgentRole.REVIEWER.value],
            expertise_areas=["quality_assurance", "review_processes", "standards_compliance"]
        ))
        
        # Problem-Solving Team Roles
        self.register_role(RoleDefinition(
            role_id="problem_analyzer",
            name="Problem Analyzer",
            description="Specialist in breaking down complex problems",
            capabilities=["problem_decomposition", "root_cause_analysis", "systems_thinking"],
            tools=DEFAULT_ROLE_TOOLS[AgentRole.PROBLEM_ANALYZER.value],
            instructions=DEFAULT_AGENT_INSTRUCTIONS[AgentRole.PROBLEM_ANALYZER.value],
            expertise_areas=["problem_analysis", "systems_analysis", "analytical_frameworks"]
        ))
        
        self.register_role(RoleDefinition(
            role_id="solution_strategist",
            name="Solution Strategist",
            description="Specialist in developing strategic approaches to solutions",
            capabilities=["strategy_development", "solution_design", "option_evaluation"],
            tools=DEFAULT_ROLE_TOOLS[AgentRole.SOLUTION_STRATEGIST.value],
            instructions=DEFAULT_AGENT_INSTRUCTIONS[AgentRole.SOLUTION_STRATEGIST.value],
            expertise_areas=["strategic_planning", "solution_architecture", "decision_analysis"]
        ))
        
        self.register_role(RoleDefinition(
            role_id="implementation_specialist",
            name="Implementation Specialist",
            description="Specialist in creating actionable implementation plans",
            capabilities=["implementation_planning", "resource_allocation", "execution_strategy"],
            tools=DEFAULT_ROLE_TOOLS[AgentRole.IMPLEMENTATION_SPECIALIST.value],
            instructions=DEFAULT_AGENT_INSTRUCTIONS[AgentRole.IMPLEMENTATION_SPECIALIST.value],
            expertise_areas=["project_management", "implementation_strategy", "resource_planning"]
        ))
        
        logger.info(f"Loaded {len(self._roles)} default agent roles")
    
    def register_role(self, role_definition: RoleDefinition):
        """Register a new role definition.
        
        Args:
            role_definition: The role definition to register
            
        Raises:
            AgentRoleError: If role is invalid or already exists
        """
        if role_definition.role_id in self._roles:
            raise AgentRoleError(f"Role {role_definition.role_id} already registered")
        
        self._roles[role_definition.role_id] = role_definition
        logger.info(f"Registered role: {role_definition.name}")
    
    def get_role(self, role_id: str) -> RoleDefinition:
        """Get a role definition by ID.
        
        Args:
            role_id: The role identifier
            
        Returns:
            The role definition
            
        Raises:
            AgentRoleError: If role not found
        """
        if role_id not in self._roles:
            raise AgentRoleError(f"Role {role_id} not found")
        
        return self._roles[role_id]
    
    def list_roles(self) -> List[RoleDefinition]:
        """List all available roles.
        
        Returns:
            List of all registered role definitions
        """
        return list(self._roles.values())
    
    def get_roles_for_team_type(self, team_type: str) -> List[RoleDefinition]:
        """Get recommended roles for a team type.
        
        Args:
            team_type: Type of team (research, content_creation, problem_solving)
            
        Returns:
            List of recommended role definitions
        """
        role_mappings = {
            "research": ["researcher", "analyst", "synthesizer"],
            "content_creation": ["writer", "editor", "reviewer"],
            "problem_solving": ["problem_analyzer", "solution_strategist", "implementation_specialist"]
        }
        
        if team_type not in role_mappings:
            logger.warning(f"Unknown team type: {team_type}")
            return []
        
        roles = []
        for role_id in role_mappings[team_type]:
            try:
                roles.append(self.get_role(role_id))
            except AgentRoleError:
                logger.warning(f"Role {role_id} not found for team type {team_type}")
        
        return roles
    
    def validate_team_roles(self, role_ids: List[str]) -> bool:
        """Validate that all role IDs exist and are unique.
        
        Args:
            role_ids: List of role identifiers
            
        Returns:
            True if all roles are valid and unique
            
        Raises:
            AgentRoleError: If validation fails
        """
        if len(role_ids) != len(set(role_ids)):
            raise AgentRoleError("Duplicate roles found in team")
        
        for role_id in role_ids:
            if role_id not in self._roles:
                raise AgentRoleError(f"Role {role_id} not found")
        
        return True


# Global role manager instance
role_manager = AgentRoleManager()