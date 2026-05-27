"""
智能体联邦组件 - 自包含实现
多Agent协作、路由发现、协作会话
"""

import time
import uuid
import hashlib
import threading
import concurrent.futures
from typing import Dict, Any, List, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import defaultdict


class AgentStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    IDLE = "idle"


class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    HEARTBEAT = "heartbeat"
    TASK = "task"
    RESULT = "result"


class RoutingStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_LOAD = "least_load"
    INTENT_MATCH = "intent_match"
    RANDOM = "random"


@dataclass
class Agent:
    agent_id: str
    name: str
    capabilities: List[str] = field(default_factory=list)
    status: AgentStatus = AgentStatus.IDLE
    load: float = 0.0
    intent_keywords: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    last_heartbeat: float = field(default_factory=time.time)


@dataclass
class Message:
    id: str
    sender_id: str
    receiver_id: Optional[str]
    msg_type: MessageType
    content: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    correlation_id: Optional[str] = None


@dataclass
class Session:
    id: str
    task: str
    participants: List[str] = field(default_factory=list)
    status: str = "active"
    created_at: float = field(default_factory=time.time)
    messages: List[Message] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IntentRoute:
    target_agent: Agent
    confidence: float
    strategy: RoutingStrategy


@dataclass
class Task:
    task_id: str
    description: str
    assigned_agent: Optional[str] = None
    status: str = "pending"
    result: Optional[Any] = None
    dependencies: List[str] = field(default_factory=list)
    priority: int = 0


@dataclass
class TaskDistributionResult:
    task_id: str
    assigned_agent: str
    success: bool
    message: str = ""


@dataclass
class AggregatedResult:
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    results: Dict[str, Any]
    execution_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class ServiceRegistry:
    def __init__(self, heartbeat_timeout: float = 60.0):
        self.heartbeat_timeout = heartbeat_timeout
        self._agents: Dict[str, Agent] = {}
        self._lock = threading.Lock()

    def register(self, agent: Agent) -> bool:
        with self._lock:
            self._agents[agent.agent_id] = agent
            agent.last_heartbeat = time.time()
            return True

    def unregister(self, agent_id: str) -> bool:
        with self._lock:
            if agent_id in self._agents:
                del self._agents[agent_id]
                return True
            return False

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        with self._lock:
            return self._agents.get(agent_id)

    def list_agents(self, status: Optional[AgentStatus] = None) -> List[Agent]:
        with self._lock:
            agents = list(self._agents.values())
            if status:
                agents = [a for a in agents if a.status == status]
            return agents

    def update_heartbeat(self, agent_id: str):
        with self._lock:
            if agent_id in self._agents:
                self._agents[agent_id].last_heartbeat = time.time()

    def update_load(self, agent_id: str, load_delta: float):
        with self._lock:
            if agent_id in self._agents:
                self._agents[agent_id].load = max(0, self._agents[agent_id].load + load_delta)

    def cleanup_stale(self) -> int:
        with self._lock:
            now = time.time()
            stale = [
                aid
                for aid, agent in self._agents.items()
                if now - agent.last_heartbeat > self.heartbeat_timeout
            ]
            for aid in stale:
                self._agents[aid].status = AgentStatus.OFFLINE
            return len(stale)


