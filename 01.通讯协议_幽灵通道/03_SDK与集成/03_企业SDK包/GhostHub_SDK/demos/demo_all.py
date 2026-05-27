"""
Ghost Hub SDK 统一Demo
演示三大核心功能：意图银行、无UI适配器、智能体联邦
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from ghost_hub_sdk import GhostHubSDK, GhostHubConfig


class GhostHubDemo:
    def __init__(self):
        self.sdk = None
        self.templates_path = Path(__file__).parent.parent / "templates"

    def print_header(self, text: str):
        print("\n" + "=" * 60)
        print(f" {text}")
        print("=" * 60)

    def print_success(self, text: str):
        print(f"✓ {text}")

    def print_info(self, text: str):
        print(f"  → {text}")

    def print_result(self, data: Dict[str, Any]):
        print(json.dumps(data, indent=2, ensure_ascii=False))

    def load_templates(self):
        index_file = self.templates_path / "index.json"
        if not index_file.exists():
            return []

        with open(index_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("templates_index", [])

    def demo_intention_bank(self):
        self.print_header("Demo 1: 意图银行 - HR面试优化")

        templates = self.load_templates()
        self.print_info(f"已加载 {len(templates)} 个模板")

        test_cases = [
            "帮我优化面试流程",
            "改进招聘效率",
            "自动化简历筛选",
        ]

        for i, text in enumerate(test_cases, 1):
            self.print_info(f"[{i}] 输入: {text}")

            matched = False
            for tpl in templates:
                if tpl["domain"] == "hr":
                    self.print_success(f"匹配模板: {tpl['name']}")
                    self.print_info(f"  - 领域: {tpl['domain']}")
                    self.print_info(f"  - 分类: {tpl['category']}")
                    matched = True
                    break

            if not matched:
                self.print_info("  → 默认HR模板")

    def demo_no_ui_adapter(self):
        self.print_header("Demo 2: 无UI适配器 - IoT设备控制")

        config = GhostHubConfig(no_ui_adapter_enabled=True)
        self.sdk = GhostHubSDK(config)

        if self.sdk.no_ui_adapter:
            self.sdk.no_ui_adapter.connect()
            self.print_success("IoT适配器已连接")

        test_commands = [
            ("打开客厅灯", "light"),
            ("空调调到25度", "thermostat"),
            ("关闭所有电器", "all_devices"),
        ]

        for intent, device_type in test_commands:
            self.print_info(f"输入: {intent}")
            if self.sdk and self.sdk.no_ui_adapter:
                command = self.sdk.no_ui_adapter.convert_intent_to_command(intent, device_type)
                self.print_success(f"命令: {command}")
            else:
                self.print_success(f"命令: cmd_{device_type}_001")

    def demo_agent_federation(self):
        self.print_header("Demo 3: 智能体联邦 - 多Agent协作")

        config = GhostHubConfig(agent_federation_enabled=True)
        self.sdk = GhostHubSDK(config)

        if self.sdk.agent_federation:
            self.sdk.agent_federation.connect()
            self.print_success("联邦网络已连接")

        tasks = [
            ("数据分析", "data_agent"),
            ("文档处理", "doc_agent"),
            ("报告生成", "report_agent"),
        ]

        for intent, agent_type in tasks:
            self.print_info(f"任务: {intent}")
            self.print_success(f"分配给: {agent_type}")
            self.print_info(f"  状态: 准备执行")

    def demo_workflow(self):
        self.print_header("Demo 4: 完整工作流")

        config = GhostHubConfig(
            intention_bank_enabled=True,
            no_ui_adapter_enabled=True,
            agent_federation_enabled=True,
        )
        self.sdk = GhostHubSDK(config)

        result = self.sdk.execute_workflow("帮我优化面试流程", "hr_optimization")

        self.print_success("工作流执行完成")
        self.print_info(f"成功: {result.get('success', False)}")
        self.print_info(f"错误: {result.get('errors', [])}")

        if result.get("intent_match"):
            match = result["intent_match"]
            self.print_info(f"匹配模板: {match.get('template_name', 'N/A')}")
            self.print_info(f"相似度: {match.get('similarity', 0):.2f}")

        if result.get("task_graph"):
            tg = result["task_graph"]
            self.print_info(f"任务数: {tg.get('task_count', 0)}")

    def demo_stats(self):
        self.print_header("Demo 5: SDK统计信息")

        config = GhostHubConfig()
        self.sdk = GhostHubSDK(config)

        stats = self.sdk.get_stats()
        self.print_result(stats)

    def run_all(self):
        print("\n" + "#" * 60)
        print("# Ghost Hub SDK 统一演示程序")
        print("#" * 60)

        self.demo_intention_bank()
        self.demo_no_ui_adapter()
        self.demo_agent_federation()
        self.demo_workflow()
        self.demo_stats()

        print("\n" + "#" * 60)
        print("# 演示完成!")
        print("#" * 60)


if __name__ == "__main__":
    demo = GhostHubDemo()
    demo.run_all()
