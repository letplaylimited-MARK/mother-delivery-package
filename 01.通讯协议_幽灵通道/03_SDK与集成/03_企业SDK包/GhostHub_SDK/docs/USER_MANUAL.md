# Ghost Hub SDK v1.0.0 - User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [Workflows](#workflows)
6. [Components](#components)
7. [Security](#security)
8. [Memory & Storage](#memory--storage)
9. [Protocols](#protocols)
10. [Configuration](#configuration)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#faq)

---

## Introduction

Ghost Hub SDK is an enterprise-grade AI workflow orchestration framework. It integrates three core components:

- **Intention Bank**: Natural language intent recognition and matching
- **NoUI Adapter**: Execute commands on devices without UI interfaces
- **Agent Federation**: Multi-agent collaboration and task coordination

### Key Features

- Natural language workflow execution
- Component-based architecture
- Built-in security (API keys, rate limiting, input validation)
- Persistent memory and storage
- Multiple protocol support (MQTT, WebSocket)
- Thread-safe concurrent operations

---

## Installation

### Requirements

- Python 3.8+
- pip

### Install from PyPI

```bash
pip install ghost-hub-sdk
```

### Install from Source

```bash
git clone https://github.com/your-org/ghost-hub-sdk.git
cd ghost-hub-sdk
pip install -e .
```

### Dependencies

The SDK requires:
- fastapi
- uvicorn
- paho-mqtt (for MQTT)
- websockets
- aiohttp

---

## Quick Start

### Your First Workflow

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

# Create SDK instance
config = GhostHubConfig()
sdk = GhostHubSDK(config)

# Execute a workflow with natural language
result = sdk.execute_workflow("打开客厅的灯")

# Check the result
if result["success"]:
    print(f"✓ {result['message']}")
else:
    print(f"✗ Error: {result.get('error', 'Unknown error')}")
```

### Output Example

```
✓ Workflow executed successfully
  Workflow ID: wf_abc123
  Tasks completed: 2
  Execution time: 0.045s
```

---

## Core Concepts

### Intent

An intent is a natural language description of what the user wants to do.

Examples:
- "打开客厅灯"
- "Turn on the bedroom light"
- "调节温度到25度"
- "Schedule a meeting for tomorrow"

### Template

A template defines a workflow pattern that can match multiple intents.

```json
{
  "template_id": "lighting_control",
  "template_name": "灯光控制",
  "patterns": ["打开*灯", "关闭*灯", "调暗*"],
  "tasks": [...]
}
```

### Workflow

A workflow is an execution instance of a matched template.

```python
{
    "workflow_id": "wf_xyz789",
    "template_id": "lighting_control",
    "intent_text": "打开客厅灯",
    "tasks": [...],
    "success": True,
    "execution_time": 0.023
}
```

### Component

Components are the building blocks that execute different aspects of a workflow:

| Component | Purpose |
|-----------|---------|
| IntentionBank | Parse and match user intents |
| NoUIAdapter | Send commands to devices |
| AgentFederation | Coordinate multi-agent tasks |

---

## Workflows

### Available Templates

The SDK includes 22 pre-built templates:

| Template | Description |
|----------|-------------|
| lighting_control | 灯光控制 |
| climate_control | 温控管理 |
| security_system | 安防系统 |
| entertainment | 娱乐控制 |
| voice_assistant | 语音助手 |
| smart_appliances | 智能家电 |
| scene_control | 场景控制 |
| energy_management | 能源管理 |
| home_automation | 家居自动化 |
| multi_room_audio | 多房间音频 |
| window_blinds | 窗帘控制 |
| irrigation_system | 灌溉系统 |
| pet_care | 宠物护理 |
| health_monitoring | 健康监测 |
| garage_control | 车库控制 |
| door_lock | 门锁管理 |
| notification_system | 通知系统 |

### Custom Templates

Add your own templates:

```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()

# Get template directory
templates = sdk.get_available_templates()

# Add custom template
sdk.add_template({
    "template_id": "my_custom_workflow",
    "template_name": "自定义工作流",
    "patterns": ["做某事", "执行任务"],
    "tasks": [...]
})
```

---

## Components

### IntentionBankComponent

Handles intent recognition:

```python
from ghost_hub_sdk.components import IntentionBankComponent

bank = IntentionBankComponent()

# Parse an intent
result = bank.parse_intent("打开客厅灯")

print(f"Matched template: {result['template_name']}")
print(f"Similarity: {result['similarity']:.2%}")
```

### NoUIAdapterComponent

Controls devices without UI:

```python
from ghost_hub_sdk.components import NoUIAdapterComponent

adapter = NoUIAdapterComponent()

# Send command
result = adapter.send_command(
    device_id="light_001",
    command="turn_on",
    brightness=80,
    color="warm_white"
)

if result.success:
    print(f"Command sent: {result.message}")
```

### AgentFederationComponent

Manages multi-agent tasks:

```python
from ghost_hub_sdk.components import AgentFederationComponent

federation = AgentFederationComponent()

# Create collaborative task
task = federation.create_task(
    name="schedule_meeting",
    agents=["calendar_agent", "email_agent", "notification_agent"]
)

# Execute
result = federation.execute_task(task)
```

---

## Security

### API Key Authentication

```python
from ghost_hub_sdk.security import SimpleAuth, AuthConfig

auth = SimpleAuth(AuthConfig())

# Generate a new API key
api_key = auth.generate_api_key()

# Add key with permissions
auth.add_api_key(
    api_key,
    name="my_app",
    permissions=["read", "write"]
)

# Validate key
info = auth.validate_api_key(api_key)
if info:
    print(f"Key belongs to: {info['name']}")
```

### Permission Levels

| Permission | Description |
|------------|-------------|
| read | Read-only access |
| write | Can modify data |
| admin | Full administrative access |

### Rate Limiting

```python
from ghost_hub_sdk.security import RateLimiter

limiter = RateLimiter(
    requests_per_minute=60,  # Normal rate
    burst=10                  # Allow bursts up to 10
)

# Check before processing
if limiter.check("client_123"):
    # Process request
    pass
else:
    print("Rate limited - try again later")
```

### Input Validation

```python
from ghost_hub_sdk.security import InputValidator

# Validate command
if not InputValidator.validate_command("turn_on"):
    raise ValueError("Invalid command")

# Validate device ID
if not InputValidator.validate_device_id(device_id):
    raise ValueError("Invalid device ID")

# Sanitize user input
safe_text = InputValidator.sanitize_text(user_input)
```

### Sensitive Data Protection

```python
from ghost_hub_sdk.security import SensitiveDataProtector

protector = SensitiveDataProtector()

# Mask sensitive fields in logs
log_data = {"username": "john", "password": "secret123"}
safe_log = protector.safe_log("User login", log_data)
# Output: "User login | data: {'username': 'john', 'password': 'se***23'}"

# Mask entire dictionary
masked = protector.mask_dict({"api_key": "sk-abc123"})
# Output: {"api_key": "sk-a*******23"}
```

---

## Memory & Storage

### Memory Layer

Persistent context across sessions:

```python
from ghost_hub_sdk.memory import GhostHubMemory

memory = GhostHubMemory()

# Record intent execution
memory.record_intent(
    "打开客厅灯",
    {"template_id": "lighting", "success": True}
)

# Learn user preferences
memory.learn_preference("user.lighting.brightness", 75)
memory.learn_preference("user.temperature", 24)

# Get preference with default
brightness = memory.get_preference("user.lighting.brightness", default=50)

# Store context data
memory.set_context("current_room", "living_room")

# Retrieve context
room = memory.get_context("current_room")
```

### Storage Options

#### JSON Storage (Simple)

```python
from ghost_hub_sdk.storage import JSONStorage

storage = JSONStorage("data.json")

# Store data
storage.set("key", {"data": "value"})

# Retrieve
data = storage.get("key")

# List keys
keys = storage.list_keys("user_*")
```

#### SQLite Storage (Advanced)

```python
from ghost_hub_sdk.storage import SQLiteStorage

storage = SQLiteStorage("app.db")

# Store with metadata
storage.set("user_settings", {"theme": "dark", "lang": "en"})

# Query
results = storage.query("SELECT * FROM storage WHERE key LIKE ?", ["user_%"])

# Version control
storage.save_version("user_settings")
versions = storage.get_versions("user_settings")
storage.restore_version("user_settings", versions[0])
```

---

## Protocols

### MQTT

Connect to IoT devices via MQTT:

```python
from ghost_hub_sdk.protocols import MQTTClient

client = MQTTClient(
    broker="mqtt.example.com",
    port=1883,
    client_id="my_client"
)

# Connect and subscribe
client.connect()
client.subscribe("home/+/status")

# Publish commands
client.publish("home/living_room/light", {"state": "on", "brightness": 80})

# Handle messages
def on_message(topic, payload):
    print(f"{topic}: {payload}")

client.set_callback(on_message)
client.loop_start()
```

### WebSocket

Real-time bidirectional communication:

```python
from ghost_hub_sdk.protocols import WebSocketClient

client = WebSocketClient("wss://api.example.com/ws")

client.connect()
client.send({"type": "subscribe", "channels": ["updates"]})

# Receive messages
while True:
    msg = client.receive()
    print(f"Received: {msg}")
```

---

## Configuration

### GhostHubConfig Options

```python
from ghost_hub_sdk import GhostHubConfig

config = GhostHubConfig(
    # Storage
    storage_path="ghost_hub_data",

    # Logging
    log_level="INFO",  # DEBUG, INFO, WARNING, ERROR

    # Performance
    enable_cache=True,
    max_history=1000,

    # Matching
    similarity_threshold=0.7,  # 0.0 to 1.0

    # Security
    enable_auth=True,
    rate_limit_per_minute=60,

    # Protocols
    mqtt_broker="mqtt.local",
    mqtt_port=1883,
)
```

### Environment Variables

```bash
# Optional environment configuration
export GHOST_HUB_STORAGE_PATH="./data"
export GHOST_HUB_LOG_LEVEL="DEBUG"
export GHOST_HUB_MQTT_BROKER="mqtt.example.com"
```

---

## Troubleshooting

### Common Issues

#### "Intent not matched"

**Cause**: Low similarity threshold or no matching template.

**Solution**: 
```python
# Increase threshold
config = GhostHubConfig(similarity_threshold=0.5)

# Or add custom template
sdk.add_template({
    "template_id": "my_template",
    "patterns": ["your pattern here"],
    ...
})
```

#### "Rate limited"

**Cause**: Too many requests in a short time.

**Solution**:
```python
# Check before processing
if limiter.check("client"):
    # Process
    pass
else:
    # Wait or queue
    time.sleep(1)
```

#### "Invalid device ID"

**Cause**: Device ID doesn't match expected format.

**Solution**: Use valid format (alphanumeric + underscore, max 64 chars):
```
✓ dev_001
✓ light_bedroom
✗ dev;rm -rf
✗ dev<script>
```

### Debug Mode

Enable detailed logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

config = GhostHubConfig(log_level="DEBUG")
sdk = GhostHubSDK(config)
```

---

## FAQ

### Q: How does intent matching work?

A: The IntentionBank uses pattern matching and similarity scoring. Each template has patterns (regex or keywords), and the SDK calculates similarity between the input intent and each pattern.

### Q: Can I add custom devices?

A: Yes! Use the NoUIAdapter's device registry:

```python
adapter = NoUIAdapterComponent()
adapter.register_device(
    device_id="my_device",
    device_type="custom",
    capabilities=["on_off", "adjust"]
)
```

### Q: Is the SDK thread-safe?

A: Yes! All core components are thread-safe. See `demo_concurrency.py` for tests.

### Q: How do I persist data?

A: Use the storage layer:
- `JSONStorage`: Simple file-based (good for small data)
- `SQLiteStorage`: Database (good for large data, queries)

### Q: Can I use custom protocols?

A: Yes! Implement the protocol interface:

```python
from ghost_hub_sdk.protocols import BaseProtocol

class MyProtocol(BaseProtocol):
    def connect(self): ...
    def disconnect(self): ...
    def send(self, data): ...
    def receive(self): ...
```

---

## Support

- **Documentation**: See `/docs` folder
- **Examples**: See `/demos` folder
- **Issues**: Report on GitHub
- **Email**: support@ghosthub.example.com

---

*Ghost Hub SDK v1.0.0 - Enterprise AI Workflow Orchestration*
