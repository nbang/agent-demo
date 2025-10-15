#!/usr/bin/env python3
"""
Fixed Research Team - Simplified Version

This version uses simpler configurations to avoid the authentication caching issues.
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
from search_config import get_search_tools
from model_config import get_configured_model, print_model_info
from topic_selector import select_research_topic, get_simple_research_prompt

# Load environment variables
load_dotenv()

def create_simple_research_team():
    """Create a simplified research team that avoids complex configurations."""
    
    # Force mock search mode to avoid network issues
    os.environ["SEARCH_MODE"] = "mock"
    
    # Web Research Agent (Simplified)
    web_researcher = Agent(
        name="Web Researcher",
        role="Research current information from web sources",
        model=get_configured_model(),
        tools=[get_search_tools("mock")],
        instructions="You research current information on topics. Keep responses focused and cite sources when possible.",
        markdown=True,
    )
    
    # Analysis Agent (Simplified)
    analysis_agent = Agent(
        name="Analysis Coordinator", 
        role="Analyze and synthesize research findings",
        model=get_configured_model(),
        instructions="You analyze research findings and create comprehensive summaries. Focus on key insights and actionable information.",
        markdown=True,
    )
    
    # Create a simple 2-agent team (avoiding complex 4-agent setup)
    research_team = Team(
        name="Simple Research Team",
        model=get_configured_model(),
        members=[web_researcher, analysis_agent],
        instructions="Work together to research the given topic. Keep responses clear and well-structured.",
        show_members_responses=True,
        markdown=True,
    )
    
    return research_team

def run_simple_research():
    """Run a simplified research example."""
    print("🔬 Simple Research Team Demo")
    print("=" * 40)
    
    # Show configuration
    print_model_info()
    
    print("🤖 Creating simple research team...")
    team = create_simple_research_team()
    
    print(f"✅ Team created with {len(team.members)} agents:")
    for agent in team.members:
        print(f"   • {agent.name}: {agent.role}")
    
    print("\n" + "=" * 40)
    print("🚀 Starting research...")
    print("=" * 40)
    
    # Interactive topic selection
    research_topic = select_research_topic()
    
    if not research_topic:
        print("❌ No topic selected. Exiting...")
        return
    
    print(f"\n📋 Research Topic: {research_topic}")
    print("-" * 40)
    
    try:
        # Use sync call instead of async to avoid streaming issues
        research_prompt = get_simple_research_prompt(research_topic)
        response = team.run(
            research_prompt,
            stream=False  # Disable streaming
        )
        
        if response and response.content:
            print("\n📄 Research Results:")
            print("-" * 20)
            print(response.content)
        else:
            print("❌ No response received")
        
        print("\n" + "=" * 40)
        print("✅ Simple research completed!")
        
    except Exception as e:
        print(f"❌ Error during research: {e}")
        print("\n🔧 Troubleshooting suggestions:")
        print("1. Check your API key is valid")
        print("2. Verify your Azure endpoint is correct")
        print("3. Try running debug_test.py first")

if __name__ == "__main__":
    try:
        run_simple_research()
        
    except KeyboardInterrupt:
        print("\n👋 Research cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()