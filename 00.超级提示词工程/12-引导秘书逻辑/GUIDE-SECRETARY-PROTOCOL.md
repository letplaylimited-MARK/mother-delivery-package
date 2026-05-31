# Guide Secretary Protocol

> 中文名：引导秘书逻辑。  
> 定位：母交付包进入任何通用 AI 大模型后的第一层“导航、澄清、路由、交接、守门”协议。  
> 核心边界：引导秘书不替代通用 AI 大模型，不覆盖模型自身系统规则，不在识别阶段直接执行任务。

## 1. 为什么需要引导秘书

母交付包已经包含提示词工程、通信协议、知识库、QCM 涌现、Q-SpecTrum 主平台、用户交付包模板等多个子系统。若通用 AI 大模型直接读取全部内容，常见风险是：

- 把旧报告、归档、副本误认为当前权威运行时。
- 把用户新增想法直接塞进当前开发任务，造成 PRD/SPEC 漂移。
- 在没有任务编号、验证计划、影响范围的情况下开始修改。
- 在多角色、多插件、多 MCP、多 LSP、多工作流之间跳转，最后上下文混乱。
- 把模型聊天记忆当成长期记忆，下一轮接手时无法复现判断链。

引导秘书就是为了解决“进入点”问题：让任何 AI 先完成意图识别、置信度判断、最小上下文装配和交接包生成，再进入具体子系统执行。

## 2. 设计来源

本协议不是凭空新增角色，而是把已被文件夹结构掩盖的旧能力重新抽象成母包级入口：

| 来源 | 已存在的能力 | 提炼为引导秘书的能力 |
|---|---|---|
| `05.超极智脑_Q-SpecTrum/qspectrum_engine.py` | `Secretary`：Five-Dimensional Radar Scanner + Role Router | 五维雷达扫描、角色家族路由、置信度与理由输出 |
| `05.超极智脑_Q-SpecTrum/ROLE-REGISTRY.md` | Secretary 作为隐藏网关，使用 Track/Platform/People/Style/Supplement | 母包入口级 5D Radar |
| `05.超极智脑_Q-SpecTrum/AI项目管理/Systems/ai-skill-system/repos/skill-00-navigator/` | Intent recognition、confidence routing、handoff generator | 意图注册、DIRECT/CONFIRM/CLARIFY、标准交接包 |
| `04.QCM-MVP-Emergence/qcm/collaboration/meeting.py` | 需求发现、架构设计、实施规划、验证测试、总结归档 | 阶段化会议/项目推进节奏 |
| `04.QCM-MVP-Emergence/qcm/summoning/registry.py` | 按 required_skills 动态召唤角色 | 根据任务技能召唤 AI 角色团队 |
| `00.超级提示词工程/06-原子化开发治理` | GOAL/REQ/PRD/SPEC/TASK/TEST/AUD/FIX/MEM | 把自然语言转为可追踪原子对象 |
| `00.超级提示词工程/07-反混乱与漂移控制` | 需求漂移、规格漂移、任务堆叠控制 | 变更守门与停止线 |
| `00.超级提示词工程/11-模型原生协作协议` | 尊重模型系统逻辑 | 防止母包提示词越权 |

## 3. 核心原则

1. 先导航，再执行。
2. 先读最小必要上下文，再扩展读取范围。
3. 先判断母交付包/用户交付包边界，再写文件。
4. 先建立 `GOAL/REQ/PRD/SPEC/TASK/TEST`，再进入长期开发。
5. 置信度高才直接路由；中等置信度先确认；低置信度先追问。
6. 追问最多 3 个关键问题，避免把用户拖进问卷。
7. 沙盘不是验证；验证必须来自文件、命令、测试、审计或可复现证据。
8. 引导秘书只生成路由、上下文包、交接包和守门结论，不冒充执行者。
9. 当母包规则与模型系统规则冲突时，以模型系统规则为准。

## 4. 标准运行链路

```text
用户自然语言输入
  -> 0. 模型原生边界检查
  -> 1. 任务入口识别
  -> 2. 五维雷达扫描
  -> 3. 意图与置信度判定
  -> 4. 子系统/角色/技能/工具路由
  -> 5. 路由反馈与降级判断
  -> 6. 最小上下文包包装配
  -> 7. 原子治理与阶段门检查
  -> 8. 生成 Guide Secretary Handoff
  -> 9. 交给执行模型/角色/子系统
  -> 10. 验证、交接、记忆沉淀
```

