# Breakpoint Repair Matrix

> 用途：把“显式断裂点”和“隐蔽断裂点”从散落问题变成可追踪、可修复、可验证的母包运行矩阵。  
> 原则：断裂点不是概念批评，而是齿轮咬合问题；每一项都必须指向协议字段、状态机、注册表、验证命令或交接产物。

## 1. 修复结论

本轮将断裂点整理为：

- 6 个显式断裂点：用户或文档可以直接看见的链路缺口。
- 4 个隐蔽断裂点：单独看文件似乎合理，但跨系统运行时会卡死或漂移。
- 5 个追加修复项：不是原始断裂点，但会导致后续 AI 接手时重复误判。

优先级判断：

```text
P0：会阻断自然语言进入母包后的正确路由、状态追踪或验证。
P1：会造成长期记忆、注册表、运行事实漂移。
P2：会降低后续自动化、可读性或审计效率。
```

## 2. 6 个显式断裂点

| ID | 断裂点 | 风险 | 本轮修复 |
|---|---|---|---|
| EXP-001 | 启动顺序不一致 | `MISSION-MEMORY`、`AI_PROJECT_CONTEXT`、`00 README`、`CROSS-PROJECT-WORKFLOW` 对唤醒、模型原生边界、引导秘书、路由矩阵的顺序不完全一致，后续 AI 可能跳过使命唤醒或直接路由 | 统一启动链：使命记忆 -> 全局地图 -> 00 README -> Master -> Model Native -> Awakening -> Guide Secretary -> Routing -> Context Pack -> USO Ledger |
| EXP-002 | 引导秘书到路由矩阵缺少反馈 | Guide Secretary 只输出“要去哪”，Routing Matrix 没有把“路由是否命中、拒绝了哪些路径、为什么需要降级”反馈给秘书和 Context Pack | 在 Guide Secretary、Handoff、Context Pack 增加 `route_feedback` 字段 |
| EXP-003 | Context Pack/交接包缺少 USO 追踪 | 跨文件夹任务只有自然语言和文件清单，没有 `uso_id`、`ledger_ref`、`validation_refs`，无法进入统一状态账本 | 增加 `traceability` 字段，绑定 `UNIFIED-STATUS-OBJECT-SPEC.md` 与 `UNIFIED-STATUS-LEDGER.yaml` |
| EXP-004 | 原子治理缺少暂停/阻塞状态 | 原状态机从 `IN_PROGRESS` 直接到 `VERIFIED`，没有表达“主动暂停”“被依赖阻塞”“被新需求替代” | 状态机增加 `PAUSED`、`BLOCKED`、`SUPERSEDED`，并补充进入条件和恢复规则 |
| EXP-005 | 验证语义被折叠 | Manifest 完整性、SDK 测试、模板 smoke、健康检查、严格交付门被混写为“验证”，容易把 smoke 当成 release gate | `VALIDATION_REGISTRY.yaml` 继续分开 integrity、test、template、health、delivery；工作流文档改成显式语义 |
| EXP-006 | 用户交付包模板态与最终态混淆 | 普通验证通过不代表最终项目交付可用；Strict 失败是模板态正常结果，但容易被误报为缺陷或完成 | 继续把 `VERIFY-DELIVERY.ps1` 与 `-Strict` 区分为 base/template gate 与 final delivery gate |

## 3. 4 个隐蔽断裂点

