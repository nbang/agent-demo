"""Researcher Role Implementation

Specialized researcher agent implementation with comprehensive research capabilities
for the multi-agent research team collaboration system.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ..agent_roles import RoleDefinition
from ..logging_config import get_multi_agent_logger

logger = get_multi_agent_logger("researcher_role")


@dataclass
class ResearchCapability:
    """A specific research capability for a researcher role."""
    
    name: str
    description: str
    tools_required: List[str]
    quality_metrics: Dict[str, float]
    output_format: str


class ResearcherRole:
    """Enhanced researcher role with specialized research capabilities."""
    
    def __init__(self, researcher_type: str = "general"):
        """Initialize researcher role.
        
        Args:
            researcher_type: Type of researcher (general, academic, industry, technical)
        """
        self.researcher_type = researcher_type
        self.capabilities = self._define_capabilities()
        self.role_definition = self._create_role_definition()
        
        logger.info(f"Created {researcher_type} researcher role")
    
    def _define_capabilities(self) -> List[ResearchCapability]:
        """Define capabilities based on researcher type."""
        base_capabilities = [
            ResearchCapability(
                name="information_gathering",
                description="Collect relevant information from multiple sources",
                tools_required=["search", "web_scraping", "database_access"],
                quality_metrics={"relevance": 0.8, "credibility": 0.9, "completeness": 0.7},
                output_format="structured_data"
            ),
            ResearchCapability(
                name="source_evaluation",
                description="Assess the quality and credibility of information sources",
                tools_required=["credibility_checker", "bias_detector"],
                quality_metrics={"accuracy": 0.9, "objectivity": 0.8},
                output_format="evaluation_report"
            ),
            ResearchCapability(
                name="fact_verification",
                description="Verify facts and cross-reference information",
                tools_required=["fact_checker", "cross_reference"],
                quality_metrics={"accuracy": 0.95, "verification_depth": 0.8},
                output_format="verification_report"
            )
        ]
        
        # Add specialized capabilities based on researcher type
        if self.researcher_type == "academic":
            base_capabilities.extend([
                ResearchCapability(
                    name="literature_review",
                    description="Conduct systematic literature reviews",
                    tools_required=["academic_search", "citation_analysis"],
                    quality_metrics={"comprehensiveness": 0.9, "citation_quality": 0.8},
                    output_format="literature_review"
                ),
                ResearchCapability(
                    name="peer_review_analysis",
                    description="Analyze peer-reviewed research papers",
                    tools_required=["paper_analyzer", "methodology_evaluator"],
                    quality_metrics={"methodological_rigor": 0.8, "evidence_strength": 0.8},
                    output_format="research_analysis"
                )
            ])
        
        elif self.researcher_type == "industry":
            base_capabilities.extend([
                ResearchCapability(
                    name="market_analysis",
                    description="Analyze market trends and industry developments",
                    tools_required=["market_data", "trend_analyzer"],
                    quality_metrics={"timeliness": 0.9, "market_relevance": 0.8},
                    output_format="market_report"
                ),
                ResearchCapability(
                    name="competitive_intelligence",
                    description="Gather competitive intelligence and analysis",
                    tools_required=["competitor_tracker", "business_intelligence"],
                    quality_metrics={"completeness": 0.8, "actionability": 0.7},
                    output_format="competitive_analysis"
                )
            ])
        
        elif self.researcher_type == "technical":
            base_capabilities.extend([
                ResearchCapability(
                    name="technical_documentation",
                    description="Research technical specifications and documentation",
                    tools_required=["tech_docs", "api_explorer", "code_analyzer"],
                    quality_metrics={"technical_accuracy": 0.9, "implementation_feasibility": 0.8},
                    output_format="technical_report"
                ),
                ResearchCapability(
                    name="standards_compliance",
                    description="Research industry standards and compliance requirements",
                    tools_required=["standards_database", "compliance_checker"],
                    quality_metrics={"compliance_coverage": 0.9, "regulatory_accuracy": 0.95},
                    output_format="compliance_report"
                )
            ])
        
        return base_capabilities
    
    def _create_role_definition(self) -> RoleDefinition:
        """Create role definition for the researcher."""
        expertise_areas = self._get_expertise_areas()
        instructions = self._generate_instructions()
        
        # Store quality standards separately since RoleDefinition doesn't include them
        self.quality_standards = {
            "min_sources": 5 if self.researcher_type == "general" else 10,
            "credibility_threshold": 0.8,
            "verification_requirement": True,
            "citation_required": self.researcher_type == "academic"
        }
        
        return RoleDefinition(
            role_id=f"{self.researcher_type}_researcher",
            name=f"{self.researcher_type.title()} Researcher",
            description=f"Specialized {self.researcher_type} researcher agent",
            capabilities=[cap.name for cap in self.capabilities],
            tools=["search", "web_scraping", "fact_checker"],  # Default tools
            instructions=instructions,
            expertise_areas=expertise_areas
        )
    
    def _get_expertise_areas(self) -> List[str]:
        """Get expertise areas based on researcher type."""
        base_areas = ["information_gathering", "source_evaluation", "fact_checking"]
        
        if self.researcher_type == "academic":
            return base_areas + ["literature_review", "peer_review", "academic_writing", "citation_analysis"]
        elif self.researcher_type == "industry":
            return base_areas + ["market_analysis", "competitive_intelligence", "business_research", "trend_analysis"]
        elif self.researcher_type == "technical":
            return base_areas + ["technical_documentation", "standards_research", "implementation_analysis", "compliance_checking"]
        else:
            return base_areas + ["general_research", "multi_domain_analysis"]
    
    def _generate_instructions(self) -> str:
        """Generate detailed instructions for the researcher role."""
        base_instructions = f"""
