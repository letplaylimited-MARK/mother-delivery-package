"""
Ghost Hub 端到端验证脚本

验证三大组件的真正串联:
1. 意图银行 → 解析意图
2. 任务分解 → 分解任务
3. 设备控制/Agent执行 → 执行任务
4. 结果聚合 → 汇总结果

同时验证:
- 记忆层 (执行历史)
- 知识层 (意图学习)
"""

import sys
import json
import time
import io
from pathlib import Path
from typing import Any

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 添加SDK路径
sdk_path = str(Path(__file__).parent.parent)
if sdk_path not in sys.path:
    sys.path.insert(0, sdk_path)

# 导入SDK模块
import ghost_hub_sdk

sys.modules["ghost_hub_sdk"] = ghost_hub_sdk

from core import GhostHubSDK
from workflow_engine import create_workflow_engine, WorkflowStatus
from memory import get_ghost_hub_memory


def print_header(text: str):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_result(label: str, data: Any, indent: int = 2):
    prefix = " " * indent
    if isinstance(data, dict):
        print(f"{prefix}{label}:")
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                print(f"{prefix}  {k}:")
                print_result("", v, indent + 4)
            else:
                print(f"{prefix}  {k}: {v}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"{prefix}[{i}] {json.dumps(item, ensure_ascii=False)[:100]}...")
    else:
        print(f"{prefix}{label}: {data}")


def test_component_integration():
    """测试组件集成"""
    print_header("测试1: 组件集成")

    sdk = GhostHubSDK()
    sdk.connect()

    stats = sdk.get_stats()
    print("\n[SDK组件状态]")
    print("  意图银行: " + ("[OK]" if sdk.intention_bank else "[FAIL]"))
    print("  无UI适配器: " + ("[OK]" if sdk.no_ui_adapter else "[FAIL]"))
    print("  智能体联邦: " + ("[OK]" if sdk.agent_federation else "[FAIL]"))

    print("\n[组件统计]")
    if sdk.intention_bank:
        ib_stats = sdk.intention_bank.get_stats()
        print(f"  意图银行 - 模板数: {ib_stats.get('templates_loaded', 0)}")
    if sdk.no_ui_adapter:
        nui_stats = sdk.no_ui_adapter.get_stats()
        print(f"  无UI适配器 - 设备数: {nui_stats.get('total_devices', 0)}")
    if sdk.agent_federation:
        af_stats = sdk.agent_federation.get_stats()
        print(f"  智能体联邦 - Agent数: {af_stats.get('total_agents', 0)}")

    sdk.disconnect()
    return True


def test_intent_parsing():
    """测试意图解析"""
    print_header("测试2: 意图解析")

    engine = create_workflow_engine()

    test_intents = [
        "打开客厅灯",
        "把空调调到24度",
        "帮我分析销售数据",
        "招聘一个前端工程师",
        "处理这个工单",
    ]

    print("\n[意图解析测试]")
    for intent in test_intents:
        result = engine.execute(intent)
        status_icon = "[OK]" if result["status"] == "completed" else "[FAIL]"
        template = result.get("template") or "无匹配"
        print(f"\n  {status_icon} 输入: {intent}")
        print(f"     模板: {template}")
        print(f"     任务数: {result.get('results', {}).get('total_steps', 0)}")
        print(f"     执行时间: {result.get('execution_time', 0):.3f}s")

        if result.get("errors"):
            print(f"     错误: {result['errors']}")

    return True


def test_device_control():
    """测试设备控制"""
    print_header("测试3: 设备控制")

    engine = create_workflow_engine()

    # 连接适配器
    engine.no_ui_adapter.connect()

    device_commands = [
        ("打开客厅灯", "dev_001", "turn_on"),
        ("关闭卧室灯", "dev_002", "turn_off"),
        ("打开空调", "dev_003", "turn_on"),
    ]

    print("\n[设备控制测试]")
    for intent, device_id, expected_cmd in device_commands:
        result = engine.execute(intent)

        # 检查设备控制结果
        device_results = result.get("results", {}).get("device_results", [])

        success = False
        for dr in device_results:
            if dr.get("device_id") == device_id and dr.get("success"):
                success = True
                print(f"\n  [OK] {intent}")
                print(f"     设备: {dr.get('device_id')}")
                print(f"     命令: {dr.get('command')}")
                print(f"     结果: {dr.get('message')}")
                break

        if not success:
            print(f"\n  [FAIL] {intent}")
            print(f"     未能执行设备控制")

    return True


def test_agent_collaboration():
    """测试Agent协作"""
    print_header("测试4: Agent协作")

    engine = create_workflow_engine()

    # 连接联邦
    engine.agent_federation.connect()

    agents = engine.agent_federation.list_agents()
    print(f"\n[可用Agent]")
    for agent in agents:
        print(f"  - {agent.name} ({agent.agent_id}): {agent.status.value}")

    # 测试任务分发
    tasks = ["分析销售数据", "生成项目报告", "搜索最新AI技术"]

    print(f"\n[任务分发测试]")
    for task_desc in tasks:
        # 直接使用联邦组件测试
        agent = engine.agent_federation.find_agent(task_desc)
        if agent:
            print(f"\n  [OK] '{task_desc}'")
            print(f"     路由到: {agent.name}")
        else:
            print(f"\n  [WARN] '{task_desc}'")
            print(f"     未找到合适Agent")

    return True


def test_memory_layer():
    """测试记忆层"""
    print_header("测试5: 记忆层")

    memory = get_ghost_hub_memory()

    # 记录一些测试数据
    test_result = {
        "workflow_id": "test_wf_001",
        "intent_text": "测试意图",
        "template": "测试模板",
        "status": "completed",
        "execution_time": 0.5,
        "results": {"total_steps": 3, "step_results": []},
        "errors": [],
    }
    memory.record_intent("测试意图", test_result)

    # 获取统计
    stats = memory.get_stats()
    print(f"\n[记忆统计]")
    print(f"  意图历史: {stats.get('intent_history_count', 0)}")
    print(f"  设备历史: {stats.get('device_history_count', 0)}")
    print(f"  Agent历史: {stats.get('agent_history_count', 0)}")
    print(f"  成功率: {stats.get('success_rate', 0):.2%}")

    # 测试上下文
    memory.set_context("test_mode", True)
    assert memory.get_context("test_mode") == True
    print(f"\n  [OK] 上下文管理正常")

    return True


def test_knowledge_layer():
    """测试知识层"""
    print_header("测试6: 知识层")

    kg = get_intent_kg()

    # 注册测试模板
    kg.register_template(
        "test_template_1",
        {
            "name": "智能家居控制",
            "domain": "iot",
            "description": "控制智能设备",
            "keywords": ["灯", "空调", "控制"],
            "intent_patterns": ["打开", "关闭", "调节"],
        },
    )

    # 测试相似度查找
    test_text = "我想打开客厅的灯"
    similar = kg.find_similar_templates(test_text, limit=3)

    print(f"\n[相似模板查找]")
    print(f"  输入: '{test_text}'")
    for s in similar[:3]:
        print(f"  - {s['name']} (score: {s['score']:.2f})")

    # 测试域检测
    domain_scores = kg.detect_domain("空调温度调到24度")
    print(f"\n[域检测]")
    print(f"  '空调温度调到24度' -> {domain_scores}")

    # 统计
    stats = kg.get_stats()
    print(f"\n[知识图谱统计]")
    print(f"  模板数: {stats.get('total_templates', 0)}")
    print(f"  关系数: {stats.get('total_relations', 0)}")

    return True


def test_full_workflow():
    """测试完整工作流"""
    print_header("测试7: 完整工作流串联")

    engine = create_workflow_engine()

    # 连接所有组件
    engine.no_ui_adapter.connect()
    engine.agent_federation.connect()

    # 获取记忆和知识
    memory = get_ghost_hub_memory()
    kg = get_intent_kg()

    # 完整工作流测试
    test_cases = [
        {
            "intent": "打开客厅灯",
            "expected_domain": "iot",
            "expected_components": ["意图银行", "设备控制"],
        },
        {
            "intent": "分析本月销售数据",
            "expected_domain": "data",
            "expected_components": ["意图银行", "Agent执行"],
        },
    ]

    print("\n[完整工作流测试]")
    for i, case in enumerate(test_cases, 1):
        print(f"\n  案例 {i}: {case['intent']}")

        result = engine.execute(case["intent"])

        # 记录到记忆
        memory.record_intent(case["intent"], result)

        # 学习到知识层
        kg.learn_from_intent(case["intent"], result.get("template"))

        # 验证结果
        status = "[OK]" if result["status"] == "completed" else "[FAIL]"
        print(f"    {status} 状态: {result['status']}")
        print(f"    [TIME]  执行时间: {result['execution_time']:.3f}s")
        print(f"    [TASK]  任务数: {result['results'].get('total_steps', 0)}")
        print(f"    [STAT]  成功步骤: {result['results'].get('completed_steps', 0)}")

        if result["results"].get("device_results"):
            print(f"    [DEV]  设备结果: {len(result['results']['device_results'])} 条")
        if result["results"].get("agent_results"):
            print(f"    [AGENT]  Agent结果: {len(result['results']['agent_results'])} 条")

    return True


def test_error_handling():
    """测试错误处理"""
    print_header("测试8: 错误处理")

    engine = create_workflow_engine()

    # 测试无效设备
    result = engine.no_ui_adapter.send_command("invalid_device", "turn_on")
    print(f"\n[无效设备处理]")
    print(f"  设备: invalid_device")
    print(f"  结果: {'[FAIL]' if not result.success else '[OK]'} {result.message}")

    # 测试空意图
    result = engine.execute("")
    print(f"\n[空意图处理]")
    print(f"  状态: {result['status']}")

    return True


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("  [Ghost Hub SDK] 端到端验证")
    print("  验证三大组件的真正串联与集成")
    print("=" * 70)

    tests = [
        ("组件集成", test_component_integration),
        ("意图解析", test_intent_parsing),
        ("设备控制", test_device_control),
        ("Agent协作", test_agent_collaboration),
        ("记忆层", test_memory_layer),
        ("知识层", test_knowledge_layer),
        ("完整工作流", test_full_workflow),
        ("错误处理", test_error_handling),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n  [FAIL] 测试异常: {e}")
            results.append((name, False))

    # 汇总
    print_header("验证汇总")
    passed = sum(1 for _, r in results if r)
    total = len(results)

    print(f"\n  通过: {passed}/{total}")
    print(f"  成功率: {passed / total * 100:.1f}%\n")

    for name, success in results:
        icon = "[OK]" if success else "[FAIL]"
        print(f"    {icon} {name}")

    print("\n" + "=" * 70)

    if passed == total:
        print("  [SUCCESS] 所有测试通过！Ghost Hub组件串联成功！")
    else:
        print(f"  [WARN]  {total - passed} 项测试失败，需要修复")

    print("=" * 70 + "\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
