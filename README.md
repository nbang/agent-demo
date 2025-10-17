# Agno Agent Demo

A comprehensive demonstration of building AI agents using the Agno framework. This project showcases various agent capabilities including basic conversational agents, memory-enabled agents, reasoning agents with structured thinking, tool-equipped agents, and multi-agent systems for collaborative problem-solving.

## 🎯 Key Features

### 🤖 Unified Agent Interface
The `single_agent_demo.py` provides five different agent modes in one application:
- **Basic Agent**: Simple conversational AI with streaming responses
- **Tools Agent**: Web search, file operations, calculations, and system utilities
- **Reasoning Agent**: Structured problem-solving with step-by-step analysis
- **Memory Agent**: Maintains conversation history and context across sessions
- **Comprehensive Agent**: All capabilities combined in one powerful agent

### 🛠️ Core Capabilities
- **Multi-Model Support**: Works with OpenAI and Azure OpenAI
- **Error Handling**: Comprehensive error recovery and user-friendly messages
- **Performance Monitoring**: Built-in metrics and system health tracking
- **Security**: Input validation and credential protection
- **Logging**: Structured logging with rotation and filtering
- **Testing**: Full test suite with unit and integration tests

### 🌟 Advanced Features
- **Streaming Responses**: Real-time token-by-token output
- **Conversation Memory**: SQLite-based persistent storage
- **Structured Reasoning**: Multi-step problem analysis with evidence
- **Tool Integration**: DuckDuckGo search, file system, calculations
- **Team Collaboration**: Multi-agent workflows with role specialization
- **Interactive Commands**: Runtime stats, health checks, and diagnostics

## 📋 Prerequisites

- **Python 3.11+** (recommended 3.12)
- **Memory**: 500MB+ available RAM
- **API Access**: OpenAI API key or Azure OpenAI credentials
- **Disk Space**: 100MB for installation and logs

## 🛠️ Installation & Setup

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd agent-demo

# Install dependencies
pip install -r requirements.txt
```

### 2. API Configuration
```bash
# Copy the example environment file
cp env.example .env
```

**Configure for OpenAI:**
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
DEFAULT_MODEL=gpt-4o-mini
LOG_LEVEL=INFO
LOG_TO_FILE=true
```

**Configure for Azure OpenAI:**
```env
AZURE_OPENAI_API_KEY=your-azure-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview
DEFAULT_MODEL=gpt-4o-mini
LOG_LEVEL=INFO
LOG_TO_FILE=true
```

### Quick Start

```bash
# Run the unified agent demo
python single_agent_demo.py

# Or run multi-agent examples
python multi_agent_demo.py

# Or explore examples directory
python examples/agent_with_memory.py
python examples/agent_with_tools.py
python examples/reasoning_agent.py
```

## 🤖 Agent Modes

The `single_agent_demo.py` provides an interactive menu to choose from five different agent modes:

### 1. **Basic Agent Mode**
A simple conversational agent with streaming responses and comprehensive error handling.

**Features:**
- Multi-model support (OpenAI & Azure OpenAI)
- Advanced error handling and recovery
- Performance monitoring and optimization
- Secure input validation
- Graceful shutdown handling
- Structured logging

### 2. **Tools Agent Mode**
Access to web search, file operations, system information, and calculations.

**Features:**
- 🔍 Web search and research (DuckDuckGo)
- 📁 File system operations (read, list, info)
- 💻 System information and monitoring
- 🧮 Mathematical calculations and expressions
- 📅 Date and time utilities
- ⚡ Safe system command execution

### 3. **Reasoning Agent Mode**
Structured problem-solving with step-by-step analysis and logical reasoning.

**Features:**
- 🔍 Complex problem decomposition and analysis
- 🧠 Multi-perspective consideration and evaluation
- 📊 Evidence-based reasoning with uncertainty handling
- 🔄 Real-time intermediate step streaming
- 📝 Comprehensive problem-solving patterns

### 4. **Memory Agent Mode**
Maintains conversation history and context across sessions using SQLite storage.

**Features:**
- 💬 Persistent conversation memory
- 🔍 Context-aware responses
- 📊 Conversation history tracking
- 🗄️ SQLite database storage
- 🔄 Session management

### 5. **Comprehensive Agent Mode**
All capabilities combined in one powerful agent with memory, tools, and reasoning.

## 🚀 Using the Single Agent Demo

Run the unified agent demo:

```bash
python single_agent_demo.py
```

**Interactive Features:**
- **Agent Selection Menu**: Choose from 5 different agent modes
- **Mode Switching**: Type `switch` to change agent types during conversation
- **Performance Stats**: Type `stats` to view response times and metrics
- **Comprehensive Help**: Type `help` for available commands

**Example Interactions:**
- "Search for the latest Python news" (Tools Mode)
- "Remember that I like Python programming" (Memory Mode)
- "Analyze the pros and cons of remote work" (Reasoning Mode)
- "List files and remember my project structure" (Comprehensive Mode)

### 🧠 **Advanced Reasoning Agent** (Mode 3 in `single_agent_demo.py`)
A sophisticated agent that performs structured, step-by-step problem analysis with comprehensive reasoning capabilities.

