"""
Ghost Channel Protocol - 100 Concurrent Stress Test
Multi-Agent Memory Sync Stress Test (100 concurrent agents)

Test Goals:
- 100 agents concurrent sync
- Verify latency, consistency, conflict rate
- Record P50/P95/P99 latency
"""

import asyncio
import sys
import time
import json
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

sys.path.insert(0, "python")
from ghost_channel_sdk import GhostChannelSDK, GhostChannelConfig
from ghost_channel_sdk.types import SyncResult, ErrorObject


@dataclass
class StressTestConfig:
    num_agents: int = 100
    num_rounds: int = 50
    sync_interval_ms: int = 10
    state_size_kb: float = 10.0
    enable_compression: bool = True
    completion_mode: str = "verify"


@dataclass
class StressTestMetrics:
    total_syncs: int = 0
    successful_syncs: int = 0
    failed_syncs: int = 0
    total_latency_ms: float = 0.0
    latencies_ms: List[float] = None
    bandwidth_reductions: List[float] = None
    consistency_checks: List[bool] = None
    errors: List[Dict] = None

    def __post_init__(self):
        self.latencies_ms = []
        self.bandwidth_reductions = []
        self.consistency_checks = []
        self.errors = []


class StressTestRunner:
    """100 Concurrent Stress Test Runner"""

    def __init__(self, config: StressTestConfig):
        self.config = config
        self.sdk = GhostChannelSDK(
            GhostChannelConfig(
                compression_level=9 if config.enable_compression else 0,
                semantic_threshold=0.7,
                audit_enabled=True,
                max_retry=3,
                completion_mode=config.completion_mode,
                await_ack=False,
            )
        )

        self.metrics = StressTestMetrics()
        self.agent_states: Dict[str, Dict] = {}
        self.agent_ids = [f"agent_{i:03d}" for i in range(config.num_agents)]

        for agent_id in self.agent_ids:
            self.agent_states[agent_id] = self._create_initial_state(agent_id)

    def _create_initial_state(self, agent_id: str) -> Dict:
        return {
            "__version__": "v0",
            "agent_id": agent_id,
            "knowledge": {},
            "decisions": [],
            "interactions": [],
            "context": f"Initial context for {agent_id}",
        }

    def _simulate_state_change(self, agent_id: str, round_num: int):
        state = self.agent_states[agent_id]
        state["__version__"] = f"v{round_num}"

        if random.random() < 0.8:
            if state["knowledge"]:
                key = random.choice(list(state["knowledge"].keys()))
                state["knowledge"][key]["confidence"] = min(
                    1.0,
                    state["knowledge"][key]["confidence"] + random.uniform(-0.05, 0.1),
                )
        else:
            state["decisions"].append(
                {
                    "round": round_num,
                    "decision": f"Decision {round_num}",
                    "rationale": f"Based on context {round_num}",
                }
            )
            state["knowledge"][f"fact_{round_num}"] = {
                "content": f"Knowledge {round_num}",
                "confidence": random.uniform(0.7, 1.0),
                "source": agent_id,
            }

        state["interactions"].append(
            {
                "round": round_num,
                "type": random.choice(["query", "response", "decision"]),
                "content": f"Interaction {round_num}",
            }
        )

    async def _single_sync(
        self, source_id: str, target_id: str, round_num: int
    ) -> SyncResult:
        old_state = self.agent_states[source_id].copy()
        self._simulate_state_change(source_id, round_num)
        new_state = self.agent_states[source_id]

        semantic_filter = f"round {round_num}" if round_num % 5 == 0 else None

        result = await self.sdk.sync_memory_delta(
            source_role=source_id,
            target_role=target_id,
            old_state=old_state,
            new_state=new_state,
            semantic_filter=semantic_filter,
        )

        if result.success:
            self.agent_states[target_id] = new_state.copy()

        return result

    async def _concurrent_round(self, round_num: int) -> List[SyncResult]:
        tasks = []
        for _ in range(self.config.num_agents // 2):
            source = random.choice(self.agent_ids)
            target = random.choice([a for a in self.agent_ids if a != source])
            tasks.append(self._single_sync(source, target, round_num))

        return await asyncio.gather(*tasks, return_exceptions=True)

    async def run(self) -> Dict:
        print("=" * 70)
        print("Ghost Channel Protocol - 100 Concurrent Stress Test")
        print(f"Agents: {self.config.num_agents} | Rounds: {self.config.num_rounds}")
        print(f"Concurrent syncs/round: {self.config.num_agents // 2}")
        print("=" * 70)

        start_time = time.perf_counter()

        for round_num in range(1, self.config.num_rounds + 1):
            results = await self._concurrent_round(round_num)

            for result in results:
                if isinstance(result, Exception):
                    self.metrics.failed_syncs += 1
                    self.metrics.errors.append(
                        {
                            "type": "exception",
                            "message": str(result),
                            "round": round_num,
                        }
                    )
                elif isinstance(result, SyncResult):
                    self.metrics.total_syncs += 1
                    if result.success:
                        self.metrics.successful_syncs += 1
                    else:
                        self.metrics.failed_syncs += 1
                        if result.errors:
                            self.metrics.errors.append(
                                {
                                    "type": "sync_error",
                                    "errors": [
                                        asdict(e) if hasattr(e, "__dict__") else e
                                        for e in result.errors
                                    ],
                                    "round": round_num,
                                }
                            )

                    self.metrics.latencies_ms.append(result.latency_ms)
                    self.metrics.bandwidth_reductions.append(result.bandwidth_reduction)
                    self.metrics.consistency_checks.append(result.consistency_verified)

            if round_num % 10 == 0:
                self._print_progress(round_num)

        total_time = time.perf_counter() - start_time
        return self._generate_report(total_time)

    def _print_progress(self, round_num: int):
        recent = self.metrics.latencies_ms[-50:] if self.metrics.latencies_ms else [0]
        p95 = (
            sorted(recent)[int(len(recent) * 0.95)] if len(recent) > 10 else max(recent)
        )

        recent_bw = (
            self.metrics.bandwidth_reductions[-50:]
            if self.metrics.bandwidth_reductions
            else [0]
        )
        avg_bw = statistics.mean(recent_bw) if recent_bw else 0

        print(
            f"  Round {round_num:3d} | "
            f"Synced: {self.metrics.total_syncs:4d} | "
            f"Success: {self.metrics.successful_syncs:4d} | "
            f"P95: {p95:.1f}ms | "
            f"BW: {avg_bw * 100:.1f}%"
        )

    def _calculate_percentiles(self, data: List[float]) -> Dict[str, float]:
        if not data:
            return {"p50": 0, "p95": 0, "p99": 0, "min": 0, "max": 0, "avg": 0}

        sorted_data = sorted(data)
        n = len(sorted_data)

        return {
            "p50": sorted_data[int(n * 0.50)],
            "p95": sorted_data[int(n * 0.95)],
            "p99": sorted_data[int(n * 0.99)],
            "min": min(data),
            "max": max(data),
            "avg": statistics.mean(data),
        }

    def _generate_report(self, total_time: float) -> Dict:
        print("\n" + "=" * 70)
        print("STRESS TEST REPORT - 100 Concurrent Multi-Agent Memory Sync")
        print("=" * 70)

        latency_stats = self._calculate_percentiles(self.metrics.latencies_ms)
        bw_stats = self._calculate_percentiles(self.metrics.bandwidth_reductions)

        consistency_rate = (
            sum(self.metrics.consistency_checks) / len(self.metrics.consistency_checks)
            if self.metrics.consistency_checks
            else 0
        )

        success_rate = self.metrics.successful_syncs / max(self.metrics.total_syncs, 1)

        report = {
            "test_config": asdict(self.config),
            "summary": {
                "total_time_seconds": round(total_time, 2),
                "total_syncs": self.metrics.total_syncs,
                "successful_syncs": self.metrics.successful_syncs,
                "failed_syncs": self.metrics.failed_syncs,
                "success_rate": round(success_rate * 100, 2),
                "throughput_per_second": round(
                    self.metrics.total_syncs / max(total_time, 0.001), 2
                ),
            },
            "latency": {
                "p50_ms": round(latency_stats["p50"], 3),
                "p95_ms": round(latency_stats["p95"], 3),
                "p99_ms": round(latency_stats["p99"], 3),
                "min_ms": round(latency_stats["min"], 3),
                "max_ms": round(latency_stats["max"], 3),
                "avg_ms": round(latency_stats["avg"], 3),
            },
            "bandwidth": {
                "p50": round(bw_stats["p50"] * 100, 2),
                "p95": round(bw_stats["p95"] * 100, 2),
                "p99": round(bw_stats["p99"] * 100, 2),
                "min": round(bw_stats["min"] * 100, 2),
                "max": round(bw_stats["max"] * 100, 2),
                "avg": round(bw_stats["avg"] * 100, 2),
            },
            "consistency": {
                "rate": round(consistency_rate * 100, 2),
                "checks_passed": sum(self.metrics.consistency_checks),
                "checks_total": len(self.metrics.consistency_checks),
            },
            "errors": {
                "count": len(self.metrics.errors),
                "samples": self.metrics.errors[:10],
            },
            "validation": {
                "latency_p99_target": 50,
                "latency_p99_pass": latency_stats["p99"] <= 50,
                "bandwidth_avg_target": 80,
                "bandwidth_avg_pass": bw_stats["avg"] * 100 >= 80,
                "consistency_target": 99,
                "consistency_pass": consistency_rate * 100 >= 99,
                "success_rate_target": 99,
                "success_rate_pass": success_rate * 100 >= 99,
            },
        }

        print(f"\n[TEST CONFIG]")
        print(f"   Agents: {self.config.num_agents}")
        print(f"   Rounds: {self.config.num_rounds}")
        print(f"   Concurrent syncs/round: {self.config.num_agents // 2}")

        print(f"\n[PERFORMANCE SUMMARY]")
        print(f"   Total syncs: {report['summary']['total_syncs']}")
        print(f"   Successful: {report['summary']['successful_syncs']}")
        print(f"   Failed: {report['summary']['failed_syncs']}")
        print(f"   Success rate: {report['summary']['success_rate']}%")
        print(f"   Throughput: {report['summary']['throughput_per_second']} syncs/s")

        print(f"\n[LATENCY STATS]")
        print(f"   P50: {report['latency']['p50_ms']:.2f}ms")
        print(f"   P95: {report['latency']['p95_ms']:.2f}ms")
        print(f"   P99: {report['latency']['p99_ms']:.2f}ms")
        print(f"   Avg: {report['latency']['avg_ms']:.2f}ms")
        print(f"   Max: {report['latency']['max_ms']:.2f}ms")
        print(
            f"   Target P99<=50ms: {'PASS' if report['validation']['latency_p99_pass'] else 'FAIL'}"
        )

        print(f"\n[BANDWIDTH REDUCTION]")
        print(f"   Avg: {report['bandwidth']['avg']:.1f}%")
        print(f"   P95: {report['bandwidth']['p95']:.1f}%")
        print(
            f"   Target>=80%: {'PASS' if report['validation']['bandwidth_avg_pass'] else 'FAIL'}"
        )

        print(f"\n[CONSISTENCY]")
        print(f"   Pass rate: {report['consistency']['rate']:.2f}%")
        print(
            f"   Target>=99%: {'PASS' if report['validation']['consistency_pass'] else 'FAIL'}"
        )

        if report["errors"]["count"] > 0:
            print(f"\n[ERRORS]: {report['errors']['count']} total")
            for err in report["errors"]["samples"][:3]:
                print(
                    f"   - {err.get('type', 'unknown')}: {err.get('message', str(err))}"
                )
        else:
            print(f"\n[ERRORS]: None")

        print(f"\n{'=' * 70}")
        print("[VALIDATION RESULTS]")
        print(
            f"   Latency P99<=50ms: {'PASS' if report['validation']['latency_p99_pass'] else 'FAIL'}"
        )
        print(
            f"   Bandwidth>=80%: {'PASS' if report['validation']['bandwidth_avg_pass'] else 'FAIL'}"
        )
        print(
            f"   Consistency>=99%: {'PASS' if report['validation']['consistency_pass'] else 'FAIL'}"
        )
        print(
            f"   Success rate>=99%: {'PASS' if report['validation']['success_rate_pass'] else 'FAIL'}"
        )

        all_pass = all(
            [
                report["validation"]["latency_p99_pass"],
                report["validation"]["bandwidth_avg_pass"],
                report["validation"]["consistency_pass"],
                report["validation"]["success_rate_pass"],
            ]
        )
        print(f"\nOverall: {'ALL PASS' if all_pass else 'PARTIAL PASS'}")
        print(f"{'=' * 70}")

        return report


async def main():
    config = StressTestConfig(
        num_agents=100,
        num_rounds=50,
        sync_interval_ms=10,
        state_size_kb=10.0,
        enable_compression=True,
        completion_mode="verify",
    )

    runner = StressTestRunner(config)
    report = await runner.run()

    report_path = "stress_test_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nReport saved: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
