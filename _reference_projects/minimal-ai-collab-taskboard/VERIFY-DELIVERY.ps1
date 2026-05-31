$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$required = @(
    "README.md",
    "AI_PROJECT_CONTEXT.md",
    "HANDOFF.md",
    "CHANGELOG.md",
    "TRACEABILITY-MATRIX.md",
    "VALIDATION_REPORT.md",
    "docs\PRD.md",
    "docs\SPEC.md",
    "tasks\TASKS.md",
    "tests\TEST_PLAN.md",
    "tests\test_smoke.py",
    "src\ai_collab_taskboard\taskboard.py"
)

foreach ($path in $required) {
    if (-not (Test-Path -LiteralPath (Join-Path $Root $path))) {
        throw "Missing required reference-project file: $path"
    }
}

python tests/test_smoke.py
if ($LASTEXITCODE -ne 0) {
    throw "Reference project smoke failed."
}

Write-Host "REFERENCE_PROJECT_VERIFY=PASS"
