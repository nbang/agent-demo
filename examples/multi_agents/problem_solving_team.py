"""
Problem-Solving Team - Multi-perspective problem analysis and solution generation.

This module provides a multi-agent team that approaches complex problems from
different perspectives (technical, business, user experience) to provide
comprehensive solution recommendations with clear reasoning.

Architecture:
- Problem Analyzer: Breaks down problems and identifies components
- Solution Strategist: Develops solution strategies from multiple angles
- Implementation Specialist: Provides practical implementation guidance
- Evaluation & Ranking: Scores solutions and analyzes trade-offs

Usage:
    team = ProblemSolvingTeam()
    result = team.solve_problem(
        problem="How to improve application performance",
        context={"current_state": "...", "constraints": "..."}
    )
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProblemType(Enum):
    """Types of problems the team can handle."""
    TECHNICAL = "technical"
    BUSINESS = "business"
    PROCESS = "process"
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    ARCHITECTURAL = "architectural"
    ORGANIZATIONAL = "organizational"


class ProblemComplexity(Enum):
    """Problem complexity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PerspectiveType(Enum):
    """Different perspectives for problem analysis."""
    TECHNICAL = "technical"
    BUSINESS = "business"
    USER_EXPERIENCE = "user_experience"
    SECURITY = "security"
    SCALABILITY = "scalability"
    COST = "cost"
    TIMELINE = "timeline"
    RISK = "risk"


class SolutionStatus(Enum):
    """Solution recommendation status."""
    DRAFT = "draft"
    EVALUATED = "evaluated"
    RECOMMENDED = "recommended"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class ProblemStatement:
    """Structured problem definition."""
    problem_id: str
    title: str
    description: str
    problem_type: ProblemType
    complexity: ProblemComplexity
    context: Dict[str, Any]
    constraints: List[str] = field(default_factory=list)
    stakeholders: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    current_state: Optional[str] = None
    desired_state: Optional[str] = None
    deadline: Optional[datetime] = None
    budget_constraints: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProblemAnalysis:
    """Analysis results from problem analyzer."""
    problem_id: str
    root_causes: List[str]
    key_components: List[str]
    dependencies: List[str]
    impact_areas: List[str]
    risk_factors: List[str]
    opportunities: List[str]
    analysis_summary: str
    analyzed_by: str
    analyzed_at: datetime = field(default_factory=datetime.now)
    confidence_score: float = 0.0


@dataclass
class SolutionStrategy:
    """Solution strategy from a specific perspective."""
    strategy_id: str
    problem_id: str
    perspective: PerspectiveType
    approach: str
    key_steps: List[str]
    benefits: List[str]
    drawbacks: List[str]
    assumptions: List[str]
    dependencies: List[str]
    estimated_effort: str
    estimated_cost: str
    estimated_timeline: str
    risk_level: str
    success_probability: float
    created_by: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ImplementationPlan:
    """Detailed implementation guidance."""
    plan_id: str
    strategy_id: str
    phases: List[Dict[str, Any]]
    resources_required: List[str]
    technical_requirements: List[str]
    skill_requirements: List[str]
    milestones: List[Dict[str, Any]]
    dependencies: List[str]
    risks: List[str]
    mitigation_strategies: List[str]
    success_metrics: List[str]
    created_by: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SolutionEvaluation:
    """Comprehensive solution evaluation."""
    evaluation_id: str
    strategy_id: str
    
    # Scoring (0-100 for each dimension)
    technical_feasibility: float
    business_value: float
    cost_effectiveness: float
    risk_level: float
    implementation_complexity: float
    time_to_value: float
    scalability: float
    maintainability: float
    
    # Overall assessment
    overall_score: float
    ranking: int
    recommendation: str
    trade_offs: List[str]
    key_considerations: List[str]
    
    evaluated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProblemSolvingResult:
    """Complete problem-solving outcome."""
    problem_id: str
    problem_statement: ProblemStatement
    analysis: ProblemAnalysis
    strategies: List[SolutionStrategy]
    implementation_plans: List[ImplementationPlan]
    evaluations: List[SolutionEvaluation]
    
    # Recommendations (sorted by rank)
    recommended_solutions: List[str]
    executive_summary: str
    detailed_report: str
    
    # Metadata
    team_members: List[str]
    total_perspectives: int
    analysis_duration: float
    completed_at: datetime = field(default_factory=datetime.now)
    
    def get_top_solution(self) -> Optional[SolutionStrategy]:
        """Get the highest-ranked solution."""
        if not self.evaluations:
            return None
        
        top_eval = min(self.evaluations, key=lambda e: e.ranking)
        return next(
            (s for s in self.strategies if s.strategy_id == top_eval.strategy_id),
            None
        )
    
    def get_solutions_by_rank(self) -> List[tuple[SolutionStrategy, SolutionEvaluation]]:
        """Get all solutions sorted by rank."""
        sorted_evals = sorted(self.evaluations, key=lambda e: e.ranking)
        result = []
        for eval in sorted_evals:
            strategy = next(
                (s for s in self.strategies if s.strategy_id == eval.strategy_id),
                None
            )
            if strategy:
                result.append((strategy, eval))
        return result


