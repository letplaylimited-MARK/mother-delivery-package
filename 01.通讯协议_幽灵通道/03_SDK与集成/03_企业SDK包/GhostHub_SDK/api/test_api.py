"""
Ghost Hub API 测试脚本
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"


class APIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint: str, params: Optional[dict] = None):
        response = self.session.get(f"{self.base_url}{endpoint}", params=params)
        return response.json()

    def post(self, endpoint: str, data: dict = None):
        response = self.session.post(f"{self.base_url}{endpoint}", json=data)
        return response.json()


def test_health(client: APIClient):
    print("\n[1] 健康检查")
    result = client.get("/health")
    print(f"状态: {result['status']}")
    print(f"时间: {result['timestamp']}")
    assert result["status"] == "healthy"
    print("✓ 通过")


def test_list_templates(client: APIClient):
    print("\n[2] 列出模板")
    result = client.get("/api/v1/templates")
    print(f"模板数量: {result['count']}")
    for tpl in result["templates"][:3]:
        print(f"  - {tpl['name']} ({tpl['domain']})")
    assert result["success"] is True
    print("✓ 通过")


def test_match_intent(client: APIClient):
    print("\n[3] 意图匹配")

    test_intents = [
        "帮我优化面试流程",
        "打开客厅灯",
        "分析成本结构",
    ]

    for intent in test_intents:
        result = client.post("/api/v1/intent/match", {"text": intent})
        if result.get("has_match"):
            match = result["match"]
            print(f"  '{intent}' -> {match['template_name']} ({match['similarity']:.2f})")
        else:
            print(f"  '{intent}' -> 无匹配")

    print("✓ 通过")


def test_workflow_execute(client: APIClient):
    print("\n[4] 执行工作流")
    result = client.post(
        "/api/v1/workflow/execute",
        {"intent_text": "帮我优化面试流程", "workflow_type": "hr_optimization"},
    )

    workflow = result.get("workflow", {})
    print(f"成功: {workflow.get('success')}")
    if workflow.get("intent_match"):
        print(f"匹配: {workflow['intent_match'].get('template_name')}")
    if workflow.get("task_graph"):
        print(f"任务数: {workflow['task_graph'].get('task_count')}")

    print("✓ 通过")


def test_devices(client: APIClient):
    print("\n[5] 设备管理")

    result = client.get("/api/v1/devices")
    print(f"设备数量: {result['count']}")
    for dev in result["devices"]:
        print(f"  - {dev['name']} ({dev['type']}) [{dev['status']}]")

    print("✓ 通过")


def test_device_command(client: APIClient):
    print("\n[6] 发送设备命令")
    result = client.post("/api/v1/devices/command", {"device_id": "dev_001", "command": "turn_on"})

    print(f"成功: {result['success']}")
    print(f"消息: {result['message']}")

    print("✓ 通过")


def test_scenes(client: APIClient):
    print("\n[7] 场景管理")

    result = client.get("/api/v1/scenes")
    print(f"场景数量: {result['count']}")
    for scene in result["scenes"]:
        print(f"  - {scene['name']}: {scene['description']}")

    print("✓ 通过")


def test_agents(client: APIClient):
    print("\n[8] 智能体列表")

    result = client.get("/api/v1/agents")
    print(f"智能体数量: {result['count']}")
    for agent in result["agents"]:
        print(f"  - {agent['name']} [{agent['status']}]")

    print("✓ 通过")


def test_find_agent(client: APIClient):
    print("\n[9] 查找智能体")

    intents = ["数据分析", "文档处理", "代码开发"]
    for intent in intents:
        result = client.get("/api/v1/agents/find", {"intent": intent})
        if result.get("success"):
            agent = result["agent"]
            print(f"  '{intent}' -> {agent['name']}")
        else:
            print(f"  '{intent}' -> 未找到")

    print("✓ 通过")


def test_intent_to_command(client: APIClient):
    print("\n[10] 意图转命令")

    intents = [
        ("打开客厅灯", "light"),
        ("空调调到25度", "thermostat"),
    ]

    for intent, dtype in intents:
        result = client.get("/api/v1/intent/to-command", {"intent": intent, "device_type": dtype})
        print(f"  '{intent}' -> {result['command']}")

    print("✓ 通过")


def test_stats(client: APIClient):
    print("\n[11] 系统统计")
    result = client.get("/api/v1/stats")
    print(json.dumps(result["stats"], indent=2, ensure_ascii=False))
    print("✓ 通过")


def run_all_tests():
    print("=" * 60)
    print(" Ghost Hub API 测试")
    print("=" * 60)

    client = APIClient()

    try:
        test_health(client)
        test_list_templates(client)
        test_match_intent(client)
        test_workflow_execute(client)
        test_devices(client)
        test_device_command(client)
        test_scenes(client)
        test_agents(client)
        test_find_agent(client)
        test_intent_to_command(client)
        test_stats(client)

        print("\n" + "=" * 60)
        print(" 全部测试通过!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n⚠ 无法连接到API服务器")
        print("请先启动服务器: python -m ghost_hub_sdk.api.main")
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")


if __name__ == "__main__":
    run_all_tests()
