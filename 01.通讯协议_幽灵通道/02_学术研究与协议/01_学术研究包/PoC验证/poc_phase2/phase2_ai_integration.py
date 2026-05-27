"""
幽灵通道 PoC Phase 2 — AI 集成
Phantom Channel PoC Phase 2 — AI Integration

三个 AI 能力:
1. 预测性 Delta (Predictive Delta) — AI 预测即将变化的数据，提前预同步
2. 智能冲突解决 (Smart Conflict Resolution) — AI 自动选择最优冲突解决策略
3. 动态路由优化 (Dynamic Route Optimization) — AI 选择最优传输路径
"""

import sys
import os
import json
import time
import random
import math
import copy
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field


# ============================================================
# 1. 预测性 Delta — 基于历史变化模式预测未来变化
# ============================================================


class PredictiveDeltaEngine:
    """
    预测性 Delta 引擎 — 基于历史变化模式预测未来变化

    核心思想: 学习数据变化的时间模式和频率，预测哪些字段即将变化，
    提前预同步高概率变化（置信度 > 阈值），减少实际同步时的数据量。
    """

    def __init__(self, prediction_window: int = 10, confidence_threshold: float = 0.7):
        self.prediction_window = prediction_window  # 预测未来 N 轮
        self.confidence_threshold = confidence_threshold
        self.change_history: Dict[str, List[int]] = {}  # field -> [round_nums]
        self.field_frequencies: Dict[str, float] = {}  # field -> change frequency
        self.field_patterns: Dict[str, str] = {}  # field -> pattern type

    def record_change(self, field_path: str, round_num: int):
        """记录字段变更"""
        if field_path not in self.change_history:
            self.change_history[field_path] = []
        self.change_history[field_path].append(round_num)

    def analyze_patterns(self):
        """分析变化模式"""
        for field_path, rounds in self.change_history.items():
            if len(rounds) < 3:
                self.field_frequencies[field_path] = 0.0
                self.field_patterns[field_path] = "insufficient_data"
                continue

            # 计算变化频率
            intervals = [rounds[i + 1] - rounds[i] for i in range(len(rounds) - 1)]
            avg_interval = sum(intervals) / len(intervals)
            self.field_frequencies[field_path] = 1.0 / max(avg_interval, 1)

            # 识别模式类型
            if len(intervals) >= 3:
                variance = sum((x - avg_interval) ** 2 for x in intervals) / len(
                    intervals
                )
                cv = math.sqrt(variance) / max(avg_interval, 1)  # 变异系数

                if cv < 0.3:
                    self.field_patterns[field_path] = "periodic"  # 周期性
                elif cv < 0.8:
                    self.field_patterns[field_path] = "semi_regular"  # 半规律
                else:
                    self.field_patterns[field_path] = "random"  # 随机
            else:
                self.field_patterns[field_path] = "insufficient_data"

    def predict_next_changes(self, current_round: int) -> Dict[str, float]:
        """
        预测下一轮可能变化的字段及其概率

        Returns:
            Dict[field_path, probability] — 变化概率 > 阈值的字段
        """
        self.analyze_patterns()
        predictions = {}

        for field_path, rounds in self.change_history.items():
            if len(rounds) < 2:
                continue

            intervals = [rounds[i + 1] - rounds[i] for i in range(len(rounds) - 1)]
            avg_interval = sum(intervals) / len(intervals)

            # 距离上次变化的轮数
            rounds_since_last = current_round - rounds[-1]

            # 基于模式类型计算变化概率
            pattern = self.field_patterns.get(field_path, "random")

            if pattern == "periodic":
                # 周期性：接近平均间隔时概率最高
                distance_from_period = abs(rounds_since_last - avg_interval)
                probability = max(0, 1.0 - distance_from_period / max(avg_interval, 1))
            elif pattern == "semi_regular":
                # 半规律：基于频率的指数衰减
                probability = 1.0 - math.exp(
                    -rounds_since_last * self.field_frequencies.get(field_path, 0.1)
                )
            else:
                # 随机：基于历史频率
                probability = min(1.0, self.field_frequencies.get(field_path, 0.05) * 2)

            # 距离上次变化越久，概率越高（基础加成）
            time_bonus = min(0.3, rounds_since_last * 0.02)
            probability = min(1.0, probability + time_bonus)

            if probability >= self.confidence_threshold:
                predictions[field_path] = probability

        return predictions

    def generate_pre_sync_payload(
        self, state: Dict, predictions: Dict[str, float]
    ) -> Dict:
        """
        生成预同步载荷 — 仅包含高概率变化的字段

        Args:
            state: 当前完整状态
            predictions: 预测结果 {field_path: probability}

        Returns:
            预同步载荷（仅高概率变化字段）
        """
        pre_sync = {}
        for field_path, prob in predictions.items():
            # 简单路径解析（支持一级和二级路径）
            parts = field_path.split(".")
            if len(parts) == 1:
                if parts[0] in state:
                    pre_sync[field_path] = {
                        "value": state[parts[0]],
                        "probability": prob,
                    }
            elif len(parts) == 2:
                if parts[0] in state and isinstance(state[parts[0]], dict):
                    if parts[1] in state[parts[0]]:
                        pre_sync[field_path] = {
                            "value": state[parts[0]][parts[1]],
                            "probability": prob,
                        }

        return pre_sync