class ProblemSolvingTeam:
    """
    Multi-agent team for comprehensive problem-solving.
    
    The team analyzes complex problems from multiple perspectives and
    provides ranked solution recommendations with implementation guidance.
    
    Workflow:
    1. Problem Analysis - Break down and understand the problem
    2. Strategy Development - Generate solutions from different perspectives
    3. Implementation Planning - Create detailed implementation guidance
    4. Evaluation & Ranking - Score solutions and identify trade-offs
    5. Recommendation - Present top solutions with clear reasoning
    """
    
    def __init__(
        self,
        team_name: str = "Problem-Solving Team",
        perspectives: Optional[List[PerspectiveType]] = None,
        enable_parallel_analysis: bool = True
    ):
        """
        Initialize the problem-solving team.
        
        Args:
            team_name: Name of the team
            perspectives: List of perspectives to analyze from
            enable_parallel_analysis: Whether to analyze perspectives in parallel
        """
        self.team_name = team_name
        self.perspectives = perspectives or [
            PerspectiveType.TECHNICAL,
            PerspectiveType.BUSINESS,
            PerspectiveType.USER_EXPERIENCE
        ]
        self.enable_parallel_analysis = enable_parallel_analysis
        
        logger.info(f"Initialized {team_name} with {len(self.perspectives)} perspectives")
    
    def solve_problem(
        self,
        problem: str,
        problem_type: ProblemType = ProblemType.TECHNICAL,
        complexity: ProblemComplexity = ProblemComplexity.MEDIUM,
        context: Optional[Dict[str, Any]] = None,
        constraints: Optional[List[str]] = None,
        success_criteria: Optional[List[str]] = None
    ) -> ProblemSolvingResult:
        """
        Solve a complex problem through multi-perspective analysis.
        
        Args:
            problem: Problem description
            problem_type: Type of problem
            complexity: Problem complexity level
            context: Additional context information
            constraints: Problem constraints
            success_criteria: Success criteria for solutions
            
        Returns:
            ProblemSolvingResult with analysis, strategies, and recommendations
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"🎯 STARTING PROBLEM-SOLVING SESSION")
        logger.info(f"{'='*80}")
        logger.info(f"Problem: {problem}")
        logger.info(f"Type: {problem_type.value} | Complexity: {complexity.value}")
        
        start_time = datetime.now()
        
        # 1. Create problem statement
        problem_statement = self._create_problem_statement(
            problem=problem,
            problem_type=problem_type,
            complexity=complexity,
            context=context or {},
            constraints=constraints or [],
            success_criteria=success_criteria or []
        )
        
        # 2. Analyze the problem
        logger.info(f"\n{'='*80}")
        logger.info("📊 PHASE 1: PROBLEM ANALYSIS")
        logger.info(f"{'='*80}")
        analysis = self._analyze_problem(problem_statement)
        
        # 3. Generate solution strategies from multiple perspectives
        logger.info(f"\n{'='*80}")
        logger.info("💡 PHASE 2: SOLUTION STRATEGY GENERATION")
        logger.info(f"{'='*80}")
        strategies = self._generate_strategies(problem_statement, analysis)
        
        # 4. Create implementation plans
        logger.info(f"\n{'='*80}")
        logger.info("🛠️  PHASE 3: IMPLEMENTATION PLANNING")
        logger.info(f"{'='*80}")
        implementation_plans = self._create_implementation_plans(strategies)
        
        # 5. Evaluate and rank solutions
        logger.info(f"\n{'='*80}")
        logger.info("⚖️  PHASE 4: SOLUTION EVALUATION & RANKING")
        logger.info(f"{'='*80}")
        evaluations = self._evaluate_solutions(strategies, problem_statement)
        
        # 6. Generate recommendations
        logger.info(f"\n{'='*80}")
        logger.info("📋 PHASE 5: RECOMMENDATIONS")
        logger.info(f"{'='*80}")
        executive_summary, detailed_report, recommended_solutions = self._generate_recommendations(
            problem_statement, analysis, strategies, evaluations
        )
        
        duration = (datetime.now() - start_time).total_seconds()
        
        result = ProblemSolvingResult(
            problem_id=problem_statement.problem_id,
            problem_statement=problem_statement,
            analysis=analysis,
            strategies=strategies,
            implementation_plans=implementation_plans,
            evaluations=evaluations,
            recommended_solutions=recommended_solutions,
            executive_summary=executive_summary,
            detailed_report=detailed_report,
            team_members=["Problem Analyzer", "Solution Strategist", "Implementation Specialist"],
            total_perspectives=len(self.perspectives),
            analysis_duration=duration
        )
        
        logger.info(f"\n{'='*80}")
        logger.info(f"✅ PROBLEM-SOLVING COMPLETE")
        logger.info(f"{'='*80}")
        logger.info(f"Duration: {duration:.2f}s")
        logger.info(f"Solutions Generated: {len(strategies)}")
        logger.info(f"Top Recommendation: {recommended_solutions[0] if recommended_solutions else 'None'}")
        
        return result
    
    def _create_problem_statement(
        self,
        problem: str,
        problem_type: ProblemType,
        complexity: ProblemComplexity,
        context: Dict[str, Any],
        constraints: List[str],
        success_criteria: List[str]
    ) -> ProblemStatement:
        """Create structured problem statement."""
        problem_id = f"PROB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return ProblemStatement(
            problem_id=problem_id,
            title=problem[:100],  # First 100 chars as title
            description=problem,
            problem_type=problem_type,
            complexity=complexity,
            context=context,
            constraints=constraints,
            success_criteria=success_criteria,
            current_state=context.get("current_state"),
            desired_state=context.get("desired_state")
        )
    
    def _analyze_problem(self, problem: ProblemStatement) -> ProblemAnalysis:
        """
        Analyze problem to identify root causes and key components.
        
        This would typically use a ProblemAnalyzer agent role.
        For now, we'll simulate the analysis.
        """
        logger.info("🔍 Problem Analyzer: Breaking down the problem...")
        
        # Simulate problem analysis
        # In real implementation, this would call ProblemAnalyzer agent
        
        analysis = ProblemAnalysis(
            problem_id=problem.problem_id,
            root_causes=[
                "Insufficient understanding of requirements",
                "Technical debt accumulation",
                "Resource constraints"
            ],
            key_components=[
                "Performance bottleneck",
                "Scalability concerns",
                "User experience impact"
            ],
            dependencies=[
                "External API availability",
                "Database performance",
                "Network infrastructure"
            ],
            impact_areas=[
                "End-user experience",
                "Operational costs",
                "Team productivity"
            ],
            risk_factors=[
                "Time constraints",
                "Budget limitations",
                "Technical complexity"
            ],
            opportunities=[
                "Technology upgrade",
                "Process improvement",
                "Team skill development"
            ],
            analysis_summary=f"Problem analyzed: {problem.title}. Identified {3} root causes and {3} key components.",
            analyzed_by="Problem Analyzer Agent",
            confidence_score=0.85
        )
        
        logger.info(f"✓ Analysis complete - Confidence: {analysis.confidence_score:.0%}")
        logger.info(f"  Root Causes: {len(analysis.root_causes)}")
        logger.info(f"  Key Components: {len(analysis.key_components)}")
        logger.info(f"  Risk Factors: {len(analysis.risk_factors)}")
        
        return analysis
    
    def _generate_strategies(
        self,
        problem: ProblemStatement,
        analysis: ProblemAnalysis
    ) -> List[SolutionStrategy]:
        """
        Generate solution strategies from multiple perspectives.
        
        This would typically use SolutionStrategist agent roles.
        """
        logger.info(f"💭 Solution Strategist: Generating strategies from {len(self.perspectives)} perspectives...")
        
        strategies = []
        
        for i, perspective in enumerate(self.perspectives, 1):
            strategy_id = f"STRAT-{problem.problem_id}-{perspective.value.upper()}"
            
            # Simulate strategy generation based on perspective
            # In real implementation, each would call SolutionStrategist agent
            
            if perspective == PerspectiveType.TECHNICAL:
                strategy = SolutionStrategy(
                    strategy_id=strategy_id,
                    problem_id=problem.problem_id,
                    perspective=perspective,
                    approach="Technical optimization and architecture refactoring",
                    key_steps=[
                        "Profile and identify performance bottlenecks",
                        "Implement caching layer",
                        "Optimize database queries",
                        "Refactor critical code paths",
                        "Implement monitoring and alerting"
                    ],
                    benefits=[
                        "Improved system performance",
                        "Better scalability",
                        "Reduced technical debt"
                    ],
                    drawbacks=[
                        "Requires development time",
                        "Potential for introducing bugs",
                        "Team learning curve"
                    ],
                    assumptions=[
                        "Team has necessary technical skills",
                        "Development environment is available",
                        "Testing infrastructure is in place"
                    ],
                    dependencies=[
                        "Development resources",
                        "Testing team availability",
                        "Production deployment window"
                    ],
                    estimated_effort="4-6 weeks",
                    estimated_cost="$50,000 - $75,000",
                    estimated_timeline="2 months",
                    risk_level="Medium",
                    success_probability=0.75,
                    created_by=f"Solution Strategist ({perspective.value})"
                )
            
            elif perspective == PerspectiveType.BUSINESS:
                strategy = SolutionStrategy(
                    strategy_id=strategy_id,
                    problem_id=problem.problem_id,
                    perspective=perspective,
                    approach="Business process optimization and resource allocation",
                    key_steps=[
                        "Conduct cost-benefit analysis",
                        "Prioritize high-impact improvements",
                        "Allocate budget for quick wins",
                        "Establish ROI tracking",
                        "Communicate value to stakeholders"
                    ],
                    benefits=[
                        "Clear ROI visibility",
                        "Stakeholder buy-in",
                        "Optimized resource allocation"
                    ],
                    drawbacks=[
                        "May not address technical root causes",
                        "Requires ongoing monitoring",
                        "Change management overhead"
                    ],
                    assumptions=[
                        "Budget is available",
                        "Stakeholders are aligned",
                        "ROI metrics are defined"
                    ],
                    dependencies=[
                        "Executive approval",
                        "Budget allocation",
                        "Team availability"
                    ],
                    estimated_effort="2-3 weeks",
                    estimated_cost="$25,000 - $40,000",
                    estimated_timeline="1 month",
                    risk_level="Low",
                    success_probability=0.85,
                    created_by=f"Solution Strategist ({perspective.value})"
                )
            
            else:  # USER_EXPERIENCE
                strategy = SolutionStrategy(
                    strategy_id=strategy_id,
                    problem_id=problem.problem_id,
                    perspective=perspective,
                    approach="User-centric improvements and experience optimization",
                    key_steps=[
                        "Gather user feedback",
                        "Identify pain points",
                        "Design UX improvements",
                        "Implement progressive enhancements",
                        "Measure user satisfaction"
                    ],
                    benefits=[
                        "Improved user satisfaction",
                        "Reduced support tickets",
                        "Better user retention"
                    ],
                    drawbacks=[
                        "Requires user research time",
                        "May not address underlying issues",
                        "Ongoing iteration needed"
                    ],
                    assumptions=[
                        "Users are willing to provide feedback",
                        "UX resources are available",
                        "Metrics tracking is in place"
                    ],
                    dependencies=[
                        "User research team",
                        "Design resources",
                        "Analytics infrastructure"
                    ],
                    estimated_effort="3-4 weeks",
                    estimated_cost="$30,000 - $50,000",
                    estimated_timeline="1.5 months",
                    risk_level="Low",
                    success_probability=0.80,
                    created_by=f"Solution Strategist ({perspective.value})"
                )
            
            strategies.append(strategy)
            logger.info(f"  [{i}/{len(self.perspectives)}] {perspective.value.upper()} perspective: {strategy.approach}")
        
        logger.info(f"✓ Generated {len(strategies)} solution strategies")
        
        return strategies
    
    def _create_implementation_plans(
        self,
        strategies: List[SolutionStrategy]
    ) -> List[ImplementationPlan]:
        """
        Create detailed implementation plans for strategies.
        
        This would typically use ImplementationSpecialist agent role.
        """
        logger.info(f"📝 Implementation Specialist: Creating implementation plans...")
        
        plans = []
        
        for strategy in strategies:
            plan_id = f"PLAN-{strategy.strategy_id}"
            
            # Simulate implementation planning
            # In real implementation, this would call ImplementationSpecialist agent
            
            plan = ImplementationPlan(
                plan_id=plan_id,
                strategy_id=strategy.strategy_id,
                phases=[
                    {
                        "phase": 1,
                        "name": "Planning & Setup",
                        "duration": "1 week",
                        "tasks": ["Requirements gathering", "Team formation", "Environment setup"]
                    },
                    {
                        "phase": 2,
                        "name": "Development",
                        "duration": strategy.estimated_effort,
                        "tasks": strategy.key_steps
                    },
                    {
                        "phase": 3,
                        "name": "Testing & Validation",
                        "duration": "1 week",
                        "tasks": ["Unit testing", "Integration testing", "User acceptance testing"]
                    },
                    {
                        "phase": 4,
                        "name": "Deployment & Monitoring",
                        "duration": "3 days",
                        "tasks": ["Production deployment", "Monitoring setup", "Documentation"]
                    }
                ],
                resources_required=[
                    "Development team (2-3 developers)",
                    "QA team (1-2 testers)",
                    "DevOps support",
                    "Project manager"
                ],
                technical_requirements=[
                    "Development environment",
                    "Testing infrastructure",
                    "Deployment pipeline",
                    "Monitoring tools"
                ],
                skill_requirements=[
                    "Software development",
                    "System architecture",
                    "Testing and QA",
                    "DevOps"
                ],
                milestones=[
                    {"name": "Planning Complete", "week": 1},
                    {"name": "50% Development", "week": 3},
                    {"name": "Testing Complete", "week": 6},
                    {"name": "Production Deployment", "week": 7}
                ],
                dependencies=strategy.dependencies,
                risks=[
                    "Resource availability issues",
                    "Technical complexity higher than estimated",
                    "Integration challenges",
                    "Timeline slippage"
                ],
                mitigation_strategies=[
                    "Buffer time in schedule",
                    "Early prototyping",
                    "Regular status updates",
                    "Contingency planning"
                ],
                success_metrics=[
                    "Performance improvement targets met",
                    "No critical bugs in production",
                    "User satisfaction improvement",
                    "ROI targets achieved"
                ],
                created_by="Implementation Specialist Agent"
            )
            
            plans.append(plan)
        
        logger.info(f"✓ Created {len(plans)} implementation plans")
        
        return plans
    
    def _evaluate_solutions(
        self,
        strategies: List[SolutionStrategy],
        problem: ProblemStatement
    ) -> List[SolutionEvaluation]:
        """
        Evaluate and rank solution strategies.
        
        This would typically use a SolutionEvaluator component.
        """
        logger.info(f"📊 Solution Evaluator: Evaluating {len(strategies)} solutions...")
        
        evaluations = []
        
        for i, strategy in enumerate(strategies):
            eval_id = f"EVAL-{strategy.strategy_id}"
            
            # Simulate evaluation scoring
            # In real implementation, this would use sophisticated evaluation logic
            
            # Score based on perspective and problem complexity
            base_score = 70.0
            
            if strategy.perspective == PerspectiveType.TECHNICAL:
                technical_feasibility = base_score + 15
                business_value = base_score + 5
                cost_effectiveness = base_score - 10
            elif strategy.perspective == PerspectiveType.BUSINESS:
                technical_feasibility = base_score - 5
                business_value = base_score + 20
                cost_effectiveness = base_score + 15
            else:  # USER_EXPERIENCE
                technical_feasibility = base_score + 5
                business_value = base_score + 10
                cost_effectiveness = base_score + 10
            
            evaluation = SolutionEvaluation(
                evaluation_id=eval_id,
                strategy_id=strategy.strategy_id,
                technical_feasibility=technical_feasibility,
                business_value=business_value,
                cost_effectiveness=cost_effectiveness,
                risk_level=100 - (75 if strategy.risk_level == "Low" else 60),
                implementation_complexity=base_score + (5 * i),
                time_to_value=80 - (5 * i),
                scalability=base_score + 10,
                maintainability=base_score + 5,
                overall_score=0.0,  # Will be calculated
                ranking=i + 1,
                recommendation="",
                trade_offs=[],
                key_considerations=[]
            )
            
            # Calculate overall score (weighted average)
            evaluation.overall_score = (
                evaluation.technical_feasibility * 0.20 +
                evaluation.business_value * 0.25 +
                evaluation.cost_effectiveness * 0.20 +
                evaluation.risk_level * 0.15 +
                evaluation.implementation_complexity * 0.10 +
                evaluation.time_to_value * 0.10
            )
            
            # Generate recommendation
            if evaluation.overall_score >= 80:
                evaluation.recommendation = "Highly Recommended"
            elif evaluation.overall_score >= 70:
                evaluation.recommendation = "Recommended"
            elif evaluation.overall_score >= 60:
                evaluation.recommendation = "Consider with Caution"
            else:
                evaluation.recommendation = "Not Recommended"
            
            # Identify trade-offs
            evaluation.trade_offs = [
                f"Higher technical feasibility vs {strategy.estimated_cost} cost",
                f"{strategy.estimated_timeline} timeline vs scope completeness",
                f"{strategy.risk_level} risk level vs innovation potential"
            ]
            
            # Key considerations
            evaluation.key_considerations = [
                f"Success probability: {strategy.success_probability:.0%}",
                f"Estimated effort: {strategy.estimated_effort}",
                f"Dependencies: {len(strategy.dependencies)} items",
                f"Perspective: {strategy.perspective.value}"
            ]
            
            evaluations.append(evaluation)
            
            logger.info(f"  [{i+1}/{len(strategies)}] {strategy.perspective.value.upper()}: "
                       f"Score={evaluation.overall_score:.1f}, {evaluation.recommendation}")
        
        # Re-rank based on overall score (highest score = rank 1)
        evaluations.sort(key=lambda e: e.overall_score, reverse=True)
        for rank, evaluation in enumerate(evaluations, 1):
            evaluation.ranking = rank
        
        logger.info(f"✓ Evaluation complete - Best solution: Rank #{evaluations[0].ranking}")
        
        return evaluations
    
    def _generate_recommendations(
        self,
        problem: ProblemStatement,
        analysis: ProblemAnalysis,
        strategies: List[SolutionStrategy],
        evaluations: List[SolutionEvaluation]
    ) -> tuple[str, str, List[str]]:
        """Generate executive summary and detailed report."""
        logger.info("📝 Generating recommendations...")
        
        # Get ranked solutions
        sorted_evals = sorted(evaluations, key=lambda e: e.ranking)
        recommended_ids = [e.strategy_id for e in sorted_evals[:3]]  # Top 3
        
        # Executive summary
        top_eval = sorted_evals[0]
        top_strategy = next(s for s in strategies if s.strategy_id == top_eval.strategy_id)
        
        executive_summary = f"""
