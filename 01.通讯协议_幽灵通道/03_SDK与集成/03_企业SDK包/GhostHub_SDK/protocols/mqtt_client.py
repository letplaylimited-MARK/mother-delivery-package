"""
MQTT 协议真实实现

支持真实的MQTT连接，用于IoT设备控制
"""

import json
import time
import threading
import asyncio
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class QoSLevel(Enum):
    QoS0 = 0  # 最多一次
    QoS1 = 1  # 至少一次
    QoS2 = 2  # 恰好一次


@dataclass
class MQTTMessage:
    """MQTT消息"""

    topic: str
    payload: str
    qos: QoSLevel = QoSLevel.QoS1
    retain: bool = False
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class MQTTConnectionConfig:
    """MQTT连接配置"""

    broker: str = "localhost"
    port: int = 1883
    client_id: str = ""
    username: Optional[str] = None
    password: Optional[str] = None
    keepalive: int = 60
    clean_session: bool = True
    ssl_enabled: bool = False
    ssl_cafile: Optional[str] = None
    ssl_certfile: Optional[str] = None
    ssl_keyfile: Optional[str] = None


class MQTTClient:
    """
    MQTT客户端实现

    支持：
    - 连接/断开
    - 发布消息
    - 订阅主题
    - 接收消息
    - QoS级别
    - 遗嘱消息
    - 重连机制
    """

    def __init__(self, config: Optional[MQTTConnectionConfig] = None):
        self.config = config or MQTTConnectionConfig()

        if not self.config.client_id:
            import uuid

            self.config.client_id = f"gh_client_{uuid.uuid4().hex[:8]}"

        self._connected = False
        self._subscribed_topics: Dict[str, QoSLevel] = {}
        self._message_handlers: Dict[str, List[Callable]] = {}
        self._pending_messages: List[MQTTMessage] = []
        self._lock = threading.Lock()

        # 回调
        self._on_connect_callback: Optional[Callable] = None
        self._on_disconnect_callback: Optional[Callable] = None
        self._on_message_callback: Optional[Callable] = None

        # 统计
        self._stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "bytes_sent": 0,
            "bytes_received": 0,
            "reconnects": 0,
            "last_connect_time": None,
            "last_disconnect_time": None,
        }

    @property
    def is_connected(self) -> bool:
        return self._connected

    def on_connect(self, callback: Callable):
        """设置连接成功回调"""
        self._on_connect_callback = callback

    def on_disconnect(self, callback: Callable):
        """设置断开连接回调"""
        self._on_disconnect_callback = callback

    def on_message(self, topic: str, callback: Callable):
        """设置消息回调"""
        if topic not in self._message_handlers:
            self._message_handlers[topic] = []
        self._message_handlers[topic].append(callback)

        # 同时设置全局回调
        if self._on_message_callback is None:
            self._on_message_callback = lambda t, p: self._dispatch_message(t, p)

    def _dispatch_message(self, topic: str, payload: Any):
        """分发消息到处理器"""
        for pattern, handlers in self._message_handlers.items():
            if self._topic_matches(pattern, topic):
                for handler in handlers:
                    try:
                        handler(topic, payload)
                    except Exception as e:
                        logger.error(f"消息处理失败: {e}")

    def _topic_matches(self, pattern: str, topic: str) -> bool:
        """检查主题是否匹配"""
        if pattern == "#":
            return True
        if pattern == "+":
            return "/" in topic

        pattern_parts = pattern.split("/")
        topic_parts = topic.split("/")

        for i, part in enumerate(pattern_parts):
            if part == "#":
                return True
            if i >= len(topic_parts):
                return False
            if part != "+" and part != topic_parts[i]:
                return False

        return len(pattern_parts) == len(topic_parts)

    def connect(self, timeout: float = 10.0) -> bool:
        """
        连接到MQTT Broker

        Args:
            timeout: 连接超时时间(秒)

        Returns:
            是否连接成功
        """
        if self._connected:
            logger.warning("已经连接到MQTT Broker")
            return True

        try:
            # 尝试导入真实MQTT库
            try:
                import paho.mqtt.client as mqtt

                self._mqtt = mqtt
                self._use_real_mqtt = True
            except ImportError:
                logger.warning("paho-mqtt未安装，使用模拟模式")
                self._use_real_mqtt = False

            if self._use_real_mqtt:
                # 真实MQTT连接
                self._client = mqtt.Client(
                    client_id=self.config.client_id, clean_session=self.config.clean_session
                )

                if self.config.username:
                    self._client.username_pw_set(self.config.username, self.config.password)

                if self.config.ssl_enabled:
                    self._client.tls_set(
                        ca_certs=self.config.ssl_cafile,
                        certfile=self.config.ssl_certfile,
                        keyfile=self.config.ssl_keyfile,
                    )

                self._client.on_connect = self._on_real_connect
                self._client.on_disconnect = self._on_real_disconnect
                self._client.on_message = self._on_real_message

                logger.info(f"连接MQTT Broker: {self.config.broker}:{self.config.port}")
                self._client.connect(
                    self.config.broker, self.config.port, keepalive=self.config.keepalive
                )
                self._client.loop_start()
            else:
                # 模拟模式
                self._connected = True
                self._stats["last_connect_time"] = time.time()
                logger.info(f"[模拟] MQTT连接到 {self.config.broker}:{self.config.port}")

            # 重新订阅之前订阅的主题
            for topic, qos in self._subscribed_topics.items():
                self.subscribe(topic, qos)

            # 调用连接回调
            if self._on_connect_callback:
                self._on_connect_callback()

            return True

        except Exception as e:
            logger.error(f"MQTT连接失败: {e}")
            return False

    def _on_real_connect(self, client, userdata, flags, rc):
        """真实连接回调"""
        if rc == 0:
            self._connected = True
            self._stats["last_connect_time"] = time.time()
            logger.info("MQTT连接成功")
            if self._on_connect_callback:
                self._on_connect_callback()
        else:
            logger.error(f"MQTT连接失败: rc={rc}")

    def _on_real_disconnect(self, client, userdata, rc):
        """真实断开连接回调"""
        self._connected = False
        self._stats["last_disconnect_time"] = time.time()
        self._stats["reconnects"] += 1
        logger.warning(f"MQTT断开连接: rc={rc}")
        if self._on_disconnect_callback:
            self._on_disconnect_callback()

    def _on_real_message(self, client, userdata, msg):
        """真实消息回调"""
        try:
            payload = json.loads(msg.payload.decode())
        except:
            payload = msg.payload.decode()

        self._stats["messages_received"] += 1
        self._stats["bytes_received"] += len(msg.payload)

        if self._on_message_callback:
            self._on_message_callback(msg.topic, payload)

    def disconnect(self):
        """断开MQTT连接"""
        if not self._connected:
            return

        try:
            if hasattr(self, "_client"):
                self._client.loop_stop()
                self._client.disconnect()

            self._connected = False
            self._stats["last_disconnect_time"] = time.time()
            logger.info("MQTT断开连接")

            if self._on_disconnect_callback:
                self._on_disconnect_callback()

        except Exception as e:
            logger.error(f"MQTT断开连接失败: {e}")

    def subscribe(self, topic: str, qos: QoSLevel = QoSLevel.QoS1) -> bool:
        """
        订阅主题

        Args:
            topic: 主题 (支持 # 和 + 通配符)
            qos: QoS级别

        Returns:
            是否订阅成功
        """
        if not self._connected:
            logger.warning("未连接到MQTT Broker")
            return False

        try:
            if hasattr(self, "_client"):
                self._client.subscribe(topic, qos.value)

            self._subscribed_topics[topic] = qos
            logger.info(f"订阅主题: {topic} (QoS{qos.value})")
            return True

        except Exception as e:
            logger.error(f"订阅失败: {e}")
            return False

    def unsubscribe(self, topic: str) -> bool:
        """取消订阅"""
        if not self._connected:
            return False

        try:
            if hasattr(self, "_client"):
                self._client.unsubscribe(topic)

            if topic in self._subscribed_topics:
                del self._subscribed_topics[topic]

            logger.info(f"取消订阅: {topic}")
            return True

        except Exception as e:
            logger.error(f"取消订阅失败: {e}")
            return False

    def publish(
        self, topic: str, payload: Any, qos: QoSLevel = QoSLevel.QoS1, retain: bool = False
    ) -> bool:
        """
        发布消息

        Args:
            topic: 主题
            payload: 消息内容
            qos: QoS级别
            retain: 是否保留消息

        Returns:
            是否发布成功
        """
        if not self._connected:
            logger.warning("未连接到MQTT Broker")
            return False

        try:
            # 序列化消息
            if isinstance(payload, (dict, list)):
                message_payload = json.dumps(payload, ensure_ascii=False)
            else:
                message_payload = str(payload)

            if hasattr(self, "_client"):
                self._client.publish(topic, message_payload, qos.value, retain)

            # 记录消息
            msg = MQTTMessage(topic, message_payload, qos, retain)
            self._pending_messages.append(msg)

            # 统计
            self._stats["messages_sent"] += 1
            self._stats["bytes_sent"] += len(message_payload)

            logger.debug(f"发布消息: {topic} ({len(message_payload)} bytes)")
            return True

        except Exception as e:
            logger.error(f"发布消息失败: {e}")
            return False

    def get_subscribed_topics(self) -> List[str]:
        """获取已订阅的主题"""
        return list(self._subscribed_topics.keys())

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self._stats,
            "connected": self._connected,
            "subscribed_topics": len(self._subscribed_topics),
            "pending_messages": len(self._pending_messages),
            "broker": self.config.broker,
            "port": self.config.port,
        }


# === 便捷函数 ===


def create_mqtt_client(
    broker: str = "localhost", port: int = 1883, username: str = None, password: str = None
) -> MQTTClient:
    """创建MQTT客户端"""
    config = MQTTConnectionConfig(broker=broker, port=port, username=username, password=password)
    return MQTTClient(config)
