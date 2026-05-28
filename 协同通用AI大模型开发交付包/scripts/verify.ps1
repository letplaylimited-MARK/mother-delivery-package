# verify.ps1 — Project-level Verification Script
# Calls the main delivery verification script
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$DeliveryScript = Join-Path (Split-Path -Parent $Root) "协同通用AI大模型开发交付包\VERIFY-DELIVERY.ps1"
if (Test-Path $DeliveryScript) {
    & $DeliveryScript -Strict
} else {
    & (Join-Path $PSScriptRoot "..\VERIFY-DELIVERY.ps1") -Strict
}
