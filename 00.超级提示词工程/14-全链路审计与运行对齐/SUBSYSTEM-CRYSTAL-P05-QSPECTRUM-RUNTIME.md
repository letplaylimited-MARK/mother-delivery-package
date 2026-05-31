# Subsystem Crystal — P05 Q-SpecTrum Runtime

> Batch: B5_P05_QSPECTRUM_RUNTIME  
> Scope: `05.超极智脑_Q-SpecTrum`  
> Status: VERIFIED current after pytest, E2E, API smoke, MCP smoke, CLI status, and integration verification  
> Purpose: Preserve executable understanding of Q-SpecTrum as the mother package's platform brain/runtime layer.

## Executive Crystal

```yaml
id: KC-P05-EXEC-001
scope: P05_QSPECTRUM_RUNTIME
evidence_level: VERIFIED
statement: "P05 is the integrated runtime brain: CLI, Web/API chatroom, MCP stdio bridge, role routing, platform DB access, BRAIN-KB memory orchestration, Ghost Channel adapter, scenario engine, closed-loop persistence, and user-facing onboarding docs."
why_it_matters: "The user's intention is not to replace general AI models. P05 gives a general model a runnable operating environment, memory/control surface, and API/MCP access so the mother folder can coordinate real project development instead of endlessly generating disconnected documents."
current_validation:
  - "python qa_runner.py validate --scope P05_QSPECTRUM -> 6/6 PASS"
  - "pytest tests -q -> 158 passed"
  - "python run.py --e2e -> 13 passed, 0 failed"
  - "python verify-integration.py -> PASS with 1 runtime _HANDOFF warning"
  - "python run.py --status -> System ALL GREEN"
  - "python run.py --query \"Research our competitors\" -> ROLE-Q02 QCM Researcher"
  - "API smoke -> /api/status roles=15, /api/roles total=15, chat routes Q02/Q06/Q08"
  - "MCP smoke -> JSON-RPC only stdout, 18 tools, execute_chat, status resource, SQL count ai_roles=15"
```

## Layer Map

### L1 Human CLI Entrypoint: `run.py`

```yaml
purpose: "Single local command surface for status, query, web server, E2E, guide, and interactive chat."
commands:
  - "python run.py --status"
  - "python run.py --query \"Research our competitors\""
  - "python run.py --web --provider mock --port <port>"
  - "python run.py --e2e"
verified_behavior:
  - "Status reports DB 40 tables / 85 rows, 15 roles, 10 protocols, 4 workflows, 7 agents."
  - "Query routes English research intent to ROLE-Q02."
  - "E2E child scripts now inherit UTF-8 environment on Windows."
side_effects:
  - "query/chat can write runtime DB state through closed-loop/project/task/resource layers."
```

### L2 Web/API Runtime: `api_server.py`

```yaml
purpose: "Standard-library HTTP API and static chat UI bridge to QSpectrumEngine."
server:
  default_host: "127.0.0.1"
  default_port: 8765
  auth: "Optional QSPECTRUM_API_TOKEN bearer token; disabled by default for localhost tool mode."
verified_routes:
  - "GET /api/status"
  - "GET /api/roles"
  - "POST /api/chat"
  - "POST /api/negotiate"
  - "POST /api/memory/append"
validation_note: "Regression tests now self-start a mock API server instead of requiring a manually running server."
```

### L3 Engine Core: `qspectrum_engine.py`

```yaml
purpose: "Actual Q-SpecTrum pipeline: input -> Secretary route -> knowledge -> prompt -> LLM/provider -> closed-loop persistence -> response."
core_components:
  - "QSpectrumDB: immutable read of AI项目管理/Platform/db/platform.db"
  - "Secretary: role routing"
  - "KnowledgeResonance and KnowledgeOrchestrator: retrieval"
  - "GhostChannelAdapter/Gate: nervous system and tier checks"
  - "ScenarioEngine, task manager, project memory, resource/result/decision layers"
  - "ProjectOrchestrator and KnowledgePipeline: runtime closed-loop state"
fixed_this_batch:
  - "ProjectOrchestrator.record_result now uses time.time_ns() IDs instead of second-level timestamps."
  - "ProjectOrchestrator record_interaction/record_result now close SQLite connections in finally blocks."
runtime_effect: "Consecutive /api/chat calls no longer hit projects.db lock contention or 10-second SQLite waits."
```

### L4 MCP Runtime: `qspectrum_mcp_server.py`

```yaml
purpose: "JSON-RPC stdio bridge exposing Q-SpecTrum to tool-capable AI clients."
verified_capabilities:
  - "initialize"
  - "tools/list -> 18 tools"
  - "resources/read qspectrum://status"
  - "tools/call execute_chat"
  - "tools/call query_database with SELECT-only guard"
protocol_boundary: "stdout must remain JSON-RPC only; logs on stderr are acceptable. Current smoke observed no non-JSON stdout."
write_boundary: "query_database is SELECT-only, but other tools such as execute_chat and graph_connect may produce runtime side effects."
```

### L5 Memory And Authority

```yaml
authority_order:
  BRAIN_KB: "P0 operational knowledge and decisions"
  project_memory_db: "P1 project/chatroom working memory"
  runtime_dbs: "P2 support stores such as projects.db, user_resources.db, task_manager.db, knowledge_pipeline.db"
  platform_db: "Authoritative role/protocol/workflow DB read immutably from AI项目管理/Platform/db/platform.db"
handoff:
  _HANDOFF: "Runtime-generated session state; warn if absent/present, but not a git-tracked source of truth."
side_effect_rule: "Status/integration checks are mostly read-only; chat/API/E2E smoke can write runtime state and must clean explicit test MEMORY.md entries."
```

