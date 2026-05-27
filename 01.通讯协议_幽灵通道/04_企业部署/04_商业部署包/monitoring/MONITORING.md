# Ghost Hub SDK Monitoring Guide

## Overview

Ghost Hub SDK provides comprehensive monitoring and logging capabilities:

- **Prometheus Metrics** - Quantitative metrics collection
- **Structured Logging** - JSON-formatted logs for analysis
- **Health Checks** - Service health monitoring
- **Audit Logging** - Compliance and security tracking

## Prometheus Metrics

### Available Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `ghost_hub_workflows_total` | Counter | Total workflows executed |
| `ghost_hub_intent_matches_total` | Counter | Intent matches by domain |
| `ghost_hub_device_commands_total` | Counter | Device commands sent |
| `ghost_hub_agent_tasks_total` | Counter | Agent tasks distributed |
| `ghost_hub_workflow_latency_seconds` | Histogram | Workflow latency |
| `ghost_hub_active_devices` | Gauge | Active IoT devices |
| `ghost_hub_active_agents` | Gauge | Active agents |

### Using Metrics

```python
from ghost_hub_sdk.monitoring import monitoring, monitor_latency

# Record custom metrics
monitoring.record_workflow("hr_recruitment", "success", 1.5)

# Decorate functions
@monitor_latency("custom_workflow")
def my_workflow():
    pass
```

### Exposing Metrics

```python
from flask import Flask, Response
from ghost_hub_sdk.monitoring import monitoring

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    return Response(
        monitoring.get_metrics(),
        mimetype='text/plain'
    )
```

## Structured Logging

### Configuration

```python
from ghost_hub_sdk.logging_config import setup_logging, get_logger

# Setup with JSON output
logger = setup_logging(
    level="INFO",
    log_file="ghost_hub.log",
    json_format=True
)

# Get module logger
log = get_logger("workflow")
log.info("Processing workflow")
```

### Log Format

```json
{
  "timestamp": "2026-04-15T20:00:00.000Z",
  "level": "INFO",
  "logger": "ghost_hub_sdk.workflow",
  "message": "Workflow completed",
  "module": "workflow",
  "function": "execute",
  "line": 123
}
```

### Context Logging

```python
from ghost_hub_sdk.logging_config import LogContext

log = get_logger("workflow")

with LogContext(log, workflow_id="wf_123", user="alice"):
    log.info("Processing request")
```

## Health Checks

### Implementing Health Check

```python
from ghost_hub_sdk.health import HealthCheck, HealthStatus

class SDKHealthCheck(HealthCheck):
    def check(self) -> HealthStatus:
        return HealthStatus(
            healthy=True,
            message="SDK operational",
            details={
                'components': {
                    'intention_bank': True,
                    'no_ui_adapter': True,
                    'agent_federation': True
                }
            }
        )
```

### Health Endpoint

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    status = sdk_health_check.check()
    return jsonify(status.to_dict()), 200 if status.healthy else 503
```

## Audit Logging

### Using Audit Logger

```python
from ghost_hub_sdk.logging_config import audit_logger

# Log resource access
audit_logger.log_access("alice", "/api/workflows", True)

# Log configuration change
audit_logger.log_config_change("admin", "max_agents", 10, 20)

# Log custom action
audit_logger.log_action(
    action="workflow_execute",
    user="alice",
    resource="hr_recruitment",
    result="success",
    details={"duration": 2.5}
)
```

## Grafana Dashboard

### Dashboard JSON

Import `grafana/dashboard.json` into Grafana for:

- Workflow execution trends
- Intent matching accuracy
- Device command latency
- Agent utilization
- System health overview

### Panels

1. **Overview**
   - Total workflows (24h)
   - Success rate
   - Average latency

2. **Intention Bank**
   - Matches by domain
   - Confidence distribution
   - Top templates

3. **IoT Integration**
   - Commands by type
   - Protocol distribution
   - Error rate

4. **Agent Federation**
   - Task distribution
   - Agent load balance
   - Queue depth

## Alerting

### Recommended Alerts

```yaml
groups:
  - name: ghost_hub_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(ghost_hub_workflows_total{status="error"}[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High workflow error rate"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, ghost_hub_workflow_latency_seconds) > 5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Workflow latency exceeds 5s"
      
      - alert: NoHealthyAgents
        expr: ghost_hub_active_agents == 0
        for: 1m
        labels:
          severity: critical
```

## Performance Tuning

### Recommended Settings

| Setting | Development | Production |
|---------|--------------|-------------|
| Log Level | DEBUG | INFO |
| Metrics | Disabled | Enabled |
| Audit Log | Disabled | Enabled |
| Log Rotation | 10MB | 100MB |
| Retention | 7 days | 30 days |
