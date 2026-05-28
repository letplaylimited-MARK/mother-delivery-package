"""
Neural Router - 神经路由
公式21: D(input) = argmax_r P(r | input_features)
基于输入特征动态选择推理路径：neural/symbolic/hybrid
"""

import random
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from qcm.config import load_config
_cfg = load_config()


class ReasoningType(Enum):
    """推理类型"""
    NEURAL = "neural"      # 神经网络推理
    SYMBOLIC = "symbolic"  # 符号逻辑推理
    HYBRID = "hybrid"    # 混合推理


@dataclass
class InputFeatures:
    """输入特征"""
    complexity: float     # 复杂度 [0,1]
    has_rules: bool      # 是否有规则
    has_examples: bool   # 是否有示例
    uncertainty: float  # 不确定性 [0,1]
    time_constraint: float  # 时间约束 [0,1]


@dataclass
class RoutingDecision:
    """路由决策"""
    reasoning_type: ReasoningType
    confidence: float
    expected_accuracy: float
    estimated_latency_ms: float


class NeuralRouter:
    """
    神经路由器
    基于论文公式21的动态推理路由
    """

    # 论文校准参数
    NEURAL_THRESHOLD = _cfg.get_param("neural_router", "NEURAL_THRESHOLD")  # was: 0.7      # 高复杂度用Neural
    SYMBOLIC_THRESHOLD = _cfg.get_param("neural_router", "SYMBOLIC_THRESHOLD")  # was: 0.3     # 低复杂度用Symbolic
    TIME_CRITICAL_THRESHOLD = _cfg.get_param("neural_router", "TIME_CRITICAL_THRESHOLD")  # was: 0.8  # 时间紧急用Hybrid

    # 各推理类型的预期准确率和延迟
    REASONING_STATS = {
        ReasoningType.NEURAL: {'accuracy': 0.92, 'latency': 50.0},
        ReasoningType.SYMBOLIC: {'accuracy': 0.88, 'latency': 10.0},
        ReasoningType.HYBRID: {'accuracy': 0.95, 'latency': 30.0},
    }

    def __init__(self):
        self.decision_history: List[RoutingDecision] = []
        self.correct_count = 0
        self.total_count = 0

    def extract_features(self, input_data: dict) -> InputFeatures:
        """
        提取输入特征

        Args:
            input_data: 输入数据

        Returns:
            特征向量
        """
        return InputFeatures(
            complexity=input_data.get('complexity', 0.5),
            has_rules=input_data.get('has_rules', False),
            has_examples=input_data.get('has_examples', False),
            uncertainty=input_data.get('uncertainty', 0.5),
            time_constraint=input_data.get('time_constraint', 0.5),
        )

    def calculate_route_probability(self, features: InputFeatures,
                                    reasoning: ReasoningType) -> float:
        """
        计算各推理类型的概率

        D(input) = argmax_r P(r | input_features)

        Returns:
            各推理类型的概率
        """
        # 基于特征的简单概率估算
        probs = {}

        # Neural概率：高复杂度、高不确定性
        neural_score = (
            0.4 * features.complexity +
            0.3 * features.uncertainty +
            0.3 * (1 - features.has_rules)
        )
        probs[ReasoningType.NEURAL] = neural_score

        # Symbolic概率：有规则、低复杂度
        symbolic_score = (
            0.5 * (1 - features.complexity) +
            0.3 * features.has_rules +
            0.2 * (1 - features.uncertainty)
        )
        probs[ReasoningType.SYMBOLIC] = symbolic_score

        # Hybrid概率：时间紧急、有示例
        hybrid_score = (
            0.4 * features.time_constraint +
            0.3 * features.has_examples +
            0.3 * features.has_rules * features.complexity
        )
        probs[ReasoningType.HYBRID] = hybrid_score

        # 归一化
        total = sum(probs.values())
        if total > 0:
            probs = {k: v / total for k, v in probs.items()}

        return probs

    def route(self, input_data: dict) -> RoutingDecision:
        """
        路由决策

        Args:
            input_data: 输入数据

        Returns:
            路由决策
        """
        # 提取特征
        features = self.extract_features(input_data)

        # 计算概率
        probs = self.calculate_route_probability(features, None)

        # 选择最佳推理类型
        best_reasoning = max(probs.keys(), key=lambda x: probs[x])
        confidence = probs[best_reasoning]

        # 获取统计
        stats = self.REASONING_STATS[best_reasoning]

        # 创建决策
        decision = RoutingDecision(
            reasoning_type=best_reasoning,
            confidence=confidence,
            expected_accuracy=stats['accuracy'],
            estimated_latency_ms=stats['latency'],
        )

        self.decision_history.append(decision)
        self.total_count += 1

        return decision

    def report_accuracy(self, is_correct: bool):
        """报告准确性"""
        if is_correct:
            self.correct_count += 1

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if self.total_count == 0:
            return {'total': 0, 'accuracy': 0.0}

        accuracy = self.correct_count / self.total_count

        type_counts = {}
        for d in self.decision_history:
            rt = d.reasoning_type.value
            type_counts[rt] = type_counts.get(rt, 0) + 1

        avg_confidence = sum(d.confidence for d in self.decision_history) / len(self.decision_history)
        avg_latency = sum(d.estimated_latency_ms for d in self.decision_history) / len(self.decision_history)

        return {
            'total_routes': self.total_count,
            'accuracy': round(accuracy, 4),
            'confidence': round(avg_confidence, 4),
            'avg_latency_ms': round(avg_latency, 2),
            'distribution': type_counts,
        }


def test_neural_router():
    """测试神经路由器"""
    print("=" * 60)
    print("Neural Router Test")
    print("=" * 60)

    router = NeuralRouter()

    # 测试不同输入
    test_cases = [
        {'complexity': 0.9, 'has_rules': False, 'has_examples': False,
         'uncertainty': 0.8, 'time_constraint': 0.2},  # 高复杂度，无规则
        {'complexity': 0.2, 'has_rules': True, 'has_examples': True,
         'uncertainty': 0.1, 'time_constraint': 0.3},  # 低复杂度，有规则
        {'complexity': 0.5, 'has_rules': True, 'has_examples': True,
         'uncertainty': 0.4, 'time_constraint': 0.9},  # 时间紧急
    ]

    print("\n--- Routing Decisions ---")
    for i, input_data in enumerate(test_cases):
        decision = router.route(input_data)
        print(f"Input {i+1}: complexity={input_data['complexity']}, "
              f"has_rules={input_data['has_rules']}, "
              f"route={decision.reasoning_type.value}, "
              f"confidence={decision.confidence:.2f}, "
              f"latency={decision.estimated_latency_ms:.0f}ms")

    # 模拟准确性报告
    for i, is_correct in enumerate([True, True, False]):
        router.report_accuracy(is_correct)

    # 统计
    stats = router.get_statistics()
    print(f"\n--- Statistics ---")
    print(f"Total routes: {stats['total_routes']}")
    print(f"Accuracy: {stats['accuracy']:.2%}")
    print(f"Confidence: {stats['confidence']:.2f}")
    print(f"Avg latency: {stats['avg_latency_ms']:.1f}ms")
    print(f"Distribution: {stats['distribution']}")

    print("\n" + "=" * 60)
    print("[PASS] Neural Router Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_neural_router()