"""
Ghost Hub 工作流引擎 - 组件串联核心

将三大组件真正串联:
意图银行 → 任务分解 → 设备控制/Agent协作 → 结果聚合
"""

import time
import uuid
import re
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from .components.intention_bank import (
    IntentionBankComponent,
    Template,
    Task,
    MatchResult,
    TaskGraph,
)
from .components.no_ui_adapter import NoUIAdapterComponent, Device, DeviceType, DeviceCommand
from .components.agent_federation import (
    AgentFederationComponent,
    Agent,
    Task as FedTask,
    AgentStatus,
)


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class TaskType(Enum):
    INTENT_PARSING = "intent_parsing"  # 意图解析
    DEVICE_CONTROL = "device_control"  # 设备控制
    AGENT_EXECUTION = "agent_execution"  # Agent执行
    DATA_PROCESSING = "data_processing"  # 数据处理
    USER_NOTIFICATION = "user_notification"  # 用户通知


@dataclass
class WorkflowStep:
    """工作流步骤"""

    step_id: str
    step_type: TaskType
    description: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def execute(self) -> bool:
        self.start_time = time.time()
        return True

    def complete(self, output: Dict[str, Any]):
        self.output_data = output
        self.status = WorkflowStatus.COMPLETED
        self.end_time = time.time()

    def fail(self, error: str):
        self.error = error
        self.status = WorkflowStatus.FAILED
        self.end_time = time.time()


@dataclass
class Workflow:
    """完整工作流"""

    workflow_id: str
    intent_text: str
    template: Optional[Template]
    steps: List[WorkflowStep] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


