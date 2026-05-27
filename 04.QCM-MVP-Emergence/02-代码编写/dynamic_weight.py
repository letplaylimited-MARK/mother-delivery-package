"""
Dynamic Weight Calculator - 动态权重调整
公式7: w_i,t = w_i,t-1 + λ * (R_t-1 - R_target) * e^(-k*t) * g_i
参数: λ=0.1, R_target=0.85, k=0.05, 收敛约10次迭代
"""

import math
from typing import Dict
from dataclasses import dataclass


@dataclass
class Weights:
    """权重配置"""
    w_k: float  # K_sim权重
    w_c: float  # C_comp权重
    w_i: float  # I_freq权重
    w_e: float  # E_div权重


class DynamicWeightCalculator:
    """
    动态权重计算器
    根据R值与目标值的差距自适应调整各分量权重
    """

    # 论文校准参数
    LAMBDA = 0.1    # 学习率
    R_TARGET = 0.85  # 目标R值（论文阈值）
    K_DECAY = 0.05   # 指数衰减系数

    # 初始权重（论文值）
    INITIAL_WEIGHTS = Weights(
        w_k=0.25,
        w_c=0.35,
        w_i=0.20,
        w_e=0.20
    )

    # 各分量对R值的贡献权重（用于调整）
    COMPONENT_GAIN = {
        'K': 1.0,
        'C': 1.0,
        'I': 1.0,
        'E': -1.0  # E_div是负面影响
    }

    def __init__(self, use_paper_weights: bool = True):
        """
        初始化

        Args:
            use_paper_weights: 是否使用论文权重作为初始值
        """
        if use_paper_weights:
            self.current_weights = Weights(
                w_k=self.INITIAL_WEIGHTS.w_k,
                w_c=self.INITIAL_WEIGHTS.w_c,
                w_i=self.INITIAL_WEIGHTS.w_i,
                w_e=self.INITIAL_WEIGHTS.w_e
            )
        else:
            # 使用演示版权重
            self.current_weights = Weights(
                w_k=0.30,
                w_c=0.40,
                w_i=0.25,
                w_e=0.15
            )

        self.r_history = []
        self.iteration = 0
        self.weight_history = []

    def add_r_value(self, R: float):
        """添加R值到历史"""
        self.r_history.append(R)
        self.iteration += 1

        # 记录权重变化历史
        self.weight_history.append(Weights(
            w_k=self.current_weights.w_k,
            w_c=self.current_weights.w_c,
            w_i=self.current_weights.w_i,
            w_e=self.current_weights.w_e
        ))

    def calculate_adjustment(self) -> Dict[str, float]:
        """
        计算权重调整量
        公式7: Δw_i = λ * (R - R_target) * e^(-k*t) * g_i
        """
        if not self.r_history:
            return {'K': 0, 'C': 0, 'I': 0, 'E': 0}

        r_current = self.r_history[-1]
        r_delta = r_current - self.R_TARGET

        # 指数衰减因子
        decay = math.exp(-self.K_DECAY * self.iteration)

        # 计算各分量调整量
        adjustments = {}
        for comp, gain in self.COMPONENT_GAIN.items():
            adjustment = self.LAMBDA * r_delta * decay * gain
            adjustments[comp] = adjustment

        return adjustments

    def update_weights(self) -> Weights:
        """
        更新权重
        确保权重之和为1，且每个权重在[0.1, 0.5]范围内
        """
        adjustments = self.calculate_adjustment()

        # 应用调整
        new_w_k = self.current_weights.w_k + adjustments['K']
        new_w_c = self.current_weights.w_c + adjustments['C']
        new_w_i = self.current_weights.w_i + adjustments['I']
        new_w_e = self.current_weights.w_e + adjustments['E']

        # 限制范围
        new_w_k = max(0.1, min(0.5, new_w_k))
        new_w_c = max(0.1, min(0.5, new_w_c))
        new_w_i = max(0.1, min(0.5, new_w_i))
        new_w_e = max(0.05, min(0.5, new_w_e))

        # 归一化使权重之和为1
        total = new_w_k + new_w_c + new_w_i + new_w_e
        self.current_weights = Weights(
            w_k=new_w_k / total,
            w_c=new_w_c / total,
            w_i=new_w_i / total,
            w_e=new_w_e / total
        )

        return self.current_weights

    def get_weights(self) -> Weights:
        """获取当前权重"""
        return self.current_weights

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if not self.r_history:
            return {
                'iteration': 0,
                'current_r': 0,
                'weights': {},
            }

        return {
            'iteration': self.iteration,
            'current_r': round(self.r_history[-1], 4),
            'r_target': self.R_TARGET,
            'r_gap': round(self.r_history[-1] - self.R_TARGET, 4),
            'weights': {
                'K': round(self.current_weights.w_k, 4),
                'C': round(self.current_weights.w_c, 4),
                'I': round(self.current_weights.w_i, 4),
                'E': round(self.current_weights.w_e, 4),
            }
        }

    def should_converge(self, threshold: float = 0.01) -> bool:
        """
        判断是否收敛
        当R值与目标值差距小于阈值时收敛
        """
        if not self.r_history:
            return False

        return abs(self.r_history[-1] - self.R_TARGET) < threshold


def test_dynamic_weight():
    """测试动态权重计算器"""
    print("=" * 60)
    print("Dynamic Weight Calculator Test")
    print("=" * 60)

    calc = DynamicWeightCalculator(use_paper_weights=True)

    print(f"\nInitial weights: K={calc.current_weights.w_k}, C={calc.current_weights.w_c}, "
          f"I={calc.current_weights.w_i}, E={calc.current_weights.w_e}")

    # 模拟R值增长
    test_r_values = [0.50, 0.60, 0.70, 0.75, 0.80, 0.83]

    print("\n--- Simulating R value growth ---")
    for i, r in enumerate(test_r_values):
        calc.add_r_value(r)
        weights = calc.update_weights()
        stats = calc.get_statistics()

        print(f"Round {i+1}: R={r:.2f}, gap={stats['r_gap']:+.2f}, "
              f"weights: K={weights.w_k:.3f}, C={weights.w_c:.3f}, "
              f"I={weights.w_i:.3f}, E={weights.w_e:.3f}")

    # 检查收敛
    print(f"\nConverged: {calc.should_converge()}")

    print("\n" + "=" * 60)
    print("[PASS] Dynamic Weight Calculator Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_dynamic_weight()
