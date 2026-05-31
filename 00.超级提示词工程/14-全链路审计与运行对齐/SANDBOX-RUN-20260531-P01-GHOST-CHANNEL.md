# Sandbox Run — 2026-05-31 P01 Ghost Channel

> Mode: six-round audit flywheel  
> Scope: `01.通讯协议_幽灵通道`  
> Output: protocol/SDK/deployment crystal plus fixes and validation evidence

## R1 — Intent And Boundary

```yaml
question: "What is P01 for inside the mother package?"
answer: "It is the communication/protocol and SDK delivery subsystem, not the universal AI replacement and not the whole mother runtime."
boundary:
  in_scope:
    - protocol core
    - lightweight Python SDK
    - TypeScript SDK
    - enterprise GhostHub SDK
    - deployment and commercial package
  out_of_scope:
    - claiming all future production deployments are validated without Docker
    - treating P01 as P04 QCM or P05 Q-SpecTrum authority
```

## R2 — Inventory And Reading

```yaml
observed_structure:
  root_files: ["README.md", "INDEX.md", "MANIFEST.yaml", "VERIFY.ps1", "LICENSE"]
  top_level_dirs:
    - "00_总览"
    - "01_核心成功与战略"
    - "02_学术研究与协议"
    - "03_SDK与集成"
    - "04_企业部署"
    - "05_商业化与市场"
    - "06_行业指引"
    - "07_交付与验收"
file_count_observed: 296
key_reads:
  - "README.md"
  - "INDEX.md"
  - "00_总览/PROJECT_HANDOFF.md"
  - "VERIFY.ps1"
  - "three pyproject.toml files"
  - "Python SDK source/test AST surface"
  - "TypeScript package/source/test surface"
  - "Dockerfiles and docker-compose files"
```

## R3 — Code And Runtime Reality

```yaml
protocol_layer:
  tests: "18/18 PASS"
  core: ["CryptoEngine", "DeltaCalculator", "VectorClock", "MerkleTree", "AuditLogger", "GhostChannel"]
lightweight_python_sdk:
  tests: "68/68 PASS"
  core: ["GhostChannelSDK", "schema_validator", "AESGCMBackend", "AckMessage", "SnapshotRecord"]
enterprise_sdk:
  tests: "76/76 PASS"
  core: ["GhostHubSDK", "IntentionBankComponent", "NoUIAdapterComponent", "AgentFederationComponent", "GhostHubWorkflowEngine"]
typescript_sdk:
  initial_state: "npm test failed because Node could not load .ts files"
  fixed_state: "22/22 PASS using node --experimental-strip-types --test on Node 22"
```

## R4 — Breakpoint Repair

```yaml
breakpoints_found:
  - id: "P01-BP-001"
    issue: "Python example imported GhostChannelSDK from stale ghost_channel namespace."
    fix: "Import ghost_channel_sdk instead."
  - id: "P01-BP-002"
    issue: "100-concurrent stress script imported GhostChannelSDK from stale ghost_channel namespace."
    fix: "Import ghost_channel_sdk and rerun 2500-sync stress."
  - id: "P01-BP-003"
    issue: "TypeScript npm test did not know how to execute .ts files."
    fix: "Use Node 22 type stripping and node:22-slim Docker image."
  - id: "P01-BP-004"
    issue: "Root deployment compose had wrong TS Dockerfile context and wrong schema-validator namespace."
    fix: "Corrected build contexts and schema-validator import."
  - id: "P01-BP-005"
    issue: "Commercial deployment compose referenced nonexistent ghost_hub_sdk.worker and Dockerfile tried app.run on FastAPI."
    fix: "Removed nonexistent worker and changed API startup to uvicorn."
  - id: "P01-BP-006"
    issue: "Manifest hashes became stale after real fixes."
    fix: "Updated MANIFEST.yaml and reran VERIFY.ps1."
  - id: "P01-BP-007"
    issue: "Standalone TypeScript example imported ../typescript/src/index.js although the source file is index.ts."
    fix: "Changed the example import to ../typescript/src/index.ts and verified it with node --experimental-strip-types."
  - id: "P01-BP-008"
    issue: "Commercial Docker deployment guide still instructed users to scale nonexistent ghost-hub-sdk-worker service."
    fix: "Replaced worker scaling instruction with capacity-planning boundary text."
  - id: "P01-BP-009"
    issue: "RFC and generated delivery HTML still contained stale `from ghost_channel import GhostChannelSDK` snippets."
    fix: "Aligned lightweight SDK snippets to `ghost_channel_sdk` and verified the stale-import scan is clean for markdown/html/python/typescript files."
  - id: "P01-BP-010"
    issue: "Delivered TypeScript example under 07_交付文档 pointed to a nonexistent index.js path."
    fix: "Changed it to the real cross-folder index.ts path and verified it with node --experimental-strip-types."
```

## R5 — Validation

```yaml
commands:
  - command: "python examples/python_memory_sync_example.py"
    result: "PASS; SyncResult(success=True)"
  - command: "python stress_test_100_concurrent.py"
    result: "PASS; 2500/2500 successful; P99 2.88ms; bandwidth 99.4%; consistency 100%"
  - command: "npm test"
    result: "PASS; 22/22 TypeScript tests"
  - command: "node --experimental-strip-types examples/typescript_memory_sync_example.ts"
    result: "PASS; returns success object"
  - command: "node --experimental-strip-types 07_交付与验收/07_交付文档/examples/typescript/memory_sync_example.ts"
    result: "PASS; returns success object"
  - command: "rg stale lightweight-SDK import/path patterns in P01 md/html/py/ts"
    result: "PASS; no matches"
  - command: "powershell -ExecutionPolicy Bypass -File VERIFY.ps1"
    result: "PASS; 299 checked; 295 verified; 4 optional binaries skipped; 0 failed; 0 missing"
  - command: "python qa_runner.py validate --scope P01_GHOST_CHANNEL"
    result: "PASS; 2/2 validation items; SDK total 184 passed"
external_gap:
  - "Docker command is unavailable in this machine, so compose build/up remains pending external validation."
```

## R6 — Synthesis Gate

```yaml
decision: "P01 can be treated as currently runnable for local SDK scenarios and integrity validation."
do_not_claim:
  - "Docker production deployment has been run end-to-end here."
  - "TypeScript SDK has production crypto parity with Python."
  - "P01 alone is the mother-package runtime."
next_batch: "Batch chain B3-B7 is now completed; future P01 work should be triggered by failing validation or a real integration sample."
```
