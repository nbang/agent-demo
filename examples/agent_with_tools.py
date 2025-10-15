#!/usr/bin/env python3
"""
Agent with Tools Example

This example demonstrates how to create an Agno agent with tools.
The agent can perform web searches using DuckDuckGo.
"""

import os
import sys
import pathlib
# Add parent directory to Python path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from model_config import get_configured_model, print_model_info

# Load environment variables
load_dotenv()

def create_agent_with_tools():
    """
    Create an agent equipped with search tools.
    """
    model = get_configured_model()
    
    agent = Agent(
        name="Research Assistant",
        model=model,
        tools=[DuckDuckGoTools()],  # Add web search capability
        instructions=[
            "You are a research assistant with access to web search.",
            "Use the search tool to find current information when needed.",
            "Always cite your sources and provide accurate information.",
            "If you can't find information, say so clearly.",
        ],
        markdown=True,
        add_datetime_to_context=True,
    )
    
    return agent

def main():
    """
    Main function to demonstrate agent with tools.
    """
    print("🔍 Agno Agent with Tools Demo")
    print("=" * 50)
    
    # Show model configuration
    print_model_info()
    
    try:
        agent = create_agent_with_tools()
        print("✅ Agent with tools created successfully!")
        
        # Example queries that benefit from web search
        example_queries = [
            "What's the latest news about AI developments?",
            "What's the weather like in Paris today?",
            "What are the current stock prices for major tech companies?",
        ]
        
        print("\n🎯 Example queries you can try:")
        for i, query in enumerate(example_queries, 1):
            print(f"{i}. {query}")
        
        print("\n💬 Ask questions (type 'quit' to exit):")
        print("-" * 50)
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print(f"\n🔍 Agent (searching and analyzing):", end=" ")
            try:
                agent.print_response(user_input, stream=True)
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your OpenAI API key is set in the .env file")

if __name__ == "__main__":
    main()