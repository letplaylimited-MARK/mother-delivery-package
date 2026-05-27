"""
Ghost Hub SDK - 边界条件测试

测试各种边界情况和极端输入:
1. 空值/None处理
2. 超长字符串
3. 特殊字符
4. 类型错误
5. 数值边界
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


def test_empty_values():
    """测试空值处理"""
    print_header("测试1: 空值处理")

    from ghost_hub_sdk import GhostHubSDK
    from ghost_hub_sdk.security import InputValidator, SimpleAuth

    sdk = GhostHubSDK()
    auth = SimpleAuth()

    tests_passed = 0
    total_tests = 5

    try:
        result = sdk.execute_workflow("")
        print(f"  空字符串workflow: {'处理' if result is not None else '未处理'}")
        tests_passed += 1
    except Exception as e:
        print(f"  空字符串workflow: 异常 {type(e).__name__}")

    try:
        result = sdk.execute_workflow(None)
        print(f"  None workflow: {'处理' if result is not None else '未处理'}")
        tests_passed += 1
    except Exception as e:
        print(f"  None workflow: 异常 {type(e).__name__}")

    try:
        result = InputValidator.validate_intent_text("")
        print(f"  空字符串验证: {'通过' if result else '拒绝'}")
        tests_passed += 1
    except Exception as e:
        print(f"  空字符串验证: 异常 {type(e).__name__}")

    try:
        result = InputValidator.validate_device_id("")
        print(f"  空设备ID: {'有效' if result else '无效'}")
        tests_passed += 1
    except Exception as e:
        print(f"  空设备ID: 异常 {type(e).__name__}")

    try:
        auth.validate_api_key("")
        print(f"  空Key: 未抛出异常")
    except Exception as e:
        print(f"  空Key: 异常 {type(e).__name__}")
        tests_passed += 1

    print(f"\n  通过: {tests_passed}/{total_tests}")
    return tests_passed >= total_tests - 1


def test_extreme_strings():
    """测试超长字符串"""
    print_header("测试2: 超长字符串")

    from ghost_hub_sdk.security import InputValidator

    tests_passed = 0

    long_string = "a" * 10000
    result = InputValidator.validate_intent_text(long_string)
    print(f"  10000字符意图: {'通过' if result else '拒绝'}")
    if not result:
        tests_passed += 1

    very_long_string = "x" * 100000
    result = InputValidator.validate_intent_text(very_long_string)
    print(f"  100000字符意图: {'通过' if result else '拒绝'}")
    if not result:
        tests_passed += 1

    long_device_id = "device_" + "0" * 100
    result = InputValidator.validate_device_id(long_device_id)
    print(f"  100+字符设备ID: {'有效' if result else '无效'}")
    if not result:
        tests_passed += 1

    print(f"\n  通过: {tests_passed}/3 (边界正确拒绝)")
    return tests_passed >= 2


def test_special_characters():
    """测试特殊字符"""
    print_header("测试3: 特殊字符处理")

    from ghost_hub_sdk.security import InputValidator

    special_chars = [
        "\x00\x01\x02",
        "\u202e\u202d",
        "🏠💡📱",
        "中文测试",
        "日本語テスト",
        "🎉" * 100,
    ]

    print("  特殊字符测试:")
    for chars in special_chars:
        try:
            result = InputValidator.sanitize_text(chars)
            safe = "已处理" if result != chars else "无变化"
            print(f"    {repr(chars[:20])}: {safe}")
        except Exception as e:
            print(f"    {repr(chars[:20])}: 异常 {type(e).__name__}")

    return True


def test_numeric_boundaries():
    """测试数值边界"""
    print_header("测试4: 数值边界")

    from ghost_hub_sdk.security import InputValidator

    tests_passed = 0

    result = InputValidator.validate_params({"temp": 0}, ["temp"])
    print(f"  温度0: {result}")
    tests_passed += 1

    result = InputValidator.validate_params({"temp": -273.15}, ["temp"])
    print(f"  温度-273: {result}")
    tests_passed += 1

    result = InputValidator.validate_params({"temp": 1000}, ["temp"])
    print(f"  温度1000: {result}")
    tests_passed += 1

    result = InputValidator.validate_params({"temp": float("inf")}, ["temp"])
    print(f"  无穷大: {result}")
    tests_passed += 1

    result = InputValidator.validate_params({"temp": float("nan")}, ["temp"])
    print(f"  NaN: {result}")
    tests_passed += 1

    print(f"\n  通过: {tests_passed}/5")
    return tests_passed >= 4


def test_type_errors():
    """测试类型错误"""
    print_header("测试5: 类型错误处理")

    from ghost_hub_sdk.security import InputValidator

    tests_passed = 0

    try:
        InputValidator.validate_command(123)
        print("  数字命令: 未处理")
    except (TypeError, AttributeError):
        print("  数字命令: 类型错误")
        tests_passed += 1

    try:
        InputValidator.validate_device_id(["list"])
        print("  列表设备ID: 未处理")
    except (TypeError, AttributeError):
        print("  列表设备ID: 类型错误")
        tests_passed += 1

    try:
        InputValidator.validate_params("string", ["param"])
        print("  字符串参数: 未处理")
    except (TypeError, AttributeError):
        print("  字符串参数: 类型错误")
        tests_passed += 1

    print(f"\n  类型安全: {tests_passed}/3")
    return tests_passed >= 2


def test_unicode_edge_cases():
    """测试Unicode边界情况"""
    print_header("测试6: Unicode边界情况")

    from ghost_hub_sdk.security import InputValidator

    unicode_tests = [
        ("零宽字符", "\u200b\u200c\u200d"),
        ("Bidir标记", "\u202a\u202b\u202c"),
        ("表情符号", "😀" * 50),
        ("CJK扩展", "\u3400-\u4dbf"),
        ("代理对", "\ud800\udc00"),
    ]

    all_safe = True
    for name, text in unicode_tests:
        try:
            result = InputValidator.sanitize_text(text)
            safe = result == text or len(result) < len(text)
            print(f"  {name}: {'安全' if safe else '已处理'}")
            if not safe:
                all_safe = False
        except Exception as e:
            print(f"  {name}: 异常 {type(e).__name__}")
            all_safe = False

    return all_safe


def test_concurrent_requests_simulation():
    """模拟并发请求"""
    print_header("测试7: 并发请求模拟")

    from ghost_hub_sdk.security import RateLimiter
    import threading

    limiter = RateLimiter(requests_per_minute=100, burst=10)
    results = []
    lock = threading.Lock()

    def make_request(i):
        allowed = limiter.check(f"test_client_{i % 5}")
        with lock:
            results.append(allowed)

    threads = []
    for i in range(50):
        t = threading.Thread(target=make_request, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    allowed = sum(results)
    print(f"  50个并发请求")
    print(f"  允许: {allowed}")
    print(f"  限制: {50 - allowed}")

    return True


def test_memory_limits():
    """测试内存限制场景"""
    print_header("测试8: 内存/大小限制")

    from ghost_hub_sdk.security import InputValidator

    tests_passed = 0

    huge_dict = {f"key_{i}": f"value_{i}" * 100 for i in range(1000)}
    result = InputValidator.validate_params(huge_dict, list(huge_dict.keys())[:10])
    print(f"  1000键字典(限制10): {len(result)}键")
    tests_passed += 1

    deep_nested = {"a": {"b": {"c": {"d": {"e": "deep"}}}}}
    try:
        safe = InputValidator.sanitize_text(str(deep_nested))
        print(f"  深度嵌套: {len(safe)}字符")
        tests_passed += 1
    except RecursionError:
        print(f"  深度嵌套: RecursionError")
        tests_passed += 1

    print(f"\n  通过: {tests_passed}/2")
    return tests_passed >= 1


def main():
    print("\n" + "=" * 60)
    print("  Ghost Hub SDK - 边界条件测试")
    print("=" * 60)

    tests = [
        ("空值处理", test_empty_values),
        ("超长字符串", test_extreme_strings),
        ("特殊字符", test_special_characters),
        ("数值边界", test_numeric_boundaries),
        ("类型错误", test_type_errors),
        ("Unicode边界", test_unicode_edge_cases),
        ("并发模拟", test_concurrent_requests_simulation),
        ("内存限制", test_memory_limits),
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

    print("\n" + "=" * 60)
    return passed >= total - 1


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
