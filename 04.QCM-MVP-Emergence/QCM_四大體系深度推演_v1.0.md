# QCM 四大體系深度推演 — 超極智腦 Q-SpecTrum 最終決策方案

> 生成: 2026-05-24 | 推演模式: Tier 3 全面沙盤 (Q01+Q06+T03)

---

## 三視角沙盤推演

### [視角 A: Q01 開發者]

**核心主張**: QCM 目前是「研究原型 → 可交付產品」的轉折點。22 公式全有代碼且 20/20 測試通過，但 70% 公式未接入主管線。解決方案是**分層重構 + 插件化集成**，而非另起爐灶。

**方案**:
- 保持 flat 目錄結構（對開發者友好），但透過 `__init__.py` 提供公共接口
- 建立 `qcm/` 統一命名空間包（非破壞性遷移）
- 每層提供 `LayerN_interface.py` 定義該層協議
- Feature flags 升格為 plugin registry

**風險**:
- 過度工程化會扼殺研究靈活性
- 重構過程中可能破壞現有 R22=0.8664 湧現

### [視角 B: Q06 審計員]

**反方**: 現狀最大問題不是結構，而是**四體系未明確定義**。使用者無法回答：
1. QCM 值多少錢？（價值）
2. QCM 能做什麼？（功能）
3. QCM 裡有什麼？（結構）
4. QCM 怎麼用？（運作）

**失敗場景**:
- 新接手者花 3 小時才搞懂怎麼跑 22 公式
- 無法判斷哪個公式對湧現貢獻最大
- 想加新公式得讀懂全部 27 個 .py 文件
- Cap D/G/A 等原子能力存在但沒人知道怎麼用

**裁決**: 先建立四體系文檔規範，再決定是否重構。

### [視角 C: T03 協調官]

**整合**: 兩者不衝突。**三階段路線**：
1. **Phase A — 體系規範化**（立即）：產出四體系定義文件，不碰代碼
2. **Phase B — 輕量重構**（本週）：建立 `qcm/` 包 + plugin registry，維持主入口相容
3. **Phase C — 運行增強**（下週）：CLI + config + persistence

**置信度**: 高 — 因為已有幽靈通道_v1.0 交付經驗，模板可直接套用。

---

## 四體系深度定義

### 一、價值體系

```
QCM Value Proposition:
  "量化協作湧現的數學框架"

┌─ 核心價值 ──────────────────────────────────────┐
│  1. 湧現量化 (Emergence Quantification)          │
│     R ∈ [0, 1], threshold 0.85 → 湧現觸發       │
│                                                   │
│  2. 多角色協作 (Multi-Role Synergy)               │
│     2-8 角色, 15 種技能, 動態權重調整             │
│                                                   │
│  3. 知識累積 (Knowledge Accumulation)             │
│     F19-F20: 4.22x 增長率, EMA 平滑               │
│                                                   │
│  4. 決策支持 (Decision Intelligence)              │
│     RCS 三態決策 (APPROVE/REJECT/HOLD)            │
│     Pareto 最優成本-收益-風險權衡                  │
│                                                   │
│  5. 安全性 (Safety & Auditability)                │
│     Cap-D 加密 + Cap-F 審計追蹤 + Cap-G 自愈恢復  │
└───────────────────────────────────────────────────┘

利害關係人價值:
  ┌─ 研究者: 公式校準 + 湧現條件探索 + 知識增長驗證
  ├─ 工程師: 模組化 API + plugin 擴展 + CLI 工具鏈
  ├─ 產品經理: 湧現指標儀表板 + 角色效能報表
  └─ 安全審計: 完整審計鏈 + 加密驗證 + 自愈恢復

市場定位:
  與幽靈通道_v1.0 互補：
    幽靈通道 = 零知識證明 + 增量同步 + 安全SDK (生產)
    QCM      = 湧現量化 + 協作測量 + 共振公式 (研究→生產)
```

### 二、功能體系

