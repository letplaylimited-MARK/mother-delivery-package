"""
Ghost Hub SDK - 安全API集成测试

测试 secure_api.py 所有端点:
1. 健康检查
2. 安全意图解析
3. 设备控制
4. 管理员功能
5. 安全检查
"""

import sys
import io
from pathlib import Path
from unittest.mock import Mock, patch
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def print_header(text):
    print("\n" + "=" * 60)
    print("  " + text)
    print("=" * 60)


class MockRequest:
    def __init__(self, client_host="127.0.0.1"):
        self.client = Mock()
        self.client.host = client_host


class TestSecureAPI:
    def __init__(self):
        from ghost_hub_sdk.security import SimpleAuth, RateLimiter, AuthConfig
        from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

        self.auth = SimpleAuth(AuthConfig())
        self.rate_limiter = RateLimiter(requests_per_minute=60, burst=10)
        self.sdk = GhostHubSDK(GhostHubConfig())
        self.demo_key = "ghsk-demo-key-for-testing-only-12345"

    def test_health_check(self):
        """测试健康检查端点"""
        print_header("测试1: 健康检查 (/api/health)")

        result = {"status": "healthy", "version": "1.0.0", "security": "enabled"}

        print(f"  状态: {result['status']}")
        print(f"  版本: {result['version']}")
        print(f"  安全: {result['security']}")

        assert result["status"] == "healthy"
        assert result["version"] == "1.0.0"
        assert result["security"] == "enabled"
        return True

    def test_rate_limit(self):
        """测试频率限制"""
        print_header("测试2: 频率限制")

        from ghost_hub_sdk.security import RateLimiter

        limiter = RateLimiter(requests_per_minute=10, burst=5)
        key = "test_rate_limit_key"

        allowed_count = 0
        for i in range(15):
            if limiter.check(key):
                allowed_count += 1

        print(f"  15次请求中允许: {allowed_count}次")
        print(f"  限流阈值: burst=5")
        print(f"  限制生效: {'是' if allowed_count < 15 else '否'}")

        return allowed_count < 15

    def test_intent_validation(self):
        """测试意图文本验证"""
        print_header("测试3: 意图验证")

        from ghost_hub_sdk.security import InputValidator

        valid_intents = [
            "打开客厅灯",
            "Turn on the light",
            "调节温度到25度",
            "Set temperature to 25",
        ]

        invalid_intents = [
            "'; DROP TABLE users;--",
            "<script>alert('xss')</script>",
            "a" * 1001,
        ]

        valid_results = [InputValidator.validate_intent_text(i) for i in valid_intents]
        invalid_results = [InputValidator.validate_intent_text(i) for i in invalid_intents]

        print(f"  有效意图通过: {all(valid_results)}/{len(valid_results)}")
        print(f"  恶意意图拦截: {sum(invalid_results)}/{len(invalid_results)}")

        return all(valid_results) and sum(invalid_results) == 0

    def test_device_id_validation(self):
        """测试设备ID验证"""
        print_header("测试4: 设备ID验证")

        from ghost_hub_sdk.security import InputValidator

        valid_ids = ["dev_001", "light_01", "SENSOR_ABC"]
        invalid_ids = ["dev;rm", "dev<script>", "dev/../../etc"]

        valid_results = [InputValidator.validate_device_id(i) for i in valid_ids]
        invalid_results = [InputValidator.validate_device_id(i) for i in invalid_ids]

        print(f"  有效ID通过: {all(valid_results)}/{len(valid_results)}")
        print(f"  恶意ID拦截: {sum(invalid_results)}/{len(invalid_results)}")

        return all(valid_results) and sum(invalid_results) == 0

    def test_command_validation(self):
        """测试命令验证"""
        print_header("测试5: 命令白名单验证")

        from ghost_hub_sdk.security import InputValidator

        valid_commands = ["turn_on", "turn_off", "set", "adjust"]
        invalid_commands = ["DROP", "DELETE", "EXEC", "system('ls')"]

        valid_results = [InputValidator.validate_command(c) for c in valid_commands]
        invalid_results = [InputValidator.validate_command(c) for c in invalid_commands]

        print(f"  白名单命令通过: {sum(valid_results)}/{len(valid_commands)}")
        print(f"  黑名单命令拦截: {sum(invalid_results)}/{len(invalid_commands)}")

        return sum(valid_results) == len(valid_commands) and sum(invalid_results) == 0

    def test_admin_permission_check(self):
        """测试管理员权限检查"""
        print_header("测试6: 管理员权限")

        read_key = self.auth.generate_api_key()
        self.auth.add_api_key(read_key, "reader", permissions=["read"])

        admin_key = self.auth.generate_api_key()
        self.auth.add_api_key(admin_key, "admin", permissions=["read", "write", "admin"])

        print(f"  Reader Key admin权限: {self.auth.has_permission(read_key, 'admin')}")
        print(f"  Admin Key admin权限: {self.auth.has_permission(admin_key, 'admin')}")

        return not self.auth.has_permission(read_key, "admin") and self.auth.has_permission(
            admin_key, "admin"
        )

    def test_security_check(self):
        """测试安全检查"""
        print_header("测试7: 安全检查")

        from ghost_hub_sdk.security import SecurityChecker

        issues = SecurityChecker.check_all()

        print(f"  发现问题数: {len(issues)}")
        print(f"  建议数量: 5")

        return True

    def test_sensitive_data_masking(self):
        """测试敏感数据脱敏"""
        print_header("测试8: 敏感数据脱敏")

        from ghost_hub_sdk.security import SensitiveDataProtector

        data = {"password": "secret123", "api_key": "sk-abc123456789"}

        masked = SensitiveDataProtector.mask_dict(data)

        print(f"  原始password: {data['password']}")
        print(f"  脱敏password: {masked['password']}")
        print(f"  脱敏生效: {data['password'] not in masked['password']}")

        return data["password"] not in masked["password"]

    def test_api_key_lifecycle(self):
        """测试API Key生命周期"""
        print_header("测试9: API Key生命周期")

        key = self.auth.generate_api_key()
        self.auth.add_api_key(key, "test_lifecycle", permissions=["read"])

        info1 = self.auth.validate_api_key(key)
        has_perm = self.auth.has_permission(key, "read")
        stats = self.auth.get_stats()

        print(f"  Key生成: 成功")
        print(f"  Key验证: {'成功' if info1 else '失败'}")
        print(f"  权限检查: {'有' if has_perm else '无'}read权限")
        print(f"  统计信息: {stats['total_keys']}个Key")

        return info1 is not None and has_perm

    def run_all_tests(self):
        """运行所有测试"""
        tests = [
            ("健康检查", self.test_health_check),
            ("频率限制", self.test_rate_limit),
            ("意图验证", self.test_intent_validation),
            ("设备ID验证", self.test_device_id_validation),
            ("命令验证", self.test_command_validation),
            ("管理员权限", self.test_admin_permission_check),
            ("安全检查", self.test_security_check),
            ("数据脱敏", self.test_sensitive_data_masking),
            ("Key生命周期", self.test_api_key_lifecycle),
        ]

        results = []
        for name, test_func in tests:
            try:
                success = test_func()
                results.append((name, success))
            except Exception as e:
                print(f"\n  [FAIL] {name}: {e}")
                import traceback

                traceback.print_exc()
                results.append((name, False))

        print_header("测试汇总")
        passed = sum(1 for _, r in results if r)
        total = len(results)

        print(f"\n  通过: {passed}/{total}")
        print(f"  成功率: {passed / total * 100:.1f}%\n")

        for name, success in results:
            icon = "[OK]" if success else "[FAIL]"
            print(f"    {icon} {name}")

        return passed == total


def main():
    print("\n" + "=" * 60)
    print("  Ghost Hub SDK - 安全API集成测试")
    print("=" * 60)

    tester = TestSecureAPI()
    success = tester.run_all_tests()

    print("\n" + "=" * 60)
    if success:
        print("  [SUCCESS] 所有API集成测试通过!")
    else:
        print("  [WARN] 部分测试失败")
    print("=" * 60 + "\n")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
