# Self-Bootstrap Project Spec and Run

> 用途: 把用户在 2026-06-01 提出的真实意图, 收敛为母包第一次“用自己开发自己”的协同通用 AI 项目实例。
> 范围: ROOT, P00 control plane, Guide Secretary routing, P03/P04/P05/USER_PACK integration boundary.
> 原则: 不过度改结构; 只修真实断点、验证失败、交接不清、权威漂移和可复现启动卡点。
> 状态: PHASE-1 VERIFIED. The control-plane self-bootstrap route is now runnable.

## 1. Inferred Socratic Answers

The user did not need another questionnaire. The nine questions resolve to this operating decision:

```yaml
inferred_answers:
  highest_goal:
    answer: "让任何新通用 AI 对话框从 GitHub 平滑启动, 并用 mother-delivery-package 自己开发 mother-delivery-package 自身。"
  delivery_shape:
    answer: "E: all outcomes, but staged. Phase 1 creates the self-bootstrap control-plane instance; later phases may create project USER_PACK instances."
  minimum_success_standard:
    answer:
      - "route natural language self-bootstrap intent into a stable cross-system path"
      - "create GOAL/REQ/SPEC/TASK/TEST evidence"
      - "run current validation gates"
      - "push a scoped repository improvement"
      - "leave a reproducible handoff for the next AI"
  project_name:
    answer: "Mother Package Self-Bootstrap AI Collaboration Project"
  main_failure_to_prevent:
    answer:
      - "AI reads without execution"
      - "AI edits without route_feedback"
      - "AI loops into prompt/role expansion"
      - "AI confuses USER_PACK strict with final business delivery"
      - "AI writes detached submodules"
  memory_target:
    answer: "Repository docs and machine-readable 00/14 artifacts are authority for this phase; Codex memory and 03/05 memory are secondary evidence sources."
  submodule_policy:
    answer: "Phase 1 does not edit 03/05 code. It only routes to them and verifies them. Future submodule editing must switch 03->main and 05->master first."
  blueprint_form:
    answer: "One combined spec-and-run artifact, registered in 00/14, to avoid structural overgrowth."
  codex_role:
    answer: "Codex acts as execution controller, product architect, route auditor, and validation owner, but every step stays behind stage gates."
```

## 2. Project Object

```yaml
self_bootstrap_project:
  id: "GOAL-20260601-MOTHER-PACK-SELF-BOOTSTRAP"
  title: "母包自举协同开发项目"
  type: "goal"
  owner_layer: "P00_SUPER_PROMPT"
  package_boundary: "cross"
  route:
    intent_id: "SELF_BOOTSTRAP_PROJECT"
    decision: "DIRECT"
    selected_route: "ROOT -> 00 -> 03/04/05 -> USER_PACK"
    confidence_after_routing: 0.86
  validation_refs:
    - "VAL-ROOT-ROUTE-SMOKE"
    - "VAL-00-AUDIT-ASSETS"
    - "VAL-00-CROSS-DOC-CONSISTENCY"
    - "VAL-END-TO-END"
    - "VAL-CROSS-INTERFACE"
    - "VAL-USER-PACK-DELIVERY-STRICT"
  phase_1_write_scope:
    - "qa_runner.py"
    - "00.超级提示词工程/02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md"
    - "00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md"
    - "00.超级提示词工程/14-全链路审计与运行对齐/*registry/ledger/audit assets"
    - "00.超级提示词工程/15-超级系统提示词工程/FIRST-DIALOG-BOOTSTRAP-PROMPT.md"
  phase_1_no_write:
    - "03.数据库管理_文件夹整理AI应用 code"
    - "05.超极智脑_Q-SpecTrum code"
    - "user project final delivery instance"
```

## 3. Actual Route Gap Found and Fixed

Before this run, the user's self-bootstrap intent was not stable:

```yaml
before_fix:
  probe_1:
    input: "我要用这个母包项目完善母包自身，形成第一次真正的协同通用AI大模型项目开发实例，并把结果反哺仓库"
    decision: "CLARIFY"
    intent_id: "IMPLEMENTATION"
    platform: "USER_PACK"
    confidence: 0.46
  probe_2:
    input: "新对话框需要从GitHub平滑启动，并用mother-delivery-package开发mother-delivery-package自己"
    decision: "CONFIRM"
    intent_id: "USER_DELIVERY"
    platform: "mother_pack"
    confidence: 0.69
```

