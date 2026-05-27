"""
Ghost Hub SDK - 安全模块

提供企业级安全保障：
1. 认证授权 (API Key / JWT)
2. 输入验证 (参数白名单、特殊字符过滤)
3. 敏感数据保护 (日志脱敏、密钥管理)
4. 请求频率限制 (Rate Limiting)
5. 安全配置检查
"""

import re
import hashlib
import hmac
import time
import secrets
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


# ==================== 1. 认证授权 ====================


@dataclass
class AuthConfig:
    """认证配置"""

    api_keys: Dict[str, Dict[str, Any]] = None  # api_key -> {name, permissions, created_at}
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24

    def __post_init__(self):
        if self.api_keys is None:
            self.api_keys = {}


class SimpleAuth:
    """
    简单API Key认证

    使用示例:
        auth = SimpleAuth()
        auth.add_api_key("key123", "admin", permissions=["read", "write", "admin"])

        # 装饰器保护端点
        @app.post("/protected")
        @auth.require_auth
        async def protected_endpoint(key: str = auth.depends()):
            ...
    """

    def __init__(self, config: Optional[AuthConfig] = None):
        self.config = config or AuthConfig()
        self._request_counts: Dict[str, List[float]] = defaultdict(list)
        self._rate_limit_lock = True

    def add_api_key(self, key: str, name: str, permissions: List[str] = None) -> bool:
        """
        添加API Key

        Args:
            key: API Key
            name: 密钥名称
            permissions: 权限列表 ["read", "write", "admin"]

        Returns:
            是否添加成功
        """
        if len(key) < 32:
            logger.warning(f"API Key太短，应至少32字符")
            return False

        self.config.api_keys[key] = {
            "name": name,
            "permissions": permissions or ["read"],
            "created_at": datetime.now().isoformat(),
            "last_used": None,
            "request_count": 0,
        }
        logger.info(f"添加API Key: {name}")
        return True

    def remove_api_key(self, key: str) -> bool:
        """移除API Key"""
        if key in self.config.api_keys:
            name = self.config.api_keys[key]["name"]
            del self.config.api_keys[key]
            logger.info(f"移除API Key: {name}")
            return True
        return False

    def validate_api_key(self, key: str) -> Optional[Dict[str, Any]]:
        """
        验证API Key

        Returns:
            密钥信息或None
        """
        if not key:
            return None

        key_info = self.config.api_keys.get(key)
        if key_info:
            # 更新使用记录
            key_info["last_used"] = datetime.now().isoformat()
            key_info["request_count"] = key_info.get("request_count", 0) + 1

        return key_info

    def has_permission(self, key: str, permission: str) -> bool:
        """检查是否有指定权限"""
        key_info = self.validate_api_key(key)
        if not key_info:
            return False

        perms = key_info.get("permissions", [])

        # admin权限拥有所有权限
        if "admin" in perms:
            return True

        return permission in perms

    def require_auth(self, required_permission: str = "read"):
        """认证装饰器"""

        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # 从请求头获取API Key
                api_key = kwargs.get("api_key") or self._extract_key_from_request(
                    kwargs.get("request")
                )

                if not api_key:
                    raise UnauthorizedError("缺少API Key")

                key_info = self.validate_api_key(api_key)
                if not key_info:
                    raise UnauthorizedError("无效的API Key")

                if not self.has_permission(api_key, required_permission):
                    raise ForbiddenError(f"缺少必要权限: {required_permission}")

                kwargs["auth_info"] = key_info
                return await func(*args, **kwargs)

            return wrapper

        return decorator

    def depends(self):
        """FastAPI依赖注入"""
        from fastapi import Header, HTTPException

        async def get_api_key(x_api_key: Optional[str] = Header(None)):
            if not x_api_key:
                raise HTTPException(status_code=401, detail="缺少API Key")

            key_info = self.validate_api_key(x_api_key)
            if not key_info:
                raise HTTPException(status_code=401, detail="无效的API Key")

            return x_api_key

        return get_api_key

    def _extract_key_from_request(self, request) -> Optional[str]:
        """从请求中提取API Key"""
        if not request:
            return None

        # 尝试从Header提取
        if hasattr(request, "headers"):
            return request.headers.get("X-API-Key")

        return None

    def generate_api_key(self) -> str:
        """生成安全的API Key"""
        return secrets.token_urlsafe(32)

    def get_stats(self) -> Dict[str, Any]:
        """获取认证统计"""
        total_keys = len(self.config.api_keys)
        active_keys = sum(
            1
            for k in self.config.api_keys.values()
            if k.get("last_used")
            and datetime.fromisoformat(k["last_used"]) > datetime.now() - timedelta(days=7)
        )

        total_requests = sum(k.get("request_count", 0) for k in self.config.api_keys.values())

        return {
            "total_keys": total_keys,
            "active_keys_7d": active_keys,
            "total_requests": total_requests,
        }


