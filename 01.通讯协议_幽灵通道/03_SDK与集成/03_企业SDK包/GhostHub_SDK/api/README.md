# Ghost Hub REST API

基于 FastAPI 的企业级AI工作流编排REST API

## 快速开始

### 1. 安装依赖

```bash
cd ghost_hub_sdk/api
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python -m ghost_hub_sdk.api.main
```

或双击 `start.bat`

### 3. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

### 意图银行

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/templates` | 列出所有模板 |
| GET | `/api/v1/templates/{id}` | 获取模板详情 |
| POST | `/api/v1/intent/match` | 匹配意图 |
| POST | `/api/v1/intent/multi-match` | 多意图匹配 |

### 设备控制

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/devices` | 列出设备 |
| GET | `/api/v1/devices/{id}` | 获取设备详情 |
| POST | `/api/v1/devices/command` | 发送命令 |
| POST | `/api/v1/devices/batch-command` | 批量命令 |
| GET | `/api/v1/scenes` | 列出场景 |
| POST | `/api/v1/scenes/{id}/execute` | 执行场景 |
| GET | `/api/v1/intent/to-command` | 意图转命令 |

### 智能体联邦

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/agents` | 列出智能体 |
| POST | `/api/v1/agents/register` | 注册智能体 |
| GET | `/api/v1/agents/find` | 查找智能体 |
| POST | `/api/v1/tasks/distribute` | 分发任务 |
| GET | `/api/v1/sessions` | 列出会话 |
| POST | `/api/v1/sessions/create` | 创建会话 |

### 工作流

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/v1/workflow/execute` | 执行工作流 |

## 示例请求

### 匹配意图

```bash
curl -X POST http://localhost:8000/api/v1/intent/match \
  -H "Content-Type: application/json" \
  -d '{"text": "帮我优化面试流程"}'
```

### 发送设备命令

```bash
curl -X POST http://localhost:8000/api/v1/devices/command \
  -H "Content-Type: application/json" \
  -d '{"device_id": "dev_001", "command": "turn_on"}'
```

### 执行工作流

```bash
curl -X POST http://localhost:8000/api/v1/workflow/execute \
  -H "Content-Type: application/json" \
  -d '{"intent_text": "打开客厅灯", "workflow_type": "iot"}'
```

## 运行测试

```bash
python test_api.py
```
