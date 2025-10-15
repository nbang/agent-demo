# SpecKit Quick Start Script for Agno Agent Demo

# This PowerShell script helps you implement SpecKit in your existing Agno Agent Demo project
# Run this script from your project root directory: d:\work\agent-demo

Write-Host "🚀 SpecKit Implementation for Agno Agent Demo" -ForegroundColor Green
Write-Host "=" * 60

# Step 1: Check prerequisites
Write-Host "`n📋 Step 1: Checking Prerequisites..." -ForegroundColor Yellow

# Navigate to project root if we're in the speckit-setup folder
if ((Get-Location).Path.EndsWith("speckit-setup")) {
    Set-Location ..
    Write-Host "📁 Moved to project root: $(Get-Location)" -ForegroundColor Cyan
}

# Check if uv is installed
try {
    $uvVersion = uv --version
    Write-Host "✅ uv is installed: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ uv is not installed. Installing uv..." -ForegroundColor Red
    Write-Host "Please install uv first: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Yellow
    Read-Host "Press Enter to continue after installing uv"
}

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    exit 1
}

# Step 2: Install SpecKit CLI
Write-Host "`n🔧 Step 2: Installing SpecKit CLI..." -ForegroundColor Yellow

try {
    Write-Host "Installing SpecKit CLI globally..."
    uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
    Write-Host "✅ SpecKit CLI installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install SpecKit CLI. Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Trying alternative installation method..." -ForegroundColor Yellow
    
    try {
        # Try with uvx
        uvx --from git+https://github.com/github/spec-kit.git specify --help
        Write-Host "✅ SpecKit CLI available via uvx!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Could not install SpecKit CLI. Please check your internet connection and try manually." -ForegroundColor Red
        exit 1
    }
}

# Step 3: Verify installation
Write-Host "`n✨ Step 3: Verifying Installation..." -ForegroundColor Yellow

try {
    specify --help | Out-Null
    Write-Host "✅ SpecKit CLI is working correctly!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  SpecKit CLI not found in PATH. Trying uvx method..." -ForegroundColor Yellow
    try {
        uvx --from git+https://github.com/github/spec-kit.git specify --help | Out-Null
        Write-Host "✅ SpecKit CLI available via uvx!" -ForegroundColor Green
        $useUvx = $true
    } catch {
        Write-Host "❌ SpecKit CLI verification failed." -ForegroundColor Red
        exit 1
    }
}

# Step 4: Check current project
Write-Host "`n📁 Step 4: Analyzing Current Project..." -ForegroundColor Yellow

$projectFiles = @(
    "agent.py",
    "requirements.txt",
    "model_config.py",
    "examples/agent_with_tools.py",
    "examples/agent_with_memory.py",
    "examples/reasoning_agent.py"
)

$missingFiles = @()
foreach ($file in $projectFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing: $file" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "⚠️  Some expected files are missing. Continuing anyway..." -ForegroundColor Yellow
}

# Step 5: Create backup
Write-Host "`n💾 Step 5: Creating Backup..." -ForegroundColor Yellow

$backupDir = "agent-demo-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
try {
    Write-Host "📁 Creating backup (excluding .venv folder)..." -ForegroundColor Gray
    
    # Get all items except .venv folder
    $itemsToBackup = Get-ChildItem -Path "." | Where-Object { $_.Name -ne ".venv" }
    
    # Create backup directory
    New-Item -Path "../$backupDir" -ItemType Directory -Force | Out-Null
    
    # Copy items excluding .venv
    foreach ($item in $itemsToBackup) {
        Copy-Item -Path $item.FullName -Destination "../$backupDir" -Recurse -Force
    }
    
    Write-Host "✅ Backup created at: ../$backupDir (excluded .venv folder)" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to create backup: $($_.Exception.Message)" -ForegroundColor Red
    $continueAnyway = Read-Host "Continue without backup? (y/N)"
    if ($continueAnyway -ne "y" -and $continueAnyway -ne "Y") {
        exit 1
    }
}

# Step 6: Initialize SpecKit
Write-Host "`n🚀 Step 6: Initializing SpecKit..." -ForegroundColor Yellow

Write-Host "Initializing SpecKit in current directory with GitHub Copilot..."

try {
    if ($useUvx) {
        uvx --from git+https://github.com/github/spec-kit.git specify init --here --ai copilot --force
    } else {
        specify init --here --ai copilot --force
    }
    Write-Host "✅ SpecKit initialized successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to initialize SpecKit: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Trying without force flag..." -ForegroundColor Yellow
    
    try {
        if ($useUvx) {
            uvx --from git+https://github.com/github/spec-kit.git specify init --here --ai copilot
        } else {
            specify init --here --ai copilot
        }
        Write-Host "✅ SpecKit initialized successfully!" -ForegroundColor Green
    } catch {
        Write-Host "❌ SpecKit initialization failed completely." -ForegroundColor Red
        exit 1
    }
}

# Step 7: Verify SpecKit structure
Write-Host "`n🔍 Step 7: Verifying SpecKit Structure..." -ForegroundColor Yellow

$specKitDirs = @(".specify", "scripts", "specs")
foreach ($dir in $specKitDirs) {
    if (Test-Path $dir) {
        Write-Host "✅ Created: $dir/" -ForegroundColor Green
    } else {
        Write-Host "❌ Missing: $dir/" -ForegroundColor Red
    }
}

# Step 8: Show next steps
Write-Host "`n🎯 Step 8: Next Steps" -ForegroundColor Yellow
Write-Host "=" * 40

Write-Host "`n1. 📋 Create Project Constitution:" -ForegroundColor Cyan
Write-Host "   Open GitHub Copilot Chat and run:" -ForegroundColor White
Write-Host "   /speckit.constitution Create principles for AI agent development using Agno framework" -ForegroundColor Gray

Write-Host "`n2. 📝 Create Feature Specifications:" -ForegroundColor Cyan
Write-Host "   For your basic agent:" -ForegroundColor White
Write-Host "   /speckit.specify Build a conversational AI agent using the Agno framework" -ForegroundColor Gray

Write-Host "`n3. 🏗️  Generate Technical Plans:" -ForegroundColor Cyan
Write-Host "   After creating specs:" -ForegroundColor White
Write-Host "   /speckit.plan Use Agno framework with OpenAI/Azure OpenAI models and Python environment" -ForegroundColor Gray

Write-Host "`n4. 📋 Break Down into Tasks:" -ForegroundColor Cyan
Write-Host "   After creating plans:" -ForegroundColor White
Write-Host "   /speckit.tasks" -ForegroundColor Gray

Write-Host "`n5. 🚀 Implement Features:" -ForegroundColor Cyan
Write-Host "   Execute the generated implementation plans" -ForegroundColor White

Write-Host "`n📚 Documentation:" -ForegroundColor Yellow
Write-Host "   - Read: SPECKIT_IMPLEMENTATION_GUIDE.md" -ForegroundColor White
Write-Host "   - Check: .specify/ directory for configuration" -ForegroundColor White
Write-Host "   - Review: specs/ directory for generated specifications" -ForegroundColor White

Write-Host "`n✨ SpecKit setup complete! Happy coding! 🎉" -ForegroundColor Green