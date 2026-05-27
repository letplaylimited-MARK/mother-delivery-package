"""
Ghost Channel - Unit Tests: Vector Clock
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "python"))

from ghost_channel.core.vector_clock import VectorClock, CausalityTracker


class TestVectorClock(unittest.TestCase):
    """向量时钟单元测试"""

    def test_increment(self):
        """测试递增"""
        vc = VectorClock()
        vc.increment("node_a")

        self.assertEqual(vc.clocks["node_a"], 1)

    def test_merge(self):
        """测试合并"""
        vc1 = VectorClock(clocks={"a": 1, "b": 2})
        vc2 = VectorClock(clocks={"b": 1, "c": 3})

        vc1.merge(vc2)

        self.assertEqual(vc1.clocks["a"], 1)
        self.assertEqual(vc1.clocks["b"], 2)
        self.assertEqual(vc1.clocks["c"], 3)

    def test_happens_before(self):
        """测试因果判断"""
        vc1 = VectorClock(clocks={"a": 1})
        vc2 = VectorClock(clocks={"a": 2})

        result = vc1.happens_before(vc2)

        self.assertEqual(result, "BEFORE")

    def test_happens_after(self):
        """测试因果判断 - after"""
        vc1 = VectorClock(clocks={"a": 2})
        vc2 = VectorClock(clocks={"a": 1})

        result = vc1.happens_before(vc2)

        self.assertEqual(result, "AFTER")

    def test_concurrent(self):
        """测试并发"""
        vc1 = VectorClock(clocks={"a": 1, "b": 0})
        vc2 = VectorClock(clocks={"a": 0, "b": 1})

        result = vc1.happens_before(vc2)

        self.assertEqual(result, "CONCURRENT")

    def test_is_concurrent(self):
        """测试并发判断"""
        vc1 = VectorClock(clocks={"a": 1, "b": 0})
        vc2 = VectorClock(clocks={"a": 0, "b": 1})

        self.assertTrue(vc1.is_concurrent(vc2))

    def test_copy(self):
        """测试复制"""
        vc = VectorClock(clocks={"a": 1, "b": 2})
        vc_copy = vc.copy()

        self.assertEqual(vc_copy.clocks, vc.clocks)
        self.assertIsNot(vc_copy, vc)

    def test_to_dict(self):
        """测试转换为字典"""
        vc = VectorClock(clocks={"a": 1, "b": 2})
        d = vc.to_dict()

        self.assertEqual(d, {"a": 1, "b": 2})


class TestCausalityTracker(unittest.TestCase):
    """因果追踪器测试"""

    def test_stamp_event(self):
        """测试事件打戳"""
        tracker = CausalityTracker(["node_a", "node_b"])

        stamped, clock = tracker.stamp_event("node_a", {"data": "test"})

        self.assertIn("__vector_clock__", stamped)
        self.assertEqual(stamped["__node_id__"], "node_a")

    def test_receive_event(self):
        """测试接收事件"""
        tracker = CausalityTracker(["node_a", "node_b"])

        incoming = {"data": "test", "__vector_clock__": {"node_a": 1}}
        result = tracker.receive_event("node_b", incoming)

        self.assertIn("__vector_clock__", result)

    def test_get_causality(self):
        """测试获取因果关系"""
        tracker = CausalityTracker(["node_a", "node_b"])

        tracker.stamp_event("node_a", {"data": "a1"})
        tracker.stamp_event("node_a", {"data": "a2"})
        tracker.stamp_event("node_b", {"data": "b1"})

        causality = tracker.get_causality("node_a", "node_b")

        self.assertIn(causality, ["BEFORE", "CONCURRENT"])


if __name__ == "__main__":
    unittest.main()
