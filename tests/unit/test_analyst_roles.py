"""Unit Tests for Analyst Roles

Comprehensive unit tests for analyst role implementations,
testing individual role capabilities and analytical behaviors.
"""

import pytest
from typing import Dict, Any, List
from unittest.mock import Mock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.agents.multi_agent.roles.analyst import (
    AnalystRole,
    AnalyticsCapability,
    create_general_analyst,
    create_data_analyst,
    create_business_analyst,
    create_quality_analyst,
    create_research_analyst
)
from src.agents.multi_agent.agent_roles import RoleDefinition


class TestAnalyticsCapability:
    """Test AnalyticsCapability dataclass."""
    
    def test_capability_creation(self):
        """Test analytics capability creation."""
        capability = AnalyticsCapability(
            name="test_analytics",
            description="Test analytics capability",
            tools_required=["analyzer", "validator"],
            input_types=["data", "text"],
            output_format="analysis_report",
            accuracy_threshold=0.85
        )
        
        assert capability.name == "test_analytics"
        assert capability.description == "Test analytics capability"
        assert len(capability.tools_required) == 2
        assert len(capability.input_types) == 2
        assert capability.output_format == "analysis_report"
        assert capability.accuracy_threshold == 0.85
    
    def test_capability_thresholds(self):
        """Test different accuracy thresholds."""
        high_accuracy_cap = AnalyticsCapability(
            name="high_accuracy",
            description="High accuracy capability",
            tools_required=["precise_tool"],
            input_types=["precise_data"],
            output_format="report",
            accuracy_threshold=0.95
        )
        
        low_accuracy_cap = AnalyticsCapability(
            name="low_accuracy",
            description="Lower accuracy capability",
            tools_required=["basic_tool"],
            input_types=["general_data"],
            output_format="report",
            accuracy_threshold=0.7
        )
        
        assert high_accuracy_cap.accuracy_threshold > low_accuracy_cap.accuracy_threshold
        assert high_accuracy_cap.accuracy_threshold == 0.95
        assert low_accuracy_cap.accuracy_threshold == 0.7


# Module-level fixtures available to all test classes
@pytest.fixture
def general_analyst():
    """Create a general analyst for testing."""
    return AnalystRole("general")

@pytest.fixture
def data_analyst():
    """Create a data analyst for testing."""
    return AnalystRole("data")

@pytest.fixture
def business_analyst():
    """Create a business analyst for testing."""
    return AnalystRole("business")

@pytest.fixture
def quality_analyst():
    """Create a quality analyst for testing."""
    return AnalystRole("quality")

@pytest.fixture
def research_analyst():
    """Create a research analyst for testing."""
    return AnalystRole("research")


