# Ghost Hub SDK 快速参考卡

> **版本**: v1.0.0 | **更新时间**: 2026-04-15

---

## 🚀 5分钟快速开始

```python
# 1. 安装
pip install ghost-hub-sdk

# 2. 导入
from ghost_hub_sdk import GhostHubSDK

# 3. 使用
sdk = GhostHubSDK()
result = sdk.execute_workflow("招聘流程")
print(result["success"])

sdk.disconnect()
```

---

## 📦 导入一览

```python
# 核心
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

# 意图银行
from ghost_hub_sdk.components.intention_bank import (
    MatchResult, IntentMatch, Template, Task, TaskGraph
)

# IoT适配器
from ghost_hub_sdk.components.no_ui_adapter import (
    Device, DeviceCommand, CommandResult, Scene
)

# 智能体联邦
from ghost_hub_sdk.components.agent_federation import (
    Task, Agent, Message, Session, AgentStatus
)

# 安全模块
from ghost_hub_sdk.security import (
    SimpleAuth, InputValidator, RateLimiter, SensitiveDataProtector
)
```

---

## 🔧 SDK初始化

```python
# 最简初始化
sdk = GhostHubSDK()

# 完整配置
config = GhostHubConfig(
    intention_bank_enabled=True,
    no_ui_adapter_enabled=True,
    agent_federation_enabled=True,
    log_level="INFO"
)
sdk = GhostHubSDK(config)
```

---

## 🏦 意图银行

```python
# 意图匹配
result = sdk.intention_bank.match_intent("招聘工程师")
if result.has_match:
    print(result.top_match.template.name)
    print(result.top_match.confidence)

# 列出模板
templates = sdk.intention_bank.list_templates(domain="hr")

# 获取特定模板
template = sdk.intention_bank.get_template("hr_recruitment")

# 构建任务图
task_graph = sdk.intention_bank.build_task_graph(template)
print(f"任务数: {len(task_graph.nodes)}")
```

---

## 🔌 IoT适配器

```python
# 连接
sdk.no_ui_adapter.connect(protocol="mqtt", broker="mqtt://localhost:1883")

# 命令转换
command = sdk.no_ui_adapter.convert_intent_to_command(
    intent="开灯",
    device_type="light"
)
print(command)  # light_turn_on

# 列出设备
devices = sdk.no_ui_adapter.list_devices()

# 执行场景
results = sdk.no_ui_adapter.execute_scene("离家模式")
```

---

## 🤖 智能体联邦

```python
# 连接
sdk.agent_federation.connect()

# 分发任务
from ghost_hub_sdk.components.agent_federation import Task

task = Task(
    task_id="t1",
    description="数据分析",
    priority=1
)
result = sdk.agent_federation.distribute_task(
    task=task,
    intent="数据分析"
)
print(f"分配给: {result.assigned_agent}")

# 列出Agent
agents = sdk.agent_federation.list_agents()

# 统计
stats = sdk.agent_federation.get_stats()
print(f"在线: {stats['online_agents']}")
```

---

## ⚡ 工作流执行

```python
# 一键执行
result = sdk.execute_workflow("招聘流程")

if result["success"]:
    print(f"类型: {result['workflow_type']}")
    print(f"任务: {result['task_graph']['task_count']}")
    print(f"ROI: {result.get('roi_estimate', {})}")
else:
    print(f"错误: {result['errors']}")
```

---

## 📊 返回值结构

### MatchResult

```python
@dataclass
class MatchResult:
    has_match: bool           # 是否有匹配
    top_match: IntentMatch   # 最佳匹配
    matches: List[IntentMatch]  # 所有匹配
```

### IntentMatch

```python
@dataclass
class IntentMatch:
    confidence: float        # 置信度 0-1
    similarity: float        # 相似度 0-1
    template: Template      # 匹配的模板
    matched_patterns: List[str]  # 匹配的模式
```

### 工作流返回

```python
{
    "intent_text": str,      # 输入意图
    "workflow_type": str,    # 工作流类型
    "success": bool,         # 是否成功
    "task_graph": {          # 任务图
        "tasks": [...],
        "task_count": int
    },
    "errors": list           # 错误列表
}
```

### Stats

```python
{
    "enabled": bool,
    "connected": bool,
    "total_agents": int,
    "online_agents": int,
    "active_sessions": int
}
```

---

## ❌ 错误处理

```python
try:
    result = sdk.execute_workflow("流程")
    if not result["success"]:
        for error in result["errors"]:
            print(f"错误: {error}")
except Exception as e:
    print(f"异常: {e}")
finally:
    sdk.disconnect()  # 始终清理
```

---

## 💡 最佳实践

| 场景 | 做法 |
|------|------|
| 意图匹配 | 总是检查 `result.has_match` |
| 置信度 | 阈值 < 0.5 提示用户确认 |
| 连接 | 复用SDK实例，避免频繁创建 |
| 清理 | 使用 `finally` 确保 `disconnect()` |

---

## 🔢 API速查

| 功能 | 方法 | 返回 |
|------|------|------|
| 初始化 | `GhostHubSDK()` | SDK实例 |
| 意图匹配 | `sdk.intention_bank.match_intent(text)` | MatchResult |
| 工作流 | `sdk.execute_workflow(text)` | dict |
| 命令转换 | `sdk.no_ui_adapter.convert_intent_to_command(intent, device_type)` | str |
| 任务分发 | `sdk.agent_federation.distribute_task(task, intent)` | TaskDistributionResult |
| 列表 | `sdk.agent_federation.list_agents()` | List[Agent] |
| 统计 | `sdk.agent_federation.get_stats()` | dict |
| 连接 | `sdk.connect()` | dict |
| 断开 | `sdk.disconnect()` | None |

---

## 📁 文档导航

| 文档 | 内容 | 阅读时间 |
|------|------|----------|
| [INSTALL_GUIDE.md](./INSTALL_GUIDE.md) | 完整安装指南 | 10分钟 |
| [USER_GUIDE.md](./USER_GUIDE.md) | 完整用户指南 | 30分钟 |
| [SCENARIOS.md](./SCENARIOS.md) | 真实案例 | 20分钟 |
| [QUICK_START.md](./QUICK_START.md) | 快速开始 | 5分钟 |

---

## 🆘 获取帮助

```
文档: https://docs.ghosthub.dev
GitHub: https://github.com/ghost-hub/sdk/issues
邮箱: support@ghosthub.dev
```
