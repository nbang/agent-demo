#!/usr/bin/env python3
"""
Comprehensive Agno Agent Demo - Single File

This script demonstrates the complete Agno framework capabilities in a single file,
combining basic agent functionality, memory capabilities, reasoning tools, and
various utility tools for a comprehensive AI assistant experience.

Features:
- Multi-model support (OpenAI & Azure OpenAI)
- Persistent memory across sessions with SQLite database
- Advanced reasoning capabilities with step-by-step analysis
- Comprehensive tool set including web search, file operations, system info
- Error handling, performance monitoring, and logging
- Interactive mode selection for different agent types
- Graceful shutdown and signal handling

Prerequisites:
1. Install dependencies: pip install -r requirements.txt
2. Set up environment variables (copy env.example to .env and fill in values)
3. Run the script: python single_agent_demo.py

Usage:
    python single_agent_demo.py
"""

import os
import signal
import sys
import time
import json
import subprocess
import platform
import psutil
import math
import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Add project root to Python path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Initialize services and imports
try:
    from agno.agent import Agent
    from agno.db.sqlite import SqliteDb
    from agno.tools.duckduckgo import DuckDuckGoTools
    from agno.tools.reasoning import ReasoningTools
    from agno.tools import tool
    from src.services.logging import get_agent_logger, setup_logging
    from src.services.error_handling import ErrorHandler, ErrorSeverity, ErrorCategory, RecoveryStrategy
    from src.services.monitoring import PerformanceMonitor
    from src.models.config import get_configured_model, get_reasoning_model, print_model_info, test_model_connection
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please ensure all required dependencies are installed.")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# Initialize global services
setup_logging()
logger = get_agent_logger(__name__, "combined", "single_agent")
error_handler = ErrorHandler("combined", "single_agent")
performance_monitor = PerformanceMonitor(agent_type="combined", agent_id="single_agent")

# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

