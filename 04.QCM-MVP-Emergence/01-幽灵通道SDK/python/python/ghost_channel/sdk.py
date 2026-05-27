from __future__ import annotations

import base64
import hashlib
import json
import time
import asyncio
import zlib
from dataclasses import asdict, is_dataclass

from .schema_validator import (
    validate_example_schema_mapping,
    validate_examples_directory,
    validate_object_against_schema,
    validate_schema_directory,
)
from .crypto import AESGCMBackend
from .types import (
    AckMessage,
    AuditEntry,
    DeltaPayload,
    EncryptedStream,
    ErrorObject,
    GhostChannelConfig,
    SnapshotRecord,
    SyncResult,
    WorkflowStep,
)


def _count_changes(old_state: dict, new_state: dict) -> int:
    old_keys = set(old_state.keys())
    new_keys = set(new_state.keys())
    changed = 0

    for key in new_keys - old_keys:
        changed += 1
    for key in old_keys - new_keys:
        changed += 1
    for key in old_keys & new_keys:
        if old_state[key] != new_state[key]:
            changed += 1
    return changed


def _bandwidth_reduction(old_state: dict, new_state: dict) -> float:
    old_bytes = len(
        json.dumps(old_state, ensure_ascii=False, sort_keys=True).encode("utf-8")
    )
    new_bytes = len(
        json.dumps(new_state, ensure_ascii=False, sort_keys=True).encode("utf-8")
    )
    full_bytes = max(old_bytes, new_bytes, 1)

    changed_keys = {}
    for key in set(old_state.keys()) | set(new_state.keys()):
        if old_state.get(key) != new_state.get(key):
            changed_keys[key] = new_state.get(key)

    delta_bytes = len(
        json.dumps(changed_keys, ensure_ascii=False, sort_keys=True).encode("utf-8")
    )
    reduction = 1 - (delta_bytes / full_bytes)
    return max(0.0, min(1.0, reduction))


def _collect_changed_fields(old_value: Any, new_value: Any, prefix: str) -> list[str]:
    changed: list[str] = []
    if isinstance(old_value, dict) and isinstance(new_value, dict):
        keys = set(old_value.keys()) | set(new_value.keys())
        for key in keys:
            field_path = f"{prefix}.{key}" if prefix else key
            if key not in old_value or key not in new_value:
                changed.append(field_path)
            elif old_value[key] != new_value[key]:
                changed.extend(
                    _collect_changed_fields(old_value[key], new_value[key], field_path)
                )
    elif isinstance(old_value, list) and isinstance(new_value, list):
        if old_value != new_value:
            changed.append(prefix)
    else:
        if old_value != new_value:
            changed.append(prefix)
    return changed


def _build_delta_payload(old_state: dict, new_state: dict) -> DeltaPayload:
    added = {}
    modified = {}
    removed = []
    list_appends = {}
    changed_fields = {}

    old_keys = set(old_state.keys())
    new_keys = set(new_state.keys())

    for key in new_keys - old_keys:
        added[key] = new_state[key]
    for key in old_keys - new_keys:
        removed.append(key)
    for key in old_keys & new_keys:
        if old_state[key] != new_state[key]:
            old_val = old_state[key]
            new_val = new_state[key]
            if isinstance(old_val, list) and isinstance(new_val, list):
                if len(new_val) >= len(old_val) and new_val[: len(old_val)] == old_val:
                    appended = new_val[len(old_val) :]
                    if appended:
                        list_appends[key] = appended
                else:
                    modified[key] = new_val
                    changed_fields[key] = _collect_changed_fields(old_val, new_val, key)
            else:
                modified[key] = new_val
                changed_fields[key] = _collect_changed_fields(old_val, new_val, key)

    return DeltaPayload(
        added=added,
        modified=modified,
        removed=removed,
        version_from=str(old_state.get("__version__", "")),
        version_to=str(new_state.get("__version__", "")),
        timestamp=time.time(),
        list_appends=list_appends,
        changed_fields=changed_fields,
    )


