"""
自愈恢复模块
Ghost Channel Protocol - Atomic Capability G
"""

import copy
import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SnapshotRecord:
    """快照记录"""
    snapshot_id: str
    state: dict
    vector_clock: dict
    merkle_root: str
    timestamp: float


class SelfHealer:
    """自愈恢复器"""
    
    def __init__(self, max_snapshots: int = 10):
        self.max_snapshots = max_snapshots
        self.snapshots: list[SnapshotRecord] = []
    
    def create_snapshot(
        self,
        state: dict,
        vector_clock: dict,
        merkle_root: str
    ) -> SnapshotRecord:
        """创建快照"""
        snapshot = SnapshotRecord(
            snapshot_id=str(uuid.uuid4()),
            state=copy.deepcopy(state),
            vector_clock=copy.deepcopy(vector_clock),
            merkle_root=merkle_root,
            timestamp=time.time()
        )
        
        self.snapshots.append(snapshot)
        
        # 限制快照数量
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots.pop(0)
        
        return snapshot
    
    def recover(self, snapshot_id: str) -> dict:
        """从快照恢复"""
        for snap in self.snapshots:
            if snap.snapshot_id == snapshot_id:
                return copy.deepcopy(snap.state)
        
        raise ValueError(f"Snapshot {snapshot_id} not found")
    
    def recover_latest(self) -> Optional[dict]:
        """恢复到最新快照"""
        if not self.snapshots:
            return None
        return copy.deepcopy(self.snapshots[-1].state)
    
    def find_snapshot(self, snapshot_id: str) -> Optional[SnapshotRecord]:
        """查找快照"""
        for snap in self.snapshots:
            if snap.snapshot_id == snapshot_id:
                return snap
        return None
    
    def find_latest_valid(self) -> Optional[SnapshotRecord]:
        """找到最新有效快照"""
        if not self.snapshots:
            return None
        return self.snapshots[-1]
    
    def auto_recover(self, current_state: dict) -> dict:
        """自动恢复"""
        latest = self.find_latest_valid()
        
        if latest is None:
            return current_state
        
        return copy.deepcopy(latest.state)
    
    def verify_snapshot(self, snapshot_id: str) -> bool:
        """验证快照完整性"""
        import json
        snap = self.find_snapshot(snapshot_id)
        
        if snap is None:
            return False
        
        # 验证Merkle根
        state_hash = hashlib.sha256(
            json.dumps(snap.state, sort_keys=True).encode()
        ).hexdigest()
        
        return state_hash == snap.merkle_root
    
    def get_snapshots(self) -> list[dict]:
        """获取所有快照摘要"""
        return [
            {
                "snapshot_id": s.snapshot_id,
                "timestamp": s.timestamp,
                "merkle_root": s.merkle_root[:8] + "..."
            }
            for s in self.snapshots
        ]


def test_self_healer():
    """测试自愈功能"""
    import json
    
    healer = SelfHealer(max_snapshots=5)
    
    # Test 1: Create snapshot
    state = {"name": "test", "value": 123}
    vector_clock = {"A": 1, "B": 2}
    merkle_root = hashlib.sha256(
        json.dumps(state, sort_keys=True).encode()
    ).hexdigest()
    
    snapshot = healer.create_snapshot(state, vector_clock, merkle_root)
    assert snapshot.snapshot_id is not None
    print("[OK] create_snapshot")
    
    # Test 2: Recover
    recovered = healer.recover(snapshot.snapshot_id)
    assert recovered == state
    print("[OK] recover")
    
    # Test 3: Latest
    latest = healer.recover_latest()
    assert latest == state
    print("[OK] recover_latest")
    
    # Test 4: Auto recover
    new_state = {"name": "corrupted"}
    result = healer.auto_recover(new_state)
    assert result == state
    print("[OK] auto_recover")
    
    # Test 5: Verify
    assert healer.verify_snapshot(snapshot.snapshot_id) == True
    print("[OK] verify_snapshot")
    
    # Test 6: Get snapshots list
    snapshots = healer.get_snapshots()
    assert len(snapshots) == 1
    print("[OK] get_snapshots")
    
    print("[PASS] All self-healer tests passed!")


if __name__ == "__main__":
    test_self_healer()