"""
Ghost Channel - Unit Tests: Delta Calculator
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "python"))

from ghost_channel.core.delta import DeltaCalculator, DeltaPayload


class TestDeltaCalculator(unittest.TestCase):
    """Delta计算器单元测试"""

    def test_calculate_delta_added(self):
        """测试新增实体"""
        old_state = {"a": 1, "b": 2}
        new_state = {"a": 1, "b": 2, "c": 3}

        delta = DeltaCalculator.calculate_delta(old_state, new_state)

        self.assertEqual(delta.added, {"c": 3})
        self.assertEqual(delta.modified, {})
        self.assertEqual(delta.removed, [])

    def test_calculate_delta_modified(self):
        """测试修改实体"""
        old_state = {"a": 1, "b": 2}
        new_state = {"a": 10, "b": 2}

        delta = DeltaCalculator.calculate_delta(old_state, new_state)

        self.assertEqual(delta.modified, {"a": 10})

    def test_calculate_delta_removed(self):
        """测试删除实体"""
        old_state = {"a": 1, "b": 2}
        new_state = {"a": 1}

        delta = DeltaCalculator.calculate_delta(old_state, new_state)

        self.assertEqual(delta.removed, ["b"])

    def test_calculate_delta_list_appends(self):
        """测试列表追加"""
        old_state = {"items": [1, 2, 3]}
        new_state = {"items": [1, 2, 3, 4, 5]}

        delta = DeltaCalculator.calculate_delta(old_state, new_state)

        self.assertEqual(delta.list_appends, {"items": [4, 5]})

    def test_apply_delta(self):
        """测试应用Delta"""
        state = {"a": 1, "b": 2}
        delta = DeltaPayload(
            added={"c": 3},
            modified={"a": 10},
            removed=["b"],
        )

        result = DeltaCalculator.apply_delta(state, delta)

        self.assertEqual(result, {"a": 10, "c": 3})
        self.assertNotIn("b", result)

    def test_bandwidth_reduction(self):
        """测试带宽降低"""
        old_state = {"data": "x" * 1000}
        new_state = {"data": "x" * 1001}

        delta = DeltaCalculator.calculate_delta(old_state, new_state)
        original_size = len(str(old_state))
        delta_size = delta.size_bytes()

        reduction = 1 - (delta_size / original_size)

        # Delta应该比原始数据小
        self.assertGreater(original_size, delta_size)


class TestDeltaPayload(unittest.TestCase):
    """DeltaPayload测试"""

    def test_change_count(self):
        """测试变更计数"""
        delta = DeltaPayload(
            added={"a": 1, "b": 2},
            modified={"c": 3},
            removed=["d"],
            list_appends={"e": [1, 2]},
        )

        self.assertEqual(delta.change_count(), 5)


if __name__ == "__main__":
    unittest.main()
