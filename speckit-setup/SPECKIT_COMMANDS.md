# SpecKit Command Reference for Agno Agent Demo

## Quick Command Reference

### Installation Commands
```powershell
# Install SpecKit CLI
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Verify installation
specify --help
specify check

# Alternative using uvx (if tool install fails)
uvx --from git+https://github.com/github/spec-kit.git specify --help
```

### Project Initialization
```powershell
# Initialize in current directory (recommended for existing projects)
specify init --here --ai copilot --force

# Initialize new project
specify init my-project --ai copilot

# Initialize with different AI agents
specify init --here --ai claude
specify init --here --ai gemini
specify init --here --ai cursor
specify init --here --ai windsurf
```

### Core SpecKit Workflow

#### 1. Create Project Constitution
```copilot-chat
/speckit.constitution Create principles focused on:
- AI agent development best practices using Agno framework
- Code quality standards for Python AI applications
- Testing requirements for AI agents
- Performance guidelines for real-time agent interactions
- Security considerations for OpenAI/Azure OpenAI integrations
- Modular architecture for scalable agent systems
```

#### 2. Create Feature Specifications
```copilot-chat
# Basic Agent
/speckit.specify Build a conversational AI agent using the Agno framework that supports both Azure OpenAI and regular OpenAI models. The agent should provide clear responses with markdown formatting, interactive chat loop, graceful error handling, and environment variable configuration.

# Tools Agent
/speckit.specify Build an AI agent with web search capabilities using DuckDuckGo integration through the Agno framework. The agent should search the web, process results, and provide informed responses based on real-time information.

# Reasoning Agent
/speckit.specify Build a reasoning AI agent using Agno that performs step-by-step problem analysis with structured thinking. The agent should break down complex problems, show reasoning steps, and present solutions clearly.

# Memory Agent
/speckit.specify Build an AI agent with persistent memory capabilities using Agno framework. The agent should store conversation history, maintain context across sessions, and provide personalized responses.

# Multi-Agent System
/speckit.specify Build a multi-agent orchestration system using Agno where specialized agents collaborate on complex tasks. Include agent communication, task delegation, result aggregation, and dynamic agent selection.
```

#### 3. Generate Technical Plans
```copilot-chat
# Basic implementation plan
/speckit.plan The agent uses Agno framework with configurable OpenAI/Azure OpenAI models. Use python-dotenv for environment management, implement model configuration abstraction, include comprehensive error handling, and provide user-friendly CLI interface.

# Advanced system plan
/speckit.plan The multi-agent system uses Agno framework with FastAPI for web interface, WebSocket for real-time communication, modular architecture for different agent types, and PostgreSQL for persistent storage. Implement agent orchestration and shared knowledge base.

# Tools integration plan
/speckit.plan The tools agent integrates DuckDuckGo search through Agno's tool system. Implement search result processing, response formatting, and error handling for failed searches. Use asyncio for concurrent operations.
```

#### 4. Break Down into Tasks
```copilot-chat
# Generate executable tasks
/speckit.tasks

# This creates task.md files with specific implementation steps
```

### Project Structure Commands
```powershell
# Check project structure
ls .specify/
ls specs/
ls scripts/

# View generated specifications
Get-Content specs/001-*/spec.md
Get-Content specs/001-*/plan.md
Get-Content specs/001-*/tasks.md
```

### Implementation Commands
```powershell
# Execute implementation plan
implement specs/001-basic-agent/plan.md

# Run setup planning workflow
scripts/powershell/setup-plan.ps1 -Json

# Check prerequisites
scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
```

## Agno Agent-Specific SpecKit Commands

### Agent Development Patterns
```copilot-chat
# Research Agno best practices
/speckit.plan Research Agno framework integration patterns, performance optimization for AI agents, and production deployment strategies for scalable agent systems.

# Agent architecture validation
/speckit.constitution Review current architecture alignment with Agno framework best practices and AI agent development principles.
```

### Feature Enhancement Specifications
```copilot-chat
# Web UI Enhancement
/speckit.specify Add a modern web interface to the Agno agent demo using FastAPI and WebSocket for real-time chat. Include agent selection, conversation history, and responsive design.

# Knowledge Base Integration
/speckit.specify Integrate a vector database knowledge base system allowing agents to store, retrieve, and share learned information across conversations using embeddings and semantic search.

# Agent Performance Monitoring
/speckit.specify Add comprehensive monitoring and logging for agent performance, response times, error rates, and usage analytics. Include dashboard for system health monitoring.
```

## File Organization

### SpecKit Directory Structure
```
.specify/
├── memory/
│   └── constitution.md      # Project principles
└── config.json            # SpecKit configuration

specs/
├── 001-basic-agent/
│   ├── spec.md            # Feature specification
│   ├── plan.md            # Technical implementation plan
│   ├── research.md        # Technology research
│   ├── data-model.md      # Data structures
│   ├── contracts/         # API contracts
│   └── tasks.md           # Executable tasks
├── 002-tools-agent/
├── 003-reasoning-agent/
└── 004-memory-agent/

scripts/
├── powershell/            # Windows automation scripts
│   ├── setup-plan.ps1
│   ├── check-prerequisites.ps1
│   └── implement.ps1
└── bash/                  # Linux/macOS scripts
```

## Troubleshooting Commands

### Common Issues
```powershell
# Permission errors
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Tool not found
uv tool list
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git --force

# Git conflicts
git status
git stash
specify init --here --ai copilot --force

# Verification
specify check
specify --version
```

### Debug Mode
```powershell
# Enable debug output
specify init my-project --ai copilot --debug

# Check tool installation
specify check --verbose
```

## Best Practices for Agno Agent Demo

### 1. Specification Writing
- Focus on "what" and "why", not "how"
- Include user experience requirements
- Specify performance requirements
- Define error handling expectations

### 2. Technical Planning
- Leverage existing Agno framework patterns
- Maintain compatibility with current structure
- Plan for scalability and modularity
- Include testing strategies

### 3. Implementation Order
1. Create contracts and API specifications
2. Write tests (contract → integration → unit)
3. Implement source code to make tests pass
4. Validate against specifications

### 4. Quality Gates
- **Simplicity Gate**: Use ≤3 projects initially
- **Anti-Abstraction Gate**: Use Agno framework directly
- **Integration-First Gate**: Write contract tests before implementation

## Next Steps Checklist

- [ ] Run `setup-speckit.ps1` to initialize SpecKit
- [ ] Create project constitution with `/speckit.constitution`
- [ ] Generate specifications for existing features
- [ ] Create technical implementation plans
- [ ] Break down features into executable tasks
- [ ] Implement enhanced project structure
- [ ] Add comprehensive testing
- [ ] Document architectural decisions

## Additional Resources

- [SpecKit Repository](https://github.com/github/spec-kit)
- [Agno Framework Documentation](https://agno.readthedocs.io/)
- [Spec-Driven Development Guide](https://github.com/github/spec-kit/blob/main/spec-driven.md)