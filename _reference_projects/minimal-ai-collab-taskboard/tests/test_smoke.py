from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ai_collab_taskboard import load_taskboard, summarize, validate_taskboard


def main() -> int:
    sample = PROJECT_ROOT / "examples" / "sample_taskboard.json"
    tasks = load_taskboard(sample)
    issues = validate_taskboard(tasks)
    summary = summarize(tasks)

    if issues:
        print("REFERENCE_PROJECT_SMOKE=FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    if summary["total"] != 2 or summary["by_status"].get("done") != 2:
        print("REFERENCE_PROJECT_SMOKE=FAIL")
        print(f"Unexpected summary: {summary}")
        return 1

    print("REFERENCE_PROJECT_SMOKE=PASS")
    print(f"tasks={summary['total']} done={summary['by_status'].get('done')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
