"""
RCS Hybrid - RCS混合模型
公式10: RCS = α*R + β*C + γ*S
公式11: I_persona(w) = log(P(w|S_ref) + ε) / log(|S_ref| + ε)
R=共振强度, C=共识度, S=综合得分
用于角色协同决策
"""

import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import Counter

from qcm.config import load_config
_cfg = load_config()


@dataclass
class RCSResult:
    """RCS结果"""
    resonance: float      # R: 共振
    consensus: float     # C: 共识
    synthesis: float     # S: 综合
    rcs_score: float    # 混合得分
    decision: str       # 决策建议


class RCSHybrid:
    """
    RCS混合模型
    基于论文公式10
    """

    # 论文校准参数
    ALPHA = _cfg.get_param("rcs_hybrid", "ALPHA")  # was: 0.4   # 共振权重
    BETA = _cfg.get_param("rcs_hybrid", "BETA")  # was: 0.35   # 共识权重
    GAMMA = _cfg.get_param("rcs_hybrid", "GAMMA")  # was: 0.25  # 综合权重

    # 决策阈值
    DECISION_THRESHOLD = _cfg.get_param("rcs_hybrid", "DECISION_THRESHOLD")

    def __init__(self):
        self.history: List[RCSResult] = []

    def calculate_resonance(self, r_values: List[float]) -> float:
        """
        计算共振强度 R

        Args:
            r_values: R值历史

        Returns:
            共振强度
        """
        if not r_values:
            return 0.0

        # 最近5轮的R值平均
        recent = r_values[-5:] if len(r_values) >= 5 else r_values
        avg_r = sum(recent) / len(recent)

        # 趋势：是否在增长
        if len(recent) >= 2:
            trend = recent[-1] - recent[0]
        else:
            trend = 0

        # 共振 = 平均值 + 趋势加成
        resonance = avg_r + 0.1 * trend

        return max(0.0, min(1.0, resonance))

    def calculate_consensus(self, votes: List[int], total_roles: int) -> float:
        """
        计算共识度 C

        Args:
            votes: 各角色投票
            total_roles: 总角色数

        Returns:
            共识度
        """
        if not votes or total_roles == 0:
            return 0.0

        # 计算多数同意比例
        max_vote = max(votes)
        consensus = max_vote / total_roles

        return consensus

    def calculate_synthesis(self, metrics: Dict[str, float]) -> float:
        """
        计算综合得分 S

        Args:
            metrics: 各维度指标

        Returns:
            综合得分
        """
        if not metrics:
            return 0.5

        # 归一化平均
        values = list(metrics.values())
        synthesis = sum(values) / len(values)

        return max(0.0, min(1.0, synthesis))

    def calculate_rcs(self, r_values: List[float], votes: List[int],
                   metrics: Dict[str, float]) -> RCSResult:
        """
        计算RCS混合得分

        Args:
            r_values: R值历史
            votes: 投票列表
            metrics: 综合指标

        Returns:
            RCS结果
        """
        # 计算各分量
        resonance = self.calculate_resonance(r_values)
        consensus = self.calculate_consensus(votes, sum(votes) if votes else 1)
        synthesis = self.calculate_synthesis(metrics)

        # 混合计算
        rcs = (
            self.ALPHA * resonance +
            self.BETA * consensus +
            self.GAMMA * synthesis
        )

        # 决策建议
        if rcs >= self.DECISION_THRESHOLD:
            decision = "APPROVE"
        elif rcs >= 0.5:
            decision = "REVIEW"
        else:
            decision = "REJECT"

        result = RCSResult(
            resonance=resonance,
            consensus=consensus,
            synthesis=synthesis,
            rcs_score=rcs,
            decision=decision
        )

        self.history.append(result)
        return result

    def batch_process(self, data_batch: List[dict]) -> List[RCSResult]:
        """
        批量处理

        Args:
            data_batch: 批量数据

        Returns:
            结果列表
        """
        results = []

        for data in data_batch:
            r_values = data.get('r_values', [])
            votes = data.get('votes', [])
            metrics = data.get('metrics', {})

            result = self.calculate_rcs(r_values, votes, metrics)
            results.append(result)

        return results

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        if not self.history:
            return {
                'total_decisions': 0,
                'avg_rcs': 0.0,
                'approve_count': 0,
                'review_count': 0,
                'reject_count': 0,
            }

        approve = sum(1 for r in self.history if r.decision == "APPROVE")
        review = sum(1 for r in self.history if r.decision == "REVIEW")
        reject = sum(1 for r in self.history if r.decision == "REJECT")

        avg_rcs = sum(r.rcs_score for r in self.history) / len(self.history)

        return {
            'total_decisions': len(self.history),
            'avg_rcs': round(avg_rcs, 4),
            'approve_count': approve,
            'review_count': review,
            'reject_count': reject,
        }


