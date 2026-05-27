# Ghost Hub SDK One-Pager

## Product Overview

**Ghost Hub SDK** is an enterprise-grade AI workflow orchestration framework that unifies intent parsing, IoT device control, and multi-agent collaboration into a single, powerful SDK.

---

## Key Benefits

| Benefit | Impact |
|---------|--------|
| **10x Faster Development** | From weeks to hours |
| **70% Cost Reduction** | Automated workflows |
| **Native AI Integration** | Built-in intent understanding |
| **Enterprise Ready** | SOC 2, SSO, SLA |

---

## Core Features

### 1. Intention Bank
Natural language intent parsing with 22 pre-built templates

```
"帮我优化招聘流程"
→ Matches HR domain
→ Creates 5-task workflow
→ Executes automatically
```

### 2. No-UI Adapter
Universal IoT device integration

```
"开灯" → MQTT Command → Device
"温度24度" → HTTP API → Thermostat
```

### 3. Agent Federation
Distributed AI agent orchestration

```
Task → Smart Routing → Best Agent → Aggregated Result
```

---

## Supported Protocols

| Protocol | Use Case |
|----------|----------|
| **MQTT** | IoT devices, sensors |
| **HTTP** | REST APIs, webhooks |
| **WebSocket** | Real-time apps |
| **CoAP** | Constrained devices |

---

## Supported Domains

| Domain | Templates |
|--------|-----------|
| HR | Recruitment, onboarding, reviews |
| IoT | Smart home, industrial control |
| Operations | Ticketing, monitoring |
| Finance | Invoicing, reporting |

---

## Deployment Options

- **Cloud**: Managed SaaS
- **On-Premise**: Docker/Kubernetes
- **Hybrid**: Cloud + on-prem

---

## Integration Examples

### Python
```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()
result = sdk.execute_workflow("优化招聘流程")
```

### REST API
```bash
curl -X POST https://api.ghosthub.dev/workflow \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"intent": "开灯", "device": "light_001"}'
```

---

## Pricing

| Tier | Price | Agents | Devices |
|------|-------|--------|---------|
| Community | Free | 5 | 10 |
| Professional | $499/yr | 50 | 500 |
| Enterprise | Custom | Unlimited | Unlimited |

---

## Customer Quote

> "Ghost Hub SDK reduced our workflow development time by 70%. The IoT integration is seamless."
> — **CTO, Industrial IoT Company**

---

## Get Started

- **Documentation**: docs.ghosthub.dev
- **GitHub**: github.com/ghost-hub/sdk
- **Demo**: demo.ghosthub.dev
- **Email**: hello@ghosthub.dev

---

## Logo Assets

Available at: ghosthub.dev/brand

---
*© 2026 Q-SpecTrum Project*
