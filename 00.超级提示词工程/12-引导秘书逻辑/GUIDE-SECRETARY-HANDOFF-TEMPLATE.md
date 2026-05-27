# Guide Secretary Handoff Template

> 用途：引导秘书完成入口判断后，把任务交给具体 AI 模型、角色、Skill、MCP、插件、LSP 或子系统执行。  
> 原则：交接包必须保留用户原话、说明置信度、列出最小文件、定义验证方式。

## 1. 完整模板

```yaml
guide_secretary_handoff:
  schema_version: "1.0"
  handoff_id: "GSH-YYYYMMDD-001"
  created_at: "<ISO8601>"

  source:
    raw_user_input: |
      <逐字保留用户输入>
    conversation_context: |
      <只写与当前任务直接相关的上下文，不复制整段聊天>

  intent:
    normalized_intent: "<一句话意图>"
    intent_id: "<PACKAGE_UNDERSTANDING|GUIDE_SECRETARY|PROJECT_INITIATION|...>"
    confidence: 0.0
    route_decision: "DIRECT|CONFIRM|CLARIFY|BLOCKED"
    route_reason: |
      <1-3 句解释为什么这样路由>
    ambiguity_flags: []

  traceability:
    uso_id: "<USO/TASK/AUD/MEM ID or null>"
    ledger_ref: "00.超级提示词工程/14-全链路审计与运行对齐/UNIFIED-STATUS-LEDGER.yaml"
    validation_refs:
      - "<VAL-xxx or null>"

  route_feedback:
    routing_matrix_version: "<date or doc version>"
    selected_route: "<matched route from SUBSYSTEM-ROUTING-MATRIX.md>"
    rejected_routes:
      - "<candidate route rejected and why>"
    confidence_after_routing: 0.0
    feedback_to_guide: "<keep|confirm|clarify|block|reroute>"
    blocked_reason: null

  radar:
    track: "<understanding|planning|prd_spec|implementation|review|delivery|memory|research|emergency>"
    platform: "<mother_pack|user_pack|00|01|02|03|04|05|cross_subsystem>"
    people:
      - "<developer|final_user|architect|secretary|risk_auditor|knowledge_manager|qa>"
    style: "<explore|decisive|deep_reading|implementation|review|handoff>"
    supplement:
      - "<missing_goal|missing_spec|need_git_status|need_tests|need_path_scan|need_user_confirmation>"

  target:
    subsystem: "<目标子系统或目录>"
    entry_files:
      - "<必须先读的文件>"
    optional_files:
      - "<需要时再读的文件>"
    role_team:
      - role: "<角色名>"
        responsibility: "<该角色负责什么>"
    tools:
      - tool: "<shell|test|MCP|LSP|browser|plugin|manual_review>"
        purpose: "<用途>"
        command_or_contract: "<命令或能力契约，未知则 null>"

  governance:
    package_boundary: "<mother_pack|user_delivery_pack|both|unknown>"
    required_atomic_ids:
      - "<GOAL-xxx|REQ-xxx|PRD-xxx|SPEC-xxx|TASK-xxx|TEST-xxx|AUD-xxx|MEM-xxx>"
    stage_gate: "<需求发现|架构设计|实施规划|验证测试|总结归档>"
    stage_gate_status: "PASS|NEED_MORE_CONTEXT|BLOCKED"
    missing_items:
      - "<缺失项>"
    stop_lines:
      - "<停止条件>"

  execution_brief:
    objective: |
      <执行者要完成的目标>
    non_goals:
      - "<明确不要做什么>"
    constraints:
      - "<路径、权限、时间、兼容性、交付边界等约束>"
    expected_outputs:
      - "<预期产物>"
    validation_plan:
      - "<验证命令、审查方式或证据要求>"

  memory_and_handoff:
    should_write_memory: false
    memory_target: "<AI_PROJECT_CONTEXT|BRAIN-KB|03-memory|handoff_doc|null>"
    handoff_summary_required: true
    final_response_requirements:
      - "说明处理子系统"
      - "列出关键文件"
      - "说明验证结果"
      - "标明未验证项"
```

`traceability` 与 `route_feedback` 是强制字段。若本轮任务还没有 `uso_id`，必须显式写 `null`，并在 `route_feedback.feedback_to_guide` 或 `governance.missing_items` 里说明是否需要先创建统一状态对象。

## 2. DIRECT 示例

