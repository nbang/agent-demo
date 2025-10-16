# Advanced Tool Agent Documentation

## Overview

The Advanced Tool Agent is a comprehensive demonstration of building AI agents with various productivity tools and capabilities using the Agno framework. This agent extends beyond simple chat by providing access to file systems, system information, mathematical calculations, web search, and safe command execution.

## Features

### 🔍 **Web Search & Research**
- DuckDuckGo web search integration
- Real-time information retrieval
- Source citation and accuracy

### 📁 **File System Operations**
- Directory listing and navigation
- File reading with encoding safety
- File information and metadata
- Secure file access with permission checks

### 💻 **System Information & Monitoring**
- Comprehensive system information
- CPU, memory, and disk usage
- Network interface details
- Platform and hardware information

### 🧮 **Mathematical Calculations**
- Safe expression evaluation
- Advanced mathematical functions
- Support for trigonometry, logarithms, and more
- Protection against code injection

### 📅 **Date & Time Utilities**
- Current date and time information
- Date parsing and formatting
- Multiple timezone support
- Timestamp conversions

### ⚡ **Safe Command Execution**
- Whitelisted system commands
- Secure execution environment
- Output capture and error handling
- Timeout protection

## Quick Start

### Running the Agent

```bash
# Method 1: Direct execution
python tools_agent.py

# Method 2: Module execution
python -m src.agents.tools

# Method 3: From Python script
from src.agents.tools import main
main()
```

### Example Interactions

```
👤 You: Search for the latest Python news

🤖 Assistant: I'll search for the latest Python news for you.
[Agent uses DuckDuckGo search tool and provides results]

👤 You: List files in the current directory

🤖 Assistant: I'll list the contents of the current directory.
[Agent uses list_directory tool and shows file listings]

👤 You: What's the system information?

🤖 Assistant: Let me get the current system information.
[Agent uses get_system_info tool and displays system details]

👤 You: Calculate the square root of 144

🤖 Assistant: I'll calculate that for you.
[Agent uses calculate tool: sqrt(144) = 12.0]
```

## Available Tools

### File System Tools

#### `list_directory(path: str = ".")`
Lists the contents of a directory with detailed information.

**Parameters:**
- `path` (optional): Directory path to list (default: current directory)

**Example:**
```
👤 You: List files in the src directory
```

#### `read_file(file_path: str, max_lines: int = 100)`
Reads the contents of a text file safely.

**Parameters:**
- `file_path`: Path to the file to read
- `max_lines` (optional): Maximum lines to read (default: 100)

**Example:**
```
👤 You: Read the README.md file
```

#### `get_file_info(file_path: str)`
Gets detailed information about a file or directory.

**Parameters:**
- `file_path`: Path to the file or directory

**Example:**
```
👤 You: Get information about agent.py
```

### System Tools

#### `get_system_info()`
Provides comprehensive system information including CPU, memory, disk, and network details.

**Example:**
```
👤 You: Show me system information
👤 You: What's the current memory usage?
```

#### `run_command(command: str, timeout: int = 30)`
Executes safe system commands with security restrictions.

**Parameters:**
- `command`: System command to run (restricted to safe commands)
- `timeout` (optional): Timeout in seconds (default: 30)

**Safe Commands:**
- `ls`, `dir`, `pwd`, `date`, `time`, `whoami`, `hostname`
- `python --version`, `pip --version`, `git --version`
- `echo`, `cat`, `head`, `tail`, `wc`, `grep`

**Example:**
```
👤 You: Run the command: python --version
👤 You: What's the current date?
```

### Mathematical Tools

#### `calculate(expression: str)`
Safely evaluates mathematical expressions with protection against code injection.

**Parameters:**
- `expression`: Mathematical expression to evaluate

**Supported Functions:**
- Basic arithmetic: `+`, `-`, `*`, `/`, `**`, `%`
- Math functions: `sin`, `cos`, `tan`, `sqrt`, `log`, `log10`, `exp`
- Constants: `pi`, `e`
- Built-ins: `abs`, `round`, `min`, `max`, `sum`, `pow`

**Examples:**
```
👤 You: Calculate 2 + 2 * 3
👤 You: What's the square root of 144?
👤 You: Calculate sin(pi/2)
👤 You: Find the area of a circle with radius 5
```

### Date & Time Tools

#### `get_current_datetime(timezone: str = None)`
Gets current date and time information with multiple formats.

**Parameters:**
- `timezone` (optional): Timezone specification

**Example:**
```
👤 You: What's the current date and time?
👤 You: Show me today's date
```

#### `parse_datetime(date_string: str, format_string: str = None)`
Parses date strings into structured datetime information.