**Features:**
- 🔍 Complex problem decomposition and analysis
- 📊 Multi-perspective consideration and evaluation
- ⚖️ Evidence-based reasoning and assessment
- 🎯 Assumption identification and testing
- ⚠️ Uncertainty analysis and risk management
- 💡 Structured solution development
- 📈 Strategic decision analysis
- 🌐 Web research for evidence gathering
- 🧠 Real-time reasoning step streaming

**Usage:**
```bash
python single_agent_demo.py
# Then select option 3: Reasoning Agent Mode
```

**Alternative standalone example:**
```bash
python examples/reasoning_agent.py
```

**Example Complex Problems:**
- "Should a company implement a 4-day work week? Analyze comprehensively."
- "How would you solve traffic congestion in a major metropolitan area?"
- "What are the ethical implications of AI in healthcare decision-making?"
- "Compare electric cars vs. public transportation for environmental impact."
- "Analyze the pros and cons of universal basic income."

For detailed documentation, see [`docs/REASONING_AGENT_GUIDE.md`](docs/REASONING_AGENT_GUIDE.md).

### 👥 **Multi-Agent Systems** (`multi_agent_demo.py`)
Collaborative agent teams that work together to solve complex problems.

**Available Teams:**
- **Research Team**: Collaborative research with multiple perspectives
- **Problem-Solving Team**: Analyze, strategize, and plan implementation
- **Content Creation Team**: Generate coordinated content across formats

**Features:**
- 🤝 Agent collaboration and coordination
- 🔄 Workflow orchestration
- 📊 Team performance metrics
- 🎯 Role specialization
- 💬 Inter-agent communication

**Usage:**
```bash
python multi_agent_demo.py
```

**Example Team Tasks:**
- "Research team: Investigate the impact of AI on education"
- "Problem-solving team: How can we reduce customer churn?"
- "Content team: Create a blog post about sustainable technology"

See [`examples/multi_agents/README.md`](examples/multi_agents/README.md) for more details.

## 💬 Interactive Usage

### Chat Commands
During conversation, use these commands:
- `stats`, `performance`, `perf` - Show performance statistics
- `health`, `system` - Display system health information
- `help`, `commands` - Show available commands
- `quit`, `exit`, `bye`, `q` - Exit gracefully

### Example Session
```
🤖 Agno Agent Demo
============================================================
Welcome to the Agno Agent Demo!
This agent features:
  • Multi-model support (OpenAI & Azure OpenAI)
  • Error handling and recovery
  • Input validation
  • Real-time response streaming
============================================================

🟢 System Health: Healthy (85.2/100)
========================================
Memory: 12.5GB free of 16.0GB (78.1% available)
Disk: 250.3GB free of 500.0GB (50.1% available)
CPU: 8 cores, 85.2% available
========================================

🔧 Model Configuration:
   Default Model: gpt-4o-mini
   Provider: OpenAI ✅
   Status: Configuration Valid ✅

🔍 Testing model connection...
✅ Model connection test successful
🚀 Creating agent...
✅ Agent created successfully!

💬 Chat Instructions:
========================================
• Type your message and press Enter
• Type 'quit', 'exit', 'bye', or 'q' to exit
• Press Ctrl+C at any time for graceful shutdown
• Empty messages are ignored
• Maximum message length: 10,000 characters
========================================

👤 You: Hello! How are you?

🤖 Agent: Hello! I'm doing well, thank you for asking! I'm Agno Assistant, powered by the Agno framework. I'm here to help you with any questions or tasks you might have. 

How can I assist you today? Whether you need help with:
- Answering questions
- Problem-solving
- Code examples
- General conversation
- Or anything else!

I'm ready to help! 😊

👤 You: stats

📊 Performance Report
========================================
Uptime: 2.3 minutes
Total Operations: 3
Successful Operations: 3
Success Rate: 100.0%
Avg Response Time: 1.24s
Max Response Time: 2.18s
Min Response Time: 0.85s
Avg Memory Usage: 145.2MB
Avg CPU Usage: 12.4%
========================================
```

## 🏗️ Project Structure

The repository has been reorganized to follow a src/ layout with clear separation between source code, examples, tests, and documentation. Root-level entry points are lightweight launchers that import implementations from `src/`.