EXECUTIVE SUMMARY
=================

Problem: {problem.title}
Type: {problem.problem_type.value.upper()}
Complexity: {problem.complexity.value.upper()}

Analysis:
- Root Causes Identified: {len(analysis.root_causes)}
- Key Components: {len(analysis.key_components)}
- Risk Factors: {len(analysis.risk_factors)}
- Analysis Confidence: {analysis.confidence_score:.0%}

Top Recommendation:
- Approach: {top_strategy.approach}
- Perspective: {top_strategy.perspective.value.upper()}
- Overall Score: {top_eval.overall_score:.1f}/100
- Recommendation: {top_eval.recommendation}
- Estimated Timeline: {top_strategy.estimated_timeline}
- Estimated Cost: {top_strategy.estimated_cost}
- Success Probability: {top_strategy.success_probability:.0%}

Key Benefits:
{chr(10).join(f'- {b}' for b in top_strategy.benefits[:3])}

Next Steps:
1. Review detailed analysis and all solution options
2. Validate assumptions and dependencies
3. Secure necessary approvals and resources
4. Begin implementation planning
"""
        
        # Detailed report
        detailed_report = f"""
DETAILED PROBLEM-SOLVING REPORT
================================

PROBLEM STATEMENT
{problem.description}

Context:
{chr(10).join(f'- {k}: {v}' for k, v in problem.context.items())}

