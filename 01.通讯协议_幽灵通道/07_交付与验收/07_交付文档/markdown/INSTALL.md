# Ghost Hub 安装指南

## 系统要求

| 组件 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Docker | 20.10+ | 24.0+ |
| Docker Compose | 2.0+ | 2.20+ |
| Python (SDK) | 3.8+ | 3.11+ |
| Node.js (SDK) | 16+ | 20 LTS |

## 安装方式

### 方式一：Docker 部署（推荐）

```bash
# 克隆项目
git clone https://github.com/ghost-hub/protocol.git
cd protocol

# 启动服务
docker-compose up -d

# 验证服务
curl http://localhost:8080/v1/health
```

### 方式二：手动部署

#### 1. 安装 Redis

```bash
# macOS
brew install redis
redis-server

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# Docker
docker run -d --name ghost-hub-redis -p 6379:6379 redis:7-alpine
```

#### 2. 安装 Ghost Hub 服务

```bash
# 下载最新版本
wget https://github.com/ghost-hub/protocol/releases/latest/ghost-hub-linux-amd64
chmod +x ghost-hub-linux-amd64

# 运行服务
./ghost-hub-linux-amd64 --port 8080 --redis-url redis://localhost:6379
```

## 环境变量

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `GHOST_HUB_PORT` | 8080 | HTTP 服务端口 |
| `GHOST_HUB_REDIS_URL` | redis://localhost:6379 | Redis 连接地址 |
| `GHOST_HUB_API_KEY` | - | API 认证密钥 |
| `GHOST_HUB_LOG_LEVEL` | info | 日志级别 |

## 验证安装

```bash
# 健康检查
curl http://localhost:8080/v1/health

# 预期响应
{"status": "healthy", "version": "1.0.0"}
```

## 卸载

```bash
# Docker 方式
docker-compose down -v

# 手动方式
pkill ghost-hub
rm /usr/local/bin/ghost-hub  # 或安装位置
```
