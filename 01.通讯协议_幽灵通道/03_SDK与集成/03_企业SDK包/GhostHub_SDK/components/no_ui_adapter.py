"""
无UI适配器组件 - 自包含实现
IoT设备集成、协议适配、命令转换
"""

import re
import hashlib
import time
import uuid
import asyncio
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum


class DeviceType(Enum):
    LIGHT = "light"
    THERMOSTAT = "thermostat"
    SWITCH = "switch"
    SENSOR = "sensor"
    CAMERA = "camera"
    LOCK = "lock"
    SPEAKER = "speaker"
    TV = "tv"
    UNKNOWN = "unknown"


class DeviceProtocol(Enum):
    HTTP = "http"
    MQTT = "mqtt"
    ZIGBEE = "zigbee"
    ZWAVE = "zwave"
    WEBSOCKET = "websocket"


@dataclass
class Device:
    id: str
    name: str
    device_type: DeviceType
    protocol: DeviceProtocol
    address: str
    state: Dict[str, Any] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)
    online: bool = True


@dataclass
class DeviceCommand:
    device_id: str
    command: str
    params: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class CommandResult:
    success: bool
    device_id: str
    command: str
    message: str
    new_state: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class BatchCommandResult:
    total: int
    success_count: int
    failed_count: int
    results: List[CommandResult]


@dataclass
class Scene:
    id: str
    name: str
    description: str
    commands: List[Dict[str, Any]]
    trigger_conditions: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IntentCommand:
    intent: str
    device_type: DeviceType
    action: str
    params: Dict[str, Any] = field(default_factory=dict)


class IntentCommandEngine:
    def __init__(self):
        self.action_mappings = {
            "打开": "turn_on",
            "开": "turn_on",
            "关闭": "turn_off",
            "关": "turn_off",
            "设置": "set",
            "调节": "adjust",
            "调": "adjust",
            "增加": "increase",
            "减少": "decrease",
            "查询": "query",
            "状态": "status",
        }

        self.device_type_keywords = {
            DeviceType.LIGHT: ["灯", "灯泡", "灯光", "照明", "lamp", "light"],
            DeviceType.THERMOSTAT: ["空调", "温度", "暖气", "thermostat", "ac", "heater"],
            DeviceType.SWITCH: ["开关", "插座", "switch", "outlet"],
            DeviceType.SENSOR: ["传感器", "感应", "sensor", "detector"],
            DeviceType.CAMERA: ["摄像头", "相机", "监控", "camera", "cam"],
            DeviceType.LOCK: ["锁", "门锁", "lock", "door"],
            DeviceType.SPEAKER: ["音箱", "音响", "speaker", "audio"],
            DeviceType.TV: ["电视", "tv", "television"],
        }

        self.param_patterns = [
            (r"(\d+)\s*度", "temperature"),
            (r"(\d+)\s*%", "brightness"),
            (r"(\d+)\s*分钟", "duration"),
        ]

    def convert(self, intent: str, device_type: str = "unknown") -> str:
        parsed = self.parse(intent, device_type)
        return self._build_command(parsed)

    def parse(self, intent: str, device_type: str = "unknown") -> IntentCommand:
        action = self._extract_action(intent)
        dt = self._detect_device_type(intent, device_type)
        params = self._extract_params(intent)
        return IntentCommand(intent=intent, device_type=dt, action=action, params=params)

    def _extract_action(self, text: str) -> str:
        for keyword, action in self.action_mappings.items():
            if keyword in text:
                return action
        return "control"

    def _detect_device_type(self, text: str, fallback: str) -> DeviceType:
        text_lower = text.lower()
        for dtype, keywords in self.device_type_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    return dtype
        if fallback:
            try:
                return DeviceType(fallback.lower())
            except ValueError:
                pass
        return DeviceType.UNKNOWN

    def _extract_params(self, text: str) -> Dict[str, Any]:
        params = {}
        for pattern, param_name in self.param_patterns:
            match = re.search(pattern, text)
            if match:
                value = match.group(1)
                params[param_name] = int(value) if value.isdigit() else value
        if "温度" in text or "调到" in text:
            temp_match = re.search(r"(\d+)\s*度", text)
            if temp_match:
                params["temperature"] = int(temp_match.group(1))
        if "亮度" in text or "调亮" in text:
            bright_match = re.search(r"(\d+)\s*%", text)
            if bright_match:
                params["brightness"] = int(bright_match.group(1))
        return params

    def _build_command(self, intent_cmd: IntentCommand) -> str:
        cmd_parts = [intent_cmd.device_type.value, intent_cmd.action]
        if intent_cmd.params:
            for key, value in intent_cmd.params.items():
                cmd_parts.append(f"{key}={value}")
        return "_".join(cmd_parts)


