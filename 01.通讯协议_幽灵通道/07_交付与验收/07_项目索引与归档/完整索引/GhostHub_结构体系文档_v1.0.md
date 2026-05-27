﻿# Ghost Hub 结构体系文档

**版本**: v1.0  
**日期**: 2026-04-15  
**用途**: 完整阐述Ghost Hub / QCM的代码结构、目录组织、模块关系与依赖管理

---

## 一、整体目录结构

### 1.1 项目根结构

```
幽灵通道_v1.0/
│
├── 00_总导航/                    # 导航入口
├── 01_学术研究包/               # 论文、白皮书、协议
├── 02_开源社区包/               # ghost-channel开源
├── 03_企业SDK包/                # GhostHub SDK ⭐
├── 04_商业部署包/               # 授权、部署、监控
├── 05_开发者资源/               # 指南、API、示例
├── 06_场景化指南/               # HR、IoT、Agent场景
├── 07_项目索引与归档/           # 索引、演进历史
└── 99_待办与行动/               # 下一步行动
```

### 1.2 SDK核心结构

```
ghost_hub_sdk/
│
├── __init__.py                  # 统一入口 (v1.0.0)
├── core.py                      # GhostHubSDK核心类
├── config.py                    # GhostHubConfig配置
├── workflow_engine.py           # 工作流引擎
│
├── components/                   # ⭐三大核心组件
│   ├── __init__.py             # 组件导出
│   ├── intention_bank.py       # 意图银行
│   ├── no_ui_adapter.py        # 无UI适配器
│   └── agent_federation.py      # 智能体联邦
│
├── memory.py                    # 记忆层
├── knowledge.py                 # 知识层
├── storage.py                   # 持久化存储
├── security.py                  # 安全模块
├── database.py                  # 数据库模块
│
├── protocols/                   # 协议实现
│   ├── __init__.py
│   ├── mqtt_client.py          # MQTT客户端
│   └── websocket_client.py     # WebSocket客户端
│
├── templates/                   # ⭐22个业务模板
│   ├── index.json              # 模板索引
│   ├── hr_interview_optimize.json
│   ├── iot_smart_home.json
│   ├── ops_ticket_resolution.json
│   └── ... (20+ more)
│
├── demos/                       # ⭐演示示例
│   ├── demo_security.py
│   ├── demo_boundary.py
│   ├── demo_concurrency.py
│   ├── demo_user_scenarios.py
│   └── demo_final_verification.py
│
├── docs/                        # ⭐完整文档
│   ├── API.md
│   ├── USER_MANUAL.md
│   ├── EXAMPLES.md
│   └── USER_SCENARIOS.md
│
├── tests/                       # ⭐完整测试
│   └── test_sdk.py
│
├── api/                         # REST API
├── web/                         # Web界面
│
├── pyproject.toml               # ⭐Python项目配置
├── README.md                    # SDK说明
├── SETUP_GUIDE.md              # 部署指南
└── QUALITY_REPORT.md           # 质量报告
```

---

## 二、模块依赖关系

### 2.1 依赖图

```
                    ┌─────────────────────┐
                    │   GhostHubSDK       │
                    │     (core.py)       │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ IntentionBank│   │ NoUIAdapter │   │AgentFederation│
    └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
  │   Memory    │     │  Storage    │     │   Security  │
  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Protocols        │
                    │ (MQTT/WebSocket)   │
                    └─────────────────────┘
```

### 2.2 模块职责

| 模块 | 文件 | 职责 | 对外依赖 |
|------|------|------|----------|
| **核心** | core.py | 统一入口、组件管理 | components |
| **配置** | config.py | 配置管理、序列化 | 无 |
| **工作流** | workflow_engine.py | 任务编排、执行 | components |
| **意图银行** | intention_bank.py | 意图解析、模板匹配 | 无 |
| **无UI适配器** | no_ui_adapter.py | 设备控制、协议转换 | 无 |
| **智能体联邦** | agent_federation.py | Agent管理、路由分发 | 无 |
| **记忆** | memory.py | 偏好/上下文存储 | 无 |
| **知识** | knowledge.py | 实体/关系管理 | 无 |
| **存储** | storage.py | JSON/SQLite持久化 | 无 |
| **安全** | security.py | 认证/限流/验证 | 无 |
| **协议** | protocols/ | MQTT/WebSocket | paho-mqtt, websocket |

