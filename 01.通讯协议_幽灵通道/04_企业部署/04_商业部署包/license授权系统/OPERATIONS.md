# Ghost Channel License Server - 运维手册

**版本**: 1.0.0  
**最后更新**: 2026-04-11

---

## 目录

1. [日常运维](#1-日常运维)
2. [监控告警](#2-监控告警)
3. [备份恢复](#3-备份恢复)
4. [安全加固](#4-安全加固)
5. [性能优化](#5-性能优化)
6. [升级维护](#6-升级维护)
7. [应急响应](#7-应急响应)

---

## 1. 日常运维

### 1.1 健康检查

```bash
# 检查服务状态
curl -s http://localhost:8001/ | jq .

# 预期响应
{
  "status": "ok",
  "service": "Ghost Channel License Server",
  "version": "1.0.0",
  "timestamp": "2026-04-11T12:00:00"
}
```

### 1.2 日志查看

```bash
# 实时日志
./deploy.sh logs

# 查看错误日志
docker-compose logs --tail=500 | grep -i error

# 查看访问日志
docker-compose logs --tail=1000 | grep -i "POST /"

# 导出完整日志
docker-compose logs > logs_$(date +%Y%m%d).log
```

### 1.3 资源监控

```bash
# Docker资源使用
docker stats --no-stream

# 检查磁盘空间
docker system df

# 清理未使用的资源
docker system prune -a
```

### 1.4 许可证统计

```bash
# 获取统计
curl -s http://localhost:8001/stats | jq .

# 响应示例
{
  "total_licenses": 150,
  "valid_licenses": 145,
  "active_activations": 200,
  "revoked": 5
}
```

---

## 2. 监控告警

### 2.1 Prometheus监控

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'ghost-license'
    static_configs:
      - targets: ['license-server:8001']
    metrics_path: '/metrics'
```

### 2.2 告警规则

```yaml
# alertmanager.yml
groups:
  - name: ghost-license
    rules:
      # 服务宕机
      - alert: LicenseServerDown
        expr: up{job="ghost-license"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "License server is down"
          
      # 高错误率
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          
      # 许可证即将过期
      - alert: LicenseExpiringSoon
        expr: count(license_expires_timestamp - time() < 86400) > 0
        labels:
          severity: warning
```

### 2.3 日志监控

```bash
# 监控错误率
watch -n 10 'docker-compose logs --tail=100 | grep -c ERROR'

# 监控请求延迟
tail -f logs/app.log | awk '/Duration/ {print $NF}'

# 异常请求监控
grep -E "(500|502|503)" access.log | wc -l
```

---

## 3. 备份恢复

### 3.1 自动备份脚本

```bash
#!/bin/bash
# backup.sh - 自动备份脚本
# 添加到 crontab: 0 2 * * * /opt/ghost-license/backup.sh

BACKUP_DIR="/opt/ghost-license/backups"
DATE=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME="ghost-license-server"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据卷
docker run --rm \
    -v ghostlicense_license_data:/data \
    -v $BACKUP_DIR:/backup \
    alpine tar czf /backup/data_$DATE.tar.gz -C / data

# 备份配置
cp docker/.env $BACKUP_DIR/config_$DATE.env

# 备份日志
docker-compose logs --tail=10000 > $BACKUP_DIR/logs_$DATE.log

# 保留最近30天备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.env" -mtime +30 -delete
find $BACKUP_DIR -name "*.log" -mtime +7 -delete

# 上传到远程存储 (可选)
# aws s3 cp $BACKUP_DIR/data_$DATE.tar.gz s3://your-bucket/backups/

echo "[$(date)] Backup completed: $DATE"
```

### 3.2 恢复流程

```bash
# 1. 停止服务
docker-compose down

# 2. 恢复数据
docker run --rm \
    -v ghostlicense_license_data:/data \
    -v $(pwd)/backups:/backup \
    alpine tar xzf /backup/data_20260411_120000.tar.gz -C /

# 3. 恢复配置
cp backups/config_20260411.env docker/.env

# 4. 重启服务
docker-compose up -d

# 5. 验证
curl http://localhost:8001/stats
```

---

## 4. 安全加固

### 4.1 服务器安全

```bash
# 1. SSH密钥登录
ssh-keygen -t ed25519
ssh-copy-id root@your-server

# 2. 禁用密码登录
vim /etc/ssh/sshd_config
# PasswordAuthentication no
# PubkeyAuthentication yes
systemctl restart sshd

# 3. 配置防火墙
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# 4. 安装fail2ban
apt install -y fail2ban
systemctl enable fail2ban
```

### 4.2 Docker安全

```bash
# 1. 使用非root用户
usermod -aG docker appuser

# 2. 限制容器资源
docker update --memory="512m" --cpus="1" ghost-license-server

# 3. 启用Docker日志限制
# 编辑 /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
systemctl restart docker
```

### 4.3 SSL配置

```bash
# 使用Let's Encrypt
apt install -y certbot
certbot certonly --standalone -d license.your-domain.com

# 配置自动续期
crontab -e
# 0 0 * * * certbot renew --quiet
```

---

## 5. 性能优化

### 5.1 Nginx优化

```nginx
# nginx.conf 优化
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 10240;
    use epoll;
    multi_accept on;
}

http {
    # 连接复用
    keepalive_timeout 65;
    keepalive_requests 10000;
    
    # 缓冲优化
    client_body_buffer_size 10K;
    client_max_body_size 8m;
    proxy_buffering on;
    proxy_buffer_size 128k;
    proxy_buffers 4 256k;
}
```

### 5.2 应用优化

```python
# server.py 优化配置
app = FastAPI(
    title="Ghost Channel License Server",
    docs_url=None,  # 生产环境禁用文档
    redoc_url=None,
)

# 添加缓存
from functools import lru_cache

@lru_cache()
def get_config():
    return load_config()
```

### 5.3 数据库优化

```bash
# 如果使用Redis
redis-cli CONFIG SET maxmemory 256mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
redis-cli CONFIG SET save "900 1 300 10 60 10000"
```

---

## 6. 升级维护

### 6.1 版本升级

```bash
# 1. 备份
./deploy.sh stop
./backup.sh

# 2. 拉取新版本
git pull origin main

# 3. 重新构建
docker-compose build --no-cache

# 4. 测试环境验证
SECRET_KEY=test ./deploy.sh local start
curl http://localhost:8001/stats

# 5. 生产部署
./deploy.sh production deploy

# 6. 验证
curl http://localhost:8001/
```

### 6.2 数据库迁移

```python
# migrations/v001_add_indexes.py
async def migrate(db):
    await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_license_expires 
        ON licenses(expires_at)
    """)
    await db.execute("""
        CREATE INDEX IF NOT EXISTS idx_activation_license 
        ON activations(license_key)
    """)
```

---

## 7. 应急响应

### 7.1 服务宕机

```bash
# 1. 检查状态
docker ps -a
systemctl status docker

# 2. 查看日志
journalctl -u docker -n 100
docker-compose logs

# 3. 重启服务
docker-compose restart

# 4. 如果无法恢复
docker-compose down
docker-compose up -d
```

### 7.2 数据泄露

```bash
# 1. 立即停用所有许可证
curl -X POST http://localhost:8001/license/revoke \
    -H "Content-Type: application/json" \
    -d '{"license_key":"ALL"}'

# 2. 导出日志用于分析
docker-compose logs > incident_$(date +%Y%m%d_%H%M%S).log

# 3. 重置密钥
SECRET_KEY=$(openssl rand -hex 32)
# 更新SECRET_KEY后重启所有服务
```

### 7.3 DDoS攻击

```bash
# 1. 查看异常请求
docker-compose logs | awk '/$remote_addr/ {print $1}' | sort | uniq -c | sort -rn | head -20

# 2. 配置Nginx限流
# nginx.conf
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;

# 3. IP黑名单
docker-compose exec nginx sh -c 'echo "deny 1.2.3.4;" >> /etc/nginx/blockip.conf && nginx -s reload'
```

---

## 联系信息

| 场景 | 联系方式 |
|------|----------|
| 技术支持 | support@q-spectrum.ai |
| 安全漏洞 | security@q-spectrum.ai |
| 商务合作 | enterprise@q-spectrum.ai |

---

*© 2026 Q-SpecTrum*
