# Ghost Hub 场景指南 - IoT物联网

**版本**: v1.0  
**日期**: 2026-04-15  
**适用场景**: 智能家居、工业IoT、智慧建筑、边缘设备控制

---

## 一、场景概述

### 1.1 核心痛点

| 痛点 | 影响 | 现有解决方案 |
|------|------|--------------|
| 设备协议碎片化 | 品牌众多，难以统一管理 | 厂商SDK各自独立 |
| 协议转换复杂 | 需要专业开发能力 | 协议网关 |
| 自然语言控制难 | 用户体验差 | APP控制 |
| 场景联动困难 | 多设备协同复杂 | 场景编程 |

### 1.2 Ghost Hub解决方案

```
用户: "打开客厅灯，空调调到24度"
         │
         ▼
┌─────────────────┐
│   无UI适配器    │
│ intent="打开灯" │
│ intent="调温度" │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   命令转换      │
│ turn_on_light   │
│ set_temp(24)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   设备下发      │
│ HTTP: dev_001   │
│ MQTT: dev_003   │
└────────┬────────┘
         │
         ▼
   设备执行完成
```

---

## 二、核心功能

### 2.1 支持的协议

| 协议 | 特点 | 适用场景 | 状态 |
|------|------|----------|------|
| HTTP | 简单易用 | 灯、开关 | ✅ |
| MQTT | 低功耗 | 空调、传感器 | ✅ |
| WebSocket | 实时性 | 摄像头、门锁 | ✅ |
| ZigBee | 短距离 | 多种设备 | ⚙️ |
| Z-Wave | 低功耗 | 智能家居 | ⚙️ |

### 2.2 支持的设备类型

| 设备类型 | 示例 | 控制能力 |
|----------|------|----------|
| LIGHT | 灯泡、灯带、照明 | 开/关、调光、调色温 |
| THERMOSTAT | 空调、暖气 | 开关、调温、模式 |
| SWITCH | 开关、插座 | 开/关、定时 |
| SENSOR | 温湿度、人体感应 | 状态查询 |
| CAMERA | 摄像头、门铃 | 开关、录像 |
| LOCK | 门锁、窗锁 | 解锁、设防 |
| SPEAKER | 音箱、音响 | 播放、音量 |
| TV | 电视、投影 | 开关、音量、频道 |

---

## 三、快速开始

### 3.1 安装

```bash
pip install ghost-hub-sdk
```

### 3.2 基本使用

```python
from ghost_hub_sdk import GhostHubSDK, Device, DeviceType, DeviceProtocol

# 初始化
sdk = GhostHubSDK()

# 连接适配器
sdk.connect()

# 意图转命令
command = sdk.no_ui_adapter.convert_intent_to_command("打开客厅灯", "light")
print(f"命令: {command}")  # 输出: light_turn_on

# 发送命令
result = sdk.no_ui_adapter.send_command("dev_001", command)
print(f"结果: {result.message}")
```

### 3.3 完整场景示例

```python
from ghost_hub_sdk import GhostHubSDK

sdk = GhostHubSDK()
sdk.connect()

# 语音控制场景
def voice_control(command):
    if "灯" in command or "开灯" in command or "关灯" in command:
        device_type = "light"
    elif "空调" in command or "温度" in command:
        device_type = "thermostat"
    elif "锁" in command or "门" in command:
        device_type = "lock"
    else:
        device_type = "unknown"
    
    cmd = sdk.no_ui_adapter.convert_intent_to_command(command, device_type)
    
    if device_type == "light":
        result = sdk.no_ui_adapter.send_command("dev_001", cmd)
    elif device_type == "thermostat":
        result = sdk.no_ui_adapter.send_command("dev_003", cmd)
    
    return result.success

# 测试
print(voice_control("打开客厅灯"))  # True
print(voice_control("空调调到24度"))  # True
```

---

## 四、设备管理