**Parameters:**
- `date_string`: Date string to parse
- `format_string` (optional): Expected format (auto-detects if not provided)

**Supported Formats:**
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:MM:SS`
- `MM/DD/YYYY`
- `DD/MM/YYYY`
- ISO format: `YYYY-MM-DDTHH:MM:SS`

**Examples:**
```
👤 You: Parse the date "2023-12-25"
👤 You: What day of the week was January 1, 2023?
```

### Web Search Tools

#### DuckDuckGo Search
Integrated web search capabilities for real-time information retrieval.

**Examples:**
```
👤 You: Search for recent developments in AI
👤 You: Find information about Python 3.12 features
👤 You: What's the weather in San Francisco?
```

## Security Features

### File System Security
- Path validation and sanitization
- Permission checking before file operations
- Protection against directory traversal attacks
- Encoding safety for text files

### Command Execution Security
- Whitelist-based command filtering
- No arbitrary code execution
- Timeout protection
- Output sanitization

### Mathematical Expression Security
- Sandboxed evaluation environment
- No access to dangerous built-ins
- Protection against code injection
- Only mathematical operations allowed

### Input Validation
- Length limits on user input
- Pattern detection for dangerous content
- Error handling and recovery
- Comprehensive logging

## Error Handling

The tool agent includes comprehensive error handling:

- **File System Errors**: Permission denied, file not found, encoding issues
- **System Errors**: Command failures, timeout errors, resource limitations
- **Mathematical Errors**: Division by zero, invalid expressions, domain errors
- **Network Errors**: Search failures, connection issues, rate limiting

All errors are handled gracefully with user-friendly messages and recovery suggestions.

## Performance Monitoring

The agent includes built-in performance monitoring:

- Response time tracking
- Memory usage monitoring
- System resource utilization
- Operation success rates
- Performance alerts and optimization suggestions

Use the `stats` or `performance` command during chat to view current metrics.

## Usage Tips

### Best Practices
1. **Be Specific**: Provide clear, specific requests for better results
2. **Use Examples**: When asking for calculations, provide the exact expression
3. **Check Paths**: Verify file paths exist before requesting file operations
4. **Start Simple**: Begin with basic operations before complex workflows

### Common Workflows

#### **File Analysis Workflow**
1. List directory contents: `"List files in the project directory"`
2. Get file information: `"Get details about setup.py"`
3. Read file contents: `"Read the first 50 lines of main.py"`

#### **System Monitoring Workflow**
1. Check system info: `"Show system information"`
2. Monitor resources: `"What's the current CPU and memory usage?"`
3. Run diagnostics: `"Run the command: python --version"`

#### **Research Workflow**
1. Search for information: `"Search for Python best practices 2024"`
2. Get current data: `"What's today's date?"`
3. Calculate metrics: `"Calculate the percentage: 75/100 * 100"`

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Make sure you're in the project directory
cd /path/to/agent-demo

# Check Python path
python -c "import sys; print(sys.path)"
```

**Permission Errors**
- Ensure read permissions for files you want to access
- Run with appropriate user permissions
- Check file ownership and permissions

**Tool Not Found**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that the Agno framework is properly installed
- Ensure environment variables are set correctly

**Performance Issues**
- Monitor system resources with the `stats` command
- Reduce file reading limits with `max_lines` parameter
- Use more specific search queries to reduce processing time

### Getting Help

During a chat session, you can:
- Type `help` for usage examples
- Type `stats` for performance information
- Type `quit` or `exit` to end the session

The agent provides helpful error messages and suggestions when issues occur.

## Architecture

### Directory Structure
```
src/agents/tools.py          # Main tool agent implementation
tools_agent.py               # Entry point script
src/lib/error_handling.py    # Error handling utilities
src/services/performance_monitor.py  # Performance monitoring
src/models/config.py         # Model configuration
```

### Tool Implementation
- Each tool is implemented as a decorated function using `@tool`
- Tools are automatically registered with the agent
- Comprehensive error handling and logging
- Security-first design with input validation

### Agent Configuration
- Multi-model support (OpenAI, Azure OpenAI)
- Streaming response capability
- Context-aware processing
- Markdown formatting support

This tool agent represents a production-ready example of building sophisticated AI agents with practical capabilities while maintaining security and reliability.

## Next Steps

To extend the tool agent:

1. **Add New Tools**: Implement additional `@tool` decorated functions
2. **Enhance Security**: Add more sophisticated input validation
3. **Expand APIs**: Integrate with additional external services
4. **Improve Performance**: Add caching and optimization features
5. **Add Persistence**: Implement session memory and data storage

The modular architecture makes it easy to add new capabilities while maintaining the existing functionality.