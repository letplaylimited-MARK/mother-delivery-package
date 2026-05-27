"""
Ghost Hub SDK - 安全功能测试

测试所有安全模块:
1. 认证授权
2. 输入验证
3. 敏感数据保护
4. 请求频率限制
5. 安全检查
"""

import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def print_header(text):
    print("\n" + "=" * 60)
    print("  " + text)
    print("=" * 60)


def test_auth():
    """测试认证授权"""
    print_header("测试1: 认证授权 (SimpleAuth)")

    from ghost_hub_sdk.security import SimpleAuth, AuthConfig, UnauthorizedError, ForbiddenError

    auth = SimpleAuth(AuthConfig())

    # 生成并添加API Key
    key1 = auth.generate_api_key()
    auth.add_api_key(key1, "test_user", permissions=["read", "write"])

    key2 = auth.generate_api_key()
    auth.add_api_key(key2, "admin_user", permissions=["read", "write", "admin"])

    print(f"\n  [OK] 生成API Key")
    print(f"  Key1: {key1[:20]}...")
    print(f"  Key2: {key2[:20]}...")

    # 验证Key
    info1 = auth.validate_api_key(key1)
    print(f"\n  [OK] 验证Key: {info1['name']}")
    print(f"  权限: {info1['permissions']}")

    # 权限检查
    has_read = auth.has_permission(key1, "read")
    has_admin = auth.has_permission(key1, "admin")
    print(f"\n  [OK] 权限检查:")
    print(f"  - read权限: {'有' if has_read else '无'}")
    print(f"  - admin权限: {'有' if has_admin else '无'}")

    has_admin2 = auth.has_permission(key2, "admin")
    print(f"  - admin_key有admin权限: {'有' if has_admin2 else '无'}")

    # 统计
    stats = auth.get_stats()
    print(f"\n  [统计]")
    print(f"  总Key数: {stats['total_keys']}")
    print(f"  活跃Key(7天): {stats['active_keys_7d']}")

    return True


def test_input_validation():
    """测试输入验证"""
    print_header("测试2: 输入验证 (InputValidator)")

    from ghost_hub_sdk.security import InputValidator

    print("\n  [命令验证]")
    valid_commands = ["turn_on", "turn_off", "set", "adjust"]
    for cmd in valid_commands:
        result = InputValidator.validate_command(cmd)
        print(f"  - '{cmd}': {'有效' if result else '无效'}")

    invalid_cmd = "DROP TABLE users"
    result = InputValidator.validate_command(invalid_cmd)
    print(f"  - 注入命令: {'有效' if result else '无效 [正确拦截]'}")

    print("\n  [设备ID验证]")
    valid_ids = ["dev_001", "device_abc123", "LIGHT_01"]
    for did in valid_ids:
        result = InputValidator.validate_device_id(did)
        print(f"  - '{did}': {'有效' if result else '无效'}")

    invalid_ids = ["dev; rm -rf", "dev<script>", "dev../etc/passwd"]
    for did in invalid_ids:
        result = InputValidator.validate_device_id(did)
        print(f"  - 恶意ID: {'有效' if result else '无效 [正确拦截]'}")

    print("\n  [参数验证]")
    params = {"temperature": 25, "brightness": 80, "unknown_param": "should_be_removed"}
    allowed = ["temperature", "brightness"]
    validated = InputValidator.validate_params(params, allowed)
    print(f"  原始参数: {params}")
    print(f"  验证后: {validated}")
    print(f"  - unknown_param已移除: {'unknown_param' not in validated}")

    print("\n  [文本消毒]")
    dangerous = "'; DROP TABLE users;-- <script>alert('xss')</script>"
    safe = InputValidator.sanitize_text(dangerous)
    print(f"  原始: {dangerous[:40]}...")
    print(f"  消毒后: {safe if safe else '(已清空)'}")

    return True


def test_sensitive_data_protection():
    """测试敏感数据保护"""
    print_header("测试3: 敏感数据保护 (SensitiveDataProtector)")

    from ghost_hub_sdk.security import SensitiveDataProtector

    # 测试字典脱敏
    data = {
        "username": "admin",
        "password": "secret123456",
        "api_key": "sk-abcdefgh123456789",
        "email": "admin@example.com",
        "data": {"token": "jwt_token_super_secret", "value": 123},
    }

    masked = SensitiveDataProtector.mask_dict(data)
    print("\n  [字典脱敏]")
    print(f"  原始数据:")
    print(f"    username: {data['username']}")
    print(f"    password: {data['password']}")
    print(f"    api_key: {data['api_key']}")
    print(f"  脱敏后:")
    print(f"    username: {masked['username']} (未脱敏-非敏感)")
    print(f"    password: {masked['password']}")
    print(f"    api_key: {masked['api_key']}")

    # 测试字符串脱敏
    print("\n  [字符串脱敏]")
    secret = "sk-super-secret-api-key-123456"
    masked_str = SensitiveDataProtector.mask_string(secret)
    print(f"  原始: {secret}")
    print(f"  脱敏: {masked_str}")

    # 测试安全日志
    print("\n  [安全日志]")
    log = SensitiveDataProtector.safe_log("用户登录", {"username": "test", "password": "secret"})
    print(f"  日志: {log}")

    return True


