#!/usr/bin/env python3
"""
Improved Web Search Tools with Error Handling and Fallbacks

This module provides robust web search capabilities with proper error handling,
rate limiting, retries, and fallback strategies for when DuckDuckGo search fails.
"""

import time
import random
from typing import List, Optional, Dict, Any
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools import Toolkit
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustWebSearchTools:
    """
    Enhanced web search tools with error handling and fallback strategies.
    """
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.ddg_tools = DuckDuckGoTools()
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.last_request_time = 0
        self.min_request_interval = 2.0  # Minimum seconds between requests
        
    def _wait_for_rate_limit(self):
        """Implement rate limiting to avoid overwhelming the service."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            # Add some jitter to avoid thundering herd
            sleep_time += random.uniform(0, 0.5)
            logger.info(f"Rate limiting: waiting {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _retry_with_backoff(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry logic."""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                self._wait_for_rate_limit()
                result = func(*args, **kwargs)
                if result:  # If we got a result, return it
                    return result
                else:
                    logger.warning(f"Empty result on attempt {attempt + 1}")
                    
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    # Exponential backoff with jitter
                    delay = self.base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"All {self.max_retries} attempts failed")
        
        # If all retries failed, return a fallback response
        return self._get_fallback_response(last_exception or Exception("Unknown error"))
    
    def _get_fallback_response(self, exception: Exception) -> List[Dict[str, Any]]:
        """Provide fallback response when all search attempts fail."""
        logger.warning("Using fallback response due to search failures")
        return [{
            'title': 'Search Service Unavailable',
            'href': 'https://example.com',
            'body': f"""
            Web search is currently unavailable due to technical issues: {str(exception)}
            
            Please consider these alternatives:
            1. Use your existing knowledge base for this topic
            2. Provide general information based on common knowledge
            3. Note that current web data is not available
            4. Suggest manual verification of any time-sensitive information
            
            This is a temporary limitation and does not affect the quality of 
            analysis based on established knowledge and best practices.
            """
        }]
    
    def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform web search with robust error handling.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of search results or fallback response
        """
        logger.info(f"Searching web for: {query}")
        
        def _search():
            return self.ddg_tools.duckduckgo_search(query=query, max_results=max_results)
        
        return self._retry_with_backoff(_search)
    
    def search_news(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform news search with robust error handling.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of news results or fallback response
        """
        logger.info(f"Searching news for: {query}")
        
        def _search():
            return self.ddg_tools.duckduckgo_news(query=query, max_results=max_results)
        
        return self._retry_with_backoff(_search)

# Create a singleton instance
robust_search_tools = RobustWebSearchTools()

class ImprovedDuckDuckGoTools(Toolkit):
    """
    Drop-in replacement for DuckDuckGoTools with improved error handling.
    """
    
    def __init__(self):
        super().__init__(name="robust_duckduckgo")
        self.robust_tools = RobustWebSearchTools()
    
    def duckduckgo_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Web search with error handling."""
        return self.robust_tools.search_web(query, max_results)
    
    def duckduckgo_news(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """News search with error handling."""
        return self.robust_tools.search_news(query, max_results)

# Alternative approach: Use mock data when web search fails
class MockWebSearchTools(Toolkit):
    """
    Fallback tools that provide realistic mock data when web search is unavailable.
    Use this when you want to test multi-agent systems without web dependencies.
    """
    
    def __init__(self):
        super().__init__(name="mock_web_search")
    
    def duckduckgo_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Provide mock web search results."""
        return [
            {
                'title': f'Mock Result 1 for: {query}',
                'href': 'https://example.com/article1',
                'body': f'This is a mock search result for the query "{query}". In a real scenario, this would contain relevant information from web sources. The content would be factual and up-to-date, providing valuable insights for research purposes.'
            },
            {
                'title': f'Mock Result 2 for: {query}',
                'href': 'https://example.com/article2', 
                'body': f'Another mock result providing additional context about "{query}". This demonstrates how multiple sources would contribute different perspectives and data points to the research process.'
            },
            {
                'title': f'Industry Report: {query}',
                'href': 'https://example.com/report',
                'body': f'A comprehensive industry analysis regarding "{query}". This mock result represents the type of authoritative sources that would typically be found through web search, including statistics, expert opinions, and current trends.'
            }
        ][:max_results]
    
    def duckduckgo_news(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Provide mock news search results."""
        return [
            {
                'title': f'Breaking: Latest developments in {query}',
                'href': 'https://news.example.com/breaking',
                'body': f'Recent news coverage of "{query}" shows significant developments in the field. This mock news result represents current events and recent announcements that would be captured by real news search.',
                'date': '2025-10-15'
            },
            {
                'title': f'Analysis: Impact of {query} on industry',
                'href': 'https://news.example.com/analysis',
                'body': f'Expert analysis of how "{query}" is affecting various sectors. This represents the type of analytical news content that provides deeper insights beyond basic reporting.',
                'date': '2025-10-14'
            }
        ][:max_results]

# Helper function to create tools based on preference
def get_search_tools(mode: str = "robust") -> object:
    """
    Get search tools based on specified mode.
    
    Args:
        mode: "robust" (with retries), "mock" (fake data), or "original" (standard DDG)
        
    Returns:
        Appropriate search tools instance
    """
    if mode == "robust":
        return ImprovedDuckDuckGoTools()
    elif mode == "mock":
        return MockWebSearchTools()
    elif mode == "original":
        return DuckDuckGoTools()
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'robust', 'mock', or 'original'")