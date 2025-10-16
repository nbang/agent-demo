"""
Solution Strategist Agent Role - Develops solution strategies from multiple perspectives.

This module provides a specialized agent role for generating solution strategies
that address complex problems from different viewpoints (technical, business,
user experience, security, scalability, etc.).

Key Capabilities:
- Multi-perspective strategy generation
- Approach development with trade-off analysis
- Benefit and drawback identification
- Assumption and dependency tracking
- Effort and cost estimation
- Risk assessment

Usage:
    strategist = create_solution_strategist(PerspectiveType.TECHNICAL)
    strategy = strategist.generate_strategy(
        problem_analysis=analysis,
        perspective=PerspectiveType.TECHNICAL,
        constraints=["budget", "timeline"]
    )
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class PerspectiveType(Enum):
    """Different perspectives for solution strategies."""
    TECHNICAL = "technical"
    BUSINESS = "business"
    USER_EXPERIENCE = "user_experience"
    SECURITY = "security"
    SCALABILITY = "scalability"
    COST = "cost"
    TIMELINE = "timeline"
    RISK = "risk"
    INNOVATION = "innovation"
    OPERATIONAL = "operational"


class StrategyApproach(Enum):
    """High-level strategy approaches."""
    INCREMENTAL = "incremental"
    TRANSFORMATIONAL = "transformational"
    HYBRID = "hybrid"
    QUICK_WIN = "quick_win"
    LONG_TERM = "long_term"
    PARALLEL = "parallel"


class SuccessProbability(Enum):
    """Success probability categories."""
    VERY_HIGH = "very_high"  # 80-100%
    HIGH = "high"  # 60-80%
    MEDIUM = "medium"  # 40-60%
    LOW = "low"  # 20-40%
    VERY_LOW = "very_low"  # 0-20%


@dataclass
class StrategyBenefit:
    """A benefit of a solution strategy."""
    benefit_id: str
    description: str
    category: str  # Performance, Cost, Quality, Risk, UX
    magnitude: str  # High, Medium, Low
    timeframe: str  # Immediate, Short-term, Long-term
    measurable: bool
    metrics: List[str] = field(default_factory=list)


@dataclass
class StrategyDrawback:
    """A drawback or limitation of a solution strategy."""
    drawback_id: str
    description: str
    category: str  # Cost, Time, Complexity, Risk
    severity: str  # Critical, High, Medium, Low
    mitigation_possible: bool
    mitigation_approaches: List[str] = field(default_factory=list)


@dataclass
class StrategyAssumption:
    """An assumption underlying a solution strategy."""
    assumption_id: str
    description: str
    category: str  # Technical, Business, Resource, External
    validity_confidence: float  # 0.0 to 1.0
    impact_if_invalid: str  # Critical, High, Medium, Low
    validation_method: str


@dataclass
class StrategyDependency:
    """A dependency required for strategy execution."""
    dependency_id: str
    description: str
    dependency_type: str  # Technical, Resource, Business, External
    criticality: str  # Critical, Important, Optional
    availability: str  # Available, Partial, Not Available
    acquisition_effort: str


@dataclass
class StrategyStep:
    """A step in the solution strategy."""
    step_number: int
    title: str
    description: str
    duration: str
    effort: str
    resources_required: List[str]
    dependencies: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)


@dataclass
class SolutionStrategy:
    """Comprehensive solution strategy from a specific perspective."""
    strategy_id: str
    problem_id: str
    perspective: PerspectiveType
    strategy_approach: StrategyApproach
    
    # Core strategy
    title: str
    description: str
    approach_summary: str
    key_steps: List[StrategyStep]
    
    # Analysis
    benefits: List[StrategyBenefit]
    drawbacks: List[StrategyDrawback]
    assumptions: List[StrategyAssumption]
    dependencies: List[StrategyDependency]
    
    # Estimates
    estimated_effort: str
    estimated_cost: str
    estimated_timeline: str
    risk_level: str
    success_probability: float
    
    # Metadata
    created_by: str
    
    # Additional context
    alternatives_considered: List[str] = field(default_factory=list)
    trade_offs: List[str] = field(default_factory=list)
    success_factors: List[str] = field(default_factory=list)
    failure_risks: List[str] = field(default_factory=list)
    
    # Metadata with defaults
    created_at: datetime = field(default_factory=datetime.now)
    confidence_score: float = 0.0
    
    def get_critical_assumptions(self) -> List[StrategyAssumption]:
        """Get assumptions with critical impact if invalid."""
        return [a for a in self.assumptions if a.impact_if_invalid == "Critical"]
    
    def get_high_magnitude_benefits(self) -> List[StrategyBenefit]:
        """Get benefits with high magnitude."""
        return [b for b in self.benefits if b.magnitude == "High"]
    
    def get_critical_dependencies(self) -> List[StrategyDependency]:
        """Get critical dependencies."""
        return [d for d in self.dependencies if d.criticality == "Critical"]


@dataclass
class StrategistCapability:
    """Capabilities of the solution strategist."""
    perspectives: List[PerspectiveType]
    strategy_approaches: List[StrategyApproach]
    expertise_areas: List[str]
    analysis_depth: str
    creative_thinking: bool
    risk_assessment: bool


class SolutionStrategistRole:
    """
    Solution Strategist agent role for developing comprehensive solution strategies.
    
    This agent generates solution strategies from specific perspectives, analyzing
    approaches, benefits, drawbacks, assumptions, and dependencies to provide
    actionable strategic recommendations.
    
    Core Capabilities:
    - Multi-perspective strategy development
    - Benefit-drawback trade-off analysis
    - Assumption identification and validation
    - Dependency mapping and management
    - Effort, cost, and timeline estimation
    - Risk and success probability assessment
    """
    
    def __init__(
        self,
        strategist_name: str = "Solution Strategist",
        primary_perspective: Optional[PerspectiveType] = None,
        expertise_areas: Optional[List[str]] = None,
        creative_thinking: bool = True
    ):
        """
        Initialize the solution strategist role.
        
        Args:
            strategist_name: Name of the strategist
            primary_perspective: Primary perspective for strategy generation
            expertise_areas: Areas of expertise
            creative_thinking: Enable creative/innovative approaches
        """
        self.strategist_name = strategist_name
        self.primary_perspective = primary_perspective or PerspectiveType.TECHNICAL
        self.expertise_areas = expertise_areas or [
            "System Architecture",
            "Business Strategy",
            "User Experience Design",
            "Risk Management",
            "Change Management"
        ]
        self.creative_thinking = creative_thinking
        
        self.capability = StrategistCapability(
            perspectives=[self.primary_perspective],
            strategy_approaches=list(StrategyApproach),
            expertise_areas=self.expertise_areas,
            analysis_depth="comprehensive",
            creative_thinking=creative_thinking,
            risk_assessment=True
        )
        
        logger.info(f"Initialized {strategist_name} with {self.primary_perspective.value} perspective")
    
    def generate_strategy(
        self,
        problem_id: str,
        problem_title: str,
        problem_description: str,
        problem_analysis: Optional[Dict[str, Any]] = None,
        perspective: Optional[PerspectiveType] = None,
        constraints: Optional[List[str]] = None,
        success_criteria: Optional[List[str]] = None
    ) -> SolutionStrategy:
        """
        Generate a comprehensive solution strategy for a problem.
        
        Args:
            problem_id: Unique problem identifier
            problem_title: Problem title
            problem_description: Problem description
            problem_analysis: Analysis results from ProblemAnalyzer
            perspective: Perspective to use (defaults to primary)
            constraints: Problem constraints
            success_criteria: Success criteria
            
        Returns:
            SolutionStrategy with complete strategic approach
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"💡 {self.strategist_name}: Generating Strategy")
        logger.info(f"{'='*60}")
        logger.info(f"Problem: {problem_title}")
        
        perspective = perspective or self.primary_perspective
        constraints = constraints or []
        success_criteria = success_criteria or []
        problem_analysis = problem_analysis or {}
        
        logger.info(f"Perspective: {perspective.value}")
        logger.info(f"Constraints: {len(constraints)}")
        
        # Determine strategy approach
        logger.info("\n🎯 Step 1: Determining Strategy Approach")
        strategy_approach = self._determine_approach(
            problem_description, perspective, constraints
        )
        logger.info(f"   Approach: {strategy_approach.value}")
        
        # Generate key steps
        logger.info("\n📝 Step 2: Developing Key Steps")
        key_steps = self._generate_steps(
            problem_description, perspective, strategy_approach
        )
        logger.info(f"   Steps: {len(key_steps)}")
        
        # Identify benefits
        logger.info("\n✨ Step 3: Identifying Benefits")
        benefits = self._identify_benefits(
            problem_description, perspective, key_steps
        )
        logger.info(f"   Benefits: {len(benefits)}")
        
        # Identify drawbacks
        logger.info("\n⚠️  Step 4: Identifying Drawbacks")
        drawbacks = self._identify_drawbacks(
            problem_description, perspective, key_steps, constraints
        )
        logger.info(f"   Drawbacks: {len(drawbacks)}")
        
        # Identify assumptions
        logger.info("\n💭 Step 5: Identifying Assumptions")
        assumptions = self._identify_assumptions(
            problem_description, perspective, key_steps
        )
        logger.info(f"   Assumptions: {len(assumptions)}")
        
        # Map dependencies
        logger.info("\n🔗 Step 6: Mapping Dependencies")
        dependencies = self._map_dependencies(
            problem_description, perspective, key_steps
        )
        logger.info(f"   Dependencies: {len(dependencies)}")
        
        # Estimate effort, cost, timeline
        logger.info("\n📊 Step 7: Creating Estimates")
        estimates = self._create_estimates(
            perspective, key_steps, strategy_approach
        )
        logger.info(f"   Effort: {estimates['effort']}")
        logger.info(f"   Cost: {estimates['cost']}")
        logger.info(f"   Timeline: {estimates['timeline']}")
        
        # Assess risk and success probability
        logger.info("\n⚖️  Step 8: Assessing Risk & Success")
        risk_assessment = self._assess_risk(
            drawbacks, assumptions, dependencies, constraints
        )
        logger.info(f"   Risk Level: {risk_assessment['risk_level']}")
        logger.info(f"   Success Probability: {risk_assessment['success_probability']:.0%}")
        
        # Generate trade-offs and success factors
        trade_offs = self._generate_trade_offs(benefits, drawbacks)
        success_factors = self._identify_success_factors(
            key_steps, assumptions, dependencies
        )
        failure_risks = self._identify_failure_risks(
            drawbacks, assumptions, constraints
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            benefits, drawbacks, assumptions, dependencies
        )
        
        strategy_id = f"STRAT-{problem_id}-{perspective.value.upper()}"
        
        strategy = SolutionStrategy(
            strategy_id=strategy_id,
            problem_id=problem_id,
            perspective=perspective,
            strategy_approach=strategy_approach,
            title=f"{perspective.value.title()} Solution Strategy",
            description=self._generate_description(perspective, strategy_approach),
            approach_summary=self._generate_approach_summary(
                perspective, strategy_approach, key_steps
            ),
            key_steps=key_steps,
            benefits=benefits,
            drawbacks=drawbacks,
            assumptions=assumptions,
            dependencies=dependencies,
            estimated_effort=estimates['effort'],
            estimated_cost=estimates['cost'],
            estimated_timeline=estimates['timeline'],
            risk_level=risk_assessment['risk_level'],
            success_probability=risk_assessment['success_probability'],
            trade_offs=trade_offs,
            success_factors=success_factors,
            failure_risks=failure_risks,
            created_by=self.strategist_name,
            confidence_score=confidence
        )
        
        logger.info(f"\n✅ Strategy Generated: {strategy_id}")
        logger.info(f"   Confidence: {confidence:.0%}")
        logger.info(f"   Critical Assumptions: {len(strategy.get_critical_assumptions())}")
        logger.info(f"   High-Value Benefits: {len(strategy.get_high_magnitude_benefits())}")
        
        return strategy
    
    def _determine_approach(
        self,
        problem_description: str,
        perspective: PerspectiveType,
        constraints: List[str]
    ) -> StrategyApproach:
        """Determine the overall strategy approach."""
        # Check for timeline constraints
        has_tight_timeline = any(
            "week" in c.lower() or "urgent" in c.lower() or "immediate" in c.lower()
            for c in constraints
        )
        
        # Check for complexity indicators
        is_complex = (
            "complex" in problem_description.lower() or
            "multiple" in problem_description.lower() or
            "legacy" in problem_description.lower()
        )
        
        if has_tight_timeline and not is_complex:
            return StrategyApproach.QUICK_WIN
        elif is_complex:
            return StrategyApproach.HYBRID
        elif perspective == PerspectiveType.INNOVATION:
            return StrategyApproach.TRANSFORMATIONAL
        else:
            return StrategyApproach.INCREMENTAL
    
    def _generate_steps(
        self,
        problem_description: str,
        perspective: PerspectiveType,
        approach: StrategyApproach
    ) -> List[StrategyStep]:
        """Generate key steps for the strategy."""
        steps = []
        
        if perspective == PerspectiveType.TECHNICAL:
            steps = [
                StrategyStep(
                    step_number=1,
                    title="Technical Assessment",
                    description="Conduct comprehensive technical assessment of current system and requirements",
                    duration="1 week",
                    effort="2-3 engineers",
                    resources_required=["Development team", "Architecture team"],
                    deliverables=["Technical assessment report", "Architecture diagram"],
                    success_criteria=["All components assessed", "Risks identified"]
                ),
                StrategyStep(
                    step_number=2,
                    title="Solution Design",
                    description="Design technical solution architecture and implementation approach",
                    duration="2 weeks",
                    effort="2-3 engineers",
                    resources_required=["Architecture team", "Development team"],
                    dependencies=["Technical Assessment"],
                    deliverables=["Solution architecture", "Implementation plan"],
                    success_criteria=["Architecture approved", "Plan validated"]
                ),
                StrategyStep(
                    step_number=3,
                    title="Implementation",
                    description="Implement solution following best practices and standards",
                    duration="4-6 weeks",
                    effort="3-5 engineers",
                    resources_required=["Development team", "DevOps team"],
                    dependencies=["Solution Design"],
                    deliverables=["Working implementation", "Test results"],
                    success_criteria=["All features implemented", "Tests passing"]
                ),
                StrategyStep(
                    step_number=4,
                    title="Testing & Validation",
                    description="Comprehensive testing and validation of solution",
                    duration="2 weeks",
                    effort="2-3 QA engineers",
                    resources_required=["QA team", "Development team"],
                    dependencies=["Implementation"],
                    deliverables=["Test reports", "Bug fixes"],
                    success_criteria=["All tests passed", "No critical bugs"]
                ),
                StrategyStep(
                    step_number=5,
                    title="Deployment",
                    description="Deploy solution to production with monitoring",
                    duration="1 week",
                    effort="2-3 engineers",
                    resources_required=["DevOps team", "Operations team"],
                    dependencies=["Testing & Validation"],
                    deliverables=["Production deployment", "Monitoring setup"],
                    success_criteria=["Successful deployment", "Monitoring active"]
                )
            ]
        
        elif perspective == PerspectiveType.BUSINESS:
            steps = [
                StrategyStep(
                    step_number=1,
                    title="Business Case Development",
                    description="Develop comprehensive business case with ROI analysis",
                    duration="1 week",
                    effort="1-2 analysts",
                    resources_required=["Business analyst", "Finance team"],
                    deliverables=["Business case", "ROI analysis"],
                    success_criteria=["ROI justified", "Stakeholder buy-in"]
                ),
                StrategyStep(
                    step_number=2,
                    title="Resource Allocation",
                    description="Secure and allocate necessary resources",
                    duration="2 weeks",
                    effort="1 project manager",
                    resources_required=["Management", "Finance"],
                    dependencies=["Business Case Development"],
                    deliverables=["Resource plan", "Budget approval"],
                    success_criteria=["Resources secured", "Budget approved"]
                ),
                StrategyStep(
                    step_number=3,
                    title="Quick Win Identification",
                    description="Identify and execute quick wins for early value",
                    duration="2-3 weeks",
                    effort="2-3 team members",
                    resources_required=["Cross-functional team"],
                    dependencies=["Resource Allocation"],
                    deliverables=["Quick wins delivered", "Value metrics"],
                    success_criteria=["Wins delivered", "Value demonstrated"]
                ),
                StrategyStep(
                    step_number=4,
                    title="Strategic Implementation",
                    description="Execute strategic initiatives per priority",
                    duration="3-4 months",
                    effort="Full team",
                    resources_required=["All teams"],
                    dependencies=["Quick Win Identification"],
                    deliverables=["Strategic outcomes", "Performance metrics"],
                    success_criteria=["Objectives achieved", "Targets met"]
                )
            ]
        
        elif perspective == PerspectiveType.USER_EXPERIENCE:
            steps = [
                StrategyStep(
                    step_number=1,
                    title="User Research",
                    description="Conduct user research to understand pain points and needs",
                    duration="2 weeks",
                    effort="1-2 UX researchers",
                    resources_required=["UX team", "Users"],
                    deliverables=["Research findings", "User personas"],
                    success_criteria=["Research complete", "Insights documented"]
                ),
                StrategyStep(
                    step_number=2,
                    title="UX Design",
                    description="Design improved user experience based on research",
                    duration="3 weeks",
                    effort="2-3 UX designers",
                    resources_required=["UX team", "Product team"],
                    dependencies=["User Research"],
                    deliverables=["UX designs", "Prototypes"],
                    success_criteria=["Designs approved", "Prototypes validated"]
                ),
                StrategyStep(
                    step_number=3,
                    title="Iterative Implementation",
                    description="Implement UX improvements iteratively with user feedback",
                    duration="4-6 weeks",
                    effort="3-4 developers",
                    resources_required=["Development team", "UX team"],
                    dependencies=["UX Design"],
                    deliverables=["UX implementations", "User feedback"],
                    success_criteria=["Improvements live", "User satisfaction improved"]
                ),
                StrategyStep(
                    step_number=4,
                    title="UX Validation",
                    description="Validate improvements through user testing and metrics",
                    duration="2 weeks",
                    effort="1-2 UX researchers",
                    resources_required=["UX team", "Analytics team"],
                    dependencies=["Iterative Implementation"],
                    deliverables=["Validation report", "Metrics analysis"],
                    success_criteria=["Validation complete", "Metrics improved"]
                )
            ]
        
        else:
            # Generic steps for other perspectives
            steps = [
                StrategyStep(
                    step_number=1,
                    title="Assessment & Planning",
                    description="Assess current state and plan approach",
                    duration="1-2 weeks",
                    effort="2-3 team members",
                    resources_required=["Assessment team"],
                    deliverables=["Assessment report", "Plan"],
                    success_criteria=["Assessment complete", "Plan approved"]
                ),
                StrategyStep(
                    step_number=2,
                    title="Execution",
                    description="Execute planned activities",
                    duration="4-8 weeks",
                    effort="Full team",
                    resources_required=["Execution team"],
                    dependencies=["Assessment & Planning"],
                    deliverables=["Outcomes", "Results"],
                    success_criteria=["Activities complete", "Outcomes achieved"]
                ),
                StrategyStep(
                    step_number=3,
                    title="Validation & Optimization",
                    description="Validate results and optimize approach",
                    duration="2 weeks",
                    effort="2-3 team members",
                    resources_required=["Validation team"],
                    dependencies=["Execution"],
                    deliverables=["Validation results", "Optimizations"],
                    success_criteria=["Results validated", "Optimizations applied"]
                )
            ]
        
        return steps
    
    def _identify_benefits(
        self,
        problem_description: str,
        perspective: PerspectiveType,
        steps: List[StrategyStep]
    ) -> List[StrategyBenefit]:
        """Identify benefits of the strategy."""
        benefits = []
        
        if perspective == PerspectiveType.TECHNICAL:
            benefits = [
                StrategyBenefit(
                    benefit_id="BEN-TECH-001",
                    description="Improved system performance and scalability",
                    category="Performance",
                    magnitude="High",
                    timeframe="Short-term",
                    measurable=True,
                    metrics=["Response time", "Throughput", "Concurrent users"]
                ),
                StrategyBenefit(
                    benefit_id="BEN-TECH-002",
                    description="Reduced technical debt and improved maintainability",
                    category="Quality",
                    magnitude="High",
                    timeframe="Long-term",
                    measurable=True,
                    metrics=["Code quality score", "Test coverage", "Bug count"]
                ),
                StrategyBenefit(
                    benefit_id="BEN-TECH-003",
                    description="Enhanced reliability and reduced downtime",
                    category="Risk",
                    magnitude="Medium",
                    timeframe="Short-term",
                    measurable=True,
                    metrics=["Uptime %", "MTBF", "Error rate"]
                )
            ]
        
        elif perspective == PerspectiveType.BUSINESS:
            benefits = [
                StrategyBenefit(
                    benefit_id="BEN-BUS-001",
                    description="Clear ROI visibility and business value tracking",
                    category="Cost",
                    magnitude="High",
                    timeframe="Immediate",
                    measurable=True,
                    metrics=["ROI %", "Cost savings", "Revenue impact"]
                ),
                StrategyBenefit(
                    benefit_id="BEN-BUS-002",
                    description="Stakeholder alignment and buy-in",
                    category="Risk",
                    magnitude="Medium",
                    timeframe="Immediate",
                    measurable=False,
                    metrics=["Stakeholder satisfaction"]
                ),
                StrategyBenefit(
                    benefit_id="BEN-BUS-003",
                    description="Optimized resource allocation and utilization",
                    category="Cost",
                    magnitude="High",
                    timeframe="Short-term",
                    measurable=True,
                    metrics=["Resource utilization %", "Cost per outcome"]
                )
            ]
        
        elif perspective == PerspectiveType.USER_EXPERIENCE:
            benefits = [
                StrategyBenefit(
                    benefit_id="BEN-UX-001",
                    description="Improved user satisfaction and engagement",
                    category="UX",
                    magnitude="High",
                    timeframe="Short-term",
                    measurable=True,
                    metrics=["NPS", "CSAT", "Engagement rate"]
                ),
                StrategyBenefit(
                    benefit_id="BEN-UX-002",
                    description="Reduced support tickets and user issues",
                    category="Cost",
                    magnitude="Medium",
                    timeframe="Short-term",
                    measurable=True,
                    metrics=["Support tickets", "Resolution time"]
                ),
                StrategyBenefit(
                    benefit_id="BEN-UX-003",
                    description="Better user retention and loyalty",
                    category="Quality",
                    magnitude="High",
                    timeframe="Long-term",
                    measurable=True,
                    metrics=["Retention rate", "Churn rate", "LTV"]
                )
            ]
        
        else:
            benefits = [
                StrategyBenefit(
                    benefit_id=f"BEN-{perspective.value.upper()}-001",
                    description=f"Addresses problem from {perspective.value} perspective",
                    category="Quality",
                    magnitude="Medium",
                    timeframe="Short-term",
                    measurable=True,
                    metrics=["Success metrics"]
                )
            ]
        
        return benefits
    
    def _identify_drawbacks(
        self,
        problem_description: str,
        perspective: PerspectiveType,
        steps: List[StrategyStep],
        constraints: List[str]
    ) -> List[StrategyDrawback]:
        """Identify drawbacks and limitations."""
        drawbacks = []
        
        # Common drawbacks based on steps
        total_duration_weeks = sum(
            int(s.duration.split()[0].split('-')[0])
            for s in steps if 'week' in s.duration.lower()
        )
        
        if total_duration_weeks > 8:
            drawbacks.append(StrategyDrawback(
                drawback_id="DRAW-001",
                description=f"Extended timeline of {total_duration_weeks}+ weeks may delay value realization",
                category="Time",
                severity="Medium",
                mitigation_possible=True,
                mitigation_approaches=[
                    "Implement in phases with early value delivery",
                    "Parallelize independent workstreams",
                    "Focus on quick wins first"
                ]
            ))
        
        if perspective == PerspectiveType.TECHNICAL:
            drawbacks.extend([
                StrategyDrawback(
                    drawback_id="DRAW-TECH-001",
                    description="Requires significant development effort and resources",
                    category="Cost",
                    severity="High",
                    mitigation_possible=True,
                    mitigation_approaches=[
                        "Leverage existing solutions and frameworks",
                        "Outsource non-core components",
                        "Implement incrementally"
                    ]
                ),
                StrategyDrawback(
                    drawback_id="DRAW-TECH-002",
                    description="Potential for introducing bugs during implementation",
                    category="Risk",
                    severity="Medium",
                    mitigation_possible=True,
                    mitigation_approaches=[
                        "Comprehensive testing strategy",
                        "Staged rollout with monitoring",
                        "Rollback procedures"
                    ]
                )
            ])
        
        elif perspective == PerspectiveType.BUSINESS:
            drawbacks.extend([
                StrategyDrawback(
                    drawback_id="DRAW-BUS-001",
                    description="May not address underlying technical root causes",
                    category="Complexity",
                    severity="Medium",
                    mitigation_possible=True,
                    mitigation_approaches=[
                        "Coordinate with technical team",
                        "Ensure technical feasibility",
                        "Regular technical review"
                    ]
                ),
                StrategyDrawback(
                    drawback_id="DRAW-BUS-002",
                    description="Requires ongoing monitoring and adjustment",
                    category="Cost",
                    severity="Low",
                    mitigation_possible=True,
                    mitigation_approaches=[
                        "Automated monitoring and reporting",
                        "Regular review cadence",
                        "Clear success metrics"
                    ]
                )
            ])
        
        elif perspective == PerspectiveType.USER_EXPERIENCE:
            drawbacks.extend([
                StrategyDrawback(
                    drawback_id="DRAW-UX-001",
                    description="Requires user research time and participation",
                    category="Time",
                    severity="Medium",
                    mitigation_possible=True,
                    mitigation_approaches=[
                        "Use existing research and data",
                        "Conduct remote/asynchronous research",
                        "Leverage analytics data"
                    ]
                ),
                StrategyDrawback(
                    drawback_id="DRAW-UX-002",
                    description="May not address systemic technical issues",
                    category="Complexity",
                    severity="Medium",
                    mitigation_possible=True,
                    mitigation_approaches=[
                        "Coordinate with technical team",
                        "Identify technical dependencies",
                        "Ensure technical feasibility"
                    ]
                )
            ])
        
        return drawbacks
    
    def _identify_assumptions(
        self,
        problem_description: str,
        perspective: PerspectiveType,
        steps: List[StrategyStep]
    ) -> List[StrategyAssumption]:
        """Identify underlying assumptions."""
        assumptions = []
        
        # Resource availability assumptions
        required_resources = set()
        for step in steps:
            required_resources.update(step.resources_required)
        
        if required_resources:
            assumptions.append(StrategyAssumption(
                assumption_id="ASM-001",
                description=f"Required resources are available: {', '.join(list(required_resources)[:3])}",
                category="Resource",
                validity_confidence=0.70,
                impact_if_invalid="Critical",
                validation_method="Resource capacity planning and availability check"
            ))
        
        # Technical assumptions
        if perspective == PerspectiveType.TECHNICAL:
            assumptions.extend([
                StrategyAssumption(
                    assumption_id="ASM-TECH-001",
                    description="Team has necessary technical skills and expertise",
                    category="Technical",
                    validity_confidence=0.75,
                    impact_if_invalid="High",
                    validation_method="Skills assessment and gap analysis"
                ),
                StrategyAssumption(
                    assumption_id="ASM-TECH-002",
                    description="Development infrastructure and tools are adequate",
                    category="Technical",
                    validity_confidence=0.80,
                    impact_if_invalid="Medium",
                    validation_method="Infrastructure audit and capacity check"
                ),
                StrategyAssumption(
                    assumption_id="ASM-TECH-003",
                    description="Testing environment mirrors production sufficiently",
                    category="Technical",
                    validity_confidence=0.70,
                    impact_if_invalid="High",
                    validation_method="Environment comparison and validation"
                )
            ])
        
        # Business assumptions
        elif perspective == PerspectiveType.BUSINESS:
            assumptions.extend([
                StrategyAssumption(
                    assumption_id="ASM-BUS-001",
                    description="Budget is available and approved",
                    category="Business",
                    validity_confidence=0.80,
                    impact_if_invalid="Critical",
                    validation_method="Budget approval confirmation"
                ),
                StrategyAssumption(
                    assumption_id="ASM-BUS-002",
                    description="Stakeholders are aligned on priorities and approach",
                    category="Business",
                    validity_confidence=0.65,
                    impact_if_invalid="High",
                    validation_method="Stakeholder alignment meetings"
                ),
                StrategyAssumption(
                    assumption_id="ASM-BUS-003",
                    description="ROI projections are based on accurate data",
                    category="Business",
                    validity_confidence=0.70,
                    impact_if_invalid="Medium",
                    validation_method="Data validation and historical comparison"
                )
            ])
        
        # UX assumptions
        elif perspective == PerspectiveType.USER_EXPERIENCE:
            assumptions.extend([
                StrategyAssumption(
                    assumption_id="ASM-UX-001",
                    description="Users are willing to provide feedback and participate",
                    category="External",
                    validity_confidence=0.75,
                    impact_if_invalid="High",
                    validation_method="User engagement and recruitment validation"
                ),
                StrategyAssumption(
                    assumption_id="ASM-UX-002",
                    description="UX resources have capacity for research and design",
                    category="Resource",
                    validity_confidence=0.70,
                    impact_if_invalid="High",
                    validation_method="Resource capacity check"
                ),
                StrategyAssumption(
                    assumption_id="ASM-UX-003",
                    description="Analytics tracking is in place and accurate",
                    category="Technical",
                    validity_confidence=0.80,
                    impact_if_invalid="Medium",
                    validation_method="Analytics audit and validation"
                )
            ])
        
        return assumptions
    
    def _map_dependencies(
        self,
        problem_description: str,
        perspective: PerspectiveType,
        steps: List[StrategyStep]
    ) -> List[StrategyDependency]:
        """Map strategy dependencies."""
        dependencies = []
        
        # Extract dependencies from steps
        for step in steps:
            for dep_name in step.dependencies:
                dependencies.append(StrategyDependency(
                    dependency_id=f"DEP-{step.step_number:03d}",
                    description=f"Step {step.step_number} depends on: {dep_name}",
                    dependency_type="Process",
                    criticality="Critical",
                    availability="Available",
                    acquisition_effort="None"
                ))
        
        # Add perspective-specific dependencies
        if perspective == PerspectiveType.TECHNICAL:
            dependencies.extend([
                StrategyDependency(
                    dependency_id="DEP-TECH-001",
                    description="Development environment and tools",
                    dependency_type="Technical",
                    criticality="Critical",
                    availability="Available",
                    acquisition_effort="Low"
                ),
                StrategyDependency(
                    dependency_id="DEP-TECH-002",
                    description="Staging and production deployment access",
                    dependency_type="Technical",
                    criticality="Critical",
                    availability="Available",
                    acquisition_effort="Low"
                )
            ])
        
        elif perspective == PerspectiveType.BUSINESS:
            dependencies.extend([
                StrategyDependency(
                    dependency_id="DEP-BUS-001",
                    description="Executive approval and sponsorship",
                    dependency_type="Business",
                    criticality="Critical",
                    availability="Partial",
                    acquisition_effort="Medium"
                ),
                StrategyDependency(
                    dependency_id="DEP-BUS-002",
                    description="Budget allocation and financial approval",
                    dependency_type="Business",
                    criticality="Critical",
                    availability="Partial",
                    acquisition_effort="Medium"
                )
            ])
        
        return dependencies
    
    def _create_estimates(
        self,
        perspective: PerspectiveType,
        steps: List[StrategyStep],
        approach: StrategyApproach
    ) -> Dict[str, str]:
        """Create effort, cost, and timeline estimates."""
        # Calculate from steps
        total_weeks = sum(
            int(s.duration.split()[0].split('-')[-1])
            for s in steps if 'week' in s.duration.lower()
        )
        
        if approach == StrategyApproach.QUICK_WIN:
            effort = "2-4 weeks"
            cost = "$10,000 - $25,000"
            timeline = "1 month"
        elif approach == StrategyApproach.INCREMENTAL:
            effort = f"{total_weeks}-{total_weeks + 2} weeks"
            cost = f"${total_weeks * 10000} - ${total_weeks * 15000}"
            timeline = f"{total_weeks // 4} months"
        elif approach == StrategyApproach.TRANSFORMATIONAL:
            effort = f"{total_weeks}-{total_weeks + 4} weeks"
            cost = f"${total_weeks * 15000} - ${total_weeks * 25000}"
            timeline = f"{(total_weeks // 4) + 1} months"
        else:  # HYBRID or LONG_TERM
            effort = f"{total_weeks}-{total_weeks + 3} weeks"
            cost = f"${total_weeks * 12000} - ${total_weeks * 20000}"
            timeline = f"{total_weeks // 4} months"
        
        return {
            'effort': effort,
            'cost': cost,
            'timeline': timeline
        }
    
    def _assess_risk(
        self,
        drawbacks: List[StrategyDrawback],
        assumptions: List[StrategyAssumption],
        dependencies: List[StrategyDependency],
        constraints: List[str]
    ) -> Dict[str, Any]:
        """Assess risk level and success probability."""
        # Count critical factors
        critical_drawbacks = sum(1 for d in drawbacks if d.severity in ["Critical", "High"])
        critical_assumptions = sum(1 for a in assumptions if a.impact_if_invalid == "Critical")
        critical_dependencies = sum(1 for d in dependencies if d.criticality == "Critical")
        
        # Calculate risk score
        risk_score = (
            critical_drawbacks * 0.3 +
            critical_assumptions * 0.4 +
            critical_dependencies * 0.2 +
            len(constraints) * 0.1
        )
        
        if risk_score > 5:
            risk_level = "High"
            success_probability = 0.50
        elif risk_score > 3:
            risk_level = "Medium"
            success_probability = 0.70
        else:
            risk_level = "Low"
            success_probability = 0.85
        
        return {
            'risk_level': risk_level,
            'success_probability': success_probability
        }
    
    def _generate_trade_offs(
        self,
        benefits: List[StrategyBenefit],
        drawbacks: List[StrategyDrawback]
    ) -> List[str]:
        """Generate trade-off descriptions."""
        trade_offs = []
        
        # Benefits vs drawbacks
        if benefits and drawbacks:
            high_benefits = [b for b in benefits if b.magnitude == "High"]
            high_drawbacks = [d for d in drawbacks if d.severity in ["Critical", "High"]]
            
            if high_benefits and high_drawbacks:
                trade_offs.append(
                    f"{len(high_benefits)} high-value benefits vs {len(high_drawbacks)} significant drawbacks"
                )
        
        # Time vs quality
        trade_offs.append("Faster delivery vs comprehensive solution")
        
        # Cost vs capability
        trade_offs.append("Lower cost vs advanced capabilities")
        
        return trade_offs
    
    def _identify_success_factors(
        self,
        steps: List[StrategyStep],
        assumptions: List[StrategyAssumption],
        dependencies: List[StrategyDependency]
    ) -> List[str]:
        """Identify critical success factors."""
        factors = []
        
        # From assumptions with high confidence
        high_confidence_assumptions = [
            a for a in assumptions if a.validity_confidence > 0.75
        ]
        if high_confidence_assumptions:
            factors.append(
                f"Valid assumptions ({len(high_confidence_assumptions)} verified)"
            )
        
        # From dependencies
        available_dependencies = [
            d for d in dependencies if d.availability == "Available"
        ]
        if available_dependencies:
            factors.append(
                f"Dependencies available ({len(available_dependencies)} ready)"
            )
        
        # General factors
        factors.extend([
            "Strong stakeholder support and engagement",
            "Clear communication and coordination",
            "Effective risk mitigation strategies",
            "Regular progress monitoring and adjustment"
        ])
        
        return factors
    
    def _identify_failure_risks(
        self,
        drawbacks: List[StrategyDrawback],
        assumptions: List[StrategyAssumption],
        constraints: List[str]
    ) -> List[str]:
        """Identify failure risks."""
        risks = []
        
        # From critical assumptions
        critical_assumptions = [
            a for a in assumptions if a.impact_if_invalid == "Critical"
        ]
        if critical_assumptions:
            risks.append(
                f"Invalid assumptions ({len(critical_assumptions)} critical)"
            )
        
        # From severe drawbacks
        severe_drawbacks = [
            d for d in drawbacks if d.severity == "Critical"
        ]
        if severe_drawbacks:
            risks.append(
                f"Severe drawbacks realized ({len(severe_drawbacks)} critical)"
            )
        
        # General risks
        risks.extend([
            "Resource availability issues",
            "Timeline slippage and delays",
            "Scope creep and changing requirements",
            "Technical complexity underestimated"
        ])
        
        return risks
    
    def _calculate_confidence(
        self,
        benefits: List[StrategyBenefit],
        drawbacks: List[StrategyDrawback],
        assumptions: List[StrategyAssumption],
        dependencies: List[StrategyDependency]
    ) -> float:
        """Calculate overall strategy confidence."""
        # High confidence factors
        high_benefits = len([b for b in benefits if b.magnitude == "High"])
        low_drawbacks = len([d for d in drawbacks if d.severity == "Low"])
        high_confidence_assumptions = len([a for a in assumptions if a.validity_confidence > 0.75])
        available_dependencies = len([d for d in dependencies if d.availability == "Available"])
        
        # Calculate confidence
        confidence = (
            (high_benefits / max(len(benefits), 1)) * 0.25 +
            (low_drawbacks / max(len(drawbacks), 1)) * 0.25 +
            (high_confidence_assumptions / max(len(assumptions), 1)) * 0.30 +
            (available_dependencies / max(len(dependencies), 1)) * 0.20
        )
        
        return min(0.95, max(0.50, confidence))
    
    def _generate_description(
        self,
        perspective: PerspectiveType,
        approach: StrategyApproach
    ) -> str:
        """Generate strategy description."""
        descriptions = {
            PerspectiveType.TECHNICAL: "Technical solution focusing on system architecture, implementation, and performance optimization",
            PerspectiveType.BUSINESS: "Business-driven approach focusing on ROI, stakeholder value, and resource optimization",
            PerspectiveType.USER_EXPERIENCE: "User-centric strategy emphasizing experience improvement and satisfaction",
            PerspectiveType.SECURITY: "Security-focused approach prioritizing protection, compliance, and risk mitigation",
            PerspectiveType.SCALABILITY: "Scalability strategy addressing growth, performance, and capacity planning"
        }
        
        return descriptions.get(
            perspective,
            f"{perspective.value.title()} perspective strategy"
        )
    
    def _generate_approach_summary(
        self,
        perspective: PerspectiveType,
        approach: StrategyApproach,
        steps: List[StrategyStep]
    ) -> str:
        """Generate approach summary."""
        return f"""
{approach.value.title()} approach addressing the problem from a {perspective.value} perspective.
The strategy consists of {len(steps)} key phases:

{chr(10).join(f'{i}. {step.title} ({step.duration})' for i, step in enumerate(steps, 1))}

This approach balances immediate impact with long-term sustainability while
addressing the core issues identified in the problem analysis.
"""


