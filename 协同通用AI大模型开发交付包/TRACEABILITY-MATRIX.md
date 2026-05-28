# Traceability Matrix

> 用途：追踪项目级 GOAL/REQ/PRD/SPEC/TASK/TEST/AUD/MEM 的对齐关系。
> 生成时间：2026-05-28。
> 状态：母交付包级追踪矩阵，覆盖跨 session 核心需求。

## 1. 目标（GOAL）

| ID | 目标 | 状态 | 验证方式 |
|---|---|---|---|
| G-1 | 建立 AI 协同开发的标准化交付流程 | 已完成 | 四体系 + VERIFY-DELIVERY.ps1 -Strict |
| G-2 | 消除验证体系中的所有非预期 FAIL | 已完成 | qa_runner.py validate: 0 非预期 FAIL |
| G-3 | 将 QCM 公式模块从硬编码迁移为 config-driven | 已完成 | 12/14 模块迁移，测试全通过 |

## 2. 需求（REQ）

| ID | 需求 | 来源 | 映射 PRD | 映射 SPEC | 状态 |
|---|---|---|---|---|---|
| REQ-1 | Python venv 隔离环境 | V-1 | — | — | 已完成 |
| REQ-2 | SDK 测试路径正确 | V-2 | — | — | 已完成 |
| REQ-3 | 文件完整性验证无误报 | V-3 | — | — | 已完成 |
| REQ-4 | PowerShell 中文路径兼容 | V-4 | — | — | 已完成 |
| REQ-5 | QCM 参数可配置 | A-1 | — | — | 已完成 |
| REQ-6 | 源提示词吸收验证 | D | — | — | 已完成 |
| REQ-7 | 交付包四体系填充 | C | — | — | 已完成 |

## 3. 任务（TASK）

| ID | 任务 | 对应 REQ | 完成时间 | 产出 |
|---|---|---|---|---|
| T-1 | 创建 venv + 安装 6 依赖 | REQ-1 | 2026-05-28 | venv + packages |
| T-2 | 修复 qa_runner.py SDK 路径 | REQ-2 | 2026-05-28 | run_cmd_raw() |
| T-3 | 重新生成 MANIFEST.yaml | REQ-3 | 2026-05-28 | 299 文件 |
| T-4 | PowerShell UTF8 编码 | REQ-4 | 2026-05-28 | _auto_run_script 修改 |
| T-5 | 扩展 config.py paper_params | REQ-5 | 2026-05-28 | 14 模块参数 |
| T-6 | 迁移 12 模块常量 | REQ-5 | 2026-05-28 | 60 个替换 |
| T-7 | 源提示词吸收审查 | REQ-6 | 2026-05-28 | 26/26 验证 |
| T-8 | 四体系内容填充 | REQ-7 | 2026-05-28 | 4 文件 |
| T-9 | 5 个缺失文件创建 | REQ-7 | 2026-05-28 | 5 文件 |

## 4. 测试（TEST）

| ID | 测试 | 映射 TASK | 结果 |
|---|---|---|---|
| TEST-1 | qa_runner.py validate（全量） | T-1~T-5 | 12 PASS / 0 FAIL |
| TEST-2 | VAL-01-SDK-TESTS（开源 SDK） | T-2 | 18 passed |
| TEST-3 | VAL-01-GHOST-VERIFY（完整性） | T-3 | 299 files ALL CLEAN |
| TEST-4 | VAL-04-QCM-ALL | T-5, T-6 | 25/25 PASS |
| TEST-5 | VAL-04-QCM-PAPER | T-5, T-6 | 38/38 PASS |
| TEST-6 | VERIFY-DELIVERY.ps1 -Strict | T-8, T-9 | 待确认 |

## 5. 审计（AUD）

| ID | 审计 | 范围 | 结果 |
|---|---|---|---|
| AUD-1 | 源提示词吸收合规性 | 00/13 全目录 | 26/26 机制验证通过，11/11 reject 零泄漏 |
| AUD-2 | 跨文档一致性 | 00 validate_consistency.py | 9/10 PASS / 1 WARN（C5 路由覆盖度） |
| AUD-3 | Markdown fence 平衡 | 全量 511 md 文件 | 0 unbalanced |

## 6. 记忆（MEM）

| ID | 记录 | 优先级 | 存储位置 |
|---|---|---|---|
| MEM-1 | Python venv 策略和路径 | P0 | MEMORY.md §4.1 |
| MEM-2 | qa_runner.py 核心修复模式 | P0 | MEMORY.md §4.2 |
| MEM-3 | Submodule 操作规范 | P0 | MEMORY.md §4.3 |
| MEM-4 | MANIFEST 排除规则 | P1 | MEMORY.md §4.2 |
| MEM-5 | 循环依赖处理方案 | P1 | HANDOFF.md §4 |