class ProtocolAdapter:
    def connect(self) -> bool:
        return True

    def disconnect(self):
        pass

    def send(self, device: Device, command: DeviceCommand) -> CommandResult:
        return CommandResult(
            success=True, device_id=device.id, command=command.command, message="Success"
        )


class HTTPAdapter(ProtocolAdapter):
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self._connected = False

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self):
        self._connected = False

    def send(self, device: Device, command: DeviceCommand) -> CommandResult:
        if not self._connected:
            return CommandResult(
                False, device.id, command.command, "Not connected", error="Adapter not connected"
            )
        return CommandResult(
            True,
            device.id,
            command.command,
            f"HTTP: {command.command} sent to {device.address}",
            new_state={"status": "ok"},
        )


class MQTTAdapter(ProtocolAdapter):
    def __init__(self, broker: str = "localhost", port: int = 1883):
        self.broker = broker
        self.port = port
        self._connected = False
        self._subscriptions: List[str] = []

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self):
        self._connected = False
        self._subscriptions.clear()

    def send(self, device: Device, command: DeviceCommand) -> CommandResult:
        if not self._connected:
            return CommandResult(
                False,
                device.id,
                command.command,
                "Not connected",
                error="MQTT broker not connected",
            )
        return CommandResult(
            True,
            device.id,
            command.command,
            f"MQTT: {command.command} published",
            new_state={"qos": 1, "retained": False},
        )


class WebSocketAdapter(ProtocolAdapter):
    def __init__(self, url: str = "ws://localhost:8080"):
        self.url = url
        self._connected = False
        self._callbacks: Dict[str, Callable] = {}

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self):
        self._connected = False
        self._callbacks.clear()

    def send(self, device: Device, command: DeviceCommand) -> CommandResult:
        if not self._connected:
            return CommandResult(
                False, device.id, command.command, "Not connected", error="WebSocket not connected"
            )
        return CommandResult(
            True,
            device.id,
            command.command,
            f"WebSocket: {command.command} sent to {device.address}",
            new_state={"protocol": "ws"},
        )

    def on_message(self, event: str, callback: Callable):
        self._callbacks[event] = callback


class SceneManager:
    def __init__(self):
        self._scenes: Dict[str, Scene] = {}
        self._init_default_scenes()

    def _init_default_scenes(self):
        self.register(
            Scene(
                id="scene_morning",
                name="早安模式",
                description="起床场景：开灯、调空调、放音乐",
                commands=[
                    {"device_id": "dev_001", "command": "turn_on"},
                    {"device_id": "dev_003", "command": "set", "params": {"temperature": 24}},
                ],
            )
        )
        self.register(
            Scene(
                id="scene_night",
                name="晚安模式",
                description="睡眠场景：关灯、关空调、设防",
                commands=[
                    {"device_id": "dev_001", "command": "turn_off"},
                    {"device_id": "dev_003", "command": "set", "params": {"temperature": 26}},
                    {"device_id": "dev_004", "command": "lock"},
                ],
            )
        )
        self.register(
            Scene(
                id="scene_leave",
                name="离家模式",
                description="出门场景：关闭所有灯、调低空调、安防设防",
                commands=[
                    {"device_id": "dev_001", "command": "turn_off"},
                    {"device_id": "dev_002", "command": "turn_off"},
                    {"device_id": "dev_003", "command": "turn_off"},
                ],
            )
        )

    def register(self, scene: Scene):
        self._scenes[scene.id] = scene

    def unregister(self, scene_id: str) -> bool:
        if scene_id in self._scenes:
            del self._scenes[scene_id]
            return True
        return False

    def get(self, scene_id: str) -> Optional[Scene]:
        return self._scenes.get(scene_id)

    def list_scenes(self) -> List[Scene]:
        return list(self._scenes.values())


