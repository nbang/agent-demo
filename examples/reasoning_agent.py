#!/usr/bin/env python3
"""
Agent with Reasoning Tools Example

This example demonstrates how to create an Agno agent with reasoning capabilities.
The agent can perform structured analysis and step-by-step problem solving.
"""

import os
import sys
import pathlib
# Add parent directory to Python path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from model_config import get_reasoning_model, print_model_info

# Load environment variables
load_dotenv()

def create_reasoning_agent():
    """
    Create an agent with reasoning capabilities.
    """
    model = get_reasoning_model()
    
    agent = Agent(
        name="Reasoning Assistant",
        model=model,
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are an expert problem-solving assistant with strong analytical skills.",
            "Always break down complex problems into component parts.",
            "Use step-by-step reasoning and show your thought process.",
            "Consider multiple perspectives and evaluate evidence.",
            "Identify assumptions and highlight areas of uncertainty.",
        ],
        markdown=True,
        add_datetime_to_context=True,
        stream_intermediate_steps=True,  # Show reasoning steps as they happen
    )
    
    return agent

def main():
    """
    Main function to demonstrate reasoning agent.
    """
    print("🧠 Agno Reasoning Agent Demo")
    print("=" * 50)
    
    try:
        agent = create_reasoning_agent()
        print("✅ Reasoning agent created successfully!")
        
        # Example complex problems for reasoning
        example_problems = [
            "Should a company implement a 4-day work week? Analyze the pros and cons.",
            "How would you solve traffic congestion in a major city?",
            "What are the ethical implications of AI in healthcare?",
            "Compare the environmental impact of electric cars vs. public transportation.",
        ]
        
        print("\n🎯 Example complex problems you can ask:")
        for i, problem in enumerate(example_problems, 1):
            print(f"{i}. {problem}")
        
        print("\n💭 Ask complex questions for analysis (type 'quit' to exit):")
        print("-" * 50)
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print(f"\n🧠 Agent (reasoning step by step):")
            print("-" * 30)
            try:
                agent.print_response(user_input, stream=True)
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your OpenAI API key is set in the .env file")

if __name__ == "__main__":
    main()