"""Enhanced Research Team Collaboration using Multi-Agent Framework

This module provides an enhanced research team implementation that demonstrates
multi-agent collaboration for comprehensive research tasks with specialized roles.
It integrates with the multi-agent framework for team management and orchestration.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

from .team_manager import MultiAgentTeam, TeamConfiguration
from .constants import TeamType  
from . import workflows
from .logging_config import get_multi_agent_logger

logger = get_multi_agent_logger("enhanced_research_team")


class EnhancedResearchTeam:
    """Enhanced research team for collaborative research tasks using multi-agent framework."""
    
    def __init__(self, topic: str, team_size: int = 3, collaboration_rounds: int = 5):
        """Initialize enhanced research team.
        
        Args:
            topic: Research topic
            team_size: Number of agents in the team (2-5)
            collaboration_rounds: Maximum collaboration rounds
        """
        self.topic = topic
        self.team_size = min(max(team_size, 2), 5)  # Enforce 2-5 agents
        self.collaboration_rounds = collaboration_rounds
        
        # Create team configuration
        config = TeamConfiguration(
            team_name=f"Enhanced Research Team - {topic}",
            team_type=TeamType.RESEARCH,
            max_agents=self.team_size,
            collaboration_timeout=300,  # 5 minutes
            quality_threshold=0.8,
            max_rounds=collaboration_rounds
        )
        
        # Initialize multi-agent team
        self.team = MultiAgentTeam(config)
        self.workflow_id = None  # Will be set when needed
        
        # Set up team
        self._setup_team()
        
        logger.info(f"Created enhanced research team for topic: {topic}")
    
    def _setup_team(self):
        """Set up the research team with specialized agents."""
        # Always add core research roles
        self.team.add_agent("lead_researcher", "researcher", {
            "instructions": f"You are the lead researcher for the topic '{self.topic}'. "
                          f"Conduct comprehensive research using multiple sources. "
                          f"Focus on gathering accurate, relevant, and credible information. "
                          f"Collaborate with analysts and synthesizers to ensure thorough coverage."
        })
        
        self.team.add_agent("data_analyst", "analyst", {
            "instructions": f"You are the data analyst for research on '{self.topic}'. "
                          f"Analyze research findings from the lead researcher. "
                          f"Identify patterns, validate information, and provide analytical insights. "
                          f"Work closely with the synthesizer to ensure accurate conclusions."
        })
        
        self.team.add_agent("research_synthesizer", "synthesizer", {
            "instructions": f"You are the research synthesizer for '{self.topic}'. "
                          f"Combine findings from researchers and analysts into coherent conclusions. "
                          f"Create well-structured, comprehensive reports with clear summaries. "
                          f"Ensure all perspectives are integrated effectively."
        })
        
        # Add additional researchers if team size allows
        if self.team_size > 3:
            self.team.add_agent("specialist_researcher", "researcher", {
                "instructions": f"You are a specialist researcher for '{self.topic}'. "
                              f"Focus on specialized aspects and niche sources. "
                              f"Provide unique perspectives and deep domain expertise. "
                              f"Collaborate with the lead researcher to ensure comprehensive coverage."
            })
        
        if self.team_size > 4:
            self.team.add_agent("quality_analyst", "analyst", {
                "instructions": f"You are the quality analyst for research on '{self.topic}'. "
                              f"Focus on validating information quality and source credibility. "
                              f"Identify gaps or inconsistencies in research findings. "
                              f"Ensure the final output meets high quality standards."
            })
        
        # Initialize the team
        self.team.initialize_team()
        
        # Set up research workflow (will be handled by team manager)
        self.workflow_id = "default_research_workflow"
        
        logger.info(f"Set up enhanced research team with {len(self.team.agents)} agents")
    
    def collaborate(
        self, 
        research_depth: str = "comprehensive",
        source_requirements: str = "academic and industry",
        output_format: str = "structured_report"
    ) -> Dict[str, Any]:
        """Execute collaborative research on the topic.
        
        Args:
            research_depth: Depth of research (basic, comprehensive, exhaustive)
            source_requirements: Types of sources required
            output_format: Format of the output report
            
        Returns:
            Research collaboration results
        """
        logger.info(f"Starting enhanced research collaboration on: {self.topic}")
        
        # Prepare collaboration context
        context = {
            "research_topic": self.topic,
            "research_depth": research_depth,
            "source_requirements": source_requirements,
            "output_format": output_format,
            "quality_standards": {
                "min_sources": 10 if research_depth == "comprehensive" else 5,
                "credibility_threshold": 0.8,
                "coverage_completeness": 0.9
            },
            "collaboration_guidelines": {
                "peer_review": True,
                "fact_checking": True,
                "cross_validation": True
            }
        }
        
        # Define expected output
        expected_output = self._get_expected_output(research_depth, output_format)
        
        try:
            # Start collaboration
            collaboration_id = self.team.start_collaboration(
                task_description=f"Research and analyze the topic: {self.topic}",
                expected_output=expected_output,
                context=context
            )
            
            # Execute with workflow
            workflow_config = {
                "workflow_id": self.workflow_id,
                "max_rounds": self.collaboration_rounds,
                "quality_threshold": self.team.config.quality_threshold
            }
            
            results = self.team.execute_collaboration(workflow_config)
            
            # Enhance results with research-specific metrics
            enhanced_results = self._enhance_results(results, context)
            
            logger.info(f"Enhanced research collaboration completed successfully")
            return enhanced_results
            
        except Exception as e:
            logger.error(f"Enhanced research collaboration failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "topic": self.topic,
                "team_id": self.team.team_id
            }
    
    def _get_expected_output(self, research_depth: str, output_format: str) -> str:
        """Generate expected output description based on parameters."""
        depth_descriptions = {
            "basic": "fundamental overview with key insights",
            "comprehensive": "detailed analysis with multiple perspectives", 
            "exhaustive": "thorough investigation covering all relevant aspects"
        }
        
        format_descriptions = {
            "structured_report": "well-organized report with clear sections",
            "executive_summary": "concise summary highlighting key findings",
            "detailed_analysis": "in-depth analysis with supporting evidence"
        }
        
        return (f"A {depth_descriptions.get(research_depth, 'comprehensive')} "
                f"research output formatted as a {format_descriptions.get(output_format, 'structured report')} "
                f"covering the topic '{self.topic}' with credible sources, analytical insights, "
                f"and synthesized conclusions from multiple agent perspectives.")
    
    def _enhance_results(self, results: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance results with research-specific metrics and analysis."""
        enhanced = results.copy()
        
        # Add research-specific metadata
        enhanced.update({
            "research_topic": self.topic,
            "research_parameters": {
                "depth": context.get("research_depth"),
                "source_requirements": context.get("source_requirements"),
                "output_format": context.get("output_format")
            },
            "team_composition": {
                "team_size": len(self.team.agents),
                "roles": [role.name for role in self.team.agent_roles.values()],
                "specializations": [role.expertise_areas for role in self.team.agent_roles.values()]
            },
            "collaboration_metrics": {
                "workflow_used": self.workflow_id,
                "communication_stats": self.team.communication.get_communication_stats(),
                "context_version": self.team.shared_context.get_version()
            }
        })
        
        # Add quality assessment
        if results.get("success"):
            enhanced["quality_assessment"] = self._assess_research_quality(results, context)
        
        return enhanced
    
    def _assess_research_quality(self, results: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality of research results."""
        quality_standards = context.get("quality_standards", {})
        
        # Simulate quality metrics (in real implementation, these would be calculated)
        return {
            "overall_score": 0.85,  # Would be calculated from actual metrics
            "criteria_met": {
                "source_diversity": True,
                "information_accuracy": True,
                "analytical_depth": True,
                "synthesis_quality": True
            },
            "recommendations": [
                "Consider additional industry sources for broader perspective",
                "Expand on emerging trends analysis"
            ]
        }
    
    def get_team_status(self) -> Dict[str, Any]:
        """Get current team status and research progress."""
        base_status = self.team.get_team_status()
        
        # Add research-specific status information
        research_status = {
            "research_topic": self.topic,
            "team_size": self.team_size,
            "collaboration_rounds": self.collaboration_rounds,
            "workflow_id": self.workflow_id,
            "research_phase": "active" if self.team.current_task else "ready"
        }
        
        base_status.update(research_status)
        return base_status
    
    def cleanup(self):
        """Clean up research team resources."""
        logger.info(f"Cleaning up enhanced research team for topic: {self.topic}")
        self.team.cleanup()


# Convenience function for quick research team creation
def create_enhanced_research_team(topic: str, team_size: int = 3) -> EnhancedResearchTeam:
    """Create an enhanced research team for the given topic.
    
    Args:
        topic: Research topic
        team_size: Number of agents (2-5)
        
    Returns:
        Configured EnhancedResearchTeam instance
    """
    return EnhancedResearchTeam(topic, team_size)


# Demo function for enhanced research team
def demo_enhanced_research_team():
    """Demonstrate enhanced research team collaboration."""
    print("Enhanced Research Team Collaboration Demo")
    print("=" * 45)
    
    # Create enhanced research team
    topic = "Impact of AI on Healthcare"
    team = create_enhanced_research_team(topic, team_size=3)
    
    print(f"Created enhanced research team for: {topic}")
    print(f"Team ID: {team.team.team_id}")
    print(f"Team size: {len(team.team.agents)} agents")
    
    # Show team status
    status = team.get_team_status()
    print(f"Team status: {status['status']}")
    print(f"Agents: {', '.join(status['agents'].keys())}")
    
    # Execute research collaboration
    try:
        print("\\nStarting enhanced research collaboration...")
        results = team.collaborate(
            research_depth="comprehensive",
            source_requirements="academic and industry sources",
            output_format="structured_report"
        )
        
        if results.get("success"):
            print("✅ Enhanced research collaboration completed successfully!")
            print(f"Execution time: {results.get('execution_time', 0):.2f} seconds")
            print(f"Quality score: {results.get('quality_assessment', {}).get('overall_score', 'N/A')}")
        else:
            print("❌ Enhanced research collaboration failed")
            print(f"Error: {results.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    
    finally:
        team.cleanup()
        print("Enhanced research team demo completed")


if __name__ == "__main__":
    demo_enhanced_research_team()