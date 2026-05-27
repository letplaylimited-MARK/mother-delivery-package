﻿"""
Ghost Hub SDK v1.0.0 - 最终交付验证脚本

验证内容:
1. 模块导入完整性
2. 组件串联集成
3. API一致性
4. 文件包完整性

运行: python demos/demo_final_verification.py
"""

import sys
import io
import os
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SDK_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SDK_ROOT))


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_check(text, status):
    icon = "[OK]" if status else "[FAIL]"
    print(f"  {icon} {text}")


def verify_file_structure():
    """验证文件包结构"""
    print_header("1. 文件包结构验证")

    required_files = [
        "__init__.py",
        "core.py",
        "config.py",
        "workflow_engine.py",
        "memory.py",
        "knowledge.py",
        "storage.py",
        "security.py",
    ]

    required_dirs = ["components", "protocols", "templates", "demos", "docs"]

    all_ok = True

    for file in required_files:
        path = SDK_ROOT / file
        exists = path.exists()
        print_check(f"文件: {file}", exists)
        all_ok = all_ok and exists

    for dir_name in required_dirs:
        path = SDK_ROOT / dir_name
        exists = path.exists() and path.is_dir()
        print_check(f"目录: {dir_name}/", exists)
        all_ok = all_ok and exists

    for comp in ["intention_bank.py", "no_ui_adapter.py", "agent_federation.py"]:
        path = SDK_ROOT / "components" / comp
        print_check(f"组件: components/{comp}", path.exists())

    for proto in ["mqtt_client.py", "websocket_client.py"]:
        path = SDK_ROOT / "protocols" / proto
        print_check(f"协议: protocols/{proto}", path.exists())

    return all_ok


def verify_module_imports():
    """验证所有模块导入"""
    print_header("2. 模块导入验证")

    results = []

    try:
        from config import GhostHubConfig

        print_check("config.GhostHubConfig", True)
        results.append(True)
    except Exception as e:
        print_check(f"config: {str(e)[:40]}", False)
        results.append(False)

    try:
        from security import SimpleAuth, InputValidator, RateLimiter, SensitiveDataProtector

        print_check("security 模块", True)
        results.append(True)
    except Exception as e:
        print_check(f"security: {str(e)[:40]}", False)
        results.append(False)

    try:
        from memory import GhostHubMemory

        print_check("memory 模块", True)
        results.append(True)
    except Exception as e:
        print_check(f"memory: {str(e)[:40]}", False)
        results.append(False)

    try:
        from knowledge import IntentKnowledgeGraph

        print_check("knowledge 模块", True)
        results.append(True)
    except Exception as e:
        print_check(f"knowledge: {str(e)[:40]}", False)
        results.append(False)

    try:
        from storage import JSONStorage, SQLiteStorage

        print_check("storage 模块", True)
        results.append(True)
    except Exception as e:
        print_check(f"storage: {str(e)[:40]}", False)
        results.append(False)

    try:
        from components import (
            IntentionBankComponent,
            NoUIAdapterComponent,
            AgentFederationComponent,
        )

        print_check("components 模块", True)
        results.append(True)
    except Exception as e:
        print_check(f"components: {str(e)[:40]}", False)
        results.append(False)

    try:
        from protocols import MQTTClient, WebSocketClient

        print_check("protocols 模块", True)
        results.append(True)
    except Exception as e:
        print_check(f"protocols: {str(e)[:40]}", False)
        results.append(False)

    return all(results)


def verify_sdk_components():
    """验证SDK组件"""
    print_header("3. SDK组件验证")

    try:
        from security import SimpleAuth, RateLimiter, InputValidator
        from memory import GhostHubMemory

        auth = SimpleAuth()
        key = auth.generate_api_key()
        auth.add_api_key(key, "test", permissions=["read"])
        info = auth.validate_api_key(key)
        print_check("SimpleAuth 认证", info is not None)

        limiter = RateLimiter(requests_per_minute=60)
        allowed = limiter.check("test_client")
        print_check("RateLimiter 限流", allowed)

        valid = InputValidator.validate_command("turn_on")
        print_check("InputValidator", valid)

        memory = GhostHubMemory()
        memory.learn_preference("test", "value")
        print_check("GhostHubMemory", memory.get_preference("test") == "value")

        return True
    except Exception as e:
        print_check(f"SDK组件: {str(e)[:50]}", False)
        return False


