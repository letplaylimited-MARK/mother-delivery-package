# verify.ps1 - Thin wrapper for project-level verification
# Delegates to the main VERIFY-DELIVERY.ps1 script with -Strict mode
$ErrorActionPreference = "Stop"
$mainScript = Join-Path $PSScriptRoot "..\VERIFY-DELIVERY.ps1"
if (-not (Test-Path $mainScript)) {
    Write-Error "Main verification script not found: $mainScript"
    exit 1
}
& $mainScript -Strict
