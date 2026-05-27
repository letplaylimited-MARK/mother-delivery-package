# 幽灵通道协议 RFC 可发布版

## Ghost Channel Protocol (GCP)

**Document ID**: GCP-RFC-0.3-PublicReview  
**Status**: Public Review Draft  
**Date**: 2026-04-05  
**Derived From**: `幽灵通道协议规范稿_SDK草案_v1.0.md`  
**Intended Audience**: protocol engineers, infrastructure engineers, AI systems architects, SDK implementers, AI execution agents  

---

## Publication Note

本文档是幽灵通道协议的**可发布版 RFC 草案**，用于对外技术评审、协议讨论与实现前校对。它不等同于最终标准文本，但已具备公开讨论与互操作性评审所需的主体结构。

本版本的目标不是给出“最终不可变标准”，而是提供一个足够稳定的公共讨论基线，使协议实现者、SDK 开发者与研究者能够围绕同一对象模型、编码约定、ACK 语义与版本兼容策略进行协作。

### Intended Use

- 用于协议设计评审
- 用于 SDK MVP 对齐
- 用于工程试点前的实现口径统一
- 用于后续 RFC 定稿、SDK 文档和参考实现的基础版本控制

### Recommended Review Focus

建议审阅者优先关注以下 5 个方面：

1. 线协议编码是否具备互操作性
2. ACK 生命周期是否足够闭环
3. Replay / duplicate / idempotency 是否足以支撑 MVP
4. 版本兼容策略是否适合渐进落地
5. SDK 公共接口是否足够稳定

---

## Table of Contents

1. Conformance Language  
2. Scope  
3. Terminology  
4. Protocol Goals  
5. Canonical Encoding Rules  
6. Core Objects  
7. Message Types  
8. State Machine  
9. Completion Semantics  
10. Replay, Duplicate, and Idempotency  
11. Error Model  
12. Versioning and Compatibility  
13. SDK Public API  
14. AI Execution Preconditions  
15. MVP Readiness  
16. Security Considerations  
17. Conclusion  

---

## Abstract

本文定义幽灵通道协议（Ghost Channel Protocol, GCP）的最小可实现规范。该协议面向分布式 AI 协作系统，提供语义感知的增量同步、因果一致性控制、端到端完整性验证与可审计状态传输机制。本文档以 RFC 风格描述协议目标、术语、对象模型、编码规则、状态机、错误处理、版本兼容与实现要求，用于指导互操作 MVP 的实现，并作为后续定稿版标准文本的公开审阅基线。

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
| canonical_json | 规范化 JSON 序列化形式 |

---

## 4. Protocol Goals

实现者 **MUST** 以以下目标为导向：

1. **Bandwidth Reduction**: 协议 **SHOULD** 最小化传输负载，避免全量同步。
2. **Causal Correctness**: 协议 **MUST** 区分先后事件与并发事件。
3. **Semantic Relevance**: 协议 **MAY** 基于语义相关性裁剪同步载荷。
4. **Trustability**: 协议 **MUST** 提供完整性验证与审计能力。
5. **Recoverability**: 协议 **MUST** 支持失败后的回滚与恢复。

---

## 5. Canonical Encoding Rules

### 5.1 canonical_json

`canonical_json(x)` **MUST** 满足：

1. UTF-8 编码
2. 对象键按字典序排序
3. 无额外空白
4. 整数使用十进制字符串表示，不得带前导零
5. 浮点数 **MUST** 使用十进制非指数形式表示
6. `-0` **MUST** 规范化为 `0`
7. `NaN`、`Infinity`、`-Infinity` **MUST NOT** 出现在协议对象中
8. 字符串 **MUST** 使用 JSON 标准转义规则（RFC 8259 兼容）
9. Unicode 字符串 **MUST** 在序列化前规范化为 NFC 形式
10. 数组元素顺序 **MUST** 保持输入顺序，不得重排
11. 布尔值 **MUST** 序列化为小写 `true` / `false`
12. 空值 **MUST** 序列化为小写 `null`

