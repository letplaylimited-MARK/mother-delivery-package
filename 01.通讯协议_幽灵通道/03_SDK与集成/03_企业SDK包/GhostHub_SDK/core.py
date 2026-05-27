"""
Ghost Hub SDK核心 - 统一入口
"""

import logging
from typing import Optional, Dict, Any, List

from .config import GhostHubConfig
from .components.intention_bank import IntentionBankComponent
from .components.no_ui_adapter import NoUIAdapterComponent
from .components.agent_federation import AgentFederationComponent

logger = logging.getLogger(__name__)


class GhostHubSDK:
    """
    Ghost Hub SDK统一入口

    整合三大核心功能:
    1. 意图银行 - 意图解析与任务分解
    2. 无UI适配器 - IoT设备集成
    3. 智能体联邦 - 多Agent协作
    """

    def __init__(self, config: Optional[GhostHubConfig] = None):
        self.config = config or GhostHubConfig()
        self._init_logger()

        self._intention_bank: Optional[IntentionBankComponent] = None
        self._no_ui_adapter: Optional[NoUIAdapterComponent] = None
        self._agent_federation: Optional[AgentFederationComponent] = None

        self._initialize_components()

        logger.info(f"GhostHub SDK初始化完成 | 版本: {self.config.version}")

    def _init_logger(self):
        level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    def _initialize_components(self):
        if self.config.intention_bank_enabled:
            self._intention_bank = IntentionBankComponent(self.config.intention_bank_config)
            logger.info("意图银行组件已初始化")

        if self.config.no_ui_adapter_enabled:
            self._no_ui_adapter = NoUIAdapterComponent(self.config.no_ui_adapter_config)
            logger.info("无UI适配器组件已初始化")

        if self.config.agent_federation_enabled:
            self._agent_federation = AgentFederationComponent(self.config.agent_federation_config)
            logger.info("智能体联邦组件已初始化")

    @property
    def intention_bank(self) -> Optional[IntentionBankComponent]:
        return self._intention_bank

    @property
    def no_ui_adapter(self) -> Optional[NoUIAdapterComponent]:
        return self._no_ui_adapter

    @property
    def agent_federation(self) -> Optional[AgentFederationComponent]:
        return self._agent_federation

    def connect(self) -> Dict[str, bool]:
        results = {}

        if self._no_ui_adapter:
            results["no_ui_adapter"] = self._no_ui_adapter.connect()

        if self._agent_federation:
            results["agent_federation"] = self._agent_federation.connect()

        return results

    def disconnect(self):
        if self._no_ui_adapter:
            self._no_ui_adapter.disconnect()

        if self._agent_federation:
            self._agent_federation.disconnect()

        logger.info("GhostHub SDK已断开")

    def get_stats(self) -> Dict[str, Any]:
        stats = {
            "name": self.config.name,
            "version": self.config.version,
            "components": {},
        }

        if self._intention_bank:
            stats["components"]["intention_bank"] = self._intention_bank.get_stats()

        if self._no_ui_adapter:
            stats["components"]["no_ui_adapter"] = self._no_ui_adapter.get_stats()

        if self._agent_federation:
            stats["components"]["agent_federation"] = self._agent_federation.get_stats()

        return stats

    def execute_workflow(self, intent_text: str, workflow_type: str = "default") -> Dict[str, Any]:
        """
        执行完整工作流

        Args:
            intent_text: 用户意图文本
            workflow_type: 工作流类型

        Returns:
            包含意图匹配、任务分解、执行的完整结果
        """
        result = {
            "intent_text": intent_text,
            "workflow_type": workflow_type,
            "success": False,
            "intent_match": None,
            "task_graph": None,
            "execution": None,
            "errors": [],
        }

        if not self._intention_bank:
            result["errors"].append("意图银行组件未启用")
            return result

        try:
            match_result = self._intention_bank.match_intent(intent_text)

            if match_result and match_result.has_match and match_result.top_match:
                top_match = match_result.top_match
                result["intent_match"] = {
                    "template_name": top_match.template.name,
                    "template_id": top_match.template.id,
                    "domain": top_match.template.domain,
                    "similarity": top_match.similarity,
                    "confidence": top_match.confidence,
                }

                tasks = self._intention_bank.decompose_task(top_match.template)
                result["task_graph"] = {
                    "tasks": [
                        {
                            "id": task.id,
                            "name": task.name,
                            "description": task.description,
                            "dependencies": task.dependencies,
                            "estimated_time": task.estimated_time,
                            "tools": task.tools,
                        }
                        for task in tasks
                    ],
                    "task_count": len(tasks),
                }

                result["roi_estimate"] = top_match.template.roi_estimate
                result["business_metrics"] = top_match.template.business_metrics
                result["success"] = True
            else:
                result["errors"].append("未找到匹配的意图模板")

        except Exception as e:
            result["errors"].append(str(e))
            logger.error(f"工作流执行失败: {str(e)}")

        return result

    def list_available_templates(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出可用模板"""
        if not self._intention_bank:
            return []

        templates = self._intention_bank.list_templates(domain)
        return [
            {
                "id": t.id,
                "name": t.name,
                "domain": t.domain,
                "description": t.description,
                "task_count": len(t.tasks),
                "tags": t.tags,
            }
            for t in templates
        ]
