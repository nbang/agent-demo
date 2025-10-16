#!/usr/bin/env python3
"""
Test Suite for Agno Agent Demo

Basic test suite covering model configuration, error handling, and core functionality.
Run with: python -m pytest tests/ -v
"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_config import (
    validate_environment, ModelConfiguration, 
    ConfigurationError, test_model_connection
)
from error_handling import (
    AgentError, APIError, NetworkError, ValidationError,
    handle_error, is_recoverable_error
)
from performance_monitor import PerformanceMonitor
from agent import validate_user_input

class TestModelConfiguration:
    """Test model configuration functionality."""
    
    def test_validate_environment_no_config(self):
        """Test validation with no API configuration."""
        with patch.dict(os.environ, {}, clear=True):
            config = validate_environment()
            assert not config.is_valid
            assert "No API configuration found" in config.error_message
    
    def test_validate_environment_openai_valid(self):
        """Test validation with valid OpenAI configuration."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test123456"}, clear=True):
            config = validate_environment()
            assert config.is_valid
            assert config.provider == "OpenAI"
    
    def test_validate_environment_openai_invalid_key(self):
        """Test validation with invalid OpenAI key format."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "invalid-key"}, clear=True):
            config = validate_environment()
            assert not config.is_valid
            assert "should start with 'sk-'" in config.error_message
    
    def test_validate_environment_azure_valid(self):
        """Test validation with valid Azure OpenAI configuration."""
        with patch.dict(os.environ, {
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_ENDPOINT": "https://test.openai.azure.com"
        }, clear=True):
            config = validate_environment()
            assert config.is_valid
            assert config.provider == "Azure OpenAI"
    
    def test_validate_environment_azure_invalid_endpoint(self):
        """Test validation with invalid Azure endpoint."""
        with patch.dict(os.environ, {
            "AZURE_OPENAI_API_KEY": "test-key",
            "AZURE_OPENAI_ENDPOINT": "invalid-endpoint"
        }, clear=True):
            config = validate_environment()
            assert not config.is_valid
            assert "valid HTTPS URL" in config.error_message

class TestErrorHandling:
    """Test error handling functionality."""
    
    def test_configuration_error_handling(self):
        """Test configuration error handling."""
        error = ConfigurationError("Test configuration error")
        message = handle_error(error)
        
        assert "Configuration Issue" in message
        assert "Test configuration error" in message
        assert "Quick Fix" in message
    
    def test_api_error_handling(self):
        """Test API error handling."""
        error = APIError("Test API error", api_provider="OpenAI", status_code=401)
        message = handle_error(error)
        
        assert "API Error (OpenAI)" in message
        assert "Status: 401" in message
        assert "authentication issue" in message
    
    def test_validation_error_handling(self):
        """Test validation error handling."""
        error = ValidationError("Test validation error", field_name="input")
        message = handle_error(error)
        
        assert "Input Error" in message
        assert "Field: input" in message
    
    def test_is_recoverable_error(self):
        """Test recoverable error detection."""
        # Network errors are recoverable
        assert is_recoverable_error(NetworkError("Network issue"))
        
        # API rate limiting is recoverable
        assert is_recoverable_error(APIError("Rate limited", status_code=429))
        
        # Configuration errors are not recoverable
        assert not is_recoverable_error(ConfigurationError("Config issue"))
        
        # Validation errors are not recoverable
        assert not is_recoverable_error(ValidationError("Invalid input"))

class TestInputValidation:
    """Test input validation functionality."""
    
    def test_valid_input(self):
        """Test valid user input."""
        result = validate_user_input("Hello, how are you?")
        assert result == "Hello, how are you?"
    
    def test_whitespace_trimming(self):
        """Test whitespace trimming."""
        result = validate_user_input("  Hello world  ")
        assert result == "Hello world"
    
    def test_empty_input_after_trimming(self):
        """Test empty input after trimming."""
        result = validate_user_input("   ")
        assert result == ""
    
    def test_input_too_long(self):
        """Test input length validation."""
        long_input = "x" * 10001
        with pytest.raises(ValidationError) as exc_info:
            validate_user_input(long_input)
        assert "too long" in str(exc_info.value)
    
    def test_suspicious_input(self):
        """Test detection of potentially unsafe input."""
        suspicious_inputs = [
            "<script>alert('test')</script>",
            "javascript:alert('test')",
            "eval('malicious code')",
            "exec('harmful command')"
        ]
        
        for suspicious_input in suspicious_inputs:
            with pytest.raises(ValidationError) as exc_info:
                validate_user_input(suspicious_input)
            assert "unsafe content" in str(exc_info.value)
    
    def test_non_string_input(self):
        """Test non-string input handling."""
        with pytest.raises(ValidationError) as exc_info:
            validate_user_input(123)
        assert "must be a string" in str(exc_info.value)

class TestPerformanceMonitor:
    """Test performance monitoring functionality."""
    
    def test_performance_monitor_creation(self):
        """Test performance monitor creation."""
        monitor = PerformanceMonitor(max_history=50)
        assert monitor.total_operations == 0
        assert monitor.successful_operations == 0
        assert len(monitor.metrics_history) == 0
    
    def test_monitor_operation_success(self):
        """Test successful operation monitoring."""
        monitor = PerformanceMonitor()
        
        with monitor.monitor_operation("test_operation"):
            pass  # Successful operation
        
        assert monitor.total_operations == 1
        assert monitor.successful_operations == 1
        assert len(monitor.metrics_history) == 1
        
        metrics = monitor.metrics_history[0]
        assert metrics.operation == "test_operation"
        assert metrics.success is True
        assert metrics.response_time > 0
    
    def test_monitor_operation_failure(self):
        """Test failed operation monitoring."""
        monitor = PerformanceMonitor()
        
        with pytest.raises(ValueError):
            with monitor.monitor_operation("test_operation"):
                raise ValueError("Test error")
        
        assert monitor.total_operations == 1
        assert monitor.successful_operations == 0
        assert len(monitor.metrics_history) == 1
        
        metrics = monitor.metrics_history[0]
        assert metrics.operation == "test_operation"
        assert metrics.success is False
        assert metrics.error_message == "Test error"
    
    def test_summary_stats_empty(self):
        """Test summary stats with no operations."""
        monitor = PerformanceMonitor()
        stats = monitor.get_summary_stats()
        
        assert stats["total_operations"] == 0
        assert stats["successful_operations"] == 0
        assert stats["success_rate"] == 0.0
        assert stats["avg_response_time"] == 0.0
    
    def test_summary_stats_with_operations(self):
        """Test summary stats with operations."""
        monitor = PerformanceMonitor()
        
        # Add some successful operations
        with monitor.monitor_operation("op1"):
            pass
        with monitor.monitor_operation("op2"):
            pass
        
        stats = monitor.get_summary_stats()
        
        assert stats["total_operations"] == 2
        assert stats["successful_operations"] == 2
        assert stats["success_rate"] == 100.0
        assert stats["avg_response_time"] > 0

if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])