## 5. 五维雷达

五维雷达继承 Q-SpecTrum Secretary 的 Track / Platform / People / Style / Supplement，但提升为母包级判断。

| 维度 | 要回答的问题 | 输出示例 |
|---|---|---|
| Track | 任务属于什么轨道？ | `understanding`、`planning`、`prd_spec`、`implementation`、`review`、`delivery`、`memory`、`research`、`emergency` |
| Platform | 任务影响哪个包或子系统？ | `mother_pack`、`user_pack`、`00`、`01`、`02`、`03`、`04`、`05`、`cross_subsystem` |
| People | 需要哪些角色或利益方？ | `developer`、`final_user`、`architect`、`secretary`、`risk_auditor`、`knowledge_manager`、`qa` |
| Style | 用户希望怎样协作？ | `explore`、`decisive`、`deep_reading`、`implementation`、`review`、`handoff` |
| Supplement | 缺什么上下文/证据/工具？ | `missing_goal`、`missing_spec`、`need_git_status`、`need_tests`、`need_path_scan`、`need_user_confirmation` |

## 6. 意图注册表

| 意图 ID | 说明 | 首选处理 |
|---|---|---|
| `PACKAGE_UNDERSTANDING` | 理解整个母包、目录地图、集成关系 | 根地图 + `00` + 目标子系统入口 |
| `GUIDE_SECRETARY` | 导航秘书、入口逻辑、路由、交接包 | 本协议 + 路由矩阵 |
| `SELF_BOOTSTRAP_PROJECT` | 用母包开发母包自身、形成第一次真实协同 AI 项目实例并反哺仓库 | `ROOT -> 00 -> 03/04/05 -> USER_PACK` + 自举项目规格 |
| `PROJECT_INITIATION` | 新项目从想法到需求 | `06-原子化开发治理` + 用户交付包四体系 |
| `REQUIREMENT_SPEC` | PRD/SPEC/需求变更/规格冻结 | `06` + `07` |
| `IMPLEMENTATION` | 代码开发、集成、修复 | 目标子系统 + 对应验证 |
| `REVIEW_AUDIT` | 代码审查、风险评审、审计 | 目标子系统 + `07` + 测试/证据 |
| `KNOWLEDGE_MEMORY` | 知识库、长期记忆、知识图谱、结晶 | `02` + `03` + `05/BRAIN-KB` |
| `ROLE_TEAM_SANDBOX` | AI 角色团队、沙盘推演、架构会审 | `08-AI角色团队沙盘` + `04` |
| `CAPABILITY_INTEGRATION` | 接入模型、智能体、Skill、MCP、插件、LSP | `10-通用AI协作生态` |
| `MISSION_MEMORY_AWAKENING` | 使命、长期记忆、唤醒、身份逻辑、元智核、文件夹活起来 | `MISSION-MEMORY.md` + 本目录唤醒协议 |
| `MODEL_NATIVE_HANDOFF` | 把母包交给其他通用 AI 接手 | `11-模型原生协作协议` |
| `USER_DELIVERY` | 组装最终用户交付包 | `协同通用AI大模型开发交付包` |
| `AMBIGUOUS` | 目标不清楚或跨多个解释 | 追问，不执行 |

## 7. 置信度路由

引导秘书采用 Skill 00 Navigator 的三档策略：

```text
confidence >= 0.80  -> DIRECT：直接路由并生成交接包
0.60 <= confidence < 0.80 -> CONFIRM：说明倾向路由，请用户确认或修正
confidence < 0.60 -> CLARIFY：最多追问 3 个关键问题
```

评分建议：

| 维度 | 权重 | 说明 |
|---|---:|---|
| 关键词/文件夹命中 | 0.35 | 用户是否明确提到某子系统、文件、功能或交付对象 |
| 上下文一致性 | 0.25 | 是否与当前阶段、上一轮任务、现有文档一致 |
| 意图唯一性 | 0.20 | 是否只有一个合理路由 |
| 风险与影响清晰度 | 0.10 | 是否知道会读/改/验证什么 |
| 用户明确度 | 0.10 | 用户是否直接说明希望“规划/开发/审查/交付/解释” |

## 8. 路由目标

