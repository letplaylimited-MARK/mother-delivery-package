# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-15

### Added
- **RFC 0001**: Ghost Channel Protocol v1.0.0 standard
- **Python SDK**: Production-ready implementation with 68 passing tests
- **TypeScript SDK**: Production-ready implementation with 22 passing tests
- **100 Concurrent Stress Test**: Validated with P99 latency <10ms and 99.5% bandwidth reduction
- **Schema Registry**: Complete JSON schemas for all protocol objects
- **CLI Tools**: Command-line interface for memory and workflow sync
- **Schema Validator**: Asset validation pipeline

### Features
- Delta-based state synchronization
- Vector clock causal ordering
- AES-256-GCM encryption with AAD
- Merkle tree integrity verification
- Semantic filtering support
- Replay window with idempotency
- ACK progression (RECEIVED → VERIFIED → APPLIED)
- Snapshot recovery
- Full audit trail

### Security
- AES-256-GCM authenticated encryption
- Canonical JSON encoding
- Nonce uniqueness requirements
- AAD coverage for header integrity

## [0.1.0] - 2026-04-05

### Added
- Initial MVP release
- Python SDK alpha
- TypeScript SDK alpha
- PoC implementation
- Basic memory sync
- Basic workflow sync

---

*This changelog follows [Keep a Changelog](https://keepachangelog.com/) format.*
