#!/usr/bin/env python3
"""Generate atomic inventory and knowledge graph seed for the mother package."""

from __future__ import annotations

import hashlib
import json
import os
import zipfile
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - qa_runner already tolerates missing yaml
    yaml = None


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_DIR = ROOT / "00.超级提示词工程" / "14-全链路审计与运行对齐"
INVENTORY_PATH = REGISTRY_DIR / "ATOMIC-FILE-INVENTORY.jsonl"
SUMMARY_PATH = REGISTRY_DIR / "ATOMIC-FILE-INVENTORY-SUMMARY.md"
GRAPH_PATH = REGISTRY_DIR / "KNOWLEDGE-GRAPH-SEED.yaml"

EXCLUDED_DIR_PARTS = {
    ".git", "__pycache__", ".pytest_cache", "node_modules", "dist", "build", "coverage"
}
EXCLUDED_FILES = {
    str(INVENTORY_PATH.relative_to(ROOT)).replace("\\", "/"),
}

SUBSYSTEM_PREFIX = {
    "00.超级提示词工程": "P00_SUPER_PROMPT",
    "01.通讯协议_幽灵通道": "P01_GHOST_CHANNEL",
    "02.通用知识库框架_Universal-KB": "P02_UNIVERSAL_KB",
    "03.数据库管理_文件夹整理AI应用": "P03_WORKBUDDY_KB",
    "04.QCM-MVP-Emergence": "P04_QCM",
    "05.超极智脑_Q-SpecTrum": "P05_QSPECTRUM",
    "协同通用AI大模型开发交付包": "USER_PACK",
}

TEXT_EXTS = {
    ".md", ".py", ".json", ".yaml", ".yml", ".txt", ".html", ".sql", ".ps1",
    ".bat", ".sh", ".toml", ".js", ".ts", ".jsonc", ".conf", ".example",
    ".template", ".gitignore", ".gitattributes", ".gitmodules", ".css",
}

DOC_EXTS = {".md", ".txt", ".html", ".pdf"}
CODE_EXTS = {".py", ".ps1", ".bat", ".sh", ".js", ".ts"}
DATA_EXTS = {".json", ".jsonl", ".yaml", ".yml", ".db", ".sqlite3", ".sql", ".toml"}
ARCHIVE_EXTS = {".zip", ".skill", ".whl"}


