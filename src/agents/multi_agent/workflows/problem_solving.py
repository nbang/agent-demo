"""
Problem-Solving Workflow - Orchestrates the complete problem-solving process.

This module provides workflow orchestration for the problem-solving system,
coordinating the ProblemAnalyzer, SolutionStrategist, and ImplementationSpecialist
roles to provide end-to-end problem resolution.

Workflow Steps:
1. Problem Analysis - Identify root causes, components, dependencies, risks
2. Strategy Generation - Develop solutions from multiple perspectives
3. Strategy Evaluation - Rank and compare strategies
4. Implementation Planning - Create detailed execution plans
5. Recommendations - Provide final recommendations and next steps

Usage:
    workflow = ProblemSolvingWorkflow()
    result = workflow.solve_problem(
        problem_title="API Performance Issues",
        problem_description="System experiencing high latency...",
        perspectives=[PerspectiveType.TECHNICAL, PerspectiveType.BUSINESS]
    )
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import logging

# Import problem-solving roles
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Ensure imports work
try:
    from ..roles.problem_analyzer import (
        ProblemAnalyzerRole,
        create_problem_analyzer,
        ComprehensiveProblemAnalysis,
        ImpactLevel
    )
    from ..roles.solution_strategist import (
        SolutionStrategistRole,
        create_solution_strategist,
        SolutionStrategy,
        PerspectiveType
    )
    from ..roles.implementation_specialist import (
        ImplementationSpecialistRole,
        create_implementation_specialist,
        ImplementationPlan
    )
except ImportError:
    # Fallback for direct execution
    from agents.multi_agent.roles.problem_analyzer import (
        ProblemAnalyzerRole,
        create_problem_analyzer,
        ComprehensiveProblemAnalysis,
        ImpactLevel
    )
    from agents.multi_agent.roles.solution_strategist import (
        SolutionStrategistRole,
        create_solution_strategist,
        SolutionStrategy,
        PerspectiveType
    )
    from agents.multi_agent.roles.implementation_specialist import (
        ImplementationSpecialistRole,
        create_implementation_specialist,
        ImplementationPlan
    )

logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status."""
    NOT_STARTED = "not_started"
    ANALYZING = "analyzing"
    STRATEGIZING = "strategizing"
    PLANNING = "planning"
    EVALUATING = "evaluating"
    COMPLETED = "completed"
    FAILED = "failed"


class RecommendationType(Enum):
    """Types of recommendations."""
    IMMEDIATE_ACTION = "immediate_action"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    RISK_MITIGATION = "risk_mitigation"
    QUICK_WIN = "quick_win"


@dataclass
class Recommendation:
    """A recommendation from the problem-solving process."""
    recommendation_id: str
    recommendation_type: RecommendationType
    title: str
    description: str
    rationale: str
    expected_impact: str
    effort_required: str
    priority: str  # Critical, High, Medium, Low
    dependencies: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)


@dataclass
class StrategyEvaluation:
    """Evaluation of a solution strategy."""
    strategy_id: str
    perspective: str
    
    # Scores (0-100)
    feasibility_score: float
    impact_score: float
    cost_efficiency_score: float
    risk_score: float
    overall_score: float
    
    # Rankings
    rank: int = 0
    
    # Strengths and weaknesses
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    
    # Recommendation
    recommended: bool = False
    recommendation_reason: str = ""


