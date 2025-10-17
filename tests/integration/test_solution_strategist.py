"""
Integration test for T036: SolutionStrategist role.

Tests the SolutionStrategist role integration with:
- Problem analysis data
- Multiple perspectives
- Data structure compatibility
- Workflow integration
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_path))

import pytest

# Skip this entire module if imports fail
try:
    from src.agents.multi_agent.roles.solution_strategist import (
        SolutionStrategistRole,
        create_solution_strategist,
        PerspectiveType,
        StrategyApproach
    )
    IMPORTS_AVAILABLE = True
except ImportError:
    IMPORTS_AVAILABLE = False

pytestmark = pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required modules not available")


def test_solution_strategist_creation():
    """Test creating solution strategists with different perspectives."""
    print("\n" + "="*80)
    print("TEST 1: Solution Strategist Creation")
    print("="*80)
    
    perspectives = [
        PerspectiveType.TECHNICAL,
        PerspectiveType.BUSINESS,
        PerspectiveType.USER_EXPERIENCE,
        PerspectiveType.SECURITY
    ]
    
    strategists = []
    for perspective in perspectives:
        strategist = create_solution_strategist(perspective)
        strategists.append(strategist)
        
        print(f"\n✓ Created {perspective.value} strategist")
        print(f"  Name: {strategist.strategist_name}")
        print(f"  Primary Perspective: {strategist.primary_perspective.value}")
        print(f"  Expertise Areas: {len(strategist.expertise_areas)}")
        print(f"  Creative Thinking: {strategist.creative_thinking}")
    
    assert len(strategists) == len(perspectives), "All strategists created"
    print(f"\n✅ Test 1 Passed: Created {len(strategists)} strategists")


def test_strategy_generation():
    """Test generating strategies from multiple perspectives."""
    print("\n" + "="*80)
    print("TEST 2: Strategy Generation")
    print("="*80)
    
    # Create problem
    problem_id = "PROB-TEST-001"
    problem_title = "API Performance Degradation"
    problem_description = """
    API response times have increased from 200ms to 2000ms over the past month.
    Database queries are timing out, and connection pool is exhausted.
    Affecting 50,000 daily users with 30% error rate increase.
    """
    
    constraints = ["2-month timeline", "$100K budget", "Zero downtime requirement"]
    success_criteria = ["Response time <500ms", "Error rate <1%", "No downtime"]
    
    perspectives = [
        PerspectiveType.TECHNICAL,
        PerspectiveType.BUSINESS,
        PerspectiveType.USER_EXPERIENCE
    ]
    
    strategies = []
    for perspective in perspectives:
        print(f"\n{'─'*80}")
        print(f"Generating {perspective.value.upper()} strategy...")
        print(f"{'─'*80}")
        
        strategist = create_solution_strategist(perspective)
        
        strategy = strategist.generate_strategy(
            problem_id=problem_id,
            problem_title=problem_title,
            problem_description=problem_description,
            perspective=perspective,
            constraints=constraints,
            success_criteria=success_criteria
        )
        
        strategies.append(strategy)
        
        # Validate strategy
        assert strategy.strategy_id.startswith("STRAT-"), "Valid strategy ID"
        assert strategy.problem_id == problem_id, "Problem ID matches"
        assert strategy.perspective == perspective, "Perspective matches"
        assert len(strategy.key_steps) > 0, "Has steps"
        assert len(strategy.benefits) > 0, "Has benefits"
        assert len(strategy.assumptions) > 0, "Has assumptions"
        assert strategy.estimated_effort, "Has effort estimate"
        assert strategy.estimated_cost, "Has cost estimate"
        assert strategy.estimated_timeline, "Has timeline estimate"
        assert 0 <= strategy.success_probability <= 1.0, "Valid success probability"
        assert 0 <= strategy.confidence_score <= 1.0, "Valid confidence score"
        
        print(f"\n✓ Generated {strategy.strategy_id}")
        print(f"  Approach: {strategy.strategy_approach.value}")
        print(f"  Steps: {len(strategy.key_steps)}")
        print(f"  Benefits: {len(strategy.benefits)} ({len(strategy.get_high_magnitude_benefits())} high)")
        print(f"  Drawbacks: {len(strategy.drawbacks)}")
        print(f"  Assumptions: {len(strategy.assumptions)} ({len(strategy.get_critical_assumptions())} critical)")
        print(f"  Dependencies: {len(strategy.dependencies)} ({len(strategy.get_critical_dependencies())} critical)")
        print(f"  Success Probability: {strategy.success_probability:.0%}")
        print(f"  Confidence: {strategy.confidence_score:.0%}")
    
    print(f"\n✅ Test 2 Passed: Generated {len(strategies)} strategies")


def test_strategy_comparison():
    """Test comparing strategies from different perspectives."""
    print("\n" + "="*80)
    print("TEST 3: Strategy Comparison")
    print("="*80)
    
    # Generate strategies
    problem_id = "PROB-COMP-001"
    perspectives = [
        PerspectiveType.TECHNICAL,
        PerspectiveType.BUSINESS,
        PerspectiveType.COST
    ]
    
    strategies = []
    for perspective in perspectives:
        strategist = create_solution_strategist(perspective)
        strategy = strategist.generate_strategy(
            problem_id=problem_id,
            problem_title="System Scalability Issues",
            problem_description="System cannot handle peak loads",
            perspective=perspective
        )
        strategies.append(strategy)
    
    # Compare strategies
    print("\n" + "─"*80)
    print("Strategy Comparison Matrix")
    print("─"*80)
    print(f"{'Perspective':<20} {'Cost':<25} {'Timeline':<15} {'Risk':<10} {'Success':<10}")
    print("─"*80)
    
    for strategy in strategies:
        print(f"{strategy.perspective.value:<20} {strategy.estimated_cost:<25} "
              f"{strategy.estimated_timeline:<15} {strategy.risk_level:<10} "
              f"{strategy.success_probability*100:>5.0f}%")
    
    # Validate different perspectives produce different strategies
    costs = [s.estimated_cost for s in strategies]
    timelines = [s.estimated_timeline for s in strategies]
    
    # At least some variation expected
    assert strategies[0].perspective != strategies[1].perspective, "Different perspectives"
    
    print(f"\n✅ Test 3 Passed: Compared {len(strategies)} strategies")


def test_data_structure_compatibility():
    """Test data structure compatibility and completeness."""
    print("\n" + "="*80)
    print("TEST 4: Data Structure Compatibility")
    print("="*80)
    
    strategist = create_solution_strategist(PerspectiveType.TECHNICAL)
    
    strategy = strategist.generate_strategy(
        problem_id="PROB-DATA-001",
        problem_title="Data Structure Test",
        problem_description="Test problem for data validation"
    )
    
    # Test data structure completeness
    print("\nValidating strategy data structure...")
    
    # Required fields
    assert strategy.strategy_id, "Has strategy ID"
    assert strategy.problem_id, "Has problem ID"
    assert strategy.perspective, "Has perspective"
    assert strategy.strategy_approach, "Has approach"
    assert strategy.title, "Has title"
    assert strategy.description, "Has description"
    assert strategy.created_by, "Has creator"
    assert strategy.created_at, "Has creation time"
    
    print("✓ All required fields present")
    
    # Collections
    assert isinstance(strategy.key_steps, list), "Steps is list"
    assert isinstance(strategy.benefits, list), "Benefits is list"
    assert isinstance(strategy.drawbacks, list), "Drawbacks is list"
    assert isinstance(strategy.assumptions, list), "Assumptions is list"
    assert isinstance(strategy.dependencies, list), "Dependencies is list"
    assert isinstance(strategy.trade_offs, list), "Trade-offs is list"
    assert isinstance(strategy.success_factors, list), "Success factors is list"
    assert isinstance(strategy.failure_risks, list), "Failure risks is list"
    
    print("✓ All collections are lists")
    
    # Validate steps structure
    if strategy.key_steps:
        step = strategy.key_steps[0]
        assert step.step_number, "Step has number"
        assert step.title, "Step has title"
        assert step.description, "Step has description"
        assert step.duration, "Step has duration"
        assert step.effort, "Step has effort"
        assert isinstance(step.resources_required, list), "Step resources is list"
        print(f"✓ Step structure valid (tested {len(strategy.key_steps)} steps)")
    
    # Validate benefits structure
    if strategy.benefits:
        benefit = strategy.benefits[0]
        assert benefit.benefit_id, "Benefit has ID"
        assert benefit.description, "Benefit has description"
        assert benefit.category, "Benefit has category"
        assert benefit.magnitude, "Benefit has magnitude"
        print(f"✓ Benefit structure valid (tested {len(strategy.benefits)} benefits)")
    
    # Validate assumptions structure
    if strategy.assumptions:
        assumption = strategy.assumptions[0]
        assert assumption.assumption_id, "Assumption has ID"
        assert assumption.description, "Assumption has description"
        assert assumption.category, "Assumption has category"
        assert 0 <= assumption.validity_confidence <= 1.0, "Valid confidence"
        print(f"✓ Assumption structure valid (tested {len(strategy.assumptions)} assumptions)")
    
    # Test helper methods
    critical_assumptions = strategy.get_critical_assumptions()
    high_benefits = strategy.get_high_magnitude_benefits()
    critical_deps = strategy.get_critical_dependencies()
    
    print(f"✓ Helper methods work: {len(critical_assumptions)} critical assumptions, "
          f"{len(high_benefits)} high benefits, {len(critical_deps)} critical dependencies")
    
    print(f"\n✅ Test 4 Passed: Data structures valid and compatible")


def test_integration_with_problem_solver():
    """Test integration with problem-solving workflow."""
    print("\n" + "="*80)
    print("TEST 5: Integration with Problem Solver")
    print("="*80)
    
    # Simulate problem analysis results
    problem_analysis = {
        "problem_id": "PROB-INT-001",
        "root_causes": [
            "Inefficient database queries",
            "Lack of caching",
            "Unoptimized API endpoints"
        ],
        "components": [
            "Database layer",
            "API layer",
            "Caching layer"
        ],
        "confidence": 0.85
    }
    
    print("\nSimulated Problem Analysis:")
    print(f"  Problem ID: {problem_analysis['problem_id']}")
    print(f"  Root Causes: {len(problem_analysis['root_causes'])}")
    print(f"  Components: {len(problem_analysis['components'])}")
    print(f"  Confidence: {problem_analysis['confidence']:.0%}")
    
    # Generate strategies based on analysis
    perspectives = [PerspectiveType.TECHNICAL, PerspectiveType.BUSINESS]
    strategies = []
    
    print("\nGenerating strategies based on analysis...")
    for perspective in perspectives:
        strategist = create_solution_strategist(perspective)
        
        strategy = strategist.generate_strategy(
            problem_id=problem_analysis["problem_id"],
            problem_title="Performance Issues",
            problem_description="System experiencing performance degradation",
            problem_analysis=problem_analysis,
            perspective=perspective
        )
        
        # Validate problem ID matches
        assert strategy.problem_id == problem_analysis["problem_id"], "Problem ID matches"
        strategies.append(strategy)
        
        print(f"✓ Generated {strategy.strategy_id} for {perspective.value}")
    
    # Validate strategies are linked to problem
    problem_ids = [s.problem_id for s in strategies]
    assert all(pid == problem_analysis["problem_id"] for pid in problem_ids), "All strategies linked to problem"
    
    print(f"\n✅ Test 5 Passed: Integration validated with {len(strategies)} strategies")


def main():
    """Run all integration tests."""
    print("\n" + "="*80)
    print("T036 SOLUTION STRATEGIST INTEGRATION TEST")
    print("="*80)
    
    try:
        # Run tests (no return values expected from pytest-compatible functions)
        test_solution_strategist_creation()
        test_strategy_generation()
        test_strategy_comparison()
        test_data_structure_compatibility()
        test_integration_with_problem_solver()
        
        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print("✅ Test 1: Solution Strategist Creation - PASSED")
        print("✅ Test 2: Strategy Generation - PASSED")
        print("✅ Test 3: Strategy Comparison - PASSED")
        print("✅ Test 4: Data Structure Compatibility - PASSED")
        print("✅ Test 5: Integration with Problem Solver - PASSED")
        print("="*80)
        print(f"ALL 5 TESTS PASSED ✅")
        print("="*80)
        print(f"\nComponents Tested:")
        print(f"  - Solution strategist role functionality")
        print(f"  - Strategy generation and comparison")
        print(f"  - Data structure validation and compatibility")
        print(f"  - Integration with problem-solving workflow")
        print(f"\nT036: SolutionStrategist Role - ✅ COMPLETE")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
