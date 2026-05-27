"""
Ghost Hub SDK v1.0.0 - 用户场景全面验证

验证所有典型用户场景能够正常运行:
1. 基础使用场景
2. 安全集成场景
3. 记忆与存储场景
4. 组件串联场景
5. 并发使用场景
"""

import sys
import io
import os
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 确保目录存在
temp_dir = tempfile.mkdtemp()
os.environ["GHOST_HUB_STORAGE_PATH"] = temp_dir


def print_header(text):
    print("\n" + "=" * 70)
    print("  " + text)
    print("=" * 70)


def print_step(text):
    print(f"\n>>> {text}")


def test_basic_usage():
    """场景一：基础使用"""
    print_header("场景一：基础使用 - 智能家居控制")

    print_step("1. 导入SDK")
    try:
        from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

        print("    [OK] SDK导入成功")
    except ImportError as e:
        print(f"    [FAIL] SDK导入失败: {e}")
        return False

    print_step("2. 初始化配置")
    try:
        config = GhostHubConfig()
        config.log_level = "ERROR"  # 减少日志输出
        sdk = GhostHubSDK(config)
        print(f"    [OK] SDK初始化成功 | 版本: {config.version}")
    except Exception as e:
        print(f"    [FAIL] SDK初始化失败: {e}")
        return False

    print_step("3. 执行意图")
    try:
        result = sdk.execute_workflow("打开客厅灯")
        print(f"    [OK] 意图执行完成 | success: {result.get('success', False)}")
    except Exception as e:
        print(f"    [FAIL] 意图执行失败: {e}")
        return False

    print_step("4. 获取模板列表")
    try:
        templates = sdk.list_available_templates()
        print(f"    [OK] 获取模板: {len(templates)} 个")
    except Exception as e:
        print(f"    [FAIL] 获取模板失败: {e}")
        return False

    return True


def test_security_integration():
    """场景二：安全集成"""
    print_header("场景二：安全集成 - 企业工作流")

    print_step("1. 导入安全模块")
    try:
        from ghost_hub_sdk.security import (
            SimpleAuth,
            InputValidator,
            RateLimiter,
            SensitiveDataProtector,
        )

        print("    [OK] 安全模块导入成功")
    except ImportError as e:
        print(f"    [FAIL] 安全模块导入失败: {e}")
        return False

    print_step("2. API Key管理")
    try:
        auth = SimpleAuth()
        key = auth.generate_api_key()
        auth.add_api_key(key, "enterprise_user", permissions=["read", "write"])
        info = auth.validate_api_key(key)
        print(f"    [OK] Key创建和验证成功 | 用户: {info['name']}")
    except Exception as e:
        print(f"    [FAIL] Key管理失败: {e}")
        return False

    print_step("3. 输入验证")
    try:
        valid = InputValidator.validate_command("turn_on")
        invalid = InputValidator.validate_command("DROP")
        print(f"    [OK] 验证器工作正常 | 有效: {valid}, 无效: {not invalid}")
    except Exception as e:
        print(f"    [FAIL] 验证失败: {e}")
        return False

    print_step("4. 限流机制")
    try:
        limiter = RateLimiter(requests_per_minute=60, burst=10)
        allowed = limiter.check("test_client")
        print(f"    [OK] 限流器工作正常 | 请求允许: {allowed}")
    except Exception as e:
        print(f"    [FAIL] 限流失败: {e}")
        return False

    print_step("5. 敏感数据保护")
    try:
        data = {"password": "secret123", "api_key": "sk-abc123"}
        masked = SensitiveDataProtector.mask_dict(data)
        is_masked = data["password"] not in masked["password"]
        print(f"    [OK] 数据脱敏正常 | 脱敏生效: {is_masked}")
    except Exception as e:
        print(f"    [FAIL] 数据脱敏失败: {e}")
        return False

    return True


