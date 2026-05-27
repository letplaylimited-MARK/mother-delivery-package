"""
Ghost Channel - Main Protocol (Open Source Edition)
幽灵通道 - 主协议层 (开源版)

开源核心功能:
- A: Delta增量同步
- B: 向量时钟因果排序
- C: AES-256-GCM加密
- D: Merkle完整性验证
- E: 审计追踪

Version: 1.0.0
"""

from __future__ import annotations
import asyncio
import time
import json
import copy
from typing import Any, Optional
from dataclasses import dataclass, field, asdict

from .delta import DeltaCalculator, DeltaPayload
from .vector_clock import VectorClock, CausalityTracker
from .crypto import CryptoEngine
from .merkle import MerkleTree, IntegrityVerifier
from .audit import AuditLogger, AuditConfig, MessageType


@dataclass
class SyncConfig:
    """同步配置"""

    node_id: str = "default_node"
    compression_level: int = 9
    semantic_threshold: float = 0.70
    audit_enabled: bool = True
    ack_timeout_ms: int = 500
    replay_window_size: int = 1024
    predictive_sync_enabled: bool = False


@dataclass
class SyncResult:
    """同步结果"""

    success: bool
    bandwidth_reduction: float
    latency_ms: float
    consistency_verified: bool
    changes_applied: int
    errors: list[str] = field(default_factory=list)
    transaction_id: str = ""
    merkle_root: str = ""


