param(
    [switch]$Full,
    [switch]$SkipRoot
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Python = "python"
$SelfBootstrapProbe = "self-bootstrap mother package project improve mother-delivery-package itself and feed the result back to the repo"
$NewProjectProbe = "project start init new project from idea to requirements spec tasks tests delivery"
$UserPackName = -join ([char[]](0x534F, 0x540C, 0x901A, 0x7528, 0x0041, 0x0049, 0x5927, 0x6A21, 0x578B, 0x5F00, 0x53D1, 0x4EA4, 0x4ED8, 0x5305))
$UserPackPath = Join-Path $Root $UserPackName

function Invoke-Step {
    param(
        [string]$Name,
        [scriptblock]$Body
    )

    Write-Host ""
    Write-Host "== $Name =="
    $started = Get-Date
    $global:LASTEXITCODE = 0
    & $Body
    if ($global:LASTEXITCODE -ne $null -and $global:LASTEXITCODE -ne 0) {
        throw "Step failed: $Name (exit=$global:LASTEXITCODE)"
    }
    $elapsed = [math]::Round(((Get-Date) - $started).TotalSeconds, 2)
    Write-Host ("PASS: {0} ({1}s)" -f $Name, $elapsed)
}

Invoke-Step "root anchors" {
    foreach ($path in @(
        "MISSION-MEMORY.md",
        "MOTHER-PACK-ACTIVATION-GUIDE.md",
        "AI_PROJECT_CONTEXT.md",
        "qa_runner.py",
        "qcm-universal-ai-system-v3.0.skill"
    )) {
        if (-not (Test-Path -LiteralPath (Join-Path $Root $path))) {
            throw "Missing root anchor: $path"
        }
    }
}

Invoke-Step "git and submodules" {
    git status --short --branch
    git submodule status
    git submodule status | ForEach-Object {
        if ($_ -match "^-") {
            throw "Submodule is not initialized: $_"
        }
    }
}

Invoke-Step "route probe: self bootstrap" {
    & $Python qa_runner.py route $SelfBootstrapProbe
}

Invoke-Step "route probe: new project golden path" {
    & $Python qa_runner.py route $NewProjectProbe
}

Invoke-Step "consistency" {
    & $Python qa_runner.py consistency
}

Invoke-Step "P00 audit assets" {
    & $Python qa_runner.py validate --scope P00_SUPER_PROMPT
}

if (-not $SkipRoot) {
    Invoke-Step "ROOT validation" {
        & $Python qa_runner.py validate --scope ROOT
    }
}

Invoke-Step "reference project smoke" {
    & $Python "_reference_projects/minimal-ai-collab-taskboard/tests/test_smoke.py"
}

Invoke-Step "USER_PACK strict" {
    $psCommand = Get-Command pwsh -ErrorAction SilentlyContinue
    if ($null -eq $psCommand) {
        $psCommand = Get-Command powershell -ErrorAction SilentlyContinue
    }
    if ($null -eq $psCommand) {
        throw "PowerShell executable not found."
    }
    Push-Location $UserPackPath
    try {
        if ($psCommand.Name -like "powershell*") {
            & $psCommand.Source -ExecutionPolicy Bypass -File ".\VERIFY-DELIVERY.ps1" -Strict
        } else {
            & $psCommand.Source -NoProfile -File ".\VERIFY-DELIVERY.ps1" -Strict
        }
    } finally {
        Pop-Location
    }
}

if ($Full) {
    Invoke-Step "full validation registry" {
        & $Python qa_runner.py validate
    }
}

Write-Host ""
Write-Host "MOTHER_PACK_VERIFY=PASS"
