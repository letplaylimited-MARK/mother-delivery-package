# SPEC

## Data Model

Each task card is a JSON object:

```json
{
  "id": "TASK-001",
  "title": "Create route feedback",
  "owner": "AI+developer",
  "route": "ROOT -> 00",
  "status": "done",
  "validation_refs": ["VAL-ROOT-ROUTE-SMOKE"],
  "stop_line": "No edits without validation anchor"
}
```

## Validation Rules

- Required fields: `id`, `title`, `owner`, `route`, `status`, `validation_refs`, `stop_line`.
- `id` must start with `TASK-`.
- `status` must be one of `todo`, `doing`, `done`, `blocked`.
- `validation_refs` must be a non-empty list.
- `stop_line` must be non-empty.

## Interfaces

- `load_taskboard(path)` reads JSON.
- `validate_task(task)` returns issue strings.
- `validate_taskboard(tasks)` returns all issues.
- `summarize(tasks)` returns count and status summary.
