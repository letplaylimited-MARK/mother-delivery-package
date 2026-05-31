# Subsystem Crystal — P01 Ghost Channel

> Batch: B2_P01_GHOST_CHANNEL  
> Scope: `01.通讯协议_幽灵通道`  
> Status: VERIFIED current, not "all future production scenarios guaranteed"  
> Purpose: Preserve the executable understanding of the Ghost Channel subsystem for future Codex / AI handoff.

## Executive Crystal

```yaml
id: KC-P01-EXEC-001
scope: P01_GHOST_CHANNEL
evidence_level: VERIFIED
statement: "P01 is a four-layer delivery subsystem: protocol core, lightweight SDK, enterprise orchestration SDK, and deployment/commercial delivery assets."
why_it_matters: "It is the communication/protocol substrate that lets the mother package discuss multi-agent memory sync, causal workflow state, AI workflow orchestration, and commercial deployment without confusing those layers."
current_validation:
  - "powershell -ExecutionPolicy Bypass -File VERIFY.ps1 -> 299 checked; 295 verified; 4 optional binary artifacts skipped; 0 failed; 0 missing"
  - "python qa_runner.py validate --scope P01_GHOST_CHANNEL -> 2/2 PASS"
  - "VAL-01-SDK-TESTS -> 184 passed, 0 failed, 0 errors"
  - "python examples/python_memory_sync_example.py -> SyncResult(success=True)"
  - "python stress_test_100_concurrent.py -> 2500/2500 syncs, 100% success, P99 2.88ms, avg bandwidth reduction 99.4%"
  - "npm test -> 22/22 TypeScript tests PASS on Node 22"
  - "node --experimental-strip-types examples/typescript_memory_sync_example.ts -> SyncResult-like success object"
```

## Layer Map

### L1 Protocol Core: `ghost_channel`

```yaml
package_path: "03_SDK与集成/02_开源社区包/ghost_channel开源库"
import_namespace: "ghost_channel"
package_name: "ghost-channel"
tests: "18/18 PASS"
core_files:
  - "src/ghost_channel/core/crypto.py"
  - "src/ghost_channel/core/delta.py"
  - "src/ghost_channel/core/vector_clock.py"
  - "src/ghost_channel/core/merkle.py"
  - "src/ghost_channel/core/audit.py"
  - "src/ghost_channel/core/protocol.py"
meaning: "This is the authoritative low-level protocol layer: AES-GCM crypto, delta payloads, vector-clock causality, Merkle integrity, audit trail, and GhostChannel manager."
boundary: "It is not the lightweight convenience SDK and does not export GhostChannelSDK."
```

### L2 Lightweight SDK: `ghost_channel_sdk`

```yaml
package_path: "03_SDK与集成/04_SDK工程包/ghost-channel-sdk/python"
import_namespace: "ghost_channel_sdk"
package_name: "ghost-channel-sdk"
tests: "68/68 PASS"
fixed_this_batch:
  - "examples/python_memory_sync_example.py now imports ghost_channel_sdk"
  - "stress_test_100_concurrent.py now imports ghost_channel_sdk"
  - "schema-validator compose command now imports ghost_channel_sdk.schema_validator"
  - "RFC and delivery HTML examples now use ghost_channel_sdk for the lightweight SDK namespace."
meaning: "This is the user-facing Python SDK for object-flow sync, ack progression, replay protection, snapshot recovery, schema/example validation, and CLI demos."
boundary: "Any future AI that imports GhostChannelSDK from ghost_channel is reading stale pre-rename material."
```

### L2b TypeScript SDK

```yaml
package_path: "03_SDK与集成/04_SDK工程包/ghost-channel-sdk/typescript"
runtime: "Node >=22"
tests: "22/22 PASS via node --experimental-strip-types --test"
fixed_this_batch:
  - "package.json test script now runs Node type stripping for .ts tests"
  - "Dockerfile.typescript uses node:22-slim and CMD instead of ENTRYPOINT"
  - "Standalone TypeScript example now imports the actual .ts module path."
  - "Delivery TypeScript example now uses the real cross-folder .ts import path."
boundary: "The TypeScript SDK currently exercises object-flow behavior and testable protocol shapes. It still uses placeholder authTag values, so it must not be represented as production cryptography parity with the Python AES-GCM implementation."
```

### L3 Enterprise SDK: `ghost_hub_sdk`

```yaml
package_path: "03_SDK与集成/03_企业SDK包/GhostHub_SDK"
import_namespace: "ghost_hub_sdk"
package_name: "ghost-hub-sdk"
tests: "76/76 PASS"
core_components:
  - "GhostHubSDK / GhostHubConfig"
  - "IntentionBankComponent"
  - "NoUIAdapterComponent"
  - "AgentFederationComponent"
  - "GhostHubWorkflowEngine"
  - "FastAPI API layer"
  - "security, storage, database, protocol adapters"
meaning: "This is not merely a protocol wrapper. It is an enterprise workflow orchestration SDK with templates, intent matching, no-UI device control abstractions, agent federation, API, security, persistence, and docs."
boundary: "It depends on heavier API/protocol packages in current pyproject; old zero-dependency-core descriptions are stale."
```

