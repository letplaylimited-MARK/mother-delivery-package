# Fresh Clone Developer Simulation

> Date: 2026-05-31  
> Scope: GitHub public clone, ROOT, 00, 03, 05, USER_PACK  
> Purpose: verify that a new developer or new AI conversation can use the GitHub repository without relying on the current local working copy.

## 1. Critical Logic Extracted

The best first-use logic is not "read every file first." It is:

```text
fresh clone with submodules
  -> confirm root and boot files
  -> run root validation/status/consistency
  -> route natural language with route_feedback
  -> read the matching subsystem crystal and entry docs
  -> run the route-specific validation gate
  -> stop unless validation fails, authority docs are stale, or a concrete handoff blocker appears
```

This protects the project from the two main failure modes:

- shallow confidence: claiming full understanding without file/command evidence
- endless expansion: adding more prompt layers instead of using the verified control plane

## 2. Memory And Crystal Inputs Reviewed

- Codex long-term memory: mother-package orientation, route feedback, memory-source authority, and validation drift rules.
- `KNOWLEDGE-CRYSTALS-BATCH0-ROOT-P00.md`: mother-package mission, startup authority, Guide Secretary boundary, route matrix, inventory and graph seeds.
- `SUBSYSTEM-CRYSTAL-B7-CROSS-SYSTEM-GOLDEN-PATHS.md`: golden paths and stop-rebuild rule.
- Subsystem crystals P01-P05 and B6 USER_PACK/P02: current validated surfaces and honest gaps.
- `SCENARIO-ACCEPTANCE-MATRIX.md`: GS-01 through GS-08 acceptance paths.
- `BREAKPOINT-REPAIR-MATRIX.md`: required route feedback, USO/ledger/validation refs, and stop-line logic.
- `MEMORY-SOURCE-INDEX.yaml`: authority split between ROOT, 03, and 05.
- `FIRST-DIALOG-BOOTSTRAP-PROMPT.md`: ordinary-chat cold-start instruction.

## 3. Simulation Environment

```text
fresh_clone_path: C:\tmp\mdp-coldstart-20260531-225429
source: https://github.com/letplaylimited-MARK/mother-delivery-package
clone_command: git clone --recurse-submodules
root_commit: b73a2135962323b4937e4e3e8896ea01bf60029f
submodule_03: 424c2cb86502ebe40904feab6692f99634eb2857
submodule_05: 7b2b7ee100eea75574b715f87857e5ce3f8128d1
```

## 4. Cold Start Evidence

```yaml
cold_start_report:
  repo_root_confirmed: true
  clone_mode: "fresh_clone"
  submodules_ready: true
  submodule_branch_state: "detached_clean"
  boot_files_read:
    - "README.md"
    - "MOTHER-PACK-ACTIVATION-GUIDE.md"
    - "MISSION-MEMORY.md"
    - "AI_PROJECT_CONTEXT.md"
    - "00.超级提示词工程/15-超级系统提示词工程/FIRST-DIALOG-BOOTSTRAP-PROMPT.md"
    - "00.超级提示词工程/14-全链路审计与运行对齐/SCENARIO-ACCEPTANCE-MATRIX.md"
    - "00.超级提示词工程/14-全链路审计与运行对齐/BREAKPOINT-REPAIR-MATRIX.md"
  validation:
    qa_validate: "PASS 31/31"
    qa_status: "PASS exit=0"
    qa_consistency: "PASS 10/10"
  git:
    root_status: "clean main...origin/main"
    submodule_status: "detached clean, expected for submodule checkout"
  stop_lines: []
```

## 5. Route Simulation Evidence

| Scenario | Input | Decision | Target | Validation refs |
|---|---|---|---|---|
| New project loop | `我想用这个母包开发一个新的AI项目，从想法到需求、规格、任务、测试、交付` | DIRECT 0.82 | `ROOT -> 00 -> 03/04/05 -> USER_PACK` | `VAL-ROOT-ROUTE-SMOKE`, `VAL-END-TO-END`, `VAL-CROSS-INTERFACE`, `VAL-USER-PACK-DELIVERY-STRICT` |
| P03 search/MCP | `我要修改03知识库的搜索功能并验证MCP工具` | DIRECT 0.82 | `03 WorkBuddy KB search/MCP` | `VAL-03-INSTALL`, `VAL-03-TESTS`, `VAL-03-HTTP-SMOKE` |
| P05 API/routes | `我要启动05 Q-SpecTrum API和角色路由` | DIRECT 0.82 | `05.Q-SpecTrum runtime/API/MCP` | `VAL-05-STATUS`, `VAL-05-API-SMOKE`, `VAL-05-MCP-SMOKE` |
| Stop rebuild | `为什么这个项目一直重构，怎么收敛？` | CONFIRM 0.68 | `00/14 + 00/07 + tests/evidence` | `VAL-END-TO-END`, `VAL-CROSS-INTERFACE` |

## 6. Finding

The public GitHub repository is usable for a new developer or new AI conversation after fresh clone. The main cold-start friction is not validation failure; it is submodule branch state:

- Fresh submodules are checked out at exact commits, so `git status` inside 03/05 shows `HEAD (no branch)`.
- This is correct for read-only validation.
- It becomes a stop line only when the developer wants to edit 03 or 05.

## 7. Repair Applied

- Updated `FIRST-DIALOG-BOOTSTRAP-PROMPT.md` to record `submodule_branch_state`.
- Added explicit branch instructions:
  - 03 -> `git checkout main`
  - 05 -> `git checkout master`
- Updated `MOTHER-PACK-ACTIVATION-GUIDE.md` and `AI_PROJECT_CONTEXT.md` with the same rule.

## 8. Acceptance Conclusion

```yaml
developer_simulation:
  evidence_level: "VERIFIED"
  can_fresh_clone: true
  can_initialize_submodules: true
  can_validate_all: true
  can_route_core_tasks: true
  can_remain_clean_after_validation: true
  remaining_gap:
    - "A real external business project instance has not yet been generated end to end; use the next real user project as GS-07 project-instance evidence."
  stop_rule: "Do not expand structure further unless a fresh-clone validation fails, an authority document drifts, or a concrete handoff blocker appears."
```
