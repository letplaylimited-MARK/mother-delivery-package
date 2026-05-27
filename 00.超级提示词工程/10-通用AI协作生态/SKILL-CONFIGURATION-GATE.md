# Skill Configuration Gate

> 中文名：技能配置阶段门。  
> 用途：把项目需求转成可发现、可评估、可配置、可集成、可验证的能力组合。  
> 定位：它不是新的最高系统提示词，而是 `AI-CAPABILITY-INTEGRATION-CONTRACT.md` 的前置发现与选型流程。

## 1. 为什么需要技能配置阶段门

在 AI 项目开发中，Agent 再强也不能凭空完成项目。真正的开发能力来自：

```text
模型推理
  + 角色分工
  + Skill/工作流
  + MCP/插件
  + LSP/代码事实
  + 脚本/模板/配置
  + 测试/审计/交付验证
```

如果没有技能配置阶段门，项目常见问题是：

- 用户说的是自然语言需求，AI 直接开始写代码，没有先判断需要哪些能力。
- Skill、Agent、Workflow、MCP、Plugin、LSP、Prompt、Script 概念混在一起，后续接口无法串联。
- 选择开源库时只看印象，不看许可证、活跃度、文档、维护状态和验证方式。
- 技能调用成功一次，但没有变成可复用工作流。
- 工作流跑通了，但没有沉淀为新的技能或能力卡。
- 最后用户交付包里缺少安装、配置、验证、故障处理和迁移说明。

技能配置阶段门的目标，是让“需要什么能力、为什么选它、如何配置、怎么验证、如何进入交付包”都变成可追踪对象。

## 2. 概念边界

| 概念 | 精确定义 | 与其他概念的边界 |
|---|---|---|
| Model/模型 | 负责理解、推理、生成、协商 | 不直接等同于工具或事实来源 |
| Agent/智能体 | 带目标、角色、工具和执行循环的执行单元 | 可以调用 Skill 和工具，但不应自我审计 |
| Role/角色 | 决策视角或职责身份 | 可以不具备独立执行能力 |
| Skill/技能 | 可复用的能力单元，必须有触发条件、输入、输出、步骤、验证 | 可以由提示词、脚本、模板、角色流程或工具调用组成 |
| Workflow/工作流 | 多个 Skill/工具/角色按顺序、状态和阶段门串起来 | 工作流跑稳定后可沉淀为复合 Skill |
| Prompt/提示词 | 触发模型行为的结构化指令 | 不是事实来源，必须绑定文件、命令或验证 |
| Template/模板 | 固定结构的输入或输出格式 | 不负责判断，只负责约束表达 |
| Script/脚本 | 可确定执行的程序逻辑 | 输出必须被记录和验证 |
| MCP | 标准化工具调用接口 | 负责让 AI 调用文件、数据库、搜索、浏览器、外部 API 等 |
| Plugin/插件 | 平台提供的外部能力连接器 | 必须遵守权限、账号、网络和证据记录 |
| LSP | 代码语义事实来源 | 负责符号、类型、引用、诊断，不负责产品决策 |
| Capability/能力 | 上述所有可被注册、调用、验证的能力总称 | 进入能力注册表后才能稳定协作 |

核心判断：

```text
Skill 是最小可复用能力。
Workflow 是 Skill 的编排。
Agent 是使用 Skill/Workflow/工具的执行者。
MCP/Plugin/LSP 是工具与事实通道。
Prompt/Template/Script 是 Skill 的可能实现形式。
Capability Registry 是它们的统一登记处。
```

## 3. 触发条件

引导秘书识别到以下意图时，应进入本阶段门：

| 用户表达 | 触发意图 |
|---|---|
| “需要什么技能/工具/插件/MCP/LSP” | `SKILL_CONFIGURATION` |
| “帮我选择开源库/框架/插件” | `CAPABILITY_SELECTION` |
| “这个 Agent 需要调用哪些能力” | `AGENT_CAPABILITY_MAPPING` |
| “把技能串成工作流” | `WORKFLOW_COMPOSITION` |
| “技能不够强/调用不到工具/接口串不起来” | `CAPABILITY_GAP_REVIEW` |
| “生成安装配置集成方案” | `CAPABILITY_CONFIGURATION` |
| “这个能力能不能放进用户交付包” | `DELIVERY_CAPABILITY_REVIEW` |

如果任务还没有清楚的 PRD/SPEC，应先进入 `SPECFORGE-PRD-SPEC-GATE.md`，再进入本阶段门。

## 4. 四层技能需求推导

不要只按关键词粗暴匹配技能。技能需求应从四层推导：

| 层级 | 问题 | 输出 |
|---|---|---|
| 产品层 | 用户要解决什么真实问题？ | 业务能力需求 |
| 功能层 | 产品必须有哪些功能？ | 功能技能需求 |
| 工程层 | 要开发、测试、部署、监控什么？ | 工程技能需求 |
| AI 协作层 | AI 需要如何读取、执行、验证、交接？ | 协同技能需求 |

