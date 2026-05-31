# Sandbox Run — 2026-05-31 P04 QCM And QCM Skill

> Mode: six-round audit flywheel  
> Scope: `04.QCM-MVP-Emergence` + `qcm-universal-ai-system-v3.0.skill`  
> Output: QCM runtime/skill crystal plus fixes and validation evidence

## R1 — Intent And Boundary

```yaml
question: "Why does this subsystem exist inside the mother package?"
answer: "It gives the mother package a concrete model for multi-role AI collaboration: formula-driven resonance, sandbox/flywheel concepts, role/stage/quality dimensions, and validation gates."
boundary:
  in_scope:
    - 22-formula QCM research runtime
    - qcm/ reusable package CLI and HTTP service
    - Cap-D/G default-off capability flags
    - 63 release tests plus guard checks
    - qcm-v3.0 skill archive validation and tests
  out_of_scope:
    - replacing the active general AI model
    - treating the embedded P04 Ghost Channel SDK as the P01 authority
    - expanding the meta-system without runnable acceptance evidence
```

## R2 — Inventory And Reading

```yaml
observed_structure:
  p04_filtered_file_count: 148
  qcm_skill_internal_file_count: 43
key_reads:
  - "04.QCM-MVP-Emergence/README.md"
  - "04.QCM-MVP-Emergence/PROJECT_HANDOFF-QCM.md"
  - "04.QCM-MVP-Emergence/22_FORMULA_SYSTEM.md"
  - "04.QCM-MVP-Emergence/USER_GUIDE.md"
  - "04.QCM-MVP-Emergence/SCENARIOS.md"
  - "04.QCM-MVP-Emergence/VERIFY-QCM.md"
  - "04.QCM-MVP-Emergence/CHANGELOG.md"
  - "04.QCM-MVP-Emergence/qcm/config.py"
  - "04.QCM-MVP-Emergence/qcm/pipeline.py"
  - "04.QCM-MVP-Emergence/qcm/main.py"
  - "04.QCM-MVP-Emergence/02-代码编写/main.py"
  - "04.QCM-MVP-Emergence/02-代码编写/main_complete.py"
  - "04.QCM-MVP-Emergence/02-代码编写/test_qcm_all.py"
  - "qcm-universal-ai-system-v3.0.skill::qcm-v3.0/SKILL.md"
  - "qcm-universal-ai-system-v3.0.skill::qcm-v3.0/config.yaml"
  - "qcm-universal-ai-system-v3.0.skill::qcm-v3.0/scripts/validate_qcm.py"
```

## R3 — Runtime Reality

```yaml
runtimes:
  legacy_standard_demo:
    command: "python \"02-代码编写/main.py\""
    result: "R22=0.8664 emergence"
  full_formula_demo:
    command: "python \"02-代码编写/main_complete.py\""
    result: "R=0.8658 emergence; active formulas 6/10 groups"
  qcm_research_cli:
    command: "python -m qcm.main --mode research --seed 42 --max-rounds 22"
    result: "R22=0.8658 emergence"
  qcm_production_cli:
    command: "python -m qcm.main --mode production --seed 42 --max-rounds 3 --output <temp>"
    result: "qcm_result_<timestamp>.json written"
  qcm_service:
    command: "python -m qcm.main --mode service --port <free-port>"
    result: "/health, /status, /simulate returned HTTP 200"
skill_archive:
  validator: "python scripts/validate_qcm.py -> PASS, 0 issues, 100.0%"
  tests: "pytest tests -q -> 173 passed"
```

## R4 — Breakpoint Repair

```yaml
breakpoints_found:
  - id: "P04-BP-001"
    issue: "test_qcm_all.py changed into 02-代码编写 and then could not import qcm namespace package from the P04 root."
    fix: "Insert P04 root into sys.path before chdir."
  - id: "P04-BP-002"
    issue: "qcm/main.py failed when executed as python qcm/main.py because the parent package root was missing from sys.path."
    fix: "Insert QCM_ROOT into sys.path before importing qcm.config."
  - id: "P04-BP-003"
    issue: "main_complete.py failed because sibling modules imported qcm.config while only script_dir was in sys.path."
    fix: "Insert the P04 root into sys.path before module imports."
  - id: "P04-BP-004"
    issue: "qcm-v3.0 skill validator still used stale V2.5 path/version assumptions and produced false P01-P09 warnings."
    fix: "Updated internal archive validator to resolve qcm-v3.0 root, expect 3.0.0, and recognize canonical phase IDs."
  - id: "P04-BP-005"
    issue: "qa_runner registered config sync as current evidence but did not execute it automatically."
    fix: "Added VAL-QCM-CONFIG-SYNC auto execution plus runtime smoke and skill archive validation handlers."
  - id: "P04-BP-006"
    issue: "Operational docs still used stale --rounds and contradictory Cap-D/G integration wording."
    fix: "Aligned USER_GUIDE, SCENARIOS, README, INSTALL, VERIFY, PROJECT_HANDOFF, 22_FORMULA_SYSTEM, and CHANGELOG."
```

## R5 — Validation

```yaml
commands:
  - command: "python \"02-代码编写/test_qcm_all.py\""
    result: "PASS; 25 PASS / 0 FAIL / 25 TOTAL"
  - command: "pytest \"02-代码编写/test_roles.py\" \"02-代码编写/test_collaboration.py\" \"02-代码编写/test_sandbox.py\" \"02-代码编写/test_flywheel.py\" \"02-代码编写/test_summoning.py\" \"02-代码编写/test_config_sync.py\" -q"
    result: "PASS; 42 passed"
  - command: "python health_check.py"
    result: "PASS; 6/6 checks passed, Status READY"
  - command: "python \"02-代码编写/main.py\""
    result: "PASS; R22=0.8664 emergence"
  - command: "python \"02-代码编写/main_complete.py\""
    result: "PASS; R=0.8658 emergence"
  - command: "python -m qcm.main --mode research --seed 42 --max-rounds 22"
    result: "PASS; R22=0.8658 emergence"
  - command: "python -m qcm.main --mode production --seed 42 --max-rounds 3 --output <temp>"
    result: "PASS; JSON output written"
  - command: "python -m qcm.main --mode production --seed 42 --max-rounds 12 --output <temp> --cap-crypto --cap-healer"
    result: "PASS; Cap-D CryptoEngine enabled, Cap-G SelfHealer enabled, JSON output written"
  - command: "service smoke via urllib"
    result: "PASS; /health, /status, /simulate"
  - command: "python qa_runner.py validate --scope P04_QCM"
    result: "PASS; 5/5 validation items; ALL CLEAR"
  - command: "python qa_runner.py validate --scope QCM_SKILL"
    result: "PASS; 2/2 validation items; ALL CLEAR"
```

## R6 — Synthesis Gate

```yaml
decision: "P04 can now be treated as runnable for QCM research, package CLI, production output, service API smoke, Cap-D/G flag smoke, and config/health guard checks. The qcm-v3.0 skill can be treated as internally consistent and test-passing."
do_not_claim:
  - "QCM replaces the general AI model."
  - "63/63 is the entire quality surface; it is the release test count only."
  - "Cap-D/G are always on."
  - "Production mode is side-effect-free."
  - "P04 embedded SDK supersedes the P01 Ghost Channel authority."
next_batch: "Batch chain B5-B7 is now completed; future P04/QCM work should be triggered by failing validation or a real role/sandbox orchestration sample."
```
