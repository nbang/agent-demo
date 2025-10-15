#!/usr/bin/env python3
"""
Agno OS Web UI

This script creates a web-based interface for your Agno agents using the built-in
Agno OS and AGUI (Agno UI) system. It provides a beautiful web interface to 
interact with all your different agent types.
"""

import os
from dotenv import load_dotenv
from agno.agent.agent import Agent
from agno.os import AgentOS
from agno.os.interfaces.agui import AGUI
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.db.sqlite import SqliteDb
from model_config import get_configured_model, get_reasoning_model, print_model_info

# Load environment variables
load_dotenv()

def create_basic_chat_agent():
    """Create a basic conversational agent."""
    return Agent(
        name="Chat Assistant",
        model=get_configured_model(),
        instructions=[
            "You are a helpful AI assistant.",
            "Provide clear, accurate, and concise responses.",
            "Be friendly and engaging in your conversations.",
            "If you're unsure about something, say so rather than guessing.",
        ],
        description="A friendly conversational AI assistant for general questions and discussions.",
        markdown=True,
        add_datetime_to_context=True,
    )

def create_research_agent():
    """Create an agent with web search capabilities."""
    return Agent(
        name="Research Assistant",
        model=get_configured_model(),
        tools=[DuckDuckGoTools()],
        instructions=[
            "You are a research assistant with access to web search.",
            "Use the search tool to find current information when needed.",
            "Always cite your sources and provide accurate information.",
            "Be thorough in your research but concise in your responses.",
        ],
        description="An AI research assistant that can search the web for current information.",
        markdown=True,
        add_datetime_to_context=True,
    )

def create_reasoning_agent():
    """Create an agent with reasoning capabilities."""
    return Agent(
        name="Reasoning Expert",
        model=get_reasoning_model(),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are an expert problem-solving assistant with strong analytical skills.",
            "Always break down complex problems into component parts.",
            "Use step-by-step reasoning and show your thought process.",
            "Consider multiple perspectives and evaluate evidence.",
            "Identify assumptions and highlight areas of uncertainty.",
        ],
        description="An AI expert specialized in structured reasoning and complex problem analysis.",
        markdown=True,
        add_datetime_to_context=True,
        stream_intermediate_steps=True,
    )

def create_memory_agent():
    """Create an agent with persistent memory."""
    # Setup SQLite database for memory
    db = SqliteDb(db_file="agno_os_memory.db")
    
    return Agent(
        name="Memory Assistant",
        model=get_configured_model(),
        db=db,
        enable_agentic_memory=True,
        instructions=[
            "You are a personal assistant with memory capabilities.",
            "Remember important information about users and conversations.",
            "Refer to previous conversations when relevant.",
            "Build context over time to provide better assistance.",
            "Ask clarifying questions to better understand user needs.",
        ],
        description="An AI assistant with persistent memory that remembers conversations across sessions.",
        markdown=True,
        add_datetime_to_context=True,
    )

def create_agent_os():
    """Create and configure the Agent OS with multiple agents."""
    print("🚀 Initializing Agno OS with AGUI...")
    print_model_info()
    
    # Create all agents
    print("Creating agents...")
    chat_agent = create_basic_chat_agent()
    print("✅ Chat Assistant created")
    
    research_agent = create_research_agent()
    print("✅ Research Assistant created")
    
    reasoning_agent = create_reasoning_agent()
    print("✅ Reasoning Expert created")
    
    memory_agent = create_memory_agent()
    print("✅ Memory Assistant created")
    
    # Create Agent OS with all agents
    agent_os = AgentOS(
        agents=[
            chat_agent,
            research_agent,
            reasoning_agent,
            memory_agent,
        ],
        interfaces=[
            AGUI(agent=chat_agent)  # AGUI will use the default agent and allow switching
        ],
    )
    
    print("✅ Agno OS initialized successfully!")
    return agent_os

def main():
    """Main function to start the Agno OS web interface."""
    print("🌐 Agno OS Web UI")
    print("=" * 50)
    
    try:
        # Create Agent OS
        agent_os = create_agent_os()
        
        # Get the FastAPI app
        app = agent_os.get_app()
        
        print("\n🎯 Starting Agno OS Web Interface...")
        print("📱 Features available in the web UI:")
        print("   • Chat Assistant - General conversations")
        print("   • Research Assistant - Web search capabilities")
        print("   • Reasoning Expert - Complex problem analysis")
        print("   • Memory Assistant - Persistent conversation memory")
        print("\n🌐 The web interface will open automatically...")
        print("📝 You can switch between different agents in the web UI")
        
        # Start the server
        agent_os.serve(
            app=app,
            host="127.0.0.1",
            port=8001,  # Use port 8001 to avoid conflicts
            reload=False,  # Disable reload for now to avoid issues
        )
        
    except Exception as e:
        print(f"❌ Error starting Agno OS: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure your .env file is configured correctly")
        print("2. Check that all dependencies are installed: pip install -r requirements.txt")
        print("3. Verify your API keys are valid")

if __name__ == "__main__":
    main()