#!/usr/bin/env python3
"""
Search Configuration for Multi-Agent Examples

This module allows easy configuration of search tools across all multi-agent examples.
You can switch between different modes based on your needs and network conditions.
"""

import os
from typing import Literal
from robust_search_tools import ImprovedDuckDuckGoTools, MockWebSearchTools
from agno.tools.duckduckgo import DuckDuckGoTools

# Configuration
SEARCH_MODE = os.getenv("SEARCH_MODE", "robust")  # Can be: "robust", "mock", "original"

# Rate limiting settings
MAX_RETRIES = int(os.getenv("SEARCH_MAX_RETRIES", "3"))
BASE_DELAY = float(os.getenv("SEARCH_BASE_DELAY", "1.0"))
MIN_REQUEST_INTERVAL = float(os.getenv("SEARCH_MIN_INTERVAL", "2.0"))

def get_search_tools(mode: Literal["robust", "mock", "original"] = None):
    """
    Get search tools based on configuration.
    
    Args:
        mode: Override the default search mode
        
    Returns:
        Appropriate search tools instance
    """
    selected_mode = mode or SEARCH_MODE
    
    if selected_mode == "robust":
        # Use improved tools with error handling and retries
        return ImprovedDuckDuckGoTools()
    elif selected_mode == "mock":
        # Use mock data (good for testing without network)
        return MockWebSearchTools()
    elif selected_mode == "original":
        # Use original DuckDuckGo tools (may fail with rate limits)
        return DuckDuckGoTools()
    else:
        raise ValueError(f"Unknown search mode: {selected_mode}")

def print_search_config():
    """Print current search configuration."""
    print("🔍 Search Tools Configuration")
    print("=" * 40)
    print(f"Mode: {SEARCH_MODE}")
    print(f"Max Retries: {MAX_RETRIES}")
    print(f"Base Delay: {BASE_DELAY}s")
    print(f"Min Request Interval: {MIN_REQUEST_INTERVAL}s")
    print()
    
    mode_descriptions = {
        "robust": "✅ Robust mode with error handling, retries, and rate limiting",
        "mock": "🧪 Mock mode with fake data (good for testing)",
        "original": "⚡ Original mode (fast but may fail with rate limits)"
    }
    
    print("Available modes:")
    for mode, description in mode_descriptions.items():
        prefix = "→ " if mode == SEARCH_MODE else "  "
        print(f"{prefix}{mode}: {description}")
    
    print("\n💡 To change mode, set SEARCH_MODE environment variable:")
    print("   export SEARCH_MODE=robust    # (recommended)")
    print("   export SEARCH_MODE=mock      # (for testing)")
    print("   export SEARCH_MODE=original  # (if network is stable)")

if __name__ == "__main__":
    print_search_config()