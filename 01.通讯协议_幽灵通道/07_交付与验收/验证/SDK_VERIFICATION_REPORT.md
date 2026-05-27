# SDK 可用性驗證報告

> 驗證日期: 2026-05-23
> 驗證方式: pip install + pytest

## 結果總覽

| SDK | 路徑 | pip install | 測試 | 狀態 |
|-----|------|-------------|------|------|
| **企業 SDK** | `GhostHub_SDK` | ✅ | ❌ 0/3 (ImportError + 缺少 fastapi 依賴) | ⚠️ 需修復 |
| **開源社群版** | `ghost_channel 開源包` | ✅ | ✅ 18/18 pass | ✅ |
| **輕量對接 SDK** | `ghost-channel-sdk` (Python) | ✅ | ✅ 68/68 pass | ✅ |

## 問題詳情

### 企業 SDK (GhostHub_SDK)

**症狀**: `pip install` 成功，但 `pytest` 報 `ModuleNotFoundError: No module named 'ghost_hub_sdk'`

**根因**: `pyproject.toml` 中 `[tool.setuptools]` 配置有誤：
```toml
packages = ["components", "protocols", "api", "demos"]
package-dir = {"ghost_hub_sdk" = "."}
```
`packages` 未包含根套件 `ghost_hub_sdk`，僅列出子套件。需修正為：
```toml
packages = ["ghost_hub_sdk", "ghost_hub_sdk.components", ...]
```

**次要問題**: `dependencies = []` 為空，但實際使用 `fastapi`、`uvicorn` 等外部套件。

**建議**: 修復 `pyproject.toml` 打包配置，補齊外部依賴清單。

### 另兩套 SDK

- **開源社群版**: 18 項測試全數通過，可直接 `pip install` 使用
- **輕量對接 SDK**: 68 項測試全數通過，Python + TypeScript 雙語支援
