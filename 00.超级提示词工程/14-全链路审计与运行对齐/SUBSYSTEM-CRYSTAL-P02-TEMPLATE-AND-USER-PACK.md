# Subsystem Crystal — P02 Universal-KB Template And User Delivery Pack

> Batch: B6_P02_TEMPLATE_AND_USER_PACK  
> Scope: `02.通用知识库框架_Universal-KB` + `协同通用AI大模型开发交付包`  
> Status: VERIFIED current after P02 template smoke and USER_PACK normal/Strict delivery gates  
> Purpose: Preserve the boundary between knowledge-template design, runnable knowledge app, and final user delivery packaging.

## Executive Crystal

```yaml
id: KC-B6-EXEC-001
scope: P02_TEMPLATE_AND_USER_PACK
evidence_level: VERIFIED
statement: "P02 is a Universal-KB template specification, while 03 is the runnable knowledge-base implementation. USER_PACK is the final delivery skeleton and validation gate for concrete projects, not a copy of the whole mother package."
why_it_matters: "The user's intent is to let general AI models collaborate with the mother package without endless restructuring. This only works if template, runtime, and final-delivery layers are not confused."
current_validation:
  - "python qa_runner.py validate --scope P02_UNIVERSAL_KB -> 1/1 PASS"
  - "python qa_runner.py validate --scope USER_PACK -> 2/2 PASS"
  - "powershell -ExecutionPolicy Bypass -File .\\VERIFY-DELIVERY.ps1 -> 0 failures / 0 warnings"
  - "powershell -ExecutionPolicy Bypass -File .\\VERIFY-DELIVERY.ps1 -Strict -> 0 failures / 0 warnings"
```

## Authority Map

```yaml
P02_UNIVERSAL_KB:
  role: "Reusable knowledge-base template and AGENTS behavior guide."
  key_entrypoints:
    - "02.通用知识库框架_Universal-KB/README.md"
    - "02.通用知识库框架_Universal-KB/INDEX.md"
    - "02.通用知识库框架_Universal-KB/04-memory/memoryos.py"
    - "02.通用知识库框架_Universal-KB/05-agents/AGENTS.md"
  validation: "py_compile + MemoryOS smoke only; this is not a full app validation."
  important_boundary: "Empty logical layer folders may be created during template initialization; current tracked files mainly hold docs, wiki examples, MemoryOS concept code, and AGENTS rules."

P03_WORKBUDDY_KB:
  role: "Runnable knowledge-base application that implements the practical Flask/MCP/search workflow."
  current_fact: "Current audit evidence is 107 pytest tests passed and verify_install 23 pass / 0 fail."

USER_PACK:
  role: "Final user delivery package skeleton and acceptance gate."
  key_entrypoints:
    - "协同通用AI大模型开发交付包/README.md"
    - "协同通用AI大模型开发交付包/交付包组装规则.md"
    - "协同通用AI大模型开发交付包/VERIFY-DELIVERY.ps1"
    - "协同通用AI大模型开发交付包/scripts/verify.ps1"
  validation: "Normal mode checks skeleton quality; Strict mode requires project context, handoff, changelog, traceability, validation report, and a project-specific verification entry."
```

## Knowledge Crystals

### KC-B6-001 — P02 Must Not Be Presented As The Runnable V2 App

```yaml
evidence_level: VERIFIED
statement: "P02 provides a six-layer Universal-KB template, a MemoryOS-style concept engine, wiki examples, and AGENTS ingest/query/lint behavior. It does not provide the full Flask/MCP/search runtime."
implication: "Future agents should route runnable KB work to 03 and route lightweight template design or new-project knowledge skeleton work to 02."
```

### KC-B6-002 — P02 Validation Is A Template Smoke Gate

```yaml
evidence_level: VERIFIED
statement: "VAL-02-TEMPLATE-REVIEW compiles and runs 04-memory/memoryos.py. Passing it proves the template code sample is coherent, not that every Universal-KB workflow is implemented as software."
minimum_gate:
  - "python -m py_compile 04-memory/memoryos.py"
  - "python 04-memory/memoryos.py"
  - "manual review that README/INDEX do not overclaim runtime status"
```

