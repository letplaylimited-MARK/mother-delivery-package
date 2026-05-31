# Sandbox Run 20260531 AI Collaboration Cold Start Simulation

> 用途: 第二次全新 cold-start 沙盒, 用一个干净 GitHub clone 模拟通用 AI 大模型或新开发者接手母包, 判断它是否能与母包共同协同项目开发。  
> 范围: ROOT, P00 first-dialog bootstrap, Guide Secretary routing, P03/P05 submodule boundary, USER_PACK delivery state.  
> 状态: VERIFIED with current command evidence on 2026-05-31.

## 1. Simulation Setup

```yaml
simulation:
  clone_path: "C:/tmp/mdp-ai-collab-sim-20260531-232651"
  clone_command: "git clone --recurse-submodules https://github.com/letplaylimited-MARK/mother-delivery-package.git"
  root_head: "943e893fbd2dfa13244c97d72a695a3be4fc08ed"
  root_branch: "main"
  submodules:
    "03":
      sha: "424c2cb86502ebe40904feab6692f99634eb2857"
      branch_state_after_clone: "HEAD (no branch)"
      edit_rule: "checkout main before editing"
    "05":
      sha: "7b2b7ee100eea75574b715f87857e5ce3f8128d1"
      branch_state_after_clone: "HEAD (no branch)"
      edit_rule: "checkout master before editing"
```

The simulation deliberately used a fresh clone instead of the working checkout. This proves what a new AI conversation or new developer can infer from the public repository itself.

## 2. Command Evidence

```yaml
command_evidence:
  - command: "python qa_runner.py consistency"
    exit_code: 0
    result: "10/10 PASS"
  - command: "python qa_runner.py status"
    exit_code: 0
    result: "registries loaded; 31 validations listed as verified_current; worktree clean"
  - command: "python qa_runner.py validate"
    exit_code: 1
    result: "first run had 30 PASS / 1 FAIL in VAL-05-PYTEST; failure localized to transient routing regression timeout"
  - command: "pytest tests/test_regression.py::test_r3_case_insensitive_routing tests/test_regression.py::test_r3_routing_accuracy -vv -s"
    cwd: "05.超极智脑_Q-SpecTrum"
    exit_code: 0
    result: "2/2 PASS"
  - command: "pytest tests -q"
    cwd: "05.超极智脑_Q-SpecTrum"
    exit_code: 0
    result: "158/158 PASS"
  - command: "python qa_runner.py validate --scope P05_QSPECTRUM"
    exit_code: 0
    result: "6/6 PASS"
  - command: "python qa_runner.py validate"
    exit_code: 0
    result: "31/31 PASS, 0 FAIL/WARN/SKIP, automatic 31/31"
```

Interpretation: the final acceptance state is green, but the first full run exposed a useful stability signal. Future agents should record the first failure, rerun the failing scope, and only claim readiness after the final current-command evidence is green.

## 3. Route Probes

```yaml
route_probes:
  - intent: "我要用母包和通用AI大模型一起开发一个新的AI项目，从想法到需求、规格、任务、测试、交付"
    decision: "DIRECT"
    target: "ROOT -> 00 -> 03/04/05 -> USER_PACK"
    confidence: 0.82
    validation_refs:
      - "VAL-ROOT-ROUTE-SMOKE"
      - "VAL-END-TO-END"
      - "VAL-CROSS-INTERFACE"
      - "VAL-USER-PACK-DELIVERY-STRICT"
    important_boundary: "DIRECT means route is clear, not that editing can begin without requirements/spec/task/validation anchors."
  - intent: "我要新增一个MCP插件并让03知识库管理应用和05运行平台协同调用"
    decision: "DIRECT"
    target: "03 WorkBuddy KB search/MCP"
    risk: "cross-subsystem intent mentions 05, but route scorer selected P03 as primary; execution needs explicit 05 integration validation."
  - intent: "我要修改03子仓库的数据库和搜索索引功能并推送"
    decision: "CLARIFY"
    target: "追问，不执行"
    boundary: "good stop line before submodule editing"
  - intent: "我要改05 API Web MCP运行平台并确保E2E"
    decision: "DIRECT"
    target: "目标子系统 + 对应验证"
    risk: "generic implementation route still reports P03 validation_refs; future route hardening should prefer explicit P05 refs when 05/API/Web/MCP keywords dominate."
  - intent: "我想把这套系统接给新的AI对话框，要求它先理解再执行"
    decision: "CLARIFY"
    target: "00/00 + MISSION-MEMORY.md"
    boundary: "correctly avoids pretending a new AI has already understood the repository"
  - intent: "我要立刻重构所有文件夹并丰富功能"
    decision: "CLARIFY"
    target: "00/00 + MISSION-MEMORY.md"
    boundary: "correct stop-rebuild behavior"
```

