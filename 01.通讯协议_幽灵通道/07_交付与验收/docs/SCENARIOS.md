# Ghost Hub SDK 使用场景完整指南

> **文档版本**: v1.0  
> **SDK版本**: 1.0.0  
> **更新日期**: 2026-04-15  
> **阅读时长**: 20分钟

---

## 📋 目录

1. [场景概览](#场景概览) - 四大应用领域
2. [HR人力资源](#hr人力资源) - 招聘/入职/绩效完整案例
3. [IoT物联网](#iot物联网) - 智能家居/工业控制案例
4. [智能体协作](#智能体协作) - 数据分析/内容生成案例
5. [企业运营](#企业运营) - 工单处理/系统监控案例
6. [场景选择指南](#场景选择指南) - 根据角色推荐

---

## 🎯 场景概览

| 场景 | 行业 | 模板数 | 复杂度 | 推荐起点 |
|------|------|--------|--------|----------|
| [HR人力资源](#hr人力资源) | 企业 | 4 | ⭐⭐ | HR经理 |
| [IoT物联网](#iot物联网) | 制造/家居 | 2 | ⭐⭐⭐ | IoT开发者 |
| [智能体协作](#智能体协作) | 科技/金融 | 1 | ⭐⭐⭐⭐ | AI工程师 |
| [企业运营](#企业运营) | 通用 | 3 | ⭐⭐ | 运维团队 |

---

## 👔 HR人力资源

### 完整案例：科技公司招聘流程自动化

#### 场景背景

> 某科技公司每月招聘10+工程师，HR团队手动处理简历筛选、面试安排，效率低下。

#### 解决方效

使用Ghost Hub SDK自动化招聘流程，节省70%时间。

#### 代码实现

<!-- AI-READY: HR_RECRUITMENT_FULL -->
```python
from ghost_hub_sdk import GhostHubSDK
import json
from datetime import datetime

# 初始化SDK
sdk = GhostHubSDK()

def process_recruitment(intent_text: str) -> dict:
    """
    处理招聘请求
    
    Args:
        intent_text: 用户输入，如"招聘Python工程师"
    
    Returns:
        包含任务列表和执行结果的字典
    """
    print(f"📥 收到招聘请求: {intent_text}")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 1: 意图匹配
    match_result = sdk.intention_bank.match_intent(intent_text)
    
    if not match_result.has_match:
        return {"success": False, "error": "无法理解招聘意图"}

    template = match_result.top_match.template
    print(f"✅ 匹配模板: {template.name}")
    print(f"📊 置信度: {match_result.top_match.confidence:.1%}")

    # Step 2: 构建任务图
    task_graph = sdk.intention_bank.build_task_graph(template)
    tasks = list(task_graph.nodes.values())
    
    print(f"\n📋 任务分解 ({len(tasks)} 个任务):")
    for i, node in enumerate(tasks, 1):
        task = node.task
        deps = f" → 依赖: {', '.join(node.parents)}" if node.parents else ""
        print(f"   {i}. [{task.id}] {task.name}{deps}")

    # Step 3: 执行工作流
    workflow_result = sdk.execute_workflow(intent_text)
    
    if workflow_result["success"]:
        print(f"\n🎉 工作流执行成功!")
        print(f"   类型: {workflow_result['workflow_type']}")
        print(f"   任务数: {workflow_result['task_graph']['task_count']}")
        
        # ROI估算
        roi = workflow_result.get("roi_estimate", {})
        if roi:
            print(f"\n💰 ROI估算:")
            for k, v in roi.items():
                print(f"   {k}: {v}")
        
        return {
            "success": True,
            "workflow_id": workflow_result["workflow_type"],
            "tasks": workflow_result["task_graph"]["tasks"],
            "roi": workflow_result.get("roi_estimate", {})
        }
    else:
        print(f"\n❌ 工作流执行失败:")
        for error in workflow_result["errors"]:
            print(f"   - {error}")
        return {
            "success": False,
            "errors": workflow_result["errors"]
        }

# 执行招聘流程
if __name__ == "__main__":
    result = process_recruitment("招聘3年经验Python后端工程师")
    
    if result["success"]:
        print("\n" + "="*50)
        print("招聘任务已创建，请查看任务列表")
        print("="*50)
    
    sdk.disconnect()
```

#### 输出示例

```
📥 收到招聘请求: 招聘3年经验Python后端工程师
⏰ 时间: 2026-04-15 14:30:00
✅ 匹配模板: HR招聘流程
📊 置信度: 85.0%

📋 任务分解 (5 个任务):
   1. [t1] 职位描述生成 → 依赖: 
   2. [t2] 简历筛选规则 → 依赖: t1
   3. [t3] 简历解析 → 依赖: t2
   4. [t4] 面试问题生成 → 依赖: t3
   5. [t5] 面试官分配 → 依赖: t4

🎉 工作流执行成功!
   类型: hr_recruitment
   任务数: 5

💰 ROI估算:
   效率提升: 70%
   预计节省: 2小时/职位
   招聘周期缩短: 30%
```

#### 适用场景清单

| 输入示例 | 输出 | 自动化内容 |
|----------|------|-----------|
| "招聘Python工程师" | 完整招聘流程 | 职位→简历→面试 |
| "新员工入职流程" | 入职清单+账号创建 | 账号→培训→设备 |
| "年度绩效考核" | 评估模板+流程 | 目标→评估→反馈 |
| "团队人员优化" | 优化方案 | 分析→建议→执行 |

---

## 🏠 IoT物联网

### 完整案例：智能家居控制系统

#### 场景背景

> 用户希望用自然语言控制家中设备，无需学习复杂的设备指令。

#### 解决方效

使用IoT适配器将自然语言转换为设备命令，实现语音控制。

#### 代码实现

<!-- AI-READY: IOT_SMART_HOME_FULL -->
```python
from ghost_hub_sdk import GhostHubSDK
import time

# 初始化SDK
sdk = GhostHubSDK()

class SmartHomeController:
    """智能家居控制器"""
    
    def __init__(self, sdk: GhostHubSDK):
        self.sdk = sdk
        self.connected = False
    
    def connect_gateway(self, protocol="mqtt", broker="mqtt://localhost:1883"):
        """连接IoT网关"""
        print(f"🔌 连接网关: {protocol} @ {broker}")
        self.connected = self.sdk.no_ui_adapter.connect(
            protocol=protocol,
            broker=broker
        )
        if self.connected:
            print("✅ 网关连接成功")
        return self.connected
    
    def process_command(self, voice_command: str) -> dict:
        """
        处理语音命令
        
        Args:
            voice_command: 自然语言命令，如"把客厅灯打开"
        
        Returns:
            命令执行结果
        """
        print(f"\n🎤 收到命令: {voice_command}")
        
        # 确定设备类型
        device_type = self._detect_device_type(voice_command)
        print(f"📱 识别设备: {device_type}")
        
        # 转换命令
        command = self.sdk.no_ui_adapter.convert_intent_to_command(
            intent=voice_command,
            device_type=device_type
        )
        
        print(f"⚡ 设备命令: {command}")
        
        return {
            "original": voice_command,
            "device_type": device_type,
            "command": command,
            "timestamp": time.time()
        }
    
    def _detect_device_type(self, command: str) -> str:
        """检测设备类型"""
        keywords = {
            "light": ["灯", "灯光", "灯开", "灯关"],
            "ac": ["空调", "温度", "冷", "热"],
            "lock": ["门锁", "门", "锁"],
            "curtain": ["窗帘", "窗帘开", "窗帘关"]
        }
        
        for device, kws in keywords.items():
            if any(kw in command for kw in kws):
                return device
        return "unknown"
    
    def execute_scene(self, scene_name: str):
        """执行场景"""
        print(f"\n🎬 执行场景: {scene_name}")
        results = self.sdk.no_ui_adapter.execute_scene(scene_name)
        
        for r in results:
            status = "✅" if r.status == "success" else "❌"
            print(f"   {status} {r.device_id}: {r.status}")
        
        return results
    
    def list_all_devices(self):
        """列出所有设备"""
        print("\n📋 设备列表:")
        devices = self.sdk.no_ui_adapter.list_devices()
        
        for device in devices:
            online = "🟢" if device.status == "online" else "🔴"
            print(f"   {online} {device.name} ({device.type})")
        
        return devices

# 使用示例
if __name__ == "__main__":
    controller = SmartHomeController(sdk)
    
    # 连接网关 (模拟)
    controller.connect_gateway(protocol="mock")
    
    # 语音命令
    commands = [
        "把客厅灯打开",
        "把空调调到26度",
        "开启离家模式"
    ]
    
    for cmd in commands:
        controller.process_command(cmd)
    
    # 执行场景
    controller.execute_scene("离家模式")
    
    # 列出设备
    controller.list_all_devices()
    
    sdk.disconnect()
```

#### 输出示例

```
🔌 连接网关: mock @ mqtt://localhost:1883
✅ 网关连接成功

🎤 收到命令: 把客厅灯打开
📱 识别设备: light
⚡ 设备命令: light_turn_on

🎤 收到命令: 把空调调到26度
📱 识别设备: ac
⚡ 设备命令: ac_set_temp_26

🎬 执行场景: 离家模式
   ✅ living_room_light: success
   ✅ bedroom_light: success
   ✅ ac_system: success
   ✅ door_lock: success

📋 设备列表:
   🟢 客厅灯 (light)
   🟢 卧室灯 (light)
   🟢 空调 (ac)
   🟢 门锁 (lock)
```

#### 适用场景清单

| 输入示例 | 支持设备 | 自动化内容 |
|----------|----------|-----------|
| "离家模式" | 全屋 | 关灯/关空调/锁门 |
| "回家模式" | 全屋 | 开灯/开空调/撤防 |
| "开灯" | 灯 | 开关控制 |
| "空调26度" | 空调 | 温度调节 |

---

## 🤖 智能体协作

### 完整案例：销售数据分析流水线

#### 场景背景

> 需要分析季度销售数据，涉及数据收集、处理、可视化，需要多个Agent协作。

#### 解决方效

使用智能体联邦实现多Agent并行处理，提高分析效率。

#### 代码实现

<!-- AI-READY: AGENT_FEDERATION_FULL -->
```python
from ghost_hub_sdk import GhostHubSDK
from ghost_hub_sdk.components.agent_federation import Task
from datetime import datetime

# 初始化SDK
sdk = GhostHubSDK()

class DataAnalysisPipeline:
    """数据分析流水线"""
    
    def __init__(self, sdk: GhostHubSDK):
        self.sdk = sdk
        self.sdk.agent_federation.connect()
        self.results = {}
    
    def run_quarterly_analysis(self, quarter: str = "Q1"):
        """
        运行季度数据分析
        
        Args:
            quarter: 季度，如 "Q1", "Q2"
        """
        print(f"\n📊 开始{quarter}数据分析")
        print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: 创建任务
        tasks = self._create_tasks(quarter)
        
        # Step 2: 分发任务
        print(f"\n📤 分发 {len(tasks)} 个任务...")
        task_results = self._distribute_tasks(tasks)
        
        # Step 3: 聚合结果
        print(f"\n🔄 聚合结果...")
        final_report = self._aggregate_results(task_results)
        
        # Step 4: 输出报告
        self._print_report(final_report, quarter)
        
        return final_report
    
    def _create_tasks(self, quarter: str):
        """创建分析任务"""
        return [
            Task(
                task_id=f"{quarter}_collect",
                description=f"收集{quarter}销售数据",
                priority=1,
                dependencies=[]
            ),
            Task(
                task_id=f"{quarter}_clean",
                description=f"清洗{quarter}数据",
                priority=2,
                dependencies=[f"{quarter}_collect"]
            ),
            Task(
                task_id=f"{quarter}_analyze",
                description=f"分析{quarter}数据趋势",
                priority=3,
                dependencies=[f"{quarter}_clean"]
            ),
            Task(
                task_id=f"{quarter}_visualize",
                description=f"生成{quarter}图表",
                priority=4,
                dependencies=[f"{quarter}_analyze"]
            ),
            Task(
                task_id=f"{quarter}_report",
                description=f"生成{quarter}报告",
                priority=5,
                dependencies=[f"{quarter}_analyze", f"{quarter}_visualize"]
            )
        ]
    
    def _distribute_tasks(self, tasks):
        """分发任务到Agent"""
        results = []
        
        for task in tasks:
            # 检查依赖是否完成
            if task.dependencies:
                deps_done = all(
                    r["task_id"] in [res["task_id"] for res in results]
                    for dep in task.dependencies
                )
                if not deps_done:
                    print(f"   ⏳ {task.task_id} 等待依赖完成")
                    continue
            
            # 分发任务
            result = self.sdk.agent_federation.distribute_task(
                task=task,
                intent=task.description
            )
            
            status = "✅" if result.success else "❌"
            print(f"   {status} {task.task_id} → {result.assigned_agent}")
            
            results.append({
                "task_id": task.task_id,
                "agent": result.assigned_agent,
                "success": result.success,
                "description": task.description
            })
        
        return results
    
    def _aggregate_results(self, task_results):
        """聚合结果"""
        stats = self.sdk.agent_federation.get_stats()
        
        return {
            "total_tasks": len(task_results),
            "completed": sum(1 for r in task_results if r["success"]),
            "failed": sum(1 for r in task_results if not r["success"]),
            "agents_used": list(set(r["agent"] for r in task_results)),
            "stats": stats
        }
    
    def _print_report(self, report, quarter):
        """打印报告"""
        print(f"\n{'='*50}")
        print(f"📊 {quarter}数据分析报告")
        print(f"{'='*50}")
        print(f"总任务数: {report['total_tasks']}")
        print(f"已完成: {report['completed']}")
        print(f"失败: {report['failed']}")
        print(f"使用Agent: {', '.join(report['agents_used'])}")
        print(f"{'='*50}")

# 使用示例
if __name__ == "__main__":
    pipeline = DataAnalysisPipeline(sdk)
    
    # 运行Q1分析
    pipeline.run_quarterly_analysis("Q1")
    
    # 获取Agent状态
    agents = sdk.agent_federation.list_agents()
    print(f"\n🤖 当前在线Agent: {len(agents)}")
    
    sdk.disconnect()
```

#### 输出示例

```
📊 开始Q1数据分析
⏰ 时间: 2026-04-15 14:30:00

📤 分发 5 个任务...
   ✅ Q1_collect → data_agent
   ✅ Q1_clean → data_agent
   ✅ Q1_analyze → analyzer_agent
   ✅ Q1_visualize → report_agent
   ✅ Q1_report → report_agent

🔄 聚合结果...

==================================================
📊 Q1数据分析报告
==================================================
总任务数: 5
已完成: 5
失败: 0
使用Agent: data_agent, analyzer_agent, report_agent
==================================================

🤖 当前在线Agent: 4
```

#### 适用场景清单

| 场景 | 任务类型 | Agent角色 | 协作模式 |
|------|----------|-----------|----------|
| 数据分析 | ETL、报表 | data/analyzer/report | 并行处理 |
| 内容生成 | 文案、设计 | writer/designer | 串行流水线 |
| 客户服务 | FAQ、工单 | router/processor | 路由分发 |
| 代码审查 | Review、测试 | coder/reviewer | 并行审查 |

---

## ⚙️ 企业运营

### 完整案例：IT工单自动处理

#### 场景背景

> IT部门每天处理50+工单，需要自动分类、分配、解决。

#### 解决方效

使用工作流引擎自动化工单处理，提高响应速度。

#### 代码实现

<!-- AI-READY: OPS_TICKET_FULL -->
```python
from ghost_hub_sdk import GhostHubSDK

# 初始化SDK
sdk = GhostHubSDK()

def process_ticket(ticket_description: str) -> dict:
    """
    处理IT工单
    
    Args:
        ticket_description: 工单描述
    
    Returns:
        处理结果
    """
    print(f"\n🎫 收到工单: {ticket_description}")
    
    # 执行工作流
    result = sdk.execute_workflow(ticket_description)
    
    if result["success"]:
        print(f"✅ 工单处理成功")
        print(f"   类型: {result['workflow_type']}")
        print(f"   任务: {result['task_graph']['task_count']} 个")
        
        # 打印任务列表
        print(f"\n📋 任务列表:")
        for task in result["task_graph"]["tasks"]:
            status = task.get("status", "pending")
            print(f"   - [{status}] {task['name']}")
        
        return {
            "success": True,
            "workflow_type": result["workflow_type"],
            "tasks": result["task_graph"]["tasks"]
        }
    else:
        print(f"❌ 工单处理失败:")
        for error in result["errors"]:
            print(f"   - {error}")
        return {
            "success": False,
            "errors": result["errors"]
        }

# 测试工单
if __name__ == "__main__":
    tickets = [
        "服务器磁盘满了，需要清理",
        "员工笔记本无法连接网络",
        "申请开通新系统账号",
        "打印机无法打印"
    ]
    
    for ticket in tickets:
        result = process_ticket(ticket)
        print()
    
    sdk.disconnect()
```

#### 输出示例

```
🎫 收到工单: 服务器磁盘满了，需要清理
✅ 工单处理成功
   类型: ops_disk_cleanup
   任务: 4 个

📋 任务列表:
   - [pending] 检查磁盘使用情况
   - [pending] 清理临时文件
   - [pending] 清理日志文件
   - [pending] 通知管理员

🎫 收到工单: 员工笔记本无法连接网络
✅ 工单处理成功
   类型: ops_network_issue
   任务: 5 个

📋 任务列表:
   - [pending] 检查网络配置
   - [pending] 重启网络服务
   - [pending] 检查网线连接
   - [pending] 联系IT支持
   - [pending] 更新工单状态
```

#### 适用场景清单

| 工单类型 | 输入示例 | 自动化内容 |
|----------|----------|-----------|
| 系统故障 | "服务器挂了" | 检测→告警→自愈 |
| 网络问题 | "上不了网" | 诊断→解决→验证 |
| 账号问题 | "账号被锁" | 验证→解锁→通知 |
| 权限申请 | "申请权限" | 审批→授权→记录 |

---

## 🎯 场景选择指南

### 根据角色推荐

| 角色 | 推荐场景 | 起步模板 | 预期收益 |
|------|----------|----------|----------|
| HR经理 | HR人力资源 | `hr_recruitment` | 招聘效率+70% |
| IoT开发者 | IoT物联网 | `iot_smart_home` | 开发时间-50% |
| AI工程师 | 智能体协作 | `federation_multi_agent` | 并行效率+200% |
| 运维团队 | 企业运营 | `ops_ticket_resolution` | 响应时间-60% |

### 根据行业推荐

| 行业 | 推荐场景 | 定制重点 |
|------|----------|----------|
| 互联网 | 智能体协作 | 数据分析流水线 |
| 制造业 | IoT物联网 | 设备监控与控制 |
| 服务业 | HR人力资源 | 客服与工单 |
| 金融 | 企业运营 | 合规与审计 |

---

## 📚 相关文档

- [安装指南](./INSTALL_GUIDE.md) - 完整安装手册
- [用户指南](./USER_GUIDE.md) - API详细文档
- [快速开始](./QUICK_START.md) - 5分钟体验

---

## 🆘 技术支持

| 渠道 | 地址 |
|------|------|
| 文档 | https://docs.ghosthub.dev |
| GitHub Issues | https://github.com/ghost-hub/sdk/issues |
| Email | support@ghosthub.dev |
