"""
Ghost Hub SDK 完整验证测试
沙盒环境 - 用户场景实际运行

验证日期: 2026-04-15
验证轮次: 第2轮 - 实际运行
"""

import sys

sys.path.insert(
    0,
    r"GhostHub_Complete_Package\03_企业SDK包\GhostHub_SDK",
)

from ghost_hub_sdk import GhostHubSDK
from ghost_hub_sdk.components.agent_federation import Task
import traceback


def test_result(title, passed, details=""):
    status = "PASS" if passed else "FAIL"
    print(f"\n{'=' * 60}")
    print(f"[{status}] {title}")
    if details:
        print(f"Details: {details}")
    print(f"{'=' * 60}")
    return passed


def run_all_tests():
    print("\n" + "=" * 70)
    print("Ghost Hub SDK 完整验证测试")
    print("=" * 70)

    results = []
    sdk = None

    try:
        # ============================================================
        # 测试1: SDK初始化
        # ============================================================
        print("\n[TEST 1] SDK初始化")
        try:
            sdk = GhostHubSDK()
            results.append(
                test_result("SDK初始化", True, f"版本: {sdk.config.version}")
            )
        except Exception as e:
            results.append(test_result("SDK初始化", False, str(e)))
            return results

        # ============================================================
        # 测试2: 意图银行 - 基础匹配
        # ============================================================
        print("\n[TEST 2] 意图银行 - 基础匹配")
        try:
            result = sdk.intention_bank.match_intent("招聘Python工程师")
            has_match = result.has_match
            if has_match:
                template_name = result.top_match.template.name
                confidence = result.top_match.confidence
                results.append(
                    test_result(
                        "意图匹配 - 招聘场景",
                        True,
                        f"模板: {template_name}, 置信度: {confidence:.2f}",
                    )
                )
            else:
                results.append(
                    test_result("意图匹配 - 招聘场景", False, "未找到匹配模板")
                )
        except Exception as e:
            results.append(test_result("意图匹配 - 招聘场景", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试3: 工作流执行
        # ============================================================
        print("\n[TEST 3] 工作流执行")
        try:
            result = sdk.execute_workflow("招聘流程")
            success = result.get("success", False)
            workflow_type = result.get("workflow_type", "unknown")
            task_count = result.get("task_graph", {}).get("task_count", 0)

            if success:
                results.append(
                    test_result(
                        "工作流执行 - 招聘流程",
                        True,
                        f"类型: {workflow_type}, 任务数: {task_count}",
                    )
                )
            else:
                errors = result.get("errors", [])
                results.append(
                    test_result("工作流执行 - 招聘流程", False, f"错误: {errors}")
                )
        except Exception as e:
            results.append(test_result("工作流执行 - 招聘流程", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试4: IoT适配器 - 命令转换
        # ============================================================
        print("\n[TEST 4] IoT适配器 - 命令转换")
        try:
            command = sdk.no_ui_adapter.convert_intent_to_command(
                intent="把客厅灯打开", device_type="light"
            )
            is_string = isinstance(command, str)
            has_value = bool(command)

            results.append(
                test_result(
                    "IoT命令转换 - 灯光控制",
                    is_string and has_value,
                    f"命令: {command}",
                )
            )
        except Exception as e:
            results.append(test_result("IoT命令转换 - 灯光控制", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试5: IoT设备列表
        # ============================================================
        print("\n[TEST 5] IoT设备列表")
        try:
            devices = sdk.no_ui_adapter.list_devices()
            is_list = isinstance(devices, list)

            results.append(
                test_result(
                    "IoT设备列表", is_list, f"设备数: {len(devices) if is_list else 0}"
                )
            )
        except Exception as e:
            results.append(test_result("IoT设备列表", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试6: Agent联邦 - 任务分发
        # ============================================================
        print("\n[TEST 6] Agent联邦 - 任务分发")
        try:
            sdk.agent_federation.connect()

            task = Task(task_id="test_001", description="分析销售数据", priority=1)
            result = sdk.agent_federation.distribute_task(task=task, intent="数据分析")

            is_success = result.success
            has_agent = bool(result.assigned_agent)

            results.append(
                test_result(
                    "Agent任务分发",
                    is_success and has_agent,
                    f"分配给: {result.assigned_agent}, 成功: {is_success}",
                )
            )
        except Exception as e:
            results.append(test_result("Agent任务分发", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试7: Agent联邦 - 统计信息
        # ============================================================
        print("\n[TEST 7] Agent联邦 - 统计信息")
        try:
            stats = sdk.agent_federation.get_stats()

            has_stats = "total_agents" in stats
            online_agents = stats.get("online_agents", 0)

            results.append(
                test_result(
                    "Agent统计信息",
                    has_stats,
                    f"总Agent: {stats.get('total_agents', 0)}, 在线: {online_agents}",
                )
            )
        except Exception as e:
            results.append(test_result("Agent统计信息", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试8: 模板列表
        # ============================================================
        print("\n[TEST 8] 模板列表")
        try:
            templates = sdk.intention_bank.list_templates()
            is_list = isinstance(templates, list)
            count = len(templates) if is_list else 0

            results.append(
                test_result("模板列表", is_list and count > 0, f"模板数: {count}")
            )
        except Exception as e:
            results.append(test_result("模板列表", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试9: 领域过滤
        # ============================================================
        print("\n[TEST 9] 领域过滤")
        try:
            hr_templates = sdk.intention_bank.list_templates(domain="hr")
            is_list = isinstance(hr_templates, list)

            results.append(
                test_result(
                    "领域过滤 - HR",
                    is_list,
                    f"HR模板数: {len(hr_templates) if is_list else 0}",
                )
            )
        except Exception as e:
            results.append(test_result("领域过滤 - HR", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试10: 任务图构建
        # ============================================================
        print("\n[TEST 10] 任务图构建")
        try:
            match_result = sdk.intention_bank.match_intent("招聘")
            if match_result.has_match:
                template = match_result.top_match.template
                task_graph = sdk.intention_bank.build_task_graph(template)

                has_nodes = hasattr(task_graph, "nodes")
                node_count = len(task_graph.nodes) if has_nodes else 0

                results.append(
                    test_result(
                        "任务图构建",
                        has_nodes and node_count > 0,
                        f"节点数: {node_count}",
                    )
                )
            else:
                results.append(test_result("任务图构建", False, "无匹配模板"))
        except Exception as e:
            results.append(test_result("任务图构建", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试11: 工单处理
        # ============================================================
        print("\n[TEST 11] 工单处理")
        try:
            result = sdk.execute_workflow("服务器磁盘满了")
            success = result.get("success", False)

            results.append(test_result("工单处理", success, f"成功: {success}"))
        except Exception as e:
            results.append(test_result("工单处理", False, str(e)))
            traceback.print_exc()

        # ============================================================
        # 测试12: 智能家居场景
        # ============================================================
        print("\n[TEST 12] 智能家居场景")
        try:
            commands = []
            for intent, device_type in [
                ("开灯", "light"),
                ("关灯", "light"),
                ("空调26度", "ac"),
            ]:
                cmd = sdk.no_ui_adapter.convert_intent_to_command(intent, device_type)
                commands.append(cmd)

            all_valid = all(isinstance(c, str) and c for c in commands)

            results.append(test_result("智能家居场景", all_valid, f"命令: {commands}"))
        except Exception as e:
            results.append(test_result("智能家居场景", False, str(e)))
            traceback.print_exc()

    finally:
        if sdk:
            try:
                sdk.disconnect()
                print("\n[INFO] SDK连接已关闭")
            except:
                pass

    # ============================================================
    # 总结
    # ============================================================
    print("\n" + "=" * 70)
    print("验证总结")
    print("=" * 70)

    passed = sum(1 for r in results if r)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    print(f"\n总测试数: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    print(f"通过率: {percentage:.1f}%")

    if passed == total:
        print("\n🎉 所有测试通过!")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，需要修复")

    return results


if __name__ == "__main__":
    run_all_tests()