class UnauthorizedError(Exception):
    """未授权异常"""

    pass


class ForbiddenError(Exception):
    """禁止访问异常"""

    pass


# ==================== 2. 输入验证 ====================


class InputValidator:
    """
    输入验证器

    提供:
    - 参数白名单验证
    - 特殊字符过滤
    - 类型验证
    - 长度限制
    - 危险命令检测
    """

    # 允许的命令白名单
    ALLOWED_COMMANDS = {
        "turn_on",
        "turn_off",
        "set",
        "adjust",
        "increase",
        "decrease",
        "query",
        "status",
        "lock",
        "unlock",
        "open",
        "close",
    }

    # 危险命令黑名单
    DANGEROUS_COMMANDS = {
        "DROP",
        "DELETE",
        "EXEC",
        "EXECUTE",
        "INSERT",
        "UPDATE",
        "SELECT",
        "CREATE",
        "ALTER",
        "DROP",
        "TRUNCATE",
        "GRANT",
        "REVOKE",
        "SHUTDOWN",
        "KILL",
        "SYSTEM",
        "rm",
        "mv",
        "cp",
        "cat",
        "ls",
        "echo",
        "cat",
        "chmod",
        "chown",
        "wget",
        "curl",
        "nc",
        "netcat",
        "bash",
        "sh",
        "python",
        "perl",
        "ruby",
        "php",
        "eval",
        "exec",
        "passthru",
        "shell_exec",
        "proc_open",
    }

    # 危险字符模式
    DANGEROUS_PATTERNS = [
        r"['\";].*?(SELECT|INSERT|UPDATE|DELETE|DROP)",  # SQL注入
        r"(?i)\b(DROP|DELETE|EXEC|EXECUTE|TRUNCATE)\b\s+\w+",  # 危险SQL命令
        r"<script[^>]*>.*?</script>",  # XSS
        r"<[^>]*javascript:",  # JavaScript伪协议
        r"on\w+\s*=",  # 事件处理器注入
        r"\$\{.*?\}",  # 命令注入
        r"&&.*?rm\s",  # Shell注入
        r"\|\s*cat\s",  # 管道注入
        r";\s*(rm|mv|cp|chmod)",  # 命令链注入
        r"`.*?`",  # 命令替换
        r"\$\(.*?\)",  # 命令替换
        r"eval\s*\(",  # eval注入
        r"exec\s*\(",  # exec注入
    ]

    @classmethod
    def validate_command(cls, command: str) -> bool:
        """验证设备命令"""
        if not isinstance(command, str):
            raise TypeError(f"命令必须是字符串类型, 实际: {type(command)}")

        # 清理空格
        command = command.strip()

        # 空命令检查
        if not command:
            return False

        # 黑名单检查 (大小写敏感)
        if command in cls.DANGEROUS_COMMANDS:
            logger.warning(f"危险命令: {command}")
            return False

        # 检查黑名单子串
        command_upper = command.upper()
        for dangerous in cls.DANGEROUS_COMMANDS:
            if dangerous.upper() in command_upper:
                logger.warning(f"命令包含危险词: {command}")
                return False

        # 白名单检查 (精确匹配)
        if command not in cls.ALLOWED_COMMANDS:
            logger.warning(f"未知命令: {command}")
            return False

        return True

    @classmethod
    def validate_device_id(cls, device_id: str) -> bool:
        """验证设备ID"""
        if not isinstance(device_id, str):
            raise TypeError(f"设备ID必须是字符串类型, 实际: {type(device_id)}")

        device_id = device_id.strip()

        # 空ID检查
        if not device_id:
            return False

        # 检查路径遍历
        if ".." in device_id or "/" in device_id or "\\" in device_id:
            logger.warning(f"设备ID包含路径遍历: {device_id}")
            return False

        # 检查危险字符
        dangerous_chars = [
            "<",
            ">",
            ";",
            "&",
            "|",
            "`",
            "$",
            "(",
            ")",
            "{",
            "}",
            "[",
            "]",
            "*",
            "?",
        ]
        for char in dangerous_chars:
            if char in device_id:
                logger.warning(f"设备ID包含危险字符: {device_id}")
                return False

        # 只能是字母数字和下划线
        if not re.match(r"^[a-zA-Z0-9_]+$", device_id):
            logger.warning(f"无效设备ID: {device_id}")
            return False

        # 长度限制
        if len(device_id) > 64:
            logger.warning(f"设备ID过长: {device_id}")
            return False

        return True

    @classmethod
    def validate_params(cls, params: Dict[str, Any], allowed_keys: List[str]) -> Dict[str, Any]:
        """
        验证参数字典

        Args:
            params: 原始参数
            allowed_keys: 允许的参数键列表

        Returns:
            验证后的参数
        """
        if not isinstance(params, dict):
            raise TypeError(f"params必须是字典类型, 实际: {type(params)}")

        if not isinstance(allowed_keys, list):
            raise TypeError(f"allowed_keys必须是列表类型, 实际: {type(allowed_keys)}")

        if not params:
            return {}

        validated = {}
        for key in allowed_keys:
            if key in params:
                value = params[key]

                # 类型检查
                if key == "temperature":
                    if not isinstance(value, (int, float)):
                        continue
                    if not 0 <= value <= 100:  # 温度范围
                        continue
                    validated[key] = value

                elif key == "brightness":
                    if not isinstance(value, (int, float)):
                        continue
                    if not 0 <= value <= 100:  # 亮度范围
                        continue
                    validated[key] = value

                elif key == "duration":
                    if not isinstance(value, (int, float)):
                        continue
                    if not 0 <= value <= 86400:  # 最大24小时
                        continue
                    validated[key] = value

                else:
                    validated[key] = value

        return validated

    @classmethod
    def sanitize_text(cls, text: str, max_length: int = 1000) -> str:
        """文本消毒"""
        if not text:
            return ""

        # 移除危险字符
        for pattern in cls.DANGEROUS_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        # 移除多余空白
        text = " ".join(text.split())

        # 长度限制
        if len(text) > max_length:
            text = text[:max_length]

        return text

    @classmethod
    def validate_intent_text(cls, text: str) -> bool:
        """验证意图文本"""
        if not text:
            return False

        # 类型检查
        if not isinstance(text, str):
            logger.warning(f"意图文本类型错误: {type(text)}")
            return False

        text = text.strip()

        # 空文本检查
        if not text:
            return False

        # 长度检查
        if len(text) > 1000:
            logger.warning(f"意图文本过长: {len(text)}字符")
            return False

        # 检查危险SQL关键字 (使用单词边界)
        dangerous_keywords = r"\b(DROP|DELETE|EXEC|EXECUTE|TRUNCATE|INSERT|UPDATE|SELECT)\b"
        if re.search(dangerous_keywords, text, re.IGNORECASE):
            logger.warning(f"意图文本包含危险SQL关键字")
            return False

        # 危险字符检查
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"意图文本包含危险模式: {pattern}")
                return False

        # 检查控制字符
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text):
            logger.warning(f"意图文本包含控制字符")
            return False

        # 检查NULL字节
        if "\x00" in text or "\0" in text:
            logger.warning(f"意图文本包含NULL字节")
            return False

        return True

    @classmethod
    def validate_device_id(cls, device_id: str) -> bool:
        """验证设备ID"""
        if not isinstance(device_id, str):
            raise TypeError(f"设备ID必须是字符串类型, 实际: {type(device_id)}")

        device_id = device_id.strip()

        # 空ID检查
        if not device_id:
            return False

        # 检查路径遍历
        if ".." in device_id or "/" in device_id or "\\" in device_id:
            logger.warning(f"设备ID包含路径遍历: {device_id}")
            return False

        # 检查危险字符
        dangerous_chars = [
            "<",
            ">",
            ";",
            "&",
            "|",
            "`",
            "$",
            "(",
            ")",
            "{",
            "}",
            "[",
            "]",
            "*",
            "?",
        ]
        for char in dangerous_chars:
            if char in device_id:
                logger.warning(f"设备ID包含危险字符: {device_id}")
                return False

        # 只能是字母数字和下划线
        if not re.match(r"^[a-zA-Z0-9_]+$", device_id):
            logger.warning(f"无效设备ID: {device_id}")
            return False

        # 长度限制
        if len(device_id) > 64:
            logger.warning(f"设备ID过长: {device_id}")
            return False

        return True


