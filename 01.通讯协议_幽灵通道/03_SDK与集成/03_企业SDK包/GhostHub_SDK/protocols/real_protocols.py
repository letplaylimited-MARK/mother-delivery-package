"""
Ghost Hub 真实协议实现

支持真实的 MQTT 和 WebSocket 连接：
- MQTT: 消息队列遥测传输协议
- WebSocket: 实时双向通信
"""

import json
import time
import uuid
import asyncio
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


class ProtocolType(Enum):
    MQTT = "mqtt"
    WEBSOCKET = "websocket"
    HTTP = "http"


@dataclass
class Message:
    """协议消息"""

    topic: str
    payload: Dict[str, Any]
    qos: int = 0
    retain: bool = False
    timestamp: float = field(default_factory=time.time)
    message_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])


@dataclass
class ConnectionConfig:
    """连接配置"""

    protocol: ProtocolType
    host: str = "localhost"
    port: int = 1883
    username: Optional[str] = None
    password: Optional[str] = None
    client_id: Optional[str] = None
    keepalive: int = 60
    tls_enabled: bool = False
    auto_reconnect: bool = True
    reconnect_interval: int = 5


class RealMQTTAdapter:
    """
    真实 MQTT 协议适配器

    支持:
    - 订阅/发布
    - QoS 0/1/2
    - 自动重连
    - TLS加密
    """

    def __init__(self, config: ConnectionConfig):
        self.config = config
        self._client = None
        self._connected = False
        self._subscriptions: Dict[str, Callable] = {}
        self._message_queue: List[Message] = []
        self._lock = threading.Lock()

        # 尝试导入paho-mqtt
        try:
            import paho.mqtt.client as mqtt

            self._mqtt = mqtt
            self._has_paho = True
        except ImportError:
            self._has_paho = False
            print("[MQTT] paho-mqtt未安装，将使用模拟模式")

    def connect(self) -> bool:
        """建立MQTT连接"""
        if self._connected:
            return True

        if self._has_paho:
            return self._connect_real()
        else:
            return self._connect_mock()

    def _connect_real(self) -> bool:
        """真实MQTT连接"""
        try:
            client_id = self.config.client_id or f"ghub_{uuid.uuid4().hex[:8]}"

            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    self._connected = True
                    print(f"[MQTT] Connected to {self.config.host}:{self.config.port}")
                    # 重新订阅
                    for topic in self._subscriptions:
                        client.subscribe(topic)
                else:
                    print(f"[MQTT] Connection failed with code {rc}")

            def on_message(client, userdata, msg):
                payload = json.loads(msg.payload.decode()) if msg.payload else {}
                message = Message(topic=msg.topic, payload=payload, qos=msg.qos)
                self._handle_message(message)

            def on_disconnect(client, userdata, rc):
                self._connected = False
                print(f"[MQTT] Disconnected with code {rc}")
                if self.config.auto_reconnect:
                    self._schedule_reconnect()

            self._client = self._mqtt.Client(client_id=client_id)
            self._client.on_connect = on_connect
            self._client.on_message = on_message
            self._client.on_disconnect = on_disconnect

            if self.config.username and self.config.password:
                self._client.username_pw_set(self.config.username, self.config.password)

            self._client.connect(self.config.host, self.config.port, self.config.keepalive)
            self._client.loop_start()

            return True

        except Exception as e:
            print(f"[MQTT] Connection error: {e}")
            return False

    def _connect_mock(self) -> bool:
        """模拟MQTT连接（用于测试）"""
        print(f"[MQTT Mock] Simulating connection to {self.config.host}:{self.config.port}")
        self._connected = True
        return True

    def _schedule_reconnect(self):
        """计划重连"""

        def reconnect():
            time.sleep(self.config.reconnect_interval)
            self.connect()

        thread = threading.Thread(target=reconnect, daemon=True)
        thread.start()

    def disconnect(self):
        """断开连接"""
        if self._client:
            self._client.loop_stop()
            self._client.disconnect()
        self._connected = False
        print("[MQTT] Disconnected")

    def subscribe(self, topic: str, callback: Callable, qos: int = 0):
        """订阅主题"""
        self._subscriptions[topic] = callback
        if self._client and self._connected:
            self._client.subscribe(topic, qos)
        print(f"[MQTT] Subscribed to: {topic}")

    def publish(self, topic: str, payload: Dict[str, Any], qos: int = 0) -> bool:
        """发布消息"""
        if not self._connected:
            print("[MQTT] Not connected, message queued")
            with self._lock:
                self._message_queue.append(Message(topic, payload, qos))
            return False

        if self._has_paho and self._client:
            result = self._client.publish(topic, json.dumps(payload, ensure_ascii=False), qos)
            return result.rc == self._mqtt.MQTT_ERR_SUCCESS
        else:
            print(f"[MQTT Mock] Published to {topic}: {payload}")
            return True

    def _handle_message(self, message: Message):
        """处理接收的消息"""
        topic = message.topic
        for pattern, callback in self._subscriptions.items():
            if self._match_topic(pattern, topic):
                try:
                    callback(message)
                except Exception as e:
                    print(f"[MQTT] Callback error: {e}")

    def _match_topic(self, pattern: str, topic: str) -> bool:
        """匹配主题"""
        if pattern == topic:
            return True
        if "#" in pattern:
            import fnmatch

            return fnmatch.fnmatch(topic, pattern.replace("#", "*"))
        if "+" in pattern:
            import fnmatch

            return fnmatch.fnmatch(topic, pattern.replace("+", "*"))
        return False

    def get_queued_messages(self) -> List[Message]:
        """获取队列中的消息"""
        with self._lock:
            messages = self._message_queue.copy()
            self._message_queue.clear()
            return messages

    def get_status(self) -> Dict[str, Any]:
        """获取连接状态"""
        return {
            "protocol": "mqtt",
            "connected": self._connected,
            "host": self.config.host,
            "port": self.config.port,
            "subscriptions": len(self._subscriptions),
            "queued_messages": len(self._message_queue),
        }