## Knowledge Crystals

### KC-P05-001 — P05 Is The Runnable Platform Brain

```yaml
evidence_level: VERIFIED
statement: "P05 is the mother package layer where role routing, memory, API, MCP, and closed-loop persistence actually run."
implication: "Future agents should use P05 to operate and test the system, not only to read prompt files."
```

### KC-P05-002 — Runtime Verification Must Include More Than `verify-integration.py`

```yaml
evidence_level: VERIFIED
statement: "verify-integration.py is structural. It checks files, DB presence, KG/vector imports, and archive state, but does not prove chat/API/MCP behavior."
minimum_runtime_gate:
  - "pytest tests -q"
  - "python run.py --e2e"
  - "API smoke"
  - "MCP stdio smoke"
  - "run.py --status"
```

### KC-P05-003 — The Projects DB Lock Was A Real Runtime Breakpoint

```yaml
evidence_level: VERIFIED
symptom: "Regression API tests initially timed out; direct profiling showed ~11s per chat after rapid consecutive interactions."
root_cause: "record_result generated duplicate second-level result_id values and did not guarantee SQLite connection close on exceptions, leaving projects.db locked."
fix: "Use time.time_ns() for result IDs and close connections in finally blocks."
validation: "Consecutive engine/API calls now complete around 0.1s; regression and full pytest pass."
```

### KC-P05-004 — Windows UTF-8 Is A First-Class Delivery Boundary

```yaml
evidence_level: VERIFIED
statement: "Several P05 user-facing scripts printed checkmark/cross symbols or read subprocess output. Without UTF-8 hardening, Windows GBK caused UnicodeEncodeError/UnicodeDecodeError."
fixes:
  - "run.py --e2e sets PYTHONUTF8 and PYTHONIOENCODING for child scripts."
  - "test_ai_model.py, test_developer.py, test_nontechnical.py, test_regression.py, and test_server_startup.py reconfigure stdout/stderr."
  - "test_nontechnical.py captures run.py --help with encoding='utf-8', errors='replace'."
```

### KC-P05-005 — SYSTEM-PROMPT Is Now A Current Bootstrap Capsule

```yaml
evidence_level: VERIFIED
statement: "SYSTEM-PROMPT.md had drifted to a legacy archive notice while E2E still expected it to onboard a fresh AI model. It now contains a concise current bootstrap capsule with roles, routing, memory, runtime commands, and scenarios."
implication: "Fresh AI model handoff can start from SYSTEM-PROMPT.md without immediately falling into legacy-only mode."
```

### KC-P05-006 — API And MCP Are Complementary, Not Equivalent

```yaml
evidence_level: VERIFIED
statement: "API validates browser/HTTP user flows; MCP validates tool-client integration over JSON-RPC stdio. Both must be tested because they fail differently."
current_evidence:
  API: "status/roles/chat routes Q02/Q06/Q08"
  MCP: "tools/resources/chat/SQL via JSON-RPC with clean stdout"
```

### KC-P05-007 — P05 Consumes Other Subsystems But Does Not Own Them

```yaml
evidence_level: INFERENCE_FROM_VERIFIED_STRUCTURE
boundaries:
  P00: "Control plane, validation registry, ledger, routing/governance."
  P01: "Authoritative Ghost Channel protocol/SDK source."
  P03: "WorkBuddy KB/search/MCP file-governance subsystem."
  P04: "QCM role/flywheel/sandbox method layer."
  P05: "Runtime brain that can integrate these ideas and expose them through CLI/API/MCP."
```

## Current Gaps And Risks

```yaml
gaps:
  - id: "P05-GAP-001"
    statement: "DeerFlow directory is not present locally; P05 reports this as a warning while keeping core system green."
  - id: "P05-GAP-002"
    statement: "run.py --e2e still surfaces an external ChromaDB Python 3.14 deprecation warning; this is dependency-side, not current P05 code failure."
  - id: "P05-GAP-003"
    statement: "Some runtime DBs are intentionally writable in repo root when the workspace is writable; audits should distinguish runtime state from source truth."
risks:
  - id: "P05-RISK-001"
    statement: "Future agents may treat structural PASS as full runtime PASS."
    mitigation: "Use VAL-05-PYTEST, VAL-05-E2E, VAL-05-API-SMOKE, and VAL-05-MCP-SMOKE as stop gates."
  - id: "P05-RISK-002"
    statement: "MCP execute_chat and API chat are not read-only."
    mitigation: "Mark side effects before smoke tests; use mock provider and controlled test entries."
```

## Recommended Next Use

```yaml
for_codex:
  - "Run python qa_runner.py validate --scope P05_QSPECTRUM before changing runtime/API/MCP behavior."
  - "Use run.py --status for fast operator confidence, then pytest/E2E/API/MCP for delivery confidence."
  - "Keep platform.db immutable and treat BRAIN-KB/project memory/runtime DBs according to MEMORY-SOURCE-INDEX.yaml authority."
for_user:
  - "Use P05 as the actual local operating brain when pairing Codex with other general AI models."
  - "Use API for browser/tool workflows and MCP for model/tool-client workflows."
  - "Stop rebuilding when the registered P05 gates pass unless a new concrete use case fails."
```
