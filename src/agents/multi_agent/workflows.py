"""Workflow Engine for Multi-Agent Collaboration

Orchestrates workflows and manages task sequences for multi-agent teams.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time

from .constants import WorkflowType, WorkflowStatus, TaskStatus
from .exceptions import WorkflowError
from .logging_config import get_multi_agent_logger

logger = get_multi_agent_logger("workflows")


@dataclass
class WorkflowStep:
    """A single step in a workflow."""
    
    step_id: str
    step_name: str
    step_type: str  # "task", "decision", "synchronization", "review"
    required_role: str
    estimated_duration: int  # minutes
    dependencies: List[str]
    success_criteria: str
    failure_handling: str


@dataclass
class QualityGate:
    """Quality gate for workflow validation."""
    
    gate_id: str
    gate_type: str  # "approval", "quality_check", "milestone"
    criteria: str
    required_score: float


class WorkflowEngine:
    """Manages workflow execution for multi-agent teams."""
    
    def __init__(self, team_id: str):
        self.team_id = team_id
        self._workflows: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"Initialized workflow engine for team {team_id}")
    
    def create_workflow(
        self,
        workflow_name: str,
        workflow_type: WorkflowType,
        description: str,
        steps: List[WorkflowStep],
        quality_gates: Optional[List[QualityGate]] = None
    ) -> str:
        """Create a new workflow template.
        
        Args:
            workflow_name: Name of the workflow
            workflow_type: Type of workflow orchestration
            description: Workflow description
            steps: List of workflow steps
            quality_gates: Optional quality gates
            
        Returns:
            Workflow ID
        """
        workflow_id = f"workflow_{int(time.time())}"
        
        # Validate workflow
        self._validate_workflow(steps)
        
        workflow = {
            "workflow_id": workflow_id,
            "name": workflow_name,
            "type": workflow_type,
            "description": description,
            "steps": steps,
            "quality_gates": quality_gates or [],
            "created_at": time.time(),
            "estimated_duration": sum(step.estimated_duration for step in steps)
        }
        
        self._workflows[workflow_id] = workflow
        logger.info(f"Created workflow {workflow_id}: {workflow_name}")
        
        return workflow_id
    
    def _validate_workflow(self, steps: List[WorkflowStep]) -> None:
        """Validate workflow structure."""
        if not steps:
            raise WorkflowError("Workflow must have at least one step")
        
        step_ids = {step.step_id for step in steps}
        
        # Check for circular dependencies
        for step in steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    raise WorkflowError(f"Step {step.step_id} depends on non-existent step {dep}")
        
        # Simple cycle detection
        visited = set()
        rec_stack = set()
        
        def has_cycle(step_id: str) -> bool:
            visited.add(step_id)
            rec_stack.add(step_id)
            
            step = next((s for s in steps if s.step_id == step_id), None)
            if step:
                for dep in step.dependencies:
                    if dep not in visited:
                        if has_cycle(dep):
                            return True
                    elif dep in rec_stack:
                        return True
            
            rec_stack.remove(step_id)
            return False
        
        for step in steps:
            if step.step_id not in visited:
                if has_cycle(step.step_id):
                    raise WorkflowError("Circular dependency detected in workflow")
    
    def get_default_research_workflow(self) -> str:
        """Get default research workflow.
        
        Returns:
            Workflow ID for research collaboration
        """
        steps = [
            WorkflowStep(
                step_id="research_gather",
                step_name="Gather Information",
                step_type="task",
                required_role="researcher",
                estimated_duration=10,
                dependencies=[],
                success_criteria="Comprehensive information gathered from multiple sources",
                failure_handling="Retry with different search terms"
            ),
            WorkflowStep(
                step_id="research_analyze",
                step_name="Analyze Findings",
                step_type="task",
                required_role="analyst",
                estimated_duration=8,
                dependencies=["research_gather"],
                success_criteria="Data analyzed and patterns identified",
                failure_handling="Request additional information from researcher"
            ),
            WorkflowStep(
                step_id="research_synthesize",
                step_name="Synthesize Results",
                step_type="task",
                required_role="synthesizer",
                estimated_duration=7,
                dependencies=["research_analyze"],
                success_criteria="Coherent conclusions drawn from analysis",
                failure_handling="Collaborate with analyst for clarification"
            )
        ]
        
        quality_gates = [
            QualityGate(
                gate_id="research_quality",
                gate_type="quality_check",
                criteria="Information accuracy and completeness",
                required_score=0.8
            )
        ]
        
        return self.create_workflow(
            workflow_name="Research Collaboration",
            workflow_type=WorkflowType.SEQUENTIAL,
            description="Standard research collaboration workflow",
            steps=steps,
            quality_gates=quality_gates
        )
    
    def get_default_content_workflow(self) -> str:
        """Get default content creation workflow."""
        steps = [
            WorkflowStep(
                step_id="content_draft",
                step_name="Create Draft",
                step_type="task",
                required_role="writer",
                estimated_duration=15,
                dependencies=[],
                success_criteria="Initial content draft created",
                failure_handling="Gather more requirements"
            ),
            WorkflowStep(
                step_id="content_edit",
                step_name="Edit Content",
                step_type="task",
                required_role="editor",
                estimated_duration=10,
                dependencies=["content_draft"],
                success_criteria="Content refined and improved",
                failure_handling="Provide feedback to writer"
            ),
            WorkflowStep(
                step_id="content_review",
                step_name="Quality Review",
                step_type="review",
                required_role="reviewer",
                estimated_duration=5,
                dependencies=["content_edit"],
                success_criteria="Content meets quality standards",
                failure_handling="Return to editor with feedback"
            )
        ]
        
        return self.create_workflow(
            workflow_name="Content Creation",
            workflow_type=WorkflowType.SEQUENTIAL,
            description="Standard content creation workflow",
            steps=steps
        )
    
    def get_default_problem_solving_workflow(self) -> str:
        """Get default problem-solving workflow."""
        steps = [
            WorkflowStep(
                step_id="problem_analyze",
                step_name="Analyze Problem",
                step_type="task",
                required_role="problem_analyzer",
                estimated_duration=12,
                dependencies=[],
                success_criteria="Problem broken down into components",
                failure_handling="Gather more problem context"
            ),
            WorkflowStep(
                step_id="solution_strategize",
                step_name="Develop Solutions",
                step_type="task",
                required_role="solution_strategist",
                estimated_duration=15,
                dependencies=["problem_analyze"],
                success_criteria="Solution alternatives identified",
                failure_handling="Collaborate with analyzer for clarification"
            ),
            WorkflowStep(
                step_id="implementation_plan",
                step_name="Create Implementation Plan",
                step_type="task",
                required_role="implementation_specialist",
                estimated_duration=10,
                dependencies=["solution_strategize"],
                success_criteria="Actionable implementation plan created",
                failure_handling="Refine solutions with strategist"
            )
        ]
        
        return self.create_workflow(
            workflow_name="Problem Solving",
            workflow_type=WorkflowType.SEQUENTIAL,
            description="Standard problem-solving workflow",
            steps=steps
        )
    
    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow by ID."""
        if workflow_id not in self._workflows:
            raise WorkflowError(f"Workflow {workflow_id} not found")
        return self._workflows[workflow_id]
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all available workflows."""
        return list(self._workflows.values())