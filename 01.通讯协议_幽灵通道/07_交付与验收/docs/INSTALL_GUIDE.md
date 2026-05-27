# Ghost Hub SDK 完整安装指南

> **文档版本**: v1.0  
> **SDK版本**: 1.0.0  
> **更新日期**: 2026-04-15  
> **阅读时长**: 10分钟

---

## 📋 目录

1. [快速安装](#快速安装) - 5分钟上手
2. [系统要求](#系统要求) - 环境检查
3. [安装方式](#安装方式) - pip/源码/Docker
4. [完整安装场景](#完整安装场景) - Windows/Mac/Linux
5. [组件安装](#组件安装) - 按需安装
6. [验证安装](#验证安装) - 确认成功
7. [故障排除](#故障排除) - 常见问题
8. [FAQ](#faq) - 常见问题解答
9. [卸载](#卸载) - 清理环境

---

## 🚀 快速安装

<!-- AI-READY: QUICK_INSTALL_BLOCK -->
```bash
# 方式1: pip安装 (推荐)
pip install ghost-hub-sdk

# 方式2: 验证安装
python -c "from ghost_hub_sdk import GhostHubSDK; print('安装成功')"
```

> **人类提示**: 如果您只需要快速体验，直接运行上面的pip命令即可。

---

## 📐 系统要求

### 最低要求

| 组件 | 最低 | 推荐 | 验证命令 |
|------|------|------|----------|
| Python | 3.10 | 3.11/3.12 | `python --version` |
| 内存 | 2GB | 4GB+ | - |
| 磁盘 | 1GB | 5GB+ | - |
| 网络 | 需要 | 稳定 | - |

### 依赖项

```
# 核心依赖 (自动安装)
- Python >= 3.10
- pip >= 21.0

# 可选依赖 (按需安装)
- paho-mqtt >= 1.6.0    # IoT MQTT支持
- cryptography >= 41.0.0 # 加密功能
```

---

## 📥 安装方式

### 方式一：pip安装 (推荐)

```bash
# 标准安装
pip install ghost-hub-sdk

# 指定版本
pip install ghost-hub-sdk==1.0.0

# 升级
pip install --upgrade ghost-hub-sdk

# 使用国内镜像 [可选]
pip install ghost-hub-sdk -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方式二：源码安装

```bash
# 克隆仓库
git clone https://github.com/ghost-hub/sdk.git
cd sdk

# 开发模式安装 (包含所有依赖)
pip install -e ".[all]"

# 或仅核心功能
pip install -e .
```

### 方式三：Docker安装

```bash
# 拉取镜像
docker pull ghosthub/sdk:1.0.0

# 运行
docker run -p 8080:8080 ghosthub/sdk:1.0.0
```

---

## 🖥️ 完整安装场景

### 场景1：Windows 11 + Python 3.12

<!-- AI-READY: WINDOWS_INSTALL -->
```powershell
# 1. 检查Python版本
python --version
# 输出应为: Python 3.12.x

# 2. 升级pip
python -m pip install --upgrade pip

# 3. 安装SDK
pip install ghost-hub-sdk

# 4. 验证安装
python -c "import ghost_hub_sdk; print(ghost_hub_sdk.__version__)"
# 输出应为: 1.0.0

# 5. 运行测试
python -c "from ghost_hub_sdk import GhostHubSDK; sdk = GhostHubSDK(); print('OK')"
```

### 场景2：macOS + Homebrew Python

<!-- AI-READY: MACOS_INSTALL -->
```bash
# 1. 检查Python
python3 --version

# 2. 安装/升级Python
brew install python@3.12
# 或: brew upgrade python@3.12

# 3. 创建虚拟环境 [推荐]
python3 -m venv ghost-hub-env
source ghost-hub-env/bin/activate

# 4. 安装SDK
pip install ghost-hub-sdk

# 5. 验证
python -c "from ghost_hub_sdk import GhostHubSDK; print('OK')"
```

### 场景3：Ubuntu 22.04 / Debian

<!-- AI-READY: UBUNTU_INSTALL -->
```bash
# 1. 安装Python
sudo apt update
sudo apt install python3.11 python3-pip python3.11-venv

# 2. 创建虚拟环境
python3 -m venv ghost-hub-env
source ghost-hub-env/bin/activate

# 3. 安装SDK
pip install ghost-hub-sdk

# 4. 验证
python -c "from ghost_hub_sdk import GhostHubSDK; print('OK')"
```

### 场景4：Docker完整环境

<!-- AI-READY: DOCKER_SETUP -->
```bash
# 1. 创建项目目录
mkdir my-ghost-hub && cd my-ghost-hub

# 2. 创建docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  ghost-hub:
    image: ghosthub/sdk:1.0.0
    ports:
      - "8080:8080"
    environment:
      - GHOST_HUB_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
EOF

# 3. 启动
docker-compose up -d

# 4. 验证
curl http://localhost:8080/health
```

---

## 🧩 组件安装

### 仅核心功能

```bash
pip install ghost-hub-sdk
```

### 仅意图银行

```bash
pip install ghost-hub-sdk[intention-bank]
```

### 仅IoT适配器

```bash
pip install ghost-hub-sdk[iot]
```

### 仅智能体联邦

```bash
pip install ghost-hub-sdk[agent]
```

### 全部功能

```bash
pip install ghost-hub-sdk[all]
```

---

## ✅ 验证安装

### 方式一：Python验证

```python
# 完整验证脚本
import ghost_hub_sdk

# 1. 检查版本
assert ghost_hub_sdk.__version__ == "1.0.0"

# 2. 导入SDK
from ghost_hub_sdk import GhostHubSDK

# 3. 初始化
sdk = GhostHubSDK()

# 4. 测试意图匹配
result = sdk.intention_bank.match_intent("测试")
print(f"意图匹配: {result.has_match}")

# 5. 清理
sdk.disconnect()

print("✅ 安装验证成功")
```

### 方式二：命令行验证

```bash
# 检查版本
python -c "import ghost_hub_sdk; print(ghost_hub_sdk.__version__)"

# 运行测试套件
python -m pytest tests/ -v

# 验证所有组件
python -c "
from ghost_hub_sdk import GhostHubSDK
sdk = GhostHubSDK()
print('意图银行:', sdk.intention_bank is not None)
print('IoT适配器:', sdk.no_ui_adapter is not None)
print('智能体联邦:', sdk.agent_federation is not None)
sdk.disconnect()
"
```

---

## 🔧 故障排除

### 问题1：Python版本不兼容

**症状**:
```
ERROR: Python 3.9 is not supported
```

**解决**:

| 系统 | 命令 |
|------|------|
| Windows | 下载 Python 3.12: https://www.python.org/downloads/ |
| macOS | `brew install python@3.12` |
| Ubuntu | `sudo apt install python3.11` |

### 问题2：pip安装失败

**症状**:
```
ERROR: Could not install packages due to OSError
```

**解决**:
```bash
# 1. 升级pip
python -m pip install --upgrade pip

# 2. 使用镜像
pip install ghost-hub-sdk -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 或使用代理
pip install ghost-hub-sdk --proxy http://proxy:8080
```

### 问题3：依赖冲突

**症状**:
```
ERROR: Cannot install paho-mqtt==1.6.0 because these packages conflict
```

**解决**:
```bash
# 使用虚拟环境隔离
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install ghost-hub-sdk
```

### 问题4：权限错误

**症状**:
```
ERROR: Could not install packages due to insufficient permissions
```

**解决**:
```bash
# 方案1: 使用用户安装
pip install --user ghost-hub-sdk

# 方案2: 检查Python权限
ls -la /usr/local/bin/python

# 方案3: 使用虚拟环境
python -m venv ~/ghost-hub-env
```

### 问题5：SSL证书错误

**症状**:
```
SSLError: HTTPSConnectionPool - Certificate verify failed
```

**解决**:
```bash
# 更新证书
pip install --upgrade certifi
python -c "import certifi; print(certifi.where())"

# 或临时跳过验证 (仅测试用)
pip install ghost-hub-sdk --trusted-host pypi.org
```

---

## ❓ FAQ

### Q1: 如何确认安装的是最新版本？

```bash
pip index versions ghost-hub-sdk
pip install ghost-hub-sdk==<最新版本>
```

### Q2: 可以同时安装多个版本吗？

不可以。建议使用虚拟环境：
```bash
python -m venv env-v0.2
source env-v0.2/bin/activate
pip install ghost-hub-sdk==1.0.0
```

### Q3: 离线环境下如何安装？

```bash
# 在线机器下载
pip download ghost-hub-sdk -d ./packages

# 离线机器安装
pip install ghost-hub-sdk --no-index --find-links=./packages
```

### Q4: 如何查看已安装的依赖？

```bash
pip show ghost-hub-sdk
pip list | grep ghost
```

### Q5: Docker镜像启动后无法访问？

```bash
# 检查容器状态
docker ps -a

# 查看日志
docker logs <container_id>

# 端口映射检查
docker port <container_id>
```

---

## 🗑️ 卸载

```bash
# pip卸载
pip uninstall ghost-hub-sdk

# 确认卸载
python -c "import ghost_hub_sdk"
# 应报错: ModuleNotFoundError
```

---

## 📚 相关文档

- [快速开始](./QUICK_START.md) - 5分钟体验
- [用户指南](./USER_GUIDE.md) - 完整功能文档
- [使用场景](./SCENARIOS.md) - 真实案例

---

## 🆘 技术支持

| 渠道 | 地址 |
|------|------|
| 文档 | https://docs.ghosthub.dev |
| GitHub Issues | https://github.com/ghost-hub/sdk/issues |
| Email | support@ghosthub.dev |
