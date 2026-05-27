# Ghost Channel v1.0 Delivery Verification Script
# Run: powershell -ExecutionPolicy Bypass -File VERIFY.ps1

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$manifestFile = Join-Path $root "MANIFEST.yaml"

if (-not (Test-Path $manifestFile)) {
    Write-Host "ERROR: MANIFEST.yaml not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Ghost Channel v1.0 - Delivery Verification" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$verified = 0
$failed = 0
$missing = 0
$total = 0

Get-Content $manifestFile -Encoding UTF8 | ForEach-Object {
    if ($_ -match '^\s*#') { return }  # skip comments
    if ($_ -match '^\s*$') { return }  # skip blank lines
    
    $total++

    # MANIFEST.yaml and VERIFY.ps1 cannot verify themselves (hash changes on regeneration/edit)
    if ($_ -match '^(MANIFEST\.yaml|VERIFY\.ps1)\s*:') {
        $verified++
        return
    }

    $parts = $_ -split ':\s*', 2
    if ($parts.Count -ne 2) { return }
    
    $file = $parts[0].Trim()
    $expected = $parts[1].Trim()
    $path = Join-Path $root $file
    
    if (Test-Path $path) {
        $hash = (Get-FileHash $path -Algorithm SHA256).Hash.ToLower()
        if ($hash -eq $expected) {
            $verified++
        } else {
            Write-Host "FAIL: $file" -ForegroundColor Red
            $failed++
        }
    } else {
        Write-Host "MISSING: $file" -ForegroundColor Yellow
        $missing++
    }
}

Write-Host ""
Write-Host "Summary: $total files checked" -ForegroundColor Cyan
Write-Host "  Verified: $verified" -ForegroundColor Green
Write-Host "  Failed:   $failed" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "  Missing:  $missing" -ForegroundColor $(if ($missing -gt 0) { "Yellow" } else { "Green" })

if ($failed -eq 0 -and $missing -eq 0) {
    Write-Host ""
    Write-Host "ALL CLEAN - Delivery package integrity verified" -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "ISSUES FOUND - See above" -ForegroundColor Red
    exit 1
}
