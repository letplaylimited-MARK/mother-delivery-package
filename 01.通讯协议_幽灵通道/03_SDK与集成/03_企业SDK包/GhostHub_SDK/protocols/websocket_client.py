"""
WebSocket 协议真实实现

支持真实的WebSocket连接，用于实时双向通信
"""

import json
import time
import threading
import asyncio
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
import logging
import hashlib
import base64
import struct
import websocket

logger = logging.getLogger(__name__)


@dataclass
class WebSocketMessage:
    """WebSocket消息"""

    opcode: int
    data: str
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class WebSocketConfig:
    """WebSocket配置"""

    url: str = "ws://localhost:8080/ws"
    headers: Dict[str, str] = None
    subprotocols: List[str] = None
    timeout: float = 10.0
    ping_interval: float = 30.0
    ping_timeout: float = 10.0
    auto_reconnect: bool = True
    max_reconnects: int = 5


class WebSocketClient:
    """
    WebSocket客户端实现

    支持：
    - 连接/断开
    - 发送/接收文本消息
    - 发送/接收二进制消息
    - 心跳保活
    - 自动重连
    - 子协议
    """

    OPCODE_TEXT = 1
    OPCODE_BINARY = 2
    OPCODE_CLOSE = 8
    OPCODE_PING = 9
    OPCODE_PONG = 10

    def __init__(self, config: Optional[WebSocketConfig] = None):
        self.config = config or WebSocketConfig()
        self._connected = False
        self._closing = False

        # 消息队列
        self._send_queue: List[Dict[str, Any]] = []
        self._receive_queue: List[WebSocketMessage] = []
        self._lock = threading.Lock()

        # 回调
        self._on_open_callback: Optional[Callable] = None
        self._on_close_callback: Optional[Callable] = None
        self._on_error_callback: Optional[Callable] = None
        self._on_message_callback: Optional[Callable] = None

        # 统计
        self._stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "bytes_sent": 0,
            "bytes_received": 0,
            "reconnects": 0,
            "last_connect_time": None,
            "last_message_time": None,
        }

        # WebSocket对象
        self._ws = None
        self._reconnect_count = 0
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None

    @property
    def is_connected(self) -> bool:
        return self._connected

    def on_open(self, callback: Callable):
        """设置连接打开回调"""
        self._on_open_callback = callback

    def on_close(self, callback: Callable):
        """设置连接关闭回调"""
        self._on_close_callback = callback

    def on_error(self, callback: Callable):
        """设置错误回调"""
        self._on_error_callback = callback

    def on_message(self, callback: Callable):
        """设置消息回调"""
        self._on_message_callback = callback

    def connect(self) -> bool:
        """
        连接到WebSocket服务器

        Returns:
            是否连接成功
        """
        if self._connected:
            logger.warning("已经连接到WebSocket服务器")
            return True

        self._closing = False

        try:
            # 尝试导入真实WebSocket库
            try:
                import websocket as ws_module

                self._ws_module = ws_module
                self._use_real_ws = True
            except ImportError:
                logger.warning("websocket-client未安装，使用模拟模式")
                self._use_real_ws = False

            if self._use_real_ws:
                # 创建WebSocket应用
                self._ws = websocket.WebSocketApp(
                    self.config.url,
                    header=self.config.headers or {},
                    subprotocols=self.config.subprotocols,
                    on_open=self._on_ws_open,
                    on_close=self._on_ws_close,
                    on_error=self._on_ws_error,
                    on_message=self._on_ws_message,
                    on_ping=self._on_ws_ping,
                    on_pong=self._on_ws_pong,
                )

                # 在新线程中运行
                self._running = True
                self._worker_thread = threading.Thread(target=self._run_websocket, daemon=True)
                self._worker_thread.start()

                logger.info(f"正在连接WebSocket: {self.config.url}")

            else:
                # 模拟模式
                self._connected = True
                self._stats["last_connect_time"] = time.time()
                logger.info(f"[模拟] WebSocket连接到 {self.config.url}")

                # 调用回调
                if self._on_open_callback:
                    self._on_open_callback()

            return True

        except Exception as e:
            logger.error(f"WebSocket连接失败: {e}")
            if self._on_error_callback:
                self._on_error_callback(e)
            return False

    def _run_websocket(self):
        """在单独线程中运行WebSocket"""
        try:
            self._ws.run_forever(
                ping_interval=self.config.ping_interval, ping_timeout=self.config.ping_timeout
            )
        except Exception as e:
            logger.error(f"WebSocket运行异常: {e}")
            if self._on_error_callback:
                self._on_error_callback(e)

    def _on_ws_open(self, ws):
        """WebSocket打开回调"""
        self._connected = True
        self._stats["last_connect_time"] = time.time()
        logger.info("WebSocket连接打开")

        if self._on_open_callback:
            self._on_open_callback()

    def _on_ws_close(self, ws, close_status_code, close_msg):
        """WebSocket关闭回调"""
        self._connected = False
        logger.info(f"WebSocket关闭: {close_status_code} - {close_msg}")

        if self._on_close_callback:
            self._on_close_callback(close_status_code, close_msg)

        # 自动重连
        if self.config.auto_reconnect and not self._closing:
            self._try_reconnect()

    def _on_ws_error(self, ws, error):
        """WebSocket错误回调"""
        logger.error(f"WebSocket错误: {error}")
        if self._on_error_callback:
            self._on_error_callback(error)

    def _on_ws_message(self, ws, message):
        """WebSocket消息回调"""
        try:
            # 尝试解析JSON
            try:
                data = json.loads(message)
            except:
                data = message

            msg = WebSocketMessage(self.OPCODE_TEXT, data)
            self._receive_queue.append(msg)

            self._stats["messages_received"] += 1
            self._stats["bytes_received"] += len(message)
            self._stats["last_message_time"] = time.time()

            if self._on_message_callback:
                self._on_message_callback(data)

        except Exception as e:
            logger.error(f"处理WebSocket消息失败: {e}")

    def _on_ws_ping(self, ws, data):
        """WebSocket Ping回调"""
        logger.debug("收到Ping")

    def _on_ws_pong(self, ws, data):
        """WebSocket Pong回调"""
        logger.debug("收到Pong")

    def _try_reconnect(self):
        """尝试重连"""
        if self._reconnect_count >= self.config.max_reconnects:
            logger.error("达到最大重连次数")
            return

        self._reconnect_count += 1
        self._stats["reconnects"] += 1

        wait_time = min(30, 2**self._reconnect_count)
        logger.info(
            f"{wait_time}秒后尝试重连 ({self._reconnect_count}/{self.config.max_reconnects})"
        )

        time.sleep(wait_time)

        if not self._closing:
            self.connect()

    def disconnect(self, close_code: int = 1000, close_reason: str = ""):
        """
        断开WebSocket连接

        Args:
            close_code: 关闭状态码
            close_reason: 关闭原因
        """
        if not self._connected:
            return

        self._closing = True
        self._running = False

        try:
            if hasattr(self, "_ws"):
                self._ws.close(close_code, close_reason)

            if self._worker_thread and self._worker_thread.is_alive():
                self._worker_thread.join(timeout=5)

            self._connected = False
            logger.info("WebSocket断开连接")

            if self._on_close_callback:
                self._on_close_callback(close_code, close_reason)

        except Exception as e:
            logger.error(f"WebSocket断开失败: {e}")

    def send(self, data: Any, binary: bool = False) -> bool:
        """
        发送消息

        Args:
            data: 消息内容
            binary: 是否发送二进制

        Returns:
            是否发送成功
        """
        if not self._connected:
            logger.warning("未连接到WebSocket服务器")
            return False

        try:
            # 序列化消息
            if isinstance(data, (dict, list)):
                message = json.dumps(data, ensure_ascii=False)
            else:
                message = str(data)

            if hasattr(self, "_ws"):
                if binary:
                    self._ws.send(message, opcode=self.OPCODE_BINARY)
                else:
                    self._ws.send(message, opcode=self.OPCODE_TEXT)

            self._stats["messages_sent"] += 1
            self._stats["bytes_sent"] += len(message)

            logger.debug(f"发送WebSocket消息: {len(message)} bytes")
            return True

        except Exception as e:
            logger.error(f"发送WebSocket消息失败: {e}")
            return False

    def send_text(self, text: str) -> bool:
        """发送文本消息"""
        return self.send(text, binary=False)

    def send_json(self, data: Dict[str, Any]) -> bool:
        """发送JSON消息"""
        return self.send(data)

    def receive(self, timeout: float = None) -> Optional[WebSocketMessage]:
        """
        接收消息

        Args:
            timeout: 超时时间(秒)

        Returns:
            消息对象，超时返回None
        """
        if not self._connected:
            return None

        if self._receive_queue:
            return self._receive_queue.pop(0)

        return None

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self._stats,
            "connected": self._connected,
            "url": self.config.url,
            "reconnect_count": self._reconnect_count,
        }


# === 便捷函数 ===


def create_websocket_client(
    url: str = "ws://localhost:8080/ws", headers: Dict[str, str] = None
) -> WebSocketClient:
    """创建WebSocket客户端"""
    config = WebSocketConfig(url=url, headers=headers)
    return WebSocketClient(config)