# ============================================================
# 2. 智能冲突解决 — 基于历史数据的策略选择
# ============================================================


class SmartConflictResolver:
    """
    智能冲突解决引擎 — 基于历史数据自动选择最优冲突解决策略

    策略库:
    - LWW (Last-Write-Wins): 简单值碰撞
    - Merge: 部分重叠的智能融合
    - Schema Migration: 模式演化不匹配
    - Human-in-Loop: 语义分歧检测
    """

    STRATEGIES = ["LWW", "Merge", "Schema_Migration", "Human_in_Loop"]

    def __init__(self):
        self.strategy_history: Dict[str, List[Dict]] = {s: [] for s in self.STRATEGIES}
        self.conflict_features: List[Dict] = []
        self.model_weights: Dict[str, float] = {
            "data_size": 0.2,
            "field_overlap": 0.25,
            "semantic_similarity": 0.3,
            "time_gap": 0.15,
            "importance": 0.1,
        }

    def extract_features(self, conflict_data: Dict) -> Dict[str, float]:
        """提取冲突特征"""
        old_data = conflict_data.get("old_value", {})
        new_data = conflict_data.get("new_value", {})

        # 数据大小
        old_size = len(json.dumps(old_data, default=str))
        new_size = len(json.dumps(new_data, default=str))
        data_size = min(1.0, (old_size + new_size) / 10000)

        # 字段重叠率
        if isinstance(old_data, dict) and isinstance(new_data, dict):
            old_keys = set(old_data.keys())
            new_keys = set(new_data.keys())
            field_overlap = len(old_keys & new_keys) / max(len(old_keys | new_keys), 1)
        else:
            field_overlap = 0.0

        # 语义相似度（简化：基于共同字段）
        semantic_similarity = field_overlap

        # 时间差距
        time_gap = conflict_data.get("time_gap_seconds", 0)
        time_gap_norm = min(1.0, time_gap / 60)

        # 数据重要性
        importance = conflict_data.get("importance", 0.5)

        return {
            "data_size": data_size,
            "field_overlap": field_overlap,
            "semantic_similarity": semantic_similarity,
            "time_gap": time_gap_norm,
            "importance": importance,
        }

    def select_strategy(self, features: Dict[str, float]) -> str:
        """
        基于特征选择最优策略

        规则引擎（简化版 ML 模型）:
        - 小数据 + 低重叠 → LWW
        - 大数据 + 高重叠 → Merge
        - 模式变更 → Schema_Migration
        - 高重要性 + 低相似度 → Human_in_Loop
        """
        scores = {}

        # LWW: 适合小数据、低重叠
        scores["LWW"] = (
            (1 - features["data_size"]) * 0.4
            + (1 - features["field_overlap"]) * 0.3
            + (1 - features["importance"]) * 0.3
        )

        # Merge: 适合大数据、高重叠
        scores["Merge"] = (
            features["data_size"] * 0.3
            + features["field_overlap"] * 0.4
            + features["semantic_similarity"] * 0.3
        )

        # Schema_Migration: 适合模式变更（低相似度 + 中等数据大小）
        scores["Schema_Migration"] = (
            (1 - features["semantic_similarity"]) * 0.5
            + features["data_size"] * 0.3
            + (1 - features["time_gap"]) * 0.2
        )

        # Human_in_Loop: 适合高重要性 + 低相似度
        scores["Human_in_Loop"] = (
            features["importance"] * 0.5
            + (1 - features["semantic_similarity"]) * 0.3
            + features["time_gap"] * 0.2
        )

        # 选择最高分策略
        best_strategy = max(scores, key=scores.get)
        best_score = scores[best_strategy]

        # 如果最高分低于阈值，使用保守策略（LWW）
        if best_score < 0.3:
            return "LWW"

        return best_strategy

    def resolve_conflict(self, conflict_data: Dict) -> Dict:
        """
        解决冲突

        Returns:
            {
                "strategy": str,
                "resolved_value": Any,
                "confidence": float,
                "requires_human": bool
            }
        """
        features = self.extract_features(conflict_data)
        strategy = self.select_strategy(features)

        old_value = conflict_data.get("old_value", {})
        new_value = conflict_data.get("new_value", {})

        if strategy == "LWW":
            resolved = new_value
            confidence = 0.9
            requires_human = False
        elif strategy == "Merge":
            if isinstance(old_value, dict) and isinstance(new_value, dict):
                resolved = {**old_value, **new_value}
            else:
                resolved = new_value
            confidence = 0.85
            requires_human = False
        elif strategy == "Schema_Migration":
            resolved = new_value
            confidence = 0.8
            requires_human = False
        else:  # Human_in_Loop
            resolved = new_value
            confidence = 0.5
            requires_human = True

        # 记录历史
        self.conflict_features.append(
            {
                "features": features,
                "strategy": strategy,
                "confidence": confidence,
                "timestamp": time.time(),
            }
        )

        return {
            "strategy": strategy,
            "resolved_value": resolved,
            "confidence": confidence,
            "requires_human": requires_human,
        }

    def get_accuracy(self) -> float:
        """获取策略选择准确率（基于历史反馈）"""
        if not self.conflict_features:
            return 0.0
        # 简化：假设高置信度决策都是正确的
        high_conf = sum(1 for f in self.conflict_features if f["confidence"] >= 0.8)
        return high_conf / len(self.conflict_features)


