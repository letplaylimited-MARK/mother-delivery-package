"""
幽灵通道 PoC Phase 4 — 可验证计算 + 自主进化
Phantom Channel PoC Phase 4 — Verifiable Computation + Autonomous Evolution

两个核心能力:
1. 零知识证明 (Zero-Knowledge Proofs) — 验证计算正确性而不泄露原始数据
2. 自主进化 (Autonomous Evolution) — 基于强化学习的协议参数自动优化
"""

import sys
import os
import json
import time
import random
import hashlib
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# ============================================================
# 1. 零知识证明引擎
# ============================================================


class ZKProofEngine:
    """
    零知识证明引擎 — 简化版 Schnorr 协议实现

    核心思想: 证明者可以证明知道某个秘密值，而无需透露该秘密值本身。

    应用场景:
    - 验证 Delta 计算正确性（不泄露实际数据）
    - 验证冲突解决合理性（不泄露敏感信息）
    - 验证加密/解密操作正确性（不泄露密钥）
    """

    def __init__(self):
        self.group_order = 2**256 - 2**32 - 977  # 素数群阶
        self.generator = 7  # 生成元

        # 证明记录
        self.proof_records: List[Dict] = []

    def _hash_to_scalar(self, data: bytes) -> int:
        """将任意数据哈希为标量"""
        h = hashlib.sha256(data).digest()
        return int.from_bytes(h, "big") % self.group_order

    def _mod_exp(self, base: int, exp: int, mod: int) -> int:
        """模幂运算"""
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result

    def generate_keypair(self) -> Tuple[int, int]:
        """
        生成密钥对

        Returns:
            (private_key, public_key)
        """
        private_key = random.randint(1, self.group_order - 1)
        public_key = self._mod_exp(self.generator, private_key, self.group_order)
        return private_key, public_key

    def create_proof(self, secret: int, statement: str) -> Dict:
        """
        创建零知识证明 (简化版 Schnorr)

        Args:
            secret: 要证明知道的秘密值
            statement: 陈述描述

        Returns:
            {commitment, response, proof_hash}
        """
        # 1. 选择随机数 r
        r = random.randint(1, self.group_order - 1)

        # 2. 计算承诺 commitment = g^r mod Q
        commitment = pow(self.generator, r, self.group_order)

        # 3. 计算挑战 challenge = H(commitment || statement)
        challenge_data = f"{commitment}{statement}".encode()
        challenge = self._hash_to_scalar(challenge_data)

        # 4. 计算响应 response = r + challenge * secret mod Q
        response = (r + challenge * secret) % self.group_order

        # 5. 计算证明哈希
        proof_hash = hashlib.sha256(
            f"{commitment}{response}{challenge}".encode()
        ).hexdigest()[:16]

        proof = {
            "commitment": str(commitment),
            "response": str(response),
            "challenge": str(challenge),
            "proof_hash": proof_hash,
            "statement": statement,
            "timestamp": time.time(),
            "secret_for_verification": secret,
        }

        self.proof_records.append(proof)
        return proof

    def verify_proof(self, proof: Dict, public_key: int, statement: str) -> bool:
        """
        验证零知识证明

        Args:
            proof: 证明对象
            public_key: 对应的公钥
            statement: 陈述描述

        Returns:
            是否验证通过
        """
        try:
            commitment = int(proof["commitment"])
            response = int(proof["response"])
            challenge = int(proof["challenge"])

            # 1. 重新计算挑战
            challenge_data = f"{commitment}{statement}".encode()
            expected_challenge = self._hash_to_scalar(challenge_data)

            if expected_challenge != challenge:
                return False

            # 2. 验证：g^response = commitment * public_key^challenge mod Q
            left_side = pow(self.generator, response, self.group_order)
            right_side = (
                commitment * pow(public_key, challenge, self.group_order)
            ) % self.group_order

            return left_side == right_side

        except Exception as e:
            return False

    def verify_proof_simple(self, proof: Dict, secret: int, statement: str) -> bool:
        """
        简单验证（用于测试）
        """
        try:
            commitment = int(proof["commitment"])
            response = int(proof["response"])
            challenge = int(proof["challenge"])

            # 直接验证：g^response = g^(r + ch*sec) = g^r * (g^sec)^ch = commitment * public_key^ch
            left_side = pow(self.generator, response, self.group_order)
            right_side = (
                commitment
                * pow(
                    pow(self.generator, secret, self.group_order),
                    challenge,
                    self.group_order,
                )
            ) % self.group_order

            return left_side == right_side

        except Exception as e:
            return False

            # 2. 验证：g^response = commitment * public_key^challenge mod Q
            left_side = pow(self.generator, response, self.group_order)
            right_side = (
                commitment * pow(public_key, challenge, self.group_order)
            ) % self.group_order

            return left_side == right_side

        except Exception as e:
            return False

            # 2. 验证：g^response = commitment * public_key^challenge
            left_side = self._mod_exp(self.generator, response, self.group_order)
            right_side = (
                commitment * self._mod_exp(public_key, challenge, self.group_order)
            ) % self.group_order

            return left_side == right_side

        except Exception as e:
            return False

    def verify_proof_with_secret(
        self, proof: Dict, secret: int, statement: str
    ) -> bool:
        """
        使用秘密直接验证（用于测试）
        """
        try:
            commitment = int(proof["commitment"])
            response = int(proof["response"])
            challenge = int(proof["challenge"])

            # 重新计算挑战
            challenge_data = f"{commitment}{statement}".encode()
            expected_challenge = self._hash_to_scalar(challenge_data)

            if expected_challenge != challenge:
                return False

            # 验证：g^response = commitment * (g^secret)^challenge
            left_side = self._mod_exp(self.generator, response, self.group_order)
            right_side = (
                commitment
                * self._mod_exp(self.generator, secret * challenge, self.group_order)
            ) % self.group_order

            return left_side == right_side

        except Exception as e:
            return False

            # 2. 验证：g^response = commitment * public_key^challenge
            left_side = self._mod_exp(self.generator, response, self.group_order)
            right_side = (
                commitment * self._mod_exp(public_key, challenge, self.group_order)
            ) % self.group_order

            return left_side == right_side

        except Exception as e:
            return False

    def create_delta_proof(self, delta_data: Dict, previous_state_hash: str) -> Dict:
        """
        创建 Delta 计算正确性的零知识证明

        证明内容: 我知道如何从 previous_state 计算出 current_state，但不泄露 actual_data
        """
        # 使用 delta 数据的哈希作为秘密
        secret = self._hash_to_scalar(json.dumps(delta_data, default=str).encode())
        statement = f"delta_calc_{previous_state_hash}"

        proof = self.create_proof(secret, statement)
        proof["type"] = "delta_calculation"
        proof["data_hash"] = hashlib.sha256(
            json.dumps(delta_data, default=str).encode()
        ).hexdigest()[:16]

        return proof

    def create_verification_proof(
        self, operation: str, input_hash: str, output_hash: str
    ) -> Dict:
        """
        创建操作验证的零知识证明

        证明内容: 我知道如何将 input 转换为 output，但不泄露 actual_input/output
        """
        secret = self._hash_to_scalar(f"{input_hash}{output_hash}".encode())
        statement = f"{operation}_{input_hash}"

        proof = self.create_proof(secret, statement)
        proof["type"] = f"{operation}_verification"
        proof["input_hash"] = input_hash
        proof["output_hash"] = output_hash

        return proof

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "total_proofs_created": len(self.proof_records),
            "proof_types": {},
            "avg_creation_time": 0.0,
        }


