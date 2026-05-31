# Knowledge Crystals — Batch 0/1 ROOT + P00

> 中文名：Batch 0/1 根层与控制平面知识结晶。  
> 范围：ROOT、`00.超级提示词工程`、`qcm-universal-ai-system-v3.0.skill` 包级索引。  
> 状态：初始结晶，后续深读会继续拆到子系统级。

## KC-ROOT-001 — 母包使命不是替代通用 AI

```yaml
id: KC-ROOT-001
scope: ROOT
evidence_level: FACT
source_refs:
  - MISSION-MEMORY.md
statement: "母包使命是帮助开发者与通用 AI 长期、稳定、可验证地协同开发项目；它不是为了取代通用 AI，也不要求 AI 形成永久人格。"
implication: "所有秘书、角色、QCM、记忆、交付机制都必须降级为项目上下文和任务态协作协议。"
next_action: "任何新协议或提示词都必须通过模型原生边界审查。"
memory_target: AI_PROJECT_CONTEXT
```

## KC-ROOT-002 — 权威启动序列存在且优先

```yaml
id: KC-ROOT-002
scope: ROOT
evidence_level: FACT
source_refs:
  - MOTHER-PACK-ACTIVATION-GUIDE.md
  - AI_PROJECT_CONTEXT.md
statement: "根目录存在唯一权威 AI 启动协议，要求先确认根目录、读取四个启动文件、检查子系统完整性，再输出 awakening_check。"
implication: "未来 AI 不应直接进入任意子系统或读取全部文件；必须先唤醒、路由、最小上下文。"
next_action: "在黄金路径 GS-01 中持续验证 awakening_check 输出。"
memory_target: none
```

## KC-P00-001 — 引导秘书是导航和守门，不是执行者

```yaml
id: KC-P00-001
scope: P00_SUPER_PROMPT
evidence_level: FACT
source_refs:
  - 00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md
statement: "引导秘书负责意图识别、置信度、路由、上下文包和交接；禁止在意图识别阶段直接执行复杂任务。"
implication: "复杂需求必须先形成 guide_secretary packet，再进入子系统执行。"
next_action: "用 qa_runner route 和 VAL-ROOT-ROUTE-SMOKE 持续验证秘书可执行入口。"
memory_target: none
```

## KC-P00-002 — 路由矩阵已覆盖核心子系统

```yaml
id: KC-P00-002
scope: P00_SUPER_PROMPT
evidence_level: VERIFIED
source_refs:
  - 00.超级提示词工程/02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md
commands:
  - python qa_runner.py consistency
  - python qa_runner.py validate --scope ROOT
statement: "路由矩阵覆盖 00/01/02/03/04/05/USER_PACK 和 QCM skill；当前 consistency 10/10 PASS，route smoke 8/8 PASS，ROOT scope 7/7 automatic PASS。"
implication: "母包已经具备最低限度的自然语言入口到子系统路由能力，但低置信场景仍需 CLARIFY/CONFIRM。"
next_action: "新增核心意图或真实项目样本时，再同步扩展 SCENARIO-ACCEPTANCE-MATRIX.md 与 ROOT smoke 矩阵。"
memory_target: none
```

## KC-P00-003 — 原子文件清单已建立，但不等于已深读

```yaml
id: KC-P00-003
scope: CROSS
evidence_level: VERIFIED
source_refs:
  - 00.超级提示词工程/14-全链路审计与运行对齐/ATOMIC-FILE-INVENTORY.jsonl
  - 00.超级提示词工程/14-全链路审计与运行对齐/ATOMIC-FILE-INVENTORY-SUMMARY.md
commands:
  - python 00.超级提示词工程/14-全链路审计与运行对齐/generate_audit_assets.py
  - python qa_runner.py validate --scope P00_SUPER_PROMPT
statement: "当前已生成 1131 个文件原子的清单，包含子系统、类型、大小、行数、sha256、优先级和 audit_state。"
implication: "可以从 inventory 推进逐批深读；但默认状态仅为 inventoried，不能宣称已 read/understood。"
next_action: "按 DEEP-AUDIT-BATCH-EXECUTION-PLAN.yaml 批量提升状态。"
memory_target: none
```

## KC-P00-004 — 知识图谱种子已建立

```yaml
id: KC-P00-004
scope: CROSS
evidence_level: VERIFIED
source_refs:
  - 00.超级提示词工程/14-全链路审计与运行对齐/KNOWLEDGE-GRAPH-SEED.yaml
commands:
  - python qa_runner.py validate --scope P00_SUPER_PROMPT
statement: "知识图谱种子当前包含 96 个节点和 186 条边，连接 Project、Capability、Artifact、Validation、MemorySource、InventoryBucket 和 QCM skill package。"
implication: "后续深读不再只靠文档叙述，而能将结论挂到图谱节点和边。"
next_action: "每个 subsystem_crystal 产出后，应补充或更新 graph seed。"
memory_target: none
```

## KC-QCM-SKILL-001 — QCM skill 是独立关键技能包

```yaml
id: KC-QCM-SKILL-001
scope: QCM_SKILL
evidence_level: FACT
source_refs:
  - qcm-universal-ai-system-v3.0.skill
statement: "根目录 qcm-universal-ai-system-v3.0.skill 是一个压缩技能包，内部当前识别 43 个文件，包含 SKILL.md、config.yaml、references、scripts、tests、templates。"
implication: "不能把它只当普通二进制；也不能在未解包深读前声称已理解 QCM-45 全部方法论。"
next_action: "Batch B4 深读时按需提取 SKILL.md、config.yaml、references 和 tests。"
memory_target: none
```

## KC-RISK-001 — 深度理解必须避免再次同构扩写

```yaml
id: KC-RISK-001
scope: CROSS
evidence_level: RISK
source_refs:
  - CODEX-DEEP-AUDIT-EXECUTION-CHARTER.md
  - DEEP-UNDERSTANDING-KNOWLEDGE-CRYSTALLIZATION-BLUEPRINT.md
statement: "本项目最大风险不是缺少构想，而是 AI 继续生成同构提示词、角色和集成层，导致仓库更庞大但更难使用。"
implication: "未来工作必须以原子清单、图谱、场景矩阵、验证门和交付门收敛。"
next_action: "每次继续前先问：这是否提升可运行、可验证、可交付？若不是，停止。"
memory_target: AI_PROJECT_CONTEXT
```
