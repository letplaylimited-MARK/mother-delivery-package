"""
Ghost Channel - Types & Exceptions
幽灵通道 - 类型定义与异常类
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Union
from enum import Enum
import time


class SyncMode(Enum):
    """同步模式"""

    DELTA = "delta"  # 增量同步
    FULL = "full"  # 全量同步
    PREDICTIVE = "predictive"  # 预测同步
    SEMANTIC = "semantic"  # 语义同步


class ConsistencyLevel(Enum):
    """一致性级别"""

    EVENTUAL = "eventual"  # 最终一致性
    CAUSAL = "causal"  # 因果一致性
    STRONG = "strong"  # 强一致性


class CompressionType(Enum):
    """压缩类型"""

    NONE = "none"
    ZLIB = "zlib"
    LZ4 = "lz4"
    ZSTD = "zstd"


@dataclass
class GhostChannelConfig:
    """幽灵通道配置"""

    node_id: str = "default"
    compression_level: int = 9
    compression_type: CompressionType = CompressionType.ZLIB
    semantic_threshold: float = 0.70
    audit_enabled: bool = True
    encryption_enabled: bool = True
    max_retry: int = 3
    completion_mode: str = "apply"
    await_ack: bool = False
    ack_timeout_ms: int = 500
    replay_window_size: int = 1024
    sync_mode: SyncMode = SyncMode.DELTA
    consistency_level: ConsistencyLevel = ConsistencyLevel.CAUSAL
    self_healing_enabled: bool = True
    predictive_sync_enabled: bool = False


@dataclass
class SyncResult:
    """同步结果"""

    success: bool
    bandwidth_reduction: float
    latency_ms: float
    consistency_verified: bool
    changes_applied: int
    transaction_id: str = ""
    merkle_root: str = ""
    errors: list[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


@dataclass
class DeltaPayload:
    """Delta载荷"""

    added: dict = field(default_factory=dict)
    modified: dict = field(default_factory=dict)
    removed: set = field(default_factory=set)
    timestamp: float = field(default_factory=time.time)


@dataclass
class VectorClockState:
    """向量时钟状态"""

    clock: dict[str, int] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class EncryptedPacket:
    """加密数据包"""

    nonce: bytes
    ciphertext: bytes
    auth_tag: bytes
    aad: Optional[bytes] = None


@dataclass
class MerkleProof:
    """Merkle证明"""

    root: str
    path: list[tuple[str, str]]  # (direction, hash)
    leaf: str


@dataclass
class AuditRecord:
    """审计记录"""

    id: str
    operation: str
    node_id: str
    timestamp: float
    details: dict = field(default_factory=dict)
    signature: str = ""


@dataclass
class HealthStatus:
    """健康状态"""

    healthy: bool
    node_id: str
    uptime_seconds: float
    last_sync_ms: float
    error_count: int = 0
    details: dict = field(default_factory=dict)


@dataclass
class Metrics:
    """性能指标"""

    total_syncs: int = 0
    successful_syncs: int = 0
    failed_syncs: int = 0
    total_bytes_original: int = 0
    total_bytes_delta: int = 0
    avg_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    bandwidth_reduction_percent: float = 0.0
    conflicts_resolved: int = 0
    self_healing_count: int = 0


# ==================== 异常类 ====================


class GhostChannelError(Exception):
    """基础异常类"""

    def __init__(self, message: str, code: str = "UNKNOWN", details: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class DeltaError(GhostChannelError):
    """Delta计算错误"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="DELTA_ERROR", details=details)


class VectorClockError(GhostChannelError):
    """向量时钟错误"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="VECTOR_CLOCK_ERROR", details=details)


class CryptoError(GhostChannelError):
    """加密/解密错误"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="CRYPTO_ERROR", details=details)


class IntegrityError(GhostChannelError):
    """完整性验证错误"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="INTEGRITY_ERROR", details=details)


class AuditError(GhostChannelError):
    """审计记录错误"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="AUDIT_ERROR", details=details)


class ConsistencyError(GhostChannelError):
    """一致性错误"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="CONSISTENCY_ERROR", details=details)


class NetworkError(GhostChannelError):
    """网络通信错误"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="NETWORK_ERROR", details=details)


class TimeoutError(GhostChannelError):
    """超时错误"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="TIMEOUT_ERROR", details=details)


class ValidationError(GhostChannelError):
    """参数验证错误"""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message, code="VALIDATION_ERROR", details=details)


__all__ = [
    # Enums
    "SyncMode",
    "ConsistencyLevel",
    "CompressionType",
    # Config
    "GhostChannelConfig",
    "SyncResult",
    "DeltaPayload",
    "VectorClockState",
    "EncryptedPacket",
    "MerkleProof",
    "AuditRecord",
    "HealthStatus",
    "Metrics",
    # Exceptions
    "GhostChannelError",
    "DeltaError",
    "VectorClockError",
    "CryptoError",
    "IntegrityError",
    "AuditError",
    "ConsistencyError",
    "NetworkError",
    "TimeoutError",
    "ValidationError",
]
