"""
Ghost Hub SDK配置
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class GhostHubConfig:
    name: str = "GhostHub"
    version: str = "1.0.0"

    intention_bank_enabled: bool = True
    intention_bank_config: Dict[str, Any] = field(
        default_factory=lambda: {
            "match_threshold": 0.3,
            "max_results": 5,
            "storage_type": "json",
        }
    )

    no_ui_adapter_enabled: bool = True
    no_ui_adapter_config: Dict[str, Any] = field(
        default_factory=lambda: {"default_protocol": "http"}
    )

    agent_federation_enabled: bool = True
    agent_federation_config: Dict[str, Any] = field(
        default_factory=lambda: {
            "agent_id": "ghost-hub-sdk",
            "agent_name": "GhostHubSDK",
        }
    )

    log_level: str = "INFO"
    enable_metrics: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "GhostHubConfig":
        return cls(
            name=data.get("name", "GhostHub"),
            version=data.get("version", "1.0.0"),
            intention_bank_enabled=data.get("intention_bank_enabled", True),
            intention_bank_config=data.get("intention_bank_config", {}),
            no_ui_adapter_enabled=data.get("no_ui_adapter_enabled", True),
            no_ui_adapter_config=data.get("no_ui_adapter_config", {}),
            agent_federation_enabled=data.get("agent_federation_enabled", True),
            agent_federation_config=data.get("agent_federation_config", {}),
            log_level=data.get("log_level", "INFO"),
            enable_metrics=data.get("enable_metrics", True),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "intention_bank_enabled": self.intention_bank_enabled,
            "intention_bank_config": self.intention_bank_config,
            "no_ui_adapter_enabled": self.no_ui_adapter_enabled,
            "no_ui_adapter_config": self.no_ui_adapter_config,
            "agent_federation_enabled": self.agent_federation_enabled,
            "agent_federation_config": self.agent_federation_config,
            "log_level": self.log_level,
            "enable_metrics": self.enable_metrics,
        }
