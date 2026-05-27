"""
Ghost Hub SDK 集成测试
测试组件间协作和完整工作流
"""

import sys
import time
import json
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ghost_hub_sdk import GhostHubSDK, GhostHubConfig
from ghost_hub_sdk.components.intention_bank import (
    IntentionBankComponent,
    IntentParser,
    Template,
    Task,
    IntentVector,
)
from ghost_hub_sdk.components.no_ui_adapter import (
    NoUIAdapterComponent,
    Device,
    DeviceType,
    DeviceProtocol,
    Scene,
)
from ghost_hub_sdk.components.agent_federation import (
    AgentFederationComponent,
    Agent,
    AgentStatus,
    RoutingStrategy,
    Task as FedTask,
)


class TestIntentionBankIntegration:
    """意图银行集成测试"""

    def test_intent_matching_pipeline(self):
        """测试意图匹配管道"""
        component = IntentionBankComponent()
        result = component.match_intent("帮我优化招聘面试流程")

        assert result is not None
        assert isinstance(result.matches, list)
        assert result.has_match or len(result.matches) >= 0

    def test_multi_intent_parsing(self):
        """测试多意图解析"""
        component = IntentionBankComponent()
        result = component.match_multi_intent("打开灯并且优化面试流程")

        assert result is not None
        assert len(result.intents) >= 1

    def test_task_graph_construction(self):
        """测试任务图构建"""
        component = IntentionBankComponent()
        templates = component.list_templates()

        if templates:
            template = templates[0]
            graph = component.build_task_graph(template)

            assert graph is not None
            assert len(graph.nodes) > 0
            assert len(graph.execution_order) > 0

    def test_template_domain_filtering(self):
        """测试模板领域过滤"""
        component = IntentionBankComponent()

        hr_templates = component.list_templates(domain="hr")
        iot_templates = component.list_templates(domain="iot")

        for tpl in hr_templates:
            assert tpl.domain == "hr"

        for tpl in iot_templates:
            assert tpl.domain == "iot"


class TestNoUIAdapterIntegration:
    """无UI适配器集成测试"""

    def test_device_lifecycle(self):
        """测试设备生命周期"""
        component = NoUIAdapterComponent()

        initial_count = len(component.list_devices())
        device = Device(
            id="test_device",
            name="Test Device",
            device_type=DeviceType.SWITCH,
            protocol=DeviceProtocol.HTTP,
            address="192.168.1.200",
        )

        component.add_device(device)
        assert len(component.list_devices()) == initial_count + 1

        component.remove_device("test_device")
        assert len(component.list_devices()) == initial_count

    def test_protocol_adapters(self):
        """测试协议适配器"""
        component = NoUIAdapterComponent()

        http_ok = component.connect(protocol="http")
        assert http_ok is True

        component.disconnect()

        mqtt_ok = component.connect(protocol="mqtt")
        assert mqtt_ok is True

        component.disconnect()

    def test_batch_command_execution(self):
        """测试批量命令执行"""
        component = NoUIAdapterComponent()
        component.connect()

        commands = [
            {"device_id": "dev_001", "command": "turn_on"},
            {"device_id": "dev_002", "command": "turn_on"},
            {"device_id": "dev_003", "command": "turn_on"},
        ]

        result = component.send_batch_commands(commands)

        assert result.total == 3
        assert result.success_count + result.failed_count == 3

    def test_scene_execution(self):
        """测试场景执行"""
        component = NoUIAdapterComponent()
        component.connect()

        result = component.execute_scene("scene_morning")

        assert result is not None
        assert result.total > 0

    def test_intent_to_command_conversion(self):
        """测试意图到命令转换"""
        component = NoUIAdapterComponent()

        cmd1 = component.convert_intent_to_command("打开客厅灯", "light")
        assert "light" in cmd1

        cmd2 = component.convert_intent_to_command("空调调到25度", "thermostat")
        assert "thermostat" in cmd2

        cmd3 = component.convert_intent_to_command("关灯", "light")
        assert "light" in cmd3


