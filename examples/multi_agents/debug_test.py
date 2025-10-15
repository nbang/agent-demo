#!/usr/bin/env python3
"""Minimal test for debugging issues"""

import os
import sys
import pathlib
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

def main():
    load_dotenv()
    
    try:
        # Test 1: Model creation
        print("1. Testing model creation...")
        from model_config import get_configured_model
        model = get_configured_model()
        print(f"   ✅ Model: {type(model).__name__}")
        
        # Test 2: Agent creation with mock search
        print("2. Testing agent creation...")
        from agno.agent import Agent
        from search_config import get_search_tools
        
        agent = Agent(
            name="Test Agent",
            role="Simple test agent",
            model=model,
            tools=[get_search_tools("mock")],
            instructions="You are a test agent.",
            markdown=True,
        )
        print("   ✅ Agent created successfully")
        
        # Test 3: Simple response
        print("3. Testing agent response...")
        response = agent.run("What is 2+2?", stream=False)
        if response and response.content:
            print(f"   ✅ Response: {response.content[:50]}...")
        else:
            print("   ❌ No response received")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