#### 5.1.1 canonical_json 示例

输入对象：

```json
{"b":2,"a":"x","arr":[3,1,true,null],"u":"é"}
```

规范化输出：

```json
{"a":"x","arr":[3,1,true,null],"b":2,"u":"é"}
```

### 5.2 delta_payload Wire Encoding

`DeltaPayload` 在 SDK 内部 **MUST** 表示为对象。在线协议中，`delta_payload` **MUST** 表示为：

```text
base64( ciphertext )
```

其中：

```text
plaintext   = zlib( utf8( canonical_json(DeltaPayload) ) )
ciphertext  = AES-256-GCM-ENC( key, nonce, plaintext, aad )
auth_tag    = GCM authentication tag (separate field)
```

即：
- `delta_payload` **MUST** 仅承载密文字节的 base64 表示；
- `auth_tag` **MUST** 作为独立字段传输；
- `nonce` **MUST** 作为独立字段传输；
- `delta_payload` **MUST NOT** 包含 `auth_tag`。

#### 5.2.1 线协议字段编码约束

| 字段 | 编码 | 说明 |
|------|------|------|
| `delta_payload` | base64 (RFC 4648 标准字母表，含 `=` padding) | 密文字节 |
| `nonce` | base64 (RFC 4648 标准字母表，含 `=` padding) | 12-byte 值 |
| `auth_tag` | base64 (RFC 4648 标准字母表，含 `=` padding) | 固定 16-byte 标签 |
| `delta_hash` | lowercase hex | 64 个十六进制字符 |
| `merkle_root` | lowercase hex | 64 个十六进制字符 |

因此：

- 在线协议中，`delta_payload` **MUST** 是 `string`
- 在 SDK 内部，`delta_payload` **MUST NOT** 直接表示为 string

### 5.3 delta_hash

`delta_hash` **MUST** 定义为：

```text
sha256( canonical_json(DeltaPayload) )
```

实现者 **MUST NOT** 对压缩后、加密后或完整线协议对象求 `delta_hash`。

`delta_hash` **MUST** 以 `lowercase hex` 形式传输，长度固定为 64 字符。

### 5.4 Nonce and Auth Tag

- `nonce` **MUST** 为 96-bit / 12-byte 值
- `nonce` **MUST** 使用标准 base64 表示
- `auth_tag` **MUST** 认证头部字段与密文载荷
- `auth_tag` **MUST** 为 128-bit / 16-byte 值
- `auth_tag` **MUST** 使用标准 base64 表示

AAD **MUST** 覆盖：

`protocol_version, schema_version, stream_id, source_role_id, destination_role_id, timestamp_ns, sequence_number, type, vector_clock, compression, encryption, delta_hash, merkle_root, audit_required`

`auth_tag` **MUST NOT** 认证 `auth_tag` 字段本身，也 **MUST NOT** 认证可选 `signature` 字段。

AAD 的序列化形式 **MUST** 为：

```text
aad = utf8(canonical_json({
  protocol_version,
  schema_version,
  stream_id,
  source_role_id,
  destination_role_id,
  timestamp_ns,
  sequence_number,
  type,
  vector_clock,
  compression,
  encryption,
  delta_hash,
  merkle_root,
  audit_required
}))
```

---

## 6. Core Objects

### 6.1 DeltaPayload

Required fields:

- `added`
- `modified`
- `removed`
- `version_from`
- `version_to`
- `timestamp`

Optional fields:

- `list_appends`
- `changed_fields`

### 6.2 EncryptedStream

An `EncryptedStream` **MUST** contain at least:

- `protocol_version`
- `schema_version`
- `stream_id`
- `source_role_id`
- `destination_role_id`
- `timestamp_ns`
- `sequence_number`
- `type`
- `vector_clock`
- `delta_hash`
- `delta_payload`
- `compression`
- `encryption`
- `auth_tag`
- `merkle_root`
- `audit_required`

