#!/usr/bin/env python3
"""
Basic Agno Agent Demo

This script demonstrates how to create a simple AI agent using the Agno framework.
The agent supports both Azure OpenAI and regular OpenAI models.

Prerequisites:
1. Install dependencies: pip install -r requirements.txt
2. Set up environment variables (copy env.example to .env and fill in values)
3. Run the script: python agent.py
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from model_config import get_configured_model, print_model_info

# Load environment variables from .env file
load_dotenv()

def create_basic_agent():
    """
    Create a basic Agno agent with configured model from environment.
    """
    # Get the configured model
    model = get_configured_model()
    agent_name = "Assistant"
    
    # Create the agent
    agent = Agent(
        name=agent_name,
        model=model,
        instructions=[
            "You are a helpful AI assistant.",
            "Provide clear, accurate, and concise responses.",
            "If you're unsure about something, say so rather than guessing.",
        ],
        markdown=True,  # Enable markdown formatting in responses
        add_datetime_to_context=True,  # Add current time to context
    )
    
    return agent

def main():
    """
    Main function to run the agent demo.
    """
    print("🤖 Agno Agent Demo")
    print("=" * 50)
    
    # Show model configuration
    print_model_info()
    
    try:
        # Create the agent
        agent = create_basic_agent()
        print("✅ Agent created successfully!")
        
        # Interactive chat loop
        print("\n💬 Chat with the agent (type 'quit' to exit):")
        print("-" * 50)
        
        while True:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit command
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Get agent response
            print("\n🤖 Agent:", end=" ")
            try:
                agent.print_response(user_input)
            except Exception as e:
                print(f"❌ Error getting response: {e}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure to:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Copy .env.example to .env and add your OpenAI API key")

if __name__ == "__main__":
    main()