---

## 三、入口与导出

### 3.1 主入口 (__init__.py)

```python
"""
Ghost Hub SDK - 统一入口

v1.0.0 模块:
- core: GhostHubSDK核心
- components: 意图银行/无UI适配器/智能体联邦
- workflow_engine: 工作流引擎
- memory: 记忆层
- knowledge: 知识层
- storage: 存储层
- security: 安全层
- protocols: MQTT/WebSocket协议
"""

from .core import GhostHubSDK, GhostHubConfig
from .components import (
    IntentionBankComponent,
    NoUIAdapterComponent,
    AgentFederationComponent,
    Template, Task, IntentMatch, MatchResult,
    Device, DeviceCommand, CommandResult,
    Scene, Agent, Message, Session, FedTask,
    IntentVector,
)

__version__ = "1.0.0"
__all__ = [
    "GhostHubSDK", "GhostHubConfig",
    "IntentionBankComponent", "NoUIAdapterComponent", "AgentFederationComponent",
    "Template", "Task", "IntentMatch", "MatchResult",
    "Device", "DeviceCommand", "CommandResult",
    "Scene", "Agent", "Message", "Session", "FedTask",
    "IntentVector",
]
```

### 3.2 组件导出 (components/__init__.py)

```python
"""
组件模块 - 自包含实现

导出:
- IntentionBankComponent: 意图银行
- NoUIAdapterComponent: 无UI适配器
- AgentFederationComponent: 智能体联邦
"""

from .intention_bank import (
    IntentionBankComponent, IntentVector, Template, Task,
    IntentMatch, MatchResult, IntentParser, IntentMatcher,
    TemplateLoader, SemanticSimilarity, TaskGraphBuilder,
)
from .no_ui_adapter import (
    NoUIAdapterComponent, Device, DeviceCommand, CommandResult,
    BatchCommandResult, Scene, DeviceType, DeviceProtocol,
    IntentCommandEngine, HTTPAdapter, MQTTAdapter, WebSocketAdapter,
    SceneManager,
)
from .agent_federation import (
    AgentFederationComponent, Agent, Message, Session,
    IntentRoute, Task, TaskDistributionResult, AggregatedResult,
    AgentStatus, MessageType, RoutingStrategy,
    ServiceRegistry, Router, MessageProtocol,
    TaskDistributor, ResultAggregator,
)
```

---

## 四、配置管理

### 4.1 GhostHubConfig

```python
@dataclass
class GhostHubConfig:
    name: str = "GhostHub"
    version: str = "1.0.0"
    
    # 组件开关
    intention_bank_enabled: bool = True
    no_ui_adapter_enabled: bool = True
    agent_federation_enabled: bool = True
    
    # 组件配置
    intention_bank_config: Dict[str, Any] = field(default_factory=lambda: {
        "match_threshold": 0.3,
        "max_results": 5,
        "storage_type": "json",
    })
    
    no_ui_adapter_config: Dict[str, Any] = field(default_factory=lambda: {
        "default_protocol": "http"
    })
    
    agent_federation_config: Dict[str, Any] = field(default_factory=lambda: {
        "agent_id": "ghost-hub-sdk",
        "agent_name": "GhostHubSDK",
    })
    
    log_level: str = "INFO"
    enable_metrics: bool = True
```

### 4.2 快速配置

```python
# 最小配置
config = GhostHubConfig()

# 自定义配置
config = GhostHubConfig(
    intention_bank_enabled=True,
    no_ui_adapter_enabled=True,
    agent_federation_enabled=True,
    intention_bank_config={"match_threshold": 0.5},
)

# 文件配置
config = GhostHubConfig.from_dict({
    "name": "MyGhostHub",
    "version": "1.0.0",
    "intention_bank_enabled": True,
})
```

---

## 五、数据模型

### 5.1 意图银行数据模型

