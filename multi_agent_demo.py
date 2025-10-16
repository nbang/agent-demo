"""Multi-Agent Collaboration System Demo

Entry point for demonstrating multi-agent collaboration capabilities.
"""

import asyncio
import sys
import io
from pathlib import Path
from typing import Dict, Any, Optional

# Set UTF-8 encoding for console output (Windows compatibility)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents.multi_agent import MultiAgentTeam, TeamConfiguration
from agents.multi_agent.constants import TeamType
from agents.multi_agent.logging_config import setup_multi_agent_logging


def create_research_team(topic: str) -> MultiAgentTeam:
    """Create a research team for the given topic.
    
    Args:
        topic: Research topic
        
    Returns:
        Configured MultiAgentTeam instance
    """
    config = TeamConfiguration(
        team_name=f"Research Team - {topic}",
        team_type=TeamType.RESEARCH,
        max_agents=3,
        collaboration_timeout=300,  # 5 minutes
        quality_threshold=0.8
    )
    
    team = MultiAgentTeam(config)
    
    # Add specialized agents
    team.add_agent("researcher_001", "researcher")
    team.add_agent("analyst_001", "analyst") 
    team.add_agent("synthesizer_001", "synthesizer")
    
    # Initialize team
    team.initialize_team()
    
    return team


def create_content_team(content_type: str, audience: str) -> MultiAgentTeam:
    """Create a content creation team.
    
    Args:
        content_type: Type of content to create
        audience: Target audience
        
    Returns:
        Configured MultiAgentTeam instance
    """
    config = TeamConfiguration(
        team_name=f"Content Team - {content_type}",
        team_type=TeamType.CONTENT_CREATION,
        max_agents=3,
        collaboration_timeout=300,
        quality_threshold=0.8
    )
    
    team = MultiAgentTeam(config)
    
    # Add specialized agents
    team.add_agent("writer_001", "writer")
    team.add_agent("editor_001", "editor")
    team.add_agent("reviewer_001", "reviewer")
    
    # Initialize team
    team.initialize_team()
    
    return team


def create_problem_solving_team(problem_domain: str) -> MultiAgentTeam:
    """Create a problem-solving team.
    
    Args:
        problem_domain: Domain of the problem
        
    Returns:
        Configured MultiAgentTeam instance
    """
    config = TeamConfiguration(
        team_name=f"Problem Solving Team - {problem_domain}",
        team_type=TeamType.PROBLEM_SOLVING,
        max_agents=3,
        collaboration_timeout=300,
        quality_threshold=0.8
    )
    
    team = MultiAgentTeam(config)
    
    # Add specialized agents
    team.add_agent("analyzer_001", "problem_analyzer")
    team.add_agent("strategist_001", "solution_strategist")
    team.add_agent("implementer_001", "implementation_specialist")
    
    # Initialize team
    team.initialize_team()
    
    return team


def demo_research_collaboration():
    """Demonstrate research team collaboration."""
    print("\\n" + "="*60)
    print("RESEARCH TEAM COLLABORATION DEMO")
    print("="*60)
    
    # Create research team
    topic = "Impact of AI on Healthcare"
    print(f"Creating research team for topic: {topic}")
    
    team = create_research_team(topic)
    print(f"Team created: {team.team_id}")
    print(f"Team status: {team.get_team_status()}")
    
    # Start collaboration
    collaboration_id = team.start_collaboration(
        task_description=f"Research and analyze the {topic}",
        expected_output="Comprehensive research report with sources, analysis, and conclusions",
        context={"research_depth": "comprehensive", "source_requirements": "academic and industry"}
    )
    
    print(f"\\nStarted collaboration: {collaboration_id}")
    
    try:
        # Execute collaboration (this would use real Agno agents in practice)
        print("Executing collaboration...")
        results = team.execute_collaboration()
        
        print("\\nCollaboration Results:")
        print(f"- Success: {results['success']}")
        print(f"- Execution time: {results['execution_time']:.2f} seconds")
        print(f"- Agents involved: {', '.join(results['agents_involved'])}")
        
        return results
        
    except Exception as e:
        print(f"Collaboration failed: {e}")
        return None
    
    finally:
        team.cleanup()


