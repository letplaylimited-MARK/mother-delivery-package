# Sandbox Run 20260531 - B7 Cross-System Golden Paths

> Mode: six-round sandbox/flywheel  
> Role team: Codex executor, route auditor, validation engineer, delivery reviewer, stop-line reviewer  
> Write scope: B7 validation, route gates, P03 HTTP smoke, control-plane records

## Round 1 - Matrix Read

Input:

- `SCENARIO-ACCEPTANCE-MATRIX.md`
- `MOTHER-CHILD-WORKFLOW-MAP.md`
- `VALIDATION_REGISTRY.yaml`
- `qa_runner.py`

Finding:

- B2-B6 proved the main subsystems individually.
- B7 still needed scenario-level evidence, especially P03 HTTP, awakening output, cross-system route, and stop-rebuild decision.

## Round 2 - Route Sampling

Commands:

- `python qa_runner.py route "请读取母包并完成唤醒激活"`
- `python qa_runner.py route "帮我测试05 Q-SpecTrum API和角色路由"`
- `python qa_runner.py route "我要运行03知识库搜索和MCP工具"`
- `python qa_runner.py route "请给出05 Q-SpecTrum当前系统状态摘要"`
- `python qa_runner.py route "从想法到需求、规格、任务、测试、交付"`
- `python qa_runner.py route "为什么这个项目一直重构，怎么收敛？"`

Result:

- Explicit P03/P05/USER_PACK/cross-system requests route with confidence >= 0.80.
- Vague "当前系统状态摘要" remains CLARIFY, which is intentional.
- Review/anti-rebuild request routes to REVIEW_AUDIT with CONFIRM, preserving human confirmation for governance judgment.

## Round 3 - P03 HTTP Reality Check

Commands:

- `python qa_runner.py validate --scope P03_WORKBUDDY_KB`
- Direct isolated `VAL-03-HTTP-SMOKE` call for detailed evidence

Result:

- P03 scope: 3/3 PASS.
- HTTP smoke: `/memory` returned keys `config,long_term_knowledge,long_term_strategies,mid_term_count,short_term_count,user_profile`.
- `/api/search?q=知识库` returned 10 results; first path `05-知识沉淀\README.md`.
- First implementation used a 5s search timeout and failed under cold-start search; timeout was raised to 30s and the gate passed.

## Round 4 - Runtime Gates

Commands:

- `python qa_runner.py validate --scope P04_QCM`
- `python qa_runner.py validate --scope QCM_SKILL`
- `python qa_runner.py validate --scope P05_QSPECTRUM`
- `python qa_runner.py validate --scope USER_PACK`

Result:

- P04_QCM: 5/5 PASS.
- QCM_SKILL: 2/2 PASS.
- P05_QSPECTRUM: 6/6 PASS.
- USER_PACK: 2/2 PASS.

## Round 5 - Repair

Repairs:

- Added `CROSS_SYSTEM_GOLDEN_PATH` route.
- Added `USER_PACK` platform detection.
- Added route `validation_refs`.
- Added deterministic USO IDs for core routes.
- Added mission `awakening_check`.
- Added `VAL-03-HTTP-SMOKE`.
- Expanded ROOT route smoke to 8 scenarios with decision, platform, confidence, and validation-ref assertions.

Verification:

- `python qa_runner.py validate --scope ROOT`: ALL CLEAR, route smoke 8/8 PASS.
- `python qa_runner.py validate --scope P03_WORKBUDDY_KB`: ALL CLEAR, 3/3 PASS.

## Round 6 - Stop-Rebuild Decision

Decision:

- Stop structural expansion for this pass.
- Do not create more subsystems, role layers, or prompt layers.
- Only accept further edits when tied to a failing validation, a stale authority document, or a concrete project handoff requirement.

Residual gap:

- A real new business project should later be used as the GS-07 full S4 sample. This B7 pass verifies the control plane and current subsystem gates; it does not fabricate a project instance.

## Post-Run Convergence - Meta Gates

Additional repair:

- `VAL-END-TO-END` is now an automatic meta gate for audit assets, B7 scenario matrix, route smoke, consistency, and USER_PACK strict.
- `VAL-CROSS-INTERFACE` is now an automatic meta gate for route smoke, P03 HTTP, QCM config sync, P05 API, P05 MCP, and USER_PACK strict.

Verification:

- `python qa_runner.py validate --scope ROOT`: 7/7 PASS, automatic 7/7, ALL CLEAR.
- `python qa_runner.py validate`: 31/31 PASS, automatic 31/31, 0 FAIL/WARN/SKIP, ALL CLEAR.

Effect:

- The earlier manual-current validation gray area is closed without adding new subsystems or expanding the conceptual surface.

## Delivery Readiness Check

Worktree state:

- Root worktree remains intentionally dirty with current audit, validation, subsystem-fix, and delivery-template changes. No files were staged or committed.
- Child workspace `03.数据库管理_文件夹整理AI应用` remains dirty with P03 runtime/test/doc fixes and two new tests.
- Child workspace `05.超极智脑_Q-SpecTrum` remains dirty with P05 runtime/API/MCP/E2E/doc fixes.
- P02 untracked directories contain only intended `.gitkeep` files preserving advertised template folders.

Runtime side effects:

- No current P03/P04/P05 validation server process was left running.
- Existing Python processes are external `mempalace-mcp.exe` processes from 2026-05-29, with no TCP listening sockets observed; they were not touched.

Current acceptance boundary:

- Full `python qa_runner.py validate`: 31/31 PASS, automatic 31/31, 0 FAIL/WARN/SKIP.
- ROOT `python qa_runner.py validate --scope ROOT`: 7/7 PASS, automatic 7/7.
- P00 `python qa_runner.py validate --scope P00_SUPER_PROMPT`: 3/3 PASS.
- `python qa_runner.py consistency`: 10/10 PASS.

Preserve:

- `qa_runner.py` B7 route/meta-validation changes.
- All subsystem crystals, sandbox records, scenario matrix, validation registry, ledger, audit coverage, and generated inventory/knowledge graph assets.
- P01/P02/P03/P04/P05/USER_PACK fixes already covered by validation evidence.

Do not claim:

- Do not claim every one of the 1150 files has been line-by-line semantically audited.
- Do not claim GS-07 has a real new business project instance yet.
- Do not claim Docker or optional external integrations were validated when the external tool was not present.