def relpath(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def should_skip(path: Path) -> bool:
    rel = relpath(path)
    if rel in EXCLUDED_FILES:
        return True
    return any(part in EXCLUDED_DIR_PARTS for part in path.relative_to(ROOT).parts)


def subsystem_for(rel: str) -> str:
    first = rel.split("/", 1)[0]
    if first == "qcm-universal-ai-system-v3.0.skill":
        return "QCM_SKILL"
    return SUBSYSTEM_PREFIX.get(first, "ROOT")


def kind_for(path: Path) -> str:
    ext = path.suffix.lower()
    name = path.name.lower()
    if ext in CODE_EXTS:
        return "code"
    if ext in DOC_EXTS:
        return "doc"
    if ext in DATA_EXTS:
        return "data"
    if ext in ARCHIVE_EXTS:
        return "archive"
    if name in {".gitignore", ".gitattributes", ".gitmodules"}:
        return "config"
    return "other"


def priority_for(rel: str, kind: str) -> str:
    p0_names = {
        "MISSION-MEMORY.md",
        "AI_PROJECT_CONTEXT.md",
        "MOTHER-PACK-ACTIVATION-GUIDE.md",
        "qa_runner.py",
        "qcm-universal-ai-system-v3.0.skill",
    }
    if rel in p0_names or "/14-全链路审计与运行对齐/" in rel:
        return "P0"
    if rel.endswith(("README.md", "INDEX.md", "AGENTS.md")):
        return "P1"
    if kind in {"code", "data"}:
        return "P1"
    return "P2"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def line_count(path: Path) -> int | None:
    if path.suffix.lower() not in TEXT_EXTS and path.name not in {".gitignore", ".gitattributes", ".gitmodules"}:
        return None
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except Exception:
        return None


def skill_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    with zipfile.ZipFile(path) as zf:
        for item in sorted(zf.infolist(), key=lambda i: i.filename):
            if item.is_dir():
                continue
            entries.append({
                "path": item.filename,
                "size_bytes": item.file_size,
                "kind": kind_for(Path(item.filename)),
                "audit_state": "inventoried",
            })
    return entries


def build_inventory() -> list[dict]:
    records = []
    for path in sorted(ROOT.rglob("*"), key=lambda p: relpath(p).lower()):
        if not path.is_file() or should_skip(path):
            continue
        rel = relpath(path)
        kind = kind_for(path)
        records.append({
            "path": rel,
            "subsystem": subsystem_for(rel),
            "kind": kind,
            "extension": path.suffix.lower() or path.name,
            "size_bytes": path.stat().st_size,
            "line_count": line_count(path),
            "sha256": sha256_file(path),
            "priority": priority_for(rel, kind),
            "audit_state": "inventoried",
            "evidence_level": "FACT",
            "deep_read_batch": None,
            "crystal_id": None,
            "validation_refs": [],
        })
    return records


def write_inventory(records: list[dict]) -> None:
    with INVENTORY_PATH.open("w", encoding="utf-8", newline="\n") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")


def write_summary(records: list[dict], skill_records: list[dict]) -> None:
    by_subsystem = Counter(r["subsystem"] for r in records)
    by_kind = Counter(r["kind"] for r in records)
    by_priority = Counter(r["priority"] for r in records)
    total_bytes = sum(r["size_bytes"] for r in records)
    lines_known = [r["line_count"] for r in records if r["line_count"] is not None]
    text_lines = sum(lines_known)
    now = datetime.now().isoformat(timespec="seconds")

    def table(counter: Counter) -> str:
        rows = ["| 项 | 数量 |", "|---|---:|"]
        for key, count in sorted(counter.items()):
            rows.append(f"| `{key}` | {count} |")
        return "\n".join(rows)

    content = f"""# Atomic File Inventory Summary

> Generated at: {now}
> Inventory: `ATOMIC-FILE-INVENTORY.jsonl`
> Scope: excludes `.git`, `__pycache__`, `.pytest_cache`, `node_modules`, `dist`, `build`, `coverage`.

## Totals

| Metric | Value |
|---|---:|
| Files inventoried | {len(records)} |
| Bytes inventoried | {total_bytes} |
| Text lines counted | {text_lines} |
| QCM skill internal files | {len(skill_records)} |

## By Subsystem

{table(by_subsystem)}

## By Kind

{table(by_kind)}

## By Priority

{table(by_priority)}

## Audit State

Every record starts at `inventoried`. Future deep-read batches must promote files to `triaged`, `read`, `understood`, `linked`, `validated`, `crystallized`, or `delivery_bound` with evidence.

## QCM Skill Package

The root `qcm-universal-ai-system-v3.0.skill` archive contains {len(skill_records)} internal files. These are tracked as a package-level capability first; deep extraction should happen only when a QCM batch needs the internal scripts, references, tests, or templates.
"""
    SUMMARY_PATH.write_text(content, encoding="utf-8", newline="\n")


def load_yaml(path: Path) -> dict:
    if yaml is None or not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_graph(records: list[dict], skill_records: list[dict]) -> None:
    nodes = []
    edges = []

    projects = load_yaml(REGISTRY_DIR / "PROJECT_REGISTRY.yaml").get("projects", [])
    capabilities = load_yaml(REGISTRY_DIR / "CAPABILITY_REGISTRY.yaml").get("capabilities", [])
    artifacts = load_yaml(REGISTRY_DIR / "ARTIFACT_REGISTRY.yaml").get("artifacts", [])
    validations = load_yaml(REGISTRY_DIR / "VALIDATION_REGISTRY.yaml").get("validations", [])
    memory_sources = load_yaml(REGISTRY_DIR / "MEMORY-SOURCE-INDEX.yaml").get("memory_sources", [])

    for project in projects:
        pid = project.get("id")
        nodes.append({"id": pid, "type": "Project", "path": project.get("path"), "status": project.get("status")})
        for target in project.get("downstream", []) or []:
            edges.append({"from": pid, "to": target, "type": "routes_or_delivers_to"})

    for cap in capabilities:
        cid = cap.get("id")
        owner = cap.get("owner_project")
        nodes.append({"id": cid, "type": "Capability", "owner": owner, "status": cap.get("status")})
        if owner:
            edges.append({"from": owner, "to": cid, "type": "owns"})
        for src in cap.get("source_files", []) or []:
            aid = "FILE:" + src
            edges.append({"from": cid, "to": aid, "type": "implemented_or_defined_by"})

    for art in artifacts:
        aid = art.get("id")
        owner = art.get("owner_project")
        path = art.get("path")
        nodes.append({"id": aid, "type": "Artifact", "owner": owner, "path": path, "artifact_type": art.get("type")})
        if owner:
            edges.append({"from": owner, "to": aid, "type": "owns"})
        if path:
            edges.append({"from": aid, "to": "FILE:" + path, "type": "points_to"})

    for val in validations:
        vid = val.get("id")
        nodes.append({"id": vid, "type": "Validation", "scope": val.get("scope"), "status": val.get("current_status")})
        scope = (val.get("scope") or "").split("/", 1)[0]
        if scope:
            edges.append({"from": vid, "to": scope, "type": "validates"})

    for src in memory_sources:
        sid = src.get("id")
        owner = src.get("owner_project")
        nodes.append({"id": sid, "type": "MemorySource", "owner": owner, "path": src.get("path"), "priority": src.get("read_priority")})
        if owner:
            edges.append({"from": owner, "to": sid, "type": "reads_or_writes_memory"})

    for subsystem, count in Counter(r["subsystem"] for r in records).items():
        nodes.append({"id": "INV:" + subsystem, "type": "InventoryBucket", "subsystem": subsystem, "file_count": count})
        edges.append({"from": subsystem, "to": "INV:" + subsystem, "type": "has_inventory_bucket"})

    nodes.append({"id": "QCM_SKILL_ARCHIVE", "type": "SkillPackage", "path": "qcm-universal-ai-system-v3.0.skill", "internal_file_count": len(skill_records)})
    edges.append({"from": "ROOT", "to": "QCM_SKILL_ARCHIVE", "type": "owns"})
    edges.append({"from": "QCM_SKILL_ARCHIVE", "to": "P04_QCM", "type": "supports_quality_sandbox"})

    graph = {
        "schema_version": "0.1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "purpose": "Seed graph connecting projects, capabilities, artifacts, validations, memory sources, inventory buckets, and QCM skill package.",
        "inventory_ref": relpath(INVENTORY_PATH),
        "nodes": nodes,
        "edges": edges,
    }
    if yaml is not None:
        GRAPH_PATH.write_text(yaml.safe_dump(graph, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n")
    else:
        GRAPH_PATH.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def main() -> int:
    records = build_inventory()
    skill_records = skill_entries(ROOT / "qcm-universal-ai-system-v3.0.skill")
    write_inventory(records)
    write_summary(records, skill_records)
    write_graph(records, skill_records)
    print(f"inventory_records={len(records)}")
    print(f"qcm_skill_internal_files={len(skill_records)}")
    print(f"wrote={relpath(INVENTORY_PATH)}")
    print(f"wrote={relpath(SUMMARY_PATH)}")
    print(f"wrote={relpath(GRAPH_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
