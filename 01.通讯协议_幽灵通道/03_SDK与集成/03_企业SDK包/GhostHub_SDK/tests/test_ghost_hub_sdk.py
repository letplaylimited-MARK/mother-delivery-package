"""
Ghost Hub SDK 统一测试
测试三大核心功能：意图银行、无UI适配器、智能体联邦
"""

import sys
import json
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ghost_hub_sdk import GhostHubSDK, GhostHubConfig
from ghost_hub_sdk.components.intention_bank import (
    IntentionBankComponent,
    IntentParser,
    IntentMatcher,
    TemplateLoader,
    IntentVector,
    TaskGraphBuilder,
    SemanticSimilarity,
    Task,
)
from ghost_hub_sdk.components.no_ui_adapter import (
    NoUIAdapterComponent,
    Device,
    DeviceCommand,
    DeviceType,
    DeviceProtocol,
    IntentCommandEngine,
    HTTPAdapter,
    MQTTAdapter,
    WebSocketAdapter,
    Scene,
    SceneManager,
    BatchCommandResult,
)
from ghost_hub_sdk.components.agent_federation import (
    AgentFederationComponent,
    Agent,
    Message,
    Session,
    AgentStatus,
    MessageType,
    RoutingStrategy,
    TaskDistributor,
    ResultAggregator,
    Task as FedTask,
    ServiceRegistry,
    Router,
)


class TestGhostHubConfig:
    def test_default_config(self):
        config = GhostHubConfig()
        assert config.name == "GhostHub"
        assert config.version == "1.0.0"

    def test_custom_config(self):
        config = GhostHubConfig(name="CustomHub", version="1.0.0")
        assert config.name == "CustomHub"
        assert config.version == "1.0.0"

    def test_config_to_dict(self):
        config = GhostHubConfig()
        data = config.to_dict()
        assert isinstance(data, dict)
        assert "name" in data


class TestGhostHubSDK:
    def test_sdk_init(self):
        config = GhostHubConfig()
        sdk = GhostHubSDK(config)
        assert sdk.config is not None

    def test_execute_workflow(self):
        config = GhostHubConfig()
        sdk = GhostHubSDK(config)
        result = sdk.execute_workflow("帮我优化面试流程")
        assert "intent_text" in result

    def test_connect_disconnect(self):
        config = GhostHubConfig()
        sdk = GhostHubSDK(config)
        results = sdk.connect()
        assert isinstance(results, dict)
        sdk.disconnect()


class TestSemanticSimilarity:
    def test_tokenize(self):
        sem = SemanticSimilarity()
        tokens = sem.tokenize("帮我优化面试流程")
        assert isinstance(tokens, list)

    def test_similarity(self):
        sem = SemanticSimilarity()
        score = sem.similarity("优化面试流程", "面试流程优化")
        assert 0 <= score <= 1


class TestIntentParser:
    def test_parse_hr_domain(self):
        parser = IntentParser()
        domain, confidence, vector = parser.parse("帮我优化面试流程")
        assert domain == "hr"

    def test_separate_intents(self):
        parser = IntentParser()
        intents = parser.separate_intents("打开灯并且关闭空调")
        assert len(intents) >= 2


class TestIntentMatcher:
    def test_match_templates(self):
        loader = TemplateLoader()
        templates = loader.load_all()
        matcher = IntentMatcher(threshold=0.3)
        result = matcher.match("帮我优化面试流程", templates)
        assert result is not None


class TestIntentionBankComponent:
    def test_component_init(self):
        config = {"match_threshold": 0.5}
        component = IntentionBankComponent(config)
        assert component.threshold == 0.5

    def test_match_intent(self):
        component = IntentionBankComponent()
        result = component.match_intent("帮我优化面试流程")
        assert result is not None

    def test_match_multi_intent(self):
        component = IntentionBankComponent()
        result = component.match_multi_intent("打开灯并且优化面试流程")
        assert result is not None

    def test_build_task_graph(self):
        component = IntentionBankComponent()
        templates = component.list_templates()
        if templates:
            graph = component.build_task_graph(templates[0])
            assert graph is not None


class TestTaskGraphBuilder:
    def test_build_graph(self):
        tasks = [
            Task(id="t1", name="Task 1", description="First task", sequence=1),
            Task(
                id="t2", name="Task 2", description="Second task", sequence=2, dependencies=["t1"]
            ),
            Task(id="t3", name="Task 3", description="Third task", sequence=3),
        ]
        builder = TaskGraphBuilder()
        graph = builder.build(tasks)
        assert len(graph.nodes) == 3
        assert len(graph.execution_order) >= 1


class TestIntentCommandEngine:
    def test_convert_light_on(self):
        engine = IntentCommandEngine()
        command = engine.convert("打开客厅灯", "light")
        assert "light" in command

    def test_convert_thermostat(self):
        engine = IntentCommandEngine()
        command = engine.convert("空调调到25度", "thermostat")
        assert "thermostat" in command


