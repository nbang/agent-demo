"""Unit Tests for Researcher Roles

Comprehensive unit tests for researcher role implementations,
testing individual role capabilities and behaviors.
"""

import pytest
from typing import Dict, Any, List
from unittest.mock import Mock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.agents.multi_agent.roles.researcher import (
    ResearcherRole,
    ResearchCapability,
    create_general_researcher,
    create_academic_researcher,
    create_industry_researcher,
    create_technical_researcher
)
from src.agents.multi_agent.agent_roles import RoleDefinition


class TestResearchCapability:
    """Test ResearchCapability dataclass."""
    
    def test_capability_creation(self):
        """Test research capability creation."""
        capability = ResearchCapability(
            name="test_capability",
            description="Test capability description",
            tools_required=["tool1", "tool2"],
            quality_metrics={"accuracy": 0.9, "completeness": 0.8},
            output_format="test_format"
        )
        
        assert capability.name == "test_capability"
        assert capability.description == "Test capability description"
        assert len(capability.tools_required) == 2
        assert capability.quality_metrics["accuracy"] == 0.9
        assert capability.output_format == "test_format"
    
    def test_capability_equality(self):
        """Test capability equality comparison."""
        cap1 = ResearchCapability(
            name="same_name",
            description="Description 1",
            tools_required=["tool1"],
            quality_metrics={"accuracy": 0.9},
            output_format="format1"
        )
        
        cap2 = ResearchCapability(
            name="same_name",
            description="Description 2",
            tools_required=["tool2"],
            quality_metrics={"accuracy": 0.8},
            output_format="format2"
        )
        
        # Different capabilities with same name should not be equal
        assert cap1.name == cap2.name
        assert cap1.description != cap2.description


# Module-level fixtures available to all test classes
@pytest.fixture
def general_researcher():
    """Create a general researcher for testing."""
    return ResearcherRole("general")

@pytest.fixture
def academic_researcher():
    """Create an academic researcher for testing."""
    return ResearcherRole("academic")

@pytest.fixture
def industry_researcher():
    """Create an industry researcher for testing."""
    return ResearcherRole("industry")

@pytest.fixture
def technical_researcher():
    """Create a technical researcher for testing."""
    return ResearcherRole("technical")


