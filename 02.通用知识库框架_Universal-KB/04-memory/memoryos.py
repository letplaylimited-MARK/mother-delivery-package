"""
Universal-KB MemoryOS 风格记忆系统
参考: BAI-LAB/MemoryOS (EMNLP 2025 Oral)

三层记忆架构:
- Short-term: 短期记忆 (FIFO淘汰)
- Mid-term: 中期记忆 (热度驱动)
- Long-term: 长期记忆 (知识沉淀)
"""

import json
import os
import tempfile
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import uuid


@dataclass
class MemoryConfig:
    """MemoryOS 风格配置参数"""
    short_term_capacity: int = 7
    mid_term_capacity: int = 1000
    long_term_knowledge_capacity: int = 100
    mid_term_heat_threshold: float = 5.0
    mid_term_similarity_threshold: float = 0.7
    decay_factor: float = 0.95


@dataclass
class MemoryEntry:
    """记忆条目"""
    id: str
    content: str
    timestamp: str
    memory_type: str
    heat: float = 1.0
    access_count: int = 0
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp,
            'memory_type': self.memory_type,
            'heat': self.heat,
            'access_count': self.access_count,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryEntry':
        return cls(**data)


class ShortTermMemory:
    """短期记忆 (FIFO, 容量7条)"""
    def __init__(self, storage_path: str, capacity: int = 7):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.capacity = capacity
        self._memory: List[MemoryEntry] = []

    def add(self, entry: MemoryEntry) -> List[MemoryEntry]:
        self._memory.append(entry)
        evicted = []
        while len(self._memory) > self.capacity:
            evicted.append(self._memory.pop(0))
        return evicted

    def get_all(self) -> List[MemoryEntry]:
        return self._memory.copy()


class MidTermMemory:
    """中期记忆 (热度驱动, 容量1000条)"""
    def __init__(self, storage_path: str, capacity: int = 1000,
                 heat_threshold: float = 5.0, similarity_threshold: float = 0.7):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.capacity = capacity
        self.heat_threshold = heat_threshold
        self.similarity_threshold = similarity_threshold
        self._memory: List[MemoryEntry] = []

    def add(self, entry: MemoryEntry) -> Tuple[List[MemoryEntry], Optional[MemoryEntry]]:
        promoted, evicted = [], None
        self._memory.append(entry)
        if entry.heat >= self.heat_threshold:
            promoted.append(entry)
            self._memory.remove(entry)
        while len(self._memory) > self.capacity:
            min_entry = min(self._memory, key=lambda x: x.heat)
            self._memory.remove(min_entry)
            evicted = min_entry
        return promoted, evicted

    def access(self, entry_id: str):
        for entry in self._memory:
            if entry.id == entry_id:
                entry.access_count += 1
                entry.heat = entry.heat * 0.95 + 1.0


class LongTermMemory:
    """长期记忆 (持久化, 容量100条)"""
    def __init__(self, storage_path: str, capacity: int = 100):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.capacity = capacity
        self.knowledge_path = self.storage_path / 'knowledge'
        self.strategies_path = self.storage_path / 'strategies'
        self.knowledge_path.mkdir(exist_ok=True)
        self.strategies_path.mkdir(exist_ok=True)
        self._knowledge: List[Dict] = []
        self._strategies: List[Dict] = []
        self._load_all()

    def _load_all(self):
        for f in self.knowledge_path.glob('*.json'):
            with open(f, 'r', encoding='utf-8') as fh:
                self._knowledge.append(json.load(fh))
        for f in self.strategies_path.glob('*.json'):
            with open(f, 'r', encoding='utf-8') as fh:
                self._strategies.append(json.load(fh))

    def add_knowledge(self, knowledge: Dict) -> bool:
        if len(self._knowledge) >= self.capacity:
            self._knowledge.pop(0)
        knowledge['added_at'] = datetime.now().isoformat()
        self._knowledge.append(knowledge)
        safe_name = knowledge.get('id', f"kg_{len(self._knowledge)}")
        with open(self.knowledge_path / f"{safe_name}.json", 'w', encoding='utf-8') as fh:
            json.dump(knowledge, fh, ensure_ascii=False, indent=2)
        return True

    def add_strategy(self, strategy: Dict) -> bool:
        if len(self._strategies) >= self.capacity // 2:
            self._strategies.pop(0)
        strategy['added_at'] = datetime.now().isoformat()
        self._strategies.append(strategy)
        safe_name = strategy.get('id', f"str_{len(self._strategies)}")
        with open(self.strategies_path / f"{safe_name}.json", 'w', encoding='utf-8') as fh:
            json.dump(strategy, fh, ensure_ascii=False, indent=2)
        return True

    def get_context(self, query: str = None) -> Dict:
        return {
            'knowledge': self._knowledge[-10:],
            'strategies': self._strategies
        }


class MemoryOS:
    """MemoryOS 主类"""
    def __init__(self, storage_path: str, config: MemoryConfig = None):
        self.config = config or MemoryConfig()
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.short_term = ShortTermMemory(str(self.storage_path), self.config.short_term_capacity)
        self.mid_term = MidTermMemory(str(self.storage_path), self.config.mid_term_capacity,
                               self.config.mid_term_heat_threshold, self.config.mid_term_similarity_threshold)
        self.long_term = LongTermMemory(str(self.storage_path), self.config.long_term_knowledge_capacity)

    def add_memory(self, content: str, memory_type: str = 'episodic', metadata: Dict = None) -> Dict:
        entry = MemoryEntry(
            id=str(uuid.uuid4()),
            content=content,
            timestamp=datetime.now().isoformat(),
            memory_type=memory_type,
            heat=1.0,
            metadata=metadata or {}
        )
        evicted = self.short_term.add(entry)
        promoted_to_long = []
        for ev_entry in evicted:
            promoted, _ = self.mid_term.add(ev_entry)
            promoted_to_long.extend(promoted)
        for long_entry in promoted_to_long:
            if long_entry.memory_type == 'semantic':
                self.long_term.add_knowledge({
                    'id': long_entry.id,
                    'content': long_entry.content,
                    'metadata': long_entry.metadata
                })
            elif long_entry.memory_type == 'procedural':
                self.long_term.add_strategy({
                    'id': long_entry.id,
                    'content': long_entry.content,
                    'metadata': long_entry.metadata
                })
        return {'status': 'added', 'entry_id': entry.id}

    def retrieve(self, query: str, memory_types: List[str] = None) -> Dict:
        if memory_types is None:
            memory_types = ['episodic', 'semantic', 'procedural']
        results = {
            'short_term': [e.to_dict() for e in self.short_term.get_all()],
            'mid_term': [],
            'context': self.long_term.get_context(query)
        }
        return results

    def get_summary(self) -> Dict:
        return {
            'short_term_count': len(self.short_term.get_all()),
            'mid_term_count': len(self.mid_term._memory),
            'long_term_knowledge': len(self.long_term._knowledge),
            'long_term_strategies': len(self.long_term._strategies)
        }


if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='universal_kb_memoryos_') as tmpdir:
        memory = MemoryOS(tmpdir)
        print("=== Universal-KB MemoryOS Test ===")
        memory.add_memory("测试知识: 三层架构 = raw + wiki + memory", memory_type='semantic')
        print(json.dumps(memory.get_summary(), indent=2, ensure_ascii=False))