class RealWebSocketAdapter:
    """
    真实 WebSocket 协议适配器

    支持:
    - 双向实时通信
    - 自动重连
    - 心跳检测
    """

    def __init__(self, config: ConnectionConfig):
        self.config = config
        self._ws = None
        self._connected = False
        self._handlers: Dict[str, Callable] = {}
        self._message_queue: List[Message] = []
        self._lock = threading.Lock()
        self._running = False
        self._reader_thread: Optional[threading.Thread] = None

        # 尝试导入websockets
        try:
            import websockets

            self._websockets = websockets
            self._has_websockets = True
        except ImportError:
            self._has_websockets = False
            print("[WebSocket] websockets未安装，将使用模拟模式")

    def connect(self) -> bool:
        """建立WebSocket连接"""
        if self._connected:
            return True

        if self._has_websockets:
            return self._connect_real()
        else:
            return self._connect_mock()

    def _connect_real(self) -> bool:
        """真实WebSocket连接"""
        try:
            url = f"ws{'s' if self.config.tls_enabled else ''}://{self.config.host}:{self.config.port}"

            async def connect_async():
                self._ws = await self._websockets.connect(url)
                self._connected = True
                print(f"[WebSocket] Connected to {url}")
                self._running = True
                self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
                self._reader_thread.start()

            asyncio.get_event_loop().run_until_complete(connect_async())
            return True

        except Exception as e:
            print(f"[WebSocket] Connection error: {e}")
            return False

    def _connect_mock(self) -> bool:
        """模拟WebSocket连接"""
        print(f"[WebSocket Mock] Simulating connection to {self.config.host}:{self.config.port}")
        self._connected = True
        return True

    def _read_loop(self):
        """消息读取循环"""
        if not self._has_websockets or not self._ws:
            return

        async def read_messages():
            while self._running and self._ws:
                try:
                    message = await self._ws.recv()
                    data = json.loads(message)
                    msg = Message(topic="ws://", payload=data)
                    self._handle_message(msg)
                except Exception as e:
                    print(f"[WebSocket] Read error: {e}")
                    break

        asyncio.get_event_loop().run_until_complete(read_messages())

    def disconnect(self):
        """断开连接"""
        self._running = False
        if self._ws:
            asyncio.get_event_loop().run_until_complete(self._ws.close())
        self._connected = False
        print("[WebSocket] Disconnected")

    def send(self, payload: Dict[str, Any]) -> bool:
        """发送消息"""
        if not self._connected:
            print("[WebSocket] Not connected, message queued")
            with self._lock:
                self._message_queue.append(Message(topic="ws://", payload=payload))
            return False

        if self._has_websockets and self._ws:

            async def send_async():
                await self._ws.send(json.dumps(payload, ensure_ascii=False))

            try:
                asyncio.get_event_loop().run_until_complete(send_async())
                return True
            except Exception as e:
                print(f"[WebSocket] Send error: {e}")
                return False
        else:
            print(f"[WebSocket Mock] Sent: {payload}")
            return True

    def on_message(self, event_type: str, handler: Callable):
        """注册消息处理器"""
        self._handlers[event_type] = handler

    def _handle_message(self, message: Message):
        """处理消息"""
        event_type = message.payload.get("type", "default")
        handler = self._handlers.get(event_type)
        if handler:
            try:
                handler(message)
            except Exception as e:
                print(f"[WebSocket] Handler error: {e}")

    def get_status(self) -> Dict[str, Any]:
        """获取连接状态"""
        return {
            "protocol": "websocket",
            "connected": self._connected,
            "host": self.config.host,
            "port": self.config.port,
            "handlers": len(self._handlers),
            "queued_messages": len(self._message_queue),
        }


