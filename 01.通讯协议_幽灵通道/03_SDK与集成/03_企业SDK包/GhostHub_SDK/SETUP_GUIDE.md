﻿# Ghost Hub SDK v1.0.0 - 部署指南

## 目录

1. [环境要求](#1-环境要求)
2. [安装方式](#2-安装方式)
3. [快速开始](#3-快速开始)
4. [配置说明](#4-配置说明)
5. [部署模式](#5-部署模式)
6. [生产环境](#6-生产环境)
7. [故障排查](#7-故障排查)

---

## 1. 环境要求

### 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| Python | 3.10 | 3.11+ |
| 内存 | 512MB | 2GB+ |
| 磁盘 | 100MB | 500MB+ |
| 网络 | 可选 | 稳定网络 |

### 依赖检查

```bash
python --version  # 确保 >= 3.10
pip --version    # 确保可用
```

---

## 2. 安装方式

### 方式一：pip 安装（推荐）

```bash
# 基础安装
pip install ghost-hub-sdk

# 完整安装（包含所有协议）
pip install ghost-hub-sdk[all]

# 开发安装
pip install -e ".[dev]"
```

### 方式二：源码安装

```bash
# 克隆仓库
git clone https://github.com/your-org/ghost-hub-sdk.git
cd ghost-hub-sdk

# 安装
pip install -e .

# 或构建wheel
pip wheel build
pip install dist/*.whl
```

### 方式三：文件包安装

```bash
# 解压文件包
unzip ghost_hub_sdk_v1.0.0.zip -d ghost_hub_sdk

# 安装
cd ghost_hub_sdk
pip install .
```

---

## 3. 快速开始

### 3.1 基础使用

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

# 创建SDK实例
config = GhostHubConfig()
sdk = GhostHubSDK(config)

# 执行意图
result = sdk.execute_workflow("打开客厅灯")

print(f"执行结果: {result}")
```

### 3.2 完整示例

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig
from ghost_hub_sdk.security import SimpleAuth, RateLimiter, InputValidator
from ghost_hub_sdk.memory import GhostHubMemory

# 初始化
config = GhostHubConfig(log_level="INFO")
sdk = GhostHubSDK(config)

# 安全设置
auth = SimpleAuth()
limiter = RateLimiter(requests_per_minute=100)

# 生成API Key
api_key = auth.generate_api_key()
auth.add_api_key(api_key, "demo_user", permissions=["read", "write"])

# 记忆层
memory = GhostHubMemory()

# 处理请求
def handle_request(intent: str, client_id: str):
    # 1. 限流检查
    if not limiter.check(client_id):
        return {"error": "Rate limited", "status": 429}
    
    # 2. 输入验证
    if not InputValidator.validate_intent_text(intent):
        return {"error": "Invalid input", "status": 400}
    
    # 3. 执行
    result = sdk.execute_workflow(intent)
    
    # 4. 记录
    memory.record_intent(intent, result)
    
    return {"result": result, "status": 200}

# 使用
response = handle_request("打开客厅灯", "client_001")
print(response)
```

---

## 4. 配置说明

### 4.1 配置文件

创建 `~/.ghost_hub/config.json`:

```json
{
    "version": "1.0.0",
    "storage": {
        "path": "~/.ghost_hub/data",
        "type": "json"
    },
    "logging": {
        "level": "INFO",
        "file": "~/.ghost_hub/logs/app.log"
    },
    "security": {
        "rate_limit": 100,
        "burst": 20
    }
}
```

### 4.2 环境变量

```bash
# 可选环境变量
export GHOST_HUB_STORAGE_PATH="~/.ghost_hub/data"
export GHOST_HUB_LOG_LEVEL="INFO"
export GHOST_HUB_CONFIG_PATH="~/.ghost_hub/config.json"
```

### 4.3 代码配置

```python
from ghost_hub_sdk import GhostHubConfig

config = GhostHubConfig(
    # 存储
    storage_path="./data",
    
    # 日志
    log_level="INFO",
    
    # 缓存
    enable_cache=True,
    max_history=1000,
    
    # 匹配阈值
    similarity_threshold=0.7,
    
    # 安全
    enable_auth=True,
    rate_limit_per_minute=100,
)
```

---

## 5. 部署模式

### 5.1 单机部署

适用于开发、测试、小规模生产：

```python
from ghost_hub_sdk import GhostHubSDK
from ghost_hub_sdk.storage import JSONStorage

# 使用JSON存储
storage = JSONStorage("./data/app.json")
sdk = GhostHubSDK()
```

### 5.2 服务部署

适用于生产环境，使用FastAPI：

```python
# server.py
from fastapi import FastAPI, HTTPException
from ghost_hub_sdk import GhostHubSDK
from ghost_hub_sdk.security import SimpleAuth, RateLimiter

app = FastAPI(title="Ghost Hub API")

sdk = GhostHubSDK()
auth = SimpleAuth()
limiter = RateLimiter(requests_per_minute=1000)

@app.post("/execute")
async def execute_intent(intent: str, api_key: str):
    # 验证
    if not auth.validate_api_key(api_key):
        raise HTTPException(401, "Invalid API Key")
    
    if not limiter.check(api_key):
        raise HTTPException(429, "Rate limited")
    
    # 执行
    result = sdk.execute_workflow(intent)
    return result

@app.get("/health")
async def health():
    return {"status": "healthy"}

# 启动
# uvicorn server:app --host 0.0.0.0 --port 8000
```

### 5.3 集群部署

适用于高可用场景：

```python
# 使用SQLite存储 + 副本
from ghost_hub_sdk.storage import SQLiteStorage

primary = SQLiteStorage("primary.db")
replicas = [SQLiteStorage(f"replica_{i}.db") for i in range(3)]

# 读写分离
def read_from_replica(intent: str):
    import random
    replica = random.choice(replicas)
    return replica.get(intent)

def write_to_primary(intent: str, result: dict):
    return primary.set(intent, result)
```

### 5.4 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  ghost-hub:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GHOST_HUB_STORAGE_PATH=/data
    volumes:
      - ./data:/data
```

---

## 6. 生产环境

### 6.1 安全配置

```python
from ghost_hub_sdk.security import (
    SimpleAuth,
    InputValidator,
    RateLimiter,
    SecurityChecker
)

# 1. 创建强密码的API Key
auth = SimpleAuth()
key = auth.generate_api_key()  # 使用安全的随机生成

# 2. 限制权限
auth.add_api_key(key, "production", permissions=["read"])

# 3. 严格限流
limiter = RateLimiter(requests_per_minute=60, burst=10)

# 4. 安全检查
issues = SecurityChecker.check_all()
if issues:
    print(f"警告：发现 {len(issues)} 个安全问题")
```

### 6.2 日志配置

```python
import logging
import logging.handlers

# 创建日志器
logger = logging.getLogger("ghost_hub")
logger.setLevel(logging.INFO)

# 文件处理器（轮转）
handler = logging.handlers.RotatingFileHandler(
    "/var/log/ghost_hub/app.log",
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
))
logger.addHandler(handler)

# 控制台处理器
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logger.addHandler(console)
```

### 6.3 监控配置

```python
# 指标收集
from dataclasses import dataclass

@dataclass
class Metrics:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_latency: float = 0.0

metrics = Metrics()

def track_request(result):
    metrics.total_requests += 1
    if result["success"]:
        metrics.successful_requests += 1
    else:
        metrics.failed_requests += 1

# 健康检查端点
@app.get("/metrics")
async def metrics():
    return {
        "requests_total": metrics.total_requests,
        "success_rate": metrics.successful_requests / max(metrics.total_requests, 1),
        "failure_rate": metrics.failed_requests / max(metrics.total_requests, 1),
    }
```

### 6.4 备份策略

```bash
# 定时备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/ghost_hub"

# 备份数据
cp -r ~/.ghost_hub/data "$BACKUP_DIR/data_$DATE"

# 保留最近30天
find "$BACKUP_DIR" -name "data_*" -mtime +30 -delete
```

---

## 7. 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| ImportError | 模块未安装 | `pip install ghost-hub-sdk` |
| PermissionError | 无写权限 | `chmod +w ~/.ghost_hub` |
| ConnectionError | 网络问题 | 检查防火墙/代理设置 |
| MemoryError | 内存不足 | 增加swap/减少max_history |

### 调试模式

```python
import logging

# 启用调试日志
logging.basicConfig(level=logging.DEBUG)

from ghost_hub_sdk import GhostHubSDK
sdk = GhostHubSDK(GhostHubConfig(log_level="DEBUG"))

# 详细输出
result = sdk.execute_workflow("打开客厅灯", verbose=True)
```

### 日志分析

```bash
# 查看错误日志
grep ERROR /var/log/ghost_hub/app.log

# 查看特定请求
grep "workflow_123" /var/log/ghost_hub/app.log

# 统计错误
grep ERROR /var/log/ghost_hub/app.log | wc -l
```

### 联系支持

- **文档**: `docs/` 目录
- **GitHub Issues**: https://github.com/your-org/ghost-hub-sdk/issues
- **Email**: support@ghosthub.example.com

---

*部署指南版本: v1.0.0*
*最后更新: 2026-04-15*
