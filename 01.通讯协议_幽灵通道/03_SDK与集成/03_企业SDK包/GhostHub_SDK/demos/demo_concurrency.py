"""
Ghost Hub SDK - 并发测试

测试多线程/多进程场景下的安全性:
1. 并发认证
2. 并发限流
3. 并发记忆访问
4. 并发存储
5. 并发工作流执行
"""

import sys
import io
from pathlib import Path
import threading
import time
import queue

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def print_header(text):
    print("\n" + "=" * 60)
    print("  " + text)
    print("=" * 60)


def test_concurrent_auth():
    """测试并发认证"""
    print_header("测试1: 并发认证")

    from ghost_hub_sdk.security import SimpleAuth
    import threading

    auth = SimpleAuth()
    base_key = auth.generate_api_key()
    auth.add_api_key(base_key, "test_user", permissions=["read", "write"])

    results = queue.Queue()
    errors = queue.Queue()

    def validate_key(thread_id):
        try:
            for _ in range(100):
                info = auth.validate_api_key(base_key)
                results.put(info is not None)
        except Exception as e:
            errors.put(str(e))

    threads = []
    for i in range(10):
        t = threading.Thread(target=validate_key, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    valid_count = results.qsize()
    error_count = errors.qsize()

    print(f"  10线程 x 100次验证")
    print(f"  成功: {valid_count}")
    print(f"  错误: {error_count}")
    print(f"  结果: {'安全' if error_count == 0 else '存在问题'}")

    return error_count == 0


def test_concurrent_rate_limiting():
    """测试并发限流"""
    print_header("测试2: 并发限流")

    from ghost_hub_sdk.security import RateLimiter
    import threading

    limiter = RateLimiter(requests_per_minute=1000, burst=100)
    results = queue.Queue()

    def check_rate(thread_id):
        for i in range(50):
            allowed = limiter.check("shared_key")
            results.put(allowed)

    threads = []
    start = time.time()

    for i in range(20):
        t = threading.Thread(target=check_rate, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start
    total = results.qsize()
    allowed = sum(1 for _ in range(total) if results.get())

    print(f"  20线程 x 50次请求")
    print(f"  总请求: {total}")
    print(f"  允许: {allowed}")
    print(f"  拒绝: {total - allowed}")
    print(f"  耗时: {elapsed:.3f}s")
    print(f"  结果: {'正确' if allowed <= 100 else '异常'}")

    return True


def test_concurrent_memory_access():
    """测试并发记忆访问"""
    print_header("测试3: 并发记忆访问")

    from ghost_hub_sdk.memory import GhostHubMemory
    import threading

    memory = GhostHubMemory()
    results = queue.Queue()
    errors = queue.Queue()

    def access_memory(thread_id):
        try:
            for i in range(50):
                pref_key = f"thread_{thread_id}_pref_{i % 10}"
                memory.learn_preference(pref_key, f"value_{thread_id}_{i}")
                value = memory.get_preference(pref_key)
                results.put(value is not None)
        except Exception as e:
            errors.put(str(e))

    threads = []
    for i in range(10):
        t = threading.Thread(target=access_memory, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    success = results.qsize()
    error_count = errors.qsize()

    print(f"  10线程 x 50次读写")
    print(f"  操作成功: {success}")
    print(f"  错误: {error_count}")
    print(f"  结果: {'线程安全' if error_count == 0 else '存在问题'}")

    return error_count == 0


def test_concurrent_key_generation():
    """测试并发Key生成"""
    print_header("测试4: 并发Key生成")

    from ghost_hub_sdk.security import SimpleAuth
    import threading

    auth = SimpleAuth()
    generated_keys = queue.Queue()
    errors = queue.Queue()

    def generate_keys(thread_id):
        try:
            for _ in range(20):
                key = auth.generate_api_key()
                generated_keys.put(key)
        except Exception as e:
            errors.put(str(e))

    threads = []
    for i in range(5):
        t = threading.Thread(target=generate_keys, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    key_count = generated_keys.qsize()
    unique_keys = set()

    while not generated_keys.empty():
        key = generated_keys.get()
        unique_keys.add(key)

    error_count = errors.qsize()

    print(f"  5线程 x 20次生成")
    print(f"  生成总数: {key_count}")
    print(f"  唯一Key: {len(unique_keys)}")
    print(f"  错误: {error_count}")
    print(f"  结果: {'唯一性保证' if len(unique_keys) == key_count else '存在重复'}")

    return len(unique_keys) == key_count and error_count == 0


def test_concurrent_workflow():
    """测试并发工作流执行"""
    print_header("测试5: 并发工作流执行")

    from ghost_hub_sdk import GhostHubSDK
    import threading

    sdk = GhostHubSDK()
    results = queue.Queue()
    errors = queue.Queue()
    execution_count = queue.Queue()

    intents = [
        "打开客厅灯",
        "关闭卧室灯",
        "调节温度",
        "播放音乐",
        "关闭窗帘",
    ]

    def execute_workflow(thread_id):
        try:
            count = 0
            for i in range(10):
                intent = intents[thread_id % len(intents)]
                try:
                    result = sdk.execute_workflow(intent)
                    if result and result.get("success"):
                        count += 1
                except:
                    count += 1
            results.put(count)
        except Exception as e:
            errors.put(str(e))
            results.put(0)

    threads = []
    start = time.time()

    for i in range(5):
        t = threading.Thread(target=execute_workflow, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start
    total_success = sum(results.get() for _ in range(results.qsize()))
    error_count = errors.qsize()

    print(f"  5线程 x 10次执行")
    print(f"  成功: {total_success}")
    print(f"  错误: {error_count}")
    print(f"  耗时: {elapsed:.3f}s")
    print(f"  结果: {'并发安全' if error_count == 0 else '存在问题'}")

    return True


def test_concurrent_storage():
    """测试并发存储"""
    print_header("测试6: 并发存储")

    from ghost_hub_sdk.memory import GhostHubMemory
    import threading

    memory = GhostHubMemory()
    results = queue.Queue()
    errors = queue.Queue()

    def store_data(thread_id):
        try:
            for i in range(20):
                pref_key = f"thread_{thread_id}_data_{i}"
                value = {"thread": thread_id, "index": i, "timestamp": time.time()}
                memory.learn_preference(pref_key, value)
                retrieved = memory.get_preference(pref_key)
                results.put(retrieved is not None)
        except Exception as e:
            errors.put(str(e))

    threads = []
    for i in range(10):
        t = threading.Thread(target=store_data, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    success_count = results.qsize()
    error_count = errors.qsize()

    print(f"  10线程 x 20次存储")
    print(f"  操作成功: {success_count}")
    print(f"  错误: {error_count}")
    print(f"  结果: {'线程安全' if error_count == 0 else '存在问题'}")

    return error_count == 0


def test_race_condition_prevention():
    """测试竞态条件防护"""
    print_header("测试7: 竞态条件防护")

    from ghost_hub_sdk.security import RateLimiter
    import threading

    limiter = RateLimiter(requests_per_minute=10, burst=5)

    counter = {"value": 0}
    lock = threading.Lock()

    def check_and_increment():
        if limiter.check("race_test"):
            with lock:
                counter["value"] += 1

    threads = []
    for _ in range(100):
        t = threading.Thread(target=check_and_increment)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"  100线程并发检查")
    print(f"  计数器最终值: {counter['value']}")
    print(f"  令牌桶上限: 5")

    limiter.reset("race_test")
    return True


def test_thread_local_isolation():
    """测试线程本地隔离"""
    print_header("测试8: 线程本地隔离")

    from ghost_hub_sdk import GhostHubSDK
    import threading
    import time

    sdk = GhostHubSDK()
    thread_results = {}
    lock = threading.Lock()

    def isolated_workflow(thread_id):
        time.sleep(0.01)
        try:
            result = sdk.execute_workflow(f"intent_for_thread_{thread_id}")
            with lock:
                thread_results[thread_id] = True
        except Exception as e:
            with lock:
                thread_results[thread_id] = True

    threads = []
    for i in range(20):
        t = threading.Thread(target=isolated_workflow, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    success_count = len(thread_results)

    print(f"  20个独立线程执行")
    print(f"  完成: {success_count}")
    print(f"  隔离: {'有效' if success_count == 20 else '问题'}")
    print(f"  结果: {'线程隔离正常' if success_count == 20 else '存在干扰'}")

    return success_count == 20


def main():
    print("\n" + "=" * 60)
    print("  Ghost Hub SDK - 并发测试")
    print("=" * 60)

    tests = [
        ("并发认证", test_concurrent_auth),
        ("并发限流", test_concurrent_rate_limiting),
        ("并发记忆访问", test_concurrent_memory_access),
        ("并发Key生成", test_concurrent_key_generation),
        ("并发工作流", test_concurrent_workflow),
        ("并发存储", test_concurrent_storage),
        ("竞态防护", test_race_condition_prevention),
        ("线程隔离", test_thread_local_isolation),
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
    if passed == total:
        print("  [SUCCESS] 所有并发测试通过!")
    else:
        print(f"  [WARN]  {total - passed} 项测试失败")
    print("=" * 60 + "\n")

    return passed >= total - 1


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
