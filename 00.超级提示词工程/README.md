# 超级提示词工程

> 定位：跨项目 AI 协同的提示词操作系统。  
> 目标：让任何通用 AI 大模型进入本交付包后，都能稳定理解、路由、调用、验证、交接所有子系统。

## 1. 核心结论

`00.超级提示词工程` 不应该只是“好用提示词合集”。它也不是为了取代通用 AI 大模型，更不能覆盖模型自身的系统逻辑。它应该成为所有项目文件夹之上的元控制层，让通用 AI 大模型可以稳定协同智能体、技能、工作流、LSP、MCP、插件、角色、知识库、测试、审计和交付系统：

```text
00.超级提示词工程
  -> 读取全局上下文
  -> 判断用户任务属于哪个子系统
  -> 装配最小必要上下文
  -> 生成需求/规格/任务/验证的原子 ID
  -> 对复杂任务启动角色团队沙盘
  -> 调用对应项目能力
  -> 产出可验证结果
  -> 做全链路审计与运行对齐
  -> 写回交接与记忆
```

它连接其他目录的方式：

| 子系统 | 在整体中的角色 | 由 00 提供什么 |
|---|---|---|
| `01.通讯协议_幽灵通道` | 通讯协议、SDK、企业部署 | 协议/SDK 集成提示词、交付审计提示词 |
| `02.通用知识库框架_Universal-KB` | 轻量知识库模板 | 知识摄取/查询/沉淀提示词 |
| `03.数据库管理_文件夹整理AI应用` | 可运行知识库与 MCP 工具层 | 文件治理、检索、整理、MCP 调用提示词 |
| `04.QCM-MVP-Emergence` | 协同公式、涌现评估、沙盘 | 共鸣评估、角色协作、QCM 推演提示词 |
| `05.超极智脑_Q-SpecTrum` | 主平台和总脑运行时 | 总控启动、角色路由、验证闭环提示词 |
| `协同通用AI大模型开发交付包` | 开发者完成项目后的最终用户交付包 | 价值/功能/结构/运作四体系装配提示词 |

## 2. 文件结构

```text
00.超级提示词工程/
├── README.md
├── 01-总控提示词/
│   └── MASTER-ORCHESTRATOR-PROMPT.md
├── 02-路由矩阵/
│   └── SUBSYSTEM-ROUTING-MATRIX.md
├── 03-上下文包模板/
│   └── AI-CONTEXT-PACK-TEMPLATE.md
├── 04-协同工作流/
│   └── CROSS-PROJECT-WORKFLOW.md
├── 05-评估与迭代/
│   └── PROMPT-EVALUATION-RUBRIC.md
├── 06-原子化开发治理/
│   ├── ATOMIC-AI-DEVELOPMENT-OPERATING-SYSTEM.md
│   ├── SPECFORGE-PRD-SPEC-GATE.md
│   └── TRACEABILITY-MATRIX-TEMPLATE.md
├── 07-反混乱与漂移控制/
│   └── ANTI-DRIFT-PROTOCOL.md
├── 08-AI角色团队沙盘/
│   ├── AI-ROLE-TEAM-SANDBOX.md
│   └── MOTHER-PACK-SANDBOX-REPLAY.md
├── 09-母包集成蓝图/
│   └── MOTHER-PACK-AI-COLLABORATION-BLUEPRINT.md
├── 10-通用AI协作生态/
│   ├── UNIVERSAL-AI-COLLABORATION-ECOSYSTEM.md
│   ├── AI-CAPABILITY-INTEGRATION-CONTRACT.md
│   └── SKILL-CONFIGURATION-GATE.md
├── 11-模型原生协作协议/
│   └── MODEL-NATIVE-COLLABORATION-PROTOCOL.md
├── 12-引导秘书逻辑/
│   ├── GUIDE-SECRETARY-PROTOCOL.md
│   ├── GUIDE-SECRETARY-HANDOFF-TEMPLATE.md
│   └── MISSION-MEMORY-AWAKENING-PROTOCOL.md
├── 13-源提示词吸收与演化/
    ├── SOURCE-PROMPT-INGESTION-PROTOCOL.md
    ├── QCM-V6.3.3-SUPER-PROMPT-DECONSTRUCTION.md
    ├── SPECFORGE-V2-SUPER-PROMPT-DECONSTRUCTION.md
    ├── SKILL-CONFIGURATION-EXPERT-V3-SUPER-PROMPT-DECONSTRUCTION.md
    ├── SUPER-PROMPT-ATOMIC-RESEARCH-REVIEW.md
    └── META-INTELLIGENCE-CORE-SUPER-PROMPT-DECONSTRUCTION.md
└── 14-全链路审计与运行对齐/
    ├── FULL-STACK-WORKFLOW-AUDIT-PROTOCOL.md
    ├── MOTHER-CHILD-WORKFLOW-MAP.md
    ├── AUDIT-COVERAGE-REGISTRY.md
    ├── WORKFLOW-AUDIT-ISSUE-LOG.md
    ├── BREAKPOINT-REPAIR-MATRIX.md
    ├── PROJECT_REGISTRY.yaml
    ├── CAPABILITY_REGISTRY.yaml
    ├── ARTIFACT_REGISTRY.yaml
    ├── VALIDATION_REGISTRY.yaml
    ├── MEMORY-SOURCE-PRIORITY.md
    ├── MEMORY-SOURCE-INDEX.yaml
    ├── UNIFIED-STATUS-OBJECT-SPEC.md
    └── UNIFIED-STATUS-LEDGER.yaml
```

