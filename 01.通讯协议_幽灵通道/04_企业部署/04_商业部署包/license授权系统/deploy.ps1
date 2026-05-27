#===============================================================================
# Ghost Channel License Server - Deployment Script (Windows)
# 幽灵通道授权服务器 - 部署脚本 (Windows PowerShell)
#
# 使用方法:
#   .\deploy.ps1 [-Environment] <string> [-Action] <string>
#
# 示例:
#   .\deploy.ps1 -Environment local -Action start
#   .\deploy.ps1 -Environment production -Action deploy
#
# 环境变量:
#   $env:SECRET_KEY          - 服务器密钥 (必填)
#   $env:REDIS_PASSWORD      - Redis密码 (可选)
#
#===============================================================================

param(
    [Parameter(Position=0)]
    [ValidateSet("local", "staging", "production", "k8s")]
    [string]$Environment = "local",
    
    [Parameter(Position=1)]
    [ValidateSet("start", "stop", "restart", "logs", "status", "deploy", "clean", "help")]
    [string]$Action = "help"
)

# 颜色 (使用Write-Host实现)
$script:ProjectRoot = Split-Path -Parent $PSScriptRoot
$script:DockerDir = Join-Path $script:ProjectRoot "docker"
$script:EnvFile = Join-Path $script:DockerDir ".env"

