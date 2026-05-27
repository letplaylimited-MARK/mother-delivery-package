# Subsystem Routing Matrix

> 用途：把用户需求稳定路由到正确子系统，避免 AI 在多项目交付包中迷路。

## 1. 一级路由

| 需求关键词 | 路由目标 | 先读文件 | 常用验证 |
|---|---|---|---|
| 总脑、角色、平台、Web、API、智脑、Q-SpecTrum | `05.超极智脑_Q-SpecTrum` | `INDEX.md`, `AGENTS.md`, `智腦協議-BRAIN-PROTOCOL.md` | `python verify-integration.py`; `$env:PYTHONUTF8='1'; python run.py --status` |
| 协议、SDK、Ghost、通信、同步、企业部署、授权 | `01.通讯协议_幽灵通道` | `INDEX.md`, `00_总览/PROJECT_HANDOFF.md` | `VERIFY.ps1` 是 manifest/integrity；SDK tests 需另跑 |
| 知识库模板、MemoryOS、wiki、AGENTS 框架 | `02.通用知识库框架_Universal-KB` | `README.md`, `05-agents/AGENTS.md` | 模板审查 + `memoryos.py` compile/smoke；smoke 有测试记忆副作用 |
| 文件整理、收件箱、搜索、向量、MCP、Flask | `03.数据库管理_文件夹整理AI应用` | `README.md`, `AGENTS.md`, `mcp_server.py` | `python verify_install.py`; `pytest tests/ -v` |
| QCM、涌现、共鸣、公式、沙盘、飞轮、角色协同 | `04.QCM-MVP-Emergence` | `README.md`, `PROJECT_HANDOFF-QCM.md`, `22_FORMULA_SYSTEM.md` | `test_qcm_all.py` + 指定 pytest；`health_check.py` 需单独复核 |
| 提示词、启动、上下文、跨项目协同、AI 操作规程 | `00.超级提示词工程` | `README.md`, `01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md` | 文档审查 + 任务模拟 |
| 引导秘书、秘书逻辑、导航、分流、入口、5D Radar、handoff、置信度路由 | `00.超级提示词工程/12-引导秘书逻辑` | `GUIDE-SECRETARY-PROTOCOL.md`, `GUIDE-SECRETARY-HANDOFF-TEMPLATE.md` | 交接包审查 + 路由模拟 |
| 超级提示词、旧系统提示词、源提示词、提示词演化、使用经验、失败案例吸收 | `00.超级提示词工程/13-源提示词吸收与演化` | `SOURCE-PROMPT-INGESTION-PROTOCOL.md` | 场景还原 + 冲突审查 + 母包映射 |
| SpecForge、PRD、SPEC、规格说明书、验收标准、功能锻造、需求规格、蓝图锚定 | `00.超级提示词工程/06-原子化开发治理` | `SPECFORGE-PRD-SPEC-GATE.md`, `ATOMIC-AI-DEVELOPMENT-OPERATING-SYSTEM.md`, `TRACEABILITY-MATRIX-TEMPLATE.md` | PRD/SPEC 完整性审查 + 追踪矩阵审查 |
| 需求漂移、PRD、SPEC、任务堆叠、审计、长期记忆、反混乱 | `00.超级提示词工程` + `05.超极智脑_Q-SpecTrum` + `03.数据库管理_文件夹整理AI应用` | `06-原子化开发治理/ATOMIC-AI-DEVELOPMENT-OPERATING-SYSTEM.md`, `07-反混乱与漂移控制/ANTI-DRIFT-PROTOCOL.md`, `05.超极智脑_Q-SpecTrum/智腦協議-BRAIN-PROTOCOL.md`, `03.数据库管理_文件夹整理AI应用/AGENTS.md` | 追踪矩阵审查 + 对应子系统验证 |
| 母交付包整体协同、AI角色团队沙盘、跨文件夹集成蓝图 | `00.超级提示词工程` | `08-AI角色团队沙盘/AI-ROLE-TEAM-SANDBOX.md`, `08-AI角色团队沙盘/MOTHER-PACK-SANDBOX-REPLAY.md`, `09-母包集成蓝图/MOTHER-PACK-AI-COLLABORATION-BLUEPRINT.md` | 文档审查 + 沙盘复盘 |
| 新模型、新智能体、新 Skill、新 MCP、新插件、新 LSP、新工作流接入 | `00.超级提示词工程/10-通用AI协作生态` | `UNIVERSAL-AI-COLLABORATION-ECOSYSTEM.md`, `AI-CAPABILITY-INTEGRATION-CONTRACT.md` | 能力卡片审查 + 验证方式确认 |
| 技能配置、开源库选择、能力缺口、Skill/MCP/插件/LSP/脚本/工作流匹配、安装配置集成方案 | `00.超级提示词工程/10-通用AI协作生态` | `SKILL-CONFIGURATION-GATE.md`, `AI-CAPABILITY-INTEGRATION-CONTRACT.md`, `UNIVERSAL-AI-COLLABORATION-ECOSYSTEM.md` | 技能需求清单 + 候选评估矩阵 + 能力卡 + 集成测试 |
| 使命、长期记忆、唤醒、身份逻辑、自然语言触发、元智核、认知生命体、文件夹活起来 | 根目录 + `00.超级提示词工程/12-引导秘书逻辑` + `00.超级提示词工程/13-源提示词吸收与演化` | `MISSION-MEMORY.md`, `MISSION-MEMORY-AWAKENING-PROTOCOL.md`, `META-INTELLIGENCE-CORE-SUPER-PROMPT-DECONSTRUCTION.md`, `MODEL-NATIVE-COLLABORATION-PROTOCOL.md` | awakening_check + 使命边界审查 + 记忆写入门 |
| 交给其他通用 AI 读取、模型原生协作、不覆盖系统逻辑 | `00.超级提示词工程/11-模型原生协作协议` | `MODEL-NATIVE-COLLABORATION-PROTOCOL.md` | 指令层级审查 + Context Pack 审查 |