Constraints:
{chr(10).join(f'- {c}' for c in problem.constraints)}

Success Criteria:
{chr(10).join(f'- {c}' for c in problem.success_criteria)}

---

PROBLEM ANALYSIS
{analysis.analysis_summary}

Root Causes:
{chr(10).join(f'{i}. {cause}' for i, cause in enumerate(analysis.root_causes, 1))}

Key Components:
{chr(10).join(f'{i}. {comp}' for i, comp in enumerate(analysis.key_components, 1))}

Risk Factors:
{chr(10).join(f'{i}. {risk}' for i, risk in enumerate(analysis.risk_factors, 1))}

Opportunities:
{chr(10).join(f'{i}. {opp}' for i, opp in enumerate(analysis.opportunities, 1))}

---

SOLUTION STRATEGIES
"""
        
        # Add each strategy to report
        for i, eval in enumerate(sorted_evals, 1):
            strategy = next(s for s in strategies if s.strategy_id == eval.strategy_id)
            detailed_report += f"""
{i}. {strategy.perspective.value.upper()} PERSPECTIVE
   Score: {eval.overall_score:.1f}/100 | {eval.recommendation}
   
   Approach: {strategy.approach}
   
   Key Steps:
   {chr(10).join(f'   - {step}' for step in strategy.key_steps)}
   
   Benefits:
   {chr(10).join(f'   ✓ {b}' for b in strategy.benefits)}
   
   Drawbacks:
   {chr(10).join(f'   ✗ {d}' for d in strategy.drawbacks)}
   
   Estimated Timeline: {strategy.estimated_timeline}
   Estimated Cost: {strategy.estimated_cost}
   Risk Level: {strategy.risk_level}
   Success Probability: {strategy.success_probability:.0%}
   
   Trade-offs:
   {chr(10).join(f'   • {t}' for t in eval.trade_offs)}
   
