"""
Ghost Hub SDK Monitoring Module
Prometheus metrics and health checks
"""

import time
from typing import Dict, Any
from functools import wraps

try:
    from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False


if PROMETHEUS_AVAILABLE:
    INFO = Info("ghost_hub_sdk", "Ghost Hub SDK information")

    WORKFLOWS_TOTAL = Counter(
        "ghost_hub_workflows_total", "Total number of workflows executed", ["status"]
    )

    INTENT_MATCHES = Counter(
        "ghost_hub_intent_matches_total",
        "Total intent matches",
        ["domain", "confidence_level"],
    )

    DEVICE_COMMANDS = Counter(
        "ghost_hub_device_commands_total",
        "Total device commands sent",
        ["device_type", "protocol", "status"],
    )

    AGENT_TASKS = Counter(
        "ghost_hub_agent_tasks_total",
        "Total agent tasks distributed",
        ["strategy", "status"],
    )

    WORKFLOW_LATENCY = Histogram(
        "ghost_hub_workflow_latency_seconds",
        "Workflow execution latency",
        ["workflow_type"],
    )

    INTENT_MATCH_LATENCY = Histogram(
        "ghost_hub_intent_match_latency_seconds", "Intent matching latency"
    )

    DEVICE_COMMAND_LATENCY = Histogram(
        "ghost_hub_device_command_latency_seconds",
        "Device command latency",
        ["protocol"],
    )

    ACTIVE_DEVICES = Gauge("ghost_hub_active_devices", "Number of active IoT devices")

    ACTIVE_AGENTS = Gauge("ghost_hub_active_agents", "Number of active agents")

    QUEUE_SIZE = Gauge(
        "ghost_hub_queue_size", "Current task queue size", ["queue_type"]
    )


class Monitoring:
    """Monitoring and metrics collection"""

    def __init__(self):
        self._start_time = time.time()
        if PROMETHEUS_AVAILABLE:
            INFO.info({"version": "1.0.0", "python_version": "3.12"})

    def record_workflow(self, workflow_type: str, status: str, duration: float):
        """Record workflow execution"""
        if PROMETHEUS_AVAILABLE:
            WORKFLOWS_TOTAL.labels(status=status).inc()
            WORKFLOW_LATENCY.labels(workflow_type=workflow_type).observe(duration)

    def record_intent_match(self, domain: str, confidence: float):
        """Record intent matching"""
        if PROMETHEUS_AVAILABLE:
            level = (
                "high" if confidence > 0.8 else "medium" if confidence > 0.5 else "low"
            )
            INTENT_MATCHES.labels(domain=domain, confidence_level=level).inc()

    def record_device_command(self, device_type: str, protocol: str, status: str):
        """Record device command"""
        if PROMETHEUS_AVAILABLE:
            DEVICE_COMMANDS.labels(
                device_type=device_type, protocol=protocol, status=status
            ).inc()

    def record_agent_task(self, strategy: str, status: str):
        """Record agent task distribution"""
        if PROMETHEUS_AVAILABLE:
            AGENT_TASKS.labels(strategy=strategy, status=status).inc()

    def update_active_devices(self, count: int):
        """Update active device count"""
        if PROMETHEUS_AVAILABLE:
            ACTIVE_DEVICES.set(count)

    def update_active_agents(self, count: int):
        """Update active agent count"""
        if PROMETHEUS_AVAILABLE:
            ACTIVE_AGENTS.set(count)

    def update_queue_size(self, queue_type: str, size: int):
        """Update queue size"""
        if PROMETHEUS_AVAILABLE:
            QUEUE_SIZE.labels(queue_type=queue_type).set(size)

    def get_metrics(self) -> bytes:
        """Get Prometheus metrics output"""
        if PROMETHEUS_AVAILABLE:
            return generate_latest()
        return b""

    def get_stats(self) -> Dict[str, Any]:
        """Get monitoring stats"""
        return {
            "uptime_seconds": time.time() - self._start_time,
            "version": "1.0.0",
            "monitoring_enabled": PROMETHEUS_AVAILABLE,
        }


def monitor_latency(metric_name: str = "default"):
    """Decorator to monitor function latency"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start
                if PROMETHEUS_AVAILABLE:
                    WORKFLOW_LATENCY.labels(workflow_type=metric_name).observe(duration)

        return wrapper

    return decorator


monitoring = Monitoring()
