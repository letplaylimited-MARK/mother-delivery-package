# Ghost Channel Protocol SDK

> Semantic-aware synchronization for distributed AI systems

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
## Overview

The Ghost Channel Protocol (GCP) is a semantic-aware synchronization protocol designed for distributed AI multi-agent systems. It provides:

- **Delta-based synchronization**: Only transmit changes, not full state
- **Causal ordering**: Vector clock-based conflict detection
- **End-to-end integrity**: AES-256-GCM encryption with Merkle verification
- **Audit trail**: Complete transaction logging
- **Self-healing**: Snapshot recovery from failures

## Performance

| Metric | Result |
|--------|--------|
| P99 Latency | < 10ms |
| Bandwidth Reduction | 99.5% |
| Consistency | 100% |
| Success Rate | 100% |

Tested with 100 concurrent agents, 2500 sync operations.

## Quick Start

### Python

```bash
pip install ghost-channel-sdk
```

```python
import asyncio
from ghost_channel_sdk import GhostChannelSDK, GhostChannelConfig

async def main():
    sdk = GhostChannelSDK(GhostChannelConfig(
        compression_level=9,
        audit_enabled=True,
        completion_mode="apply",
    ))
    
    result = await sdk.sync_memory_delta(
        source_role="agent_a",
        target_role="agent_b",
        old_state={"v": "v1", "data": 1},
        new_state={"v": "v2", "data": 2},
    )
    print(f"Success: {result.success}")
    print(f"Bandwidth reduction: {result.bandwidth_reduction:.1%}")

asyncio.run(main())
```

### TypeScript

```bash
npm install ghost-channel-sdk
```

```typescript
import { GhostChannelClient } from 'ghost-channel-sdk';

const client = new GhostChannelClient({
  compressionLevel: 9,
  auditEnabled: true,
  completionMode: 'apply',
});

const result = await client.syncMemoryDelta(
  'agent_a',
  'agent_b',
  { v: 'v1', data: 1 },
  { v: 'v2', data: 2 },
);
console.log(`Success: ${result.success}`);
```

## Documentation

### User Documentation
- [HTML Documentation](../../../../07_交付与验收/07_交付文档/html/index.html) - Browser-friendly docs
- [Markdown Docs](../../../../07_交付与验收/07_交付文档/markdown/README.md) - AI-readable format
- [OpenAPI Spec](../../../../07_交付与验收/07_交付文档/openapi/ghost-hub-api.yaml) - API specification

### Developer Documentation
- [Developer Guide](DEVELOPER_GUIDE_v1.1.md)
- [API Reference](python/ghost_channel_sdk/)

## Protocol

The Ghost Channel Protocol is a semantic-aware synchronization protocol.

Key components:
- **DeltaPayload**: Minimal change set between states
- **EncryptedStream**: Wire format for transmissions
- **AckMessage**: Acknowledgment with monotonic progression
- **AuditEntry**: Transaction audit record

## SDK Architecture

```
ghost-channel-sdk/
├── python/                 # Python SDK (v1.0.0)
│   ├── ghost_channel_sdk/   # Package source
│   │   ├── sdk.py         # Main SDK class
│   │   ├── crypto.py      # AES-256-GCM backend
│   │   ├── types.py       # Protocol types
│   │   └── cli.py         # CLI tools
│   └── tests/             # 68 unit tests
├── typescript/            # TypeScript SDK (v1.0.0)
│   ├── src/               # Package source
│   └── test/              # 22 unit tests
├── schemas/               # JSON schemas (9 schemas)
├── examples/              # Example files
└── RFC_0001_*.md          # Protocol specification
```

## Testing

### Python

```bash
cd python
pip install -e .
pytest tests/ -v
```

### TypeScript

```bash
cd typescript
npm install
npm test
```

### Stress Test

```bash
python stress_test_100_concurrent.py
```

## License

MIT License - see [LICENSE](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

*Ghost Channel Protocol - RFC 0001*
