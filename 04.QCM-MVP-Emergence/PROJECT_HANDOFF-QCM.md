# QCM-MVP-Emergence — 專案交接文檔

> **版本**: v6.3 交付版 (Phase A+B+C + Paper Modules)
> **生成**: 2026-05-24
> **交付包**: 145 檔案, 63/63 VERIFY ALL PASS；2026-05-31 補跑 config-sync / health / service smoke
> **前身**: 涌 (Emergence) 研究原型 → QCM-MVP → qcm/ 命名空間包

---

## 1. 專案概要

QCM-MVP-Emergence 是 Q-SpecTrum 體系的原始研究原型，實現了 22 條共振公式（L1-L5）和 10 大原子能力，以展示**涌現 (Emergence)** 的計算模型。

- **入口**: `02-代码编写/main.py`（標準湧入口，R22=0.8664 湧現）
- **完整入口**: `02-代码编写/main_complete.py`（22 公式全集成管線）
- **驗證**: `02-代码编写/test_qcm_all.py`（25/25 ALL PASS）+ 5 模組測試（38/38 ALL PASS）+ `test_config_sync.py`（4/4）+ `health_check.py`（6/6 READY）

---

## 2. 架構

```
QCM-MVP-Emergence/
├── 00-知识结晶/          ← 13 篇核心論文/規格/規劃 (只讀知識庫)
├── 01-幽灵通道SDK/       ← Ghost Channel SDK (Python/TypeScript/JSON Schema)
├── 02-代码编写/          ← 32 .py 檔案 (所有公式 + 能力 + 入口 + 測試)
├── qcm/                 ← 34 檔案命名空間包 (含 5 論文模組子包)
│   ├── __init__.py       ← 路徑注入 + 公共 API
│   ├── config.py         ← 配置系統
│   ├── plugin.py         ← 註冊系統 (10 插件)
│   ├── pipeline.py       ← 22 公式管線 + Cap-D/G
│   ├── main.py           ← 三模式入口 + logging
│   ├── core/             ← L1 核心模組 (角色/增量/時鐘/計算/檢測)
│   ├── enhanced/         ← L2-L3 增強模組 (EPR/權重/距離/RCS/死鎖)
│   ├── evolution/        ← L4 演化模組 (沙盒/飛輪/知識增長)
│   ├── decision/         ← L5 決策模組 (路由/Pareto)
│   ├── capabilities/     ← 10 原子能力 (審計/加密/自愈/匹配/嵌入)
│   ├── roles/            ← §3.2 論文: 角色身份 + 共識
│   ├── collaboration/    ← §4 論文: 會議/投票/死鎖/審計
│   ├── sandbox/          ← §7 論文: 沙盒 SRS 排程器
│   ├── flywheel/         ← §8 論文: 雙環飛輪穩定性
│   └── summoning/        ← §9 論文: 技能召喚 TF-IDF
├── 04-运行结果/          ← 執行結果記錄 (只讀)
├── 05-参考资料/          ← 參考論文 (只讀)
├── docs/superpowers/     ← Paper module specs & plans (2 檔案)
├── QCM_四大體系深度推演_v1.0.md  ← 四大體系三視角沙盤推演
└── *.md                 ← 項目根文件
```

### 02-代码编写/ 核心模組

| 層級 | 公式 | 模組 | 說明 |
|------|------|------|------|
| L1 | F1-F5 | `calculator.py` | 共振計算 (R) — 核心湧量 |
| L1 | — | `simple_role.py` | 角色系統 (2-8 角色) |
| L1 | — | `delta.py` | 增量同步 (D) |
| L1 | — | `vector_clock.py` | 向量時鐘 (H) |
| L1 | — | `detector.py` | 湧現檢測 (J) |
| L2 | F6 | `epr_entanglement.py` | EPR 糾纏度 |
| L2 | F7 | `dynamic_weight.py` | 動態權重調整 |
| L3 | F8-F9 | `mahalanobis_distance.py` | 馬氏距離 + 對比損失 |
| L3 | F10-F11 | `rcs_hybrid.py` | RCS 決策系統 |
| L3 | F12-F13 | `deadlock_detector.py` | 死鎖檢測 (E) |
| L4 | F14-F15 | `sandbox.py` | 沙盒模擬 |
| L4 | F16-F18 | `flywheel.py` | 飛輪優化器 |
| L4 | F19-F20 | `knowledge_growth.py` | 知識增長引擎 |
| L5 | F21 | `neural_router.py` | 神經路由 |
| L5 | F22 | `pareto_cost.py` | Pareto 成本優化 |
| Cap-A | — | `semantic_matcher.py` | 語義匹配 |
| Cap-C | — | `embedding.py` | 語義嵌入 |
| Cap-D | — | `crypto.py` | AES-256-GCM 加密 |
| Cap-F | — | `audit.py` | 審計追蹤 |
| Cap-G | — | `self_healer.py` | 自愈恢復 |

