# Agno Agent Demo Project

A comprehensive demonstration of building AI agents using the Agno framework. This project showcases various capabilities including basic agents, tools integration, reasoning, and memory management.

## 🚀 Features

- **Basic Agent**: Simple conversational AI agent
- **Agent with Tools**: Web search capabilities using DuckDuckGo
- **Reasoning Agent**: Step-by-step problem analysis and structured thinking
- **Memory Agent**: Persistent memory across conversations

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key (or other supported model provider)
- pip package manager

## 🛠️ Installation

1. **Clone or download this project**
   ```bash
   cd agent-demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your API configuration:
   
   **For Azure OpenAI (Recommended for Enterprise):**
   ```env
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
   AZURE_OPENAI_API_VERSION=2023-12-01-preview
   DEFAULT_MODEL=gpt-4o-mini
   ```
   
   **For Regular OpenAI:**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DEFAULT_MODEL=gpt-4o-mini
   ```

4. **Configure Model Preferences (Optional)**
   
   You can customize which models to use for different purposes:
   ```env
   # Main model for most tasks
   DEFAULT_MODEL=gpt-4o-mini
   
   # Specialized model for complex reasoning (optional)
   REASONING_MODEL=gpt-4o
   
   # Fast model for simple tasks (optional)
   FAST_MODEL=gpt-3.5-turbo
   ```

## 🎮 Usage

### Basic Agent
Run the simple conversational agent:
```bash
python agent.py
```

### Agent with Tools
Run the agent with web search capabilities:
```bash
python examples/agent_with_tools.py
```

### Reasoning Agent
Run the agent with structured reasoning capabilities:
```bash
python examples/reasoning_agent.py
```

### Memory Agent
Run the agent with persistent memory:
```bash
python examples/agent_with_memory.py
```

### Azure OpenAI Specific Examples
Run Azure OpenAI specific implementations:
```bash
python azure_agent.py
python examples/azure_agent_with_tools.py
```

## 🏗️ Project Structure

```
agent-demo/
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot configuration
├── examples/
│   ├── agent_with_tools.py       # Agent with web search tools
│   ├── reasoning_agent.py        # Agent with reasoning capabilities
│   └── agent_with_memory.py      # Agent with persistent memory
├── agent.py                      # Basic agent implementation
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🔧 Configuration

### Model Selection
You can change the AI model in any script by modifying the model parameter:

```python
# OpenAI models
model=OpenAIChat(id="gpt-4")           # More capable, slower
model=OpenAIChat(id="gpt-3.5-turbo")   # Faster, less expensive

# Other supported models (uncomment dependencies in requirements.txt)
# model=Anthropic(id="claude-3-sonnet")
# model=Groq(id="llama-3.3-70b-versatile")
# model=Cohere(id="command-r-plus")
```

### Adding Tools
The Agno framework supports various tools:

```python
from agno.tools.duckduckgo import DuckDuckGoTools      # Web search
from agno.tools.reasoning import ReasoningTools        # Structured reasoning
from agno.tools.dalle import DalleTools                # Image generation
```

## 🎯 Example Interactions

### Basic Agent
```
👤 You: What is artificial intelligence?
🤖 Agent: Artificial intelligence (AI) is a branch of computer science...
```

### Agent with Tools
```
👤 You: What's the weather like in Tokyo today?
🔍 Agent: *Searching for current weather information...*
Based on current data, Tokyo is experiencing...
```

### Reasoning Agent
```
👤 You: Should companies adopt remote work policies?
🧠 Agent: Let me analyze this systematically:

1. **Economic Considerations**
   - Cost savings on office space...
   - Productivity metrics show...

2. **Employee Satisfaction**
   - Surveys indicate...
```

### Memory Agent
```
👤 You: My name is Alice and I love hiking
🧠 Agent: Nice to meet you, Alice! I'll remember that you enjoy hiking...

# Later in conversation or next session:
👤 You: What outdoor activities would you recommend?
🧠 Agent: Since you mentioned you love hiking, Alice, I'd recommend...
```

## 🔍 Advanced Features

### Custom Instructions
Customize agent behavior by modifying the instructions:

```python
agent = Agent(
    instructions=[
        "You are a helpful coding assistant.",
        "Always provide working code examples.",
        "Explain complex concepts in simple terms.",
    ]
)
```

### Knowledge Integration
Add knowledge bases for domain-specific information:

```python
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

knowledge = Knowledge(
    vector_db=PgVector(table_name="docs", db_url="your_db_url"),
)
knowledge.add_content(url="https://example.com/documentation.pdf")

agent = Agent(
    model=OpenAIChat(id="gpt-4"),
    knowledge=knowledge,
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Make sure you've installed all dependencies: `pip install -r requirements.txt`
   - Check that you're using Python 3.8 or higher

2. **API Key Errors**
   - Verify your `.env` file contains the correct API key
   - Ensure the API key has sufficient credits/permissions

3. **Model Access Errors**
   - Some models require special access or different API keys
   - Check the model provider's documentation

### Debug Mode
Add debug information to your agent:

```python
agent = Agent(
    model=OpenAIChat(id="gpt-4"),
    debug=True,  # Enable debug output
)
```

## 📚 Learn More

- [Agno Framework Documentation](https://docs.agno.ai)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Python Environment Setup](https://docs.python.org/3/tutorial/venv.html)

## 🤝 Contributing

Feel free to experiment with the code and add your own examples! Some ideas:
- Add support for different model providers
- Create agents with specialized tools
- Implement multi-agent workflows
- Add web interfaces using Streamlit or FastAPI

## 📄 License

This project is for educational purposes. Please check the licenses of individual dependencies and model providers for production use.

## � SpecKit Integration

Transform your development process with **SpecKit** - a spec-driven development tool that helps you create structured specifications, implementation plans, and executable tasks.

### Quick Setup
```bash
# Run the automated setup
.\speckit-setup\setup-speckit.ps1

# Follow the checklist
# Open speckit-setup\SPECKIT_CHECKLIST.md
```

### What You Get
- 📋 **Structured Specifications** - Convert ideas into clear requirements
- 🏗️ **Implementation Plans** - Technical architecture and approach
- ✅ **Task Breakdowns** - Executable development steps
- 🧪 **Quality Gates** - Built-in best practices enforcement

### Resources
- 📁 **All SpecKit files** are in the `speckit-setup/` folder
- 🚀 **Quick Start** - `speckit-setup/README.md`
- 📋 **Step-by-step** - `speckit-setup/SPECKIT_CHECKLIST.md`
- 📚 **Complete Guide** - `speckit-setup/SPECKIT_IMPLEMENTATION_GUIDE.md`

## �🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the Agno framework documentation
3. Ensure all dependencies are correctly installed
4. Verify your environment variables are properly set
5. For SpecKit issues, check `speckit-setup/SPECKIT_COMMANDS.md`

Happy coding with Agno! 🚀