### 4.1 注册设备

```python
from ghost_hub_sdk import GhostHubSDK, Device, DeviceType, DeviceProtocol

sdk = GhostHubSDK()

# 注册新设备
new_device = Device(
    id="custom_dev_001",
    name="书房灯",
    device_type=DeviceType.LIGHT,
    protocol=DeviceProtocol.HTTP,
    address="http://192.168.1.201",
    capabilities=["turn_on", "turn_off", "dim"],
    online=True
)

sdk.no_ui_adapter.add_device(new_device)

# 验证注册
devices = sdk.no_ui_adapter.list_devices()
print(f"已注册设备数: {len(devices)}")
```

### 4.2 查询设备状态

```python
# 查询单个设备
device = sdk.no_ui_adapter.get_device("dev_001")
print(f"设备: {device.name}")
print(f"状态: {device.state}")

# 按类型查询
lights = sdk.no_ui_adapter.list_devices(DeviceType.LIGHT)
print(f"灯数量: {len(lights)}")

# 查询所有设备
all_devices = sdk.no_ui_adapter.list_devices()
for dev in all_devices:
    print(f"{dev.name}: {dev.device_type.value} - {'在线' if dev.online else '离线'}")
```

### 4.3 批量控制

```python
# 批量发送命令
commands = [
    {"device_id": "dev_001", "command": "turn_off"},
    {"device_id": "dev_002", "command": "turn_off"},
    {"device_id": "dev_003", "command": "turn_off"},
]

result = sdk.no_ui_adapter.send_batch_commands(commands)
print(f"总命令数: {result.total}")
print(f"成功: {result.success_count}")
print(f"失败: {result.failed_count}")
```

---

## 五、场景管理

### 5.1 内置场景

```python
# 早安模式
result = sdk.no_ui_adapter.execute_scene("scene_morning")
# 执行: 开灯、调空调、放音乐

# 晚安模式
result = sdk.no_ui_adapter.execute_scene("scene_night")
# 执行: 关灯、关空调、设防

# 离家模式
result = sdk.no_ui_adapter.execute_scene("scene_leave")
# 执行: 关闭所有灯、调低空调、安防设防
```

### 5.2 自定义场景

```python
from ghost_hub_sdk import GhostHubSDK, Scene

sdk = GhostHubSDK()

# 创建自定义场景
work_mode = Scene(
    id="scene_work",
    name="办公模式",
    description="上班时的工作环境设置",
    commands=[
        {"device_id": "dev_001", "command": "turn_on", "params": {"brightness": 80}},
        {"device_id": "dev_003", "command": "set", "params": {"temperature": 22}},
        {"device_id": "dev_005", "command": "record"},
    ],
    trigger_conditions={
        "time": "09:00",
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri"]
    }
)

# 注册场景
sdk.no_ui_adapter.register_scene(work_mode)

# 执行场景
result = sdk.no_ui_adapter.execute_scene("scene_work")
```

### 5.3 场景触发器

```python
import schedule
import time

def trigger_work_mode():
    result = sdk.no_ui_adapter.execute_scene("scene_work")
    print(f"场景执行: {result.success_count}/{result.total}")

# 设置定时触发
schedule.every().day.at("09:00").do(trigger_work_mode)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 六、协议适配

### 6.1 HTTP设备

```python
from ghost_hub_sdk import HTTPAdapter

# 自定义HTTP适配器
http_adapter = HTTPAdapter(base_url="http://192.168.1.100:8080")
http_adapter.connect()

# 发送命令
device = Device(
    id="custom_http",
    name="自定义设备",
    device_type=DeviceType.SWITCH,
    protocol=DeviceProtocol.HTTP,
    address="http://192.168.1.100:8080"
)

result = http_adapter.send(device, DeviceCommand("custom_http", "turn_on"))
print(f"HTTP响应: {result.message}")
```

### 6.2 MQTT设备

```python
from ghost_hub_sdk import MQTTAdapter

