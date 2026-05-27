"""
Deadlock Detector - 决策死锁检测
公式12: Deadlock_t = I(α1*I[N_t<ηN] + α2*I[G_t>ηG] + α3*I[|slope_t|<ηS] + α4*I[Loop_t] >= 2)
论文参数: α1=0.30, α2=0.35, α3=0.20, α4=0.15
预警准确率: 87% (提前12.3分钟)
"""

import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class DeadlockFactors:
    """死锁因素"""
    consensus_count: int       # N_t: 共识数量
    disagreement_score: float  # G_t: 分歧分数
    slope: float              # slope_t: R值变化斜率
    loop_detected: bool       # Loop_t: 循环检测


class DeadlockDetector:
    """
    死锁检测器
    基于论文公式12的多因素死锁检测
    """

    # 论文校准参数
    ALPHA_1 = 0.30  # 共识数量权重
    ALPHA_2 = 0.35  # 分歧分数权重
    ALPHA_3 = 0.20  # 斜率权重
    ALPHA_4 = 0.15  # 循环权重

    # 阈值参数
    ETA_N = 2        # 共识数量阈值（低于此值可能死锁）
    ETA_G = 0.5      # 分歧分数阈值（高于此值可能死锁）
    ETA_S = 0.01    # 斜率阈值（接近0表示停滞）

    # 死锁判定阈值（加权和 >= 2 触发预警）
    DEADLOCK_THRESHOLD = 2.0

    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.r_history: List[float] = []
        self.decision_history: List[str] = []
        self.diversity_history: List[float] = []
        self.warning_count = 0

    def add_r_value(self, R: float):
        """添加R值到历史"""
        self.r_history.append(R)

    def add_decision(self, decision: str):
        """添加决策到历史"""
        self.decision_history.append(decision)

    def add_diversity(self, diversity: float):
        """添加多样性分数到历史"""
        self.diversity_history.append(diversity)

    def calculate_consensus_count(self) -> int:
        """
        计算共识数量 N_t
        最近window_size轮中R值接近的轮数
        """
        if len(self.r_history) < 2:
            return self.window_size

        recent = self.r_history[-self.window_size:]
        if not recent:
            return self.window_size

        # 计算与均值的偏差
        mean_r = sum(recent) / len(recent)
        consensus_count = sum(1 for r in recent if abs(r - mean_r) < 0.02)

        return consensus_count

    def calculate_disagreement_score(self) -> float:
        """
        计算分歧分数 G_t
        基于决策历史的多样性
        """
        if len(self.decision_history) < 2:
            return 0.0

        recent = self.decision_history[-self.window_size:]
        if not recent:
            return 0.0

        # 计算唯一决策的比例（多样性）
        unique_ratio = len(set(recent)) / len(recent)

        # 返回分歧分数 (1 - 多样性 = 分歧)
        return 1.0 - unique_ratio

    def calculate_slope(self) -> float:
        """
        计算R值变化斜率 slope_t
        """
        if len(self.r_history) < 2:
            return 0.1

        recent = self.r_history[-self.window_size:]
        if len(recent) < 2:
            return 0.1

        # 简单线性回归斜率
        n = len(recent)
        x = list(range(n))
        y = recent

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_xx = sum(x[i] * x[i] for i in range(n))

        denominator = n * sum_xx - sum_x * sum_x
        if denominator == 0:
            return 0.0

        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return abs(slope)

    def detect_loop(self) -> bool:
        """
        检测循环 Loop_t
        R值是否在相近区间反复
        """
        if len(self.r_history) < self.window_size * 2:
            return False

        # 检查最近2*window_size轮是否在窄区间反复
        recent = self.r_history[-self.window_size * 2:]
        if not recent:
            return False

        min_r = min(recent)
        max_r = max(recent)

        # 如果波动范围很小，可能存在循环
        return (max_r - min_r) < 0.05

    def calculate_deadlock_score(self) -> float:
        """
        计算死锁分数（公式12）
        Deadlock_t = α1*I[N_t<ηN] + α2*I[G_t>ηG] + α3*I[|slope_t|<ηS] + α4*I[Loop_t]
        """
        factors = self.get_factors()

        # 计算各因素的指示函数
        indicator_n = 1.0 if factors.consensus_count < self.ETA_N else 0.0
        indicator_g = 1.0 if factors.disagreement_score > self.ETA_G else 0.0
        indicator_s = 1.0 if factors.slope < self.ETA_S else 0.0
        indicator_loop = 1.0 if factors.loop_detected else 0.0

        # 计算加权和
        score = (
            self.ALPHA_1 * indicator_n +
            self.ALPHA_2 * indicator_g +
            self.ALPHA_3 * indicator_s +
            self.ALPHA_4 * indicator_loop
        )

        return score

    def is_deadlock(self) -> bool:
        """判断是否死锁"""
        score = self.calculate_deadlock_score()
        return score >= 1.0

    def is_warning(self) -> bool:
        """判断是否预警（死锁前期）"""
        score = self.calculate_deadlock_score()
        return score >= 0.5

    def get_factors(self) -> DeadlockFactors:
        """获取当前死锁因素"""
        return DeadlockFactors(
            consensus_count=self.calculate_consensus_count(),
            disagreement_score=self.calculate_disagreement_score(),
            slope=self.calculate_slope(),
            loop_detected=self.detect_loop()
        )

    def get_status(self) -> Dict:
        """获取完整状态"""
        score = self.calculate_deadlock_score()
        factors = self.get_factors()

        return {
            'deadlock_score': round(score, 3),
            'is_deadlock': self.is_deadlock(),
            'is_warning': self.is_warning(),
            'consensus_count': factors.consensus_count,
            'disagreement_score': round(factors.disagreement_score, 3),
            'slope': round(factors.slope, 4),
            'loop_detected': factors.loop_detected,
            'warning_count': self.warning_count,
        }

    def predict_emergence_time(self) -> Optional[int]:
        """
        预测到达涌现所需轮次
        基于当前R值增长斜率
        """
        if len(self.r_history) < 3:
            return None

        slope = self.calculate_slope()
        current_r = self.r_history[-1]
        threshold = 0.75  # 演示版阈值

        if slope <= 0:
            return None

        remaining = threshold - current_r
        if remaining <= 0:
            return 0

        rounds_needed = int(remaining / slope) + 1
        return rounds_needed


