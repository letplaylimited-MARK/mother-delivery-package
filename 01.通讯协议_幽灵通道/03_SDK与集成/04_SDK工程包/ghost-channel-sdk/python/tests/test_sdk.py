import asyncio
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ghost_channel_sdk import (
    AckMessage,
    AuditEntry,
    DeltaPayload,
    EncryptedStream,
    ErrorObject,
    GhostChannelSDK,
    SnapshotRecord,
)
from ghost_channel_sdk.crypto import AESGCMBackend


class GhostChannelSDKTests(unittest.TestCase):
    def test_aesgcm_backend_returns_nonce_ciphertext_tag(self) -> None:
        backend = AESGCMBackend()
        encrypted = backend.encrypt(
            key=b"0" * 32,
            plaintext=b"hello world",
            aad=b"header",
        )

        self.assertIn("nonce", encrypted)
        self.assertIn("ciphertext", encrypted)
        self.assertIn("auth_tag", encrypted)
        self.assertEqual(len(encrypted["nonce"]), 12)

    def test_aesgcm_backend_roundtrip(self) -> None:
        backend = AESGCMBackend()
        encrypted = backend.encrypt(
            key=b"0" * 32,
            plaintext=b"ghost-channel",
            aad=b"aad",
        )
        decrypted = backend.decrypt(
            key=b"0" * 32,
            nonce=encrypted["nonce"],
            ciphertext=encrypted["ciphertext"],
            auth_tag=encrypted["auth_tag"],
            aad=b"aad",
        )
        self.assertEqual(decrypted, b"ghost-channel")

    def test_aesgcm_backend_rejects_tampered_auth_tag(self) -> None:
        backend = AESGCMBackend()
        encrypted = backend.encrypt(
            key=b"0" * 32,
            plaintext=b"ghost-channel",
            aad=b"aad",
        )
        tampered_tag = (
            bytes([encrypted["auth_tag"][0] ^ 0xFF]) + encrypted["auth_tag"][1:]
        )

        with self.assertRaises(ValueError):
            backend.decrypt(
                key=b"0" * 32,
                nonce=encrypted["nonce"],
                ciphertext=encrypted["ciphertext"],
                auth_tag=tampered_tag,
                aad=b"aad",
            )

    def test_aesgcm_backend_rejects_tampered_ciphertext(self) -> None:
        backend = AESGCMBackend()
        encrypted = backend.encrypt(
            key=b"0" * 32,
            plaintext=b"ghost-channel",
            aad=b"aad",
        )
        tampered_ciphertext = (
            bytes([encrypted["ciphertext"][0] ^ 0x01]) + encrypted["ciphertext"][1:]
        )

        with self.assertRaises(ValueError):
            backend.decrypt(
                key=b"0" * 32,
                nonce=encrypted["nonce"],
                ciphertext=tampered_ciphertext,
                auth_tag=encrypted["auth_tag"],
                aad=b"aad",
            )

    def test_aesgcm_backend_rejects_wrong_aad(self) -> None:
        backend = AESGCMBackend()
        encrypted = backend.encrypt(
            key=b"0" * 32,
            plaintext=b"ghost-channel",
            aad=b"aad",
        )

        with self.assertRaises(ValueError):
            backend.decrypt(
                key=b"0" * 32,
                nonce=encrypted["nonce"],
                ciphertext=encrypted["ciphertext"],
                auth_tag=encrypted["auth_tag"],
                aad=b"wrong-aad",
            )

    def test_sdk_uses_real_aesgcm_backend(self) -> None:
        sdk = GhostChannelSDK()
        self.assertIsInstance(sdk.crypto, AESGCMBackend)

    def test_sdk_constructs(self) -> None:
        sdk = GhostChannelSDK()
        self.assertIsNotNone(sdk)

    def test_sync_memory_delta_returns_nonzero_changes_and_audit(self) -> None:
        sdk = GhostChannelSDK()

        old_state = {
            "__version__": "v1",
            "memory": {"anchor_a": {"weight": 0.72}},
            "interaction_log": [],
        }
        new_state = {
            "__version__": "v2",
            "memory": {"anchor_a": {"weight": 0.88}},
            "interaction_log": [{"role": "secretary_v1", "content": "scope clarified"}],
        }

        result = asyncio.run(
            sdk.sync_memory_delta(
                source_role="secretary_v1",
                target_role="researcher_v1",
                old_state=old_state,
                new_state=new_state,
                semantic_filter=None,
            )
        )

        self.assertTrue(result.success)
        self.assertGreater(result.changes_applied, 0)
        self.assertTrue(result.consistency_verified)
        self.assertGreaterEqual(result.bandwidth_reduction, 0)
        audit = sdk.get_audit_trail()
        self.assertEqual(len(audit), 1)
        self.assertIsInstance(audit[0], AuditEntry)

    def test_sync_workflow_state_blocks_when_dependency_missing(self) -> None:
        sdk = GhostChannelSDK()

        result = asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_001",
                step_id="step_02",
                step_state={"status": "completed"},
                dependencies=["step_01"],
            )
        )

        self.assertFalse(result.success)
        self.assertTrue(result.errors)
        self.assertIsInstance(result.errors[0], ErrorObject)
        self.assertEqual(result.errors[0].error_code, "GC-SYNC-DEP-BLOCKED")

    def test_sync_workflow_state_succeeds_when_dependency_preloaded(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_001",
                step_id="step_01",
                step_state={"status": "completed"},
                dependencies=[],
            )
        )

        result = asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_001",
                step_id="step_02",
                step_state={"status": "completed"},
                dependencies=["step_01"],
            )
        )

        self.assertTrue(result.success)
        self.assertGreaterEqual(result.changes_applied, 1)

    def test_sync_workflow_state_rejects_invalid_step_state_input(self) -> None:
        sdk = GhostChannelSDK()

        result = asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_invalid",
                step_id="step_01",
                step_state="not-a-dict",
                dependencies=[],
            )
        )

        self.assertFalse(result.success)
        self.assertTrue(result.errors)
        self.assertEqual(result.errors[0].error_code, "GC-VAL-WORKFLOW-INPUT-INVALID")

    def test_sync_workflow_state_validates_generated_workflow_step_object(self) -> None:
        sdk = GhostChannelSDK()

        result = asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_validate",
                step_id="step_01",
                step_state={"status": "completed", "payload": {"x": 1}},
                dependencies=[],
            )
        )

        self.assertTrue(result.success)
        self.assertIn("workflow_step", sdk.last_validation_report)
        self.assertTrue(sdk.last_validation_report["workflow_step"]["valid"])

    def test_sync_workflow_state_records_last_encrypted_stream_object(self) -> None:
        sdk = GhostChannelSDK()

        result = asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_stream",
                step_id="step_01",
                step_state={"status": "completed", "payload": {"x": 1}},
                dependencies=[],
            )
        )

        self.assertTrue(result.success)
        self.assertIsInstance(sdk.last_encrypted_stream, EncryptedStream)
        self.assertEqual(sdk.last_encrypted_stream.type, "WORKFLOW_SYNC")
        self.assertEqual(sdk.last_encrypted_stream.source_role_id, "wf_stream")
        self.assertEqual(sdk.last_encrypted_stream.destination_role_id, "step_01")

    def test_sync_workflow_state_validates_generated_encrypted_stream_object(
        self,
    ) -> None:
        sdk = GhostChannelSDK()

        result = asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_stream_validate",
                step_id="step_01",
                step_state={"status": "completed", "payload": {"x": 1}},
                dependencies=[],
            )
        )

        self.assertTrue(result.success)
        self.assertIn("encrypted_stream", sdk.last_validation_report)
        self.assertTrue(sdk.last_validation_report["encrypted_stream"]["valid"])

    def test_sync_workflow_state_records_delta_payload_object(self) -> None:
        sdk = GhostChannelSDK()

        result = asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_delta",
                step_id="step_01",
                step_state={"status": "completed", "payload": {"x": 1}},
                dependencies=[],
            )
        )

        self.assertTrue(result.success)
        self.assertIsInstance(sdk.last_workflow_delta_payload, DeltaPayload)
        self.assertEqual(sdk.last_workflow_delta_payload.version_to, "step_01")

    def test_sync_workflow_state_uses_zero_changes_when_payload_is_identical(
        self,
    ) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_same",
                step_id="step_same",
                step_state={"status": "completed", "payload": {"x": 1}},
                dependencies=[],
            )
        )

        result = asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_same",
                step_id="step_same",
                step_state={"status": "completed", "payload": {"x": 1}},
                dependencies=[],
            )
        )

        self.assertTrue(result.success)
        self.assertEqual(result.changes_applied, 0)

    def test_sync_workflow_state_updates_snapshot_chain_with_new_delta(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_chain",
                step_id="step_chain",
                step_state={"status": "completed", "payload": {"x": 1}},
                dependencies=[],
            )
        )
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_chain",
                step_id="step_chain",
                step_state={"status": "completed", "payload": {"x": 2}},
                dependencies=[],
            )
        )

        self.assertEqual(len(sdk._snapshots["step_chain"]), 2)
        self.assertEqual(sdk._snapshots["step_chain"][-1].state["payload"]["x"], 2)

    def test_sync_workflow_state_waits_for_verified_ack_in_verify_mode(self) -> None:
        async def scenario() -> None:
            sdk = GhostChannelSDK()
            sdk.config.completion_mode = "verify"
            sdk.config.await_ack = True

            task = asyncio.create_task(
                sdk.sync_workflow_state(
                    workflow_id="wf_wait_verify",
                    step_id="step_01",
                    step_state={"status": "completed", "payload": {"x": 1}},
                    dependencies=[],
                )
            )

            await asyncio.sleep(0.01)
            self.assertFalse(task.done())

            await sdk.receive_ack(
                AckMessage(
                    protocol_version="1.1.0",
                    schema_version="ghost-channel.ack/1.1",
                    stream_id="wf_wait_verify:step_01",
                    sequence_number=1,
                    ack_type="VERIFIED",
                    status="ok",
                    receiver_id="step_01",
                    merkle_root_verified=True,
                    applied=False,
                    timestamp_ns=1712345678123456789,
                )
            )

            result = await task
            self.assertTrue(result.success)

        asyncio.run(scenario())

    def test_sync_workflow_state_waits_for_applied_ack_in_apply_mode(self) -> None:
        async def scenario() -> None:
            sdk = GhostChannelSDK()
            sdk.config.completion_mode = "apply"
            sdk.config.await_ack = True

            task = asyncio.create_task(
                sdk.sync_workflow_state(
                    workflow_id="wf_wait_apply",
                    step_id="step_01",
                    step_state={"status": "completed", "payload": {"x": 1}},
                    dependencies=[],
                )
            )

            await asyncio.sleep(0.01)
            self.assertFalse(task.done())

            await sdk.receive_ack(
                AckMessage(
                    protocol_version="1.1.0",
                    schema_version="ghost-channel.ack/1.1",
                    stream_id="wf_wait_apply:step_01",
                    sequence_number=1,
                    ack_type="VERIFIED",
                    status="ok",
                    receiver_id="step_01",
                    merkle_root_verified=True,
                    applied=False,
                    timestamp_ns=1712345678123456789,
                )
            )

            await asyncio.sleep(0.01)
            self.assertFalse(task.done())

            await sdk.receive_ack(
                AckMessage(
                    protocol_version="1.1.0",
                    schema_version="ghost-channel.ack/1.1",
                    stream_id="wf_wait_apply:step_01",
                    sequence_number=1,
                    ack_type="APPLIED",
                    status="ok",
                    receiver_id="step_01",
                    merkle_root_verified=True,
                    applied=True,
                    timestamp_ns=1712345678123456799,
                )
            )

            result = await task
            self.assertTrue(result.success)

        asyncio.run(scenario())

    def test_stats_increase_after_operations(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={"__version__": "v1"},
                new_state={"__version__": "v2", "x": 1},
            )
        )
        stats = sdk.get_stats()
        self.assertEqual(stats["total_syncs"], 1)

    def test_receive_ack_updates_ack_stats_and_last_ack(self) -> None:
        sdk = GhostChannelSDK()
        ack = AckMessage(
            protocol_version="1.1.0",
            schema_version="ghost-channel.ack/1.1",
            stream_id="stream_001",
            sequence_number=1,
            ack_type="APPLIED",
            status="ok",
            receiver_id="role_b",
            merkle_root_verified=True,
            applied=True,
            timestamp_ns=1712345678123456789,
        )

        asyncio.run(sdk.receive_ack(ack))

        stats = sdk.get_stats()
        self.assertEqual(stats["acks_received"], 1)
        self.assertEqual(stats["last_ack_type"], "APPLIED")

    def test_audit_entries_are_object_flow_not_dict_flow(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={"__version__": "v1"},
                new_state={"__version__": "v2", "x": 1},
            )
        )
        entry = sdk.get_audit_trail()[0]
        self.assertIsInstance(entry, AuditEntry)
        self.assertEqual(entry.message_type, "MEMORY_SYNC")

    def test_sync_memory_delta_is_idempotent_for_same_payload(self) -> None:
        sdk = GhostChannelSDK()
        old_state = {"__version__": "v1"}
        new_state = {"__version__": "v2", "x": 1}

        first = asyncio.run(sdk.sync_memory_delta("a", "b", old_state, new_state))
        second = asyncio.run(sdk.sync_memory_delta("a", "b", old_state, new_state))

        self.assertTrue(first.success)
        self.assertTrue(second.success)
        self.assertEqual(second.changes_applied, 0)
        self.assertEqual(len(sdk.get_audit_trail()), 1)

    def test_validate_assets_reports_current_sdk_assets_valid(self) -> None:
        sdk = GhostChannelSDK()
        report = sdk.validate_assets()

        self.assertTrue(report["valid"])
        self.assertIn("schemas", report)
        self.assertIn("examples", report)
        self.assertIn("mapping", report)

    def test_sync_memory_delta_records_last_delta_payload_object(self) -> None:
        sdk = GhostChannelSDK()

        result = asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={"__version__": "v1", "x": 1},
                new_state={"__version__": "v2", "x": 2, "y": 3},
            )
        )

        self.assertTrue(result.success)
        self.assertIsInstance(sdk.last_delta_payload, DeltaPayload)
        self.assertEqual(sdk.last_delta_payload.version_from, "v1")
        self.assertEqual(sdk.last_delta_payload.version_to, "v2")

    def test_delta_payload_tracks_changed_fields_for_nested_object(self) -> None:
        sdk = GhostChannelSDK()

        asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={
                    "__version__": "v1",
                    "memory": {"anchor_a": {"weight": 0.72, "label": "old"}},
                },
                new_state={
                    "__version__": "v2",
                    "memory": {"anchor_a": {"weight": 0.88, "label": "new"}},
                },
            )
        )

        delta = sdk.last_delta_payload
        self.assertIn("memory", delta.modified)
        self.assertIn("memory.anchor_a.weight", delta.changed_fields["memory"])
        self.assertIn("memory.anchor_a.label", delta.changed_fields["memory"])

    def test_delta_payload_uses_list_appends_instead_of_full_list_replace(self) -> None:
        sdk = GhostChannelSDK()

        asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={
                    "__version__": "v1",
                    "interaction_log": [{"id": 1, "content": "hello"}],
                },
                new_state={
                    "__version__": "v2",
                    "interaction_log": [
                        {"id": 1, "content": "hello"},
                        {"id": 2, "content": "world"},
                    ],
                },
            )
        )

        delta = sdk.last_delta_payload
        self.assertIn("interaction_log", delta.list_appends)
        self.assertEqual(len(delta.list_appends["interaction_log"]), 1)
        self.assertEqual(delta.list_appends["interaction_log"][0]["id"], 2)
        self.assertNotIn("interaction_log", delta.modified)

    def test_delta_payload_full_list_replace_when_existing_items_change(self) -> None:
        sdk = GhostChannelSDK()

        asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={
                    "__version__": "v1",
                    "interaction_log": [{"id": 1, "content": "hello"}],
                },
                new_state={
                    "__version__": "v2",
                    "interaction_log": [{"id": 1, "content": "changed"}],
                },
            )
        )

        delta = sdk.last_delta_payload
        self.assertIn("interaction_log", delta.modified)
        self.assertNotIn("interaction_log", delta.list_appends)

    def test_sync_memory_delta_records_last_encrypted_stream_object(self) -> None:
        sdk = GhostChannelSDK()

        result = asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={"__version__": "v1"},
                new_state={"__version__": "v2", "payload": {"k": "v"}},
            )
        )

        self.assertTrue(result.success)
        self.assertIsInstance(sdk.last_encrypted_stream, EncryptedStream)
        self.assertEqual(sdk.last_encrypted_stream.source_role_id, "a")
        self.assertEqual(sdk.last_encrypted_stream.destination_role_id, "b")

    def test_sync_memory_delta_waits_for_verified_ack_in_verify_mode(self) -> None:
        async def scenario() -> None:
            sdk = GhostChannelSDK()
            sdk.config.completion_mode = "verify"
            sdk.config.await_ack = True

            task = asyncio.create_task(
                sdk.sync_memory_delta(
                    source_role="a",
                    target_role="b",
                    old_state={"__version__": "v1"},
                    new_state={"__version__": "v2", "x": 1},
                )
            )

            await asyncio.sleep(0.01)
            self.assertFalse(task.done())

            await sdk.receive_ack(
                AckMessage(
                    protocol_version="1.1.0",
                    schema_version="ghost-channel.ack/1.1",
                    stream_id=sdk.last_encrypted_stream.stream_id,
                    sequence_number=sdk.last_encrypted_stream.sequence_number,
                    ack_type="VERIFIED",
                    status="ok",
                    receiver_id="b",
                    merkle_root_verified=True,
                    applied=False,
                    timestamp_ns=1712345678123456789,
                )
            )

            result = await task
            self.assertTrue(result.success)

        asyncio.run(scenario())

    def test_sync_memory_delta_waits_past_verified_in_apply_mode_until_applied(
        self,
    ) -> None:
        async def scenario() -> None:
            sdk = GhostChannelSDK()
            sdk.config.completion_mode = "apply"
            sdk.config.await_ack = True

            task = asyncio.create_task(
                sdk.sync_memory_delta(
                    source_role="a",
                    target_role="b",
                    old_state={"__version__": "v1"},
                    new_state={"__version__": "v2", "x": 1},
                )
            )

            await asyncio.sleep(0.01)
            self.assertFalse(task.done())

            await sdk.receive_ack(
                AckMessage(
                    protocol_version="1.1.0",
                    schema_version="ghost-channel.ack/1.1",
                    stream_id=sdk.last_encrypted_stream.stream_id,
                    sequence_number=sdk.last_encrypted_stream.sequence_number,
                    ack_type="VERIFIED",
                    status="ok",
                    receiver_id="b",
                    merkle_root_verified=True,
                    applied=False,
                    timestamp_ns=1712345678123456789,
                )
            )

            await asyncio.sleep(0.01)
            self.assertFalse(task.done())

            await sdk.receive_ack(
                AckMessage(
                    protocol_version="1.1.0",
                    schema_version="ghost-channel.ack/1.1",
                    stream_id=sdk.last_encrypted_stream.stream_id,
                    sequence_number=sdk.last_encrypted_stream.sequence_number,
                    ack_type="APPLIED",
                    status="ok",
                    receiver_id="b",
                    merkle_root_verified=True,
                    applied=True,
                    timestamp_ns=1712345678123456799,
                )
            )

            result = await task
            self.assertTrue(result.success)

        asyncio.run(scenario())

    def test_encrypted_stream_delta_payload_is_base64_string(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={"__version__": "v1"},
                new_state={"__version__": "v2", "payload": {"k": "v"}},
            )
        )

        encoded = sdk.last_encrypted_stream.delta_payload
        self.assertIsInstance(encoded, str)
        # base64 strings should be decodable
        import base64

        decoded = base64.b64decode(encoded.encode("ascii"))
        self.assertGreater(len(decoded), 0)

    def test_encrypted_stream_payload_roundtrip_recovers_delta_payload_content(
        self,
    ) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={"__version__": "v1", "x": 1},
                new_state={"__version__": "v2", "x": 2, "y": 3},
            )
        )

        decoded = sdk.decode_delta_payload(sdk.last_encrypted_stream.delta_payload)
        self.assertEqual(decoded.version_from, "v1")
        self.assertEqual(decoded.version_to, "v2")
        self.assertEqual(decoded.modified["x"], 2)
        self.assertEqual(decoded.added["y"], 3)

    def test_encrypted_stream_delta_hash_matches_decoded_payload(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={"__version__": "v1"},
                new_state={"__version__": "v2", "x": 1},
            )
        )

        decoded = sdk.decode_delta_payload(sdk.last_encrypted_stream.delta_payload)
        expected_hash = sdk.compute_delta_hash(decoded)
        self.assertEqual(expected_hash, sdk.last_encrypted_stream.delta_hash)

    def test_sync_memory_delta_sets_protocol_versions_on_encrypted_stream(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={"__version__": "v1"},
                new_state={"__version__": "v2", "payload": {"k": "v"}},
            )
        )
        self.assertEqual(sdk.last_encrypted_stream.protocol_version, "1.1.0")
        self.assertEqual(
            sdk.last_encrypted_stream.schema_version,
            "ghost-channel.encrypted-stream/1.1",
        )

    def test_receive_ack_rejects_invalid_ok_ack_with_error(self) -> None:
        sdk = GhostChannelSDK()
        ack = AckMessage(
            protocol_version="1.1.0",
            schema_version="ghost-channel.ack/1.1",
            stream_id="stream_001",
            sequence_number=1,
            ack_type="APPLIED",
            status="ok",
            receiver_id="role_b",
            merkle_root_verified=True,
            applied=True,
            timestamp_ns=1712345678123456789,
            error=ErrorObject(
                error_code="GC-CRY-002",
                error_name="MACVerificationFailed",
                severity="critical",
                message="bad",
                retryable=False,
                rollback_required=True,
                context={},
                timestamp=1712345678.0,
            ),
        )

        with self.assertRaises(ValueError):
            asyncio.run(sdk.receive_ack(ack))

    def test_recover_from_failure_returns_latest_snapshot_when_available(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_recovery",
                step_id="step_01",
                step_state={"status": "completed", "payload": {"x": 1}},
                dependencies=[],
            )
        )

        recovered = asyncio.run(
            sdk.recover_from_failure("step_01", {"status": "fallback"})
        )

        self.assertEqual(recovered["status"], "completed")
        self.assertEqual(recovered["payload"]["x"], 1)

    def test_recover_from_failure_records_snapshot_object(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_snapshot",
                step_id="step_01",
                step_state={"status": "completed", "payload": {"x": 1}},
                dependencies=[],
            )
        )

        self.assertIn("step_01", sdk._snapshots)
        self.assertIsInstance(sdk._snapshots["step_01"][-1], SnapshotRecord)

    def test_recover_from_failure_prefers_snapshot_state_over_fallback(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_snapshot",
                step_id="step_99",
                step_state={"status": "completed", "payload": {"value": 42}},
                dependencies=[],
            )
        )

        recovered = asyncio.run(
            sdk.recover_from_failure(
                "step_99", {"status": "fallback", "payload": {"value": -1}}
            )
        )

        self.assertEqual(recovered["payload"]["value"], 42)

    def test_recover_from_failure_uses_latest_non_corrupted_snapshot(self) -> None:
        sdk = GhostChannelSDK()
        # first snapshot
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_recovery_chain",
                step_id="step_chain",
                step_state={"status": "completed", "payload": {"value": 1}},
                dependencies=[],
            )
        )
        # second snapshot should supersede first
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_recovery_chain",
                step_id="step_chain",
                step_state={"status": "completed", "payload": {"value": 2}},
                dependencies=[],
            )
        )

        recovered = asyncio.run(
            sdk.recover_from_failure(
                "step_chain", {"status": "fallback", "payload": {"value": -1}}
            )
        )

        self.assertEqual(recovered["payload"]["value"], 2)

    def test_recover_from_failure_skips_corrupted_snapshot(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_corrupt",
                step_id="step_corrupt",
                step_state={"status": "completed", "payload": {"value": 1}},
                dependencies=[],
            )
        )
        # corrupt latest snapshot manually
        latest = sdk._snapshots["step_corrupt"][-1]
        latest.status = "corrupted"

        recovered = asyncio.run(
            sdk.recover_from_failure(
                "step_corrupt", {"status": "fallback", "payload": {"value": -1}}
            )
        )

        # no valid snapshot left, should fall back
        self.assertEqual(recovered["payload"]["value"], -1)

    def test_recover_from_failure_prefers_rollback_candidate_snapshot(self) -> None:
        sdk = GhostChannelSDK()
        asyncio.run(
            sdk.sync_workflow_state(
                workflow_id="wf_rollback",
                step_id="step_rb",
                step_state={"status": "completed", "payload": {"value": 10}},
                dependencies=[],
            )
        )
        snap = sdk._snapshots["step_rb"][-1]
        snap.status = "rollback_candidate"

        recovered = asyncio.run(
            sdk.recover_from_failure(
                "step_rb", {"status": "fallback", "payload": {"value": -1}}
            )
        )

        self.assertEqual(recovered["payload"]["value"], 10)

    def test_duplicate_sync_returns_zero_changes_and_does_not_append_audit(
        self,
    ) -> None:
        sdk = GhostChannelSDK()
        old_state = {"__version__": "v1"}
        new_state = {"__version__": "v2", "x": 1}

        first = asyncio.run(sdk.sync_memory_delta("a", "b", old_state, new_state))
        second = asyncio.run(sdk.sync_memory_delta("a", "b", old_state, new_state))

        self.assertTrue(first.success)
        self.assertTrue(second.success)
        self.assertEqual(second.changes_applied, 0)
        self.assertEqual(len(sdk.get_audit_trail()), 1)

    def test_receive_ack_rejects_replayed_sequence_with_different_ack_type(
        self,
    ) -> None:
        sdk = GhostChannelSDK()
        ack1 = AckMessage(
            protocol_version="1.1.0",
            schema_version="ghost-channel.ack/1.1",
            stream_id="stream_001",
            sequence_number=1,
            ack_type="RECEIVED",
            status="ok",
            receiver_id="role_b",
            merkle_root_verified=False,
            applied=False,
            timestamp_ns=1712345678123456789,
        )
        ack2 = AckMessage(
            protocol_version="1.1.0",
            schema_version="ghost-channel.ack/1.1",
            stream_id="stream_001",
            sequence_number=1,
            ack_type="FAILED",
            status="error",
            receiver_id="role_b",
            merkle_root_verified=False,
            applied=False,
            timestamp_ns=1712345678123456799,
            error=ErrorObject(
                error_code="GC-RCV-002",
                error_name="ReplayConflict",
                severity="high",
                message="replayed sequence mismatch",
                retryable=False,
                rollback_required=True,
                context={},
                timestamp=1712345678.0,
            ),
        )

        asyncio.run(sdk.receive_ack(ack1))
        with self.assertRaises(ValueError):
            asyncio.run(sdk.receive_ack(ack2))

    def test_receive_ack_accepts_monotonic_ack_progression(self) -> None:
        sdk = GhostChannelSDK()
        received = AckMessage(
            protocol_version="1.1.0",
            schema_version="ghost-channel.ack/1.1",
            stream_id="stream_002",
            sequence_number=2,
            ack_type="RECEIVED",
            status="ok",
            receiver_id="role_b",
            merkle_root_verified=False,
            applied=False,
            timestamp_ns=1712345678123456789,
        )
        applied = AckMessage(
            protocol_version="1.1.0",
            schema_version="ghost-channel.ack/1.1",
            stream_id="stream_002",
            sequence_number=2,
            ack_type="APPLIED",
            status="ok",
            receiver_id="role_b",
            merkle_root_verified=True,
            applied=True,
            timestamp_ns=1712345678123456799,
        )

        asyncio.run(sdk.receive_ack(received))
        asyncio.run(sdk.receive_ack(applied))

        stats = sdk.get_stats()
        self.assertEqual(stats["last_ack_type"], "APPLIED")

    def test_completion_mode_verify_accepts_verified_ack(self) -> None:
        sdk = GhostChannelSDK()
        sdk.config.completion_mode = "verify"
        self.assertTrue(sdk._is_terminal_ack("VERIFIED"))
        self.assertFalse(sdk._is_terminal_ack("RECEIVED"))

    def test_completion_mode_apply_requires_applied_or_failed_or_rolled_back(
        self,
    ) -> None:
        sdk = GhostChannelSDK()
        sdk.config.completion_mode = "apply"
        self.assertFalse(sdk._is_terminal_ack("VERIFIED"))
        self.assertTrue(sdk._is_terminal_ack("APPLIED"))
        self.assertTrue(sdk._is_terminal_ack("FAILED"))
        self.assertTrue(sdk._is_terminal_ack("ROLLED_BACK"))

    def test_replay_window_allows_recent_duplicate_tracking(self) -> None:
        sdk = GhostChannelSDK()
        sdk.config.replay_window_size = 3

        for seq in (1, 2, 3):
            ack = AckMessage(
                protocol_version="1.1.0",
                schema_version="ghost-channel.ack/1.1",
                stream_id="stream_window",
                sequence_number=seq,
                ack_type="RECEIVED",
                status="ok",
                receiver_id="role_b",
                merkle_root_verified=False,
                applied=False,
                timestamp_ns=1712345678000000000 + seq,
            )
            asyncio.run(sdk.receive_ack(ack))

        self.assertEqual(sdk._replay_windows["stream_window"], [1, 2, 3])

    def test_replay_window_evicts_oldest_sequence_when_capacity_exceeded(self) -> None:
        sdk = GhostChannelSDK()
        sdk.config.replay_window_size = 3

        for seq in (1, 2, 3, 4):
            ack = AckMessage(
                protocol_version="1.1.0",
                schema_version="ghost-channel.ack/1.1",
                stream_id="stream_window",
                sequence_number=seq,
                ack_type="RECEIVED",
                status="ok",
                receiver_id="role_b",
                merkle_root_verified=False,
                applied=False,
                timestamp_ns=1712345678000000000 + seq,
            )
            asyncio.run(sdk.receive_ack(ack))

        self.assertEqual(sdk._replay_windows["stream_window"], [2, 3, 4])

    def test_replay_window_rejects_expired_sequence_outside_window(self) -> None:
        sdk = GhostChannelSDK()
        sdk.config.replay_window_size = 3

        for seq in (1, 2, 3, 4):
            ack = AckMessage(
                protocol_version="1.1.0",
                schema_version="ghost-channel.ack/1.1",
                stream_id="stream_window",
                sequence_number=seq,
                ack_type="RECEIVED",
                status="ok",
                receiver_id="role_b",
                merkle_root_verified=False,
                applied=False,
                timestamp_ns=1712345678000000000 + seq,
            )
            asyncio.run(sdk.receive_ack(ack))

        expired = AckMessage(
            protocol_version="1.1.0",
            schema_version="ghost-channel.ack/1.1",
            stream_id="stream_window",
            sequence_number=1,
            ack_type="RECEIVED",
            status="ok",
            receiver_id="role_b",
            merkle_root_verified=False,
            applied=False,
            timestamp_ns=1712345678999999999,
        )

        with self.assertRaises(ValueError):
            asyncio.run(sdk.receive_ack(expired))

    def test_sync_memory_delta_rejects_invalid_input_state(self) -> None:
        sdk = GhostChannelSDK()

        result = asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state="not-a-dict",
                new_state={"__version__": "v2"},
            )
        )

        self.assertFalse(result.success)
        self.assertTrue(result.errors)
        self.assertEqual(result.errors[0].error_code, "GC-VAL-INPUT-INVALID")

    def test_receive_ack_rejects_invalid_ack_shape(self) -> None:
        sdk = GhostChannelSDK()

        with self.assertRaises(ValueError):
            asyncio.run(sdk.receive_ack({"ack_type": "APPLIED"}))

    def test_sync_memory_delta_validates_generated_encrypted_stream(self) -> None:
        sdk = GhostChannelSDK()
        result = asyncio.run(
            sdk.sync_memory_delta(
                source_role="a",
                target_role="b",
                old_state={"__version__": "v1"},
                new_state={"__version__": "v2", "payload": {"k": "v"}},
            )
        )

        self.assertTrue(result.success)
        self.assertTrue(sdk.last_validation_report["valid"])
        self.assertIn("encrypted_stream", sdk.last_validation_report)


if __name__ == "__main__":
    unittest.main()