@tool
def list_directory(path: str = ".") -> str:
    """List contents of a directory with detailed information."""
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return f"Error: Path {path} does not exist"
        
        if not path_obj.is_dir():
            return f"Error: Path {path} is not a directory"
        
        items = []
        for item in path_obj.iterdir():
            item_type = "directory" if item.is_dir() else "file"
            size = f" ({item.stat().st_size} bytes)" if item.is_file() else ""
            modified = datetime.datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            items.append(f"{item_type}: {item.name}{size} (modified: {modified})")
        
        result = f"Contents of {path_obj.absolute()}:\n"
        result += f"Total items: {len(items)}\n\n"
        result += "\n".join(items)
        return result
    except PermissionError:
        return f"Error: Permission denied accessing {path}"
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@tool
def read_file(file_path: str, max_lines: int = 100) -> str:
    """Read contents of a text file."""
    try:
        path_obj = Path(file_path)
        if not path_obj.exists():
            return f"Error: File {file_path} does not exist"
        
        if not path_obj.is_file():
            return f"Error: Path {file_path} is not a file"
        
        with open(path_obj, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            truncated_msg = f"\n\n[File truncated - showing first {max_lines} lines of {total_lines}]"
        else:
            truncated_msg = ""
        
        result = f"Contents of {path_obj.absolute()}:\n"
        result += f"File size: {path_obj.stat().st_size} bytes\n\n"
        result += ''.join(lines) + truncated_msg
        return result
    except UnicodeDecodeError:
        return f"Error: File {file_path} is not a text file or has encoding issues"
    except PermissionError:
        return f"Error: Permission denied reading {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def get_file_info(file_path: str) -> str:
    """Get detailed information about a file or directory."""
    try:
        path_obj = Path(file_path)
        if not path_obj.exists():
            return f"Error: Path {file_path} does not exist"
        
        stat = path_obj.stat()
        result = f"Information for: {path_obj.absolute()}\n"
        result += f"Name: {path_obj.name}\n"
        result += f"Type: {'directory' if path_obj.is_dir() else 'file'}\n"
        result += f"Size: {stat.st_size} bytes\n"
        result += f"Created: {datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"Modified: {datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"Accessed: {datetime.datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += f"Permissions: {oct(stat.st_mode)[-3:]}\n"
        result += f"Readable: {'Yes' if os.access(path_obj, os.R_OK) else 'No'}\n"
        result += f"Writable: {'Yes' if os.access(path_obj, os.W_OK) else 'No'}\n"
        result += f"Executable: {'Yes' if os.access(path_obj, os.X_OK) else 'No'}"
        return result
    except Exception as e:
        return f"Error getting file info: {str(e)}"

@tool
def get_system_info() -> str:
    """Get comprehensive system information."""
    try:
        result = "System Information:\n"
        result += "=" * 50 + "\n\n"
        
        # Platform info
        result += f"System: {platform.system()} {platform.release()}\n"
        result += f"Machine: {platform.machine()}\n"
        result += f"Processor: {platform.processor()}\n"
        result += f"Python: {platform.python_version()}\n\n"
        
        # Memory info
        memory = psutil.virtual_memory()
        result += f"Memory:\n"
        result += f"  Total: {memory.total / (1024**3):.1f} GB\n"
        result += f"  Used: {memory.used / (1024**3):.1f} GB ({memory.percent}%)\n"
        result += f"  Available: {memory.available / (1024**3):.1f} GB\n\n"
        
        # CPU info
        result += f"CPU:\n"
        result += f"  Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count()} logical\n"
        result += f"  Usage: {psutil.cpu_percent(interval=1)}%\n\n"
        
        # Disk info
        result += "Disk Usage:\n"
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                result += f"  {partition.device} ({partition.fstype}): "
                result += f"{usage.used / (1024**3):.1f} GB / {usage.total / (1024**3):.1f} GB "
                result += f"({(usage.used / usage.total) * 100:.1f}%)\n"
            except PermissionError:
                continue
        
        return result
    except Exception as e:
        return f"Error getting system info: {str(e)}"

@tool
def run_safe_command(command: str, timeout: int = 30) -> str:
    """Run a safe system command with security restrictions."""
    # Security: Only allow specific safe commands
    safe_commands = [
        'ls', 'dir', 'pwd', 'date', 'time', 'whoami', 'hostname',
        'python --version', 'pip --version', 'git --version',
        'echo', 'head', 'tail', 'wc'
    ]
    
    command_base = command.split()[0] if command.split() else ""
    if not any(command.startswith(safe_cmd) for safe_cmd in safe_commands):
        return f"Error: Command '{command_base}' is not allowed for security reasons.\nAllowed commands: {', '.join(safe_commands)}"
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        output = f"Command: {command}\n"
        output += f"Exit Code: {result.returncode}\n\n"
        
        if result.stdout:
            output += f"Output:\n{result.stdout}\n"
        
        if result.stderr:
            output += f"Errors:\n{result.stderr}\n"
        
        return output
    except subprocess.TimeoutExpired:
        return f"Error: Command '{command}' timed out after {timeout} seconds"
    except Exception as e:
        return f"Error running command: {str(e)}"

@tool
def calculate_math(expression: str) -> str:
    """Safely calculate mathematical expressions."""
    try:
        # Security: Only allow safe mathematical operations
        allowed_chars = set('0123456789+-*/.() ')
        allowed_functions = ['abs', 'round', 'min', 'max', 'sum', 'sqrt', 'pow']
        
        # Basic validation
        if not all(c in allowed_chars or c.isalpha() for c in expression):
            return "Error: Expression contains invalid characters"
        
        # Replace math functions
        safe_expr = expression
        for func in allowed_functions:
            if func in safe_expr:
                if func == 'sqrt':
                    safe_expr = safe_expr.replace('sqrt', 'math.sqrt')
                elif func == 'pow':
                    safe_expr = safe_expr.replace('pow', 'math.pow')
                else:
                    safe_expr = safe_expr.replace(func, f'math.{func}' if hasattr(math, func) else func)
        
        # Evaluate safely
        result = eval(safe_expr, {"__builtins__": {}, "math": math})
        return f"Expression: {expression}\nResult: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError as e:
        return f"Error: Invalid mathematical operation - {str(e)}"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"

@tool
def get_current_time(timezone: str = "local") -> str:
    """Get current date and time information."""
    try:
        now = datetime.datetime.now()
        result = f"Current Date and Time:\n"
        result += f"Date: {now.strftime('%Y-%m-%d')}\n"
        result += f"Time: {now.strftime('%H:%M:%S')}\n"
        result += f"Weekday: {now.strftime('%A')}\n"
        result += f"Month: {now.strftime('%B')}\n"
        result += f"Year: {now.year}\n"
        result += f"Timestamp: {int(now.timestamp())}\n"
        result += f"ISO Format: {now.isoformat()}"
        return result
    except Exception as e:
        return f"Error getting time: {str(e)}"

# ============================================================================
# AGENT CREATION FUNCTIONS
# ============================================================================

def create_basic_agent() -> Agent:
    """Create a basic Agno agent with enhanced capabilities."""
    model = get_configured_model()
    
    enhanced_instructions = [
        "You are Agno Assistant, a helpful AI assistant powered by the Agno framework.",
        "Provide clear, accurate, and concise responses with helpful context.",
        "Use markdown formatting to structure your responses when appropriate.",
        "If you're unsure about something, say so rather than guessing.",
        "Be conversational and friendly while maintaining professionalism.",
        "When providing code examples, use proper syntax highlighting.",
        "If the user asks about complex topics, break them down into digestible parts.",
    ]
    
    agent = Agent(
        name="Agno Assistant (Basic Mode)",
        model=model,
        instructions=enhanced_instructions,
        markdown=True,
        add_datetime_to_context=True,
    )
    
    return agent

def create_tools_agent() -> Agent:
    """Create an agent with comprehensive tool capabilities."""
    model = get_configured_model()
    
    tools_instructions = [
        "You are Agno Assistant with comprehensive tool capabilities.",
        "You have access to web search, file operations, system information, and calculations.",
        "Use tools when they can help provide better, more accurate information.",
        "Always explain what tools you're using and why.",
        "Prioritize user safety and security in all operations.",
        "Provide step-by-step explanations when using multiple tools.",
        "Format tool outputs clearly and explain their significance.",
    ]
    
    # Create agent with tools
    agent = Agent(
        name="Agno Assistant (Tools Mode)",
        model=model,
        instructions=tools_instructions,
        tools=[
            # Web search tools
            DuckDuckGoTools(),
            # File and system tools
            list_directory,
            read_file,
            get_file_info,
            get_system_info,
            run_safe_command,
            calculate_math,
            get_current_time,
        ],
        markdown=True,
        add_datetime_to_context=True,
    )
    
    return agent

def create_reasoning_agent() -> Agent:
    """Create an agent with advanced reasoning capabilities."""
    model = get_reasoning_model()
    
    reasoning_instructions = [
        "You are Agno Assistant with advanced reasoning capabilities.",
        "When analyzing problems, break them down systematically:",
        "1. Identify the key components and relationships",
        "2. State your assumptions clearly",
        "3. Consider multiple perspectives and alternatives",
        "4. Evaluate evidence and reasoning quality",
        "5. Handle uncertainty appropriately",
        "6. Present conclusions with supporting logic",
        "Show your reasoning process step-by-step.",
        "Distinguish between facts, assumptions, and opinions.",
        "Consider potential counterarguments and limitations.",
        "Use structured thinking patterns for complex problems.",
    ]
    
    agent = Agent(
        name="Agno Assistant (Reasoning Mode)",
        model=model,
        instructions=reasoning_instructions,
        tools=[
            ReasoningTools(),
            DuckDuckGoTools(),  # For research support
        ],
        markdown=True,
        add_datetime_to_context=True,
    )
    
    return agent

def create_memory_agent() -> Agent:
    """Create an agent with persistent memory capabilities."""
    model = get_configured_model()
    
    # Set up database
    db_path = Path("data/agent_memory.db")
    db_path.parent.mkdir(exist_ok=True)
    
    memory_db = SqliteDb(
        db_file=str(db_path)
    )
    
    memory_instructions = [
        "You are Agno Assistant with persistent memory across conversations.",
        "Remember important details about users and conversations.",
        "Store relevant information that might be useful in future interactions.",
        "Refer to previous conversations when relevant to current questions.",
        "Build context and understanding over time.",
        "Ask follow-up questions based on stored information.",
        "Maintain conversation continuity across sessions.",
        "Respect user privacy - only store appropriate information.",
    ]
    
    agent = Agent(
        name="Agno Assistant (Memory Mode)",
        model=model,
        instructions=memory_instructions,
        db=memory_db,
        add_datetime_to_context=True,
        markdown=True,
    )
    
    return agent

def create_comprehensive_agent() -> Agent:
    """Create an agent with all capabilities combined."""
    model = get_reasoning_model()  # Use reasoning model for best performance
    
    # Set up database for memory
    db_path = Path("data/comprehensive_agent_memory.db")
    db_path.parent.mkdir(exist_ok=True)
    
    memory_db = SqliteDb(
        db_file=str(db_path)
    )
    
    comprehensive_instructions = [
        "You are Agno Assistant with comprehensive AI capabilities.",
        "You have access to persistent memory, advanced reasoning, and powerful tools.",
        "",
        "MEMORY: Remember important user information across sessions.",
        "REASONING: Use structured, step-by-step analysis for complex problems.",
        "TOOLS: Leverage web search, file operations, and system tools when helpful.",
        "",
        "Approach each interaction with:",
        "- Context awareness from memory",
        "- Logical, systematic thinking",
        "- Appropriate tool usage",
        "- Clear, helpful communication",
        "",
        "Always explain your reasoning and tool choices.",
        "Build understanding over time through memory.",
        "Prioritize accuracy, safety, and user value.",
    ]
    
    agent = Agent(
        name="Agno Assistant (Comprehensive Mode)",
        model=model,
        instructions=comprehensive_instructions,
        tools=[
            # Reasoning tools
            ReasoningTools(),
            # Web search tools
            DuckDuckGoTools(),
            # File and system tools
            list_directory,
            read_file,
            get_file_info,
            get_system_info,
            run_safe_command,
            calculate_math,
            get_current_time,
        ],
        db=memory_db,
        markdown=True,
        add_datetime_to_context=True,
    )
    
    return agent

# ============================================================================
# USER INTERFACE AND UTILITIES
# ============================================================================

def display_welcome_banner():
    """Display an enhanced welcome banner."""
    try:
        print("🤖 Agno Agent Demo - Comprehensive Edition")
    except UnicodeEncodeError:
        print("Agno Agent Demo - Comprehensive Edition")
    print("=" * 60)
    print("Welcome to the comprehensive Agno Agent Demo!")
    print("Choose from multiple agent modes with different capabilities:")
    try:
        print("  • Basic: Simple conversational AI")
        print("  • Tools: Web search, file ops, system info")  
        print("  • Reasoning: Advanced step-by-step analysis")
        print("  • Memory: Persistent conversation history")
        print("  • Comprehensive: All capabilities combined")
    except UnicodeEncodeError:
        print("  - Basic: Simple conversational AI")
        print("  - Tools: Web search, file ops, system info")
        print("  - Reasoning: Advanced step-by-step analysis")
        print("  - Memory: Persistent conversation history")
        print("  - Comprehensive: All capabilities combined")
    print("=" * 60)

def display_agent_selection() -> str:
    """Display agent selection menu and get user choice."""
    print("\n🎯 Agent Selection:")
    print("=" * 40)
    print("1. Basic Agent - Simple conversational AI")
    print("2. Tools Agent - Web search & file operations")
    print("3. Reasoning Agent - Advanced analysis & logic")
    print("4. Memory Agent - Persistent conversation memory")
    print("5. Comprehensive Agent - All capabilities")
    print("=" * 40)
    
    while True:
        try:
            choice = input("\nSelect agent type (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            else:
                print("❌ Please enter a number between 1 and 5")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            sys.exit(0)

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
        print("• Type 'switch' to change agent mode")
        print("• Type 'stats' for performance statistics")
        print("• Type 'help' for available commands")
        print("• Press Ctrl+C at any time for graceful shutdown")
    except UnicodeEncodeError:
        print("- Type your message and press Enter")
        print("- Type 'quit', 'exit', 'bye', or 'q' to exit")
        print("- Type 'switch' to change agent mode")
        print("- Type 'stats' for performance statistics")
        print("- Type 'help' for available commands")
        print("- Press Ctrl+C at any time for graceful shutdown")
    print("=" * 40)

def setup_signal_handlers():
    """Set up signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        print("\n\n👋 Received shutdown signal. Goodbye!")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def validate_user_input(user_input: str) -> str:
    """Validate and sanitize user input."""
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")
    
    cleaned_input = user_input.strip()
    
    if len(cleaned_input) > 10000:
        raise ValueError("Input is too long (maximum 10,000 characters)")
    
    # Basic security check
    suspicious_patterns = ['<script', 'javascript:', 'eval(', 'exec(']
    if any(pattern.lower() in cleaned_input.lower() for pattern in suspicious_patterns):
        raise ValueError("Input contains potentially unsafe content")
    
    return cleaned_input

def get_agent_by_choice(choice: str) -> Agent:
    """Get agent instance based on user choice."""
    agent_map = {
        '1': create_basic_agent,
        '2': create_tools_agent, 
        '3': create_reasoning_agent,
        '4': create_memory_agent,
        '5': create_comprehensive_agent,
    }
    
    agent_names = {
        '1': "Basic Agent",
        '2': "Tools Agent",
        '3': "Reasoning Agent", 
        '4': "Memory Agent",
        '5': "Comprehensive Agent",
    }
    
    print(f"\n🚀 Creating {agent_names[choice]}...")
    agent = agent_map[choice]()
    print(f"✅ {agent_names[choice]} created successfully!")
    return agent

# ============================================================================
# MAIN APPLICATION LOGIC
# ============================================================================

def main():
    """Main function to run the comprehensive agent demo."""
    # Set up signal handlers for graceful shutdown
    setup_signal_handlers()
    
    # Display welcome banner
    display_welcome_banner()
    
    # Show system health
    print("💻 System Status: Ready")
    
    # Show model configuration
    print_model_info()
    
    # Test model connection
    print("🔍 Testing model connection...")
    with performance_monitor.monitor_operation("model_connection_test"):
        if not test_model_connection():
            print("❌ Cannot continue without a working model connection.")
            return
    
    # Agent selection and creation
    current_agent = None
    
    while True:
        try:
            # Get agent selection if needed
            if current_agent is None:
                choice = display_agent_selection()
                current_agent = get_agent_by_choice(choice)
                display_chat_instructions()
            
            # Main chat loop
            while True:
                try:
                    # Get user input
                    user_input = input("\n👤 You: ").strip()
                    
                    # Check for exit commands
                    if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                        print("👋 Goodbye!")
                        return
                    
                    # Check for agent switching
                    if user_input.lower() in ['switch', 'change']:
                        current_agent = None
                        print("\n🔄 Switching agent mode...")
                        break
                    
                    # Check for special commands
                    if user_input.lower() in ['stats', 'performance', 'perf']:
                        stats = performance_monitor.get_summary_stats()
                        print(f"📊 Performance Stats:")
                        print(f"   Operations: {stats['total_operations']}")
                        print(f"   Success Rate: {stats['success_rate']:.1f}%")
                        print(f"   Avg Response Time: {stats['avg_response_time']:.2f}s")
                        continue
                    elif user_input.lower() in ['help', 'commands']:
                        print("\n🔧 Available Commands:")
                        print("• stats/performance/perf - Show performance statistics")
                        print("• switch/change - Switch agent mode")
                        print("• help/commands - Show this help message")
                        print("• quit/exit/bye/q - Exit the application")
                        continue
                    elif user_input.lower() in ['health', 'system']:
                        print("💻 System Status: Operational")
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
                    
                    try:
                        with performance_monitor.monitor_operation("agent_response"):
                            if current_agent:
                                current_agent.print_response(validated_input)
                            else:
                                print("❌ Agent not initialized. Please select an agent mode first.")
                            
                        # Log successful interaction
                        processing_time = time.time() - start_time
                        logger.info(f"User interaction completed - Input length: {len(validated_input)}, Processing time: {processing_time}s")
                        
                    except Exception as e:
                        error_message = f"Agent error: {e}"
                        logger.error(f"Agent error during processing: {e}")
                        print(f"❌ {error_message}")
                        
                        if "network" in str(e).lower() or "timeout" in str(e).lower():
                            print("🔄 This appears to be a network error - please try again in a moment.")
                        else:
                            print("\n💡 Suggestions:")
                            print("   • Check your internet connection")
                            print("   • Verify your API keys are correctly set")
                            print("   • Try a simpler question if the error persists")
                
                except KeyboardInterrupt:
                    print("\n\n👋 Goodbye!")
                    return
                except EOFError:
                    print("\n\n👋 Goodbye!")
                    return
                except Exception as e:
                    error_message = f"Processing error: {e}"
                    logger.error(f"Processing error: {e}")
                    print(f"\n❌ {error_message}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            return
        except Exception as e:
            error_message = f"Unexpected error: {e}"
            logger.error(f"Unexpected error: {e}")
            print(f"\n❌ {error_message}")
            
            print("\n💡 Try these steps:")
            print("   1. Check your internet connection")
            print("   2. Verify your API keys are correctly set")
            print("   3. Try restarting the application")
            
            # Ask if user wants to continue
            try:
                continue_choice = input("\n❓ Do you want to continue? (y/n): ").strip().lower()
                if continue_choice not in ['y', 'yes']:
                    print("👋 Goodbye!")
                    return
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Goodbye!")
                return
    
    # Show final performance report
    print("\n📊 Final Performance Summary:")
    stats = performance_monitor.get_summary_stats()
    print(f"   Total Operations: {stats['total_operations']}")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")
    if stats['avg_response_time'] > 0:
        print(f"   Avg Response Time: {stats['avg_response_time']:.2f}s")
    
    print("\n👋 Thank you for using Agno Agent Demo!")

if __name__ == "__main__":
    main()