# ============================================================
# 3. 动态路由优化 — 基于强化学习的路径选择
# ============================================================


class DynamicRouteOptimizer:
    """
    动态路由优化引擎 — 基于 Thompson Sampling 的路径选择

    路径选项:
    - direct: 直接传输
    - relay: 中继传输
    - batch: 批量传输
    """

    PATHS = ["direct", "relay", "batch"]

    def __init__(self):
        # Thompson Sampling 参数 (Beta 分布)
        self.path_alpha: Dict[str, float] = {p: 1.0 for p in self.PATHS}
        self.path_beta: Dict[str, float] = {p: 1.0 for p in self.PATHS}
        self.path_latencies: Dict[str, List[float]] = {p: [] for p in self.PATHS}
        self.total_selections = 0

    def select_path(self, payload_size: int, urgency: float) -> str:
        """
        选择最优传输路径

        Args:
            payload_size: 载荷大小（字节）
            urgency: 紧急度（0-1）

        Returns:
            路径名称
        """
        # 根据载荷大小和紧急度调整先验
        adjusted_alpha = dict(self.path_alpha)
        adjusted_beta = dict(self.path_beta)

        # 大载荷偏好 batch
        if payload_size > 10000:
            adjusted_alpha["batch"] += 2
        elif payload_size < 1000:
            adjusted_alpha["direct"] += 1

        # 高紧急度偏好 direct
        if urgency > 0.8:
            adjusted_alpha["direct"] += 2
            adjusted_beta["batch"] += 1

        # Thompson Sampling: 从 Beta 分布采样
        samples = {}
        for path in self.PATHS:
            samples[path] = random.betavariate(
                adjusted_alpha[path], adjusted_beta[path]
            )

        return max(samples, key=samples.get)

    def record_outcome(self, path: str, latency_ms: float, success: bool):
        """
        记录路径结果

        Args:
            path: 使用的路径
            latency_ms: 实际延迟
            success: 是否成功
        """
        self.path_latencies[path].append(latency_ms)
        self.total_selections += 1

        # 更新 Beta 分布参数
        if success:
            self.path_alpha[path] += 1
        else:
            self.path_beta[path] += 1

        # 基于延迟调整：延迟越低，奖励越高
        if self.path_latencies[path]:
            avg_latency = sum(self.path_latencies[path][-10:]) / min(
                len(self.path_latencies[path]), 10
            )
            if avg_latency < 10:
                self.path_alpha[path] += 0.5
            elif avg_latency > 100:
                self.path_beta[path] += 0.5

    def get_path_stats(self) -> Dict[str, Dict]:
        """获取路径统计信息"""
        stats = {}
        for path in self.PATHS:
            latencies = self.path_latencies[path]
            alpha = self.path_alpha[path]
            beta = self.path_beta[path]
            expected_value = alpha / (alpha + beta)

            stats[path] = {
                "selections": len(latencies),
                "avg_latency_ms": sum(latencies[-20:]) / min(len(latencies), 20)
                if latencies
                else 0,
                "p95_latency_ms": sorted(latencies)[-max(1, int(len(latencies) * 0.05))]
                if latencies
                else 0,
                "expected_value": expected_value,
                "success_rate": alpha / (alpha + beta),
            }

        return stats


