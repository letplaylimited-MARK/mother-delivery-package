# Minimal AI Collaboration Taskboard

> Purpose: a tiny, deterministic reference project that proves the mother package can turn an AI collaboration idea into PRD, SPEC, TASK, TEST, validation evidence, and a runnable artifact.

This project is intentionally outside `协同通用AI大模型开发交付包/`. The delivery package stays a reusable template; this directory is a concrete project instance built from the mother-package method.

## What It Does

The taskboard validates AI collaboration task cards. Each card must declare an owner, route, status, validation references, and stop-line state. The smoke test proves that a future AI/developer can run a real project check without API keys or external services.

## Run

```powershell
powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1
```

Or directly:

```bash
python tests/test_smoke.py
```

Expected marker:

```text
REFERENCE_PROJECT_SMOKE=PASS
```

## Mother-Package Trace

```text
User idea
-> PRD
-> SPEC
-> TASKS
-> tests/test_smoke.py
-> VALIDATION_REPORT
-> mother qa_runner.py VAL-REFERENCE-PROJECT-SMOKE
```
