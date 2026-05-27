"""
AES-256-GCM Encryption Module
Ghost Channel Protocol - Atomic Capability D
"""

import os
import hashlib
import hmac
from typing import TypedDict

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class EncryptedPacket(TypedDict):
    """加密数据包"""
    nonce: bytes
    ciphertext: bytes
    auth_tag: bytes


class CryptoEngine:
    """加密引擎 - AES-256-GCM实现"""
    
    NONCE_SIZE = 12  # 96位
    TAG_SIZE = 16     # 128位
    KEY_SIZE = 32     # 256位
    
    def __init__(self, key: bytes = None):
        if key is None:
            key = os.urandom(self.KEY_SIZE)
        elif len(key) != self.KEY_SIZE:
            raise ValueError(f"Key must be {self.KEY_SIZE} bytes")
        
        self.key = key
        self._aesgcm = AESGCM(key) if CRYPTO_AVAILABLE else None
    
    @staticmethod
    def generate_key() -> bytes:
        """生成256位随机密钥"""
        return os.urandom(32)
    
    def encrypt(self, plaintext: bytes, aad: bytes = None) -> EncryptedPacket:
        """
        加密数据
        
        Args:
            plaintext: 明文字节
            aad: 附加认证数据 (可选)
            
        Returns:
            EncryptedPacket: {nonce, ciphertext, auth_tag}
        """
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("cryptography library not installed")
        
        nonce = os.urandom(self.NONCE_SIZE)
        encrypted = self._aesgcm.encrypt(nonce, plaintext, aad)
        
        ciphertext = encrypted[:-self.TAG_SIZE]
        auth_tag = encrypted[-self.TAG_SIZE:]
        
        return {
            "nonce": nonce,
            "ciphertext": ciphertext,
            "auth_tag": auth_tag
        }
    
    def decrypt(self, packet: EncryptedPacket, aad: bytes = None) -> bytes:
        """
        解密数据
        
        Args:
            packet: 加密数据包
            aad: 附加认证数据 (可选)
            
        Returns:
            明文字节
        """
        if not CRYPTO_AVAILABLE:
            raise RuntimeError("cryptography library not installed")
        
        try:
            return self._aesgcm.decrypt(
                packet["nonce"],
                packet["ciphertext"] + packet["auth_tag"],
                aad
            )
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    def sign(self, data: bytes) -> str:
        """HMAC-SHA256签名"""
        return hmac.new(self.key, data, hashlib.sha256).hexdigest()
    
    def verify(self, data: bytes, signature: str) -> bool:
        """验证HMAC-SHA256签名"""
        expected = hmac.new(self.key, data, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)
    
    def derive_key(self, password: str, salt: bytes, iterations: int = 100000) -> bytes:
        """PBKDF2-SHA256密钥派生"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt,
            iterations,
            dklen=self.KEY_SIZE
        )
    
    def hash_data(self, data: bytes) -> str:
        """SHA-256哈希"""
        return hashlib.sha256(data).hexdigest()


def test_crypto():
    """测试加密功能"""
    if not CRYPTO_AVAILABLE:
        print("[SKIP] cryptography library not installed")
        return
    
    # Test 1: Generate key
    key = CryptoEngine.generate_key()
    assert len(key) == 32
    print("[OK] generate_key")
    
    # Test 2: Encrypt/Decrypt
    engine = CryptoEngine(key)
    plaintext = b"Hello, Ghost Channel!"
    encrypted = engine.encrypt(plaintext)
    decrypted = engine.decrypt(encrypted)
    assert decrypted == plaintext
    print("[OK] encrypt/decrypt")
    
    # Test 3: Sign/Verify
    signature = engine.sign(plaintext)
    assert engine.verify(plaintext, signature) == True
    assert engine.verify(b"wrong", signature) == False
    print("[OK] sign/verify")
    
    # Test 4: Derive key
    salt = os.urandom(16)
    derived = engine.derive_key("password", salt)
    assert len(derived) == 32
    print("[OK] derive_key")
    
    # Test 5: Hash
    hash_val = engine.hash_data(plaintext)
    assert len(hash_val) == 64
    print("[OK] hash_data")
    
    print("[PASS] All crypto tests passed!")


if __name__ == "__main__":
    test_crypto()