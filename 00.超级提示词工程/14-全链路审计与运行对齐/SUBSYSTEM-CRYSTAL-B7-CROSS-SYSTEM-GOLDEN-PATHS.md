# B7 Cross-System Golden Paths Knowledge Crystal

> Date: 2026-05-31  
> Scope: ROOT, 00, 03, 04, 05, QCM skill, USER_PACK  
> Purpose: turn the mother package from a large collection of subsystems into a reproducible AI collaboration control plane.

## 1. Core Understanding

The mother package is not intended to replace a general AI model. Its practical value is to give a future AI model a disciplined collaboration surface:

- Read mission and boundaries before acting.
- Route natural language into a concrete subsystem.
- Attach every route to ledger, validation refs, and stop lines.
- Use runnable subsystems only after current validation.
- Stop expanding when the current goal is verified and remaining gaps are registered.

B7 therefore does not ask, "can each folder run alone?" That was B2-B6. B7 asks, "can an AI enter through natural language, pick the right gear, execute real validation, and know when to stop?"

## 2. Golden Path State

| Scenario | Current state | Evidence |
|---|---|---|
| GS-01 awakening | VERIFIED | `qa_runner.py route "请读取母包并完成唤醒激活"` returns DIRECT 0.82 and an `awakening_check` block with model-native, mother-pack, and user-pack boundaries. |
| GS-02 secretary route | VERIFIED | `python qa_runner.py validate --scope ROOT` route smoke covers 8/8 core Chinese scenarios with route decisions, platforms, confidence, route feedback, and validation refs. |
| GS-03 P03 KB HTTP | VERIFIED | `python qa_runner.py validate --scope P03_WORKBUDDY_KB` now includes `VAL-03-HTTP-SMOKE`; install/tests/HTTP smoke are 3/3 PASS. |
| GS-04 QCM sandbox | VERIFIED | `python qa_runner.py validate --scope P04_QCM` is 5/5 PASS; `python qa_runner.py validate --scope QCM_SKILL` is 2/2 PASS. |
| GS-05 P05 runtime | VERIFIED | `python qa_runner.py validate --scope P05_QSPECTRUM` is 6/6 PASS, covering integration, status, pytest, E2E, API smoke, and MCP smoke. |
| GS-06 USER_PACK strict | VERIFIED | `python qa_runner.py validate --scope USER_PACK` is 2/2 PASS; strict mode returns 0 failures and 0 warnings. |
| GS-07 cross-system loop | VERIFIED-CONTROL | `qa_runner.py route "从想法到需求、规格、任务、测试、交付"` returns DIRECT 0.81, platform `cross_subsystem`, USO `AUD-20260531-B7-CROSS-SYSTEM-GOLDEN-PATHS`, and validation refs. `VAL-END-TO-END` and `VAL-CROSS-INTERFACE` are now automatic meta gates. A real new business project instance is still a future sample, not claimed here. |
| GS-08 stop rebuild | VERIFIED | The stop decision is: stop structural expansion; only fix failing validation, stale authority docs, or concrete execution blockers. Remaining productization ideas are tracked as gaps, not immediate rebuild work. |

## 3. B7 Fixes Landed

- Added explicit cross-system golden-path routing for idea -> requirement -> spec -> task -> test -> delivery.
- Added route `validation_refs` and deterministic USO IDs for core paths.
- Added `awakening_check` output for mission activation.
- Added `USER_PACK` platform detection.
- Added P03 HTTP validation as `VAL-03-HTTP-SMOKE`.
- Expanded route smoke from 4 loose scenarios to 8 golden-path scenarios with decision, platform, confidence, and validation-ref checks.
- Converted `VAL-END-TO-END` and `VAL-CROSS-INTERFACE` from manual-current summaries into automatic meta gates.
- Preserved cautious behavior for vague input: "请给出当前系统状态摘要" remains CLARIFY until the target system is named.

## 4. Remaining Gaps

| Gap | Meaning | Stop rule |
|---|---|---|
| Real sample project instance | GS-07 control-plane route is verified, but no new business project was generated end to end in this B7 pass. | Do not create a fake project just to claim S4. Use the next real user project as the sample. |
| Docker/optional external integrations | P01 Docker and optional external integrations depend on local tools not present in this run. | Keep as external gaps; do not block core mother-package acceptance. |

## 5. Practical Use

If I were using this repository as its owner, I would use it like this:

1. Start every new AI session with mission activation and ROOT validation.
2. Let `qa_runner.py route "<request>"` choose the subsystem and validation refs.
3. Read the matching subsystem crystal before editing.
4. Run only the validation scope that matches the route.
5. If validation is green, stop expanding and write the result to the ledger or user pack.
6. If validation fails, fix the smallest real blocker and rerun the same gate.

This is the convergence path: not less intelligence, but less uncontrolled multiplication.
