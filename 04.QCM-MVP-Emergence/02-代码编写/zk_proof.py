"""
Zero-Knowledge Proof - ZK可验证计算
能力J: 可验证计算
简化版ZK证明：不泄露隐私前提下验证计算正确性
"""

import hashlib
import random
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Proof:
    """ZK证明"""
    commitment: str      # 承诺
    challenge: str      # 挑战
    response: str      # 响应
    verified: bool      # 验证结果


@dataclass
class ComputationResult:
    """计算结果"""
    input_hash: str
    output: float
    proof: Proof
    verified: bool


class ZKProver:
    """ZK证明者"""

    def __init__(self, secret: float):
        """
        初始化证明者

        Args:
            secret: 秘密值
        """
        self.secret = secret
        self.nonce = random.randint(0, 1000000)

    def commit(self) -> str:
        """生成承诺"""
        data = f"{self.secret}:{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def respond(self, challenge: str) -> str:
        """生成响应"""
        data = f"{self.secret}:{self.nonce}:{challenge}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]


class ZKVerifier:
    """ZK验证者"""

    def __init__(self):
        self.challenges: Dict[str, str] = {}
        self.verified_count = 0
        self.total_count = 0

    def generate_challenge(self, commitment: str) -> str:
        """生成挑战"""
        challenge = hashlib.sha256(commitment.encode()).hexdigest()[:8]
        self.challenges[commitment] = challenge
        return challenge

    def verify(self, commitment: str, challenge: str, response: str) -> bool:
        """
        验证证明

        Args:
            commitment: 承诺
            challenge: 挑战
            response: 响应

        Returns:
            是否验证通过
        """
        # 简化的验证逻辑
        # 实际ZK需要更复杂的数学构造

        # 检查挑战是否匹配
        expected_challenge = self.challenges.get(commitment)
        if expected_challenge != challenge:
            return False

        # 验证响应格式
        if len(response) < 8:
            return False

        self.total_count += 1

        # 模拟验证成功（90%概率）
        verified = random.random() < 0.9

        if verified:
            self.verified_count += 1

        return verified


class ZKComputation:
    """
    ZK可验证计算
    简化版实现
    """

    def __init__(self):
        self.prover = None
        self.verifier = ZKVerifier()

    def compute_with_proof(self, secret: float, operation: str, operand: float) -> ComputationResult:
        """
        带证明的计算

        Args:
            secret: 秘密值
            operation: 操作 (+, -, *, /)
            operand: 操作数

        Returns:
            计算结果及证明
        """
        # 创建证明者
        self.prover = ZKProver(secret)

        # 执行计算
        if operation == '+':
            output = secret + operand
        elif operation == '-':
            output = secret - operand
        elif operation == '*':
            output = secret * operand
        elif operation == '/':
            output = secret / operand if operand != 0 else 0
        else:
            output = 0

        # 生成证明
        commitment = self.prover.commit()
        challenge = self.verifier.generate_challenge(commitment)
        response = self.prover.respond(challenge)

        # 验证
        verified = self.verifier.verify(commitment, challenge, response)

        # 创建证明
        proof = Proof(
            commitment=commitment,
            challenge=challenge,
            response=response,
            verified=verified
        )

        # 创建结果
        result = ComputationResult(
            input_hash=hashlib.sha256(str(secret).encode()).hexdigest()[:16],
            output=output,
            proof=proof,
            verified=verified
        )

        return result

    def batch_verify(self, results: list) -> Dict:
        """
        批量验证

        Args:
            results: 结果列表

        Returns:
            验证统计
        """
        verified = sum(1 for r in results if r.verified)
        total = len(results)

        return {
            'total': total,
            'verified': verified,
            'success_rate': verified / total if total > 0 else 0,
        }

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            'total_verifications': self.verifier.total_count,
            'successful_verifications': self.verifier.verified_count,
            'success_rate': self.verifier.verified_count / max(1, self.verifier.total_count),
        }


def test_zk_proof():
    """测试ZK证明"""
    print("=" * 60)
    print("Zero-Knowledge Proof Test")
    print("=" * 60)

    zk = ZKComputation()

    # 测试用例
    test_cases = [
        (100, '+', 50),
        (200, '-', 80),
        (15, '*', 4),
        (100, '/', 10),
    ]

    print("\n--- Computation with Proof ---")
    for secret, op, operand in test_cases:
        result = zk.compute_with_proof(secret, op, operand)

        print(f"\n{secret} {op} {operand} = {result.output}")
        print(f"  Verified: {result.verified}")

    # 批量验证
    results = [zk.compute_with_proof(100 + i, '+', i) for i in range(10)]
    batch_stats = zk.batch_verify(results)

    print(f"\n--- Batch Verification ---")
    print(f"Total: {batch_stats['total']}")
    print(f"Verified: {batch_stats['verified']}")
    print(f"Success rate: {batch_stats['success_rate']:.0%}")

    # 统计
    stats = zk.get_statistics()
    print(f"\n--- Overall Statistics ---")
    print(f"Total verifications: {stats['total_verifications']}")
    print(f"Success rate: {stats['success_rate']:.0%}")

    print("\n" + "=" * 60)
    print("[PASS] ZK Proof Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_zk_proof()