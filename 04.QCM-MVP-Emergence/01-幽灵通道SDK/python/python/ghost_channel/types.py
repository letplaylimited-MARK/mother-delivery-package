from dataclasses import dataclass, field
from typing import Any


@dataclass
class ErrorObject:
    error_code: str
    error_name: str
    severity: str
    message: str
    retryable: bool
    rollback_required: bool
    context: dict[str, Any]
    timestamp: float


@dataclass
class DeltaPayload:
    added: dict[str, Any]
    modified: dict[str, Any]
    removed: list[str]
    version_from: str
    version_to: str
    timestamp: float
    list_appends: dict[str, list[Any]] = field(default_factory=dict)
    changed_fields: dict[str, list[str]] = field(default_factory=dict)


VectorClock = dict[str, int]


@dataclass
class EncryptedStream:
    protocol_version: str
    schema_version: str
    stream_id: str
    source_role_id: str
    destination_role_id: str
    timestamp_ns: int
    sequence_number: int
    type: str
    vector_clock: dict[str, int]
    delta_hash: str
    delta_payload: str
    nonce: str
    compression: dict[str, Any]
    encryption: dict[str, Any]
    auth_tag: str
    merkle_root: str
    audit_required: bool
    signature: str | None = None
    extensions: dict[str, Any] = field(default_factory=dict)


@dataclass
class AckMessage:
    protocol_version: str
    schema_version: str
    stream_id: str
    sequence_number: int
    ack_type: str
    status: str
    receiver_id: str
    merkle_root_verified: bool
    applied: bool
    timestamp_ns: int
    extensions: dict[str, Any] = field(default_factory=dict)
    error: ErrorObject | None = None


@dataclass
class AuditEntry:
    transaction_id: str
    timestamp: float
    source_role: str
    destination_role: str
    message_type: str
    delta_hash: str
    merkle_root_before: str
    merkle_root_after: str
    bandwidth_saved_bytes: int
    transmission_duration_ms: float
    signature_verified: bool
    tamper_detected: bool


@dataclass
class WorkflowStep:
    step_id: str
    name: str
    dependencies: list[str]
    status: str
    start_time: float | None = None
    end_time: float | None = None
    error: str | None = None
    state: dict[str, Any] = field(default_factory=dict)


@dataclass
class SnapshotRecord:
    snapshot_id: str
    stream_id: str
    sequence_number: int
    state_hash: str
    merkle_root: str
    created_at: float
    status: str
    state: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SyncResult:
    success: bool
    bandwidth_reduction: float
    latency_ms: float
    consistency_verified: bool
    changes_applied: int
    errors: list[ErrorObject] = field(default_factory=list)


@dataclass
class GhostChannelConfig:
    compression_level: int = 9
    semantic_threshold: float = 0.70
    audit_enabled: bool = True
    max_retry: int = 3
    completion_mode: str = "apply"
    await_ack: bool = False
    ack_timeout_ms: int = 500
    replay_window_size: int = 1024