### L4 Deployment and Commercial Assets

```yaml
paths:
  - "04_企业部署/docker-compose.yml"
  - "04_企业部署/04_商业部署包/docker"
  - "04_企业部署/04_商业部署包/license授权系统"
  - "05_商业化与市场"
  - "07_交付与验收"
fixed_this_batch:
  - "Root one-click compose build contexts now match Dockerfiles."
  - "Python demo image copies both protocol core and lightweight SDK."
  - "TypeScript demo image uses Node 22."
  - "schema-validator command uses the real ghost_channel_sdk namespace."
  - "Commercial Dockerfile now copies the local Enterprise SDK and starts FastAPI with uvicorn."
  - "Nonexistent ghost_hub_sdk.worker service was removed from commercial compose."
  - "Deployment guide no longer recommends scaling a nonexistent worker service."
boundary: "Docker CLI is not installed on this machine, so compose syntax/path fixes are reviewed and source-level aligned, but image build/runtime remains a pending external-environment verification. `license.json` remains an external deployment prerequisite."
```

## Six Knowledge Crystals

### KC-P01-001 — `VERIFY.ps1` Is Integrity, Not Functional Testing

```yaml
evidence_level: VERIFIED
source_refs:
  - "01.通讯协议_幽灵通道/VERIFY.ps1"
  - "01.通讯协议_幽灵通道/MANIFEST.yaml"
statement: "VERIFY.ps1 checks manifest integrity and optional binary presence semantics. It does not prove SDK behavior."
implication: "Future reports must separate manifest ALL CLEAN from SDK tests, stress tests, npm tests, and Docker deployment tests."
```

### KC-P01-002 — SDK Functional Gate Is Now 184 Tests

```yaml
evidence_level: VERIFIED
source_refs:
  - "qa_runner.py"
  - "00.超级提示词工程/14-全链路审计与运行对齐/VALIDATION_REGISTRY.yaml"
statement: "VAL-01-SDK-TESTS now covers Python core/lightweight/enterprise suites plus TypeScript npm tests: 18 + 68 + 76 + 22 = 184."
implication: "The older 162-test figure is still useful for Python-only history but no longer represents the full SDK gate."
```

### KC-P01-003 — Namespace Rename Is a Real Operational Boundary

```yaml
evidence_level: VERIFIED
statement: "The protocol package is ghost_channel; the lightweight SDK package is ghost_channel_sdk. Mixing them caused runnable example and stress-test failures."
fix_refs:
  - "03_SDK与集成/04_SDK工程包/ghost-channel-sdk/examples/python_memory_sync_example.py"
  - "03_SDK与集成/04_SDK工程包/ghost-channel-sdk/stress_test_100_concurrent.py"
implication: "Future AI should treat old `from ghost_channel import GhostChannelSDK` as a stale artifact."
current_guard: "`rg` scan over P01 markdown/html/python/typescript delivery files no longer finds stale lightweight-SDK imports."
```

### KC-P01-004 — Current Stress Evidence Is Strong but Synthetic

```yaml
evidence_level: VERIFIED
command: "python stress_test_100_concurrent.py"
result: "2500 syncs; 100% success; P99 2.88ms; avg bandwidth reduction 99.4%; consistency 100%"
boundary: "This validates local in-process SDK behavior, not networked production deployment under Docker/Kubernetes."
```

### KC-P01-005 — Enterprise SDK Is Workflow Orchestration, Not Just Ghost Channel

```yaml
evidence_level: FACT
statement: "GhostHub_SDK adds intention matching, templates, no-UI adapters, agent federation, API/security/storage/database, and workflow engine."
implication: "P01 should be routed to for protocol/SDK/deployment questions; P04/P05 should own QCM/platform orchestration unless explicitly using GhostHub as embedded SDK."
```

### KC-P01-006 — Production Deployment Still Has External Verification Gap

```yaml
evidence_level: GAP
statement: "Docker is not installed in the current environment, so docker compose build/up could not be executed."
mitigations_done:
  - "Fixed obvious build context, CMD/ENTRYPOINT, import, and nonexistent worker references."
  - "Kept this as a GAP rather than claiming full production deployment validation."
next_action: "Run docker compose config/build/up in an environment with Docker Desktop or CI."
```

## Best Use Pattern

1. Use `ghost_channel` when the task is about protocol primitives: delta, vector clocks, Merkle integrity, crypto, audit.
2. Use `ghost_channel_sdk` when the task is about practical memory/workflow sync, schema validation, ACK handling, snapshots, stress testing, or developer onboarding.
3. Use `ghost_hub_sdk` when the task is about enterprise workflow orchestration, templates, REST API, no-UI adapters, or agent federation.
4. Use deployment/commercial folders only after source tests pass, and treat Docker as pending until an actual Docker environment confirms it.
5. Do not use P01 as the final mother-package brain. It is a communication/protocol subsystem that can support P04/P05 and future user projects.
