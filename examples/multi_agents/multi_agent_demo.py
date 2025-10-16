"""Multi-Agent System Demonstration

This module provides comprehensive demonstrations of the multi-agent framework
capabilities, showcasing different types of agent teams and their collaboration
patterns.
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

import sys
from pathlib import Path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from agents.multi_agent.research_team import EnhancedResearchTeam
from agents.multi_agent.roles.researcher import (
    create_general_researcher, 
    create_academic_researcher,
    create_industry_researcher,
    create_technical_researcher
)
from agents.multi_agent.roles.analyst import (
    create_general_analyst,
    create_data_analyst,
    create_business_analyst,
    create_quality_analyst,
    create_research_analyst
)
from agents.multi_agent.roles.synthesizer import (
    create_general_synthesizer,
    create_research_synthesizer,
    create_content_synthesizer,
    create_executive_synthesizer
)
from agents.multi_agent.workflows.research_orchestration import (
    create_research_workflow_orchestrator,
    ResearchPhase
)
from agents.multi_agent.problem_solving_integration import (
    create_problem_solving_team,
    ProblemSolvingTeamManager
)
from agents.multi_agent.roles.solution_strategist import PerspectiveType


class MultiAgentDemoRunner:
    """Demo runner for multi-agent system capabilities."""
    
    def __init__(self):
        self.demos = {}
        self.results = {}
    
    def register_demo(self, name: str, description: str, demo_func):
        """Register a demo."""
        self.demos[name] = {
            "description": description,
            "demo_func": demo_func
        }
    
    def run_demo(self, name: str) -> Dict[str, Any]:
        """Run a specific demo."""
        if name not in self.demos:
            raise ValueError(f"Demo '{name}' not found")
        
        print(f"\\n{'='*80}")
        print(f"DEMO: {name.upper().replace('_', ' ')}")
        print(f"{'='*80}")
        print(f"Description: {self.demos[name]['description']}")
        print(f"{'='*80}")
        
        start_time = time.time()
        
        try:
            result = self.demos[name]["demo_func"]()
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        demo_result = {
            "name": name,
            "success": success,
            "execution_time": execution_time,
            "result": result,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        
        self.results[name] = demo_result
        
        print(f"\\n{'='*80}")
        if success:
            print(f"✅ DEMO COMPLETED SUCCESSFULLY in {execution_time:.2f} seconds")
        else:
            print(f"❌ DEMO FAILED: {error}")
        print(f"{'='*80}")
        
        return demo_result
    
    def run_all_demos(self):
        """Run all registered demos."""
        print("\\n" + "="*100)
        print("MULTI-AGENT SYSTEM COMPREHENSIVE DEMONSTRATION")
        print("="*100)
        print("This demonstration showcases the enhanced multi-agent framework")
        print("with specialized teams, advanced workflows, and comprehensive")
        print("collaboration capabilities.")
        print("="*100)
        
        total_demos = len(self.demos)
        successful = 0
        
        for i, name in enumerate(self.demos, 1):
            print(f"\\n[{i}/{total_demos}] Starting demo: {name}")
            result = self.run_demo(name)
            if result["success"]:
                successful += 1
            
            # Brief pause between demos
            time.sleep(1)
        
        # Final summary
        self._print_final_summary(successful, total_demos)
        
        return self.results
    
    def _print_final_summary(self, successful: int, total: int):
        """Print final demonstration summary."""
        print("\\n" + "="*100)
        print("FINAL DEMONSTRATION SUMMARY")
        print("="*100)
        print(f"Total demos executed: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {total - successful}")
        print(f"Success rate: {successful/total:.1%}")
        
        if successful < total:
            print("\\nFailed demos:")
            for name, result in self.results.items():
                if not result["success"]:
                    print(f"  ❌ {name}: {result['error']}")
        
        print("\\nDemo execution times:")
        for name, result in self.results.items():
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {name}: {result['execution_time']:.2f}s")
        
        total_time = sum(r["execution_time"] for r in self.results.values())
        print(f"\\nTotal execution time: {total_time:.2f} seconds")
        
        print("\\nRECOMMENDATIONS:")
        if successful == total:
            print("🎉 All demos passed! The multi-agent system is fully functional.")
            print("   You can now use these patterns in your own applications.")
        elif successful >= total * 0.8:
            print("⚠️  Most demos passed. Check failed demos for system issues.")
        else:
            print("🚨 Multiple demo failures detected. System needs debugging.")
        
        print("="*100)


# Initialize demo runner
demo_runner = MultiAgentDemoRunner()


def research_team_basic_demo() -> Dict[str, Any]:
    """Basic research team collaboration demonstration."""
    topic = "The Future of Artificial Intelligence in Education"
    
    print(f"🔬 Creating research team for topic: '{topic}'")
    
    # Create research team
    team = EnhancedResearchTeam(topic, team_size=3, collaboration_rounds=3)
    
    print(f"Team created with ID: {team.team.team_id}")
    print(f"Team size: {team.team_size} specialized agents")
    
    # Show initial status
    status = team.get_team_status()
    print(f"\\nInitial team status: {status['status']}")
    print("Team composition:")
    for agent_id, agent_info in status['agents'].items():
        role = agent_info.get('role', 'Unknown')
        print(f"  • {agent_id}: {role}")
    
    # Execute research collaboration
    print("\\n🚀 Starting research collaboration...")
    print("Parameters:")
    print("  - Research depth: comprehensive")
    print("  - Source requirements: academic and industry sources")
    print("  - Output format: structured report")
    
    collaboration_result = team.collaborate(
        research_depth="comprehensive",
        source_requirements="academic and industry sources",
        output_format="structured_report"
    )
    
    # Process and display results
    if collaboration_result.get("success"):
        print("\\n✅ Research collaboration completed successfully!")
        
        quality_assessment = collaboration_result.get("quality_assessment", {})
        quality_score = quality_assessment.get("overall_score", 0)
        execution_time = collaboration_result.get("execution_time", 0)
        
        print(f"\\n📊 Results Summary:")
        print(f"  Quality Score: {quality_score:.2f}/5.0")
        print(f"  Execution Time: {execution_time:.2f} seconds")
        print(f"  Team Efficiency: {quality_score/execution_time:.3f} quality/second")
        
        # Show collaboration metrics
        collab_metrics = collaboration_result.get("collaboration_metrics", {})
        if collab_metrics:
            print(f"\\n🤝 Collaboration Metrics:")
            print(f"  Rounds completed: {collab_metrics.get('rounds_completed', 0)}")
            print(f"  Agent interactions: {collab_metrics.get('agent_interactions', 0)}")
            print(f"  Consensus achieved: {collab_metrics.get('consensus_achieved', False)}")
        
        result = {
            "demo_type": "research_team_basic",
            "topic": topic,
            "team_id": team.team.team_id,
            "team_size": team.team_size,
            "collaboration_success": True,
            "quality_score": quality_score,
            "execution_time": execution_time,
            "efficiency_score": quality_score/execution_time if execution_time > 0 else 0,
            "collaboration_metrics": collab_metrics
        }
        
    else:
        print("\\n❌ Research collaboration failed!")
        error_msg = collaboration_result.get("error", "Unknown error")
        print(f"Error: {error_msg}")
        
        result = {
            "demo_type": "research_team_basic",
            "topic": topic,
            "collaboration_success": False,
            "error": error_msg
        }
    
    # Cleanup
    team.cleanup()
    print("\\n🧹 Team resources cleaned up")
    
    return result


def research_team_advanced_demo() -> Dict[str, Any]:
    """Advanced research team with maximum configuration."""
    topic = "Sustainable Technology Integration in Smart Cities: A Multi-Disciplinary Analysis"
    
    print(f"🏙️ Creating advanced research team for complex topic:")
    print(f"'{topic}'")
    
    # Create maximum size research team
    team = EnhancedResearchTeam(topic, team_size=5, collaboration_rounds=5)
    
    print(f"\\nAdvanced team configuration:")
    print(f"  Team ID: {team.team.team_id}")
    print(f"  Team size: {team.team_size} agents (maximum)")
    print(f"  Collaboration rounds: 5 (extended)")
    
    # Show detailed team composition
    status = team.get_team_status()
    print(f"\\n👥 Team Composition:")
    for i, (agent_id, agent_info) in enumerate(status['agents'].items(), 1):
        role = agent_info.get('role', 'Unknown')
        expertise = agent_info.get('expertise_areas', [])
        print(f"  {i}. {agent_id}")
        print(f"     Role: {role}")
        print(f"     Expertise: {', '.join(expertise[:3])}{'...' if len(expertise) > 3 else ''}")
    
    # Execute advanced collaboration
    print("\\n🚀 Starting advanced research collaboration...")
    print("Advanced parameters:")
    print("  - Research depth: exhaustive")
    print("  - Sources: academic, industry, governmental, international")
    print("  - Output: detailed multi-perspective analysis")
    
    collaboration_result = team.collaborate(
        research_depth="exhaustive",
        source_requirements="academic, industry, governmental, and international sources",
        output_format="detailed_analysis"
    )
    
    # Analyze advanced results
    if collaboration_result.get("success"):
        print("\\n✅ Advanced collaboration completed successfully!")
        
        # Detailed metrics analysis
        quality_assessment = collaboration_result.get("quality_assessment", {})
        team_composition = collaboration_result.get("team_composition", {})
        collab_metrics = collaboration_result.get("collaboration_metrics", {})
        
        quality_score = quality_assessment.get("overall_score", 0)
        execution_time = collaboration_result.get("execution_time", 0)
        
        print(f"\\n📈 Advanced Results Analysis:")
        print(f"  Overall Quality: {quality_score:.2f}/5.0")
        print(f"  Execution Time: {execution_time:.2f} seconds")
        print(f"  Team Utilization: {team_composition.get('team_size', 0)}/{team.team_size} agents")
        
        # Quality breakdown
        print(f"\\n🎯 Quality Assessment Breakdown:")
        for metric, score in quality_assessment.items():
            if metric != "overall_score" and isinstance(score, (int, float)):
                print(f"  {metric.replace('_', ' ').title()}: {score:.2f}")
        
        # Collaboration insights
        print(f"\\n🤝 Collaboration Insights:")
        print(f"  Agent interactions: {collab_metrics.get('agent_interactions', 0)}")
        print(f"  Consensus rounds: {collab_metrics.get('consensus_rounds', 0)}")
        print(f"  Knowledge sharing events: {collab_metrics.get('knowledge_sharing', 0)}")
        
        result = {
            "demo_type": "research_team_advanced",
            "topic": topic,
            "team_id": team.team.team_id,
            "team_size": team.team_size,
            "collaboration_success": True,
            "quality_score": quality_score,
            "execution_time": execution_time,
            "advanced_features": {
                "exhaustive_research": True,
                "multi_source_integration": True,
                "detailed_analysis": True,
                "maximum_team_size": True
            },
            "quality_breakdown": quality_assessment,
            "collaboration_insights": collab_metrics
        }
        
    else:
        print("\\n❌ Advanced collaboration failed!")
        error_msg = collaboration_result.get("error", "Unknown error")
        print(f"Error: {error_msg}")
        
        result = {
            "demo_type": "research_team_advanced",
            "topic": topic,
            "collaboration_success": False,
            "error": error_msg
        }
    
    # Cleanup
    team.cleanup()
    print("\\n🧹 Advanced team resources cleaned up")
    
    return result


def role_specialization_showcase() -> Dict[str, Any]:
    """Showcase individual role specializations and capabilities."""
    print("🎭 Demonstrating Individual Role Specializations")
    print("This showcase tests each specialized role type independently")
    
    role_results = {}
    
    # Test Researcher Roles
    print("\\n🔍 RESEARCHER ROLES:")
    print("-" * 40)
    
    researchers = {
        "General Researcher": create_general_researcher(),
        "Academic Researcher": create_academic_researcher(),
        "Industry Researcher": create_industry_researcher(),
        "Technical Researcher": create_technical_researcher()
    }
    
    for name, researcher in researchers.items():
        print(f"\\n  Testing {name}:")
        print(f"    Capabilities: {len(researcher.capabilities)}")
        print(f"    Expertise areas: {len(researcher.role_definition.expertise_areas)}")
        
        # Test research quality evaluation
        mock_research = {
            "capabilities_used": ["information_gathering", "source_evaluation"],
            "format": "structured_data",
            "findings": [f"Sample finding from {name.lower()}"],
            "quality_metrics": {"credibility": 0.9, "completeness": 0.8}
        }
        
        evaluation = researcher.evaluate_research_quality(mock_research)
        quality_score = evaluation["overall_score"]
        
        print(f"    Quality evaluation: {quality_score:.2f}/5.0")
        
        role_results[name.lower().replace(" ", "_")] = {
            "type": "researcher",
            "capabilities_count": len(researcher.capabilities),
            "expertise_areas": len(researcher.role_definition.expertise_areas),
            "quality_score": quality_score,
            "status": "✅ Functional"
        }
    
    # Test Analyst Roles
    print("\\n📊 ANALYST ROLES:")
    print("-" * 40)
    
    analysts = {
        "General Analyst": create_general_analyst(),
        "Data Analyst": create_data_analyst(),
        "Business Analyst": create_business_analyst(),
        "Quality Analyst": create_quality_analyst(),
        "Research Analyst": create_research_analyst()
    }
    
    for name, analyst in analysts.items():
        print(f"\\n  Testing {name}:")
        print(f"    Capabilities: {len(analyst.capabilities)}")
        
        # Test analysis functionality
        test_data = {
            "research_findings": ["Finding A", "Finding B", "Finding C"],
            "numerical_data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "quality_indicators": {"accuracy": 0.85, "reliability": 0.90}
        }
        
        analysis_result = analyst.analyze_data(test_data, "comprehensive")
        accuracy_score = analysis_result["quality_assessment"]["accuracy_score"]
        recommendations_count = len(analysis_result["recommendations"])
        
        print(f"    Analysis accuracy: {accuracy_score:.2f}")
        print(f"    Recommendations: {recommendations_count}")
        
        role_results[name.lower().replace(" ", "_")] = {
            "type": "analyst",
            "capabilities_count": len(analyst.capabilities),
            "analysis_accuracy": accuracy_score,
            "recommendations_count": recommendations_count,
            "status": "✅ Functional"
        }
    
    # Test Synthesizer Roles
    print("\\n🔄 SYNTHESIZER ROLES:")
    print("-" * 40)
    
    synthesizers = {
        "General Synthesizer": create_general_synthesizer(),
        "Research Synthesizer": create_research_synthesizer(),
        "Content Synthesizer": create_content_synthesizer(),
        "Executive Synthesizer": create_executive_synthesizer()
    }
    
    for name, synthesizer in synthesizers.items():
        print(f"\\n  Testing {name}:")
        print(f"    Capabilities: {len(synthesizer.capabilities)}")
        
        # Test synthesis functionality
        synthesis_inputs = {
            "research_data": ["Research item 1", "Research item 2", "Research item 3"],
            "analysis_results": {
                "patterns": ["Pattern A", "Pattern B"],
                "insights": ["Insight X", "Insight Y"]
            },
            "expert_input": {
                "opinions": ["Expert opinion 1", "Expert opinion 2"],
                "recommendations": ["Expert rec 1"]
            }
        }
        
        synthesis_result = synthesizer.synthesize_information(
            synthesis_inputs, 
            "comprehensive", 
            "structured_report"
        )
        
        coherence_score = synthesis_result["quality_metrics"]["coherence_score"]
        integration_quality = synthesis_result["quality_metrics"]["integration_quality"]
        
        print(f"    Coherence: {coherence_score:.2f}")
        print(f"    Integration quality: {integration_quality:.2f}")
        
        role_results[name.lower().replace(" ", "_")] = {
            "type": "synthesizer",
            "capabilities_count": len(synthesizer.capabilities),
            "coherence_score": coherence_score,
            "integration_quality": integration_quality,
            "status": "✅ Functional"
        }
    
    # Summary
    total_roles = len(role_results)
    functional_roles = len([r for r in role_results.values() if "✅" in r["status"]])
    
    print(f"\\n📋 ROLE SPECIALIZATION SUMMARY:")
    print(f"  Total roles tested: {total_roles}")
    print(f"  Functional roles: {functional_roles}")
    print(f"  Success rate: {functional_roles/total_roles:.1%}")
    
    return {
        "demo_type": "role_specialization",
        "total_roles_tested": total_roles,
        "functional_roles": functional_roles,
        "success_rate": functional_roles/total_roles,
        "role_details": role_results,
        "specialization_coverage": {
            "researchers": len(researchers),
            "analysts": len(analysts),
            "synthesizers": len(synthesizers)
        }
    }


def workflow_orchestration_demo() -> Dict[str, Any]:
    """Demonstrate advanced workflow orchestration capabilities."""
    topic = "Digital Transformation Strategies for Healthcare Organizations"
    team_id = "workflow_demo_team"
    
    print(f"⚙️ Creating workflow orchestrator for:")
    print(f"'{topic}'")
    
    # Create workflow orchestrator
    orchestrator = create_research_workflow_orchestrator(team_id, topic)
    
    print(f"\\nWorkflow Configuration:")
    print(f"  Workflow ID: {orchestrator.workflow_id}")
    print(f"  Total tasks: {len(orchestrator.tasks)}")
    print(f"  Quality gates: {len(orchestrator.quality_gates)}")
    print(f"  Research phases: {len([p for p in ResearchPhase])}")
    
    # Show workflow phases
    print(f"\\n📋 Workflow Phases:")
    for i, phase in enumerate(ResearchPhase, 1):
        print(f"  {i}. {phase.value.replace('_', ' ').title()}")
    
    # Start workflow
    print("\\n🚀 Starting workflow orchestration...")
    start_result = orchestrator.start_workflow()
    
    if not start_result["success"]:
        return {
            "demo_type": "workflow_orchestration",
            "workflow_id": orchestrator.workflow_id,
            "success": False,
            "error": "Failed to start workflow"
        }
    
    print(f"✅ Workflow started successfully!")
    print(f"Estimated duration: {start_result['estimated_duration_minutes']} minutes")
    
    # Execute workflow phases
    phase_results = []
    max_demo_phases = 4  # Limit for demo purposes
    
    for phase_num in range(max_demo_phases):
        print(f"\\n📍 Executing Phase {phase_num + 1}:")
        
        # Get current status
        status = orchestrator.get_workflow_status()
        current_phase = status["current_phase"]
        progress = status["progress"]
        
        print(f"  Current phase: {current_phase.replace('_', ' ').title()}")
        print(f"  Overall progress: {progress:.1%}")
        
        # Execute next phase
        print(f"  ⏳ Processing phase...")
        execution_result = orchestrator.execute_next_phase()
        
        if execution_result["success"]:
            executed_tasks = execution_result["executed_tasks"]
            print(f"  ✅ Phase completed: {executed_tasks} tasks executed")
            
            phase_results.append({
                "phase": current_phase,
                "executed_tasks": executed_tasks,
                "success": True,
                "phase_number": phase_num + 1
            })
        else:
            error_msg = execution_result.get("error", "Unknown error")
            print(f"  ❌ Phase failed: {error_msg}")
            
            phase_results.append({
                "phase": current_phase,
                "success": False,
                "error": error_msg,
                "phase_number": phase_num + 1
            })
            break
        
        # Check if workflow is complete
        final_status = orchestrator.get_workflow_status()
        if final_status["progress"] >= 1.0:
            print(f"  🎉 Workflow completed!")
            break
    
    # Get final workflow status
    final_status = orchestrator.get_workflow_status()
    successful_phases = len([p for p in phase_results if p["success"]])
    
    print(f"\\n📊 Workflow Orchestration Results:")
    print(f"  Phases executed: {len(phase_results)}")
    print(f"  Successful phases: {successful_phases}")
    print(f"  Final progress: {final_status['progress']:.1%}")
    print(f"  Workflow status: {final_status['status']}")
    
    return {
        "demo_type": "workflow_orchestration",
        "workflow_id": orchestrator.workflow_id,
        "topic": topic,
        "total_tasks": len(orchestrator.tasks),
        "quality_gates": len(orchestrator.quality_gates),
        "phases_executed": len(phase_results),
        "successful_phases": successful_phases,
        "final_progress": final_status["progress"],
        "workflow_status": final_status["status"],
        "phase_results": phase_results,
        "success": successful_phases > 0
    }


def integration_scalability_test() -> Dict[str, Any]:
    """Test system integration and scalability."""
    print("⚡ Running Integration & Scalability Test")
    print("This test evaluates system performance under various load conditions")
    
    test_scenarios = [
        {
            "name": "Concurrent Teams",
            "description": "Multiple research teams running simultaneously",
            "teams": 3,
            "team_size": 3
        },
        {
            "name": "Large Team",
            "description": "Single team with maximum agent count",
            "teams": 1,
            "team_size": 5
        },
        {
            "name": "Complex Research",
            "description": "Complex topic with exhaustive research depth",
            "teams": 1,
            "team_size": 4,
            "complexity": "high"
        }
    ]
    
    scenario_results = {}
    
    for scenario in test_scenarios:
        print(f"\\n🧪 Testing: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        
        scenario_start = time.time()
        teams = []
        results = []
        
        try:
            if scenario["name"] == "Concurrent Teams":
                # Create multiple teams
                topics = [
                    "AI in Renewable Energy Systems",
                    "Blockchain for Supply Chain Transparency",  
                    "IoT Security in Smart Manufacturing"
                ]
                
                print(f"  Creating {scenario['teams']} concurrent teams...")
                for i, topic in enumerate(topics[:scenario["teams"]]):
                    team = EnhancedResearchTeam(
                        topic, 
                        team_size=scenario["team_size"],
                        collaboration_rounds=3
                    )
                    teams.append(team)
                    print(f"    Team {i+1}: {topic}")
                
                # Execute collaborations
                print(f"  Executing concurrent collaborations...")
                for i, team in enumerate(teams):
                    result = team.collaborate(research_depth="comprehensive")
                    results.append(result)
                    print(f"    Team {i+1}: {'✅' if result.get('success') else '❌'}")
            
            elif scenario["name"] == "Large Team":
                # Create maximum size team
                topic = "Comprehensive Analysis: Future of Work in Digital Economy"
                print(f"  Creating large team (size {scenario['team_size']})...")
                
                team = EnhancedResearchTeam(
                    topic, 
                    team_size=scenario["team_size"],
                    collaboration_rounds=5
                )
                teams.append(team)
                
                print(f"  Executing large team collaboration...")
                result = team.collaborate(research_depth="comprehensive")
                results.append(result)
                print(f"    Large team: {'✅' if result.get('success') else '❌'}")
            
            elif scenario["name"] == "Complex Research":
                # Create complex research scenario
                complex_topic = (
                    "Interdisciplinary Analysis of Socioeconomic Impacts of "
                    "Emerging Technologies on Global Sustainable Development Goals"
                )
                print(f"  Creating complex research scenario...")
                
                team = EnhancedResearchTeam(
                    complex_topic, 
                    team_size=scenario["team_size"],
                    collaboration_rounds=4
                )
                teams.append(team)
                
                print(f"  Executing complex research...")
                result = team.collaborate(
                    research_depth="exhaustive",
                    source_requirements="academic, industry, governmental, and international sources",
                    output_format="detailed_analysis"
                )
                results.append(result)
                print(f"    Complex research: {'✅' if result.get('success') else '❌'}")
            
            scenario_end = time.time()
            scenario_time = scenario_end - scenario_start
            
            # Analyze results
            successful_results = [r for r in results if r.get("success", False)]
            success_rate = len(successful_results) / len(results) if results else 0
            
            avg_quality = 0
            if successful_results:
                quality_scores = [
                    r.get("quality_assessment", {}).get("overall_score", 0) 
                    for r in successful_results
                ]
                avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            
            scenario_results[scenario["name"].lower().replace(" ", "_")] = {
                "scenario": scenario,
                "teams_created": len(teams),
                "collaborations_executed": len(results),
                "success_rate": success_rate,
                "average_quality": avg_quality,
                "total_time": scenario_time,
                "performance_score": (success_rate * avg_quality) / scenario_time if scenario_time > 0 else 0,
                "status": "✅ Passed" if success_rate >= 0.7 else "❌ Failed"
            }
            
            print(f"  📊 Results: {success_rate:.1%} success, "
                  f"Avg quality: {avg_quality:.2f}, "
                  f"Time: {scenario_time:.2f}s")
            print(f"  Status: {scenario_results[scenario['name'].lower().replace(' ', '_')]['status']}")
            
        except Exception as e:
            print(f"  ❌ Scenario failed: {str(e)}")
            scenario_results[scenario["name"].lower().replace(" ", "_")] = {
                "scenario": scenario,
                "status": "❌ Failed",
                "error": str(e)
            }
        
        finally:
            # Cleanup all teams
            for team in teams:
                try:
                    team.cleanup()
                except:
                    pass
    
    # Overall assessment
    passed_scenarios = len([r for r in scenario_results.values() if "✅" in r.get("status", "")])
    total_scenarios = len(test_scenarios)
    overall_success = passed_scenarios / total_scenarios
    
    print(f"\\n📋 Integration & Scalability Summary:")
    print(f"  Scenarios tested: {total_scenarios}")
    print(f"  Scenarios passed: {passed_scenarios}")
    print(f"  Overall success: {overall_success:.1%}")
    
    system_status = "🟢 EXCELLENT" if overall_success >= 0.9 else \
                    "🟡 GOOD" if overall_success >= 0.7 else \
                    "🔴 NEEDS IMPROVEMENT"
    
    print(f"  System status: {system_status}")
    
    return {
        "demo_type": "integration_scalability",
        "scenarios_tested": total_scenarios,
        "scenarios_passed": passed_scenarios,
        "overall_success_rate": overall_success,
        "system_status": system_status,
        "scenario_results": scenario_results
    }


def problem_solving_team_demo() -> Dict[str, Any]:
    """Demonstrate problem-solving team capabilities."""
    print("\n🔧 Creating Problem-Solving Team...")
    print("="*60)
    
    # Create problem-solving team
    team_manager = create_problem_solving_team(
        team_name="E-commerce Problem-Solving Team",
        perspectives=[
            PerspectiveType.TECHNICAL,
            PerspectiveType.BUSINESS,
            PerspectiveType.USER_EXPERIENCE
        ]
    )
    
    # Display team status
    status = team_manager.get_team_status()
    print(f"✓ Team Created: {status['team_id']}")
    print(f"  Status: {status['status']}")
    print(f"  Agents: {status['agent_count']}")
    for agent_id, agent_info in status['agents'].items():
        print(f"    - {agent_id}: {agent_info['role']}")
    
    # Solve a business problem
    print("\n💡 Solving Business Problem...")
    print("="*60)
    print("Problem: E-commerce Checkout Abandonment")
    print("Issue: 35% cart abandonment rate costing $2M/month")
    
    result = team_manager.solve_problem(
        problem_title="E-commerce Checkout Abandonment",
        problem_description="""
        Our e-commerce platform has a critical checkout abandonment issue:
        - Cart abandonment rate increased from 15% to 35% in last quarter
        - Average checkout time increased from 2 minutes to 8 minutes
        - Mobile checkout completion rate dropped to 40%
        - Payment gateway failures increased to 12%
        - Customer complaints about confusing checkout flow
        - Estimated revenue loss: $2M per month
        """,
        context={
            "platform": "E-commerce",
            "monthly_visitors": 500000,
            "revenue_loss": "$2M/month",
            "urgency": "Critical"
        },
        constraints=[
            "Must maintain PCI DSS compliance",
            "Cannot take site offline during fixes",
            "Budget limited to $200K",
            "Must implement within 3 months"
        ],
        success_criteria=[
            "Reduce abandonment rate to under 20%",
            "Decrease checkout time to under 3 minutes",
            "Increase mobile completion to >70%",
            "Reduce payment failures to <3%"
        ]
    )
    
    # Display results
    print(f"\n✅ Problem Solved!")
    print("="*60)
    print(f"Problem ID: {result.problem_id}")
    print(f"Status: {result.status.value}")
    print(f"Duration: {result.duration:.2f}s")
    print(f"Success Probability: {result.success_probability:.0%}")
    
    # Analysis summary
    print(f"\n📊 Analysis Results:")
    print("-"*60)
    if result.problem_analysis:
        print(f"Root Causes Identified: {len(result.problem_analysis.root_causes)}")
        for i, cause in enumerate(result.problem_analysis.root_causes[:3], 1):
            print(f"  {i}. {cause.description}")
            print(f"     Category: {cause.category}, Impact: {cause.impact_level.value}")
        
        print(f"\nKey Components: {len(result.problem_analysis.key_components)}")
        for component in result.problem_analysis.key_components[:3]:
            print(f"  - {component.name}: {component.role_in_problem}")
        
        print(f"\nAnalysis Confidence: {result.problem_analysis.confidence_score:.0%}")
    
    # Strategies
    print(f"\n💡 Strategies Generated: {len(result.strategies)}")
    print("-"*60)
    for i, strategy in enumerate(result.strategies, 1):
        eval_score = next((e.overall_score for e in result.strategy_evaluations 
                          if e.strategy_id == strategy.strategy_id), 0)
        print(f"{i}. {strategy.strategy_name} ({strategy.perspective.value})")
        print(f"   Score: {eval_score:.1f}/100 | Success: {strategy.success_probability:.0%}")
        print(f"   Timeline: {strategy.estimated_timeline} | Cost: ${strategy.estimated_cost_min:,}-${strategy.estimated_cost_max:,}")
        print(f"   Steps: {len(strategy.steps)} | Benefits: {len(strategy.benefits)}")
    
    # Recommended strategy
    print(f"\n🎯 Recommended Strategy:")
    print("-"*60)
    if result.recommended_strategy:
        print(f"Strategy: {result.recommended_strategy.strategy_name}")
        print(f"Perspective: {result.recommended_strategy.perspective.value}")
        print(f"Approach: {result.recommended_strategy.approach.value}")
        print(f"Success Probability: {result.recommended_strategy.success_probability:.0%}")
        print(f"Risk Level: {result.recommended_strategy.risk_level.value}")
        
        print(f"\nKey Steps:")
        for i, step in enumerate(result.recommended_strategy.steps[:5], 1):
            print(f"  {i}. {step.description}")
        
        print(f"\nTop Benefits:")
        for benefit in result.recommended_strategy.benefits[:3]:
            print(f"  • {benefit.description}")
            print(f"    Magnitude: {benefit.magnitude.value}, Metrics: {', '.join(benefit.metrics)}")
    
    # Implementation plan
    print(f"\n🏗️  Implementation Plan:")
    print("-"*60)
    if result.recommended_strategy:
        plan_id = f"PLAN-{result.recommended_strategy.strategy_id}"
        if plan_id in result.implementation_plans:
            plan = result.implementation_plans[plan_id]
            print(f"Duration: {plan.duration_days} days ({plan.duration_days/30:.1f} months)")
            print(f"Total Effort: {plan.total_effort_hours} hours ({plan.total_effort_hours/160:.1f} FTEs)")
            print(f"Total Cost: ${plan.total_cost:,.0f}")
            
            print(f"\nPhases: {len(plan.phases)}")
            for phase in plan.phases:
                phase_tasks = [t for t in plan.get_all_tasks() if t.phase_id == phase.phase_id]
                print(f"  • {phase.phase_name}: {len(phase_tasks)} tasks, {phase.duration_days} days")
            
            print(f"\nMilestones: {len(plan.get_all_milestones())}")
            for milestone in sorted(plan.get_all_milestones(), 
                                   key=lambda m: m.target_date)[:5]:
                print(f"  • {milestone.name} ({milestone.milestone_type.value})")
            
            print(f"\nQuality Gates: {len(plan.quality_gates)}")
            print(f"Risk Mitigation Plans: {len(plan.risk_mitigation_plans)}")
    
    # Recommendations
    print(f"\n📝 Recommendations: {len(result.recommendations)}")
    print("-"*60)
    for i, rec in enumerate(result.recommendations[:5], 1):
        print(f"{i}. {rec.title}")
        print(f"   Type: {rec.recommendation_type.value} | Priority: {rec.priority}")
        print(f"   {rec.description[:100]}...")
    
    # Executive summary
    print(f"\n📋 Executive Summary:")
    print("-"*60)
    print(result.executive_summary[:400] + "...")
    
    # Cleanup
    team_manager.cleanup()
    
    return {
        "team_id": status['team_id'],
        "problem_id": result.problem_id,
        "status": result.status.value,
        "duration": result.duration,
        "success_probability": result.success_probability,
        "root_causes_count": len(result.problem_analysis.root_causes) if result.problem_analysis else 0,
        "strategies_count": len(result.strategies),
        "recommended_strategy": result.recommended_strategy.strategy_name if result.recommended_strategy else None,
        "implementation_duration_days": result.implementation_plans[f"PLAN-{result.recommended_strategy.strategy_id}"].duration_days if result.recommended_strategy and f"PLAN-{result.recommended_strategy.strategy_id}" in result.implementation_plans else 0,
        "implementation_cost": result.implementation_plans[f"PLAN-{result.recommended_strategy.strategy_id}"].total_cost if result.recommended_strategy and f"PLAN-{result.recommended_strategy.strategy_id}" in result.implementation_plans else 0,
        "recommendations_count": len(result.recommendations),
        "key_insights": result.key_insights
    }


# Register all demos
demo_runner.register_demo(
    "research_team_basic",
    "Basic research team collaboration with 3 agents",
    research_team_basic_demo
)

demo_runner.register_demo(
    "research_team_advanced",
    "Advanced research team with maximum configuration",
    research_team_advanced_demo
)

demo_runner.register_demo(
    "role_specialization",
    "Individual role specialization showcase",
    role_specialization_showcase
)

demo_runner.register_demo(
    "workflow_orchestration",
    "Advanced workflow orchestration demonstration",
    workflow_orchestration_demo
)

demo_runner.register_demo(
    "integration_scalability",
    "System integration and scalability testing",
    integration_scalability_test
)

demo_runner.register_demo(
    "problem_solving_team",
    "Problem-solving team with comprehensive analysis and recommendations",
    problem_solving_team_demo
)


def main():
    """Main demonstration function."""
    print("MULTI-AGENT SYSTEM DEMONSTRATION")
    print("="*80)
    print("Welcome to the comprehensive multi-agent framework demonstration!")
    print("This system showcases advanced research team collaboration,")
    print("specialized agent roles, and sophisticated workflow orchestration.")
    print()
    
    # Show available demos
    print("Available Demonstrations:")
    for i, (name, info) in enumerate(demo_runner.demos.items(), 1):
        print(f"{i}. {name.replace('_', ' ').title()}")
        print(f"   {info['description']}")
        print()
    
    # Get user choice
    print("Options:")
    print("- Enter demo number (1-5) to run specific demo")
    print("- Enter 'all' to run complete demonstration suite")
    print("- Enter 'q' to quit")
    
    choice = input("\\nYour choice: ").strip().lower()
    
    if choice == 'q':
        print("\\nGoodbye! 👋")
        return
    
    elif choice == 'all':
        # Run comprehensive demonstration
        results = demo_runner.run_all_demos()
        
        # Offer detailed results
        print("\\n" + "="*80)
        show_details = input("Show detailed results for each demo? (y/n): ").strip().lower()
        
        if show_details == 'y':
            for name, result in results.items():
                if result["success"] and result["result"]:
                    print(f"\\n{'-'*60}")
                    print(f"DETAILED RESULTS: {name.upper()}")
                    print(f"{'-'*60}")
                    for key, value in result["result"].items():
                        if isinstance(value, dict):
                            print(f"{key}: {len(value)} items")
                        elif isinstance(value, list):
                            print(f"{key}: {len(value)} items")
                        else:
                            print(f"{key}: {value}")
    
    elif choice.isdigit():
        # Run specific demo
        demo_num = int(choice)
        demo_names = list(demo_runner.demos.keys())
        
        if 1 <= demo_num <= len(demo_names):
            demo_name = demo_names[demo_num - 1]
            result = demo_runner.run_demo(demo_name)
            
            # Show detailed result
            if result["success"] and result["result"]:
                print("\\n" + "="*60)
                print("DETAILED DEMO RESULTS")
                print("="*60)
                for key, value in result["result"].items():
                    if isinstance(value, dict):
                        print(f"{key}: {len(value)} items")
                        if len(value) <= 5:  # Show small dicts
                            for subkey, subvalue in value.items():
                                print(f"  {subkey}: {subvalue}")
                    elif isinstance(value, list):
                        print(f"{key}: {len(value)} items")
                    else:
                        print(f"{key}: {value}")
        else:
            print("Invalid demo number!")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()