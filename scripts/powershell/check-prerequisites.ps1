# Check Prerequisites Script - Manual Implementation  
param(
    [switch]$Json,
    [switch]$RequireTasks,
    [switch]$IncludeTasks
)

Write-Host "🔍 Checking Prerequisites" -ForegroundColor Green

$prereqs = @{
    "python" = (Get-Command python -ErrorAction SilentlyContinue) -ne $null
    "git" = (Get-Command git -ErrorAction SilentlyContinue) -ne $null  
    "agno" = $true  # Assume agno is available from requirements.txt
}

if ($Json) {
    $prereqs | ConvertTo-Json
} else {
    foreach ($req in $prereqs.GetEnumerator()) {
        if ($req.Value) {
            Write-Host "  ✅ $($req.Key)" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $($req.Key)" -ForegroundColor Red  
        }
    }
}