`signature` is OPTIONAL. `extensions` is OPTIONAL.

### 6.3 AckMessage

An `AckMessage` **MUST** contain at least:

- `protocol_version`
- `schema_version`
- `stream_id`
- `sequence_number`
- `ack_type`
- `status`
- `receiver_id`
- `merkle_root_verified`
- `applied`
- `timestamp_ns`

`error` **MUST** be `null` when `status = ok`, and **MUST** conform to `ErrorObject` when `status = error`.

### 6.4 AuditEntry

An `AuditEntry` **MUST** capture at least:

- transaction identity
- source/destination
- message type
- `delta_hash`
- `merkle_root_before`
- `merkle_root_after`
- transmission timing
- verification result

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

Workflow-specific or alert-specific metadata **MUST** be carried in `extensions` rather than as top-level unknown fields.

---

## 8. State Machine

### 8.1 Sender-side View

The sender-side observable states are:

- `Idle`
- `DeltaComputed`
- `Filtered`
- `Compressed`
- `Encrypted`
- `Sent`
- `AckObserved`
- `Completed`
- `Failed`

The sender **MUST NOT** locally infer receiver-side states beyond what is explicitly reported by `AckMessage`.

### 8.2 Receiver-side View

The receiver-side processing states are:

- `Received`
- `Verified`
- `Applied`
- `Blocked`
- `RolledBack`
- `Recovered`
- `Failed`

### 8.3 ACK Semantics

ACKs use a cumulative model:

- `VERIFIED` implies `RECEIVED`
- `APPLIED` implies `VERIFIED`
- `ROLLED_BACK` implies reception plus failed application path
- `FAILED` indicates that processing cannot progress to a valid terminal applied state

An implementation **MAY** emit multiple ACK stages, but **MUST** preserve monotonicity. An implementation **MUST NOT** emit `RECEIVED` after `VERIFIED`, or `VERIFIED` after `APPLIED`.

For MVP interoperability, receivers **MUST** support at least the following legal progressions:

1. `RECEIVED -> VERIFIED -> APPLIED`
2. `RECEIVED -> VERIFIED -> ROLLED_BACK`
3. `RECEIVED -> FAILED`

Receivers **MAY** skip intermediate emission and send only the highest achieved ACK stage, provided cumulative semantics are preserved.

### 8.4 ACK Type × Status 合法矩阵

| ack_type | status=ok | status=error | 说明 |
|----------|-----------|--------------|------|
| `RECEIVED` | ✅ | ❌ | 成功接收但尚未验证 |
| `VERIFIED` | ✅ | ❌ | 完整性与认证验证通过 |
| `APPLIED` | ✅ | ❌ | 状态已成功应用 |
| `ROLLED_BACK` | ❌ | ✅ | 已执行回滚，必须携带 error |
| `FAILED` | ❌ | ✅ | 无法完成处理，必须携带 error |

规则：
- 当 `status = ok` 时，`error` **MUST** 为 `null`
- 当 `status = error` 时，`error` **MUST** 为合法 `ErrorObject`
- `APPLIED` 与 `ROLLED_BACK` **MUST NOT** 同时出现于同一 ACK

---

## 9. Completion Semantics

SDKs **MUST** support at least two completion policies:

### 9.1 `verify` mode

Operation completes when ACK reaches `VERIFIED` or `FAILED`.

### 9.2 `apply` mode (default)

Operation completes only when ACK reaches one of:

- `APPLIED`
- `ROLLED_BACK`
- `FAILED`

If no terminal ACK arrives before `apply_timeout_ms`, the SDK **MUST** surface a timeout error.

---

## 10. Replay, Duplicate, and Idempotency

### 10.1 Replay Window

Each `stream_id` **MUST** maintain a replay window keyed by `sequence_number`. Recommended default size: `1024`.