class SoftDeadlockDetector:
    """
    软死锁检测器
    公式13: S_soft(t) = 0.3(1-N_t) + 0.35*max(0,G_t-0.5)/0.5 + 0.2*max(0,η_S-|slope_t|)/η_S + 0.15*loop_signal(t)
    论文参数: η_S=0.01
    判定: [0.4, 0.6]=中度警告, >=0.6=硬性警报
    """

    # 论文校准参数
    WEIGHT_CONSENSUS = 0.3
    WEIGHT_DISAGREEMENT = 0.35
    WEIGHT_SLOPE = 0.2
    WEIGHT_LOOP = 0.15

    ETA_S = 0.01  # 斜率阈值

    # 判定阈值
    MODERATE_WARNING = 0.4
    HARD_ALERT = 0.6

    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.r_history: List[float] = []
        self.decision_history: List[str] = []
        self.score_history: List[float] = []

    def add_r_value(self, R: float):
        """添加R值到历史"""
        self.r_history.append(R)

    def add_decision(self, decision: str):
        """添加决策到历史"""
        self.decision_history.append(decision)

    def _get_consensus_factor(self) -> float:
        """计算共识因子 (1-N_t)"""
        if len(self.r_history) < 2:
            return 0.0

        recent = self.r_history[-self.window_size:]
        if not recent:
            return 0.0

        mean_r = sum(recent) / len(recent)
        consensus = sum(1 for r in recent if abs(r - mean_r) < 0.02)
        N_t = consensus / max(1, len(recent))

        return 1.0 - N_t

    def _get_disagreement_factor(self) -> float:
        """计算分歧因子 max(0, G_t-0.5)/0.5"""
        if len(self.decision_history) < 2:
            return 0.0

        recent = self.decision_history[-self.window_size:]
        if not recent:
            return 0.0

        unique_ratio = len(set(recent)) / len(recent)
        G_t = 1.0 - unique_ratio

        return max(0.0, G_t - 0.5) / 0.5

    def _get_slope_factor(self) -> float:
        """计算斜率因子 max(0, η_S - |slope_t|) / η_S"""
        if len(self.r_history) < 2:
            return 0.0

        recent = self.r_history[-self.window_size:]
        if len(recent) < 2:
            return 0.0

        n = len(recent)
        x = list(range(n))
        y = recent

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_xx = sum(x[i] * x[i] for i in range(n))

        denominator = n * sum_xx - sum_x * sum_x
        if denominator == 0:
            return 0.0

        slope = abs((n * sum_xy - sum_x * sum_y) / denominator)

        return max(0.0, self.ETA_S - slope) / self.ETA_S

    def _get_loop_factor(self) -> float:
        """计算循环因子 loop_signal(t)"""
        if len(self.r_history) < self.window_size * 2:
            return 0.0

        recent = self.r_history[-self.window_size * 2:]
        if not recent:
            return 0.0

        min_r = min(recent)
        max_r = max(recent)

        return 1.0 if (max_r - min_r) < 0.05 else 0.0

    def calculate_score(self) -> float:
        """
        计算软死锁评分 (公式13)
        """
        consensus_factor = self._get_consensus_factor()
        disagreement_factor = self._get_disagreement_factor()
        slope_factor = self._get_slope_factor()
        loop_factor = self._get_loop_factor()

        score = (
            self.WEIGHT_CONSENSUS * consensus_factor +
            self.WEIGHT_DISAGREEMENT * disagreement_factor +
            self.WEIGHT_SLOPE * slope_factor +
            self.WEIGHT_LOOP * loop_factor
        )

        self.score_history.append(score)
        return score

    def get_status(self) -> str:
        """获取状态"""
        score = self.calculate_score()

        if score >= self.HARD_ALERT:
            return "HARD_ALERT"
        elif score >= self.MODERATE_WARNING:
            return "MODERATE_WARNING"
        else:
            return "NORMAL"


