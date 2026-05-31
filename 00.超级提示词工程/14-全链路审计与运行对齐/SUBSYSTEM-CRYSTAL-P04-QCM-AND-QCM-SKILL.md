# Subsystem Crystal — P04 QCM And QCM Skill

> Batch: B4_P04_QCM_AND_QCM_SKILL  
> Scope: `04.QCM-MVP-Emergence` + root `qcm-universal-ai-system-v3.0.skill`  
> Status: VERIFIED current after runtime smoke and archive validation  
> Purpose: Preserve executable understanding of QCM as the mother package's role/flywheel/sandbox reasoning engine and the qcm-v3.0 skill as its portable AI operating method.

## Executive Crystal

```yaml
id: KC-P04-EXEC-001
scope: P04_QCM_AND_QCM_SKILL
evidence_level: VERIFIED
statement: "P04 is the QCM emergence laboratory: formula runtime, multi-role cooperation model, feature-flagged pipeline, research/production/service CLI, and paper-module tests. The root qcm-v3.0 .skill is a portable AI operating skill that packages expert roles, workflow stages, quality dimensions, validators, and templates."
why_it_matters: "The user is not trying to replace a general AI model. This subsystem gives the general model a disciplined collaboration scaffold: measure resonance, simulate role interaction, route work through expert/stage/dimension checks, and stop endless rebuild cycles with repeatable validation."
current_validation:
  - "python qa_runner.py validate --scope P04_QCM -> 5/5 PASS"
  - "python qa_runner.py validate --scope QCM_SKILL -> 2/2 PASS"
  - "python \"02-代码编写/main_complete.py\" -> R=0.8658 emergence, 6/10 formula groups active"
  - "python -m qcm.main --mode research --seed 42 --max-rounds 22 -> R22=0.8658 emergence"
  - "production smoke -> isolated JSON output written"
  - "service smoke -> /health, /status, /simulate HTTP 200"
  - "qcm-v3.0 skill validator -> 0 issues, 100.0%, PASS"
  - "qcm-v3.0 skill tests -> 173 passed"
```

## Layer Map

### L1 Legacy Research Runtime: `02-代码编写/`

```yaml
purpose: "Original executable formula lab and standalone tests."
entrypoints:
  - "python \"02-代码编写/main.py\""
  - "python \"02-代码编写/main_complete.py\""
  - "python \"02-代码编写/test_qcm_all.py\""
test_surfaces:
  - "test_qcm_all.py: 25 comprehensive checks"
  - "paper module pytest files: 38 tests"
  - "test_config_sync.py: 4 config/constant drift guards"
fixed_this_batch:
  - "test_qcm_all.py now inserts the P04 root into sys.path before changing into 02-代码编写"
  - "main_complete.py now inserts the P04 root into sys.path so sibling modules can import qcm.config"
boundary: "This layer is the research/demo compatibility layer. It should remain runnable and reproducible, but new orchestration should prefer the qcm/ namespace package."
```

### L2 Namespace Runtime: `qcm/`

```yaml
purpose: "Reusable package form of the QCM pipeline."
entrypoints:
  - "python -m qcm.main --mode research --seed 42 --max-rounds 22"
  - "python -m qcm.main --mode production --seed 42 --max-rounds 3 --output <isolated-dir>"
  - "python -m qcm.main --mode service --port <port>"
core_files:
  - "qcm/config.py: DEFAULT_CONFIG, plugin flags, thresholds, max_rounds, output dir"
  - "qcm/plugin.py: 10 plugin registrations"
  - "qcm/pipeline.py: PipelineEngine, run_round, run, report, Cap-D/G hooks"
  - "qcm/main.py: research/production/service CLI and HTTP API"
fixed_this_batch:
  - "qcm/main.py now supports both direct script execution and module execution from P04 root"
  - "qa_runner.py now auto-runs config sync and runtime smoke checks"
side_effects:
  - "production mode writes qcm_result_<timestamp>.json to output.dir"
  - "service mode starts a long-running uvicorn process until terminated"
audit_rule: "Use isolated temp output directories for production smoke. Do not let routine audit create persistent output clutter unless the user wants artifacts."
```

### L3 QCM Skill Archive: `qcm-universal-ai-system-v3.0.skill`

```yaml
purpose: "Portable QCM universal AI collaboration skill."
archive_type: "zip-format .skill"
internal_root: "qcm-v3.0/"
internal_file_count: 43
important_files:
  - "SKILL.md: activation and workflow"
  - "config.yaml: version 3.0.0, 45 experts, 9 stages, 24 dimensions"
  - "scripts/validate_qcm.py: archive consistency validator"
  - "scripts/validation_engine.py: quality validation engine"
  - "tests/: 173 tests"
fixed_this_batch:
  - "validate_qcm.py default project path now resolves to qcm-v3.0 root"
  - "validator expected version updated from stale 2.5.0 to 3.0.0"
  - "P01-P09 canonical stage IDs are recognized without false warnings"
boundary: "The .skill is a method package for AI collaboration and quality gates, not the formula runtime itself."
```

### L4 Mother-Package Integration Boundary