### qcm/ 命名空間包 (Phase A+B+C + Paper Modules)

| 模組/子包 | 功能 | 層級 |
|-----------|------|------|
| `qcm/config.py` | JSON/YAML/dict 配置, plugin flag/權重/門檻 | 基礎 |
| `qcm/plugin.py` | PluginRegistry, 10 插件註冊 | 基礎 |
| `qcm/pipeline.py` | PipelineEngine, 22 公式全管線 + Cap-D/G 整合 | 核心 |
| `qcm/main.py` | 三模式入口 + logging + 強化 argparse + FastAPI 服務 | 入口 |
| `qcm/core/` | L1 核心: SimpleRole/DeltaSyncer/VectorClock/Calculator/Detector | L1 |
| `qcm/enhanced/` | L2-L3: EPR/DW/Mahalanobis/RCS/Deadlock | L2-L3 |
| `qcm/evolution/` | L4: Sandbox/Flywheel/KnowledgeGrowth | L4 |
| `qcm/decision/` | L5: NeuralRouter/ParetoCost | L5 |
| `qcm/capabilities/` | Cap A-J: Audit/Crypto/SelfHealer/Matcher/Embedder | 原子 |
| `qcm/roles/` | §3.2 論文: RoleIdentity + weighted consensus + safety veto | §3.2 |
| `qcm/collaboration/` | §4 論文: MeetingProtocol + Voting + Deadlock + Audit | §4 |
| `qcm/sandbox/` | §7 論文: 3-layer sandbox + SRS + CBP scheduler | §7 |
| `qcm/flywheel/` | §8 論文: outer/inner loop + energy + Lyapunov stability | §8 |
| `qcm/summoning/` | §9 論文: TF-IDF + ensemble matching + dynamic penalty | §9 |

---

## 3. 修復摘要（本次會話）

| 問題 | 修復 |
|------|------|
| 74 建構殘留 (pycache/egg-info/.pyc) | 全部刪除 |
| 12 個探索腳本 | 全部刪除 |
| 2 處 C:\Users 硬編碼路徑 | 已清除 |
| 重複論文 (00-知識結晶/ + 05-參考資料/) | 刪除 00- 副本 |
| 輸出文件 (debug_*.txt, verify_*.txt) | 全部刪除 |
| qcm_emergence/ 包 vs 平坦檔案衝突 | 抽取 4 唯一文件 → 平坦層，刪除 qcm_emergence/ |
| F19-F20 知識增長 198x 溢出 | 改用 EMA synergy + 微分積分 → 4.94x |
| self_healer.py import json 缺失 | 已補 |

---

## 4. 驗證狀態

```
test_qcm_all.py (standalone):
  25/25 ALL PASS ✅

test_roles.py (pytest):
  6/6 ALL PASS ✅

test_collaboration.py (pytest):
  7/7 ALL PASS ✅

test_sandbox.py (pytest):
  8/8 ALL PASS ✅

test_flywheel.py (pytest):
  11/11 ALL PASS ✅

test_summoning.py (pytest):
  6/6 ALL PASS ✅

Total:
  63/63 ALL PASS ✅

test_config_sync.py:
  4/4 PASS ✅

health_check.py:
  6/6 checks passed, Status READY ✅

main.py:
  R22=0.8664 湧現觸發 (threshold 0.85) ✅

main_complete.py:
  R22=0.8658 湧現觸發 ✅
  6/10 公式組活躍 (epr/dw/mdist/rcs/deadlock/kgrowth)
  知識增長 4.94x (目標 4.22x)

service smoke:
  /health, /status, /simulate HTTP 200 ✅
```

---

## 5. 交付物

- `VERIFY-QCM.md` — 交付驗收清單
- `MANIFEST-QCM.txt` — 143 檔案完整清單 (v6.3)
- `INDEX-QCM.md` — 檔案索引與分類統計 (v6.3)
- `PROJECT_HANDOFF-QCM.md` — 本文件 (v6.3)

## 6. 使用方式

```bash
# 標準湧入口 (保持不變)
cd 02-代码编写
python main.py

# 22 公式完整管線
python main_complete.py

# 全模組驗證
python test_qcm_all.py

# qcm/ 命名空間包 (Phase A+B+C)
python -m qcm.main --mode research --seed 42 --max-rounds 22
python -m qcm.main --mode production --seed 42 --max-rounds 22 --output ./results
python -m qcm.main --mode research --seed 42 --plugins epr dw rcs kgrowth
python -m qcm.main --mode research --cap-crypto --cap-healer
python -m qcm.main --mode service --port 8080
python -m qcm.main --mode research --config my_config.yaml
python -m qcm.main --mode research --log-level DEBUG
```