```
agent-demo/
├── src/                         # Source code (package-style layout)
│   ├── agents/                  # Agent implementations (basic, memory, reasoning, tools, multi-agent)
│   │   ├── basic.py
│   │   ├── memory.py
│   │   ├── reasoning.py
│   │   ├── tools.py
│   │   └── multi_agent/         # Multi-agent components
│   ├── models/                  # Model configuration and provider adapters
│   │   └── config.py
│   ├── services/                # Supporting services (monitoring, storage, utils)
│   │   └── performance_monitor.py
│   └── lib/                  # Shared utilities
│       ├── error_handling.py
│       └── logging_config.py
├── examples/                    # Example scripts and multi-agent demos
├── tests/                       # Unit, integration, and contract tests
├── docs/                        # Documentation (guides, status, how-tos)
├── specs/                       # Feature specifications and plans
├── .specify/                    # SpecKit configuration
├── single_agent_demo.py         # Main entry point - unified agent with 5 modes
├── multi_agent_demo.py          # Root-level launcher for multi-agent demos
├── streamlit_ui.py              # Streamlit web interface
├── agno_os_ui.py                # Advanced UI interface
├── requirements.txt             # Python dependencies
└── .env                         # Environment configuration (not committed)
```

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Categories
```bash
# Model configuration tests
python -m pytest tests/test_agent_functionality.py::TestModelConfiguration -v

# Error handling tests
python -m pytest tests/test_agent_functionality.py::TestErrorHandling -v

# Performance monitoring tests
python -m pytest tests/test_agent_functionality.py::TestPerformanceMonitor -v
```

## 📊 Performance Monitoring

### Built-in Monitoring Features
- **Response Time Tracking**: Monitor API call performance
- **Memory Usage**: Track memory consumption patterns
- **System Health**: CPU, memory, and disk usage monitoring
- **Error Rate Tracking**: Success/failure ratio monitoring
- **Performance Alerts**: Automatic alerts for performance issues

### Performance Thresholds
- **Response Time**: < 5 seconds (alerts if exceeded)
- **Memory Usage**: < 500MB (alerts if exceeded)
- **CPU Usage**: < 80% (alerts if exceeded)

## 🔒 Security Features

### Input Validation
- Maximum input length: 10,000 characters
- Suspicious content detection (script injection, etc.)
- Input sanitization and trimming

### Secure Logging
- Automatic credential redaction in logs
- Structured logging with secure filtering
- Log rotation to prevent disk space issues

### API Key Protection
- Environment variable validation
- No hardcoded credentials
- Secure error message handling

## 🔧 Configuration Options

### Environment Variables
```env
# Model Configuration
DEFAULT_MODEL=gpt-4o-mini          # Default model to use
REASONING_MODEL=gpt-4              # Model for reasoning tasks (optional)
FAST_MODEL=gpt-3.5-turbo          # Model for fast responses (optional)

# Logging Configuration
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_FILE=true                   # Enable file logging
LOG_MAX_SIZE=10                    # Max log file size in MB

# Performance Configuration
PERFORMANCE_ALERTS=true            # Enable performance alerts
MAX_RESPONSE_TIME=5.0             # Max response time in seconds
MAX_MEMORY_USAGE=500.0            # Max memory usage in MB
```

## 🚨 Troubleshooting

### Common Issues

#### "Configuration Invalid" Error
```bash
# Check your .env file
cat .env

# Verify API key format
# OpenAI keys start with 'sk-'
# Azure keys are typically 32 characters
```

#### Performance Alerts
```bash
# Check system resources
python -c "from performance_monitor import get_performance_monitor; get_performance_monitor().print_system_health()"

# View performance stats
# Type 'stats' during chat session
```

#### Connection Issues
```bash
# Test model connection
python -c "from model_config import test_model_connection; test_model_connection()"

# Check logs
tail -f logs/agent.log
```

### Getting Help
1. Check the logs in `logs/agent.log`
2. Run the test suite: `python -m pytest tests/ -v`
3. Use the `help` command during chat sessions
4. Check system health with the `health` command

## 📈 Performance Optimization

### Tips for Better Performance
1. **Use appropriate models**: `gpt-4o-mini` for general tasks, `gpt-4` for complex reasoning
2. **Monitor resource usage**: Use built-in `health` command
3. **Optimize input length**: Keep messages concise for faster responses
4. **Check system resources**: Ensure adequate memory and disk space

### Performance Benchmarks
- **Response Time**: < 2 seconds for basic interactions
- **Memory Usage**: < 200MB for typical sessions  
- **CPU Usage**: < 20% during normal operation
- **Success Rate**: > 99% for valid API configurations

## 📚 Documentation

### Quick Start Guides
- **[Memory Agent Guide](docs/MEMORY_AGENT_GUIDE.md)** - Build agents with conversation history
- **[Reasoning Agent Guide](docs/REASONING_AGENT_GUIDE.md)** - Build agents with structured reasoning
- **[Tools Agent Guide](docs/TOOLS_AGENT_GUIDE.md)** - Build agents with web search and tools

### Project Documentation
- **[Pre-Push Checklist](docs/PRE_PUSH_CHECKLIST.md)** - Development workflow checklist
- **[Documentation Organization](docs/DOCS_ORGANIZATION.md)** - How documentation is structured

For a complete documentation index, see **[docs/README.md](docs/README.md)**.

## 🤝 Contributing

This project follows a clean development workflow:

1. **Review the project structure** in the `src/` directory
2. **Run tests** before submitting changes: `python -m pytest tests/ -v`
3. **Update documentation** for new features
4. **Check the [Pre-Push Checklist](docs/PRE_PUSH_CHECKLIST.md)** before pushing

## 📄 License

This project is open source and available under the MIT License.

---

**🎉 Ready to build amazing AI agents with enhanced reliability and performance!**