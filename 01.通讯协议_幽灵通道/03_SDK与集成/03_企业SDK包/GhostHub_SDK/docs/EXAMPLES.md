# Ghost Hub SDK - 完整示例代码

本文档提供 Ghost Hub SDK 的完整使用示例，涵盖各种应用场景。

## 目录

1. [基础使用](#1-基础使用)
2. [安全集成](#2-安全集成)
3. [并发场景](#3-并发场景)
4. [记忆与存储](#4-记忆与存储)
5. [工作流编排](#5-工作流编排)
6. [协议通信](#6-协议通信)
7. [企业级应用](#7-企业级应用)

---

## 1. 基础使用

### 1.1 快速初始化

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

# 最简初始化
sdk = GhostHubSDK()

# 自定义配置
config = GhostHubConfig(
    storage_path="./data",
    log_level="INFO",
    enable_cache=True,
    similarity_threshold=0.7
)
sdk = GhostHubSDK(config)
```

### 1.2 执行意图

```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()

# 单意图执行
result = sdk.execute_workflow("打开客厅灯")

if result["success"]:
    print(f"执行成功: {result['message']}")
    print(f"工作流ID: {result['workflow_id']}")
    print(f"耗时: {result['execution_time']:.3f}s")
```

### 1.3 批量执行

```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()

intents = [
    "打开客厅灯",
    "关闭卧室灯",
    "调节温度到24度",
    "播放音乐",
    "关闭窗帘"
]

results = []
for intent in intents:
    result = sdk.execute_workflow(intent)
    results.append(result)
    
# 统计
success_count = sum(1 for r in results if r["success"])
print(f"成功率: {success_count}/{len(results)}")
```

---

## 2. 安全集成

### 2.1 API Key 认证

```python
from ghost_hub_sdk.security import SimpleAuth, AuthConfig

auth = SimpleAuth(AuthConfig())

# 生成新 Key
api_key = auth.generate_api_key()
auth.add_api_key(
    api_key,
    name="my_application",
    permissions=["read", "write"]
)

# 验证 Key
key_info = auth.validate_api_key(api_key)
if key_info:
    print(f"用户: {key_info['name']}")
    print(f"权限: {key_info['permissions']}")

# 权限检查
if auth.has_permission(api_key, "admin"):
    print("有管理员权限")
else:
    print("权限不足")
```

### 2.2 完整请求验证流程

```python
from ghost_hub_sdk.security import SimpleAuth, RateLimiter, InputValidator
from ghost_hub_sdk import GhostHubSDK

def process_request(api_key: str, intent_text: str, client_id: str):
    """
    完整的请求处理流程，包含认证、限流、验证
    """
    # 1. 初始化组件
    auth = SimpleAuth()
    limiter = RateLimiter(requests_per_minute=60, burst=10)
    sdk = GhostHubSDK()
    
    # 2. 认证检查
    key_info = auth.validate_api_key(api_key)
    if not key_info:
        return {"error": "无效的API Key", "status": 401}
    
    # 3. 限流检查
    if not limiter.check(client_id):
        remaining = limiter.get_remaining(client_id)
        return {"error": f"请求过于频繁，剩余: {remaining}", "status": 429}
    
    # 4. 输入验证
    if not InputValidator.validate_intent_text(intent_text):
        return {"error": "无效的意图文本", "status": 400}
    
    # 5. 消毒处理
    safe_intent = InputValidator.sanitize_text(intent_text)
    
    # 6. 执行工作流
    result = sdk.execute_workflow(safe_intent)
    
    return {
        "result": result,
        "remaining": limiter.get_remaining(client_id),
        "status": 200
    }

# 使用示例
response = process_request(
    api_key="ghsk_xxx",
    intent_text="打开客厅灯",
    client_id="client_001"
)
print(response)
```

### 2.3 敏感数据保护

```python
from ghost_hub_sdk.security import SensitiveDataProtector

protector = SensitiveDataProtector()

# 字典脱敏
sensitive_data = {
    "username": "admin",
    "password": "super_secret_123",
    "api_key": "sk-live-abc123xyz",
    "email": "admin@example.com",
    "credit_card": "4111-1111-1111-1111"
}

masked = protector.mask_dict(sensitive_data)
print("脱敏后:")
for key, value in masked.items():
    print(f"  {key}: {value}")

# 日志脱敏
log_message = protector.safe_log(
    "User login attempt",
    {"username": "john", "password": "secret123", "ip": "192.168.1.1"}
)
print(f"安全日志: {log_message}")
```

### 2.4 FastAPI 集成

```python
from fastapi import FastAPI, HTTPException, Header, Depends
from typing import Optional
from ghost_hub_sdk.security import SimpleAuth, RateLimiter, InputValidator

app = FastAPI()

# 安全组件
auth = SimpleAuth()
limiter = RateLimiter(requests_per_minute=60)

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="缺少API Key")
    if not auth.validate_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="无效的API Key")
    return x_api_key

@app.post("/api/execute")
async def execute_intent(
    intent: str,
    api_key: str = Depends(verify_api_key)
):
    # 限流检查
    if not limiter.check(api_key):
        raise HTTPException(status_code=429, detail="请求过于频繁")
    
    # 输入验证
    if not InputValidator.validate_intent_text(intent):
        raise HTTPException(status_code=400, detail="无效的意图")
    
    # 执行
    from ghost_hub_sdk import GhostHubSDK
    sdk = GhostHubSDK()
    result = sdk.execute_workflow(intent)
    
    return {
        "success": result["success"],
        "result": result,
        "remaining": limiter.get_remaining(api_key)
    }
```

---

## 3. 并发场景

### 3.1 多线程执行

```python
from ghost_hub_sdk import GhostHubSDK
import threading
import queue

sdk = GhostHubSDK()
results = queue.Queue()

def worker(intent: str, thread_id: int):
    """工作线程"""
    try:
        result = sdk.execute_workflow(intent)
        results.put({"thread": thread_id, "result": result, "error": None})
    except Exception as e:
        results.put({"thread": thread_id, "result": None, "error": str(e)})

# 准备任务
tasks = [
    ("打开客厅灯", 1),
    ("关闭卧室灯", 2),
    ("调节温度", 3),
    ("播放音乐", 4),
    ("关闭窗帘", 5),
]

# 启动线程
threads = []
for intent, thread_id in tasks:
    t = threading.Thread(target=worker, args=(intent, thread_id))
    threads.append(t)
    t.start()

# 等待完成
for t in threads:
    t.join()

# 收集结果
print("执行结果:")
while not results.empty():
    r = results.get()
    if r["error"]:
        print(f"  线程{r['thread']}: 错误 - {r['error']}")
    else:
        print(f"  线程{r['thread']}: {'成功' if r['result']['success'] else '失败'}")
```

### 3.2 线程安全的 Rate Limiter

```python
from ghost_hub_sdk.security import RateLimiter
import threading
import time

limiter = RateLimiter(requests_per_minute=100, burst=20)

def client_worker(client_id: str, request_count: int):
    """模拟客户端请求"""
    allowed = 0
    denied = 0
    
    for _ in range(request_count):
        if limiter.check(client_id):
            allowed += 1
        else:
            denied += 1
    
    return {"client": client_id, "allowed": allowed, "denied": denied}

# 并发测试
threads = []
clients = [f"client_{i}" for i in range(10)]

for client_id in clients:
    t = threading.Thread(target=lambda c=client_id: threads.append(
        threading.Thread(target=lambda: client_worker(c, 50))
    ))
    t.start()
    threads.append(t)

# 等待所有客户端完成
for t in threads:
    t.join()

# 统计
stats = limiter.get_stats()
print(f"跟踪的客户端数: {stats['tracked_keys']}")
```

### 3.3 线程安全的 Memory

```python
from ghost_hub_sdk.memory import GhostHubMemory
import threading

memory = GhostHubMemory()
lock = threading.Lock()

def concurrent_learner(thread_id: int):
    """并发学习偏好"""
    for i in range(100):
        key = f"user_{thread_id}_pref_{i % 10}"
        value = f"value_from_thread_{thread_id}_{i}"
        memory.learn_preference(key, value)

# 启动并发学习
threads = []
for i in range(10):
    t = threading.Thread(target=concurrent_learner, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# 检查结果
stats = memory.get_stats()
print(f"学习到的偏好数: {stats['preferences_count']}")
```

---

## 4. 记忆与存储

### 4.1 记忆层使用

```python
from ghost_hub_sdk.memory import GhostHubMemory

memory = GhostHubMemory()

# 记录意图执行
memory.record_intent("打开客厅灯", {
    "template": "lighting_control",
    "status": "completed",
    "workflow_id": "wf_123"
})

# 获取历史
history = memory.get_intent_history(limit=10)
for record in history:
    print(f"{record.intent_text} - {record.success}")

# 学习用户偏好
memory.learn_preference("user.lighting.brightness", 75)
memory.learn_preference("user.temperature", 24)
memory.learn_preference("user.scene", "movie_mode")

# 获取偏好
brightness = memory.get_preference("user.lighting.brightness", default=50)
print(f"用户亮度偏好: {brightness}")

# 设置上下文
memory.set_context("current_room", "living_room")
memory.set_context("time_of_day", "evening")

# 获取上下文
room = memory.get_context("current_room")
full_context = memory.get_full_context()
print(f"当前房间: {room}")
print(f"完整上下文: {full_context}")
```

### 4.2 JSON 存储

```python
from ghost_hub_sdk.storage import JSONStorage

storage = JSONStorage("my_data.json")

# 基本操作
storage.set("user_profile", {
    "name": "张三",
    "email": "zhangsan@example.com",
    "settings": {"theme": "dark", "lang": "zh-CN"}
})

storage.set("session_token", "abc123xyz")
storage.set("last_login", {"timestamp": 1234567890, "ip": "192.168.1.1"})

# 查询
if storage.exists("user_profile"):
    profile = storage.get("user_profile")
    print(f"用户: {profile['name']}")

# 列表查询
keys = storage.list_keys("user_*")
print(f"用户相关键: {keys}")

# 批量操作
storage.batch_set([
    ("key1", {"data": "value1"}),
    ("key2", {"data": "value2"}),
    ("key3", {"data": "value3"}),
])

# 删除
storage.delete("session_token")

# 统计
stats = storage.get_stats()
print(f"存储统计: {stats}")
```

### 4.3 SQLite 存储

```python
from ghost_hub_sdk.storage import SQLiteStorage

storage = SQLiteStorage("app_data.db")

# 基本操作
storage.set("config", {"debug": True, "log_level": "INFO"})
storage.set("cache", {"data": [1, 2, 3, 4, 5]})

# 版本控制
storage.save_version("config")
storage.save_version("config")

storage.set("config", {"debug": False, "log_level": "WARNING"})

# 获取版本历史
versions = storage.get_versions("config")
print(f"版本数: {len(versions)}")

# 恢复版本
if versions:
    storage.restore_version("config", versions[0]["version_id"])

# SQL 查询
results = storage.query(
    "SELECT * FROM storage WHERE key LIKE ?",
    ["config%"]
)
for row in results:
    print(f"Key: {row['key']}, Value: {row['value']}")

# 批量操作
storage.batch_set([
    ("batch_1", {"index": 1}),
    ("batch_2", {"index": 2}),
])

# 统计
stats = storage.get_stats()
print(f"总记录数: {stats['total_records']}")
```

---

## 5. 工作流编排

### 5.1 模板管理

```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()

# 获取可用模板
templates = sdk.get_available_templates()
print(f"可用模板数: {len(templates)}")

for template in templates[:5]:
    print(f"  - {template['template_name']}: {template['template_id']}")

# 获取模板详情
template_info = sdk.get_template_info("lighting_control")
if template_info:
    print(f"\n模板: {template_info['template_name']}")
    print(f"描述: {template_info.get('description', 'N/A')}")
    print(f"任务数: {len(template_info.get('tasks', []))}")
```

### 5.2 自定义模板

```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()

# 添加自定义模板
custom_template = {
    "template_id": "my_custom_workflow",
    "template_name": "我的自定义工作流",
    "description": "处理特定业务逻辑",
    "patterns": [
        "处理订单",
        "创建工单",
        "审批流程"
    ],
    "tasks": [
        {
            "task_id": "task_1",
            "task_name": "数据验证",
            "action": "validate",
            "params": {"required_fields": ["id", "amount"]}
        },
        {
            "task_id": "task_2",
            "task_name": "发送通知",
            "action": "notify",
            "params": {"channel": "email"}
        }
    ]
}

# 注册模板 (如果 SDK 支持)
# sdk.add_template(custom_template)
```

### 5.3 工作流引擎

```python
from ghost_hub_sdk.workflow_engine import create_workflow_engine, WorkflowStatus

engine = create_workflow_engine()

# 创建工作流
workflow = engine.create_workflow(
    name="数据处理流程",
    tasks=[
        {"id": "t1", "name": "获取数据", "action": "fetch"},
        {"id": "t2", "name": "处理数据", "action": "process"},
        {"id": "t3", "name": "保存结果", "action": "save"},
    ]
)

print(f"工作流ID: {workflow.workflow_id}")
print(f"状态: {workflow.status}")

# 执行工作流
result = engine.execute(workflow.workflow_id)
print(f"执行结果: {result}")

# 获取状态
status = engine.get_status(workflow.workflow_id)
print(f"最终状态: {status}")
```

---

## 6. 协议通信

### 6.1 MQTT 连接

```python
from ghost_hub_sdk.protocols import MQTTClient

def on_message(topic: str, payload: dict):
    """消息处理回调"""
    print(f"收到消息 [{topic}]: {payload}")

# 创建客户端
client = MQTTClient(
    broker="mqtt.example.com",
    port=1883,
    client_id="ghost_hub_client",
    username="user",
    password="pass"
)

# 连接
client.connect()

# 订阅主题
client.subscribe("home/+/status")
client.subscribe("devices/+/telemetry")

# 设置回调
client.set_callback(on_message)

# 发布消息
client.publish("home/living_room/light", {
    "state": "on",
    "brightness": 80
})

# 启动消息循环
client.loop_start()

# 保持连接
import time
time.sleep(60)

# 断开
client.loop_stop()
client.disconnect()
```

### 6.2 WebSocket 连接

```python
from ghost_hub_sdk.protocols import WebSocketClient
import json

def on_message(data: dict):
    """消息处理"""
    print(f"收到: {data}")

# 创建客户端
ws = WebSocketClient("wss://api.example.com/ws")

# 连接
ws.connect()

# 发送订阅
ws.send({
    "type": "subscribe",
    "channels": ["updates", "alerts"]
})

# 设置回调
ws.set_callback(on_message)

# 接收消息
while True:
    message = ws.receive()
    if message:
        print(f"Received: {message}")
```

---

## 7. 企业级应用

### 7.1 微服务架构

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig
from ghost_hub_sdk.security import SimpleAuth, RateLimiter, InputValidator
from ghost_hub_sdk.memory import GhostHubMemory
from ghost_hub_sdk.storage import SQLiteStorage
import logging

class GhostHubService:
    """企业级 Ghost Hub 服务"""
    
    def __init__(self, config: dict):
        # 配置
        self.config = GhostHubConfig(
            storage_path=config.get("storage_path", "./data"),
            log_level=config.get("log_level", "INFO"),
            similarity_threshold=config.get("similarity_threshold", 0.7)
        )
        
        # 核心组件
        self.sdk = GhostHubSDK(self.config)
        self.auth = SimpleAuth()
        self.limiter = RateLimiter(
            requests_per_minute=config.get("rate_limit", 1000),
            burst=config.get("burst", 100)
        )
        self.memory = GhostHubMemory()
        self.storage = SQLiteStorage(config.get("db_path", "service.db"))
        
        # 日志
        logging.basicConfig(level=self.config.log_level)
        self.logger = logging.getLogger(__name__)
        
    def handle_request(self, api_key: str, intent: str, client_id: str) -> dict:
        """处理请求的完整流程"""
        try:
            # 1. 认证
            if not self.auth.validate_api_key(api_key):
                return {"error": "认证失败", "status": 401}
            
            # 2. 限流
            if not self.limiter.check(client_id):
                return {"error": "请求过于频繁", "status": 429}
            
            # 3. 验证输入
            if not InputValidator.validate_intent_text(intent):
                return {"error": "无效的意图", "status": 400}
            
            # 4. 消毒
            safe_intent = InputValidator.sanitize_text(intent)
            
            # 5. 执行
            result = self.sdk.execute_workflow(safe_intent)
            
            # 6. 记录到记忆
            self.memory.record_intent(safe_intent, result)
            
            # 7. 返回结果
            return {
                "result": result,
                "remaining": self.limiter.get_remaining(client_id),
                "status": 200
            }
            
        except Exception as e:
            self.logger.error(f"处理请求失败: {e}")
            return {"error": str(e), "status": 500}

# 使用示例
service = GhostHubService({
    "storage_path": "./service_data",
    "db_path": "service.db",
    "rate_limit": 1000,
    "log_level": "INFO"
})

response = service.handle_request(
    api_key="ghsk_xxx",
    intent="打开客厅灯",
    client_id="client_001"
)
print(response)
```

### 7.2 高可用部署

```python
from ghost_hub_sdk import GhostHubSDK
from ghost_hub_sdk.storage import SQLiteStorage
import threading
import time

class HighAvailabilityGhostHub:
    """高可用 Ghost Hub 实现"""
    
    def __init__(self, primary_db: str, replica_dbs: list):
        self.primary = SQLiteStorage(primary_db)
        self.replicas = [SQLiteStorage(db) for db in replica_dbs]
        self.sdk = GhostHubSDK()
        self.lock = threading.Lock()
        self.current_replica = 0
        
    def read_from_replica(self):
        """从副本读取"""
        with self.lock:
            replica = self.replicas[self.current_replica]
            self.current_replica = (self.current_replica + 1) % len(self.replicas)
        return replica
        
    def write_to_primary(self, key: str, value: dict):
        """写入主库"""
        return self.primary.set(key, value)
    
    def execute_read(self, intent: str):
        """执行读取操作（使用副本）"""
        replica = self.read_from_replica()
        return replica.get(intent)
    
    def execute_write(self, key: str, value: dict):
        """执行写入操作（使用主库）"""
        return self.write_to_primary(key, value)
```

---

## 完整项目示例

```python
"""
完整的 Ghost Hub SDK 使用示例
包含认证、安全、执行、存储等所有功能
"""

from ghost_hub_sdk import GhostHubSDK, GhostHubConfig
from ghost_hub_sdk.security import (
    SimpleAuth, AuthConfig,
    RateLimiter, InputValidator,
    SensitiveDataProtector, SecurityChecker
)
from ghost_hub_sdk.memory import GhostHubMemory
from ghost_hub_sdk.storage import SQLiteStorage
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # 1. 初始化配置
    config = GhostHubConfig(
        storage_path="./ghost_hub_data",
        log_level="INFO",
        similarity_threshold=0.7
    )
    
    # 2. 初始化组件
    sdk = GhostHubSDK(config)
    auth = SimpleAuth(AuthConfig())
    limiter = RateLimiter(requests_per_minute=100, burst=20)
    memory = GhostHubMemory()
    storage = SQLiteStorage("ghost_hub.db")
    
    # 3. 创建 API Key
    api_key = auth.generate_api_key()
    auth.add_api_key(api_key, "demo_user", permissions=["read", "write"])
    
    logger.info(f"API Key 已创建: {api_key[:20]}...")
    
    # 4. 安全检查
    issues = SecurityChecker.check_all()
    if issues:
        logger.warning(f"发现 {len(issues)} 个安全问题")
        for issue in issues:
            logger.warning(f"  [{issue['severity']}] {issue['message']}")
    
    # 5. 处理用户请求
    client_id = "client_001"
    intent = "打开客厅灯并调节到50%亮度"
    
    # 验证
    if not limiter.check(client_id):
        logger.error("请求过于频繁")
        return
    
    if not InputValidator.validate_intent_text(intent):
        logger.error("无效的意图")
        return
    
    # 执行
    result = sdk.execute_workflow(intent)
    
    # 6. 记录到记忆
    memory.record_intent(intent, result)
    
    # 7. 保存到存储
    storage.set(f"workflow_{result['workflow_id']}", result)
    
    # 8. 返回结果
    logger.info(f"执行成功: {result['message']}")
    logger.info(f"工作流ID: {result['workflow_id']}")
    logger.info(f"执行时间: {result['execution_time']:.3f}s")
    
    # 9. 敏感数据保护示例
    sensitive = SensitiveDataProtector.mask_dict({
        "password": "secret123",
        "api_key": api_key
    })
    logger.info(f"脱敏数据: {sensitive}")
    
    # 10. 统计
    stats = {
        "memory": memory.get_stats(),
        "limiter": limiter.get_stats(),
        "storage": storage.get_stats()
    }
    logger.info(f"统计: {stats}")

if __name__ == "__main__":
    main()
```

---

## 运行示例

```bash
# 运行基础示例
python examples/basic_usage.py

# 运行安全示例
python examples/security_example.py

# 运行并发示例
python examples/concurrency_example.py

# 运行完整企业级示例
python examples/enterprise_example.py
```

---

*文档版本: v1.0.0*
*最后更新: 2026-04-15*
