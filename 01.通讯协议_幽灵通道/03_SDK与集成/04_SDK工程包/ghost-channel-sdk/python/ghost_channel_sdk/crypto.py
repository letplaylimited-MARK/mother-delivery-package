from __future__ import annotations

from typing import TypedDict

from ghost_channel.core.crypto import CryptoEngine


class EncryptedPacket(TypedDict):
    nonce: bytes
    ciphertext: bytes
    auth_tag: bytes


class AESGCMBackend:
    """Real AES-256-GCM backend wrapping CryptoEngine from ghost_channel."""

    NONCE_SIZE = CryptoEngine.NONCE_SIZE
    TAG_SIZE = CryptoEngine.TAG_SIZE

    def encrypt(self, *, key: bytes, plaintext: bytes, aad: bytes) -> EncryptedPacket:
        engine = CryptoEngine(key)
        return engine.encrypt(plaintext, aad)

    def decrypt(
        self,
        *,
        key: bytes,
        nonce: bytes,
        ciphertext: bytes,
        auth_tag: bytes,
        aad: bytes,
    ) -> bytes:
        engine = CryptoEngine(key)
        return engine.decrypt(nonce, ciphertext, auth_tag, aad)
