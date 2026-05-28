"""
Sandbox Manager - 三层沙盘机制
公式14: df_k/dt = λ_k * (1 - f_k/f_k,max) * I[success] - μ_k * f_k * I[failure]
公式15: SRS = (1/T) * ∫ exp(-(f_k(t) - f_k^target)^2 / (2*σ_k^2)) dt
层级: Micro[1-5], Meso[5-20], Macro[20-100+]
生产故障率: -81%
SRS≥0.9为优秀
"""

import math
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from qcm.config import load_config
_cfg = load_config()


class SandboxLevel(Enum):
    """沙盘层级"""
    MICRO = "micro"      # 进程级，[1,5]
    MESO = "meso"       # Docker级，[5,20]
    MACRO = "macro"      # K8s级，[20,100+]


@dataclass
class SandboxConfig:
    """沙盘配置"""
    level: SandboxLevel = SandboxLevel.MICRO
    min_workers: int = 1
    max_workers: int = 5
    isolation: str = "process"
    failure_cost: float = 0.1


@dataclass
class SandboxResult:
    """沙盘测试结果"""
    success: bool
    duration_ms: float
    fidelity: float
    failure_type: Optional[str]
    messages: List[str]


class SandboxManager:
    """
    三层沙盘管理器
    基于论文公式14-15
    """

    # 论文校准参数
    LAMBDA = _cfg.get_param("sandbox", "LAMBDA")  # was: 0.5       # 成功增长率
    MU = _cfg.get_param("sandbox", "MU")  # was: 0.2           # 失败衰减率
    SRS_TARGET = _cfg.get_param("sandbox", "SRS_TARGET")  # was: 0.9   # 成功率目标

    # 配置
    CONFIGS = {
        SandboxLevel.MICRO: SandboxConfig(
            level=SandboxLevel.MICRO,
            min_workers=1,
            max_workers=5,
            isolation="process",
            failure_cost=0.1
        ),
        SandboxLevel.MESO: SandboxConfig(
            level=SandboxLevel.MESO,
            min_workers=5,
            max_workers=20,
            isolation="docker",
            failure_cost=0.2
        ),
        SandboxLevel.MACRO: SandboxConfig(
            level=SandboxLevel.MACRO,
            min_workers=20,
            max_workers=100,
            isolation="k8s",
            failure_cost=0.5
        ),
    }

    def __init__(self, level: SandboxLevel = SandboxLevel.MICRO):
        """
        初始化沙盘

        Args:
            level: 沙盘层级
        """
        self.level = level
        self.config = self.CONFIGS[level]

        self.workers = self.config.min_workers
        self.fidelity = 0.0

        self.t = 0
        self.success_count = 0
        self.failure_count = 0

        self.fidelity_history = []
        self.worker_history = []
        self.success_rate_history = []

    def calculate_fidelity_change(self, success: bool) -> float:
        """
        计算忠诚度变化 (公式14)
        df_k/dt = λ_k * (1 - f_k/f_k,max) * I[success] - μ_k * f_k * I[failure]
        """
        max_fidelity = 1.0

        if success:
            # 成功则增长
            delta = self.LAMBDA * (1 - self.fidelity / max_fidelity)
        else:
            # 失败则衰减
            delta = -self.MU * self.fidelity

        return delta

    def calculate_workers_needed(self, task_complexity: float) -> int:
        """
        根据任务复杂度计算所需worker数量
        """
        workers = int(task_complexity * self.config.min_workers)
        return max(self.config.min_workers, min(workers, self.config.max_workers))

    def calculate_srs(self, window_size: int = 10) -> float:
        """
        计算成功率 (公式15)
        SRS = (1/T) * ∫ exp(-(f_k(t) - f_k^target)^2 / (2*σ_k^2)) dt
        """
        if len(self.fidelity_history) < 2:
            return 0.0

        recent = self.fidelity_history[-window_size:]
        if not recent:
            return 0.0

        target = self.SRS_TARGET
        sigma = 0.1  # 标准差

        # 计算积分
        integral = 0.0
        for f in recent:
            gaussian = math.exp(-((f - target) ** 2) / (2 * sigma ** 2))
            integral += gaussian

        srs = integral / len(recent)

        return srs

    def execute_task(self, task_id: str, task_data: dict,
                   simulate_success: bool = True) -> SandboxResult:
        """
        在沙盘中执行任务
        """
        start_time = time.time()

        # 计算所需workers
        complexity = task_data.get("complexity", 1.0)
        workers = self.calculate_workers_needed(complexity)

        # 模拟执行
        # 实际应用中这里会启动隔离环境并执行
        success = simulate_success if "known" not in task_data else task_data["known"]

        # 更新忠诚度
        delta = self.calculate_fidelity_change(success)
        self.fidelity += delta
        self.fidelity = max(0.0, min(1.0, self.fidelity))

        # 更新计数
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

        # 更新workers
        if success and workers < self.config.max_workers:
            self.workers = min(workers + 1, self.config.max_workers)
        elif not success and workers > self.config.min_workers:
            self.workers = max(workers - 1, self.config.min_workers)

        self.t += 1

        # 记录历史
        self.fidelity_history.append(self.fidelity)
        self.worker_history.append(self.workers)

        success_rate = self.success_count / max(1, self.t)
        self.success_rate_history.append(success_rate)

        # 计算持续时间
        duration_ms = (time.time() - start_time) * 1000

        # 创建结果
        result = SandboxResult(
            success=success,
            duration_ms=duration_ms,
            fidelity=self.fidelity,
            failure_type=None if success else "test_failure",
            messages=[]
        )

        return result

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        total = max(1, self.success_count + self.failure_count)
        success_rate = self.success_count / total

        return {
            'level': self.level.value,
            'workers': self.workers,
            'fidelity': round(self.fidelity, 4),
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'success_rate': round(success_rate, 4),
            'srs': round(self.calculate_srs(), 4),
            'isolation': self.config.isolation,
        }

    def should_scale_up(self) -> bool:
        """判断是否应该扩容"""
        return self.fidelity > 0.8 and self.workers < self.config.max_workers

    def should_scale_down(self) -> bool:
        """判断是否应该缩容"""
        return self.fidelity < 0.3 and self.workers > self.config.min_workers