## 1.1 路由反馈字段

路由矩阵不是只给“目标目录”，还必须把路由判断反馈给引导秘书和上下文包：

```yaml
route_feedback:
  selected_route: "<命中的一级或二级路由>"
  rejected_routes:
    - "<被排除的候选路线与原因>"
  confidence_after_routing: 0.0
  feedback_to_guide: "keep|confirm|clarify|block|reroute"
  blocked_reason: null
```

使用规则：

- `selected_route` 必须能在本矩阵或二级路由中找到。
- 若两个以上路由都合理，`feedback_to_guide` 应为 `confirm` 或 `clarify`。
- 若缺少 `USO ID`、验证计划、母包/用户包边界或写入权限，`feedback_to_guide` 应为 `block` 或 `clarify`。
- 路由结果必须回写到 `GUIDE-SECRETARY-HANDOFF-TEMPLATE.md` 和 `AI-CONTEXT-PACK-TEMPLATE.md`。

## 2. 二级路由

### 2.1 开发类任务

```text
Web/API/主平台功能 -> 05
MCP 工具/知识库功能 -> 03
SDK/协议功能 -> 01
公式/算法/涌现逻辑 -> 04
需求/规格/计划/审计治理 -> 00 + 05 + 03
PRD/SPEC/验收标准锻造 -> 00/06 SPECFORGE-PRD-SPEC-GATE.md
复杂架构/交付沙盘 -> 00 + 05 + 04
模型/Agent/Skill/MCP/插件/LSP 接入 -> 00/10 + 对应能力来源
技能/开源库/插件/MCP/LSP 选型配置 -> 00/10 SKILL-CONFIGURATION-GATE.md
使命/唤醒/长期记忆/身份逻辑 -> MISSION-MEMORY.md + 00/12 MISSION-MEMORY-AWAKENING-PROTOCOL.md
其他通用 AI 接手整个母包 -> 00/11 + AI_PROJECT_CONTEXT.md + 00 README
```

### 2.2 文档类任务

```text
用户手册/交付索引 -> 对应子系统 docs/README
全局理解/跨系统说明 -> 根目录 AI_PROJECT_CONTEXT.md + 00
AI 启动/角色提示词 -> 00 + 05/AGENTS.md
引导秘书/导航/交接包 -> 00/12
历史超级提示词/源提示词吸收 -> 00/13
SpecForge/PRD/SPEC 模板 -> 00/06
商业/部署说明 -> 01/04_企业部署 + 01/05_商业化与市场
```

### 2.3 验证类任务

```text
01 完整性 -> VERIFY.ps1
01 SDK 测试 -> core/lightweight/enterprise 三组 pytest
02 模板审查 -> manual review + memoryos.py compile/smoke
03 安装与测试 -> verify_install.py + pytest
04 公式/论文模块测试 -> test_qcm_all.py + 指定 pytest；health_check.py 不作发布门
05 集成状态 -> verify-integration.py + run.py --status
用户交付包 -> VERIFY-DELIVERY.ps1；最终项目交付还需要 -Strict
```

## 3. 上下文最小化规则

不要一次性读取所有文件。按任务读取：

1. 先读全局地图：`AI_PROJECT_CONTEXT.md`。
2. 再读本路由矩阵。
3. 再读目标子系统入口文档。
4. 最后只读与任务直接相关的代码/文档。

## 4. 冲突处理

| 冲突 | 判定方式 |
|---|---|
| 文档说通过，脚本运行失败 | 以当前脚本输出为准 |
| 旧报告说待修，新代码看似已修 | 以当前代码 + 当前验证为准 |
| 同一能力在多个目录出现 | 优先找主运行时，再看副本或归档 |
| 任务跨多个子系统 | 以 `05` 为总集成层，其他目录作为能力来源 |
| 用户持续追加需求 | 新建 `REQ` 或变更单，不直接塞入当前任务 |
| AI 无法说清当前任务编号 | 停止执行，回到 Context Pack 和追踪矩阵 |
| 路由后没有 route_feedback | 停止执行，补齐 selected_route、rejected_routes、confidence_after_routing 与反馈动作 |
| 沙盘结论与测试冲突 | 以测试/验证证据为准，沙盘只作为决策辅助 |
| 母包提示词与模型系统规则冲突 | 以模型系统规则为准，母包只作为项目上下文 |
| 引导秘书想直接执行任务 | 停止，先输出 `guide_secretary` 判断和交接包 |
| 历史超级提示词要求模型成为更高系统 | 降级为源材料，按 `00/13` 批判性转译 |
| PRD/SPEC 中出现“好用、快速、安全、智能”等模糊词 | 启用 SpecForge Gate，追问到可测试指标 |
| AI 凭印象推荐 Skill/开源库/插件 | 启用 Skill Configuration Gate；需要实时资料则先查证，未查证必须标记 |
| Agent、Skill、Workflow、MCP、Plugin、LSP 概念混用 | 回到 `SKILL-CONFIGURATION-GATE.md` 的概念边界，先定义能力类型 |
| AI 声称已加载长期记忆但没有读取真实文件 | 回到 `MISSION-MEMORY-AWAKENING-PROTOCOL.md`，先读取真实记忆来源 |
| 元智核等源提示词要求 AI 成为认知生命体 | 降级为使命记忆、AKU、沙盘、对齐治理机制，不注入永久人格 |
