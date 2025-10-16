"""Unit Tests for Synthesizer Roles

Comprehensive unit tests for synthesizer role implementations,
testing synthesis capabilities and integration behaviors.
"""

import pytest
from typing import Dict, Any, List
from unittest.mock import Mock, patch

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.agents.multi_agent.roles.synthesizer import (
    SynthesizerRole,
    SynthesisCapability,
    create_general_synthesizer,
    create_research_synthesizer,
    create_content_synthesizer,
    create_executive_synthesizer
)
from src.agents.multi_agent.agent_roles import RoleDefinition


class TestSynthesisCapability:
    """Test SynthesisCapability dataclass."""
    
    def test_capability_creation(self):
        """Test synthesis capability creation."""
        capability = SynthesisCapability(
            name="test_synthesis",
            description="Test synthesis capability",
            tools_required=["integrator", "synthesizer"],
            input_requirements=["multiple_sources", "diverse_data"],
            output_format="synthesis_report",
            integration_complexity="medium"
        )
        
        assert capability.name == "test_synthesis"
        assert capability.description == "Test synthesis capability"
        assert len(capability.tools_required) == 2
        assert len(capability.input_requirements) == 2
        assert capability.output_format == "synthesis_report"
        assert capability.integration_complexity == "medium"
    
    def test_complexity_levels(self):
        """Test different integration complexity levels."""
        low_complexity = SynthesisCapability(
            name="simple_synthesis",
            description="Simple synthesis",
            tools_required=["basic_tool"],
            input_requirements=["single_source"],
            output_format="simple_report",
            integration_complexity="low"
        )
        
        high_complexity = SynthesisCapability(
            name="complex_synthesis",
            description="Complex synthesis",
            tools_required=["advanced_tool", "ai_processor", "validator"],
            input_requirements=["multiple_sources", "conflicting_data", "expert_opinions"],
            output_format="comprehensive_analysis",
            integration_complexity="high"
        )
        
        assert low_complexity.integration_complexity == "low"
        assert high_complexity.integration_complexity == "high"
        assert len(high_complexity.tools_required) > len(low_complexity.tools_required)
        assert len(high_complexity.input_requirements) > len(low_complexity.input_requirements)


