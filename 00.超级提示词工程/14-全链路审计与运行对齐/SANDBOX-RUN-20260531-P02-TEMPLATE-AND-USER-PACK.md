# Sandbox Run — 2026-05-31 P02 Template And User Pack

> Mode: six-round audit flywheel  
> Scope: `02.通用知识库框架_Universal-KB` + `协同通用AI大模型开发交付包`  
> Output: B6 boundary crystal plus template/delivery fixes and validation evidence

## R1 — Intent And Boundary

```yaml
question: "Why audit P02 and USER_PACK together?"
answer: "They are both handoff layers. P02 hands a lightweight knowledge-base structure to an AI/user; USER_PACK hands a concrete project result to an end user or next AI."
boundary:
  P02:
    is: "Universal-KB template specification with MemoryOS smoke and AGENTS rules."
    is_not: "The full runnable Flask/MCP/search app."
  USER_PACK:
    is: "Final delivery skeleton, four-system documentation contract, and hygiene verifier."
    is_not: "A guarantee that an arbitrary concrete app has passed its own runtime tests."
```

## R2 — Inventory And Reading

```yaml
observed_structure:
  P02_filtered_file_count_after_fix: 28
  USER_PACK_filtered_file_count: 14
key_reads:
  - "02.通用知识库框架_Universal-KB/README.md"
  - "02.通用知识库框架_Universal-KB/INDEX.md"
  - "02.通用知识库框架_Universal-KB/docs/验证指南.md"
  - "02.通用知识库框架_Universal-KB/docs/快速开始.md"
  - "02.通用知识库框架_Universal-KB/docs/三体体系.md"
  - "02.通用知识库框架_Universal-KB/04-memory/memoryos.py"
  - "02.通用知识库框架_Universal-KB/05-agents/AGENTS.md"
  - "协同通用AI大模型开发交付包/README.md"
  - "协同通用AI大模型开发交付包/INDEX.md"
  - "协同通用AI大模型开发交付包/交付包组装规则.md"
  - "协同通用AI大模型开发交付包/VERIFY-DELIVERY.ps1"
  - "协同通用AI大模型开发交付包/scripts/verify.ps1"
  - "协同通用AI大模型开发交付包/AI_PROJECT_CONTEXT.md"
  - "协同通用AI大模型开发交付包/HANDOFF.md"
  - "协同通用AI大模型开发交付包/VALIDATION_REPORT.md"
  - "协同通用AI大模型开发交付包/TRACEABILITY-MATRIX.md"
```

## R3 — Reality Checks

```yaml
checks:
  - id: "B6-CHK-001"
    question: "Does P02 preserve its advertised empty template directories after clone?"
    result: "Fixed by adding .gitkeep files to 01-raw, 02-processed, 04-memory short/mid/long, and 06-output."
  - id: "B6-CHK-002"
    question: "Does P02 smoke write runtime state into the mother package root?"
    result: "Fixed. memoryos.py now uses tempfile.TemporaryDirectory and cleans the test data."
  - id: "B6-CHK-003"
    question: "Does P02 overclaim full runtime application status?"
    result: "Fixed in README/INDEX and high-risk docs; complete app is explicitly 03."
  - id: "B6-CHK-004"
    question: "Does USER_PACK current-state narrative match validation registry?"
    result: "Fixed. Context, validation report, handoff, traceability, and four-system docs now cite current 2026-05-31 evidence."
  - id: "B6-CHK-005"
    question: "Can Strict verification be misread as full business runtime validation?"
    result: "Mitigated. README, assembly rules, and scripts/verify.ps1 now state the skeleton wrapper must be extended/replaced for concrete project smoke/tests."
```

## R4 — Breakpoint Repair

```yaml
breakpoints_found:
  - id: "B6-BP-001"
    issue: "P02 README/INDEX referenced a migration file as if it belonged inside P02."
    fix: "Clarified that migration guidance lives in README scheme A/B and the mother-root migration document."
  - id: "B6-BP-002"
    issue: "P02 logical directories were documented but not preserved in Git."
    fix: "Added .gitkeep placeholders."
  - id: "B6-BP-003"
    issue: "MemoryOS smoke created test_memory relative to caller cwd."
    fix: "Use TemporaryDirectory for isolated smoke data."
  - id: "B6-BP-004"
    issue: "USER_PACK retained old test counts and validation snapshots."
    fix: "Updated current-state docs to the 30-registration evidence set."
  - id: "B6-BP-005"
    issue: "AI reading order skipped handoff and validation state."
    fix: "README and INDEX now route AI through context, handoff, validation, traceability, changelog, then four-system docs."
```

## R5 — Validation

```yaml
commands:
  - command: "python qa_runner.py validate --scope P02_UNIVERSAL_KB"
    result: "PASS; 1/1, py_compile OK, MemoryOS smoke exit 0"
  - command: "python qa_runner.py validate --scope USER_PACK"
    result: "PASS; 2/2, normal and Strict delivery gates clear"
  - command: "powershell -ExecutionPolicy Bypass -File .\\VERIFY-DELIVERY.ps1"
    cwd: "协同通用AI大模型开发交付包"
    result: "PASS; 14 files scanned, 12 Markdown checked, 0 warnings, 0 failures"
  - command: "powershell -ExecutionPolicy Bypass -File .\\VERIFY-DELIVERY.ps1 -Strict"
    cwd: "协同通用AI大模型开发交付包"
    result: "PASS; 14 files scanned, 12 Markdown checked, 0 warnings, 0 failures"
  - command: "rg high-risk stale phrases in P02"
    result: "No matches for complete-app/test_memory/stale-count risk patterns"
  - command: "Remove generated root test_memory after verifying it contained no files"
    result: "Cleaned runtime artifact produced by the older smoke behavior"
```

## R6 — Synthesis Gate

```yaml
decision: "B6 is verified as a handoff-boundary layer: P02 is a preserved template with smoke-testable MemoryOS; USER_PACK is a strict delivery-hygiene package that still requires concrete project tests when used for real delivery."
do_not_claim:
  - "P02 is the complete runnable KB app."
  - "USER_PACK Strict means a future app's business runtime has passed."
  - "A historical validation count in CHANGELOG is current evidence."
next_batch: "B7_CROSS_SYSTEM_GOLDEN_PATHS completed; next real step is GS-07 full sample with an actual user project, not a fabricated demo."
```
