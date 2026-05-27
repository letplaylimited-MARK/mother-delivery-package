# Unified Status Object Spec

> 中文名：统一状态对象规范。  
> 用途：把自然语言任务、需求、规格、执行、验证、审计、记忆和交付压缩成同一种可追踪对象，避免 AI 只靠聊天上下文串联。  
> 状态：v0.1，先以 Markdown/YAML 落地；后续可映射到 Ghost Channel、03 MCP、05 DB 或 QCM 沙盘。

## 1. 为什么必须有统一状态对象

上一轮审计确认：母包已经有使命唤醒、引导秘书、路由矩阵、SpecForge、Skill Gate、QCM、Q-SpecTrum、MemoryOS、MCP、用户交付包四体系。

真正会卡住的地方不是“没有模块”，而是：

```text
用户自然语言
  -> 被多个协议解释
  -> 进入多个文件夹
  -> 产生多个文档/命令/记忆
  -> 但没有同一种状态对象串起来
  -> 后续 AI 不知道当前任务、证据、风险、验证和下一步
```

统一状态对象就是母包的最小“任务事实单元”。任何长期协同任务，至少要能落成一个对象。

## 2. 对象类型

| 类型 | 用途 | 典型来源 | 典型下游 |
|---|---|---|---|
| `goal` | 用户或项目的目标 | 原始对话、MISSION-MEMORY | requirement/spec |
| `requirement` | 可追踪需求 | SpecForge、用户确认 | spec/task/test |
| `spec` | 可实现规格 | PRD/SPEC Gate | task/test |
| `plan` | 执行计划 | 引导秘书、角色沙盘 | task |
| `task` | 可执行任务 | 计划、修复项 | code/doc/config |
| `validation` | 验证记录 | 命令、测试、人工验收 | audit/delivery |
| `audit` | 审计发现 | 全链路审计、代码审查 | fix/task |
| `handoff` | 交接记录 | 任务结束、模型切换 | future_ai |
| `memory` | 长期记忆候选 | 决策、模式、限制 | BRAIN-KB/MemoryOS |
| `delivery` | 用户交付物状态 | 子包组装 | final_user |

## 3. YAML Schema

```yaml
unified_status_object:
  schema_version: "0.1"
  id: "USO-YYYYMMDD-001"
  type: "goal|requirement|spec|plan|task|validation|audit|handoff|memory|delivery"
  title: "<短标题>"
  status: "draft|active|paused|blocked|validated|closed|superseded"
  priority: "P0|P1|P2|P3"
  package_boundary: "mother_pack|user_pack|subsystem|cross"
  owner_layer: "ROOT|00|01|02|03|04|05|USER_PACK"

  source:
    raw_user_input_ref: "<原始用户输入摘要或文件位置>"
    source_files:
      - path: "<相对路径>"
        role: "authority|context|evidence|historical"
        locator: "<章节/行号/命令输出摘要>"
    source_type: "user|file|command|database|subagent|inference"

  routing:
    guide_secretary_handoff_id: "<GSH-id|null>"
    intent_id: "<intent|null>"
    route_decision: "DIRECT|CONFIRM|CLARIFY|BLOCKED|null"
    target_subsystems:
      - "00|01|02|03|04|05|USER_PACK"
    route_feedback:
      selected_route: "<route|null>"
      rejected_routes:
        - "<route and reason>"
      confidence_after_routing: 0.0
      feedback_to_guide: "keep|confirm|clarify|block|reroute|null"
      blocked_reason: "<reason|null>"

  traceability:
    goal_id: "<GOAL-id|null>"
    parent_id: "<parent USO id|null>"
    related_ids:
      - "<USO/WAI/VAL/ART/CAP id>"
    atomic_ids:
      - "<GOAL|REQ|PRD|SPEC|TASK|TEST|AUD|MEM id>"

  workflow:
    trigger:
      natural_language:
        - "<触发词或表达>"
      explicit_command:
        - "<命令|null>"
    input_artifacts:
      - "<输入文件/DB/API/上下文>"
    process_steps:
      - "<步骤>"
    output_artifacts:
      - "<输出文件/DB/API/报告>"
    downstream:
      - "<下游对象或交付物>"

  execution:
    cwd: "<相对 cwd 或 null>"
    commands:
      - command: "<命令>"
        writes_files: false
        expected_result: "<预期>"
        current_result: "<当前证据或 null>"
    permissions:
      read: true
      write_docs: false
      write_code: false
      execute: false
    rollback:
      strategy: "<回退方式或 null>"

  evidence:
    level: "FACT|VERIFIED|INFERENCE|GAP|RISK"
    items:
      - kind: "file|command|database|test|manual|subagent"
        ref: "<路径、命令或来源>"
        summary: "<证据摘要>"

  validation:
    validation_refs:
      - "<VAL-id>"
    required_before_close:
      - "<必须完成的验证>"
    current_status: "not_run|verified_current|verified_previous|verified_with_findings|needs_review|failed"

  memory:
    read_from:
      - "<真实记忆源>"
    write_needed: false
    write_target: "<MISSION-MEMORY|AI_PROJECT_CONTEXT|00/14|05/BRAIN-KB|05/_HANDOFF|03-memory|USER_PACK|null>"
    write_gate: "P0|P1|P2|none"

  risks:
    - id: "<WAI/RISK id>"
      summary: "<风险>"
      mitigation: "<缓解>"

  next_action:
    - "<下一步>"

  timestamps:
    created_at: "<YYYY-MM-DD>"
    updated_at: "<YYYY-MM-DD>"
```