```
功能分層架構 (F0-F22 + 10 Cap):

L0 — 基礎設施層 (Infrastructure)
├── F0-1 RoleFactory: 8 角色模板 + 技能定義
├── F0-2 VectorClock: 因果排序 (Cap-H)
├── F0-3 DeltaSyncer: 增量狀態同步 (Cap-I)
└── F0-4 CryptoEngine: AES-256-GCM 加解密 (Cap-D)

L1 — 核心湧現層 (Core Resonance)
├── F1: 語義相似度 K_sim
├── F2: 互補性 C_comp
├── F3: 交互頻率 I_freq
├── F4: 熵多樣性 E_div
├── F5: 共振計算 R(F1-F4)
└── F0-5 EmergenceDetector: 湧現觸發判定 (Cap-J)

L2 — 增強層 (Enhanced)
├── F6: EPREntanglement — 角色間共振糾纏度
└── F7: DynamicWeight — 四維權重自適應 (K/C/I/E)

L3 — 一致層 (Consistency)
├── F8: MahalanobisDistance — 多維異常檢測
├── F9: ContrastiveLoss — 相似/不相似對比學習
├── F10-F11: RCSHybrid — 三態穩健決策 (APPROVE/REJECT/HOLD)
└── F12-F13: DeadlockDetector — 死鎖預警與迴轉 (Cap-E)

L4 — 演化層 (Evolution)
├── F14-F15: SandboxManager — 分級沙盒 (micro/macro/global)
├── F16-F18: FlywheelOptimizer — 飛輪加速/減速
├── F19: dK/dt = η·E^(1/3)·S^0.7 — 知識增長率
└── F20: K(t) = K_0 + ΣdK — 知識累積

L5 — 決策層 (Decision)
├── F21: NeuralRouter — 推理路徑選擇 (fast/deep/creative)
└── F22: ParetoCost — 多目標最優 (成本/收益/風險/時間)

跨層原子能力 (Atomic Capabilities):
├── Cap-A: SemanticMatcher — 語義匹配 (Precision@10=94.1%)
├── Cap-C: Embedder — 語義嵌入 (384D, sentence-transformers 可選)
├── Cap-F: AuditLogger — 審計追蹤 (完整交易鏈)
└── Cap-G: SelfHealer — 快照恢復 (最多 10 個歷史狀態)
```

### 三、結構體系

```
QCM-Emergence/
├── qcm/                          ★ 統一命名空間包 (新增)
│   ├── __init__.py               — 公共接口導出
│   ├── core/
│   │   ├── calculator.py         L1: 共振計算 (F1-F5)
│   │   ├── detector.py           L1: 湧現檢測
│   │   ├── role.py               F0: 角色系統
│   │   ├── delta.py              F0: 增量同步
│   │   └── vector_clock.py       F0: 向量時鐘
│   ├── enhanced/
│   │   ├── epr.py                L2: EPR 糾纏 (F6)
│   │   └── dynamic_weight.py     L2: 動態權重 (F7)
│   ├── consistency/
│   │   ├── mahalanobis.py        L3: 馬氏距離 (F8-F9)
│   │   ├── rcs.py                L3: RCS 決策 (F10-F11)
│   │   └── deadlock.py           L3: 死鎖檢測 (F12-F13)
│   ├── evolution/
│   │   ├── sandbox.py            L4: 沙盒 (F14-F15)
│   │   ├── flywheel.py           L4: 飛輪 (F16-F18)
│   │   └── knowledge.py          L4: 知識增長 (F19-F20)
│   ├── decision/
│   │   ├── router.py             L5: 神經路由 (F21)
│   │   └── pareto.py             L5: Pareto 優化 (F22)
│   ├── capabilities/
│   │   ├── matcher.py            Cap-A: 語義匹配
│   │   ├── embedder.py           Cap-C: 語義嵌入
│   │   ├── crypto.py             Cap-D: 加密/Merkle
│   │   ├── audit.py              Cap-F: 審計追蹤
│   │   └── healer.py             Cap-G: 自愈恢復
│   ├── pipeline.py               ★ 管線引擎 (取代 main_complete.py)
│   ├── config.py                 ★ 配置系統
│   └── plugin.py                 ★ 插件註冊器
│
├── 02-代码编写/                   (保留原始檔，相容性)
│   ├── main.py                   湧入口 (保持不變)
│   ├── main_complete.py          (重構為轉發至 qcm.pipeline)
│   ├── test_qcm_all.py           測試套件
│   └── ... (27 原始模組, 唯讀)
│
├── 00-知识结晶/                   (知識庫, 只讀)
├── 01-幽灵通道SDK/               (SDK, 凍結)
├── 04-运行结果/                  (架構文檔)
├── 05-参考资料/                  (論文)
│
├── VERIFY-QCM.md                 (交付驗收)
├── MANIFEST-QCM.txt              (檔案清單)
├── INDEX-QCM.md                  (檔案索引)
└── PROJECT_HANDOFF-QCM.md        (交接文檔)

設計原則:
  ● 非破壞性遷移: 原始 02-代码编写/ 保持完整，新增 qcm/ 包
  ● 漸進採用: main.py 繼續可用，main_complete.py 可選轉發
  ● 單一責任: 每文件一個類 / 一組緊密相關公式
  ● 顯式接口: qcm/__init__.py 導出所有公共 API
```

