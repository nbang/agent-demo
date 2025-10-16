#!/usr/bin/env python3
"""
Agno Agent Demo Entry Point

This script provides an easy way to run the Agno agent demo.
It handles the proper import paths and runs the main agent.

Usage:
    python agent.py
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the main agent
if __name__ == "__main__":
    from src.agents.basic import main
    main()
