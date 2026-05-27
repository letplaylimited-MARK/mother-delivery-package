#!/bin/bash
#===============================================================================
# Ghost Channel License Server - Deployment Script
# 幽灵通道授权服务器 - 部署脚本
#
# 使用方法:
#   ./deploy.sh [environment] [action]
#
# 示例:
#   ./deploy.sh local start
#   ./deploy.sh production deploy
#   ./deploy.sh production logs
#
# 环境变量 (必须在部署前设置):
#   SECRET_KEY          - 服务器密钥 (必填)
#   REDIS_PASSWORD      - Redis密码 (可选)
#
#===============================================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCKER_DIR="$PROJECT_ROOT/docker"
ENV_FILE="$DOCKER_DIR/.env"

# 默认值
DEFAULT_ENV="local"
DEFAULT_ACTION="help"

#-------------------------------------------------------------------------------
# 辅助函数
#-------------------------------------------------------------------------------

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "========================================"
    echo " Ghost Channel License Server Deploy"
    echo "========================================"
}

print_help() {
    print_header
    echo "用法: ./deploy.sh [环境] [操作]"
    echo ""
    echo "环境:"
    echo "  local       - 本地Docker部署"
    echo "  staging     - 预发布环境"
    echo "  production  - 生产环境"
    echo ""
    echo "操作:"
    echo "  start       - 启动服务"
    echo "  stop        - 停止服务"
    echo "  restart     - 重启服务"
    echo "  logs        - 查看日志"
    echo "  status      - 查看状态"
    echo "  deploy      - 完整部署 (包含构建)"
    echo "  clean       - 清理资源"
    echo "  help        - 显示帮助"
    echo ""
    echo "必需环境变量:"
    echo "  SECRET_KEY           - 服务器密钥"
    echo "  DOMAIN               - 域名 (生产环境)"
    echo ""
    echo "示例:"
    echo "  SECRET_KEY=mysecret ./deploy.sh local start"
    echo "  SECRET_KEY=xxx DOMAIN=license.example.com ./deploy.sh production deploy"
}

#-------------------------------------------------------------------------------
# 检查函数
#-------------------------------------------------------------------------------

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装"
        exit 1
    fi
    if ! docker info &> /dev/null; then
        log_error "Docker未运行"
        exit 1
    fi
}

check_env_file() {
    if [ ! -f "$ENV_FILE" ]; then
        log_warning "环境配置文件不存在，创建默认配置..."
        create_env_file
    fi
}

create_env_file() {
    cat > "$ENV_FILE" << 'EOF'
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

# SSL配置
# SSL_ENABLED=true
# SSL_CERT_PATH=/path/to/cert.pem
# SSL_KEY_PATH=/path/to/key.pem
EOF
    log_info "已创建环境配置文件: $ENV_FILE"
}

load_env_file() {
    if [ -f "$ENV_FILE" ]; then
        export $(grep -v '^#' "$ENV_FILE" | xargs)
        log_info "已加载环境配置"
    fi
}

validate_env() {
    if [ -z "$SECRET_KEY" ]; then
        log_error "SECRET_KEY未设置"
        echo ""
        echo "请设置 SECRET_KEY:"
        echo "  export SECRET_KEY=your_strong_secret_key"
        echo "  或者编辑 $ENV_FILE"
        exit 1
    fi

    if [ "$SECRET_KEY" = "CHANGE_ME_IN_PRODUCTION" ]; then
        log_warning "使用默认SECRET_KEY，生产环境请修改"
    fi
}

#-------------------------------------------------------------------------------
# Docker操作
#-------------------------------------------------------------------------------

docker_start() {
    log_info "启动Docker服务..."
    cd "$DOCKER_DIR"
    docker-compose up -d
    log_success "服务已启动"
    docker_status
}

docker_stop() {
    log_info "停止Docker服务..."
    cd "$DOCKER_DIR"
    docker-compose down
    log_success "服务已停止"
}