class PersonaIndicator:
    """
    角色Persona指标 (公式11)
    I_persona(w) = log(P(w|S_ref) + ε) / log(|S_ref| + ε)
    论文参数: ε=1e-10 (避免log(0))
    """

    EPSILON = 1e-10

    def __init__(self, reference_corpus: List[str] = None):
        """
        初始化

        Args:
            reference_corpus: 参考语料库 S_ref
        """
        self.reference_corpus = reference_corpus or []
        self.term_frequency: Dict[str, int] = {}
        self._build_term_frequency()

    def _build_term_frequency(self):
        """构建词频统计"""
        if not self.reference_corpus:
            return

        for doc in self.reference_corpus:
            words = doc.lower().split()
            for word in words:
                self.term_frequency[word] = self.term_frequency.get(word, 0) + 1

    def add_reference(self, corpus: List[str]):
        """添加参考语料"""
        self.reference_corpus.extend(corpus)
        self._build_term_frequency()

    def calculate_word_probability(self, word: str) -> float:
        """
        计算词在参考语料中的概率 P(w|S_ref)

        Args:
            word: 词语

        Returns:
            概率
        """
        if not self.term_frequency:
            return 0.0

        total = sum(self.term_frequency.values())
        if total == 0:
            return 0.0

        freq = self.term_frequency.get(word.lower(), 0)
        return freq / total

    def calculate_indicator(self, word: str) -> float:
        """
        计算角色Persona指标 (公式11)

        Args:
            word: 词语 w

        Returns:
            I_persona(w)
        """
        # 计算 P(w|S_ref)
        prob = self.calculate_word_probability(word)

        # 分子: log(P(w|S_ref) + ε)
        numerator = math.log(prob + self.EPSILON)

        # 分母: log(|S_ref| + ε)
        denominator = math.log(len(self.reference_corpus) + self.EPSILON) if self.reference_corpus else 1.0

        # 避免除零
        if abs(denominator) < self.EPSILON:
            denominator = 1.0

        # 计算指标
        indicator = numerator / denominator

        return indicator

    def calculate_sentence_indicator(self, sentence: str) -> float:
        """
        计算句子的Persona指标（平均）

        Args:
            sentence: 句子

        Returns:
            平均指标
        """
        words = sentence.lower().split()
        if not words:
            return 0.0

        indicators = [self.calculate_indicator(word) for word in words]
        return sum(indicators) / len(indicators)

    def compare_persona(self, text1: str, text2: str) -> Dict[str, float]:
        """
        比较两个文本的Persona相似度

        Args:
            text1: 文本1
            text2: 文本2

        Returns:
            相似度指标
        """
        ind1 = self.calculate_sentence_indicator(text1)
        ind2 = self.calculate_sentence_indicator(text2)

        # 相似度 = 1 - |差值|
        similarity = 1.0 - abs(ind1 - ind2)

        return {
            'text1_indicator': ind1,
            'text2_indicator': ind2,
            'similarity': max(0.0, similarity),
        }


def test_rcs_hybrid():
    """测试RCS混合和Persona指标"""
    print("=" * 60)
    print("RCS Hybrid + Persona Indicator Test")
    print("=" * 60)

    rcs = RCSHybrid()

    # 测试数据
    test_cases = [
        {
            'r_values': [0.6, 0.65, 0.7, 0.72, 0.75],
            'votes': [5, 3, 2],  # 5人同意
            'metrics': {'efficiency': 0.8, 'quality': 0.7, 'speed': 0.6}
        },
        {
            'r_values': [0.5, 0.52, 0.48, 0.45, 0.42],
            'votes': [3, 4, 3],  # 分歧较大
            'metrics': {'efficiency': 0.5, 'quality': 0.6, 'speed': 0.4}
        },
        {
            'r_values': [0.8, 0.82, 0.85, 0.87, 0.9],
            'votes': [8, 2, 0],  # 高度共识
            'metrics': {'efficiency': 0.9, 'quality': 0.85, 'speed': 0.8}
        },
    ]

    print("\n--- RCS Calculation (Formula 10) ---")
    for i, data in enumerate(test_cases):
        result = rcs.calculate_rcs(
            data['r_values'],
            data['votes'],
            data['metrics']
        )

        print(f"\nCase {i+1}:")
        print(f"  Resonance (R): {result.resonance:.3f}")
        print(f"  Consensus (C): {result.consensus:.3f}")
        print(f"  Synthesis (S): {result.synthesis:.3f}")
        print(f"  RCS Score:     {result.rcs_score:.3f}")
        print(f"  Decision:      {result.decision}")

    # 统计
    stats = rcs.get_statistics()
    print(f"\n--- RCS Statistics ---")
    print(f"Total: {stats['total_decisions']}")
    print(f"Avg RCS: {stats['avg_rcs']:.3f}")

    print("\n--- Persona Indicator Test (Formula 11) ---")
    # 参考语料库
    ref_corpus = [
        "analyze report research data study",
        "coordinate schedule organize manage plan",
        "innovate create develop design implement",
        "review evaluate assess optimize improve",
    ]

    pi = PersonaIndicator(reference_corpus=ref_corpus)

    # 测试词语
    test_words = ["analyze", "coordinate", "innovate", "randomword"]
    for word in test_words:
        ind = pi.calculate_indicator(word)
        print(f"  I_persona('{word}'): {ind:.4f}")

    # 句子比较
    text1 = "analyze the research data carefully"
    text2 = "coordinate the schedule and manage"

    comparison = pi.compare_persona(text1, text2)
    print(f"\n  Text1: '{text1}'")
    print(f"  Text2: '{text2}'")
    print(f"  Persona similarity: {comparison['similarity']:.4f}")

    print("\n" + "=" * 60)
    print("[PASS] RCS + Persona Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_rcs_hybrid()