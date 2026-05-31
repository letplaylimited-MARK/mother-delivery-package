# verify.ps1 - Template-level verification wrapper.
# Concrete final projects should extend or replace this file with real smoke/tests.
# This skeleton delegates to the main VERIFY-DELIVERY.ps1 script with -Strict mode.
$ErrorActionPreference = "Stop"
$mainScript = Join-Path $PSScriptRoot "..\VERIFY-DELIVERY.ps1"
if (-not (Test-Path $mainScript)) {
    Write-Error "Main verification script not found: $mainScript"
    exit 1
}
& $mainScript -Strict