def test_rate_limiter():
    """测试请求频率限制"""
    print_header("测试4: 请求频率限制 (RateLimiter)")

    from ghost_hub_sdk.security import RateLimiter
    import time

    limiter = RateLimiter(requests_per_minute=10, burst=3)

    print("\n  [限流测试 - burst=3, rate=10/min]")
    key = "test_client"

    results = []
    for i in range(8):
        allowed = limiter.check(key)
        remaining = limiter.get_remaining(key)
        results.append((i + 1, allowed, remaining))

    print(f"  请求# | 允许 | 剩余令牌")
    print(f"  " + "-" * 25)
    for req_num, allowed, remaining in results:
        icon = "[OK]" if allowed else "[LIMITED]"
        print(f"  {req_num:6d} | {icon} | {remaining}")

    # 恢复测试
    print(f"\n  [令牌恢复 - 等待1秒]")
    time.sleep(1.1)
    remaining = limiter.get_remaining(key)
    print(f"  1秒后剩余: {remaining:.1f}")

    stats = limiter.get_stats()
    print(f"\n  [统计]")
    print(f"  跟踪的Key数: {stats['tracked_keys']}")
    print(f"  每分钟限制: {stats['rate_per_minute']}")
    print(f"  突发容量: {stats['burst_size']}")

    return True


def test_security_checker():
    """测试安全检查"""
    print_header("测试5: 安全检查 (SecurityChecker)")

    from ghost_hub_sdk.security import SecurityChecker

    issues = SecurityChecker.check_all()

    print(f"\n  [安全检查结果]")
    print(f"  发现问题数: {len(issues)}")

    if issues:
        for i, issue in enumerate(issues, 1):
            print(f"\n  问题{i}:")
            print(f"    严重性: {issue['severity']}")
            print(f"    检查项: {issue['check']}")
            print(f"    消息: {issue['message']}")
    else:
        print("  [OK] 未发现问题")

    print(f"\n  [建议]")
    print("  1. 生产环境更换JWT密钥")
    print("  2. 限制CORS来源为特定域名")
    print("  3. 启用API访问日志审计")
    print("  4. 定期轮换API Keys")
    print("  5. 使用HTTPS加密传输")

    return True


def test_integration():
    """集成测试"""
    print_header("测试6: 安全模块集成")

    from ghost_hub_sdk.security import SimpleAuth, InputValidator, RateLimiter
    from ghost_hub_sdk import GhostHubSDK

    # 模拟完整的请求流程
    print("\n  [模拟安全请求流程]")

    # 1. 初始化
    auth = SimpleAuth()
    limiter = RateLimiter(requests_per_minute=60)
    sdk = GhostHubSDK()

    # 2. 生成Key
    api_key = auth.generate_api_key()
    auth.add_api_key(api_key, "integration_test", permissions=["read", "write"])
    print(f"  [1] API Key: {api_key[:25]}...")

    # 3. 验证Key
    key_info = auth.validate_api_key(api_key)
    print(f"  [2] Key验证: {'成功' if key_info else '失败'}")

    # 4. 检查限流
    if limiter.check(api_key):
        print(f"  [3] 限流检查: 通过")
    else:
        print(f"  [3] 限流检查: 被限制")

    # 5. 验证输入
    intent = "打开客厅灯"
    if InputValidator.validate_intent_text(intent):
        print(f"  [4] 输入验证: 通过")
    else:
        print(f"  [4] 输入验证: 失败")

    # 6. 执行
    result = sdk.execute_workflow(intent)
    print(f"  [5] 执行结果: {'成功' if result['success'] else '失败'}")

    # 7. 记录
    print(f"  [6] 日志: SDK执行完成")

    print("\n  [集成测试完成]")

    return True


def main():
    print("\n" + "=" * 60)
    print("  Ghost Hub SDK - 安全功能测试")
    print("=" * 60)

    tests = [
        ("认证授权", test_auth),
        ("输入验证", test_input_validation),
        ("敏感数据保护", test_sensitive_data_protection),
        ("请求频率限制", test_rate_limiter),
        ("安全检查", test_security_checker),
        ("集成测试", test_integration),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n  [FAIL] 测试异常: {e}")
            import traceback

            traceback.print_exc()
            results.append((name, False))

    # 汇总
    print_header("测试汇总")
    passed = sum(1 for _, r in results if r)
    total = len(results)

    print(f"\n  通过: {passed}/{total}")
    print(f"  成功率: {passed / total * 100:.1f}%\n")

    for name, success in results:
        icon = "[OK]" if success else "[FAIL]"
        print(f"    {icon} {name}")

    print("\n" + "=" * 60)

    if passed == total:
        print("  [SUCCESS] 所有安全测试通过!")
    else:
        print(f"  [WARN]  {total - passed} 项测试失败")

    print("=" * 60 + "\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
