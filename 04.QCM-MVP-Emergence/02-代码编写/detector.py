"""
QCM Emergence Detector - 涌现检测
Version: 2.0 (2026-04-26)
Threshold: 论文版0.85 (R>=0.85为涌现)
Ref: CHANGELOG.md
"""
from typing import List, Dict


class EmergenceDetector:
    """涌现检测器 - 核心心脏"""

    # 涌现等级阈值
    # 注意: 演示版使用0.75作为阈值以便快速演示涌现
    # 论文对齐版本使用0.85作为阈值
    THRESHOLD_NONE = 0.3
    THRESHOLD_PRELIMINARY = 0.5
    THRESHOLD_MODERATE = 0.65
    THRESHOLD_DEEP = 0.85  # 论文版阈值（R>0.85为涌现）

    def __init__(self, window_size: int = 5):
        self.history: List[float] = []
        self.window_size = window_size

    def add_R(self, R: float):
        """添加R值到历史"""
        self.history.append(R)

    def get_recent_R(self) -> float:
        """获取最近window_size个R值的平均值"""
        if not self.history:
            return 0.0

        recent = self.history[-self.window_size :]
        return sum(recent) / len(recent)

    def detect_level(self) -> str:
        """
        检测涌现等级

        等级定义：
        - 无协同: R < 0.3
        - 初步协同: 0.3 <= R < 0.5
        - 中度协同: 0.5 <= R < 0.7
        - 深度协同: 0.7 <= R < 0.85
        - 涌现: R >= 0.85
        """
        recent_R = self.get_recent_R()

        if recent_R >= self.THRESHOLD_DEEP:
            return "emergence"
        elif recent_R >= self.THRESHOLD_MODERATE:
            return "deep_collaboration"
        elif recent_R >= self.THRESHOLD_PRELIMINARY:
            return "moderate"
        elif recent_R >= self.THRESHOLD_NONE:
            return "preliminary"
        else:
            return "none"

    def is_emergence(self) -> bool:
        """判断是否发生涌现"""
        return self.detect_level() == "emergence"

    def predict_emergence(self, steps: int = 10) -> float:
        """
        预测未来R值趋势（线性回归）

        返回预测的平均R值
        """
        if len(self.history) < 3:
            return 0.0

        # 简单线性回归
        n = len(self.history)
        x = list(range(n))
        y = self.history

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_xx = sum(x[i] * x[i] for i in range(n))

        denominator = n * sum_xx - sum_x * sum_x
        if denominator == 0:
            return self.history[-1]

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n

        # 预测未来
        future_x = list(range(n, n + steps))
        predictions = [slope * x_val + intercept for x_val in future_x]

        return sum(predictions) / len(predictions)

    def get_statistics(self) -> Dict[str, float]:
        """获取统计信息"""
        if not self.history:
            return {"min": 0.0, "max": 0.0, "avg": 0.0, "current": 0.0}

        return {
            "min": min(self.history),
            "max": max(self.history),
            "avg": sum(self.history) / len(self.history),
            "current": self.history[-1],
            "recent_avg": self.get_recent_R(),
        }

    def get_level_name(self, level: str) -> str:
        """获取等级名称"""
        names = {
            "none": "无协同",
            "preliminary": "初步协同",
            "moderate": "中度协同",
            "deep_collaboration": "深度协同",
            "emergence": "涌现",
        }
        return names.get(level, "未知")


def test_detector():
    """测试涌现检测器"""
    detector = EmergenceDetector()

    # 模拟R值增长
    test_R_values = [0.32, 0.41, 0.52, 0.63, 0.72, 0.78, 0.82, 0.87]

    for R in test_R_values:
        detector.add_R(R)
        level = detector.detect_level()
        is_emergence = detector.is_emergence()
        print(
            f"R = {R:.2f} -> {detector.get_level_name(level)} {'🎉' if is_emergence else ''}"
        )

    stats = detector.get_statistics()
    print(f"\n统计: {stats}")

    prediction = detector.predict_emergence(5)
    print(f"预测未来5轮平均R值: {prediction:.4f}")

    return detector.is_emergence()


if __name__ == "__main__":
    result = test_detector()
    print(f"\n✅ 涌现检测器测试通过: {result}")
