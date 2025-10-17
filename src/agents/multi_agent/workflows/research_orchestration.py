"""Research Collaboration Workflow Orchestration

Advanced workflow orchestration specifically designed for research team collaboration,
providing structured processes for comprehensive research projects.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import time
from datetime import datetime, timedelta

from ..constants import WorkflowType, WorkflowStatus, TaskStatus
from ..exceptions import WorkflowError
from ..logging_config import get_multi_agent_logger

logger = get_multi_agent_logger("research_workflow")


class ResearchPhase(Enum):
    """Research collaboration phases."""
    INITIALIZATION = "initialization"
    INFORMATION_GATHERING = "information_gathering"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"
    FINALIZATION = "finalization"


@dataclass
class ResearchTask:
    """A research task within the workflow."""
    
    task_id: str
    task_name: str
    phase: ResearchPhase
    assigned_role: str
    dependencies: List[str]
    estimated_duration_minutes: int
    priority: str  # "high", "medium", "low"
    deliverables: List[str]
    quality_criteria: Dict[str, Any]
    
    # Runtime properties
    status: TaskStatus = TaskStatus.ASSIGNED
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    assigned_agent: Optional[str] = None
    output: Optional[Dict[str, Any]] = None


@dataclass
class QualityGate:
    """Quality gate for research workflow validation."""
    
    gate_id: str
    gate_name: str
    phase: ResearchPhase
    validation_criteria: Dict[str, Any]
    required_score: float
    validator_roles: List[str]
    
    # Runtime properties
    status: str = "pending"  # "pending", "passed", "failed"
    validation_results: Optional[Dict[str, Any]] = None


class ResearchWorkflowOrchestrator:
    """Orchestrates research collaboration workflows with specialized phases."""
    
    def __init__(self, team_id: str, research_topic: str):
        """Initialize research workflow orchestrator.
        
        Args:
            team_id: ID of the research team
            research_topic: Topic being researched
        """
        self.team_id = team_id
        self.research_topic = research_topic
        self.workflow_id = f"research_workflow_{int(time.time())}"
        self.current_phase = ResearchPhase.INITIALIZATION
        self.workflow_status = WorkflowStatus.PENDING
        
        # Workflow components
        self.tasks: Dict[str, ResearchTask] = {}
        self.quality_gates: Dict[str, QualityGate] = {}
        self.phase_dependencies: Dict[ResearchPhase, List[ResearchPhase]] = {}
        
        # Runtime tracking
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.execution_log: List[Dict[str, Any]] = []
        self.collaboration_context: Dict[str, Any] = {}
        
        # Initialize workflow
        self._initialize_research_workflow()
        
        logger.info(f"Initialized research workflow orchestrator for topic: {research_topic}")
    
    def _initialize_research_workflow(self):
        """Initialize the research workflow with tasks and quality gates."""
        # Define phase dependencies
        self.phase_dependencies = {
            ResearchPhase.INITIALIZATION: [],
            ResearchPhase.INFORMATION_GATHERING: [ResearchPhase.INITIALIZATION],
            ResearchPhase.ANALYSIS: [ResearchPhase.INFORMATION_GATHERING],
            ResearchPhase.SYNTHESIS: [ResearchPhase.ANALYSIS],
            ResearchPhase.VALIDATION: [ResearchPhase.SYNTHESIS],
            ResearchPhase.FINALIZATION: [ResearchPhase.VALIDATION]
        }
        
        # Create research tasks
        self._create_research_tasks()
        
        # Create quality gates
        self._create_quality_gates()
        
        logger.info(f"Research workflow initialized with {len(self.tasks)} tasks and {len(self.quality_gates)} quality gates")
    
    def _create_research_tasks(self):
        """Create research tasks for the workflow."""
        
        # Initialization Phase
        self.tasks["init_research_scope"] = ResearchTask(
            task_id="init_research_scope",
            task_name="Define Research Scope and Objectives",
            phase=ResearchPhase.INITIALIZATION,
            assigned_role="lead_researcher",
            dependencies=[],
            estimated_duration_minutes=30,
            priority="high",
            deliverables=["research_scope_document", "research_objectives"],
            quality_criteria={"clarity": 0.8, "completeness": 0.9, "feasibility": 0.8}
        )
        
        self.tasks["init_methodology"] = ResearchTask(
            task_id="init_methodology",
            task_name="Establish Research Methodology",
            phase=ResearchPhase.INITIALIZATION,
            assigned_role="lead_researcher",
            dependencies=["init_research_scope"],
            estimated_duration_minutes=20,
            priority="high",
            deliverables=["methodology_plan", "quality_standards"],
            quality_criteria={"rigor": 0.9, "appropriateness": 0.8}
        )
        
        # Information Gathering Phase
        self.tasks["gather_primary_sources"] = ResearchTask(
            task_id="gather_primary_sources",
            task_name="Gather Primary Source Information",
            phase=ResearchPhase.INFORMATION_GATHERING,
            assigned_role="lead_researcher",
            dependencies=["init_methodology"],
            estimated_duration_minutes=60,
            priority="high",
            deliverables=["primary_sources", "source_credibility_assessment"],
            quality_criteria={"source_quality": 0.8, "relevance": 0.9, "diversity": 0.7}
        )
        
        self.tasks["gather_secondary_sources"] = ResearchTask(
            task_id="gather_secondary_sources",
            task_name="Gather Secondary Source Information",
            phase=ResearchPhase.INFORMATION_GATHERING,
            assigned_role="specialist_researcher",
            dependencies=["init_methodology"],
            estimated_duration_minutes=45,
            priority="medium",
            deliverables=["secondary_sources", "literature_review_foundation"],
            quality_criteria={"comprehensiveness": 0.8, "currency": 0.7, "authority": 0.8}
        )
        
        self.tasks["validate_sources"] = ResearchTask(
            task_id="validate_sources",
            task_name="Validate Source Credibility and Quality",
            phase=ResearchPhase.INFORMATION_GATHERING,
            assigned_role="quality_analyst",
            dependencies=["gather_primary_sources", "gather_secondary_sources"],
            estimated_duration_minutes=30,
            priority="high",
            deliverables=["source_validation_report", "credibility_scores"],
            quality_criteria={"validation_thoroughness": 0.9, "accuracy": 0.95}
        )
        
        # Analysis Phase
        self.tasks["analyze_information"] = ResearchTask(
            task_id="analyze_information",
            task_name="Analyze Gathered Information",
            phase=ResearchPhase.ANALYSIS,
            assigned_role="data_analyst",
            dependencies=["validate_sources"],
            estimated_duration_minutes=50,
            priority="high",
            deliverables=["analysis_results", "pattern_identification", "insights"],
            quality_criteria={"analytical_depth": 0.8, "objectivity": 0.9, "evidence_support": 0.8}
        )
        
        self.tasks["cross_validate_findings"] = ResearchTask(
            task_id="cross_validate_findings",
            task_name="Cross-Validate Research Findings",
            phase=ResearchPhase.ANALYSIS,
            assigned_role="quality_analyst",
            dependencies=["analyze_information"],
            estimated_duration_minutes=25,
            priority="high",
            deliverables=["validation_results", "consistency_check"],
            quality_criteria={"validation_coverage": 0.9, "consistency": 0.8}
        )
        
        # Synthesis Phase
        self.tasks["synthesize_findings"] = ResearchTask(
            task_id="synthesize_findings",
            task_name="Synthesize All Research Findings",
            phase=ResearchPhase.SYNTHESIS,
            assigned_role="research_synthesizer",
            dependencies=["cross_validate_findings"],
            estimated_duration_minutes=45,
            priority="high",
            deliverables=["synthesis_report", "integrated_conclusions"],
            quality_criteria={"integration_quality": 0.8, "coherence": 0.9, "completeness": 0.8}
        )
        
        self.tasks["create_recommendations"] = ResearchTask(
            task_id="create_recommendations",
            task_name="Create Research-Based Recommendations",
            phase=ResearchPhase.SYNTHESIS,
            assigned_role="research_synthesizer",
            dependencies=["synthesize_findings"],
            estimated_duration_minutes=20,
            priority="medium",
            deliverables=["recommendations", "implementation_guidance"],
            quality_criteria={"actionability": 0.8, "evidence_basis": 0.9}
        )
        
        # Validation Phase
        self.tasks["peer_review"] = ResearchTask(
            task_id="peer_review",
            task_name="Conduct Peer Review of Research Output",
            phase=ResearchPhase.VALIDATION,
            assigned_role="lead_researcher",
            dependencies=["create_recommendations"],
            estimated_duration_minutes=30,
            priority="high",
            deliverables=["peer_review_results", "quality_assessment"],
            quality_criteria={"review_thoroughness": 0.9, "constructive_feedback": 0.8}
        )
        
        self.tasks["quality_assurance"] = ResearchTask(
            task_id="quality_assurance",
            task_name="Final Quality Assurance Check",
            phase=ResearchPhase.VALIDATION,
            assigned_role="quality_analyst",
            dependencies=["peer_review"],
            estimated_duration_minutes=20,
            priority="high",
            deliverables=["qa_report", "compliance_verification"],
            quality_criteria={"quality_compliance": 0.95, "standards_adherence": 0.9}
        )
        
        # Finalization Phase
        self.tasks["finalize_output"] = ResearchTask(
            task_id="finalize_output",
            task_name="Finalize Research Output and Documentation",
            phase=ResearchPhase.FINALIZATION,
            assigned_role="research_synthesizer",
            dependencies=["quality_assurance"],
            estimated_duration_minutes=25,
            priority="high",
            deliverables=["final_research_report", "executive_summary", "methodology_documentation"],
            quality_criteria={"presentation_quality": 0.9, "completeness": 0.95, "accessibility": 0.8}
        )
    
    def _create_quality_gates(self):
        """Create quality gates for the research workflow."""
        
        self.quality_gates["initialization_gate"] = QualityGate(
            gate_id="initialization_gate",
            gate_name="Research Initialization Quality Gate",
            phase=ResearchPhase.INITIALIZATION,
            validation_criteria={
                "scope_clarity": 0.8,
                "objectives_measurability": 0.8,
                "methodology_appropriateness": 0.8,
                "resource_adequacy": 0.7
            },
            required_score=0.8,
            validator_roles=["lead_researcher", "quality_analyst"]
        )
        
        self.quality_gates["information_gate"] = QualityGate(
            gate_id="information_gate",
            gate_name="Information Gathering Quality Gate",
            phase=ResearchPhase.INFORMATION_GATHERING,
            validation_criteria={
                "source_quality": 0.8,
                "information_completeness": 0.8,
                "source_diversity": 0.7,
                "credibility_validation": 0.9
            },
            required_score=0.8,
            validator_roles=["quality_analyst", "specialist_researcher"]
        )
        
        self.quality_gates["analysis_gate"] = QualityGate(
            gate_id="analysis_gate",
            gate_name="Analysis Quality Gate",
            phase=ResearchPhase.ANALYSIS,
            validation_criteria={
                "analytical_rigor": 0.8,
                "findings_validity": 0.9,
                "evidence_support": 0.8,
                "bias_minimization": 0.8
            },
            required_score=0.8,
            validator_roles=["data_analyst", "quality_analyst"]
        )
        
        self.quality_gates["synthesis_gate"] = QualityGate(
            gate_id="synthesis_gate",
            gate_name="Synthesis Quality Gate",
            phase=ResearchPhase.SYNTHESIS,
            validation_criteria={
                "integration_coherence": 0.8,
                "synthesis_completeness": 0.8,
                "conclusion_validity": 0.9,
                "recommendation_actionability": 0.7
            },
            required_score=0.8,
            validator_roles=["research_synthesizer", "lead_researcher"]
        )
        
        self.quality_gates["final_gate"] = QualityGate(
            gate_id="final_gate",
            gate_name="Final Quality Gate",
            phase=ResearchPhase.VALIDATION,
            validation_criteria={
                "overall_quality": 0.85,
                "objective_achievement": 0.9,
                "methodology_compliance": 0.9,
                "deliverable_completeness": 0.95
            },
            required_score=0.85,
            validator_roles=["lead_researcher", "quality_analyst", "research_synthesizer"]
        )
    
    def start_workflow(self) -> Dict[str, Any]:
        """Start the research collaboration workflow."""
        if self.workflow_status != WorkflowStatus.PENDING:
            raise WorkflowError(f"Workflow already started with status: {self.workflow_status}")
        
        self.workflow_status = WorkflowStatus.EXECUTING
        self.start_time = datetime.now()
        self.current_phase = ResearchPhase.INITIALIZATION
        
        # Initialize collaboration context
        self.collaboration_context = {
            "research_topic": self.research_topic,
            "team_id": self.team_id,
            "workflow_start": self.start_time.isoformat(),
            "quality_standards": self._get_quality_standards(),
            "collaboration_guidelines": self._get_collaboration_guidelines()
        }
        
        self._log_event("workflow_started", {
            "workflow_id": self.workflow_id,
            "research_topic": self.research_topic,
            "total_tasks": len(self.tasks),
            "estimated_duration": self._calculate_estimated_duration()
        })
        
        logger.info(f"Started research workflow for topic: {self.research_topic}")
        
        return {
            "success": True,
            "workflow_id": self.workflow_id,
            "status": self.workflow_status.value,
            "current_phase": self.current_phase.value,
            "estimated_duration_minutes": self._calculate_estimated_duration()
        }
    
    def execute_next_phase(self) -> Dict[str, Any]:
        """Execute the next phase in the research workflow."""
        if self.workflow_status != WorkflowStatus.EXECUTING:
            raise WorkflowError(f"Cannot execute phase - workflow status: {self.workflow_status}")
        
        # Check if current phase is complete
        if not self._is_phase_complete(self.current_phase):
            return self._execute_current_phase()
        
        # Validate current phase quality gate
        quality_gate_result = self._validate_phase_quality_gate(self.current_phase)
        if not quality_gate_result["passed"]:
            return {
                "success": False,
                "error": "Quality gate validation failed",
                "quality_gate_results": quality_gate_result,
                "required_actions": quality_gate_result.get("required_actions", [])
            }
        
        # Move to next phase
        next_phase = self._get_next_phase(self.current_phase)
        if next_phase is None:
            return self._complete_workflow()
        
        self.current_phase = next_phase
        self._log_event("phase_transition", {
            "from_phase": self.current_phase.value,
            "to_phase": next_phase.value
        })
        
        return self._execute_current_phase()
    
    def _execute_current_phase(self) -> Dict[str, Any]:
        """Execute tasks in the current phase."""
        phase_tasks = [task for task in self.tasks.values() if task.phase == self.current_phase]
        ready_tasks = [task for task in phase_tasks if self._are_dependencies_met(task)]
        
        if not ready_tasks:
            return {
                "success": False,
                "error": "No ready tasks in current phase",
                "current_phase": self.current_phase.value,
                "waiting_for": self._get_waiting_dependencies(phase_tasks)
            }
        
        # Execute ready tasks
        execution_results = []
        for task in ready_tasks:
            if task.status == TaskStatus.ASSIGNED:
                result = self._execute_task(task)
                execution_results.append(result)
        
        return {
            "success": True,
            "current_phase": self.current_phase.value,
            "executed_tasks": len(execution_results),
            "task_results": execution_results,
            "phase_progress": self._get_phase_progress(self.current_phase)
        }
    
    def _execute_task(self, task: ResearchTask) -> Dict[str, Any]:
        """Execute a single research task."""
        task.status = TaskStatus.IN_PROGRESS
        task.start_time = datetime.now()
        
        self._log_event("task_started", {
            "task_id": task.task_id,
            "task_name": task.task_name,
            "phase": task.phase.value,
            "assigned_role": task.assigned_role
        })
        
        # Simulate task execution (in real implementation, this would delegate to agents)
        execution_result = self._simulate_task_execution(task)
        
        # Update task status
        task.status = TaskStatus.COMPLETED if execution_result["success"] else TaskStatus.FAILED
        task.end_time = datetime.now()
        task.output = execution_result
        
        self._log_event("task_completed", {
            "task_id": task.task_id,
            "status": task.status.value,
            "duration_minutes": (task.end_time - task.start_time).total_seconds() / 60,
            "quality_score": execution_result.get("quality_score", 0)
        })
        
        return {
            "task_id": task.task_id,
            "task_name": task.task_name,
            "status": task.status.value,
            "execution_result": execution_result,
            "duration_minutes": (task.end_time - task.start_time).total_seconds() / 60
        }
    
    def _simulate_task_execution(self, task: ResearchTask) -> Dict[str, Any]:
        """Simulate task execution (placeholder for actual agent execution)."""
        # In real implementation, this would delegate to appropriate agents
        return {
            "success": True,
            "deliverables": task.deliverables,
            "quality_score": 0.85,  # Simulated quality score
            "output_data": f"Simulated output for {task.task_name}",
            "execution_method": "agent_collaboration",
            "validation_status": "passed"
        }
    
    def _is_phase_complete(self, phase: ResearchPhase) -> bool:
        """Check if all tasks in a phase are complete."""
        phase_tasks = [task for task in self.tasks.values() if task.phase == phase]
        return all(task.status == TaskStatus.COMPLETED for task in phase_tasks)
    
    def _validate_phase_quality_gate(self, phase: ResearchPhase) -> Dict[str, Any]:
        """Validate quality gate for a phase."""
        # Find quality gate for this phase
        quality_gate = None
        for gate in self.quality_gates.values():
            if gate.phase == phase:
                quality_gate = gate
                break
        
        if not quality_gate:
            return {"passed": True, "reason": "No quality gate defined for phase"}
        
        # Simulate quality gate validation
        validation_results = {}
        total_score = 0
        
        for criterion, required_score in quality_gate.validation_criteria.items():
            # Simulate criterion evaluation
            actual_score = 0.85  # Would be calculated from actual task outputs
            validation_results[criterion] = {
                "required": required_score,
                "actual": actual_score,
                "passed": actual_score >= required_score
            }
            total_score += actual_score
        
        average_score = total_score / len(quality_gate.validation_criteria)
        overall_passed = average_score >= quality_gate.required_score
        
        quality_gate.validation_results = validation_results
        quality_gate.status = "passed" if overall_passed else "failed"
        
        return {
            "passed": overall_passed,
            "quality_gate_id": quality_gate.gate_id,
            "average_score": average_score,
            "required_score": quality_gate.required_score,
            "criterion_results": validation_results,
            "required_actions": [] if overall_passed else ["Improve quality in failed criteria"]
        }
    
    def _get_next_phase(self, current_phase: ResearchPhase) -> Optional[ResearchPhase]:
        """Get the next phase in the workflow."""
        phase_order = [
            ResearchPhase.INITIALIZATION,
            ResearchPhase.INFORMATION_GATHERING,
            ResearchPhase.ANALYSIS,
            ResearchPhase.SYNTHESIS,
            ResearchPhase.VALIDATION,
            ResearchPhase.FINALIZATION
        ]
        
        try:
            current_index = phase_order.index(current_phase)
            if current_index < len(phase_order) - 1:
                return phase_order[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def _complete_workflow(self) -> Dict[str, Any]:
        """Complete the research workflow."""
        self.workflow_status = WorkflowStatus.COMPLETED
        self.end_time = datetime.now()
        
        workflow_results = self._generate_workflow_results()
        
        self._log_event("workflow_completed", {
            "workflow_id": self.workflow_id,
            "total_duration_minutes": (self.end_time - self.start_time).total_seconds() / 60,
            "total_tasks_completed": len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
            "overall_quality_score": workflow_results.get("overall_quality_score", 0)
        })
        
        logger.info(f"Completed research workflow for topic: {self.research_topic}")
        
        return {
            "success": True,
            "workflow_completed": True,
            "workflow_results": workflow_results
        }
    
    def _generate_workflow_results(self) -> Dict[str, Any]:
        """Generate comprehensive workflow results."""
        completed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]
        failed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.FAILED]
        
        # Calculate quality metrics
        quality_scores = [t.output.get("quality_score", 0) for t in completed_tasks if t.output]
        average_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return {
            "workflow_id": self.workflow_id,
            "research_topic": self.research_topic,
            "execution_summary": {
                "total_tasks": len(self.tasks),
                "completed_tasks": len(completed_tasks),
                "failed_tasks": len(failed_tasks),
                "success_rate": len(completed_tasks) / len(self.tasks) if self.tasks else 0
            },
            "quality_metrics": {
                "overall_quality_score": average_quality,
                "quality_gates_passed": len([g for g in self.quality_gates.values() if g.status == "passed"]),
                "quality_gates_total": len(self.quality_gates)
            },
            "timing_metrics": {
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "total_duration_minutes": (self.end_time - self.start_time).total_seconds() / 60 if self.end_time and self.start_time else 0
            },
            "deliverables": self._collect_deliverables(completed_tasks),
            "recommendations": self._generate_workflow_recommendations()
        }
    
    def _collect_deliverables(self, completed_tasks: List[ResearchTask]) -> List[str]:
        """Collect all deliverables from completed tasks."""
        deliverables = []
        for task in completed_tasks:
            deliverables.extend(task.deliverables)
        return list(set(deliverables))  # Remove duplicates
    
    def _generate_workflow_recommendations(self) -> List[str]:
        """Generate recommendations based on workflow execution."""
        recommendations = [
            "Review and validate all research findings",
            "Consider peer review for research quality assurance",
            "Archive research process documentation for future reference"
        ]
        
        # Add specific recommendations based on execution
        failed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.FAILED]
        if failed_tasks:
            recommendations.append("Address failed tasks before finalizing research")
        
        return recommendations
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status and progress."""
        return {
            "workflow_id": self.workflow_id,
            "research_topic": self.research_topic,
            "status": self.workflow_status.value,
            "current_phase": self.current_phase.value if self.current_phase else None,
            "progress": self._calculate_progress(),
            "phase_progress": {phase.value: self._get_phase_progress(phase) for phase in ResearchPhase},
            "quality_gates_status": {gate.gate_id: gate.status for gate in self.quality_gates.values()},
            "next_tasks": self._get_next_ready_tasks()
        }
    
    def _calculate_progress(self) -> float:
        """Calculate overall workflow progress."""
        if not self.tasks:
            return 0.0
        
        completed_tasks = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        return completed_tasks / len(self.tasks)
    
    def _get_phase_progress(self, phase: ResearchPhase) -> Dict[str, Any]:
        """Get progress for a specific phase."""
        phase_tasks = [task for task in self.tasks.values() if task.phase == phase]
        if not phase_tasks:
            return {"progress": 0.0, "completed": 0, "total": 0}
        
        completed = len([t for t in phase_tasks if t.status == TaskStatus.COMPLETED])
        return {
            "progress": completed / len(phase_tasks),
            "completed": completed,
            "total": len(phase_tasks),
            "status": "completed" if completed == len(phase_tasks) else "in_progress" if completed > 0 else "pending"
        }
    
    def _get_next_ready_tasks(self) -> List[str]:
        """Get list of tasks that are ready to execute."""
        ready_tasks = []
        for task in self.tasks.values():
            if task.status == TaskStatus.ASSIGNED and self._are_dependencies_met(task):
                ready_tasks.append(task.task_id)
        return ready_tasks
    
    def _are_dependencies_met(self, task: ResearchTask) -> bool:
        """Check if all dependencies for a task are met."""
        for dep_id in task.dependencies:
            if dep_id in self.tasks:
                if self.tasks[dep_id].status != TaskStatus.COMPLETED:
                    return False
            else:
                logger.warning(f"Dependency {dep_id} not found for task {task.task_id}")
                return False
        return True
    
    def _get_waiting_dependencies(self, tasks: List[ResearchTask]) -> List[str]:
        """Get list of dependencies that tasks are waiting for."""
        waiting_deps = []
        for task in tasks:
            if task.status == TaskStatus.ASSIGNED:
                for dep_id in task.dependencies:
                    if dep_id in self.tasks and self.tasks[dep_id].status != TaskStatus.COMPLETED:
                        waiting_deps.append(dep_id)
        return list(set(waiting_deps))
    
    def _calculate_estimated_duration(self) -> int:
        """Calculate estimated duration for the entire workflow."""
        return sum(task.estimated_duration_minutes for task in self.tasks.values())
    
    def _get_quality_standards(self) -> Dict[str, Any]:
        """Get quality standards for the research workflow."""
        return {
            "minimum_quality_score": 0.8,
            "source_credibility_threshold": 0.8,
            "validation_coverage": 0.9,
            "peer_review_required": True,
            "documentation_completeness": 0.95
        }
    
    def _get_collaboration_guidelines(self) -> Dict[str, Any]:
        """Get collaboration guidelines for the research team."""
        return {
            "communication_frequency": "high",
            "peer_review_process": "mandatory",
            "quality_feedback_loops": True,
            "knowledge_sharing": "continuous",
            "conflict_resolution": "evidence_based"
        }
    
    def _log_event(self, event_type: str, event_data: Dict[str, Any]):
        """Log workflow events."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": event_data
        }
        self.execution_log.append(event)


# Factory function
def create_research_workflow_orchestrator(team_id: str, research_topic: str) -> ResearchWorkflowOrchestrator:
    """Create a research workflow orchestrator.
    
    Args:
        team_id: ID of the research team
        research_topic: Topic being researched
        
    Returns:
        Configured ResearchWorkflowOrchestrator instance
    """
    return ResearchWorkflowOrchestrator(team_id, research_topic)


# Demo function
def demo_research_workflow():
    """Demonstrate research workflow orchestration."""
    print("Research Workflow Orchestration Demo")
    print("=" * 40)
    
    # Create workflow orchestrator
    topic = "Impact of AI on Healthcare"
    orchestrator = create_research_workflow_orchestrator("demo_team", topic)
    
    print(f"Created research workflow for: {topic}")
    print(f"Workflow ID: {orchestrator.workflow_id}")
    print(f"Total tasks: {len(orchestrator.tasks)}")
    print(f"Total quality gates: {len(orchestrator.quality_gates)}")
    
    # Start workflow
    start_result = orchestrator.start_workflow()
    print(f"\\nWorkflow started: {start_result['success']}")
    print(f"Estimated duration: {start_result['estimated_duration_minutes']} minutes")
    
    # Show workflow status
    status = orchestrator.get_workflow_status()
    print(f"\\nWorkflow Status:")
    print(f"  Current phase: {status['current_phase']}")
    print(f"  Progress: {status['progress']:.1%}")
    print(f"  Next ready tasks: {len(status['next_tasks'])}")
    
    print("\\nResearch workflow orchestration demo completed!")


if __name__ == "__main__":
    demo_research_workflow()