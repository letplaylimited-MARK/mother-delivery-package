# Full-Stack Workflow Audit Protocol

> 中文名：母包/子包全链路工作流审计协议。  
> 用途：审计每个文件夹的数据工作流、业务工作流、运行工作流、记忆工作流和交付工作流是否真正咬合。  
> 边界：本协议不声称一次阅读即可 100% 理解所有语义；它要求用文件、命令、日志、数据库、验证结果和交接记录逐层证明理解。

## 1. 为什么需要这一层

母交付包已经具备很多强能力：

- `00` 有总控、路由、引导秘书、SpecForge、技能配置、模型原生协作、使命唤醒。
- `01` 有 Ghost Channel 通讯/同步/审计/部署协议。
- `02` 有通用知识库模板。
- `03` 有可运行的 Flask + MCP + MemoryOS + 文件整理能力。
- `04` 有 QCM 公式、沙盘、飞轮、涌现验证。
- `05` 有 Q-SpecTrum 主平台、角色、DB、API、MCP、BRAIN-KB、handoff。
- `协同通用AI大模型开发交付包` 有最终用户四体系骨架。

真正风险不是“没有概念”，而是：

```text
概念存在
  但没有登记为可执行工作流
  但上下游输入输出没有对齐
  但验证命令没有绑定
  但记忆落点没有固定
  但交付边界没有锁住
  -> 最后 AI 只能靠聊天上下文硬串联，项目又会漂移和重构。
```

因此，任何跨文件夹任务都必须先进入本审计协议，至少完成“可复核基线”。

## 2. 审计对象定义

每个工作流都必须拆成一个对象：

```yaml
workflow_audit_item:
  id: "WFA-YYYYMMDD-001"
  subsystem: "00|01|02|03|04|05|USER-PACK|ROOT"
  workflow_type: "data|business|runtime|memory|delivery|verification|security"
  source_files:
    - "<相对路径>"
  current_state: "fact|inference|unknown"
  trigger:
    natural_language:
      - "<用户自然表达>"
    explicit_command:
      - "<命令或脚本>"
  input:
    artifacts:
      - "<输入文件/数据库/API/用户话语>"
    required_context:
      - "<必须先读的文件>"
  process:
    steps:
      - "<步骤>"
    owner_layer: "<00/03/05/子系统>"
  output:
    artifacts:
      - "<输出文件/结果/API响应/日志>"
    handoff:
      - "<交接位置>"
  memory:
    read_from:
      - "<BRAIN-KB/_HANDOFF/MemoryOS/DB/Context Pack>"
    write_to:
      - "<真实文件或数据库>"
    write_gate: "P0|P1|P2|none"
  validation:
    commands:
      - "<可运行命令>"
    manual_checks:
      - "<人工验收>"
    evidence_required:
      - "<输出证据>"
  downstream:
    - "<下游工作流或交付物>"
  risks:
    - "<风险>"
  gaps:
    - "<缺口>"
  next_action:
    - "<下一步>"
```

## 3. 七层审计面

| 层 | 审计面 | 必须回答的问题 | 主要证据 |
|---|---|---|---|
| L0 | 使命与边界 | AI 是否理解母包/子包边界、模型原生边界、真实记忆边界？ | `MISSION-MEMORY.md`, `AI_PROJECT_CONTEXT.md`, `00/11`, `00/12` |
| L1 | 入口与路由 | 自然语言如何进入正确阶段门？ | `MASTER`, `ROUTING`, `GUIDE-SECRETARY` |
| L2 | 数据工作流 | 数据从哪里来、被谁处理、存到哪里？ | DB、jsonl、README、API、MCP server |
| L3 | 业务工作流 | 用户想法如何变成 PRD/SPEC/TASK/TEST/交付？ | `00/06`, `00/09`, 子包四体系 |
| L4 | 运行工作流 | 哪些命令真正能启动、验证、部署？ | `VERIFY.ps1`, `verify_install.py`, `run.py`, `verify-integration.py` |
| L5 | 记忆与交接 | 什么进入长期记忆，谁读取，怎么防幻觉？ | `BRAIN-KB`, `_HANDOFF`, MemoryOS, context pack |
| L6 | 能力与工具 | Skill/MCP/LSP/插件/脚本如何登记、调用、退出？ | `00/10`, `03/mcp_server.py`, `05/qspectrum_mcp_server.py` |
| L7 | 交付与迁移 | 开发者如何从母包生成用户交付包？ | `开发者母交付包使用说明.md`, 子包 README, `交付包组装规则.md` |