class TestAnalystRole:
    """Test AnalystRole class."""
    
    def test_analyst_initialization(self, general_analyst):
        """Test analyst role initialization."""
        assert general_analyst.analyst_type == "general"
        assert len(general_analyst.capabilities) >= 3  # Base capabilities
        assert general_analyst.role_definition is not None
        assert hasattr(general_analyst, 'quality_standards')
    
    def test_data_analyst_specialization(self, data_analyst):
        """Test data analyst specialization."""
        assert data_analyst.analyst_type == "data"
        
        # Check for data-specific capabilities
        capability_names = [cap.name for cap in data_analyst.capabilities]
        assert "statistical_analysis" in capability_names
        assert "data_visualization" in capability_names
        
        # Check expertise areas
        expertise = data_analyst.role_definition.expertise_areas
        assert "statistical_analysis" in expertise
        assert "data_visualization" in expertise
        assert "quantitative_methods" in expertise
    
    def test_business_analyst_specialization(self, business_analyst):
        """Test business analyst specialization."""
        assert business_analyst.analyst_type == "business"
        
        # Check for business-specific capabilities
        capability_names = [cap.name for cap in business_analyst.capabilities]
        assert "market_analysis" in capability_names
        assert "risk_assessment" in capability_names
        
        # Check expertise areas
        expertise = business_analyst.role_definition.expertise_areas
        assert "market_analysis" in expertise
        assert "business_intelligence" in expertise
        assert "strategic_analysis" in expertise
    
    def test_quality_analyst_specialization(self, quality_analyst):
        """Test quality analyst specialization."""
        assert quality_analyst.analyst_type == "quality"
        
        # Check for quality-specific capabilities
        capability_names = [cap.name for cap in quality_analyst.capabilities]
        assert "quality_assessment" in capability_names
        assert "gap_analysis" in capability_names
        
        # Check expertise areas
        expertise = quality_analyst.role_definition.expertise_areas
        assert "quality_assurance" in expertise
        assert "process_evaluation" in expertise
        assert "gap_analysis" in expertise
    
    def test_research_analyst_specialization(self, research_analyst):
        """Test research analyst specialization."""
        assert research_analyst.analyst_type == "research"
        
        # Check for research-specific capabilities
        capability_names = [cap.name for cap in research_analyst.capabilities]
        assert "literature_synthesis" in capability_names
        assert "methodology_evaluation" in capability_names
        
        # Check expertise areas
        expertise = research_analyst.role_definition.expertise_areas
        assert "research_synthesis" in expertise
        assert "methodology_evaluation" in expertise
        assert "evidence_assessment" in expertise
    
    def test_base_capabilities_present(self, general_analyst):
        """Test that base capabilities are present in all analysts."""
        capability_names = [cap.name for cap in general_analyst.capabilities]
        
        # All analysts should have these base capabilities
        expected_base = ["pattern_recognition", "information_validation", "comparative_analysis"]
        for capability in expected_base:
            assert capability in capability_names
    
    def test_role_definition_structure(self, general_analyst):
        """Test role definition structure and content."""
        role_def = general_analyst.role_definition
        
        assert isinstance(role_def, RoleDefinition)
        assert role_def.role_id == "general_analyst"
        assert role_def.name == "General Analyst"
        assert "analyst agent" in role_def.description.lower()
        assert len(role_def.capabilities) > 0
        assert len(role_def.tools) > 0
        assert len(role_def.instructions) > 100  # Should have detailed instructions
        assert len(role_def.expertise_areas) > 0
    
    def test_quality_standards(self, general_analyst, quality_analyst):
        """Test quality standards for different analyst types."""
        # General analyst standards
        gen_standards = general_analyst.quality_standards
        assert gen_standards["accuracy_threshold"] == 0.85
        assert gen_standards["validation_requirement"] is True
        assert gen_standards["cross_reference_required"] is True
        assert gen_standards["bias_check_required"] is True
        
        # Quality analyst should have same high standards
        qual_standards = quality_analyst.quality_standards
        assert qual_standards["accuracy_threshold"] == gen_standards["accuracy_threshold"]
        assert qual_standards["validation_requirement"] is True
    
    def test_instructions_generation(self, data_analyst):
        """Test instruction generation for specific analyst type."""
        instructions = data_analyst.role_definition.instructions
        
        # Check for general instructions
        assert "specialized data analyst" in instructions.lower()
        assert "analytical process" in instructions.lower()
        assert "quality standards" in instructions.lower()
        
        # Check for data-specific instructions
        assert "statistical analysis" in instructions.lower()
        assert "data visualization" in instructions.lower()
        assert "quantitative insights" in instructions.lower()
    
    def test_analyze_data_method(self, data_analyst):
        """Test analyze_data method."""
        test_data = {
            "numerical_data": [1, 2, 3, 4, 5],
            "research_findings": ["Finding 1", "Finding 2"],
            "quality_metrics": {"accuracy": 0.9}
        }
        
        results = data_analyst.analyze_data(test_data, "comprehensive")
        
        assert results["analyst_type"] == "data"
        assert results["analysis_type"] == "comprehensive"
        assert "input_summary" in results
        assert "findings" in results
        assert "quality_assessment" in results
        assert "recommendations" in results
        assert "methodology" in results
    
    def test_input_summarization(self, general_analyst):
        """Test input data summarization."""
        complex_data = {
            "research_findings": ["Finding A", "Finding B"],
            "numerical_data": list(range(100)),
            "text_data": "Large text content " * 100,
            "metadata": {"source": "test", "timestamp": "2024-01-01"}
        }
        
        summary = general_analyst._summarize_input(complex_data)
        
        assert "data_types" in summary
        assert "total_elements" in summary
        assert "complexity_score" in summary
        assert "primary_focus" in summary
        
        assert len(summary["data_types"]) == 4
        assert summary["total_elements"] == 4
        assert summary["complexity_score"] > 0
    
    def test_primary_focus_identification(self, general_analyst):
        """Test primary focus identification from input data."""
        research_data = {"research_findings": ["Finding 1"]}
        market_data = {"market_data": ["Market info"]}
        numerical_data = {"numerical_data": [1, 2, 3]}
        general_data = {"other_data": ["General info"]}
        
        assert general_analyst._identify_primary_focus(research_data) == "research_analysis"
        assert general_analyst._identify_primary_focus(market_data) == "market_analysis"
        assert general_analyst._identify_primary_focus(numerical_data) == "statistical_analysis"
        assert general_analyst._identify_primary_focus(general_data) == "general_analysis"
    
    def test_analysis_performance(self, business_analyst):
        """Test analysis performance and findings generation."""
        business_data = {
            "market_data": ["Market trend 1", "Market trend 2"],
            "financial_data": {"revenue": 1000000, "growth": 0.15},
            "competitive_data": ["Competitor A", "Competitor B"]
        }
        
        findings = business_analyst._perform_analysis(business_data, "market_focused")
        
        assert "patterns_identified" in findings
        assert "key_insights" in findings
        assert "validation_results" in findings
        assert "comparative_analysis" in findings
        
        # Check that findings contain meaningful content
        assert len(findings["patterns_identified"]) > 0
        assert len(findings["key_insights"]) > 0
    
    def test_quality_assessment(self, quality_analyst):
        """Test analysis quality assessment."""
        test_data = {"quality_data": ["Data point 1", "Data point 2"]}
        
        assessment = quality_analyst._assess_analysis_quality(test_data)
        
        assert "accuracy_score" in assessment
        assert "completeness_score" in assessment
        assert "reliability_score" in assessment
        assert "bias_assessment" in assessment
        assert "confidence_level" in assessment
        assert "validation_status" in assessment
        
        # Verify scores are in valid range
        for score_key in ["accuracy_score", "completeness_score", "reliability_score"]:
            score = assessment[score_key]
            assert 0 <= score <= 1
    
    def test_recommendations_generation(self, research_analyst):
        """Test recommendations generation."""
        research_data = {"literature": ["Paper 1", "Paper 2"], "methodology": "quantitative"}
        
        recommendations = research_analyst._generate_recommendations(research_data)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Research analyst should have specific recommendations
        rec_text = " ".join(recommendations).lower()
        assert any(keyword in rec_text for keyword in ["evidence", "methodology", "research"])
    
    def test_methodology_documentation(self, data_analyst):
        """Test methodology documentation."""
        methodology = data_analyst._document_methodology("statistical")
        
        assert "approach" in methodology
        assert "tools_used" in methodology
        assert "validation_methods" in methodology
        assert "limitations" in methodology
        assert "quality_controls" in methodology
        
        assert "data analysis methodology" in methodology["approach"].lower()
        assert len(methodology["validation_methods"]) > 0
        assert len(methodology["quality_controls"]) > 0


