"""Problem-Solving Team Integration

Integrates the Problem-Solving Workflow with Team Manager for complete
framework integration.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

from .team_manager import MultiAgentTeam, TeamConfiguration
from .constants import TeamType
from .workflows.problem_solving import (
    ProblemSolvingWorkflow,
    ProblemSolvingResult,
    WorkflowStatus
)
from .roles.solution_strategist import PerspectiveType

logger = logging.getLogger(__name__)


@dataclass
class ProblemSolvingTeamConfig:
    """Configuration for a problem-solving team."""
    
    team_name: str = "Problem-Solving Team"
    perspectives: List[PerspectiveType] = None
    max_agents: int = 5
    collaboration_timeout: int = 1800  # 30 minutes
    quality_threshold: float = 0.7
    
    def __post_init__(self):
        """Initialize default perspectives if not provided."""
        if self.perspectives is None:
            self.perspectives = [
                PerspectiveType.TECHNICAL,
                PerspectiveType.BUSINESS,
                PerspectiveType.USER_EXPERIENCE
            ]


class ProblemSolvingTeamManager:
    """Manages problem-solving teams integrated with Team Manager."""
    
    def __init__(self, config: Optional[ProblemSolvingTeamConfig] = None):
        """Initialize problem-solving team manager.
        
        Args:
            config: Team configuration (uses defaults if not provided)
        """
        self.config = config or ProblemSolvingTeamConfig()
        self.workflow = ProblemSolvingWorkflow()
        self.team: Optional[MultiAgentTeam] = None
        self.active_results: Dict[str, ProblemSolvingResult] = {}
        
        logger.info(f"Initialized Problem-Solving Team Manager: {self.config.team_name}")
    
    def create_team(self) -> MultiAgentTeam:
        """Create a multi-agent team for problem-solving.
        
        Returns:
            Configured MultiAgentTeam instance
        """
        # Create team configuration
        team_config = TeamConfiguration(
            team_name=self.config.team_name,
            team_type=TeamType.PROBLEM_SOLVING,
            max_agents=self.config.max_agents,
            collaboration_timeout=self.config.collaboration_timeout,
            quality_threshold=self.config.quality_threshold
        )
        
        # Create team instance
        self.team = MultiAgentTeam(team_config)
        
        # Add problem-solving agents (using role IDs from agent_roles)
        try:
            self.team.add_agent("problem_analyzer", "problem_analyzer")
            self.team.add_agent("solution_strategist", "solution_strategist")
            self.team.add_agent("implementation_specialist", "implementation_specialist")
            
            # Initialize the team
            self.team.initialize_team()
            
            logger.info(f"Created problem-solving team: {self.team.team_id}")
            return self.team
            
        except Exception as e:
            logger.error(f"Failed to create problem-solving team: {e}")
            raise
    
    def solve_problem(
        self,
        problem_title: str,
        problem_description: str,
        context: Optional[Dict[str, Any]] = None,
        perspectives: Optional[List[PerspectiveType]] = None,
        constraints: Optional[List[str]] = None,
        success_criteria: Optional[List[str]] = None
    ) -> ProblemSolvingResult:
        """Solve a problem using the integrated workflow.
        
        Args:
            problem_title: Brief problem title
            problem_description: Detailed problem description
            context: Additional context information
            perspectives: Analysis perspectives (uses config defaults if not provided)
            constraints: Solution constraints
            success_criteria: Success criteria
            
        Returns:
            ProblemSolvingResult with complete analysis and recommendations
        """
        # Ensure team is created
        if self.team is None:
            self.create_team()
        
        # Use configured perspectives if not provided
        perspectives = perspectives or self.config.perspectives
        
        # Start collaboration in team context
        try:
            session_id = self.team.start_collaboration(
                task_description=f"Solve problem: {problem_title}",
                expected_output="Comprehensive problem analysis with solution strategies and implementation plans",
                context=context or {},
                constraints={"perspectives": [p.value for p in perspectives]}
            )
            
            logger.info(f"Started problem-solving collaboration: {session_id}")
            
            # Execute workflow
            result = self.workflow.solve_problem(
                problem_title=problem_title,
                problem_description=problem_description,
                context=context,
                perspectives=perspectives,
                constraints=constraints,
                success_criteria=success_criteria
            )
            
            # Store result
            self.active_results[session_id] = result
            
            # Update shared context with results
            if result.status == WorkflowStatus.COMPLETED:
                self.team.shared_context.set(
                    "problem_solving_result",
                    {
                        "problem_id": result.problem_id,
                        "status": result.status.value,
                        "strategies_count": len(result.strategies),
                        "recommended_strategy": result.recommended_strategy.strategy_id if result.recommended_strategy else None,
                        "success_probability": result.success_probability
                    },
                    updated_by="problem_solving_workflow"
                )
                
                # Complete collaboration
                self.team.complete_collaboration(
                    results={
                        "problem_solving_result": result,
                        "executive_summary": result.executive_summary,
                        "key_insights": result.key_insights,
                        "recommendations": [r.__dict__ for r in result.recommendations]
                    }
                )
            
            logger.info(f"Problem-solving completed: {result.problem_id}")
            return result
            
        except Exception as e:
            logger.error(f"Problem-solving failed: {e}")
            if self.team:
                self.team.fail_collaboration(str(e))
            raise
    
    def get_active_result(self, session_id: str) -> Optional[ProblemSolvingResult]:
        """Get results for an active problem-solving session.
        
        Args:
            session_id: Collaboration session ID
            
        Returns:
            ProblemSolvingResult if found, None otherwise
        """
        return self.active_results.get(session_id)
    
    def get_team_status(self) -> Dict[str, Any]:
        """Get current team status.
        
        Returns:
            Team status information
        """
        if self.team is None:
            return {
                "status": "not_created",
                "message": "Problem-solving team has not been created yet"
            }
        
        team_status = self.team.get_team_status()
        team_status["active_sessions"] = len(self.active_results)
        team_status["workflow_id"] = self.workflow.workflow_id
        
        return team_status
    
    def cleanup(self) -> None:
        """Clean up team resources."""
        if self.team:
            self.team.cleanup()
            logger.info("Cleaned up problem-solving team resources")


def create_problem_solving_team(
    team_name: str = "Problem-Solving Team",
    perspectives: Optional[List[PerspectiveType]] = None
) -> ProblemSolvingTeamManager:
    """Factory function to create a problem-solving team.
    
    Args:
        team_name: Name for the team
        perspectives: Analysis perspectives to use
        
    Returns:
        Configured ProblemSolvingTeamManager instance
    """
    config = ProblemSolvingTeamConfig(
        team_name=team_name,
        perspectives=perspectives
    )
    
    manager = ProblemSolvingTeamManager(config)
    manager.create_team()
    
    return manager


# Demo function
def demo_problem_solving_integration():
    """Demonstrate problem-solving team integration."""
    print("\n" + "="*80)
    print("🚀 PROBLEM-SOLVING TEAM INTEGRATION DEMONSTRATION")
    print("="*80)
    
    # Create problem-solving team
    print("\n1. Creating problem-solving team...")
    team_manager = create_problem_solving_team(
        team_name="E-commerce Problem-Solving Team",
        perspectives=[
            PerspectiveType.TECHNICAL,
            PerspectiveType.BUSINESS,
            PerspectiveType.USER_EXPERIENCE
        ]
    )
    
    # Check team status
    status = team_manager.get_team_status()
    print(f"   ✓ Team created: {status['team_id']}")
    print(f"   ✓ Status: {status['status']}")
    print(f"   ✓ Agents: {status['agent_count']}")
    for agent_id, agent_info in status['agents'].items():
        print(f"      - {agent_id}: {agent_info['role']}")
    
    # Solve a problem
    print("\n2. Solving e-commerce checkout problem...")
    result = team_manager.solve_problem(
        problem_title="E-commerce Checkout Performance Issues",
        problem_description="""
        Our e-commerce platform is experiencing severe performance issues during checkout:
        - Page load times increased from 2s to 8-10s
        - 35% cart abandonment rate (up from 15%)
        - Database connection pool exhaustion during peak hours
        - Payment gateway timeouts affecting 10% of transactions
        - Customer complaints about slow checkout experience
        """,
        context={
            "platform": "E-commerce",
            "impact": "High - affecting revenue",
            "urgency": "Critical"
        },
        constraints=[
            "Must maintain PCI compliance",
            "Cannot take site offline",
            "Budget limited to $150K"
        ],
        success_criteria=[
            "Reduce page load time to under 3s",
            "Decrease cart abandonment to under 20%",
            "Eliminate payment timeouts"
        ]
    )
    
    # Display results
    print(f"\n   ✓ Problem solved: {result.problem_id}")
    print(f"   ✓ Status: {result.status.value}")
    print(f"   ✓ Duration: {result.duration:.2f}s")
    print(f"   ✓ Success Probability: {result.success_probability:.0%}")
    
    print(f"\n3. Analysis Results:")
    if result.problem_analysis:
        print(f"   - Root Causes: {len(result.problem_analysis.root_causes)}")
        print(f"   - Key Components: {len(result.problem_analysis.key_components)}")
        print(f"   - Confidence: {result.problem_analysis.confidence_score:.0%}")
    
    print(f"\n4. Strategies Generated: {len(result.strategies)}")
    for i, strategy in enumerate(result.strategies, 1):
        print(f"   {i}. {strategy.strategy_name} ({strategy.perspective.value})")
        print(f"      - Success: {strategy.success_probability:.0%}")
        print(f"      - Timeline: {strategy.estimated_timeline}")
        print(f"      - Cost: ${strategy.estimated_cost_min:,} - ${strategy.estimated_cost_max:,}")
    
    print(f"\n5. Recommended Strategy:")
    if result.recommended_strategy:
        print(f"   - {result.recommended_strategy.strategy_name}")
        print(f"   - Perspective: {result.recommended_strategy.perspective.value}")
        print(f"   - Success Probability: {result.recommended_strategy.success_probability:.0%}")
    
    print(f"\n6. Implementation Plans: {len(result.implementation_plans)}")
    for plan_id, plan in result.implementation_plans.items():
        print(f"   - {plan_id}: {plan.duration_days} days, {len(plan.get_all_tasks())} tasks, ${plan.total_cost:,.0f}")
    
    print(f"\n7. Recommendations: {len(result.recommendations)}")
    for rec in result.recommendations[:3]:  # Show first 3
        print(f"   - {rec.title} ({rec.recommendation_type.value})")
        print(f"     Priority: {rec.priority}")
    
    print(f"\n8. Executive Summary:")
    print(f"   {result.executive_summary[:200]}...")
    
    # Cleanup
    print("\n9. Cleaning up...")
    team_manager.cleanup()
    print("   ✓ Resources cleaned up")
    
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    demo_problem_solving_integration()
