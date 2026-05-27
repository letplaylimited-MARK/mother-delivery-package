# 使用場景

> **版本**: v6.3 | **更新**: 2026-05-24 | **測試**: 63/63 ALL PASS ✅ | **湧現**: R22=0.8664

## 場景一：湧現理論驗證（研究用途）

**目標**: 觀察多角色 AI 協作系統中知識共鳴如何驅動湧現行為。

**適用對象**: 研究人員、AI 理論學者、博士生

**使用方式**:
```bash
python "02-代码编写/main.py"
# 22 輪後觀測 R 值從 0.74 增長至 0.86，湧現發生
```

**觀測指標**:
- R 值成長曲線（每輪記錄於 `rounds_log`）
- 湧現發生的輪次（預設 R22）
- 四分量（K_sim, C_comp, I_freq, E_div）變化趨勢

**論文對照**: 對應論文第 2 章數學理論基礎，驗證 F1-F22 公式系統的湧現行為。

---

## 場景二：多角色協作協議開發（工程用途）

**目標**: 基於 QCM 協作協議設計與測試多角色 AI 協作系統。

**適用對象**: 系統架構師、AI 工程師

**核心模組**:
- `qcm/collaboration/` — 5 階段會議協議 + 投票機制 + 死鎖檢測
- `qcm/roles/` — 角色身份系統 + 加權共識 + 安全否決權
- `qcm/summoning/` — 角色召喚與技能匹配

**使用方式**:
```python
from qcm.collaboration import MeetingOrchestrator, detect_deadlock
from qcm.roles import weighted_consensus

meeting = MeetingOrchestrator()
meeting.add_message("researcher", "分析需求文檔")
state = meeting.get_state()
# state.current_phase -> 1, state.is_deadlocked -> False
```

**輸出結果**: 協作會議記錄、決策審計日誌、死鎖檢測報告。

---

## 場景三：飛輪優化與穩定性分析（進階用途）

**目標**: 分析系統動態行為，調優學習率、收斂條件與能量函數。

**適用對象**: 機器學習工程師、控制理論研究人員

**核心模組**:
- `qcm/flywheel/` — 外迴圈（使用者能力）+ 內迴圈（系統狀態）+ Lyapunov 穩定性
- `qcm/sandbox/` — 3 層沙盤隔離 + SRS 成功率評分

**可調參數**:
```python
from qcm.flywheel import adaptive_learning_rate, has_converged

lr = adaptive_learning_rate(t=10, init_lr=0.1, gamma=0.01)
converged = has_converged(recent_improvements, threshold=0.01)
```

**輸出結果**: 學習率變化曲線、收斂判斷、Lyapunov 能量函數軌跡、頻譜半徑。

---

## 場景四：全管線整合部署（生產用途）

**目標**: 將 QCM 管線整合到現有 AI 系統中，作為協作決策引擎。

**適用對象**: 後端開發者、DevOps 工程師

**使用方式**:
```bash
# API 服務模式
python qcm/main.py --mode service --port 8080

# 或單輪執行
python qcm/main.py --mode production --rounds 5
```

**API 端點**:
| 端點 | 方法 | 說明 |
|------|------|------|
| `/health` | GET | 系統健康檢查 |
| `/status` | GET | 系統狀態查詢 |
| `/simulate` | POST | 執行多輪模擬（含回合數/角色/插件參數） |
| `/step` | POST | 執行一輪計算 |
| `/reset` | POST | 重置管線狀態 |
| `/history` | GET | 查看歷史紀錄 |
| `/capabilities` | POST | 啟用/停用加密或自癒能力 |

**配置整合**:
```python
from qcm import QCMConfig
config = QCMConfig()
config.set("modules", True)           # 啟用論文模組
config.set("capabilities.crypto", True)  # 啟用加密
```

---

## 場景五：教育演示（教學用途）

**目標**: 以視覺化方式展示「湧現」這一複雜系統概念。

**適用對象**: 教授、學生、AI 科普

**執行**:
```bash
python "02-代码编写/main.py"
```

**觀察要點**:
1. 前 10 輪：R 值緩慢增長（角色間建立信任）
2. 第 10-18 輪：R 值加速上升（知識共鳴形成）
3. 第 19-22 輪：R 值突破 0.85（湧現發生）

**湧現等級對照**:

| R 值範圍 | 等級 | 意義 |
|----------|------|------|
| < 0.3 | 無協同 | 角色獨立工作，無互動 |
| 0.3-0.5 | 初步協同 | 簡單資訊交換 |
| 0.5-0.7 | 中度協同 | 任務層級協調 |
| 0.7-0.85 | 深度協同 | 知識層級共鳴 |
| > 0.85 | **湧現** | 自主智慧行為 |

---

## 場景六：論文模組獨立測試（開發用途）

**目標**: 針對論文 §3.2/§4/§7/§8/§9 的獨立實現進行驗證與擴展。

**適用對象**: 論文作者、審稿人、貢獻者

| 論文章節 | 測試 | 測試數量 | 覆蓋範圍 |
|----------|------|----------|----------|
| §3.2 角色 | `test_roles.py` | 6 | 角色註冊、共識投票、安全否決 |
| §4 協作 | `test_collaboration.py` | 7 | 會議階段、投票、死鎖、審計 |
| §7 沙盒 | `test_sandbox.py` | 8 | 隔離層、SRS、CBP 調度 |
| §8 飛輪 | `test_flywheel.py` | 11 | 狀態更新、收斂、能量、Lyapunov |
| §9 召喚 | `test_summoning.py` | 6 | TF-IDF、技能匹配、距離計算 |
| **合計** | **63/63 ALL PASS** | **38** | **test_qcm_all.py 25 + pytest 38** |

```bash
pytest "02-代码编写/test_roles.py" -v
```