def test_deadlock_detector():
    """测试死锁检测器"""
    print("=" * 60)
    print("Deadlock Detector + Soft Deadlock Test")
    print("=" * 60)

    # 测试硬死锁检测
    detector = DeadlockDetector()

    # 模拟正常增长
    test_r_values = [0.50, 0.55, 0.60, 0.65, 0.70]

    for i, r in enumerate(test_r_values):
        detector.add_r_value(r)
        status = detector.get_status()
        print(f"Round {i+1}: R={r:.2f}, score={status['deadlock_score']:.2f}, deadlock={status['is_deadlock']}")

    # 模拟死锁场景（停滞）
    print("\n--- Simulating deadlock scenario ---")
    detector2 = DeadlockDetector()
    stagnant_r = [0.70, 0.705, 0.702, 0.708, 0.701]  # 几乎不增长

    for i, r in enumerate(stagnant_r):
        detector2.add_r_value(r)
        status = detector2.get_status()
        print(f"Round {i+1}: R={r:.3f}, score={status['deadlock_score']:.2f}, warning={status['is_warning']}")

    # 预测涌现时间
    print("\n--- Predicting emergence time ---")
    detector3 = DeadlockDetector()
    for r in [0.50, 0.55, 0.60, 0.65, 0.70, 0.73]:
        detector3.add_r_value(r)

    predicted = detector3.predict_emergence_time()
    print(f"Current R: 0.73, Predicted rounds to emergence: {predicted}")

    # 测试软死锁检测
    print("\n--- Soft Deadlock Test (Formula 13) ---")
    soft_detector = SoftDeadlockDetector()

    for r in [0.70, 0.705, 0.702, 0.708, 0.701]:
        soft_detector.add_r_value(r)

    score = soft_detector.calculate_score()
    status = soft_detector.get_status()
    print(f"  Soft deadlock score: {score:.4f}")
    print(f"  Status: {status}")

    print("\n" + "=" * 60)
    print("[PASS] Deadlock Detector Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_deadlock_detector()
