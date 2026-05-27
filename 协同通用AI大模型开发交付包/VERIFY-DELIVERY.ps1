param(
    [switch]$Strict
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Failures = New-Object System.Collections.Generic.List[string]
$Warnings = New-Object System.Collections.Generic.List[string]

function Add-Failure {
    param([string]$Message)
    $Failures.Add($Message) | Out-Null
}

function Add-Warning {
    param([string]$Message)
    $Warnings.Add($Message) | Out-Null
}

function Get-RelativePath {
    param([string]$Path)
    $full = [System.IO.Path]::GetFullPath($Path)
    $base = [System.IO.Path]::GetFullPath($Root)
    if (-not $base.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $base += [System.IO.Path]::DirectorySeparatorChar
    }
    if ($full.StartsWith($base, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $full.Substring($base.Length)
    }
    return $full
}

function Test-RequiredPath {
    param([string]$RelativePath)
    $path = Join-Path $Root $RelativePath
    if (-not (Test-Path -LiteralPath $path)) {
        Add-Failure "Missing required path: $RelativePath"
    }
}

function Get-DirectoryByPrefix {
    param([string]$Prefix)
    return Get-ChildItem -LiteralPath $Root -Directory -Force |
        Where-Object { $_.Name.StartsWith($Prefix, [System.StringComparison]::Ordinal) } |
        Select-Object -First 1
}

Write-Host "== User delivery package verification =="
Write-Host "Root: $Root"
if ($Strict) {
    Write-Host "Mode: strict final-delivery checks"
} else {
    Write-Host "Mode: template/base checks"
}

Test-RequiredPath "README.md"

$rootMarkdown = Get-ChildItem -LiteralPath $Root -File -Force -Filter "*.md" |
    Where-Object { $_.Name -ne "README.md" }
if ($rootMarkdown.Count -lt 1) {
    Add-Failure "Missing a root assembly/rules Markdown file beside README.md."
}

foreach ($prefix in @("01-", "02-", "03-", "04-")) {
    $dir = Get-DirectoryByPrefix $prefix
    if ($null -eq $dir) {
        Add-Failure "Missing required system directory with prefix: $prefix"
        continue
    }

    $readme = Join-Path $dir.FullName "README.md"
    if (-not (Test-Path -LiteralPath $readme)) {
        Add-Failure "Missing README.md in required system directory: $($dir.Name)"
    }
}

$strictPaths = @(
    "AI_PROJECT_CONTEXT.md",
    "HANDOFF.md",
    "CHANGELOG.md",
    "TRACEABILITY-MATRIX.md",
    "VALIDATION_REPORT.md"
)

foreach ($item in $strictPaths) {
    $path = Join-Path $Root $item
    if (-not (Test-Path -LiteralPath $path)) {
        if ($Strict) {
            Add-Failure "Strict mode requires project artifact: $item"
        } else {
            Add-Warning "Project artifact not found yet: $item"
        }
    }
}

$excludedDirectoryPattern = "\\(\.git|__pycache__|\.pytest_cache|\.ruff_cache|node_modules|dist|build|coverage)(\\|$)"
$textExtensions = @(
    ".md", ".txt", ".ps1", ".py", ".js", ".ts", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".html", ".css", ".example"
)

$files = Get-ChildItem -LiteralPath $Root -Recurse -File -Force |
    Where-Object { $_.FullName -notmatch $excludedDirectoryPattern }

$markdownFiles = $files | Where-Object { $_.Extension -eq ".md" }
foreach ($file in $markdownFiles) {
    $text = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    $fenceCount = ([regex]::Matches($text, '```')).Count
    if (($fenceCount % 2) -ne 0) {
        Add-Failure "Unbalanced Markdown code fences: $(Get-RelativePath $file.FullName) ($fenceCount fences)"
    }
}

$localPathPatterns = @(
    "[A-Za-z]:[\\/]",
    "/Users/[^/\s]+/",
    "/home/[^/\s]+/"
)

$secretPatterns = @(
    "(?i)api[_-]?key\s*[:=]\s*['""]?[A-Za-z0-9_\-]{16,}",
    "(?i)secret\s*[:=]\s*['""]?[A-Za-z0-9_\-]{16,}",
    "(?i)token\s*[:=]\s*['""]?[A-Za-z0-9_\-]{20,}",
    "sk-[A-Za-z0-9]{20,}",
    "AKIA[0-9A-Z]{16}",
    "-----BEGIN [A-Z ]*PRIVATE KEY-----"
)

$placeholderPatterns = @(
    "\[TODO\]",
    "<project-name>",
    "<project_name>",
    "<TODO>",
    "TODO:"
)

$fillMarker = ([string][char]0x586B) + ([string][char]0x5199)
$pendingMarker = ([string][char]0x5F85) + ([string][char]0x586B) + ([string][char]0x5199)
$placeholderPatterns += @(
    "<[^>]*$fillMarker[^>]*>",
    "<[^>]*$pendingMarker[^>]*>"
)

function New-UString {
    param([int[]]$CodePoints)
    return (-join ($CodePoints | ForEach-Object { [string][char]$_ }))
}

$placeholderWhitelist = @(
    "<" + (New-UString @(0x7528,0x6237,0x4EA4,0x4ED8,0x5305,0x6839,0x76EE,0x5F55)) + ">",
    "<" + (New-UString @(0x6BCD,0x4EA4,0x4ED8,0x5305,0x6839,0x76EE,0x5F55)) + ">",
    "<" + (New-UString @(0x9879,0x76EE,0x6839,0x76EE,0x5F55)) + ">",
    "<" + (New-UString @(0x5B50,0x7CFB,0x7EDF,0x6839,0x76EE,0x5F55)) + ">"
)

$strictSystemPlaceholderPatterns = @(
    "<[^>`r`n]+>"
)

foreach ($file in $files) {
    if ($file.FullName -eq $MyInvocation.MyCommand.Path) {
        continue
    }

    if ($file.Length -gt 5MB) {
        continue
    }

    $isTextCandidate = $textExtensions -contains $file.Extension
    if ($file.Name -like ".env*" -or $file.Name -eq "Dockerfile" -or $file.Extension -eq "") {
        $isTextCandidate = $true
    }
    if (-not $isTextCandidate) {
        continue
    }

    try {
        $text = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    } catch {
        Add-Warning "Skipped unreadable text scan: $(Get-RelativePath $file.FullName)"
        continue
    }

    foreach ($pattern in $localPathPatterns) {
        if ($text -match $pattern) {
            Add-Failure "Possible local absolute path leak in $(Get-RelativePath $file.FullName): pattern $pattern"
            break
        }
    }

    foreach ($pattern in $secretPatterns) {
        if ($text -match $pattern) {
            Add-Failure "Possible secret or token leak in $(Get-RelativePath $file.FullName)"
            break
        }
    }

    $placeholderScanText = $text
    foreach ($token in $placeholderWhitelist) {
        $placeholderScanText = $placeholderScanText.Replace($token, "")
    }

    $relativePath = Get-RelativePath $file.FullName
    $activePlaceholderPatterns = $placeholderPatterns
    if ($Strict -and ($relativePath -match "^(01-|02-|03-|04-)")) {
        $activePlaceholderPatterns = $placeholderPatterns + $strictSystemPlaceholderPatterns
    }

    foreach ($pattern in $activePlaceholderPatterns) {
        if ($placeholderScanText -match $pattern) {
            if ($Strict) {
                Add-Failure "Strict mode placeholder remains in $(Get-RelativePath $file.FullName): pattern $pattern"
            } else {
                Add-Warning "Template placeholder remains in $(Get-RelativePath $file.FullName): pattern $pattern"
            }
            break
        }
    }
}

$projectVerifyCandidates = @(
    "scripts\verify.ps1",
    "scripts\verify.py",
    "tests",
    "pytest.ini",
    "package.json",
    "pyproject.toml"
)

$hasProjectVerify = $false
foreach ($item in $projectVerifyCandidates) {
    if (Test-Path -LiteralPath (Join-Path $Root $item)) {
        $hasProjectVerify = $true
        break
    }
}

if (-not $hasProjectVerify) {
    if ($Strict) {
        Add-Failure "Strict mode requires a project-specific verification entry, such as scripts\verify.ps1, tests, package.json, or pyproject.toml."
    } else {
        Add-Warning "No project-specific verification entry detected yet; expected for the template skeleton."
    }
}

Write-Host ""
Write-Host "Files scanned: $($files.Count)"
Write-Host "Markdown files checked: $($markdownFiles.Count)"
Write-Host "Warnings: $($Warnings.Count)"
Write-Host "Failures: $($Failures.Count)"

if ($Warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "Warnings:"
    foreach ($warning in $Warnings) {
        Write-Host "  - $warning"
    }
}

if ($Failures.Count -gt 0) {
    Write-Host ""
    Write-Host "Failures:"
    foreach ($failure in $Failures) {
        Write-Host "  - $failure"
    }
    exit 1
}

Write-Host ""
Write-Host "PASS: delivery package base verification completed."
exit 0