## 4. 生命周期

```text
draft
  -> active
  -> paused
  -> active
  -> validated
  -> closed
```

允许的异常状态：

- `blocked`：缺少用户确认、文件、权限、依赖或验证。
- `paused`：主动暂停，等待用户确认、范围裁决、验证结果或依赖恢复。
- `superseded`：被新的对象替代，但保留历史。
- `validated_with_findings` 不作为对象状态使用；它应写在 `validation.current_status` 中。

## 5. 与现有文件的关系

| 现有文件 | 与统一状态对象的关系 |
|---|---|
| `MISSION-MEMORY.md` | 给对象提供使命、边界、停止线 |
| `AI_PROJECT_CONTEXT.md` | 提供全局地图和子系统状态 |
| `GUIDE-SECRETARY-HANDOFF-TEMPLATE.md` | 负责把自然语言入口转换为交接包 |
| `PROJECT_REGISTRY.yaml` | 告诉对象可路由到哪些子系统 |
| `CAPABILITY_REGISTRY.yaml` | 告诉对象可调用哪些能力 |
| `ARTIFACT_REGISTRY.yaml` | 告诉对象可引用哪些文档/代码/数据 |
| `VALIDATION_REGISTRY.yaml` | 告诉对象必须如何验证 |
| `BREAKPOINT-REPAIR-MATRIX.md` | 提供显式/隐蔽断裂点与修复状态 |
| `MEMORY-SOURCE-INDEX.yaml` | 提供真实记忆源优先级、写入目标和冲突 owner |
| `WORKFLOW-AUDIT-ISSUE-LOG.md` | 提供对象关联的审计问题 |
| `UNIFIED-STATUS-LEDGER.yaml` | 保存当前对象账本 |

## 6. 强制规则

1. 任何跨文件夹任务必须至少产生一个 `task` 或 `audit` 对象。
2. 任何“已完成”必须有 `validation.current_status` 和证据。
3. 任何“长期记忆”必须填写 `memory.write_target` 和 `write_gate`。
4. 任何“用户交付完成”必须引用用户交付包 Strict 验证结果。
5. 沙盘/QCM 输出只能作为 `INFERENCE` 或 `RISK`，不能直接作为 `VERIFIED`。
6. 历史报告只能作为 `context` 或 `historical`，不能覆盖当前命令输出。
7. 没有来源的自然语言结论不能进入 `closed`。

## 7. 最小对象示例

```yaml
unified_status_object:
  schema_version: "0.1"
  id: "AUD-20260526-MOTHER-PACK-WORKFLOW"
  type: "audit"
  title: "母包/子包全链路工作流审计"
  status: "active"
  priority: "P0"
  package_boundary: "mother_pack"
  owner_layer: "00"
  source:
    raw_user_input_ref: "用户要求严谨审计所有文件夹数据/业务/运行工作流"
    source_files:
      - path: "MISSION-MEMORY.md"
        role: "authority"
        locator: "母包使命与边界"
      - path: "00.超级提示词工程/14-全链路审计与运行对齐/FULL-STACK-WORKFLOW-AUDIT-PROTOCOL.md"
        role: "authority"
        locator: "审计对象定义"
    source_type: "user"
  evidence:
    level: "VERIFIED"
    items:
      - kind: "command"
        ref: "PowerShell file baseline"
        summary: "1118 stable files, excluding runtime caches"
  validation:
    validation_refs: ["VAL-ROOT-FILE-COUNT", "VAL-ROOT-HARDCODE-PATH"]
    required_before_close:
      - "逐项关闭 P0/P1 工作流审计问题"
    current_status: "verified_with_findings"
  next_action:
    - "把注册表升级为可调度账本"
```