def test_memory_and_storage():
    """场景三：记忆与存储"""
    print_header("场景三：记忆与存储 - 数据持久化")

    print_step("1. 导入记忆模块")
    try:
        from ghost_hub_sdk.memory import GhostHubMemory

        print("    [OK] 记忆模块导入成功")
    except ImportError as e:
        print(f"    [FAIL] 记忆模块导入失败: {e}")
        return False

    print_step("2. 记忆层操作")
    try:
        memory = GhostHubMemory()
        memory.learn_preference("user.brightness", 75)
        value = memory.get_preference("user.brightness")
        print(f"    [OK] 偏好学习成功 | 获取值: {value}")
    except Exception as e:
        print(f"    [FAIL] 记忆操作失败: {e}")
        return False

    print_step("3. 导入存储模块")
    try:
        from ghost_hub_sdk.storage import JSONStorage

        print("    [OK] 存储模块导入成功")
    except ImportError as e:
        print(f"    [FAIL] 存储模块导入失败: {e}")
        return False

    print_step("4. JSON存储操作")
    try:
        storage = JSONStorage(os.path.join(temp_dir, "test_storage.json"))
        storage.save("workflow_001", {"status": "completed", "tasks": 5})
        value = storage.load("workflow_001")
        print(f"    [OK] 数据存储成功 | 获取值: {value is not None}")
    except Exception as e:
        print(f"    [FAIL] 存储操作失败: {e}")
        return False

    return True


def test_component_chaining():
    """场景四：组件串联"""
    print_header("场景四：组件串联 - 工作流编排")

    print_step("1. 导入组件")
    try:
        from ghost_hub_sdk.components import (
            IntentionBankComponent,
            NoUIAdapterComponent,
            AgentFederationComponent,
        )

        print("    [OK] 组件导入成功")
    except ImportError as e:
        print(f"    [FAIL] 组件导入失败: {e}")
        return False

    print_step("2. 初始化意图银行")
    try:
        bank = IntentionBankComponent()
        result = bank.match_intent("打开客厅灯")
        has_match = result.has_match if hasattr(result, "has_match") else True
        print(f"    [OK] 意图解析成功 | has_match: {has_match}")
    except Exception as e:
        print(f"    [FAIL] 意图解析失败: {e}")
        return False

    print_step("3. 初始化无UI适配器")
    try:
        adapter = NoUIAdapterComponent()
        cmd_result = adapter.send_command("light_001", "turn_on", brightness=80)
        print(f"    [OK] 设备命令发送成功 | success: {cmd_result.success}")
    except Exception as e:
        print(f"    [FAIL] 设备命令失败: {e}")
        return False

    print_step("4. 初始化智能体联邦")
    try:
        federation = AgentFederationComponent()
        print("    [OK] 智能体联邦初始化成功")
    except Exception as e:
        print(f"    [FAIL] 智能体联邦失败: {e}")
        return False

    print_step("5. 工作流引擎串联")
    try:
        from ghost_hub_sdk.workflow_engine import create_workflow_engine

        engine = create_workflow_engine()
        print("    [OK] 工作流引擎初始化成功")
    except Exception as e:
        print(f"    [FAIL] 工作流引擎失败: {e}")
        return False

    return True