This was a real control-plane gap: the first real self-bootstrap project instance was being routed as generic implementation or delivery instead of a cross-system mother-package goal.

The fix added `SELF_BOOTSTRAP_PROJECT` as an explicit Guide Secretary intent and route smoke scenario.

```yaml
after_fix:
  command: "python qa_runner.py route \"我要用这个母包项目完善母包自身，形成第一次真正的协同通用AI大模型项目开发实例，并把结果反哺仓库\""
  exit_code: 0
  intent_id: "SELF_BOOTSTRAP_PROJECT"
  decision: "DIRECT"
  platform: "cross_subsystem"
  selected_route: "ROOT -> 00 -> 03/04/05 -> USER_PACK"
  confidence_after_routing: 0.86
  uso_id: "GOAL-20260601-MOTHER-PACK-SELF-BOOTSTRAP"
```

## 4. Traceability

```yaml
traceability:
  GOAL-20260601-MOTHER-PACK-SELF-BOOTSTRAP:
    statement: "Use the mother package to develop the mother package itself as the first real collaborative AI project instance."
  REQ-20260601-001:
    statement: "A new AI dialogue must be able to start from GitHub without prior chat memory."
    validation: ["VAL-ROOT-ROUTE-SMOKE", "VAL-END-TO-END"]
  REQ-20260601-002:
    statement: "The self-bootstrap intent must route to a cross-system path, not generic USER_PACK or IMPLEMENTATION."
    validation: ["VAL-ROOT-ROUTE-SMOKE"]
  REQ-20260601-003:
    statement: "The first self-bootstrap pass must not over-modify structure or touch 03/05 code."
    validation: ["git status for root, 03, 05"]
  REQ-20260601-004:
    statement: "The repository must preserve evidence fields: route_feedback, uso_id, ledger_ref, validation_refs, command evidence, and stop lines."
    validation: ["VAL-00-AUDIT-ASSETS", "VAL-00-CROSS-DOC-CONSISTENCY"]
  SPEC-20260601-001:
    statement: "Add an explicit SELF_BOOTSTRAP_PROJECT intent to qa_runner.py and route smoke."
  SPEC-20260601-002:
    statement: "Document the self-bootstrap project as one combined spec-and-run artifact."
  TASK-20260601-001:
    statement: "Patch route logic and smoke coverage."
  TASK-20260601-002:
    statement: "Register the self-bootstrap artifact and update counts."
  TEST-20260601-001:
    statement: "Run self-bootstrap route probe and ROOT validation."
```

## 5. Stage Gates

| Gate | Current Result | Evidence |
|---|---|---|
| P0 Boundary | PASS | Project remains model-native; no instruction asks AI to override model/platform rules. |
| P1 Integrity | PASS | Root, 03, and 05 working trees checked; 03 is on `main`, 05 is on `master` in the local owner checkout. |
| P2 Route | PASS | `SELF_BOOTSTRAP_PROJECT` now routes DIRECT to `ROOT -> 00 -> 03/04/05 -> USER_PACK`. |
| P3 Spec | PASS | This file contains GOAL/REQ/SPEC/TASK/TEST traceability for Phase 1. |
| P4 Execution Eligibility | ROOT_EDIT | Phase 1 edits only root/P00 control-plane files; no 03/05 code edits. |
| P5 Validation | PASS | ROOT scoped validation passed after route repair: 7/7 PASS with route smoke 9/9. |

## 6. What This Phase Proves

This phase proves that the mother package can now recognize and enter its first real self-development project instance:

```text
user intent
-> SELF_BOOTSTRAP_PROJECT
-> ROOT -> 00 -> 03/04/05 -> USER_PACK
-> GOAL/REQ/SPEC/TASK/TEST
-> route smoke validation
-> repository improvement
```

It does not yet claim that a full external business project has been generated. It also does not claim that 03 or 05 code was modified. Those are later phases and require separate edit eligibility.

## 7. Next Real Phase

The next phase should be a restrained self-bootstrap development cycle:

```text
Phase 2:
  input: one concrete user project idea or one concrete mother-package usability gap
  output: minimal PRD/SPEC/TASK/TEST package
  execution: route to the smallest subsystem set
  validation: scoped qa_runner gates plus USER_PACK strict if delivery artifacts change
  stop: when validation is green and the handoff can be replayed
```

Stop here if no real blocker is found. The point is to make the mother package usable, not to multiply frameworks.