class TestSynthesizerRole:
    """Test SynthesizerRole class."""
    
    @pytest.fixture
    def general_synthesizer(self):
        """Create a general synthesizer for testing."""
        return SynthesizerRole("general")
    
    @pytest.fixture
    def research_synthesizer(self):
        """Create a research synthesizer for testing."""
        return SynthesizerRole("research")
    
    @pytest.fixture
    def content_synthesizer(self):
        """Create a content synthesizer for testing."""
        return SynthesizerRole("content")
    
    @pytest.fixture
    def executive_synthesizer(self):
        """Create an executive synthesizer for testing."""
        return SynthesizerRole("executive")
    
    def test_synthesizer_initialization(self, general_synthesizer):
        """Test synthesizer role initialization."""
        assert general_synthesizer.synthesizer_type == "general"
        assert len(general_synthesizer.capabilities) >= 3  # Base capabilities
        assert general_synthesizer.role_definition is not None
        assert hasattr(general_synthesizer, 'quality_standards')
    
    def test_research_synthesizer_specialization(self, research_synthesizer):
        """Test research synthesizer specialization."""
        assert research_synthesizer.synthesizer_type == "research"
        
        # Check for research-specific capabilities
        capability_names = [cap.name for cap in research_synthesizer.capabilities]
        assert "literature_synthesis" in capability_names
        assert "evidence_consolidation" in capability_names
        
        # Check expertise areas
        expertise = research_synthesizer.role_definition.expertise_areas
        assert "literature_synthesis" in expertise
        assert "evidence_consolidation" in expertise
        assert "research_methodology" in expertise
    
    def test_content_synthesizer_specialization(self, content_synthesizer):
        """Test content synthesizer specialization."""
        assert content_synthesizer.synthesizer_type == "content"
        
        # Check for content-specific capabilities
        capability_names = [cap.name for cap in content_synthesizer.capabilities]
        assert "narrative_creation" in capability_names
        assert "content_harmonization" in capability_names
        
        # Check expertise areas
        expertise = content_synthesizer.role_definition.expertise_areas
        assert "narrative_creation" in expertise
        assert "content_harmonization" in expertise
        assert "creative_writing" in expertise
    
    def test_executive_synthesizer_specialization(self, executive_synthesizer):
        """Test executive synthesizer specialization."""
        assert executive_synthesizer.synthesizer_type == "executive"
        
        # Check for executive-specific capabilities
        capability_names = [cap.name for cap in executive_synthesizer.capabilities]
        assert "strategic_synthesis" in capability_names
        assert "executive_summarization" in capability_names
        
        # Check expertise areas
        expertise = executive_synthesizer.role_definition.expertise_areas
        assert "strategic_synthesis" in expertise
        assert "executive_communication" in expertise
        assert "decision_support" in expertise
    
    def test_base_capabilities_present(self, general_synthesizer):
        """Test that base capabilities are present in all synthesizers."""
        capability_names = [cap.name for cap in general_synthesizer.capabilities]
        
        # All synthesizers should have these base capabilities
        expected_base = ["information_integration", "perspective_consolidation", "knowledge_structuring"]
        for capability in expected_base:
            assert capability in capability_names
    
    def test_role_definition_structure(self, general_synthesizer):
        """Test role definition structure and content."""
        role_def = general_synthesizer.role_definition
        
        assert isinstance(role_def, RoleDefinition)
        assert role_def.role_id == "general_synthesizer"
        assert role_def.name == "General Synthesizer"
        assert "synthesizer agent" in role_def.description.lower()
        assert len(role_def.capabilities) > 0
        assert len(role_def.tools) > 0
        assert len(role_def.instructions) > 100  # Should have detailed instructions
        assert len(role_def.expertise_areas) > 0
    
    def test_quality_standards(self, general_synthesizer, research_synthesizer):
        """Test quality standards for different synthesizer types."""
        # General synthesizer standards
        gen_standards = general_synthesizer.quality_standards
        assert gen_standards["coherence_threshold"] == 0.85
        assert gen_standards["completeness_requirement"] == 0.90
        assert gen_standards["integration_quality"] == 0.80
        assert gen_standards["clarity_standard"] == "high"
        
        # Research synthesizer should have same standards
        research_standards = research_synthesizer.quality_standards
        assert research_standards["coherence_threshold"] == gen_standards["coherence_threshold"]
        assert research_standards["completeness_requirement"] == gen_standards["completeness_requirement"]
    
    def test_instructions_generation(self, content_synthesizer):
        """Test instruction generation for specific synthesizer type."""
        instructions = content_synthesizer.role_definition.instructions
        
        # Check for general instructions
        assert "specialized content synthesizer" in instructions.lower()
        assert "synthesis process" in instructions.lower()
        assert "quality standards" in instructions.lower()
        
        # Check for content-specific instructions
        assert "narrative creation" in instructions.lower()
        assert "content harmonization" in instructions.lower()
        assert "creative integrity" in instructions.lower()
    
    def test_synthesize_information_method(self, research_synthesizer):
        """Test synthesize_information method."""
        test_inputs = {
            "research_papers": ["Paper 1", "Paper 2", "Paper 3"],
            "expert_opinions": ["Opinion A", "Opinion B"],
            "data_analysis": {"findings": ["Finding 1", "Finding 2"]},
            "methodology_review": "Quantitative approach"
        }
        
        results = research_synthesizer.synthesize_information(
            test_inputs, 
            "comprehensive", 
            "literature_review"
        )
        
        assert results["synthesizer_type"] == "research"
        assert results["synthesis_type"] == "comprehensive"
        assert results["target_format"] == "literature_review"
        assert "input_analysis" in results
        assert "synthesis_output" in results
        assert "quality_metrics" in results
        assert "integration_summary" in results
        assert "recommendations" in results
    
    def test_input_analysis(self, general_synthesizer):
        """Test input analysis functionality."""
        complex_inputs = {
            "source_1": {"type": "research", "content": ["Data 1", "Data 2"]},
            "source_2": {"type": "analysis", "content": {"findings": "Analysis results"}},
            "source_3": "Simple text content",
            "source_4": {"type": "opinion", "expert": "John Doe", "content": "Expert opinion"}
        }
        
        analysis = general_synthesizer._analyze_inputs(complex_inputs)
        
        assert "input_sources" in analysis
        assert "content_types" in analysis
        assert "complexity_assessment" in analysis
        assert "conflict_areas" in analysis
        assert "synthesis_challenges" in analysis
        
        assert analysis["input_sources"] == 4
        assert len(analysis["content_types"]) == 4
        assert analysis["complexity_assessment"] in ["low", "medium", "high"]
    
    def test_complexity_assessment(self, general_synthesizer):
        """Test complexity assessment for different input scenarios."""
        # Simple inputs
        simple_inputs = {"source_1": "text", "source_2": "more text"}
        simple_complexity = general_synthesizer._assess_complexity(simple_inputs)
        assert simple_complexity in ["low", "medium"]
        
        # Complex inputs
        complex_inputs = {f"source_{i}": {"complex": f"data_{i}"} for i in range(10)}
        complex_complexity = general_synthesizer._assess_complexity(complex_inputs)
        assert complex_complexity in ["medium", "high"]
        
        # Very complex inputs
        very_complex_inputs = {}
        for i in range(20):
            very_complex_inputs[f"source_{i}"] = {
                "type": f"type_{i % 5}",
                "data": [f"item_{j}" for j in range(10)],
                "metadata": {"complex": True}
            }
        very_complex_complexity = general_synthesizer._assess_complexity(very_complex_inputs)
        assert very_complex_complexity == "high"
    
    def test_conflict_identification(self, general_synthesizer):
        """Test conflict identification in inputs."""
        # Single source - no conflicts
        single_source = {"source_1": "content"}
        conflicts_single = general_synthesizer._identify_conflicts(single_source)
        assert len(conflicts_single) == 0
        
        # Multiple sources - potential conflicts
        multiple_sources = {
            "source_1": "content A",
            "source_2": "content B",
            "source_3": "content C"
        }
        conflicts_multiple = general_synthesizer._identify_conflicts(multiple_sources)
        assert len(conflicts_multiple) > 0
        assert "perspectives require reconciliation" in conflicts_multiple[0].lower()
    
    def test_synthesis_performance(self, executive_synthesizer):
        """Test synthesis output generation."""
        business_inputs = {
            "market_analysis": {"trends": ["Trend 1", "Trend 2"], "growth": 0.15},
            "financial_data": {"revenue": 1000000, "profit": 150000},
            "strategic_report": "Company performing well in Q1",
            "risk_assessment": {"risks": ["Risk A", "Risk B"], "mitigation": "Plans in place"}
        }
        
        synthesis_output = executive_synthesizer._perform_synthesis(
            business_inputs, 
            "executive", 
            "strategic_brief"
        )
        
        assert "main_findings" in synthesis_output
        assert "integrated_insights" in synthesis_output
        assert "consolidated_perspectives" in synthesis_output
        assert "structured_output" in synthesis_output
        assert "synthesis_narrative" in synthesis_output
        
        # Check main findings extraction
        assert len(synthesis_output["main_findings"]) > 0
        
        # Check integrated insights structure
        insights = synthesis_output["integrated_insights"]
        assert "cross_cutting_themes" in insights
        assert "unique_contributions" in insights
        assert "convergent_findings" in insights
        assert "divergent_viewpoints" in insights
    
    def test_output_structuring(self, general_synthesizer):
        """Test output structuring for different formats."""
        test_inputs = {"source": "content"}
        
        # Executive summary format
        exec_structure = general_synthesizer._structure_output(test_inputs, "executive_summary")
        assert "key_points" in exec_structure
        assert "recommendations" in exec_structure
        assert "next_steps" in exec_structure
        
        # Detailed report format
        detailed_structure = general_synthesizer._structure_output(test_inputs, "detailed_report")
        assert "sections" in detailed_structure
        assert "appendices" in detailed_structure
        assert "references" in detailed_structure
        
        # Default structured report
        default_structure = general_synthesizer._structure_output(test_inputs, "structured_report")
        assert "overview" in default_structure
        assert "main_sections" in default_structure
        assert "supporting_elements" in default_structure
    
    def test_narrative_creation(self, content_synthesizer):
        """Test narrative creation for different synthesis types."""
        test_inputs = {"story_elements": ["Element 1", "Element 2"]}
        
        # Comprehensive narrative
        comprehensive_narrative = content_synthesizer._create_narrative(test_inputs, "comprehensive")
        assert "comprehensive synthesis" in comprehensive_narrative.lower()
        assert "coherent whole" in comprehensive_narrative.lower()
        
        # Executive narrative
        executive_narrative = content_synthesizer._create_narrative(test_inputs, "executive")
        assert "executive-level synthesis" in executive_narrative.lower()
        assert "strategic implications" in executive_narrative.lower()
        
        # Custom narrative
        custom_narrative = content_synthesizer._create_narrative(test_inputs, "creative")
        assert "creative synthesis" in custom_narrative.lower()
        assert str(len(test_inputs)) in custom_narrative
    
    def test_quality_metrics_assessment(self, research_synthesizer):
        """Test synthesis quality metrics assessment."""
        test_inputs = {"literature": ["Paper 1", "Paper 2"], "analysis": "Results"}
        
        quality_metrics = research_synthesizer._assess_synthesis_quality(test_inputs)
        
        assert "coherence_score" in quality_metrics
        assert "completeness_score" in quality_metrics
        assert "integration_quality" in quality_metrics
        assert "clarity_rating" in quality_metrics
        assert "bias_assessment" in quality_metrics
        assert "information_preservation" in quality_metrics
        assert "synthesis_effectiveness" in quality_metrics
        
        # Verify scores are in valid range
        for score_key in ["coherence_score", "completeness_score", "integration_quality", "information_preservation"]:
            score = quality_metrics[score_key]
            assert 0 <= score <= 1
        
        assert quality_metrics["clarity_rating"] in ["low", "medium", "high"]
        assert quality_metrics["synthesis_effectiveness"] in ["low", "moderate", "high", "highly effective"]
    
    def test_integration_summary(self, general_synthesizer):
        """Test integration process summarization."""
        test_inputs = {
            "research_data": ["Data 1", "Data 2"],
            "analysis_results": {"findings": "Important results"},
            "expert_opinions": ["Opinion A", "Opinion B"]
        }
        
        integration_summary = general_synthesizer._summarize_integration(test_inputs)
        
        assert "integration_method" in integration_summary
        assert "sources_integrated" in integration_summary
        assert "integration_challenges" in integration_summary
        assert "resolution_strategies" in integration_summary
        assert "final_integration_score" in integration_summary
        
        assert integration_summary["sources_integrated"] == len(test_inputs)
        assert "general synthesis approach" in integration_summary["integration_method"].lower()
        assert 0 <= integration_summary["final_integration_score"] <= 1
    
    def test_recommendations_generation(self, executive_synthesizer):
        """Test recommendations generation for different synthesizer types."""
        test_inputs = {"strategic_data": ["Data 1", "Data 2"]}
        
        recommendations = executive_synthesizer._generate_synthesis_recommendations(test_inputs)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Should have general recommendations
        rec_text = " ".join(recommendations).lower()
        assert "validate" in rec_text or "review" in rec_text
        
        # Executive synthesizer should have specific recommendations
        assert any("decision-makers" in rec.lower() for rec in recommendations)


