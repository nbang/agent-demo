"""
Implementation Specialist Agent Role - Creates detailed implementation plans from solution strategies.

This module provides a specialized agent role for developing comprehensive implementation
plans that translate solution strategies into actionable execution plans with phases,
tasks, resources, timelines, and success criteria.

Key Capabilities:
- Detailed implementation planning
- Task breakdown and sequencing
- Resource allocation and management
- Timeline and milestone planning
- Risk mitigation planning
- Quality assurance integration

Usage:
    specialist = create_implementation_specialist()
    plan = specialist.create_implementation_plan(
        strategy=solution_strategy,
        constraints=["budget", "timeline"],
        resources={"developers": 5, "qa": 2}
    )
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(Enum):
    """Task status values."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class ResourceType(Enum):
    """Types of resources."""
    HUMAN = "human"
    TECHNICAL = "technical"
    FINANCIAL = "financial"
    INFRASTRUCTURE = "infrastructure"
    EXTERNAL = "external"


class MilestoneType(Enum):
    """Types of milestones."""
    PHASE_START = "phase_start"
    PHASE_END = "phase_end"
    DELIVERY = "delivery"
    REVIEW = "review"
    APPROVAL = "approval"
    GO_LIVE = "go_live"


@dataclass
class Resource:
    """A resource required for implementation."""
    resource_id: str
    name: str
    resource_type: ResourceType
    quantity: int
    unit: str  # hours, people, dollars, etc.
    availability: str  # Available, Partial, Not Available
    cost_per_unit: Optional[float] = None
    notes: str = ""


@dataclass
class Task:
    """A task in the implementation plan."""
    task_id: str
    title: str
    description: str
    phase_id: str
    
    # Scheduling
    duration_days: int
    start_offset_days: int  # Days from phase start
    priority: TaskPriority
    status: TaskStatus = TaskStatus.NOT_STARTED
    
    # Dependencies
    dependencies: List[str] = field(default_factory=list)  # Task IDs
    blocking_tasks: List[str] = field(default_factory=list)  # Tasks blocked by this
    
    # Resources
    resources_required: List[Resource] = field(default_factory=list)
    estimated_effort_hours: int = 0
    
    # Deliverables and criteria
    deliverables: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)
    quality_checks: List[str] = field(default_factory=list)
    
    # Risk and notes
    risks: List[str] = field(default_factory=list)
    mitigation_actions: List[str] = field(default_factory=list)
    notes: str = ""
    
    def is_ready_to_start(self, completed_tasks: List[str]) -> bool:
        """Check if all dependencies are completed."""
        return all(dep_id in completed_tasks for dep_id in self.dependencies)
    
    def get_completion_percentage(self) -> int:
        """Get estimated completion percentage."""
        status_percentages = {
            TaskStatus.NOT_STARTED: 0,
            TaskStatus.IN_PROGRESS: 50,
            TaskStatus.COMPLETED: 100,
            TaskStatus.BLOCKED: 0,
            TaskStatus.CANCELLED: 0
        }
        return status_percentages.get(self.status, 0)


@dataclass
class Milestone:
    """A milestone in the implementation plan."""
    milestone_id: str
    title: str
    description: str
    milestone_type: MilestoneType
    phase_id: str
    target_date_offset: int  # Days from plan start
    
    # Criteria
    completion_criteria: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    
    # Status
    achieved: bool = False
    achieved_date: Optional[datetime] = None
    notes: str = ""


@dataclass
class Phase:
    """An implementation phase."""
    phase_id: str
    phase_number: int
    title: str
    description: str
    
    # Timing
    duration_days: int
    start_offset_days: int  # Days from plan start
    
    # Tasks and milestones
    tasks: List[Task] = field(default_factory=list)
    milestones: List[Milestone] = field(default_factory=list)
    
    # Objectives and outcomes
    objectives: List[str] = field(default_factory=list)
    expected_outcomes: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    
    # Dependencies
    depends_on_phases: List[str] = field(default_factory=list)  # Phase IDs
    
    def get_critical_tasks(self) -> List[Task]:
        """Get tasks with critical priority."""
        return [t for t in self.tasks if t.priority == TaskPriority.CRITICAL]
    
    def get_completion_percentage(self) -> float:
        """Calculate phase completion percentage."""
        if not self.tasks:
            return 0.0
        total = sum(task.get_completion_percentage() for task in self.tasks)
        return total / len(self.tasks)