function Write-Info { param([string]$msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Success { param([string]$msg) Write-Host "[SUCCESS] $msg" -ForegroundColor Green }
function Write-Warning { param([string]$msg) Write-Host "[WARNING] $msg" -ForegroundColor Yellow }
function Write-Error { param([string]$msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

function Print-Header {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host " Ghost Channel License Server Deploy" -ForegroundColor Magenta
    Write-Host "========================================" -ForegroundColor Magenta
    Write-Host ""
}

function Print-Help {
    Print-Header
    Write-Host "用法: .\deploy.ps1 [-Environment] <环境> [-Action] <操作>`n"
    Write-Host "环境:" -ForegroundColor White
    Write-Host "  local       - 本地Docker部署"
    Write-Host "  staging     - 预发布环境"
    Write-Host "  production  - 生产环境"
    Write-Host "  k8s         - Kubernetes部署`n"
    Write-Host "操作:" -ForegroundColor White
    Write-Host "  start       - 启动服务"
    Write-Host "  stop        - 停止服务"
    Write-Host "  restart     - 重启服务"
    Write-Host "  logs        - 查看日志 (tail 100行)"
    Write-Host "  status      - 查看状态"
    Write-Host "  deploy      - 完整部署"
    Write-Host "  clean       - 清理资源`n"
    Write-Host "必需环境变量:" -ForegroundColor White
    Write-Host "  `$env:SECRET_KEY    - 服务器密钥"
    Write-Host "  `$env:DOMAIN        - 域名 (生产环境)`n"
    Write-Host "示例:" -ForegroundColor White
    Write-Host '  $env:SECRET_KEY="mysecret"; .\deploy.ps1 local start'
    Write-Host '  $env:SECRET_KEY="xxx"; .\deploy.ps1 production deploy'
}

function Test-EnvironmentFile {
    if (-not (Test-Path $script:EnvFile)) {
        Write-Warning "环境配置文件不存在，创建默认配置..."
        New-EnvironmentFile
    }
}

function New-EnvironmentFile {
    $content = @"
# Ghost Channel License Server - Environment Configuration
# ======================================================

# 必填配置
SECRET_KEY=CHANGE_ME_IN_PRODUCTION

# 服务器配置
APP_ENV=production
SERVER_PORT=8001
LOG_LEVEL=INFO

# Redis配置 (可选)
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

# CORS配置
CORS_ORIGINS=*

# 域名 (生产环境)
DOMAIN=license.ghost-channel.io
"@
    Set-Content -Path $script:EnvFile -Value $content
    Write-Info "已创建环境配置文件: $($script:EnvFile)"
}

function Load-EnvironmentFile {
    if (Test-Path $script:EnvFile) {
        Get-Content $script:EnvFile | ForEach-Object {
            if ($_ -match '^[A-Z_]+=' -and $_ -notmatch '^#') {
                $key, $value = $_.Split('=', 2)
                Set-Item -Path "env:$key" -Value $value -Force
            }
        }
        Write-Info "已加载环境配置"
    }
}

function Validate-Environment {
    if (-not $env:SECRET_KEY) {
        Write-Error "SECRET_KEY未设置"
        Write-Host ""
        Write-Host '请设置 $env:SECRET_KEY:' -ForegroundColor White
        Write-Host '  $env:SECRET_KEY = "your_strong_secret_key"'
        Write-Host '  或者编辑 $($script:EnvFile)'
        exit 1
    }
    
    if ($env:SECRET_KEY -eq "CHANGE_ME_IN_PRODUCTION") {
        Write-Warning "使用默认SECRET_KEY，生产环境请修改"
    }
}

function Test-Docker {
    try {
        $null = docker info 2>&1
        return $true
    }
    catch {
        Write-Error "Docker未安装或未运行"
        return $false
    }
}

function Docker-Start {
    Write-Info "启动Docker服务..."
    Set-Location $script:DockerDir
    docker-compose up -d
    Write-Success "服务已启动"
    Docker-Status
}

function Docker-Stop {
    Write-Info "停止Docker服务..."
    Set-Location $script:DockerDir
    docker-compose down
    Write-Success "服务已停止"
}

function Docker-Restart {
    Write-Info "重启Docker服务..."
    Set-Location $script:DockerDir
    docker-compose restart
    Write-Success "服务已重启"
}

function Docker-Status {
    Set-Location $script:DockerDir
    docker-compose ps
}

function Docker-Logs {
    Set-Location $script:DockerDir
    docker-compose logs -f --tail=100
}

function Docker-Clean {
    Write-Warning "清理Docker资源..."
    Set-Location $script:DockerDir
    docker-compose down -v --remove-orphans
    docker image prune -f
    Write-Success "清理完成"
}

function Deploy-Production {
    Print-Header
    Write-Info "开始生产部署..."

    if (-not $env:SECRET_KEY) {
        Write-Error "生产部署需要设置 SECRET_KEY"
        exit 1
    }

    # 构建镜像
    Write-Info "构建Docker镜像..."
    Set-Location $script:DockerDir
    docker build -t ghost-license-server:1.0.0 ..
    docker tag ghost-license-server:1.0.0 ghcr.io/q-spectrum/ghost-license-server:1.0.0

    # 启动服务
    Write-Info "启动服务..."
    docker-compose up -d

    # 等待服务就绪
    Write-Info "等待服务就绪..."
    Start-Sleep -Seconds 10

    # 检查健康状态
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8001/" -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Success "服务部署成功!"
        }
    }
    catch {
        Write-Error "服务健康检查失败"
        docker-compose logs
        exit 1
    }

    Docker-Status
}

#===============================================================================
# 主程序
#===============================================================================

Print-Header
Write-Info "环境: $Environment"
Write-Info "操作: $Action"
Write-Host ""

switch ($Action) {
    "start" {
        Test-EnvironmentFile
        Load-EnvironmentFile
        Validate-Environment
        if (Test-Docker) { Docker-Start }
    }
    "stop" {
        if (Test-Docker) { Docker-Stop }
    }
    "restart" {
        Test-EnvironmentFile
        Load-EnvironmentFile
        if (Test-Docker) { Docker-Restart }
    }
    "logs" {
        if (Test-Docker) { Docker-Logs }
    }
    "status" {
        if (Test-Docker) { Docker-Status }
    }
    "deploy" {
        Test-EnvironmentFile
        Load-EnvironmentFile
        Validate-Environment
        if (Test-Docker) { Deploy-Production }
    }
    "clean" {
        if (Test-Docker) { Docker-Clean }
    }
    "help" {
        Print-Help
    }
}
