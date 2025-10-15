# Multi-Agent Examples with Agno Framework

This directory contains comprehensive examples of multi-agent systems using the Agno framework, demonstrating different collaboration patterns and use cases.

## 🤖 Available Examples

### 1. Research Team (`research_team.py`)
**Collaborative research with specialized agents**
- **Web Researcher**: Real-time information gathering from news and web sources
- **Academic Researcher**: Scholarly literature review and citations
- **Social Media Researcher**: Public sentiment and social trends analysis
- **Analysis Coordinator**: Synthesis and comprehensive reporting

**Use cases**: Market research, competitive analysis, trend investigation, comprehensive reports

### 2. Content Creation Team (`content_creation_team.py`) 
**End-to-end content production pipeline**
- **Research Specialist**: Information gathering and fact-checking
- **Content Strategist**: Planning, structure, and messaging strategy
- **Content Writer**: Creative writing and composition
- **Content Editor**: Review, editing, and quality improvement
- **SEO Specialist**: Search optimization and engagement enhancement

**Use cases**: Blog posts, articles, marketing content, documentation, publications

### 3. Customer Service Team (`customer_service_team.py`)
**Multi-tier customer support system**
- **Triage Agent**: Initial assessment and intelligent routing
- **Technical Support**: Technical troubleshooting and problem-solving
- **Billing Support**: Payment and account issue resolution
- **Product Specialist**: Feature guidance and training support
- **Escalation Manager**: Complex cases and complaint resolution

**Use cases**: Customer support, help desk operations, service management

## 🚀 Getting Started

### Prerequisites
1. **Environment Setup**: Ensure your `.env` file is configured with API keys
2. **Dependencies**: Install required packages from `requirements.txt`
3. **Model Configuration**: The examples use the centralized `model_config.py`

### Running Examples

#### Option 1: Interactive Menu
```bash
cd examples/multi_agents
python run_examples.py
```

#### Option 2: Run Individual Examples
```bash
# Research Team
python research_team.py

# Content Creation Team  
python content_creation_team.py

# Customer Service Team
python customer_service_team.py
```

#### Option 3: Get Examples Information
```bash
python run_examples.py --info
```

## 🎯 Key Multi-Agent Patterns Demonstrated

### **Specialization**
Each agent has distinct expertise and tools:
- Different knowledge domains
- Specialized tool access (web search, reasoning, etc.)
- Role-specific instructions and behavior

### **Collaboration** 
Agents work together towards common goals:
- Information sharing between agents
- Building on each other's work
- Coordinated problem-solving

### **Workflow**
Structured processes with clear handoffs:
- Sequential task execution
- Quality control stages
- Review and refinement cycles

### **Escalation**
Hierarchical handling of complex cases:
- Triage and routing systems
- Specialist consultation
- Management oversight

## 📊 Example Output

When you run these examples, you'll see:
- **Individual agent responses** with specialized expertise
- **Team coordination** and task delegation
- **Comprehensive final outputs** combining all perspectives
- **Source citations** and reference materials
- **Interactive prompts** for user input and customization

## 🔧 Customization

Each example can be customized by:
- **Modifying agent instructions** for different domains
- **Adding new specialized agents** to teams
- **Changing collaboration patterns** and workflows  
- **Integrating additional tools** and capabilities
- **Adjusting output formats** and structures

## 💡 Technical Architecture

### **Team Structure**
```python
team = Team(
    name="Team Name",
    model=get_configured_model(),
    members=[agent1, agent2, agent3],
    instructions="Team coordination instructions",
    show_members_responses=True,  # Show individual contributions
    markdown=True,
)
```

### **Agent Configuration**
```python
agent = Agent(
    name="Agent Name",
    role="Agent's specific role",
    model=get_configured_model(),
    tools=[DuckDuckGoTools(), ReasoningTools()],
    instructions="Detailed role-specific instructions",
    add_name_to_context=True,
    markdown=True,
)
```

## 📋 Environment Variables Required

Make sure your `.env` file includes:
```bash
# Azure OpenAI (if using Azure)
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
OPENAI_MODEL_NAME=your_model_name

# Or Standard OpenAI
OPENAI_API_KEY=your_openai_key
```

## 🎯 Best Practices

1. **Clear Role Definition**: Each agent should have distinct, well-defined responsibilities
2. **Appropriate Tool Selection**: Match tools to agent capabilities and needs
3. **Effective Instructions**: Provide detailed, actionable guidance for each agent
4. **Team Coordination**: Use clear team-level instructions for collaboration
5. **Output Management**: Structure responses for clarity and usefulness

## 🚦 Troubleshooting

### Common Issues:
- **API Key Errors**: Check your `.env` file configuration
- **Import Errors**: Ensure all dependencies are installed
- **Model Access**: Verify your model permissions and quotas
- **Tool Limitations**: Some tools may have rate limits or usage restrictions

### Getting Help:
- Check the main project `README.md` for setup instructions
- Review `model_config.py` for configuration options
- Test individual agents before running full teams
- Monitor API usage and costs during development

## 📚 Learn More

- **Agno Documentation**: Learn about the framework capabilities
- **Tool Integration**: Explore available tools and extensions
- **Custom Agents**: Create your own specialized agents
- **Advanced Patterns**: Implement complex multi-agent workflows

---

*These examples demonstrate the power of specialized AI agents working together to solve complex problems. Each pattern can be adapted and extended for your specific use cases and requirements.*