@dataclass
class ProblemSolvingResult:
    """Complete result of the problem-solving workflow."""
    workflow_id: str
    problem_id: str
    problem_title: str
    
    # Workflow execution
    status: WorkflowStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0
    
    # Analysis phase
    problem_analysis: Optional[ComprehensiveProblemAnalysis] = None
    
    # Strategy phase
    strategies: List[SolutionStrategy] = field(default_factory=list)
    strategy_evaluations: List[StrategyEvaluation] = field(default_factory=list)
    recommended_strategy: Optional[SolutionStrategy] = None
    
    # Implementation phase
    implementation_plans: Dict[str, ImplementationPlan] = field(default_factory=dict)
    recommended_plan: Optional[ImplementationPlan] = None
    
    # Recommendations
    recommendations: List[Recommendation] = field(default_factory=list)
    
    # Summary
    executive_summary: str = ""
    key_insights: List[str] = field(default_factory=list)
    success_probability: float = 0.0
    
    # Metadata
    perspectives_analyzed: List[str] = field(default_factory=list)
    total_strategies_generated: int = 0
    total_plans_created: int = 0
    
    def get_top_strategies(self, n: int = 3) -> List[Tuple[SolutionStrategy, StrategyEvaluation]]:
        """Get top N strategies by overall score."""
        if not self.strategy_evaluations:
            return []
        
        sorted_evals = sorted(
            self.strategy_evaluations,
            key=lambda e: e.overall_score,
            reverse=True
        )[:n]
        
        result = []
        for eval in sorted_evals:
            strategy = next((s for s in self.strategies if s.strategy_id == eval.strategy_id), None)
            if strategy:
                result.append((strategy, eval))
        
        return result
    
    def get_critical_recommendations(self) -> List[Recommendation]:
        """Get recommendations with critical priority."""
        return [r for r in self.recommendations if r.priority == "Critical"]
    
    def get_quick_wins(self) -> List[Recommendation]:
        """Get quick win recommendations."""
        return [r for r in self.recommendations if r.recommendation_type == RecommendationType.QUICK_WIN]


