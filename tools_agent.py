#!/usr/bin/env python3
"""
Advanced Tool Agent Entry Point

A comprehensive demonstration of building agents with various tools and capabilities.
This agent includes web search, file operations, system information, calculations,
and other useful tools for productivity and research.

Features:
- Web search capabilities
- File system operations
- System monitoring and information
- Mathematical calculations
- Date/time utilities
- Safe system command execution

Usage:
    python tools_agent.py
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the tools agent
if __name__ == "__main__":
    from src.agents.tools import main
    main()
