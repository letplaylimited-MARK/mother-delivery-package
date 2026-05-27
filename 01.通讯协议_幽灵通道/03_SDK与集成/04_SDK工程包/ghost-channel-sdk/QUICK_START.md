# Ghost Channel Protocol - Developer Quick Start

## 5-Minute Quick Start

### 1. Install SDK

**Python:**
```bash
pip install ghost-channel-sdk
```

**TypeScript:**
```bash
npm install ghost-channel-sdk
```

### 2. Basic Memory Sync

**Python:**
```python
import asyncio
from ghost_channel_sdk import GhostChannelSDK, GhostChannelConfig

async def main():
    sdk = GhostChannelSDK(GhostChannelConfig())
    
    result = await sdk.sync_memory_delta(
        source_role="agent_1",
        target_role="agent_2",
        old_state={"version": "v1", "data": [1, 2, 3]},
        new_state={"version": "v2", "data": [1, 2, 3, 4, 5]},
    )
    print(f"Bandwidth saved: {result.bandwidth_reduction:.1%}")

asyncio.run(main())
```

**TypeScript:**
```typescript
import { GhostChannelClient } from 'ghost-channel-sdk';

const client = new GhostChannelClient({});
const result = await client.syncMemoryDelta(
  'agent_1',
  'agent_2',
  { version: 'v1', data: [1, 2, 3] },
  { version: 'v2', data: [1, 2, 3, 4, 5] },
);
console.log(`Bandwidth saved: ${result.bandwidthReduction * 100}%`);
```

### 3. Workflow State Sync

**Python:**
```python
result = await sdk.sync_workflow_state(
    workflow_id="build_pipeline",
    step_id="compile",
    step_state={"status": "completed", "output": "/dist/app.js"},
    dependencies=["fetch_dependencies"],
)
```

**TypeScript:**
```typescript
const result = await client.syncWorkflowState(
  'build_pipeline',
  'compile',
  { status: 'completed', output: '/dist/app.js' },
  ['fetch_dependencies'],
);
```

### 4. Failure Recovery

**Python:**
```python
recovered_state = await sdk.recover_from_failure(
    step_id="compile",
    last_known_state={"status": "failed"},
)
```

**TypeScript:**
```typescript
const recovered = await client.recoverFromFailure(
  'compile',
  { status: 'failed' },
);
```

## Configuration Options

### GhostChannelConfig

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `compression_level` | int | 9 | zlib compression (0-9) |
| `semantic_threshold` | float | 0.7 | Semantic filter threshold |
| `audit_enabled` | bool | true | Enable audit trail |
| `max_retry` | int | 3 | Max retry attempts |
| `completion_mode` | str | "apply" | "apply" or "verify" |
| `await_ack` | bool | false | Wait for ACK |
| `ack_timeout_ms` | int | 500 | ACK timeout |
| `replay_window_size` | int | 1024 | Replay window |

## Common Patterns

### Pattern 1: Bidirectional Sync

```python
# Agent A syncs to Agent B
await sdk.sync_memory_delta("A", "B", state_a_old, state_a_new)

# Agent B syncs to Agent A
await sdk.sync_memory_delta("B", "A", state_b_old, state_b_new)
```

### Pattern 2: Multi-Agent Broadcast

```python
async def broadcast(source, targets, new_state):
    tasks = []
    for target in targets:
        tasks.append(sdk.sync_memory_delta(source, target, old_state, new_state))
    await asyncio.gather(*tasks)
```

### Pattern 3: Workflow Pipeline

```python
steps = ["fetch", "process", "store"]
for i, step in enumerate(steps):
    deps = [steps[i-1]] if i > 0 else []
    await sdk.sync_workflow_state("pipeline", step, {"status": "done"}, deps)
```

## CLI Usage

```bash
# Memory sync demo
python -m ghost_channel_sdk.cli demo-memory

# Workflow sync demo
python -m ghost_channel_sdk.cli demo-workflow

# Validate schemas and examples
python -m ghost_channel_sdk.cli validate-assets
```

## Troubleshooting

### Issue: "ACK timeout"

**Solution:** Increase `ack_timeout_ms` or set `await_ack=false`

### Issue: "Bandwidth reduction too low"

**Solution:** 
- Ensure `compression_level=9`
- Use incremental state changes
- Enable semantic filtering for large states

### Issue: "Consistency check failed"

**Solution:** Check that both sides use the same `protocol_version`

## Next Steps

- Read [RFC 0001](RFC_0001_GHOST_CHANNEL_PROTOCOL_v1.0.md)
- Review [API Reference](python/ghost_channel_sdk/)
- Run [Stress Test](stress_test_100_concurrent.py)

---

*Quick Start Guide v1.0.0*
