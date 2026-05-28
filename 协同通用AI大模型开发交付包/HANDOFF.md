# Handoff Document

> 用途：项目交接文档，记录当前状态、未完成事项和后续建议。
> 生成时间：2026-05-28。
> 交接方：AI 辅助开发系统 → 开发者/接收方。

## 1. 当前状态

| 项 | 状态 |
|---|---|
| 验证结果 | 12 PASS / 0 FAIL / 1 WARN / 4 MANUAL |
| Git 状态 | 10 commits，working tree clean，remote 已同步 |
| 四体系填充 | 已完成（价值/功能/结构/运作） |
| 交付验证 | `VERIFY-DELIVERY.ps1 -Strict` 待最终确认 |

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

## 3. 未完成事项

| 优先级 | 事项 | 说明 |
|---|---|---|
| P2 | AKU-KNOWLEDGE-ATOM-SPEC.md | 知识原子进入知识库的正式规范文档 |
| P2 | TRACEABILITY-MATRIX.md 实例 | 当前仅有模板，需填充真实项目 GOAL/REQ/SPEC/TASK |
| P3 | 02 通用知识库升级 | 从模板态升级为可运行应用 |
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
- 05 的 `requirements.txt` 与 `pyproject.toml` 对依赖描述不一致（不影响运行，但文档需统一）。