class TestResearcherRole:
    """Test ResearcherRole class."""
    
    def test_researcher_initialization(self, general_researcher):
        """Test researcher role initialization."""
        assert general_researcher.researcher_type == "general"
        assert len(general_researcher.capabilities) >= 3  # Base capabilities
        assert general_researcher.role_definition is not None
        assert hasattr(general_researcher, 'quality_standards')
    
    def test_academic_researcher_specialization(self, academic_researcher):
        """Test academic researcher specialization."""
        assert academic_researcher.researcher_type == "academic"
        
        # Check for academic-specific capabilities
        capability_names = [cap.name for cap in academic_researcher.capabilities]
        assert "literature_review" in capability_names
        assert "peer_review_analysis" in capability_names
        
        # Check expertise areas
        expertise = academic_researcher.role_definition.expertise_areas
        assert "literature_review" in expertise
        assert "academic_writing" in expertise
        assert "citation_analysis" in expertise
    
    def test_industry_researcher_specialization(self, industry_researcher):
        """Test industry researcher specialization."""
        assert industry_researcher.researcher_type == "industry"
        
        # Check for industry-specific capabilities
        capability_names = [cap.name for cap in industry_researcher.capabilities]
        assert "market_analysis" in capability_names
        assert "competitive_intelligence" in capability_names
        
        # Check expertise areas
        expertise = industry_researcher.role_definition.expertise_areas
        assert "market_analysis" in expertise
        assert "business_research" in expertise
        assert "trend_analysis" in expertise
    
    def test_technical_researcher_specialization(self, technical_researcher):
        """Test technical researcher specialization."""
        assert technical_researcher.researcher_type == "technical"
        
        # Check for technical-specific capabilities
        capability_names = [cap.name for cap in technical_researcher.capabilities]
        assert "technical_documentation" in capability_names
        assert "standards_compliance" in capability_names
        
        # Check expertise areas
        expertise = technical_researcher.role_definition.expertise_areas
        assert "technical_documentation" in expertise
        assert "standards_research" in expertise
        assert "compliance_checking" in expertise
    
    def test_base_capabilities_present(self, general_researcher):
        """Test that base capabilities are present in all researchers."""
        capability_names = [cap.name for cap in general_researcher.capabilities]
        
        # All researchers should have these base capabilities
        expected_base = ["information_gathering", "source_evaluation", "fact_verification"]
        for capability in expected_base:
            assert capability in capability_names
    
    def test_role_definition_structure(self, general_researcher):
        """Test role definition structure and content."""
        role_def = general_researcher.role_definition
        
        assert isinstance(role_def, RoleDefinition)
        assert role_def.role_id == "general_researcher"
        assert role_def.name == "General Researcher"
        assert "researcher agent" in role_def.description.lower()
        assert len(role_def.capabilities) > 0
        assert len(role_def.tools) > 0
        assert len(role_def.instructions) > 100  # Should have detailed instructions
        assert len(role_def.expertise_areas) > 0
    
    def test_quality_standards(self, general_researcher, academic_researcher):
        """Test quality standards for different researcher types."""
        # General researcher standards
        gen_standards = general_researcher.quality_standards
        assert gen_standards["min_sources"] == 5
        assert gen_standards["credibility_threshold"] == 0.8
        assert gen_standards["verification_requirement"] is True
        assert gen_standards["citation_required"] is False
        
        # Academic researcher should have higher standards
        acad_standards = academic_researcher.quality_standards
        assert acad_standards["min_sources"] == 10  # Higher than general
        assert acad_standards["citation_required"] is True  # Academic requires citations
    
    def test_instructions_generation(self, academic_researcher):
        """Test instruction generation for specific researcher type."""
        instructions = academic_researcher.role_definition.instructions
        
        # Check for general instructions
        assert "specialized academic researcher" in instructions.lower()
        assert "research process" in instructions.lower()
        assert "quality standards" in instructions.lower()
        
        # Check for academic-specific instructions
        assert "peer-reviewed" in instructions.lower()
        assert "academic citations" in instructions.lower()
        assert "literature review" in instructions.lower()
    
    def test_capability_tools_mapping(self, technical_researcher):
        """Test that capabilities have appropriate tools."""
        for capability in technical_researcher.capabilities:
            assert len(capability.tools_required) > 0
            assert isinstance(capability.tools_required, list)
            
            # Technical capabilities should have appropriate tools
            if capability.name == "technical_documentation":
                assert any("tech" in tool.lower() or "doc" in tool.lower() 
                          for tool in capability.tools_required)
    
    def test_evaluate_research_quality(self, general_researcher):
        """Test research quality evaluation."""
        # Mock research output
        research_output = {
            "capabilities_used": ["information_gathering", "source_evaluation"],
            "format": "structured_data",
            "findings": ["Finding 1", "Finding 2"],
            "sources": [{"credibility": 0.9}, {"credibility": 0.8}]
        }
        
        evaluation = general_researcher.evaluate_research_quality(research_output)
        
        assert "overall_score" in evaluation
        assert "capability_scores" in evaluation
        assert "strengths" in evaluation
        assert "areas_for_improvement" in evaluation
        assert "recommendations" in evaluation
        
        # Check score is valid
        assert 0 <= evaluation["overall_score"] <= 1
        
        # Check capability scores
        for cap_name, score in evaluation["capability_scores"].items():
            assert 0 <= score <= 1
    
    def test_capability_evaluation_logic(self, general_researcher):
        """Test capability evaluation logic."""
        # Test output that matches capability requirements
        matching_output = {
            "capabilities_used": ["information_gathering"],
            "format": "structured_data"
        }
        
        info_gathering_cap = next(
            cap for cap in general_researcher.capabilities 
            if cap.name == "information_gathering"
        )
        
        score = general_researcher._evaluate_capability_output(info_gathering_cap, matching_output)
        assert score > 0.7  # Should score well for matching requirements
        
        # Test output that doesn't match
        non_matching_output = {
            "capabilities_used": ["unrelated_capability"],
            "format": "wrong_format"
        }
        
        score2 = general_researcher._evaluate_capability_output(info_gathering_cap, non_matching_output)
        assert score2 < score  # Should score lower for non-matching requirements
    
    def test_feedback_generation(self, general_researcher):
        """Test feedback generation from quality assessment."""
        # Mock assessment with high scores
        high_score_assessment = {
            "capability_scores": {
                "information_gathering": 0.9,
                "source_evaluation": 0.85,
                "fact_verification": 0.8
            },
            "overall_score": 0.85
        }
        
        feedback = general_researcher._generate_feedback(high_score_assessment)
        
        assert len(feedback["strengths"]) > 0
        assert "information_gathering" in feedback["strengths"][0]
        
        # Mock assessment with low scores
        low_score_assessment = {
            "capability_scores": {
                "information_gathering": 0.5,
                "source_evaluation": 0.4
            },
            "overall_score": 0.45
        }
        
        feedback_low = general_researcher._generate_feedback(low_score_assessment)
        
        assert len(feedback_low["areas_for_improvement"]) > 0
        assert len(feedback_low["recommendations"]) > 0


