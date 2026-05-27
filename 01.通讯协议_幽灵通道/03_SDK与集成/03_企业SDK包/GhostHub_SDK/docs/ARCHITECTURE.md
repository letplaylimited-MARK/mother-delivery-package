# Ghost Hub SDK Architecture

> Technical architecture and design decisions

---

## Overview

Ghost Hub SDK is an enterprise-grade AI workflow orchestration framework that unifies three core capabilities:

1. **Intention Bank** - Intent parsing and task decomposition
2. **No-UI Adapter** - IoT device integration
3. **Agent Federation** - Multi-agent collaboration

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GhostHubSDK                               │
│  ┌──────────────┐  ┌────────────────┐  ┌────────────────────┐  │
│  │  Intention   │  │  No-UI Adapter  │  │ Agent Federation   │  │
│  │    Bank      │  │                │  │                    │  │
│  │              │  │  ┌──────────┐  │  │  ┌─────────────┐  │  │
│  │ ┌──────────┐ │  │  │Protocols│  │  │  │   Routing   │  │  │
│  │ │ Template │ │  │  │   MQTT  │  │  │  │  Strategies │  │  │
│  │ │  Matcher │ │  │  │   HTTP  │  │  │  └─────────────┘  │  │
│  │ └──────────┘ │  │  │   WS    │  │  │  ┌─────────────┐  │  │
│  │ ┌──────────┐ │  │  │   CoAP  │  │  │  │  Discovery  │  │  │
│  │ │  Intent  │ │  │  └──────────┘  │  │  └─────────────┘  │  │
│  │ │  Parser  │ │  │                │  │                    │  │
│  │ └──────────┘ │  │  ┌──────────┐  │  │                    │  │
│  │ ┌──────────┐ │  │  │  Device  │  │  │                    │  │
│  │ │   Task   │ │  │  │  Command │  │  │                    │  │
│  │ │  Builder │ │  │  │  Engine  │  │  │                    │  │
│  │ └──────────┘ │  │  └──────────┘  │  │                    │  │
│  └──────────────┘  └────────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                     Supporting Modules                            │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌──────────────────┐  │
│  │ Memory  │  │Knowledge │  │ Storage │  │     Security     │  │
│  └─────────┘  └──────────┘  └─────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Intention Bank

The Intention Bank processes natural language input and converts it into actionable tasks.

```
User Input → Tokenization → Pattern Matching → Intent Classification → Task Graph
     │                                            │
     │                                            ▼
     │                                      Templates
     │                                         (22+)
     ▼
  Semantics
  Analysis
```

**Key Classes:**
- `IntentParser` - Parses user input
- `TemplateMatcher` - Matches against templates
- `TaskGraphBuilder` - Constructs task dependencies
- `SemanticSimilarity` - Computes semantic similarity

### No-UI Adapter

The No-UI Adapter bridges natural language commands to IoT devices.

```
Intent → Command Engine → Protocol Adapter → Device
                      │
                      ▼
              Device Registry
```

**Supported Protocols:**
- MQTT (publish/subscribe)
- HTTP (REST API)
- WebSocket (bidirectional)
- CoAP (constrained devices)

**Supported Device Types:**
- Smart home (lights, thermostats, locks)
- Industrial (PLC, sensors)
- Wearables
- Automotive

### Agent Federation

The Agent Federation manages distributed AI agents.

```
Task → Discovery → Routing Strategy → Agent → Result Aggregation
                              │
                              ▼
                        Agent Registry
```

**Routing Strategies:**
- Round Robin
- Load Balance
- Capability Match
- Affinity Based

## Data Flow

### Workflow Execution

```
1. User Input: "optimize interview process"
        │
        ▼
2. Intention Bank Processing
   - Tokenize input
   - Match against HR templates
   - Confidence score: 0.85
        │
        ▼
3. Task Graph Construction
   - Task 1: Screen resumes
   - Task 2: Schedule interviews  
   - Task 3: Send notifications
   - Dependencies: T1 → T2 → T3
        │
        ▼
4. Execution (parallel where possible)
   - Agent 1: Resume screening
   - Agent 2: Calendar integration
        │
        ▼
5. Result Aggregation
   - Status: Complete
   - Time: 2.3s
   - Output: Interview schedule
```

## Module Structure

```
ghost_hub_sdk/
├── __init__.py           # Package entry
├── core.py               # GhostHubSDK main class
├── config.py             # Configuration
│
├── components/
│   ├── intention_bank.py # Intent processing
│   ├── no_ui_adapter.py  # IoT integration
│   └── agent_federation.py # Multi-agent
│
├── protocols/
│   ├── mqtt_client.py    # MQTT implementation
│   ├── websocket_client.py
│   └── real_protocols.py
│
├── templates/            # Business templates (JSON)
│   ├── hr_*.json
│   ├── iot_*.json
│   └── ops_*.json
│
├── demos/                # Usage examples
├── tests/                # Unit tests
└── docs/                 # Documentation
```

## Extension Points

### Custom Templates

```python
custom_template = {
    "id": "custom_hr_001",
    "name": "Custom HR Workflow",
    "domain": "hr",
    "patterns": ["custom pattern"],
    "tasks": [...]
}

sdk.intention_bank.add_template(custom_template)
```

### Custom Protocol Adapters

```python
class CustomProtocol(ProtocolAdapter):
    def connect(self):
        pass
    
    def send(self, command):
        pass

sdk.no_ui_adapter.register_protocol("custom", CustomProtocol())
```

### Custom Routing Strategies

```python
def my_strategy(agents, task):
    return agents[0]  # Simple first-agent strategy

sdk.agent_federation.register_strategy("custom", my_strategy)
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│            Security Layer               │
│                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  Auth   │  │   ACL  │  │  Audit  │  │
│  └─────────┘  └─────────┘  └─────────┘  │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      Input Validation           │   │
│  │  - Sanitization                 │   │
│  │  - Type checking                │   │
│  │  - Size limits                  │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │      Rate Limiting              │   │
│  │  - Per-user limits              │   │
│  │  - Global limits                │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## Performance Characteristics

| Operation | Average Time | Notes |
|-----------|--------------|-------|
| Intent matching | <10ms | Local templates |
| Task graph build | <5ms | Simple workflows |
| IoT command | <50ms | Network dependent |
| Agent distribution | <20ms | Registry lookup |

## Scalability

- **Horizontal**: Add more agents for task distribution
- **Vertical**: Component-level scaling (intention bank, IoT adapter)
- **Clustering**: Support for distributed deployment

---

## Version History

| Version | Changes |
|---------|---------|
| 1.0.0 | Agent Federation, improved templates |
| 0.1.0 | Initial release with Intention Bank, No-UI Adapter |