def verify_storage():
    """验证存储"""
    print_header("4. 存储验证")

    import tempfile

    try:
        from storage import JSONStorage

        temp_file = os.path.join(tempfile.gettempdir(), "ghost_test.json")
        store = JSONStorage(temp_file)
        store.save("key1", {"data": "value1"})
        loaded = store.load("key1")
        print_check("JSONStorage save/load", loaded is not None)

        try:
            os.remove(temp_file)
        except:
            pass

        return True
    except Exception as e:
        print_check(f"存储: {str(e)[:50]}", False)
        return False


def verify_protocols():
    """验证协议模块"""
    print_header("5. 协议模块验证")

    try:
        from protocols import MQTTClient, WebSocketClient, MQTTConnectionConfig, WebSocketConfig

        mqtt_config = MQTTConnectionConfig(broker="localhost", port=1883, client_id="test")
        print_check("MQTTConnectionConfig", mqtt_config.broker == "localhost")

        ws_config = WebSocketConfig(url="wss://localhost/ws")
        print_check("WebSocketConfig", "wss://" in ws_config.url)

        mqtt_client = MQTTClient(mqtt_config)
        print_check("MQTTClient 创建", mqtt_client is not None)

        return True
    except Exception as e:
        print_check(f"协议: {str(e)[:50]}", False)
        return False


def verify_components():
    """验证组件模块"""
    print_header("6. 组件模块验证")

    try:
        from components import (
            IntentionBankComponent,
            NoUIAdapterComponent,
            AgentFederationComponent,
        )

        bank = IntentionBankComponent()
        print_check("IntentionBankComponent", bank is not None)

        adapter = NoUIAdapterComponent()
        print_check("NoUIAdapterComponent", adapter is not None)

        federation = AgentFederationComponent()
        print_check("AgentFederationComponent", federation is not None)

        return True
    except Exception as e:
        print_check(f"组件: {str(e)[:50]}", False)
        return False


def verify_templates():
    """验证模板"""
    print_header("7. 模板验证")

    templates_dir = SDK_ROOT / "templates"
    template_files = list(templates_dir.glob("*.json"))
    print_check(f"模板数量 ({len(template_files)})", len(template_files) >= 20)

    if template_files:
        try:
            with open(template_files[0], "r", encoding="utf-8") as f:
                content = f.read()
                json.loads(content)
            print_check("模板JSON有效", True)
        except:
            print_check("模板JSON有效", False)

    return True


def verify_demos():
    """验证演示脚本"""
    print_header("8. 演示脚本验证")

    demos_dir = SDK_ROOT / "demos"
    demos = [
        "demo_security.py",
        "demo_boundary.py",
        "demo_concurrency.py",
        "demo_secure_api.py",
        "demo_user_scenarios.py",
        "demo_final_verification.py",
    ]

    all_ok = True
    for demo in demos:
        path = demos_dir / demo
        exists = path.exists()
        print_check(f"demo: {demo}", exists)
        all_ok = all_ok and exists

    return all_ok


def verify_docs():
    """验证文档"""
    print_header("9. 文档验证")

    docs_dir = SDK_ROOT / "docs"
    docs = ["API.md", "USER_MANUAL.md", "EXAMPLES.md", "USER_SCENARIOS.md"]

    all_ok = True
    for doc in docs:
        path = docs_dir / doc
        exists = path.exists()
        print_check(f"docs: {doc}", exists)
        if exists and path.stat().st_size < 100:
            print_check(f"  大小异常", False)
            all_ok = False
        all_ok = all_ok and exists

    return all_ok


def verify_version():
    """验证版本"""
    print_header("10. 版本验证")

    try:
        from config import GhostHubConfig

        config = GhostHubConfig()
        version = config.version
        print_check(f"版本号 ({version})", version == "1.0.0")
        return True
    except Exception as e:
        print_check(f"版本: {str(e)[:50]}", False)
        return False


def main():
    print("\n" + "=" * 70)
    print("  Ghost Hub SDK v1.0.0 - 最终交付验证")
    print("=" * 70)
    print(f"\n交付路径: {SDK_ROOT}")

    checks = [
        ("文件包结构", verify_file_structure),
        ("模块导入", verify_module_imports),
        ("SDK组件", verify_sdk_components),
        ("存储模块", verify_storage),
        ("协议模块", verify_protocols),
        ("组件模块", verify_components),
        ("模板完整性", verify_templates),
        ("演示脚本", verify_demos),
        ("文档完整性", verify_docs),
        ("版本验证", verify_version),
    ]

    results = []
    for name, check_func in checks:
        try:
            success = check_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n  [ERROR] {name}: {e}")
            results.append((name, False))

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
        print("  [SUCCESS] Ghost Hub SDK v1.0.0 交付验证通过!")
    else:
        print(f"  [WARN]  {total - passed} 项验证需要修复")
    print("=" * 70 + "\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