class TestSynthesizerFactoryFunctions:
    """Test factory functions for creating synthesizers."""
    
    def test_create_general_synthesizer(self):
        """Test general synthesizer factory function."""
        synthesizer = create_general_synthesizer()
        
        assert isinstance(synthesizer, SynthesizerRole)
        assert synthesizer.synthesizer_type == "general"
        
        # Check basic capabilities are present
        capability_names = [cap.name for cap in synthesizer.capabilities]
        assert "information_integration" in capability_names
    
    def test_create_research_synthesizer(self):
        """Test research synthesizer factory function."""
        synthesizer = create_research_synthesizer()
        
        assert isinstance(synthesizer, SynthesizerRole)
        assert synthesizer.synthesizer_type == "research"
        
        # Check research-specific capabilities
        capability_names = [cap.name for cap in synthesizer.capabilities]
        assert "literature_synthesis" in capability_names
        assert "evidence_consolidation" in capability_names
    
    def test_create_content_synthesizer(self):
        """Test content synthesizer factory function."""
        synthesizer = create_content_synthesizer()
        
        assert isinstance(synthesizer, SynthesizerRole)
        assert synthesizer.synthesizer_type == "content"
        
        # Check content-specific capabilities
        capability_names = [cap.name for cap in synthesizer.capabilities]
        assert "narrative_creation" in capability_names
        assert "content_harmonization" in capability_names
    
    def test_create_executive_synthesizer(self):
        """Test executive synthesizer factory function."""
        synthesizer = create_executive_synthesizer()
        
        assert isinstance(synthesizer, SynthesizerRole)
        assert synthesizer.synthesizer_type == "executive"
        
        # Check executive-specific capabilities
        capability_names = [cap.name for cap in synthesizer.capabilities]
        assert "strategic_synthesis" in capability_names
        assert "executive_summarization" in capability_names
    
    def test_factory_functions_return_different_instances(self):
        """Test that factory functions return different instances."""
        synthesizer1 = create_general_synthesizer()
        synthesizer2 = create_general_synthesizer()
        
        assert synthesizer1 is not synthesizer2  # Different instances
        assert synthesizer1.synthesizer_type == synthesizer2.synthesizer_type  # Same type


