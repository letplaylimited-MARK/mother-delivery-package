# Ghost Hub SDK v1.0.0 - 用户使用场景分析

## 目录

1. [用户画像分析](#1-用户画像分析)
2. [典型使用场景](#2-典型使用场景)
3. [常见问题预防](#3-常见问题预防)
4. [安全风险提示](#4-安全风险提示)
5. [交付清单](#5-交付清单)

---

## 1. 用户画像分析

### 目标用户

| 用户类型 | 技术水平 | 使用场景 | 关注点 |
|---------|----------|----------|--------|
| 企业开发者 | 高 | 集成到企业系统 | 稳定性、安全性、文档 |
| IoT集成商 | 中高 | 设备控制场景 | 易用性、协议支持 |
| AI应用开发者 | 高 | 工作流编排 | 灵活性、扩展性 |
| 独立开发者 | 中 | 快速原型开发 | 上手速度、示例代码 |
| 技术爱好者 | 不等 | 学习研究 | 代码质量、架构设计 |

### 用户痛点

1. **集成困难** - SDK与现有系统对接复杂
2. **文档不足** - 缺少实际使用示例
3. **安全问题** - 不了解安全最佳实践
4. **性能问题** - 高并发场景下性能下降
5. **调试困难** - 错误信息不清晰

---

## 2. 典型使用场景

### 场景一：智能家居控制

**用户意图**: "打开客厅灯、调暗到50%、设置空调到24度"

**SDK使用**:
```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()

# 解析意图
result = sdk.execute_workflow("打开客厅灯并调暗到50%")

if result["success"]:
    print(f"灯光已调整到 {result['brightness']}%")
```

**预防问题**:
- ❌ 用户可能输入恶意命令 → 已实现输入验证
- ❌ 设备离线 → 需要超时处理
- ❌ 并发控制 → 已实现限流

### 场景二：企业工作流编排

**用户意图**: 自动处理工单、审批流程

**SDK使用**:
```python
from ghost_hub_sdk import GhostHubSDK
from ghost_hub_sdk.security import SimpleAuth

sdk = GhostHubSDK()
auth = SimpleAuth()

# 创建API Key
key = auth.generate_api_key()
auth.add_api_key(key, "workflow_service", permissions=["read", "write"])

# 执行工作流
result = sdk.execute_workflow("创建工单并通知审批人")
```

**预防问题**:
- ❌ 权限失控 → 已实现RBAC权限模型
- ❌ 数据泄露 → 已实现敏感数据脱敏
- ❌ API滥用 → 已实现请求频率限制

### 场景三：多智能体协作

**用户意图**: 多个AI智能体协同完成复杂任务

**SDK使用**:
```python
from ghost_hub_sdk.components import AgentFederationComponent

federation = AgentFederationComponent()

# 创建协作任务
task = federation.create_task(
    name="会议安排",
    agents=["calendar_agent", "email_agent", "notification_agent"]
)

# 执行
result = federation.execute_task(task)
```

**预防问题**:
- ❌ 智能体冲突 → 已实现路由策略
- ❌ 结果不一致 → 已实现结果聚合
- ❌ 死锁 → 已实现超时机制

### 场景四：数据采集与存储

**用户意图**: 设备数据持久化、查询分析

**SDK使用**:
```python
from ghost_hub_sdk.storage import SQLiteStorage

storage = SQLiteStorage("iot_data.db")

# 存储数据
storage.set("device_001", {
    "temperature": 25.5,
    "humidity": 60,
    "timestamp": 1234567890
})

# 查询
results = storage.query(
    "SELECT * FROM storage WHERE key LIKE ?",
    ["device_%"]
)
```

**预防问题**:
- ❌ SQL注入 → 已实现表名验证
- ❌ 数据丢失 → 已实现版本控制
- ❌ 存储溢出 → 已实现容量限制

### 场景五：实时监控告警

**用户意图**: 设备异常实时告警

**SDK使用**:
```python
from ghost_hub_sdk.protocols import MQTTClient

client = MQTTClient(
    broker="mqtt.example.com",
    port=1883
)

def on_alert(topic, payload):
    if payload["severity"] == "critical":
        print(f"紧急告警: {payload['message']}")

client.connect()
client.subscribe("home/+/alert")
client.set_callback(on_alert)
client.loop_start()
```

**预防问题**:
- ❌ 连接中断 → 已实现自动重连
- ❌ 消息丢失 → 已实现QoS级别
- ❌ 资源泄漏 → 已实现清理机制

---

## 3. 常见问题预防

### 问题一：模块导入失败

**症状**: `ImportError: cannot import name 'xxx'`

**原因**: 模块导出不完整

**预防**:
```python
# ✅ 正确做法：检查模块是否可用
try:
    from ghost_hub_sdk import GhostHubSDK
except ImportError:
    print("请安装 ghost-hub-sdk: pip install ghost-hub-sdk")

# ✅ 使用可选导入
try:
    from ghost_hub_sdk.protocols import MQTTClient
except ImportError:
    print("MQTT模块需要额外依赖: pip install paho-mqtt")
```

### 问题二：配置文件丢失

**症状**: `FileNotFoundError: config.json`

**原因**: 未检查配置目录

**预防**:
```python
from pathlib import Path

# ✅ 正确做法：确保配置目录存在
config_path = Path.home() / ".ghost_hub"
config_path.mkdir(parents=True, exist_ok=True)

# ✅ 创建默认配置
config_file = config_path / "config.json"
if not config_file.exists():
    config_file.write_text('{"log_level": "INFO"}')
```

### 问题三：并发访问冲突

**症状**: 数据不一致、丢失更新

**原因**: 未使用线程锁

**预防**:
```python
import threading
from ghost_hub_sdk.memory import GhostHubMemory

# ✅ GhostHubMemory 已内置线程锁
memory = GhostHubMemory()

# 并发访问是安全的
for i in range(100):
    threading.Thread(
        target=lambda: memory.learn_preference(f"key_{i}", f"value_{i}")
    ).start()
```

### 问题四：资源未释放

**症状**: 文件句柄泄漏、连接池耗尽

**原因**: 缺少清理代码

**预防**:
```python
from ghost_hub_sdk.storage import SQLiteStorage

# ✅ 正确做法：使用上下文管理器
storage = SQLiteStorage("data.db")
try:
    storage.set("key", {"data": "value"})
finally:
    storage.close()  # 显式关闭

# ✅ 或使用 with 语句（如果实现了）
# with SQLiteStorage("data.db") as storage:
#     storage.set("key", {"data": "value"})
```

### 问题五：超时无响应

**症状**: 请求无响应、界面卡死

**原因**: 阻塞操作无超时

**预防**:
```python
import signal

# ✅ 正确做法：设置超时
def timeout_handler(signum, frame):
    raise TimeoutError("操作超时")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30秒超时

try:
    result = sdk.execute_workflow("复杂任务")
except TimeoutError:
    print("任务执行超时")
finally:
    signal.alarm(0)  # 取消超时
```

---

## 4. 安全风险提示

### 风险一：API Key泄露

**风险**: 恶意用户利用泄露的Key

**防护措施**:
```python
# ✅ 1. 不在代码中硬编码Key
# ❌ 错误
API_KEY = "sk_live_xxx"

# ✅ 正确：使用环境变量
import os
API_KEY = os.environ.get("GHOST_HUB_API_KEY")

# ✅ 2. 定期轮换Key
auth = SimpleAuth()
auth.rotate_api_key(old_key)  # 定期调用

# ✅ 3. 监控异常访问
stats = auth.get_stats()
if stats["total_requests"] > 10000:
    print("警告：API使用量异常")
```

### 风险二：注入攻击

**风险**: 恶意输入执行危险命令

**防护措施**:
```python
# ✅ 所有用户输入必须验证
from ghost_hub_sdk.security import InputValidator

user_input = request.form["intent"]

# 验证
if not InputValidator.validate_intent_text(user_input):
    abort(400, "无效的输入")

# 消毒
safe_input = InputValidator.sanitize_text(user_input)
```

### 风险三：权限提升

**风险**: 普通用户获得管理员权限

**防护措施**:
```python
# ✅ 1. 最小权限原则
auth.add_api_key(key, "user", permissions=["read"])

# ✅ 2. 权限检查
if not auth.has_permission(key, "admin"):
    abort(403, "需要管理员权限")

# ✅ 3. 审计日志
logger.info(f"权限检查: user={name}, action={action}")
```

### 风险四：数据泄露

**风险**: 敏感信息暴露

**防护措施**:
```python
from ghost_hub_sdk.security import SensitiveDataProtector

# ✅ 日志脱敏
log = SensitiveDataProtector.safe_log(
    "User action",
    {"password": "secret", "api_key": key}
)
# 输出: "User action | data: {'password': 'se***t', 'api_key': 'sk_***'}"

# ✅ 配置检查
issues = SecurityChecker.check_all()
for issue in issues:
    if issue["severity"] == "high":
        print(f"高风险: {issue['message']}")
```

---

## 5. 交付清单

### 文件包结构

```
ghost_hub_sdk_v1.0.0/
├── __init__.py                    # 包入口
├── core.py                        # 核心SDK
├── config.py                      # 配置类
│
├── components/                    # 三大组件
│   ├── __init__.py
│   ├── intention_bank.py         # 意图银行
│   ├── no_ui_adapter.py          # 无UI适配器
│   └── agent_federation.py       # 智能体联邦
│
├── workflow_engine.py             # 工作流引擎
├── memory.py                      # 记忆层
├── knowledge.py                   # 知识层
├── storage.py                     # 持久化存储
├── security.py                    # 安全模块
│
├── protocols/                     # 协议实现
│   ├── __init__.py
│   ├── mqtt_client.py           # MQTT客户端
│   └── websocket_client.py       # WebSocket客户端
│
├── templates/                     # 业务模板
│   ├── index.json
│   ├── lighting_control.json
│   └── ...
│
├── demos/                        # 示例代码
│   ├── demo_integration.py       # 集成测试
│   ├── demo_security.py          # 安全测试
│   ├── demo_secure_api.py        # API测试
│   ├── demo_boundary.py          # 边界测试
│   └── demo_concurrency.py        # 并发测试
│
├── docs/                         # 文档
│   ├── API.md                    # API参考
│   ├── USER_MANUAL.md            # 用户手册
│   └── EXAMPLES.md               # 示例代码
│
├── tests/                        # 单元测试
│   ├── test_core.py
│   ├── test_security.py
│   └── ...
│
├── pyproject.toml                # 项目配置
├── README.md                     # 项目说明
├── LICENSE                       # 许可证
└── SETUP_GUIDE.md               # 部署指南
```

### 依赖清单

```
# 核心依赖
Python >= 3.10

# 可选依赖
fastapi >= 0.100.0              # API支持
uvicorn >= 0.23.0               # ASGI服务器
paho-mqtt >= 1.6.1              # MQTT支持
websockets >= 11.0.0             # WebSocket支持

# 开发依赖
pytest >= 7.0.0                  # 测试框架
pytest-asyncio >= 0.21.0         # 异步测试
pytest-cov >= 4.0.0             # 覆盖率
```

### 安装命令

```bash
# 基础安装
pip install ghost-hub-sdk

# 完整安装（含所有协议）
pip install ghost-hub-sdk[all]

# 开发安装
pip install -e ".[dev]"
```

### 快速验证

```bash
# 运行所有测试
python -m pytest tests/

# 运行集成测试
python demos/demo_integration.py

# 运行安全测试
python demos/demo_security.py
```

### 部署检查清单

- [ ] Python 版本 >= 3.10
- [ ] 所有依赖已安装
- [ ] 测试全部通过
- [ ] 配置文件存在且正确
- [ ] 日志目录可写
- [ ] 数据目录存在
- [ ] 安全配置已审查

---

## 技术支持

- **文档**: `docs/` 目录
- **示例**: `demos/` 目录
- **Issues**: GitHub Issues
- **Email**: support@ghosthub.example.com

---

*文档版本: v1.0.0*
*最后更新: 2026-04-15*