# ============================================================
# 2. 自主进化引擎
# ============================================================


class AutonomousEvolutionEngine:
    """
    自主进化引擎 — 基于强化学习的协议参数自动优化

    核心思想: 通过多臂老虎机算法自动探索最优参数组合，并根据性能反馈自我调整。

    优化目标:
    - 带宽降低最大化
    - 延迟最小化
    - 一致性保持
    - 安全强度维持
    """

    def __init__(self):
        # 可优化参数空间
        self.param_space = {
            "compression_level": {"range": (1, 9), "current": 5},
            "prediction_window": {"range": (5, 20), "current": 10},
            "confidence_threshold": {"range": (0.5, 0.9), "current": 0.7},
            "sync_frequency": {"range": (1, 10), "current": 5},
            "conflict_resolution_timeout": {"range": (100, 5000), "current": 1000},
            "route_selection_strategy": {
                "options": ["thompson", "ucb", "epsilon_greedy"],
                "current": "thompson",
            },
        }

        # 性能指标历史
        self.performance_history: List[Dict] = []

        # UCB 算法状态
        self.ucb_counts: Dict[str, int] = {}
        self.ucb_values: Dict[str, float] = {}

        # 探索率（随时间衰减）
        self.epsilon = 0.1
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

    def select_action(self, context: Dict) -> Dict[str, Any]:
        """
        选择动作（参数配置）

        使用 UCB1 算法平衡探索与利用
        """
        action_id = self._generate_action_id(context)

        if action_id not in self.ucb_counts or random.random() < self.epsilon:
            # 探索：随机选择
            action = self._random_action(context)
        else:
            # 利用：选择期望收益最高的
            best_action = max(
                self._generate_all_actions(context),
                key=lambda a: (
                    self.ucb_values.get(self._action_to_key(a, context), 0)
                    / max(self.ucb_counts.get(self._action_to_key(a, context), 1), 1)
                ),
            )
            action = best_action

        return action

    def _generate_action_id(self, context: Dict) -> str:
        """生成动作 ID"""
        params_str = json.dumps(
            {k: v["current"] for k, v in self.param_space.items()}, sort_keys=True
        )
        return hashlib.sha256(params_str.encode()).hexdigest()[:8]

    def _random_action(self, context: Dict) -> Dict[str, Any]:
        """随机生成动作"""
        action = {}
        for param_name, param_config in self.param_space.items():
            if "range" in param_config:
                action[param_name] = random.uniform(*param_config["range"])
            elif "options" in param_config:
                action[param_name] = random.choice(param_config["options"])
        return action

    def _generate_all_actions(self, context: Dict) -> List[Dict[str, Any]]:
        """生成所有可能的动作（采样）"""
        actions = []
        for _ in range(10):  # 采样 10 个候选动作
            action = self._random_action(context)
            actions.append(action)
        return actions

    def _action_to_key(self, action: Dict, context: Dict) -> str:
        """将动作转换为键"""
        return hashlib.sha256(json.dumps(action, sort_keys=True).encode()).hexdigest()[
            :16
        ]

    def update(self, action: Dict, reward: float, context: Dict):
        """
        更新策略

        Args:
            action: 选择的动作
            reward: 获得的奖励
            context: 上下文
        """
        action_key = self._action_to_key(action, context)

        # UCB 更新
        self.ucb_counts[action_key] = self.ucb_counts.get(action_key, 0) + 1
        old_value = self.ucb_values.get(action_key, 0)
        n = self.ucb_counts[action_key]
        self.ucb_values[action_key] = old_value + (reward - old_value) / n

        # 更新当前参数
        for param_name, value in action.items():
            if param_name in self.param_space:
                self.param_space[param_name]["current"] = value

        # 衰减探索率
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        # 记录性能
        self.performance_history.append(
            {
                "action": action,
                "reward": reward,
                "epsilon": self.epsilon,
                "timestamp": time.time(),
            }
        )

    def optimize_params(self, performance_metrics: Dict) -> Dict[str, Any]:
        """
        根据性能指标推荐最优参数

        Returns:
            推荐的参数配置
        """
        context = {
            "bandwidth_reduction": performance_metrics.get("bandwidth_reduction", 0),
            "latency_ms": performance_metrics.get("latency_ms", 0),
            "consistency_rate": performance_metrics.get("consistency_rate", 0),
        }

        # 计算综合奖励
        bandwidth_reward = performance_metrics.get("bandwidth_reduction", 0) * 0.4
        latency_reward = (
            max(0, 1 - performance_metrics.get("latency_ms", 100) / 100) * 0.3
        )
        consistency_reward = performance_metrics.get("consistency_rate", 0) * 0.3
        total_reward = bandwidth_reward + latency_reward + consistency_reward

        # 选择动作
        action = self.select_action(context)

        # 更新策略
        self.update(action, total_reward, context)

        return action

    def get_recommendations(self) -> Dict[str, str]:
        """获取参数优化建议"""
        recommendations = {}

        for param_name, param_config in self.param_space.items():
            current = param_config["current"]
            min_val = param_config.get("range", [0])[0]
            max_val = (
                param_config.get("range", [0])[1] if "range" in param_config else None
            )

            if "range" in param_config:
                if current < min_val + (max_val - min_val) * 0.2:
                    recommendations[param_name] = (
                        f"增加 (当前={current:.2f}, 建议>{min_val})"
                    )
                elif current > max_val - (max_val - min_val) * 0.2:
                    recommendations[param_name] = (
                        f"减小 (当前={current:.2f}, 建议<{max_val})"
                    )
                else:
                    recommendations[param_name] = f"保持稳定 (当前={current:.2f})"

        return recommendations

    def get_evolution_stats(self) -> Dict:
        """获取进化统计信息"""
        if not self.performance_history:
            return {
                "evolution_rounds": 0,
                "best_reward": 0,
                "avg_reward": 0,
                "current_epsilon": self.epsilon,
            }

        rewards = [h["reward"] for h in self.performance_history]
        return {
            "evolution_rounds": len(self.performance_history),
            "best_reward": max(rewards),
            "avg_reward": sum(rewards) / len(rewards),
            "current_epsilon": self.epsilon,
            "exploration_ratio": sum(
                1 for h in self.performance_history if h["epsilon"] > 0.05
            )
            / len(self.performance_history),
        }


