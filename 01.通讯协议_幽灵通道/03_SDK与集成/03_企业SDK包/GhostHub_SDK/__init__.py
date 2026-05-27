"""
Ghost Hub SDK - 统一入口

企业级AI工作流编排器
整合意图银行、无UI适配器、智能体联邦三大功能

v1.0.0 模块:
- core: 核心SDK
- components: 三大组件 (意图银行/无UI适配器/智能体联邦)
- workflow_engine: 工作流引擎(组件串联)
- memory: 记忆层
- knowledge: 知识层
- storage: 持久化存储
- protocols: MQTT/WebSocket协议
- security: 安全模块(认证/验证/脱敏/限流)
"""

from .core import GhostHubSDK, GhostHubConfig
from .components import (
    IntentionBankComponent,
    NoUIAdapterComponent,
    AgentFederationComponent,
    Template,
    Task,
    IntentMatch,
    MatchResult,
    Device,
    DeviceCommand,
    CommandResult,
    Scene,
    Agent,
    Message,
    Session,
    FedTask,
    IntentVector,
)

try:
    from .workflow_engine import GhostHubWorkflowEngine, WorkflowStatus, TaskType
except ImportError:
    pass

try:
    from .memory import GhostHubMemory, get_ghost_hub_memory
except ImportError:
    pass

try:
    from .knowledge import GhostHubKnowledge, get_ghost_hub_knowledge
except ImportError:
    pass

try:
    from .storage import JSONStorage, SQLiteStorage
except ImportError:
    pass

try:
    from .security import (
        SimpleAuth,
        InputValidator,
        RateLimiter,
        SensitiveDataProtector,
        SecurityChecker,
        AuthConfig,
    )
except ImportError:
    pass

try:
    from .protocols import (
        MQTTClient,
        WebSocketClient,
        MQTTConnectionConfig,
        WebSocketConfig,
    )
except ImportError:
    pass

__version__ = "1.0.0"
__all__ = [
    "GhostHubSDK",
    "GhostHubConfig",
    "IntentionBankComponent",
    "NoUIAdapterComponent",
    "AgentFederationComponent",
    "Template",
    "Task",
    "IntentMatch",
    "MatchResult",
    "Device",
    "DeviceCommand",
    "CommandResult",
    "Scene",
    "Agent",
    "Message",
    "Session",
    "FedTask",
    "IntentVector",
]