class NoUIAdapterComponent:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.default_protocol = self.config.get("default_protocol", "http")
        self.broker = self.config.get("mqtt_broker", "localhost")
        self.broker_port = self.config.get("mqtt_port", 1883)

        self._intent_engine = IntentCommandEngine()
        self._scene_manager = SceneManager()
        self._devices: Dict[str, Device] = {}
        self._adapters: Dict[str, ProtocolAdapter] = {}
        self._connected = False

        self._init_adapters()
        self._register_default_devices()

    def _init_adapters(self):
        self._adapters["http"] = HTTPAdapter()
        self._adapters["mqtt"] = MQTTAdapter(broker=self.broker, port=self.broker_port)
        self._adapters["websocket"] = WebSocketAdapter()

    def _register_default_devices(self):
        default_devices = [
            Device("dev_001", "客厅灯", DeviceType.LIGHT, DeviceProtocol.HTTP, "192.168.1.101"),
            Device("dev_002", "卧室灯", DeviceType.LIGHT, DeviceProtocol.HTTP, "192.168.1.102"),
            Device("dev_003", "空调", DeviceType.THERMOSTAT, DeviceProtocol.MQTT, "192.168.1.103"),
            Device("dev_004", "前门锁", DeviceType.LOCK, DeviceProtocol.ZIGBEE, "192.168.1.104"),
            Device(
                "dev_005", "摄像头", DeviceType.CAMERA, DeviceProtocol.WEBSOCKET, "192.168.1.105"
            ),
        ]
        for device in default_devices:
            self._devices[device.id] = device

    def connect(self, protocol: Optional[str] = None) -> bool:
        target = protocol or self.default_protocol
        if target in self._adapters:
            self._connected = self._adapters[target].connect()
            return self._connected
        return False

    def disconnect(self):
        for adapter in self._adapters.values():
            adapter.disconnect()
        self._connected = False

    def send_command(self, device_id: str, command: str, **kwargs) -> CommandResult:
        device = self._devices.get(device_id)
        if not device:
            return CommandResult(
                False, device_id, command, "Device not found", error="Unknown device"
            )

        protocol_key = device.protocol.value
        if protocol_key == "zigbee":
            protocol_key = "http"
        adapter = self._adapters.get(protocol_key, self._adapters.get("http"))

        device_cmd = DeviceCommand(device_id=device_id, command=command, params=kwargs)
        result = adapter.send(device, device_cmd)

        if result.success:
            device.state.update(result.new_state or {})

        return result

    def send_batch_commands(self, commands: List[Dict[str, Any]]) -> BatchCommandResult:
        results = []
        success_count = 0
        failed_count = 0

        for cmd in commands:
            device_id = cmd.get("device_id")
            command = cmd.get("command")
            params = cmd.get("params", {})
            result = self.send_command(device_id, command, **params)
            results.append(result)
            if result.success:
                success_count += 1
            else:
                failed_count += 1

        return BatchCommandResult(
            total=len(commands),
            success_count=success_count,
            failed_count=failed_count,
            results=results,
        )

    def execute_scene(self, scene_id: str) -> BatchCommandResult:
        scene = self._scene_manager.get(scene_id)
        if not scene:
            return BatchCommandResult(0, 0, 0, [])
        return self.send_batch_commands(scene.commands)

    def convert_intent_to_command(self, intent: str, device_type: str = "unknown") -> str:
        return self._intent_engine.convert(intent, device_type)

    def add_device(self, device: Device):
        self._devices[device.id] = device

    def remove_device(self, device_id: str) -> bool:
        if device_id in self._devices:
            del self._devices[device_id]
            return True
        return False

    def list_devices(self, device_type: Optional[DeviceType] = None) -> List[Device]:
        if device_type:
            return [d for d in self._devices.values() if d.device_type == device_type]
        return list(self._devices.values())

    def get_device(self, device_id: str) -> Optional[Device]:
        return self._devices.get(device_id)

    def register_scene(self, scene: Scene):
        self._scene_manager.register(scene)

    def list_scenes(self) -> List[Scene]:
        return self._scene_manager.list_scenes()

    def get_stats(self) -> Dict[str, Any]:
        device_types = {}
        for device in self._devices.values():
            dtype = device.device_type.value
            device_types[dtype] = device_types.get(dtype, 0) + 1

        return {
            "enabled": True,
            "connected": self._connected,
            "default_protocol": self.default_protocol,
            "total_devices": len(self._devices),
            "devices_by_type": device_types,
            "available_protocols": list(self._adapters.keys()),
            "total_scenes": len(self._scene_manager.list_scenes()),
        }