docker_restart() {
    log_info "重启Docker服务..."
    cd "$DOCKER_DIR"
    docker-compose restart
    log_success "服务已重启"
}

docker_status() {
    cd "$DOCKER_DIR"
    docker-compose ps
}

docker_logs() {
    cd "$DOCKER_DIR"
    if [ "$#" -gt 0 ]; then
        docker-compose logs -f --tail="$1"
    else
        docker-compose logs -f --tail=100
    fi
}

docker_clean() {
    log_warning "清理Docker资源..."
    cd "$DOCKER_DIR"
    docker-compose down -v --remove-orphans
    docker image prune -f
    log_success "清理完成"
}

#-------------------------------------------------------------------------------
# 生产部署
#-------------------------------------------------------------------------------

deploy_production() {
    print_header
    log_info "开始生产部署..."

    # 检查环境变量
    if [ -z "$SECRET_KEY" ]; then
        log_error "生产部署需要设置 SECRET_KEY"
        exit 1
    fi

    # 构建镜像
    log_info "构建Docker镜像..."
    cd "$DOCKER_DIR"
    docker build -t ghost-license-server:1.0.0 ..
    docker tag ghost-license-server:1.0.0 ghcr.io/q-spectrum/ghost-license-server:1.0.0

    # 启动服务
    log_info "启动服务..."
    docker-compose -f docker-compose.yml up -d

    # 等待服务就绪
    log_info "等待服务就绪..."
    sleep 10

    # 检查健康状态
    if curl -sf http://localhost:8001/ > /dev/null; then
        log_success "服务部署成功!"
    else
        log_error "服务健康检查失败"
        docker-compose logs
        exit 1
    fi

    docker_status
}

#-------------------------------------------------------------------------------
# 本地开发
#-------------------------------------------------------------------------------

dev_start() {
    log_info "启动开发环境..."
    cd "$PROJECT_ROOT/license_server"
    pip install -r requirements.txt
    SECRET_KEY=dev_secret python server.py
}

#-------------------------------------------------------------------------------
# K8s部署
#-------------------------------------------------------------------------------

k8s_deploy() {
    log_info "Kubernetes部署..."

    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl未安装"
        exit 1
    fi

    # 应用配置
    log_info "应用Kubernetes配置..."
    kubectl apply -f "$DOCKER_DIR/k8s/deployment.yaml"

    # 检查部署状态
    log_info "检查部署状态..."
    kubectl rollout status deployment/ghost-license-server -n ghost-license

    log_success "Kubernetes部署完成"
}

#-------------------------------------------------------------------------------
# 主程序
#-------------------------------------------------------------------------------

main() {
    local env="${1:-$DEFAULT_ENV}"
    local action="${2:-$DEFAULT_ACTION}"

    print_header
    log_info "环境: $env"
    log_info "操作: $action"
    echo ""

    case "$action" in
        start)
            load_env_file
            validate_env
            check_docker
            docker_start
            ;;
        stop)
            check_docker
            docker_stop
            ;;
        restart)
            load_env_file
            check_docker
            docker_restart
            ;;
        logs)
            check_docker
            docker_logs "${@:3}"
            ;;
        status)
            check_docker
            docker_status
            ;;
        deploy)
            case "$env" in
                production)
                    deploy_production
                    ;;
                staging)
                    deploy_production
                    ;;
                local)
                    load_env_file
                    validate_env
                    check_docker
                    docker_start
                    ;;
                k8s)
                    k8s_deploy
                    ;;
                *)
                    log_error "未知环境: $env"
                    print_help
                    exit 1
                    ;;
            esac
            ;;
        clean)
            check_docker
            docker_clean
            ;;
        help|--help|-h)
            print_help
            ;;
        *)
            log_error "未知操作: $action"
            print_help
            exit 1
            ;;
    esac
}

# 运行
main "$@"
