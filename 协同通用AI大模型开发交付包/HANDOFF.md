# Handoff Document

> 用途：项目交接文档，记录当前状态、未完成事项和后续建议。
> 生成时间：2026-05-31。
> 交接方：AI 辅助开发系统 → 开发者/接收方。

## 1. 当前状态

| 项 | 状态 |
|---|---|
| 验证结果 | 31 项注册验证：31 自动 PASS / 0 manual-current / 0 FAIL / 0 WARN / 0 SKIP |
| Git 状态 | 当前审计过程中存在本轮修复改动；交付前以 `git status` 和最终 commit/push 为准 |
| 四体系填充 | 已完成，并在 2026-05-31 按当前审计事实刷新 |
| 交付验证 | `VERIFY-DELIVERY.ps1` 与 `VERIFY-DELIVERY.ps1 -Strict` 当前均 0 failures / 0 warnings |

## 2. 本次 session 完成的工作

### P0: 交付门禁
- 创建 GitHub 根仓库 + 配置 remote
- Push 03 submodule (e1b8318) + 05 submodule (c6deb02)
- Push 根仓库全量（10 commits）

### P1: 验证消除（6→0 FAIL）
- Python venv 创建 + 6 依赖安装
- qa_runner.py: venv 路由、SDK PYTHONPATH、PowerShell UTF8、QCM 路径修复
- MANIFEST.yaml 重新生成（299 文件，排除 cache）
- 05/_HANDOFF/ 三文件创建（STATUS/CRITICAL-REMINDERS/MEMORY-INDEX）

### P2: QCM Phase 2 config-driven
- config.py: 新增 paper_params 段（14 模块所有参数）
- 12/14 模块完成常量迁移（60 个常量）
- calculator/detector 因循环依赖保留原始值但标注 config source
- 测试全通过（25/25 + 38/38）

### D: 源提示词吸收验证
- 26 个原子机制全部验证（96.2% 全量实现）
- keep 实现率 100%，reject 11/11 零泄漏

### C: 协同交付包填充
- 四体系从模板态升级为实际内容
- 5 个缺失文件创建（AI_PROJECT_CONTEXT/HANDOFF/CHANGELOG/TRACEABILITY/VALIDATION_REPORT）

### B2-B6: 2026-05-31 深度审计与运行对齐
- 01 Ghost Channel：完整性 299 checked / 295 verified / 4 optional skips，SDK 总计 184 passed。
- 03 knowledge-base-manager：verify_install 23 pass / 0 fail；pytest 107 passed。
- 04 QCM + qcm-universal-ai-system-v3.0.skill：QCM 5/5 scope PASS，Skill validate 0 issues，Skill tests 173 passed。
- 05 Q-SpecTrum：pytest 158 passed，E2E 13/13，API/MCP smoke 通过，快速连续对话锁库问题已修复。
- 02 Universal-KB + 协同交付包：模板 smoke 与普通/Strict 交付门禁通过，文档已对齐当前事实。

## 3. 未完成事项

| 优先级 | 事项 | 说明 |
|---|---|---|
| P2 | AKU 知识原子进入项目知识库的正式落地流程 | 规范已有源提示词/审计锚点，后续需把它变成可执行 ingest/lint 流程 |
| P2 | TRACEABILITY-MATRIX.md 项目级持续更新 | 已有母包级实例；后续每个新项目应继续追加自己的 GOAL/REQ/SPEC/TASK/TEST |
| P3 | 02 通用知识库升级 | 目前明确为模板态；可运行实现仍以 03 子系统为准 |
| P3 | calculator.py/detector.py config 化 | 需要重构 qcm/core/__init__.py 解决循环依赖后才能迁移 |
| P3 | CI/CD pipeline | GitHub Actions 自动化验证 |

## 4. 关键技术决策

1. **venv 路径**: `~/.workbuddy/binaries/python/envs/default/`（managed 隔离）
2. **Git push**: 需要 `GIT_TERMINAL_PROMPT=0`（避免 credential manager GUI 挂起）
3. **循环依赖**: qcm.core → calculator → qcm.config，通过保留原始值 + 注释标注解决
4. **MANIFEST 排除**: `.pytest_cache/`、`__pycache__/`、`.git/`（避免 hash 漂移）
5. **PowerShell 编码**: `_auto_run_script` 使用 `[Console]::OutputEncoding = UTF8`

## 5. 风险提示

- calculator.py/detector.py 的类常量是硬编码的，修改 config.py 的 paper_params 不会自动生效（需先解决循环依赖）。
- 03 知识库的 `.env` 未配置时，高级 AI 功能（API 调用）不可用，但不影响基础运行。
- 05 已统一为 Python 3.10+ + `requirements.txt` 交接口径；运行验证以 `pytest tests -q`、`python run.py --e2e`、API/MCP smoke 为准。
