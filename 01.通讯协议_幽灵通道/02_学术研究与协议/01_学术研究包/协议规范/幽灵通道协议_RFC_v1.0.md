# 幽灵通道协议 RFC 1.0

## Ghost Channel Protocol (GCP) - RFC 0001

**Document ID**: GCP-RFC-0001  
**Status**: Internet Standard  
**RFC Version**: 1.0.0  
**Date**: 2026-04-15  
**Obsoletes**: GCP-RFC-0.3-PublicReview  
**Intended Audience**: protocol engineers, infrastructure engineers, AI systems architects, SDK implementers

---

## Publication Notice

本文档定义了**幽灵通道协议（Ghost Channel Protocol, GCP）**的正式标准版本。

---

## Abstract

本文定义幽灵通道协议（Ghost Channel Protocol, GCP）的最小可实现规范。该协议面向分布式 AI 协作系统，提供语义感知的增量同步、因果一致性控制、端到端完整性验证与可审计状态传输机制。

---

## Table of Contents

1. [Conformance Language](#1-conformance-language)
2. [Scope](#2-scope)
3. [Terminology](#3-terminology)
4. [Protocol Goals](#4-protocol-goals)
5. [Canonical Encoding Rules](#5-canonical-encoding-rules)
6. [Core Objects](#6-core-objects)
7. [Message Types](#7-message-types)
8. [State Machine](#8-state-machine)
9. [Completion Semantics](#9-completion-semantics)
10. [Replay, Duplicate, and Idempotency](#10-replay-duplicate-and-idempotency)
11. [Error Model](#11-error-model)
12. [Versioning and Compatibility](#12-versioning-and-compatibility)
13. [SDK Public API](#13-sdk-public-api)
14. [Security Considerations](#14-security-considerations)

---

## 1. Conformance Language

关键词 **MUST**、**MUST NOT**、**REQUIRED**、**SHALL**、**SHALL NOT**、**SHOULD**、**SHOULD NOT**、**RECOMMENDED**、**MAY**、**OPTIONAL** 按 RFC 2119 / RFC 8174 的含义解释。

---

## 2. Scope

幽灵通道协议定义以下能力：

1. 状态差分提取与传输
2. 语义过滤后的同步负载构造
3. 因果顺序追踪
4. 加密传输与认证
5. 完整性验证与审计记录
6. 回滚、重放与幂等处理

本协议 **MUST NOT** 被解释为数据库本身、消息中间件本身或业务逻辑执行框架的替代品。

---

## 3. Terminology

| Term | Definition |
|------|------------|
| DeltaPayload | 两个状态快照之间的最小变化集合 |
| VectorClock | 用于表达事件偏序关系的时钟结构 |
| EncryptedStream | 协议的主线传输对象 |
| AckMessage | 接收方返回的确认对象 |
| AuditEntry | 一次同步事件的结构化审计记录 |

---

## 4. Protocol Goals

实现者 **MUST** 以以下目标为导向：

1. **Bandwidth Reduction**: 协议 **SHOULD** 最小化传输负载
2. **Causal Correctness**: 协议 **MUST** 区分先后事件与并发事件
3. **Semantic Relevance**: 协议 **MAY** 基于语义相关性裁剪同步载荷
4. **Trustability**: 协议 **MUST** 提供完整性验证与审计能力
5. **Recoverability**: 协议 **MUST** 支持失败后的回滚与恢复

---

## 5. Canonical Encoding Rules

### 5.1 canonical_json

`canonical_json(x)` **MUST** 满足：
1. UTF-8 编码
2. 对象键按字典序排序
3. 无额外空白
4. 布尔值 **MUST** 序列化为小写 `true` / `false`
5. 空值 **MUST** 序列化为小写 `null`

### 5.2 Wire Encoding

`DeltaPayload` 在线协议中 **MUST** 表示为：

```
base64( AES-256-GCM-ENC( key, nonce, zlib(utf8(canonical_json(DeltaPayload))), aad ) )
```

### 5.3 delta_hash

`delta_hash` **MUST** 定义为：

```
sha256( canonical_json(DeltaPayload) )
```

`delta_hash` **MUST** 以 `lowercase hex` 形式传输，长度固定为 64 字符。

---

## 6. Core Objects

### 6.1 DeltaPayload

**Required fields**:
- `added`: object
- `modified`: object
- `removed`: array of strings
- `version_from`: string
- `version_to`: string
- `timestamp`: number

**Optional fields**:
- `list_appends`: object
- `changed_fields`: object

### 6.2 EncryptedStream

**Required fields**:
- `protocol_version`: string
- `schema_version`: string
- `stream_id`: string
- `source_role_id`: string
- `destination_role_id`: string
- `timestamp_ns`: number
- `sequence_number`: number
- `type`: string
- `vector_clock`: object
- `delta_hash`: string
- `delta_payload`: string (base64)
- `nonce`: string (base64)
- `compression`: object
- `encryption`: object
- `auth_tag`: string (base64)
- `merkle_root`: string
- `audit_required`: boolean

**Optional fields**:
- `signature`: string | null
- `extensions`: object

### 6.3 AckMessage

**Required fields**:
- `protocol_version`: string
- `schema_version`: string
- `stream_id`: string
- `sequence_number`: number
- `ack_type`: enum
- `status`: enum
- `receiver_id`: string
- `merkle_root_verified`: boolean
- `applied`: boolean
- `timestamp_ns`: number

**Optional fields**:
- `error`: ErrorObject | null
- `extensions`: object

`ack_type` **MUST** be one of: `RECEIVED`, `VERIFIED`, `APPLIED`, `ROLLED_BACK`, `FAILED`
`status` **MUST** be one of: `ok`, `error`

### 6.4 ErrorObject

**Required fields**:
- `error_code`: string
- `error_name`: string
- `severity`: enum
- `message`: string
- `retryable`: boolean
- `rollback_required`: boolean
- `context`: object
- `timestamp`: number

`severity` **MUST** be one of: `low`, `medium`, `high`, `critical`

### 6.5 AuditEntry

**Required fields**:
- `transaction_id`: string
- `timestamp`: number
- `source_role`: string
- `destination_role`: string
- `message_type`: string
- `delta_hash`: string
- `merkle_root_before`: string
- `merkle_root_after`: string
- `bandwidth_saved_bytes`: number
- `transmission_duration_ms`: number
- `signature_verified`: boolean
- `tamper_detected`: boolean

---

## 7. Message Types

The `type` field **MUST** be one of:

- `KNOWLEDGE_UPDATE`
- `QUERY_RESPONSE`
- `DECISION_PROPOSAL`
- `DEADLOCK_ALERT`
- `META_COMMENTARY`
- `WORKFLOW_SYNC`
- `MEMORY_SYNC`

---

## 8. State Machine

### 8.1 Sender-side States

- `Idle` → `DeltaComputed` → `Filtered` → `Compressed` → `Encrypted` → `Sent` → `AckObserved` → `Completed` | `Failed`

### 8.2 Receiver-side States

- `Received` → `Verified` → `Applied` | `Blocked` | `RolledBack` | `Failed`

### 8.3 ACK Semantics

ACKs use a cumulative model:

| ack_type | Implies |
|----------|---------|
| `VERIFIED` | `RECEIVED` |
| `APPLIED` | `VERIFIED` |
| `ROLLED_BACK` | reception + failed application |

Legal ACK progressions:
1. `RECEIVED → VERIFIED → APPLIED`
2. `RECEIVED → VERIFIED → ROLLED_BACK`
3. `RECEIVED → FAILED`

---

## 9. Completion Semantics

SDKs **MUST** support two completion policies:

### 9.1 `verify` mode

Operation completes when ACK reaches `VERIFIED` or `FAILED`.

### 9.2 `apply` mode (default)

Operation completes only when ACK reaches `APPLIED`, `ROLLED_BACK`, or `FAILED`.

---

## 10. Replay, Duplicate, and Idempotency

### 10.1 Replay Window

Each `stream_id` **MUST** maintain a replay window keyed by `sequence_number`. Recommended default size: `1024`.

### 10.2 Duplicate Handling

| Condition | Required Behavior |
|----------|-------------------|
| Same `stream_id`, `sequence_number`, `delta_hash` | MUST return idempotent ACK |
| Same `stream_id`, `sequence_number`, different `delta_hash` | MUST raise error |
| Expired `sequence_number` | MUST raise error |

### 10.3 Idempotency

The receiver **MUST NOT** re-apply a delta already successfully applied with the same `(stream_id, sequence_number, delta_hash)` triple.

---

## 11. Error Model

Required error codes:

| Prefix | Description |
|--------|-------------|
| `GC-VAL-*` | Schema validation errors |
| `GC-SYNC-*` | Synchronization errors |
| `GC-CLK-*` | Clock/causality errors |
| `GC-CRY-*` | Cryptographic errors |
| `GC-MRK-*` | Merkle verification errors |
| `GC-AUD-*` | Audit errors |
| `GC-RCV-*` | Receiver errors |

---

## 12. Versioning and Compatibility

### 12.1 Version Format

Version strings **MUST** follow `MAJOR.MINOR.PATCH` syntax.

### 12.2 Compatibility Matrix

| Sender | Receiver | Required Outcome |
|--------|----------|------------------|
| Same major, same minor | Accept |
| Same major, sender minor higher | Accept if unknown fields are in `extensions` |
| Same major, sender minor lower | Accept |
| Different major | Reject with `GC-VAL-002` |

---

## 13. SDK Public API

### 13.1 Python SDK

```python
from ghost_channel_sdk import GhostChannelSDK, GhostChannelConfig

sdk = GhostChannelSDK(GhostChannelConfig(
    compression_level=9,
    semantic_threshold=0.7,
    audit_enabled=True,
    max_retry=3,
    completion_mode="apply",  # or "verify"
))

result = await sdk.sync_memory_delta(
    source_role="agent_a",
    target_role="agent_b",
    old_state={"v": "v1", "data": 1},
    new_state={"v": "v2", "data": 2},
    semantic_filter="optional filter",
)
```

### 13.2 TypeScript SDK

```typescript
import { GhostChannelClient } from 'ghost-channel-sdk';

const client = new GhostChannelClient({
  compressionLevel: 9,
  semanticThreshold: 0.7,
  auditEnabled: true,
  maxRetry: 3,
  completionMode: 'apply',
});

const result = await client.syncMemoryDelta(
  'agent_a',
  'agent_b',
  { v: 'v1', data: 1 },
  { v: 'v2', data: 2 },
);
```

---

## 14. Security Considerations

Implementers **MUST** review:

1. Nonce uniqueness guarantees
2. Deterministic canonical JSON encoding
3. Authenticated header coverage
4. Merkle root reproducibility
5. Audit storage immutability
6. Replay-window storage durability

---

## Appendix A: Schema References

All protocol objects are defined by JSON schemas in the `schemas/` directory of the reference implementation.

## Appendix B: Reference Implementation

Reference implementations are available at:
- Python: `https://github.com/ghost-channel/python-sdk`
- TypeScript: `https://github.com/ghost-channel/typescript-sdk`

---

*RFC 0001 - Ghost Channel Protocol v1.0.0*
*© 2026 Q-SpecTrum Project*