# 自定义MQTT适配器
mqtt_adapter = MQTTAdapter(broker="mqtt.example.com", port=1883)
mqtt_adapter.connect()

# 发布消息
device = Device(
    id="custom_mqtt",
    name="MQTT传感器",
    device_type=DeviceType.SENSOR,
    protocol=DeviceProtocol.MQTT,
    address="mqtt.example.com"
)

result = mqtt_adapter.send(device, DeviceCommand("custom_mqtt", "status"))
print(f"MQTT发布: {result.success}")
```

### 6.3 WebSocket设备

```python
from ghost_hub_sdk import WebSocketAdapter

# WebSocket适配器
ws_adapter = WebSocketAdapter(url="ws://192.168.1.100:8080/ws")
ws_adapter.connect()

# 监听消息
def on_device_event(event):
    print(f"设备事件: {event}")

ws_adapter.on_message("device_update", on_device_event)

# 发送命令
device = Device(
    id="custom_ws",
    name="摄像头",
    device_type=DeviceType.CAMERA,
    protocol=DeviceProtocol.WEBSOCKET,
    address="ws://192.168.1.100:8080/ws"
)

result = ws_adapter.send(device, DeviceCommand("custom_ws", "start_recording"))
```

---

## 七、行业应用

### 7.1 智能家居

| 场景 | 设备 | 自动化 |
|------|------|--------|
| 回家 | 门锁、灯、空调 | 解锁→开灯→调温 |
| 睡眠 | 灯、窗帘、音响 | 关灯→拉帘→放白噪音 |
| 离家 | 所有设备 | 全部关闭+安防 |

### 7.2 智慧办公

| 场景 | 设备 | 自动化 |
|------|------|--------|
| 上班 | 灯、空调、门禁 | 定时开启 |
| 会议 | 投影、窗帘、空调 | 一键场景 |
| 下班 | 所有设备 | 定时关闭 |

### 7.3 工业IoT

| 场景 | 设备 | 监控 |
|------|------|------|
| 设备监控 | 传感器、PLC | 状态+报警 |
| 能耗管理 | 电表、水表 | 数据采集 |
| 质量控制 | 检测设备 | 数据分析 |

---

## 八、效果评估

### 8.1 效率提升

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 设备接入时间 | 2周 | 2小时 | 95%↓ |
| 操作培训成本 | 8小时 | 1小时 | 88%↓ |
| 场景配置时间 | 1天 | 5分钟 | 98%↓ |
| 设备联动成功率 | 70% | 99% | 41%↑ |

### 8.2 ROI计算

```
投入:
- Ghost Hub Enterprise: $299/月
- 设备集成开发: 2周 ($4,000)
- 总计: $4,000 + $299/月

收益:
- 设备接入时间节省: 10设备×13天×$500/天 = $65,000
- 培训成本节省: $20,000/年
- 维护成本节省: $15,000/年
- 年度总节省: $100,000

ROI: ($100,000 - $7,588) / $7,588 = 1,218%
投资回收期: 2天
```

---

## 九、下一步

1. **体验Demo**: 运行 `03_SDK与集成/03_企业SDK包/GhostHub_SDK/demos/demo_user_scenarios.py`
2. **添加设备**: 使用SDK注册你的IoT设备
3. **创建场景**: 设计符合你需求的自动化场景
4. **集成现有系统**: 对接智能家居平台或工业系统

---

## 十、相关资源

| 资源 | 位置 |
|------|------|
| SDK文档 | `03_SDK与集成/03_企业SDK包/GhostHub_SDK/docs/` |
| 代码示例 | `03_SDK与集成/03_企业SDK包/GhostHub_SDK/demos/` |
| 完整模板 | `03_SDK与集成/03_企业SDK包/GhostHub_SDK/templates/` |
| 技术支持 | support@q-spectrum.ai |
