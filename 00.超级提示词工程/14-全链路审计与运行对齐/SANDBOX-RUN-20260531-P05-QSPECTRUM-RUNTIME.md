# Sandbox Run — 2026-05-31 P05 Q-SpecTrum Runtime

> Mode: six-round audit flywheel  
> Scope: `05.超极智脑_Q-SpecTrum`  
> Output: P05 runtime/API/MCP crystal plus fixes and validation evidence

## R1 — Intent And Boundary

```yaml
question: "Why does P05 exist inside the mother package?"
answer: "P05 is the local platform brain that lets general AI models operate the mother package through a real CLI, Web/API server, MCP bridge, memory layers, role routing, and closed-loop persistence."
boundary:
  in_scope:
    - "run.py CLI/status/query/web/e2e"
    - "api_server.py HTTP chat and management API"
    - "qspectrum_engine.py routing and runtime pipeline"
    - "qspectrum_mcp_server.py JSON-RPC stdio bridge"
    - "BRAIN-KB, platform.db, project/runtime memory boundary"
    - "Windows UTF-8 runnable user entrypoints"
  out_of_scope:
    - "claiming P05 replaces general AI models"
    - "treating structural verify-integration as full runtime validation"
    - "making DeerFlow a hard dependency when current local core works without it"
```

## R2 — Inventory And Reading

```yaml
observed_structure:
  p05_filtered_file_count: 423
key_reads:
  - "05.超极智脑_Q-SpecTrum/README.md"
  - "05.超极智脑_Q-SpecTrum/INDEX.md"
  - "05.超极智脑_Q-SpecTrum/AGENTS.md"
  - "05.超极智脑_Q-SpecTrum/智腦協議-BRAIN-PROTOCOL.md"
  - "05.超极智脑_Q-SpecTrum/run.py"
  - "05.超极智脑_Q-SpecTrum/api_server.py"
  - "05.超极智脑_Q-SpecTrum/qspectrum_engine.py"
  - "05.超极智脑_Q-SpecTrum/qspectrum_mcp_server.py"
  - "05.超极智脑_Q-SpecTrum/brain_core/mcp_router.py"
  - "05.超极智脑_Q-SpecTrum/closed_loop_core.py"
  - "05.超极智脑_Q-SpecTrum/project_memory.py"
  - "05.超极智脑_Q-SpecTrum/BRAIN-KB/**/INDEX.md"
```

## R3 — Runtime Reality

```yaml
entrypoints_verified:
  integration:
    command: "python verify-integration.py"
    result: "PASS with 1 warning for runtime-generated _HANDOFF/"
  status:
    command: "python run.py --status"
    result: "System ALL GREEN"
  query:
    command: "python run.py --query \"Research our competitors\""
    result: "ROLE-Q02 QCM Researcher"
  pytest:
    command: "pytest tests -q"
    result: "158 passed"
  e2e:
    command: "python run.py --e2e"
    result: "13 passed, 0 failed"
  api_smoke:
    command: "start run.py --web --provider mock on free port"
    result: "/api/status, /api/roles, /api/chat routes Q02/Q06/Q08"
  mcp_smoke:
    command: "qspectrum_mcp_server.py --provider mock with JSON-RPC stdin"
    result: "initialize/tools/resources/execute_chat/query_database OK"
registered_gate:
  command: "python qa_runner.py validate --scope P05_QSPECTRUM"
  result: "6/6 PASS, ALL CLEAR"
```

## R4 — Breakpoint Repair

```yaml
breakpoints_found:
  - id: "P05-BP-001"
    issue: "tests/test_regression.py required an already-running server, so pytest failed on clean workstations."
    fix: "Regression suite now starts a local mock API server, waits for /api/status, and terminates it at exit."
  - id: "P05-BP-002"
    issue: "Regression server stdout was captured but not drained, creating deadlock risk."
    fix: "Regression server child output now goes to DEVNULL."
  - id: "P05-BP-003"
    issue: "Consecutive chat requests slowed to ~11s after duplicate project result IDs left projects.db locked."
    fix: "ProjectOrchestrator record_result uses time.time_ns(); record_interaction/record_result close connections in finally."
  - id: "P05-BP-004"
    issue: "Windows GBK caused UnicodeDecodeError/UnicodeEncodeError in subprocess output and direct test scripts."
    fix: "run.py --e2e child env now sets UTF-8; direct scripts reconfigure stdout/stderr; subprocess capture uses UTF-8 replace."
  - id: "P05-BP-005"
    issue: "ghost_channel_adapter.py left .ghost_channel_key file handle unclosed."
    fix: "Key file read now uses with open(...)."
  - id: "P05-BP-006"
    issue: "decision_layer.py used deprecated datetime.utcnow() under Python 3.14."
    fix: "Use timezone-aware datetime.now(timezone.utc)."
  - id: "P05-BP-007"
    issue: "SYSTEM-PROMPT.md, QUICK-START.md, and README.md had drifted from current runtime and self-check expectations."
    fix: "Added current bootstrap capsule, quick-start method/step commands, and developer integration facts."
```

## R5 — Validation

```yaml
commands:
  - command: "python verify-integration.py"
    result: "PASS; DB, roles, scripts, KG, vector, MCP present; 1 _HANDOFF warning"
  - command: "python run.py --status"
    result: "PASS; System ALL GREEN"
  - command: "python run.py --query \"Research our competitors\""
    result: "PASS; ROLE-Q02 QCM Researcher"
  - command: "pytest tests/test_regression.py -q"
    result: "PASS; 12 passed after self-start/server-lock fixes"
  - command: "pytest tests -q"
    result: "PASS; 158 passed in 156.18s"
  - command: "python run.py --e2e"
    result: "PASS; 13 passed, 0 failed"
  - command: "python tests/test_ai_model.py"
    result: "PASS; all critical sections present"
  - command: "python tests/test_nontechnical.py"
    result: "PASS; prerequisites/methods/commands/steps recognized"
  - command: "python tests/test_developer.py"
    result: "PASS; documentation structure/code path/API/database checks recognized"
  - command: "API smoke via urllib"
    result: "PASS; status roles=15, roles total=15, Q02/Q06/Q08 routes"
  - command: "MCP smoke via subprocess stdio"
    result: "PASS; 5 JSON messages, 18 tools, no non-JSON stdout"
  - command: "python qa_runner.py validate --scope P05_QSPECTRUM"
    result: "PASS; 6/6 validation items; ALL CLEAR"
```

## R6 — Synthesis Gate

```yaml
decision: "P05 can now be treated as runnable for local CLI status/query, pytest suite, Q-SpecTrum E2E scripts, HTTP API smoke, and MCP stdio smoke. Runtime side effects are understood and registered."
do_not_claim:
  - "verify-integration.py alone proves full runtime behavior."
  - "API/MCP smoke is read-only."
  - "DeerFlow is installed locally."
  - "External ChromaDB Python 3.14 deprecation warning is fixed by this repository."
  - "P05 replaces the active general AI model."
next_batch: "Batch chain B6-B7 is now completed; future P05 work should be triggered by failing validation or a real platform-brain integration sample."
```
