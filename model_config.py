#!/usr/bin/env python3
"""
Model Configuration Utility

This module provides utility functions to create and configure AI models
for the Agno framework, supporting both Azure OpenAI and regular OpenAI.
"""

import os
from typing import Any, Optional


def get_configured_model(model_name: Optional[str] = None) -> Any:
    """
    Get a configured AI model based on environment variables.
    
    Args:
        model_name: Optional model name override. If not provided, uses DEFAULT_MODEL from env.
        
    Returns:
        Configured model instance (AzureOpenAI or OpenAIChat)
        
    Raises:
        ValueError: If no valid API configuration is found
    """
    # Get model name from parameter or environment
    if model_name is None:
        model_name = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    
    # Check for Azure OpenAI configuration first
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if azure_api_key and azure_endpoint:
        # Use Azure OpenAI
        from agno.models.azure.openai_chat import AzureOpenAI
        print(f"🔵 Using Azure OpenAI with model: {model_name}")
        
        return AzureOpenAI(
            id=model_name,
            # Optional: specify deployment name if different from model id
            # deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        )
        
    elif openai_api_key:
        # Use regular OpenAI
        from agno.models.openai import OpenAIChat
        print(f"🟢 Using OpenAI with model: {model_name}")
        
        return OpenAIChat(id=model_name)
        
    else:
        raise ValueError(
            "No API configuration found. Please set either:\n"
            "- Azure OpenAI: AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT\n"
            "- Regular OpenAI: OPENAI_API_KEY\n"
            "Check your .env file."
        )


def get_reasoning_model() -> Any:
    """
    Get a model specifically configured for reasoning tasks.
    Uses REASONING_MODEL from environment or falls back to DEFAULT_MODEL.
    """
    reasoning_model_name = os.getenv("REASONING_MODEL")
    if reasoning_model_name:
        return get_configured_model(reasoning_model_name)
    else:
        # Use the same model as default if no specific reasoning model is set
        return get_configured_model()


def get_fast_model() -> Any:
    """
    Get a model configured for fast responses.
    Uses FAST_MODEL from environment or falls back to DEFAULT_MODEL.
    """
    fast_model_name = os.getenv("FAST_MODEL")
    if fast_model_name:
        return get_configured_model(fast_model_name)
    else:
        # Use the same model as default if no specific fast model is set
        return get_configured_model()


def print_model_info():
    """
    Print information about the current model configuration.
    """
    print("🔧 Model Configuration:")
    print(f"   Default Model: {os.getenv('DEFAULT_MODEL', 'gpt-4o-mini')}")
    
    reasoning_model = os.getenv('REASONING_MODEL')
    if reasoning_model:
        print(f"   Reasoning Model: {reasoning_model}")
    
    fast_model = os.getenv('FAST_MODEL')
    if fast_model:
        print(f"   Fast Model: {fast_model}")
    
    # Check which provider is configured
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        print("   Provider: Azure OpenAI")
        print(f"   Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        if deployment:
            print(f"   Deployment: {deployment}")
    elif os.getenv("OPENAI_API_KEY"):
        print("   Provider: OpenAI")
    else:
        print("   ⚠️  No valid API configuration found!")
    
    print()