You are a specialized {self.researcher_type} researcher in a collaborative research team.

Your primary responsibilities:
1. Conduct thorough research using appropriate sources and methodologies
2. Evaluate source credibility and information reliability
3. Verify facts through cross-referencing and validation
4. Collaborate effectively with other team members
5. Maintain high quality standards in all research outputs

Research Process:
1. Define research scope and objectives clearly
2. Identify and access relevant information sources
3. Gather comprehensive data while maintaining focus
4. Evaluate and filter information for quality and relevance
5. Organize findings in structured, accessible formats
6. Collaborate with analysts and synthesizers for validation
7. Provide clear, well-documented research outputs

Quality Standards:
- Minimum {self.quality_standards['min_sources']} credible sources
- Source credibility threshold: {self.quality_standards['credibility_threshold']}
- All facts must be verifiable and cross-referenced
- Maintain objectivity and identify potential biases
        """
        
        # Add specialized instructions based on researcher type
        if self.researcher_type == "academic":
            base_instructions += """
Academic Research Specialization:
- Focus on peer-reviewed journals and academic publications
- Conduct systematic literature reviews when appropriate
- Analyze research methodologies and evaluate evidence quality
- Provide proper academic citations and references
- Consider theoretical frameworks and conceptual foundations
- Identify research gaps and future research directions
            """
        
        elif self.researcher_type == "industry":
            base_instructions += """
Industry Research Specialization:
- Focus on market trends, industry reports, and business intelligence
- Analyze competitive landscapes and market dynamics
- Track regulatory changes and industry developments
- Consider practical business implications and applications
- Evaluate commercial viability and market opportunities
- Provide actionable insights for business decision-making
            """
        
        elif self.researcher_type == "technical":
            base_instructions += """
