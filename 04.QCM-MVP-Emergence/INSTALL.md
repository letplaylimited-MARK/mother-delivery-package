# QCM-MVP-Emergence 安裝指南

> **版本**: v6.3 | **更新**: 2026-05-24 | **測試**: 63/63 ALL PASS ✅ | **湧現**: R22=0.8664

## 系統需求

| 項目 | 最低要求 | 建議 |
|------|----------|------|
| Python | 3.8+ | **3.10+** |
| 記憶體 | 256 MB | 512 MB |
| 磁碟空間 | 50 MB | 100 MB |

## 安裝步驟

### 1. 確認 Python 版本

```bash
python --version
# 需要 Python 3.8 以上
```

### 2. 安裝核心依賴

```bash
# 最小安裝（僅核心功能）
pip install numpy pyyaml
```

### 3. 選擇性安裝（依需求）

```bash
# 加密能力（Cap-D CryptoEngine）
pip install cryptography

# API 伺服器模式（FastAPI 服務）
pip install fastapi uvicorn pydantic

# 語義嵌入（Cap-A semantic matching）
pip install sentence-transformers

# 開發/測試工具
pip install pytest pytest-cov
```

### 4. 驗證安裝

```bash
# 進入專案目錄
cd QCM-MVP-Emergence

# 測試基本湧現演示
python "02-代码编写/main.py"
# 預期輸出: 22 輪後 R=0.8664，湧現發生

# 運行完整測試套件
python "02-代码编写/test_qcm_all.py"
# 預期: 25 PASS / 0 FAIL / 25 TOTAL

# 執行 5 個論文模組測試（38 項）
pytest "02-代码编写/test_roles.py" "02-代码编写/test_collaboration.py" "02-代码编写/test_sandbox.py" "02-代码编写/test_flywheel.py" "02-代码编写/test_summoning.py" -v
# 預期: 38 passed

# 總計: 63/63 ALL PASS ✅
```

## 快速驗證

一行指令確認核心功能正常：

```bash
python -c "from qcm.pipeline import PipelineEngine, QCMConfig; p=PipelineEngine(); p.run_round(); print('OK, R=%.4f' % p.rounds_log[-1].R)"
# 預期輸出: OK, R=0.74xx
```

## 目錄結構說明

```
QCM-MVP-Emergence/
├── 02-代码编写/      # 獨立腳本（入口 + 22 公式實現 + 測試）
│   └── main.py       # 湧現演示入口
├── qcm/              # Python 命名空間包（10 子包）
│   ├── config.py     # 配置系統
│   ├── pipeline.py   # 22 公式全管線
│   └── main.py       # 三模式入口
└── README.md         # 專案概述
```

## 疑難排解

| 問題 | 原因 | 解決 |
|------|------|------|
| `ModuleNotFoundError: numpy` | 缺少核心依賴 | `pip install numpy` |
| `ModuleNotFoundError: yaml` | 缺少 PyYAML | `pip install pyyaml` |
| `ImportError: qcm.*` | 工作目錄錯誤 | 在 `QCM-MVP-Emergence/` 根目錄執行 |
| R 值卡在 0.5-0.6 | 缺少必要組件 | 確認 `numpy` 已安裝 |
| 編碼錯誤 (GBK) | Windows 終端 | 在 PowerShell 中執行，或設定 `$env:PYTHONUTF8=1` |