## 4. Multi-Role Findings

```yaml
role_review:
  new_developer_ai_view:
    can_start: true
    key_entrypoints:
      - "README.md"
      - "MOTHER-PACK-ACTIVATION-GUIDE.md"
      - "FIRST-DIALOG-BOOTSTRAP-PROMPT.md"
      - "MISSION-MEMORY.md"
      - "AI_PROJECT_CONTEXT.md"
      - "GUIDE-SECRETARY-PROTOCOL.md"
      - "SUBSYSTEM-ROUTING-MATRIX.md"
      - "VALIDATION_REGISTRY.yaml"
    main_gaps:
      - "Mode A awakening_check also needs explicit execution_eligibility."
      - "verified_current in registries must not be mistaken for current-command evidence."
      - "DIRECT routing must not be mistaken for write permission."
      - "USER_PACK strict validation proves package hygiene, not a completed real business project."
  control_plane_view:
    control_plane_ready: true
    full_project_instance_done: false
    required_evidence_fields:
      - "route_feedback.selected_route"
      - "route_feedback.rejected_routes"
      - "route_feedback.confidence_after_routing"
      - "route_feedback.feedback_to_guide"
      - "route_feedback.blocked_reason"
      - "uso_id"
      - "ledger_ref"
      - "validation_refs"
      - "authority_scope"
      - "write_target"
      - "conflict_owner"
```

## 5. Acceptance Judgment

```yaml
acceptance:
  mother_package_control_plane: "READY"
  fresh_clone_developer_takeover: "READY_WITH_GUARDRAILS"
  ai_collaboration_project_development: "CONTROL_PLANE_READY"
  full_real_project_instance: "NOT_YET_RUN"
  submodule_editing: "BLOCKED_UNTIL_BRANCH_CHECKOUT"
  final_delivery_claim: "BLOCKED_UNTIL_PROJECT_INSTANCE_AND_BUSINESS_SMOKE"
```

The project is ready to guide a universal AI model through collaborative development at the control-plane level. The next higher standard is not another abstract refactor; it is a real project-instance rehearsal:

```text
natural-language idea
-> requirement/spec/task/test objects
-> route_feedback + USO + ledger_ref + validation_refs
-> P03/P04/P05/USER_PACK execution
-> project-specific smoke tests
-> final delivery package in strict mode
```

## 6. Prompt Hardening Decisions

```yaml
prompt_hardening:
  add_to_first_dialog:
    - "canonical_start_matrix"
    - "DIRECT_is_not_write_permission"
    - "validation evidence source: current_command vs registry_claim"
    - "submodule branch commands for 03 and 05"
    - "delivery_instance_state: template|project_instance|final_delivery"
    - "transient validation failure handling: rerun failing scope, then rerun full gate"
  add_to_activation_guide:
    - "awakening success is not edit permission"
    - "P4 execution eligibility is mandatory before writing"
    - "USER_PACK strict is delivery hygiene unless tied to a real project instance"
```

## 7. Stop Lines

- Do not continue expanding roles, prompts, or architecture unless a current validation fails, an authority document drifts, or a real handoff blocker appears.
- Do not edit 03/05 from detached HEAD.
- Do not claim "full project delivery" from USER_PACK strict validation alone.
- Do not report registry `verified_current` as if it were freshly rerun unless command evidence says so.
- Do not treat `DIRECT` as permission to write; it only says the routing target is clear.
