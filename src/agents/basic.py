#!/usr/bin/env python3
"""
Basic Agno Agent Demo

This script demonstrates how to create a simple AI agent using the Agno framework.
The agent supports both Azure OpenAI and regular OpenAI models.

Prerequisites:
1. Install dependencies: pip install -r requirements.txt
2. Set up environment variables (copy env.example to .env and fill in values)
3. Run the script: python agent.py
"""

import os
import signal
import sys
import time
from dotenv import load_dotenv

# Add project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# Initialize logging first
from src.lib.logging_config import get_logger, log_user_interaction, log_security_event
from agno.agent import Agent
from src.models.config import get_configured_model, print_model_info, test_model_connection
from src.lib.error_handling import (
    AgentError, ConfigurationError, APIError, NetworkError, 
    ValidationError, UserInteractionError, handle_error, 
    create_error_recovery_suggestions, is_recoverable_error
)
from src.services.performance_monitor import get_performance_monitor, monitor_agent_response

# Load environment variables from .env file
load_dotenv()

# Get logger for this module
logger = get_logger(__name__)

def create_basic_agent():
    """
    Create a basic Agno agent with configured model from environment.
    """
    # Get the configured model
    model = get_configured_model()
    agent_name = "Agno Assistant"
    
    # Enhanced instructions for better performance
    enhanced_instructions = [
        "You are Agno Assistant, a helpful AI assistant powered by the Agno framework.",
        "Provide clear, accurate, and concise responses with helpful context.",
        "Use markdown formatting to structure your responses when appropriate.",
        "If you're unsure about something, say so rather than guessing.",
        "Be conversational and friendly while maintaining professionalism.",
        "When providing code examples, use proper syntax highlighting.",
        "If the user asks about complex topics, break them down into digestible parts.",
    ]
    
    # Create the agent with enhanced configuration
    agent = Agent(
        name=agent_name,
        model=model,
        instructions=enhanced_instructions,
        markdown=True,  # Enable markdown formatting in responses
        add_datetime_to_context=True,  # Add current time to context
        # Note: Response streaming is handled by the agent automatically
    )
    
    return agent

def display_welcome_banner():
    """Display an enhanced welcome banner with helpful information."""
    try:
        print("🤖 Agno Agent Demo")
    except UnicodeEncodeError:
        print("Agno Agent Demo")
    print("=" * 60)
    print("Welcome to the enhanced Agno Agent Demo!")
    print("This agent features:")
    try:
        print("  • Multi-model support (OpenAI & Azure OpenAI)")
        print("  • Comprehensive error handling")
        print("  • Input validation and security")
        print("  • Graceful shutdown handling")
        print("  • Real-time response streaming")
    except UnicodeEncodeError:
        print("  - Multi-model support (OpenAI & Azure OpenAI)")
        print("  - Comprehensive error handling")
        print("  - Input validation and security")
        print("  - Graceful shutdown handling")
        print("  - Real-time response streaming")
    print("=" * 60)

def display_chat_instructions():
    """Display chat instructions and available commands."""
    try:
        print("\n💬 Chat Instructions:")
    except UnicodeEncodeError:
        print("\nChat Instructions:")
    print("=" * 40)
    try:
        print("• Type your message and press Enter")
        print("• Type 'quit', 'exit', 'bye', or 'q' to exit")
        print("• Press Ctrl+C at any time for graceful shutdown")
        print("• Empty messages are ignored")
        print("• Maximum message length: 10,000 characters")
    except UnicodeEncodeError:
        print("- Type your message and press Enter")
        print("- Type 'quit', 'exit', 'bye', or 'q' to exit")
        print("- Press Ctrl+C at any time for graceful shutdown")
        print("- Empty messages are ignored")
        print("- Maximum message length: 10,000 characters")
    print("=" * 40)