class TestAgentFederationIntegration:
    """智能体联邦集成测试"""

    def test_agent_registration(self):
        """测试智能体注册"""
        component = AgentFederationComponent()

        agent = Agent(
            agent_id="integration_test_agent",
            name="Integration Test Agent",
            capabilities=["integration", "testing"],
            intent_keywords=["测试", "集成"],
        )

        result = component.register_agent(agent)
        assert result is True

        retrieved = component.find_agent("测试")
        assert retrieved is not None

    def test_routing_strategies(self):
        """测试路由策略"""
        strategies = [
            ("round_robin", RoutingStrategy.ROUND_ROBIN),
            ("least_load", RoutingStrategy.LEAST_LOAD),
            ("intent_match", RoutingStrategy.INTENT_MATCH),
            ("random", RoutingStrategy.RANDOM),
        ]

        for name, strategy in strategies:
            config = {"routing_strategy": name}
            component = AgentFederationComponent(config)
            component.connect()

            agent = component.find_agent("数据分析")
            assert agent is not None

    def test_task_distribution(self):
        """测试任务分发"""
        component = AgentFederationComponent()
        component.connect()

        tasks = [
            FedTask("t1", "分析销售数据", priority=1),
            FedTask("t2", "生成报告", priority=2),
            FedTask("t3", "发送通知", priority=1),
        ]

        results = component.distribute_tasks(tasks)

        assert len(results) == 3
        for result in results:
            assert result.success is True
            assert result.assigned_agent != ""

    def test_collaborative_session(self):
        """测试协作会话"""
        component = AgentFederationComponent()

        session = component.create_session(
            task="完成项目报告",
            participants=["data_agent", "doc_agent"],
        )

        assert session is not None
        assert len(session.participants) == 2
        assert session.status == "active"

    def test_message_broadcast(self):
        """测试消息广播"""
        component = AgentFederationComponent()
        component.connect()

        messages = component.broadcast("Test broadcast message")

        assert isinstance(messages, list)


class TestCrossComponentIntegration:
    """跨组件集成测试"""

    def test_intent_to_device_control(self):
        """测试意图到设备控制的完整链路"""
        intention_bank = IntentionBankComponent()
        no_ui_adapter = NoUIAdapterComponent()
        no_ui_adapter.connect()

        intent = "打开客厅灯"
        match_result = intention_bank.match_intent(intent)

        if match_result.has_match:
            command = no_ui_adapter.convert_intent_to_command(intent, "light")
            assert "light" in command

            result = no_ui_adapter.send_command("dev_001", command)
            assert result is not None

    def test_intent_to_agent_routing(self):
        """测试意图到智能体路由的完整链路"""
        intention_bank = IntentionBankComponent()
        federation = AgentFederationComponent()
        federation.connect()

        intent = "分析本月销售数据并生成报告"
        match_result = intention_bank.match_intent(intent)

        agent = federation.find_agent(intent)
        assert agent is not None

        if match_result.has_match:
            task = FedTask("generated_task", intent)
            dist_result = federation.distribute_task(task, intent)
            assert dist_result.success is True

    def test_multi_agent_task_flow(self):
        """测试多智能体任务流程"""
        federation = AgentFederationComponent()
        federation.connect()

        tasks = [
            FedTask("t1", "收集销售数据", priority=1),
            FedTask("t2", "数据分析", priority=2, dependencies=["t1"]),
            FedTask("t3", "生成可视化图表", priority=2, dependencies=["t2"]),
            FedTask("t4", "撰写报告", priority=3, dependencies=["t2", "t3"]),
        ]

        dist_results = federation.distribute_tasks(tasks)

        assert len(dist_results) == 4

        aggregated = federation.aggregate_results(tasks)
        assert aggregated.total_tasks == 4


