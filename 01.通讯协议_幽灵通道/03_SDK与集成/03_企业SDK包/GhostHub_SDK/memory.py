"""
Ghost Hub 记忆层 - 组件执行历史与上下文管理

为Ghost Hub三大组件提供记忆能力：
- 意图执行历史
- 设备状态历史
- Agent协作记录
- 用户偏好学习
"""

import json
import time
import uuid
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict


@dataclass
class IntentRecord:
    """意图执行记录"""

    record_id: str
    intent_text: str
    template_id: Optional[str]
    template_name: Optional[str]
    similarity: float
    timestamp: float
    workflow_id: str
    success: bool
    execution_time: float
    tasks_count: int
    errors: List[str]


@dataclass
class DeviceStateRecord:
    """设备状态记录"""

    record_id: str
    device_id: str
    device_name: str
    device_type: str
    command: str
    params: Dict[str, Any]
    success: bool
    timestamp: float
    new_state: Dict[str, Any]
    error: Optional[str]


@dataclass
class AgentActivityRecord:
    """Agent活动记录"""

    record_id: str
    agent_id: str
    agent_name: str
    action: str
    intent: str
    success: bool
    timestamp: float
    result_summary: str
    execution_time: float


class GhostHubMemory:
    """
    Ghost Hub 记忆层

    管理三大组件的执行历史和上下文

    使用示例:
        memory = GhostHubMemory()
        memory.record_intent(intent_text, result)
        memory.record_device_command(device_id, command, result)
    """

    def __init__(self, storage_path: Optional[str] = None):
        if storage_path is None:
            storage_path = Path.home() / ".ghost_hub" / "memory"

        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # 线程锁保护
        self._lock = threading.Lock()

        # 内存缓存 - 受锁保护
        self._intent_history: List[IntentRecord] = []
        self._device_history: List[DeviceStateRecord] = []
        self._agent_history: List[AgentActivityRecord] = []
        self._user_preferences: Dict[str, Any] = {}
        self._context: Dict[str, Any] = {}

        # 加载历史
        self._load()

    def _get_record_path(self, record_type: str) -> Path:
        return self.storage_path / f"{record_type}_history.json"

    def _load(self):
        """加载历史记录"""
        # 加载意图历史
        path = self._get_record_path("intent")
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._intent_history = [IntentRecord(**r) for r in data[-100:]]
            except:
                pass

        # 加载设备历史
        path = self._get_record_path("device")
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._device_history = [DeviceStateRecord(**r) for r in data[-100:]]
            except:
                pass

        # 加载Agent历史
        path = self._get_record_path("agent")
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._agent_history = [AgentActivityRecord(**r) for r in data[-100:]]
            except:
                pass

        # 加载用户偏好
        path = self.storage_path / "preferences.json"
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self._user_preferences = json.load(f)
            except:
                pass

    def _save(self, record_type: str):
        """保存历史记录"""
        path = self._get_record_path(record_type)

        if record_type == "intent":
            data = [asdict(r) for r in self._intent_history[-100:]]
        elif record_type == "device":
            data = [asdict(r) for r in self._device_history[-100:]]
        elif record_type == "agent":
            data = [asdict(r) for r in self._agent_history[-100:]]
        else:
            return

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # === 意图记录 ===

    def record_intent(self, intent_text: str, result: Dict[str, Any]):
        """记录意图执行"""
        step_results = result.get("results", {}).get("step_results", [])
        similarity = 0
        if step_results and len(step_results) > 0:
            similarity = step_results[0].get("output", {}).get("similarity", 0)

        record = IntentRecord(
            record_id=f"ir_{uuid.uuid4().hex[:8]}",
            intent_text=intent_text,
            template_id=result.get("template"),
            template_name=result.get("template"),
            similarity=similarity,
            timestamp=time.time(),
            workflow_id=result.get("workflow_id", ""),
            success=result.get("status") == "completed",
            execution_time=result.get("execution_time", 0),
            tasks_count=result.get("results", {}).get("total_steps", 0),
            errors=result.get("errors", []),
        )

        with self._lock:
            self._intent_history.append(record)
            self._save("intent")
            self._context["last_intent"] = intent_text
            self._context["last_template"] = record.template_name
            self._context["last_success"] = record.success

    def get_intent_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取意图历史"""
        records = self._intent_history[-limit:]
        return [asdict(r) for r in reversed(records)]

    def get_intent_by_template(self, template_name: str) -> List[IntentRecord]:
        """按模板筛选意图"""
        return [r for r in self._intent_history if r.template_name == template_name]

    # === 设备记录 ===

    def record_device_command(
        self,
        device_id: str,
        device_name: str,
        device_type: str,
        command: str,
        params: Dict[str, Any],
        result: Any,
    ):
        """记录设备命令"""
        record = DeviceStateRecord(
            record_id=f"dr_{uuid.uuid4().hex[:8]}",
            device_id=device_id,
            device_name=device_name,
            device_type=device_type,
            command=command,
            params=params,
            success=result.success if hasattr(result, "success") else False,
            timestamp=time.time(),
            new_state=result.new_state if hasattr(result, "new_state") else {},
            error=result.error if hasattr(result, "error") else None,
        )

        self._device_history.append(record)
        self._save("device")

    def get_device_history(
        self, device_id: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """获取设备历史"""
        records = self._device_history
        if device_id:
            records = [r for r in records if r.device_id == device_id]

        records = records[-limit:]
        return [asdict(r) for r in reversed(records)]

    def get_device_state(self, device_id: str) -> Dict[str, Any]:
        """获取设备当前状态"""
        device_records = [r for r in self._device_history if r.device_id == device_id]
        if not device_records:
            return {"device_id": device_id, "state": "unknown"}

        latest = device_records[-1]
        return {
            "device_id": device_id,
            "device_name": latest.device_name,
            "device_type": latest.device_type,
            "last_command": latest.command,
            "last_success": latest.success,
            "current_state": latest.new_state,
            "last_updated": datetime.fromtimestamp(latest.timestamp).isoformat(),
        }

    # === Agent记录 ===

    def record_agent_activity(
        self, agent_id: str, agent_name: str, action: str, intent: str, success: bool, result: Any
    ):
        """记录Agent活动"""
        record = AgentActivityRecord(
            record_id=f"ar_{uuid.uuid4().hex[:8]}",
            agent_id=agent_id,
            agent_name=agent_name,
            action=action,
            intent=intent,
            success=success,
            timestamp=time.time(),
            result_summary=str(result)[:100],
            execution_time=0,
        )

        self._agent_history.append(record)
        self._save("agent")

    def get_agent_history(
        self, agent_id: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """获取Agent历史"""
        records = self._agent_history
        if agent_id:
            records = [r for r in records if r.agent_id == agent_id]

        records = records[-limit:]
        return [asdict(r) for r in reversed(records)]

    def get_agent_stats(self) -> Dict[str, Any]:
        """获取Agent统计"""
        agent_counts = defaultdict(int)
        agent_success = defaultdict(int)

        for record in self._agent_history:
            agent_counts[record.agent_name] += 1
            if record.success:
                agent_success[record.agent_name] += 1

        return {
            agent_name: {
                "total": count,
                "success": agent_success[agent_name],
                "rate": agent_success[agent_name] / count if count > 0 else 0,
            }
            for agent_name, count in agent_counts.items()
        }

    # === 用户偏好 ===

    def learn_preference(self, key: str, value: Any):
        """学习用户偏好"""
        with self._lock:
            self._user_preferences[key] = value

            path = self.storage_path / "preferences.json"
            try:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self._user_preferences, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

    def get_preference(self, key: str, default: Any = None) -> Any:
        """获取用户偏好"""
        with self._lock:
            return self._user_preferences.get(key, default)

    def get_all_preferences(self) -> Dict[str, Any]:
        """获取所有偏好"""
        with self._lock:
            return self._user_preferences.copy()

    # === 上下文管理 ===

    def set_context(self, key: str, value: Any):
        """设置上下文"""
        with self._lock:
            self._context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """获取上下文"""
        with self._lock:
            return self._context.get(key, default)

    def get_full_context(self) -> Dict[str, Any]:
        """获取完整上下文"""
        with self._lock:
            return self._context.copy()

    def clear_context(self):
        """清空上下文"""
        with self._lock:
            self._context.clear()

    # === 统计 ===

    def get_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        recent = self._intent_history[-5:] if self._intent_history else []
        return {
            "intent_history_count": len(self._intent_history),
            "device_history_count": len(self._device_history),
            "agent_history_count": len(self._agent_history),
            "preferences_count": len(self._user_preferences),
            "context_keys": list(self._context.keys()),
            "recent_intents": [r.intent_text[:30] for r in recent],
            "success_rate": sum(1 for r in self._intent_history if r.success)
            / max(len(self._intent_history), 1),
        }

    # === 知识提取 ===

    def extract_patterns(self) -> List[Dict[str, Any]]:
        """从历史中提取模式"""
        patterns = []

        # 意图-模板关联模式
        intent_template_map = defaultdict(list)
        for record in self._intent_history:
            if record.template_name:
                intent_template_map[record.template_name].append(record.intent_text)

        for template, intents in intent_template_map.items():
            patterns.append(
                {
                    "pattern_type": "intent_template",
                    "template": template,
                    "sample_intents": intents[:5],
                    "frequency": len(intents),
                }
            )

        # 设备-命令模式
        device_command_map = defaultdict(list)
        for record in self._device_history:
            device_command_map[record.device_id].append(record.command)

        for device, commands in device_command_map.items():
            patterns.append(
                {
                    "pattern_type": "device_commands",
                    "device_id": device,
                    "commands": list(set(commands)),
                    "frequency": len(commands),
                }
            )

        return patterns


# 全局单例
_global_memory: Optional[GhostHubMemory] = None


def get_ghost_hub_memory() -> GhostHubMemory:
    """获取全局记忆实例"""
    global _global_memory
    if _global_memory is None:
        _global_memory = GhostHubMemory()
    return _global_memory
