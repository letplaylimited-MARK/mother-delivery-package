"""
幽灵通道 PoC — 场景一：多智能体记忆同步
Phantom Channel PoC — Scenario 1: Multi-Agent Memory Sync
"""

import sys
import os
import asyncio
import json
import time
import random
import copy

# 添加核心模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.protocol import PhantomChannel, VectorClock, DeltaCalculator, MerkleVerifier


class MemorySyncPoC:
    """多智能体记忆同步 PoC"""

    def __init__(self, num_roles: int = 3, num_rounds: int = 50):
        self.num_roles = num_roles
        self.num_rounds = num_rounds
        self.role_ids = [f"role_{i}" for i in range(num_roles)]

        # 初始化幽灵通道
        self.channel = PhantomChannel(self.role_ids)

        # 模拟记忆数据
        self.memories = {
            rid: {
                "__version__": f"v0",
                "context": f"Initial context for {rid}",
                "decisions": [],
                "knowledge": {},
                "interactions": [],
            }
            for rid in self.role_ids
        }

        # 结果收集
        self.results = {
            "sync_results": [],
            "bandwidth_reductions": [],
            "latencies": [],
            "consistency_checks": [],
            "conflicts": [],
        }

    async def run(self):
        """运行 PoC 验证"""
        print(f"=" * 70)
        print(f"幽灵通道 PoC — 场景一：多智能体记忆同步")
        print(f"角色数: {self.num_roles} | 轮次: {self.num_rounds}")
        print(f"=" * 70)

        for round_num in range(1, self.num_rounds + 1):
            await self._execute_round(round_num)

            if round_num % 10 == 0:
                self._print_progress(round_num)

        # 最终一致性验证
        await self._verify_consistency()

        # 生成报告
        self._generate_report()

    async def _execute_round(self, round_num: int):
        """执行单轮同步"""
        # 随机选择一个角色更新记忆
        source_role = random.choice(self.role_ids)
        target_role = random.choice([r for r in self.role_ids if r != source_role])

        # 模拟记忆变更（小变更为主）
        self._simulate_memory_change(source_role, round_num)

        # 执行同步 — 目标是让 target 追上 source 的状态
        memory_snapshot = self.memories[source_role]
        semantic_filter = None

        # 每 5 轮使用语义过滤
        if round_num % 5 == 0:
            semantic_filter = "decision knowledge"

        result = await self.channel.sync_memory_delta(
            source_role=source_role,
            target_role=target_role,
            memory_snapshot=memory_snapshot,
            semantic_filter=semantic_filter,
        )

        # 同步成功后，更新本地记忆副本（模拟传播）
        if result.success:
            self.memories[target_role] = copy.deepcopy(memory_snapshot)

        # 记录结果
        self.results["sync_results"].append(result)
        self.results["bandwidth_reductions"].append(result.bandwidth_reduction)
        self.results["latencies"].append(result.latency_ms)
        self.results["consistency_checks"].append(result.consistency_verified)

    def _simulate_memory_change(self, role_id: str, round_num: int):
        """模拟记忆变更 — 大多数轮次仅修改少量现有数据"""
        memory = self.memories[role_id]
        memory["__version__"] = f"v{round_num}"

        # 80% 的轮次仅修改现有数据（模拟真实场景：大部分数据不变）
        if round_num > 5 and random.random() < 0.8:
            # 修改现有知识条目的置信度
            if memory["knowledge"]:
                key = random.choice(list(memory["knowledge"].keys()))
                memory["knowledge"][key]["confidence"] = min(
                    1.0,
                    memory["knowledge"][key]["confidence"] + random.uniform(-0.05, 0.1),
                )
                memory["knowledge"][key]["last_updated"] = round_num
        else:
            # 20% 的轮次添加新数据
            memory["decisions"].append(
                {
                    "round": round_num,
                    "decision": f"Decision at round {round_num}",
                    "rationale": f"Based on context at round {round_num}",
                }
            )
            memory["knowledge"][f"fact_{round_num}"] = {
                "content": f"Knowledge acquired at round {round_num}",
                "confidence": random.uniform(0.7, 1.0),
                "source": role_id,
            }

        # 每轮仅添加 1 条交互记录（小变更）
        memory["interactions"].append(
            {
                "round": round_num,
                "type": random.choice(["query", "response", "decision"]),
                "content": f"Interaction at round {round_num}",
            }
        )

    async def _verify_consistency(self):
        """最终一致性验证"""
        print(f"\n{'=' * 70}")
        print(f"最终一致性验证")
        print(f"{'=' * 70}")

        consistent_pairs = 0
        total_pairs = 0

        for i, role_a in enumerate(self.role_ids):
            for role_b in self.role_ids[i + 1 :]:
                total_pairs += 1

                # 比较关键状态
                state_a = self.channel.states.get(role_a, {})
                state_b = self.channel.states.get(role_b, {})

                # 检查版本
                version_a = state_a.get("__version__", "")
                version_b = state_b.get("__version__", "")

                # 检查 Merkle Root
                merkle_a = self.channel.merkle_roots.get(role_a, "")
                merkle_b = self.channel.merkle_roots.get(role_b, "")

                # 如果版本相同，Merkle Root 应该相同
                if version_a == version_b:
                    if merkle_a == merkle_b:
                        consistent_pairs += 1
                    else:
                        print(
                            f"  ⚠️ 不一致: {role_a} vs {role_b} (版本相同但 Merkle 不同)"
                        )

        consistency_rate = consistent_pairs / max(total_pairs, 1)
        print(f"  一致对: {consistent_pairs}/{total_pairs}")
        print(f"  一致性率: {consistency_rate * 100:.1f}%")

        self.results["final_consistency_rate"] = consistency_rate

    def _print_progress(self, round_num: int):
        """打印进度"""
        stats = self.channel.get_stats()
        print(
            f"  Round {round_num:3d}/{self.num_rounds} | "
            f"同步: {stats['total_syncs']} | "
            f"带宽: {stats['avg_bandwidth_reduction']} | "
            f"延迟: {stats['avg_latency_ms']} | "
            f"冲突: {stats['conflict_rate']}"
        )

    def _generate_report(self):
        """生成 PoC 报告"""
        print(f"\n{'=' * 70}")
        print(f"PoC 验证报告 — 多智能体记忆同步")
        print(f"{'=' * 70}")

        # 带宽降低
        avg_bw = sum(self.results["bandwidth_reductions"]) / len(
            self.results["bandwidth_reductions"]
        )
        print(f"\n📊 带宽降低:")
        print(f"   平均: {avg_bw * 100:.1f}%")
        print(f"   目标: ≥80%")
        print(f"   状态: {'✅ 达标' if avg_bw >= 0.80 else '❌ 未达标'}")

        # 延迟
        avg_latency = sum(self.results["latencies"]) / len(self.results["latencies"])
        p99_latency = sorted(self.results["latencies"])[
            int(len(self.results["latencies"]) * 0.99)
        ]
        print(f"\n⏱️ 同步延迟:")
        print(f"   平均: {avg_latency:.1f}ms")
        print(f"   P99:  {p99_latency:.1f}ms")
        print(f"   目标: ≤50ms (P99)")
        print(
            f"   状态: {'✅ 达标' if p99_latency <= 50 else '⚠️ 接近' if p99_latency <= 100 else '❌ 未达标'}"
        )

        # 一致性
        consistency = sum(self.results["consistency_checks"]) / len(
            self.results["consistency_checks"]
        )
        print(f"\n🔒 一致性验证:")
        print(f"   通过率: {consistency * 100:.1f}%")
        print(f"   目标: ≥99%")
        print(f"   状态: {'✅ 达标' if consistency >= 0.99 else '❌ 未达标'}")

        # 冲突率
        conflict_rate = self.channel.causality.get_conflict_rate()
        print(f"\n⚡ 冲突率:")
        print(f"   实际: {conflict_rate * 100:.2f}%")
        print(f"   目标: ≤0.1%")
        print(
            f"   状态: {'✅ 达标' if conflict_rate <= 0.001 else '⚠️ 接近' if conflict_rate <= 0.005 else '❌ 未达标'}"
        )

        # 统计摘要
        stats = self.channel.get_stats()
        print(f"\n📈 统计摘要:")
        print(f"   总同步次数: {stats['total_syncs']}")
        print(f"   平均带宽降低: {stats['avg_bandwidth_reduction']}")
        print(f"   平均延迟: {stats['avg_latency_ms']}")
        print(f"   冲突率: {stats['conflict_rate']}")
        print(f"   总节省字节: {stats['total_bytes_saved']}")

        # 审计链
        audit_trail = self.channel.get_audit_trail(limit=5)
        print(f"\n📋 审计链（最近 5 条）:")
        for entry in audit_trail:
            print(
                f"   [{entry['transaction_id'][:8]}...] "
                f"{entry['source']} → {entry['destination']} | "
                f"类型: {entry['type']} | "
                f"延迟: {entry['latency_ms']:.1f}ms | "
                f"完整性: {'✅' if entry['integrity_ok'] else '❌'}"
            )

        print(f"\n{'=' * 70}")
        print(f"PoC 验证完成")
        print(f"{'=' * 70}")


async def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="幽灵通道 PoC — 多智能体记忆同步")
    parser.add_argument("--roles", type=int, default=3, help="角色数量 (默认: 3)")
    parser.add_argument("--rounds", type=int, default=50, help="同步轮次 (默认: 50)")
    args = parser.parse_args()

    poc = MemorySyncPoC(num_roles=args.roles, num_rounds=args.rounds)
    await poc.run()


if __name__ == "__main__":
    asyncio.run(main())