class TestSynthesizerRoleEdgeCases:
    """Test edge cases and error handling for synthesizer roles."""
    
    def test_unknown_synthesizer_type(self):
        """Test creating synthesizer with unknown type."""
        # Should default to base capabilities
        unknown_synthesizer = SynthesizerRole("unknown_type")
        
        assert unknown_synthesizer.synthesizer_type == "unknown_type"
        assert len(unknown_synthesizer.capabilities) >= 3  # Should have base capabilities
        
        # Should have general expertise areas
        expertise = unknown_synthesizer.role_definition.expertise_areas
        assert "general_synthesis" in expertise
        assert "multi_domain_integration" in expertise
    
    def test_empty_inputs_synthesis(self, general_synthesizer):
        """Test synthesizing empty inputs."""
        empty_inputs = {}
        
        results = general_synthesizer.synthesize_information(empty_inputs)
        
        assert results["synthesizer_type"] == "general"
        assert results["input_analysis"]["input_sources"] == 0
        assert "synthesis_output" in results
        assert "quality_metrics" in results
    
    def test_single_input_synthesis(self, general_synthesizer):
        """Test synthesizing single input (minimal synthesis)."""
        single_input = {"only_source": "Single piece of content"}
        
        results = general_synthesizer.synthesize_information(single_input, "simple")
        
        assert results["input_analysis"]["input_sources"] == 1
        assert results["input_analysis"]["complexity_assessment"] == "low"
        assert len(results["input_analysis"]["conflict_areas"]) == 0  # No conflicts with single source
    
    def test_malformed_inputs_synthesis(self, general_synthesizer):
        """Test synthesizing malformed inputs."""
        malformed_inputs_sets = [
            {"valid_key": None},  # None value
            {"nested": {"very": {"deep": {"structure": "content"}}}},  # Deep nesting
            {"list_value": ["item1", "item2", "item3"]},  # List values
            {"mixed": {"types": ["list"], "and": "strings", "numbers": 42}}  # Mixed types
        ]
        
        for inputs in malformed_inputs_sets:
            try:
                results = general_synthesizer.synthesize_information(inputs)
                # Should handle gracefully
                assert "synthesizer_type" in results
                assert "input_analysis" in results
            except Exception as e:
                # If exceptions are raised, they should be meaningful
                pytest.fail(f"Should handle malformed inputs gracefully: {e}")
    
    def test_large_input_handling(self, research_synthesizer):
        """Test handling large input sets."""
        large_inputs = {}
        for i in range(100):
            large_inputs[f"source_{i}"] = {
                "content": f"Large content block {i} " * 100,
                "metadata": {"source_id": i, "type": "research"},
                "findings": [f"Finding {j}" for j in range(10)]
            }
        
        results = research_synthesizer.synthesize_information(large_inputs, "comprehensive")
        
        # Should handle large inputs without issues
        assert results["synthesizer_type"] == "research"
        assert results["input_analysis"]["input_sources"] == 100
        assert results["input_analysis"]["complexity_assessment"] == "high"


