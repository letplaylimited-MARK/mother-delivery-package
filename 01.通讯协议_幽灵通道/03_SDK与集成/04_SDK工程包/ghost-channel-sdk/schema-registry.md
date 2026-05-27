# Ghost Channel Schema Registry

**版本**: v1.0  
**日期**: 2026-04-05  
**作用**: 幽灵通道协议核心 Schema 注册表与清单索引  

---

## 1. 注册表说明

本文件汇总 `schemas/` 目录下的全部协议核心 Schema，作为：

1. 工程实现时的对象索引
2. SDK 校验时的引用清单
3. 后续 RFC / 协议规范中的对象注册表基础

Schema 根目录：

```text
./schemas/
```

---

## 2. Schema 总表

| Schema 名称 | 文件名 | 类型 | 作用 |
|-------------|--------|------|------|
| DeltaPayload | `delta-payload.schema.json` | 核心协议对象 | 描述状态差分载荷 |
| EncryptedStream | `encrypted-stream.schema.json` | 线协议对象 | 描述主消息传输对象 |
| AckMessage | `ack-message.schema.json` | 线协议对象 | 描述接收方确认消息 |
| SyncResult | `sync-result.schema.json` | SDK 返回对象 | 描述同步调用的返回结果 |
| ErrorObject | `error-object.schema.json` | 通用对象 | 描述标准错误结构 |
| VectorClock | `vector-clock.schema.json` | 核心协议对象 | 描述因果时钟 |
| AuditEntry | `audit-entry.schema.json` | 核心协议对象 | 描述审计追踪记录 |
| WorkflowStep | `workflow-step.schema.json` | 工作流对象 | 描述单个工作流步骤状态 |
| SnapshotRecord | `snapshot-record.schema.json` | 恢复对象 | 描述快照记录与回滚候选 |

---

## 3. Schema 详情

### 3.1 DeltaPayload

**文件**: `delta-payload.schema.json`  
**Schema ID**: `ghost-channel/schemas/delta-payload.json`

**职责**: 表示两个状态快照之间的最小变化集合。

**必填字段**:
- `added`
- `modified`
- `removed`
- `version_from`
- `version_to`
- `timestamp`

**可选字段**:
- `list_appends`
- `changed_fields`

**典型用途**:
- Memory Sync
- Workflow Sync
- Delta Hash 计算输入

### 3.2 EncryptedStream

**文件**: `encrypted-stream.schema.json`  
**Schema ID**: `ghost-channel/schemas/encrypted-stream.json`

**职责**: 幽灵通道的主线协议消息对象。

**必填字段**:
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

**可选字段**:
- `signature`
- `extensions`

**典型用途**:
- MEMORY_SYNC
- WORKFLOW_SYNC
- DEADLOCK_ALERT
- KNOWLEDGE_UPDATE

### 3.3 AckMessage

**文件**: `ack-message.schema.json`  
**Schema ID**: `ghost-channel/schemas/ack-message.json`

**职责**: 接收方对线协议消息的阶段性或终态确认。

**必填字段**:
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

**可选字段**:
- `extensions`
- `error`

**ACK 枚举**:
- `RECEIVED`
- `VERIFIED`
- `APPLIED`
- `ROLLED_BACK`
- `FAILED`

### 3.4 SyncResult

**文件**: `sync-result.schema.json`  
**Schema ID**: `ghost-channel/schemas/sync-result.json`

**职责**: SDK 层同步调用的标准返回结构。

**必填字段**:
- `success`
- `bandwidth_reduction`
- `latency_ms`
- `consistency_verified`
- `changes_applied`
- `errors`

### 3.5 ErrorObject

**文件**: `error-object.schema.json`  
**Schema ID**: `ghost-channel/schemas/error-object.json`

**职责**: 表达标准化错误信息，供 ACK、SyncResult、审计和 AI 决策使用。

**必填字段**:
- `error_code`
- `error_name`
- `severity`
- `message`
- `retryable`
- `rollback_required`
- `context`
- `timestamp`

### 3.6 VectorClock

**文件**: `vector-clock.schema.json`  
**Schema ID**: `ghost-channel/schemas/vector-clock.json`

**职责**: 描述分布式事件的偏序关系。

**结构特点**:
- 动态 key-value 对象
- key 为节点 ID
- value 为非负整数计数器

### 3.7 AuditEntry

**文件**: `audit-entry.schema.json`  
**Schema ID**: `ghost-channel/schemas/audit-entry.json`

**职责**: 表达单次同步事务的可追溯审计记录。

**必填字段**:
- `transaction_id`
- `timestamp`
- `source_role`
- `destination_role`
- `message_type`
- `delta_hash`
- `merkle_root_before`
- `merkle_root_after`
- `bandwidth_saved_bytes`
- `transmission_duration_ms`
- `signature_verified`
- `tamper_detected`

### 3.8 WorkflowStep

**文件**: `workflow-step.schema.json`  
**职责**: 描述工作流中单个步骤的运行状态、依赖和错误信息。

**状态枚举**:
- `pending`
- `running`
- `completed`
- `failed`
- `blocked`
- `recovered`

### 3.9 SnapshotRecord

**文件**: `snapshot-record.schema.json`  
**职责**: 表达用于恢复与回滚的快照记录。

**必填字段**:
- `snapshot_id`
- `stream_id`
- `sequence_number`
- `state_hash`
- `merkle_root`
- `created_at`
- `status`

**状态枚举**:
- `active`
- `archived`
- `rollback_candidate`
- `corrupted`

---

## 4. 实现优先级建议

### MVP 必须实现

1. `DeltaPayload`
2. `EncryptedStream`
3. `AckMessage`
4. `SyncResult`
5. `ErrorObject`
6. `VectorClock`
7. `AuditEntry`

### 工作流扩展实现

1. `WorkflowStep`
2. `SnapshotRecord`

---

## 5. 维护约定

未来若新增 schema，建议同时更新：

1. 本注册表
2. `schemas/README.md`
3. 协议规范稿中的对象模型章节
4. RFC 草案中的 Core Objects 章节

---

*本文件作为幽灵通道 SDK 的 schema 注册表，用于统一对象索引与维护。*
