"""
Ghost Channel Enterprise - License Server
幽灵通道商业版 - 授权服务器

提供许可证激活、验证、管理API
"""

import hashlib
import hmac
import time
import uuid
import json
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class Feature(Enum):
    """商业功能"""

    SEMANTIC_MATCHING = "semantic_matching"
    PREDICTIVE_SYNC = "predictive_sync"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    KNOWLEDGE_CRYSTALLIZER = "crystallizer"
    LEARNING_ENGINE = "learning_engine"
    SELF_HEALING_PRO = "self_healing_pro"


class LicenseType(Enum):
    """许可证类型"""

    TRIAL = "trial"
    PRO = "pro"
    TEAM = "team"
    ENTERPRISE = "enterprise"


@dataclass
class License:
    """许可证"""

    key: str
    license_type: str
    features: List[str]
    issued_at: float
    expires_at: float
    max_activations: int
    activation_count: int = 0
    customer_id: Optional[str] = None
    customer_email: Optional[str] = None
    revoked: bool = False
    metadata: Dict = field(default_factory=dict)


@dataclass
class Activation:
    """激活记录"""

    activation_id: str
    license_key: str
    machine_id: str
    activated_at: float
    last_verified: float
    expires_at: float
    is_valid: bool = True


class LicenseServer:
    """授权服务器"""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.licenses: Dict[str, License] = {}
        self.activations: Dict[str, Activation] = {}
        self._generate_server_keys()

    def _generate_server_keys(self):
        """生成服务器密钥对"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def _sign_data(self, data: str) -> str:
        """签名数据"""
        signature = self.private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
        )
        return signature.hex()

    def _verify_signature(self, data: str, signature: str) -> bool:
        """验证签名"""
        try:
            self.public_key.verify(
                bytes.fromhex(signature),
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
            )
            return True
        except:
            return False

    def generate_license_key(
        self,
        license_type: str,
        features: List[str],
        duration_days: int = 365,
        max_activations: int = 1,
        customer_id: str = None,
        customer_email: str = None,
    ) -> str:
        """生成许可证密钥"""
        key_id = secrets.token_hex(8)
        timestamp = int(time.time())
        expires = timestamp + (duration_days * 86400)

        key_data = f"{license_type}:{','.join(features)}:{timestamp}:{expires}:{max_activations}"
        signature = self._sign_data(key_data)

        key = f"gc_ent_{license_type[0]}{''.join(f[0] for f in features)}_{key_id}_{expires}_{signature[:16]}"

        license = License(
            key=key,
            license_type=license_type,
            features=features,
            issued_at=timestamp,
            expires_at=expires,
            max_activations=max_activations,
            customer_id=customer_id,
            customer_email=customer_email,
        )

        self.licenses[key] = license
        return key

    def verify_license(self, license_key: str) -> Tuple[bool, str, List[str]]:
        """验证许可证"""
        if license_key not in self.licenses:
            return False, "License not found", []

        license = self.licenses[license_key]

        if license.revoked:
            return False, "License has been revoked", []

        if time.time() > license.expires_at:
            return False, "License has expired", []

        return True, "Valid", license.features

    def activate(
        self,
        license_key: str,
        machine_id: str,
    ) -> Tuple[bool, str, Optional[str]]:
        """激活许可证"""
        valid, message, features = self.verify_license(license_key)
        if not valid:
            return False, message, None

        license = self.licenses[license_key]

        if license.activation_count >= license.max_activations:
            return False, "Maximum activations reached", None

        activation_id = str(uuid.uuid4())
        expires_at = license.expires_at

        activation = Activation(
            activation_id=activation_id,
            license_key=license_key,
            machine_id=machine_id,
            activated_at=time.time(),
            last_verified=time.time(),
            expires_at=expires_at,
        )

        self.activations[activation_id] = activation
        license.activation_count += 1

        return True, "Activated", activation_id

    def verify_activation(
        self,
        activation_id: str,
        machine_id: str,
    ) -> Tuple[bool, str]:
        """验证激活"""
        if activation_id not in self.activations:
            return False, "Activation not found"

        activation = self.activations[activation_id]

        if not activation.is_valid:
            return False, "Activation has been deactivated"

        if activation.machine_id != machine_id:
            return False, "Machine ID mismatch"

        if time.time() > activation.expires_at:
            return False, "Activation has expired"

        activation.last_verified = time.time()
        return True, "Valid"

    def deactivate(self, activation_id: str) -> bool:
        """停用激活"""
        if activation_id in self.activations:
            self.activations[activation_id].is_valid = False
            return True
        return False

    def revoke_license(self, license_key: str) -> bool:
        """撤销许可证"""
        if license_key in self.licenses:
            self.licenses[license_key].revoked = True
            for activation in self.activations.values():
                if activation.license_key == license_key:
                    activation.is_valid = False
            return True
        return False

    def get_stats(self) -> Dict:
        """获取统计"""
        total = len(self.licenses)
        valid = sum(
            1
            for l in self.licenses.values()
            if not l.revoked and l.expires_at > time.time()
        )
        active = sum(1 for a in self.activations.values() if a.is_valid)

        return {
            "total_licenses": total,
            "valid_licenses": valid,
            "active_activations": active,
            "revoked": total - valid,
        }


# FastAPI应用
app = FastAPI(title="Ghost Channel License Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局授权服务器实例 (生产环境应使用数据库)
SERVER = LicenseServer(secret_key="change-me-in-production")


# 请求/响应模型
class GenerateLicenseRequest(BaseModel):
    license_type: str = "pro"
    features: List[str] = ["semantic_matching"]
    duration_days: int = 365
    max_activations: int = 1
    customer_id: Optional[str] = None
    customer_email: Optional[str] = None


class GenerateLicenseResponse(BaseModel):
    license_key: str
    expires_at: str
    features: List[str]


class ActivateRequest(BaseModel):
    license_key: str
    machine_id: str


class ActivateResponse(BaseModel):
    success: bool
    message: str
    activation_id: Optional[str] = None


class VerifyRequest(BaseModel):
    activation_id: str
    machine_id: str


class VerifyResponse(BaseModel):
    valid: bool
    message: str


class DeactivateRequest(BaseModel):
    activation_id: str


class RevokeRequest(BaseModel):
    license_key: str


# API端点


@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "ok",
        "service": "Ghost Channel License Server",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/stats")
async def get_stats():
    """获取服务器统计"""
    return SERVER.get_stats()


@app.post("/license/generate", response_model=GenerateLicenseResponse)
async def generate_license(request: GenerateLicenseRequest):
    """生成许可证"""
    key = SERVER.generate_license_key(
        license_type=request.license_type,
        features=request.features,
        duration_days=request.duration_days,
        max_activations=request.max_activations,
        customer_id=request.customer_id,
        customer_email=request.customer_email,
    )

    license = SERVER.licenses[key]

    return GenerateLicenseResponse(
        license_key=key,
        expires_at=datetime.fromtimestamp(license.expires_at).isoformat(),
        features=license.features,
    )


@app.post("/license/verify")
async def verify_license(license_key: str):
    """验证许可证"""
    valid, message, features = SERVER.verify_license(license_key)
    return {
        "valid": valid,
        "message": message,
        "features": features,
    }


@app.post("/license/revoke")
async def revoke_license(request: RevokeRequest):
    """撤销许可证"""
    success = SERVER.revoke_license(request.license_key)
    if not success:
        raise HTTPException(status_code=404, detail="License not found")
    return {"success": True, "message": "License revoked"}


@app.post("/activation/activate", response_model=ActivateResponse)
async def activate(request: ActivateRequest):
    """激活许可证"""
    success, message, activation_id = SERVER.activate(
        license_key=request.license_key,
        machine_id=request.machine_id,
    )

    return ActivateResponse(
        success=success,
        message=message,
        activation_id=activation_id,
    )


@app.post("/activation/verify", response_model=VerifyResponse)
async def verify_activation(request: VerifyRequest):
    """验证激活"""
    valid, message = SERVER.verify_activation(
        activation_id=request.activation_id,
        machine_id=request.machine_id,
    )

    return VerifyResponse(valid=valid, message=message)


@app.post("/activation/deactivate")
async def deactivate(request: DeactivateRequest):
    """停用激活"""
    success = SERVER.deactivate(request.activation_id)
    return {"success": success, "message": "Deactivated" if success else "Not found"}


@app.get("/activations")
async def list_activations():
    """列出所有激活"""
    return {
        "activations": [
            {
                "id": a.activation_id,
                "license_key": a.license_key[:20] + "...",
                "machine_id": a.machine_id,
                "activated_at": datetime.fromtimestamp(a.activated_at).isoformat(),
                "is_valid": a.is_valid,
            }
            for a in SERVER.activations.values()
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
