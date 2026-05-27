# Ghost Hub SDK User Guide

> Complete guide to using Ghost Hub SDK in your applications

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Configuration](#configuration)
3. [Intention Bank](#intention-bank)
4. [IoT Integration](#iot-integration)
5. [Agent Federation](#agent-federation)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation

```bash
pip install ghost-hub-sdk
```

### Basic Usage

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

# Initialize SDK
sdk = GhostHubSDK()

# Execute a workflow
result = sdk.execute_workflow("帮我优化面试流程")

# Access results
print(f"Tasks created: {result['task_graph']['task_count']}")
```

---

## Configuration

### Minimal Configuration

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

config = GhostHubConfig(
    log_level="INFO"
)

sdk = GhostHubSDK(config)
```

### Full Configuration

```python
config = GhostHubConfig(
    intention_bank_enabled=True,
    no_ui_adapter_enabled=True,
    agent_federation_enabled=True,
    log_level="DEBUG"
)

sdk = GhostHubSDK(config)
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GHOST_HUB_LOG_LEVEL` | Logging level | INFO |
| `GHOST_HUB_CONFIG_PATH` | Config file path | None |

---

## Intention Bank

### Matching User Intent

```python
# Match a single intent
sdk = GhostHubSDK()
match = sdk.intention_bank.match_intent("优化招聘流程")

print(f"Confidence: {match.confidence}")
print(f"Template: {match.template_id}")
print(f"Tasks: {[t.name for t in match.tasks]}")
```

### Domain Filtering

```python
# Filter by domain
hr_match = sdk.intention_bank.match_intent(
    "绩效考核", 
    domain="hr"
)

iot_match = sdk.intention_bank.match_intent(
    "温度调节", 
    domain="iot"
)
```

### Available Domains

| Domain | Description | Templates |
|--------|-------------|-----------|
| `hr` | Human Resources | recruitment, onboarding, review |
| `iot` | IoT Control | smart_home, industrial |
| `ops` | Operations | ticketing, monitoring |
| `finance` | Finance | invoicing, expense |

### Building Task Graphs

```python
# Get matched intent
match = sdk.intention_bank.match_intent("优化招聘流程")

# Build task graph
task_graph = sdk.intention_bank.build_task_graph(match)

# Access graph structure
for task in task_graph['tasks']:
    print(f"{task['name']}: {task['status']}")
```

---

## IoT Integration

### Connecting to IoT Gateway

```python
# Initialize adapter
sdk = GhostHubSDK()
sdk.no_ui_adapter.connect(protocol="mqtt")

# Or use HTTP
sdk.no_ui_adapter.connect(protocol="http")
```

### Sending Commands

```python
# Convert intent to command
command = sdk.no_ui_adapter.convert_intent_to_command(
    intent="开灯",
    device_type="light"
)

# Send to device
result = sdk.no_ui_adapter.send_command(
    command=command,
    device_id="light_living_001"
)

print(f"Status: {result.status}")
```

### Working with Devices

```python
# List all devices
devices = sdk.no_ui_adapter.list_devices()

for device in devices:
    print(f"{device.name}: {device.status}")

# Register new device
new_device = Device(
    id="light_002",
    name="Bedroom Light",
    type="light",
    protocol="mqtt"
)
sdk.no_ui_adapter.register_device(new_device)
```

### Using Scenes

```python
# Execute predefined scene
results = sdk.no_ui_adapter.execute_scene("离家模式")

# Create custom scene
sdk.no_ui_adapter.create_scene(
    name="电影模式",
    commands=[
        {"device": "light_001", "action": "dim", "level": 20},
        {"device": "tv_001", "action": "power_on"}
    ]
)
```

---

## Agent Federation

### Distributing Tasks

```python
# Initialize federation
sdk = GhostHubSDK()
sdk.connect()

# Create task
task = {
    "name": "数据分析",
    "description": "分析销售数据",
    "priority": "high"
}

# Distribute to agents
result = sdk.agent_federation.distribute_task(
    task=task,
    strategy="capability_match"
)

print(f"Assigned to: {result['agent_id']}")
print(f"Estimated time: {result['estimated_time']}")
```

### Collaborative Sessions

```python
# Create collaboration session
session = sdk.agent_federation.create_session(
    session_id="project_alpha",
    agents=["data_agent", "viz_agent", "report_agent"]
)

# Start session
session.start()

# Distribute work
for subtask in subtasks:
    session.distribute(subtask)

# Aggregate results
final_result = session.aggregate()
```

### Managing Agents

```python
# List available agents
agents = sdk.agent_federation.list_agents()

for agent in agents:
    print(f"{agent.name}: {agent.status}")
    print(f"  Load: {agent.current_load}")
    print(f"  Capabilities: {agent.capabilities}")
```

---

## Best Practices

### Error Handling

```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()

try:
    result = sdk.execute_workflow("optimize process")
except Exception as e:
    print(f"Error: {e}")
    # Implement fallback
```

### Resource Management

```python
sdk = GhostHubSDK()
try:
    sdk.connect()
    # Do work
    result = sdk.execute_workflow("task")
finally:
    sdk.disconnect()  # Always cleanup
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

sdk = GhostHubSDK(GhostHubConfig(log_level="DEBUG"))

# View detailed logs
sdk.execute_workflow("complex workflow")
```

### Performance

```python
# Batch operations when possible
commands = [
    sdk.no_ui_adapter.convert_intent_to_command("开灯", "light"),
    sdk.no_ui_adapter.convert_intent_to_command("调温度", "thermostat"),
]

# Send batch
results = sdk.no_ui_adapter.send_batch_commands(commands)
```

---

## Troubleshooting

### Common Issues

#### ImportError
```
ModuleNotFoundError: No module named 'ghost_hub_sdk'
```
**Solution:** Install the package: `pip install ghost-hub-sdk`

#### Connection Failed
```
ConnectionError: Failed to connect to MQTT broker
```
**Solution:** Check network connectivity and broker address

#### Template Not Found
```
ValueError: No matching template found
```
**Solution:** Use a more specific intent or check available templates

### Debug Mode

```python
config = GhostHubConfig(log_level="DEBUG")
sdk = GhostHubSDK(config)
```

### Getting Help

- GitHub Issues: https://github.com/ghost-hub/sdk/issues
- Documentation: https://docs.ghosthub.dev
- Discord: https://discord.gg/ghosthub