```
IntentVector
├── urgency: float (0-1)
├── complexity: float (0-1)
├── autonomy: float (0-1)
├── cooperation: float (0-1)
├── risk_tolerance: float (0-1)
└── domain: str

Template
├── id: str
├── name: str
├── domain: str
├── description: str
├── intent_patterns: List[str]
├── intent_vector: IntentVector
├── tasks: List[Task]
├── business_metrics: Dict
├── roi_estimate: Dict
└── tags: List[str]

Task
├── id: str
├── name: str
├── description: str
├── sequence: int
├── dependencies: List[str]
├── estimated_time: str
└── tools: List[str]
```

### 5.2 无UI适配器数据模型

```
Device
├── id: str
├── name: str
├── device_type: DeviceType (LIGHT/THERMOSTAT/SWITCH/...)
├── protocol: DeviceProtocol (HTTP/MQTT/WebSocket/...)
├── address: str
├── state: Dict
└── capabilities: List[str]

DeviceCommand
├── device_id: str
├── command: str
├── params: Dict
└── timestamp: float

Scene
├── id: str
├── name: str
├── description: str
├── commands: List[Dict]
└── trigger_conditions: Dict
```

### 5.3 智能体联邦数据模型

```
Agent
├── agent_id: str
├── name: str
├── capabilities: List[str]
├── status: AgentStatus (ONLINE/OFFLINE/BUSY/IDLE)
├── load: float (0-1)
├── intent_keywords: List[str]
└── last_heartbeat: float

Message
├── id: str
├── sender_id: str
├── receiver_id: Optional[str]
├── msg_type: MessageType (REQUEST/RESPONSE/BROADCAST/...)
├── content: str
├── payload: Dict
├── timestamp: float
└── correlation_id: Optional[str]

Session
├── id: str
├── task: str
├── participants: List[str]
├── status: str (active/completed)
├── created_at: float
├── messages: List[Message]
└── results: Dict
```

---

## 六、API设计

### 6.1 GhostHubSDK主API

```python
class GhostHubSDK:
    def __init__(self, config: Optional[GhostHubConfig] = None)
    
    # 组件访问
    @property
    def intention_bank(self) -> Optional[IntentionBankComponent]
    
    @property
    def no_ui_adapter(self) -> Optional[NoUIAdapterComponent]
    
    @property
    def agent_federation(self) -> Optional[AgentFederationComponent]
    
    # 连接管理
    def connect(self) -> Dict[str, bool]
    def disconnect(self)
    
    # 工作流
    def execute_workflow(self, intent_text: str, workflow_type: str = "default") -> Dict
    
    # 统计
    def get_stats(self) -> Dict[str, Any]
```

### 6.2 意图银行API

```python
class IntentionBankComponent:
    def match_intent(self, text: str) -> MatchResult
    def match_multi_intent(self, text: str) -> MultiIntentResult
    def build_task_graph(self, template: Template) -> TaskGraph
    def list_templates(self, domain: Optional[str] = None) -> List[Template]
    def get_template(self, template_id: str) -> Optional[Template]
    def get_stats(self) -> Dict[str, Any]
```

### 6.3 无UI适配器API

```python
class NoUIAdapterComponent:
    def connect(self, protocol: Optional[str] = None) -> bool
    def disconnect()
    def send_command(self, device_id: str, command: str, **kwargs) -> CommandResult
    def send_batch_commands(self, commands: List[Dict]) -> BatchCommandResult
    def execute_scene(self, scene_id: str) -> BatchCommandResult
    def convert_intent_to_command(self, intent: str, device_type: str = "unknown") -> str
    def list_devices(self, device_type: Optional[DeviceType] = None) -> List[Device]
```

### 6.4 智能体联邦API

```python
class AgentFederationComponent:
    def connect(self) -> bool
    def disconnect()
    def find_agent(self, intent: str) -> Optional[Agent]
    def route_intent(self, intent: str) -> Optional[IntentRoute]
    def distribute_task(self, task: FedTask, intent: str = "") -> TaskDistributionResult
    def distribute_tasks(self, tasks: List[FedTask], intents: List[str] = None) -> List[TaskDistributionResult]
    def aggregate_results(self, tasks: List[FedTask]) -> AggregatedResult
    def list_agents(self, status: Optional[AgentStatus] = None) -> List[Agent]
```

---

## 七、扩展机制

### 7.1 自定义模板

