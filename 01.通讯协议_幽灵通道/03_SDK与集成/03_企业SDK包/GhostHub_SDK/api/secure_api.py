"""
Ghost Hub SDK - 安全增强API示例

展示如何集成安全模块：
1. API Key认证
2. 输入验证
3. 敏感数据脱敏
4. 请求频率限制
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, HTTPException, Header, Depends, Request
from typing import Optional
import logging

from ghost_hub_sdk.security import (
    SimpleAuth,
    InputValidator,
    SensitiveDataProtector,
    RateLimiter,
    SecurityChecker,
    AuthConfig,
)
from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Ghost Hub API (安全增强版)",
    description="企业级AI工作流编排器 - 含完整安全防护",
    version="1.0.0",
)

# ==================== 安全组件初始化 ====================

# 1. 认证
auth = SimpleAuth(AuthConfig())

# 2. 限流
rate_limiter = RateLimiter(requests_per_minute=60, burst=10)

# 3. 初始化Ghost Hub SDK
sdk = GhostHubSDK(GhostHubConfig())


# ==================== 依赖注入 ====================


async def get_api_key(x_api_key: Optional[str] = Header(None)):
    """验证API Key"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="缺少API Key")

    key_info = auth.validate_api_key(x_api_key)
    if not key_info:
        raise HTTPException(status_code=401, detail="无效的API Key")

    return x_api_key


async def check_rate_limit(request: Request, api_key: str = Depends(get_api_key)):
    """检查请求频率"""
    client_ip = request.client.host if request.client else "unknown"
    rate_key = f"{client_ip}:{api_key}"

    if not rate_limiter.check(rate_key):
        remaining = rate_limiter.get_remaining(rate_key)
        raise HTTPException(
            status_code=429, detail=f"请求过于频繁，请稍后再试。剩余请求数: {remaining}"
        )

    return rate_key


# ==================== 安全端点示例 ====================


@app.post("/api/secure/intent", summary="安全意图解析")
async def secure_intent_parse(
    intent_text: str, request: Request, api_key: str = Depends(check_rate_limit)
):
    """
    安全意图解析端点

    安全特性:
    - API Key认证
    - 请求频率限制
    - 输入验证
    - 日志脱敏
    """
    # 输入验证
    if not InputValidator.validate_intent_text(intent_text):
        raise HTTPException(status_code=400, detail="无效的意图文本")

    # 安全脱敏
    safe_intent = InputValidator.sanitize_text(intent_text)

    # 执行
    result = sdk.execute_workflow(safe_intent)

    # 脱敏日志
    logger.info(
        SensitiveDataProtector.safe_log(
            f"意图解析请求 | 客户端: {request.client.host}", {"intent": safe_intent[:50]}
        )
    )

    return {
        "success": True,
        "result": result,
        "remaining_requests": rate_limiter.get_remaining(api_key),
    }


@app.post("/api/secure/device/command", summary="安全设备控制")
async def secure_device_command(
    device_id: str,
    command: str,
    params: Optional[dict] = None,
    api_key: str = Depends(get_api_key),
    rate_key: str = Depends(check_rate_limit),
):
    """
    安全设备控制端点

    安全特性:
    - 命令白名单验证
    - 设备ID验证
    - 参数类型和范围验证
    """
    # 验证设备ID
    if not InputValidator.validate_device_id(device_id):
        raise HTTPException(status_code=400, detail="无效的设备ID")

    # 验证命令
    if not InputValidator.validate_command(command):
        raise HTTPException(status_code=400, detail="无效的命令")

    # 验证参数
    allowed_params = ["temperature", "brightness", "duration"]
    validated_params = InputValidator.validate_params(params or {}, allowed_params)

    # 执行
    result = sdk.no_ui_adapter.send_command(device_id, command, **validated_params)

    return {
        "success": result.success,
        "message": result.message,
        "remaining_requests": rate_limiter.get_remaining(rate_key),
    }


@app.get("/api/admin/keys", summary="管理API Keys")
async def list_api_keys(api_key: str = Depends(get_api_key)):
    """列出API Keys (仅管理员)"""
    key_info = auth.validate_api_key(api_key)

    if "admin" not in key_info.get("permissions", []):
        raise HTTPException(status_code=403, detail="需要管理员权限")

    stats = auth.get_stats()

    return {
        "total_keys": stats["total_keys"],
        "active_keys_7d": stats["active_keys_7d"],
        "total_requests": stats["total_requests"],
    }


@app.post("/api/admin/keys/generate", summary="生成新API Key")
async def generate_api_key(
    name: str, permissions: list = ["read"], admin_key: str = Depends(get_api_key)
):
    """生成新的API Key (仅管理员)"""
    key_info = auth.validate_api_key(admin_key)

    if "admin" not in key_info.get("permissions", []):
        raise HTTPException(status_code=403, detail="需要管理员权限")

    new_key = auth.generate_api_key()
    auth.add_api_key(new_key, name, permissions)

    return {
        "api_key": new_key,  # 仅首次返回完整密钥
        "name": name,
        "permissions": permissions,
        "warning": "请妥善保存密钥，丢失后将无法找回",
    }


@app.get("/api/security/check", summary="安全检查")
async def security_check():
    """执行安全配置检查"""
    issues = SecurityChecker.check_all()

    return {
        "total_issues": len(issues),
        "issues": issues,
        "recommendations": [
            "生产环境请更换JWT密钥",
            "限制CORS来源",
            "启用请求日志审计",
            "定期轮换API Keys",
        ],
    }


@app.get("/api/health", summary="健康检查")
async def health_check():
    """健康检查 (无需认证)"""
    return {"status": "healthy", "version": "1.0.0", "security": "enabled"}


# ==================== 初始化 ====================


@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    # 添加默认API Key (演示用，生产环境应删除或通过环境变量覆盖)
    import os
    demo_key = os.environ.get("GHOST_HUB_DEMO_KEY", "ghsk-demo-key-for-testing-only-12345")
    auth.add_api_key(demo_key, "demo_user", permissions=["read", "write"])

    # 执行安全检查
    issues = SecurityChecker.check_all()
    if issues:
        logger.warning(f"发现 {len(issues)} 个安全问题")
        for issue in issues:
            logger.warning(f"  [{issue['severity']}] {issue['message']}")

    logger.info("Ghost Hub API (安全增强版) 已启动")
    logger.info(f"演示API Key: {demo_key}")


@app.on_event("shutdown")
async def shutdown_event():
    """关闭时清理"""
    logger.info("Ghost Hub API 已关闭")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