def demo_content_creation():
    """Demonstrate content creation team collaboration."""
    print("\\n" + "="*60)
    print("CONTENT CREATION TEAM DEMO")
    print("="*60)
    
    # Create content team
    content_type = "Blog Post"
    audience = "Software Developers"
    print(f"Creating content team for: {content_type} targeting {audience}")
    
    team = create_content_team(content_type, audience)
    print(f"Team created: {team.team_id}")
    
    # Start collaboration
    collaboration_id = team.start_collaboration(
        task_description=f"Create a {content_type} about API best practices for {audience}",
        expected_output="Well-structured, engaging blog post with examples and actionable advice",
        context={"tone": "professional but approachable", "length": "1500-2000 words"}
    )
    
    print(f"\\nStarted collaboration: {collaboration_id}")
    
    try:
        print("Executing collaboration...")
        results = team.execute_collaboration()
        
        print("\\nCollaboration Results:")
        print(f"- Success: {results['success']}")
        print(f"- Execution time: {results['execution_time']:.2f} seconds")
        print(f"- Agents involved: {', '.join(results['agents_involved'])}")
        
        return results
        
    except Exception as e:
        print(f"Collaboration failed: {e}")
        return None
    
    finally:
        team.cleanup()


def demo_problem_solving():
    """Demonstrate problem-solving team collaboration."""
    print("\\n" + "="*60)
    print("PROBLEM-SOLVING TEAM DEMO")
    print("="*60)
    
    # Import the new standalone ProblemSolvingTeam
    try:
        from examples.multi_agents.problem_solving_team import (
            ProblemSolvingTeam, ProblemType, ProblemComplexity
        )
        
        print("Using standalone ProblemSolvingTeam implementation...")
        
        # Create problem-solving team
        team = ProblemSolvingTeam(
            team_name="Customer Retention Problem Solving Team",
            enable_parallel_analysis=True
        )
        
        # Define the problem
        problem = """
        Our SaaS company is experiencing high customer churn rate of 8% monthly.
        We need to reduce it to 6% (25% reduction) to improve revenue retention
        and customer lifetime value.
        
        Current situation:
        - Monthly churn: 8%
        - Customer base: 5,000 active customers
        - Average customer lifetime: 12.5 months
        - Lost revenue: $200K/month from churned customers
        
        Key observations:
        - 60% of churned customers cite product complexity
        - 25% leave due to pricing concerns
        - 15% switch to competitors
        
        Constraints:
        - Cannot reduce pricing more than 15%
        - Must maintain profitability
        - Solution needed within 6 months
        """
        
        context = {
            "industry": "SaaS",
            "current_churn_rate": "8%",
            "target_churn_rate": "6%",
            "customer_base": "5,000 customers",
            "revenue_impact": "$200K/month loss"
        }
        
        constraints = [
            "Cannot reduce pricing more than 15%",
            "Must maintain profitability",
            "6-month implementation timeline"
        ]
        
        success_criteria = [
            "Reduce churn from 8% to 6%",
            "Improve customer satisfaction scores",
            "Maintain or improve profit margins",
            "Scalable solution for growth"
        ]
        
        # Solve the problem
        import time
        start_time = time.time()
        
        result = team.solve_problem(
            problem=problem,
            problem_type=ProblemType.BUSINESS,
            complexity=ProblemComplexity.HIGH,
            context=context,
            constraints=constraints,
            success_criteria=success_criteria
        )
        
        execution_time = time.time() - start_time
        
        print("\\n" + "="*60)
        print("COLLABORATION RESULTS")
        print("="*60)
        print(f"- Success: ✅ TRUE")
        print(f"- Execution time: {execution_time:.2f} seconds")
        print(f"- Analysis Duration: {result.analysis_duration:.2f}s")
        print(f"- Strategies Generated: {len(result.strategies)}")
        print(f"- Team Members: {', '.join(result.team_members)}")
        print(f"- Perspectives Analyzed: {result.total_perspectives}")
        
        # Show top solution
        top_solution = result.get_top_solution()
        if top_solution:
            print(f"\\n📊 TOP RECOMMENDATION:")
            print(f"   Perspective: {top_solution.perspective.value.upper()}")
            print(f"   Approach: {top_solution.approach}")
            print(f"   Timeline: {top_solution.estimated_timeline}")
            print(f"   Cost: {top_solution.estimated_cost}")
            print(f"   Success Probability: {top_solution.success_probability:.0%}")
        
        return {
            'success': True,
            'execution_time': execution_time,
            'agents_involved': result.team_members,
            'strategies_count': len(result.strategies),
            'confidence': result.analysis.confidence_score
        }
        
    except ImportError as e:
        print(f"Warning: Could not import ProblemSolvingTeam: {e}")
        print("Falling back to framework-based implementation...")
        
        # Fallback to framework-based implementation
        problem_domain = "Customer Retention"
        print(f"Creating problem-solving team for domain: {problem_domain}")
        
        team = create_problem_solving_team(problem_domain)
        print(f"Team created: {team.team_id}")
        
        # Start collaboration
        collaboration_id = team.start_collaboration(
            task_description="Analyze and solve the problem of reducing customer churn by 25%",
            expected_output="Comprehensive solution with analysis, strategy, and implementation plan",
            context={"industry": "SaaS", "current_churn_rate": "8%", "target_churn_rate": "6%"}
        )
        
        print(f"\\nStarted collaboration: {collaboration_id}")
        
        try:
            print("Executing collaboration...")
            results = team.execute_collaboration()
            
            print("\\nCollaboration Results:")
            print(f"- Success: {results['success']}")
            print(f"- Execution time: {results['execution_time']:.2f} seconds")
            print(f"- Agents involved: {', '.join(results['agents_involved'])}")
            
            return results
            
        except Exception as e:
            print(f"Collaboration failed: {e}")
            return None
        
        finally:
            team.cleanup()
    
    except Exception as e:
        print(f"Problem-solving demo failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main demo function."""
    print("Multi-Agent Collaboration System Demo")
    print("====================================")
    
    # Set up logging
    logger = setup_multi_agent_logging(log_level="INFO")
    
    try:
        # Test Phase 5 components first
        print("\\n" + "="*60)
        print("PHASE 5 INTEGRATION TEST")
        print("="*60)
        
        # Test ProblemAnalyzer standalone
        try:
            from agents.multi_agent.roles.problem_analyzer import (
                create_problem_analyzer, AnalysisDepth
            )
            
            print("\\n✅ ProblemAnalyzer role loaded successfully")
            
            analyzer = create_problem_analyzer(
                analyzer_name="Integration Test Analyzer",
                analysis_depth=AnalysisDepth.MODERATE
            )
            
            # Quick analysis test
            analysis = analyzer.analyze_problem(
                problem_id="TEST-001",
                problem_title="Integration Test Problem",
                problem_description="Testing problem analyzer integration with performance issues",
                context={"test": "integration"}
            )
            
            print(f"   - Analysis completed: {analysis.analysis_id}")
            print(f"   - Root causes found: {len(analysis.root_causes)}")
            print(f"   - Confidence: {analysis.confidence_score:.0%}")
            print("   ✅ ProblemAnalyzer integration test PASSED")
            
        except Exception as e:
            print(f"   ❌ ProblemAnalyzer integration test FAILED: {e}")
        
        # Run demonstrations
        print("\\n" + "="*60)
        print("RUNNING TEAM DEMONSTRATIONS")
        print("="*60)
        
        research_results = demo_research_collaboration()
        content_results = demo_content_creation()
        problem_results = demo_problem_solving()
        
        # Summary
        print("\\n" + "="*60)
        print("DEMO SUMMARY")
        print("="*60)
        
        demos = [
            ("Research Team", research_results),
            ("Content Creation Team", content_results),
            ("Problem-Solving Team", problem_results)
        ]
        
        for demo_name, results in demos:
            if results and results.get('success'):
                print(f"✅ {demo_name}: SUCCESS ({results['execution_time']:.2f}s)")
            else:
                print(f"❌ {demo_name}: FAILED")
        
        print("\\nDemo completed!")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"Demo failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)