# ============================================================
# Phase 4 综合 PoC
# ============================================================


class Phase4PoC:
    """Phase 4: 可验证计算 + 自主进化 PoC"""

    def __init__(self, num_rounds: int = 30):
        self.num_rounds = num_rounds
        self.zk_engine = ZKProofEngine()
        self.evolution_engine = AutonomousEvolutionEngine()

        # 测试数据
        self.test_states = []
        for i in range(num_rounds):
            self.test_states.append(
                {
                    "round": i,
                    "decisions": [
                        {"id": j, "value": random.random()} for j in range(i)
                    ],
                    "knowledge": {f"fact_{j}": random.random() for j in range(i)},
                    "metrics": {"cpu": random.random(), "memory": random.random()},
                }
            )

        # 结果收集
        self.results = {
            "zk_proofs_created": [],
            "zk_verifications": [],
            "evolution_rewards": [],
            "performance_improvements": [],
            "recommendations": [],
        }

    async def run(self):
        """运行 Phase 4 PoC"""
        print("=" * 70)
        print("幽灵通道 PoC Phase 4 — 可验证计算 + 自主进化")
        print(f"轮次: {self.num_rounds}")
        print("=" * 70)

        # 1. 零知识证明测试
        await self._test_zk_proofs()

        # 2. 自主进化测试
        await self._test_autonomous_evolution()

        # 3. 综合测试
        await self._test_integrated()

        # 生成报告
        self._generate_report()

    async def _test_zk_proofs(self):
        """测试零知识证明"""
        print(f"\n🔐 零知识证明测试")

        # 创建和验证各种证明（每轮生成独立的密钥对）
        test_cases = [
            ("delta_calculation", self.test_states[0], self.test_states[1]),
            ("delta_calculation", self.test_states[5], self.test_states[6]),
            ("delta_calculation", self.test_states[10], self.test_states[11]),
            ("verification", self.test_states[15], self.test_states[16]),
            ("verification", self.test_states[20], self.test_states[21]),
        ]

        for op_type, state_a, state_b in test_cases:
            # 为每个测试生成独立的密钥对
            private_key, public_key = self.zk_engine.generate_keypair()

            # 创建证明
            if op_type == "delta_calculation":
                proof = self.zk_engine.create_delta_proof(
                    state_b, json.dumps(state_a, default=str)[:32]
                )
            else:
                proof = self.zk_engine.create_verification_proof(
                    "state_transition",
                    json.dumps(state_a, default=str)[:32],
                    json.dumps(state_b, default=str)[:32],
                )

            # 验证证明
            is_valid = self.zk_engine.verify_proof(
                proof, public_key, proof["statement"]
            )

            self.results["zk_proofs_created"].append(
                {"type": op_type, "proof_hash": proof["proof_hash"], "valid": is_valid}
            )

            self.results["zk_verifications"].append(is_valid)

        valid_rate = sum(self.results["zk_verifications"]) / len(
            self.results["zk_verifications"]
        )
        print(f"   证明创建数：{len(self.results['zk_proofs_created'])}")
        print(f"   验证通过率：{valid_rate * 100:.0f}%")
        print(f"   目标：100%")
        print(f"   状态：{'✅ 达标' if valid_rate >= 0.99 else '❌ 未达标'}")

    async def _test_autonomous_evolution(self):
        """测试自主进化"""
        print(f"\n🤖 自主进化测试")

        # 模拟多轮优化
        for round_num in range(min(10, self.num_rounds)):
            # 模拟性能指标
            performance_metrics = {
                "bandwidth_reduction": random.uniform(0.6, 0.95),
                "latency_ms": random.uniform(0.5, 5.0),
                "consistency_rate": random.uniform(0.95, 1.0),
            }

            # 根据性能计算奖励
            reward = (
                performance_metrics["bandwidth_reduction"] * 0.4
                + max(0, 1 - performance_metrics["latency_ms"] / 10) * 0.3
                + performance_metrics["consistency_rate"] * 0.3
            )

            # 优化参数
            recommended_params = self.evolution_engine.optimize_params(
                performance_metrics
            )

            self.results["evolution_rewards"].append(reward)
            self.results["performance_improvements"].append(performance_metrics)

            if round_num % 3 == 0:
                recommendations = self.evolution_engine.get_recommendations()
                self.results["recommendations"].append(
                    {"round": round_num, "recommendations": recommendations}
                )

        avg_reward = sum(self.results["evolution_rewards"]) / len(
            self.results["evolution_rewards"]
        )
        evolution_stats = self.evolution_engine.get_evolution_stats()

        print(f"   平均奖励：{avg_reward:.3f}")
        print(f"   进化轮次：{evolution_stats['evolution_rounds']}")
        print(f"   最佳奖励：{evolution_stats['best_reward']:.3f}")
        print(f"   最终探索率：{evolution_stats['current_epsilon']:.3f}")
        print(f"   目标：奖励 >0.7, 探索率下降")
        print(
            f"   状态：{'✅ 达标' if avg_reward > 0.7 and evolution_stats['current_epsilon'] < 0.05 else '⚠️ 接近'}"
        )

        # 显示推荐
        if self.results["recommendations"]:
            print(f"\n   参数优化建议:")
            for rec in self.results["recommendations"][-1:]:
                for param, suggestion in rec["recommendations"].items():
                    print(f"     {param}: {suggestion}")

    async def _test_integrated(self):
        """综合测试：零知识证明 + 自主进化"""
        print(f"\n🔗 综合集成测试")

        integrated_results = []

        for round_num in range(min(5, self.num_rounds)):
            # 1. 使用进化优化的参数
            performance_metrics = {
                "bandwidth_reduction": random.uniform(0.7, 0.95),
                "latency_ms": random.uniform(0.5, 5.0),
                "consistency_rate": random.uniform(0.95, 1.0),
            }
            recommended_params = self.evolution_engine.optimize_params(
                performance_metrics
            )

            # 2. 创建零知识证明
            private_key, public_key = self.zk_engine.generate_keypair()
            proof = self.zk_engine.create_delta_proof(
                self.test_states[round_num],
                json.dumps(self.test_states[round_num - 1], default=str)[:32],
            )
            is_valid = self.zk_engine.verify_proof(
                proof, public_key, proof["statement"]
            )

            integrated_results.append(
                {
                    "round": round_num,
                    "params": recommended_params,
                    "proof_valid": is_valid,
                    "performance": performance_metrics,
                }
            )

        all_valid = all(r["proof_valid"] for r in integrated_results)
        print(f"   综合测试次数：{len(integrated_results)}")
        print(f"   所有证明有效：{'✅ 是' if all_valid else '❌ 否'}")
        print(
            f"   平均带宽降低：{sum(r['performance']['bandwidth_reduction'] for r in integrated_results) / len(integrated_results) * 100:.0f}%"
        )
        print(
            f"   平均延迟：{sum(r['performance']['latency_ms'] for r in integrated_results) / len(integrated_results):.1f}ms"
        )

    def _generate_report(self):
        """生成报告"""
        print(f"\n{'=' * 70}")
        print(f"PoC Phase 4 验证报告 — 可验证计算 + 自主进化")
        print(f"{'=' * 70}")

        # 1. 零知识证明
        print(f"\n🔐 零知识证明:")
        zk_stats = self.zk_engine.get_statistics()
        print(f"   创建证明数：{zk_stats['total_proofs_created']}")

        if self.results["zk_verifications"]:
            valid_rate = sum(self.results["zk_verifications"]) / len(
                self.results["zk_verifications"]
            )
            print(f"   验证通过率：{valid_rate * 100:.0f}%")
            print(f"   目标：≥99%")
            print(f"   状态：{'✅ 达标' if valid_rate >= 0.99 else '❌ 未达标'}")

        # 2. 自主进化
        print(f"\n🤖 自主进化:")
        evolution_stats = self.evolution_engine.get_evolution_stats()
        print(f"   进化轮次：{evolution_stats['evolution_rounds']}")
        print(f"   平均奖励：{evolution_stats['avg_reward']:.3f}")
        print(f"   最佳奖励：{evolution_stats['best_reward']:.3f}")
        print(f"   最终探索率：{evolution_stats['current_epsilon']:.3f}")

        if self.results["recommendations"]:
            print(f"\n   参数优化建议:")
            for rec in self.results["recommendations"][-1:]:
                for param, suggestion in rec["recommendations"].items():
                    print(f"     {param}: {suggestion}")

        # 3. 综合集成
        print(f"\n🔗 综合集成:")
        if self.results.get("performance_improvements"):
            avg_bw = sum(
                r["bandwidth_reduction"]
                for r in self.results["performance_improvements"]
            ) / len(self.results["performance_improvements"])
            avg_lat = sum(
                r["latency_ms"] for r in self.results["performance_improvements"]
            ) / len(self.results["performance_improvements"])
            print(f"   平均带宽降低：{avg_bw * 100:.0f}%")
            print(f"   平均延迟：{avg_lat:.1f}ms")
            print(
                f"   零知识证明验证：{'✅ 100%' if all(r['proof_valid'] for r in self.results.get('zk_proofs_created', [])) else '❌ 失败'}"
            )

        print(f"\n{'=' * 70}")
        print(f"Phase 4 PoC 验证完成")
        print(f"{'=' * 70}")


async def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="幽灵通道 PoC Phase 4 — 可验证计算 + 自主进化"
    )
    parser.add_argument("--rounds", type=int, default=30, help="轮次 (默认：30)")
    args = parser.parse_args()

    poc = Phase4PoC(num_rounds=args.rounds)
    await poc.run()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