def setup_signal_handlers():
    """Set up signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        print("\n\n👋 Received shutdown signal. Goodbye!")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def validate_user_input(user_input: str) -> str:
    """
    Validate and sanitize user input.
    
    Args:
        user_input: Raw user input
        
    Returns:
        str: Validated and cleaned input
        
    Raises:
        ValidationError: If input is invalid
    """
    # Basic input validation
    if not isinstance(user_input, str):
        raise ValidationError("Input must be a string")
    
    # Trim whitespace
    cleaned_input = user_input.strip()
    
    # Check for reasonable length (prevent very long inputs)
    if len(cleaned_input) > 10000:
        raise ValidationError("Input is too long (maximum 10,000 characters)")
    
    # Check for potential security issues (basic check)
    suspicious_patterns = ['<script', 'javascript:', 'eval(', 'exec(']
    if any(pattern.lower() in cleaned_input.lower() for pattern in suspicious_patterns):
        raise ValidationError("Input contains potentially unsafe content")
    
    return cleaned_input

def main():
    """
    Main function to run the agent demo with comprehensive error handling.
    """
    # Get performance monitor
    perf_monitor = get_performance_monitor()
    
    # Set up signal handlers for graceful shutdown
    setup_signal_handlers()
    
    # Display enhanced welcome banner
    display_welcome_banner()
    
    # Show system health
    perf_monitor.print_system_health()
    
    # Show model configuration
    print_model_info()
    
    # Test model connection with performance monitoring
    print("🔍 Testing model connection...")
    with perf_monitor.monitor_operation("model_connection_test"):
        if not test_model_connection():
            print("❌ Cannot continue without a working model connection.")
            return
    
    try:
        # Create the agent
        print("🚀 Creating agent...")
        agent = create_basic_agent()
        print("✅ Agent created successfully!")
        
        # Display chat instructions
        display_chat_instructions()
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("👋 Goodbye!")
                    break
                
                # Check for special commands
                if user_input.lower() in ['stats', 'performance', 'perf']:
                    perf_monitor.print_performance_report()
                    continue
                elif user_input.lower() in ['health', 'system']:
                    perf_monitor.print_system_health()
                    continue
                elif user_input.lower() in ['help', 'commands']:
                    print("\n🔧 Available Commands:")
                    print("• stats/performance/perf - Show performance statistics")
                    print("• health/system - Show system health information")
                    print("• help/commands - Show this help message")
                    print("• quit/exit/bye/q - Exit the application")
                    continue
                
                # Skip empty inputs
                if not user_input:
                    continue
                
                # Validate user input
                try:
                    validated_input = validate_user_input(user_input)
                except ValidationError as e:
                    print(f"❌ {handle_error(e)}")
                    continue
                
                # Get agent response with performance monitoring
                print("\n🤖 Agent:", end=" ")
                start_time = time.time()
                response_generated = False
                
                try:
                    with perf_monitor.monitor_operation("agent_response"):
                        agent.print_response(validated_input)
                        response_generated = True
                        
                    # Log successful interaction
                    processing_time = time.time() - start_time
                    log_user_interaction(len(validated_input), response_generated, processing_time)
                    
                except Exception as e:
                    error_message = handle_error(e)
                    print(f"❌ {error_message}")
                    
                    # Check if error is recoverable
                    if is_recoverable_error(e):
                        print("🔄 This error might be temporary. Try again in a moment.")
                    else:
                        suggestions = create_error_recovery_suggestions(e)
                        if suggestions:
                            print("\n💡 Suggestions:")
                            for suggestion in suggestions[:3]:  # Show top 3 suggestions
                                print(f"   • {suggestion}")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                error_message = handle_error(e)
                print(f"\n❌ {error_message}")
                
                # For critical errors, ask if user wants to continue
                if isinstance(e, AgentError) and e.severity.value in ['high', 'critical']:
                    try:
                        continue_choice = input("\n❓ Do you want to continue? (y/n): ").strip().lower()
                        if continue_choice not in ['y', 'yes']:
                            print("👋 Goodbye!")
                            break
                    except (KeyboardInterrupt, EOFError):
                        print("\n� Goodbye!")
                        break
    
    except ConfigurationError as e:
        error_message = handle_error(e)
        print(f"\n❌ {error_message}")
        print("\n🔧 Fix the configuration and try again.")
    except APIError as e:
        error_message = handle_error(e)
        print(f"\n❌ {error_message}")
    except NetworkError as e:
        error_message = handle_error(e)
        print(f"\n❌ {error_message}")
    except Exception as e:
        error_message = handle_error(e)
        print(f"\n❌ {error_message}")
        
        suggestions = create_error_recovery_suggestions(e)
        if suggestions:
            print("\n💡 Try these steps:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")
    
    # Show final performance report
    print("\n📊 Final Performance Summary:")
    perf_monitor.print_performance_report()
    
    print("\n👋 Thank you for using Agno Agent Demo!")

if __name__ == "__main__":
    main()