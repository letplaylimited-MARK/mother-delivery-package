from __future__ import annotations

import hashlib
import hmac
import os
from typing import TypedDict

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class EncryptedPacket(TypedDict):
    nonce: bytes
    ciphertext: bytes
    auth_tag: bytes


class AESGCMBackend:
    """真实 AES-256-GCM 后端。"""

    NONCE_SIZE = 12
    TAG_SIZE = 16

    def encrypt(self, *, key: bytes, plaintext: bytes, aad: bytes) -> EncryptedPacket:
        nonce = os.urandom(self.NONCE_SIZE)
        aesgcm = AESGCM(key)
        encrypted = aesgcm.encrypt(nonce, plaintext, aad)
        ciphertext = encrypted[: -self.TAG_SIZE]
        auth_tag = encrypted[-self.TAG_SIZE :]
        return {
            "nonce": nonce,
            "ciphertext": ciphertext,
            "auth_tag": auth_tag,
        }

    def decrypt(
        self,
        *,
        key: bytes,
        nonce: bytes,
        ciphertext: bytes,
        auth_tag: bytes,
        aad: bytes,
    ) -> bytes:
        aesgcm = AESGCM(key)
        try:
            return aesgcm.decrypt(nonce, ciphertext + auth_tag, aad)
        except Exception as exc:
            raise ValueError("auth tag verification failed") from exc