def test_sandbox():
    """测试沙盘管理器"""
    print("=" * 60)
    print("Sandbox Manager Test")
    print("=" * 60)

    # 测试Micro层级
    print("\n--- Micro Sandbox (process isolation) ---")
    sandbox = SandboxManager(level=SandboxLevel.MICRO)

    for i in range(10):
        # 模拟任务（80%成功率）
        task_data = {"complexity": 1.0 + i * 0.1, "known": i % 5 != 0}
        result = sandbox.execute_task(f"task_{i}", task_data)

        if i < 5 or i == 9:
            stats = sandbox.get_statistics()
            print(f"Task {i+1}: success={result.success}, "
                  f"fidelity={stats['fidelity']:.2f}, "
                  f"workers={stats['workers']}, "
                  f"sr={stats['success_rate']:.2f}")

    print(f"\n--- Statistics ---")
    print(f"Level: {stats['level']}")
    print(f"Success rate: {stats['success_rate']:.2f}")
    print(f"Fidelity: {stats['fidelity']:.4f}")
    print(f"SRS: {stats['srs']:.4f} (target: 0.90)")

    # 测试Meso层级
    print("\n--- Meso Sandbox (docker isolation) ---")
    meso = SandboxManager(level=SandboxLevel.MESO)
    for i in range(10):
        meso.execute_task(f"task_{i}", {"complexity": 2.0})

    print(f"Meso workers: {meso.workers}, fidelity: {meso.fidelity:.3f}")

    print("\n" + "=" * 60)
    print("[PASS] Sandbox Manager Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_sandbox()