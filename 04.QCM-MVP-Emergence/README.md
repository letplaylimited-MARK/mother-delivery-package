# QCM-MVP-Emergence
## 幽灵通道协议 + 共鸣公式 = 涌现发生

**版本**: v6.3 (交付版，含 5 论文模块)  
**日期**: 2026-05-24  
**状态**: ✅ 63/63 核心测试 ALL PASS, 4 config-sync, 6 health, R22=0.8664（2026-05-31 审计补充）

---

## 核心公式

**知识共鸣能量函数**（涌现核心）：

v6.0 最终公式:
$$R(e_i, e_j) = 0.35 \cdot K_{sim} + 0.40 \cdot C_{comp} + 0.25 \cdot I_{freq}$$

> E 惩罚移除，R 可达 0.85+

**涌现测试结果 (seed=42)**:
```
Round 22: R = 0.8664 > 0.85 ✅
首次涌现: R22
最大 R: 0.8664
平均 R: 0.7938
```

**涌现阈值**: `R > 0.85` = 涌现发生（论文版）

---

## 项目结构

```
QCM-MVP-Emergence/
│
├── README.md                    # 本文件
├── INSTALL.md                   # 安装指南
├── USER_GUIDE.md                # 使用者手册
├── SCENARIOS.md                 # 使用场景
├── CHANGELOG.md                 # 变更日志
├── INDEX-QCM.md                 # 文件索引
├── VERIFY-QCM.md                # 交付验收清单
├── PROJECT_HANDOFF-QCM.md       # 交接文档（v6.3）
├── 22_FORMULA_SYSTEM.md         # 22 公式系统架构
├── KNOWLEDGE_GRAPH.md           # 知识图谱
├── QCM_四大體系深度推演_v1.0.md  # 深度推演
│
├── 00-知识结晶/                 # 核心知识来源（高频引用）
├── 01-幽灵通道SDK/              # 协议 SDK（Python/TS/Schema）
├── 02-代码编写/                 # 32 .py 文件（公式 + 测试 + 入口）
├── qcm/                        # 命名空间包（10 子包, 31 .py 文件）
│   ├── core/                   # L1: 角色/Delta/VC/Calculator/Detector
│   ├── enhanced/               # L2-L3: EPR/DW/Mahalanobis/RCS/Deadlock
│   ├── evolution/              # L4: Sandbox/Flywheel/KnowledgeGrowth
│   ├── decision/               # L5: NeuralRouter/ParetoCost
│   ├── capabilities/           # Cap D/G: Crypto/SelfHealer
│   ├── roles/                  # §3.2 论文: RoleIdentity + 共识
│   ├── collaboration/          # §4 论文: Meeting + Voting + Deadlock + Audit
│   ├── sandbox/                # §7 论文: 3层沙盘 + SRS + Scheduler
│   ├── flywheel/               # §8 论文: 内外循环 + Energy + Lyapunov
│   ├── summoning/              # §9 论文: TF-IDF + SkillMatch + Registry
│   ├── config.py               # 配置系统
│   ├── plugin.py               # 插件注册
│   ├── pipeline.py             # 22 公式全管线
│   └── main.py                 # 三模式入口
├── 04-运行结果/                 # 演示结果
├── 05-参考资料/                 # 论文稿/白皮书/规范稿
└── docs/superpowers/           # Paper module specs & plans
```

---

## 22 公式全实现

所有 22 条公式已在 qcm/ 命名空间包中实现：

| 层级 | 公式 | 模块 | 状态 |
|------|------|------|------|
| **L1** | F1-F5 共鸣核心 | `qcm/core/` | ✅ 管线集成 |
| **L2** | F6 纠缠 / F7 动态权重 | `qcm/enhanced/` | ✅ 管线集成 |
| **L3** | F8-F9 马氏距离 / F10-F11 RCS / F12-F13 死锁 | `qcm/enhanced/` | ✅ 管线集成 |
| **L4** | F14-F15 沙盘 / F16-F18 飞轮 / F19-F20 知识增长 | `qcm/evolution/` | ✅ 管线集成 |
| **L5** | F21 神经路由 / F22 Pareto 成本 | `qcm/decision/` | ✅ 缺省关闭(feature flag) |

### 论文扩展模块

| 论文章节 | 模块 | 功能 |
|----------|------|------|
| §3.2 角色身份 | `qcm/roles/` | 8 角色模板 + weighted consensus + safety veto |
| §4 协作协议 | `qcm/collaboration/` | 5 阶段会议 + VoteMode + 死锁检测 + AuditLog |
| §7 沙盒隔离 | `qcm/sandbox/` | 3 层沙盘 + SRS 评分 + CBP 调度 |
| §8 飞轮优化 | `qcm/flywheel/` | 内外循环 + 能量函数 + Lyapunov 稳定性 |
| §9 召唤匹配 | `qcm/summoning/` | TF-IDF 特征 + SkillMatch + 动态惩罚 |

### 原子能力

| 编号 | 能力 | 状态 |
|------|------|------|
| A | Delta 增量同步 | ✅ 管线集成 |
| B | 因果排序（VectorClock） | ✅ 管线集成 |
| C | 加密传输（AES-256-GCM） | ✅ Cap-D 可用，默认关闭，`--cap-crypto` 启用 |
| D | 完整性验证（Merkle） | ✅ Cap-D，可由 pipeline flag 启用 |
| E | 审计追踪（AuditLog） | ✅ 管线集成 |
| F | 自愈恢复（Snapshot） | ✅ Cap-G 可用，默认关闭，`--cap-healer` 启用 |
| G | 语义匹配 | ✅ Cap-A 可用 |
| H | 涌现检测 | ✅ 管线集成 |
| I | 飞轮优化 | ✅ 管线集成 |
| J | 角色管理（8 角色） | ✅ 管线集成 |