```python
from ghost_hub_sdk import GhostHubSDK, Template, Task, IntentVector

sdk = GhostHubSDK()

# 添加自定义模板
custom_template = Template(
    id="custom_001",
    name="自定义流程",
    domain="custom",
    description="用户自定义业务模板",
    intent_patterns=["自定义", "我的流程"],
    intent_vector=IntentVector(0.5, 0.5, 0.5, 0.5, 0.5, "custom"),
    tasks=[
        Task("c1", "步骤1", "第一步操作", 1),
        Task("c2", "步骤2", "第二步操作", 2, ["c1"]),
    ],
)

sdk.intention_bank._templates.append(custom_template)
```

### 7.2 自定义设备

```python
from ghost_hub_sdk import GhostHubSDK, Device, DeviceType, DeviceProtocol

sdk = GhostHubSDK()

# 添加自定义设备
custom_device = Device(
    id="custom_dev_001",
    name="我的设备",
    device_type=DeviceType.CUSTOM,
    protocol=DeviceProtocol.HTTP,
    address="http://192.168.1.200",
    capabilities=["on", "off", "status"],
)

sdk.no_ui_adapter.add_device(custom_device)
```

### 7.3 自定义Agent

```python
from ghost_hub_sdk import GhostHubSDK, Agent, AgentStatus

sdk = GhostHubSDK()

# 注册自定义Agent
custom_agent = Agent(
    agent_id="custom_agent",
    name="自定义Agent",
    capabilities=["自定义处理"],
    status=AgentStatus.ONLINE,
    intent_keywords=["自定义", "特殊"],
)

sdk.agent_federation.register_agent(custom_agent)
```

---

## 八、部署架构

### 8.1 开发环境

```
┌─────────────────┐
│   开发机器      │
│  (localhost)    │
├─────────────────┤
│ Python 3.8+     │
│ pip install -e . │
│                  │
│ ┌─────────────┐ │
│ │ GhostHubSDK │ │
│ │ (本地调试)  │ │
│ └─────────────┘ │
└─────────────────┘
```

### 8.2 生产环境

```
                    ┌─────────────────┐
                    │   负载均衡器     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌─────────┐    ┌─────────┐    ┌─────────┐
        │ GhostHub│    │ GhostHub│    │ GhostHub│
        │ Server 1│    │ Server 2│    │ Server 3│
        └────┬────┘    └────┬────┘    └────┬────┘
             │              │              │
             └──────────────┼──────────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        ┌─────────┐   ┌─────────┐   ┌─────────┐
        │  Redis  │   │ Postgre │   │ S3/OSS  │
        │ (缓存)   │   │ SQL(存储)│   │ (文件)  │
        └─────────┘   └─────────┘   └─────────┘
```

### 8.3 Docker部署

```yaml
# docker-compose.yml
version: '3.8'
services:
  ghost-hub:
    image: ghosthub/server:latest
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://postgres:password@db:5432/ghosthub
    depends_on:
      - redis
      - db

  redis:
    image: redis:7-alpine

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=ghosthub
```

---

## 九、测试结构

### 9.1 测试组织

```
tests/
├── test_sdk.py                 # 核心SDK测试
├── test_intention_bank.py      # 意图银行测试
├── test_no_ui_adapter.py       # 无UI适配器测试
├── test_agent_federation.py    # 智能体联邦测试
├── test_security.py            # 安全测试
└── test_integration.py         # 集成测试
```

### 9.2 测试示例

```python
import pytest
from ghost_hub_sdk import GhostHubSDK

class TestGhostHubSDK:
    def test_basic_initialization(self):
        sdk = GhostHubSDK()
        assert sdk.config.name == "GhostHub"
        assert sdk.config.version == "1.0.0"
    
    def test_intention_bank(self):
        sdk = GhostHubSDK()
        result = sdk.intention_bank.match_intent("优化面试流程")
        assert result.has_match
        assert result.top_match.similarity > 0.3
```

---

*本文档是Ghost Hub结构体系的完整阐述，配套文档包括：*
- *价值体系: `GhostHub_价值体系文档_v1.0.md`*
- *功能体系: `GhostHub_功能体系文档_v1.0.md`*