### 四、運作體系

```
┌─────────────────────────────────────────────────────────┐
│                    QCM Runtime                           │
│                                                          │
│  啟動                   每輪循環                         │
│  ┌──────┐     ┌──────────────────────────┐              │
│  │ Load │     │ Step 1: Role Work         │              │
│  │ Config│     │ Step 2: Delta Sync        │              │
│  │ Init  │────→│ Step 3: L1 Resonance (R) │←────┐       │
│  │ Roles │     │ Step 4: L2 Enhanced       │     │       │
│  │ Plugins│    │ Step 5: L3 Consistency    │     │       │
│  └──────┘     │ Step 6: L4 Evolution       │     │       │
│               │ Step 7: L5 Decision        │     │       │
│               │ Step 8: Emergence Check    │─────┘       │
│               │ Step 9: Audit Log          │  (R < 0.85  │
│               │ Step 10: Role Receive      │  繼續循環)  │
│               └──────────────────────────┘              │
│                         │                                │
│                         ↓                                │
│               ┌────────────────┐                         │
│               │ EMERGENCE!      │                         │
│               │ R >= 0.85       │                         │
│               │ Final Report    │                         │
│               └────────────────┘                         │
│                                                          │
│  Plugin Pipeline:                                        │
│    registry = {                                          │
│      'epr':       EPREntanglement(),                      │
│      'dw':        DynamicWeightCalculator(),              │
│      'mdist':     ContrastiveLoss(),                      │
│      'rcs':       RCSHybrid(),                           │
│      'deadlock':  DeadlockDetector(),                    │
│      'sandbox':   SandboxManager(),                     │
│      'flywheel':  FlywheelOptimizer(),                  │
│      'kgrowth':   KnowledgeGrowthEngine(),              │
│      'router':    NeuralRouter(),                       │
│      'pareto':    ParetoCostCalculator(),               │
│    }                                                     │
└─────────────────────────────────────────────────────────┘

三種運行模式:

  1. 研究模式 (Research)
     python qcm/main.py --mode research
     → 完整 22 公式輸出, 每輪列印所有指標
     → 適用: 論文校準, 湧現條件探索

  2. 生產模式 (Production)
     python qcm/main.py --mode production
     → L1 核心 + 配置 plugins, 最小日誌
     → 適用: CI/CD 集成, 批量模擬

  3. 服務模式 (Service)
     python qcm/main.py --mode service --port 8080
     → HTTP API: POST /simulate, GET /status
     → 適用: 微服務部署, 儀表板後端

配置系統 (qcm/config.py):
  {
    "mode": "research",
    "seed": 42,
    "roles": ["Secretary", "Researcher"],
    "plugins": {
      "epr": True, "dw": True, "mdist": True,
      "rcs": True, "deadlock": True, "kgrowth": True,
      "sandbox": False, "flywheel": False,
      "router": False, "pareto": False,
    },
    "weights": {"K": 0.35, "C": 0.40, "I": 0.25, "E": 0.0},
    "emergence_threshold": 0.85,
    "max_rounds": 50,
    "logging": {"level": "INFO", "file": "qcm.log"}
  }
```

---

