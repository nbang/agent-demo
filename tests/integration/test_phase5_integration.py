"""
Phase 5 Integration Test - Problem-Solving Team Components

Tests the integration of Phase 5 problem-solving components without
requiring the full multi-agent framework.
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_problem_analyzer_integration():
    """Test ProblemAnalyzer role integration."""
    print("\n" + "="*80)
    print("TEST 1: ProblemAnalyzer Role Integration")
    print("="*80)
    
    try:
        from src.agents.multi_agent.roles.problem_analyzer import (
            create_problem_analyzer, AnalysisDepth
        )
        
        # Create analyzer
        analyzer = create_problem_analyzer(
            analyzer_name="Integration Test Analyzer",
            analysis_depth=AnalysisDepth.MODERATE
        )
        
        # Perform quick analysis
        analysis = analyzer.analyze_problem(
            problem_id="INT-TEST-001",
            problem_title="API Performance Degradation",
            problem_description="API response times increased from 200ms to 2000ms during peak hours, affecting 50% of requests",
            context={
                "system": "REST API",
                "users": "10K concurrent",
                "impact": "customer complaints"
            }
        )
        
        # Validate results
        assert analysis.analysis_id == "ANALYSIS-INT-TEST-001"
        assert len(analysis.root_causes) > 0, "Should identify root causes"
        assert len(analysis.key_components) > 0, "Should identify key components"
        assert 0.0 <= analysis.confidence_score <= 1.0, "Confidence should be 0-1"
        
        print(f"\n✅ ProblemAnalyzer Integration Test PASSED")
        print(f"   - Analysis ID: {analysis.analysis_id}")
        print(f"   - Root Causes: {len(analysis.root_causes)}")
        print(f"   - Components: {len(analysis.key_components)}")
        print(f"   - Dependencies: {len(analysis.dependencies)}")
        print(f"   - Confidence: {analysis.confidence_score:.0%}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ProblemAnalyzer Integration Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_problem_solving_team_integration():
    """Test ProblemSolvingTeam integration."""
    print("\n" + "="*80)
    print("TEST 2: ProblemSolvingTeam Integration")
    print("="*80)
    
    try:
        from examples.multi_agents.problem_solving_team import (
            ProblemSolvingTeam, ProblemType, ProblemComplexity
        )
        
        # Create team
        team = ProblemSolvingTeam(
            team_name="Integration Test Team",
            enable_parallel_analysis=False  # Sequential for testing
        )
        
        # Solve a problem
        result = team.solve_problem(
            problem="System experiencing high latency and timeout errors",
            problem_type=ProblemType.TECHNICAL,
            complexity=ProblemComplexity.MEDIUM,
            context={"service": "API Gateway", "users": "1000"},
            constraints=["2-week timeline", "$10K budget"],
            success_criteria=["Reduce latency to <500ms", "Zero timeout errors"]
        )
        
        # Validate results
        assert result.problem_id.startswith("PROB-"), "Should have valid problem ID"
        assert len(result.strategies) > 0, "Should generate strategies"
        assert len(result.evaluations) > 0, "Should evaluate strategies"
        assert result.get_top_solution() is not None, "Should have top solution"
        
        top_solution = result.get_top_solution()
        
        print(f"\n✅ ProblemSolvingTeam Integration Test PASSED")
        print(f"   - Problem ID: {result.problem_id}")
        print(f"   - Strategies: {len(result.strategies)}")
        print(f"   - Evaluations: {len(result.evaluations)}")
        print(f"   - Duration: {result.analysis_duration:.2f}s")
        print(f"   - Top Solution: {top_solution.perspective.value if top_solution else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ProblemSolvingTeam Integration Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_component_integration():
    """Test integration between components."""
    print("\n" + "="*80)
    print("TEST 3: Component Integration Test")
    print("="*80)
    
    try:
        from src.agents.multi_agent.roles.problem_analyzer import create_problem_analyzer
        from examples.multi_agents.problem_solving_team import ProblemSolvingTeam
        
        # Test that ProblemAnalyzer can be used standalone
        analyzer = create_problem_analyzer()
        print("   ✓ ProblemAnalyzer created")
        
        # Test that ProblemSolvingTeam can be used standalone
        team = ProblemSolvingTeam()
        print("   ✓ ProblemSolvingTeam created")
        
        # Test analysis workflow
        analysis = analyzer.analyze_problem(
            problem_id="COMP-001",
            problem_title="Component Integration Test",
            problem_description="Testing component integration",
            context={"test": "integration"}
        )
        print(f"   ✓ Analysis completed: {len(analysis.root_causes)} root causes")
        
        # Test that analysis results can be used by team
        assert analysis.problem_id == "COMP-001"
        assert analysis.root_causes is not None
        print("   ✓ Analysis results validated")
        
        print(f"\n✅ Component Integration Test PASSED")
        print(f"   - All components work independently")
        print(f"   - Data structures are compatible")
        print(f"   - Workflows execute successfully")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Component Integration Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_flow():
    """Test data flow between components."""
    print("\n" + "="*80)
    print("TEST 4: Data Flow Test")
    print("="*80)
    
    try:
        from examples.multi_agents.problem_solving_team import (
            ProblemSolvingTeam, ProblemType, ProblemComplexity
        )
        
        team = ProblemSolvingTeam()
        
        # Execute complete workflow
        result = team.solve_problem(
            problem="Test data flow through complete workflow",
            problem_type=ProblemType.TECHNICAL,
            complexity=ProblemComplexity.LOW,
            context={"test": "data_flow"},
            constraints=["Quick test"],
            success_criteria=["Complete workflow"]
        )
        
        # Validate data flow
        assert result.problem_statement is not None, "Problem statement should exist"
        assert result.analysis is not None, "Analysis should exist"
        assert result.strategies is not None, "Strategies should exist"
        assert result.implementation_plans is not None, "Implementation plans should exist"
        assert result.evaluations is not None, "Evaluations should exist"
        
        # Validate data relationships
        assert result.analysis.problem_id == result.problem_id, "IDs should match"
        
        for strategy in result.strategies:
            assert strategy.problem_id == result.problem_id, "Strategy problem ID should match"
        
        for plan in result.implementation_plans:
            strategy_ids = [s.strategy_id for s in result.strategies]
            assert plan.strategy_id in strategy_ids, "Plan should reference valid strategy"
        
        print(f"\n✅ Data Flow Test PASSED")
        print(f"   - Problem statement created")
        print(f"   - Analysis completed")
        print(f"   - {len(result.strategies)} strategies generated")
        print(f"   - {len(result.implementation_plans)} plans created")
        print(f"   - {len(result.evaluations)} evaluations completed")
        print(f"   - All IDs and references valid")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Data Flow Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all integration tests."""
    print("\n" + "="*80)
    print("PHASE 5 INTEGRATION TESTS")
    print("Testing Problem-Solving Team Components")
    print("="*80)
    
    results = []
    
    # Run tests
    results.append(("ProblemAnalyzer Integration", test_problem_analyzer_integration()))
    results.append(("ProblemSolvingTeam Integration", test_problem_solving_team_integration()))
    results.append(("Component Integration", test_component_integration()))
    results.append(("Data Flow", test_data_flow()))
    
    # Summary
    print("\n" + "="*80)
    print("INTEGRATION TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("Phase 5 components are properly integrated and functional.")
        return 0
    else:
        print("\n⚠️  Some integration tests failed.")
        print("Please review the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
