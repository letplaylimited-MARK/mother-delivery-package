"""
Ghost Hub SDK Complete Validation Test
Sandbox Environment - User Scenario Execution
"""

import sys

sys.path.insert(
    0,
    r"GhostHub_Complete_Package\03_企业SDK包\GhostHub_SDK",
)

from ghost_hub_sdk import GhostHubSDK
from ghost_hub_sdk.components.agent_federation import Task
import traceback

results = []
sdk = None
output = []


def add_result(title, passed, details=""):
    status = "PASS" if passed else "FAIL"
    line = f"\n{'=' * 60}\n[{status}] {title}\nDetails: {details}\n{'=' * 60}"
    output.append(line)
    results.append(passed)
    return passed


def run_all_tests():
    global sdk
    output.append("\n" + "=" * 70)
    output.append("Ghost Hub SDK Complete Validation Test")
    output.append("=" * 70)

    try:
        # TEST 1: SDK Init
        output.append("\n[TEST 1] SDK Init")
        try:
            sdk = GhostHubSDK()
            add_result("SDK Init", True, f"Version: {sdk.config.version}")
        except Exception as e:
            add_result("SDK Init", False, str(e))
            return results

        # TEST 2: Intention Match
        output.append("\n[TEST 2] Intention Match")
        try:
            result = sdk.intention_bank.match_intent("Recruit Python Engineer")
            has_match = result.has_match
            if has_match:
                template_name = result.top_match.template.name
                confidence = result.top_match.confidence
                add_result(
                    "Intent Match - Recruit",
                    True,
                    f"Template: {template_name}, Confidence: {confidence:.2f}",
                )
            else:
                add_result("Intent Match - Recruit", False, "No match found")
        except Exception as e:
            add_result("Intent Match - Recruit", False, str(e))
            traceback.print_exc()

        # TEST 3: Workflow Execute
        output.append("\n[TEST 3] Workflow Execute")
        try:
            result = sdk.execute_workflow("Recruitment Process")
            success = result.get("success", False)
            workflow_type = result.get("workflow_type", "unknown")
            task_count = result.get("task_graph", {}).get("task_count", 0)
            add_result(
                "Workflow Execute",
                success,
                f"Type: {workflow_type}, Tasks: {task_count}",
            )
        except Exception as e:
            add_result("Workflow Execute", False, str(e))

        # TEST 4: IoT Command Convert
        output.append("\n[TEST 4] IoT Command Convert")
        try:
            command = sdk.no_ui_adapter.convert_intent_to_command(
                intent="Turn on the living room light", device_type="light"
            )
            is_string = isinstance(command, str)
            add_result("IoT Command Convert", is_string, f"Command: {command}")
        except Exception as e:
            add_result("IoT Command Convert", False, str(e))

        # TEST 5: IoT Device List
        output.append("\n[TEST 5] IoT Device List")
        try:
            devices = sdk.no_ui_adapter.list_devices()
            is_list = isinstance(devices, list)
            add_result(
                "IoT Device List",
                is_list,
                f"Device count: {len(devices) if is_list else 0}",
            )
        except Exception as e:
            add_result("IoT Device List", False, str(e))

        # TEST 6: Agent Task Distribution
        output.append("\n[TEST 6] Agent Task Distribution")
        try:
            sdk.agent_federation.connect()
            task = Task(
                task_id="test_001", description="Analyze sales data", priority=1
            )
            result = sdk.agent_federation.distribute_task(
                task=task, intent="Data Analysis"
            )
            is_success = result.success
            add_result(
                "Agent Task Distribution",
                is_success,
                f"Assigned to: {result.assigned_agent}",
            )
        except Exception as e:
            add_result("Agent Task Distribution", False, str(e))

        # TEST 7: Agent Stats
        output.append("\n[TEST 7] Agent Stats")
        try:
            stats = sdk.agent_federation.get_stats()
            has_stats = "total_agents" in stats
            add_result(
                "Agent Stats",
                has_stats,
                f"Total: {stats.get('total_agents', 0)}, Online: {stats.get('online_agents', 0)}",
            )
        except Exception as e:
            add_result("Agent Stats", False, str(e))

        # TEST 8: Template List
        output.append("\n[TEST 8] Template List")
        try:
            templates = sdk.intention_bank.list_templates()
            is_list = isinstance(templates, list)
            add_result(
                "Template List",
                is_list and len(templates) > 0,
                f"Template count: {len(templates) if is_list else 0}",
            )
        except Exception as e:
            add_result("Template List", False, str(e))

        # TEST 9: Domain Filter
        output.append("\n[TEST 9] Domain Filter")
        try:
            hr_templates = sdk.intention_bank.list_templates(domain="hr")
            is_list = isinstance(hr_templates, list)
            add_result(
                "Domain Filter - HR",
                is_list,
                f"HR Templates: {len(hr_templates) if is_list else 0}",
            )
        except Exception as e:
            add_result("Domain Filter - HR", False, str(e))

        # TEST 10: Task Graph Build
        output.append("\n[TEST 10] Task Graph Build")
        try:
            match_result = sdk.intention_bank.match_intent("Recruit")
            if match_result.has_match:
                template = match_result.top_match.template
                task_graph = sdk.intention_bank.build_task_graph(template)
                has_nodes = hasattr(task_graph, "nodes")
                add_result(
                    "Task Graph Build",
                    has_nodes,
                    f"Nodes: {len(task_graph.nodes) if has_nodes else 0}",
                )
            else:
                add_result("Task Graph Build", False, "No match")
        except Exception as e:
            add_result("Task Graph Build", False, str(e))

        # TEST 11: Ticket Processing
        output.append("\n[TEST 11] Ticket Processing")
        try:
            result = sdk.execute_workflow("Server disk is full")
            success = result.get("success", False)
            add_result("Ticket Processing", success, f"Success: {success}")
        except Exception as e:
            add_result("Ticket Processing", False, str(e))

        # TEST 12: Smart Home Scenario
        output.append("\n[TEST 12] Smart Home Scenario")
        try:
            commands = []
            for intent, device_type in [
                ("Turn on light", "light"),
                ("Turn off light", "light"),
                ("Set AC to 26", "ac"),
            ]:
                cmd = sdk.no_ui_adapter.convert_intent_to_command(intent, device_type)
                commands.append(cmd)
            all_valid = all(isinstance(c, str) and c for c in commands)
            add_result("Smart Home Scenario", all_valid, f"Commands: {commands}")
        except Exception as e:
            add_result("Smart Home Scenario", False, str(e))

    finally:
        if sdk:
            try:
                sdk.disconnect()
            except:
                pass

    # Summary
    passed = sum(1 for r in results if r)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0

    output.append("\n" + "=" * 70)
    output.append("VALIDATION SUMMARY")
    output.append("=" * 70)
    output.append(f"\nTotal Tests: {total}")
    output.append(f"Passed: {passed}")
    output.append(f"Failed: {total - passed}")
    output.append(f"Pass Rate: {percentage:.1f}%")

    if passed == total:
        output.append("\nALL TESTS PASSED!")
    else:
        output.append(f"\nWARNING: {total - passed} tests failed, need fixes")

    return results


if __name__ == "__main__":
    run_all_tests()

    # Write to file
    with open(
        r"GhostHub_Complete_Package\验证\test_results.txt",
        "w",
        encoding="utf-8",
    ) as f:
        f.write("\n".join(output))

    print("\nResults written to test_results.txt")
