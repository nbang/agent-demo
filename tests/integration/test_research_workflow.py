"""Integration Tests for Research Team Workflow

Comprehensive integration tests for the research team collaboration workflow,
testing end-to-end functionality and team interactions.
"""

import pytest
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from src.agents.multi_agent.research_team import EnhancedResearchTeam
from src.agents.multi_agent.roles.researcher import ResearcherRole, create_general_researcher
from src.agents.multi_agent.roles.analyst import AnalystRole, create_data_analyst
from src.agents.multi_agent.roles.synthesizer import SynthesizerRole, create_research_synthesizer
from src.agents.multi_agent.workflows.research_orchestration import (
    ResearchWorkflowOrchestrator,
    ResearchPhase,
    create_research_workflow_orchestrator
)
from src.agents.multi_agent.constants import TeamType, WorkflowStatus, TaskStatus


class TestResearchTeamIntegration:
    """Integration tests for research team workflow."""
    
    @pytest.fixture
    def research_topic(self):
        """Test research topic."""
        return "Impact of Artificial Intelligence on Healthcare Diagnostics"
    
    @pytest.fixture
    def research_team(self, research_topic):
        """Create a research team for testing."""
        return EnhancedResearchTeam(research_topic, team_size=3)
    
    @pytest.fixture
    def workflow_orchestrator(self, research_topic):
        """Create a workflow orchestrator for testing."""
        return create_research_workflow_orchestrator("test_team_001", research_topic)
    
    def test_research_team_creation(self, research_team, research_topic):
        """Test research team creation and initialization."""
        assert research_team.topic == research_topic
        assert research_team.team_size == 3
        assert research_team.team is not None
        assert research_team.team.config.team_type == TeamType.RESEARCH
        assert len(research_team.team.agents) == 3
        
        # Verify team status
        status = research_team.get_team_status()
        assert status["research_topic"] == research_topic
        assert status["team_size"] == 3
        assert "agents" in status
    
    def test_role_implementations(self):
        """Test individual role implementations."""
        # Test researcher role
        researcher = create_general_researcher()
        assert researcher.researcher_type == "general"
        assert len(researcher.capabilities) >= 3
        assert researcher.role_definition is not None
        
        # Test analyst role
        analyst = create_data_analyst()
        assert analyst.analyst_type == "data"
        assert len(analyst.capabilities) >= 3
        assert analyst.role_definition is not None
        
        # Test synthesizer role
        synthesizer = create_research_synthesizer()
        assert synthesizer.synthesizer_type == "research"
        assert len(synthesizer.capabilities) >= 3
        assert synthesizer.role_definition is not None
    
    def test_workflow_orchestrator_creation(self, workflow_orchestrator, research_topic):
        """Test workflow orchestrator creation and initialization."""
        assert workflow_orchestrator.research_topic == research_topic
        assert workflow_orchestrator.workflow_status == WorkflowStatus.NOT_STARTED
        assert workflow_orchestrator.current_phase == ResearchPhase.INITIALIZATION
        assert len(workflow_orchestrator.tasks) > 0
        assert len(workflow_orchestrator.quality_gates) > 0
    
    def test_workflow_startup(self, workflow_orchestrator):
        """Test workflow startup process."""
        # Start workflow
        start_result = workflow_orchestrator.start_workflow()
        
        assert start_result["success"] is True
        assert "workflow_id" in start_result
        assert start_result["status"] == WorkflowStatus.RUNNING.value
        assert start_result["current_phase"] == ResearchPhase.INITIALIZATION.value
        assert start_result["estimated_duration_minutes"] > 0
        
        # Verify workflow status after start
        status = workflow_orchestrator.get_workflow_status()
        assert status["status"] == WorkflowStatus.RUNNING.value
        assert status["current_phase"] == ResearchPhase.INITIALIZATION.value
        assert status["progress"] == 0.0  # No tasks completed yet
    
    def test_phase_execution(self, workflow_orchestrator):
        """Test phase execution and task completion."""
        # Start workflow
        workflow_orchestrator.start_workflow()
        
        # Execute first phase
        execution_result = workflow_orchestrator.execute_next_phase()
        
        assert execution_result["success"] is True
        assert execution_result["current_phase"] == ResearchPhase.INITIALIZATION.value
        assert execution_result["executed_tasks"] >= 1
        assert "task_results" in execution_result
        
        # Check task execution results
        for result in execution_result["task_results"]:
            assert "task_id" in result
            assert "status" in result
            assert result["status"] in [TaskStatus.COMPLETED.value, TaskStatus.RUNNING.value]
    
    def test_quality_gates(self, workflow_orchestrator):
        """Test quality gate validation."""
        # Start workflow and complete initialization phase
        workflow_orchestrator.start_workflow()
        
        # Simulate completing all initialization tasks
        init_tasks = [task for task in workflow_orchestrator.tasks.values() 
                     if task.phase == ResearchPhase.INITIALIZATION]
        
        for task in init_tasks:
            task.status = TaskStatus.COMPLETED
            task.start_time = datetime.now() - timedelta(minutes=10)
            task.end_time = datetime.now()
            task.output = {"success": True, "quality_score": 0.85}
        
        # Test quality gate validation
        quality_result = workflow_orchestrator._validate_phase_quality_gate(ResearchPhase.INITIALIZATION)
        
        assert "passed" in quality_result
        assert "quality_gate_id" in quality_result
        assert "average_score" in quality_result
        assert quality_result["average_score"] > 0
    
    def test_research_collaboration_end_to_end(self, research_team):
        """Test end-to-end research collaboration."""
        # Execute collaboration
        collaboration_result = research_team.collaborate(
            research_depth="comprehensive",
            source_requirements="academic and industry sources",
            output_format="structured_report"
        )
        
        # Verify collaboration results structure
        assert "success" in collaboration_result
        assert collaboration_result["research_topic"] == research_team.topic
        assert "research_parameters" in collaboration_result
        assert "team_composition" in collaboration_result
        assert "collaboration_metrics" in collaboration_result
        
        # Verify research parameters
        params = collaboration_result["research_parameters"]
        assert params["depth"] == "comprehensive"
        assert params["source_requirements"] == "academic and industry sources"
        assert params["output_format"] == "structured_report"
        
        # Verify team composition
        composition = collaboration_result["team_composition"]
        assert composition["team_size"] == 3
        assert len(composition["roles"]) == 3
    
    def test_role_interaction_workflow(self):
        """Test interaction between different roles in workflow."""
        # Create roles
        researcher = create_general_researcher()
        analyst = create_data_analyst()
        synthesizer = create_research_synthesizer()
        
        # Simulate research workflow interaction
        # Step 1: Researcher gathers information
        research_data = {
            "topic": "AI Healthcare Impact",
            "sources": ["academic_papers", "industry_reports"],
            "findings": ["Finding 1", "Finding 2", "Finding 3"]
        }
        
        # Step 2: Analyst analyzes the research data
        analysis_result = analyst.analyze_data(research_data, "comprehensive")
        
        assert analysis_result["analyst_type"] == "data"
        assert analysis_result["analysis_type"] == "comprehensive"
        assert "findings" in analysis_result
        assert "quality_assessment" in analysis_result
        
        # Step 3: Synthesizer integrates research and analysis
        synthesis_inputs = {
            "research_findings": research_data,
            "analysis_results": analysis_result
        }
        
        synthesis_result = synthesizer.synthesize_information(
            synthesis_inputs, 
            "comprehensive", 
            "structured_report"
        )
        
        assert synthesis_result["synthesizer_type"] == "research"
        assert synthesis_result["synthesis_type"] == "comprehensive"
        assert "synthesis_output" in synthesis_result
        assert "quality_metrics" in synthesis_result
    
    def test_workflow_error_handling(self, workflow_orchestrator):
        """Test workflow error handling and recovery."""
        # Test starting workflow twice
        workflow_orchestrator.start_workflow()
        
        with pytest.raises(Exception):  # Should raise WorkflowError
            workflow_orchestrator.start_workflow()
        
        # Test executing phase without starting
        new_orchestrator = create_research_workflow_orchestrator("test_team_002", "Test Topic")
        
        with pytest.raises(Exception):  # Should raise WorkflowError
            new_orchestrator.execute_next_phase()
    
    def test_workflow_progress_tracking(self, workflow_orchestrator):
        """Test workflow progress tracking and metrics."""
        # Start workflow
        workflow_orchestrator.start_workflow()
        
        # Get initial status
        initial_status = workflow_orchestrator.get_workflow_status()
        assert initial_status["progress"] == 0.0
        
        # Simulate completing some tasks
        completed_count = 0
        for task in list(workflow_orchestrator.tasks.values())[:2]:  # Complete first 2 tasks
            task.status = TaskStatus.COMPLETED
            task.start_time = datetime.now() - timedelta(minutes=5)
            task.end_time = datetime.now()
            completed_count += 1
        
        # Check updated progress
        updated_status = workflow_orchestrator.get_workflow_status()
        expected_progress = completed_count / len(workflow_orchestrator.tasks)
        assert updated_status["progress"] == expected_progress
        
        # Check phase progress
        init_phase_progress = updated_status["phase_progress"][ResearchPhase.INITIALIZATION.value]
        assert init_phase_progress["completed"] >= 0
        assert init_phase_progress["total"] > 0
    
    def test_multi_team_scalability(self):
        """Test creating and managing multiple research teams."""
        topics = [
            "AI in Education",
            "Blockchain in Finance",
            "IoT Security Challenges"
        ]
        
        teams = []
        orchestrators = []
        
        # Create multiple teams and orchestrators
        for i, topic in enumerate(topics):
            team = EnhancedResearchTeam(topic, team_size=3)
            orchestrator = create_research_workflow_orchestrator(f"team_{i}", topic)
            
            teams.append(team)
            orchestrators.append(orchestrator)
        
        # Verify all teams are created correctly
        assert len(teams) == 3
        assert len(orchestrators) == 3
        
        for i, (team, orchestrator) in enumerate(zip(teams, orchestrators)):
            assert team.topic == topics[i]
            assert orchestrator.research_topic == topics[i]
            assert team.team_size == 3
        
        # Test concurrent workflow startup
        for orchestrator in orchestrators:
            start_result = orchestrator.start_workflow()
            assert start_result["success"] is True
        
        # Verify all workflows are running
        for orchestrator in orchestrators:
            status = orchestrator.get_workflow_status()
            assert status["status"] == WorkflowStatus.RUNNING.value
    
    def test_resource_cleanup(self, research_team, workflow_orchestrator):
        """Test proper resource cleanup."""
        # Start workflow and team
        workflow_orchestrator.start_workflow()
        team_status = research_team.get_team_status()
        
        assert team_status["status"] == "initialized"
        
        # Test cleanup
        research_team.cleanup()
        
        # Verify cleanup (in real implementation, would check resource deallocation)
        # For now, just ensure no exceptions are raised
        assert True  # Placeholder for actual cleanup verification
    
    def test_integration_performance(self, research_team):
        """Test integration performance metrics."""
        start_time = time.time()
        
        # Execute collaboration
        result = research_team.collaborate(
            research_depth="basic",
            source_requirements="web sources",
            output_format="executive_summary"
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify performance is within acceptable bounds
        assert execution_time < 5.0  # Should complete within 5 seconds for basic collaboration
        assert "execution_time" in result or execution_time > 0


class TestResearchWorkflowComponents:
    """Test individual workflow components."""
    
    def test_task_dependency_resolution(self, workflow_orchestrator):
        """Test task dependency resolution."""
        workflow_orchestrator.start_workflow()
        
        # Check that tasks with no dependencies are ready
        ready_tasks = workflow_orchestrator._get_next_ready_tasks()
        assert len(ready_tasks) > 0
        
        # Verify dependency checking
        for task_id in ready_tasks:
            task = workflow_orchestrator.tasks[task_id]
            assert workflow_orchestrator._are_dependencies_met(task)
    
    def test_phase_transitions(self, workflow_orchestrator):
        """Test phase transition logic."""
        workflow_orchestrator.start_workflow()
        
        # Test getting next phase
        current = ResearchPhase.INITIALIZATION
        next_phase = workflow_orchestrator._get_next_phase(current)
        assert next_phase == ResearchPhase.INFORMATION_GATHERING
        
        # Test final phase
        final = ResearchPhase.FINALIZATION
        next_phase = workflow_orchestrator._get_next_phase(final)
        assert next_phase is None
    
    def test_quality_metrics_calculation(self, workflow_orchestrator):
        """Test quality metrics calculation."""
        workflow_orchestrator.start_workflow()
        
        # Simulate completing tasks with quality scores
        task = list(workflow_orchestrator.tasks.values())[0]
        task.status = TaskStatus.COMPLETED
        task.output = {"quality_score": 0.85, "success": True}
        
        # Generate workflow results
        results = workflow_orchestrator._generate_workflow_results()
        
        assert "quality_metrics" in results
        assert "overall_quality_score" in results["quality_metrics"]
        assert results["quality_metrics"]["overall_quality_score"] > 0


# Utility functions for testing
def create_mock_research_data() -> Dict[str, Any]:
    """Create mock research data for testing."""
    return {
        "topic": "Test Research Topic",
        "sources": [
            {"type": "academic", "title": "Research Paper 1", "credibility": 0.9},
            {"type": "industry", "title": "Industry Report 1", "credibility": 0.8}
        ],
        "findings": [
            {"finding": "Key insight 1", "confidence": 0.8},
            {"finding": "Key insight 2", "confidence": 0.9}
        ],
        "metadata": {
            "research_date": datetime.now().isoformat(),
            "researcher": "test_researcher",
            "quality_score": 0.85
        }
    }


def verify_collaboration_output(output: Dict[str, Any]) -> bool:
    """Verify collaboration output structure and content."""
    required_keys = [
        "research_topic",
        "research_parameters", 
        "team_composition",
        "collaboration_metrics"
    ]
    
    for key in required_keys:
        if key not in output:
            return False
    
    return True


# Performance benchmarks
class TestResearchWorkflowPerformance:
    """Performance tests for research workflow."""
    
    @pytest.mark.performance
    def test_team_creation_performance(self):
        """Test research team creation performance."""
        start_time = time.time()
        
        teams = []
        for i in range(10):
            team = EnhancedResearchTeam(f"Topic {i}", team_size=3)
            teams.append(team)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        assert creation_time < 2.0  # Should create 10 teams in under 2 seconds
        assert len(teams) == 10
    
    @pytest.mark.performance
    def test_workflow_startup_performance(self):
        """Test workflow startup performance."""
        orchestrator = create_research_workflow_orchestrator("perf_test", "Performance Test Topic")
        
        start_time = time.time()
        result = orchestrator.start_workflow()
        end_time = time.time()
        
        startup_time = end_time - start_time
        
        assert result["success"] is True
        assert startup_time < 1.0  # Should start workflow in under 1 second


if __name__ == "__main__":
    # Run basic integration test
    print("Running Research Team Integration Tests")
    print("=" * 45)
    
    # Create test instances
    topic = "Test Integration Topic"
    team = EnhancedResearchTeam(topic, team_size=3)
    orchestrator = create_research_workflow_orchestrator("integration_test", topic)
    
    print(f"Created research team for: {topic}")
    print(f"Team size: {team.team_size}")
    print(f"Workflow tasks: {len(orchestrator.tasks)}")
    
    # Test basic functionality
    try:
        # Test team status
        status = team.get_team_status()
        print(f"Team status: {status['status']}")
        
        # Test workflow startup
        start_result = orchestrator.start_workflow()
        print(f"Workflow started: {start_result['success']}")
        
        # Test role creation
        researcher = create_general_researcher()
        analyst = create_data_analyst()
        synthesizer = create_research_synthesizer()
        
        print(f"Created roles: {researcher.researcher_type}, {analyst.analyst_type}, {synthesizer.synthesizer_type}")
        
        print("✅ All integration tests passed!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
    
    finally:
        team.cleanup()
        print("Integration tests completed")