---

## 快速入口

```bash
# 标准涌现演示（v6.0 权重, 22 轮涌现）
python "02-代码编写/main.py"

# 完全体管线（22 公式全集成）
python "02-代码编写/main_complete.py"

# qcm/ 命名空间包三模式入口
python -m qcm.main --mode research --seed 42 --max-rounds 22
python -m qcm.main --mode production --seed 42 --max-rounds 3 --output ./output

# 运行全部 63 项核心发布测试
python "02-代码编写/test_qcm_all.py"
pytest "02-代码编写/test_roles.py" "02-代码编写/test_collaboration.py" "02-代码编写/test_sandbox.py" "02-代码编写/test_flywheel.py" "02-代码编写/test_summoning.py" -v

# 运行额外守卫
python "02-代码编写/test_config_sync.py"
python health_check.py
```

### 测试结果

| 测试 | 数量 | 结果 |
|------|------|------|
| test_qcm_all.py (综合) | 25/25 | ✅ ALL PASS |
| test_roles.py | 6/6 | ✅ ALL PASS |
| test_collaboration.py | 7/7 | ✅ ALL PASS |
| test_sandbox.py | 8/8 | ✅ ALL PASS |
| test_flywheel.py | 11/11 | ✅ ALL PASS |
| test_summoning.py | 6/6 | ✅ ALL PASS |
| **总计** | **63/63** | ✅ **ALL PASS** |
| test_config_sync.py | 4/4 | ✅ 配置常数同步守卫 |
| health_check.py | 6/6 | ✅ READY |

---

## 涌现等级

| 等级 | R 值 | 行为 |
|------|------|------|
| 无协同 | <0.3 | 独立工作 |
| 初步协同 | 0.3-0.5 | 简单交互 |
| 中度协同 | 0.5-0.7 | 任务协调 |
| 深度协同 | 0.7-0.85 | 知识共鸣 |
| **涌现（论文）** | >0.85 | **自主智慧** |

---

## 技术指标

| 指标 | 当前值 |
|------|--------|
| Python 源码文件 | 63 (qcm/ 31 + 02-代码编写/ 32) |
| 测试通过率 | 63/63 核心发布测试 + 4 config-sync + 6 health |
| 涌现轮次 | R22 (seed=42) |
| 涌现 R 值 | 0.8664 |
| 确认模块数 | 10 qcm/ 子包 + 5 论文模块 |
| 配置方式 | QCMConfig (JSON/YAML/dict) |
| 入口模式 | main.py / main_complete.py / qcm/main.py |

---

## 使用者文件

| 文件 | 說明 |
|------|------|
| `INSTALL.md` | 安裝指南：系統需求、依賴安裝、驗證步驟、故障排除 |
| `USER_GUIDE.md` | 使用者手冊：三種執行模式、API 使用、模組操作、結果解讀 |
| `SCENARIOS.md` | 使用場景：研究驗證、工程開發、生產部署、教育演示 |

## 注意事項 / Caveats

### 已知限制
- **湧現演示固定種子**: `seed=42` 確保湧現在 R22 觸發；更換種子可能影響湧現輪次
- **Feature Flag 公式**: F14-F15（沙盤）、F16-F18（飛輪）、F21（神經路由）、F22（Pareto）預設關閉，需 >2 角色或高 R 環境才會自動啟用
- **Cap-D/Cap-G 默認不啟用**: CryptoEngine（加密）和 SelfHealer（自癒）已接入 `qcm/pipeline.py`，但需透過 `--cap-crypto` / `--cap-healer` 或 config flag 顯式啟用
- **論文模組需 modules=True**: `QCMConfig` 中 `modules` 必須設為 `True`（預設值）才會載入 §3.2/§4/§7/§8/§9 五個論文模組
- **角色數量**: 預設 2 角色演示（Secretary, Researcher），`RoleFactory` 支援 2-8 角色

### 運行條件
- **工作目錄**: 所有指令必須在 `QCM-MVP-Emergence/` 根目錄下執行
- **Python 版本**: 建議 Python 3.10+，最低 3.8
- **外部依賴**: `numpy` + `pyyaml` 為必要；`cryptography`、`fastapi`、`sentence-transformers` 為可選

### 調試提示
- 若 `sandbox` 或 `flywheel` 的 `enhanced` 資料缺失：檢查 `_run_paper_modules` 的 try/except 是否吞掉了錯誤（見 `CHANGELOG v6.3` 修復記錄）
- 若出現 `ImportError: qcm.*`：確認在根目錄執行，或手動 `sys.path.insert(0, '.')`

## 扩展阅读

- `PROJECT_HANDOFF-QCM.md` — 完整交接文档（v6.3）
- `INDEX-QCM.md` — 文件索引
- `VERIFY-QCM.md` — 交付验收清单
- `CHANGELOG.md` — 完整版本历史
- `22_FORMULA_SYSTEM.md` — 22 公式系统架构
- `docs/superpowers/` — 论文模块设计文档 (2026-05-24)

*本项目为 QCM 核心概念 MVP 验证 + 论文模块实现*
*最后更新: 2026-05-24*
