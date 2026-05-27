"""
Ghost Channel - Basic Example
幽灵通道 - 基础示例
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src", "python"))

from ghost_channel.core.protocol import GhostChannel, SyncConfig


async def basic_sync_example():
    """基础同步示例"""
    print("=" * 50)
    print("Ghost Channel - 基础同步示例")
    print("=" * 50)

    # 创建通道
    config = SyncConfig(node_id="node1")
    channel = GhostChannel(config, ["role_a", "role_b", "role_c"])

    # 初始状态
    state_a = {
        "context": "Project Alpha Development",
        "tasks": [],
        "decisions": [],
        "knowledge": {},
    }

    # 模拟多轮同步
    for round_num in range(1, 6):
        print(f"\n--- Round {round_num} ---")

        # 更新状态
        state_a["tasks"].append(f"Task {round_num}")
        state_a["decisions"].append(
            {
                "round": round_num,
                "decision": f"Decision {round_num}",
            }
        )
        state_a["knowledge"][f"fact_{round_num}"] = {
            "content": f"Knowledge {round_num}",
            "confidence": 0.8 + round_num * 0.02,
        }

        # 执行同步
        result = await channel.sync_memory_delta(
            source_role="role_a",
            target_role="role_b",
            memory_snapshot=state_a,
        )

        print(f"  成功: {result.success}")
        print(f"  带宽降低: {result.bandwidth_reduction * 100:.1f}%")
        print(f"  延迟: {result.latency_ms:.2f}ms")
        print(f"  变更数: {result.changes_applied}")
        print(f"  一致性: {result.consistency_verified}")

    # 最终统计
    print("\n" + "=" * 50)
    print("最终统计")
    print("=" * 50)

    stats = channel.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # 审计日志
    print("\n审计链 (最近3条):")
    audit = channel.get_audit_trail(limit=3)
    for entry in audit:
        print(
            f"  {entry['source_role']} → {entry['destination_role']} | "
            f"{entry['message_type']} | {entry['bandwidth_saved_bytes']} bytes saved"
        )


async def semantic_filter_example():
    """语义过滤示例"""
    print("\n" + "=" * 50)
    print("Ghost Channel - 语义过滤示例")
    print("=" * 50)

    config = SyncConfig(node_id="semantic_node")
    channel = GhostChannel(config, ["researcher", "architect"])

    # 复杂状态
    state = {
        "decisions": [
            {"type": "decision", "content": "Choose microservices architecture"},
            {"type": "decision", "content": "Use PostgreSQL for data"},
        ],
        "notes": [
            {"type": "note", "content": "Team meeting scheduled"},
            {"type": "note", "content": "Budget review needed"},
        ],
        "code": [
            {"file": "main.py", "lines": 100},
            {"file": "utils.py", "lines": 50},
        ],
    }

    # 使用语义过滤 - 仅同步与"decision"相关的内容
    result = await channel.sync_memory_delta(
        source_role="researcher",
        target_role="architect",
        memory_snapshot=state,
        semantic_filter_query="decision architecture",
    )

    print(f"  成功: {result.success}")
    print(f"  带宽降低: {result.bandwidth_reduction * 100:.1f}%")


async def workflow_example():
    """工作流示例"""
    print("\n" + "=" * 50)
    print("Ghost Channel - 工作流同步示例")
    print("=" * 50)

    config = SyncConfig(node_id="workflow_node")
    channel = GhostChannel(config, ["workflow"])

    # 创建简单工作流
    steps = [
        "initialize",
        "analyze",
        "design",
        "implement",
        "test",
        "deploy",
    ]

    state = {"status": "starting", "steps": []}

    for step in steps:
        state["steps"].append(step)
        state["current"] = step

        result = await channel.sync_workflow_state(
            workflow_id="project_wf",
            step_id=step,
            step_state=state,
            dependencies=[steps[steps.index(step) - 1]]
            if steps.index(step) > 0
            else [],
        )

        print(f"  步骤: {step} | 成功: {result.success}")

    print(f"\n最终统计: {channel.get_stats()}")


async def main():
    """主函数"""
    await basic_sync_example()
    await semantic_filter_example()
    await workflow_example()

    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
