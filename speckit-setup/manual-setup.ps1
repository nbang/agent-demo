# Manual SpecKit Setup (GitHub API Workaround)

# This script creates a SpecKit-like structure manually without relying on GitHub API
# Use this when the main setup-speckit.ps1 fails due to GitHub API rate limiting

Write-Host "🛠️  Manual SpecKit Setup (GitHub API Workaround)" -ForegroundColor Green
Write-Host "=" * 60

# Navigate to project root if we're in the speckit-setup folder
if ((Get-Location).Path.EndsWith("speckit-setup")) {
    Set-Location ..
    Write-Host "📁 Moved to project root: $(Get-Location)" -ForegroundColor Cyan
}

Write-Host "`n📋 Creating SpecKit-compatible project structure..." -ForegroundColor Yellow

# Step 1: Create .specify directory structure
Write-Host "1. Creating .specify directory..." -ForegroundColor White
New-Item -Path ".specify" -ItemType Directory -Force | Out-Null
New-Item -Path ".specify/memory" -ItemType Directory -Force | Out-Null

# Create config.json
$configContent = @"
{
  "version": "1.0.0",
  "ai_agent": "copilot",
  "project_type": "python",
  "framework": "agno",
  "created": "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')"
}
"@
Set-Content -Path ".specify/config.json" -Value $configContent
Write-Host "   ✅ Created .specify/config.json" -ForegroundColor Green

# Step 2: Create specs directory structure
Write-Host "2. Creating specs directory..." -ForegroundColor White
New-Item -Path "specs" -ItemType Directory -Force | Out-Null
Write-Host "   ✅ Created specs/ directory" -ForegroundColor Green

# Step 3: Create scripts directory structure
Write-Host "3. Creating scripts directory..." -ForegroundColor White
New-Item -Path "scripts" -ItemType Directory -Force | Out-Null
New-Item -Path "scripts/powershell" -ItemType Directory -Force | Out-Null
New-Item -Path "scripts/bash" -ItemType Directory -Force | Out-Null

# Create basic PowerShell scripts
$setupPlanScript = @"
# Setup Plan Script - Manual Implementation
param(
    [switch]`$Json
)

Write-Host "🔧 Setup Plan Workflow" -ForegroundColor Green
Write-Host "This is a manual implementation for GitHub API workaround"

if (`$Json) {
    Write-Host '{"status": "manual_setup", "message": "SpecKit structure created manually"}' 
} else {
    Write-Host "SpecKit project structure has been set up manually."
    Write-Host "You can now create specifications using GitHub Copilot Chat:"
    Write-Host "  /speckit.constitution"
    Write-Host "  /speckit.specify"  
    Write-Host "  /speckit.plan"
    Write-Host "  /speckit.tasks"
}
"@
Set-Content -Path "scripts/powershell/setup-plan.ps1" -Value $setupPlanScript
Write-Host "   ✅ Created scripts/powershell/setup-plan.ps1" -ForegroundColor Green

$checkPrereqScript = @"
# Check Prerequisites Script - Manual Implementation  
param(
    [switch]`$Json,
    [switch]`$RequireTasks,
    [switch]`$IncludeTasks
)

Write-Host "🔍 Checking Prerequisites" -ForegroundColor Green

`$prereqs = @{
    "python" = (Get-Command python -ErrorAction SilentlyContinue) -ne `$null
    "git" = (Get-Command git -ErrorAction SilentlyContinue) -ne `$null  
    "agno" = `$true  # Assume agno is available from requirements.txt
}

if (`$Json) {
    `$prereqs | ConvertTo-Json
} else {
    foreach (`$req in `$prereqs.GetEnumerator()) {
        if (`$req.Value) {
            Write-Host "  ✅ `$(`$req.Key)" -ForegroundColor Green
        } else {
            Write-Host "  ❌ `$(`$req.Key)" -ForegroundColor Red  
        }
    }
}
"@
Set-Content -Path "scripts/powershell/check-prerequisites.ps1" -Value $checkPrereqScript
Write-Host "   ✅ Created scripts/powershell/check-prerequisites.ps1" -ForegroundColor Green