```yaml
guide_secretary_handoff:
  schema_version: "1.0"
  handoff_id: "GSH-YYYYMMDD-001"
  created_at: "<ISO8601>"
  source:
    raw_user_input: |
      请完善引导秘书逻辑，让未来 AI 可以读懂整个母包并协同开发。
    conversation_context: |
      用户正在完善母交付包，希望母包辅助通用 AI 协同开发，不替代模型。
  intent:
    normalized_intent: "建立母包入口级引导秘书协议"
    intent_id: "GUIDE_SECRETARY"
    confidence: 0.94
    route_decision: "DIRECT"
    route_reason: |
      用户明确提到引导秘书，并指出 QCM 与 Q-SpecTrum 已有旧设计，需要重新抽象为母包级协议。
    ambiguity_flags: []
  radar:
    track: "planning"
    platform: "00"
    people: ["developer", "secretary", "architect", "risk_auditor"]
    style: "deep_reading"
    supplement: ["need_path_scan"]
  target:
    subsystem: "00.超级提示词工程/12-引导秘书逻辑"
    entry_files:
      - "00.超级提示词工程/README.md"
      - "05.超极智脑_Q-SpecTrum/qspectrum_engine.py"
      - "05.超极智脑_Q-SpecTrum/AI项目管理/Systems/ai-skill-system/repos/skill-00-navigator/README.md"
      - "04.QCM-MVP-Emergence/qcm/collaboration/meeting.py"
    optional_files:
      - "04.QCM-MVP-Emergence/qcm/summoning/registry.py"
    role_team:
      - role: "Guide Secretary"
        responsibility: "主持意图识别、置信度、路由、交接"
      - role: "Chief Architect"
        responsibility: "确认母包级架构边界"
      - role: "Risk Auditor"
        responsibility: "检查越权、漂移、无验证完成声明"
    tools:
      - tool: "shell"
        purpose: "读取文件与扫描硬编码路径"
        command_or_contract: "rg / Get-Content / verification commands"
  governance:
    package_boundary: "mother_pack"
    required_atomic_ids: ["GOAL-guide-secretary", "SPEC-guide-secretary", "TASK-doc-protocol"]
    stage_gate: "架构设计"
    stage_gate_status: "PASS"
    missing_items: []
    stop_lines:
      - "不得要求其他模型忽略自身系统规则"
      - "不得把引导秘书设计成直接执行者"
  execution_brief:
    objective: |
      将 QCM 与 Q-SpecTrum 中被掩盖的秘书/导航逻辑抽象为 00 的正式协议。
    non_goals:
      - "不重写 Q-SpecTrum 运行时代码"
      - "不把用户交付包做成母包镜像"
    constraints:
      - "文档不得硬编码本机绝对路径"
      - "必须保持母包辅助通用 AI，而非替代通用 AI"
    expected_outputs:
      - "GUIDE-SECRETARY-PROTOCOL.md"
      - "GUIDE-SECRETARY-HANDOFF-TEMPLATE.md"
      - "README / Master / Routing Matrix / Context Map 更新"
    validation_plan:
      - "扫描硬编码本机路径"
      - "核对 00 文件数量与全局地图"
  memory_and_handoff:
    should_write_memory: false
    memory_target: null
    handoff_summary_required: true
    final_response_requirements:
      - "说明新增协议"
      - "说明验证结果"
```

## 3. CONFIRM 示例

```yaml
guide_secretary_handoff:
  schema_version: "1.0"
  handoff_id: "GSH-YYYYMMDD-002"
  intent:
    normalized_intent: "可能是完善用户交付包，也可能是完善母包入口协议"
    intent_id: "AMBIGUOUS"
    confidence: 0.68
    route_decision: "CONFIRM"
    route_reason: |
      用户提到交付包和引导逻辑，但未说明本轮要写入母包还是用户交付包。
    ambiguity_flags:
      - "package_boundary_unclear"
  next_questions:
    - "本轮要完善的是母交付包的 AI 协作入口，还是某个具体项目的用户交付包？"
```

## 4. CLARIFY 示例

```yaml
guide_secretary_handoff:
  schema_version: "1.0"
  handoff_id: "GSH-YYYYMMDD-003"
  intent:
    normalized_intent: "用户目标不足以安全路由"
    intent_id: "AMBIGUOUS"
    confidence: 0.42
    route_decision: "CLARIFY"
    route_reason: |
      当前输入没有说明目标、交付对象或期望产物，直接执行会造成误改。
  next_questions:
    - "你希望我现在做规划、写文档、改代码，还是做审查？"
    - "目标对象是母交付包、用户交付包，还是某个子系统？"
    - "本轮完成标准是什么？"
```

## 5. 自检清单

生成交接包后，引导秘书必须自检：

- `raw_user_input` 是否逐字保留。
- `route_decision` 是否与 `confidence` 档位一致。
- `traceability.uso_id`、`ledger_ref`、`validation_refs` 是否能追踪到统一状态对象和验证证据。
- `route_feedback.selected_route` 是否来自路由矩阵，`rejected_routes` 是否说明排除依据。
- `package_boundary` 是否明确；不明确则不能写入用户交付包。
- `entry_files` 是否是最小集合。
- `validation_plan` 是否可执行或可审查。
- `stop_lines` 是否覆盖越权、漂移、无证据完成声明。
- `final_response_requirements` 是否要求说明未验证项。