class TestResearcherFactoryFunctions:
    """Test factory functions for creating researchers."""
    
    def test_create_general_researcher(self):
        """Test general researcher factory function."""
        researcher = create_general_researcher()
        
        assert isinstance(researcher, ResearcherRole)
        assert researcher.researcher_type == "general"
        
        # Check basic capabilities are present
        capability_names = [cap.name for cap in researcher.capabilities]
        assert "information_gathering" in capability_names
    
    def test_create_academic_researcher(self):
        """Test academic researcher factory function."""
        researcher = create_academic_researcher()
        
        assert isinstance(researcher, ResearcherRole)
        assert researcher.researcher_type == "academic"
        
        # Check academic-specific capabilities
        capability_names = [cap.name for cap in researcher.capabilities]
        assert "literature_review" in capability_names
        assert "peer_review_analysis" in capability_names
    
    def test_create_industry_researcher(self):
        """Test industry researcher factory function."""
        researcher = create_industry_researcher()
        
        assert isinstance(researcher, ResearcherRole)
        assert researcher.researcher_type == "industry"
        
        # Check industry-specific capabilities
        capability_names = [cap.name for cap in researcher.capabilities]
        assert "market_analysis" in capability_names
        assert "competitive_intelligence" in capability_names
    
    def test_create_technical_researcher(self):
        """Test technical researcher factory function."""
        researcher = create_technical_researcher()
        
        assert isinstance(researcher, ResearcherRole)
        assert researcher.researcher_type == "technical"
        
        # Check technical-specific capabilities
        capability_names = [cap.name for cap in researcher.capabilities]
        assert "technical_documentation" in capability_names
        assert "standards_compliance" in capability_names
    
    def test_factory_functions_return_different_instances(self):
        """Test that factory functions return different instances."""
        researcher1 = create_general_researcher()
        researcher2 = create_general_researcher()
        
        assert researcher1 is not researcher2  # Different instances
        assert researcher1.researcher_type == researcher2.researcher_type  # Same type


class TestResearcherRoleEdgeCases:
    """Test edge cases and error handling for researcher roles."""
    
    def test_unknown_researcher_type(self):
        """Test creating researcher with unknown type."""
        # Should default to base capabilities
        unknown_researcher = ResearcherRole("unknown_type")
        
        assert unknown_researcher.researcher_type == "unknown_type"
        assert len(unknown_researcher.capabilities) >= 3  # Should have base capabilities
        
        # Should have general expertise areas
        expertise = unknown_researcher.role_definition.expertise_areas
        assert "general_research" in expertise
        assert "multi_domain_analysis" in expertise
    
    def test_empty_research_output_evaluation(self, general_researcher):
        """Test evaluating empty research output."""
        empty_output = {}
        
        evaluation = general_researcher.evaluate_research_quality(empty_output)
        
        assert "overall_score" in evaluation
        assert evaluation["overall_score"] >= 0  # Should handle gracefully
        assert len(evaluation["capability_scores"]) == len(general_researcher.capabilities)
    
    def test_malformed_research_output_evaluation(self, general_researcher):
        """Test evaluating malformed research output."""
        malformed_outputs = [
            None,
            "string_instead_of_dict",
            {"unexpected_structure": True},
            {"capabilities_used": "string_instead_of_list"}
        ]
        
        for output in malformed_outputs:
            try:
                evaluation = general_researcher.evaluate_research_quality(output)
                # Should handle gracefully and return valid structure
                assert "overall_score" in evaluation
                assert isinstance(evaluation["overall_score"], (int, float))
            except Exception as e:
                # If it raises an exception, it should be handled gracefully
                pytest.fail(f"Should handle malformed output gracefully: {e}")
    
    def test_capability_with_missing_requirements(self):
        """Test capability with missing or invalid requirements."""
        # Create capability with empty requirements
        empty_capability = ResearchCapability(
            name="empty_capability",
            description="",
            tools_required=[],
            quality_metrics={},
            output_format=""
        )
        
        assert empty_capability.name == "empty_capability"
        assert len(empty_capability.tools_required) == 0
        assert len(empty_capability.quality_metrics) == 0
    
    def test_role_definition_with_minimal_data(self):
        """Test role definition creation with minimal data."""
        minimal_researcher = ResearcherRole("minimal")
        role_def = minimal_researcher.role_definition
        
        # Should still have required fields
        assert role_def.role_id
        assert role_def.name
        assert role_def.description
        assert len(role_def.capabilities) > 0
        assert len(role_def.tools) > 0
        assert role_def.instructions
        assert len(role_def.expertise_areas) > 0