class TestFullWorkflowIntegration:
    """完整工作流集成测试"""

    def test_hr_interview_workflow(self):
        """测试HR面试优化工作流"""
        config = GhostHubConfig()
        sdk = GhostHubSDK(config)

        result = sdk.execute_workflow("帮我优化面试流程", "hr_optimization")

        assert result is not None
        assert "intent_text" in result
        assert "success" in result
        assert result["intent_text"] == "帮我优化面试流程"

        if result["success"]:
            assert result.get("intent_match") is not None
            assert result.get("task_graph") is not None

    def test_iot_control_workflow(self):
        """测试IoT设备控制工作流"""
        config = GhostHubConfig()
        sdk = GhostHubSDK(config)

        result = sdk.execute_workflow("打开客厅灯并调空调到24度", "iot_control")

        assert result is not None
        assert "intent_text" in result

    def test_multi_domain_workflow(self):
        """测试多领域工作流"""
        config = GhostHubConfig()
        sdk = GhostHubSDK(config)

        test_cases = [
            ("优化招聘流程", "hr"),
            ("打开客厅灯", "iot"),
            ("处理客服工单", "ops"),
            ("分析成本结构", "finance"),
        ]

        for intent, expected_domain in test_cases:
            result = sdk.execute_workflow(intent)
            assert result["intent_text"] == intent

    def test_workflow_with_connections(self):
        """测试带连接的工作流"""
        config = GhostHubConfig(
            no_ui_adapter_enabled=True,
            agent_federation_enabled=True,
        )
        sdk = GhostHubSDK(config)

        results = sdk.connect()
        assert isinstance(results, dict)

        sdk.disconnect()


class TestEdgeCases:
    """边界情况测试"""

    def test_empty_intent(self):
        """测试空意图"""
        component = IntentionBankComponent()
        result = component.match_intent("")

        assert result is not None
        assert result.has_match is False

    def test_unknown_domain(self):
        """测试未知领域"""
        component = IntentionBankComponent()
        result = component.match_intent("xyz123 unknown intent abc")

        assert result is not None

    def test_device_not_found(self):
        """测试设备未找到"""
        component = NoUIAdapterComponent()
        component.connect()

        result = component.send_command("nonexistent_device", "turn_on")

        assert result.success is False
        assert result.error is not None

    def test_agent_not_found(self):
        """测试智能体未找到"""
        component = AgentFederationComponent()
        component.connect()

        message = component.send_message("nonexistent_agent", "test message")

        assert message is None

    def test_invalid_scene(self):
        """测试无效场景"""
        component = NoUIAdapterComponent()
        component.connect()

        result = component.execute_scene("nonexistent_scene")

        assert result.total == 0

    def test_no_templates(self):
        """测试无模板情况"""
        config = {"templates_dir": "/nonexistent/path"}
        component = IntentionBankComponent(config)

        templates = component.list_templates()

        assert isinstance(templates, list)


class TestPerformance:
    """性能测试"""

    def test_intent_matching_performance(self):
        """测试意图匹配性能"""
        component = IntentionBankComponent()

        start = time.time()
        for _ in range(100):
            component.match_intent("帮我优化面试流程")
        elapsed = time.time() - start

        assert elapsed < 5.0

    def test_batch_command_performance(self):
        """测试批量命令性能"""
        component = NoUIAdapterComponent()
        component.connect()

        commands = [{"device_id": "dev_001", "command": "turn_on"} for _ in range(50)]

        start = time.time()
        component.send_batch_commands(commands)
        elapsed = time.time() - start

        assert elapsed < 2.0

    def test_task_distribution_performance(self):
        """测试任务分发性能"""
        component = AgentFederationComponent()
        component.connect()

        tasks = [FedTask(f"t{i}", f"Task {i}") for i in range(100)]

        start = time.time()
        component.distribute_tasks(tasks)
        elapsed = time.time() - start

        assert elapsed < 3.0


class TestErrorHandling:
    """错误处理测试"""

    def test_invalid_device_type(self):
        """测试无效设备类型"""
        component = NoUIAdapterComponent()

        command = component.convert_intent_to_command("打开设备", "invalid_type")

        assert isinstance(command, str)

    def test_invalid_routing_strategy(self):
        """测试无效路由策略"""
        config = {"routing_strategy": "invalid_strategy"}
        component = AgentFederationComponent(config)

        component.connect()
        agent = component.find_agent("test")

        assert agent is not None

    def test_disconnected_send(self):
        """测试未连接时发送"""
        component = NoUIAdapterComponent()

        result = component.send_command("dev_001", "turn_on")

        assert result.success is False
        assert result.error is not None


def run_all_tests():
    """运行所有集成测试"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_all_tests()
