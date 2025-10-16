"""Research Team Example Implementation

Comprehensive example implementation showcasing the enhanced research team
collaboration capabilities using the multi-agent framework.
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.agents.multi_agent.research_team import EnhancedResearchTeam
from src.agents.multi_agent.roles.researcher import (
    create_general_researcher, 
    create_academic_researcher,
    create_industry_researcher
)
from src.agents.multi_agent.roles.analyst import (
    create_data_analyst,
    create_quality_analyst
)
from src.agents.multi_agent.roles.synthesizer import (
    create_research_synthesizer,
    create_executive_synthesizer
)
from src.agents.multi_agent.workflows.research_orchestration import (
    create_research_workflow_orchestrator,
    ResearchPhase
)


class ResearchTeamExampleRunner:
    """Runner class for research team examples."""
    
    def __init__(self):
        self.examples = {}
        self.results = {}
        
    def register_example(self, name: str, description: str, runner_func):
        """Register an example implementation."""
        self.examples[name] = {
            "description": description,
            "runner": runner_func
        }
    
    def run_example(self, name: str) -> Dict[str, Any]:
        """Run a specific example."""
        if name not in self.examples:
            raise ValueError(f"Example '{name}' not found")
        
        print(f"\\nRunning Example: {name}")
        print("=" * 60)
        print(f"Description: {self.examples[name]['description']}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            result = self.examples[name]["runner"]()
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        example_result = {
            "name": name,
            "success": success,
            "execution_time": execution_time,
            "result": result,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        
        self.results[name] = example_result
        
        if success:
            print(f"✅ Example completed successfully in {execution_time:.2f} seconds")
        else:
            print(f"❌ Example failed: {error}")
        
        return example_result
    
    def run_all_examples(self):
        """Run all registered examples."""
        print("Running All Research Team Examples")
        print("=" * 80)
        
        total_examples = len(self.examples)
        successful = 0
        
        for name in self.examples:
            result = self.run_example(name)
            if result["success"]:
                successful += 1
        
        print("\\n" + "=" * 80)
        print(f"Examples Summary: {successful}/{total_examples} successful")
        
        if successful < total_examples:
            failed_examples = [name for name, result in self.results.items() if not result["success"]]
            print(f"Failed examples: {', '.join(failed_examples)}")
        
        return self.results


# Initialize the example runner
runner = ResearchTeamExampleRunner()


def basic_research_team_example() -> Dict[str, Any]:
    """Basic research team collaboration example."""
    topic = "Impact of Remote Work on Team Productivity"
    
    # Create research team
    team = EnhancedResearchTeam(topic, team_size=3, collaboration_rounds=3)
    
    print(f"Created research team for: {topic}")
    print(f"Team ID: {team.team.team_id}")
    print(f"Team size: {team.team_size} agents")
    
    # Get initial team status
    status = team.get_team_status()
    print(f"Initial status: {status['status']}")
    print(f"Agents: {', '.join(status['agents'].keys())}")
    
    # Execute collaboration
    print("\\nExecuting research collaboration...")
    collaboration_result = team.collaborate(
        research_depth="comprehensive",
        source_requirements="academic and industry sources",
        output_format="structured_report"
    )
    
    # Process results
    if collaboration_result.get("success"):
        print("✅ Collaboration completed successfully")
        
        # Extract key metrics
        quality_score = collaboration_result.get("quality_assessment", {}).get("overall_score", 0)
        execution_time = collaboration_result.get("execution_time", 0)
        
        print(f"Quality score: {quality_score:.2f}")
        print(f"Execution time: {execution_time:.2f} seconds")
        
        result = {
            "team_id": team.team.team_id,
            "topic": topic,
            "collaboration_success": True,
            "quality_score": quality_score,
            "execution_time": execution_time,
            "team_composition": collaboration_result.get("team_composition", {}),
            "research_parameters": collaboration_result.get("research_parameters", {})
        }
    else:
        print("❌ Collaboration failed")
        result = {
            "team_id": team.team.team_id,
            "topic": topic,
            "collaboration_success": False,
            "error": collaboration_result.get("error", "Unknown error")
        }
    
    # Cleanup
    team.cleanup()
    
    return result


def advanced_research_team_example() -> Dict[str, Any]:
    """Advanced research team with specialized roles."""
    topic = "Artificial Intelligence Ethics in Healthcare Applications"
    
    # Create research team with maximum size
    team = EnhancedResearchTeam(topic, team_size=5, collaboration_rounds=5)
    
    print(f"Created advanced research team for: {topic}")
    print(f"Team size: {team.team_size} agents (maximum configuration)")
    
    # Show team composition
    status = team.get_team_status()
    print("\\nTeam composition:")
    for agent_id, agent_info in status["agents"].items():
        print(f"  • {agent_id}: {agent_info.get('role', 'Unknown role')}")
    
    # Execute comprehensive collaboration
    print("\\nExecuting comprehensive research collaboration...")
    collaboration_result = team.collaborate(
        research_depth="exhaustive",
        source_requirements="academic, industry, regulatory, and ethical sources",
        output_format="detailed_analysis"
    )
    
    # Analyze results
    success = collaboration_result.get("success", False)
    
    if success:
        print("✅ Advanced collaboration completed")
        
        # Detailed result analysis
        team_comp = collaboration_result.get("team_composition", {})
        collab_metrics = collaboration_result.get("collaboration_metrics", {})
        quality_assessment = collaboration_result.get("quality_assessment", {})
        
        print(f"Team utilized {team_comp.get('team_size', 0)} specialized agents")
        print(f"Workflow: {collab_metrics.get('workflow_used', 'N/A')}")
        print(f"Quality score: {quality_assessment.get('overall_score', 0):.2f}")
        
        result = {
            "team_id": team.team.team_id,
            "topic": topic,
            "team_size": team.team_size,
            "collaboration_success": True,
            "advanced_features": {
                "exhaustive_research": True,
                "multi_source_integration": True,
                "detailed_analysis": True
            },
            "performance_metrics": {
                "quality_score": quality_assessment.get("overall_score", 0),
                "team_utilization": team_comp.get("team_size", 0),
                "workflow_complexity": "high"
            },
            "collaboration_result": collaboration_result
        }
    else:
        print("❌ Advanced collaboration failed")
        result = {
            "team_id": team.team.team_id,
            "topic": topic,
            "collaboration_success": False,
            "error": collaboration_result.get("error", "Unknown error")
        }
    
    # Cleanup
    team.cleanup()
    
    return result


def role_specialization_example() -> Dict[str, Any]:
    """Example showcasing individual role specializations."""
    print("Demonstrating individual role specializations...")
    
    roles_tested = {}
    
    # Test researcher roles
    print("\\n1. Testing Researcher Roles:")
    researchers = {
        "general": create_general_researcher(),
        "academic": create_academic_researcher(),
        "industry": create_industry_researcher()
    }
    
    for name, researcher in researchers.items():
        print(f"   • {name.title()} Researcher: {len(researcher.capabilities)} capabilities")
        
        # Test quality evaluation
        mock_output = {
            "capabilities_used": ["information_gathering", "source_evaluation"],
            "format": "structured_data",
            "findings": [f"Sample finding from {name} researcher"],
            "quality_metrics": {"credibility": 0.9}
        }
        
        evaluation = researcher.evaluate_research_quality(mock_output)
        roles_tested[f"{name}_researcher"] = {
            "type": "researcher",
            "capabilities": len(researcher.capabilities),
            "quality_score": evaluation["overall_score"],
            "expertise_areas": len(researcher.role_definition.expertise_areas)
        }
    
    # Test analyst roles
    print("\\n2. Testing Analyst Roles:")
    analysts = {
        "data": create_data_analyst(),
        "quality": create_quality_analyst()
    }
    
    for name, analyst in analysts.items():
        print(f"   • {name.title()} Analyst: {len(analyst.capabilities)} capabilities")
        
        # Test analysis functionality
        test_data = {
            "research_findings": ["Finding A", "Finding B"],
            "numerical_data": [1, 2, 3, 4, 5],
            "quality_indicators": {"accuracy": 0.85}
        }
        
        analysis_result = analyst.analyze_data(test_data, "comprehensive")
        roles_tested[f"{name}_analyst"] = {
            "type": "analyst",
            "capabilities": len(analyst.capabilities),
            "analysis_quality": analysis_result["quality_assessment"]["accuracy_score"],
            "recommendations": len(analysis_result["recommendations"])
        }
    
    # Test synthesizer roles
    print("\\n3. Testing Synthesizer Roles:")
    synthesizers = {
        "research": create_research_synthesizer(),
        "executive": create_executive_synthesizer()
    }
    
    for name, synthesizer in synthesizers.items():
        print(f"   • {name.title()} Synthesizer: {len(synthesizer.capabilities)} capabilities")
        
        # Test synthesis functionality
        synthesis_inputs = {
            "research_data": ["Research item 1", "Research item 2"],
            "analysis_results": {"patterns": ["Pattern A", "Pattern B"]},
            "expert_input": {"opinion": "Expert perspective"}
        }
        
        synthesis_result = synthesizer.synthesize_information(
            synthesis_inputs, 
            "comprehensive", 
            "structured_report"
        )
        
        roles_tested[f"{name}_synthesizer"] = {
            "type": "synthesizer",
            "capabilities": len(synthesizer.capabilities),
            "synthesis_quality": synthesis_result["quality_metrics"]["coherence_score"],
            "integration_score": synthesis_result["quality_metrics"]["integration_quality"]
        }
    
    print(f"\\n✅ Tested {len(roles_tested)} specialized roles")
    
    return {
        "roles_tested": len(roles_tested),
        "role_details": roles_tested,
        "specialization_coverage": {
            "researchers": len(researchers),
            "analysts": len(analysts),
            "synthesizers": len(synthesizers)
        }
    }


def workflow_orchestration_example() -> Dict[str, Any]:
    """Example showcasing workflow orchestration capabilities."""
    topic = "Blockchain Technology Adoption in Supply Chain Management"
    team_id = "workflow_demo_team"
    
    print(f"Creating workflow orchestrator for: {topic}")
    
    # Create workflow orchestrator
    orchestrator = create_research_workflow_orchestrator(team_id, topic)
    
    print(f"Workflow ID: {orchestrator.workflow_id}")
    print(f"Total tasks: {len(orchestrator.tasks)}")
    print(f"Quality gates: {len(orchestrator.quality_gates)}")
    
    # Start workflow
    print("\\nStarting workflow...")
    start_result = orchestrator.start_workflow()
    
    if not start_result["success"]:
        return {
            "workflow_id": orchestrator.workflow_id,
            "success": False,
            "error": "Failed to start workflow"
        }
    
    print(f"✅ Workflow started successfully")
    print(f"Estimated duration: {start_result['estimated_duration_minutes']} minutes")
    
    # Execute workflow phases
    phase_results = []
    max_phases = 3  # Limit for demo purposes
    
    for phase_num in range(max_phases):
        print(f"\\nExecuting phase {phase_num + 1}...")
        
        # Get current status
        status = orchestrator.get_workflow_status()
        current_phase = status["current_phase"]
        progress = status["progress"]
        
        print(f"Current phase: {current_phase}")
        print(f"Overall progress: {progress:.1%}")
        
        # Execute next phase
        execution_result = orchestrator.execute_next_phase()
        
        if execution_result["success"]:
            print(f"✅ Phase executed: {execution_result['executed_tasks']} tasks completed")
            phase_results.append({
                "phase": current_phase,
                "executed_tasks": execution_result["executed_tasks"],
                "success": True
            })
        else:
            print(f"❌ Phase execution failed: {execution_result.get('error', 'Unknown error')}")
            phase_results.append({
                "phase": current_phase,
                "success": False,
                "error": execution_result.get("error")
            })
            break
        
        # Check if workflow is complete
        final_status = orchestrator.get_workflow_status()
        if final_status["progress"] >= 1.0:
            print("🎉 Workflow completed!")
            break
    
    # Get final workflow status
    final_status = orchestrator.get_workflow_status()
    
    return {
        "workflow_id": orchestrator.workflow_id,
        "topic": topic,
        "total_tasks": len(orchestrator.tasks),
        "quality_gates": len(orchestrator.quality_gates),
        "phases_executed": len(phase_results),
        "final_progress": final_status["progress"],
        "workflow_status": final_status["status"],
        "phase_results": phase_results,
        "success": len([p for p in phase_results if p["success"]]) > 0
    }


def comparative_research_example() -> Dict[str, Any]:
    """Example comparing different research configurations."""
    base_topic = "Machine Learning in Medical Diagnosis"
    
    print("Comparing different research team configurations...")
    
    configurations = [
        {"name": "Small Team", "size": 2, "rounds": 3},
        {"name": "Medium Team", "size": 3, "rounds": 4},
        {"name": "Large Team", "size": 5, "rounds": 5}
    ]
    
    comparison_results = {}
    
    for config in configurations:
        print(f"\\nTesting {config['name']} configuration...")
        
        # Create team with specific configuration
        team = EnhancedResearchTeam(
            topic=f"{base_topic} ({config['name']})",
            team_size=config["size"],
            collaboration_rounds=config["rounds"]
        )
        
        start_time = time.time()
        
        # Execute collaboration
        result = team.collaborate(
            research_depth="comprehensive",
            source_requirements="academic and clinical sources",
            output_format="structured_report"
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Analyze results
        if result.get("success"):
            quality_score = result.get("quality_assessment", {}).get("overall_score", 0)
            team_composition = result.get("team_composition", {})
            
            comparison_results[config["name"].lower().replace(" ", "_")] = {
                "configuration": config,
                "execution_time": execution_time,
                "quality_score": quality_score,
                "team_size": team_composition.get("team_size", 0),
                "success": True,
                "efficiency_score": quality_score / execution_time if execution_time > 0 else 0
            }
            
            print(f"✅ {config['name']}: Quality {quality_score:.2f}, Time {execution_time:.2f}s")
        else:
            comparison_results[config["name"].lower().replace(" ", "_")] = {
                "configuration": config,
                "success": False,
                "error": result.get("error", "Unknown error")
            }
            
            print(f"❌ {config['name']}: Failed")
        
        # Cleanup
        team.cleanup()
    
    # Analyze comparison
    successful_configs = [name for name, result in comparison_results.items() if result["success"]]
    
    if successful_configs:
        # Find best configuration by efficiency
        best_config = max(
            successful_configs,
            key=lambda name: comparison_results[name]["efficiency_score"]
        )
        
        print(f"\\n🏆 Best configuration: {best_config.replace('_', ' ').title()}")
        best_result = comparison_results[best_config]
        print(f"   Efficiency score: {best_result['efficiency_score']:.3f}")
        print(f"   Quality: {best_result['quality_score']:.2f}")
        print(f"   Time: {best_result['execution_time']:.2f}s")
    
    return {
        "configurations_tested": len(configurations),
        "successful_configurations": len(successful_configs),
        "comparison_results": comparison_results,
        "best_configuration": best_config if successful_configs else None
    }


def integration_stress_test() -> Dict[str, Any]:
    """Stress test for research team integration."""
    print("Running integration stress test...")
    
    stress_scenarios = [
        {"name": "Multiple Teams", "teams": 3, "concurrent": True},
        {"name": "Large Team", "teams": 1, "team_size": 5},
        {"name": "Complex Topic", "teams": 1, "complexity": "high"}
    ]
    
    stress_results = {}
    
    for scenario in stress_scenarios:
        print(f"\\nTesting {scenario['name']} scenario...")
        
        scenario_start = time.time()
        teams = []
        results = []
        
        try:
            # Create teams based on scenario
            if scenario["name"] == "Multiple Teams":
                topics = [
                    "AI in Autonomous Vehicles",
                    "Quantum Computing Applications",
                    "Biotechnology Innovations"
                ]
                
                for i, topic in enumerate(topics):
                    team = EnhancedResearchTeam(topic, team_size=3)
                    teams.append(team)
                
                # Execute collaborations
                for team in teams:
                    result = team.collaborate()
                    results.append(result)
            
            elif scenario["name"] == "Large Team":
                team = EnhancedResearchTeam("Complex Research Topic", team_size=5)
                teams.append(team)
                result = team.collaborate(research_depth="exhaustive")
                results.append(result)
            
            elif scenario["name"] == "Complex Topic":
                complex_topic = ("Interdisciplinary Analysis of Socio-Economic Impacts "
                               "of Emerging Technologies on Global Healthcare Systems")
                team = EnhancedResearchTeam(complex_topic, team_size=4)
                teams.append(team)
                result = team.collaborate(
                    research_depth="exhaustive",
                    source_requirements="academic, industry, governmental, and international sources",
                    output_format="detailed_analysis"
                )
                results.append(result)
            
            scenario_end = time.time()
            scenario_time = scenario_end - scenario_start
            
            # Analyze results
            successful_results = [r for r in results if r.get("success", False)]
            success_rate = len(successful_results) / len(results) if results else 0
            
            avg_quality = sum(
                r.get("quality_assessment", {}).get("overall_score", 0) 
                for r in successful_results
            ) / len(successful_results) if successful_results else 0
            
            stress_results[scenario["name"].lower().replace(" ", "_")] = {
                "scenario": scenario,
                "teams_created": len(teams),
                "collaborations_executed": len(results),
                "success_rate": success_rate,
                "average_quality": avg_quality,
                "total_time": scenario_time,
                "successful": success_rate > 0.5  # 50% threshold
            }
            
            print(f"✅ {scenario['name']}: {success_rate:.1%} success rate, "
                  f"Avg quality: {avg_quality:.2f}, Time: {scenario_time:.2f}s")
            
        except Exception as e:
            print(f"❌ {scenario['name']}: Exception - {str(e)}")
            stress_results[scenario["name"].lower().replace(" ", "_")] = {
                "scenario": scenario,
                "successful": False,
                "error": str(e)
            }
        
        finally:
            # Cleanup all teams
            for team in teams:
                try:
                    team.cleanup()
                except:
                    pass  # Ignore cleanup errors
    
    # Overall stress test assessment
    successful_scenarios = [name for name, result in stress_results.items() if result.get("successful", False)]
    overall_success = len(successful_scenarios) / len(stress_scenarios)
    
    print(f"\\n📊 Stress test summary: {len(successful_scenarios)}/{len(stress_scenarios)} scenarios passed")
    print(f"Overall success rate: {overall_success:.1%}")
    
    return {
        "scenarios_tested": len(stress_scenarios),
        "successful_scenarios": len(successful_scenarios),
        "overall_success_rate": overall_success,
        "scenario_results": stress_results,
        "stress_test_passed": overall_success >= 0.67  # 67% threshold
    }


# Register all examples
runner.register_example(
    "basic_research_team",
    "Basic research team collaboration with 3 agents",
    basic_research_team_example
)

runner.register_example(
    "advanced_research_team",
    "Advanced research team with maximum configuration and specialized roles",
    advanced_research_team_example
)

runner.register_example(
    "role_specialization",
    "Individual role specialization showcase",
    role_specialization_example
)

runner.register_example(
    "workflow_orchestration",
    "Research workflow orchestration and phase management",
    workflow_orchestration_example
)

runner.register_example(
    "comparative_research",
    "Comparison of different research team configurations",
    comparative_research_example
)

runner.register_example(
    "integration_stress_test",
    "Stress test for research team integration and scalability",
    integration_stress_test
)


def main():
    """Main function to run research team examples."""
    print("Research Team Example Implementation")
    print("=" * 80)
    print("This module demonstrates the enhanced research team collaboration")
    print("capabilities using the multi-agent framework.")
    print()
    
    # Show available examples
    print("Available Examples:")
    for i, (name, info) in enumerate(runner.examples.items(), 1):
        print(f"{i}. {name}: {info['description']}")
    
    print()
    choice = input("Enter example number to run (or 'all' for all examples): ").strip().lower()
    
    if choice == 'all':
        # Run all examples
        results = runner.run_all_examples()
        
        # Generate summary report
        print("\\n" + "=" * 80)
        print("FINAL SUMMARY REPORT")
        print("=" * 80)
        
        total = len(results)
        successful = len([r for r in results.values() if r["success"]])
        
        print(f"Total examples run: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {total - successful}")
        print(f"Success rate: {successful/total:.1%}")
        
        if successful < total:
            print("\\nFailed examples:")
            for name, result in results.items():
                if not result["success"]:
                    print(f"  - {name}: {result['error']}")
        
        print("\\nExample execution times:")
        for name, result in results.items():
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {name}: {result['execution_time']:.2f}s")
    
    elif choice.isdigit():
        # Run specific example
        example_num = int(choice)
        example_names = list(runner.examples.keys())
        
        if 1 <= example_num <= len(example_names):
            example_name = example_names[example_num - 1]
            result = runner.run_example(example_name)
            
            print("\\n" + "=" * 60)
            print("EXAMPLE RESULT SUMMARY")
            print("=" * 60)
            print(f"Example: {result['name']}")
            print(f"Success: {'Yes' if result['success'] else 'No'}")
            print(f"Execution time: {result['execution_time']:.2f} seconds")
            
            if result['success'] and result['result']:
                print("\\nKey results:")
                for key, value in result['result'].items():
                    if isinstance(value, (str, int, float, bool)):
                        print(f"  {key}: {value}")
            elif not result['success']:
                print(f"Error: {result['error']}")
        else:
            print("Invalid example number!")
    
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()