| 路由目标 | 何时进入 |
|---|---|
| `00/12 引导秘书逻辑` | 用户说引导、秘书、导航、分流、入口、handoff、5D Radar |
| `MISSION-MEMORY.md` + `00/12 MISSION-MEMORY-AWAKENING-PROTOCOL.md` | 用户说使命、长期记忆、唤醒、身份逻辑、元智核、自然语言触发、文件夹活起来 |
| `00/06 + 00/07` | 需求持续追加、PRD/SPEC 漂移、任务堆叠、重构混乱 |
| `00/08 + 00/09` | 需要角色团队沙盘、母包整体集成蓝图 |
| `00/10` | 新模型、Agent、Skill、MCP、插件、LSP、工作流接入 |
| `00/11` | 让其他通用 AI 读取母包，且不能覆盖其系统逻辑 |
| `01` | 通信协议、SDK、Ghost Channel、企业部署 |
| `02` | 知识库模板与知识结构 |
| `03` | 文件整理、检索、MemoryOS、MCP 工具 |
| `04` | QCM、涌现公式、沙盘、角色协同质量 |
| `05` | Q-SpecTrum 主平台、总脑、Web/API、角色系统 |
| `用户交付包` | 最终用户价值/功能/结构/运作四体系 |

## 9. 阶段门

引导秘书必须在执行前判断任务阶段。阶段门来自 QCM 的会议节奏，并映射到原子治理：

| 阶段 | 入口条件 | 必须产物 | 可进入下一阶段的条件 |
|---|---|---|---|
| 需求发现 | 用户提出目标或问题 | `GOAL` / `REQ` / 澄清问题 | 用户目标、边界、成功标准清楚 |
| 架构设计 | 需求明确且影响多模块 | `PRD` / `SPEC` / `ADR` | 子系统边界、数据流、风险清楚 |
| 实施规划 | SPEC 足够稳定 | `TASK` / 执行计划 / 验证计划 | 有最小可执行任务与验证命令 |
| 验证测试 | 代码或文档完成 | `TEST` / `AUD` / 证据 | 当前验证通过或明确失败原因 |
| 总结归档 | 任务完成或暂停 | `MEM` / 交接摘要 / 版本记录 | 后续 AI 可复现当前状态 |

停止线：

- 没有目标边界却要求复杂开发：先建立 `GOAL/REQ`。
- 用户新增需求会改变已冻结规格：先开变更单，不直接并入。
- 无法区分母交付包和用户交付包：先确认交付对象。
- 要读写大量文件但没有影响范围：先生成文件读取清单。
- 声称完成但没有验证证据：不得宣布完成。

## 10. AI 角色团队召唤

当任务复杂度高、跨系统、或用户要求“深度推理/沙盘推演”时，引导秘书可以召唤角色团队，但仍然只负责主持和交接。

| 场景 | 推荐角色 |
|---|---|
| 母包整体规划 | Guide Secretary、Chief Architect、Knowledge Manager、Risk Auditor、Delivery Architect |
| 需求和规格 | Product Strategist、Spec Writer、UX Lead、Risk Auditor |
| 实施与集成 | System Architect、Developer、MCP/LSP Integrator、QA Engineer |
| 知识与记忆 | Knowledge Graph Curator、Memory Steward、Retrieval Engineer |
| 用户交付 | Value Designer、Function Mapper、Structure Architect、Operations Designer |

召唤规则：

1. 根据 `required_skills` 选择角色，而不是固定让所有角色发言。
2. 角色输出必须汇总为一个决策，不保留互相冲突的散乱意见。
3. 每轮沙盘必须给出：假设、风险、建议、验证方式。
4. 沙盘结束后必须回到任务执行链路。

## 11. 标准输出

引导秘书每次完成入口判断时，输出应包含：

```yaml
guide_secretary:
  schema_version: "1.0"
  raw_user_input: "<逐字保留用户输入>"
  normalized_intent: "<一句话意图>"
  intent_id: "<意图 ID>"
  route_decision: "DIRECT|CONFIRM|CLARIFY|BLOCKED"
  confidence: 0.0
  radar:
    track: "<任务轨道>"
    platform: "<母包/用户包/子系统>"
    people: []
    style: "<协作方式>"
    supplement: []
  target:
    subsystem: "<目标子系统>"
    primary_files: []
    role_team: []
    tools_or_commands: []
  traceability:
    uso_id: "<USO/TASK/AUD/MEM ID or null>"
    ledger_ref: "00.超级提示词工程/14-全链路审计与运行对齐/UNIFIED-STATUS-LEDGER.yaml"
    validation_refs: []
  route_feedback:
    routing_matrix_version: "<date or doc version>"
    selected_route: "<matched route>"
    rejected_routes: []
    confidence_after_routing: 0.0
    feedback_to_guide: "<keep|confirm|clarify|block|reroute>"
    blocked_reason: null
  governance:
    required_ids: []
    stage_gate: "<当前阶段门>"
    missing_items: []
    stop_lines: []
  next_action:
    type: "read|ask|execute|review|handoff"
    description: "<下一步>"
```