The initial valid `sequence_number` for a new `stream_id` **MUST** be `0` or `1`, but implementations **MUST** choose exactly one convention and document it consistently.

Replay-window state **MUST** be persisted across process restarts for any durable deployment.

If a receiver observes a gap in `sequence_number`, it **MUST** classify the event as one of:

- `gap-bufferable`
- `gap-expired`
- `gap-invalid`

### 10.2 Duplicate Handling

| Condition | Required Behavior |
|----------|-------------------|
| Same `stream_id`, `sequence_number`, `delta_hash` | MUST return idempotent ACK |
| Same `stream_id`, `sequence_number`, different `delta_hash` | MUST raise `GC-CLK-003` |
| Expired `sequence_number` | MUST raise `GC-SYNC-003` |

Out-of-order delivery within the replay window **MAY** be buffered, but **MUST NOT** be applied if causal dependencies are not yet satisfied.

### 10.2.1 Gap / Out-of-Order 决策表

| 条件 | 结果 |
|------|------|
| `sequence_number = expected_next` | 直接处理 |
| `sequence_number > expected_next` 且 gap 在 replay window 内 | 缓冲，等待缺失消息 |
| `sequence_number > expected_next` 且 gap 超出 replay window | `GC-SYNC-003` |
| `sequence_number < window_min` | `GC-SYNC-003` |
| `sequence_number < expected_next` 且 `(stream_id, sequence_number, delta_hash)` 已存在 | 幂等 ACK |

### 10.2.2 `sequence_number` 与 `vector_clock` 联合规则

- `sequence_number` 负责**流内顺序**
- `vector_clock` 负责**跨节点因果关系**

实现者 **MUST** 同时满足：
1. `sequence_number` 合法
2. `vector_clock` 不违反因果顺序

若 `sequence_number` 合法但 `vector_clock` 显示因果逆序，则 **MUST** 触发 `GC-CLK-002 CausalOrderViolation`。

### 10.3 Idempotency

The receiver **MUST NOT** re-apply a delta already successfully applied with the same `(stream_id, sequence_number, delta_hash)` triple.

---

## 11. Error Model

Required error families:

- `GC-VAL-*`
- `GC-SYNC-*`
- `GC-CLK-*`
- `GC-SEM-*`
- `GC-CRY-*`
- `GC-MRK-*`
- `GC-AUD-*`
- `GC-RCV-*`

MVP implementations **MUST** support at least:

- `GC-VAL-001`
- `GC-VAL-002`
- `GC-SYNC-001`
- `GC-SYNC-002`
- `GC-SYNC-003`
- `GC-CLK-001`
- `GC-CLK-002`
- `GC-CLK-003`
- `GC-CRY-001`
- `GC-CRY-002`
- `GC-MRK-001`
- `GC-AUD-001`
- `GC-RCV-001`
- `GC-RCV-002`

---

## 12. Versioning and Compatibility

### 12.1 Version Types

- Document version: descriptive only
- `protocol_version`: wire behavior version
- `schema_version`: object schema version

Version strings **MUST** follow `MAJOR.MINOR.PATCH` syntax where each component is a non-negative integer encoded in decimal.

Examples:
- `1.0.0`
- `1.1.0`
- `2.0.3`

### 12.2 Compatibility Rules

| Sender | Receiver | Required Outcome |
|--------|----------|------------------|
| Same major, same minor | Accept |
| Same major, sender minor higher | Accept if unknown fields are only in `extensions` |
| Same major, sender minor lower | Accept |
| Different major | Reject with `GC-VAL-002` |

`AckMessage` and `EncryptedStream` **MUST** share the same `protocol_version` within one exchange.

---

## 13. SDK Public API

### 13.1 Python API

