# Sandbox Run — 2026-05-31 P03 WorkBuddy Knowledge Base

> Mode: six-round audit flywheel  
> Scope: `03.数据库管理_文件夹整理AI应用`  
> Output: knowledge/search/MCP runtime crystal plus fixes and validation evidence

## R1 — Intent And Boundary

```yaml
question: "What is P03 for inside the mother package?"
answer: "It is the runnable knowledge workbench that lets a human or AI search, browse, route, index, remember, and process local project knowledge."
boundary:
  in_scope:
    - Flask/Web/REST/CLI entrypoint
    - MCP stdio tool server
    - local search and vector index
    - MemoryOS runtime memory
    - file processing and batch import
    - agent/model orchestration scaffolding
  out_of_scope:
    - replacing the general AI model
    - claiming ChromaDB/FTS5/HNSW as current runtime
    - treating derived DB/FAISS caches as hand-authored authority
    - claiming external model API validation without .env/API keys
```

## R2 — Inventory And Reading

```yaml
observed_structure:
  filtered_file_count: 153
  root_files:
    - "README.md"
    - "INDEX.md"
    - "AGENTS.md"
    - "API文档.md"
    - "app.py"
    - "mcp_server.py"
    - "batch_import.py"
    - "verify_install.py"
  major_dirs:
    - ".workbuddy/scripts"
    - ".workbuddy/记忆层"
    - ".workbuddy/AI协作体系"
    - ".workbuddy/templates"
    - "05-知识沉淀/wiki"
    - "tests"
key_reads:
  - "README.md / AGENTS.md / INDEX.md"
  - "app.py"
  - "mcp_server.py"
  - ".workbuddy/scripts/vector_search.py"
  - ".workbuddy/scripts/search_content.py"
  - ".workbuddy/scripts/update_index.py"
  - ".workbuddy/scripts/auto_organizer.py"
  - ".workbuddy/记忆层/memoryos.py"
  - ".workbuddy/scripts/model_adapter.py"
  - ".workbuddy/scripts/agent_orchestrator.py"
  - "tests/test_mcp_integration.py"
  - "tests/test_vector_search.py"
```

## R3 — Code And Runtime Reality

```yaml
web_runtime:
  entrypoint: "app.py"
  core_routes: ["/", "/search", "/browse/", "/ingest", "/memory", "/maintain", "/api/search", "/api/index"]
  bootstrap_side_effect: "default app startup may create demo files and rebuild index"
mcp_runtime:
  server: "db-knowledge"
  tools: 20
  dispatch: "TOOL_DEFINITIONS and HANDLERS are checked by tests"
search_runtime:
  sqlite: ".workbuddy/index/search_index.db"
  faiss: "IndexFlatL2 + IndexIDMap when optional vector deps are available"
  fallback: "SQLite LIKE and file scan keyword search"
memory_runtime:
  short_term: "daily JSONL"
  mid_term: "per-type JSON"
  long_term: "profile/knowledge/strategies JSON"
tests_before_fixes:
  direct_pytest: "101 passed, 2 failed, 3 warnings"
  failure: "MCP integration UnicodeDecodeError from subprocess stdout decoding/protocol pollution"
```

## R4 — Breakpoint Repair

```yaml
breakpoints_found:
  - id: "P03-BP-001"
    issue: "MCP tool handlers allowed internal print output to leak to stdout, corrupting stdio JSON-RPC and causing UnicodeDecodeError in integration tests."
    fix: "Force UTF-8 stream configuration and wrap handler execution with redirect_stdout(sys.stderr)."
  - id: "P03-BP-002"
    issue: "Web /browse used string prefix checking and could allow same-prefix path escape."
    fix: "Resolve base/current and enforce current.relative_to(base)."
  - id: "P03-BP-003"
    issue: "batch_import.py passed string paths into Path-oriented AutoOrganizer and read ContentInsight as dict."
    fix: "Pass Path objects, read dataclass attributes, and count success by `executed`."
  - id: "P03-BP-004"
    issue: "vector_search tests deleted/wrote the real workspace search_index.db and could pollute derived cache evidence."
    fix: "Monkeypatch vector_search WORKSPACE/INDEX_DIR/DB_PATH/FAISS_PATH to pytest temp paths."
  - id: "P03-BP-005"
    issue: "Docs claimed ChromaDB, SQLite FTS5, HNSW, weighted fusion, and old CLI options as current facts."
    fix: "Aligned API, INDEX, FRAMEWORK, wiki concepts, MemoryOS config/docs, and MCP entity docs to current runtime reality."
```

## R5 — Validation

```yaml
commands:
  - command: "python -m pytest tests/test_app_web.py -q"
    result: "PASS; 2 passed"
  - command: "python -m pytest tests/test_mcp_integration.py::test_mcp_content_tools tests/test_mcp_integration.py::test_mcp_rebuild_index -q"
    result: "PASS; 2 passed"
  - command: "python -m pytest tests/test_batch_import.py tests/test_vector_search.py tests/test_app_web.py -q"
    result: "PASS; 10 passed, 3 warnings"
  - command: "python -m pytest tests -q"
    result: "PASS; 107 passed, 3 warnings"
  - command: "python verify_install.py"
    result: "PASS; 23 pass, 0 fail, 1 .env warning; 107 tests collected"
  - command: "python qa_runner.py validate --scope P03_WORKBUDDY_KB"
    result: "PASS; 2/2 validation items; ALL CLEAR"
```

## R6 — Synthesis Gate

```yaml
decision: "P03 can now be treated as currently runnable for local knowledge workbench, MCP smoke/integration, search/index, and sandbox model-adapter scenarios."
do_not_claim:
  - "External AI provider calls are validated without .env/API keys."
  - "ChromaDB, FTS5, HNSW, RRF, or weighted fusion are implemented current runtime."
  - "Search DB rows are canonical if source markdown disagrees."
  - "Maintenance/backup full side effects are covered by quick MCP integration tests."
next_batch: "Batch chain B4-B7 is now completed; future P03 work should be triggered by failing validation or a real knowledge/search integration sample."
```
