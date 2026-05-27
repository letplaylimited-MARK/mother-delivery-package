# QCM 論文模組補全設計文檔

## 目標

將 QCM 論文定義的 5 大未實現創新模組，按論文規格完整實作至 `qcm/` 包，使 QCM-MVP-Emergence 從「共鳴引擎原型」提升為「論文級框架」。

## 五大模組

| # | 模組 | 論文章節 | 當前狀態 | 新增 .py | 新測試 |
|---|------|---------|---------|---------|-------|
| 1 | 角色身份 | §3.2 | ❌ SimpleRole 無完整身份 | 3 | 3 |
| 2 | 協同協議 | §7 | ⚠️ deadlock plugin 部分 | 4 | 3 |
| 3 | 三層沙盤 | §8 | ❌ stub 回傳模擬值 | 3 | 3 |
| 4 | 雙層飛輪 | §4 | ⚠️ flywheel plugin 基本公式 | 4 | 3 |
| 5 | 動態召喚 | §9 | ⚠️ mdist+router 部分 | 4 | 3 |

## 整體架構

```
qcm/
├── roles/          新增: §3.2 8角色超級身份
│   ├── __init__.py     重導出
│   ├── identity.py     RoleIdentity, ROLE_REGISTRY
│   └── consensus.py    加權共識算法
├── collaboration/  新增: §7 多角色協同協議
│   ├── __init__.py
│   ├── meeting.py      5階段工作坊, 下位發言人預測
│   ├── voting.py       3模式投票
│   ├── deadlock.py     死鎖偵測+突破 (升級現有)
│   └── audit.py        決策審計
├── sandbox/        新增: §8 三層沙盤
│   ├── __init__.py
│   ├── layers.py       3層定義+複雜度微分方程
│   ├── srs.py          SRS評分+置信門控+CBP
│   └── scheduler.py    優先級排程+資源爭用
├── flywheel/       新增: §4 雙層循環飛輪
│   ├── __init__.py
│   ├── outer_loop.py   外環: 用戶能力+ZPD
│   ├── inner_loop.py   內環: 系統進化+收斂
│   ├── energy.py       能量統一框架
│   └── stability.py    Lyapunov+譜半徑+學習率
├── summoning/      新增: §9 動態角色召喚
│   ├── __init__.py
│   ├── features.py     六特徵提取+加權投票
│   ├── matching.py     三階段管線+馬氏距離
│   └── registry.py     動態角色註冊表
├── core/           既有
├── enhanced/       既有
├── evolution/      既有
├── decision/       既有
├── capabilities/   既有
├── __init__.py     既有 (擴充 import)
├── config.py       既有
├── plugin.py       既有
├── pipeline.py     既有 (擴充 _init_modules + run_round)
└── main.py         既有
```

依賴鏈: roles → collaboration → sandbox → flywheel ← summoning

## Module 1: qcm/roles/ — 8 角色超級身份架構

### identity.py

```python
@dataclass
class RoleIdentity:
    role_id: str
    name: str
    core_mission: str
    kpi_name: str
    kpi_threshold: float
    autonomy_level: int     # 1-4
    consistency_score: float
    consensus_weight: float
    prompt_template: str
    embedding: list[float]  # 768d
```

8 角色靜態註冊表 (ROLE_REGISTRY):

| role_id | 權重 | 自主 | KPI | 閾值 | 一致性 |
|---------|------|------|-----|------|--------|
| secretary | 0.20 | L4 | Task_Assignment_Accuracy | 95% | 96% |
| chief_architect | 0.25 | L3 | Design_Consistency_Score | 0.85 | 94% |
| researcher | 0.20 | L3 | Knowledge_Retrieval_Accuracy | 90% | 93% |
| creator | 0.20 | L2 | Content_Quality_Score | 0.80 | 91% |
| analyst | 0.25 | L2 | Insight_Accuracy | 85% | 92% |
| ux_lead | 0.20 | L2 | User_Satisfaction_Score | 4.0/5.0 | 90% |
| risk_auditor | 0.30 | L3 | Threat_Detection_Rate | 99% | 95% |
| ai_companion | 0.20 | L2 | Empathy_Score | 0.85 | 89% |

### consensus.py

加權共識: Risk Auditor 安全決策有最高否決權 (0.30)，Chief Architect 技術決策主導 (0.25)。

論文公式: `score(option) = Σ w_i · vote_i · relevance_i`

### 整合