# Step 4: Create initial constitution template
Write-Host "4. Creating initial constitution template..." -ForegroundColor White
$constitutionContent = @"
# Project Constitution

> **Note**: This constitution was created manually due to GitHub API limitations.  
> You can update it using GitHub Copilot Chat with: `/speckit.constitution`

## Project Principles

### Core Values
- **AI-First Development**: Leverage AI agents for enhanced productivity
- **Agno Framework Integration**: Follow Agno best practices and patterns
- **Quality Over Speed**: Prioritize maintainable, tested code
- **User-Centric Design**: Focus on user experience and usability

### Development Standards
- **Code Quality**: Maintain clean, readable, and well-documented code
- **Testing Requirements**: Include comprehensive testing for all features
- **Performance Guidelines**: Ensure responsive AI agent interactions (<2s response time)
- **Security Practices**: Secure handling of API keys and user data

### Architecture Principles
- **Modular Design**: Separate concerns between different agent types
- **Framework Trust**: Use Agno framework features directly, avoid unnecessary abstractions
- **Simplicity First**: Start with simple solutions, add complexity only when needed
- **Integration Testing**: Prioritize integration tests over mocks

## Agno Agent Specific Guidelines

### Agent Development
- Each agent type should have clear, single responsibility
- Maintain consistent error handling across all agents
- Implement proper logging and monitoring
- Support both OpenAI and Azure OpenAI configurations

### Tool Integration
- Tools should be composable and reusable
- Include proper error handling for external API calls
- Cache results where appropriate to improve performance
- Document tool capabilities and limitations

### Memory Management
- Implement efficient conversation history storage
- Provide clear privacy controls for stored data
- Support conversation export/import functionality
- Regular cleanup of old conversation data

---
*Constitution created: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')*
*Framework: Agno | AI Agent: GitHub Copilot*
"@
Set-Content -Path ".specify/memory/constitution.md" -Value $constitutionContent
Write-Host "   ✅ Created .specify/memory/constitution.md" -ForegroundColor Green

# Step 5: Create example specification template
Write-Host "5. Creating example specification template..." -ForegroundColor White
New-Item -Path "specs/000-example" -ItemType Directory -Force | Out-Null

$exampleSpec = @"
# Example Feature Specification

> **Template created manually** - Use this as a starting point for your specifications.
> 
> **To create real specifications**: Use GitHub Copilot Chat with `/speckit.specify [description]`

## Feature Overview
This is an example specification template showing the structure for SpecKit specifications.

## User Stories
- As a developer, I want to understand the SpecKit specification format
- As a team member, I want to see examples of well-structured requirements

## Acceptance Criteria
- [ ] Specification includes clear user stories
- [ ] Acceptance criteria are testable and measurable  
- [ ] Technical requirements are documented
- [ ] Success metrics are defined

## Technical Requirements
- Compatible with Agno framework
- Follows project constitution principles
- Includes error handling and logging
- Supports both OpenAI and Azure OpenAI

## Success Metrics
- Feature works as specified in acceptance criteria
- Code coverage > 80%
- Response time < 2 seconds
- No breaking changes to existing functionality

---
*Example specification template*
*Created: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')*
"@
Set-Content -Path "specs/000-example/spec.md" -Value $exampleSpec
Write-Host "   ✅ Created specs/000-example/spec.md" -ForegroundColor Green

# Step 6: Create README for manual usage
Write-Host "6. Creating manual usage guide..." -ForegroundColor White
$manualUsageGuide = @"
# Manual SpecKit Usage Guide

Since the GitHub API is rate-limited, you'll need to use GitHub Copilot Chat manually to create specifications.

## How to Use SpecKit Commands (Manual Process)

