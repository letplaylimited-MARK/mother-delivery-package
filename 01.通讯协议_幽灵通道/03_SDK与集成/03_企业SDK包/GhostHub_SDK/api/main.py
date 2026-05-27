"""
Ghost Hub SDK - REST API
FastAPI实现的企业级AI工作流编排API
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from ghost_hub_sdk import GhostHubSDK, GhostHubConfig
from ghost_hub_sdk.components.intention_bank import IntentionBankComponent
from ghost_hub_sdk.components.no_ui_adapter import NoUIAdapterComponent, Scene, DeviceType
from ghost_hub_sdk.components.agent_federation import AgentFederationComponent, AgentStatus


app = FastAPI(
    title="Ghost Hub API",
    description="企业级AI工作流编排器 REST API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 安全配置：限制CORS来源
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)

sdk = GhostHubSDK(GhostHubConfig())


class IntentRequest(BaseModel):
    text: str = Field(..., description="意图文本")
    threshold: Optional[float] = Field(0.3, description="匹配阈值")


class WorkflowRequest(BaseModel):
    intent_text: str = Field(..., description="用户意图")
    workflow_type: Optional[str] = Field("default", description="工作流类型")


class DeviceCommandRequest(BaseModel):
    device_id: str = Field(..., description="设备ID")
    command: str = Field(..., description="命令")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict, description="参数")


class BatchCommandRequest(BaseModel):
    commands: List[Dict[str, Any]] = Field(..., description="命令列表")


class SceneRequest(BaseModel):
    scene_id: str = Field(..., description="场景ID")


class AgentRegisterRequest(BaseModel):
    agent_id: str = Field(..., description="智能体ID")
    name: str = Field(..., description="智能体名称")
    capabilities: List[str] = Field(..., description="能力列表")
    intent_keywords: Optional[List[str]] = Field(default_factory=list, description="意图关键词")


class TaskDistributeRequest(BaseModel):
    tasks: List[Dict[str, Any]] = Field(..., description="任务列表")


class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


@app.get("/", tags=["Root"])
async def root():
    return {"name": "Ghost Hub API", "version": "0.1.0", "status": "running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ==================== 意图银行 API ====================


@app.get("/api/v1/templates", tags=["意图银行"])
async def list_templates(domain: Optional[str] = None):
    templates = sdk.intention_bank.list_templates(domain)
    return {
        "success": True,
        "count": len(templates),
        "templates": [
            {
                "id": t.id,
                "name": t.name,
                "domain": t.domain,
                "description": t.description,
                "task_count": len(t.tasks),
                "tags": t.tags,
            }
            for t in templates
        ],
    }


@app.get("/api/v1/templates/{template_id}", tags=["意图银行"])
async def get_template(template_id: str):
    template = sdk.intention_bank.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    return {
        "success": True,
        "template": {
            "id": template.id,
            "name": template.name,
            "domain": template.domain,
            "description": template.description,
            "intent_vector": {
                "urgency": template.intent_vector.urgency,
                "complexity": template.intent_vector.complexity,
                "autonomy": template.intent_vector.autonomy,
                "cooperation": template.intent_vector.cooperation,
                "risk_tolerance": template.intent_vector.risk_tolerance,
            },
            "tasks": [
                {
                    "id": t.id,
                    "name": t.name,
                    "description": t.description,
                    "sequence": t.sequence,
                    "dependencies": t.dependencies,
                    "estimated_time": t.estimated_time,
                    "tools": t.tools,
                }
                for t in template.tasks
            ],
            "business_metrics": template.business_metrics,
            "roi_estimate": template.roi_estimate,
            "tags": template.tags,
        },
    }


@app.post("/api/v1/intent/match", tags=["意图银行"])
async def match_intent(request: IntentRequest):
    result = sdk.intention_bank.match_intent(request.text)

    if not result.has_match:
        return {
            "success": False,
            "message": "未找到匹配的意图",
            "has_match": False,
        }

    match = result.top_match
    return {
        "success": True,
        "has_match": True,
        "match": {
            "template_id": match.template.id,
            "template_name": match.template.name,
            "domain": match.template.domain,
            "similarity": round(match.similarity, 3),
            "confidence": round(match.confidence, 3),
        },
    }


@app.post("/api/v1/intent/multi-match", tags=["意图银行"])
async def match_multi_intent(request: IntentRequest):
    result = sdk.intention_bank.match_multi_intent(request.text)

    return {
        "success": True,
        "intents": result.intents,
        "templates": [
            {
                "id": t.id,
                "name": t.name,
                "domain": t.domain,
            }
            for t in result.templates
        ],
        "execution_order": result.execution_order,
    }


@app.post("/api/v1/workflow/execute", tags=["工作流"])
async def execute_workflow(request: WorkflowRequest):
    result = sdk.execute_workflow(request.intent_text, request.workflow_type)
    return {
        "success": result["success"],
        "workflow": result,
    }


# ==================== 设备控制 API ====================


@app.get("/api/v1/devices", tags=["设备控制"])
async def list_devices(device_type: Optional[str] = None):
    dtype = None
    if device_type:
        try:
            dtype = DeviceType(device_type)
        except ValueError:
            pass

    devices = sdk.no_ui_adapter.list_devices(dtype)
    return {
        "success": True,
        "count": len(devices),
        "devices": [
            {
                "id": d.id,
                "name": d.name,
                "type": d.device_type.value,
                "protocol": d.protocol.value,
                "address": d.address,
                "online": d.online,
                "state": d.state,
            }
            for d in devices
        ],
    }


@app.get("/api/v1/devices/{device_id}", tags=["设备控制"])
async def get_device(device_id: str):
    device = sdk.no_ui_adapter.get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="设备不存在")

    return {
        "success": True,
        "device": {
            "id": device.id,
            "name": device.name,
            "type": device.device_type.value,
            "protocol": device.protocol.value,
            "address": device.address,
            "online": device.online,
            "state": device.state,
        },
    }


@app.post("/api/v1/devices/command", tags=["设备控制"])
async def send_command(request: DeviceCommandRequest):
    sdk.no_ui_adapter.connect()
    result = sdk.no_ui_adapter.send_command(request.device_id, request.command, **request.params)

    return {
        "success": result.success,
        "device_id": result.device_id,
        "command": result.command,
        "message": result.message,
        "new_state": result.new_state,
        "error": result.error,
    }


@app.post("/api/v1/devices/batch-command", tags=["设备控制"])
async def send_batch_commands(request: BatchCommandRequest):
    sdk.no_ui_adapter.connect()
    result = sdk.no_ui_adapter.send_batch_commands(request.commands)

    return {
        "success": result.failed_count == 0,
        "total": result.total,
        "success_count": result.success_count,
        "failed_count": result.failed_count,
        "results": [
            {
                "success": r.success,
                "device_id": r.device_id,
                "command": r.command,
                "message": r.message,
            }
            for r in result.results
        ],
    }


@app.get("/api/v1/scenes", tags=["设备控制"])
async def list_scenes():
    scenes = sdk.no_ui_adapter.list_scenes()
    return {
        "success": True,
        "count": len(scenes),
        "scenes": [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "command_count": len(s.commands),
            }
            for s in scenes
        ],
    }


@app.post("/api/v1/scenes/{scene_id}/execute", tags=["设备控制"])
async def execute_scene(scene_id: str):
    sdk.no_ui_adapter.connect()
    result = sdk.no_ui_adapter.execute_scene(scene_id)

    return {
        "success": result.failed_count == 0,
        "scene_id": scene_id,
        "total": result.total,
        "success_count": result.success_count,
        "failed_count": result.failed_count,
    }


@app.post("/api/v1/intent/to-command", tags=["设备控制"])
async def intent_to_command(intent: str, device_type: str = "unknown"):
    command = sdk.no_ui_adapter.convert_intent_to_command(intent, device_type)
    return {
        "success": True,
        "intent": intent,
        "device_type": device_type,
        "command": command,
    }


# ==================== 智能体联邦 API ====================


@app.get("/api/v1/agents", tags=["智能体联邦"])
async def list_agents(status: Optional[str] = None):
    agent_status = None
    if status:
        try:
            agent_status = AgentStatus(status)
        except ValueError:
            pass

    agents = sdk.agent_federation.list_agents(agent_status)

    return {
        "success": True,
        "count": len(agents),
        "agents": [
            {
                "id": a.agent_id,
                "name": a.name,
                "status": a.status.value,
                "capabilities": a.capabilities,
                "load": round(a.load, 2),
                "intent_keywords": a.intent_keywords,
            }
            for a in agents
        ],
    }


@app.post("/api/v1/agents/register", tags=["智能体联邦"])
async def register_agent(request: AgentRegisterRequest):
    from ghost_hub_sdk.components.agent_federation import Agent

    agent = Agent(
        agent_id=request.agent_id,
        name=request.name,
        capabilities=request.capabilities,
        intent_keywords=request.intent_keywords,
    )

    result = sdk.agent_federation.register_agent(agent)

    return {
        "success": result,
        "agent_id": request.agent_id,
        "message": "注册成功" if result else "注册失败",
    }


@app.get("/api/v1/agents/find", tags=["智能体联邦"])
async def find_agent(intent: str):
    agent = sdk.agent_federation.find_agent(intent)
    if not agent:
        raise HTTPException(status_code=404, detail="未找到匹配的智能体")

    return {
        "success": True,
        "agent": {
            "id": agent.agent_id,
            "name": agent.name,
            "status": agent.status.value,
            "capabilities": agent.capabilities,
            "load": round(agent.load, 2),
        },
    }


@app.post("/api/v1/tasks/distribute", tags=["智能体联邦"])
async def distribute_tasks(request: TaskDistributeRequest):
    from ghost_hub_sdk.components.agent_federation import Task as FedTask

    sdk.agent_federation.connect()

    tasks = [
        FedTask(
            task_id=t.get("task_id", f"task_{i}"),
            description=t.get("description", ""),
            priority=t.get("priority", 0),
            dependencies=t.get("dependencies", []),
        )
        for i, t in enumerate(request.tasks)
    ]

    results = sdk.agent_federation.distribute_tasks(tasks)

    return {
        "success": True,
        "total": len(results),
        "distributions": [
            {
                "task_id": r.task_id,
                "assigned_agent": r.assigned_agent,
                "success": r.success,
                "message": r.message,
            }
            for r in results
        ],
    }


@app.get("/api/v1/sessions", tags=["智能体联邦"])
async def list_sessions(status: Optional[str] = None):
    sessions = sdk.agent_federation.list_sessions(status)

    return {
        "success": True,
        "count": len(sessions),
        "sessions": [
            {
                "id": s.id,
                "task": s.task,
                "status": s.status,
                "participants": s.participants,
                "created_at": datetime.fromtimestamp(s.created_at).isoformat(),
            }
            for s in sessions
        ],
    }


@app.post("/api/v1/sessions/create", tags=["智能体联邦"])
async def create_session(task: str, participants: Optional[str] = None):
    participant_list = participants.split(",") if participants else None

    session = sdk.agent_federation.create_session(task, participant_list)

    return {
        "success": True,
        "session": {
            "id": session.id,
            "task": session.task,
            "status": session.status,
            "participants": session.participants,
        },
    }


# ==================== 统计 API ====================


@app.get("/api/v1/stats", tags=["统计"])
async def get_stats():
    stats = sdk.get_stats()
    return {
        "success": True,
        "stats": stats,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