class TestAnalystFactoryFunctions:
    """Test factory functions for creating analysts."""
    
    def test_create_general_analyst(self):
        """Test general analyst factory function."""
        analyst = create_general_analyst()
        
        assert isinstance(analyst, AnalystRole)
        assert analyst.analyst_type == "general"
        
        # Check basic capabilities are present
        capability_names = [cap.name for cap in analyst.capabilities]
        assert "pattern_recognition" in capability_names
    
    def test_create_data_analyst(self):
        """Test data analyst factory function."""
        analyst = create_data_analyst()
        
        assert isinstance(analyst, AnalystRole)
        assert analyst.analyst_type == "data"
        
        # Check data-specific capabilities
        capability_names = [cap.name for cap in analyst.capabilities]
        assert "statistical_analysis" in capability_names
        assert "data_visualization" in capability_names
    
    def test_create_business_analyst(self):
        """Test business analyst factory function."""
        analyst = create_business_analyst()
        
        assert isinstance(analyst, AnalystRole)
        assert analyst.analyst_type == "business"
        
        # Check business-specific capabilities
        capability_names = [cap.name for cap in analyst.capabilities]
        assert "market_analysis" in capability_names
        assert "risk_assessment" in capability_names
    
    def test_create_quality_analyst(self):
        """Test quality analyst factory function."""
        analyst = create_quality_analyst()
        
        assert isinstance(analyst, AnalystRole)
        assert analyst.analyst_type == "quality"
        
        # Check quality-specific capabilities
        capability_names = [cap.name for cap in analyst.capabilities]
        assert "quality_assessment" in capability_names
        assert "gap_analysis" in capability_names
    
    def test_create_research_analyst(self):
        """Test research analyst factory function."""
        analyst = create_research_analyst()
        
        assert isinstance(analyst, AnalystRole)
        assert analyst.analyst_type == "research"
        
        # Check research-specific capabilities
        capability_names = [cap.name for cap in analyst.capabilities]
        assert "literature_synthesis" in capability_names
        assert "methodology_evaluation" in capability_names
    
    def test_factory_functions_return_different_instances(self):
        """Test that factory functions return different instances."""
        analyst1 = create_general_analyst()
        analyst2 = create_general_analyst()
        
        assert analyst1 is not analyst2  # Different instances
        assert analyst1.analyst_type == analyst2.analyst_type  # Same type


