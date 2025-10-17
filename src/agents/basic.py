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

# Initialize services
from src.services.logging import get_agent_logger, setup_logging
from src.services.error_handling import ErrorHandler, ErrorSeverity, ErrorCategory, RecoveryStrategy
from src.services.monitoring import PerformanceMonitor
from agno.agent import Agent
from src.models.config import get_configured_model, print_model_info, test_model_connection

# Initialize services for basic agent
logger = get_agent_logger(__name__, "basic", "basic_agent")
error_handler = ErrorHandler("basic", "basic_agent")
performance_monitor = PerformanceMonitor(agent_type="basic", agent_id="basic_agent")

# Load environment variables from .env file
load_dotenv()

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
        ValueError: If input is invalid
    """
    # Basic input validation
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")
    
    # Trim whitespace
    cleaned_input = user_input.strip()
    
    # Check for reasonable length (prevent very long inputs)
    if len(cleaned_input) > 10000:
        raise ValueError("Input is too long (maximum 10,000 characters)")
    
    # Check for potential security issues (basic check)
    suspicious_patterns = ['<script', 'javascript:', 'eval(', 'exec(']
    if any(pattern.lower() in cleaned_input.lower() for pattern in suspicious_patterns):
        raise ValueError("Input contains potentially unsafe content")
    
    return cleaned_input

def main():
    """
    Main function to run the agent demo with comprehensive error handling.
    """
    # Use the global performance monitor
    perf_monitor = performance_monitor
    
    # Set up signal handlers for graceful shutdown
    setup_signal_handlers()
    
    # Display enhanced welcome banner
    display_welcome_banner()
    
    # Show system health
    print("💻 System Status: Ready")
    
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
                    stats = perf_monitor.get_summary_stats()
                    print(f"📊 Performance Stats:")
                    print(f"   Operations: {stats['total_operations']}")
                    print(f"   Success Rate: {stats['success_rate']:.1f}%")
                    print(f"   Avg Response Time: {stats['avg_response_time']:.2f}s")
                    continue
                elif user_input.lower() in ['health', 'system']:
                    print("💻 System Status: Operational")
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
                except ValueError as e:
                    print(f"❌ Input validation error: {e}")
                    logger.error(f"Validation error: {e}")
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
                    logger.info(f"User interaction completed - Input length: {len(validated_input)}, Response generated: {response_generated}, Processing time: {processing_time}s")
                    
                except Exception as e:
                    error_message = f"Agent error: {e}"
                    logger.error(f"Agent error during processing: {e}")
                    print(f"❌ {error_message}")
                    
                    # Check if error is recoverable based on type
                    if "network" in str(e).lower() or "timeout" in str(e).lower():
                        print("🔄 This appears to be a network error - please try again in a moment.")
                    else:
                        print("\n💡 Suggestions:")
                        print("   • Check your internet connection")
                        print("   • Verify your API keys are correctly set")
                        print("   • Try a simpler question if the error persists")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                error_message = f"Processing error: {e}"
                logger.error(f"Processing error: {e}")
                print(f"\n❌ {error_message}")
                
                # For critical errors, ask if user wants to continue
                if "critical" in str(e).lower() or "fatal" in str(e).lower():
                    try:
                        continue_choice = input("\n❓ Critical error detected. Do you want to continue? (y/n): ").strip().lower()
                        if continue_choice not in ['y', 'yes']:
                            print("👋 Goodbye!")
                            logger.info("User chose to exit after critical error")
                            break
                    except (KeyboardInterrupt, EOFError):
                        print("\n👋 Goodbye!")
                        logger.info("User exited after critical error")
                        break
    
    except ValueError as e:
        error_message = f"Configuration error: {e}"
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ {error_message}")
        print("\n🔧 Please check your configuration and try again.")
    except ConnectionError as e:
        error_message = f"Network error: {e}"
        logger.error(f"Network error: {e}")
        print(f"\n❌ {error_message}")
        print("\n🌐 Please check your internet connection and try again.")
    except Exception as e:
        error_message = f"Unexpected error: {e}"
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ {error_message}")
        
        print("\n💡 Try these steps:")
        print("   1. Check your internet connection")
        print("   2. Verify your API keys are correctly set")
        print("   3. Try restarting the application")
    
    # Show final performance report
    print("\n📊 Final Performance Summary:")
    stats = perf_monitor.get_summary_stats()
    print(f"   Total Operations: {stats['total_operations']}")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")
    if stats['avg_response_time'] > 0:
        print(f"   Avg Response Time: {stats['avg_response_time']:.2f}s")
    
    print("\n👋 Thank you for using Agno Agent Demo!")

if __name__ == "__main__":
    main()