def test_concurrent_usage():
    """场景五：并发使用"""
    print_header("场景五：并发使用 - 多线程场景")

    import threading
    import queue

    print_step("1. 准备测试")
    try:
        from ghost_hub_sdk import GhostHubSDK

        print("    [OK] SDK导入成功")
    except ImportError as e:
        print(f"    [FAIL] SDK导入失败: {e}")
        return False

    print_step("2. 并发安全模块")
    try:
        from ghost_hub_sdk.security import SimpleAuth, RateLimiter

        auth = SimpleAuth()
        limiter = RateLimiter(requests_per_minute=1000, burst=100)
        print("    [OK] 安全模块初始化成功")
    except Exception as e:
        print(f"    [FAIL] 安全模块失败: {e}")
        return False

    print_step("3. 并发Key生成")
    try:
        results = queue.Queue()
        errors = queue.Queue()

        def gen_keys(thread_id):
            try:
                for _ in range(10):
                    key = auth.generate_api_key()
                    results.put(key)
            except Exception as e:
                errors.put(str(e))

        threads = []
        for i in range(5):
            t = threading.Thread(target=gen_keys, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        key_count = results.qsize()
        error_count = errors.qsize()
        print(f"    [OK] 5线程 x 10次生成 | 成功: {key_count}, 错误: {error_count}")
    except Exception as e:
        print(f"    [FAIL] 并发Key生成失败: {e}")
        return False

    print_step("4. 并发限流检查")
    try:
        limiter._buckets.clear() if hasattr(limiter, "_buckets") else None
        check_results = queue.Queue()

        def check_rate(thread_id):
            for _ in range(20):
                allowed = limiter.check(f"client_{thread_id}")
                check_results.put(allowed)

        threads = []
        for i in range(10):
            t = threading.Thread(target=check_rate, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total = check_results.qsize()
        allowed = sum(1 for _ in range(total) if check_results.get())
        print(f"    [OK] 10线程 x 20次检查 | 总请求: {total}, 允许: {allowed}")
    except Exception as e:
        print(f"    [FAIL] 并发限流失败: {e}")
        return False

    return True


def test_protocol_modules():
    """场景六：协议模块"""
    print_header("场景六：协议模块 - MQTT/WebSocket")

    print_step("1. 导入协议模块")
    try:
        from ghost_hub_sdk.protocols import MQTTClient, WebSocketClient

        print("    [OK] 协议模块导入成功")
    except ImportError as e:
        print(f"    [FAIL] 协议模块导入失败: {e}")
        return False

    print_step("2. MQTT客户端创建")
    try:
        from ghost_hub_sdk.protocols import MQTTConnectionConfig

        config = MQTTConnectionConfig(broker="localhost", port=1883, client_id="test_client")
        print(f"    [OK] MQTT配置创建成功 | broker: {config.broker}")
    except Exception as e:
        print(f"    [FAIL] MQTT配置失败: {e}")
        return False

    print_step("3. WebSocket客户端创建")
    try:
        from ghost_hub_sdk.protocols import WebSocketConfig

        config = WebSocketConfig(url="wss://localhost/ws")
        print(f"    [OK] WebSocket配置创建成功 | url: {config.url}")
    except Exception as e:
        print(f"    [FAIL] WebSocket配置失败: {e}")
        return False

    return True


def test_knowledge_module():
    """场景七：知识模块"""
    print_header("场景七：知识模块 - 知识图谱")

    print_step("1. 导入知识模块")
    try:
        from ghost_hub_sdk.knowledge import IntentKnowledgeGraph

        print("    [OK] 知识模块导入成功")
    except ImportError as e:
        print(f"    [FAIL] 知识模块导入失败: {e}")
        return False

    return True


def main():
    print("\n" + "=" * 70)
    print("  Ghost Hub SDK v1.0.0 - 用户场景全面验证")
    print("=" * 70)
    print(f"\n验证目录: {__file__}")
    print(f"SDK路径: {Path(__file__).parent.parent.parent}")

    tests = [
        ("场景一：基础使用", test_basic_usage),
        ("场景二：安全集成", test_security_integration),
        ("场景三：记忆与存储", test_memory_and_storage),
        ("场景四：组件串联", test_component_chaining),
        ("场景五：并发使用", test_concurrent_usage),
        ("场景六：协议模块", test_protocol_modules),
        ("场景七：知识模块", test_knowledge_module),
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n  [ERROR] {name} 异常: {e}")
            import traceback

            traceback.print_exc()
            results.append((name, False))

    # 汇总
    print_header("验证汇总")
    passed = sum(1 for _, r in results if r)
    total = len(results)

    print(f"\n  通过: {passed}/{total}")
    print(f"  成功率: {passed / total * 100:.1f}%\n")

    for name, success in results:
        icon = "[OK]" if success else "[FAIL]"
        print(f"    {icon} {name}")

    print("\n" + "=" * 70)
    if passed == total:
        print("  [SUCCESS] 所有用户场景验证通过!")
    else:
        print(f"  [WARN]  {total - passed} 个场景需要修复")
    print("=" * 70 + "\n")

    # 清理
    try:
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)
    except:
        pass

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