@dataclass
class RiskMitigationPlan:
    """Risk mitigation plan."""
    risk_id: str
    risk_description: str
    probability: str  # High, Medium, Low
    impact: str  # Critical, High, Medium, Low
    
    mitigation_strategy: str
    mitigation_actions: List[str]
    contingency_plan: str
    
    owner: str
    status: str  # Active, Mitigated, Realized, Closed


@dataclass
class QualityGate:
    """Quality gate for the implementation."""
    gate_id: str
    title: str
    phase_id: str
    
    criteria: List[str]
    checks: List[str]
    
    required_approvers: List[str]
    passed: bool = False
    notes: str = ""


@dataclass
class ImplementationPlan:
    """Comprehensive implementation plan."""
    plan_id: str
    strategy_id: str
    problem_id: str
    
    # Plan overview
    title: str
    description: str
    objectives: List[str]
    
    # Structure
    phases: List[Phase]
    
    # Resources
    total_resources: List[Resource]
    resource_allocation: Dict[str, List[Resource]]  # phase_id -> resources
    
    # Timeline
    total_duration_days: int
    estimated_start_date: Optional[datetime] = None
    estimated_end_date: Optional[datetime] = None
    
    # Risk management
    risk_mitigation_plans: List[RiskMitigationPlan] = field(default_factory=list)
    
    # Quality assurance
    quality_gates: List[QualityGate] = field(default_factory=list)
    
    # Estimates
    total_effort_hours: int = 0
    total_cost: str = ""
    
    # Tracking
    overall_status: str = "Not Started"
    completion_percentage: float = 0.0
    
    # Metadata
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def get_critical_path(self) -> List[Task]:
        """Identify tasks on the critical path."""
        critical_tasks = []
        for phase in self.phases:
            critical_tasks.extend(phase.get_critical_tasks())
        return critical_tasks
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all phases."""
        all_tasks = []
        for phase in self.phases:
            all_tasks.extend(phase.tasks)
        return all_tasks
    
    def get_all_milestones(self) -> List[Milestone]:
        """Get all milestones across all phases."""
        all_milestones = []
        for phase in self.phases:
            all_milestones.extend(phase.milestones)
        return all_milestones
    
    def calculate_completion(self) -> float:
        """Calculate overall completion percentage."""
        if not self.phases:
            return 0.0
        total = sum(phase.get_completion_percentage() for phase in self.phases)
        return total / len(self.phases)
    
    def get_next_milestones(self, days: int = 30) -> List[Milestone]:
        """Get milestones due within specified days."""
        if not self.estimated_start_date:
            return []
        
        cutoff_date = datetime.now() + timedelta(days=days)
        upcoming = []
        
        for milestone in self.get_all_milestones():
            if not milestone.achieved:
                milestone_date = self.estimated_start_date + timedelta(days=milestone.target_date_offset)
                if milestone_date <= cutoff_date:
                    upcoming.append(milestone)
        
        return sorted(upcoming, key=lambda m: m.target_date_offset)


@dataclass
class SpecialistCapability:
    """Capabilities of the implementation specialist."""
    planning_methodologies: List[str]
    resource_management: bool
    risk_management: bool
    quality_assurance: bool
    agile_planning: bool
    waterfall_planning: bool


class ImplementationSpecialistRole:
    """
    Implementation Specialist agent role for creating detailed implementation plans.
    
    This agent takes solution strategies and creates comprehensive, actionable
    implementation plans with phases, tasks, resources, timelines, milestones,
    and quality gates.
    
    Core Capabilities:
    - Multi-phase implementation planning
    - Task breakdown and dependency mapping
    - Resource allocation and management
    - Timeline and milestone planning
    - Risk identification and mitigation
    - Quality gate definition
    """
    
    def __init__(
        self,
        specialist_name: str = "Implementation Specialist",
        methodologies: Optional[List[str]] = None,
        enable_agile: bool = True,
        enable_quality_gates: bool = True
    ):
        """
        Initialize the implementation specialist role.
        
        Args:
            specialist_name: Name of the specialist
            methodologies: Planning methodologies (Agile, Waterfall, Hybrid)
            enable_agile: Enable agile planning features
            enable_quality_gates: Enable quality gate creation
        """
        self.specialist_name = specialist_name
        self.methodologies = methodologies or ["Agile", "Waterfall", "Hybrid"]
        self.enable_agile = enable_agile
        self.enable_quality_gates = enable_quality_gates
        
        self.capability = SpecialistCapability(
            planning_methodologies=self.methodologies,
            resource_management=True,
            risk_management=True,
            quality_assurance=enable_quality_gates,
            agile_planning=enable_agile,
            waterfall_planning=True
        )
        
        logger.info(f"Initialized {specialist_name} with {len(self.methodologies)} methodologies")
    
    def create_implementation_plan(
        self,
        problem_id: str,
        strategy_id: str,
        strategy_title: str,
        strategy_steps: List[Any],
        strategy_approach: str,
        estimated_timeline: str,
        available_resources: Optional[Dict[str, int]] = None,
        constraints: Optional[List[str]] = None,
        methodology: str = "Hybrid"
    ) -> ImplementationPlan:
        """
        Create a comprehensive implementation plan from a strategy.
        
        Args:
            problem_id: Problem identifier
            strategy_id: Strategy identifier
            strategy_title: Strategy title
            strategy_steps: Steps from the strategy
            strategy_approach: Strategy approach (incremental, transformational, etc.)
            estimated_timeline: Timeline estimate from strategy
            available_resources: Available resources (e.g., {"developers": 5, "qa": 2})
            constraints: Implementation constraints
            methodology: Planning methodology (Agile, Waterfall, Hybrid)
            
        Returns:
            ImplementationPlan with complete execution plan
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"🏗️  {self.specialist_name}: Creating Implementation Plan")
        logger.info(f"{'='*60}")
        logger.info(f"Strategy: {strategy_title}")
        logger.info(f"Approach: {strategy_approach}")
        
        available_resources = available_resources or {}
        constraints = constraints or []
        
        logger.info(f"Methodology: {methodology}")
        logger.info(f"Resources: {len(available_resources)} types")
        logger.info(f"Constraints: {len(constraints)}")
        
        # Create phases from strategy steps
        logger.info("\n📋 Step 1: Creating Implementation Phases")
        phases = self._create_phases(strategy_steps, methodology)
        logger.info(f"   Phases: {len(phases)}")
        
        # Break down phases into detailed tasks
        logger.info("\n📝 Step 2: Breaking Down Tasks")
        self._create_tasks_for_phases(phases, methodology)
        total_tasks = sum(len(p.tasks) for p in phases)
        logger.info(f"   Tasks: {total_tasks}")
        
        # Create milestones
        logger.info("\n🎯 Step 3: Defining Milestones")
        self._create_milestones(phases)
        total_milestones = sum(len(p.milestones) for p in phases)
        logger.info(f"   Milestones: {total_milestones}")
        
        # Allocate resources
        logger.info("\n👥 Step 4: Allocating Resources")
        total_resources, resource_allocation = self._allocate_resources(
            phases, available_resources
        )
        logger.info(f"   Resource Types: {len(total_resources)}")
        
        # Identify and plan for risks
        logger.info("\n⚠️  Step 5: Risk Mitigation Planning")
        risk_plans = self._create_risk_mitigation_plans(phases, constraints)
        logger.info(f"   Risk Plans: {len(risk_plans)}")
        
        # Create quality gates
        quality_gates = []
        if self.enable_quality_gates:
            logger.info("\n✅ Step 6: Creating Quality Gates")
            quality_gates = self._create_quality_gates(phases)
            logger.info(f"   Quality Gates: {len(quality_gates)}")
        
        # Calculate totals
        logger.info("\n📊 Step 7: Calculating Totals")
        total_duration = sum(p.duration_days for p in phases)
        total_effort = sum(
            task.estimated_effort_hours
            for phase in phases
            for task in phase.tasks
        )
        total_cost = self._estimate_total_cost(total_resources, total_effort)
        
        logger.info(f"   Duration: {total_duration} days")
        logger.info(f"   Effort: {total_effort} hours")
        logger.info(f"   Cost: {total_cost}")
        
        plan_id = f"PLAN-{strategy_id}"
        
        plan = ImplementationPlan(
            plan_id=plan_id,
            strategy_id=strategy_id,
            problem_id=problem_id,
            title=f"Implementation Plan: {strategy_title}",
            description=f"Comprehensive implementation plan for {strategy_title} using {methodology} methodology",
            objectives=self._extract_objectives(strategy_steps),
            phases=phases,
            total_resources=total_resources,
            resource_allocation=resource_allocation,
            total_duration_days=total_duration,
            estimated_start_date=datetime.now(),
            estimated_end_date=datetime.now() + timedelta(days=total_duration),
            risk_mitigation_plans=risk_plans,
            quality_gates=quality_gates,
            total_effort_hours=total_effort,
            total_cost=total_cost,
            created_by=self.specialist_name
        )
        
        logger.info(f"\n✅ Implementation Plan Created: {plan_id}")
        logger.info(f"   Phases: {len(plan.phases)}")
        logger.info(f"   Tasks: {len(plan.get_all_tasks())}")
        logger.info(f"   Milestones: {len(plan.get_all_milestones())}")
        logger.info(f"   Critical Path: {len(plan.get_critical_path())} tasks")
        
        return plan
    
    def _create_phases(
        self,
        strategy_steps: List[Any],
        methodology: str
    ) -> List[Phase]:
        """Create implementation phases from strategy steps."""
        phases = []
        current_offset = 0
        
        for i, step in enumerate(strategy_steps, 1):
            # Extract duration from step
            duration_str = getattr(step, 'duration', '1 week')
            duration_days = self._parse_duration(duration_str)
            
            phase = Phase(
                phase_id=f"PHASE-{i:02d}",
                phase_number=i,
                title=getattr(step, 'title', f"Phase {i}"),
                description=getattr(step, 'description', ''),
                duration_days=duration_days,
                start_offset_days=current_offset,
                objectives=[],
                expected_outcomes=getattr(step, 'deliverables', []),
                success_criteria=getattr(step, 'success_criteria', [])
            )
            
            # Set dependencies
            if i > 1:
                phase.depends_on_phases = [f"PHASE-{i-1:02d}"]
            
            phases.append(phase)
            current_offset += duration_days
        
        return phases
    
    def _create_tasks_for_phases(
        self,
        phases: List[Phase],
        methodology: str
    ) -> None:
        """Create detailed tasks for each phase."""
        for phase in phases:
            # Create tasks based on phase objectives
            if methodology == "Agile":
                tasks = self._create_agile_tasks(phase)
            else:
                tasks = self._create_waterfall_tasks(phase)
            
            phase.tasks = tasks
    
    def _create_agile_tasks(self, phase: Phase) -> List[Task]:
        """Create tasks for Agile methodology."""
        tasks = []
        task_templates = [
            {
                "title": "Sprint Planning",
                "description": f"Plan sprint activities for {phase.title}",
                "duration": 1,
                "priority": TaskPriority.HIGH,
                "effort": 8
            },
            {
                "title": "Development Sprint",
                "description": f"Execute development work for {phase.title}",
                "duration": max(5, phase.duration_days - 4),
                "priority": TaskPriority.CRITICAL,
                "effort": max(40, (phase.duration_days - 4) * 8)
            },
            {
                "title": "Daily Standups",
                "description": "Daily synchronization meetings",
                "duration": phase.duration_days,
                "priority": TaskPriority.MEDIUM,
                "effort": phase.duration_days
            },
            {
                "title": "Sprint Review",
                "description": "Review sprint outcomes and deliverables",
                "duration": 1,
                "priority": TaskPriority.HIGH,
                "effort": 4
            },
            {
                "title": "Sprint Retrospective",
                "description": "Retrospective and continuous improvement",
                "duration": 1,
                "priority": TaskPriority.MEDIUM,
                "effort": 4
            }
        ]
        
        offset = 0
        for i, template in enumerate(task_templates, 1):
            task = Task(
                task_id=f"{phase.phase_id}-TASK-{i:02d}",
                title=template["title"],
                description=template["description"],
                phase_id=phase.phase_id,
                duration_days=template["duration"],
                start_offset_days=offset,
                priority=template["priority"],
                estimated_effort_hours=template["effort"],
                deliverables=[f"{template['title']} outcomes"],
                acceptance_criteria=[f"{template['title']} completed successfully"],
                quality_checks=["Code review", "Testing", "Documentation"]
            )
            
            # Set dependencies
            if i > 1:
                task.dependencies = [f"{phase.phase_id}-TASK-{i-1:02d}"]
            
            tasks.append(task)
            offset += template["duration"]
        
        return tasks
    
    def _create_waterfall_tasks(self, phase: Phase) -> List[Task]:
        """Create tasks for Waterfall methodology."""
        tasks = []
        
        # Generic task breakdown
        phase_duration = phase.duration_days
        tasks_count = min(5, max(3, phase_duration // 3))
        duration_per_task = phase_duration // tasks_count
        
        task_types = [
            ("Planning", TaskPriority.HIGH),
            ("Execution", TaskPriority.CRITICAL),
            ("Review", TaskPriority.HIGH),
            ("Testing", TaskPriority.CRITICAL),
            ("Finalization", TaskPriority.MEDIUM)
        ]
        
        offset = 0
        for i in range(tasks_count):
            task_type, priority = task_types[i] if i < len(task_types) else ("Activity", TaskPriority.MEDIUM)
            
            task = Task(
                task_id=f"{phase.phase_id}-TASK-{i+1:02d}",
                title=f"{phase.title} - {task_type}",
                description=f"{task_type} activities for {phase.title}",
                phase_id=phase.phase_id,
                duration_days=duration_per_task,
                start_offset_days=offset,
                priority=priority,
                estimated_effort_hours=duration_per_task * 8,
                deliverables=[f"{task_type} deliverables"],
                acceptance_criteria=[f"{task_type} criteria met"],
                quality_checks=["Review", "Approval"]
            )
            
            # Set dependencies
            if i > 0:
                task.dependencies = [f"{phase.phase_id}-TASK-{i:02d}"]
            
            tasks.append(task)
            offset += duration_per_task
        
        return tasks
    
    def _create_milestones(self, phases: List[Phase]) -> None:
        """Create milestones for phases."""
        for phase in phases:
            # Phase start milestone
            start_milestone = Milestone(
                milestone_id=f"{phase.phase_id}-MS-START",
                title=f"{phase.title} - Start",
                description=f"Start of {phase.title}",
                milestone_type=MilestoneType.PHASE_START,
                phase_id=phase.phase_id,
                target_date_offset=phase.start_offset_days,
                completion_criteria=["Phase initiated", "Resources allocated"],
                deliverables=["Phase kickoff complete"]
            )
            
            # Phase end milestone
            end_milestone = Milestone(
                milestone_id=f"{phase.phase_id}-MS-END",
                title=f"{phase.title} - Completion",
                description=f"Completion of {phase.title}",
                milestone_type=MilestoneType.PHASE_END,
                phase_id=phase.phase_id,
                target_date_offset=phase.start_offset_days + phase.duration_days,
                completion_criteria=phase.success_criteria or ["Phase objectives met"],
                deliverables=phase.expected_outcomes or ["Phase deliverables"]
            )
            
            phase.milestones = [start_milestone, end_milestone]
            
            # Add delivery milestone if this is a major phase
            if phase.duration_days > 10:
                mid_point = phase.start_offset_days + (phase.duration_days // 2)
                delivery_milestone = Milestone(
                    milestone_id=f"{phase.phase_id}-MS-DELIVERY",
                    title=f"{phase.title} - Mid-Phase Delivery",
                    description=f"Mid-phase delivery for {phase.title}",
                    milestone_type=MilestoneType.DELIVERY,
                    phase_id=phase.phase_id,
                    target_date_offset=mid_point,
                    completion_criteria=["Interim deliverables ready"],
                    deliverables=["Mid-phase outputs"]
                )
                phase.milestones.insert(1, delivery_milestone)
    
    def _allocate_resources(
        self,
        phases: List[Phase],
        available_resources: Dict[str, int]
    ) -> tuple:
        """Allocate resources to phases."""
        # Create resource objects
        total_resources = []
        resource_id = 1
        
        for resource_name, quantity in available_resources.items():
            resource = Resource(
                resource_id=f"RES-{resource_id:03d}",
                name=resource_name,
                resource_type=ResourceType.HUMAN if resource_name in ["developers", "qa", "designers"] else ResourceType.TECHNICAL,
                quantity=quantity,
                unit="people" if resource_name in ["developers", "qa", "designers"] else "units",
                availability="Available",
                cost_per_unit=self._get_resource_cost(resource_name)
            )
            total_resources.append(resource)
            resource_id += 1
        
        # If no resources specified, create default resources
        if not total_resources:
            default_resources = [
                ("Developers", ResourceType.HUMAN, 3, "people", 150),
                ("QA Engineers", ResourceType.HUMAN, 2, "people", 120),
                ("DevOps", ResourceType.HUMAN, 1, "people", 140)
            ]
            
            for name, res_type, qty, unit, cost in default_resources:
                resource = Resource(
                    resource_id=f"RES-{resource_id:03d}",
                    name=name,
                    resource_type=res_type,
                    quantity=qty,
                    unit=unit,
                    availability="Available",
                    cost_per_unit=cost
                )
                total_resources.append(resource)
                resource_id += 1
        
        # Allocate resources to phases
        resource_allocation = {}
        for phase in phases:
            resource_allocation[phase.phase_id] = total_resources.copy()
        
        return total_resources, resource_allocation
    
    def _create_risk_mitigation_plans(
        self,
        phases: List[Phase],
        constraints: List[str]
    ) -> List[RiskMitigationPlan]:
        """Create risk mitigation plans."""
        risk_plans = []
        
        # Common implementation risks
        common_risks = [
            {
                "description": "Resource availability issues",
                "probability": "Medium",
                "impact": "High",
                "strategy": "Proactive resource management and backup planning",
                "actions": [
                    "Maintain resource pipeline",
                    "Cross-train team members",
                    "Establish backup resources"
                ],
                "contingency": "Engage external contractors if needed"
            },
            {
                "description": "Timeline slippage",
                "probability": "High",
                "impact": "Medium",
                "strategy": "Buffer time and critical path management",
                "actions": [
                    "Build 15% buffer into timeline",
                    "Monitor critical path daily",
                    "Implement early warning system"
                ],
                "contingency": "Reduce scope or extend timeline with stakeholder approval"
            },
            {
                "description": "Technical complexity underestimated",
                "probability": "Medium",
                "impact": "High",
                "strategy": "Technical spike and proof of concept",
                "actions": [
                    "Conduct technical assessment early",
                    "Build proof of concepts",
                    "Engage technical experts"
                ],
                "contingency": "Re-plan with revised estimates"
            },
            {
                "description": "Quality issues",
                "probability": "Low",
                "impact": "Critical",
                "strategy": "Comprehensive quality assurance",
                "actions": [
                    "Implement automated testing",
                    "Regular code reviews",
                    "Quality gates at each phase"
                ],
                "contingency": "Halt progress until quality standards met"
            }
        ]
        
        for i, risk in enumerate(common_risks, 1):
            plan = RiskMitigationPlan(
                risk_id=f"RISK-{i:02d}",
                risk_description=risk["description"],
                probability=risk["probability"],
                impact=risk["impact"],
                mitigation_strategy=risk["strategy"],
                mitigation_actions=risk["actions"],
                contingency_plan=risk["contingency"],
                owner="Project Manager",
                status="Active"
            )
            risk_plans.append(plan)
        
        return risk_plans
    
    def _create_quality_gates(self, phases: List[Phase]) -> List[QualityGate]:
        """Create quality gates for phases."""
        quality_gates = []
        
        for phase in phases:
            gate = QualityGate(
                gate_id=f"{phase.phase_id}-QG",
                title=f"{phase.title} Quality Gate",
                phase_id=phase.phase_id,
                criteria=[
                    "All phase tasks completed",
                    "All deliverables produced",
                    "Quality standards met",
                    "Success criteria achieved"
                ],
                checks=[
                    "Code review completed",
                    "Testing completed and passed",
                    "Documentation complete",
                    "Stakeholder review passed"
                ],
                required_approvers=["Technical Lead", "Project Manager"]
            )
            quality_gates.append(gate)
        
        return quality_gates
    
    def _extract_objectives(self, strategy_steps: List[Any]) -> List[str]:
        """Extract objectives from strategy steps."""
        objectives = []
        for step in strategy_steps:
            title = getattr(step, 'title', '')
            if title:
                objectives.append(f"Complete {title}")
        return objectives or ["Execute implementation successfully"]
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse duration string to days."""
        duration_str = duration_str.lower()
        
        if 'week' in duration_str:
            # Extract number of weeks
            weeks = 1
            parts = duration_str.split()
            for i, part in enumerate(parts):
                if 'week' in part and i > 0:
                    try:
                        weeks = int(parts[i-1])
                    except (ValueError, IndexError):
                        weeks = 1
            return weeks * 7
        elif 'day' in duration_str:
            days = 1
            parts = duration_str.split()
            for i, part in enumerate(parts):
                if 'day' in part and i > 0:
                    try:
                        days = int(parts[i-1])
                    except (ValueError, IndexError):
                        days = 1
            return days
        elif 'month' in duration_str:
            months = 1
            parts = duration_str.split()
            for i, part in enumerate(parts):
                if 'month' in part and i > 0:
                    try:
                        months = int(parts[i-1])
                    except (ValueError, IndexError):
                        months = 1
            return months * 30
        
        return 7  # Default to 1 week
    
    def _get_resource_cost(self, resource_name: str) -> float:
        """Get cost per unit for a resource."""
        cost_map = {
            "developers": 150.0,
            "qa": 120.0,
            "designers": 130.0,
            "devops": 140.0,
            "architects": 180.0,
            "managers": 160.0
        }
        return cost_map.get(resource_name.lower(), 100.0)
    
    def _estimate_total_cost(
        self,
        resources: List[Resource],
        total_effort_hours: int
    ) -> str:
        """Estimate total implementation cost."""
        total_cost = 0.0
        
        for resource in resources:
            if resource.cost_per_unit:
                # Estimate resource usage
                resource_hours = total_effort_hours * (resource.quantity / 10)  # Rough estimate
                total_cost += resource_hours * resource.cost_per_unit
        
        if total_cost > 0:
            # Add 20% overhead
            total_cost *= 1.2
            return f"${total_cost:,.0f}"
        
        return "Cost estimate pending"


def create_implementation_specialist(
    specialist_name: Optional[str] = None,
    methodology: Optional[str] = None
) -> ImplementationSpecialistRole:
    """
    Factory function to create an implementation specialist agent.
    
    Args:
        specialist_name: Custom name for the specialist
        methodology: Preferred methodology (Agile, Waterfall, Hybrid)
        
    Returns:
        Configured ImplementationSpecialistRole instance
    """
    name = specialist_name or "Implementation Specialist"
    
    return ImplementationSpecialistRole(
        specialist_name=name,
        methodologies=["Agile", "Waterfall", "Hybrid"],
        enable_agile=True,
        enable_quality_gates=True
    )


def demo_implementation_specialist():
    """Demonstrate implementation specialist capabilities."""
    print("\n" + "="*80)
    print("🏗️  IMPLEMENTATION SPECIALIST DEMONSTRATION")
    print("="*80)
    
    # Simulate a strategy with steps
    from dataclasses import dataclass as dc
    from typing import List as TList
    
    @dc
    class MockStep:
        title: str
        description: str
        duration: str
        deliverables: TList[str]
        success_criteria: TList[str]
    
    strategy_steps = [
        MockStep(
            title="Technical Assessment",
            description="Assess current system and requirements",
            duration="1 week",
            deliverables=["Assessment report", "Architecture diagram"],
            success_criteria=["All components assessed", "Risks identified"]
        ),
        MockStep(
            title="Solution Design",
            description="Design solution architecture",
            duration="2 weeks",
            deliverables=["Solution architecture", "Implementation plan"],
            success_criteria=["Architecture approved", "Plan validated"]
        ),
        MockStep(
            title="Implementation",
            description="Implement solution",
            duration="4 weeks",
            deliverables=["Working implementation", "Test results"],
            success_criteria=["Features implemented", "Tests passing"]
        ),
        MockStep(
            title="Testing & Validation",
            description="Comprehensive testing",
            duration="2 weeks",
            deliverables=["Test reports", "Bug fixes"],
            success_criteria=["All tests passed", "No critical bugs"]
        ),
        MockStep(
            title="Deployment",
            description="Deploy to production",
            duration="1 week",
            deliverables=["Production deployment", "Monitoring"],
            success_criteria=["Successful deployment", "Monitoring active"]
        )
    ]
    
    # Test different methodologies
    methodologies = ["Agile", "Waterfall", "Hybrid"]
    
    for methodology in methodologies:
        print(f"\n{'='*80}")
        print(f"Methodology: {methodology}")
        print(f"{'='*80}")
        
        specialist = create_implementation_specialist()
        
        plan = specialist.create_implementation_plan(
            problem_id="PROB-001",
            strategy_id="STRAT-001",
            strategy_title="API Performance Optimization",
            strategy_steps=strategy_steps,
            strategy_approach="incremental",
            estimated_timeline="10 weeks",
            available_resources={
                "developers": 5,
                "qa": 2,
                "devops": 1
            },
            constraints=["Budget: $200K", "Timeline: 10 weeks"],
            methodology=methodology
        )
        
        print(f"\n📊 IMPLEMENTATION PLAN SUMMARY: {plan.plan_id}")
        print(f"   Methodology: {methodology}")
        print(f"   Phases: {len(plan.phases)}")
        print(f"   Total Tasks: {len(plan.get_all_tasks())}")
        print(f"   Total Milestones: {len(plan.get_all_milestones())}")
        print(f"   Critical Path: {len(plan.get_critical_path())} tasks")
        print(f"   Duration: {plan.total_duration_days} days")
        print(f"   Effort: {plan.total_effort_hours} hours")
        print(f"   Cost: {plan.total_cost}")
        print(f"   Resources: {len(plan.total_resources)} types")
        print(f"   Risk Plans: {len(plan.risk_mitigation_plans)}")
        print(f"   Quality Gates: {len(plan.quality_gates)}")
        
        # Show phase breakdown
        print(f"\n   Phase Breakdown:")
        for phase in plan.phases:
            print(f"     - {phase.title}")
            print(f"       Tasks: {len(phase.tasks)} | Duration: {phase.duration_days} days")
            print(f"       Critical: {len(phase.get_critical_tasks())} | Milestones: {len(phase.milestones)}")
    
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*80)
    print(f"Generated {len(methodologies)} implementation plans")
    print(f"Demonstrated all planning methodologies")


if __name__ == "__main__":
    demo_implementation_specialist()
