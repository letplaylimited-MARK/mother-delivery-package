# Ghost Hub SDK 快速开始 (API v1.0.0)

> 5分钟快速体验 Ghost Hub SDK

> **⚠️ 重要提示**: 意图银行主要支持**中文**输入。使用中文可获得最佳匹配效果。

---

## 第一步：安装（30秒）

```bash
pip install ghost-hub-sdk
```

---

## 第二步：基础使用（2分钟）

### 2.1 初始化SDK

```python
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

# 最简初始化
sdk = GhostHubSDK()

# 或自定义配置
config = GhostHubConfig(
    intention_bank_enabled=True,
    no_ui_adapter_enabled=True,
    agent_federation_enabled=True,
    log_level="INFO"
)
sdk = GhostHubSDK(config)
```

### 2.2 执行工作流

```python
# HR工作流示例
result = sdk.execute_workflow("帮我优化招聘流程")

# 检查结果
if result["success"]:
    print(f"工作流类型: {result['workflow_type']}")
    print(f"任务数: {len(result['task_graph']['tasks'])}")
else:
    print(f"错误: {result['errors']}")
```

### 2.3 意图匹配

```python
# 自然语言匹配 - 返回 MatchResult
result = sdk.intention_bank.match_intent("开灯")

# 检查匹配
if result.has_match:
    top = result.top_match
    print(f"模板: {top.template.name}")
    print(f"置信度: {top.confidence:.2f}")
    print(f"相似度: {top.similarity:.2f}")
```

---

## 第三步：IoT集成（1分钟）

### 3.1 连接设备

```python
# 连接MQTT网关
sdk.no_ui_adapter.connect(protocol="mqtt")
```

### 3.2 发送命令

```python
# 自然语言转命令 - 返回字符串
command = sdk.no_ui_adapter.convert_intent_to_command(
    intent="把灯打开",
    device_type="light"
)

print(f"命令: {command}")  # 例如: light_turn_on
```

---

## 第四步：智能体协作（1分钟）

### 4.1 分发任务

```python
from ghost_hub_sdk.components.agent_federation import Task

# 创建任务
task = Task(
    task_id="task_001",
    description="分析销售数据",
    priority=1
)

# 分发到智能体 (参数为 intent 用于路由)
result = sdk.agent_federation.distribute_task(
    task=task,
    intent="数据分析"
)

print(f"分配给: {result.assigned_agent}")
print(f"成功: {result.success}")
```

### 4.2 获取统计

```python
# 获取智能体统计
stats = sdk.agent_federation.get_stats()

print(f"在线智能体: {stats['online_agents']}")
print(f"活跃会话: {stats['active_sessions']}")
```

---

## 第五步：清理资源

```python
# 断开连接
sdk.disconnect()
```

---

## 完整示例代码

```python
#!/usr/bin/env python3
"""
Ghost Hub SDK 快速开始示例 v1.0.0
"""

from ghost_hub_sdk import GhostHubSDK

def main():
    print("Ghost Hub SDK Quick Start\n")
    
    # 1. 初始化
    print("1. Initialize SDK...")
    sdk = GhostHubSDK()
    print("   Done\n")
    
    # 2. 执行HR工作流
    print("2. Execute HR workflow...")
    result = sdk.execute_workflow("招聘流程")
    if result["success"]:
        print(f"   Success! Tasks: {len(result['task_graph']['tasks'])}")
    print()
    
    # 3. 意图匹配
    print("3. Test intent matching...")
    match = sdk.intention_bank.match_intent("开灯")
    if match.has_match:
        print(f"   Matched: {match.top_match.template.name}")
        print(f"   Confidence: {match.top_match.confidence:.2f}")
    print()
    
    # 4. IoT命令
    print("4. Test IoT command...")
    command = sdk.no_ui_adapter.convert_intent_to_command("开灯", "light")
    print(f"   Command: {command}")
    print()
    
    # 5. 清理
    print("5. Cleanup...")
    sdk.disconnect()
    print("   Done!\n")
    
    print("Quick Start Complete!")

if __name__ == "__main__":
    main()
```

---

## 核心数据结构速查

| 类型 | 用途 | 关键属性 |
|------|------|----------|
| `MatchResult` | 意图匹配结果 | `has_match`, `top_match`, `matches` |
| `IntentMatch` | 单个匹配 | `confidence`, `template`, `similarity` |
| `Template` | 业务模板 | `id`, `name`, `tasks` |
| `TaskGraph` | 任务图 | `tasks`, `dependencies` |

---

## 下一步

| 场景 | 指南 |
|------|------|
| HR自动化 | [用户场景-HR](./SCENARIOS.md#hr) |
| IoT控制 | [用户场景-IoT](./SCENARIOS.md#iot) |
| 智能体协作 | [用户场景-Agent](./SCENARIOS.md#agent) |
| 企业部署 | [部署指南](../../04_企业部署/04_商业部署包/docker/DEPLOYMENT.md) |

---

## 常见问题

**Q: 导入报错？**
```bash
pip install ghost-hub-sdk
```

**Q: 意图不匹配？**
```python
# 检查 has_match
result = sdk.intention_bank.match_intent("某句话")
if not result.has_match:
    print("未找到匹配")

# 检查置信度
if result.top_match.confidence < 0.5:
    print("置信度太低")
```

**Q: 工作流执行失败？**
```python
result = sdk.execute_workflow("流程")
if not result["success"]:
    print(f"错误: {result['errors']}")
```