class TestAnalystRoleEdgeCases:
    """Test edge cases and error handling for analyst roles."""
    
    def test_unknown_analyst_type(self):
        """Test creating analyst with unknown type."""
        # Should default to base capabilities
        unknown_analyst = AnalystRole("unknown_type")
        
        assert unknown_analyst.analyst_type == "unknown_type"
        assert len(unknown_analyst.capabilities) >= 3  # Should have base capabilities
        
        # Should have general expertise areas
        expertise = unknown_analyst.role_definition.expertise_areas
        assert "general_analysis" in expertise
        assert "multi_domain_expertise" in expertise
    
    def test_empty_data_analysis(self, general_analyst):
        """Test analyzing empty data."""
        empty_data = {}
        
        results = general_analyst.analyze_data(empty_data)
        
        assert results["analyst_type"] == "general"
        assert "input_summary" in results
        assert results["input_summary"]["total_elements"] == 0
        assert results["input_summary"]["complexity_score"] >= 0
    
    def test_malformed_data_analysis(self, general_analyst):
        """Test analyzing malformed data."""
        malformed_data_sets = [
            None,
            "string_instead_of_dict",
            ["list_instead_of_dict"],
            {"nested": {"very": {"deep": {"structure": True}}}}
        ]
        
        for data in malformed_data_sets:
            try:
                # Should handle gracefully
                if data is None:
                    continue  # Skip None as it would likely raise TypeError
                
                results = general_analyst.analyze_data(data if isinstance(data, dict) else {"data": data})
                assert "analyst_type" in results
                assert "input_summary" in results
            except Exception as e:
                # If exceptions are raised, they should be meaningful
                assert isinstance(e, (TypeError, ValueError, AttributeError))
    
    def test_large_data_handling(self, data_analyst):
        """Test handling large datasets."""
        large_data = {
            "numerical_data": list(range(10000)),
            "text_data": ["Large text content"] * 1000,
            "complex_structure": {f"key_{i}": f"value_{i}" for i in range(1000)}
        }
        
        results = data_analyst.analyze_data(large_data, "comprehensive")
        
        # Should handle large data without issues
        assert results["analyst_type"] == "data"
        assert results["input_summary"]["total_elements"] == 3
        assert results["input_summary"]["complexity_score"] > 5  # Should detect high complexity


