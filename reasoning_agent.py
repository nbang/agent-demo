#!/usr/bin/env python3
"""
Advanced Reasoning Agent Entry Point

A sophisticated AI agent that performs structured, step-by-step problem analysis 
with comprehensive reasoning capabilities. This agent breaks down complex problems, 
shows detailed reasoning steps, and provides logical analysis with real-time 
reasoning visibility.

Features:
- Step-by-step structured problem analysis
- Multi-perspective consideration and evaluation
- Assumption identification and uncertainty handling
- Evidence-based reasoning and evaluation
- Real-time intermediate step streaming
- Comprehensive problem decomposition
- Different reasoning patterns (deductive, inductive, abductive)

Usage:
    python reasoning_agent.py
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the reasoning agent
if __name__ == "__main__":
    from src.agents.reasoning import main
    main()