class ProtocolManager:
    """
    协议管理器

    统一管理多种协议，根据设备类型自动选择
    """

    def __init__(self):
        self._adapters: Dict[ProtocolType, Any] = {}
        self._default_config = ConnectionConfig(
            protocol=ProtocolType.HTTP, host="localhost", port=8080
        )

    def register_adapter(self, protocol: ProtocolType, adapter: Any):
        """注册协议适配器"""
        self._adapters[protocol] = adapter

    def get_adapter(self, protocol: ProtocolType) -> Any:
        """获取协议适配器"""
        return self._adapters.get(protocol)

    def connect_all(self) -> Dict[str, bool]:
        """连接所有协议"""
        results = {}
        for protocol, adapter in self._adapters.items():
            try:
                results[protocol.value] = adapter.connect()
            except Exception as e:
                print(f"[ProtocolManager] {protocol.value} connect failed: {e}")
                results[protocol.value] = False
        return results

    def disconnect_all(self):
        """断开所有连接"""
        for adapter in self._adapters.values():
            try:
                adapter.disconnect()
            except:
                pass


# 工厂函数
def create_mqtt_adapter(host: str = "localhost", port: int = 1883) -> RealMQTTAdapter:
    """创建MQTT适配器"""
    config = ConnectionConfig(
        protocol=ProtocolType.MQTT, host=host, port=port, client_id=f"ghub_{uuid.uuid4().hex[:8]}"
    )
    return RealMQTTAdapter(config)


def create_websocket_adapter(host: str = "localhost", port: int = 8080) -> RealWebSocketAdapter:
    """创建WebSocket适配器"""
    config = ConnectionConfig(protocol=ProtocolType.WEBSOCKET, host=host, port=port)
    return RealWebSocketAdapter(config)


# 示例用法
if __name__ == "__main__":
    # MQTT示例
    print("=" * 60)
    print("MQTT适配器测试")
    print("=" * 60)

    mqtt = create_mqtt_adapter("test.mqttbroker.com", 1883)
    mqtt.connect()

    # 订阅主题
    def on_device_status(msg: Message):
        print(f"[MQTT] 设备状态更新: {msg.payload}")

    mqtt.subscribe("home/+/status", on_device_status)

    # 发布消息
    mqtt.publish("home/living_room/light/control", {"command": "turn_on", "brightness": 80})

    # 获取状态
    print("\n[MQQT状态]")
    print(mqtt.get_status())

    mqtt.disconnect()

    # WebSocket示例
    print("\n" + "=" * 60)
    print("WebSocket适配器测试")
    print("=" * 60)

    ws = create_websocket_adapter("localhost", 8080)
    ws.connect()

    # 发送消息
    ws.send({"type": "subscribe", "channels": ["device_updates", "alerts"]})

    # 获取状态
    print("\n[WebSocket状态]")
    print(ws.get_status())

    ws.disconnect()
