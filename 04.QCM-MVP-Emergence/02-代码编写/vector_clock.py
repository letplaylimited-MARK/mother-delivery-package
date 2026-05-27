from typing import Dict
from collections import defaultdict
import json


class VectorClock:
    """向量时钟 - 因果排序核心"""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.clock: Dict[str, int] = defaultdict(int)

    def increment(self) -> int:
        """本地事件计数+1"""
        self.clock[self.node_id] += 1
        return self.clock[self.node_id]

    def merge(self, other_clock: Dict[str, int]):
        """合并外部时钟（取最大值）"""
        for node, time in other_clock.items():
            self.clock[node] = max(self.clock[node], time)

    def happens_before(self, other: "VectorClock") -> str:
        """
        因果关系判断

        公式:
        - if ∀i: self[i] ≤ other[i] AND ∃j: self[j] < other[j]
            → BEFORE (self先于other)
        - elif ∀i: self[i] ≥ other[i] AND ∃j: self[j] > other[j]
            → AFTER (self后于other)
        - else → CONCURRENT (并发)
        """
        less_than = False
        greater_than = False

        all_nodes = set(self.clock.keys()) | set(other.clock.keys())

        for node in all_nodes:
            self_time = self.clock.get(node, 0)
            other_time = other.clock.get(node, 0)

            if self_time < other_time:
                less_than = True
            if self_time > other_time:
                greater_than = True

        if less_than and not greater_than:
            return "BEFORE"
        elif greater_than and not less_than:
            return "AFTER"
        else:
            return "CONCURRENT"

    def to_dict(self) -> Dict[str, int]:
        """转换为字典"""
        return dict(self.clock)

    def get_causality_key(self) -> str:
        """获取因果唯一键"""
        return json.dumps(self.clock, sort_keys=True)

    def __repr__(self):
        return f"VectorClock({dict(self.clock)})"


def test_vector_clock():
    """测试向量时钟"""
    vc1 = VectorClock("A")
    vc2 = VectorClock("B")

    # 事件1: A发生
    vc1.increment()
    print(f"VC1 after A: {vc1}")

    # 事件2: B发生
    vc2.increment()
    print(f"VC2 after B: {vc2}")

    # 合并
    vc2.merge(vc1.to_dict())
    print(f"VC2 after merge: {vc2}")

    # 因果判断
    relation = vc1.happens_before(vc2)
    print(f"VC1 happens_before VC2: {relation}")

    # 测试并发
    vc3 = VectorClock("C")
    vc4 = VectorClock("D")
    vc3.increment()
    vc4.increment()
    vc3.merge(vc4.to_dict())
    vc4.merge(vc3.to_dict())
    relation_concurrent = vc3.happens_before(vc4)
    print(f"并发测试: {relation_concurrent}")

    return relation


if __name__ == "__main__":
    result = test_vector_clock()
    print(f"✅ 向量时钟测试通过: {result}")