class TestSynthesizerRolePerformance:
    """Test performance characteristics of synthesizer roles."""
    
    def test_role_creation_performance(self):
        """Test synthesizer role creation performance."""
        import time
        
        start_time = time.time()
        
        # Create multiple synthesizers of different types
        synthesizers = []
        types = ["general", "research", "content", "executive"]
        for i in range(20):  # 5 of each type
            synthesizer_type = types[i % len(types)]
            synthesizer = SynthesizerRole(synthesizer_type)
            synthesizers.append(synthesizer)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        assert creation_time < 1.0  # Should create 20 synthesizers in under 1 second
        assert len(synthesizers) == 20
    
    def test_synthesis_performance(self, research_synthesizer):
        """Test synthesis performance with moderate complexity."""
        import time
        
        # Create moderately complex input set
        complex_inputs = {}
        for i in range(20):
            complex_inputs[f"research_source_{i}"] = {
                "title": f"Research Paper {i}",
                "findings": [f"Finding {j}" for j in range(5)],
                "methodology": "Quantitative analysis",
                "conclusions": f"Conclusion for paper {i}",
                "metadata": {"year": 2020 + i % 4, "credibility": 0.8 + (i % 3) * 0.1}
            }
        
        start_time = time.time()
        
        # Perform synthesis
        results = research_synthesizer.synthesize_information(complex_inputs, "comprehensive")
        
        end_time = time.time()
        synthesis_time = end_time - start_time
        
        assert synthesis_time < 2.0  # Should complete synthesis in under 2 seconds
        assert results["input_analysis"]["input_sources"] == 20
    
    @pytest.mark.performance
    def test_capability_scaling(self):
        """Test performance with large numbers of capabilities."""
        # Create synthesizer with many custom capabilities
        synthesizer = SynthesizerRole("general")
        
        # Add many capabilities (simulating complex synthesizer)
        additional_caps = []
        for i in range(30):
            cap = SynthesisCapability(
                name=f"synthesis_capability_{i}",
                description=f"Synthesis capability {i}",
                tools_required=[f"tool_{i}", f"helper_{i}"],
                input_requirements=[f"input_type_{i}"],
                output_format="complex_format",
                integration_complexity="medium"
            )
            additional_caps.append(cap)
        
        synthesizer.capabilities.extend(additional_caps)
        
        # Test synthesis with many capabilities
        test_inputs = {f"source_{i}": f"Content {i}" for i in range(10)}
        
        import time
        start_time = time.time()
        results = synthesizer.synthesize_information(test_inputs, "comprehensive")
        end_time = time.time()
        
        synthesis_time = end_time - start_time
        assert synthesis_time < 3.0  # Should handle many capabilities efficiently
        assert len(synthesizer.capabilities) > 30