Technical Research Specialization:
- Focus on technical documentation, specifications, and standards
- Analyze implementation requirements and technical feasibility
- Research compliance requirements and regulatory standards
- Evaluate technical solutions and architectural approaches
- Consider scalability, security, and performance implications
- Provide detailed technical analysis and recommendations
            """
        
        return base_instructions.strip()
    
    def get_role_definition(self) -> RoleDefinition:
        """Get the role definition for this researcher."""
        return self.role_definition
    
    def get_capabilities(self) -> List[ResearchCapability]:
        """Get all capabilities for this researcher."""
        return self.capabilities
    
    def evaluate_research_quality(self, research_output: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the quality of research output."""
        quality_assessment = {
            "overall_score": 0.0,
            "capability_scores": {},
            "strengths": [],
            "areas_for_improvement": [],
            "recommendations": []
        }
        
        # Evaluate each capability
        total_score = 0
        for capability in self.capabilities:
            score = self._evaluate_capability_output(capability, research_output)
            quality_assessment["capability_scores"][capability.name] = score
            total_score += score
        
        # Calculate overall score
        quality_assessment["overall_score"] = total_score / len(self.capabilities)
        
        # Generate feedback
        quality_assessment.update(self._generate_feedback(quality_assessment))
        
        return quality_assessment
    
    def _evaluate_capability_output(self, capability: ResearchCapability, output: Dict[str, Any]) -> float:
        """Evaluate output for a specific capability."""
        # Simplified evaluation - in practice, this would be more sophisticated
        base_score = 0.7
        
        # Check if output contains expected elements
        if capability.name in output.get("capabilities_used", []):
            base_score += 0.2
        
        # Check output format
        if output.get("format") == capability.output_format:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _generate_feedback(self, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate feedback based on quality assessment."""
        feedback = {
            "strengths": [],
            "areas_for_improvement": [],
            "recommendations": []
        }
        
        # Identify strengths
        high_scoring_capabilities = [
            name for name, score in assessment["capability_scores"].items() 
            if score >= 0.8
        ]
        if high_scoring_capabilities:
            feedback["strengths"].append(f"Strong performance in: {', '.join(high_scoring_capabilities)}")
        
        # Identify areas for improvement
        low_scoring_capabilities = [
            name for name, score in assessment["capability_scores"].items() 
            if score < 0.6
        ]
        if low_scoring_capabilities:
            feedback["areas_for_improvement"].append(f"Needs improvement in: {', '.join(low_scoring_capabilities)}")
        
        # Generate recommendations
        if assessment["overall_score"] < 0.7:
            feedback["recommendations"].append("Consider using additional sources for more comprehensive research")
            feedback["recommendations"].append("Focus on improving fact verification and source evaluation")
        
        return feedback


# Factory functions for different researcher types
def create_general_researcher() -> ResearcherRole:
    """Create a general researcher role."""
    return ResearcherRole("general")


def create_academic_researcher() -> ResearcherRole:
    """Create an academic researcher role."""
    return ResearcherRole("academic")


def create_industry_researcher() -> ResearcherRole:
    """Create an industry researcher role."""
    return ResearcherRole("industry")


def create_technical_researcher() -> ResearcherRole:
    """Create a technical researcher role."""
    return ResearcherRole("technical")


# Demo function
def demo_researcher_roles():
    """Demonstrate different researcher role types."""
    print("Researcher Role Implementation Demo")
    print("=" * 40)
    
    # Create different researcher types
    researchers = [
        ("General", create_general_researcher()),
        ("Academic", create_academic_researcher()),
        ("Industry", create_industry_researcher()),
        ("Technical", create_technical_researcher())
    ]
    
    for name, researcher in researchers:
        print(f"\\n{name} Researcher:")
        print(f"  Type: {researcher.researcher_type}")
        print(f"  Capabilities: {len(researcher.capabilities)}")
        print(f"  Expertise Areas: {', '.join(researcher.role_definition.expertise_areas[:3])}...")
        
        # Show sample capabilities
        if researcher.capabilities:
            cap = researcher.capabilities[0]
            print(f"  Sample Capability: {cap.name} - {cap.description}")
    
    print("\\nResearcher roles demo completed!")


if __name__ == "__main__":
    demo_researcher_roles()