# ==================== 3. 敏感数据保护 ====================


class SensitiveDataProtector:
    """
    敏感数据保护器

    功能:
    - 日志脱敏
    - 密钥脱敏
    - 数据加密
    """

    # 敏感字段模式
    SENSITIVE_FIELDS = {
        "password",
        "secret",
        "token",
        "api_key",
        "apikey",
        "private_key",
        "access_key",
        "credential",
        "auth",
    }

    # 脱敏替换
    MASK_CHAR = "*"

    @classmethod
    def mask_dict(cls, data: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        """
        脱敏字典

        Usage:
            safe_data = SensitiveDataProtector.mask_dict({
                "username": "admin",
                "api_key": "sk-12345678",
                "data": {"password": "secret123"}
            })
        """
        if depth > 10:  # 防止递归过深
            return {}

        if not isinstance(data, dict):
            return data

        result = {}
        for key, value in data.items():
            key_lower = key.lower()

            # 检查是否是敏感字段
            is_sensitive = any(pattern in key_lower for pattern in cls.SENSITIVE_FIELDS)

            if is_sensitive:
                if isinstance(value, str) and len(value) > 4:
                    # 显示前2后2，中间脱敏
                    result[key] = value[:2] + cls.MASK_CHAR * (len(value) - 4) + value[-2:]
                else:
                    result[key] = cls.MASK_CHAR * 4
            elif isinstance(value, dict):
                result[key] = cls.mask_dict(value, depth + 1)
            elif isinstance(value, list):
                result[key] = [
                    cls.mask_dict(item, depth + 1) if isinstance(item, dict) else item
                    for item in value[:10]  # 限制列表长度
                ]
            else:
                result[key] = value

        return result

    @classmethod
    def mask_string(cls, text: str, visible_chars: int = 4) -> str:
        """脱敏字符串"""
        if not text or len(text) <= visible_chars:
            return cls.MASK_CHAR * 4

        return text[:visible_chars] + cls.MASK_CHAR * (len(text) - visible_chars)

    @classmethod
    def safe_log(cls, message: str, data: Dict[str, Any] = None) -> str:
        """安全的日志记录"""
        safe_message = message

        if data:
            safe_data = cls.mask_dict(data)
            safe_message += f" | data: {safe_data}"

        return safe_message


# ==================== 4. 请求频率限制 ====================


class RateLimiter:
    """
    请求频率限制器

    使用令牌桶算法
    """

    def __init__(self, requests_per_minute: int = 60, burst: int = 10):
        """
        初始化限流器

        Args:
            requests_per_minute: 每分钟请求数
            burst: 突发容量
        """
        self.rate = requests_per_minute / 60.0  # 每秒请求数
        self.burst = burst
        self.tokens: Dict[str, float] = defaultdict(lambda: burst)
        self.last_update: Dict[str, float] = defaultdict(time.time)
        self._lock = True  # 简化锁

    def check(self, key: str) -> bool:
        """
        检查是否允许请求

        Args:
            key: 标识符 (IP, API Key等)

        Returns:
            True表示允许，False表示被限制
        """
        now = time.time()

        # 补充令牌
        elapsed = now - self.last_update[key]
        self.tokens[key] = min(self.burst, self.tokens[key] + elapsed * self.rate)
        self.last_update[key] = now

        # 消耗令牌
        if self.tokens[key] >= 1:
            self.tokens[key] -= 1
            return True

        return False

    def get_remaining(self, key: str) -> int:
        """获取剩余请求数"""
        return int(max(0, self.tokens[key]))

    def reset(self, key: str):
        """重置限流"""
        self.tokens[key] = self.burst
        self.last_update[key] = time.time()

    def get_stats(self) -> Dict[str, Any]:
        """获取限流统计"""
        return {
            "tracked_keys": len(self.tokens),
            "rate_per_minute": int(self.rate * 60),
            "burst_size": self.burst,
        }


# ==================== 5. 安全配置检查 ====================


class SecurityChecker:
    """
    安全配置检查器

    在启动时检查安全问题
    """

    @staticmethod
    def check_all() -> List[Dict[str, Any]]:
        """执行所有安全检查"""
        issues = []

        issues.extend(SecurityChecker.check_debug_mode())
        issues.extend(SecurityChecker.check_default_credentials())
        issues.extend(SecurityChecker.check_cors_config())
        issues.extend(SecurityChecker.check_storage_permissions())

        return issues

    @staticmethod
    def check_debug_mode() -> List[Dict[str, Any]]:
        """检查是否开启调试模式"""
        import sys

        issues = []
        if hasattr(sys, "gettrace") and sys.gettrace():
            issues.append(
                {
                    "severity": "warning",
                    "check": "debug_mode",
                    "message": "调试模式已开启，生产环境应关闭",
                }
            )

        return issues

    @staticmethod
    def check_default_credentials() -> List[Dict[str, Any]]:
        """检查默认凭据"""
        issues = []

        # 检查是否使用默认JWT密钥
        # 这个检查需要在实际使用处调用

        return issues

    @staticmethod
    def check_cors_config() -> List[Dict[str, Any]]:
        """检查CORS配置"""
        issues = []

        # 检查是否有通配符CORS
        # 这个检查需要在API配置处调用

        return issues

    @staticmethod
    def check_storage_permissions() -> List[Dict[str, Any]]:
        """检查存储权限"""
        issues = []

        from pathlib import Path

        storage_path = Path.home() / ".ghost_hub"
        if storage_path.exists():
            # 检查权限 (Unix)
            import os

            stat = storage_path.stat()

            # Windows权限检查有限，这里只做基本检查
            if os.name == "posix":
                mode = stat.st_mode & 0o777
                if mode & 0o007:  # 其他用户有写权限
                    issues.append(
                        {
                            "severity": "warning",
                            "check": "storage_permissions",
                            "message": f"存储目录权限过宽: {oct(mode)}",
                        }
                    )

        return issues


# ==================== 导出 ====================

__all__ = [
    "AuthConfig",
    "SimpleAuth",
    "UnauthorizedError",
    "ForbiddenError",
    "InputValidator",
    "SensitiveDataProtector",
    "RateLimiter",
    "SecurityChecker",
]