---

## 7. 已知事項

- **F14-F15/ F16-F18/ F21/ F22**: 默認關閉 (feature flag)，需 >2 角色或高 R 環境
- **Cap-D Merkle**: `crypto.py` 實現 AES-256-GCM，已接入 `qcm/pipeline.py`，默認關閉，需 `--cap-crypto`
- **Cap-G Self-Heal**: `self_healer.py` 實現快照恢復，已接入 `qcm/pipeline.py`，默認關閉，需 `--cap-healer`
- **Cap-A Semantic**: `semantic_matcher.py` 使用 `embedding.py` 可選真實嵌入
- **SDK 測試**: 幽靈通道 SDK (01-幽靈通道SDK/) 維持 v1.0 狀態，獨立測試
- **main.py vs main_complete.py**: main.py 是標準湧入口 (v6.0 權重)，main_complete.py 是 22 公式研究管線
- **qcm/ 包**: Phase A 命名空間包，非破壞性追加；當前已支援在專案根目錄直接執行 `python -m qcm.main`
- **qcm/pipeline.py**: 同步 main_complete.py 演算法，但經驗證 R22=0.8658 湧現一致

---

## 8. 與幽靈通道_v1.0 關係

| 項目 | QCM-MVP-Emergence | 幽靈通道_v1.0 |
|------|-------------------|----------------|
| 性質 | 研究原型 + qcm/ 包 + 5 論文模組 | 生產交付包 |
| 檔案 | 143 (交付清淨) | 303 |
| 公式 | 22 (L1-L5) + 5 論文模組 (§3.2/§4/§7/§8/§9) | 核心 + SDK |
| 入口 | main.py / qcm.main (三模式) | 3 SDK |
| 測試 | 25 + 38 = 63/63 ALL PASS；另有 config-sync 4 + health 6 | VERIFY 303/303 + SDK 162/162 |
| 狀態 | 維護中 + Phase A+B+C + Paper Modules 完成 | 凍結 (不可修改) |

---

## 9. 已完成

### Phase A — qcm/ 命名空間包 ✅
- config/plugin/pipeline/main 全完成
- 非破壞性追加，原始碼不動

### Phase B — 模組分層搬遷 ✅
- core/enhanced/evolution/decision/capabilities 五子包
- re-export 架構，import 路徑更新

### Phase C — 能力強化 ✅
- argparse 強化 (--output/--log-level/--plugins/--cap-crypto/--cap-healer)
- logging 模組
- FastAPI 服務 (6 端點: /health /status /simulate /step /reset /history /capabilities)
- Cap-D CryptoEngine 整合 (delta 加密驗證)
- Cap-G SelfHealer 整合 (快照 + 恢復)

### Phase 6 — 5 論文模組 (§3.2/§4/§7/§8/§9) ✅
- **§3.2 Identity & Consensus**: `qcm/roles/` — 角色身份技能向量 + 加權共識投票 (含安全否決權)
- **§4 Collaboration**: `qcm/collaboration/` — 5 階段會議協議 + 4 模式投票 + 死鎖檢測 + 審計追蹤
- **§7 Sandbox**: `qcm/sandbox/` — 3 層沙盒 (naive/analytic/trusted) + SRS 評分 + CBP 排程器
- **§8 Flywheel**: `qcm/flywheel/` — 雙環飛輪 (outer: 能力適應; inner: 收斂) + 能量率 + Lyapunov 穩定性
- **§9 Summoning**: `qcm/summoning/` — TF-IDF 特徵提取 + 集成匹配 + 動態罰分
- **測試**: 38 個新測試 (6+7+8+11+6), 全通過 ✅
- **規範**: `docs/superpowers/specs/` (設計規格) + `docs/superpowers/plans/` (12 任務實施計畫)

## 10. 建議下一步

1. **跨模組整合**: 將 5 論文模組接入 qcm/pipeline.py 主管線，實現端到端協作
2. **Phase D**: SQLite/CSV 結果持久化, 8 角色擴展, 飛輪啟用, Cap-D/G 完整啟用
3. **F19-F20 微調**: 調整 η 或 synergy_beta 使增長精確匹配 4.22x
4. **性能分析**: 100+ 輪堆疊測試，分析 R 收斂曲線
5. **TypeScript SDK**: 幽靈通道 SDK 已含 TypeScript 版 (14 測試)