pipeline.py `_init_roles()` 改為從 `RoleIdentityRegistry` 建立角色。

## Module 2: qcm/collaboration/ — 多角色協同協議

### meeting.py

5 階段工作坊:
| Phase | 時長 | 焦點 | 主要角色 |
|-------|------|------|---------|
| 1: 需求發現 | 15min | 需求澄清 | Secretary, Chief Architect |
| 2: 架構設計 | 20min | 高層設計 | Chief Architect, Researcher |
| 3: 實施規劃 | 25min | 任務分解 | Creator, Analyst, UX Lead |
| 4: 驗證測試 | 20min | 驗收標準 | Risk Auditor, Creator |
| 5: 總結歸檔 | 10min | 決策記錄 | Secretary, AI Companion |

下位發言人預測: `score = 0.20·time + 0.30·content + 0.25·participation + 0.25·phase`

約束: 每次回覆 ≤300 字, 超時 120s。3 輪未達共識觸發升級。

### voting.py

3 模式:
| 模式 | 通過閾值 | 觸發條件 |
|------|---------|---------|
| 簡單多數決 | >50% | 日常操作性決策 |
| 超級多數決 | ≥75% | 架構變更、資源重新分配 |
| 全體共識 | 100% (可1票棄權) | 戰略方向、核心算法變更 |

### deadlock.py (升級現有 plugin)

擴充現有 DeadlockDetector 加入:
- 3 條件: 循環(新穎率<15%×5輪) + 不平衡(基尼>0.7) + 停滯(|斜率|<0.01/分鐘×20min)
- 軟死鎖評分: S_soft(t) = 0.3(1-N_t) + 0.35·G_t' + 0.2·S_t' + 0.15·loop(t)
- 突破模式: 輕微→妥協 / 中度→迷你工作坊 / 嚴重→迴避協議

論文實測: 預警準確率 87%, 誤報率 8%, 提前 12.3 分鐘。

### audit.py

決策記錄 JSON schema (按論文 §7.6):
```json
{
  "decision_id": "DEC-001",
  "topic": "...",
  "options_evaluated": ["A", "B", "C"],
  "chosen_option": "B",
  "rationale": "...",
  "voting_results": {"B": 5, "A": 1, "C": 1},
  "voting_method": "majority",
  "final_approver": "chief_architect",
  "consensus_level": 0.71
}
```

## Module 3: qcm/sandbox/ — 三層沙盤機制

### layers.py

| Layer | 名稱 | f 範圍 | 隔離 | 持續時間 | 記憶體 | 變量 |
|-------|------|--------|------|---------|--------|------|
| L1 | Sandbox | [1,5] | 進程 | <1s | <50MB | 3-5 |
| L2 | War Room | [5,20] | Compose | 1-60s | 200-500MB | 10-20 |
| L3 | Simulation | [20,100+] | K8s | 分-小時 | 1-4GB | 50-100+ |

公式實作:
- `df_k/dt = λ_k·(1 - f_k/f_k_max)·I[success] - μ_k·f_k·I[failure]`
- 當 μ=0: `f_k(t) = f_k_max·(1 - e^(-λ_k·t))`

### srs.py

- SRS: `SRS = 1/T ∫ exp(-(f_k - f_k_target)²/(2σ²)) dt`
- 門控: θ₀=0.85 (L1→L2), θ₁=0.90 (L2→L3)
- CBP: `CBP = 0.4·min(1, (R_limit - R_avg)/R_limit) + 0.3·I[violations=0] + 0.3·log(1+innovation)`

### scheduler.py

優先級排程: `P = 0.35·urgency + 0.30·value + 0.20·resources + 0.15·knowledge_transfer`

資源爭用解決: 基於優先級搶占 / 協商共享 / 替代資源重路由

### RL 獎勵函數 (Sandbox L3):

`R(s,a,s') = w1·Quality + w2·Efficiency + w3·Satisfaction + w4·Knowledge`

收斂準則: 最近 10 循環提升 <1%

## Module 4: qcm/flywheel/ — 雙層循環飛輪

### outer_loop.py

`U(t+1) = U(t) + η_u·(G(t) - U(t))·(1 - e^(-βt))`

難度自適應:
- 準確率>0.9 且速度>0.8 → 升級
- 準確率<0.7 → 降級
- 每週改進率>0.1 → 加速

### inner_loop.py

`S(t+1) = S(t) + η_s·∇F(S(t))·e^(-γt)`