class TestProtocolAdapters:
    def test_http_adapter(self):
        adapter = HTTPAdapter()
        assert adapter.connect() is True
        device = Device("d1", "Test", DeviceType.LIGHT, DeviceProtocol.HTTP, "127.0.0.1")
        cmd = DeviceCommand("d1", "turn_on")
        result = adapter.send(device, cmd)
        assert result.success is True

    def test_mqtt_adapter(self):
        adapter = MQTTAdapter()
        assert adapter.connect() is True
        device = Device("d1", "Test", DeviceType.THERMOSTAT, DeviceProtocol.MQTT, "127.0.0.1")
        cmd = DeviceCommand("d1", "set")
        result = adapter.send(device, cmd)
        assert result.success is True

    def test_websocket_adapter(self):
        adapter = WebSocketAdapter()
        assert adapter.connect() is True


class TestSceneManager:
    def test_register_scene(self):
        manager = SceneManager()
        scene = Scene("test_scene", "Test Scene", "Test", [])
        manager.register(scene)
        assert manager.get("test_scene") is not None

    def test_list_scenes(self):
        manager = SceneManager()
        scenes = manager.list_scenes()
        assert len(scenes) > 0


class TestNoUIAdapterComponent:
    def test_component_init(self):
        config = {"default_protocol": "http"}
        component = NoUIAdapterComponent(config)
        assert component.default_protocol == "http"

    def test_connect_disconnect(self):
        component = NoUIAdapterComponent()
        result = component.connect()
        assert result is True
        component.disconnect()

    def test_convert_intent(self):
        component = NoUIAdapterComponent()
        command = component.convert_intent_to_command("开灯", "light")
        assert isinstance(command, str)

    def test_list_devices(self):
        component = NoUIAdapterComponent()
        devices = component.list_devices()
        assert len(devices) > 0

    def test_send_command(self):
        component = NoUIAdapterComponent()
        component.connect()
        result = component.send_command("dev_001", "turn_on")
        assert result is not None

    def test_send_batch_commands(self):
        component = NoUIAdapterComponent()
        component.connect()
        commands = [
            {"device_id": "dev_001", "command": "turn_on"},
            {"device_id": "dev_002", "command": "turn_off"},
        ]
        result = component.send_batch_commands(commands)
        assert isinstance(result, BatchCommandResult)
        assert result.total == 2

    def test_execute_scene(self):
        component = NoUIAdapterComponent()
        component.connect()
        result = component.execute_scene("scene_morning")
        assert isinstance(result, BatchCommandResult)

    def test_list_scenes(self):
        component = NoUIAdapterComponent()
        scenes = component.list_scenes()
        assert len(scenes) > 0


class TestAgentFederationComponent:
    def test_distribute_task(self):
        component = AgentFederationComponent()
        component.connect()
        task = FedTask(task_id="task_1", description="分析销售数据")
        result = component.distribute_task(task, "数据分析")
        assert result.success is True

    def test_distribute_tasks(self):
        component = AgentFederationComponent()
        component.connect()
        tasks = [
            FedTask(task_id="t1", description="分析数据"),
            FedTask(task_id="t2", description="生成报告"),
        ]
        results = component.distribute_tasks(tasks)
        assert len(results) == 2

    def test_create_session(self):
        component = AgentFederationComponent()
        session = component.create_session("测试任务")
        assert session is not None

    def test_list_agents(self):
        component = AgentFederationComponent()
        agents = component.list_agents()
        assert len(agents) > 0

    def test_get_stats(self):
        component = AgentFederationComponent()
        component.connect()
        stats = component.get_stats()
        assert "total_agents" in stats
        assert stats["online_agents"] > 0


class TestTaskDistributor:
    def test_distribute_task(self):
        registry = ServiceRegistry()
        router = Router()
        distributor = TaskDistributor(registry, router)
        agent = Agent("test_agent", "Test", ["test"])
        registry.register(agent)
        task = FedTask(task_id="t1", description="Test task")
        result = distributor.distribute_task(task, "test")
        assert result is not None


class TestResultAggregator:
    def test_aggregate(self):
        import time as time_module

        aggregator = ResultAggregator()
        tasks = [
            FedTask(
                task_id="t1", description="Task 1", status="completed", result={"data": "value1"}
            ),
            FedTask(
                task_id="t2", description="Task 2", status="completed", result={"data": "value2"}
            ),
        ]
        result = aggregator.aggregate(tasks, time_module.time())
        assert result.total_tasks == 2
        assert result.completed_tasks == 2


class TestTemplates:
    def test_templates_directory(self):
        templates_path = Path(__file__).parent.parent / "templates"
        assert templates_path.exists()

    def test_template_structure(self):
        templates_path = Path(__file__).parent.parent / "templates"
        if templates_path.exists():
            for json_file in templates_path.glob("*.json"):
                if json_file.name == "index.json":
                    continue
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                assert "id" in data
                assert "name" in data
                assert "tasks" in data


class TestIntegration:
    def test_full_sdk_init(self):
        config = GhostHubConfig()
        sdk = GhostHubSDK(config)
        assert sdk.intention_bank is not None
        assert sdk.no_ui_adapter is not None
        assert sdk.agent_federation is not None

    def test_workflow_hr(self):
        config = GhostHubConfig()
        sdk = GhostHubSDK(config)
        result = sdk.execute_workflow("帮我优化面试流程")
        assert result["intent_text"] == "帮我优化面试流程"

    def test_workflow_iot(self):
        config = GhostHubConfig()
        sdk = GhostHubSDK(config)
        result = sdk.execute_workflow("打开客厅灯")
        assert "intent_text" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