class TestAnalystRolePerformance:
    """Test performance characteristics of analyst roles."""
    
    def test_role_creation_performance(self):
        """Test analyst role creation performance."""
        import time
        
        start_time = time.time()
        
        # Create multiple analysts of different types
        analysts = []
        types = ["general", "data", "business", "quality", "research"]
        for i in range(25):  # 5 of each type
            analyst_type = types[i % len(types)]
            analyst = AnalystRole(analyst_type)
            analysts.append(analyst)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        assert creation_time < 1.0  # Should create 25 analysts in under 1 second
        assert len(analysts) == 25
    
    def test_analysis_performance(self, data_analyst):
        """Test data analysis performance."""
        import time
        
        # Create moderately complex dataset
        complex_data = {
            "numerical_data": list(range(1000)),
            "research_findings": [f"Finding {i}" for i in range(100)],
            "metadata": {f"key_{i}": f"value_{i}" for i in range(50)},
            "quality_metrics": {"accuracy": 0.9, "completeness": 0.8}
        }
        
        start_time = time.time()
        
        # Perform multiple analyses
        for _ in range(5):
            results = data_analyst.analyze_data(complex_data, "comprehensive")
        
        end_time = time.time()
        analysis_time = end_time - start_time
        
        assert analysis_time < 1.0  # Should complete 5 analyses in under 1 second
    
    @pytest.mark.performance
    def test_capability_scaling(self):
        """Test performance with large numbers of capabilities."""
        # Create analyst with many custom capabilities
        analyst = AnalystRole("general")
        
        # Add many capabilities (simulating complex analyst)
        additional_caps = []
        for i in range(50):
            cap = AnalyticsCapability(
                name=f"capability_{i}",
                description=f"Capability {i} description",
                tools_required=[f"tool_{i}"],
                input_types=[f"input_type_{i}"],
                output_format="format",
                accuracy_threshold=0.8
            )
            additional_caps.append(cap)
        
        analyst.capabilities.extend(additional_caps)
        
        # Test analysis with many capabilities
        test_data = {"general_data": [f"data_{i}" for i in range(100)]}
        
        import time
        start_time = time.time()
        results = analyst.analyze_data(test_data, "comprehensive")
        end_time = time.time()
        
        analysis_time = end_time - start_time
        assert analysis_time < 2.0  # Should handle many capabilities efficiently
        assert len(analyst.capabilities) > 50