class GhostHubWorkflowEngine:
    """
    Ghost Hub 工作流引擎 - 三大组件串联核心

    工作流程:
    1. 意图银行 → 解析用户意图，匹配模板
    2. 任务分解 → 将模板分解为可执行任务
    3. 智能路由 → 根据任务类型路由到:
       - 设备控制 (无UI适配器)
       - Agent执行 (智能体联邦)
    4. 结果聚合 → 汇总执行结果

    使用示例:
        engine = GhostHubWorkflowEngine()
        result = engine.execute("打开客厅灯，温度调到24度")
    """

    def __init__(
        self,
        intention_bank: Optional[IntentionBankComponent] = None,
        no_ui_adapter: Optional[NoUIAdapterComponent] = None,
        agent_federation: Optional[AgentFederationComponent] = None,
    ):

        # 三大组件
        self.intention_bank = intention_bank or IntentionBankComponent()
        self.no_ui_adapter = no_ui_adapter or NoUIAdapterComponent()
        self.agent_federation = agent_federation or AgentFederationComponent()

        # 工作流历史
        self._workflows: Dict[str, Workflow] = {}

        # 任务处理器映射
        self._task_handlers: Dict[str, Callable] = {}
        self._register_default_handlers()

    def _register_default_handlers(self):
        """注册默认任务处理器"""

        def device_control_handler(step: WorkflowStep) -> Dict[str, Any]:
            """设备控制处理器"""
            device_id = step.input_data.get("device_id")
            command = step.input_data.get("command")
            params = step.input_data.get("params", {})

            if not device_id or not command:
                return {"success": False, "error": "Missing device_id or command"}

            result = self.no_ui_adapter.send_command(device_id, command, **params)
            return {
                "success": result.success,
                "device_id": device_id,
                "command": command,
                "message": result.message,
                "new_state": result.new_state,
            }

        def agent_execution_handler(step: WorkflowStep) -> Dict[str, Any]:
            """Agent执行处理器"""
            task_desc = step.input_data.get("task_description")
            intent = step.input_data.get("intent", "")

            if not task_desc:
                return {"success": False, "error": "Missing task_description"}

            # 查找合适的Agent
            agent = self.agent_federation.find_agent(intent or task_desc)

            if not agent:
                return {"success": False, "error": "No available agent found"}

            # 创建任务
            task = FedTask(
                task_id=step.step_id,
                description=task_desc,
                assigned_agent=agent.agent_id,
                status="assigned",
            )

            # 分发任务
            dist_result = self.agent_federation.distribute_task(task, intent)

            if dist_result.success:
                result = self.agent_federation.execute_task(task)
                return {
                    "success": True,
                    "agent_id": agent.agent_id,
                    "agent_name": agent.name,
                    "result": result,
                }
            else:
                return {"success": False, "error": dist_result.message}

        self._task_handlers[TaskType.DEVICE_CONTROL.value] = device_control_handler
        self._task_handlers[TaskType.AGENT_EXECUTION.value] = agent_execution_handler

    def register_task_handler(self, task_type: TaskType, handler: Callable):
        """注册自定义任务处理器"""
        self._task_handlers[task_type.value] = handler

    def execute(self, intent_text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行完整工作流

        Args:
            intent_text: 用户意图文本
            context: 额外上下文

        Returns:
            完整执行结果
        """
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
        workflow = Workflow(
            workflow_id=workflow_id, intent_text=intent_text, template=None, steps=[]
        )

        start_time = time.time()

        try:
            # === 阶段1: 意图解析 ===
            step1 = self._parse_intent(intent_text, context or {})
            workflow.steps.append(step1)

            if step1.status == WorkflowStatus.FAILED:
                workflow.status = WorkflowStatus.FAILED
                workflow.errors.append(f"意图解析失败: {step1.error}")
                return self._build_response(workflow, start_time)

            template = step1.output_data.get("template")
            workflow.template = template

            # === 阶段2: 任务分解 ===
            step2 = self._decompose_tasks(template)
            workflow.steps.append(step2)

            if step2.status == WorkflowStatus.FAILED:
                workflow.status = WorkflowStatus.FAILED
                workflow.errors.append(f"任务分解失败: {step2.error}")
                return self._build_response(workflow, start_time)

            tasks = step2.output_data.get("tasks", [])

            # === 阶段3: 任务执行 ===
            for task in tasks:
                task_step = self._execute_task(task, intent_text, context or {})
                workflow.steps.append(task_step)

                if task_step.status == WorkflowStatus.FAILED:
                    workflow.errors.append(f"任务 {task.id} 执行失败: {task_step.error}")

            # === 阶段4: 结果聚合 ===
            workflow.results = self._aggregate_results(workflow.steps)
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = time.time()

        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.errors.append(str(e))
            workflow.completed_at = time.time()

        self._workflows[workflow_id] = workflow
        return self._build_response(workflow, start_time)

    def _parse_intent(self, intent_text: str, context: Dict[str, Any]) -> WorkflowStep:
        """阶段1: 意图解析"""
        step = WorkflowStep(
            step_id=f"step_{uuid.uuid4().hex[:6]}",
            step_type=TaskType.INTENT_PARSING,
            description=f"解析意图: {intent_text[:50]}...",
        )
        step.execute()

        try:
            match_result = self.intention_bank.match_intent(intent_text)

            if match_result.has_match:
                template = match_result.top_match.template
                step.complete(
                    {
                        "template": template,
                        "template_name": template.name,
                        "domain": template.domain,
                        "similarity": match_result.top_match.similarity,
                        "confidence": match_result.top_match.confidence,
                        "intent_vector": {
                            "urgency": template.intent_vector.urgency,
                            "complexity": template.intent_vector.complexity,
                            "autonomy": template.intent_vector.autonomy,
                            "cooperation": template.intent_vector.cooperation,
                        },
                    }
                )
            else:
                # 没有匹配模板，创建默认任务
                step.complete(
                    {
                        "template": None,
                        "intent_vector": context.get("intent_vector", {}),
                        "fallback_tasks": self._create_fallback_tasks(intent_text),
                    }
                )

        except Exception as e:
            step.fail(str(e))

        return step

    def _decompose_tasks(self, template: Optional[Template]) -> WorkflowStep:
        """阶段2: 任务分解"""
        step = WorkflowStep(
            step_id=f"step_{uuid.uuid4().hex[:6]}",
            step_type=TaskType.DATA_PROCESSING,
            description="分解任务",
        )
        step.execute()

        try:
            if template:
                tasks = self.intention_bank.decompose_task(template)
                task_graph = self.intention_bank.build_task_graph(template)

                step.complete(
                    {
                        "tasks": [
                            {
                                "id": t.id,
                                "name": t.name,
                                "description": t.description,
                                "sequence": t.sequence,
                                "dependencies": t.dependencies,
                                "tools": t.tools,
                                "estimated_time": t.estimated_time,
                            }
                            for t in tasks
                        ],
                        "task_count": len(tasks),
                        "execution_order": task_graph.execution_order,
                    }
                )
            else:
                step.complete({"tasks": [], "task_count": 0})

        except Exception as e:
            step.fail(str(e))

        return step

    def _execute_task(
        self, task_data: Dict[str, Any], intent: str, context: Dict[str, Any]
    ) -> WorkflowStep:
        """阶段3: 执行单个任务"""
        task_id = task_data.get("id", f"task_{uuid.uuid4().hex[:6]}")

        # 根据任务类型决定执行方式
        task_type = self._classify_task(task_data, intent)

        step = WorkflowStep(
            step_id=task_id,
            step_type=task_type,
            description=f"执行: {task_data.get('name', task_id)}",
        )
        step.execute()

        try:
            # 准备输入数据
            step.input_data = self._prepare_task_input(task_data, intent, context)

            # 获取处理器
            handler = self._task_handlers.get(task_type.value)

            if handler:
                result = handler(step)
                step.complete(result)
            else:
                step.complete({"success": True, "message": "No handler, simulated"})

        except Exception as e:
            step.fail(str(e))

        return step

    def _classify_task(self, task_data: Dict[str, Any], intent: str) -> TaskType:
        """根据任务数据分类任务类型"""
        name = task_data.get("name", "").lower()
        desc = task_data.get("description", "").lower()
        tools = task_data.get("tools", [])
        text = (name + desc + " ".join(tools)).lower()

        # IoT相关关键词
        iot_keywords = [
            "灯",
            "空调",
            "设备",
            "控制",
            "开",
            "关",
            "调",
            "温度",
            "light",
            "device",
            "control",
        ]
        if any(kw in text for kw in iot_keywords):
            return TaskType.DEVICE_CONTROL

        # Agent执行关键词
        agent_keywords = ["分析", "处理", "生成", "搜索", "研究", "analyze", "generate", "search"]
        if any(kw in text for kw in agent_keywords):
            return TaskType.AGENT_EXECUTION

        # 意图解析
        parse_keywords = ["解析", "识别", "理解", "parse", "recognize"]
        if any(kw in text for kw in parse_keywords):
            return TaskType.INTENT_PARSING

        return TaskType.DATA_PROCESSING

    def _prepare_task_input(
        self, task_data: Dict[str, Any], intent: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """准备任务输入数据"""
        input_data = task_data.copy()

        # 从意图中提取设备控制信息
        if "设备" in intent or "灯" in intent or "空调" in intent:
            # 尝试解析设备ID
            if "客厅" in intent:
                input_data["device_id"] = "dev_001"
            elif "卧室" in intent:
                input_data["device_id"] = "dev_002"
            elif "空调" in intent:
                input_data["device_id"] = "dev_003"

            # 解析命令
            if "打开" in intent or "开" in intent:
                input_data["command"] = "turn_on"
            elif "关闭" in intent or "关" in intent:
                input_data["command"] = "turn_off"
            elif "调" in intent:
                input_data["command"] = "adjust"

            # 解析参数
            temp_match = re.search(r"(\d+)\s*度", intent)
            if temp_match:
                input_data["params"] = {"temperature": int(temp_match.group(1))}

        # 从上下文获取
        if context:
            input_data.setdefault("params", {}).update(context.get("params", {}))

        return input_data

    def _create_fallback_tasks(self, intent_text: str) -> List[Dict[str, Any]]:
        """创建默认任务"""
        return [
            {
                "id": f"fallback_{uuid.uuid4().hex[:6]}",
                "name": "意图理解",
                "description": f"理解用户意图: {intent_text}",
                "sequence": 1,
            },
            {
                "id": f"fallback_{uuid.uuid4().hex[:6]}",
                "name": "任务规划",
                "description": "规划执行步骤",
                "sequence": 2,
                "dependencies": [],
            },
        ]

    def _aggregate_results(self, steps: List[WorkflowStep]) -> Dict[str, Any]:
        """阶段4: 结果聚合"""
        results = {
            "total_steps": len(steps),
            "completed_steps": sum(1 for s in steps if s.status == WorkflowStatus.COMPLETED),
            "failed_steps": sum(1 for s in steps if s.status == WorkflowStatus.FAILED),
            "step_results": [],
            "device_results": [],
            "agent_results": [],
            "summary": "",
        }

        for step in steps:
            step_result = {
                "step_id": step.step_id,
                "step_type": step.step_type.value,
                "status": step.status.value,
                "description": step.description,
                "output": step.output_data,
            }
            results["step_results"].append(step_result)

            # 分类收集结果
            if step.step_type == TaskType.DEVICE_CONTROL:
                results["device_results"].append(step.output_data)
            elif step.step_type == TaskType.AGENT_EXECUTION:
                results["agent_results"].append(step.output_data)

        # 生成摘要
        if results["failed_steps"] == 0:
            results["summary"] = "所有任务执行成功"
        elif results["completed_steps"] > 0:
            results["summary"] = f"部分成功 ({results['completed_steps']}/{results['total_steps']})"
        else:
            results["summary"] = "所有任务执行失败"

        return results

    def _build_response(self, workflow: Workflow, start_time: float) -> Dict[str, Any]:
        """构建响应"""
        return {
            "workflow_id": workflow.workflow_id,
            "intent_text": workflow.intent_text,
            "status": workflow.status.value,
            "template": workflow.template.name if workflow.template else None,
            "execution_time": time.time() - start_time,
            "results": workflow.results,
            "errors": workflow.errors,
        }

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """获取工作流"""
        return self._workflows.get(workflow_id)

    def list_workflows(self, status: Optional[WorkflowStatus] = None) -> List[Dict[str, Any]]:
        """列出工作流"""
        workflows = list(self._workflows.values())
        if status:
            workflows = [w for w in workflows if w.status == status]

        return [
            {
                "workflow_id": w.workflow_id,
                "intent_text": w.intent_text[:50],
                "status": w.status.value,
                "created_at": datetime.fromtimestamp(w.created_at).isoformat(),
                "steps_count": len(w.steps),
            }
            for w in workflows
        ]

    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        total = len(self._workflows)
        completed = sum(1 for w in self._workflows.values() if w.status == WorkflowStatus.COMPLETED)
        failed = sum(1 for w in self._workflows.values() if w.status == WorkflowStatus.FAILED)

        return {
            "total_workflows": total,
            "completed": completed,
            "failed": failed,
            "success_rate": completed / total if total > 0 else 0,
            "components": {
                "intention_bank": self.intention_bank.get_stats(),
                "no_ui_adapter": self.no_ui_adapter.get_stats(),
                "agent_federation": self.agent_federation.get_stats(),
            },
        }


# === 快捷函数 ===


def create_workflow_engine() -> GhostHubWorkflowEngine:
    """创建工作流引擎（使用默认组件）"""
    return GhostHubWorkflowEngine()


def execute_intent(intent_text: str, **kwargs) -> Dict[str, Any]:
    """快速执行意图"""
    engine = create_workflow_engine()
    return engine.execute(intent_text, kwargs)