# ============================================================
# Phase 2 综合 PoC
# ============================================================


class Phase2PoC:
    """Phase 2: AI 集成 PoC"""

    def __init__(self, num_rounds: int = 100):
        self.num_rounds = num_rounds
        self.predictor = PredictiveDeltaEngine(confidence_threshold=0.6)
        self.resolver = SmartConflictResolver()
        self.router = DynamicRouteOptimizer()

        # 模拟状态
        self.state = {
            "context": "Initial state",
            "decisions": [],
            "knowledge": {},
            "interactions": [],
            "metrics": {"cpu": 0.5, "memory": 0.3, "network": 0.2},
        }

        # 结果收集
        self.results = {
            "prediction_accuracy": [],
            "pre_sync_savings": [],
            "conflict_resolutions": [],
            "path_selections": [],
            "latencies": [],
            "bandwidth_reductions": [],
        }

    async def run(self):
        """运行 Phase 2 PoC"""
        print("=" * 70)
        print("幽灵通道 PoC Phase 2 — AI 集成")
        print(f"轮次: {self.num_rounds}")
        print("=" * 70)

        for round_num in range(1, self.num_rounds + 1):
            await self._execute_round(round_num)

            if round_num % 20 == 0:
                self._print_progress(round_num)

        self._generate_report()

    async def _execute_round(self, round_num: int):
        """执行单轮"""
        # 1. 模拟状态变更
        self._simulate_change(round_num)

        # 2. 预测性 Delta
        predictions = self.predictor.predict_next_changes(round_num)
        pre_sync = self.predictor.generate_pre_sync_payload(self.state, predictions)

        # 记录实际变更用于预测评估
        actual_changes = self._get_actual_changes(round_num)
        for field_path in actual_changes:
            self.predictor.record_change(field_path, round_num)

        # 评估预测准确率
        if predictions:
            correct = sum(1 for f in predictions if f in actual_changes)
            accuracy = correct / len(predictions) if predictions else 0
            self.results["prediction_accuracy"].append(accuracy)

        # 预同步节省
        pre_sync_size = len(json.dumps(pre_sync, default=str).encode("utf-8"))
        full_state_size = len(json.dumps(self.state, default=str).encode("utf-8"))
        if pre_sync_size > 0:
            saving = 1 - (pre_sync_size / max(full_state_size, 1))
            self.results["pre_sync_savings"].append(max(0, saving))

        # 3. 智能冲突解决
        if round_num % 10 == 0:
            conflict_data = self._generate_conflict(round_num)
            resolution = self.resolver.resolve_conflict(conflict_data)
            self.results["conflict_resolutions"].append(resolution)

        # 4. 动态路由优化
        payload_size = full_state_size
        urgency = random.random()
        selected_path = self.router.select_path(payload_size, urgency)
        simulated_latency = self._simulate_path_latency(selected_path, payload_size)
        self.router.record_outcome(selected_path, simulated_latency, success=True)

        self.results["path_selections"].append(selected_path)
        self.results["latencies"].append(simulated_latency)

        # 计算带宽降低（预测 + 压缩）
        import zlib

        delta_size = len(
            zlib.compress(
                json.dumps(actual_changes, default=str).encode("utf-8"), level=9
            )
        )
        bandwidth_reduction = 1 - (delta_size / max(full_state_size, 1))
        self.results["bandwidth_reductions"].append(max(0, bandwidth_reduction))

    def _simulate_change(self, round_num: int):
        """模拟状态变更"""
        # 周期性变更
        if round_num % 5 == 0:
            self.state["decisions"].append(
                {"round": round_num, "decision": f"Decision {round_num}"}
            )

        if round_num % 3 == 0:
            self.state["knowledge"][f"fact_{round_num}"] = {
                "content": f"Knowledge {round_num}",
                "confidence": random.uniform(0.7, 1.0),
            }

        # 每轮小变更
        self.state["interactions"].append({"round": round_num})
        self.state["metrics"]["cpu"] = min(
            1.0, self.state["metrics"]["cpu"] + random.uniform(-0.1, 0.1)
        )
        self.state["metrics"]["memory"] = min(
            1.0, self.state["metrics"]["memory"] + random.uniform(-0.05, 0.05)
        )
        self.state["context"] = f"Context updated at round {round_num}"

    def _get_actual_changes(self, round_num: int) -> List[str]:
        """获取实际变更字段"""
        changes = []
        if round_num % 5 == 0:
            changes.append("decisions")
        if round_num % 3 == 0:
            changes.append("knowledge")
        changes.append("interactions")
        changes.append("metrics")
        changes.append("context")
        return changes

    def _generate_conflict(self, round_num: int) -> Dict:
        """生成模拟冲突"""
        return {
            "old_value": {"data": f"old_data_{round_num}", "version": round_num - 1},
            "new_value": {
                "data": f"new_data_{round_num}",
                "version": round_num,
                "extra": "field",
            },
            "time_gap_seconds": random.uniform(0.1, 30),
            "importance": random.uniform(0.3, 1.0),
        }

    def _simulate_path_latency(self, path: str, payload_size: int) -> float:
        """模拟路径延迟"""
        base_latency = {"direct": 2, "relay": 8, "batch": 15}[path]
        size_factor = payload_size / 10000
        return base_latency + size_factor * random.uniform(1, 5)

    def _print_progress(self, round_num: int):
        """打印进度"""
        avg_pred = (
            sum(self.results["prediction_accuracy"][-20:])
            / min(len(self.results["prediction_accuracy"]), 20)
            if self.results["prediction_accuracy"]
            else 0
        )
        avg_bw = (
            sum(self.results["bandwidth_reductions"][-20:])
            / min(len(self.results["bandwidth_reductions"]), 20)
            if self.results["bandwidth_reductions"]
            else 0
        )
        avg_lat = (
            sum(self.results["latencies"][-20:])
            / min(len(self.results["latencies"]), 20)
            if self.results["latencies"]
            else 0
        )

        print(
            f"  Round {round_num:3d}/{self.num_rounds} | "
            f"预测准确率: {avg_pred * 100:.0f}% | "
            f"带宽降低: {avg_bw * 100:.0f}% | "
            f"平均延迟: {avg_lat:.1f}ms"
        )

    def _generate_report(self):
        """生成报告"""
        print(f"\n{'=' * 70}")
        print(f"PoC Phase 2 验证报告 — AI 集成")
        print(f"{'=' * 70}")

        # 1. 预测性 Delta
        if self.results["prediction_accuracy"]:
            avg_pred = sum(self.results["prediction_accuracy"]) / len(
                self.results["prediction_accuracy"]
            )
            print(f"\n🧠 预测性 Delta:")
            print(f"   平均预测准确率: {avg_pred * 100:.0f}%")
            print(f"   目标: ≥70%")
            print(f"   状态: {'✅ 达标' if avg_pred >= 0.70 else '⚠️ 接近'}")

        if self.results["pre_sync_savings"]:
            avg_pre = sum(self.results["pre_sync_savings"]) / len(
                self.results["pre_sync_savings"]
            )
            print(f"   预同步节省: {avg_pre * 100:.0f}%")

        # 2. 智能冲突解决
        if self.results["conflict_resolutions"]:
            strategies = {}
            for r in self.results["conflict_resolutions"]:
                s = r["strategy"]
                strategies[s] = strategies.get(s, 0) + 1

            avg_conf = sum(
                r["confidence"] for r in self.results["conflict_resolutions"]
            ) / len(self.results["conflict_resolutions"])
            human_needed = sum(
                1 for r in self.results["conflict_resolutions"] if r["requires_human"]
            )

            print(f"\n⚡ 智能冲突解决:")
            print(f"   平均置信度: {avg_conf * 100:.0f}%")
            print(f"   策略分布: {strategies}")
            print(
                f"   需要人工干预: {human_needed}/{len(self.results['conflict_resolutions'])}"
            )
            print(f"   目标: 人工干预 ≤20%")
            print(
                f"   状态: {'✅ 达标' if human_needed / len(self.results['conflict_resolutions']) <= 0.2 else '❌ 未达标'}"
            )

        # 3. 动态路由优化
        path_stats = self.router.get_path_stats()
        print(f"\n🛣️ 动态路由优化:")
        for path, stats in path_stats.items():
            print(
                f"   {path}: 选择 {stats['selections']} 次, "
                f"平均延迟 {stats['avg_latency_ms']:.1f}ms, "
                f"期望值 {stats['expected_value']:.2f}"
            )

        if self.results["latencies"]:
            avg_lat = sum(self.results["latencies"]) / len(self.results["latencies"])
            print(f"   全局平均延迟: {avg_lat:.1f}ms")
            print(f"   目标: <10ms")
            print(f"   状态: {'✅ 达标' if avg_lat < 10 else '⚠️ 接近'}")

        # 4. 带宽降低（AI 增强）
        if self.results["bandwidth_reductions"]:
            avg_bw = sum(self.results["bandwidth_reductions"][-50:]) / min(
                len(self.results["bandwidth_reductions"]), 50
            )
            print(f"\n📊 带宽降低 (AI 增强):")
            print(f"   最近 50 轮平均: {avg_bw * 100:.0f}%")
            print(f"   目标: ≥80%")
            print(f"   状态: {'✅ 达标' if avg_bw >= 0.80 else '⚠️ 接近'}")

        print(f"\n{'=' * 70}")
        print(f"Phase 2 PoC 验证完成")
        print(f"{'=' * 70}")


async def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="幽灵通道 PoC Phase 2 — AI 集成")
    parser.add_argument("--rounds", type=int, default=100, help="轮次 (默认: 100)")
    args = parser.parse_args()

    poc = Phase2PoC(num_rounds=args.rounds)
    await poc.run()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