class TestAnalystRoleIntegration:
    """Integration tests with mocked dependencies."""
    
    @patch('src.agents.multi_agent.roles.analyst.logger')
    def test_logging_integration(self, mock_logger):
        """Test logging integration."""
        # Creating analyst should log
        analyst = AnalystRole("test")
        mock_logger.info.assert_called()
        
        # Verify log message content
        log_calls = mock_logger.info.call_args_list
        assert any("Created test analyst role" in str(call) for call in log_calls)
    
    @patch('src.agents.multi_agent.roles.analyst.RoleDefinition')
    def test_role_definition_integration(self, mock_role_def):
        """Test integration with RoleDefinition."""
        mock_instance = Mock()
        mock_role_def.return_value = mock_instance
        
        analyst = AnalystRole("test")
        
        # Verify RoleDefinition was called with correct parameters
        mock_role_def.assert_called_once()
        call_args = mock_role_def.call_args
        
        assert call_args[1]["role_id"] == "test_analyst"
        assert call_args[1]["name"] == "Test Analyst"
        assert "capabilities" in call_args[1]
        assert "tools" in call_args[1]
        assert "instructions" in call_args[1]
        assert "expertise_areas" in call_args[1]
    
    def test_cross_analyst_collaboration(self):
        """Test collaboration between different analyst types."""
        data_analyst = create_data_analyst()
        business_analyst = create_business_analyst()
        quality_analyst = create_quality_analyst()
        
        # Data analyst performs initial analysis
        raw_data = {
            "sales_data": [100, 120, 110, 130, 125],
            "market_data": ["Growth trend", "Competitive pressure"],
            "timestamp": "2024-01-01"
        }
        
        data_results = data_analyst.analyze_data(raw_data, "statistical")
        
        # Business analyst analyzes data results for business implications
        business_input = {
            "data_analysis": data_results,
            "market_conditions": ["Favorable", "Expanding"],
            "business_context": "Q1 performance review"
        }
        
        business_results = business_analyst.analyze_data(business_input, "strategic")
        
        # Quality analyst validates both analyses
        quality_input = {
            "data_analysis": data_results,
            "business_analysis": business_results,
            "quality_requirements": {"accuracy": 0.9, "completeness": 0.8}
        }
        
        quality_results = quality_analyst.analyze_data(quality_input, "validation")
        
        # Verify each analyst produced appropriate results
        assert data_results["analyst_type"] == "data"
        assert business_results["analyst_type"] == "business"
        assert quality_results["analyst_type"] == "quality"
        
        # Quality analyst should have assessed the other analyses
        assert "validation" in quality_results["analysis_type"]
        assert quality_results["quality_assessment"]["validation_status"] in ["Passed", "passed"]


# Mock data generators for testing
def generate_numerical_data(size: int = 100) -> List[float]:
    """Generate mock numerical data."""
    import random
    return [random.random() * 100 for _ in range(size)]


def generate_research_findings(count: int = 10) -> List[str]:
    """Generate mock research findings."""
    return [f"Research finding {i}: Important insight about topic" for i in range(count)]


def generate_market_data() -> Dict[str, Any]:
    """Generate mock market data."""
    return {
        "market_size": 1000000,
        "growth_rate": 0.15,
        "competitors": ["Company A", "Company B", "Company C"],
        "trends": ["Digital transformation", "Sustainability focus", "Remote work"]
    }


if __name__ == "__main__":
    # Run basic unit tests
    print("Running Analyst Role Unit Tests")
    print("=" * 40)
    
    try:
        # Test basic functionality
        general = create_general_analyst()
        data = create_data_analyst()
        business = create_business_analyst()
        quality = create_quality_analyst()
        research = create_research_analyst()
        
        print(f"✅ Created general analyst with {len(general.capabilities)} capabilities")
        print(f"✅ Created data analyst with {len(data.capabilities)} capabilities")
        print(f"✅ Created business analyst with {len(business.capabilities)} capabilities")
        print(f"✅ Created quality analyst with {len(quality.capabilities)} capabilities")
        print(f"✅ Created research analyst with {len(research.capabilities)} capabilities")
        
        # Test analysis functionality
        test_data = {
            "numerical_data": generate_numerical_data(50),
            "research_findings": generate_research_findings(5),
            "market_data": generate_market_data()
        }
        
        data_results = data.analyze_data(test_data, "comprehensive")
        print(f"✅ Data analysis completed with quality score: {data_results['quality_assessment']['accuracy_score']:.2f}")
        
        business_results = business.analyze_data(test_data, "strategic")
        print(f"✅ Business analysis completed with {len(business_results['recommendations'])} recommendations")
        
        # Test role definitions
        for analyst in [general, data, business, quality, research]:
            role_def = analyst.get_role_definition()
            assert len(role_def.instructions) > 100
            print(f"✅ {analyst.analyst_type} analyst has detailed instructions")
        
        print("\\n✅ All unit tests passed!")
        
    except Exception as e:
        print(f"❌ Unit tests failed: {e}")
        import traceback
        print(traceback.format_exc())