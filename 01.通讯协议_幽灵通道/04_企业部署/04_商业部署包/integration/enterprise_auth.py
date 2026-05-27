"""
Ghost Hub SDK Enterprise Integration
SSO, LDAP, API Gateway integration
"""

import hashlib
import hmac
import time
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum


class AuthMethod(Enum):
    API_KEY = "api_key"
    JWT = "jwt"
    LDAP = "ldap"
    SSO = "sso"
    OAUTH2 = "oauth2"


@dataclass
class AuthContext:
    user_id: str
    user_name: str
    email: str
    roles: list
    auth_method: str
    permissions: list


@dataclass
class AuthResult:
    success: bool
    context: Optional[AuthContext] = None
    error: Optional[str] = None


class AuthManager:
    """Authentication and authorization manager"""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode()
        self._users: Dict[str, Dict] = {}
        self._api_keys: Dict[str, str] = {}

    def authenticate_api_key(self, api_key: str) -> AuthResult:
        """Authenticate using API key"""
        if api_key in self._api_keys:
            user_id = self._api_keys[api_key]
            user = self._users.get(user_id)
            if user:
                return AuthResult(
                    success=True,
                    context=AuthContext(
                        user_id=user_id,
                        user_name=user["name"],
                        email=user["email"],
                        roles=user["roles"],
                        auth_method=AuthMethod.API_KEY.value,
                        permissions=user.get("permissions", []),
                    ),
                )
        return AuthResult(success=False, error="Invalid API key")

    def authenticate_jwt(self, token: str) -> AuthResult:
        """Authenticate using JWT token"""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return AuthResult(success=False, error="Invalid token format")

            header, payload, signature = parts

            expected_sig = hmac.new(
                self.secret_key, f"{header}.{payload}".encode(), hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, expected_sig):
                return AuthResult(success=False, error="Invalid signature")

            import base64
            import json

            payload_data = json.loads(base64.urlsafe_b64decode(payload + "=="))

            if payload_data.get("exp", 0) < time.time():
                return AuthResult(success=False, error="Token expired")

            return AuthResult(
                success=True,
                context=AuthContext(
                    user_id=payload_data["sub"],
                    user_name=payload_data.get("name", ""),
                    email=payload_data.get("email", ""),
                    roles=payload_data.get("roles", []),
                    auth_method=AuthMethod.JWT.value,
                    permissions=payload_data.get("permissions", []),
                ),
            )
        except Exception as e:
            return AuthResult(success=False, error=str(e))

    def register_user(
        self,
        user_id: str,
        name: str,
        email: str,
        roles: list = None,
        permissions: list = None,
    ):
        """Register a user"""
        self._users[user_id] = {
            "name": name,
            "email": email,
            "roles": roles or [],
            "permissions": permissions or [],
        }

    def generate_api_key(self, user_id: str) -> str:
        """Generate API key for user"""
        import secrets

        api_key = secrets.token_urlsafe(32)
        self._api_keys[api_key] = user_id
        return api_key

    def check_permission(self, context: AuthContext, permission: str) -> bool:
        """Check if user has permission"""
        if "admin" in context.roles:
            return True
        return permission in context.permissions


class LDAPConnector:
    """LDAP authentication connector"""

    def __init__(self, server: str, base_dn: str):
        self.server = server
        self.base_dn = base_dn
        self._connection = None

    def authenticate(self, username: str, password: str) -> AuthResult:
        """Authenticate against LDAP"""
        try:
            import ldap

            conn = ldap.initialize(self.server)
            user_dn = f"uid={username},{self.base_dn}"

            conn.simple_bind_s(user_dn, password)

            search_result = conn.search_s(user_dn, ldap.SCOPE_BASE, "(objectClass=*)")

            attrs = search_result[0][1]

            conn.unbind_s()

            return AuthResult(
                success=True,
                context=AuthContext(
                    user_id=username,
                    user_name=attrs.get("cn", [b""])[0].decode(),
                    email=attrs.get("mail", [b""])[0].decode(),
                    roles=attrs.get("memberOf", []),
                    auth_method=AuthMethod.LDAP.value,
                    permissions=[],
                ),
            )
        except Exception as e:
            return AuthResult(success=False, error=str(e))


class SSOConnector:
    """SSO integration connector"""

    def __init__(self, sso_url: str, client_id: str, client_secret: str):
        self.sso_url = sso_url
        self.client_id = client_id
        self.client_secret = client_secret

    def authenticate(self, sso_token: str) -> AuthResult:
        """Authenticate using SSO token"""
        return AuthResult(success=False, error="Not implemented")


class RateLimiter:
    """Rate limiting implementation"""

    def __init__(self):
        self._requests: Dict[str, list] = {}
        self._limits = {
            "default": {"requests": 100, "window": 60},
            "api_key": {"requests": 1000, "window": 60},
            "authenticated": {"requests": 10000, "window": 60},
        }

    def check_rate_limit(self, identifier: str, limit_type: str = "default") -> bool:
        """Check if request is within rate limit"""
        now = time.time()
        limit_config = self._limits.get(limit_type, self._limits["default"])

        if identifier not in self._requests:
            self._requests[identifier] = []

        requests = self._requests[identifier]
        window_start = now - limit_config["window"]

        requests = [r for r in requests if r > window_start]
        self._requests[identifier] = requests

        if len(requests) >= limit_config["requests"]:
            return False

        requests.append(now)
        return True

    def set_limit(self, limit_type: str, requests: int, window: int):
        """Set custom rate limit"""
        self._limits[limit_type] = {"requests": requests, "window": window}


class APIKeyManager:
    """API key lifecycle management"""

    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self._key_metadata: Dict[str, Dict] = {}

    def create_key(
        self,
        user_id: str,
        name: str,
        scopes: list = None,
        expires_in: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create new API key"""
        api_key = self.auth_manager.generate_api_key(user_id)

        metadata = {
            "name": name,
            "scopes": scopes or ["read"],
            "created": time.time(),
            "expires": time.time() + expires_in if expires_in else None,
            "last_used": None,
        }

        self._key_metadata[api_key] = metadata

        return {"api_key": api_key, "metadata": metadata}

    def revoke_key(self, api_key: str):
        """Revoke API key"""
        if api_key in self._key_metadata:
            del self._key_metadata[api_key]
        if api_key in self.auth_manager._api_keys:
            del self.auth_manager._api_keys[api_key]

    def get_key_info(self, api_key: str) -> Optional[Dict]:
        """Get API key metadata"""
        return self._key_metadata.get(api_key)

    def list_keys(self, user_id: str) -> list:
        """List all keys for user"""
        return [
            {"key": k, **v}
            for k, v in self._key_metadata.items()
            if self.auth_manager._api_keys.get(k) == user_id
        ]
