"""
审计追踪模块
Ghost Channel Protocol - Atomic Capability F
"""

import json
import time
import uuid
from dataclasses import dataclass, asdict, field
from typing import Optional


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


class AuditLogger:
    """审计日志器"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file
        self.entries: list[AuditEntry] = []
    
    def log(self, entry: AuditEntry):
        """记录审计条目"""
        self.entries.append(entry)
        
        if self.log_file:
            self._persist(entry)
    
    def _persist(self, entry: AuditEntry):
        """持久化到文件"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(entry), ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Warning: Failed to persist audit log: {e}")
    
    def create_entry(
        self,
        source_role: str,
        destination_role: str,
        message_type: str,
        delta_hash: str,
        merkle_root_before: str,
        merkle_root_after: str,
        bandwidth_saved_bytes: int,
        transmission_duration_ms: float,
        signature_verified: bool = True,
        tamper_detected: bool = False
    ) -> AuditEntry:
        """创建审计条目"""
        return AuditEntry(
            transaction_id=str(uuid.uuid4()),
            timestamp=time.time(),
            source_role=source_role,
            destination_role=destination_role,
            message_type=message_type,
            delta_hash=delta_hash,
            merkle_root_before=merkle_root_before,
            merkle_root_after=merkle_root_after,
            bandwidth_saved_bytes=bandwidth_saved_bytes,
            transmission_duration_ms=transmission_duration_ms,
            signature_verified=signature_verified,
            tamper_detected=tamper_detected
        )
    
    def query(
        self,
        source_role: Optional[str] = None,
        destination_role: Optional[str] = None,
        message_type: Optional[str] = None,
        limit: int = 100
    ) -> list[AuditEntry]:
        """查询审计日志"""
        results = self.entries
        
        if source_role:
            results = [e for e in results if e.source_role == source_role]
        if destination_role:
            results = [e for e in results if e.destination_role == destination_role]
        if message_type:
            results = [e for e in results if e.message_type == message_type]
        
        return results[-limit:]
    
    def verify_chain(self) -> bool:
        """验证审计链完整性"""
        if len(self.entries) < 2:
            return True
        
        for i in range(1, len(self.entries)):
            prev_time = self.entries[i-1].timestamp
            curr_time = self.entries[i].timestamp
            
            if curr_time < prev_time:
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
                "tamper_detections": 0
            }
        
        total_bandwidth = sum(e.bandwidth_saved_bytes for e in self.entries)
        total_latency = sum(e.transmission_duration_ms for e in self.entries)
        sig_failures = sum(1 for e in self.entries if not e.signature_verified)
        tamper_det = sum(1 for e in self.entries if e.tamper_detected)
        
        return {
            "total_transactions": len(self.entries),
            "total_bandwidth_saved": total_bandwidth,
            "average_latency_ms": total_latency / len(self.entries),
            "signature_failures": sig_failures,
            "tamper_detections": tamper_det
        }


def test_audit():
    """测试审计功能"""
    logger = AuditLogger()
    
    # Test 1: Create entry
    entry = logger.create_entry(
        source_role="Secretary",
        destination_role="Researcher",
        message_type="KNOWLEDGE_UPDATE",
        delta_hash="abc123",
        merkle_root_before="root1",
        merkle_root_after="root2",
        bandwidth_saved_bytes=1000,
        transmission_duration_ms=15.0
    )
    assert entry.transaction_id is not None
    print("[OK] create_entry")
    
    # Test 2: Log entry
    logger.log(entry)
    assert len(logger.entries) == 1
    print("[OK] log")
    
    # Test 3: Query
    results = logger.query(source_role="Secretary")
    assert len(results) == 1
    print("[OK] query")
    
    # Test 4: Verify chain
    assert logger.verify_chain() == True
    print("[OK] verify_chain")
    
    # Test 5: Statistics
    stats = logger.get_statistics()
    assert stats["total_transactions"] == 1
    print("[OK] get_statistics")
    
    print("[PASS] All audit tests passed!")


if __name__ == "__main__":
    test_audit()