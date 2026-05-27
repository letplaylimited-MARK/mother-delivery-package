"""测试统一SDK"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ghost_hub_sdk import GhostHubSDK, GhostHubConfig

print("测试1: 导入成功")

config = GhostHubConfig()
sdk = GhostHubSDK(config)

print("测试2: SDK初始化成功")

stats = sdk.get_stats()
print(f"测试3: 统计信息: {stats}")

print("所有测试通过!")