```yaml
upstream:
  P00_CONTROL_PLANE: "Routing, audit ledger, validation registry, scenario matrix"
  P01_GHOST_CHANNEL: "Authoritative protocol/SDK; P04 embedded SDK is snapshot/demo context"
downstream:
  P05_QSPECTRUM: "Platform brain/runtime can consume QCM as role/flywheel/sandbox reasoning pattern"
  USER_PACK: "Final delivery templates can cite QCM gates when packaging project work"
integration_principle: "QCM should guide general AI collaboration by making role, resonance, sandbox, and quality decisions explicit. It should not become an endless meta-system that prevents delivery."
```

## Knowledge Crystals

### KC-P04-001 — QCM Is A Collaboration Engine, Not A Replacement Model

```yaml
evidence_level: VERIFIED
statement: "P04 models how multiple AI roles coordinate and reach emergence. Its value is as a scaffold for general models to reason, validate, and collaborate, not as a standalone intelligence replacement."
implication: "Future AI should use QCM to structure work and checks, while still using the active general model for coding, reading, and judgment."
```

### KC-P04-002 — There Are Three Runnable Runtime Surfaces

```yaml
evidence_level: VERIFIED
surfaces:
  research_script: "02-代码编写/main.py and main_complete.py"
  package_cli: "python -m qcm.main"
  http_service: "qcm.main --mode service"
validation: "All three were smoke-tested on 2026-05-31."
implication: "A future audit should not stop at tests; it must also prove at least one real CLI mode and the service mode if API use is claimed."
```

### KC-P04-003 — 63 Is The Release Test Count, Not The Whole Guardrail Count

```yaml
evidence_level: VERIFIED
release_tests:
  test_qcm_all: 25
  paper_pytest: 38
  total: 63
extra_guards:
  config_sync: 4
  health_check: 6
  runtime_smoke: "research + production output + service API"
  skill_archive: "validator + 173 tests"
implication: "Do not collapse all checks into '63'. Use '63 release tests plus guards' when reporting current quality."
```

### KC-P04-004 — Cap-D And Cap-G Are Available But Default-Off

```yaml
evidence_level: VERIFIED
statement: "Cap-D CryptoEngine and Cap-G SelfHealer are wired into qcm/pipeline.py, but DEFAULT_CONFIG leaves them disabled unless flags/config enable them."
validation: "production --cap-crypto --cap-healer --max-rounds 12 initialized both capabilities and wrote output."
implication: "Docs and future agents should not say these are absent or always-on."
```

### KC-P04-005 — `--max-rounds` Is The Current CLI Contract

```yaml
evidence_level: VERIFIED
statement: "qcm/main.py exposes --max-rounds. Older docs that said --rounds were stale and have been aligned in operational docs."
implication: "Use module execution and current argparse flags in all future runbooks."
```

### KC-P04-006 — Production Mode Has A Real Write Side Effect

```yaml
evidence_level: VERIFIED
statement: "production mode writes JSON results to output.dir, defaulting to output."
audit_practice: "Use a temporary or explicit isolated output directory during audit."
implication: "Do not run production casually from repo root without deciding whether generated output is desired."
```

### KC-P04-007 — The qcm-v3.0 Skill Is A Quality Operating System

```yaml
evidence_level: VERIFIED
statement: "The .skill package contains 45 experts, 9 stages, 24 quality dimensions, sub-agent templates, validators, and templates. It is the portable operating method for AI review and delivery discipline."
validation: "Isolated extraction validator and tests both pass."
implication: "For future multi-agent review, activate this skill as a method layer and route concrete code/runtime checks back to the local repository."
```

### KC-P04-008 — P04 Should Feed P05 And P00, Not Float Alone

```yaml
evidence_level: INFERENCE_FROM_VERIFIED_STRUCTURE
statement: "P04's future value increases when its role/sandbox/flywheel concepts are connected to P00 routing/ledger and P05 runtime/platform brain."
next_use:
  - "P00 validation registry now includes P04 runtime and skill checks"
  - "P05 should later decide whether QCM signals become runtime metrics, route scores, or governance gates"
```

## Current Gaps And Risks

```yaml
gaps:
  - id: "P04-GAP-001"
    statement: "Service mode requires optional FastAPI/Pydantic/Uvicorn dependencies. Current local environment now has FastAPI installed, but portable setup still depends on INSTALL.md."
  - id: "P04-GAP-002"
    statement: "qcm-v3.0 .skill is a zip archive; small text drift inside it is less transparent than normal source files."
  - id: "P04-GAP-003"
    statement: "P04 embedded Ghost Channel SDK remains a snapshot/demo context; P01 is the authoritative protocol implementation."
risks:
  - id: "P04-RISK-001"
    statement: "Future AI may over-expand QCM meta-work instead of using it to stop rebuild loops."
    mitigation: "Treat runtime smoke + tests + validation registry PASS as a stop condition unless a new user goal requires deeper change."
```

## Recommended Next Use

```yaml
for_codex:
  - "Start in P00 routing/validation docs."
  - "Use P04 crystal to pick the correct entrypoint."
  - "Run qa_runner.py validate --scope P04_QCM before changing formula/runtime code."
  - "Run qa_runner.py validate --scope QCM_SKILL after editing the .skill archive."
  - "Use qcm-v3.0 skill as a review method, not as a reason to postpone delivery."
for_user:
  - "Use P04 as the proof-of-coordination layer when asking general AI models to collaborate on the mother package."
  - "Ask future agents to report '63 release tests plus guards' so test evidence remains honest."
```