## 3. 使用顺序

新 AI 或新会话进入时，按这个顺序：

1. 先读根目录 `MISSION-MEMORY.md`，确认母包使命、身份边界和唤醒握手。
2. 再读根目录 `AI_PROJECT_CONTEXT.md`。
3. 再读本目录 `README.md`。
4. 执行 `01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md` 的启动逻辑。
5. 读取 `11-模型原生协作协议/MODEL-NATIVE-COLLABORATION-PROTOCOL.md`，确认母包不覆盖模型自身系统逻辑。
6. 用 `12-引导秘书逻辑/MISSION-MEMORY-AWAKENING-PROTOCOL.md` 完成使命唤醒和自然语言触发判断。
7. 用 `12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md` 完成意图识别、置信度、澄清、路由和交接包判断。
8. 用 `02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md` 判断任务归属，并回写 `route_feedback`。
9. 用 `03-上下文包模板/AI-CONTEXT-PACK-TEMPLATE.md` 组装任务上下文，并绑定 `uso_id`、`ledger_ref`、`validation_refs`。
10. 按 `04-协同工作流/CROSS-PROJECT-WORKFLOW.md` 执行。
11. 用 `05-评估与迭代/PROMPT-EVALUATION-RUBRIC.md` 检查输出质量。
12. 若是持续开发、复杂需求或交付任务，加载 `06-原子化开发治理/ATOMIC-AI-DEVELOPMENT-OPERATING-SYSTEM.md`。
13. 若任务涉及新项目、PRD、SPEC、复杂功能、验收标准或需求变更，加载 `06-原子化开发治理/SPECFORGE-PRD-SPEC-GATE.md`。
14. 若出现需求漂移、规格漂移、任务堆叠、反复重构，加载 `07-反混乱与漂移控制/ANTI-DRIFT-PROTOCOL.md`。
15. 若涉及架构、跨系统、长期路线图或发布门，加载 `08-AI角色团队沙盘/AI-ROLE-TEAM-SANDBOX.md`。
16. 若目标是完善母交付包整体协同，加载 `09-母包集成蓝图/MOTHER-PACK-AI-COLLABORATION-BLUEPRINT.md`。
17. 若要接入新的模型、智能体、Skill、MCP、插件、LSP、工作流或外部系统，加载 `10-通用AI协作生态/AI-CAPABILITY-INTEGRATION-CONTRACT.md`。
18. 若要从项目需求推导技能、寻找开源能力、评估候选、生成安装配置和集成测试，加载 `10-通用AI协作生态/SKILL-CONFIGURATION-GATE.md`。
19. 若要吸收历史超级提示词、使用经验或失败案例，加载 `13-源提示词吸收与演化/SOURCE-PROMPT-INGESTION-PROTOCOL.md`，先做批判性转译，再决定是否进入运行协议。
20. 若要复核 QCM、SpecForge、技能配置专家、元智核之间的机制串联，加载 `13-源提示词吸收与演化/SUPER-PROMPT-ATOMIC-RESEARCH-REVIEW.md` 和 `13-源提示词吸收与演化/META-INTELLIGENCE-CORE-SUPER-PROMPT-DECONSTRUCTION.md`。
21. 若要审计每个文件夹的数据工作流、业务工作流、运行工作流、记忆工作流和交付工作流，加载 `14-全链路审计与运行对齐/FULL-STACK-WORKFLOW-AUDIT-PROTOCOL.md`，并同步维护 `MOTHER-CHILD-WORKFLOW-MAP.md`、`AUDIT-COVERAGE-REGISTRY.md`、`WORKFLOW-AUDIT-ISSUE-LOG.md`、`BREAKPOINT-REPAIR-MATRIX.md`、四个注册表、`MEMORY-SOURCE-PRIORITY.md`、`MEMORY-SOURCE-INDEX.yaml`、`UNIFIED-STATUS-OBJECT-SPEC.md` 和 `UNIFIED-STATUS-LEDGER.yaml`。

