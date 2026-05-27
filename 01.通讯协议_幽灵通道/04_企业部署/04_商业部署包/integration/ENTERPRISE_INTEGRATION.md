# Ghost Hub SDK Enterprise Integration Guide

## Overview

Enterprise integration features include:
- **Multi-method Authentication** - API Key, JWT, LDAP, SSO, OAuth2
- **Rate Limiting** - Per-user, per-API-key, per-IP limits
- **Role-Based Access Control** - Granular permissions
- **Audit Trail** - Complete action logging

---

## Authentication

### API Key Authentication

```python
from ghost_hub_sdk.enterprise_auth import AuthManager

auth = AuthManager(secret_key="your-secret-key")

# Register user
auth.register_user(
    user_id="alice",
    name="Alice Wang",
    email="alice@company.com",
    roles=["engineer"],
    permissions=["workflow:execute", "device:control"]
)

# Generate API key
api_key = auth.generate_api_key("alice")
print(f"API Key: {api_key}")

# Authenticate
result = auth.authenticate_api_key(api_key)
if result.success:
    print(f"Authenticated as: {result.context.user_name}")
```

### JWT Authentication

```python
import jwt
import time

# Generate JWT token
payload = {
    'sub': 'alice',
    'name': 'Alice Wang',
    'email': 'alice@company.com',
    'roles': ['engineer'],
    'permissions': ['workflow:execute'],
    'exp': int(time.time()) + 3600
}

token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')

# Authenticate with JWT
result = auth.authenticate_jwt(token)
```

### LDAP Authentication

```python
from ghost_hub_sdk.enterprise_auth import LDAPConnector

ldap = LDAPConnector(
    server="ldap://ldap.company.com:389",
    base_dn="ou=users,dc=company,dc=com"
)

result = ldap.authenticate("alice", "password")
```

---

## Rate Limiting

### Configuration

```python
from ghost_hub_sdk.enterprise_auth import RateLimiter

limiter = RateLimiter()

# Default: 100 requests per minute
limiter.check_rate_limit("user123")

# Custom limits
limiter.set_limit("premium", requests=10000, window=60)

# Check with custom limit
limiter.check_rate_limit("premium_user", "premium")
```

### Implementation

```python
def rate_limit_handler(limiter, identifier, limit_type='default'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not limiter.check_rate_limit(identifier, limit_type):
                raise Exception("Rate limit exceeded")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit_handler(limiter, "user123", "default")
def my_endpoint():
    return {"status": "ok"}
```

---

## Permission System

### Permission Types

| Permission | Description |
|------------|-------------|
| `workflow:execute` | Execute workflows |
| `workflow:create` | Create custom workflows |
| `workflow:delete` | Delete workflows |
| `device:control` | Control IoT devices |
| `device:register` | Register new devices |
| `agent:manage` | Manage agents |
| `admin:*` | Full admin access |

### Checking Permissions

```python
auth = AuthManager("secret")
result = auth.authenticate_api_key("api-key")

if result.success:
    context = result.context
    
    if auth.check_permission(context, "workflow:execute"):
        print("Can execute workflows")
    
    if "admin" in context.roles:
        print("Is admin")
```

---

## API Gateway Integration

### Middleware Example

```python
from flask import Flask, request, jsonify
from ghost_hub_sdk.enterprise_auth import AuthManager, RateLimiter

app = Flask(__name__)
auth = AuthManager("secret")
limiter = RateLimiter()

@app.before_request
def auth_middleware():
    api_key = request.headers.get('X-API-Key')
    if api_key:
        result = auth.authenticate_api_key(api_key)
        if not result.success:
            return jsonify({"error": "Unauthorized"}), 401
        
        if not limiter.check_rate_limit(api_key):
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        request.auth_context = result.context
```

---

## Enterprise SSO Integration

### SAML Configuration

```yaml
sso:
  enabled: true
  provider: saml
  idp_metadata: https://idp.company.com/metadata
  sp_entity_id: ghost-hub-sdk
  acs_url: https://api.ghosthub.dev/auth/saml/callback
```

### OAuth2 Configuration

```yaml
oauth2:
  enabled: true
  provider: azure_ad
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
  auth_url: https://login.microsoftonline.com/TENANT/oauth2/v2.0/authorize
  token_url: https://login.microsoftonline.com/TENANT/oauth2/v2.0/token
  scopes:
    - openid
    - profile
    - email
    - https://graph.microsoft.com/.default
```

---

## Audit Logging

### Configuration

```yaml
audit:
  enabled: true
  retention_days: 90
  events:
    - authentication
    - workflow_execution
    - device_control
    - configuration_change
    - permission_change
```

### Integration

```python
from ghost_hub_sdk.logging_config import audit_logger

# Log authentication
audit_logger.log_access(
    user="alice",
    resource="/api/workflows/execute",
    granted=True
)

# Log action
audit_logger.log_action(
    action="workflow_execute",
    user="alice",
    resource="hr_recruitment",
    result="success",
    details={
        "workflow_id": "wf_123",
        "duration": 2.5
    }
)
```

---

## High Availability

### Load Balancer Configuration

```
Upstream ghost_hub_backend {
    server sdk-1:8080;
    server sdk-2:8080;
    server sdk-3:8080;
}

server {
    listen 443 ssl;
    
    location /api {
        proxy_pass http://ghost_hub_backend;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Session Affinity

```python
# For stateful operations, enable sticky sessions
# Load balancer should route same user to same instance
```

---

## Compliance

### GDPR Compliance

```python
# Data export
def export_user_data(user_id):
    return {
        'workflows': get_user_workflows(user_id),
        'devices': get_user_devices(user_id),
        'audit_logs': get_user_audit_logs(user_id)
    }

# Data deletion
def delete_user_data(user_id):
    delete_workflows(user_id)
    delete_devices(user_id)
    delete_audit_logs(user_id)
    delete_user(user_id)
```

### SOC 2 Compliance

- All access logged with timestamp
- Encryption in transit (TLS 1.3)
- Encryption at rest (AES-256)
- Regular security audits
- Incident response plan
