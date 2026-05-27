# Ghost Channel License Server - 部署指南

**版本**: 1.0.0  
**最后更新**: 2026-04-11

---

## 目录

1. [架构概述](#1-架构概述)
2. [快速部署](#2-快速部署)
3. [生产部署](#3-生产部署)
4. [云服务商部署](#4-云服务商部署)
5. [配置说明](#5-配置说明)
6. [运维操作](#6-运维操作)
7. [故障排除](#7-故障排除)
8. [AI管理指南](#8-ai管理指南)

---

## 1. 架构概述

```
                           ┌─────────────────┐
                           │   客户端SDK     │
                           └────────┬────────┘
                                    │ HTTPS
                                    ▼
┌─────────────────────────────────────────────────────────┐
│                    Ghost Channel License Server          │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ License  │  │Activation│  │ Verify   │  │ Stats  │ │
│  │ Generate │  │  API     │  │  API     │  │  API   │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │              License Database (SQLite/Redis)      │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Monitor    │
                    └──────────────┘
```

---

## 2. 快速部署

### 2.1 本地Docker部署

```bash
# 1. 进入部署目录
cd enterprise

# 2. 复制配置模板
cp docker/env.template docker/.env

# 3. 编辑配置
vim docker/.env
# 设置 SECRET_KEY=your_strong_secret_key

# 4. 启动服务
./deploy.sh local start

# 或使用PowerShell (Windows)
.\deploy.ps1 -Environment local -Action start
```

### 2.2 验证部署

```bash
# 检查服务状态
curl http://localhost:8001/

# 响应:
# {"status":"ok","service":"Ghost Channel License Server","version":"1.0.0"}

# 查看统计
curl http://localhost:8001/stats
```

### 2.3 测试许可证生成

```bash
# 生成试用许可证
python license_server/generate_key.py --trial

# 生成Pro许可证
python license_server/generate_key.py --pro

# 生成自定义许可证
python license_server/generate_key.py --custom semantic_matching predictive_sync --days 365
```

---

## 3. 生产部署

### 3.1 服务器要求

| 项目 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 1核 | 2核 |
| 内存 | 512MB | 1GB |
| 磁盘 | 10GB | 20GB |
| 带宽 | 1Mbps | 5Mbps |

### 3.2 生产部署步骤

```bash
# 1. 服务器初始化
ssh root@your-server
apt update && apt install -y docker.io docker-compose

# 2. 创建部署目录
mkdir -p /opt/ghost-license
cd /opt/ghost-license

# 3. 上传代码 (使用scp或git)
git clone https://github.com/q-spectrum/ghost-channel.git
cd ghost-channel/enterprise

# 4. 配置环境变量
cp docker/env.template docker/.env
vim docker/.env
# 必填: SECRET_KEY, DOMAIN

# 5. 配置SSL证书 (可选但推荐)
mkdir -p nginx/ssl
# 放置你的SSL证书到 nginx/ssl/

# 6. 启动服务
./deploy.sh production deploy

# 7. 配置防火墙
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

### 3.3 配置Nginx HTTPS

```bash
# 获取Let's Encrypt证书
apt install -y certbot
certbot certonly --standalone -d license.your-domain.com

# 复制证书
cp /etc/letsencrypt/live/license.your-domain.com/fullchain.pem nginx/ssl/cert.pem
cp /etc/letsencrypt/live/license.your-domain.com/privkey.pem nginx/ssl/key.pem
```

---

## 4. 云服务商部署

### 4.1 AWS (EC2 + ECS)

```bash
# 1. 创建EC2实例
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t3.micro \
    --key-name your-key \
    --security-groups sg-xxxxx

# 2. SSH连接后执行部署
ssh -i your-key.pem ec2-user@your-ip
# ... 执行上述生产部署步骤
```

### 4.2 阿里云 (ECS)

```bash
# 1. 创建ECS实例
# - 选择Ubuntu 22.04
# - 配置安全组: 开放80, 443, 8001端口

# 2. SSH连接后安装Docker
curl -fsSL https://get.docker.com | sh

# 3. 执行部署
git clone https://github.com/q-spectrum/ghost-channel.git
cd ghost-channel/enterprise
./deploy.sh production deploy
```

### 4.3 Vultr / DigitalOcean

```bash
# 创建快照后执行标准部署
# 1. 安装Docker
curl -fsSL https://get.docker.com | sh

# 2. 部署
cd ghost-channel/enterprise
SECRET_KEY=xxx ./deploy.sh production deploy
```

### 4.4 Kubernetes部署

```bash
# 1. 配置kubectl
kubectl config use-context your-cluster

# 2. 部署
kubectl apply -f docker/k8s/deployment.yaml

# 3. 检查状态
kubectl get pods -n ghost-license
kubectl get svc -n ghost-license
```

---

## 5. 配置说明

### 5.1 环境变量

| 变量 | 必填 | 说明 | 示例 |
|------|------|------|------|
| SECRET_KEY | 是 | 服务器密钥(32+字符) | `secrets.token_hex(32)` |
| APP_ENV | 是 | 运行环境 | `production` |
| SERVER_PORT | 否 | 服务端口 | `8001` |
| LOG_LEVEL | 否 | 日志级别 | `INFO` |
| REDIS_HOST | 否 | Redis主机 | `redis` |
| CORS_ORIGINS | 否 | CORS来源 | `*` |
| DOMAIN | 是 | 服务器域名 | `license.ghost-channel.io` |

### 5.2 生成强密钥

```python
# Python生成
python3 -c "import secrets; print(secrets.token_hex(32))"

# Linux生成
openssl rand -hex 32
```

---

## 6. 运维操作

### 6.1 日常运维

```bash
# 查看服务状态
./deploy.sh status

# 查看日志
./deploy.sh logs

# 查看实时日志 (最后100行)
docker-compose -f docker/docker-compose.yml logs -f --tail=100

# 重启服务
./deploy.sh restart

# 停止服务
./deploy.sh stop
```

### 6.2 许可证管理

```bash
# 生成许可证
python license_server/generate_key.py --pro --email customer@example.com

# 验证许可证
curl -X POST http://localhost:8001/license/verify?license_key=YOUR_KEY

# 撤销许可证
curl -X POST http://localhost:8001/license/revoke \
    -H "Content-Type: application/json" \
    -d '{"license_key":"YOUR_KEY"}'

# 查看所有激活
curl http://localhost:8001/activations
```

### 6.3 监控

```bash
# Prometheus指标 (如果启用)
curl http://localhost:8001/metrics

# 健康检查
curl http://localhost:8001/

# 服务器统计
curl http://localhost:8001/stats
```

### 6.4 备份

```bash
# 备份数据卷
docker run --rm \
    -v ghostlicense_license_data:/data \
    -v $(pwd)/backup:/backup \
    alpine tar czf /backup/license_data_$(date +%Y%m%d).tar.gz /data

# 恢复数据
docker run --rm \
    -v ghostlicense_license_data:/data \
    -v $(pwd)/backup:/backup \
    alpine tar xzf /backup/license_data_20260411.tar.gz -C /
```

---

## 7. 故障排除

### 7.1 服务无法启动

```bash
# 1. 检查Docker状态
docker ps -a

# 2. 查看日志
docker-compose logs

# 3. 检查端口占用
netstat -tlnp | grep 8001

# 4. 检查配置
cat docker/.env
```

### 7.2 许可证验证失败

```bash
# 1. 检查服务器时钟
timedatectl

# 2. 检查网络连接
curl -v http://localhost:8001/

# 3. 检查许可证数据库
docker exec -it ghost-license-server python -c "
from server import SERVER
print(SERVER.licenses)
"
```

### 7.3 性能问题

```bash
# 1. 检查资源使用
docker stats

# 2. 查看慢查询日志
docker-compose logs | grep -i slow

# 3. 增加资源
# 编辑docker-compose.yml中的resources配置
```

---

## 8. AI管理指南

### 8.1 AI理解结构

```
enterprise/
├── deploy.sh / deploy.ps1    # 主部署脚本 (AI入口点)
├── docker/
│   ├── Dockerfile            # 容器构建
│   ├── docker-compose.yml     # 服务编排
│   ├── k8s/                  # K8s部署配置
│   │   └── deployment.yaml   # K8s部署清单
│   ├── nginx/
│   │   └── nginx.conf        # 反向代理配置
│   └── env.template          # 配置模板
├── license_server/
│   ├── server.py             # 授权服务器主程序
│   ├── generate_key.py       # 密钥生成CLI
│   └── requirements.txt      # Python依赖
└── README.md                 # 本文件
```

### 8.2 AI常用命令

```bash
# 启动服务
./deploy.sh local start

# 查看状态
./deploy.sh status

# 查看日志
./deploy.sh logs

# 部署生产环境
SECRET_KEY=xxx DOMAIN=xxx ./deploy.sh production deploy

# 生成许可证
python license_server/generate_key.py --pro

# 清理资源
./deploy.sh clean
```

### 8.3 AI配置检查清单

部署前检查:
- [ ] SECRET_KEY 已设置 (32+字符)
- [ ] DOMAIN 已配置
- [ ] 端口8001未被占用
- [ ] Docker已安装
- [ ] SSL证书已配置 (生产环境)

---

## 联系方式

- **技术支持**: support@q-spectrum.ai
- **企业销售**: enterprise@q-spectrum.ai
- **文档**: https://ghost-channel.io/docs

---

*© 2026 Q-SpecTrum*