class Router:
    def __init__(self, strategy: RoutingStrategy = RoutingStrategy.LEAST_LOAD):
        self.strategy = strategy
        self._round_robin_index = 0
        self._lock = threading.Lock()

    def route(self, intent: str, agents: List[Agent]) -> Optional[IntentRoute]:
        if not agents:
            return None

        online_agents = [a for a in agents if a.status == AgentStatus.ONLINE]
        if not online_agents:
            online_agents = [a for a in agents if a.status == AgentStatus.IDLE]

        if not online_agents:
            return None

        if self.strategy == RoutingStrategy.ROUND_ROBIN:
            return self._route_round_robin(intent, online_agents)
        elif self.strategy == RoutingStrategy.LEAST_LOAD:
            return self._route_least_load(intent, online_agents)
        elif self.strategy == RoutingStrategy.INTENT_MATCH:
            return self._route_intent_match(intent, online_agents)
        else:
            return self._route_random(intent, online_agents)

    def _route_round_robin(self, intent: str, agents: List[Agent]) -> IntentRoute:
        with self._lock:
            agent = agents[self._round_robin_index % len(agents)]
            self._round_robin_index += 1
        return IntentRoute(agent, 1.0, self.strategy)

    def _route_least_load(self, intent: str, agents: List[Agent]) -> IntentRoute:
        agent = min(agents, key=lambda a: a.load)
        return IntentRoute(agent, 1.0 - agent.load * 0.5, self.strategy)

    def _route_intent_match(self, intent: str, agents: List[Agent]) -> IntentRoute:
        if not agents:
            raise ValueError("No agents available for routing")

        intent_lower = intent.lower()
        best_agent = agents[0]
        best_score = 0.0

        for agent in agents:
            score = sum(1 for kw in agent.intent_keywords if kw.lower() in intent_lower)
            if score > best_score:
                best_score = score
                best_agent = agent

        confidence = min(1.0, best_score / max(len(best_agent.intent_keywords), 1))
        return IntentRoute(best_agent, confidence, self.strategy)

    def _route_random(self, intent: str, agents: List[Agent]) -> IntentRoute:
        import random

        agent = random.choice(agents)
        return IntentRoute(agent, 0.5, self.strategy)


