# Subsystem Crystal — P03 WorkBuddy Knowledge Base

> Batch: B3_P03_WORKBUDDY_KB  
> Scope: `03.数据库管理_文件夹整理AI应用`  
> Status: VERIFIED current, with explicit external/API-key boundaries  
> Purpose: Preserve executable understanding of the knowledge/search/MCP runtime for future Codex / AI handoff.

## Executive Crystal

```yaml
id: KC-P03-EXEC-001
scope: P03_WORKBUDDY_KB
evidence_level: VERIFIED
statement: "P03 is the runnable WorkBuddy knowledge workbench: Flask/Web/REST, MCP stdio tools, file organization pipeline, local search index, MemoryOS runtime memory, and AI role/model orchestration scaffolding."
why_it_matters: "This subsystem turns the mother package's knowledge folders into something a general AI model can query, browse, route, index, and maintain. It should support AI collaboration; it is not intended to replace the general model."
current_validation:
  - "python verify_install.py -> 23 pass, 0 fail, 1 optional .env warning; 107 tests collected"
  - "python -m pytest tests -q -> 107 passed, 3 warnings"
  - "python qa_runner.py validate --scope P03_WORKBUDDY_KB -> 2/2 PASS"
  - "Focused regressions: app browse boundary, MCP stdio JSON-RPC integrity, batch_import Path handling, vector_search test isolation"
```

## Layer Map

### L1 Web / REST / CLI Entrypoint: `app.py`

```yaml
entrypoint: "03.数据库管理_文件夹整理AI应用/app.py"
routes:
  - "/"
  - "/search"
  - "/browse/"
  - "/ingest"
  - "/memory"
  - "/maintain"
  - "/api/search"
  - "/api/index"
cli:
  - "python app.py --cli search <query>"
  - "python app.py --port 5000"
side_effects:
  - "default startup bootstrap may create demo files and rebuild search index"
  - "/api/index and /maintain write derived index/maintenance outputs"
fixed_this_batch:
  - "browse() now uses Path.relative_to() after resolving the wiki base, preventing same-prefix path escape such as ../wiki_evil"
  - "tests/test_app_web.py covers allowed wiki browse and forbidden escape"
boundary: "The browse route intentionally exposes only `05-知识沉淀/wiki/`, not the full workspace."
```

### L2 MCP Server: `mcp_server.py`

```yaml
entrypoint: "03.数据库管理_文件夹整理AI应用/mcp_server.py"
server_name: "db-knowledge"
transport: "stdio"
tools: 20
core_tool_groups:
  search:
    - "search_all"
    - "vector_search"
    - "search_memory"
    - "keyword_search"
  content_pipeline:
    - "analyze_content"
    - "route_content"
    - "process_file"
    - "run_file_pipeline"
    - "project_decision_workflow"
    - "extract_docx_text"
  maintenance:
    - "get_status"
    - "rebuild_index"
    - "run_maintenance"
    - "run_backup"
  monitoring_workflow:
    - "get_graph"
    - "watch_inbox"
    - "get_content_stats"
    - "enhanced_scan_inbox"
    - "analyze_project_relationships"
    - "run_workflow"
fixed_this_batch:
  - "sys.stdout/sys.stderr are reconfigured to UTF-8 with replacement"
  - "tool handler debug stdout is redirected to stderr so stdout remains valid JSON-RPC"
boundary: "MCP stdout must be reserved for protocol frames. Any future script prints during tool execution must not leak to stdout."
```

### L3 Scripts And Pipelines

```yaml
scripts_dir: "03.数据库管理_文件夹整理AI应用/.workbuddy/scripts"
important_runtime_scripts:
  - "vector_search.py: SQLite metadata + FAISS IndexFlatL2 semantic search, keyword fallback"
  - "search_content.py: workspace file-name/content keyword scan"
  - "update_index.py: scan core folders, update AGENTS.md timestamps, rebuild search index"
  - "auto_organizer.py: analyze -> route -> move/rename -> index -> MemoryOS record"
  - "file_processing_pipeline.py: read/understand/coexistence/naming/report pipeline"
  - "project_decision_workflow.py: project boundary and decision workflow"
  - "agent_orchestrator.py: agent/role loading and model-adapter execution"
  - "model_adapter.py: sandbox-safe model calls plus optional OpenAI/Anthropic/Zhipu/Yi clients"
fixed_this_batch:
  - "batch_import.py now passes Path objects to AutoOrganizer.process_and_store"
  - "batch_import.py now uses returned `executed` and ContentInsight attributes correctly"
  - "tests/test_batch_import.py covers import and preview behavior"
boundary: "Scripts are not one unified CLI. Some scripts are library-style; API文档.md now documents actual current command surfaces."
```

### L4 Knowledge, Memory, And Derived Caches

```yaml
authority_sources:
  wiki_static_knowledge: "05-知识沉淀/wiki/"
  memory_index_doc: ".workbuddy/记忆层/MEMORY.md"
  memory_runtime_data: ".workbuddy/记忆层/memory_data/ (gitignored runtime state)"
  ai_collaboration_rules: "AGENTS.md and .workbuddy/AI协作体系/"
derived_caches:
  sqlite_search_db: ".workbuddy/index/search_index.db"
  faiss_index: ".workbuddy/index/vectors.faiss or TEMP/km_vectors.faiss on non-ASCII Windows paths"
current_search_reality:
  - "FAISS uses IndexFlatL2 + IndexIDMap, not HNSW"
  - "keyword fallback uses SQLite LIKE and/or file scanning, not SQLite FTS5"
  - "ChromaDB is not an installed runtime dependency and should not be claimed as current implementation"
fixed_this_batch:
  - "MemoryOS config no longer claims ChromaDB is enabled"
  - "wiki/API/FRAMEWORK docs now distinguish current implementation from future extensions"
  - "tests/test_vector_search.py uses temporary workspace/index paths and no longer deletes or pollutes the real search_index.db"
```