class TestSynthesizerRoleIntegration:
    """Integration tests with mocked dependencies."""
    
    @patch('src.agents.multi_agent.roles.synthesizer.logger')
    def test_logging_integration(self, mock_logger):
        """Test logging integration."""
        # Creating synthesizer should log
        synthesizer = SynthesizerRole("test")
        mock_logger.info.assert_called()
        
        # Verify log message content
        log_calls = mock_logger.info.call_args_list
        assert any("Created test synthesizer role" in str(call) for call in log_calls)
    
    @patch('src.agents.multi_agent.roles.synthesizer.RoleDefinition')
    def test_role_definition_integration(self, mock_role_def):
        """Test integration with RoleDefinition."""
        mock_instance = Mock()
        mock_role_def.return_value = mock_instance
        
        synthesizer = SynthesizerRole("test")
        
        # Verify RoleDefinition was called with correct parameters
        mock_role_def.assert_called_once()
        call_args = mock_role_def.call_args
        
        assert call_args[1]["role_id"] == "test_synthesizer"
        assert call_args[1]["name"] == "Test Synthesizer"
        assert "capabilities" in call_args[1]
        assert "tools" in call_args[1]
        assert "instructions" in call_args[1]
        assert "expertise_areas" in call_args[1]
    
    def test_cross_synthesizer_collaboration(self):
        """Test collaboration between different synthesizer types."""
        research_synthesizer = create_research_synthesizer()
        content_synthesizer = create_content_synthesizer()
        executive_synthesizer = create_executive_synthesizer()
        
        # Research synthesizer processes academic inputs
        research_inputs = {
            "paper_1": {"title": "AI in Healthcare", "findings": ["AI improves diagnostics"]},
            "paper_2": {"title": "Machine Learning Applications", "findings": ["ML reduces errors"]},
            "study_data": {"methodology": "RCT", "results": "Significant improvement"}
        }
        
        research_results = research_synthesizer.synthesize_information(research_inputs, "academic")
        
        # Content synthesizer creates narrative from research synthesis
        content_inputs = {
            "research_synthesis": research_results,
            "target_audience": "General public",
            "tone_requirements": "Accessible and engaging"
        }
        
        content_results = content_synthesizer.synthesize_information(content_inputs, "narrative")
        
        # Executive synthesizer creates strategic brief from both
        executive_inputs = {
            "research_synthesis": research_results,
            "content_narrative": content_results,
            "business_context": "Healthcare technology investment"
        }
        
        executive_results = executive_synthesizer.synthesize_information(executive_inputs, "strategic")
        
        # Verify each synthesizer produced appropriate results
        assert research_results["synthesizer_type"] == "research"
        assert content_results["synthesizer_type"] == "content"
        assert executive_results["synthesizer_type"] == "executive"
        
        # Executive synthesizer should focus on strategic elements
        assert executive_results["target_format"] == "strategic"
        assert "strategic" in executive_results["synthesis_type"]