"""
        
        detailed_report += f"""
---

RECOMMENDATIONS

Based on comprehensive analysis from {len(self.perspectives)} perspectives, we recommend:

1. PRIMARY RECOMMENDATION: {top_strategy.perspective.value.upper()} approach
   - Overall Score: {top_eval.overall_score:.1f}/100
   - Timeline: {top_strategy.estimated_timeline}
   - Cost: {top_strategy.estimated_cost}
   - Success Probability: {top_strategy.success_probability:.0%}

2. ALTERNATIVE OPTIONS: Consider {sorted_evals[1].strategy_id if len(sorted_evals) > 1 else 'None'}
   as backup or complementary approach

3. IMPLEMENTATION PRIORITY: Begin with Phase 1 planning immediately
   to validate assumptions and secure resources

4. RISK MITIGATION: Address identified risk factors through
   contingency planning and staged rollout

---

NEXT STEPS

1. Stakeholder Review - Present findings to decision makers
2. Resource Allocation - Secure budget and team assignments
3. Detailed Planning - Develop comprehensive implementation plan
4. Risk Assessment - Validate assumptions and dependencies
5. Kickoff - Begin execution of recommended solution
"""
        
        logger.info(f"✓ Recommendations generated")
        logger.info(f"  Top 3 Solutions: {', '.join(recommended_ids[:3])}")
        
        return executive_summary, detailed_report, recommended_ids


def demo_problem_solving_team():
    """Demonstrate problem-solving team capabilities."""
    print("\n" + "="*80)
    print("🎯 PROBLEM-SOLVING TEAM DEMONSTRATION")
    print("="*80)
    
    # Initialize team
    team = ProblemSolvingTeam(
        team_name="Elite Problem-Solving Team",
        perspectives=[
            PerspectiveType.TECHNICAL,
            PerspectiveType.BUSINESS,
            PerspectiveType.USER_EXPERIENCE
        ]
    )
    
    # Define a complex problem
    problem = """
    Our e-commerce platform is experiencing performance degradation during peak 
    hours, resulting in slow page loads (5-10 seconds) and cart abandonment 
    rates of 35%. This is impacting revenue by an estimated $500K per month.
    
    Current infrastructure:
    - Monolithic application architecture
    - Single database instance
    - Limited caching
    - No CDN for static assets
    - 1M+ daily active users
    
    We need a solution that:
    - Reduces page load time to <2 seconds
    - Handles 10x traffic spikes
    - Is cost-effective
    - Can be implemented within 3 months
    """
    
    context = {
        "current_state": "Performance issues during peak hours, high cart abandonment",
        "desired_state": "Fast, scalable platform with <2s page loads",
        "revenue_impact": "$500K/month loss",
        "traffic": "1M+ daily active users"
    }
    
    constraints = [
        "3-month implementation timeline",
        "Budget: $200K maximum",
        "Must maintain 99.9% uptime during migration",
        "Cannot require full rewrite"
    ]
    
    success_criteria = [
        "Page load time <2 seconds",
        "Handle 10x traffic spikes",
        "Cart abandonment rate <20%",
        "Cost-effective solution within budget"
    ]
    
    # Solve the problem
    result = team.solve_problem(
        problem=problem,
        problem_type=ProblemType.TECHNICAL,
        complexity=ProblemComplexity.HIGH,
        context=context,
        constraints=constraints,
        success_criteria=success_criteria
    )
    
    # Display results
    print("\n" + "="*80)
    print("📊 RESULTS")
    print("="*80)
    
    print("\n" + result.executive_summary)
    
    print("\n" + "="*80)
    print("🏆 TOP SOLUTIONS RANKING")
    print("="*80)
    
    for strategy, evaluation in result.get_solutions_by_rank():
        print(f"\n#{evaluation.ranking}. {strategy.perspective.value.upper()} APPROACH")
        print(f"   Score: {evaluation.overall_score:.1f}/100")
        print(f"   Recommendation: {evaluation.recommendation}")
        print(f"   Approach: {strategy.approach}")
        print(f"   Timeline: {strategy.estimated_timeline}")
        print(f"   Cost: {strategy.estimated_cost}")
        print(f"   Success Probability: {strategy.success_probability:.0%}")
    
    # Save detailed report
    print("\n" + "="*80)
    print("💾 SAVING DETAILED REPORT")
    print("="*80)
    
    report_filename = f"problem_solving_report_{result.problem_id}.txt"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(result.detailed_report)
    
    print(f"✓ Detailed report saved to: {report_filename}")
    
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*80)
    print(f"Total Duration: {result.analysis_duration:.2f}s")
    print(f"Strategies Evaluated: {len(result.strategies)}")
    print(f"Perspectives Analyzed: {result.total_perspectives}")
    top_solution = result.get_top_solution()
    print(f"Top Recommendation: {top_solution.perspective.value.upper() if top_solution else 'None'}")


if __name__ == "__main__":
    # Run demonstration
    demo_problem_solving_team()