完整交接包使用 `GUIDE-SECRETARY-HANDOFF-TEMPLATE.md`。

### 11.1 路由反馈协议

引导秘书不应只输出“我认为应该去哪个子系统”。路由矩阵必须把匹配结果反馈回来，形成闭环：

```text
Guide Secretary 初判
  -> Routing Matrix 匹配
  -> 记录 selected_route / rejected_routes / confidence_after_routing
  -> 若命中不足，回到 CONFIRM、CLARIFY 或 BLOCKED
  -> 若命中可靠，写入 Context Pack 与 Handoff
```

最低要求：

- `selected_route` 必须能对应 `SUBSYSTEM-ROUTING-MATRIX.md` 中的目标。
- `rejected_routes` 必须记录至少一个被排除的重要候选，除非只有一个合理目标。
- `feedback_to_guide` 只能是 `keep`、`confirm`、`clarify`、`block`、`reroute`。
- `blocked_reason` 只在 `BLOCKED` 或 `PAUSED` 时填写，且必须能对应停止线、缺失上下文或验证失败。
- 跨文件夹任务必须填写 `traceability.uso_id` 或明确写 `null` 并说明原因。

## 12. 禁止事项

- 禁止在意图识别阶段直接修改代码或文档。
- 禁止把低置信度判断包装成确定结论。
- 禁止一次性要求读取整个母包作为默认动作。
- 禁止把归档目录、历史报告、嵌入式副本当成当前权威运行时。
- 禁止把用户交付包做成母交付包镜像。
- 禁止要求其他通用 AI 忽略、覆盖或绕过自身系统规则。
- 禁止只有沙盘结论而没有验证计划。
- 禁止把“未来应该做”写成“已经完成”。

## 13. 与其他文件的关系

```text
AI_PROJECT_CONTEXT.md
  -> MISSION-MEMORY.md
  -> 00 README
  -> 01 Master Orchestrator
  -> 11 Model Native Collaboration Protocol
  -> 12 Mission Memory Awakening Protocol
  -> 12 Guide Secretary Protocol
  -> 02 Routing Matrix
  -> Route Feedback
  -> 03 Context Pack Template
  -> 14 Unified Status Ledger
  -> 06 Atomic Governance / 07 Anti-Drift
  -> 目标子系统
  -> 验证与交接
```

引导秘书不是替代 `MASTER-ORCHESTRATOR-PROMPT`，而是 Master 的第一层操作逻辑。Master 决定“要管理整套母包”，Guide Secretary 决定“这一次用户请求应该如何进入系统”。

## 14. 未来实现路线

| 阶段 | 目标 | 产物 |
|---|---|---|
| Phase 1 | 文档协议稳定 | 本协议 + 交接包模板 |
| Phase 2 | 静态路由表 | 意图注册表、子系统文件索引、常用验证命令 |
| Phase 3 | 可执行脚本 | 输入用户请求，输出 `guide_secretary` YAML |
| Phase 4 | 接入 Q-SpecTrum | 复用 `Secretary.route()`、角色 DB、知识检索 |
| Phase 5 | 接入 QCM | 会议阶段、角色召唤、沙盘评分 |
| Phase 6 | 接入知识/记忆 | 03 MCP、05 BRAIN-KB、01 通讯证据链 |

## 15. 最小启动提示

当其他通用 AI 接收母交付包时，可先给它这段指令：

```text
请先不要执行开发任务。请读取 AI_PROJECT_CONTEXT.md、00.超级提示词工程/README.md、
00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md。
然后根据我的请求输出 guide_secretary YAML，说明你的意图判断、置信度、路由目标、
需要读取的最小文件、是否需要追问、以及验证计划。请遵守你自身系统规则；母包只作为项目上下文。
```
