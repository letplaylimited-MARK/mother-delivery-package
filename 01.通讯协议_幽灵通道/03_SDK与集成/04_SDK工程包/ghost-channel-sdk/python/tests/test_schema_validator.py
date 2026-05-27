from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ghost_channel_sdk.schema_validator import (
    validate_examples_directory,
    validate_schema_directory,
    validate_example_file,
    validate_example_schema_mapping,
)


class SchemaValidatorTests(unittest.TestCase):
    def test_validate_schema_directory_reports_all_current_schemas(self) -> None:
        root = Path(__file__).resolve().parents[2]
        schemas_dir = root / "schemas"

        report = validate_schema_directory(schemas_dir)

        self.assertTrue(report["valid"])
        self.assertGreaterEqual(report["schema_count"], 7)
        self.assertEqual(report["errors"], [])
        self.assertIn("delta-payload.schema.json", report["files"])

    def test_validate_schema_directory_detects_missing_ref_file(self) -> None:
        root = Path(__file__).resolve().parent
        tmp_dir = root / "_tmp_schema_validation"
        if tmp_dir.exists():
            for child in tmp_dir.iterdir():
                child.unlink()
        else:
            tmp_dir.mkdir()

        try:
            (tmp_dir / "root.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                '"$id":"ghost-channel/schemas/root.json",'
                '"title":"Root","type":"object",'
                '"properties":{"child":{"$ref":"./missing.schema.json"}},'
                '"additionalProperties":false}',
                encoding="utf-8",
            )

            report = validate_schema_directory(tmp_dir)

            self.assertFalse(report["valid"])
            self.assertEqual(report["schema_count"], 1)
            self.assertTrue(
                any("missing.schema.json" in err for err in report["errors"])
            )
        finally:
            for child in tmp_dir.iterdir():
                child.unlink()
            tmp_dir.rmdir()

    def test_validate_schema_directory_detects_required_key_missing_from_properties(
        self,
    ) -> None:
        root = Path(__file__).resolve().parent
        tmp_dir = root / "_tmp_schema_required"
        if tmp_dir.exists():
            for child in tmp_dir.iterdir():
                child.unlink()
        else:
            tmp_dir.mkdir()

        try:
            (tmp_dir / "bad.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                '"$id":"ghost-channel/schemas/bad.json",'
                '"title":"Bad","type":"object",'
                '"required":["foo"],'
                '"properties":{"bar":{"type":"string"}},'
                '"additionalProperties":false}',
                encoding="utf-8",
            )

            report = validate_schema_directory(tmp_dir)

            self.assertFalse(report["valid"])
            self.assertTrue(
                any(
                    "required key 'foo' missing from properties" in err
                    for err in report["errors"]
                )
            )
        finally:
            for child in tmp_dir.iterdir():
                child.unlink()
            tmp_dir.rmdir()

    def test_validate_schema_directory_detects_empty_enum(self) -> None:
        root = Path(__file__).resolve().parent
        tmp_dir = root / "_tmp_schema_enum"
        if tmp_dir.exists():
            for child in tmp_dir.iterdir():
                child.unlink()
        else:
            tmp_dir.mkdir()

        try:
            (tmp_dir / "bad-enum.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                '"$id":"ghost-channel/schemas/bad-enum.json",'
                '"title":"BadEnum","type":"object",'
                '"properties":{"state":{"type":"string","enum":[]}},'
                '"additionalProperties":false}',
                encoding="utf-8",
            )

            report = validate_schema_directory(tmp_dir)

            self.assertFalse(report["valid"])
            self.assertTrue(any("empty enum" in err for err in report["errors"]))
        finally:
            for child in tmp_dir.iterdir():
                child.unlink()
            tmp_dir.rmdir()

    def test_validate_schema_directory_detects_orphan_schema(self) -> None:
        root = Path(__file__).resolve().parent
        tmp_dir = root / "_tmp_schema_orphan"
        if tmp_dir.exists():
            for child in tmp_dir.iterdir():
                child.unlink()
        else:
            tmp_dir.mkdir()

        try:
            (tmp_dir / "entry.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                '"$id":"ghost-channel/schemas/entry.json",'
                '"title":"Entry","type":"object",'
                '"properties":{"child":{"$ref":"./child.schema.json"}},'
                '"additionalProperties":false}',
                encoding="utf-8",
            )
            (tmp_dir / "child.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                '"$id":"ghost-channel/schemas/child.json",'
                '"title":"Child","type":"object",'
                '"properties":{},"additionalProperties":false}',
                encoding="utf-8",
            )
            (tmp_dir / "orphan.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                '"$id":"ghost-channel/schemas/orphan.json",'
                '"title":"Orphan","type":"object",'
                '"properties":{},"additionalProperties":false}',
                encoding="utf-8",
            )

            report = validate_schema_directory(tmp_dir)

            self.assertFalse(report["valid"])
            self.assertTrue(any("orphan schema" in err for err in report["errors"]))
        finally:
            for child in tmp_dir.iterdir():
                child.unlink()
            tmp_dir.rmdir()

    def test_validate_schema_directory_detects_ref_cycle(self) -> None:
        root = Path(__file__).resolve().parent
        tmp_dir = root / "_tmp_schema_cycle"
        if tmp_dir.exists():
            for child in tmp_dir.iterdir():
                child.unlink()
        else:
            tmp_dir.mkdir()

        try:
            (tmp_dir / "a.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                '"$id":"ghost-channel/schemas/a.json",'
                '"title":"A","type":"object",'
                '"properties":{"b":{"$ref":"./b.schema.json"}},'
                '"additionalProperties":false}',
                encoding="utf-8",
            )
            (tmp_dir / "b.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                '"$id":"ghost-channel/schemas/b.json",'
                '"title":"B","type":"object",'
                '"properties":{"a":{"$ref":"./a.schema.json"}},'
                '"additionalProperties":false}',
                encoding="utf-8",
            )

            report = validate_schema_directory(tmp_dir)

            self.assertFalse(report["valid"])
            self.assertTrue(any("reference cycle" in err for err in report["errors"]))
        finally:
            for child in tmp_dir.iterdir():
                child.unlink()
            tmp_dir.rmdir()

    def test_validate_example_file_accepts_valid_ack_example(self) -> None:
        root = Path(__file__).resolve().parents[2]
        schema_path = root / "schemas" / "ack-message.schema.json"

        tmp_example = Path(__file__).resolve().parent / "_tmp_valid_ack.json"
        try:
            tmp_example.write_text(
                "{"
                '"protocol_version":"1.1.0",'
                '"schema_version":"ghost-channel.ack/1.1",'
                '"stream_id":"stream_001",'
                '"sequence_number":1,'
                '"ack_type":"APPLIED",'
                '"status":"ok",'
                '"receiver_id":"role_b",'
                '"merkle_root_verified":true,'
                '"applied":true,'
                '"extensions":{},'
                '"error":null,'
                '"timestamp_ns":1712345678123456789'
                "}",
                encoding="utf-8",
            )
            report = validate_example_file(schema_path, tmp_example)
            self.assertTrue(report["valid"])
            self.assertEqual(report["errors"], [])
        finally:
            if tmp_example.exists():
                tmp_example.unlink()

    def test_validate_example_file_rejects_missing_required_field(self) -> None:
        root = Path(__file__).resolve().parents[2]
        schema_path = root / "schemas" / "ack-message.schema.json"

        tmp_example = Path(__file__).resolve().parent / "_tmp_invalid_ack.json"
        try:
            tmp_example.write_text(
                "{"
                '"protocol_version":"1.1.0",'
                '"schema_version":"ghost-channel.ack/1.1",'
                '"stream_id":"stream_001",'
                '"sequence_number":1,'
                '"ack_type":"APPLIED",'
                '"status":"ok",'
                '"receiver_id":"role_b",'
                '"applied":true,'
                '"error":null,'
                '"timestamp_ns":1712345678123456789'
                "}",
                encoding="utf-8",
            )
            report = validate_example_file(schema_path, tmp_example)
            self.assertFalse(report["valid"])
            self.assertTrue(
                any(
                    "missing required field 'merkle_root_verified'" in err
                    for err in report["errors"]
                )
            )
        finally:
            if tmp_example.exists():
                tmp_example.unlink()

    def test_validate_examples_directory_reports_current_examples(self) -> None:
        root = Path(__file__).resolve().parents[2]
        schemas_dir = root / "schemas"
        examples_dir = root / "examples"

        report = validate_examples_directory(schemas_dir, examples_dir)

        self.assertTrue(report["valid"])
        self.assertGreaterEqual(report["example_count"], 8)
        self.assertEqual(report["errors"], [])
        self.assertIn("ack-message.example.json", report["files"])

    def test_validate_examples_directory_detects_missing_schema_pair(self) -> None:
        root = Path(__file__).resolve().parent
        schemas_dir = root / "_tmp_example_schemas"
        examples_dir = root / "_tmp_example_examples"
        schemas_dir.mkdir(exist_ok=True)
        examples_dir.mkdir(exist_ok=True)

        try:
            (examples_dir / "unknown.example.json").write_text("{}", encoding="utf-8")

            report = validate_examples_directory(schemas_dir, examples_dir)

            self.assertFalse(report["valid"])
            self.assertTrue(
                any("missing matching schema" in err for err in report["errors"])
            )
        finally:
            for child in schemas_dir.iterdir():
                child.unlink()
            for child in examples_dir.iterdir():
                child.unlink()
            schemas_dir.rmdir()
            examples_dir.rmdir()

    def test_validate_example_schema_mapping_accepts_valid_manifest(self) -> None:
        root = Path(__file__).resolve().parents[2]
        manifest = root / "examples" / "example-schema-map.json"
        report = validate_example_schema_mapping(
            root / "schemas", root / "examples", manifest
        )
        self.assertTrue(report["valid"])
        self.assertGreaterEqual(report["mapping_count"], 5)
        self.assertEqual(report["errors"], [])

    def test_validate_example_schema_mapping_detects_missing_example(self) -> None:
        root = Path(__file__).resolve().parent
        schemas_dir = root / "_tmp_map_schemas"
        examples_dir = root / "_tmp_map_examples"
        schemas_dir.mkdir(exist_ok=True)
        examples_dir.mkdir(exist_ok=True)
        manifest = root / "_tmp_map_manifest.json"

        try:
            (schemas_dir / "foo.schema.json").write_text(
                '{"$schema":"https://json-schema.org/draft/2020-12/schema",'
                '"$id":"ghost-channel/schemas/foo.json",'
                '"title":"Foo","type":"object","properties":{},"additionalProperties":false}',
                encoding="utf-8",
            )
            manifest.write_text(
                '{"mappings":[{"example":"foo.example.json","schema":"foo.schema.json"}]}',
                encoding="utf-8",
            )

            report = validate_example_schema_mapping(
                schemas_dir, examples_dir, manifest
            )
            self.assertFalse(report["valid"])
            self.assertTrue(
                any("missing example file" in err for err in report["errors"])
            )
        finally:
            for child in schemas_dir.iterdir():
                child.unlink()
            for child in examples_dir.iterdir():
                child.unlink()
            schemas_dir.rmdir()
            examples_dir.rmdir()
            if manifest.exists():
                manifest.unlink()


if __name__ == "__main__":
    unittest.main()