## 4. 审计证据等级

| 等级 | 含义 | 可以怎么说 | 不能怎么说 |
|---|---|---|---|
| FACT | 已读到文件、命令、数据库、测试结果 | “文件 X 声明 Y；命令 Z 通过” | “应该没问题” |
| VERIFIED | 当前会话实际运行并通过 | “刚运行 Z，结果为 PASS” | “以前通过所以现在通过” |
| INFERENCE | 基于证据的推断 | “从 A/B 推断该工作流目标是...” | “系统已经完整自动运行” |
| GAP | 证据链缺失或接口未登记 | “缺少能力注册表” | “未来会自然补上” |
| RISK | 可能导致漂移、误调用、不可交付 | “文档与代码入口不一致” | “只是小问题不用管” |

## 5. 最小审计流程

```text
1. 读取 MISSION-MEMORY.md 与 AI_PROJECT_CONTEXT.md
2. 扫描文件清单、类型、入口、数据库、jsonl、验证脚本
3. 读取每个子系统 README / INDEX / AGENTS / HANDOFF / PROTOCOL
4. 提取数据流、业务流、运行流、记忆流、交付流
5. 标注 FACT / VERIFIED / INFERENCE / GAP / RISK
6. 生成母包/子包齿轮咬合图
7. 更新覆盖登记表
8. 运行最小验证命令
9. 把结论写入交接或长期记忆候选
```

## 6. 强制停止线

遇到以下情况必须停下来标注风险：

- AI 声称“已完整理解所有文件”，但没有文件清单、阅读范围和验证证据。
- AI 声称“长期记忆已加载”，但没有读取真实记忆文件、数据库或 handoff。
- AI 声称“系统已经运行”，但没有运行命令或服务状态证据。
- 某工作流跨多个目录，但没有最小上下文包和回写位置。
- 能力/插件/MCP/LSP 被调用，但没有能力卡、权限、输入输出、失败处理和验证。
- 用户交付包混入母包研究资料、旧报告、本机路径、密钥或未验证能力。

## 7. 与其他协议的关系

```text
MISSION-MEMORY
  -> 定义使命、边界、唤醒
  -> 本协议审计它是否被入口和路由真实引用

GUIDE-SECRETARY
  -> 做自然语言识别和路由
  -> 本协议审计路由之后是否有真实上下文、执行、验证、交接

SpecForge / Atomic Governance
  -> 管 PRD/SPEC/TASK/TEST
  -> 本协议审计需求到验证是否闭环

Skill Configuration Gate
  -> 管 Skill/MCP/LSP/插件接入
  -> 本协议审计能力是否登记、可调用、可退出

Q-SpecTrum / MemoryOS / BRAIN-KB
  -> 承载运行时、记忆和平台能力
  -> 本协议审计记忆读写与运行证据
```

## 8. 审计输出物

本协议至少产生以下文档和注册表：

1. `MOTHER-CHILD-WORKFLOW-MAP.md`：母包/子包齿轮咬合图。
2. `AUDIT-COVERAGE-REGISTRY.md`：当前审计覆盖范围、证据和缺口。
3. `PROJECT_REGISTRY.yaml`：项目/子系统状态。
4. `CAPABILITY_REGISTRY.yaml`：能力、工具、Skill、MCP、LSP、插件。
5. `ARTIFACT_REGISTRY.yaml`：关键文档、代码、DB、交付物。
6. `VALIDATION_REGISTRY.yaml`：验证命令、证据与状态。
7. `MEMORY-SOURCE-PRIORITY.md`：多记忆源读写与冲突解决规则。
8. `MEMORY-SOURCE-INDEX.yaml`：多记忆源的机器可读权威范围、查询入口、写入目标、冲突 owner 和副作用。
9. `BREAKPOINT-REPAIR-MATRIX.md`：显式/隐蔽断裂点、修复动作和后续验证清单。
10. `UNIFIED-STATUS-OBJECT-SPEC.md`：跨文件夹任务的统一状态对象规范。
11. `UNIFIED-STATUS-LEDGER.yaml`：当前跨文件夹任务和审计修复状态账本。

## 9. 结论

本协议的目的不是让母包更“宏大”，而是让每个宏大概念最终都能落到：

```text
可定位的文件
可解释的工作流
可运行的命令
可复核的证据
可交接的记忆
可迁移的用户交付包
```