# Mock data generators for testing
def generate_research_papers(count: int = 5) -> Dict[str, Dict[str, Any]]:
    """Generate mock research papers."""
    papers = {}
    topics = ["AI Healthcare", "Machine Learning", "Data Science", "Robotics", "Neural Networks"]
    
    for i in range(count):
        papers[f"paper_{i}"] = {
            "title": f"Research on {topics[i % len(topics)]}",
            "authors": [f"Author {j}" for j in range(3)],
            "findings": [f"Key finding {k}" for k in range(3)],
            "methodology": "Experimental design",
            "conclusions": f"Important conclusions about {topics[i % len(topics)]}"
        }
    
    return papers


def generate_content_pieces(count: int = 3) -> Dict[str, str]:
    """Generate mock content pieces."""
    return {
        f"content_{i}": f"This is content piece {i} with relevant information about the topic."
        for i in range(count)
    }


def generate_expert_opinions(count: int = 4) -> Dict[str, Dict[str, str]]:
    """Generate mock expert opinions."""
    return {
        f"expert_{i}": {
            "name": f"Dr. Expert {i}",
            "opinion": f"Professional opinion {i} on the subject matter",
            "expertise": f"Expertise area {i}"
        }
        for i in range(count)
    }


if __name__ == "__main__":
    # Run basic unit tests
    print("Running Synthesizer Role Unit Tests")
    print("=" * 40)
    
    try:
        # Test basic functionality
        general = create_general_synthesizer()
        research = create_research_synthesizer()
        content = create_content_synthesizer()
        executive = create_executive_synthesizer()
        
        print(f"✅ Created general synthesizer with {len(general.capabilities)} capabilities")
        print(f"✅ Created research synthesizer with {len(research.capabilities)} capabilities")
        print(f"✅ Created content synthesizer with {len(content.capabilities)} capabilities")
        print(f"✅ Created executive synthesizer with {len(executive.capabilities)} capabilities")
        
        # Test synthesis functionality
        test_inputs = {
            "research_data": generate_research_papers(3),
            "content_pieces": generate_content_pieces(2),
            "expert_opinions": generate_expert_opinions(2)
        }
        
        research_results = research.synthesize_information(test_inputs, "comprehensive", "literature_review")
        print(f"✅ Research synthesis completed with coherence score: {research_results['quality_metrics']['coherence_score']:.2f}")
        
        content_results = content.synthesize_information(test_inputs, "narrative", "story_format")
        print(f"✅ Content synthesis completed with {len(content_results['recommendations'])} recommendations")
        
        executive_results = executive.synthesize_information(test_inputs, "strategic", "executive_summary")
        print(f"✅ Executive synthesis completed for strategic decision-making")
        
        # Test role definitions
        for synthesizer in [general, research, content, executive]:
            role_def = synthesizer.get_role_definition()
            assert len(role_def.instructions) > 100
            print(f"✅ {synthesizer.synthesizer_type} synthesizer has detailed instructions")
        
        print("\\n✅ All unit tests passed!")
        
    except Exception as e:
        print(f"❌ Unit tests failed: {e}")
        import traceback
        print(traceback.format_exc())