### KC-B6-003 — USER_PACK Is A Delivery Contract, Not A Development Dump

```yaml
evidence_level: VERIFIED
statement: "The user delivery package defines value/function/structure/operation systems, assembly rules, context/handoff/traceability/validation files, and a strict verifier."
implication: "Concrete projects should copy only the useful project artifacts and necessary subsystem slices, not the entire mother package history."
```

### KC-B6-004 — Strict Delivery Gate Checks Transfer Hygiene

```yaml
evidence_level: VERIFIED
statement: "VERIFY-DELIVERY.ps1 scans required files, four system folders, Markdown fences, hardcoded local paths, secrets, placeholders, and project verification entries."
limitation: "It cannot prove the concrete application works beyond detecting that a project verification entry exists. Project-specific tests remain required."
```

### KC-B6-005 — Current-Fact Drift Was The Real B6 Breakpoint

```yaml
evidence_level: VERIFIED
symptom: "P02 and USER_PACK still referenced missing or stale items such as a local P02 migration file, old P03 test counts, old PASS snapshots, and an outdated Python delivery baseline."
fixes:
  - "P02 README/INDEX now clarify migration location, current 03 test count, and Windows PowerShell copy/init commands."
  - "P02 empty template directories now have .gitkeep files so clone/fresh handoff preserves the advertised structure."
  - "MemoryOS smoke now uses a temporary directory, preventing root-level test_memory runtime drift."
  - "USER_PACK context, handoff, validation, traceability, and four-system docs now reflect 2026-05-31 validation facts."
  - "USER_PACK AI reading order now includes AI_PROJECT_CONTEXT, HANDOFF, VALIDATION_REPORT, TRACEABILITY, and CHANGELOG before the four-system docs."
```

## Fixed This Batch

```yaml
P02:
  - "Removed implication that P02 contains its own V1_TO_V2_MIGRATION.md."
  - "Updated 03 implementation evidence from old test counts to current 107 passed."
  - "Added Windows PowerShell copy and directory initialization commands."
  - "Clarified template-vs-implementation boundary."

USER_PACK:
  - "Updated AI_PROJECT_CONTEXT.md from the 2026-05-28 snapshot to current 30-validation evidence."
  - "Aligned validation evidence after B7 to 31/31 automatic PASS; no remaining manual-current root gate."
  - "Updated HANDOFF.md to avoid false working-tree-clean claims."
  - "Updated TRACEABILITY-MATRIX.md and four-system docs with current P03/P05/P01 evidence."
  - "Kept historical changelog entries as history, not current status."
```

## Current Risks And Guardrails

```yaml
risks:
  - id: "B6-RISK-001"
    statement: "A future AI may treat P02 empty logical folders as missing implementation instead of template initialization output."
    guardrail: "Read P02 README/INDEX first and route runtime work to 03."
  - id: "B6-RISK-002"
    statement: "USER_PACK Strict passing may be mistaken for full application acceptance."
    guardrail: "Strict only verifies delivery-package hygiene; concrete apps must still expose and pass their own tests."
  - id: "B6-RISK-003"
    statement: "Exact file counts drift whenever audit crystals or generated assets are added."
    guardrail: "Use ATOMIC-FILE-INVENTORY-SUMMARY.md as the authority for current counts."
```

## Recommended Next Use

```yaml
for_codex:
  - "When creating a new knowledge-heavy project, use P02 as the folder/AGENTS template and P03 as the runnable implementation reference."
  - "When preparing final delivery, run USER_PACK normal and Strict gates, then run the concrete project's own tests."
  - "When refreshing facts, update USER_PACK narrative docs and validation registry together."
for_user:
  - "Treat the mother package as the development factory."
  - "Treat USER_PACK as the curated final package that another user or AI can understand, run, verify, and maintain."
```