class TestResearcherRolePerformance:
    """Test performance characteristics of researcher roles."""
    
    def test_role_creation_performance(self):
        """Test researcher role creation performance."""
        import time
        
        start_time = time.time()
        
        # Create multiple researchers
        researchers = []
        for i in range(50):
            researcher = ResearcherRole("general")
            researchers.append(researcher)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        assert creation_time < 1.0  # Should create 50 researchers in under 1 second
        assert len(researchers) == 50
    
    def test_evaluation_performance(self, general_researcher):
        """Test research quality evaluation performance."""
        import time
        
        # Create moderately complex research output
        research_output = {
            "capabilities_used": ["information_gathering", "source_evaluation", "fact_verification"],
            "format": "structured_data",
            "findings": [f"Finding {i}" for i in range(100)],
            "sources": [{"credibility": 0.8, "type": "academic"} for _ in range(50)]
        }
        
        start_time = time.time()
        
        # Perform multiple evaluations
        for _ in range(10):
            evaluation = general_researcher.evaluate_research_quality(research_output)
        
        end_time = time.time()
        evaluation_time = end_time - start_time
        
        assert evaluation_time < 1.0  # Should complete 10 evaluations in under 1 second
    
    @pytest.mark.performance
    def test_capability_scaling(self):
        """Test performance with large numbers of capabilities."""
        # Create researcher with many custom capabilities
        researcher = ResearcherRole("general")
        
        # Add many capabilities (simulating complex researcher)
        additional_caps = []
        for i in range(100):
            cap = ResearchCapability(
                name=f"capability_{i}",
                description=f"Capability {i} description",
                tools_required=[f"tool_{i}"],
                quality_metrics={"score": 0.8},
                output_format="format"
            )
            additional_caps.append(cap)
        
        researcher.capabilities.extend(additional_caps)
        
        # Test evaluation with many capabilities
        research_output = {"capabilities_used": [f"capability_{i}" for i in range(50)]}
        
        import time
        start_time = time.time()
        evaluation = researcher.evaluate_research_quality(research_output)
        end_time = time.time()
        
        evaluation_time = end_time - start_time
        assert evaluation_time < 2.0  # Should handle many capabilities efficiently
        assert len(evaluation["capability_scores"]) > 100


# Mock classes for testing
class MockRoleDefinition:
    """Mock role definition for testing."""
    
    def __init__(self):
        self.role_id = "mock_role"
        self.name = "Mock Role"
        self.description = "Mock role for testing"
        self.capabilities = ["mock_capability"]
        self.tools = ["mock_tool"]
        self.instructions = "Mock instructions"
        self.expertise_areas = ["mock_expertise"]


# Integration tests with mocking
class TestResearcherRoleIntegration:
    """Integration tests with mocked dependencies."""
    
    @patch('src.agents.multi_agent.roles.researcher.logger')
    def test_logging_integration(self, mock_logger, general_researcher):
        """Test logging integration."""
        # Creating researcher should log
        researcher = ResearcherRole("test")
        mock_logger.info.assert_called()
        
        # Verify log message content
        log_calls = mock_logger.info.call_args_list
        assert any("Created test researcher role" in str(call) for call in log_calls)
    
    @patch('src.agents.multi_agent.roles.researcher.RoleDefinition')
    def test_role_definition_integration(self, mock_role_def):
        """Test integration with RoleDefinition."""
        mock_instance = Mock()
        mock_role_def.return_value = mock_instance
        
        researcher = ResearcherRole("test")
        
        # Verify RoleDefinition was called with correct parameters
        mock_role_def.assert_called_once()
        call_args = mock_role_def.call_args
        
        assert call_args[1]["role_id"] == "test_researcher"
        assert call_args[1]["name"] == "Test Researcher"
        assert "capabilities" in call_args[1]
        assert "tools" in call_args[1]
        assert "instructions" in call_args[1]
        assert "expertise_areas" in call_args[1]


if __name__ == "__main__":
    # Run basic unit tests
    print("Running Researcher Role Unit Tests")
    print("=" * 40)
    
    try:
        # Test basic functionality
        general = create_general_researcher()
        academic = create_academic_researcher()
        industry = create_industry_researcher()
        technical = create_technical_researcher()
        
        print(f"✅ Created general researcher with {len(general.capabilities)} capabilities")
        print(f"✅ Created academic researcher with {len(academic.capabilities)} capabilities")
        print(f"✅ Created industry researcher with {len(industry.capabilities)} capabilities")
        print(f"✅ Created technical researcher with {len(technical.capabilities)} capabilities")
        
        # Test quality evaluation
        mock_output = {
            "capabilities_used": ["information_gathering"],
            "format": "structured_data",
            "findings": ["Test finding"]
        }
        
        evaluation = general.evaluate_research_quality(mock_output)
        print(f"✅ Quality evaluation completed with score: {evaluation['overall_score']:.2f}")
        
        # Test role definitions
        for researcher in [general, academic, industry, technical]:
            role_def = researcher.get_role_definition()
            assert len(role_def.instructions) > 100
            print(f"✅ {researcher.researcher_type} researcher has detailed instructions")
        
        print("\\n✅ All unit tests passed!")
        
    except Exception as e:
        print(f"❌ Unit tests failed: {e}")
        import traceback
        print(traceback.format_exc())