#!/usr/bin/env python3
"""
Multi-Agent Content Creation Team Example

This example demonstrates a content creation pipeline with specialized agents
working together to create high-quality content from research to final output.

Team Members:
- Research Agent: Gathers information and data
- Content Strategist: Plans content structure and approach
- Writer Agent: Creates the actual content
- Editor Agent: Reviews, edits, and improves the content
- SEO Specialist: Optimizes for search and engagement
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

# Load environment variables
load_dotenv()

def create_content_team():
    """Create a content creation team with specialized roles."""
    
    # Research Agent
    research_agent = Agent(
        name="Research Specialist",
        role="Gather comprehensive information and data for content creation",
        model=get_configured_model(),
        tools=[get_search_tools()],  # Use configured search tools with error handling
        add_name_to_context=True,
        instructions=dedent("""
        You are a content research specialist.
        - Research the topic thoroughly using multiple sources
        - Gather current statistics, trends, and factual information
        - Identify key points, examples, and supporting evidence
        - Find relevant quotes from experts and authorities
        - Compile a comprehensive research brief for the content team
        - Ensure all information is accurate and up-to-date
        """),
        markdown=True,
    )
    
    # Content Strategist
    content_strategist = Agent(
        name="Content Strategist",
        role="Plan content structure, approach, and strategy",
        model=get_configured_model(),
        tools=[ReasoningTools()],
        add_name_to_context=True,
        instructions=dedent("""
        You are a content strategy expert.
        - Analyze the research and target audience requirements
        - Develop a clear content structure and outline
        - Define the tone, style, and messaging approach
        - Identify key messages and calls-to-action
        - Plan content flow and logical progression
        - Consider SEO and engagement optimization opportunities
        - Provide detailed content brief for the writing team
        """),
        markdown=True,
    )
    
    # Writer Agent
    writer_agent = Agent(
        name="Content Writer",
        role="Create engaging, high-quality written content",
        model=get_configured_model(),
        add_name_to_context=True,
        instructions=dedent("""
        You are a professional content writer.
        - Write compelling, engaging content based on the research and strategy
        - Follow the content structure and guidelines provided
        - Use clear, accessible language appropriate for the target audience
        - Include relevant examples, statistics, and supporting evidence
        - Create engaging headlines, subheadings, and transitions
        - Ensure content flows logically and maintains reader interest
        - Write in the specified tone and style
        """),
        markdown=True,
    )
    
    # Editor Agent
    editor_agent = Agent(
        name="Content Editor",
        role="Review, edit, and improve content quality",
        model=get_configured_model(),
        tools=[ReasoningTools()],
        add_name_to_context=True,
        instructions=dedent("""
        You are a professional content editor.
        - Review content for clarity, flow, and coherence
        - Check grammar, spelling, and style consistency
        - Improve sentence structure and readability
        - Ensure factual accuracy and proper citations
        - Verify that content meets objectives and guidelines
        - Suggest improvements for engagement and impact
        - Provide constructive feedback and revisions
        """),
        markdown=True,
    )
    
    # SEO Specialist Agent
    seo_specialist = Agent(
        name="SEO Specialist",
        role="Optimize content for search engines and engagement",
        model=get_configured_model(),
        add_name_to_context=True,
        instructions=dedent("""
        You are an SEO and content optimization specialist.
        - Analyze content for SEO best practices
        - Suggest keyword optimization and placement
        - Recommend meta descriptions and title improvements
        - Identify opportunities for internal/external linking
        - Suggest formatting improvements for readability
        - Recommend social media optimization strategies
        - Provide final optimization recommendations
        """),
        markdown=True,
    )
    
    # Create the content creation team
    content_team = Team(
        name="Content Creation Team",
        model=get_configured_model(),
        members=[
            research_agent,
            content_strategist,
            writer_agent,
            editor_agent,
            seo_specialist,
        ],
        instructions=dedent("""
        You are managing a professional content creation team.
        
        Content Creation Process:
        1. Research: Gather comprehensive information on the topic
        2. Strategy: Develop content approach, structure, and messaging
        3. Writing: Create high-quality content based on research and strategy
        4. Editing: Review, refine, and improve the content
        5. Optimization: Apply SEO and engagement best practices
        
        Quality Standards:
        - Ensure accuracy and credibility of all information
        - Maintain consistent tone and style throughout
        - Create engaging, valuable content for the target audience
        - Follow SEO and accessibility best practices
        - Deliver polished, professional final output
        """),
        show_members_responses=True,
        markdown=True,
    )
    
    return content_team

def run_content_creation_example():
    """Run a content creation collaboration example."""
    print("📝 Multi-Agent Content Creation Team Demo")
    print("=" * 60)
    
    # Show configuration
    print_model_info()
    
    print("🤖 Creating content creation team...")
    team = create_content_team()
    
    print(f"✅ Team created with {len(team.members)} specialized agents:")
    for agent in team.members:
        print(f"   • {agent.name}: {agent.role}")
    
    print("\n" + "=" * 60)
    print("🚀 Starting content creation process...")
    print("=" * 60)
    
    # Content creation brief
    content_brief = """
    Create a comprehensive blog post on the following topic:
    
    **Topic:** "The Future of Remote Work: Trends, Challenges, and Opportunities in 2024"
    
    **Target Audience:** Business leaders, HR professionals, and remote workers
    
    **Content Requirements:**
    - Length: 1500-2000 words
    - Tone: Professional but accessible
    - Include current statistics and trends
    - Provide actionable insights and recommendations
    - Optimize for SEO with relevant keywords
    - Include compelling headlines and subheadings
    
    **Key Areas to Cover:**
    1. Current state of remote work adoption
    2. Emerging trends and technologies
    3. Challenges faced by organizations and employees
    4. Best practices and solutions
    5. Future predictions and implications
    
    **Deliverable:** 
    A complete, publication-ready blog post that is well-researched, 
    professionally written, edited, and optimized for engagement and SEO.
    """
    
    try:
        print(f"📋 Content Brief: {content_brief.split('**Topic:**')[1].split('**Target Audience:**')[0].strip()}")
        print("\n" + "-" * 60)
        
        team.print_response(
            input=content_brief,
            stream=True,
        )
        
        print("\n" + "=" * 60)
        print("✅ Content creation completed! The team has delivered a comprehensive blog post.")
        
    except Exception as e:
        print(f"❌ Error during content creation: {e}")

if __name__ == "__main__":
    try:
        run_content_creation_example()
        
    except KeyboardInterrupt:
        print("\n👋 Content creation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure your environment is configured correctly:")
        print("1. Check your .env file has the correct API keys")
        print("2. Ensure all dependencies are installed")