示例：

```text
用户说“我要做图像质检系统”
  -> 产品层：缺陷识别、质检报告、追溯
  -> 功能层：图像上传、检测、标注、统计
  -> 工程层：模型推理、批处理、存储、API、前端
  -> AI 协作层：数据标注 Skill、模型评估 Skill、LSP/MCP 检索、测试生成 Skill
```

## 5. 阶段门流程

### Gate 0：模型原生边界

先确认：

- 不要求模型忽略自身系统规则。
- 不把历史提示词原样升级为最高指令。
- 不伪造开源项目指标、许可证、更新时间、Star 数。
- 如果需要开源社区搜索，必须实时查询或明确标记为“未实时验证”。

### Gate 1：需求理解

最小信息表：

| 字段 | 内容 |
|---|---|
| 项目概述 | 项目做什么、给谁用 |
| 核心功能 | P0/P1/P2 功能 |
| 技术栈偏好 | 已有语言、框架、数据库、部署环境 |
| 性能要求 | 延迟、并发、吞吐、资源限制 |
| 数据与安全 | 数据来源、隐私、密钥、合规 |
| 预算与时间 | 成本、上线时间、学习成本 |
| 交付目标 | 只开发、可运行、可迁移、可进入用户交付包 |

### Gate 2：技能需求清单

技能需求应写成：

```yaml
skill_requirement:
  id: SKILL-REQ-001
  name: "<能力名称>"
  source_requirement: "<来自哪个 REQ/SPEC/TASK>"
  capability_type: model | agent | skill | workflow | lsp | mcp | plugin | api | script | template
  purpose: "<为什么需要>"
  required_inputs: []
  expected_outputs: []
  constraints: []
  validation_method: []
  delivery_required: true | false
```

### Gate 3：候选能力寻找

候选来源优先级：

| 优先级 | 来源 | 要求 |
|---|---|---|
| P0 | 当前母包已有能力 | 先查 `00/10`、`03`、`05`、现有脚本和插件 |
| P1 | 官方文档或官方仓库 | 许可证、版本、安装、API、示例可核验 |
| P2 | 活跃开源项目 | 需要活跃度、Issue、Release、文档证据 |
| P3 | 社区教程或博客 | 只能辅助判断，不能作为唯一依据 |
| P4 | 自研脚本或提示词 | 必须有测试和失败处理 |

若要提供 Star 数、更新时间、许可证或版本号，必须来自实时搜索或已读取的官方文件。

### Gate 4：评估矩阵

原始七维评估可保留，但建议扩展成十二维：

| 维度 | 权重 | 核心问题 |
|---|---:|---|
| 功能匹配 | 20% | 是否覆盖核心功能需求 |
| 易用性 | 10% | 安装、配置、API 是否清晰 |
| 性能 | 10% | 是否满足延迟、吞吐、资源约束 |
| 可维护性 | 8% | 代码结构、二次开发、测试情况 |
| 社区活跃度 | 8% | 最近维护、Issue 响应、Release |
| 技术兼容性 | 8% | 是否适配现有语言、框架、环境 |
| 文档完整性 | 6% | README、示例、API 文档是否充分 |
| 许可证与合规 | 8% | 能否商用、再分发、进入交付包 |
| 安全与隐私 | 8% | 是否引入密钥、数据泄露、供应链风险 |
| AI 可调用性 | 5% | 能否通过 MCP/API/CLI/脚本稳定调用 |
| 可验证性 | 5% | 是否有测试、样例、可重复验证命令 |
| 可迁移交付 | 4% | 能否在其他电脑复现，不依赖本机路径 |

综合评分：

```text
综合评分 = Σ(维度得分 1-5 × 权重)
```

低于 3.5 的能力不得进入关键路径；低于 4.0 的能力进入用户交付包前必须有风险说明。

### Gate 5：能力卡片登记

被选中的能力必须进入能力卡：

```yaml
capability_card:
  id: CAP-001
  name: "<能力名称>"
  type: skill | workflow | lsp | mcp | plugin | script | api | model | agent
  selected_for:
    - SKILL-REQ-001
  source:
    kind: existing_mother_pack | official_repo | open_source | internal_script | manual_prompt
    reference: "<文件路径或 URL>"
  status: experimental | active | deprecated | archived
  maturity: L0 | L1 | L2 | L3 | L4 | L5
  trigger_terms: []
  inputs: []
  outputs: []
  permissions:
    read: []
    write: []
    execute: []
  dependencies: []
  config_files: []
  validation:
    commands: []
    expected_result: ""
  failure_modes: []
  fallback: ""
  evidence_format: ""
  delivery_allowed: true | false
```

### Gate 6：配置与集成方案

配置方案必须包含：