優化循環: 資料收集 → 性能分析 → 識別改進 → 生成假設 → A/B測試 → 整合

收斂: 最近 10 循環 <1%

### energy.py

`E_total = E_resonance + E_flywheel + E_phantom`

- E_resonance = ΣΣ w_ij·sim(S_i,S_j)·exp(-λ·dist(I_i,I_j))
- dE_flywheel/dt = P_input - P_dissipation + P_synergy

### stability.py

- Lyapunov: V(θ) = ½‖θ‖², ˙V ≤ -cV (漸近穩定)
- 譜半徑: ρ_max = 0.73, 警報 >0.95
- 學習率: α(t) = α_init/(1+γ·t^κ)·exp(-λ·loss_variance)
  - α_init=0.1, γ=0.01, κ=0.6, λ=0.5, 動量 β=0.9
- 自我改進: A(t) = A₀·(1+η·t/t_ref)^ζ, η=0.3, ζ=1.4, t_ref=7

## Module 5: qcm/summoning/ — 動態角色召喚引擎

### features.py

6 特徵提取器:

| F | 特徵 | 方法 | 實作 |
|---|------|------|------|
| F1 | 關鍵詞密度 | TF-IDF (10K 詞表) | sklearn |
| F2 | 語義相似度 | Sentence-BERT (768d) | mock 介面 |
| F3 | 意圖識別 | RoBERTa | mock 7 類機率 |
| F4 | 歷史偏好 | 協同過濾 | 簡化用戶-任務矩陣 |
| F5 | 上下文連貫性 | LSTM | mock 注意力權重 |
| F6 | 緊急度偵測 | 時間分類器 | 時間戳→1-10 |

集成加權投票: `w = [0.25, 0.30, 0.20, 0.10, 0.10, 0.05]`

### matching.py

三階段管線:
1. 高層語境標註: NER + 分類 (F1=0.89)
2. 領域技能嵌入: BAAI/bge-base-zh-v1.5 (768d)
3. 馬氏距離度量學習: 學習特徵權重矩陣

技能匹配: `match_score = calculate_skill_match(skills, role)`, 激活 >0.75

動態懲罰: ≤8 角色=0 / 9-12=線性 / >12=指數

### registry.py

`DynamicRoleRegistry`: 可擴展角色庫, `summon_optimal_roles(context, max=15)`

## Pipeline 整合

`pipeline.py` 擴充:

```python
class PipelineEngine:
    def _init_modules(self):   # 新增
        self.role_registry = RoleIdentityRegistry()
        self.meeting = MeetingOrchestrator(self.role_registry)
        self.sandbox = SandboxEngine()
        self.flywheel = FlywheelEngine()
        self.summoning = SummoningEngine()

    def run_round(self):
        # ... 既有 R 計算 (22 formulas) ...
        
        # 新增整合點 (模組化 after R)
        meeting_state = self.meeting.process_round(self.round_count, R)
        sandbox_result = self.sandbox.evaluate(self.round_count, R, components)
        fw_state = self.flywheel.step(R=R, round_count=self.round_count)
        
        # Report 擴充
        result.modules = {
            'meeting': meeting_state,
            'sandbox': sandbox_result,
            'flywheel': fw_state._asdict(),
        }
```

向後相容: 可透過 config 啟用/停用, 預設啟用。不影響現有 test_qcm_all.py。

## 測試策略

新增 ~15 測試, 保持原有 25/25 ALL PASS:

| 測試文件 | 測試數 | 驗證內容 |
|---------|--------|---------|
| `test_roles.py` | 3 | 8 角色完整性, 共識算法, 一致性 |
| `test_collaboration.py` | 3 | 會議流程, 投票計數, 死鎖偵測 |
| `test_sandbox.py` | 3 | SRS, 門控, 排程 |
| `test_flywheel.py` | 3 | 外環迭代, 能量框架, 穩定性 |
| `test_summoning.py` | 3 | 技能匹配, 馬氏距離, 召喚 |

## 實作順序

Phase 1: roles/ + test_roles.py (基礎, 無依賴)
Phase 2: collaboration/ + test_collaboration.py (依賴 roles)
Phase 3: sandbox/ + test_sandbox.py (依賴 collaboration)
Phase 4: flywheel/ + test_flywheel.py (依賴 sandbox + 引擎)
Phase 5: summoning/ + test_summoning.py (依賴 roles + core)
Phase 6: pipeline 整合 + 回歸 25/25 + 新 ~15 測試 ALL PASS
