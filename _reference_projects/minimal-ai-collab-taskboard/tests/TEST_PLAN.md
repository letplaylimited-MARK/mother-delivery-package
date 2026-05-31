# Test Plan

## Smoke

Command:

```bash
python tests/test_smoke.py
```

Expected:

```text
REFERENCE_PROJECT_SMOKE=PASS
```

## Coverage

- Loads sample JSON.
- Validates required fields.
- Validates `TASK-` prefix.
- Validates non-empty `validation_refs`.
- Produces a status summary.