def create_solution_strategist(
    perspective: PerspectiveType = PerspectiveType.TECHNICAL,
    strategist_name: Optional[str] = None
) -> SolutionStrategistRole:
    """
    Factory function to create a solution strategist agent.
    
    Args:
        perspective: Primary perspective for strategy generation
        strategist_name: Custom name for the strategist
        
    Returns:
        Configured SolutionStrategistRole instance
    """
    name = strategist_name or f"{perspective.value.title()} Strategist"
    
    return SolutionStrategistRole(
        strategist_name=name,
        primary_perspective=perspective,
        expertise_areas=[
            "System Architecture",
            "Business Strategy",
            "User Experience",
            "Risk Management",
            "Implementation Planning"
        ],
        creative_thinking=True
    )


def demo_solution_strategist():
    """Demonstrate solution strategist capabilities."""
    print("\n" + "="*80)
    print("💡 SOLUTION STRATEGIST DEMONSTRATION")
    print("="*80)
    
    # Create strategists for different perspectives
    perspectives = [
        PerspectiveType.TECHNICAL,
        PerspectiveType.BUSINESS,
        PerspectiveType.USER_EXPERIENCE
    ]
    
    problem_description = """
    Our e-commerce platform experiences 35% cart abandonment during checkout
    due to slow page loads (5-10 seconds) and complex multi-step process.
    This results in $500K monthly revenue loss.
    """
    
    print("\nGenerating strategies from multiple perspectives...\n")
    
    strategies = []
    for perspective in perspectives:
        print(f"\n{'='*80}")
        print(f"Perspective: {perspective.value.upper()}")
        print(f"{'='*80}")
        
        strategist = create_solution_strategist(perspective)
        
        strategy = strategist.generate_strategy(
            problem_id="PROB-001",
            problem_title="E-commerce Cart Abandonment",
            problem_description=problem_description,
            constraints=["6-month timeline", "$200K budget"],
            success_criteria=["Reduce abandonment to <20%", "Page load <2s"]
        )
        
        strategies.append(strategy)
        
        print(f"\n📊 STRATEGY SUMMARY: {strategy.strategy_id}")
        print(f"   Approach: {strategy.strategy_approach.value}")
        print(f"   Steps: {len(strategy.key_steps)}")
        print(f"   Benefits: {len(strategy.benefits)} ({len(strategy.get_high_magnitude_benefits())} high-value)")
        print(f"   Drawbacks: {len(strategy.drawbacks)}")
        print(f"   Assumptions: {len(strategy.assumptions)} ({len(strategy.get_critical_assumptions())} critical)")
        print(f"   Dependencies: {len(strategy.dependencies)}")
        print(f"   Effort: {strategy.estimated_effort}")
        print(f"   Cost: {strategy.estimated_cost}")
        print(f"   Timeline: {strategy.estimated_timeline}")
        print(f"   Risk: {strategy.risk_level}")
        print(f"   Success Probability: {strategy.success_probability:.0%}")
        print(f"   Confidence: {strategy.confidence_score:.0%}")
    
    # Compare strategies
    print("\n" + "="*80)
    print("📊 STRATEGY COMPARISON")
    print("="*80)
    
    for strategy in strategies:
        print(f"\n{strategy.perspective.value.upper()}")
        print(f"  Score: {strategy.success_probability:.0%} success | {strategy.confidence_score:.0%} confidence")
        print(f"  Cost: {strategy.estimated_cost}")
        print(f"  Timeline: {strategy.estimated_timeline}")
        print(f"  Risk: {strategy.risk_level}")
    
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*80)
    print(f"Generated {len(strategies)} comprehensive strategies")
    print(f"Total perspectives analyzed: {len(perspectives)}")


if __name__ == "__main__":
    demo_solution_strategist()
