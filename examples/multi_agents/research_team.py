#!/usr/bin/env python3
"""
Multi-Agent Research Team Example

This example demonstrates a collaborative team of specialized research agents
working together to provide comprehensive analysis on any topic.

Team Members:
- Web Researcher: Searches current web information
- Academic Researcher: Finds scholarly articles and papers  
- Social Media Researcher: Tracks trends and discussions
- Analysis Coordinator: Synthesizes findings and provides final report
"""

import os
import sys
import pathlib
import asyncio
from textwrap import dedent

# Add project root to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from model_config import get_configured_model, print_model_info
from search_config import get_search_tools
from topic_selector import select_research_topic, get_research_prompt

# Load environment variables
load_dotenv()

def create_research_team():
    """Create a collaborative research team with specialized agents."""
    
    # Web Research Agent
    web_researcher = Agent(
        name="Web Researcher",
        role="Search the web for current information and trends",
        model=get_configured_model(),
        tools=[get_search_tools()],
        add_name_to_context=True,
        instructions=dedent("""
        You are a web research specialist.
        - Search for the most current and relevant information on the given topic
        - Focus on recent news, articles, and authoritative sources  
        - Provide citations and links when possible
        - Identify key trends and developments
        - Summarize findings clearly and concisely
        """),
        markdown=True,
    )
    
    # Academic Research Agent  
    academic_researcher = Agent(
        name="Academic Researcher",
        role="Research academic papers and scholarly content",
        model=get_configured_model(),
        tools=[get_search_tools()],  # Uses robust search tools
        add_name_to_context=True,
        instructions=dedent("""
        You are an academic research specialist.
        - Search for peer-reviewed articles, research papers, and scholarly content
        - Focus on scientific studies, academic publications, and expert analysis
        - Look for statistical data, research methodologies, and evidence-based findings
        - Identify key researchers and institutions in the field  
        - Provide academic credibility to the research
        """),
        markdown=True,
    )
    
    # Social Media Research Agent
    social_researcher = Agent(
        name="Social Media Researcher", 
        role="Research social trends and public discussions",
        model=get_configured_model(),
        tools=[get_search_tools()],
        add_name_to_context=True,
        instructions=dedent("""
        You are a social media and trends research specialist.
        - Research public opinion, discussions, and trending topics
        - Look for sentiment analysis and public perception  
        - Identify influential voices and thought leaders
        - Track hashtags, viral content, and social movements
        - Analyze community discussions and user-generated content
        """),
        markdown=True,
    )
    
    # Analysis Coordinator Agent
    analysis_coordinator = Agent(
        name="Analysis Coordinator",
        role="Synthesize research findings and provide comprehensive analysis",
        model=get_configured_model(),
        tools=[ReasoningTools(add_instructions=True)],
        add_name_to_context=True,
        instructions=dedent("""
        You are a research analysis coordinator and synthesizer.
        - Review and analyze all research findings from team members
        - Identify patterns, connections, and insights across different sources
        - Provide balanced, objective analysis considering multiple perspectives
        - Structure findings into clear, actionable insights
        - Create comprehensive summaries and recommendations
        - Highlight areas of consensus and disagreement among sources
        """),
        markdown=True,
    )
    
    # Create the collaborative team
    research_team = Team(
        name="Comprehensive Research Team",
        model=get_configured_model(),
        members=[
            web_researcher,
            academic_researcher, 
            social_researcher,
            analysis_coordinator,
        ],
        instructions=dedent("""
        You are leading a comprehensive research team.
        
        Team Process:
        1. Delegate research tasks to specialized team members based on their expertise
        2. Ensure all members contribute their unique perspective
        3. Facilitate collaboration and information sharing
        4. Guide the team toward a comprehensive, well-rounded analysis  
        5. Synthesize findings into a cohesive final report
        
        Quality Standards:
        - Ensure accuracy and fact-checking across all sources
        - Maintain objectivity and consider multiple viewpoints
        - Provide evidence-based conclusions
        - Include diverse source types (academic, news, social, etc.)
        """),
        show_members_responses=True,  # Show individual agent contributions
        markdown=True,
    )
    
    return research_team

async def run_research_example():
    """Run an example research collaboration."""
    print("🔬 Multi-Agent Research Team Demo")
    print("=" * 60)
    
    # Show configuration
    print_model_info()
    
    print("🤖 Creating specialized research team...")
    team = create_research_team()
    
    print(f"✅ Team created with {len(team.members)} specialized agents:")
    for agent in team.members:
        print(f"   • {agent.name}: {agent.role}")
    
    print("\n" + "=" * 60)
    print("🚀 Starting collaborative research...")
    print("=" * 60)
    
    # Interactive topic selection
    topic = select_research_topic()
    
    if not topic:
        print("❌ No topic selected. Exiting...")
        return
    
    print(f"\n📋 Research Topic: {topic}")
    print("\n" + "-" * 60)
    
    # Run the collaborative research
    research_prompt = get_research_prompt(topic)
    
    try:
        await team.aprint_response(
            input=research_prompt,
            stream=True,
            stream_intermediate_steps=True,
        )
        
        print("\n" + "=" * 60)
        print("✅ Research completed! The team has provided comprehensive analysis.")
        
    except Exception as e:
        print(f"❌ Error during research: {e}")

def run_sync_research_example():
    """Synchronous version for easier testing."""
    print("🔬 Multi-Agent Research Team Demo (Sync)")
    print("=" * 60)
    
    # Show configuration
    print_model_info()
    
    print("🤖 Creating specialized research team...")
    team = create_research_team()
    
    print(f"✅ Team created with {len(team.members)} specialized agents:")
    for agent in team.members:
        print(f"   • {agent.name}: {agent.role}")
    
    print("\n" + "=" * 60)
    print("🚀 Starting collaborative research...")
    print("=" * 60)
    
    # Interactive topic selection
    topic = select_research_topic()
    
    if not topic:
        print("❌ No topic selected. Exiting...")
        return
    
    print(f"\n📋 Research Topic: {topic}")
    print("\n" + "-" * 60)
    
    research_prompt = get_research_prompt(topic)
    
    try:
        team.print_response(
            input=research_prompt,
            stream=True,
        )
        
        print("\n" + "=" * 60)
        print("✅ Research completed!")
        
    except Exception as e:
        print(f"❌ Error during research: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_research_example())
            
    except KeyboardInterrupt:
        print("\n👋 Research cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")