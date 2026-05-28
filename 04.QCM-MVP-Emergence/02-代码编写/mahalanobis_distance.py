"""
Mahalanobis Distance - 马氏距离
公式8: d_M(x, y) = sqrt((x - y)^T * Σ^(-1) * (x - y))
公式9: L = Σ max(0, d_M(x_i,x_j) - m_pos) + Σ max(0, m_neg - d_M(x_i,x_j))
用于度量角色技能空间中的距离，考虑特征相关性
"""

import math
import random
from typing import List, Dict, Tuple, Optional
import numpy as np

from qcm.config import load_config
_cfg = load_config()


class ContrastiveLoss:
    """
    对比损失函数 (公式9)
    L = Σ_{(x_i,x_j)∈P} max(0, d_M(x_i,x_j) - m_pos) + Σ_{(x_i,x_j)∈N} max(0, m_neg - d_M(x_i,x_j))
    论文参数: m_pos=0.5, m_neg=2.0
    """

    # 论文校准参数
    MARGIN_POS = _cfg.get_param("mahalanobis_distance", "MARGIN_POS")  # was: 0.5   # 正样本距离阈值
    MARGIN_NEG = _cfg.get_param("mahalanobis_distance", "MARGIN_NEG")  # was: 2.0   # 负样本距离阈值

    def __init__(self):
        self.loss_history: List[float] = []

    def calculate(self, positive_distances: List[float], negative_distances: List[float]) -> float:
        """
        计算对比损失

        Args:
            positive_distances: 正样本对距离列表
            negative_distances: 负样本对距离列表

        Returns:
            总损失
        """
        loss = 0.0

        # 正样本损失：距离应该小于m_pos
        for d in positive_distances:
            loss += max(0.0, d - self.MARGIN_POS)

        # 负样本损失：距离应该大于m_neg
        for d in negative_distances:
            loss += max(0.0, self.MARGIN_NEG - d)

        # 平均
        n = len(positive_distances) + len(negative_distances)
        if n > 0:
            loss /= n

        self.loss_history.append(loss)
        return loss

    def calculate_batch(self, distances: List[Tuple[float, bool]]) -> float:
        """
        批量计算对比损失

        Args:
            distances: [(distance, is_positive), ...]

        Returns:
            总损失
        """
        pos_dists = [d for d, is_pos in distances if is_pos]
        neg_dists = [d for d, is_pos in distances if not is_pos]

        return self.calculate(pos_dists, neg_dists)

    def get_accuracy(self, distances: List[Tuple[float, bool]]) -> Dict[str, float]:
        """
        计算准确率
        正样本对距离 < m_pos 视为正确
        负样本对距离 > m_neg 视为正确
        """
        if not distances:
            return {'accuracy': 0.0, 'positive_accuracy': 0.0, 'negative_accuracy': 0.0}

        pos_correct = 0
        pos_total = 0
        neg_correct = 0
        neg_total = 0

        for d, is_pos in distances:
            if is_pos:
                pos_total += 1
                if d < self.MARGIN_POS:
                    pos_correct += 1
            else:
                neg_total += 1
                if d > self.MARGIN_NEG:
                    neg_correct += 1

        pos_acc = pos_correct / max(1, pos_total)
        neg_acc = neg_correct / max(1, neg_total)
        total_correct = pos_correct + neg_correct
        total = len(distances)

        return {
            'accuracy': total_correct / max(1, total),
            'positive_accuracy': pos_acc,
            'negative_accuracy': neg_acc,
        }


class MahalanobisDistance:
    """
    马氏距离计算器
    基于论文公式8
    """

    def __init__(self, dimension: int = 4):
        """
        初始化

        Args:
            dimension: 特征维度
        """
        self.dimension = dimension
        self.covariance_matrix = np.eye(dimension)
        self.inv_covariance = np.eye(dimension)

    def fit(self, data: List[List[float]]):
        """
        从数据学习协方差矩阵

        Args:
            data: 训练数据
        """
        if len(data) < 2:
            return

        # 转换为numpy数组
        X = np.array(data)

        # 计算协方差矩阵
        self.covariance_matrix = np.cov(X, rowvar=False)

        # 计算逆矩阵
        try:
            self.inv_covariance = np.linalg.inv(self.covariance_matrix)
        except np.linalg.LinAlgError:
            # 如果奇异，使用伪逆
            self.inv_covariance = np.linalg.pinv(self.covariance_matrix)

    def calculate(self, x: List[float], y: List[float]) -> float:
        """
        计算马氏距离

        Args:
            x: 向量1
            y: 向量2

        Returns:
            马氏距离
        """
        if len(x) != len(y):
            return 0.0

        # 转换为numpy数组
        x = np.array(x)
        y = np.array(y)

        # 计算差值
        diff = x - y

        # 计算马氏距离: sqrt(diff^T * Σ^(-1) * diff)
        try:
            md = math.sqrt(np.dot(np.dot(diff, self.inv_covariance), diff))
        except:
            md = math.sqrt(sum((x - y) ** 2))

        return float(md)

    def calculate_euclidean(self, x: List[float], y: List[float]) -> float:
        """计算欧氏距离（对比）"""
        if len(x) != len(y):
            return 0.0
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))

    def calculate_manhattan(self, x: List[float], y: List[float]) -> float:
        """计算曼哈顿距离（对比）"""
        if len(x) != len(y):
            return 0.0
        return sum(abs(a - b) for a, b in zip(x, y))

    def get_covariance_matrix(self) -> np.ndarray:
        """获取协方差矩阵"""
        return self.covariance_matrix


def test_mahalanobis():
    """测试马氏距离和对比损失"""
    print("=" * 60)
    print("Mahalanobis Distance + Contrastive Loss Test")
    print("=" * 60)

    md = MahalanobisDistance(dimension=4)
    cl = ContrastiveLoss()

    # 训练数据（模拟技能分布）
    training_data = [
        [0.9, 0.1, 0.2, 0.3],
        [0.8, 0.2, 0.3, 0.2],
        [0.7, 0.3, 0.2, 0.4],
        [0.6, 0.4, 0.3, 0.3],
        [0.5, 0.5, 0.4, 0.2],
    ]
    md.fit(training_data)

    print("\n--- Distance Comparison ---")

    # 测试向量
    test_pairs = [
        ([0.9, 0.1, 0.2, 0.3], [0.8, 0.2, 0.3, 0.2]),
        ([0.9, 0.1, 0.2, 0.3], [0.5, 0.5, 0.4, 0.2]),
        ([0.7, 0.3, 0.2, 0.4], [0.6, 0.4, 0.3, 0.3]),
    ]

    distances = []
    for i, (x, y) in enumerate(test_pairs):
        m_dist = md.calculate(x, y)
        e_dist = md.calculate_euclidean(x, y)
        is_positive = i < 2  # 前两对是正样本
        distances.append((m_dist, is_positive))

        print(f"Pair {i+1}:")
        print(f"  Mahalanobis: {m_dist:.4f}")
        print(f"  Euclidean:   {e_dist:.4f}")

    print("\n--- Contrastive Loss (Formula 9) ---")
    loss = cl.calculate_batch(distances)
    print(f"  Loss: {loss:.4f}")

    acc = cl.get_accuracy(distances)
    print(f"  Accuracy: {acc['accuracy']:.2%}")
    print(f"  Positive accuracy: {acc['positive_accuracy']:.2%}")
    print(f"  Negative accuracy: {acc['negative_accuracy']:.2%}")

    print("\n" + "=" * 60)
    print("[PASS] Mahalanobis + Contrastive Loss Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_mahalanobis()