class MessageProtocol:
    def encode(self, message: Message) -> Dict[str, Any]:
        return {
            "id": message.id,
            "sender": message.sender_id,
            "receiver": message.receiver_id,
            "type": message.msg_type.value,
            "content": message.content,
            "payload": message.payload,
            "timestamp": message.timestamp,
            "correlation_id": message.correlation_id,
        }

    def decode(self, data: Dict[str, Any]) -> Message:
        required_fields = ["id", "sender", "type", "content"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Message data missing required field: '{field}'")

        return Message(
            id=data["id"],
            sender_id=data["sender"],
            receiver_id=data.get("receiver"),
            msg_type=MessageType(data["type"]),
            content=data["content"],
            payload=data.get("payload", {}),
            timestamp=data.get("timestamp", time.time()),
            correlation_id=data.get("correlation_id"),
        )


class TaskDistributor:
    def __init__(self, registry: ServiceRegistry, router: Router):
        self.registry = registry
        self.router = router

    def distribute_task(self, task: Task, intent: str = "") -> TaskDistributionResult:
        agents = self.registry.list_agents(AgentStatus.ONLINE)
        if not agents:
            agents = self.registry.list_agents()

        if not agents:
            return TaskDistributionResult(task.task_id, "", False, "No available agents")

        route = self.router.route(intent or task.description, agents)
        if not route:
            return TaskDistributionResult(task.task_id, "", False, "Routing failed")

        task.assigned_agent = route.target_agent.agent_id
        task.status = "assigned"
        self.registry.update_load(route.target_agent.agent_id, 0.1)

        return TaskDistributionResult(
            task.task_id,
            route.target_agent.agent_id,
            True,
            f"Task assigned to {route.target_agent.name}",
        )

    def distribute_parallel(
        self, tasks: List[Task], intents: List[str] = None
    ) -> List[TaskDistributionResult]:
        results = []
        for i, task in enumerate(tasks):
            intent = intents[i] if intents and i < len(intents) else ""
            result = self.distribute_task(task, intent)
            results.append(result)
        return results


class ResultAggregator:
    def __init__(self):
        self._results: Dict[str, Any] = {}

    def add_result(self, task_id: str, agent_id: str, result: Any):
        self._results[task_id] = {
            "agent_id": agent_id,
            "result": result,
            "timestamp": time.time(),
        }

    def aggregate(self, tasks: List[Task], start_time: float) -> AggregatedResult:
        completed = sum(1 for t in tasks if t.status == "completed")
        failed = sum(1 for t in tasks if t.status == "failed")

        results = {
            "task_results": {t.task_id: t.result for t in tasks if t.result is not None},
            "aggregated_data": self._aggregate_data(tasks),
        }

        return AggregatedResult(
            total_tasks=len(tasks),
            completed_tasks=completed,
            failed_tasks=failed,
            results=results,
            execution_time=time.time() - start_time,
        )

    def _aggregate_data(self, tasks: List[Task]) -> Dict[str, Any]:
        aggregated = defaultdict(list)
        for task in tasks:
            if task.result:
                if isinstance(task.result, dict):
                    for key, value in task.result.items():
                        aggregated[key].append(value)
                else:
                    aggregated["values"].append(task.result)
        return dict(aggregated)


class AgentFederationComponent:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.agent_id = self.config.get("agent_id", f"agent_{uuid.uuid4().hex[:8]}")
        self.agent_name = self.config.get("agent_name", "GhostHubAgent")
        strategy_str = self.config.get("routing_strategy", "least_load")
        try:
            strategy = RoutingStrategy(strategy_str)
        except ValueError:
            strategy = RoutingStrategy.LEAST_LOAD

        self._registry = ServiceRegistry()
        self._router = Router(strategy)
        self._protocol = MessageProtocol()
        self._distributor = TaskDistributor(self._registry, self._router)
        self._aggregator = ResultAggregator()

        self._this_agent = Agent(
            agent_id=self.agent_id,
            name=self.agent_name,
            capabilities=["intent_matching", "task_decomposition", "coordination"],
            status=AgentStatus.IDLE,
            intent_keywords=["分析", "处理", "优化", "automation"],
        )

        self._sessions: Dict[str, Session] = {}
        self._message_handlers: Dict[MessageType, Callable] = {}
        self._task_handlers: Dict[str, Callable] = {}
        self._connected = False

        self._heartbeat_thread: Optional[threading.Thread] = None
        self._running = False

        self._register_default_agents()

    def _register_default_agents(self):
        default_agents = [
            Agent(
                "data_agent",
                "数据分析Agent",
                ["数据分析", "统计", "可视化"],
                AgentStatus.ONLINE,
                intent_keywords=["分析", "数据", "统计", "报表"],
            ),
            Agent(
                "doc_agent",
                "文档处理Agent",
                ["文档处理", "摘要", "翻译"],
                AgentStatus.ONLINE,
                intent_keywords=["文档", "总结", "翻译", "报告"],
            ),
            Agent(
                "code_agent",
                "代码开发Agent",
                ["代码生成", "代码审查", "测试"],
                AgentStatus.ONLINE,
                intent_keywords=["代码", "开发", "编程", "实现"],
            ),
            Agent(
                "research_agent",
                "研究Agent",
                ["搜索", "调研", "学习"],
                AgentStatus.ONLINE,
                intent_keywords=["研究", "调研", "搜索", "学习"],
            ),
        ]
        for agent in default_agents:
            self._registry.register(agent)

    def connect(self) -> bool:
        if self._connected:
            return True
        self._registry.register(self._this_agent)
        self._this_agent.status = AgentStatus.ONLINE
        self._running = True
        self._heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()
        self._connected = True
        return True

    def disconnect(self):
        self._running = False
        self._this_agent.status = AgentStatus.OFFLINE
        self._registry.unregister(self.agent_id)
        if self._heartbeat_thread:
            self._heartbeat_thread.join(timeout=2)
        self._connected = False

    def _heartbeat_loop(self):
        while self._running:
            self._registry.update_heartbeat(self.agent_id)
            self._registry.cleanup_stale()
            time.sleep(10)

    def register_agent(self, agent: Agent) -> bool:
        return self._registry.register(agent)

    def unregister_agent(self, agent_id: str) -> bool:
        return self._registry.unregister(agent_id)

    def find_agent(self, intent: str) -> Optional[Agent]:
        route = self._router.route(intent, self._registry.list_agents())
        return route.target_agent if route else None

    def route_intent(self, intent: str) -> Optional[IntentRoute]:
        return self._router.route(intent, self._registry.list_agents())

    def distribute_task(self, task: Task, intent: str = "") -> TaskDistributionResult:
        return self._distributor.distribute_task(task, intent)

    def distribute_tasks(
        self, tasks: List[Task], intents: List[str] = None
    ) -> List[TaskDistributionResult]:
        return self._distributor.distribute_parallel(tasks, intents)

    def aggregate_results(self, tasks: List[Task]) -> AggregatedResult:
        return self._aggregator.aggregate(tasks, time.time())

    def execute_task(self, task: Task, handler: Optional[Callable] = None) -> Any:
        if task.assigned_agent and handler:
            return handler(task)
        elif task.assigned_agent in self._task_handlers:
            return self._task_handlers[task.assigned_agent](task)
        else:
            task.result = f"Simulated result for: {task.description}"
            task.status = "completed"
            return task.result

    def register_task_handler(self, agent_id: str, handler: Callable):
        self._task_handlers[agent_id] = handler

    def send_message(
        self, target_id: str, content: str, msg_type: str = "request", **kwargs
    ) -> Optional[Message]:
        target = self._registry.get_agent(target_id)
        if not target:
            return None
        msg_type_enum = MessageType(msg_type)
        message = Message(
            id=uuid.uuid4().hex,
            sender_id=self.agent_id,
            receiver_id=target_id,
            msg_type=msg_type_enum,
            content=content,
            payload=kwargs,
        )
        if msg_type_enum in self._message_handlers:
            self._message_handlers[msg_type_enum](message)
        return message

    def broadcast(self, content: str, **kwargs) -> List[Message]:
        messages = []
        for agent in self._registry.list_agents():
            if agent.agent_id != self.agent_id:
                msg = self.send_message(agent.agent_id, content, "broadcast", **kwargs)
                if msg:
                    messages.append(msg)
        return messages

    def register_handler(self, msg_type: MessageType, handler: Callable):
        self._message_handlers[msg_type] = handler

    def create_session(self, task: str, participants: Optional[List[str]] = None) -> Session:
        session = Session(id=uuid.uuid4().hex, task=task, participants=[])
        if participants:
            for pid in participants:
                agent = self._registry.get_agent(pid)
                if agent and pid not in session.participants:
                    session.participants.append(pid)
        self._sessions[session.id] = session
        return session

    def add_session_message(self, session_id: str, message: Message):
        if session_id in self._sessions:
            self._sessions[session_id].messages.append(message)

    def complete_session(self, session_id: str, results: Dict[str, Any]):
        if session_id in self._sessions:
            self._sessions[session_id].status = "completed"
            self._sessions[session_id].results = results

    def get_session(self, session_id: str) -> Optional[Session]:
        return self._sessions.get(session_id)

    def list_sessions(self, status: Optional[str] = None) -> List[Session]:
        sessions = list(self._sessions.values())
        if status:
            sessions = [s for s in sessions if s.status == status]
        return sessions

    def list_agents(self, status: Optional[AgentStatus] = None) -> List[Agent]:
        return self._registry.list_agents(status)

    def get_stats(self) -> Dict[str, Any]:
        agents = self._registry.list_agents()
        online_count = sum(1 for a in agents if a.status == AgentStatus.ONLINE)
        return {
            "enabled": True,
            "connected": self._connected,
            "this_agent": {
                "id": self.agent_id,
                "name": self.agent_name,
                "status": self._this_agent.status.value,
            },
            "total_agents": len(agents),
            "online_agents": online_count,
            "active_sessions": len(self.list_sessions("active")),
            "total_sessions": len(self._sessions),
        }
