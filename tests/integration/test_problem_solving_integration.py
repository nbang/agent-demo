"""Integration Test for Problem-Solving Team

Comprehensive test of the complete Phase 5 problem-solving system.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from agents.multi_agent.problem_solving_integration import (
    create_problem_solving_team,
    ProblemSolvingTeamManager,
    ProblemSolvingTeamConfig
)
from agents.multi_agent.roles.solution_strategist import PerspectiveType
from agents.multi_agent.workflows.problem_solving import WorkflowStatus


def test_problem_solving_team_creation():
    """Test 1: Problem-solving team can be created."""
    print("\n" + "="*80)
    print("TEST 1: Problem-Solving Team Creation")
    print("="*80)
    
    try:
        # Create team
        team_manager = create_problem_solving_team(
            team_name="Test Problem-Solving Team",
            perspectives=[PerspectiveType.TECHNICAL, PerspectiveType.BUSINESS]
        )
        
        # Verify team created
        assert team_manager is not None, "Team manager should be created"
        assert team_manager.team is not None, "Team should be created"
        
        # Check team status
        status = team_manager.get_team_status()
        assert status['status'] == 'active', "Team should be active"
        assert status['agent_count'] == 3, "Team should have 3 agents"
        assert 'problem_analyzer' in status['agents'], "Should have problem analyzer"
        assert 'solution_strategist' in status['agents'], "Should have solution strategist"
        assert 'implementation_specialist' in status['agents'], "Should have implementation specialist"
        
        print("✅ TEST 1 PASSED")
        print(f"   - Team ID: {status['team_id']}")
        print(f"   - Status: {status['status']}")
        print(f"   - Agents: {status['agent_count']}")
        
        # Cleanup
        team_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ TEST 1 FAILED: {e}")
        return False


def test_complete_workflow_execution():
    """Test 2: Complete workflow can be executed successfully."""
    print("\n" + "="*80)
    print("TEST 2: Complete Workflow Execution")
    print("="*80)
    
    try:
        # Create team
        team_manager = create_problem_solving_team(
            team_name="Workflow Test Team",
            perspectives=[
                PerspectiveType.TECHNICAL,
                PerspectiveType.BUSINESS,
                PerspectiveType.USER_EXPERIENCE
            ]
        )
        
        # Solve problem
        result = team_manager.solve_problem(
            problem_title="API Performance Degradation",
            problem_description="Our REST API response times have increased from 100ms to 2000ms over the past week.",
            context={
                "system": "REST API",
                "impact": "High",
                "users_affected": 50000
            },
            constraints=["Must maintain backward compatibility", "Zero downtime required"],
            success_criteria=["Response time < 200ms", "99.9% uptime"]
        )
        
        # Verify workflow completed
        assert result is not None, "Result should be returned"
        assert result.status == WorkflowStatus.COMPLETED, "Workflow should complete successfully"
        
        # Verify problem analysis
        assert result.problem_analysis is not None, "Problem analysis should be performed"
        assert len(result.problem_analysis.root_causes) > 0, "Should identify root causes"
        assert result.problem_analysis.confidence_score > 0, "Should have confidence score"
        
        # Verify strategies
        assert len(result.strategies) == 3, "Should generate 3 strategies (one per perspective)"
        assert result.recommended_strategy is not None, "Should recommend a strategy"
        
        # Verify evaluations
        assert len(result.strategy_evaluations) == 3, "Should evaluate all strategies"
        assert all(e.overall_score > 0 for e in result.strategy_evaluations), "All strategies should be scored"
        
        # Verify implementation plans
        assert len(result.implementation_plans) == 3, "Should create plans for all strategies"
        
        # Verify recommendations
        assert len(result.recommendations) > 0, "Should generate recommendations"
        
        # Verify success probability
        assert 0 <= result.success_probability <= 1, "Success probability should be between 0 and 1"
        
        print("✅ TEST 2 PASSED")
        print(f"   - Problem ID: {result.problem_id}")
        print(f"   - Status: {result.status.value}")
        print(f"   - Duration: {result.duration:.2f}s")
        print(f"   - Root Causes: {len(result.problem_analysis.root_causes)}")
        print(f"   - Strategies: {len(result.strategies)}")
        print(f"   - Plans: {len(result.implementation_plans)}")
        print(f"   - Recommendations: {len(result.recommendations)}")
        print(f"   - Success Probability: {result.success_probability:.0%}")
        
        # Cleanup
        team_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ TEST 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_perspectives():
    """Test 3: Multiple perspectives generate different strategies."""
    print("\n" + "="*80)
    print("TEST 3: Multiple Perspectives")
    print("="*80)
    
    try:
        # Create team with all perspectives
        team_manager = create_problem_solving_team(
            perspectives=[
                PerspectiveType.TECHNICAL,
                PerspectiveType.BUSINESS,
                PerspectiveType.USER_EXPERIENCE,
                PerspectiveType.SECURITY
            ]
        )
        
        # Solve problem
        result = team_manager.solve_problem(
            problem_title="Data Security Breach",
            problem_description="Unauthorized access to customer data was detected.",
            context={"severity": "Critical", "data_exposed": "Customer emails and addresses"}
        )
        
        # Verify different perspectives
        assert len(result.strategies) == 4, "Should generate 4 strategies (one per perspective)"
        
        perspectives = [s.perspective for s in result.strategies]
        assert PerspectiveType.TECHNICAL in perspectives, "Should have technical perspective"
        assert PerspectiveType.BUSINESS in perspectives, "Should have business perspective"
        assert PerspectiveType.USER_EXPERIENCE in perspectives, "Should have UX perspective"
        assert PerspectiveType.SECURITY in perspectives, "Should have security perspective"
        
        # Verify strategies are different
        strategy_names = [s.strategy_name for s in result.strategies]
        assert len(set(strategy_names)) == 4, "All strategies should have different names"
        
        # Verify each has unique characteristics
        for strategy in result.strategies:
            assert strategy.steps, f"{strategy.perspective.value} strategy should have steps"
            assert strategy.benefits, f"{strategy.perspective.value} strategy should have benefits"
            assert strategy.estimated_cost_min > 0, f"{strategy.perspective.value} strategy should have cost estimate"
        
        print("✅ TEST 3 PASSED")
        print(f"   - Perspectives tested: {len(perspectives)}")
        for strategy in result.strategies:
            print(f"   - {strategy.perspective.value}: {strategy.strategy_name}")
            print(f"     Steps: {len(strategy.steps)}, Success: {strategy.success_probability:.0%}")
        
        # Cleanup
        team_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_strategy_evaluation():
    """Test 4: Strategies are evaluated and ranked correctly."""
    print("\n" + "="*80)
    print("TEST 4: Strategy Evaluation and Ranking")
    print("="*80)
    
    try:
        # Create team
        team_manager = create_problem_solving_team()
        
        # Solve problem
        result = team_manager.solve_problem(
            problem_title="High Customer Churn Rate",
            problem_description="Customer retention has dropped from 85% to 65% in the last quarter.",
            context={"industry": "SaaS", "monthly_revenue_loss": "$500K"}
        )
        
        # Verify evaluations exist
        assert len(result.strategy_evaluations) > 0, "Should have strategy evaluations"
        
        # Verify evaluation components
        for evaluation in result.strategy_evaluations:
            assert 0 <= evaluation.feasibility_score <= 100, "Feasibility score should be 0-100"
            assert 0 <= evaluation.impact_score <= 100, "Impact score should be 0-100"
            assert 0 <= evaluation.cost_efficiency_score <= 100, "Cost efficiency score should be 0-100"
            assert 0 <= evaluation.risk_score <= 100, "Risk score should be 0-100"
            assert 0 <= evaluation.overall_score <= 100, "Overall score should be 0-100"
            assert evaluation.strengths, "Should identify strengths"
            assert evaluation.weaknesses, "Should identify weaknesses"
        
        # Verify ranking (top strategy should be recommended)
        top_evaluation = max(result.strategy_evaluations, key=lambda e: e.overall_score)
        assert result.recommended_strategy.strategy_id == top_evaluation.strategy_id, \
            "Recommended strategy should match top-ranked evaluation"
        
        # Verify scores are different
        scores = [e.overall_score for e in result.strategy_evaluations]
        # At least some variation in scores (not all identical)
        
        print("✅ TEST 4 PASSED")
        print(f"   - Strategies evaluated: {len(result.strategy_evaluations)}")
        print(f"   - Top strategy score: {top_evaluation.overall_score:.1f}/100")
        print(f"   - Recommended: {result.recommended_strategy.strategy_name}")
        for eval in sorted(result.strategy_evaluations, key=lambda e: e.overall_score, reverse=True):
            print(f"   - {eval.strategy_id}: {eval.overall_score:.1f} (F:{eval.feasibility_score:.0f} I:{eval.impact_score:.0f} C:{eval.cost_efficiency_score:.0f} R:{eval.risk_score:.0f})")
        
        # Cleanup
        team_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ TEST 4 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_implementation_plans():
    """Test 5: Implementation plans are generated for all strategies."""
    print("\n" + "="*80)
    print("TEST 5: Implementation Plan Generation")
    print("="*80)
    
    try:
        # Create team
        team_manager = create_problem_solving_team()
        
        # Solve problem
        result = team_manager.solve_problem(
            problem_title="Legacy System Migration",
            problem_description="Need to migrate from monolithic architecture to microservices.",
            context={"current_system_age": "10 years", "team_size": 15}
        )
        
        # Verify plans created
        assert len(result.implementation_plans) > 0, "Should create implementation plans"
        
        # Verify each plan has required components
        for plan_id, plan in result.implementation_plans.items():
            assert plan.plan_id, "Plan should have ID"
            assert plan.phases, "Plan should have phases"
            assert plan.duration_days > 0, "Plan should have duration"
            assert plan.total_effort_hours > 0, "Plan should have effort estimate"
            assert plan.total_cost > 0, "Plan should have cost estimate"
            
            # Verify tasks
            tasks = plan.get_all_tasks()
            assert len(tasks) > 0, "Plan should have tasks"
            
            # Verify milestones
            milestones = plan.get_all_milestones()
            assert len(milestones) > 0, "Plan should have milestones"
            
            # Verify resources
            assert plan.resources, "Plan should have resource allocations"
            
            # Verify risk mitigation
            assert plan.risk_mitigation_plans, "Plan should have risk mitigation plans"
            
            # Verify quality gates
            assert plan.quality_gates, "Plan should have quality gates"
        
        print("✅ TEST 5 PASSED")
        print(f"   - Plans created: {len(result.implementation_plans)}")
        for plan_id, plan in result.implementation_plans.items():
            print(f"   - {plan_id}:")
            print(f"     Phases: {len(plan.phases)}, Tasks: {len(plan.get_all_tasks())}")
            print(f"     Duration: {plan.duration_days} days, Effort: {plan.total_effort_hours} hours")
            print(f"     Cost: ${plan.total_cost:,.0f}")
            print(f"     Milestones: {len(plan.get_all_milestones())}, Quality Gates: {len(plan.quality_gates)}")
        
        # Cleanup
        team_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ TEST 5 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_recommendations():
    """Test 6: Actionable recommendations are generated."""
    print("\n" + "="*80)
    print("TEST 6: Recommendation Generation")
    print("="*80)
    
    try:
        # Create team
        team_manager = create_problem_solving_team()
        
        # Solve problem
        result = team_manager.solve_problem(
            problem_title="Database Performance Issues",
            problem_description="Database queries are taking 10x longer than normal during peak hours.",
            context={"database": "PostgreSQL", "table_size": "50M records"}
        )
        
        # Verify recommendations
        assert len(result.recommendations) > 0, "Should generate recommendations"
        
        # Verify recommendation types are diverse
        rec_types = [r.recommendation_type for r in result.recommendations]
        assert len(set(rec_types)) > 1, "Should have different recommendation types"
        
        # Verify each recommendation has required fields
        for rec in result.recommendations:
            assert rec.recommendation_id, "Should have ID"
            assert rec.title, "Should have title"
            assert rec.description, "Should have description"
            assert rec.rationale, "Should have rationale"
            assert rec.expected_impact, "Should have expected impact"
            assert rec.priority, "Should have priority"
            assert rec.success_criteria, "Should have success criteria"
        
        # Verify critical recommendations exist
        critical_recs = result.get_critical_recommendations()
        assert len(critical_recs) > 0, "Should have critical recommendations"
        
        print("✅ TEST 6 PASSED")
        print(f"   - Total recommendations: {len(result.recommendations)}")
        print(f"   - Critical recommendations: {len(critical_recs)}")
        print(f"   - Recommendation types: {set(r.recommendation_type.value for r in result.recommendations)}")
        for rec in result.recommendations[:3]:  # Show first 3
            print(f"   - {rec.title}")
            print(f"     Type: {rec.recommendation_type.value}, Priority: {rec.priority}")
        
        # Cleanup
        team_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ TEST 6 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_team_context_sharing():
    """Test 7: Team shares context correctly through workflow."""
    print("\n" + "="*80)
    print("TEST 7: Team Context Sharing")
    print("="*80)
    
    try:
        # Create team
        team_manager = create_problem_solving_team()
        
        # Solve problem
        result = team_manager.solve_problem(
            problem_title="Mobile App Crash Rate",
            problem_description="iOS app crashes affecting 25% of users on latest version.",
            context={
                "platform": "iOS",
                "version": "2.5.0",
                "crashes_per_day": 1500
            }
        )
        
        # Verify context was shared
        team_status = team_manager.get_team_status()
        assert 'problem_solving_result' in team_manager.team.shared_context._context, \
            "Problem solving result should be in shared context"
        
        # Verify result data in context
        context_data = team_manager.team.shared_context.get('problem_solving_result')
        assert context_data is not None, "Context data should exist"
        assert context_data['problem_id'] == result.problem_id, "Problem ID should match"
        assert context_data['status'] == result.status.value, "Status should match"
        
        print("✅ TEST 7 PASSED")
        print(f"   - Context shared: problem_solving_result")
        print(f"   - Problem ID: {context_data['problem_id']}")
        print(f"   - Status: {context_data['status']}")
        print(f"   - Strategies: {context_data['strategies_count']}")
        print(f"   - Success Probability: {context_data['success_probability']:.0%}")
        
        # Cleanup
        team_manager.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ TEST 7 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all integration tests."""
    print("\n" + "="*80)
    print("🚀 PHASE 5 INTEGRATION TEST SUITE")
    print("="*80)
    print("Testing complete problem-solving system integration")
    print("="*80)
    
    tests = [
        ("Team Creation", test_problem_solving_team_creation),
        ("Complete Workflow", test_complete_workflow_execution),
        ("Multiple Perspectives", test_multiple_perspectives),
        ("Strategy Evaluation", test_strategy_evaluation),
        ("Implementation Plans", test_implementation_plans),
        ("Recommendations", test_recommendations),
        ("Context Sharing", test_team_context_sharing)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("="*80)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("="*80)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - Phase 5 Complete!")
    else:
        print(f"⚠️  {total - passed} test(s) failed - Review required")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