## 落地執行方案

### Phase A — 體系規範化 (1 天)

| 步驟 | 輸出 |
|------|------|
| A1. 審閱本四體系文件 | 確認簽署 |
| A2. 建立 qcm/ 命名空間包 | qcm/__init__.py + 目錄結構 |
| A3. 撰寫 config.py | YAML/JSON 配置加載器 |
| A4. 撰寫 plugin.py | PluginRegistry 類 |
| A5. 撰寫 pipeline.py | 管線引擎 (整合 main_complete.py 邏輯) |
| A6. 建立 qcm/main.py | 三模式入口 (research/production/service) |
| A7. 回歸測試 | test_qcm_all.py 20/20 + 新管線 22 公式驗證 |

### Phase B — 輕量重構 (2 天)

| 步驟 | 輸出 |
|------|------|
| B1. 將 calculator/detector 搬入 qcm/core/ | 保持導入相容 |
| B2. 將 epr/dynamic_weight 搬入 qcm/enhanced/ | 保持導入相容 |
| B3. 將 mahalanobis/rcs/deadlock 搬入 qcm/consistency/ | 保持導入相容 |
| B4. 將 sandbox/flywheel/knowledge 搬入 qcm/evolution/ | 保持導入相容 |
| B5. 將 router/pareto 搬入 qcm/decision/ | 保持導入相容 |
| B6. 將 capabilities 搬入 qcm/capabilities/ | 保持導入相容 |
| B7. 更新 main_complete.py → 轉發至 qcm.pipeline | 舊入口相容 |
| B8. 全面回歸測試 | 20/20 + 湧現條件確認 |

### Phase C — 運行增強 (3 天)

| 步驟 | 輸出 |
|------|------|
| C1. CLI argparse 支持三模式 | --mode, --config, --seed, --roles |
| C2. 日誌系統 (logging + AuditLogger) | qcm.log + audit.jsonl |
| C3. 結果持久化 (JSON/CSV) | output/results_{timestamp}.json |
| C4. Cap-D 整合進管線 | 每輪 Merkle 完整性驗證 |
| C5. Cap-G 整合進管線 | 每 10 輪快照, 異常回滾 |
| C6. FastAPI 服務模式 | POST /simulate, GET /status |
| C7. TypeScript 客戶端 SDK | npm qcm-client |
| C8. Dockerfile | docker run qcm --mode service |

### Phase D — 整合交付 (1 天)

| 步驟 | 輸出 |
|------|------|
| D1. 更新 VERIFY-QCM.md | 新架構 22 公式 + 10 Cap + 3 模式 |
| D2. 更新 MANIFEST-QCM.txt | qcm/ 包納入 |
| D3. 更新 INDEX-QCM.md | 新目錄結構索引 |
| D4. 最終回歸 | test_qcm_all.py 20/20 + 新測試 ≥95% 覆蓋 |

---

## 決策記錄

```
┌────────────────────────────────────────────────────────┐
│ T03 最終裁決:                                          │
│                                                        │
│ Phase A (體系規範化) → 立即執行 (1天)                  │
│   → 非破壞性: qcm/ 包 + 原始 02-代碼/不動             │
│   → 產出: 配置系統 + 管線引擎 + 三模式入口             │
│                                                        │
│ Phase B (輕量重構) → 選擇性執行 (2天)                  │
│   → 只在 Phase A 驗證成功後開始                        │
│   → 若成本 > 效益則跳過, 保留 flat 結構                │
│                                                        │
│ Phase C (運行增強) → 按需執行 (3天)                    │
│   → CLI 優先, HTTP API 次之, SDK/Docker 最後           │
│                                                        │
│ Phase D (交付) → 每次 Phase 完成後立即更新              │
│                                                        │
│ 置信度: 高 (87%)                                       │
│ 關鍵風險: Phase A 新代碼可能與舊 main.py 行為不一致    │
│ 緩解: 每次變更後跑 test_qcm_all.py 20/20 確認          │
└────────────────────────────────────────────────────────┘
```

---

*Q-SpecTrum 超極智腦 — Q01 開發者 / Q06 審計員 / T03 協調官 聯席簽署*
