#!/usr/bin/env python3
"""
Agent with Memory Example

This example demonstrates how to create an Agno agent with persistent memory.
The agent can remember previous conversations and build context over time.
"""

import os
import sys
import pathlib
# Add parent directory to Python path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from model_config import get_configured_model, print_model_info

# Load environment variables
load_dotenv()

def create_agent_with_memory():
    """
    Create an agent with persistent memory using SQLite.
    """
    # Setup SQLite database for memory
    db = SqliteDb(db_file="agent_memory.db")
    model = get_configured_model()
    
    agent = Agent(
        name="Memory Assistant",
        model=model,
        db=db,
        enable_agentic_memory=True,  # Enable agent-controlled memory
        instructions=[
            "You are a personal assistant with memory capabilities.",
            "Remember important information about the user and our conversations.",
            "Refer to previous conversations when relevant.",
            "Ask clarifying questions to better understand the user's needs.",
        ],
        markdown=True,
        add_datetime_to_context=True,
    )
    
    return agent

def main():
    """
    Main function to demonstrate agent with memory.
    """
    print("🧠 Agno Agent with Memory Demo")
    print("=" * 50)
    
    try:
        agent = create_agent_with_memory()
        print("✅ Agent with memory created successfully!")
        print("💾 Memory database: agent_memory.db")
        
        print("\n💡 Tips:")
        print("- Tell the agent about yourself (name, preferences, goals)")
        print("- The agent will remember information across sessions")
        print("- Try asking about things you mentioned in previous conversations")
        
        print("\n💬 Chat with the memory-enabled agent (type 'quit' to exit):")
        print("-" * 50)
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 I'll remember our conversation for next time!")
                break
            
            if not user_input:
                continue
            
            print(f"\n🧠 Agent:", end=" ")
            try:
                agent.print_response(user_input)
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your OpenAI API key is set in the .env file")

if __name__ == "__main__":
    main()