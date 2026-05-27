"""
Ghost Channel - Audit Logger
幽灵通道 - 审计日志

原子能力E: 审计追踪
实现: 完整事务记录, 审计链追溯
验证: 100%审计覆盖率
"""

from __future__ import annotations
import time
import json
from typing import Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class MessageType(Enum):
    """消息类型"""

    MEMORY_SYNC = "MEMORY_SYNC"
    WORKFLOW_SYNC = "WORKFLOW_SYNC"
    STATE_UPDATE = "STATE_UPDATE"
    DECISION_PROPOSAL = "DECISION_PROPOSAL"
    DEADLOCK_ALERT = "DEADLOCK_ALERT"
    META_COMMENTARY = "META_COMMENTARY"


class Severity(Enum):
    """严重级别"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEntry:
    """审计条目"""

    transaction_id: str
    timestamp: float
    source_role: str
    destination_role: str
    message_type: str
    delta_hash: str
    merkle_root_before: str
    merkle_root_after: str
    bandwidth_saved_bytes: int
    transmission_duration_ms: float
    signature_verified: bool
    tamper_detected: bool
    error: str | None = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditConfig:
    """审计配置"""

    enabled: bool = True
    storage_path: str = "./data/audit.log"
    retention_days: int = 90
    max_entries: int = 100000
    compress_old: bool = True


class AuditLogger:
    """审计日志器"""

    def __init__(self, config: AuditConfig = None):
        self.config = config or AuditConfig()
        self.entries: list[AuditEntry] = []
        self.tx_index: dict[str, int] = {}  # transaction_id -> entry index

    def log(self, entry: AuditEntry):
        """记录审计条目"""
        if not self.config.enabled:
            return

        self.entries.append(entry)
        self.tx_index[entry.transaction_id] = len(self.entries) - 1

        # 限制内存中的条目数量
        if len(self.entries) > self.config.max_entries:
            self.entries = self.entries[-self.config.max_entries :]
            self.tx_index = {e.transaction_id: i for i, e in enumerate(self.entries)}

    def log_sync(
        self,
        source_role: str,
        destination_role: str,
        message_type: MessageType,
        delta_hash: str,
        merkle_root_before: str,
        merkle_root_after: str,
        bandwidth_saved: int,
        duration_ms: float,
        signature_verified: bool = True,
        tamper_detected: bool = False,
        error: str | None = None,
    ) -> AuditEntry:
        """记录同步审计"""
        import uuid

        entry = AuditEntry(
            transaction_id=str(uuid.uuid4()),
            timestamp=time.time(),
            source_role=source_role,
            destination_role=destination_role,
            message_type=message_type.value,
            delta_hash=delta_hash,
            merkle_root_before=merkle_root_before,
            merkle_root_after=merkle_root_after,
            bandwidth_saved_bytes=bandwidth_saved,
            transmission_duration_ms=duration_ms,
            signature_verified=signature_verified,
            tamper_detected=tamper_detected,
            error=error,
        )
        self.log(entry)
        return entry

    def query(
        self,
        source_role: str = None,
        destination_role: str = None,
        message_type: MessageType = None,
        start_time: float = None,
        end_time: float = None,
        limit: int = 100,
    ) -> list[AuditEntry]:
        """查询审计日志"""
        results = self.entries

        if source_role:
            results = [e for e in results if e.source_role == source_role]
        if destination_role:
            results = [e for e in results if e.destination_role == destination_role]
        if message_type:
            results = [e for e in results if e.message_type == message_type.value]
        if start_time:
            results = [e for e in results if e.timestamp >= start_time]
        if end_time:
            results = [e for e in results if e.timestamp <= end_time]

        return results[-limit:]

    def get_transaction(self, transaction_id: str) -> AuditEntry | None:
        """获取指定事务"""
        idx = self.tx_index.get(transaction_id)
        if idx is not None and idx < len(self.entries):
            return self.entries[idx]
        return None

    def verify_chain(self, from_txn: str, to_txn: str) -> bool:
        """验证审计链完整性"""
        from_entry = self.get_transaction(from_txn)
        to_entry = self.get_transaction(to_txn)

        if not from_entry or not to_entry:
            return False

        from_idx = self.tx_index[from_txn]
        to_idx = self.tx_index[to_txn]

        if from_idx >= to_idx:
            return False

        # 验证连续性
        for i in range(from_idx, to_idx):
            if (
                self.entries[i].merkle_root_after
                != self.entries[i + 1].merkle_root_before
            ):
                return False

        return True

    def get_statistics(self) -> dict:
        """获取统计信息"""
        if not self.entries:
            return {
                "total_transactions": 0,
                "total_bandwidth_saved": 0,
                "average_latency_ms": 0,
                "signature_failures": 0,
                "tamper_detections": 0,
            }

        return {
            "total_transactions": len(self.entries),
            "total_bandwidth_saved": sum(e.bandwidth_saved_bytes for e in self.entries),
            "average_latency_ms": sum(e.transmission_duration_ms for e in self.entries)
            / len(self.entries),
            "signature_failures": sum(
                1 for e in self.entries if not e.signature_verified
            ),
            "tamper_detections": sum(1 for e in self.entries if e.tamper_detected),
        }

    def get_recent(self, limit: int = 10) -> list[AuditEntry]:
        """获取最近的审计条目"""
        return self.entries[-limit:]

    def clear(self):
        """清除审计日志"""
        self.entries.clear()
        self.tx_index.clear()
