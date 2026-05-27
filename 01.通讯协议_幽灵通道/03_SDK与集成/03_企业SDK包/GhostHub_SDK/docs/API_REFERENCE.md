﻿# Ghost Hub SDK API Reference

> v1.0.0 | Enterprise AI Workflow Orchestration

---

## Table of Contents

1. [GhostHubSDK](#ghosthubsdk)
2. [GhostHubConfig](#ghosthubconfig)
3. [IntentionBankComponent](#intentionbankcomponent)
4. [NoUIAdapterComponent](#nouiadaptercomponent)
5. [AgentFederationComponent](#agentfederationcomponent)

---

## GhostHubSDK

Main SDK entry point for enterprise AI workflow orchestration.

### Constructor

```python
GhostHubSDK(config: Optional[GhostHubConfig] = None)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config` | GhostHubConfig | None | Configuration object |

### Methods

#### `execute_workflow(workflow_name: str, context: Optional[Dict] = None) -> Dict`

Execute a named workflow with optional context.

```python
sdk = GhostHubSDK()
result = sdk.execute_workflow("帮我优化面试流程")
```

**Parameters:**
- `workflow_name` (str): Name or description of the workflow
- `context` (Dict, optional): Additional context data

**Returns:** `Dict` containing workflow execution result

**Example Response:**
```json
{
  "workflow_id": "wf_abc123",
  "status": "success",
  "task_graph": {
    "task_count": 3,
    "tasks": [...]
  },
  "results": [...]
}
```

#### `connect() -> bool`

Establish connections to configured services.

```python
sdk.connect()
```

#### `disconnect() -> None`

Close all connections and cleanup resources.

```python
sdk.disconnect()
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `intention_bank` | IntentionBankComponent | Intent parsing component |
| `no_ui_adapter` | NoUIAdapterComponent | IoT adapter component |
| `agent_federation` | AgentFederationComponent | Multi-agent component |

---

## GhostHubConfig

Configuration for GhostHub SDK initialization.

### Constructor

```python
GhostHubConfig(
    intention_bank_enabled: bool = True,
    no_ui_adapter_enabled: bool = True,
    agent_federation_enabled: bool = True,
    log_level: str = "INFO",
    version: str = "1.0.0"
)
```

### Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `intention_bank_enabled` | bool | True | Enable intention bank |
| `no_ui_adapter_enabled` | bool | True | Enable IoT adapter |
| `agent_federation_enabled` | bool | True | Enable agent federation |
| `log_level` | str | "INFO" | Logging level |
| `version` | str | "1.0.0" | SDK version |

### Methods

#### `to_dict() -> Dict`

Convert configuration to dictionary.

```python
config = GhostHubConfig(log_level="DEBUG")
config_dict = config.to_dict()
```

---

## IntentionBankComponent

Handles intent parsing, template matching, and task decomposition.

### Constructor

```python
IntentionBankComponent(config: Optional[Dict] = None)
```

### Methods

#### `match_intent(user_input: str, domain: Optional[str] = None) -> IntentMatch`

Match user input against available templates.

```python
sdk = GhostHubSDK()
match = sdk.intention_bank.match_intent("优化招聘流程", domain="hr")
```

**Parameters:**
- `user_input` (str): User's natural language input
- `domain` (str, optional): Filter by domain (hr, iot, ops, finance)

**Returns:** `IntentMatch` object

#### `parse_intent(user_input: str) -> List[IntentVector]`

Parse user input into structured intent vectors.

```python
intents = sdk.intention_bank.parse_intent("优化招聘流程并发送通知")
```

#### `build_task_graph(intent: IntentMatch) -> Dict`

Build a task dependency graph from matched intent.

```python
task_graph = sdk.intention_bank.build_task_graph(match)
```

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `templates` | List[Template] | Available templates |
| `domains` | List[str] | Available domains |

---

## NoUIAdapterComponent

Handles IoT device integration and protocol adaptation.

### Constructor

```python
NoUIAdapterComponent(config: Optional[Dict] = None)
```

### Methods

#### `connect(protocol: str = "mqtt") -> bool`

Connect to IoT gateway.

```python
sdk = GhostHubSDK()
sdk.no_ui_adapter.connect(protocol="mqtt")
```

#### `convert_intent_to_command(intent: str, device_type: str) -> DeviceCommand`

Convert natural language intent to device command.

```python
command = sdk.no_ui_adapter.convert_intent_to_command("开灯", "light")
```

#### `send_command(command: DeviceCommand, device_id: str) -> CommandResult`

Send command to IoT device.

```python
result = sdk.no_ui_adapter.send_command(command, "light_001")
```

#### `execute_scene(scene_name: str) -> List[CommandResult]`

Execute a predefined scene.

```python
results = sdk.no_ui_adapter.execute_scene("离家模式")
```

#### `list_devices() -> List[Device]`

List all registered devices.

```python
devices = sdk.no_ui_adapter.list_devices()
```

#### `list_scenes() -> List[Scene]`

List all available scenes.

```python
scenes = sdk.no_ui_adapter.list_scenes()
```

### Supported Device Types

- `light` - Smart lights
- `thermostat` - Smart thermostats
- `lock` - Smart locks
- `camera` - Security cameras
- `sensor` - Environmental sensors
- `appliance` - Smart appliances

### Supported Protocols

- `mqtt` - MQTT broker
- `http` - REST API
- `websocket` - WebSocket
- `coap` - CoAP protocol

---

## AgentFederationComponent

Manages multi-agent collaboration and task distribution.

### Constructor

```python
AgentFederationComponent(config: Optional[Dict] = None)
```

### Methods

#### `distribute_task(task: FedTask, strategy: str = "round_robin") -> Dict`

Distribute task to available agents.

```python
result = sdk.agent_federation.distribute_task(
    task={"name": "数据分析", "data": {...}},
    strategy="load_balance"
)
```

#### `create_session(session_id: str, agents: List[str]) -> Session`

Create a collaborative session.

```python
session = sdk.agent_federation.create_session(
    session_id="collab_001",
    agents=["data_agent", "report_agent"]
)
```

#### `list_agents() -> List[Agent]`

List all registered agents.

```python
agents = sdk.agent_federation.list_agents()
```

#### `get_stats() -> Dict`

Get federation statistics.

```python
stats = sdk.agent_federation.get_stats()
```

### Distribution Strategies

| Strategy | Description |
|----------|-------------|
| `round_robin` | Distribute evenly |
| `load_balance` | Route to least busy agent |
| `capability_match` | Match task to agent capability |
| `affinity` | Route based on historical success |

---

## Data Models

### Template

```python
@dataclass
class Template:
    id: str
    name: str
    description: str
    domain: str
    patterns: List[str]
    tasks: List[Task]
    priority: int = 0
```

### IntentMatch

```python
@dataclass
class IntentMatch:
    template_id: str
    confidence: float
    matched_pattern: str
    tasks: List[Task]
```

### DeviceCommand

```python
@dataclass
class DeviceCommand:
    device_id: str
    action: str
    parameters: Dict[str, Any]
    protocol: str
    timestamp: datetime
```

### Agent

```python
@dataclass
class Agent:
    id: str
    name: str
    capabilities: List[str]
    status: str
    current_load: float
```

---

## Error Handling

All methods may raise `GhostHubError` for general errors:

```python
try:
    sdk.execute_workflow("test")
except GhostHubError as e:
    print(f"SDK Error: {e}")
```

### Error Types

| Error | Description |
|-------|-------------|
| `GhostHubError` | General SDK error |
| `ConnectionError` | Failed to connect |
| `TimeoutError` | Operation timed out |
| `ValidationError` | Invalid input |
| `AuthenticationError` | Auth failed |

---

## Examples

See `demos/` directory for complete examples.
