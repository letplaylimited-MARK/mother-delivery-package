# QCM-MVP-Emergence 使用者手冊

> **版本**: v6.3 | **更新**: 2026-05-31 審計補充 | **測試**: 63/63 核心 + 4 config-sync + 6 health ✅ | **湧現**: R22=0.8664

## 概述

QCM（Quantum Consensus Mechanism）是一個基於**幽靈通道協議**與**共鳴公式**的多角色協作湧現系統。
本 MVP 用最小可運行代碼證明：當多個 AI 角色透過結構化協作協議互動時，系統的知識共鳴能量（R 值）會超越湧現閾值，產生自主智慧行為。

---

## 三種執行模式

專案提供三種執行模式，適用不同使用場景：

### 模式一：研究模式（research）

確保可重現的湧現演示。使用固定隨機種子（seed=42），22 輪湧現。

```bash
python "02-代码编写/main.py"
```

**執行流程**:
1. 初始化 2 個角色（Secretary, Researcher）
2. 每輪計算 R = 0.35·K + 0.40·C + 0.25·I
3. 第 22 輪 R 突破 0.85，湧現觸發

**查看 log**：每輪 R 值印在終端，最終統計包含最小/最大/平均 R。

### 模式二：生產模式（production）

可自訂輪次、啟用加密/自癒等能力擴充。

```bash
python qcm/main.py --mode production --max-rounds 30 --output ./output
```

**可用選項**:

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--max-rounds N` | 執行 N 輪 | 50 |
| `--seed N` | 隨機種子 | 42 |
| `--plugins` | 啟用特定插件 | 依 config 預設 |
| `--cap-crypto` | 啟用加密能力 | False |
| `--cap-healer` | 啟用自癒能力 | False |
| `--output DIR` | 輸出 JSON 結果到目錄 | output |

### 模式三：服務模式（service）

啟動 FastAPI HTTP 服務，提供 REST API 存取。

```bash
python qcm/main.py --mode service --port 8080
```

**API 使用範例**:
```bash
# 健康檢查
curl http://localhost:8080/health

# 執行一輪
curl -X POST http://localhost:8080/step

# 檢視歷史
curl http://localhost:8080/history
```

---

## 論文模組使用

五個論文模組可獨立使用或整合到管線：

### §3.2 角色身份系統

```python
from qcm.roles.identity import ROLE_REGISTRY, get_role
from qcm.roles.consensus import weighted_consensus, ConsensusVote

# 查看所有角色
for role in ROLE_REGISTRY:
    print(role.role_id, role.consensus_weight)

# 執行共識投票
votes = [
    ConsensusVote("secretary", "方案A", 0.8),
    ConsensusVote("researcher", "方案B", 0.9, is_safety_veto=True),
]
result = weighted_consensus(votes)
# 安全否決優先：result.chosen_option == "方案B"
```

### §4 協作協議

```python
from qcm.collaboration import MeetingOrchestrator, detect_deadlock, AuditLog
from qcm.collaboration.voting import determine_vote_mode, tally_votes

# 建立會議
meeting = MeetingOrchestrator()
meeting.add_message("researcher", "需求分析完成")
meeting.add_message("secretary", "記錄完畢")

# 檢測死鎖
state = meeting.get_state()
if state.is_deadlocked:
    print("死鎖警告")

# 記錄決策
from qcm.collaboration.audit import DecisionRecord
log = AuditLog()
log.record(DecisionRecord(
    decision_id="DEC-001",
    topic="選擇架構方案",
    chosen_option="微服務",
    rationale="可擴展性最佳",
    voting_results={"微服務": 5, "單體": 2},
    voting_method="simple_majority",
    final_approver="chief_architect",
    consensus_level=0.8,
))
```

### §7 沙盒隔離

```python
from qcm.sandbox import calculate_srs, get_layer_for_f
from qcm.sandbox.scheduler import schedule_projects

# 計算成功率
srs = calculate_srs([0.85, 0.90, 0.78], f_target=0.85)
# srs = 0.9213