```python
class GhostChannelSDK:
    async def sync_memory_delta(self, source_role: str, target_role: str, old_state: dict, new_state: dict, semantic_filter: str | None = None) -> SyncResult: ...
    async def sync_workflow_state(self, workflow_id: str, step_id: str, step_state: dict, dependencies: list[str]) -> SyncResult: ...
    async def recover_from_failure(self, step_id: str, last_known_state: dict) -> dict: ...
    async def receive_ack(self, ack: dict) -> None: ...
```

### 13.2 TypeScript API

```ts
export class GhostChannelClient {
  syncMemoryDelta(sourceRole: string, targetRole: string, oldState: Record<string, unknown>, newState: Record<string, unknown>, semanticFilter?: string): Promise<SyncResult>
  syncWorkflowState(workflowId: string, stepId: string, stepState: Record<string, unknown>, dependencies: string[]): Promise<SyncResult>
  recoverFromFailure(stepId: string, lastKnownState: Record<string, unknown>): Promise<Record<string, unknown>>
  receiveAck(ack: Record<string, unknown>): Promise<void>
}
```

SDKs **MUST** return `SyncResult`, not raw ACK payloads, from public `sync_*` methods.

---

## 14. AI Execution Preconditions

An AI agent **MUST NOT** claim direct execution capability unless the runtime provides:

1. snapshot storage access
2. vector clock persistence access
3. transport endpoint mapping
4. audit sink access
5. key management access

If any of these are absent, the agent **MUST** enter `analysis_only` mode.

---

## 15. MVP Readiness

This draft is suitable for MVP implementation if an engineering team:

1. adopts the normative encoding rules in Section 5,
2. implements all required objects in Section 6,
3. respects ACK lifecycle in Section 8,
4. implements replay/idempotency in Section 10,
5. uses the SDK public APIs in Section 13,
6. treats advanced zero-knowledge / post-quantum optimizations as optional or experimental.

### 15.1 MVP vs Experimental Scope

| Scope | Features |
|------|----------|
| **MVP Required** | Delta sync, VectorClock, AckMessage, replay/idempotency, audit, AES-256-GCM, Merkle verification |
| **MVP Optional** | Semantic filtering, compression tuning, dynamic routing |
| **Experimental** | Multimodal alignment, post-quantum hardening, zero-knowledge proofs, verifiable computation |

---

## 16. Security Considerations

Implementers **MUST** review the following items before production deployment:

- nonce uniqueness guarantees
- deterministic canonical JSON encoder
- authenticated header coverage
- Merkle root reproducibility
- audit storage immutability
- replay-window storage durability

---

## 17. Conclusion

This public review draft defines the minimum interoperable shape of Ghost Channel as a semantic-aware synchronization layer for distributed AI systems. The protocol is now sufficiently constrained to guide an MVP implementation, while still leaving room for experimental extensions in multimodal alignment, post-quantum hardening, and verifiable computation. Its purpose is to provide a stable review surface for public technical discussion prior to final standardization.

---

## Document Status and Next Steps

This document is released as a **Public Review Draft**. Reviewers are expected to focus on:

- wire-format interoperability
- SDK implementation feasibility
- ACK lifecycle correctness
- replay / idempotency edge cases
- version compatibility handling

Future versions are expected to include:

- Appendix-level registries for enums and error codes
- explicit transport binding profiles
- formal reference test vectors
- conformance test suite alignment

---

## Publication Metadata

| Item | Value |
|------|------|
| Review Status | Public Review Draft |
| Intended Review Window | 30 days |
| Change Scope | MVP wire protocol, ACK lifecycle, replay/idempotency, SDK alignment |
| Not Yet Finalized | ZKP integration, post-quantum performance tuning, multimodal production profiles |

This version is suitable for:

- internal architecture review
- external protocol review with trusted partners
- SDK MVP alignment
- implementation planning and conformance preparation

This version is **not yet intended** to be treated as a frozen public standard.

---

*End of RFC public review draft.*

*© 2026 Q-SpecTrum Project*
