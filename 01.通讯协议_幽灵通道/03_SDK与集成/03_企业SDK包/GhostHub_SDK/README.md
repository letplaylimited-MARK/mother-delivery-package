# Ghost Hub SDK

> Enterprise-grade AI Workflow Orchestration Framework

[![PyPI Version](https://img.shields.io/pypi/v/ghost-hub-sdk.svg)](https://pypi.org/project/ghost-hub-sdk/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ghost-hub-sdk.svg)](https://pypi.org/project/ghost-hub-sdk/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Ghost Hub** is an enterprise-grade AI workflow orchestration SDK that enables seamless integration between human intent, IoT devices, and multi-agent systems.

## Features

### Core Components

| Component | Description |
|-----------|-------------|
| **Intention Bank** | Intent parsing, template matching, task decomposition |
| **No-UI Adapter** | IoT device integration, protocol adaptation, command conversion |
| **Agent Federation** | Multi-agent collaboration, route discovery, cooperative sessions |

### Key Capabilities

- **Smart Intent Recognition**: 22+ business templates for HR, IoT, Operations, Finance scenarios
- **IoT Protocol Support**: MQTT, HTTP, WebSocket, CoAP
- **Multi-Agent Routing**: Dynamic agent discovery and task distribution
- **Enterprise-Ready**: Configurable, extensible, production-grade

## Installation

```bash
pip install ghost-hub-sdk              # Core (zero external deps)
pip install ghost-hub-sdk[protocols]   # + MQTT/WebSocket protocol support
pip install ghost-hub-sdk[api]         # + FastAPI REST API server
pip install ghost-hub-sdk[all]         # Everything
```

## Quick Start

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

config = GhostHubConfig(
    intention_bank_enabled=True,
    no_ui_adapter_enabled=True,
    agent_federation_enabled=True,
)

sdk = GhostHubSDK(config)

result = sdk.execute_workflow("帮我优化面试流程")
print(f"Tasks: {result['task_graph']['task_count']}")
print(f"Workflow: {result['workflow_id']}")
```

## Use Cases

### Human Resources
```python
sdk.execute_workflow("优化招聘流程")
sdk.execute_workflow("员工入职手续")
sdk.execute_workflow("绩效考核评估")
```

### IoT Integration
```python
sdk.no_ui_adapter.connect()
sdk.no_ui_adapter.convert_intent_to_command("开灯", "light")
sdk.no_ui_adapter.execute_command(command, "smart_home")
```

### Multi-Agent Collaboration
```python
sdk.agent_federation.start_session("data_analysis")
sdk.agent_federation.route_task(task, agents)
```

## Architecture

```
ghost_hub_sdk/
├── core.py                 # SDK Core
├── config.py               # Configuration
├── security.py             # Auth, validation, rate limiting
├── workflow_engine.py      # Workflow orchestration
├── memory.py               # Memory layer
├── knowledge.py            # Knowledge layer
├── storage.py              # JSON/SQLite persistence
├── components/
│   ├── intention_bank.py   # Intent parsing & task decomposition
│   ├── no_ui_adapter.py    # IoT device integration
│   └── agent_federation.py # Multi-agent coordination
├── protocols/
│   ├── mqtt_client.py      # MQTT protocol support
│   ├── websocket_client.py # WebSocket protocol support
│   └── real_protocols.py   # Production protocol implementations
├── api/
│   ├── main.py             # FastAPI REST API
│   └── secure_api.py       # Secure API with auth
├── templates/              # 23 business templates
├── demos/                  # Usage examples
└── tests/                  # Test suite
```

## Documentation

- [Full Documentation](https://docs.ghosthub.dev)
- [API Reference](https://docs.ghosthub.dev/api)
- [Examples](demos/)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with ❤️ for the AI workflow future