class ProblemSolvingWorkflow:
    """
    Orchestrates the complete problem-solving workflow.
    
    This workflow coordinates multiple specialized agents to analyze problems,
    generate solution strategies, create implementation plans, and provide
    actionable recommendations.
    
    Workflow Phases:
    1. Problem Analysis - Deep analysis of the problem
    2. Strategy Generation - Multi-perspective solution strategies
    3. Strategy Evaluation - Rank and compare strategies
    4. Implementation Planning - Detailed execution plans
    5. Final Recommendations - Actionable next steps
    """
    
    def __init__(
        self,
        workflow_name: str = "Problem Solving Workflow",
        enable_parallel_strategies: bool = True,
        max_strategies_per_perspective: int = 1
    ):
        """
        Initialize the problem-solving workflow.
        
        Args:
            workflow_name: Name of the workflow
            enable_parallel_strategies: Generate strategies in parallel
            max_strategies_per_perspective: Max strategies per perspective
        """
        self.workflow_name = workflow_name
        self.enable_parallel_strategies = enable_parallel_strategies
        self.max_strategies_per_perspective = max_strategies_per_perspective
        
        logger.info(f"Initialized {workflow_name}")
    
    def solve_problem(
        self,
        problem_title: str,
        problem_description: str,
        problem_context: Optional[Dict[str, Any]] = None,
        perspectives: Optional[List[PerspectiveType]] = None,
        constraints: Optional[List[str]] = None,
        success_criteria: Optional[List[str]] = None,
        available_resources: Optional[Dict[str, int]] = None,
        methodology: str = "Hybrid"
    ) -> ProblemSolvingResult:
        """
        Execute the complete problem-solving workflow.
        
        Args:
            problem_title: Title of the problem
            problem_description: Detailed problem description
            problem_context: Additional context information
            perspectives: Perspectives to analyze (default: Technical, Business, UX)
            constraints: Problem constraints
            success_criteria: Success criteria
            available_resources: Available resources for implementation
            methodology: Implementation methodology (Agile, Waterfall, Hybrid)
            
        Returns:
            ProblemSolvingResult with complete analysis, strategies, and plans
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"🚀 {self.workflow_name}: Starting Problem-Solving Workflow")
        logger.info(f"{'='*80}")
        logger.info(f"Problem: {problem_title}")
        
        start_time = datetime.now()
        problem_id = f"PROB-{start_time.strftime('%Y%m%d%H%M%S')}"
        workflow_id = f"WF-{start_time.strftime('%Y%m%d%H%M%S')}"
        
        # Default perspectives
        perspectives = perspectives or [
            PerspectiveType.TECHNICAL,
            PerspectiveType.BUSINESS,
            PerspectiveType.USER_EXPERIENCE
        ]
        
        constraints = constraints or []
        success_criteria = success_criteria or []
        problem_context = problem_context or {}
        available_resources = available_resources or {}
        
        logger.info(f"Workflow ID: {workflow_id}")
        logger.info(f"Problem ID: {problem_id}")
        logger.info(f"Perspectives: {len(perspectives)}")
        
        # Initialize result
        result = ProblemSolvingResult(
            workflow_id=workflow_id,
            problem_id=problem_id,
            problem_title=problem_title,
            status=WorkflowStatus.NOT_STARTED,
            started_at=start_time,
            perspectives_analyzed=[p.value for p in perspectives]
        )
        
        try:
            # Phase 1: Problem Analysis
            result.status = WorkflowStatus.ANALYZING
            analysis = self._analyze_problem(
                problem_id,
                problem_title,
                problem_description,
                problem_context
            )
            result.problem_analysis = analysis
            
            # Phase 2: Strategy Generation
            result.status = WorkflowStatus.STRATEGIZING
            strategies = self._generate_strategies(
                problem_id,
                problem_title,
                problem_description,
                analysis,
                perspectives,
                constraints,
                success_criteria
            )
            result.strategies = strategies
            result.total_strategies_generated = len(strategies)
            
            # Phase 3: Strategy Evaluation
            result.status = WorkflowStatus.EVALUATING
            evaluations = self._evaluate_strategies(strategies)
            result.strategy_evaluations = evaluations
            
            # Select recommended strategy
            if evaluations:
                top_eval = max(evaluations, key=lambda e: e.overall_score)
                result.recommended_strategy = next(
                    (s for s in strategies if s.strategy_id == top_eval.strategy_id),
                    None
                )
            
            # Phase 4: Implementation Planning
            result.status = WorkflowStatus.PLANNING
            plans = self._create_implementation_plans(
                problem_id,
                strategies,
                available_resources,
                constraints,
                methodology
            )
            result.implementation_plans = plans
            result.total_plans_created = len(plans)
            
            # Select recommended plan
            if result.recommended_strategy and result.recommended_strategy.strategy_id in plans:
                result.recommended_plan = plans[result.recommended_strategy.strategy_id]
            
            # Phase 5: Generate Recommendations
            recommendations = self._generate_recommendations(
                result.problem_analysis,
                result.strategies,
                result.strategy_evaluations,
                result.implementation_plans
            )
            result.recommendations = recommendations
            
            # Generate executive summary
            result.executive_summary = self._generate_executive_summary(result)
            result.key_insights = self._extract_key_insights(result)
            result.success_probability = self._calculate_success_probability(result)
            
            # Complete workflow
            result.status = WorkflowStatus.COMPLETED
            result.completed_at = datetime.now()
            result.duration_seconds = (result.completed_at - start_time).total_seconds()
            
            logger.info(f"\n✅ Workflow Completed Successfully")
            logger.info(f"   Duration: {result.duration_seconds:.2f} seconds")
            logger.info(f"   Analysis: {len(result.problem_analysis.root_causes) if result.problem_analysis else 0} root causes")
            logger.info(f"   Strategies: {len(result.strategies)} generated")
            logger.info(f"   Plans: {len(result.implementation_plans)} created")
            logger.info(f"   Recommendations: {len(result.recommendations)}")
            logger.info(f"   Success Probability: {result.success_probability:.0%}")
            
        except Exception as e:
            logger.error(f"❌ Workflow failed: {e}")
            result.status = WorkflowStatus.FAILED
            result.completed_at = datetime.now()
            result.duration_seconds = (result.completed_at - start_time).total_seconds()
            raise
        
        return result
    
    def _analyze_problem(
        self,
        problem_id: str,
        problem_title: str,
        problem_description: str,
        problem_context: Dict[str, Any]
    ) -> ComprehensiveProblemAnalysis:
        """Execute problem analysis phase."""
        logger.info(f"\n{'─'*80}")
        logger.info(f"📊 PHASE 1: Problem Analysis")
        logger.info(f"{'─'*80}")
        
        # Create analyzer
        analyzer = create_problem_analyzer()
        
        # Perform analysis
        analysis = analyzer.analyze_problem(
            problem_id=problem_id,
            problem_title=problem_title,
            problem_description=problem_description,
            context=problem_context
        )
        
        logger.info(f"✓ Analysis completed")
        logger.info(f"  Root Causes: {len(analysis.root_causes)}")
        logger.info(f"  Dependencies: {len(analysis.dependencies)}")
        logger.info(f"  Risk Factors: {len(analysis.risk_factors)}")
        logger.info(f"  Confidence: {analysis.confidence_score:.0%}")
        
        return analysis
    
    def _generate_strategies(
        self,
        problem_id: str,
        problem_title: str,
        problem_description: str,
        analysis: ComprehensiveProblemAnalysis,
        perspectives: List[PerspectiveType],
        constraints: List[str],
        success_criteria: List[str]
    ) -> List[SolutionStrategy]:
        """Execute strategy generation phase."""
        logger.info(f"\n{'─'*80}")
        logger.info(f"💡 PHASE 2: Strategy Generation")
        logger.info(f"{'─'*80}")
        logger.info(f"Generating strategies for {len(perspectives)} perspectives")
        
        strategies = []
        
        for perspective in perspectives:
            logger.info(f"\n  Generating {perspective.value} strategy...")
            
            # Create strategist for this perspective
            strategist = create_solution_strategist(perspective)
            
            # Generate strategy
            strategy = strategist.generate_strategy(
                problem_id=problem_id,
                problem_title=problem_title,
                problem_description=problem_description,
                problem_analysis={
                    "root_causes": [rc.description for rc in analysis.root_causes],
                    "key_components": [c.name for c in analysis.key_components],
                    "confidence": analysis.confidence_score
                },
                perspective=perspective,
                constraints=constraints,
                success_criteria=success_criteria
            )
            
            strategies.append(strategy)
            
            logger.info(f"  ✓ {strategy.strategy_id} created")
            logger.info(f"    Approach: {strategy.strategy_approach.value}")
            logger.info(f"    Steps: {len(strategy.key_steps)}")
            logger.info(f"    Success Probability: {strategy.success_probability:.0%}")
        
        logger.info(f"\n✓ Generated {len(strategies)} strategies")
        
        return strategies
    
    def _evaluate_strategies(
        self,
        strategies: List[SolutionStrategy]
    ) -> List[StrategyEvaluation]:
        """Execute strategy evaluation phase."""
        logger.info(f"\n{'─'*80}")
        logger.info(f"⚖️  PHASE 3: Strategy Evaluation")
        logger.info(f"{'─'*80}")
        logger.info(f"Evaluating {len(strategies)} strategies")
        
        evaluations = []
        
        for strategy in strategies:
            # Calculate evaluation scores
            feasibility = self._calculate_feasibility_score(strategy)
            impact = self._calculate_impact_score(strategy)
            cost_efficiency = self._calculate_cost_efficiency_score(strategy)
            risk = self._calculate_risk_score(strategy)
            
            # Calculate overall score (weighted average)
            overall = (
                feasibility * 0.25 +
                impact * 0.35 +
                cost_efficiency * 0.25 +
                risk * 0.15
            )
            
            # Identify strengths and weaknesses
            strengths = self._identify_strengths(strategy)
            weaknesses = self._identify_weaknesses(strategy)
            
            evaluation = StrategyEvaluation(
                strategy_id=strategy.strategy_id,
                perspective=strategy.perspective.value,
                feasibility_score=feasibility,
                impact_score=impact,
                cost_efficiency_score=cost_efficiency,
                risk_score=risk,
                overall_score=overall,
                strengths=strengths,
                weaknesses=weaknesses
            )
            
            evaluations.append(evaluation)
            
            logger.info(f"\n  {strategy.strategy_id} ({strategy.perspective.value})")
            logger.info(f"    Overall Score: {overall:.1f}/100")
            logger.info(f"    Feasibility: {feasibility:.1f} | Impact: {impact:.1f}")
            logger.info(f"    Cost Efficiency: {cost_efficiency:.1f} | Risk: {risk:.1f}")
        
        # Rank strategies
        evaluations.sort(key=lambda e: e.overall_score, reverse=True)
        for i, evaluation in enumerate(evaluations, 1):
            evaluation.rank = i
            if i == 1:
                evaluation.recommended = True
                evaluation.recommendation_reason = "Highest overall score across all evaluation criteria"
        
        logger.info(f"\n✓ Evaluation completed")
        if evaluations:
            top = evaluations[0]
            logger.info(f"  Top Strategy: {top.strategy_id} ({top.perspective})")
            logger.info(f"  Score: {top.overall_score:.1f}/100")
        
        return evaluations
    
    def _create_implementation_plans(
        self,
        problem_id: str,
        strategies: List[SolutionStrategy],
        available_resources: Dict[str, int],
        constraints: List[str],
        methodology: str
    ) -> Dict[str, ImplementationPlan]:
        """Execute implementation planning phase."""
        logger.info(f"\n{'─'*80}")
        logger.info(f"🏗️  PHASE 4: Implementation Planning")
        logger.info(f"{'─'*80}")
        logger.info(f"Creating plans for {len(strategies)} strategies")
        
        plans = {}
        specialist = create_implementation_specialist()
        
        for strategy in strategies:
            logger.info(f"\n  Creating plan for {strategy.strategy_id}...")
            
            plan = specialist.create_implementation_plan(
                problem_id=problem_id,
                strategy_id=strategy.strategy_id,
                strategy_title=strategy.title,
                strategy_steps=strategy.key_steps,
                strategy_approach=strategy.strategy_approach.value,
                estimated_timeline=strategy.estimated_timeline,
                available_resources=available_resources,
                constraints=constraints,
                methodology=methodology
            )
            
            plans[strategy.strategy_id] = plan
            
            logger.info(f"  ✓ {plan.plan_id} created")
            logger.info(f"    Duration: {plan.total_duration_days} days")
            logger.info(f"    Tasks: {len(plan.get_all_tasks())}")
            logger.info(f"    Cost: {plan.total_cost}")
        
        logger.info(f"\n✓ Created {len(plans)} implementation plans")
        
        return plans
    
    def _generate_recommendations(
        self,
        analysis: Optional[ComprehensiveProblemAnalysis],
        strategies: List[SolutionStrategy],
        evaluations: List[StrategyEvaluation],
        plans: Dict[str, ImplementationPlan]
    ) -> List[Recommendation]:
        """Generate final recommendations."""
        logger.info(f"\n{'─'*80}")
        logger.info(f"📝 PHASE 5: Generating Recommendations")
        logger.info(f"{'─'*80}")
        
        recommendations = []
        rec_id = 1
        
        # Recommendation 1: Immediate action based on top strategy
        if evaluations:
            top_eval = evaluations[0]
            top_strategy = next((s for s in strategies if s.strategy_id == top_eval.strategy_id), None)
            
            if top_strategy:
                rec = Recommendation(
                    recommendation_id=f"REC-{rec_id:03d}",
                    recommendation_type=RecommendationType.IMMEDIATE_ACTION,
                    title=f"Implement {top_strategy.perspective.value.title()} Strategy",
                    description=f"Execute the {top_strategy.title} as the primary solution approach",
                    rationale=f"Scored {top_eval.overall_score:.1f}/100 - highest across all evaluation criteria",
                    expected_impact="High - Directly addresses core problem",
                    effort_required=top_strategy.estimated_effort,
                    priority="Critical",
                    success_criteria=[
                        f"Strategy execution initiated within 1 week",
                        f"All phases completed per timeline",
                        f"Success metrics tracked and reported"
                    ]
                )
                recommendations.append(rec)
                rec_id += 1
        
        # Recommendation 2: Address critical root causes
        if analysis and analysis.root_causes:
            critical_causes = [rc for rc in analysis.root_causes 
                             if rc.impact_level in [ImpactLevel.CRITICAL, ImpactLevel.HIGH]]
            if critical_causes:
                rec = Recommendation(
                    recommendation_id=f"REC-{rec_id:03d}",
                    recommendation_type=RecommendationType.SHORT_TERM,
                    title="Address Critical Root Causes",
                    description=f"Focus on resolving {len(critical_causes)} critical root causes identified in analysis",
                    rationale="Root causes must be addressed to prevent problem recurrence",
                    expected_impact="High - Prevents future occurrences",
                    effort_required="2-4 weeks",
                    priority="High",
                    success_criteria=[
                        "Root causes validated and confirmed",
                        "Mitigation actions implemented",
                        "Effectiveness measured"
                    ]
                )
                recommendations.append(rec)
                rec_id += 1
        
        # Recommendation 3: Quick wins
        quick_win_strategies = [
            s for s in strategies
            if s.strategy_approach.value == "quick_win" or s.estimated_timeline.lower().startswith("1")
        ]
        
        if quick_win_strategies:
            rec = Recommendation(
                recommendation_id=f"REC-{rec_id:03d}",
                recommendation_type=RecommendationType.QUICK_WIN,
                title="Execute Quick Wins",
                description=f"Implement {len(quick_win_strategies)} quick win strategies for early value delivery",
                rationale="Quick wins build momentum and demonstrate progress",
                expected_impact="Medium - Immediate visible improvements",
                effort_required="1-2 weeks",
                priority="High",
                success_criteria=[
                    "Quick wins identified and prioritized",
                    "Implementation completed within 2 weeks",
                    "Value demonstrated to stakeholders"
                ]
            )
            recommendations.append(rec)
            rec_id += 1
        
        # Recommendation 4: Risk mitigation
        high_risk_strategies = [s for s in strategies if s.risk_level in ["High", "Critical"]]
        
        if high_risk_strategies:
            rec = Recommendation(
                recommendation_id=f"REC-{rec_id:03d}",
                recommendation_type=RecommendationType.RISK_MITIGATION,
                title="Implement Risk Mitigation Plans",
                description=f"Execute mitigation plans for {len(high_risk_strategies)} high-risk scenarios",
                rationale="Proactive risk management reduces likelihood of failures",
                expected_impact="High - Reduces execution risk",
                effort_required="Ongoing",
                priority="High",
                success_criteria=[
                    "Risk mitigation plans created",
                    "Mitigation actions initiated",
                    "Risk levels monitored and tracked"
                ]
            )
            recommendations.append(rec)
            rec_id += 1
        
        # Recommendation 5: Long-term improvements
        rec = Recommendation(
            recommendation_id=f"REC-{rec_id:03d}",
            recommendation_type=RecommendationType.LONG_TERM,
            title="Establish Continuous Improvement Process",
            description="Implement ongoing monitoring and optimization to prevent future issues",
            rationale="Long-term sustainability requires continuous improvement",
            expected_impact="Medium - Prevents future problems",
            effort_required="Ongoing",
            priority="Medium",
            success_criteria=[
                "Monitoring systems in place",
                "Regular review cadence established",
                "Improvement process documented"
            ]
        )
        recommendations.append(rec)
        
        logger.info(f"✓ Generated {len(recommendations)} recommendations")
        
        return recommendations
    
    def _calculate_feasibility_score(self, strategy: SolutionStrategy) -> float:
        """Calculate feasibility score for a strategy."""
        score = 50.0  # Base score
        
        # Higher confidence increases feasibility
        score += strategy.confidence_score * 20
        
        # Lower risk increases feasibility
        risk_map = {"Low": 20, "Medium": 10, "High": 0, "Critical": -10}
        score += risk_map.get(strategy.risk_level, 0)
        
        # Success probability contributes
        score += strategy.success_probability * 10
        
        # Critical assumptions reduce feasibility
        critical_assumptions = strategy.get_critical_assumptions()
        score -= len(critical_assumptions) * 2
        
        return max(0, min(100, score))
    
    def _calculate_impact_score(self, strategy: SolutionStrategy) -> float:
        """Calculate impact score for a strategy."""
        score = 50.0  # Base score
        
        # High magnitude benefits increase impact
        high_benefits = strategy.get_high_magnitude_benefits()
        score += len(high_benefits) * 10
        
        # Total benefits contribute
        score += len(strategy.benefits) * 3
        
        # Success probability contributes
        score += strategy.success_probability * 15
        
        return max(0, min(100, score))
    
    def _calculate_cost_efficiency_score(self, strategy: SolutionStrategy) -> float:
        """Calculate cost efficiency score for a strategy."""
        score = 60.0  # Base score
        
        # Parse estimated cost (rough estimation)
        cost_str = strategy.estimated_cost.lower()
        if "$" in cost_str:
            # Extract numbers and estimate
            import re
            numbers = re.findall(r'\d+', cost_str.replace(',', ''))
            if numbers:
                avg_cost = sum(int(n) for n in numbers) / len(numbers)
                # Lower cost = higher score
                if avg_cost < 50000:
                    score += 20
                elif avg_cost < 100000:
                    score += 10
                elif avg_cost > 200000:
                    score -= 10
        
        # Shorter timeline = better efficiency
        timeline_str = strategy.estimated_timeline.lower()
        if "week" in timeline_str and "1" in timeline_str:
            score += 15
        elif "month" in timeline_str and "1" in timeline_str:
            score += 10
        elif "month" in timeline_str and any(str(i) in timeline_str for i in range(3, 7)):
            score += 5
        
        return max(0, min(100, score))
    
    def _calculate_risk_score(self, strategy: SolutionStrategy) -> float:
        """Calculate risk score for a strategy (higher = lower risk)."""
        score = 50.0  # Base score
        
        # Risk level
        risk_map = {"Low": 30, "Medium": 15, "High": 0, "Critical": -20}
        score += risk_map.get(strategy.risk_level, 0)
        
        # Success probability
        score += strategy.success_probability * 20
        
        # Confidence
        score += strategy.confidence_score * 10
        
        return max(0, min(100, score))
    
    def _identify_strengths(self, strategy: SolutionStrategy) -> List[str]:
        """Identify strategy strengths."""
        strengths = []
        
        if strategy.success_probability >= 0.75:
            strengths.append("High success probability")
        
        if strategy.confidence_score >= 0.70:
            strengths.append("High confidence in approach")
        
        if strategy.risk_level == "Low":
            strengths.append("Low implementation risk")
        
        high_benefits = strategy.get_high_magnitude_benefits()
        if len(high_benefits) >= 2:
            strengths.append(f"{len(high_benefits)} high-value benefits")
        
        if len(strategy.key_steps) <= 5:
            strengths.append("Clear and concise execution plan")
        
        return strengths or ["Comprehensive approach"]
    
    def _identify_weaknesses(self, strategy: SolutionStrategy) -> List[str]:
        """Identify strategy weaknesses."""
        weaknesses = []
        
        if strategy.success_probability < 0.60:
            weaknesses.append("Lower success probability")
        
        if strategy.risk_level in ["High", "Critical"]:
            weaknesses.append(f"{strategy.risk_level} implementation risk")
        
        critical_assumptions = strategy.get_critical_assumptions()
        if len(critical_assumptions) >= 2:
            weaknesses.append(f"{len(critical_assumptions)} critical assumptions")
        
        if len(strategy.drawbacks) > len(strategy.benefits):
            weaknesses.append("More drawbacks than benefits")
        
        # Check timeline
        if "month" in strategy.estimated_timeline.lower():
            months = [i for i in range(1, 13) if str(i) in strategy.estimated_timeline]
            if months and max(months) >= 6:
                weaknesses.append("Extended timeline")
        
        return weaknesses or ["Requires careful execution"]
    
    def _generate_executive_summary(self, result: ProblemSolvingResult) -> str:
        """Generate executive summary of the workflow results."""
        summary_parts = []
        
        summary_parts.append(f"Problem: {result.problem_title}\n")
        
        if result.problem_analysis:
            summary_parts.append(
                f"Analysis identified {len(result.problem_analysis.root_causes)} root causes "
                f"with {result.problem_analysis.confidence_score:.0%} confidence.\n"
            )
        
        if result.strategies:
            summary_parts.append(
                f"Generated {len(result.strategies)} solution strategies from "
                f"{len(result.perspectives_analyzed)} perspectives.\n"
            )
        
        if result.recommended_strategy:
            summary_parts.append(
                f"Recommended Strategy: {result.recommended_strategy.title} "
                f"({result.recommended_strategy.perspective.value})\n"
                f"- Success Probability: {result.recommended_strategy.success_probability:.0%}\n"
                f"- Risk Level: {result.recommended_strategy.risk_level}\n"
                f"- Timeline: {result.recommended_strategy.estimated_timeline}\n"
            )
        
        if result.recommended_plan:
            summary_parts.append(
                f"Implementation: {result.recommended_plan.total_duration_days} days, "
                f"{len(result.recommended_plan.get_all_tasks())} tasks, "
                f"Cost: {result.recommended_plan.total_cost}\n"
            )
        
        critical_recs = result.get_critical_recommendations()
        if critical_recs:
            summary_parts.append(
                f"{len(critical_recs)} critical recommendations require immediate action.\n"
            )
        
        return "".join(summary_parts)
    
    def _extract_key_insights(self, result: ProblemSolvingResult) -> List[str]:
        """Extract key insights from the workflow results."""
        insights = []
        
        if result.problem_analysis:
            insights.append(
                f"Problem has {len(result.problem_analysis.root_causes)} root causes "
                f"and {len(result.problem_analysis.key_components)} key components"
            )
        
        if result.strategies:
            perspectives = list(set(s.perspective.value for s in result.strategies))
            insights.append(f"Analyzed from {len(perspectives)} perspectives: {', '.join(perspectives)}")
        
        if result.strategy_evaluations:
            top_eval = max(result.strategy_evaluations, key=lambda e: e.overall_score)
            insights.append(
                f"Top strategy scores {top_eval.overall_score:.0f}/100 "
                f"({top_eval.perspective} perspective)"
            )
        
        quick_wins = result.get_quick_wins()
        if quick_wins:
            insights.append(f"{len(quick_wins)} quick win opportunities identified")
        
        if result.recommended_plan:
            insights.append(
                f"Implementation requires {result.recommended_plan.total_duration_days} days "
                f"and {result.recommended_plan.total_effort_hours} hours"
            )
        
        return insights
    
    def _calculate_success_probability(self, result: ProblemSolvingResult) -> float:
        """Calculate overall success probability."""
        if not result.recommended_strategy:
            return 0.5
        
        # Base on recommended strategy's success probability
        probability = result.recommended_strategy.success_probability
        
        # Adjust based on analysis confidence
        if result.problem_analysis:
            probability = (probability + result.problem_analysis.confidence_score) / 2
        
        # Adjust based on evaluation scores
        if result.strategy_evaluations:
            top_eval = max(result.strategy_evaluations, key=lambda e: e.overall_score)
            score_factor = top_eval.overall_score / 100
            probability = (probability + score_factor) / 2
        
        return probability


def demo_problem_solving_workflow():
    """Demonstrate the problem-solving workflow."""
    print("\n" + "="*80)
    print("🚀 PROBLEM-SOLVING WORKFLOW DEMONSTRATION")
    print("="*80)
    
    # Create workflow
    workflow = ProblemSolvingWorkflow()
    
    # Define problem
    problem_title = "E-commerce Checkout Performance Issues"
    problem_description = """
    Our e-commerce platform is experiencing severe performance issues during checkout:
    - Page load times increased from 2s to 8-10s
    - 35% cart abandonment rate (up from 15%)
    - Database connection pool exhaustion
    - API timeouts during peak hours
    - Customer complaints increasing by 200%
    - Estimated revenue impact: $500K/month
    """
    
    print(f"\nProblem: {problem_title}")
    print(f"Description: {problem_description[:200]}...")
    
    # Execute workflow
    print("\nExecuting problem-solving workflow...")
    
    result = workflow.solve_problem(
        problem_title=problem_title,
        problem_description=problem_description,
        perspectives=[
            PerspectiveType.TECHNICAL,
            PerspectiveType.BUSINESS,
            PerspectiveType.USER_EXPERIENCE
        ],
        constraints=["Budget: $200K", "Timeline: 3 months", "Zero downtime"],
        success_criteria=[
            "Page load < 2 seconds",
            "Cart abandonment < 20%",
            "Zero timeouts",
            "Customer satisfaction > 90%"
        ],
        available_resources={
            "developers": 5,
            "qa": 2,
            "devops": 1
        },
        methodology="Agile"
    )
    
    # Display results
    print("\n" + "="*80)
    print("📊 WORKFLOW RESULTS")
    print("="*80)
    
    print(f"\nStatus: {result.status.value}")
    print(f"Duration: {result.duration_seconds:.2f} seconds")
    print(f"Success Probability: {result.success_probability:.0%}")
    
    print(f"\n📋 Executive Summary:")
    print(result.executive_summary)
    
    print(f"\n💡 Key Insights:")
    for insight in result.key_insights:
        print(f"  • {insight}")
    
    print(f"\n🎯 Top Strategies:")
    for i, (strategy, evaluation) in enumerate(result.get_top_strategies(3), 1):
        print(f"  {i}. {strategy.title}")
        print(f"     Score: {evaluation.overall_score:.1f}/100 | Risk: {strategy.risk_level}")
        print(f"     Success: {strategy.success_probability:.0%} | Timeline: {strategy.estimated_timeline}")
    
    print(f"\n📝 Critical Recommendations:")
    for rec in result.get_critical_recommendations():
        print(f"  • {rec.title}")
        print(f"    {rec.description}")
        print(f"    Expected Impact: {rec.expected_impact}")
    
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    demo_problem_solving_workflow()
