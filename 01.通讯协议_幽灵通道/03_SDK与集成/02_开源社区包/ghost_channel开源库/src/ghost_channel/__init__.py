"""
Ghost Channel Protocol - Open Source Edition
幽灵通道协议 - 开源版

面向分布式AI协作系统的语义感知增量同步协议层

核心功能:
- Delta增量同步 (61-93%带宽降低)
- 向量时钟因果排序 (100%一致性)
- AES-256-GCM加密传输
- Merkle完整性验证
- 审计追踪

Version: 1.0.0
"""

from .core.protocol import GhostChannel, SyncConfig, SyncResult
from .core.delta import DeltaCalculator, DeltaPayload
from .core.vector_clock import VectorClock, CausalityTracker
from .core.crypto import CryptoEngine
from .core.merkle import MerkleTree, IntegrityVerifier
from .core.audit import AuditLogger, AuditConfig, MessageType

__version__ = "1.0.0"

__all__ = [
    "GhostChannel",
    "SyncConfig",
    "SyncResult",
    "DeltaCalculator",
    "DeltaPayload",
    "VectorClock",
    "CausalityTracker",
    "CryptoEngine",
    "MerkleTree",
    "IntegrityVerifier",
    "AuditLogger",
    "AuditConfig",
    "MessageType",
]