## Eight Knowledge Crystals

### KC-P03-001 — P03 Is The Runnable KB App, P02 Is The Template

```yaml
evidence_level: VERIFIED
statement: "P03 contains the runnable V2 knowledge workbench with app.py, MCP server, scripts, tests, templates, runtime index, and MemoryOS. P02 should remain the lightweight Universal-KB template unless explicitly promoted."
implication: "For real knowledge/search/MCP testing, route to P03. For reusable scaffold generation, route to P02."
```

### KC-P03-002 — Search Index Is A Derived Cache

```yaml
evidence_level: VERIFIED
statement: "search_index.db and FAISS files are generated runtime artifacts, not hand-authored knowledge authority."
authority_order:
  - "wiki markdown and source documents"
  - "AGENTS/MEMORY/AI collaboration docs"
  - "runtime MemoryOS data when validating current local state"
  - "search DB / FAISS only as rebuildable cache"
implication: "Future AI should not treat stale DB rows as canonical if markdown/source files disagree."
```

### KC-P03-003 — MCP Stdio Has A Hard Protocol Boundary

```yaml
evidence_level: VERIFIED
breakpoint: "Full pytest initially failed 2 MCP integration tests with UnicodeDecodeError because tool-side prints polluted stdout."
fix: "mcp_server.py forces UTF-8 streams and redirects handler stdout to stderr."
validation: "python -m pytest tests/test_mcp_integration.py::test_mcp_content_tools tests/test_mcp_integration.py::test_mcp_rebuild_index -q -> 2 passed"
implication: "MCP tool handlers may log, but must not write non-protocol bytes to stdout."
```

### KC-P03-004 — Web Browse Must Stay Inside Wiki

```yaml
evidence_level: VERIFIED
breakpoint: "The old string-prefix path check could be bypassed by same-prefix folders such as wiki_evil."
fix: "browse() now resolves base/current and enforces current.relative_to(base)."
validation: "tests/test_app_web.py -> 2 passed"
implication: "Future browse expansion must use Path ancestry checks, not string prefix checks."
```

### KC-P03-005 — Batch Import Is A Real Mutating Entrypoint

```yaml
evidence_level: VERIFIED
breakpoint: "batch_import.py passed str(file_path) into a Path-oriented AutoOrganizer pipeline and read ContentInsight as a dict."
fix: "Pass Path objects, read dataclass attributes, and count success via `executed`."
validation: "tests/test_batch_import.py -> 2 passed"
boundary: "batch_import.py can move files and write indexes/memory. Use a copy or dry-run style workflow before production imports."
```

### KC-P03-006 — Tests Now Prove More, But Not Everything

```yaml
evidence_level: VERIFIED_WITH_GAPS
current: "107 passed, 3 warnings"
covered:
  - "MCP definition and integration smoke"
  - "vector search/index primitives"
  - "file processing pipeline"
  - "project decision workflow"
  - "model adapter sandbox behavior"
  - "agent orchestrator"
  - "Flask browse boundary"
  - "batch import adapter behavior"
not_fully_covered:
  - "run_maintenance/run_backup full side effects"
  - "successful real process_file/run_file_pipeline over production files"
  - "external model API calls because .env/API keys are optional and absent"
  - "large-scale search performance"
```

### KC-P03-007 — Docs Must Separate Current Runtime From Roadmap

```yaml
evidence_level: VERIFIED
statement: "ChromaDB, SQLite FTS5, HNSW, weighted fusion, and advanced CLI options existed in documents/specs, but not in current runtime code."
fix_refs:
  - "INDEX.md"
  - "API文档.md"
  - ".workbuddy/FRAMEWORK.md"
  - "05-知识沉淀/wiki/entities/MCP-Server.md"
  - "05-知识沉淀/wiki/concepts/向量语义搜索.md"
  - "05-知识沉淀/wiki/concepts/混合检索.md"
  - "05-知识沉淀/wiki/concepts/记忆层级.md"
implication: "Future agents should read current code/validation before inheriting historical roadmap language."
```

### KC-P03-008 — Best Use Pattern For General AI Collaboration

```yaml
best_use:
  - "Use Flask/Web when a human wants to browse/search/index locally."
  - "Use MCP when a model or agent client needs tool access to search, memory, routing, and workflow functions."
  - "Use `.workbuddy/scripts` directly for controlled maintenance, search, routing, and batch processing."
  - "Use MemoryOS for local episodic/semantic/procedural memory, while treating `.workbuddy/记忆层/MEMORY.md` as the hand-authored memory index."
  - "Use P03 as the runnable knowledge workbench behind the mother package's secretary/routing layer; do not make it the whole mother brain."
```

## Operational Commands

```powershell
cd <mother-delivery-package>\03.数据库管理_文件夹整理AI应用
python verify_install.py
python -m pytest tests -q
python app.py --port 5000
python mcp_server.py
python batch_import.py <目录路径>
```

## Remaining Honest Gaps

1. `.env` is not configured, so external model provider calls are not validated in this machine.
2. `run_maintenance` and `run_backup` are intentionally not fully exercised in the MCP integration suite because they are long/mutating operations.
3. ChromaDB/FTS5/HNSW/RRF are not current runtime facts; they remain roadmap or historical design language where found under `docs/superpowers`.
4. Full browser visual QA of the Flask UI was not started in this batch; Flask route behavior was tested via the test client.