| ID | 隐蔽断裂点 | 为什么隐蔽 | 本轮修复 |
|---|---|---|---|
| HID-001 | 停止线分散 | Guide Secretary、Mission Memory、Anti-Drift、Full Audit 都有停止线，但没有统一裁决口径 | 在 Guide/Handoff/Context Pack 中把停止线纳入 `governance` 与 `route_feedback.blocked_reason`，后续可升级为 Stop-Line Adjudicator |
| HID-002 | 记忆源优先级未机器化 | `MEMORY-SOURCE-PRIORITY.md` 是人读文档，03/05 的 DB、JSONL、BRAIN-KB、handoff 之间仍可能被混用 | 新增 `MEMORY-SOURCE-INDEX.yaml`，给每个记忆源定义权威范围、读优先级、写目标、查询入口、冲突 owner |
| HID-003 | 运行事实与展示事实重复漂移 | 05 有核心平台 DB、根目录 DB、runtime DB、dashboard 统计；单独看都像真实状态 | 在记忆源索引中标记 `source_status` 和冲突规则，强调以核心 DB / _HANDOFF / BRAIN-KB 为准 |
| HID-004 | 验证命令隐藏副作用 | `02 memoryos.py` smoke 会写测试记忆；`04 --mode production` 写输出；service 是长运行；pytest 生成缓存 | 在工作流和验证登记中标注 side effects，避免把“检查”误当成无副作用读取 |

## 4. 追加修复项

| ID | 追加项 | 原因 | 状态 |
|---|---|---|---|
| ADD-001 | 注册表字段需要 `semantics`、`side_effects`、`source_status` | 否则 AI 只能知道“有命令/有文件”，不知道命令含义和副作用 | 本轮先在新记忆源索引落地，后续扩展到验证/能力注册表 |
| ADD-002 | `03` 搜索 DB 优先级需与记忆优先级一致 | 先前 artifact registry 把 search DB 标为 P2，但记忆优先级文档已把 03 搜索/记忆列入 P1 | 本轮把 `ART-03-SEARCH-DB` 修为 P1 |
| ADD-003 | 路由后必须回写 Context Pack | 没有回写，下一位 AI 看不到为何走这条路径 | 本轮增加 `route_feedback` 与 `traceability` 字段 |
| ADD-004 | 深度审计不等于已读 100% | 目前是重点文件和验证链路深读，不应声称 1118 文件全部语义审计完成 | 保留 Coverage Registry 的 `PARTIAL-DEEP` 口径 |
| ADD-005 | 需要后续自动校验脚本 | 当前矩阵与索引仍依赖人工维护 | 标记为下一轮 P1 自动化任务 |

## 5. 修复后的标准齿轮链

```text
用户自然语言
  -> Mission Memory
  -> AI Project Context
  -> 00 README / Master Orchestrator
  -> Model Native Boundary
  -> Awakening Check
  -> Guide Secretary
  -> Routing Matrix
  -> Route Feedback
  -> Context Pack
  -> Atomic Governance / USO Ledger
  -> Execute / Verify / Audit
  -> Handoff / Memory Source Index
  -> User Pack or Mother Pack next action
```

关键要求：

- `Guide Secretary` 不能只给路由结论，必须记录 `route_feedback`。
- `Context Pack` 不能只给文件清单，必须带 `traceability`。
- `Atomic Governance` 不能只记录进行中和完成，必须能暂停、阻塞、替代。
- `Memory` 不能只说“写入长期记忆”，必须说明写入哪个权威源、以谁为准。
- `Validation` 不能只说“已验证”，必须说明验证类型、命令、证据等级和副作用。

## 6. 后续验证清单

- [x] 新 AI 冷启动时能按统一启动链输出 `awakening_check`。（已验证：P0-3统一ACTIVATION-GUIDE为唯一权威启动协议）
- [x] Guide Secretary 的 YAML 中包含 `traceability` 与 `route_feedback`。（已验证：GUIDE-SECRETARY-PROTOCOL.md 第192/196行）
- [x] Context Pack 中包含 `uso_id`、`ledger_ref`、`validation_refs`。（已验证：AI-CONTEXT-PACK-TEMPLATE.md 第17-19行）
- [x] 原子任务可以进入 `PAUSED`、`BLOCKED`、`SUPERSEDED`，且有恢复或关闭条件。（已验证：ATOMIC-AI-DEVELOPMENT-OPERATING-SYSTEM.md 第77-111行）
- [x] 记忆源冲突时可从 `MEMORY-SOURCE-INDEX.yaml` 找到权威 owner。（已验证：28处owner/权威/conflict引用）
- [x] 验证登记能区分 integrity、test、template smoke、health、delivery strict。（已验证：VALIDATION_REGISTRY.yaml 存在）
