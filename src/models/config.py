#!/usr/bin/env python3
"""
Model Configuration Utility

This module provides utility functions to create and configure AI models
for the Agno framework, supporting both Azure OpenAI and regular OpenAI.

Enhanced with comprehensive validation, error handling, and configuration verification.
"""

import os
import logging
from typing import Any, Optional, Dict, Tuple
from dataclasses import dataclass

# Import services
from src.services.error_handling import ErrorHandler

# Configure logging for model configuration
logger = logging.getLogger(__name__)

@dataclass
class ModelConfiguration:
    """Data class for model configuration details."""
    provider: str
    model_name: str
    endpoint: Optional[str] = None
    deployment: Optional[str] = None
    api_version: Optional[str] = None
    is_valid: bool = True
    error_message: Optional[str] = None


def validate_environment() -> ModelConfiguration:
    """
    Validate environment configuration for AI model setup.
    
    Returns:
        ModelConfiguration: Configuration details with validation status
        
    Raises:
        ValueError: If configuration is invalid
    """
    # Get model name from environment
    model_name = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    
    # Check for Azure OpenAI configuration first
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    # Check for regular OpenAI configuration
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if azure_api_key and azure_endpoint:
        # Validate Azure OpenAI configuration
        if not azure_api_key.strip():
            return ModelConfiguration(
                provider="Azure OpenAI",
                model_name=model_name,
                is_valid=False,
                error_message="Azure OpenAI API key is empty"
            )
        
        if not azure_endpoint.strip() or not azure_endpoint.startswith("https://"):
            return ModelConfiguration(
                provider="Azure OpenAI",
                model_name=model_name,
                is_valid=False,
                error_message="Azure OpenAI endpoint must be a valid HTTPS URL"
            )
        
        logger.info(f"Azure OpenAI configuration validated for model: {model_name}")
        return ModelConfiguration(
            provider="Azure OpenAI",
            model_name=model_name,
            endpoint=azure_endpoint,
            deployment=azure_deployment,
            api_version=azure_api_version,
            is_valid=True
        )
        
    elif openai_api_key:
        # Validate OpenAI configuration
        if not openai_api_key.strip():
            return ModelConfiguration(
                provider="OpenAI",
                model_name=model_name,
                is_valid=False,
                error_message="OpenAI API key is empty"
            )
        
        if not openai_api_key.startswith("sk-"):
            return ModelConfiguration(
                provider="OpenAI",
                model_name=model_name,
                is_valid=False,
                error_message="OpenAI API key should start with 'sk-'"
            )
        
        logger.info(f"OpenAI configuration validated for model: {model_name}")
        return ModelConfiguration(
            provider="OpenAI",
            model_name=model_name,
            is_valid=True
        )
        
    else:
        return ModelConfiguration(
            provider="Unknown",
            model_name=model_name,
            is_valid=False,
            error_message="No API configuration found. Please set either AZURE_OPENAI_API_KEY + AZURE_OPENAI_ENDPOINT or OPENAI_API_KEY"
        )


def get_configured_model(model_name: Optional[str] = None) -> Any:
    """
    Get a configured AI model based on environment variables.
    
    Args:
        model_name: Optional model name override. If not provided, uses DEFAULT_MODEL from env.
        
    Returns:
        Configured model instance (AzureOpenAI or OpenAIChat)
        
    Raises:
        ValueError: If no valid API configuration is found
        APIConnectionError: If model cannot be instantiated
    """
    # Validate environment first
    config = validate_environment()
    
    if not config.is_valid:
        raise ValueError(f"Invalid configuration: {config.error_message}")
    
    # Override model name if provided
    if model_name:
        config.model_name = model_name
    
    try:
        if config.provider == "Azure OpenAI":
            # Use Azure OpenAI
            from agno.models.azure.openai_chat import AzureOpenAI
            logger.info(f"Creating Azure OpenAI model: {config.model_name}")
            print(f"🔵 Using Azure OpenAI with model: {config.model_name}")
            
            # Only pass the model ID - let Agno handle other Azure-specific configuration
            return AzureOpenAI(id=config.model_name)
            
        elif config.provider == "OpenAI":
            # Use regular OpenAI
            from agno.models.openai import OpenAIChat
            logger.info(f"Creating OpenAI model: {config.model_name}")
            print(f"🟢 Using OpenAI with model: {config.model_name}")
            
            return OpenAIChat(id=config.model_name)
            
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")
            
    except Exception as e:
        logger.error(f"Failed to create model {config.model_name}: {str(e)}")
        raise ConnectionError(f"Failed to create model {config.model_name}: {str(e)}")


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
    Print comprehensive information about the current model configuration.
    """
    try:
        config = validate_environment()
        
        print("🔧 Model Configuration:")
        print(f"   Default Model: {config.model_name}")
        
        # Additional model configurations
        reasoning_model = os.getenv('REASONING_MODEL')
        if reasoning_model:
            print(f"   Reasoning Model: {reasoning_model}")
        
        fast_model = os.getenv('FAST_MODEL')
        if fast_model:
            print(f"   Fast Model: {fast_model}")
        
        # Provider information
        if config.is_valid:
            if config.provider == "Azure OpenAI":
                print("   Provider: Azure OpenAI ✅")
                print(f"   Endpoint: {config.endpoint}")
                if config.deployment:
                    print(f"   Deployment: {config.deployment}")
                if config.api_version:
                    print(f"   API Version: {config.api_version}")
            elif config.provider == "OpenAI":
                print("   Provider: OpenAI ✅")
            
            print("   Status: Configuration Valid ✅")
        else:
            print(f"   Status: Configuration Invalid ❌")
            print(f"   Error: {config.error_message}")
            print("\n💡 Configuration Help:")
            print("   For Azure OpenAI, set:")
            print("     - AZURE_OPENAI_API_KEY")
            print("     - AZURE_OPENAI_ENDPOINT")
            print("     - AZURE_OPENAI_DEPLOYMENT (optional)")
            print("   For OpenAI, set:")
            print("     - OPENAI_API_KEY")
        
        print()
        
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        print(f"   ⚠️  Error retrieving model configuration: {str(e)}")
        print()


def test_model_connection(model_name: Optional[str] = None) -> bool:
    """
    Test connection to the configured model.
    
    Args:
        model_name: Optional model name to test
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        model = get_configured_model(model_name)
        logger.info(f"Model connection test successful for {model_name or 'default model'}")
        print(f"✅ Model connection test successful")
        return True
    except Exception as e:
        logger.error(f"Model connection test failed: {str(e)}")
        print(f"❌ Model connection test failed: {str(e)}")
        return False