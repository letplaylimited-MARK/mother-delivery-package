# Ghost Hub SDK 完整用户指南

> **文档版本**: v1.1  
> **SDK版本**: 1.0.0  
> **更新日期**: 2026-04-15  
> **阅读时长**: 30分钟
> 
> **⚠️ 重要提示**: 当前版本意图银行主要支持**中文**输入。英文输入可能在模板匹配时返回无匹配结果。

---

## 📋 目录

1. [概述](#概述) - 产品定位与核心能力
2. [架构设计](#架构设计) - 系统组件与数据流
3. [快速开始](#快速开始) - 3步完成集成
4. [核心功能](#核心功能) - 三大组件详解
5. [API参考](#api参考) - 完整API文档
6. [最佳实践](#最佳实践) - 生产环境指南
7. [性能优化](#性能优化) - 性能调优建议
8. [安全指南](#安全指南) - 安全配置
9. [迁移指南](#迁移指南) - 从旧版本升级

---

## 🎯 概述

### 产品定位

Ghost Hub SDK 是**企业级AI工作流编排框架**，通过三大核心能力实现智能化业务流程：

| 能力 | 功能 | 典型场景 |
|------|------|----------|
| 🏦 **意图银行** | 自然语言理解、模板匹配、任务分解 | HR招聘、客服问答 |
| 🔌 **IoT适配器** | 设备控制、协议转换、场景联动 | 智能家居、工业控制 |
| 🤖 **智能体联邦** | 多Agent协作、任务分发、结果聚合 | 数据分析、内容生成 |

### 核心优势

```
✅ 零配置启动 - 安装即用
✅ 模块化设计 - 按需启用
✅ 模板化业务 - 23+预置模板
✅ 多协议支持 - MQTT/HTTP/WebSocket
✅ 企业级安全 - 认证/限流/脱敏
```

---

## 🏗️ 架构设计

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     Ghost Hub SDK                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  意图银行   │  │  IoT适配器  │  │ 智能体联邦  │         │
│  │ Intention   │  │  No-UI     │  │   Agent     │         │
│  │   Bank      │  │  Adapter    │  │ Federation  │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          ▼                                │
│               ┌─────────────────┐                         │
│               │   工作流引擎    │                         │
│               │ Workflow Engine │                         │
│               └────────┬────────┘                         │
│                        │                                  │
│         ┌──────────────┼──────────────┐                   │
│         ▼              ▼              ▼                    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐            │
│  │   记忆层   │ │   知识层   │ │   存储层   │            │
│  │  Memory   │ │ Knowledge  │ │  Storage   │            │
│  └────────────┘ └────────────┘ └────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 数据流

```
用户输入 → 意图解析 → 模板匹配 → 任务分解 → 工作流执行 → 结果输出
    │          │           │           │           │
    ▼          ▼           ▼           ▼           ▼
意图银行    语义分析    相似度计算   依赖图构建   执行报告
```

---

## 🚀 快速开始

### ⚠️ 重要说明

> **意图匹配语言支持**: 当前版本的意图银行主要针对**中文**输入进行了优化。使用中文输入可获得最佳匹配效果。

| 输入语言 | 匹配效果 | 建议 |
|----------|----------|------|
| 中文 | ✅ 最佳 | 优先使用 |
| 英文 | ⚠️ 部分支持 | 可能无匹配 |

### 3步完成集成

#### Step 1: 安装

```bash
pip install ghost-hub-sdk
```

#### Step 2: 初始化

```python
from ghost_hub_sdk import GhostHubSDK

# 最简初始化
sdk = GhostHubSDK()

# 完整配置
from ghost_hub_sdk import GhostHubConfig

config = GhostHubConfig(
    intention_bank_enabled=True,
    no_ui_adapter_enabled=True,
    agent_federation_enabled=True,
    log_level="INFO"
)
sdk = GhostHubSDK(config)
```

#### Step 3: 使用

```python
# 意图匹配 (使用中文)
result = sdk.intention_bank.match_intent("招聘Python工程师")
if result.has_match:
    print(f"匹配模板: {result.top_match.template.name}")

# 工作流执行 (使用中文)
result = sdk.execute_workflow("优化招聘流程")
if result["success"]:
    print(f"任务数: {len(result['task_graph']['tasks'])}")

# IoT控制
command = sdk.no_ui_adapter.convert_intent_to_command("开灯", "light")
print(f"命令: {command}")

# 任务分发
from ghost_hub_sdk.components.agent_federation import Task
task = Task(task_id="t1", description="数据分析", priority=1)
result = sdk.agent_federation.distribute_task(task=task, intent="分析")

# 清理
sdk.disconnect()
```

---

## 🔧 核心功能

### 1. 意图银行 (Intention Bank)

意图银行是SDK的核心模块，负责理解用户意图并匹配业务模板。

#### 功能列表

| 功能 | 说明 | API |
|------|------|-----|
| 意图解析 | 自然语言转结构化意图 | `match_intent()` |
| 模板匹配 | 语义相似度计算 | `match_multi_intent()` |
| 任务分解 | 意图转任务依赖图 | `build_task_graph()` |
| 领域过滤 | 按领域筛选模板 | `list_templates(domain=)` |

#### 代码示例

```python
# 基础意图匹配
result = sdk.intention_bank.match_intent("帮我招聘前端工程师")

if result.has_match:
    top = result.top_match
    print(f"模板: {top.template.name}")
    print(f"置信度: {top.confidence:.2f}")
    print(f"相似度: {top.similarity:.2f}")
    print(f"匹配模式: {top.matched_patterns}")

# 领域过滤
hr_templates = sdk.intention_bank.list_templates(domain="hr")
print(f"HR模板数: {len(hr_templates)}")

# 构建任务图
template = result.top_match.template
task_graph = sdk.intention_bank.build_task_graph(template)
print(f"任务节点: {len(task_graph.nodes)}")
```

#### MatchResult 结构

<!-- AI-READY: MATCH_RESULT_STRUCT -->
```python
@dataclass
class MatchResult:
    """意图匹配结果"""
    matches: List[IntentMatch]      # 所有匹配列表
    top_match: Optional[IntentMatch] # 最佳匹配

    @property
    def has_match(self) -> bool:
        """是否有有效匹配"""
        return self.top_match is not None and \
               self.top_match.similarity >= 0.3
```

#### IntentMatch 结构

<!-- AI-READY: INTENT_MATCH_STRUCT -->
```python
@dataclass
class IntentMatch:
    """单个匹配结果"""
    template: Template      # 匹配的模板
    similarity: float        # 相似度分数
    confidence: float       # 置信度
    matched_patterns: List[str]  # 匹配的模式
```

#### Template 结构

<!-- AI-READY: TEMPLATE_STRUCT -->
```python
@dataclass
class Template:
    """业务模板"""
    id: str                    # 模板ID
    name: str                  # 模板名称
    domain: str                # 领域
    description: str           # 描述
    intent_patterns: List[str] # 意图模式
    intent_vector: IntentVector # 意图向量
    tasks: List[Task]          # 任务列表
    business_metrics: Dict[str, str]  # 业务指标
    roi_estimate: Dict[str, Any]     # ROI估算
    tags: List[str]            # 标签
```

---

### 2. IoT适配器 (No-UI Adapter)

IoT适配器提供设备控制能力，支持MQTT/HTTP协议。

#### 功能列表

| 功能 | 说明 | API |
|------|------|-----|
| 设备连接 | MQTT/HTTP连接 | `connect()` |
| 命令转换 | 自然语言转设备命令 | `convert_intent_to_command()` |
| 设备管理 | 列出和控制设备 | `list_devices()` |
| 场景执行 | 执行预定义场景 | `execute_scene()` |

#### 代码示例

```python
# 连接设备
sdk.no_ui_adapter.connect(protocol="mqtt", broker="mqtt://localhost:1883")

# 自然语言转命令
command = sdk.no_ui_adapter.convert_intent_to_command(
    intent="把客厅灯调暗到50%",
    device_type="light"
)
print(f"命令: {command}")  # 输出: light_dim_50

# 列出设备
devices = sdk.no_ui_adapter.list_devices()
for device in devices:
    print(f"{device.name} ({device.type}): {device.status}")

# 执行场景
results = sdk.no_ui_adapter.execute_scene("离家模式")
for r in results:
    print(f"{r.device_id}: {r.status}")
```

---

### 3. 智能体联邦 (Agent Federation)

智能体联邦支持多Agent协作，实现分布式任务处理。

#### 功能列表

| 功能 | 说明 | API |
|------|------|-----|
| Agent注册 | 注册和管理Agent | `register_agent()` |
| 任务分发 | 智能路由任务 | `distribute_task()` |
| 结果聚合 | 聚合多Agent结果 | `aggregate_results()` |
| 协作会话 | 创建协作会话 | `create_session()` |

#### 代码示例

```python
from ghost_hub_sdk.components.agent_federation import Task

# 连接联邦
sdk.agent_federation.connect()

# 创建并分发任务
task = Task(
    task_id="sales_analysis_001",
    description="分析Q1销售数据",
    priority=1,
    dependencies=[]
)
result = sdk.agent_federation.distribute_task(
    task=task,
    intent="数据分析"
)
print(f"分配给: {result.assigned_agent}")

# 列出Agent
agents = sdk.agent_federation.list_agents()
for agent in agents:
    print(f"{agent.name}: {agent.status.value}")

# 获取统计
stats = sdk.agent_federation.get_stats()
print(f"在线Agent: {stats['online_agents']}")
```

#### Agent路由策略

| 策略 | 说明 | 选择场景 |
|------|------|----------|
| `least_load` | 选择负载最低 | 负载均衡 |
| `round_robin` | 轮询选择 | 公平分发 |
| `intent_match` | 意图匹配 | 技能匹配 |
| `random` | 随机选择 | 测试环境 |

---

## 📖 API参考

### GhostHubSDK 类

<!-- AI-READY: GHOST_HUB_SDK_API -->
```python
class GhostHubSDK:
    """Ghost Hub SDK 统一入口"""

    def __init__(self, config: Optional[GhostHubConfig] = None):
        """初始化SDK"""
        pass

    # 属性
    @property
    def intention_bank(self) -> Optional[IntentionBankComponent]:
        """意图银行组件"""
        pass

    @property
    def no_ui_adapter(self) -> Optional[NoUIAdapterComponent]:
        """IoT适配器组件"""
        pass

    @property
    def agent_federation(self) -> Optional[AgentFederationComponent]:
        """智能体联邦组件"""
        pass

    # 方法
    def connect(self) -> Dict[str, bool]:
        """连接所有启用的组件"""
        pass

    def disconnect(self):
        """断开所有连接"""
        pass

    def get_stats(self) -> Dict[str, Any]:
        """获取全局统计"""
        pass

    def execute_workflow(self, intent_text: str, workflow_type: str = "default") -> Dict[str, Any]:
        """执行完整工作流"""
        pass

    def list_available_templates(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出可用模板"""
        pass
```

### 返回值结构

#### execute_workflow 返回

<!-- AI-READY: WORKFLOW_RESULT -->
```python
{
    "intent_text": str,           # 输入意图
    "workflow_type": str,         # 工作流类型
    "success": bool,             # 是否成功
    "intent_match": {            # 匹配结果
        "template_name": str,
        "template_id": str,
        "domain": str,
        "similarity": float,
        "confidence": float
    },
    "task_graph": {              # 任务图
        "tasks": [...],
        "task_count": int
    },
    "roi_estimate": dict,        # ROI估算
    "business_metrics": dict,   # 业务指标
    "errors": list               # 错误列表
}
```

---

## 💡 最佳实践

### 错误处理

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubError

sdk = GhostHubSDK()

try:
    result = sdk.execute_workflow("招聘流程")

    if not result["success"]:
        for error in result["errors"]:
            print(f"错误: {error}")
        return

    # 正常处理
    print(f"任务数: {result['task_graph']['task_count']}")

except GhostHubError as e:
    print(f"SDK错误: {e.code} - {e.message}")
except Exception as e:
    print(f"未知错误: {type(e).__name__}: {e}")
finally:
    sdk.disconnect()  # 始终清理
```

### 意图匹配最佳实践

```python
# 1. 总是检查 has_match
result = sdk.intention_bank.match_intent(user_input)
if not result.has_match:
    return {"error": "无法理解意图，请重新描述"}

# 2. 检查置信度阈值
if result.top_match.confidence < 0.5:
    return {"error": "置信度太低，请提供更多信息"}

# 3. 展示多个选项
for i, match in enumerate(result.matches[:3]):
    print(f"{i+1}. {match.template.name} ({match.confidence:.0%})")
```

### 连接复用

```python
# 推荐：复用SDK实例
sdk = GhostHubSDK()
sdk.connect()  # 建立连接

for query in user_queries:
    result = sdk.execute_workflow(query)

sdk.disconnect()  # 统一清理

# 不推荐：每次创建新实例
for query in user_queries:
    sdk = GhostHubSDK()  # 每次都新建
    result = sdk.execute_workflow(query)
    sdk.disconnect()
```

---

## ⚡ 性能优化

### 1. 连接池配置

```python
from ghost_hub_sdk import GhostHubConfig

config = GhostHubConfig(
    # IoT适配器连接池
    no_ui_adapter_config={
        "pool_size": 10,
        "timeout": 30,
        "retry": 3
    },
    # 智能体联邦配置
    agent_federation_config={
        "heartbeat_interval": 10,
        "max_concurrent_tasks": 20
    }
)
```

### 2. 缓存配置

```python
config = GhostHubConfig(
    # 模板缓存
    intention_bank_config={
        "cache_templates": True,
        "cache_ttl": 3600  # 秒
    }
)
```

### 3. 并发处理

```python
from concurrent.futures import ThreadPoolExecutor

def process_intent(text):
    sdk = GhostHubSDK()
    result = sdk.execute_workflow(text)
    sdk.disconnect()
    return result

# 并发处理
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_intent, q) for q in queries]
    results = [f.result() for f in futures]
```

---

## 🔒 安全指南

### 认证配置

```python
from ghost_hub_sdk.security import SimpleAuth, AuthConfig

auth_config = AuthConfig(
    api_key="your-api-key",  # 生产环境使用环境变量
    rate_limit=100,  # 每分钟请求数
    whitelist=["192.168.1.0/24"]
)

auth = SimpleAuth(auth_config)
```

### 输入验证

```python
from ghost_hub_sdk.security import InputValidator

validator = InputValidator(
    max_length=1000,
    allowed_chars=" alphanumeric chinese punctuation",
    block_patterns=["sql_injection", "xss"]
)

# 验证用户输入
if not validator.validate(user_input):
    raise ValueError("输入包含非法字符")
```

### 敏感数据保护

```python
from ghost_hub_sdk.security import SensitiveDataProtector

protector = SensitiveDataProtector(
    patterns={
        "email": r"[\w.-]+@[\w.-]+\.\w+",
        "phone": r"\d{11}",
        "id_card": r"\d{17}[\dXx]"
    },
    mask_char="*"
)

safe_result = protector.protect(result)
```

---

## 🔄 迁移指南

### 从 v0.1.x 升级

#### API变化

| v0.1.x | v1.0.0 |
|--------|--------|
| `match.template_id` | `result.top_match.template.id` |
| `result.workflow_id` | `result.workflow_type` |
| `distribute_task(task, strategy)` | `distribute_task(task, intent)` |

#### 迁移步骤

```python
# v0.1.x
result = sdk.match_intent("招聘")
task_id = result.match.template_id

# v1.0.0
result = sdk.intention_bank.match_intent("招聘")
task_id = result.top_match.template.id
```

---

## 📚 相关文档

- [安装指南](./INSTALL_GUIDE.md) - 完整安装手册
- [快速开始](./QUICK_START.md) - 5分钟体验
- [使用场景](./SCENARIOS.md) - 真实案例

---

## 🆘 技术支持

| 渠道 | 地址 |
|------|------|
| 文档 | https://docs.ghosthub.dev |
| GitHub Issues | https://github.com/ghost-hub/sdk/issues |
| Email | support@ghosthub.dev |
