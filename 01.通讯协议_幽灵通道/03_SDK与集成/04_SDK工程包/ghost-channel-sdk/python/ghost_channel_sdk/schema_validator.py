from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _iter_schema_files(schemas_dir: Path) -> list[Path]:
    return sorted(p for p in schemas_dir.glob("*.schema.json") if p.is_file())


def _collect_refs(obj: Any, refs: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "$ref" and isinstance(value, str):
                refs.append(value)
            else:
                _collect_refs(value, refs)
    elif isinstance(obj, list):
        for item in obj:
            _collect_refs(item, refs)


def _build_ref_graph(schema_files: list[Path]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for schema_file in schema_files:
        refs: list[str] = []
        data = json.loads(schema_file.read_text(encoding="utf-8"))
        _collect_refs(data, refs)
        graph[schema_file.name] = set()
        for ref in refs:
            if ref.startswith("./"):
                graph[schema_file.name].add(Path(ref[2:]).name)
    return graph


def _detect_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node: str, path: list[str]) -> None:
        if node in visiting:
            if node in path:
                idx = path.index(node)
                cycles.append(path[idx:] + [node])
            return
        if node in visited:
            return
        visiting.add(node)
        path.append(node)
        for neigh in graph.get(node, set()):
            if neigh in graph:
                dfs(neigh, path)
        path.pop()
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        dfs(node, [])
    return cycles


def _load_schema(schema_path: Path) -> dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def _resolve_ref(base_schema: Path, ref: str) -> dict[str, Any]:
    if not ref.startswith("./"):
        raise ValueError(f"unsupported ref format: {ref}")
    target = (base_schema.parent / ref[2:]).resolve()
    return _load_schema(target)


def _type_matches(expected: str, value: Any) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(
            value, bool
        )
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _validate_value(
    schema: dict[str, Any], value: Any, schema_path: Path, path: str, errors: list[str]
) -> None:
    if "$ref" in schema:
        ref_schema = _resolve_ref(schema_path, schema["$ref"])
        _validate_value(
            ref_schema,
            value,
            (schema_path.parent / schema["$ref"][2:]).resolve(),
            path,
            errors,
        )
        return

    if "oneOf" in schema:
        branch_errors: list[list[str]] = []
        for branch in schema["oneOf"]:
            local_errors: list[str] = []
            _validate_value(branch, value, schema_path, path, local_errors)
            if not local_errors:
                return
            branch_errors.append(local_errors)
        errors.append(f"{path}: does not satisfy any allowed schema branch")
        return

    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        if not any(_type_matches(t, value) for t in schema_type):
            errors.append(
                f"{path}: expected one of {schema_type}, got {type(value).__name__}"
            )
            return
    elif isinstance(schema_type, str):
        if not _type_matches(schema_type, value):
            errors.append(f"{path}: expected {schema_type}, got {type(value).__name__}")
            return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum {schema['enum']}")
        return

    if schema_type == "object" and isinstance(value, dict):
        required = schema.get("required", [])
        for req in required:
            if req not in value:
                errors.append(f"{path}: missing required field '{req}'")

        properties = schema.get("properties", {})
        additional_allowed = schema.get("additionalProperties", True)
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key in properties:
                _validate_value(properties[key], child, schema_path, child_path, errors)
            elif isinstance(additional_allowed, dict):
                _validate_value(
                    additional_allowed, child, schema_path, child_path, errors
                )
            elif additional_allowed is False:
                errors.append(f"{path}: unexpected field '{key}'")

    if schema_type == "array" and isinstance(value, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for idx, item in enumerate(value):
                _validate_value(
                    item_schema, item, schema_path, f"{path}[{idx}]", errors
                )

    if (
        schema_type == "integer"
        and isinstance(value, int)
        and not isinstance(value, bool)
    ):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value {value} < minimum {schema['minimum']}")

    if (
        schema_type == "number"
        and (isinstance(value, int) or isinstance(value, float))
        and not isinstance(value, bool)
    ):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value {value} > maximum {schema['maximum']}")


def _validate_object_required_properties(
    schema_name: str, obj: Any, errors: list[str]
) -> None:
    if isinstance(obj, dict):
        if obj.get("type") == "object":
            required = obj.get("required", [])
            properties = obj.get("properties", {})
            if isinstance(required, list) and isinstance(properties, dict):
                for key in required:
                    if key not in properties:
                        errors.append(
                            f"{schema_name}: required key '{key}' missing from properties"
                        )
        for value in obj.values():
            _validate_object_required_properties(schema_name, value, errors)
    elif isinstance(obj, list):
        for item in obj:
            _validate_object_required_properties(schema_name, item, errors)


def _validate_enums(schema_name: str, obj: Any, errors: list[str]) -> None:
    if isinstance(obj, dict):
        if "enum" in obj:
            enum_values = obj.get("enum")
            if not isinstance(enum_values, list) or len(enum_values) == 0:
                errors.append(f"{schema_name}: empty enum")
            elif len(enum_values) != len(set(map(str, enum_values))):
                errors.append(f"{schema_name}: duplicated enum values")
        for value in obj.values():
            _validate_enums(schema_name, value, errors)
    elif isinstance(obj, list):
        for item in obj:
            _validate_enums(schema_name, item, errors)


def validate_schema_directory(schemas_dir: Path) -> dict[str, Any]:
    errors: list[str] = []
    files: list[str] = []
    schema_count = 0

    if not schemas_dir.exists() or not schemas_dir.is_dir():
        return {
            "valid": False,
            "schema_count": 0,
            "files": [],
            "errors": [f"schema directory not found: {schemas_dir}"],
        }

    schema_files = _iter_schema_files(schemas_dir)
    schema_count = len(schema_files)
    graph: dict[str, set[str]] = {}

    for schema_file in schema_files:
        files.append(schema_file.name)
        try:
            data = json.loads(schema_file.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(f"{schema_file.name}: invalid json: {exc}")
            continue

        required_top_level = ["$schema", "$id", "title", "type"]
        for key in required_top_level:
            if key not in data:
                errors.append(f"{schema_file.name}: missing top-level key '{key}'")

        _validate_object_required_properties(schema_file.name, data, errors)
        _validate_enums(schema_file.name, data, errors)

        refs: list[str] = []
        _collect_refs(data, refs)
        for ref in refs:
            if ref.startswith("./"):
                target = (schema_file.parent / ref[2:]).resolve()
                if not target.exists():
                    errors.append(
                        f"{schema_file.name}: missing referenced file '{ref}'"
                    )

    # Build ref graph after basic parsing succeeds enough to read files
    try:
        graph = _build_ref_graph(schema_files)
    except Exception:
        graph = {}

    # Orphan detection: only enforced when explicit entry/root schemas exist
    if graph:
        referenced = set().union(*graph.values()) if graph.values() else set()
        roots = {
            name
            for name in graph.keys()
            if name.startswith(("root.", "entry.", "index."))
        }
        if roots:
            for schema_name in graph.keys():
                if schema_name not in referenced and schema_name not in roots:
                    if len(graph) > 1:
                        errors.append(
                            f"{schema_name}: orphan schema (not referenced by any other schema)"
                        )

        # Cycle detection
        for cycle in _detect_cycles(graph):
            if cycle:
                errors.append(f"reference cycle detected: {' -> '.join(cycle)}")

    return {
        "valid": len(errors) == 0,
        "schema_count": schema_count,
        "files": files,
        "errors": errors,
    }


def validate_example_file(schema_path: Path, example_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    try:
        schema = _load_schema(schema_path)
    except Exception as exc:
        return {"valid": False, "errors": [f"failed to load schema: {exc}"]}

    try:
        example = json.loads(example_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"valid": False, "errors": [f"failed to load example: {exc}"]}

    _validate_value(schema, example, schema_path, "root", errors)
    return {
        "valid": len(errors) == 0,
        "schema": schema_path.name,
        "example": example_path.name,
        "errors": errors,
    }


def validate_object_against_schema(
    schema_path: Path, obj: dict[str, Any]
) -> dict[str, Any]:
    errors: list[str] = []
    try:
        schema = _load_schema(schema_path)
    except Exception as exc:
        return {"valid": False, "errors": [f"failed to load schema: {exc}"]}

    _validate_value(schema, obj, schema_path, "root", errors)
    return {
        "valid": len(errors) == 0,
        "schema": schema_path.name,
        "errors": errors,
    }


def validate_examples_directory(
    schemas_dir: Path, examples_dir: Path
) -> dict[str, Any]:
    errors: list[str] = []
    files: list[str] = []

    if not examples_dir.exists() or not examples_dir.is_dir():
        return {
            "valid": False,
            "example_count": 0,
            "files": [],
            "errors": [f"examples directory not found: {examples_dir}"],
        }

    example_files = sorted(
        p for p in examples_dir.glob("*.example.json") if p.is_file()
    )

    for example_file in example_files:
        files.append(example_file.name)
        stem = example_file.name.replace(".example.json", "")
        schema_file = schemas_dir / f"{stem}.schema.json"
        if not schema_file.exists():
            errors.append(
                f"{example_file.name}: missing matching schema '{schema_file.name}'"
            )
            continue

        report = validate_example_file(schema_file, example_file)
        if not report["valid"]:
            errors.extend([f"{example_file.name}: {err}" for err in report["errors"]])

    return {
        "valid": len(errors) == 0,
        "example_count": len(example_files),
        "files": files,
        "errors": errors,
    }


def validate_example_schema_mapping(
    schemas_dir: Path, examples_dir: Path, manifest_path: Path
) -> dict[str, Any]:
    errors: list[str] = []
    files: list[str] = []

    if not manifest_path.exists():
        return {
            "valid": False,
            "mapping_count": 0,
            "files": [],
            "errors": [f"mapping manifest not found: {manifest_path}"],
        }

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "valid": False,
            "mapping_count": 0,
            "files": [],
            "errors": [f"invalid manifest json: {exc}"],
        }

    mappings = manifest.get("mappings", [])
    if not isinstance(mappings, list):
        return {
            "valid": False,
            "mapping_count": 0,
            "files": [],
            "errors": ["manifest field 'mappings' must be a list"],
        }

    for item in mappings:
        example_name = item.get("example")
        schema_name = item.get("schema")
        if not example_name or not schema_name:
            errors.append("mapping item missing 'example' or 'schema'")
            continue

        files.append(example_name)
        example_path = examples_dir / example_name
        schema_path = schemas_dir / schema_name

        if not example_path.exists():
            errors.append(f"{example_name}: missing example file")
            continue
        if not schema_path.exists():
            errors.append(f"{example_name}: missing schema file '{schema_name}'")
            continue

        report = validate_example_file(schema_path, example_path)
        if not report["valid"]:
            errors.extend([f"{example_name}: {err}" for err in report["errors"]])

    return {
        "valid": len(errors) == 0,
        "mapping_count": len(mappings),
        "files": files,
        "errors": errors,
    }


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    schemas_dir = root / "schemas"
    examples_dir = root / "examples"
    manifest_path = examples_dir / "example-schema-map.json"
    schema_report = validate_schema_directory(schemas_dir)
    example_report = validate_examples_directory(schemas_dir, examples_dir)
    mapping_report = validate_example_schema_mapping(
        schemas_dir, examples_dir, manifest_path
    )
    report = {
        "schemas": schema_report,
        "examples": example_report,
        "mapping": mapping_report,
        "valid": schema_report["valid"]
        and example_report["valid"]
        and mapping_report["valid"],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
