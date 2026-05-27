from __future__ import annotations

import argparse
import asyncio
import json
from dataclasses import asdict, is_dataclass
from typing import Any

from .sdk import GhostChannelSDK


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {k: _to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    return value


async def _run_sync_memory_demo() -> dict[str, Any]:
    sdk = GhostChannelSDK()
    result = await sdk.sync_memory_delta(
        source_role="secretary_v1",
        target_role="researcher_v1",
        old_state={"__version__": "v1", "memory": {"anchor_a": {"weight": 0.72}}},
        new_state={
            "__version__": "v2",
            "memory": {"anchor_a": {"weight": 0.88}},
            "interaction_log": [{"role": "secretary_v1", "content": "scope clarified"}],
        },
    )
    return {
        "result": _to_jsonable(result),
        "last_delta_payload": _to_jsonable(sdk.last_delta_payload),
        "last_encrypted_stream": _to_jsonable(sdk.last_encrypted_stream),
        "audit_trail": _to_jsonable(sdk.get_audit_trail()),
        "stats": sdk.get_stats(),
    }


async def _run_workflow_demo() -> dict[str, Any]:
    sdk = GhostChannelSDK()
    await sdk.sync_workflow_state(
        workflow_id="wf_demo",
        step_id="step_01",
        step_state={"status": "completed", "payload": {"x": 1}},
        dependencies=[],
    )
    result = await sdk.sync_workflow_state(
        workflow_id="wf_demo",
        step_id="step_02",
        step_state={"status": "completed", "payload": {"x": 2}},
        dependencies=["step_01"],
    )
    return {
        "result": _to_jsonable(result),
        "last_workflow_delta_payload": _to_jsonable(sdk.last_workflow_delta_payload),
        "snapshots": {
            key: [_to_jsonable(v) for v in values]
            for key, values in sdk._snapshots.items()
        },
        "audit_trail": _to_jsonable(sdk.get_audit_trail()),
        "stats": sdk.get_stats(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="ghost-channel", description="Ghost Channel Python SDK demo runner"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate-assets", help="Validate schemas/examples/mapping assets")
    sub.add_parser("sync-memory-demo", help="Run memory sync demo")
    sub.add_parser("workflow-demo", help="Run workflow sync demo")

    args = parser.parse_args()

    if args.command == "validate-assets":
        sdk = GhostChannelSDK()
        report = sdk.validate_assets()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report.get("valid") else 1

    if args.command == "sync-memory-demo":
        report = asyncio.run(_run_sync_memory_demo())
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    if args.command == "workflow-demo":
        report = asyncio.run(_run_workflow_demo())
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
