# Ghost Channel v1.0 Delivery Verification Script
# Run: powershell -ExecutionPolicy Bypass -File VERIFY.ps1
#
# Cross-platform: tries both raw and LF-normalized hashes for text files,
# so verification passes on Windows (autocrlf), Linux, and macOS.

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

# Text file extensions that may have CRLF/LF differences
$textExtensions = @('.md','.py','.yaml','.yml','.json','.html','.css','.js','.ts','.sh','.ps1','.bat','.txt','.toml')

function Get-NormalizedHash($path) {
    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $normalized = $content -replace "`r`n", "`n"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($normalized)
    $stream = New-Object System.IO.MemoryStream(,$bytes)
    $hash = (Get-FileHash -InputStream $stream -Algorithm SHA256).Hash.ToLower()
    $stream.Close()
    return $hash
}

Get-Content $manifestFile -Encoding UTF8 | ForEach-Object {
    if ($_ -match '^\s*#') { return }
    if ($_ -match '^\s*$') { return }
    
    $total++

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
        $ext = [System.IO.Path]::GetExtension($file).ToLower()
        $hash = $null
        $hashNorm = $null
        
        if ($textExtensions -contains $ext) {
            # Try both raw and normalized hashes for text files
            $hash = (Get-FileHash $path -Algorithm SHA256).Hash.ToLower()
            $hashNorm = Get-NormalizedHash $path
        } else {
            $hash = (Get-FileHash $path -Algorithm SHA256).Hash.ToLower()
        }
        
        if ($hash -eq $expected -or $hashNorm -eq $expected) {
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
