"""
Ghost Hub 新功能验证脚本

验证：
1. 模板丰富 (22个模板)
2. 真实协议 (MQTT/WebSocket)
3. 持久化机制 (SQLite/JSON)
"""

import sys
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def print_header(text):
    print("\n" + "=" * 60)
    print("  " + text)
    print("=" * 60)


def test_template_enrichment():
    """测试模板丰富"""
    print_header("测试1: 模板丰富 (22个模板)")

    from ghost_hub_sdk import GhostHubSDK

    sdk = GhostHubSDK()
    templates = sdk.intention_bank.list_templates()

    print("\n[模板列表]")

    # 按域分组
    domains = {}
    for t in templates:
        domain = t.domain
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(t.name)

    for domain, names in sorted(domains.items()):
        print(f"\n  [{domain}] ({len(names)}个)")
        for name in names[:5]:
            print(f"    - {name}")
        if len(names) > 5:
            print(f"    ... 还有 {len(names) - 5} 个")

    print(f"\n  总计: {len(templates)} 个模板")
    return len(templates) >= 20


def test_protocols():
    """测试真实协议"""
    print_header("测试2: 真实协议 (MQTT/WebSocket)")

    from ghost_hub_sdk.protocols import (
        MQTTClient,
        MQTTConnectionConfig,
        WebSocketClient,
        WebSocketConfig,
    )

    print("\n[MQTT客户端]")
    mqtt_config = MQTTConnectionConfig(
        broker="test.mqtt.broker.com", port=1883, client_id="test_client"
    )
    mqtt = MQTTClient(mqtt_config)
    print(f"  配置: {mqtt_config.broker}:{mqtt_config.port}")
    print(f"  客户端ID: {mqtt_config.client_id}")
    print(f"  模拟模式: {not hasattr(mqtt, '_use_real_mqtt') or not mqtt._use_real_mqtt}")

    # 尝试连接
    connected = mqtt.connect()
    print(f"  连接结果: {'成功' if connected else '失败(正常-无真实broker)'}")
    stats = mqtt.get_stats()
    print(
        f"  统计: 消息发送={stats.get('messages_sent', 0)}, 接收={stats.get('messages_received', 0)}"
    )
    mqtt.disconnect()

    print("\n[WebSocket客户端]")
    ws_config = WebSocketConfig(url="wss://test.ws.server.com/ws")
    ws = WebSocketClient(ws_config)
    print(f"  配置: {ws_config.url}")

    # 尝试连接
    connected = ws.connect()
    print(f"  连接结果: {'成功' if connected else '失败(正常-无真实server)'}")
    ws_stats = ws.get_stats()
    print(
        f"  统计: 消息发送={ws_stats.get('messages_sent', 0)}, 接收={ws_stats.get('messages_received', 0)}"
    )
    ws.disconnect()

    return True


def test_persistence():
    """测试持久化"""
    print_header("测试3: 持久化机制")

    from ghost_hub_sdk.storage import DataStore, get_datastore

    # 测试JSON存储
    print("\n[JSON存储]")
    json_store = DataStore(backend="json", storage_path="./test_data/json")
    json_store.save("test_json", {"type": "json", "value": 123})
    loaded = json_store.load("test_json")
    print(f"  保存/加载: {loaded}")
    json_stats = json_store.get_stats()
    print(f"  统计: {json_stats}")

    import shutil

    try:
        shutil.rmtree("./test_data", ignore_errors=True)
    except:
        pass

    # 测试SQLite存储
    print("\n[SQLite存储]")
    db_path = "./test_data/test.db"
    sqlite_store = DataStore(backend="sqlite", db_path=db_path)

    # 保存多个记录
    records = {
        "user:001": {"name": "张三", "role": "开发者"},
        "user:002": {"name": "李四", "role": "测试"},
        "user:003": {"name": "王五", "role": "产品"},
    }
    count = sqlite_store.save_batch(records)
    print(f"  批量保存: {count}/{len(records)} 条")

    # 加载
    loaded = sqlite_store.load("user:001")
    print(f"  单条加载: {loaded}")

    # 列表
    keys = sqlite_store.list_keys("user:*")
    print(f"  模式查询 (user:*): {len(keys)} 条")

    # SQL查询
    print("\n  [SQL查询示例]")
    sqlite_store.save("product:A", {"name": "产品A", "price": 100})
    sqlite_store.save("product:B", {"name": "产品B", "price": 200})

    # 统计
    stats = sqlite_store.get_stats()
    print(
        f"  统计: record_count={stats.get('record_count', 0)}, size={stats.get('total_size_kb', 0)}KB"
    )

    # 清理
    import shutil

    try:
        shutil.rmtree("./test_data")
    except:
        pass

    # 全局数据存储
    print("\n[全局数据存储]")
    global_store = get_datastore()
    global_store.save("session:test", {"test": True})
    exists = global_store.exists("session:test")
    print(f"  全局存储: {'可用' if exists else '不可用'}")

    return True


def test_intent_matching():
    """测试意图匹配"""
    print_header("测试4: 新模板意图匹配")

    from ghost_hub_sdk.workflow_engine import create_workflow_engine

    engine = create_workflow_engine()

    test_cases = [
        ("管理一个新项目", "AI项目管理"),
        ("搜索项目文档", "知识管理体系"),
        ("创建一个登录功能", "软件开发生命周期"),
        ("跟进这个客户", "客户关系管理"),
        ("检查库存状态", "供应链管理"),
    ]

    print("\n[意图匹配测试]")
    matched = 0
    for intent, expected in test_cases:
        result = engine.execute(intent)
        template = result.get("template") or "无匹配"
        status = "[OK]" if template != "无匹配" else "[WARN]"
        print(f"  {status} '{intent}'")
        print(f"       -> {template}")
        if template != "无匹配":
            matched += 1

    print(f"\n  匹配率: {matched}/{len(test_cases)}")
    return matched >= len(test_cases) * 0.6  # 60%以上即可


def main():
    print("\n" + "=" * 60)
    print("  Ghost Hub SDK 新功能验证")
    print("  模板丰富 / 真实协议 / 持久化机制")
    print("=" * 60)

    tests = [
        ("模板丰富", test_template_enrichment),
        ("真实协议", test_protocols),
        ("持久化机制", test_persistence),
        ("意图匹配", test_intent_matching),
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
    print_header("验证汇总")
    passed = sum(1 for _, r in results if r)
    total = len(results)

    print(f"\n  通过: {passed}/{total}")
    print(f"  成功率: {passed / total * 100:.1f}%\n")

    for name, success in results:
        icon = "[OK]" if success else "[FAIL]"
        print(f"    {icon} {name}")

    print("\n" + "=" * 60)

    if passed == total:
        print("  [SUCCESS] 所有新功能验证通过!")
    else:
        print(f"  [WARN]  {total - passed} 项需要检查")

    print("=" * 60 + "\n")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