## 4. 设计原则

- 提示词必须绑定真实文件、真实命令、真实验证结果。
- 每个提示词必须声明适用场景、输入、输出、验证方式和失败处理。
- 不让 AI 靠聊天记忆协同；必须靠 context pack、registry、handoff、tests、logs 协同。
- 所有跨目录任务都必须先路由，再执行，避免把归档、副本、旧报告当成主运行时。
- `05.超极智脑_Q-SpecTrum` 是主集成层；`00` 是启动和提示词调度层。
- 涉及交付时，先区分“母交付包给开发者”和“用户交付包给最终用户”，再决定写入哪个目录。
- 涉及长期开发时，必须把自然语言意图转成可追踪的 `GOAL/REQ/PRD/SPEC/TASK/TEST/AUD/MEM`。
- 涉及 PRD/SPEC 时，必须经过 SpecForge Gate，把模糊描述锻造成可验证指标、范围边界、功能契约和验收标准。
- 涉及复杂任务时，必须先做角色团队沙盘，再执行。
- 涉及外部 AI 能力或工具接入时，必须先声明输入、输出、权限、失败处理、验证方式和证据格式。
- 涉及 Skill、MCP、插件、LSP、开源库或工作流选型时，必须经过技能配置阶段门，先判断母包已有能力，再做候选评估、能力卡、配置和集成测试。
- 涉及不同通用 AI 大模型接手时，必须尊重该模型自身系统规则；母包只提供项目上下文、协作契约和证据链。
- 涉及使命、长期记忆、唤醒、身份逻辑时，必须先读 `MISSION-MEMORY.md`，并通过 `MISSION-MEMORY-AWAKENING-PROTOCOL.md`；不得让 AI 假装永久人格或假装已加载记忆。
- 涉及任何新任务入口时，先经过引导秘书逻辑；引导秘书只做识别、澄清、路由、交接和守门，不在识别阶段直接执行任务。
- 涉及历史超级提示词时，必须先视为源材料；不得原样提升为系统规则，必须经过场景还原、机制提炼、风险审查和母包映射。
- 涉及“完整阅读、全链路审计、齿轮咬合、数据/业务/运行工作流对齐”时，必须进入 `14-全链路审计与运行对齐`；不得把愿景、旧报告或沙盘推断当成已经验证完成。

## 5. 最小闭环

真正可用的提示词工程必须满足这个闭环：

```text
意图识别 -> 子系统路由 -> 上下文装配 -> 任务执行 -> 验证 -> 交接 -> 记忆沉淀
```

缺任何一环，提示词都会退化成一次性话术，而不是长期协作能力。
