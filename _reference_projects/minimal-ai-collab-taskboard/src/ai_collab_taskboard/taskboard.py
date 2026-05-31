"""Deterministic task-card validation for the reference project."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = ("id", "title", "owner", "route", "status", "validation_refs", "stop_line")
VALID_STATUSES = {"todo", "doing", "done", "blocked"}


def load_taskboard(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("taskboard must be a JSON list")
    return data


def validate_task(task: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in task:
            issues.append(f"{task.get('id', '<unknown>')}: missing {field}")

    task_id = str(task.get("id", ""))
    if not task_id.startswith("TASK-"):
        issues.append(f"{task_id or '<unknown>'}: id must start with TASK-")

    if task.get("status") not in VALID_STATUSES:
        issues.append(f"{task_id}: invalid status {task.get('status')!r}")

    validation_refs = task.get("validation_refs")
    if not isinstance(validation_refs, list) or not validation_refs:
        issues.append(f"{task_id}: validation_refs must be a non-empty list")

    if not str(task.get("stop_line", "")).strip():
        issues.append(f"{task_id}: stop_line must be non-empty")

    return issues


def validate_taskboard(tasks: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    for task in tasks:
        issues.extend(validate_task(task))
    return issues


def summarize(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    by_status: dict[str, int] = {}
    for task in tasks:
        status = str(task.get("status", "unknown"))
        by_status[status] = by_status.get(status, 0) + 1
    return {"total": len(tasks), "by_status": by_status}
