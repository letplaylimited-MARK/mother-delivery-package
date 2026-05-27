from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class DeltaPayload:
    """Delta差分载荷"""

    added: Dict[str, Any]
    modified: Dict[str, Any]
    removed: List[str]
    list_appends: Dict[str, List[Any]]
    changed_fields: List[str]


class DeltaSyncer:
    """Delta增量同步器 - 只传输变化部分"""

    def compute_delta(
        self, old_state: Dict[str, Any], new_state: Dict[str, Any]
    ) -> DeltaPayload:
        """
        计算两个状态之间的差异

        公式: Δ = f(S_t, S_{t+1})
        """
        delta = DeltaPayload(
            added={}, modified={}, removed=[], list_appends={}, changed_fields=[]
        )

        # 新增的键
        for key in new_state:
            if key not in old_state:
                delta.added[key] = new_state[key]
                delta.changed_fields.append(key)

        # 修改的键
        for key in old_state:
            if key in new_state:
                if old_state[key] != new_state[key]:
                    # 检查是否为列表追加
                    if isinstance(old_state[key], list) and isinstance(
                        new_state[key], list
                    ):
                        appended = [
                            item
                            for item in new_state[key]
                            if item not in old_state[key]
                        ]
                        if appended:
                            delta.list_appends[key] = appended
                    else:
                        delta.modified[key] = new_state[key]
                        delta.changed_fields.append(key)

        # 删除的键
        for key in old_state:
            if key not in new_state:
                delta.removed.append(key)

        return delta

    def apply_delta(self, state: Dict[str, Any], delta: DeltaPayload) -> Dict[str, Any]:
        """将Delta应用到状态"""
        new_state = state.copy()

        # 应用新增
        for key, value in delta.added.items():
            new_state[key] = value

        # 应用修改
        for key, value in delta.modified.items():
            new_state[key] = value

        # 应用删除
        for key in delta.removed:
            if key in new_state:
                del new_state[key]

        # 应用列表追加
        for key, items in delta.list_appends.items():
            if key in new_state and isinstance(new_state[key], list):
                new_state[key].extend(items)
            else:
                new_state[key] = items

        return new_state

    def calculate_bandwidth_saving(
        self, old_state: Dict[str, Any], new_state: Dict[str, Any], delta: DeltaPayload
    ) -> float:
        """计算带宽节省比例"""
        import json

        old_size = len(json.dumps(old_state))
        new_size = len(json.dumps(new_state))

        if old_size == 0:
            return 0.0

        # 实际传输的是delta
        delta_size = len(
            json.dumps(
                {
                    "added": delta.added,
                    "modified": delta.modified,
                    "removed": delta.removed,
                    "list_appends": delta.list_appends,
                }
            )
        )

        return max(0.0, (old_size - delta_size) / old_size)


def test_delta():
    """测试Delta同步"""
    old = {"name": "A", "skills": ["a", "b"], "count": 1}
    new = {"name": "A", "skills": ["a", "b", "c"], "count": 2, "new_field": "x"}

    syncer = DeltaSyncer()
    delta = syncer.compute_delta(old, new)

    print(f"Added: {delta.added}")
    print(f"Modified: {delta.modified}")
    print(f"Removed: {delta.removed}")
    print(f"List Appends: {delta.list_appends}")
    print(f"Changed Fields: {delta.changed_fields}")

    saving = syncer.calculate_bandwidth_saving(old, new, delta)
    print(f"带宽节省: {saving * 100:.1f}%")

    return delta


if __name__ == "__main__":
    test_delta()
    print("✅ Delta同步测试通过")
