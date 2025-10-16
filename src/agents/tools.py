#!/usr/bin/env python3
"""
Advanced Tool Agent

A comprehensive demonstration of building agents with various tools and capabilities.
This agent includes web search, file operations, system information, calculations,
and other useful tools for productivity and research.

Features:
- Web search capabilities
- File system operations
- System monitoring and information
- Mathematical calculations
- Date/time utilities
- Weather information (if configured)
- Code execution and analysis
- Data processing tools

Usage:
    python tools_agent.py
    
or

    python -m src.agents.tools
"""

import os
import sys
import signal
import json
import subprocess
import platform
import psutil
import math
import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from src.models.config import get_configured_model, print_model_info, test_model_connection
from src.lib.error_handling import (
    handle_error, AgentError, ConfigurationError, ValidationError,
    is_recoverable_error, log_error_for_debugging
)
from src.services.performance_monitor import PerformanceMonitor
from src.lib.logging_config import setup_logging, get_logger

# Initialize logging
setup_logging()
logger = get_logger(__name__)

# Custom tool functions using the @tool decorator
from agno.tools import tool

@tool
def list_directory(path: str = ".") -> str:
    """List contents of a directory."""
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
        
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            truncated_msg = f"\n\n[File truncated - showing first {max_lines} lines of {len(lines)}]"
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
def run_command(command: str, timeout: int = 30) -> str:
    """Run a safe system command."""
    # Security: Only allow specific safe commands
    safe_commands = [
        'ls', 'dir', 'pwd', 'date', 'time', 'whoami', 'hostname',
        'python --version', 'pip --version', 'git --version',
        'echo', 'cat', 'head', 'tail', 'wc', 'grep'
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
        output += f"Exit code: {result.returncode}\n\n"
        
        if result.stdout:
            output += f"Output:\n{result.stdout}\n"
        
        if result.stderr:
            output += f"Errors:\n{result.stderr}\n"
        
        if result.returncode != 0:
            output += f"\nCommand failed with exit code {result.returncode}"
        
        return output
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error running command: {str(e)}"

@tool
def calculate(expression: str) -> str:
    """Safely evaluate mathematical expressions."""
    # Security: Only allow mathematical operations
    allowed_names = {
        "__builtins__": {},
        "abs": abs, "round": round, "min": min, "max": max,
        "sum": sum, "pow": pow, "divmod": divmod,
        "math": math, "pi": math.pi, "e": math.e,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
        "exp": math.exp, "ceil": math.ceil, "floor": math.floor
    }
    
    try:
        # Remove potentially dangerous characters
        if any(char in expression for char in ['import', 'exec', 'eval', '__']):
            return "Error: Expression contains potentially dangerous operations"
        
        result = eval(expression, allowed_names, {})
        return f"Expression: {expression}\nResult: {result}\nType: {type(result).__name__}"
    except ZeroDivisionError:
        return f"Error: Division by zero in expression: {expression}"
    except ValueError as e:
        return f"Math error in '{expression}': {str(e)}"
    except SyntaxError:
        return f"Invalid mathematical expression: {expression}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

@tool
def get_current_datetime(timezone: Optional[str] = None) -> str:
    """Get current date and time information."""
    now = datetime.datetime.now()
    
    result = "Current Date and Time:\n"
    result += "=" * 30 + "\n\n"
    result += f"Current time: {now.isoformat()}\n"
    result += f"Formatted date: {now.strftime('%Y-%m-%d')}\n"
    result += f"Formatted time: {now.strftime('%H:%M:%S')}\n"
    result += f"Readable format: {now.strftime('%A, %B %d, %Y at %I:%M %p')}\n\n"
    
    result += "Components:\n"
    result += f"  Year: {now.year}\n"
    result += f"  Month: {now.month}\n"
    result += f"  Day: {now.day}\n"
    result += f"  Hour: {now.hour}\n"
    result += f"  Minute: {now.minute}\n"
    result += f"  Second: {now.second}\n"
    result += f"  Weekday: {now.strftime('%A')}\n"
    result += f"  Day of year: {now.timetuple().tm_yday}\n\n"
    
    result += f"Unix timestamp: {int(now.timestamp())}"
    
    return result

@tool
def parse_datetime(date_string: str, format_string: Optional[str] = None) -> str:
    """Parse a date string into datetime components."""
    try:
        if format_string:
            dt = datetime.datetime.strptime(date_string, format_string)
        else:
            # Try common formats
            formats = [
                "%Y-%m-%d",
                "%Y-%m-%d %H:%M:%S",
                "%m/%d/%Y",
                "%d/%m/%Y",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M"
            ]
            
            dt = None
            for fmt in formats:
                try:
                    dt = datetime.datetime.strptime(date_string, fmt)
                    break
                except ValueError:
                    continue
            
            if dt is None:
                return f"Error: Unable to parse date string: {date_string}"
        
        result = f"Parsed Date: {date_string}\n"
        result += "=" * 30 + "\n\n"
        result += f"Parsed as: {dt.isoformat()}\n"
        result += f"Readable: {dt.strftime('%A, %B %d, %Y at %I:%M %p')}\n\n"
        
        result += "Components:\n"
        result += f"  Year: {dt.year}\n"
        result += f"  Month: {dt.month}\n"
        result += f"  Day: {dt.day}\n"
        result += f"  Hour: {dt.hour}\n"
        result += f"  Minute: {dt.minute}\n"
        result += f"  Second: {dt.second}\n"
        result += f"  Weekday: {dt.strftime('%A')}"
        
        return result
    except ValueError as e:
        return f"Date parsing error: {str(e)}"

def create_tools_agent() -> Agent:
    """Create an agent equipped with comprehensive tools."""
    try:
        model = get_configured_model()
        
        # Create the agent with all tools
        agent = Agent(
            name="Advanced Tool Assistant",
            model=model,
            tools=[
                DuckDuckGoTools(),  # Web search capabilities
                list_directory,
                read_file,
                get_file_info,
                get_system_info,
                run_command,
                calculate,
                get_current_datetime,
                parse_datetime,
            ],
            instructions=[
                "You are an Advanced Tool Assistant with access to various productivity tools.",
                "You can help with:",
                "- Web searches and research",
                "- File system operations (reading files, listing directories)",
                "- System information and monitoring",
                "- Mathematical calculations",
                "- Date and time operations",
                "- Safe system command execution",
                "",
                "Always explain what you're doing before using tools.",
                "Be helpful, accurate, and secure in your responses.",
                "If you encounter errors, explain them clearly and suggest alternatives.",
                "Respect user privacy and system security at all times."
            ],
            markdown=True,
            add_datetime_to_context=True,
        )
        
        return agent
        
    except Exception as e:
        logger.error(f"Error creating tools agent: {str(e)}")
        raise ConfigurationError(f"Failed to create tools agent: {str(e)}")

def display_tools_banner():
    """Display welcome banner for the tools agent."""
    try:
        print("🛠️ Advanced Tool Agent")
    except UnicodeEncodeError:
        print("Advanced Tool Agent")
    print("=" * 60)
    print("Welcome to the Advanced Tool Agent!")
    print("This agent has access to various productivity tools:")
    try:
        print("  🔍 Web search and research")
        print("  📁 File system operations")
        print("  💻 System information and monitoring")
        print("  🧮 Mathematical calculations")
        print("  📅 Date and time utilities")
        print("  ⚡ Safe system command execution")
    except UnicodeEncodeError:
        print("  - Web search and research")
        print("  - File system operations")
        print("  - System information and monitoring")
        print("  - Mathematical calculations")
        print("  - Date and time utilities")
        print("  - Safe system command execution")
    print("=" * 60)

def display_usage_examples():
    """Display usage examples for the tools agent."""
    print("\n💡 Example Queries:")
    print("=" * 40)
    print("• 'Search for the latest Python news'")
    print("• 'List files in the current directory'")
    print("• 'Show system information'")
    print("• 'Calculate the square root of 144'")
    print("• 'What's the current date and time?'")
    print("• 'Read the README.md file'")
    print("• 'Run the command: python --version'")
    print("=" * 40)

def setup_signal_handlers():
    """Set up signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        print("\n\n👋 Shutting down Tool Agent. Goodbye!")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def validate_user_input(user_input: str) -> bool:
    """Validate user input for security and safety."""
    if not user_input or not user_input.strip():
        return False
    
    if len(user_input) > 10000:  # Reasonable length limit
        return False
    
    # Basic security checks - could be expanded
    dangerous_patterns = ['__import__', 'exec(', 'eval(', 'subprocess.', 'os.system']
    if any(pattern in user_input.lower() for pattern in dangerous_patterns):
        return False
    
    return True

def main():
    """Main function to run the advanced tool agent."""
    # Setup
    setup_signal_handlers()
    performance_monitor = PerformanceMonitor()
    
    try:
        # Validate environment and create agent
        print("🔧 Initializing Advanced Tool Agent...")
        
        # Test model connection
        print("📡 Testing model connection...")
        connection_result = test_model_connection()
        if not connection_result:
            raise ConfigurationError("Model connection failed. Please check your configuration.")
        
        print("✅ Model connection successful!")
        
        # Create and configure agent
        print("🤖 Creating agent with tools...")
        agent = create_tools_agent()
        print("✅ Agent created successfully!")
        
        # Display information
        display_tools_banner()
        print_model_info()
        display_usage_examples()
        
        print("\n💬 Start chatting with the Tool Agent!")
        print("Type 'quit', 'exit', 'bye', or 'q' to exit")
        print("Type 'help' for more examples")
        print("-" * 60)
        
        # Main chat loop
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    display_usage_examples()
                    continue
                elif user_input.lower() in ['stats', 'performance', 'perf']:
                    print("\n📊 Performance Statistics:")
                    performance_monitor.print_performance_report()
                    continue
                
                # Validate input
                if not validate_user_input(user_input):
                    print("❌ Invalid input. Please try again with a different query.")
                    continue
                
                # Process with agent
                print("\n🤖 Assistant: ", end="", flush=True)
                
                # Use the agent's print_response method for better formatting
                try:
                    agent.print_response(user_input, stream=True)
                    print()  # New line after response
                    
                    # Log interaction
                    logger.info("User query processed successfully")
                except Exception as e:
                    print(f"\n❌ Error processing query: {str(e)}")
                    log_error_for_debugging(e)
                
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                error_message = handle_error(e)
                print(f"\n❌ {error_message}")
                
                if is_recoverable_error(e):
                    print("🔄 You can try again with a different query.")
                else:
                    print("⚠️ This error may require restarting the agent.")
    
    except ConfigurationError as e:
        error_message = handle_error(e)
        print(f"\n❌ Configuration Error: {error_message}")
        print("\n🔧 Please check your environment setup and try again.")
        sys.exit(1)
    except Exception as e:
        error_message = handle_error(e)
        print(f"\n❌ Unexpected Error: {error_message}")
        log_error_for_debugging(e)
        sys.exit(1)
    
    # Final performance report
    print("\n📊 Final Performance Summary:")
    performance_monitor.print_performance_report()
    
    print("\n👋 Thank you for using the Advanced Tool Agent!")

if __name__ == "__main__":
    main()
