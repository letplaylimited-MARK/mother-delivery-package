"""
Ghost Channel - Crypto Engine
幽灵通道 - 加密引擎

原子能力C: 加密传输
实现: AES-256-GCM + HMAC-SHA256
验证: 端到端加密, 100%完整性验证
"""

from __future__ import annotations
import os
import hmac
import hashlib
import secrets
from typing import TypedDict
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptedPacket(TypedDict):
    """加密数据包"""

    nonce: bytes
    ciphertext: bytes
    auth_tag: bytes


class CryptoEngine:
    """加密引擎 - AES-256-GCM"""

    NONCE_SIZE = 12  # 96位
    KEY_SIZE = 32  # 256位
    TAG_SIZE = 16  # 128位

    def __init__(self, key: bytes = None):
        """
        初始化加密引擎

        Args:
            key: 256位密钥（如果为None则生成随机密钥）
        """
        self.key = key or os.urandom(self.KEY_SIZE)
        self.aesgcm = AESGCM(self.key)

    def generate_key(
        self, password: str, salt: bytes = None, iterations: int = 100000
    ) -> tuple[bytes, bytes]:
        """
        使用PBKDF2从密码派生密钥

        Args:
            password: 密码
            salt: 盐（如果为None则生成随机盐）
            iterations: 迭代次数

        Returns:
            (密钥, 盐)
        """
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_SIZE,
            salt=salt,
            iterations=iterations,
        )
        key = kdf.derive(password.encode())
        return key, salt

    def encrypt(self, plaintext: bytes, aad: bytes = None) -> EncryptedPacket:
        """
        加密数据

        Args:
            plaintext: 明文
            aad: 附加认证数据

        Returns:
            EncryptedPacket: {nonce, ciphertext, auth_tag}
        """
        nonce = os.urandom(self.NONCE_SIZE)
        encrypted = self.aesgcm.encrypt(nonce, plaintext, aad)

        ciphertext = encrypted[: -self.TAG_SIZE]
        auth_tag = encrypted[-self.TAG_SIZE :]

        return {
            "nonce": nonce,
            "ciphertext": ciphertext,
            "auth_tag": auth_tag,
        }

    def decrypt(
        self, nonce: bytes, ciphertext: bytes, auth_tag: bytes, aad: bytes = None
    ) -> bytes:
        """
        解密数据

        Args:
            nonce: nonce
            ciphertext: 密文
            auth_tag: 认证标签
            aad: 附加认证数据

        Returns:
            明文

        Raises:
            ValueError: 认证失败
        """
        try:
            return self.aesgcm.decrypt(nonce, ciphertext + auth_tag, aad)
        except Exception:
            raise ValueError("Decryption failed - auth tag verification failed")

    def sign(self, data: bytes) -> str:
        """
        HMAC-SHA256签名

        Args:
            data: 数据

        Returns:
            十六进制签名字符串
        """
        return hmac.new(self.key, data, hashlib.sha256).hexdigest()

    def verify(self, data: bytes, signature: str) -> bool:
        """
        验证HMAC签名

        Args:
            data: 数据
            signature: 签名

        Returns:
            是否验证通过
        """
        expected = hmac.new(self.key, data, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def compute_hash(self, data: bytes) -> str:
        """计算SHA-256哈希"""
        return hashlib.sha256(data).hexdigest()

    def compute_hash_dict(self, data: dict) -> str:
        """计算字典的SHA-256哈希"""
        import json

        data_str = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(data_str).hexdigest()

    @staticmethod
    def generate_nonce(size: int = 12) -> bytes:
        """生成随机nonce"""
        return os.urandom(size)

    @staticmethod
    def generate_salt(size: int = 16) -> bytes:
        """生成随机盐"""
        return os.urandom(size)


class KeyManager:
    """密钥管理器"""

    def __init__(self):
        self.keys: dict[str, CryptoEngine] = {}
        self.salt: dict[str, bytes] = {}

    def create_key(self, key_id: str, password: str = None) -> str:
        """创建新密钥"""
        if password:
            crypto = CryptoEngine()
            key, salt = crypto.generate_key(password)
            crypto = CryptoEngine(key)
            self.keys[key_id] = crypto
            self.salt[key_id] = salt
            return key.hex()
        else:
            crypto = CryptoEngine()
            self.keys[key_id] = crypto
            return crypto.key.hex()

    def get_key(self, key_id: str) -> CryptoEngine:
        """获取密钥"""
        return self.keys.get(key_id)

    def delete_key(self, key_id: str):
        """删除密钥"""
        self.keys.pop(key_id, None)
        self.salt.pop(key_id, None)
