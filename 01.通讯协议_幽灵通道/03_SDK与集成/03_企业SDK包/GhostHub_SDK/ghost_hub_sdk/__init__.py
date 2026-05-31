"""Source-tree import shim for Ghost Hub SDK tests.

The package is distributed with ``package-dir = {"ghost_hub_sdk" = "."}``,
so editable installs import the repository root as ``ghost_hub_sdk``. A
fresh checkout without editable install still needs to import the current
source tree during tests; extending ``__path__`` to the parent directory keeps
those imports local to this checkout.
"""

from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
__path__.append(str(_ROOT))

from .core import GhostHubConfig, GhostHubSDK
from .components import (
    Agent,
    AgentFederationComponent,
    CommandResult,
    Device,
    DeviceCommand,
    FedTask,
    IntentMatch,
    IntentVector,
    IntentionBankComponent,
    MatchResult,
    Message,
    NoUIAdapterComponent,
    Scene,
    Session,
    Task,
    Template,
)

try:
    from .workflow_engine import GhostHubWorkflowEngine, TaskType, WorkflowStatus
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
        AuthConfig,
        InputValidator,
        RateLimiter,
        SecurityChecker,
        SensitiveDataProtector,
        SimpleAuth,
    )
except ImportError:
    pass

try:
    from .protocols import (
        MQTTClient,
        MQTTConnectionConfig,
        WebSocketClient,
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
