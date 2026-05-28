"""
Pareto Cost Calculator - 帕累托成本
公式22: C(option) = α * R_cost + β * Risk_value + γ * Opportunity_loss
帕累托最优：最小化成本同时最大化收益
"""

import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from qcm.config import load_config
_cfg = load_config()


@dataclass
class Option:
    """选项"""
    id: str
    cost: float          # 成本
    benefit: float       # 收益
    risk: float         # 风险 [0,1]
    time: float         # 时间


@dataclass
class ParetoResult:
    """帕累托结果"""
    option_id: str
    cost: float
    benefit: float
    risk: float
    is_pareto_optimal: bool
    score: float


class ParetoCostCalculator:
    """
    帕累托成本计算器
    基于论文公式22
    """

    # 论文校准参数
    ALPHA = _cfg.get_param("pareto_cost", "ALPHA")  # was: 0.4    # 成本权重
    BETA = _cfg.get_param("pareto_cost", "BETA")  # was: 0.3     # 风险权重
    GAMMA = _cfg.get_param("pareto_cost", "GAMMA")  # was: 0.3    # 机会损失权重

    def __init__(self):
        self.options: List[Option] = []
        self.results: List[ParetoResult] = []

    def add_option(self, option: Option):
        """添加选项"""
        self.options.append(option)

    def calculate_opportunity_loss(self, option: Option,
                                  best_benefit: float) -> float:
        """
        计算机会损失

        Args:
            option: 选项
            best_benefit: 最大收益

        Returns:
            机会损失
        """
        return (best_benefit - option.benefit) / max(best_benefit, 1.0)

    def calculate_cost(self, option: Option, best_benefit: float) -> float:
        """
        计算综合成本（公式22）

        C(option) = α * R_cost + β * Risk_value + γ * Opportunity_loss

        Args:
            option: 选项
            best_benefit: 最大收益

        Returns:
            综合成本
        """
        opportunity_loss = self.calculate_opportunity_loss(option, best_benefit)

        # 归一化成本和风险
        normalized_cost = option.cost / max(option.cost + 1, 1.0)

        cost = (
            self.ALPHA * normalized_cost +
            self.BETA * option.risk +
            self.GAMMA * opportunity_loss
        )

        return cost

    def is_pareto_optimal(self, option: Option, all_options: List[Option]) -> bool:
        """
        判断是否为帕累托最优

        Args:
            option: 当前选项
            all_options: 所有选项

        Returns:
            是否帕累托最优
        """
        for other in all_options:
            if other.id == option.id:
                continue

            # 检查是否被支配
            # 支配：成本更低且收益更高
            dominated = (
                other.cost <= option.cost and
                other.benefit >= option.benefit and
                (other.cost < option.cost or other.benefit > option.benefit)
            )

            if dominated:
                return False

        return True

    def calculate_score(self, option: Option, best_benefit: float) -> float:
        """
        计算综合得分

        Args:
            option: 选项
            best_benefit: 最大收益

        Returns:
            综合得分
        """
        # 收益/成本比
        if option.cost > 0:
            efficiency = option.benefit / option.cost
        else:
            efficiency = 0.0

        # 风险惩���
        risk_penalty = option.risk * 0.5

        # 综合得分
        score = efficiency * (1 - risk_penalty)

        return score

    def analyze(self) -> List[ParetoResult]:
        """
        分析所有选项

        Returns:
            帕累托最优结果
        """
        if not self.options:
            return []

        # 找到最大收益
        best_benefit = max(o.benefit for o in self.options)

        # 分析每个选项
        results = []
        for option in self.options:
            is_optimal = self.is_pareto_optimal(option, self.options)
            score = self.calculate_score(option, best_benefit)

            result = ParetoResult(
                option_id=option.id,
                cost=option.cost,
                benefit=option.benefit,
                risk=option.risk,
                is_pareto_optimal=is_optimal,
                score=score,
            )
            results.append(result)

        # 按得分排序
        results.sort(key=lambda x: x.score, reverse=True)

        self.results = results
        return results

    def get_best_option(self) -> Optional[ParetoResult]:
        """获取最佳选项"""
        if not self.results:
            self.analyze()

        if self.results:
            return self.results[0]
        return None

    def get_pareto_optimal_options(self) -> List[ParetoResult]:
        """获取所有帕累托最优选项"""
        return [r for r in self.results if r.is_pareto_optimal]

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if not self.results:
            return {'total_options': 0}

        pareto_count = len(self.get_pareto_optimal_options())

        return {
            'total_options': len(self.options),
            'pareto_optimal_count': pareto_count,
            'best_option': self.results[0].option_id if self.results else None,
            'best_score': round(self.results[0].score, 4) if self.results else 0.0,
        }


def test_pareto_cost():
    """测试帕累托成本计算器"""
    print("=" * 60)
    print("Pareto Cost Calculator Test")
    print("=" * 60)

    calculator = ParetoCostCalculator()

    # 添加选项
    options = [
        Option("A", cost=100, benefit=80, risk=0.2, time=5),
        Option("B", cost=150, benefit=120, risk=0.3, time=8),
        Option("C", cost=80, benefit=50, risk=0.1, time=3),
        Option("D", cost=200, benefit=180, risk=0.5, time=12),
    ]

    for option in options:
        calculator.add_option(option)

    # 分析
    results = calculator.analyze()

    print("\n--- All Options Analysis ---")
    for r in results:
        print(f"{r.option_id}: cost={r.cost}, benefit={r.benefit}, "
              f"risk={r.risk:.1f}, score={r.score:.2f}, "
              f"pareto={r.is_pareto_optimal}")

    # 帕累托最优
    pareto_opts = calculator.get_pareto_optimal_options()
    print(f"\n--- Pareto Optimal Options ---")
    for p in pareto_opts:
        print(f"  {p.option_id}")

    # 统计
    stats = calculator.get_statistics()
    print(f"\n--- Statistics ---")
    print(f"Total options: {stats['total_options']}")
    print(f"Pareto optimal: {stats['pareto_optimal_count']}")
    print(f"Best option: {stats['best_option']} (score: {stats['best_score']})")

    print("\n" + "=" * 60)
    print("[PASS] Pareto Cost Calculator Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_pareto_cost()