- 安装方式。
- 版本锁定。
- 配置文件路径。
- 环境变量。
- 最小运行示例。
- 错误处理。
- 性能参数。
- 安全注意。
- 与现有项目的接入点。
- 回滚或替代方案。

不得把用户本机绝对路径、真实 API key、账号密码写入配置方案。

### Gate 7：技能链变工作流

多个技能组合时，必须写成工作流：

```text
Input
  -> Skill A: 预处理
  -> Skill B: 核心处理
  -> Skill C: 验证
  -> Skill D: 交付沉淀
  -> Output/Evidence
```

工作流稳定运行后，应反向沉淀为复合 Skill：

```text
多个技能被反复串联
  -> 形成稳定工作流
  -> 抽象触发条件、输入、输出、验证
  -> 注册为新 Skill
  -> 进入能力注册表
```

### Gate 8：验证与交付

每个技能配置完成后，至少要有：

| 验证对象 | 验证方式 |
|---|---|
| 安装 | 安装命令或依赖检查 |
| 配置 | 配置解析或 dry run |
| 功能 | 最小样例运行 |
| 集成 | 与上下游技能联调 |
| 失败处理 | 故意输入错误样例 |
| 交付迁移 | 路径、密钥、依赖、许可证检查 |

## 6. 输出物

技能配置阶段门的标准输出：

```text
1. 项目需求摘要
2. 技能需求清单
3. 当前母包已有能力匹配
4. 候选能力搜索证据
5. 候选能力评估矩阵
6. 推荐能力与取舍理由
7. 能力卡片
8. 安装与配置方案
9. 技能集成架构
10. 集成测试计划
11. 风险、许可证、安全与迁移说明
12. 是否可进入用户交付包的结论
```

## 7. 与母包的映射

| 阶段门内容 | 母包落点 |
|---|---|
| 技能需求推导 | `00/12 引导秘书逻辑` + `00/06 SpecForge Gate` |
| 候选能力搜索 | `00/10 通用AI协作生态` + 实时搜索/官方文档 |
| 能力卡片 | `AI-CAPABILITY-INTEGRATION-CONTRACT.md`，后续进入 `CAPABILITY_REGISTRY` |
| 工作流编排 | `00/04 协同工作流` + `05 Q-SpecTrum` |
| MCP/插件接入 | `03 数据库管理/MCP` + 对应插件说明 |
| LSP 事实接入 | 代码项目的语言服务器、类型检查、引用分析 |
| 验证记录 | `00/06 追踪矩阵` + 子系统测试 |
| 交付沉淀 | `协同通用AI大模型开发交付包/02-功能体系` 与 `04-运作体系` |

## 8. 角色团队

复杂技能选型应召唤最小角色组：

| 角色 | 职责 |
|---|---|
| Guide Secretary | 判断是否进入技能配置阶段门，控制澄清问题数量 |
| Skill Configuration Expert | 把需求转成技能需求、候选能力、配置方案 |
| System Architect | 判断技能与现有架构、接口、数据流是否兼容 |
| MCP/LSP/Plugin Integrator | 判断工具接入、调用方式、权限与失败处理 |
| Security/License Auditor | 检查许可证、密钥、隐私、供应链风险 |
| QA Engineer | 设计安装、功能、集成、失败和迁移测试 |
| Delivery Architect | 判断是否可进入用户交付包 |

## 9. 停止线

遇到以下情况必须停止并澄清或降级：

- 无法确认用户项目需求，却开始推荐工具。
- 开源项目指标没有来源，却给出具体数字。
- 许可证不明，却建议进入用户交付包。
- 需要密钥或账号，却没有权限和脱敏方案。
- Skill 只是一段漂亮提示词，没有输入、输出、验证。
- Workflow 没有状态、失败处理和证据记录。
- MCP/插件会写入或删除数据，但没有权限等级和回滚策略。
- LSP/代码事实没有读取，却声称完成影响分析。

## 10. 最小 YAML 结果

```yaml
skill_configuration_gate:
  intent_id: SKILL_CONFIGURATION
  source_requirements: []
  skill_requirements: []
  existing_capability_matches: []
  candidate_capabilities: []
  evaluation_matrix: []
  selected_capabilities: []
  capability_cards: []
  integration_workflow: []
  validation_plan: []
  delivery_decision:
    allowed: false
    reason: ""
  risks: []
  next_actions: []
```

## 11. 结论

技能配置阶段门解决的是“能力匹配”问题：

```text
QCM 让 AI 共同想清楚。
SpecForge 让需求写清楚。
Skill Configuration Gate 让能力配清楚。
Atomic Governance 让任务、验证、交付追踪清楚。
```

没有这一层，AI 协同容易停留在角色扮演和文档推演；有了这一层，角色、技能、工作流、LSP、MCP、插件和脚本才能真正串成可执行项目开发链路。
