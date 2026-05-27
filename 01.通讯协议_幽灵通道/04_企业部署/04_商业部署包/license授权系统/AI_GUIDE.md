# Ghost Channel Enterprise - AI管理指南

**版本**: 1.0.0  
**最后更新**: 2026-04-11

---

## AI快速入门

### 我是什么项目？

Ghost Channel Enterprise 是一个 **商业许可证授权服务器**，用于管理Ghost Channel Protocol的商业许可证。

### 核心组件

| 组件 | 路径 | 说明 |
|------|------|------|
| **授权服务器** | `license_server/server.py` | FastAPI服务，端口8001 |
| **密钥生成器** | `license_server/generate_key.py` | CLI工具，生成许可证密钥 |
| **部署脚本** | `deploy.sh` / `deploy.ps1` | 一键部署 |
| **Docker配置** | `docker/` | 容器化部署 |

---

## AI常用命令

### 部署相关

```bash
# 查看部署帮助
./deploy.sh help

# 本地启动
./deploy.sh local start

# 查看状态
./deploy.sh status

# 查看日志
./deploy.sh logs

# 生产部署
SECRET_KEY=xxx ./deploy.sh production deploy

# 清理
./deploy.sh clean
```

### 许可证管理

```bash
# 生成许可证
python license_server/generate_key.py --trial           # 试用版
python license_server/generate_key.py --pro             # Pro版
python license_server/generate_key.py --team            # Team版
python license_server/generate_key.py --enterprise     # 企业版

# 带参数
python license_server/generate_key.py --pro --email user@example.com --days 365
```

### 运维命令

```bash
# 健康检查
curl http://localhost:8001/

# 获取统计
curl http://localhost:8001/stats

# 验证许可证
curl -X POST "http://localhost:8001/license/verify?license_key=YOUR_KEY"

# 撤销许可证
curl -X POST http://localhost:8001/license/revoke \
  -H "Content-Type: application/json" \
  -d '{"license_key":"YOUR_KEY"}'

# 查看激活列表
curl http://localhost:8001/activations
```

---

## 目录结构

```
enterprise/
├── deploy.sh                    # Bash部署脚本 (Linux/Mac)
├── deploy.ps1                  # PowerShell部署脚本 (Windows)
├── README.md                    # 英文说明
├── DEPLOYMENT.md                # 部署指南
├── OPERATIONS.md                # 运维手册
│
├── ghost_channel_enterprise/    # 商业模块源代码
│   ├── semantics.pyx           # 语义匹配 (Cython)
│   ├── predictive.pyx         # 预测同步 (Cython)
│   ├── knowledge_graph.pyx     # 知识图谱 (Cython)
│   └── client_sdk.py          # 客户端SDK
│
├── license_server/             # 授权服务器
│   ├── server.py              # FastAPI主程序
│   ├── generate_key.py        # 密钥生成CLI
│   └── requirements.txt       # Python依赖
│
├── setup_cython.py            # Cython编译配置
│
└── docker/                    # Docker部署
    ├── Dockerfile             # 容器定义
    ├── docker-compose.yml     # 服务编排
    ├── nginx/
    │   └── nginx.conf        # 反向代理
    ├── k8s/
    │   └── deployment.yaml    # K8s部署
    └── env.template          # 配置模板
```

---

## 配置说明

### 必须配置

| 变量 | 说明 | 如何设置 |
|------|------|----------|
| `SECRET_KEY` | 服务器密钥 | `python3 -c "import secrets; print(secrets.token_hex(32))"` |
| `DOMAIN` | 服务器域名 | 生产环境必填 |

### 可选配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SERVER_PORT` | 8001 | 服务端口 |
| `LOG_LEVEL` | INFO | 日志级别 |
| `REDIS_HOST` | redis | Redis主机 |
| `CORS_ORIGINS` | * | CORS来源 |

---

## 常见问题

### Q: 服务无法启动怎么办？

```bash
# 1. 检查端口占用
netstat -tlnp | grep 8001

# 2. 查看日志
docker-compose logs

# 3. 检查配置
cat docker/.env
```

### Q: 如何生成许可证？

```bash
# 试用版 (14天)
python license_server/generate_key.py --trial

# Pro版 (1年)
python license_server/generate_key.py --pro --email user@example.com
```

### Q: 如何撤销许可证？

```bash
curl -X POST http://localhost:8001/license/revoke \
  -H "Content-Type: application/json" \
  -d '{"license_key":"要撤销的密钥"}'
```

### Q: 如何查看服务器统计？

```bash
curl http://localhost:8001/stats | python -m json.tool
```

---

## 安全注意事项

1. **SECRET_KEY**: 绝不能泄露，必须32字符以上
2. **生产环境**: 必须启用SSL
3. **备份**: 定期备份数据和配置
4. **日志**: 监控异常访问

---

## 升级流程

```bash
# 1. 备份
./deploy.sh stop
./backup.sh

# 2. 更新代码
git pull origin main

# 3. 重新构建
docker-compose build

# 4. 启动
./deploy.sh production deploy
```

---

## 联系支持

- **技术支持**: support@q-spectrum.ai
- **商务合作**: enterprise@q-spectrum.ai

---

*© 2026 Q-SpecTrum*
