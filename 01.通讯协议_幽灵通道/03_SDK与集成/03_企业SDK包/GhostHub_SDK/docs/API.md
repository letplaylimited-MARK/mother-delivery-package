# Ghost Hub SDK v1.0.0 - API Documentation

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core SDK](#core-sdk)
3. [Components](#components)
4. [Security Module](#security-module)
5. [Memory Layer](#memory-layer)
6. [Storage](#storage)
7. [Protocols](#protocols)
8. [API Reference](#api-reference)

---

## Quick Start

### Installation

```bash
pip install ghost-hub-sdk
```

### Basic Usage

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

# Initialize
config = GhostHubConfig()
sdk = GhostHubSDK(config)

# Execute workflow
result = sdk.execute_workflow("打开客厅灯")

# Check result
if result["success"]:
    print(f"执行成功: {result['message']}")
```

---

## Core SDK

### GhostHubSDK

Main SDK class for workflow orchestration.

#### Constructor

```python
GhostHubSDK(config: Optional[GhostHubConfig] = None)
```

#### Methods

##### `execute_workflow(intent_text: str) -> Dict[str, Any]`

Execute a workflow based on intent text.

**Parameters:**
- `intent_text` (str): Natural language intent

**Returns:**
```python
{
    "success": bool,
    "message": str,
    "workflow_id": str,
    "tasks": List[Dict],
    "execution_time": float
}
```

##### `get_available_templates() -> List[Dict]`

Get all available workflow templates.

##### `get_template_info(template_id: str) -> Optional[Dict]`

Get information about a specific template.

---

### GhostHubConfig

Configuration class for SDK initialization.

```python
@dataclass
class GhostHubConfig:
    storage_path: str = "ghost_hub_data"
    log_level: str = "INFO"
    enable_cache: bool = True
    max_history: int = 1000
    similarity_threshold: float = 0.7
```

---

## Components

### IntentionBankComponent

Handles intent recognition and matching.

```python
from ghost_hub_sdk.components import IntentionBankComponent

bank = IntentionBankComponent()

# Parse intent
result = bank.parse_intent("打开客厅灯")
# Returns: {"template_id": "...", "template_name": "...", "similarity": 0.95}
```

### NoUIAdapterComponent

Executes commands on devices without UI.

```python
from ghost_hub_sdk.components import NoUIAdapterComponent

adapter = NoUIAdapterComponent()

# Send command
result = adapter.send_command("light_001", "turn_on", brightness=80)
```

### AgentFederationComponent

Manages multi-agent collaboration.

```python
from ghost_hub_sdk.components import AgentFederationComponent

federation = AgentFederationComponent()

# Create task
task = federation.create_task("complex_task", agents=["agent1", "agent2"])
```

---

## Security Module

### SimpleAuth

API Key authentication.

```python
from ghost_hub_sdk.security import SimpleAuth, AuthConfig

auth = SimpleAuth(AuthConfig())

# Generate API Key
key = auth.generate_api_key()
auth.add_api_key(key, "user_name", permissions=["read", "write"])

# Validate
info = auth.validate_api_key(key)
# Returns: {"name": "user_name", "permissions": [...], "created_at": ...}

# Check permission
if auth.has_permission(key, "admin"):
    print("Has admin access")
```

### InputValidator

Input validation and sanitization.

```python
from ghost_hub_sdk.security import InputValidator

# Validate command
if InputValidator.validate_command("turn_on"):
    print("Valid command")

# Validate device ID
if InputValidator.validate_device_id("dev_001"):
    print("Valid device ID")

# Validate intent text
if InputValidator.validate_intent_text("打开灯光"):
    print("Valid intent")

# Validate parameters
params = InputValidator.validate_params(
    {"temperature": 25, "unknown": "value"},
    ["temperature", "brightness"]
)
# Returns: {"temperature": 25}  (unknown removed)

# Sanitize text
safe = InputValidator.sanitize_text(user_input, max_length=500)
```

### RateLimiter

Request rate limiting.

```python
from ghost_hub_sdk.security import RateLimiter

limiter = RateLimiter(requests_per_minute=60, burst=10)

# Check rate limit
if limiter.check("client_key"):
    print("Request allowed")
else:
    print("Rate limited")

# Get remaining requests
remaining = limiter.get_remaining("client_key")

# Reset limit
limiter.reset("client_key")

# Get stats
stats = limiter.get_stats()
```

### SensitiveDataProtector

Data masking and protection.

```python
from ghost_hub_sdk.security import SensitiveDataProtector

# Mask dictionary
data = {"password": "secret123", "api_key": "sk-abc123"}
masked = SensitiveDataProtector.mask_dict(data)
# Returns: {"password": "se*****23", "api_key": "sk-a*******23"}

# Mask string
masked_str = SensitiveDataProtector.mask_string("sk-secret-key-123")
# Returns: "sk-s***************23"

# Safe log
log = SensitiveDataProtector.safe_log("User login", {"password": "secret"})
# Returns: "User login | data: {'password': 'se***et'}"
```

### SecurityChecker

Security configuration checking.

```python
from ghost_hub_sdk.security import SecurityChecker

issues = SecurityChecker.check_all()
# Returns list of security issues

for issue in issues:
    print(f"[{issue['severity']}] {issue['check']}: {issue['message']}")
```

---

## Memory Layer

### GhostHubMemory

Persistent memory with context management.

```python
from ghost_hub_sdk.memory import GhostHubMemory

memory = GhostHubMemory()

# Record intent
memory.record_intent("打开客厅灯", {
    "template_id": "lighting",
    "success": True
})

# Get intent history
history = memory.get_intent_history(limit=10)

# Record device command
memory.record_device_command(
    device_id="light_001",
    device_name="客厅灯",
    command="turn_on",
    params={"brightness": 80},
    success=True
)

# Learn preference
memory.learn_preference("user.brightness", 75)
brightness = memory.get_preference("user.brightness", default=50)

# Set context
memory.set_context("current_room", "living_room")
room = memory.get_context("current_room")

# Get full context
context = memory.get_full_context()

# Get stats
stats = memory.get_stats()
```

---

## Storage

### JSONStorage

JSON file-based storage.

```python
from ghost_hub_sdk.storage import JSONStorage

storage = JSONStorage("data.json")

# Set value
storage.set("key", {"data": "value"})

# Get value
value = storage.get("key")

# Check exists
if storage.exists("key"):
    print("Key exists")

# Delete
storage.delete("key")

# List keys
keys = storage.list_keys("user_*")

# Get stats
stats = storage.get_stats()
```

### SQLiteStorage

SQLite database storage.

```python
from ghost_hub_sdk.storage import SQLiteStorage

storage = SQLiteStorage("data.db")

# Set value
storage.set("key", {"data": "value"})

# Get value
value = storage.get("key")

# Query by pattern
results = storage.query("SELECT * FROM storage WHERE key LIKE ?", ["user_%"])

# Batch operations
storage.batch_set([
    ("key1", {"data": "value1"}),
    ("key2", {"data": "value2"})
])

# Version control
storage.save_version("key")
versions = storage.get_versions("key")
storage.restore_version("key", "version_id")

# Stats
stats = storage.get_stats()
```

---

## Protocols

### MQTTClient

MQTT protocol client.

```python
from ghost_hub_sdk.protocols import MQTTClient

client = MQTTClient(
    broker="mqtt.example.com",
    port=1883,
    client_id="ghost_hub_client"
)

# Connect
client.connect()

# Subscribe
client.subscribe("home/+/status")

# Publish
client.publish("home/living_room/light", {"state": "on"})

# Callback
def on_message(topic, payload):
    print(f"Received on {topic}: {payload}")

client.set_callback(on_message)

# Loop
client.loop_start()
```

### WebSocketClient

WebSocket protocol client.

```python
from ghost_hub_sdk.protocols import WebSocketClient

client = WebSocketClient("wss://example.com/ws")

# Connect
client.connect()

# Send
client.send({"type": "subscribe", "channel": "updates"})

# Receive
message = client.receive()

# Callback
def on_message(data):
    print(f"Received: {data}")

client.set_callback(on_message)
```

---

## API Reference

### REST API Endpoints

When using `api/secure_api.py`:

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/api/health` | GET | Health check | No |
| `/api/secure/intent` | POST | Secure intent parsing | Yes |
| `/api/secure/device/command` | POST | Device control | Yes |
| `/api/admin/keys` | GET | List API keys | Admin |
| `/api/admin/keys/generate` | POST | Generate API key | Admin |
| `/api/security/check` | GET | Security check | No |

### Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (missing/invalid API key) |
| 403 | Forbidden (insufficient permissions) |
| 429 | Too Many Requests (rate limited) |
| 500 | Internal Server Error |

---

## Examples

### Complete Workflow Example

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig
from ghost_hub_sdk.security import SimpleAuth, RateLimiter

# Initialize
config = GhostHubConfig(log_level="DEBUG")
sdk = GhostHubSDK(config)
auth = SimpleAuth()
limiter = RateLimiter(requests_per_minute=60)

# Create API key
api_key = auth.generate_api_key()
auth.add_api_key(api_key, "demo_user", permissions=["read", "write"])

# Check rate limit
client_key = "demo_client"
if not limiter.check(client_key):
    print("Rate limited")
    exit(1)

# Execute workflow
result = sdk.execute_workflow("打开客厅灯并调暗到50%")

print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
```

### Multi-Agent Collaboration

```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()

# Create collaborative workflow
result = sdk.execute_workflow("帮我安排一个会议，需要邮件和日历两个智能体协作")

print(f"Workflow ID: {result['workflow_id']}")
print(f"Tasks: {len(result['tasks'])}")
```

---

## Version History

### v1.0.0 (Current)
- Added workflow engine
- Added memory layer
- Added knowledge layer
- Added storage layer
- Added MQTT/WebSocket protocols
- Added security module

### v0.1.0
- Initial release
- Basic intent parsing
- Device control
- Agent federation