### 1. Create/Update Constitution
In GitHub Copilot Chat, type:
\`\`\`
/speckit.constitution Create principles for AI agent development using Agno framework, focusing on code quality, testing standards, and performance requirements for real-time agent interactions.
\`\`\`

This will generate content that you should save to: `.specify/memory/constitution.md`

### 2. Create Feature Specifications  
For each feature, use:
\`\`\`
/speckit.specify Build a conversational AI agent using the Agno framework that supports both Azure OpenAI and regular OpenAI models. The agent should provide clear responses with markdown formatting, interactive chat loop, and graceful error handling.
\`\`\`

Save the generated content to: `specs/001-feature-name/spec.md`

### 3. Generate Technical Plans
After creating specifications:
\`\`\`
/speckit.plan The agent uses Agno framework with configurable OpenAI/Azure OpenAI models. Use python-dotenv for environment management, implement model configuration abstraction, include comprehensive error handling.
\`\`\`

Save to: `specs/001-feature-name/plan.md`

### 4. Create Task Breakdowns
Finally, generate executable tasks:
\`\`\`
/speckit.tasks
\`\`\`

Save to: `specs/001-feature-name/tasks.md`

## Directory Structure

Your project now has this structure:
\`\`\`
.specify/
├── memory/
│   └── constitution.md      # Project principles (update via /speckit.constitution)
└── config.json            # Project configuration  

specs/
├── 000-example/            # Example specification template
│   └── spec.md
└── [your-features]/        # Create via /speckit.specify commands
    ├── spec.md            # Feature specification  
    ├── plan.md            # Technical implementation plan
    ├── tasks.md           # Executable task breakdown
    └── contracts/         # API contracts (create manually)

scripts/
├── powershell/            # Basic automation scripts
└── bash/                 # Cross-platform scripts
\`\`\`

## Next Steps

1. **Start with Constitution**: Use `/speckit.constitution` to create your project principles
2. **Specify Features**: Use `/speckit.specify` for each agent type (basic, tools, reasoning, memory)
3. **Create Plans**: Use `/speckit.plan` to generate technical implementation details
4. **Break Down Tasks**: Use `/speckit.tasks` to create actionable development steps
5. **Implement**: Follow the test-first development approach outlined in your plans

## Benefits Even Without CLI

- ✅ Structured project organization
- ✅ Clear specification templates
- ✅ GitHub Copilot Chat integration
- ✅ Manual workflow that works around API limits
- ✅ Foundation for when CLI becomes available

The manual process gives you all the benefits of spec-driven development while avoiding GitHub API limitations!
"@
Set-Content -Path "MANUAL_SPECKIT_USAGE.md" -Value $manualUsageGuide
Write-Host "   ✅ Created MANUAL_SPECKIT_USAGE.md" -ForegroundColor Green

# Step 7: Summary
Write-Host "`n🎉 Manual SpecKit Setup Complete!" -ForegroundColor Green
Write-Host "=" * 50

Write-Host "`n📁 Created Structure:" -ForegroundColor Yellow
Write-Host "  ✅ .specify/ - Configuration and memory" -ForegroundColor Green
Write-Host "  ✅ specs/ - Feature specifications directory" -ForegroundColor Green  
Write-Host "  ✅ scripts/ - Automation scripts" -ForegroundColor Green
Write-Host "  ✅ MANUAL_SPECKIT_USAGE.md - Usage guide" -ForegroundColor Green

Write-Host "`n🚀 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Read: MANUAL_SPECKIT_USAGE.md" -ForegroundColor White
Write-Host "  2. Open GitHub Copilot Chat" -ForegroundColor White  
Write-Host "  3. Start with: /speckit.constitution" -ForegroundColor White
Write-Host "  4. Then create specs: /speckit.specify [description]" -ForegroundColor White

Write-Host "`n💡 This manual setup gives you all SpecKit benefits without GitHub API issues!" -ForegroundColor Yellow
Write-Host "✨ Happy spec-driven development! 🎉" -ForegroundColor Green