# Validation Report

> 用途：项目验证报告，记录所有验证命令的执行结果。
> 生成时间：2026-05-31。
> 执行环境：Windows, Python 3.14.4, Git submodule managed。

## 总览

| 指标 | 数值 |
|---|---|
| 验证项总数 | 31 |
| 自动验证 PASS | 31 |
| FAIL | 0 |
| WARN | 0 |
| SKIP | 0 |
| MANUAL/CURRENT | 0 |
| 未预期 FAIL | 0 |

## 详细结果

### 自动 PASS（31 项）

| ID | 名称 | 关键指标 |
|---|---|---|
| VAL-ROOT-FILE-COUNT | 根目录文件计数 | 1150 文件；submodule/runtime 差异正常 |
| VAL-ROOT-HARDCODE-PATH | 硬编码路径检查 | 无本机绝对路径泄漏 |
| VAL-ROOT-MARKDOWN-FENCES | Markdown 围栏检查 | 541 文件全通过 |
| VAL-ROOT-YAML-PARSE | YAML 解析检查 | 8 文件全通过 |
| VAL-ROOT-ROUTE-SMOKE | Guide Secretary 路由 | 8/8 黄金路径场景通过，覆盖 route_decision / platform / confidence / validation_refs |
| VAL-00-MEMORY-SOURCE-INDEX | 记忆源索引 | 13 条目字段合规 |
| VAL-00-AUDIT-ASSETS | 深度审计资产 | inventory 1150；graph 131 nodes / 247 edges |
| VAL-01-GHOST-VERIFY | Ghost Channel 完整性 | 299 checked；295 verified；4 optional binaries skipped |
| VAL-01-SDK-TESTS | SDK 单元测试 | 184 passed（Python 三组 SDK + TypeScript） |
| VAL-02-TEMPLATE-REVIEW | Universal-KB 模板 smoke | py_compile + smoke OK |
| VAL-03-INSTALL | 知识库安装验证 | verify_install 23 通过，0 失败 |
| VAL-03-TESTS | 知识库测试套件 | 107 passed |
| VAL-03-HTTP-SMOKE | 知识库 HTTP smoke | `/memory` 与 `/api/search?q=知识库` 通过，search 返回 10 条 |
| VAL-04-QCM-ALL | QCM 全量测试 | 25/25 PASS |
| VAL-04-QCM-PAPER | QCM 论文测试 | 38/38 PASS |
| VAL-04-HEALTH | QCM 健康检查 | 6/6 READY |
| VAL-04-QCM-RUNTIME-SMOKE | QCM 运行烟测 | research / production / service 均通过 |
| VAL-QCM-CONFIG-SYNC | QCM 配置同步 | detector thresholds 与 weights 配置同步测试通过 |
| VAL-QCM-SKILL-VALIDATE | QCM Skill 包验证 | 0 issues，FINAL RESULT PASS |
| VAL-QCM-SKILL-TESTS | QCM Skill 测试 | 173 passed |
| VAL-05-INTEGRATION | Q-SpecTrum 结构集成 | PASS；仅 runtime `_HANDOFF/` 提示 |
| VAL-05-STATUS | Q-SpecTrum 健康报告 | System: ALL GREEN |
| VAL-05-PYTEST | Q-SpecTrum pytest | 158 passed |
| VAL-05-E2E | Q-SpecTrum E2E | 13 passed / 0 failed |
| VAL-05-API-SMOKE | Q-SpecTrum API 烟测 | status/roles/chat routing PASS |
| VAL-05-MCP-SMOKE | Q-SpecTrum MCP 烟测 | 18 tools，JSON-RPC stdout clean |
| VAL-USER-PACK-DELIVERY | 交付包基础验证 | 0 failures / 0 warnings |
| VAL-USER-PACK-DELIVERY-STRICT | 交付包严格验证 | 0 failures / 0 warnings |
| VAL-00-CROSS-DOC-CONSISTENCY | 跨文档一致性 | 10/10 PASS |
| VAL-END-TO-END | 端到端链路元验证 | audit assets / scenario matrix / route smoke / consistency / USER_PACK strict 全通过 |
| VAL-CROSS-INTERFACE | 跨子系统接口元验证 | route smoke / P03 HTTP / QCM config / P05 API+MCP / USER_PACK strict 全通过 |

### MANUAL/CURRENT（0 项）

| ID | 名称 | 说明 |
|---|---|---|
| 无 | 无 | B7 后 `VAL-END-TO-END` 与 `VAL-CROSS-INTERFACE` 已升级为自动元验证 |

## 修复历史

| 时间 | 修复项 | 之前状态 | 之后状态 |
|---|---|---|---|
| 2026-05-28 | venv + 6 依赖安装 | VAL-03/04/05 FAIL | PASS |
| 2026-05-28 | SDK PYTHONPATH + cryptography | VAL-01-SDK-TESTS FAIL (0 tests) | PASS (18 passed) |
| 2026-05-28 | MANIFEST 重新生成（排除 cache） | VAL-01-GHOST-VERIFY FAIL | PASS (299 CLEAN) |
| 2026-05-28 | PowerShell UTF8 编码 | VAL-01-GHOST-VERIFY 乱码 | 正常输出 |
| 2026-05-28 | QCM 路径 + PYTHONPATH | VAL-04-QCM-ALL FAIL | PASS (25/25) |
| 2026-05-28 | _HANDOFF 目录创建 | VAL-05-INTEGRATION FAIL | PASS |
| 2026-05-28 | 四体系填充 + 5 文件创建 | VAL-USER-PACK-DELIVERY-STRICT FAIL | PASS |
| 2026-05-31 | SDK 验证器失败准则修复 | SDK 子套件失败可被误报为通过 | 162 Python tests 才通过 |
| 2026-05-31 | TypeScript SDK 与部署入口修复 | `npm test` 无法加载 `.ts`；一键部署 compose 存在旧导入/错误 context | 22 TS tests 纳入 VAL-01-SDK-TESTS；P01 SDK 总数 184 passed |
| 2026-05-31 | P05 fresh-clone handoff 判定修复 | git-ignored `_HANDOFF` 被当作必需文件 | Route A 必需文件通过；runtime handoff 作为提示 |
| 2026-05-31 | Windows CLI 输出硬化 | `route` 与 `run.py --status` 可被 GBK/emoji 打断 | 直接命令运行通过 |
| 2026-05-31 | 深度审计资产落地 | 无原子文件清单/图谱/场景矩阵验证门 | VAL-00-AUDIT-ASSETS PASS |
| 2026-05-31 | P03/P05/B6 当前事实刷新 | 交付包文档仍引用旧测试数、旧 PASS 快照和 2026-05-28 状态 | 文档对齐到当前 P03/P05/验证注册证据与 B6 严格门禁 |
| 2026-05-31 | B7 验证元门与交付包口径刷新 | 交付包仍引用 30 项、28 自动 PASS、2 manual-current 与 1148 inventory | 文档对齐到 31/31 automatic PASS、1150 inventory、ROOT route smoke 8/8 与 0 manual-current |

## 下一步

- 保持 `python qa_runner.py validate`、`python qa_runner.py consistency`、`VERIFY-DELIVERY.ps1 -Strict` 为停止重构前的三道门。
- 后续只针对失败验证项或真实场景缺口修复，避免无边界扩写。
