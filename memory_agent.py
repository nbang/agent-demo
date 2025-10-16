#!/usr/bin/env python3
"""
Advanced Memory Agent Entry Point

A sophisticated AI agent with persistent memory capabilities that stores and retrieves
conversation history, maintains context across sessions, and provides personalized 
responses based on previous interactions.

Features:
- Persistent conversation history across application sessions
- Intelligent memory storage with agentic control
- Contextual recall of relevant past interactions
- Personalized responses based on interaction history
- Privacy-conscious local data storage
- Performance monitoring and optimization

Usage:
    python memory_agent.py
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the memory agent
if __name__ == "__main__":
    from src.agents.memory import main
    main()