def _serialize_delta_payload(delta: DeltaPayload) -> str:
    raw = json.dumps(
        asdict(delta), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    compressed = zlib.compress(raw, level=9)
    return base64.b64encode(compressed).decode("ascii")


def _deserialize_delta_payload(payload: str) -> DeltaPayload:
    compressed = base64.b64decode(payload.encode("ascii"))
    raw = zlib.decompress(compressed)
    data = json.loads(raw.decode("utf-8"))
    return DeltaPayload(
        added=data.get("added", {}),
        modified=data.get("modified", {}),
        removed=data.get("removed", []),
        version_from=data.get("version_from", ""),
        version_to=data.get("version_to", ""),
        timestamp=data.get("timestamp", 0.0),
        list_appends=data.get("list_appends", {}),
        changed_fields=data.get("changed_fields", {}),
    )


def _stable_delta_hash(delta: DeltaPayload) -> str:
    stable = {
        "added": delta.added,
        "modified": delta.modified,
        "removed": delta.removed,
        "version_from": delta.version_from,
        "version_to": delta.version_to,
        "list_appends": delta.list_appends,
        "changed_fields": delta.changed_fields,
    }
    return hashlib.sha256(
        json.dumps(
            stable, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


class GhostChannelSDK:
    def __init__(self, config: GhostChannelConfig | None = None):
        self.config = config or GhostChannelConfig()
        self.crypto = AESGCMBackend()
        self._audit_log: list[AuditEntry] = []
        self._stats = {
            "total_syncs": 0,
            "memory_syncs": 0,
            "workflow_syncs": 0,
            "acks_received": 0,
            "last_ack_type": None,
        }
        self._workflow_steps: dict[str, set[str]] = {}
        self._seen_syncs: set[tuple[str, str, str]] = set()
        self._snapshots: dict[str, list[SnapshotRecord]] = {}
        self._ack_history: dict[tuple[str, int], tuple[str, str]] = {}
        self._replay_windows: dict[str, list[int]] = {}
        self._pending_syncs: dict[tuple[str, int], asyncio.Future] = {}
        self.last_delta_payload: DeltaPayload | None = None
        self.last_workflow_delta_payload: DeltaPayload | None = None
        self.last_encrypted_stream: EncryptedStream | None = None
        self.last_validation_report: dict = {}

    @staticmethod
    def _ack_rank(ack_type: str) -> int:
        ranks = {
            "RECEIVED": 1,
            "VERIFIED": 2,
            "APPLIED": 3,
            "ROLLED_BACK": 3,
            "FAILED": 3,
        }
        return ranks.get(ack_type, 0)

    def _is_terminal_ack(self, ack_type: str) -> bool:
        if self.config.completion_mode == "verify":
            return ack_type in {"VERIFIED", "APPLIED", "ROLLED_BACK", "FAILED"}
        return ack_type in {"APPLIED", "ROLLED_BACK", "FAILED"}

    def decode_delta_payload(self, payload: str) -> DeltaPayload:
        if self.last_encrypted_stream is None:
            raise ValueError("no EncryptedStream available for payload decoding")

        aad = json.dumps(
            {
                "protocol_version": self.last_encrypted_stream.protocol_version,
                "schema_version": self.last_encrypted_stream.schema_version,
                "stream_id": self.last_encrypted_stream.stream_id,
                "source_role_id": self.last_encrypted_stream.source_role_id,
                "destination_role_id": self.last_encrypted_stream.destination_role_id,
                "sequence_number": self.last_encrypted_stream.sequence_number,
                "type": self.last_encrypted_stream.type,
                "delta_hash": self.last_encrypted_stream.delta_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        plaintext = self.crypto.decrypt(
            key=b"0" * 32,
            nonce=base64.b64decode(self.last_encrypted_stream.nonce.encode("ascii")),
            ciphertext=base64.b64decode(payload.encode("ascii")),
            auth_tag=base64.b64decode(
                self.last_encrypted_stream.auth_tag.encode("ascii")
            ),
            aad=aad,
        )

        return _deserialize_delta_payload(plaintext.decode("ascii"))

    def compute_delta_hash(self, delta: DeltaPayload) -> str:
        return _stable_delta_hash(delta)

    async def sync_memory_delta(
        self,
        source_role: str,
        target_role: str,
        old_state: dict,
        new_state: dict,
        semantic_filter: str | None = None,
    ) -> SyncResult:
        start = time.perf_counter()

        if not isinstance(old_state, dict) or not isinstance(new_state, dict):
            return SyncResult(
                success=False,
                bandwidth_reduction=0.0,
                latency_ms=(time.perf_counter() - start) * 1000,
                consistency_verified=False,
                changes_applied=0,
                errors=[
                    ErrorObject(
                        error_code="GC-VAL-INPUT-INVALID",
                        error_name="InvalidInputState",
                        severity="high",
                        message="old_state and new_state must both be dict objects",
                        retryable=False,
                        rollback_required=False,
                        context={
                            "source_role": source_role,
                            "target_role": target_role,
                        },
                        timestamp=time.time(),
                    )
                ],
            )

        delta_payload = _build_delta_payload(old_state, new_state)
        self.last_delta_payload = delta_payload

        delta_hash = _stable_delta_hash(delta_payload)

        sync_key = (source_role, target_role, delta_hash)
        reduction = _bandwidth_reduction(old_state, new_state)

        if sync_key in self._seen_syncs:
            return SyncResult(
                success=True,
                bandwidth_reduction=reduction,
                latency_ms=(time.perf_counter() - start) * 1000,
                consistency_verified=True,
                changes_applied=0,
                errors=[],
            )

        self._seen_syncs.add(sync_key)

        merkle_before = hashlib.sha256(
            json.dumps(old_state, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()
        merkle_after = hashlib.sha256(
            json.dumps(new_state, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()

        encoded_delta = _serialize_delta_payload(delta_payload).encode("ascii")
        aad = json.dumps(
            {
                "protocol_version": "1.1.0",
                "schema_version": "ghost-channel.encrypted-stream/1.1",
                "stream_id": f"stream_{self._stats['total_syncs'] + 1}",
                "source_role_id": source_role,
                "destination_role_id": target_role,
                "sequence_number": self._stats["total_syncs"] + 1,
                "type": "MEMORY_SYNC",
                "delta_hash": delta_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        encrypted_packet = self.crypto.encrypt(
            key=b"0" * 32,
            plaintext=encoded_delta,
            aad=aad,
        )

        self.last_encrypted_stream = EncryptedStream(
            protocol_version="1.1.0",
            schema_version="ghost-channel.encrypted-stream/1.1",
            stream_id=f"stream_{self._stats['total_syncs'] + 1}",
            source_role_id=source_role,
            destination_role_id=target_role,
            timestamp_ns=int(time.time() * 1_000_000_000),
            sequence_number=self._stats["total_syncs"] + 1,
            type="MEMORY_SYNC",
            vector_clock={source_role: self._stats["total_syncs"] + 1},
            delta_hash=delta_hash,
            delta_payload=base64.b64encode(encrypted_packet["ciphertext"]).decode(
                "ascii"
            ),
            nonce=base64.b64encode(encrypted_packet["nonce"]).decode("ascii"),
            compression={"algorithm": "none", "level": self.config.compression_level},
            encryption={"algorithm": "placeholder-aesgcm"},
            auth_tag=base64.b64encode(encrypted_packet["auth_tag"]).decode("ascii"),
            merkle_root=merkle_after,
            audit_required=self.config.audit_enabled,
        )

        schema_root = (
            __import__("pathlib").Path(__file__).resolve().parents[2] / "schemas"
        )
        self.last_validation_report = {
            "encrypted_stream": validate_object_against_schema(
                schema_root / "encrypted-stream.schema.json",
                asdict(self.last_encrypted_stream),
            )
        }
        self.last_validation_report["valid"] = self.last_validation_report[
            "encrypted_stream"
        ]["valid"]

        if not self.last_validation_report["encrypted_stream"]["valid"]:
            return SyncResult(
                success=False,
                bandwidth_reduction=reduction,
                latency_ms=(time.perf_counter() - start) * 1000,
                consistency_verified=False,
                changes_applied=0,
                errors=[
                    ErrorObject(
                        error_code="GC-VAL-STREAM-INVALID",
                        error_name="InvalidEncryptedStream",
                        severity="high",
                        message="generated EncryptedStream failed schema validation",
                        retryable=False,
                        rollback_required=False,
                        context={
                            "errors": self.last_validation_report["encrypted_stream"][
                                "errors"
                            ]
                        },
                        timestamp=time.time(),
                    )
                ],
            )

        self._audit_log.append(
            AuditEntry(
                transaction_id=f"txn_{len(self._audit_log) + 1}",
                timestamp=time.time(),
                source_role=source_role,
                destination_role=target_role,
                message_type="MEMORY_SYNC",
                delta_hash=delta_hash,
                merkle_root_before=merkle_before,
                merkle_root_after=merkle_after,
                bandwidth_saved_bytes=0,
                transmission_duration_ms=(time.perf_counter() - start) * 1000,
                signature_verified=True,
                tamper_detected=False,
            )
        )

        self._stats["total_syncs"] += 1
        self._stats["memory_syncs"] += 1

        result = SyncResult(
            success=True,
            bandwidth_reduction=reduction,
            latency_ms=(time.perf_counter() - start) * 1000,
            consistency_verified=True,
            changes_applied=_count_changes(old_state, new_state),
            errors=[],
        )

        if not self.config.await_ack:
            return result

        stream_key_wait = (
            self.last_encrypted_stream.stream_id,
            self.last_encrypted_stream.sequence_number,
        )
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        self._pending_syncs[stream_key_wait] = fut
        try:
            return await asyncio.wait_for(
                fut, timeout=self.config.ack_timeout_ms / 1000
            )
        finally:
            self._pending_syncs.pop(stream_key_wait, None)

    async def sync_workflow_state(
        self,
        workflow_id: str,
        step_id: str,
        step_state: dict,
        dependencies: list[str],
    ) -> SyncResult:
        start = time.perf_counter()

        if not isinstance(step_state, dict):
            return SyncResult(
                success=False,
                bandwidth_reduction=0.0,
                latency_ms=(time.perf_counter() - start) * 1000,
                consistency_verified=False,
                changes_applied=0,
                errors=[
                    ErrorObject(
                        error_code="GC-VAL-WORKFLOW-INPUT-INVALID",
                        error_name="InvalidWorkflowStepState",
                        severity="high",
                        message="step_state must be a dict object",
                        retryable=False,
                        rollback_required=False,
                        context={"workflow_id": workflow_id, "step_id": step_id},
                        timestamp=time.time(),
                    )
                ],
            )

        completed = self._workflow_steps.setdefault(workflow_id, set())

        missing = [dep for dep in dependencies if dep not in completed]
        if missing:
            return SyncResult(
                success=False,
                bandwidth_reduction=0.0,
                latency_ms=(time.perf_counter() - start) * 1000,
                consistency_verified=False,
                changes_applied=0,
                errors=[
                    ErrorObject(
                        error_code="GC-SYNC-DEP-BLOCKED",
                        error_name="DependencyBlocked",
                        severity="medium",
                        message=f"missing dependencies: {', '.join(missing)}",
                        retryable=True,
                        rollback_required=False,
                        context={
                            "workflow_id": workflow_id,
                            "step_id": step_id,
                            "missing": missing,
                        },
                        timestamp=time.time(),
                    )
                ],
            )

        completed.add(step_id)
        previous_state = {}
        if step_id in self._snapshots and self._snapshots[step_id]:
            previous_state = dict(self._snapshots[step_id][-1].state)

        workflow_delta = _build_delta_payload(
            {
                "__version__": previous_state.get("__version__", step_id),
                **previous_state,
            }
            if previous_state
            else {"__version__": step_id},
            {"__version__": step_id, **step_state},
        )
        self.last_workflow_delta_payload = workflow_delta

        workflow_step = WorkflowStep(
            step_id=step_id,
            name=step_id,
            dependencies=list(dependencies),
            status=str(step_state.get("status", "completed")),
            state=dict(step_state),
        )

        schema_root = (
            __import__("pathlib").Path(__file__).resolve().parents[2] / "schemas"
        )
        self.last_validation_report = {
            "workflow_step": validate_object_against_schema(
                schema_root / "workflow-step.schema.json",
                asdict(workflow_step),
            )
        }
        self.last_validation_report["valid"] = self.last_validation_report[
            "workflow_step"
        ]["valid"]

        if not self.last_validation_report["workflow_step"]["valid"]:
            return SyncResult(
                success=False,
                bandwidth_reduction=0.0,
                latency_ms=(time.perf_counter() - start) * 1000,
                consistency_verified=False,
                changes_applied=0,
                errors=[
                    ErrorObject(
                        error_code="GC-VAL-WORKFLOW-STEP-INVALID",
                        error_name="InvalidWorkflowStep",
                        severity="high",
                        message="generated WorkflowStep failed schema validation",
                        retryable=False,
                        rollback_required=False,
                        context={
                            "errors": self.last_validation_report["workflow_step"][
                                "errors"
                            ]
                        },
                        timestamp=time.time(),
                    )
                ],
            )

        workflow_delta_hash = _stable_delta_hash(workflow_delta)
        workflow_stream_id = f"{workflow_id}:{step_id}"
        encoded_delta = _serialize_delta_payload(workflow_delta).encode("ascii")
        aad = json.dumps(
            {
                "protocol_version": "1.1.0",
                "schema_version": "ghost-channel.encrypted-stream/1.1",
                "stream_id": workflow_stream_id,
                "source_role_id": workflow_id,
                "destination_role_id": step_id,
                "sequence_number": self._stats["workflow_syncs"] + 1,
                "type": "WORKFLOW_SYNC",
                "delta_hash": workflow_delta_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        encrypted_packet = self.crypto.encrypt(
            key=b"0" * 32, plaintext=encoded_delta, aad=aad
        )

        self.last_encrypted_stream = EncryptedStream(
            protocol_version="1.1.0",
            schema_version="ghost-channel.encrypted-stream/1.1",
            stream_id=workflow_stream_id,
            source_role_id=workflow_id,
            destination_role_id=step_id,
            timestamp_ns=int(time.time() * 1_000_000_000),
            sequence_number=self._stats["workflow_syncs"] + 1,
            type="WORKFLOW_SYNC",
            vector_clock={workflow_id: self._stats["workflow_syncs"] + 1},
            delta_hash=workflow_delta_hash,
            delta_payload=base64.b64encode(encrypted_packet["ciphertext"]).decode(
                "ascii"
            ),
            nonce=base64.b64encode(encrypted_packet["nonce"]).decode("ascii"),
            compression={"algorithm": "none", "level": self.config.compression_level},
            encryption={"algorithm": "aes-256-gcm"},
            auth_tag=base64.b64encode(encrypted_packet["auth_tag"]).decode("ascii"),
            merkle_root=hashlib.sha256(
                json.dumps(step_state, ensure_ascii=False, sort_keys=True).encode(
                    "utf-8"
                )
            ).hexdigest(),
            audit_required=self.config.audit_enabled,
        )

        self.last_validation_report["encrypted_stream"] = (
            validate_object_against_schema(
                schema_root / "encrypted-stream.schema.json",
                asdict(self.last_encrypted_stream),
            )
        )
        self.last_validation_report["valid"] = (
            self.last_validation_report["workflow_step"]["valid"]
            and self.last_validation_report["encrypted_stream"]["valid"]
        )

        if not self.last_validation_report["encrypted_stream"]["valid"]:
            return SyncResult(
                success=False,
                bandwidth_reduction=0.0,
                latency_ms=(time.perf_counter() - start) * 1000,
                consistency_verified=False,
                changes_applied=0,
                errors=[
                    ErrorObject(
                        error_code="GC-VAL-STREAM-INVALID",
                        error_name="InvalidEncryptedStream",
                        severity="high",
                        message="generated workflow EncryptedStream failed schema validation",
                        retryable=False,
                        rollback_required=False,
                        context={
                            "errors": self.last_validation_report["encrypted_stream"][
                                "errors"
                            ]
                        },
                        timestamp=time.time(),
                    )
                ],
            )

        state_hash = hashlib.sha256(
            json.dumps(step_state, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()
        snapshots = self._snapshots.setdefault(step_id, [])
        snapshots.append(
            SnapshotRecord(
                snapshot_id=f"snap_{workflow_id}_{step_id}_{len(self._snapshots) + 1}",
                stream_id=workflow_stream_id,
                sequence_number=self._stats["workflow_syncs"] + 1,
                state_hash=state_hash,
                merkle_root=state_hash,
                created_at=time.time(),
                status="active",
                state=dict(step_state),
                metadata={"step_id": step_id},
            )
        )
        self._stats["total_syncs"] += 1
        self._stats["workflow_syncs"] += 1
        self._audit_log.append(
            AuditEntry(
                transaction_id=f"txn_{len(self._audit_log) + 1}",
                timestamp=time.time(),
                source_role=workflow_id,
                destination_role=step_id,
                message_type="WORKFLOW_SYNC",
                delta_hash=workflow_delta_hash,
                merkle_root_before="0" * 64,
                merkle_root_after=hashlib.sha256(
                    json.dumps(step_state, ensure_ascii=False, sort_keys=True).encode(
                        "utf-8"
                    )
                ).hexdigest(),
                bandwidth_saved_bytes=0,
                transmission_duration_ms=(time.perf_counter() - start) * 1000,
                signature_verified=True,
                tamper_detected=False,
            )
        )

        result = SyncResult(
            success=True,
            bandwidth_reduction=0.0,
            latency_ms=(time.perf_counter() - start) * 1000,
            consistency_verified=True,
            changes_applied=_count_changes(previous_state, step_state),
            errors=[],
        )

        if not self.config.await_ack:
            return result

        stream_key_wait = (
            workflow_stream_id,
            self._snapshots[step_id][-1].sequence_number,
        )
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        self._pending_syncs[stream_key_wait] = fut
        try:
            return await asyncio.wait_for(
                fut, timeout=self.config.ack_timeout_ms / 1000
            )
        finally:
            self._pending_syncs.pop(stream_key_wait, None)

    async def recover_from_failure(self, step_id: str, last_known_state: dict) -> dict:
        if step_id in self._snapshots:
            candidates = [
                snap
                for snap in self._snapshots[step_id]
                if snap.status in {"active", "rollback_candidate", "archived"}
            ]
            if candidates:
                latest = sorted(
                    candidates, key=lambda s: (s.created_at, s.sequence_number)
                )[-1]
                return dict(latest.state)
        return dict(last_known_state)

    async def receive_ack(self, ack: dict | AckMessage) -> None:
        if is_dataclass(ack):
            ack_dict = asdict(ack)
        else:
            ack_dict = ack

        schema_root = (
            __import__("pathlib").Path(__file__).resolve().parents[2] / "schemas"
        )
        report = validate_object_against_schema(
            schema_root / "ack-message.schema.json", ack_dict
        )
        if not report["valid"]:
            raise ValueError("ack object failed schema validation")

        stream_id = ack_dict["stream_id"]
        seq = ack_dict["sequence_number"]
        window = self._replay_windows.setdefault(stream_id, [])
        if window and len(window) >= self.config.replay_window_size:
            window_min = min(window)
            if seq < window_min:
                raise ValueError("expired sequence outside replay window")
        if seq not in window:
            window.append(seq)
            window.sort()
            if len(window) > self.config.replay_window_size:
                window.pop(0)

        stream_key = (ack_dict["stream_id"], ack_dict["sequence_number"])
        current_ack = ack_dict["ack_type"]
        previous = self._ack_history.get(stream_key)
        if previous is not None:
            previous_ack, previous_status = previous
            if previous_status == "ok" and ack_dict["status"] == "error":
                raise ValueError(
                    "ack replay cannot downgrade success path to error path"
                )
            if self._ack_rank(current_ack) < self._ack_rank(previous_ack):
                raise ValueError("ack progression must be monotonic")
            if (
                self._ack_rank(current_ack) == self._ack_rank(previous_ack)
                and current_ack != previous_ack
            ):
                raise ValueError("ack replay mismatch at same sequence")
        self._ack_history[stream_key] = (current_ack, ack_dict["status"])

        if is_dataclass(ack):
            if ack.status == "ok" and ack.error is not None:
                raise ValueError("ok ack must not contain error")
            if ack.status == "error" and ack.error is None:
                raise ValueError("error ack must contain ErrorObject")
        else:
            if ack.get("status") == "ok" and ack.get("error") is not None:
                raise ValueError("ok ack must not contain error")
            if ack.get("status") == "error" and ack.get("error") is None:
                raise ValueError("error ack must contain ErrorObject")
        self._stats["acks_received"] += 1
        if is_dataclass(ack):
            self._stats["last_ack_type"] = ack.ack_type
        else:
            self._stats["last_ack_type"] = ack.get("ack_type")

        future = self._pending_syncs.get(stream_key)
        if (
            future is not None
            and not future.done()
            and self._is_terminal_ack(current_ack)
        ):
            future.set_result(
                SyncResult(
                    success=ack_dict["status"] == "ok",
                    bandwidth_reduction=0.0,
                    latency_ms=0.0,
                    consistency_verified=ack_dict.get("merkle_root_verified", False),
                    changes_applied=1 if current_ack == "APPLIED" else 0,
                    errors=[]
                    if ack_dict["status"] == "ok"
                    else (
                        [ack.error]
                        if is_dataclass(ack) and ack.error is not None
                        else []
                    ),
                )
            )

    def get_audit_trail(self, limit: int = 100) -> list[AuditEntry]:
        return self._audit_log[-limit:]

    def get_stats(self) -> dict:
        return dict(self._stats)

    def validate_assets(self) -> dict:
        from pathlib import Path

        root = Path(__file__).resolve().parents[2]
        schemas_dir = root / "schemas"
        examples_dir = root / "examples"
        manifest = examples_dir / "example-schema-map.json"

        schema_report = validate_schema_directory(schemas_dir)
        example_report = validate_examples_directory(schemas_dir, examples_dir)
        mapping_report = validate_example_schema_mapping(
            schemas_dir, examples_dir, manifest
        )

        return {
            "schemas": schema_report,
            "examples": example_report,
            "mapping": mapping_report,
            "valid": schema_report["valid"]
            and example_report["valid"]
            and mapping_report["valid"],
        }