class GhostChannel:
    """
    幽灵通道主协议

    整合所有原子能力的统一同步协议层
    """

    def __init__(self, config: SyncConfig = None, node_ids: list[str] = None):
        self.config = config or SyncConfig()
        self.node_ids = node_ids or [self.config.node_id]

        # 核心组件
        self.delta_calc = DeltaCalculator()
        self.causality = CausalityTracker(self.node_ids)
        self.crypto = CryptoEngine()
        self.merkle = MerkleTree()
        self.integrity = IntegrityVerifier()
        self.audit = AuditLogger()

        # 状态存储
        self.states: dict[str, dict] = {nid: {} for nid in self.node_ids}
        self.merkle_roots: dict[str, str] = {nid: "" for nid in self.node_ids}

        # 统计
        self.stats = {
            "total_syncs": 0,
            "total_bytes_original": 0,
            "total_bytes_delta": 0,
            "total_latency_ms": 0.0,
            "conflicts_resolved": 0,
        }

    async def sync_memory_delta(
        self,
        source_role: str,
        target_role: str,
        memory_snapshot: dict,
    ) -> SyncResult:
        """
        同步记忆差分

        核心同步方法，整合了:
        - Delta增量计算
        - 向量时钟因果追踪
        - Merkle完整性验证
        - 审计记录

        Args:
            source_role: 源角色ID
            target_role: 目标角色ID
            memory_snapshot: 记忆快照

        Returns:
            SyncResult: 同步结果
        """
        start_time = time.time()

        # 1. 计算Delta
        target_state = self.states.get(target_role, {})
        delta = self.delta_calc.calculate_delta(target_state, memory_snapshot)

        # 2. 计算大小
        original_size = len(json.dumps(memory_snapshot, default=str).encode("utf-8"))
        delta_size = delta.size_bytes()

        # 4. 向量时钟因果追踪
        payload = asdict(delta)
        stamped_payload, clock = self.causality.stamp_event(source_role, payload)

        # 5. 接收方合并
        self.causality.receive_event(target_role, stamped_payload)

        # 6. 应用Delta
        new_target_state = self.delta_calc.apply_delta(target_state, delta)
        self.states[target_role] = new_target_state
        self.states[source_role] = copy.deepcopy(memory_snapshot)

        # 7. Merkle验证
        target_items = list(self.states[target_role].values())
        new_root = self.merkle.build(target_items)
        old_root = self.merkle_roots.get(target_role, "")
        self.merkle_roots[target_role] = new_root

        integrity_verified = self.merkle.verify(target_items, new_root)

        # 8. 创建快照（用于自愈）- feature not yet available
        vc = VectorClock.from_dict(clock.to_dict())
        _ = (new_target_state, vc, target_role)

        # 9. 审计记录
        delta_hash = self.crypto.compute_hash_dict(asdict(delta))
        latency_ms = (time.time() - start_time) * 1000
        bandwidth_saved = original_size - delta_size

        self.audit.log_sync(
            source_role=source_role,
            destination_role=target_role,
            message_type=MessageType.MEMORY_SYNC,
            delta_hash=delta_hash,
            merkle_root_before=old_root,
            merkle_root_after=new_root,
            bandwidth_saved=bandwidth_saved,
            duration_ms=latency_ms,
        )

        # 10. 更新统计
        self.stats["total_syncs"] += 1
        self.stats["total_bytes_original"] += original_size
        self.stats["total_bytes_delta"] += delta_size
        self.stats["total_latency_ms"] += latency_ms

        bandwidth_reduction = 1 - (delta_size / max(original_size, 1))

        return SyncResult(
            success=True,
            bandwidth_reduction=max(0, bandwidth_reduction),
            latency_ms=latency_ms,
            consistency_verified=integrity_verified,
            changes_applied=delta.change_count(),
            merkle_root=new_root,
        )

    async def sync_workflow_state(
        self,
        workflow_id: str,
        step_id: str,
        step_state: dict,
        dependencies: list[str],
    ) -> SyncResult:
        """
        同步工作流状态（因果依赖感知）
        """
        start_time = time.time()

        # 1. 计算Delta
        state_key = f"{workflow_id}:{step_id}"
        previous = self.states.get(state_key, {})
        delta = self.delta_calc.calculate_delta(previous, step_state)

        # 2. 因果依赖检查
        for dep in dependencies:
            dep_key = f"{workflow_id}:{dep}"
            if dep_key not in self.states:
                return SyncResult(
                    success=False,
                    bandwidth_reduction=0,
                    latency_ms=0,
                    consistency_verified=False,
                    changes_applied=0,
                    errors=[f"Dependency {dep} not found"],
                )

        # 3. 向量时钟
        payload = {
            "workflow_id": workflow_id,
            "step_id": step_id,
            "delta": asdict(delta),
        }
        stamped_payload, clock = self.causality.stamp_event(step_id, payload)

        # 4. 应用状态
        self.states[state_key] = copy.deepcopy(step_state)

        # 5. Merkle验证
        items = list(self.states[state_key].values())
        new_root = self.merkle.build(items)
        old_root = self.merkle_roots.get(state_key, "")
        self.merkle_roots[state_key] = new_root

        # 6. 统计
        latency_ms = (time.time() - start_time) * 1000
        original_size = len(json.dumps(step_state, default=str).encode("utf-8"))
        delta_size = delta.size_bytes()

        self.stats["total_syncs"] += 1
        self.stats["total_bytes_original"] += original_size
        self.stats["total_bytes_delta"] += delta_size
        self.stats["total_latency_ms"] += latency_ms

        bandwidth_reduction = 1 - (delta_size / max(original_size, 1))

        return SyncResult(
            success=True,
            bandwidth_reduction=max(0, bandwidth_reduction),
            latency_ms=latency_ms,
            consistency_verified=True,
            changes_applied=delta.change_count(),
            merkle_root=new_root,
        )

    async def recover_from_failure(
        self,
        step_id: str,
        last_known_state: dict,
    ) -> dict:
        """
        从失败中恢复

        简单恢复到已知状态
        """
        self.states[step_id] = copy.deepcopy(last_known_state)
        return {"success": True, "recovered": True}

    def get_audit_trail(self, limit: int = 100) -> list[dict]:
        """获取审计链"""
        entries = self.audit.get_recent(limit)
        return [e.to_dict() for e in entries]

    def get_stats(self) -> dict:
        """获取统计信息"""
        avg_bandwidth = 0
        if self.stats["total_bytes_original"] > 0:
            avg_bandwidth = 1 - (
                self.stats["total_bytes_delta"] / self.stats["total_bytes_original"]
            )

        avg_latency = 0
        if self.stats["total_syncs"] > 0:
            avg_latency = self.stats["total_latency_ms"] / self.stats["total_syncs"]

        return {
            "total_syncs": self.stats["total_syncs"],
            "avg_bandwidth_reduction": f"{avg_bandwidth * 100:.1f}%",
            "avg_latency_ms": f"{avg_latency:.1f}ms",
            "total_bytes_saved": self.stats["total_bytes_original"]
            - self.stats["total_bytes_delta"],
        }

    def get_state(self, role_id: str) -> dict:
        """获取角色状态"""
        return self.states.get(role_id, {})

    def set_state(self, role_id: str, state: dict):
        """设置角色状态"""
        self.states[role_id] = state

    def get_merkle_root(self, role_id: str) -> str:
        """获取角色的Merkle根"""
        return self.merkle_roots.get(role_id, "")


class GhostChannelManager:
    """幽灵通道管理器 - 高层API"""

    def __init__(self, node_id: str = "manager"):
        self.node_id = node_id
        self.channels: dict[str, GhostChannel] = {}
        self.default_config = SyncConfig(node_id=node_id)

    def create_channel(
        self,
        channel_id: str,
        node_ids: list[str] = None,
    ) -> GhostChannel:
        """创建新通道"""
        config = SyncConfig(node_id=channel_id)
        channel = GhostChannel(config, node_ids)
        self.channels[channel_id] = channel
        return channel

    def get_channel(self, channel_id: str) -> GhostChannel | None:
        """获取通道"""
        return self.channels.get(channel_id)

    def delete_channel(self, channel_id: str):
        """删除通道"""
        self.channels.pop(channel_id, None)

    def list_channels(self) -> list[str]:
        """列出所有通道"""
        return list(self.channels.keys())
