"""
Ghost Channel Enterprise - Client Activation SDK
幽灵通道商业版 - 客户端激活SDK

在客户端代码中使用此SDK进行许可证激活和验证
"""

import hashlib
import os
import platform
import time
import uuid
from typing import Tuple, List, Optional
from dataclasses import dataclass

import httpx


@dataclass
class ActivationResult:
    """激活结果"""

    success: bool
    message: str
    activation_id: Optional[str] = None
    features: List[str] = None


@dataclass
class VerificationResult:
    """验证结果"""

    valid: bool
    message: str


class MachineIdentifier:
    """机器标识生成器"""

    @staticmethod
    def get_machine_id() -> str:
        """获取唯一机器ID"""
        components = [
            platform.node(),
            platform.machine(),
            platform.processor(),
            str(uuid.getnode()),
        ]

        if hasattr(uuid, "getnode"):
            mac = ":".join(
                f"{(uuid.getnode() >> i) & 0xFF:02x}" for i in range(0, 48, 8)
            )
            components.append(mac)

        combined = "_".join(components)
        return hashlib.sha256(combined.encode()).hexdigest()[:32]


class ClientActivationSDK:
    """客户端激活SDK"""

    def __init__(
        self,
        license_key: str,
        server_url: str = "http://localhost:8001",
        auto_verify: bool = True,
        verify_interval: int = 3600,
    ):
        self.license_key = license_key
        self.server_url = server_url.rstrip("/")
        self.activation_id: Optional[str] = None
        self.machine_id = MachineIdentifier.get_machine_id()
        self.enabled_features: List[str] = []
        self._is_valid = False
        self._last_verify = 0
        self._verify_interval = verify_interval
        self._offline_mode = False

    def activate(self) -> ActivationResult:
        """
        激活许可证

        Returns:
            ActivationResult: 激活结果
        """
        try:
            response = httpx.post(
                f"{self.server_url}/activation/activate",
                json={
                    "license_key": self.license_key,
                    "machine_id": self.machine_id,
                },
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                self.activation_id = data.get("activation_id")
                self._is_valid = data.get("success", False)

                if self._is_valid:
                    self._fetch_features()

                return ActivationResult(
                    success=data.get("success", False),
                    message=data.get("message", ""),
                    activation_id=self.activation_id,
                    features=self.enabled_features,
                )
            else:
                return ActivationResult(
                    success=False,
                    message=f"Server error: {response.status_code}",
                )

        except httpx.ConnectError:
            self._offline_mode = True
            return self._offline_activation()
        except Exception as e:
            return ActivationResult(success=False, message=str(e))

    def _offline_activation(self) -> ActivationResult:
        """离线激活 (基于机器ID验证密钥格式)"""
        parts = self.license_key.split("_")
        if len(parts) < 4:
            return ActivationResult(success=False, message="Invalid key format")

        expires = int(parts[3])
        if time.time() > expires:
            return ActivationResult(success=False, message="License expired")

        self._is_valid = True
        self.activation_id = f"offline_{self.machine_id[:8]}"
        self.enabled_features = self._parse_features_from_key()
        self._offline_mode = True

        return ActivationResult(
            success=True,
            message="Offline activation successful",
            activation_id=self.activation_id,
            features=self.enabled_features,
        )

    def _parse_features_from_key(self) -> List[str]:
        """从密钥解析功能列表"""
        feature_map = {
            "s": "semantic_matching",
            "p": "predictive_sync",
            "k": "knowledge_graph",
            "c": "crystallizer",
            "l": "learning_engine",
            "h": "self_healing_pro",
        }

        features = []
        key_parts = self.license_key.split("_")
        if len(key_parts) > 1:
            codes = key_parts[2][:6]
            for char in codes:
                if char in feature_map:
                    features.append(feature_map[char])

        return features

    def verify(self, force: bool = False) -> VerificationResult:
        """
        验证激活状态

        Args:
            force: 是否强制验证 (忽略缓存)

        Returns:
            VerificationResult: 验证结果
        """
        if not self._is_valid:
            return VerificationResult(False, "Not activated")

        if not force and time.time() - self._last_verify < self._verify_interval:
            return VerificationResult(True, "Cached valid")

        if self._offline_mode:
            return self._offline_verify()

        try:
            response = httpx.post(
                f"{self.server_url}/activation/verify",
                json={
                    "activation_id": self.activation_id,
                    "machine_id": self.machine_id,
                },
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                self._is_valid = data.get("valid", False)
                return VerificationResult(
                    valid=data.get("valid", False),
                    message=data.get("message", ""),
                )
            else:
                return VerificationResult(False, f"Error: {response.status_code}")

        except httpx.ConnectError:
            return self._offline_verify()
        except Exception as e:
            return VerificationResult(False, str(e))

    def _offline_verify(self) -> VerificationResult:
        """离线验证"""
        parts = self.license_key.split("_")
        if len(parts) < 4:
            return VerificationResult(False, "Invalid key")

        expires = int(parts[3])
        if time.time() > expires:
            return VerificationResult(False, "License expired")

        return VerificationResult(True, "Offline valid")

    def deactivate(self) -> bool:
        """
        停用当前机器的激活

        Returns:
            bool: 是否成功
        """
        if not self.activation_id:
            return False

        try:
            response = httpx.post(
                f"{self.server_url}/activation/deactivate",
                json={"activation_id": self.activation_id},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                self._is_valid = False
                self.activation_id = None
                return data.get("success", False)

        except Exception:
            pass

        return False

    def is_feature_enabled(self, feature: str) -> bool:
        """检查功能是否已启用"""
        if not self._is_valid:
            return False

        if not self.enabled_features:
            return False

        return feature in self.enabled_features

    def get_enabled_features(self) -> List[str]:
        """获取已启用的功能列表"""
        if not self._is_valid:
            return []

        return self.enabled_features.copy()

    def get_machine_id(self) -> str:
        """获取当前机器ID"""
        return self.machine_id


def activate_license(
    license_key: str,
    server_url: str = "http://localhost:8001",
) -> ClientActivationSDK:
    """
    便捷函数: 激活许可证

    Args:
        license_key: 许可证密钥
        server_url: 许可证服务器URL

    Returns:
        ClientActivationSDK: 激活SDK实例
    """
    sdk = ClientActivationSDK(license_key, server_url)
    result = sdk.activate()

    if not result.success:
        raise LicenseError(result.message)

    return sdk


class LicenseError(Exception):
    """许可证错误"""

    pass


class LicenseManager:
    """许可证管理器 (单例)"""

    _instance = None
    _activation: Optional[ClientActivationSDK] = None

    @classmethod
    def get_instance(cls) -> Optional[ClientActivationSDK]:
        """获取激活实例"""
        return cls._activation

    @classmethod
    def set_activation(cls, activation: ClientActivationSDK):
        """设置激活实例"""
        cls._activation = activation

    @classmethod
    def check_feature(cls, feature: str) -> bool:
        """检查功能是否可用"""
        if cls._activation is None:
            return False
        return cls._activation.is_feature_enabled(feature)


__all__ = [
    "ClientActivationSDK",
    "ActivationResult",
    "VerificationResult",
    "MachineIdentifier",
    "activate_license",
    "LicenseError",
    "LicenseManager",
]