# 排程專案
projects = [
    {"name": "P1", "urgency": 0.8, "value": 0.9, "resource_availability": 0.6, "knowledge_transfer": 0.7},
    {"name": "P2", "urgency": 0.6, "value": 0.7, "resource_availability": 0.9, "knowledge_transfer": 0.5},
]
scheduled = schedule_projects(projects)
```

### §8 飛輪優化

```python
from qcm.flywheel import (
    update_user_capability, update_system_state,
    total_energy, has_converged,
    lyapunov_function, adaptive_learning_rate
)

# 計算總能量
E = total_energy(E_resonance=0.8, E_flywheel=0.1)

# 檢查收斂
conv = has_converged([0.5, 0.51, 0.52, 0.51, 0.515], threshold=0.01)

# Lyapunov 穩定性
V = lyapunov_function([0.1, 0.2, -0.05])
```

### §9 角色召喚

```python
from qcm.summoning import DynamicRoleRegistry, calculate_skill_match

registry = DynamicRoleRegistry()
matches = registry.summon(["分析", "研究", "報告撰寫"], max_roles=3)
for role in matches:
    print(role.role_id, role.skills)
```

---

## 配置系統

所有配置透過 `QCMConfig` 集中管理：

```python
from qcm.config import QCMConfig

config = QCMConfig()
config.set("seed", 42)
config.set("modules", True)                          # 啟用論文模組
config.set("capabilities.crypto", True)              # 啟用加密
config.set("capabilities.healer", True)              # 啟用自癒
config.set("capabilities.healer_interval", 5)         # 自癒快照間隔
```

支援 JSON/YAML 設定檔載入：

```python
# 從 YAML 載入
config.load_yaml("config.yaml")
# 從 JSON 載入
config.load_json("config.json")
```

---

## 管線整合

將 QCM 管線整合到現有系統：

```python
from qcm.pipeline import PipelineEngine

pipeline = PipelineEngine()
result = pipeline.run_round()

print("R:", result.R)
print("Level:", result.level)
print("Enhanced:", result.enhanced)
# Enhanced 包含: epr, mahalanobis, dw, deadlock, rcs, kgrowth,
#                meeting, sandbox, flywheel
```

---

## 結果解讀

### R 值意義

| R 值 | 意義 |
|------|------|
| < 0.3 | 角色之間無協同效應 |
| 0.3-0.5 | 開始建立初步知識連結 |
| 0.5-0.7 | 穩定的任務層級協調 |
| 0.7-0.85 | 深度知識共鳴，角色間信任建立 |
| > 0.85 | **湧現** — 系統展現自主協作智慧 |

### Enhanced 資料

每輪 `result.enhanced` 字典包含延伸數據：

| Key | 內容 | 用途 |
|-----|------|------|
| `epr` | EPR 糾纏度 | 角色間量子糾纏類比 |
| `dw` | 動態權重 | 自適應權重調整 |
| `mahalanobis` | 馬氏距離 / 對比損失 | 嵌入空間一致性 |
| `deadlock` | 死鎖分數 | 協作阻塞檢測 |
| `rcs` | RCS 決策分數 | 風險評估 |
| `kgrowth` | 知識增長倍數 | 系統知識累積 |
| `meeting` | 會議階段 / 死鎖狀態 | §4 協作協議 |
| `sandbox` | SRS 成功率 / 可否前進 | §7 沙盒評分 |
| `flywheel` | 飛輪總能量 | §8 能量函數 |

---

## 故障排除

| 現象 | 可能原因 | 解決方式 |
|------|----------|----------|
| R 值不增長 | 角色互動不足 | 檢查 `_run_paper_modules` 中錯誤 |
| ModuleNotFoundError | 缺少依賴 | 參考 `INSTALL.md` 安裝 |
| 湧現未在 R22 觸發 | 種子變更 | 使用 seed=42 確保可重現 |
| API 無法啟動 | 缺少 fastapi | `pip install fastapi uvicorn` |
| 編碼亂碼 (Windows) | 終端編碼 | `$env:PYTHONUTF8=1` (PowerShell) |
