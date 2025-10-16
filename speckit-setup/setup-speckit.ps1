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

Write-Host "⚠️  Note: If you get GitHub API 403 errors, this is due to rate limiting." -ForegroundColor Yellow
Write-Host "   We'll try multiple installation methods..." -ForegroundColor Gray

$installSuccess = $false

# Method 1: Direct uv tool install
try {
    Write-Host "Method 1: Installing SpecKit CLI globally with uv tool..."
    uv tool install specify-cli --from git+https://github.com/github/spec-kit.git 2>$null
    # Test if it worked
    specify --help 2>$null | Out-Null
    Write-Host "✅ SpecKit CLI installed successfully via uv tool!" -ForegroundColor Green
    $installSuccess = $true
} catch {
    Write-Host "❌ Method 1 failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Method 2: Try with uvx if method 1 failed
if (-not $installSuccess) {
    try {
        Write-Host "Method 2: Trying installation with uvx..."
        uvx --from git+https://github.com/github/spec-kit.git specify --help 2>$null | Out-Null
        Write-Host "✅ SpecKit CLI available via uvx!" -ForegroundColor Green
        $script:useUvx = $true
        $installSuccess = $true
    } catch {
        Write-Host "❌ Method 2 failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Method 3: Manual installation guidance
if (-not $installSuccess) {
    Write-Host "`n❌ Automatic installation failed. This is likely due to:" -ForegroundColor Red
    Write-Host "   • GitHub API rate limiting (403 errors)" -ForegroundColor Yellow
    Write-Host "   • Network connectivity issues" -ForegroundColor Yellow
    Write-Host "   • Corporate firewall restrictions" -ForegroundColor Yellow
    
    Write-Host "`n🔧 Manual Installation Options:" -ForegroundColor Cyan
    Write-Host "   1. Wait a few minutes and try again (rate limit resets)" -ForegroundColor White
    Write-Host "   2. Use a GitHub token: set GITHUB_TOKEN environment variable" -ForegroundColor White
    Write-Host "   3. Try from a different network" -ForegroundColor White
    Write-Host "   4. Continue without SpecKit CLI (use uvx method)" -ForegroundColor White
    
    $continueChoice = Read-Host "`nContinue setup without CLI installation? (y/N)"
    if ($continueChoice -ne "y" -and $continueChoice -ne "Y") {
        Write-Host "`n💡 To retry with GitHub token:" -ForegroundColor Yellow
        Write-Host "   Set-Item -Path Env:GITHUB_TOKEN -Value 'your_token_here'" -ForegroundColor Gray
        Write-Host "   Then run this script again." -ForegroundColor Gray
        exit 1
    } else {
        Write-Host "⚠️  Continuing without CLI. You'll need to use uvx method:" -ForegroundColor Yellow
        Write-Host "   uvx --from git+https://github.com/github/spec-kit.git specify [command]" -ForegroundColor Gray
        $script:useUvx = $true
    }
}

# Step 3: Verify installation
Write-Host "`n✨ Step 3: Verifying Installation..." -ForegroundColor Yellow

if ($script:useUvx) {
    Write-Host "Using uvx method for SpecKit commands..." -ForegroundColor Gray
    try {
        uvx --from git+https://github.com/github/spec-kit.git specify --help 2>$null | Out-Null
        Write-Host "✅ SpecKit CLI verified via uvx!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  SpecKit verification via uvx failed. You may need to try manually later." -ForegroundColor Yellow
        Write-Host "   This could be due to continued GitHub API rate limiting." -ForegroundColor Gray
    }
} else {
    try {
        specify --help 2>$null | Out-Null
        Write-Host "✅ SpecKit CLI is working correctly!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  SpecKit CLI not found in PATH. Falling back to uvx method..." -ForegroundColor Yellow
        $script:useUvx = $true
        Write-Host "✅ Will use uvx method for SpecKit commands" -ForegroundColor Green
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
    if ($script:useUvx) {
        Write-Host "Using uvx method to initialize SpecKit..." -ForegroundColor Gray
        uvx --from git+https://github.com/github/spec-kit.git specify init --here --ai copilot --force
    } else {
        specify init --here --ai copilot --force
    }
    Write-Host "✅ SpecKit initialized successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to initialize SpecKit: $($_.Exception.Message)" -ForegroundColor Red
    
    # Check if it's a GitHub API issue
    if ($_.Exception.Message -like "*403*" -or $_.Exception.Message -like "*api.github.com*") {
        Write-Host "`n🔍 This appears to be a GitHub API rate limiting issue." -ForegroundColor Yellow
        Write-Host "   Options to resolve:" -ForegroundColor White
        Write-Host "   1. Wait 10-15 minutes and try again" -ForegroundColor Gray
        Write-Host "   2. Set up a GitHub personal access token" -ForegroundColor Gray
        Write-Host "   3. Try from a different network/IP address" -ForegroundColor Gray
        
        Write-Host "`n💡 To set up GitHub token:" -ForegroundColor Cyan
        Write-Host "   1. Go to https://github.com/settings/tokens" -ForegroundColor Gray
        Write-Host "   2. Generate a new token (classic) with 'repo' permissions" -ForegroundColor Gray
        Write-Host "   3. Set environment variable:" -ForegroundColor Gray
        Write-Host "      Set-Item -Path Env:GITHUB_TOKEN -Value 'your_token_here'" -ForegroundColor Gray
        Write-Host "   4. Run this script again" -ForegroundColor Gray
        
        $waitAndRetry = Read-Host "`nTry without --force flag? (y/N)"
        if ($waitAndRetry -eq "y" -or $waitAndRetry -eq "Y") {
            try {
                if ($script:useUvx) {
                    uvx --from git+https://github.com/github/spec-kit.git specify init --here --ai copilot
                } else {
                    specify init --here --ai copilot
                }
                Write-Host "✅ SpecKit initialized successfully!" -ForegroundColor Green
            } catch {
                Write-Host "❌ SpecKit initialization still failed. Please try manual setup later." -ForegroundColor Red
                Write-Host "   You can continue with the project setup and add SpecKit later." -ForegroundColor Yellow
            }
        } else {
            Write-Host "⚠️  Skipping SpecKit initialization. You can try manually later:" -ForegroundColor Yellow
            Write-Host "   uvx --from git+https://github.com/github/spec-kit.git specify init --here --ai copilot" -ForegroundColor Gray
        }
    } else {
        Write-Host "Trying without force flag..." -ForegroundColor Yellow
        try {
            if ($script:useUvx) {
                uvx --from git+https://github.com/github/spec-kit.git specify init --here --ai copilot
            } else {
                specify init --here --ai copilot
            }
            Write-Host "✅ SpecKit initialized successfully!" -ForegroundColor Green
        } catch {
            Write-Host "❌ SpecKit initialization failed completely." -ForegroundColor Red
            Write-Host "   This may be due to network issues or GitHub API limits." -ForegroundColor Yellow
        }
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

Write-Host "`n🔧 Troubleshooting GitHub API 403 Errors:" -ForegroundColor Yellow
Write-Host "   If you encountered GitHub API rate limiting (403 errors):" -ForegroundColor White
Write-Host "   • This is common when GitHub limits API requests per IP" -ForegroundColor Gray
Write-Host "   • Wait 10-15 minutes and try running the script again" -ForegroundColor Gray
Write-Host "   • Or set up a GitHub token for higher rate limits:" -ForegroundColor Gray
Write-Host "     1. Visit: https://github.com/settings/tokens" -ForegroundColor Gray
Write-Host "     2. Generate new token (classic) with 'repo' permissions" -ForegroundColor Gray
Write-Host "     3. Set token: Set-Item -Path Env:GITHUB_TOKEN -Value 'your_token'" -ForegroundColor Gray
Write-Host "     4. Re-run this script" -ForegroundColor Gray

Write-Host "`n🎯 Alternative Solutions:" -ForegroundColor Cyan
Write-Host "   Option 1 - Use uvx method:" -ForegroundColor White
Write-Host "     uvx --from git+https://github.com/github/spec-kit.git specify init --here --ai copilot" -ForegroundColor Gray
Write-Host "   Option 2 - Use manual setup (recommended for persistent API issues):" -ForegroundColor White  
Write-Host "     .\speckit-setup\manual-setup.ps1" -ForegroundColor Gray

Write-Host "`n💡 The manual setup creates the same structure and works with GitHub Copilot Chat!" -ForegroundColor Yellow

Write-Host "`n✨ SpecKit setup complete! Happy coding! 🎉" -ForegroundColor Green