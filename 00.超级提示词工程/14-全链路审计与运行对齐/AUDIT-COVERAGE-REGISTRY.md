# Audit Coverage Registry

> 中文名：审计覆盖登记表。  
> 用途：记录当前这轮审计真正覆盖了什么、证据来自哪里、哪些仍然只是推断或缺口。  
> 时间：2026-05-31。  
> 口径：排除 `.git`、`node_modules`、`dist/build/coverage`、`__pycache__`、`.pytest_cache`。

## 1. 覆盖声明

本轮是“全链路审计基线”，不是最终 100% 逐字逐行语义深读完成。

已完成：

- 顶层目录识别。
- 文件数量和类型盘点。
- 关键入口文档读取。
- 关键运行入口扫描。
- 扩展本机路径/旧项目路径泄漏扫描。
- 数据库/jsonl/yaml/json 等数据载体盘点。
- 子系统 README / INDEX / AGENTS / HANDOFF / PROTOCOL 标题级审计。
- 控制平面与母包/子包边界审计。
- 新增全链路审计协议、齿轮咬合图、审计问题日志、统一状态对象规范、统一状态账本、四个初始注册表和记忆源优先级。
- B2/P01、B3/P03、B4/P04+QCM Skill、B5/P05 Q-SpecTrum Runtime、B6/P02+USER_PACK、B7/CROSS Golden Paths 已进入“知识结晶 + 沙盘记录 + 当前验证”状态。

未完成：

- 1150 个当前基线文件逐文件语义审计。
- 所有 Python 模块的调用图/LSP 级分析。
- 所有 SQLite 表结构和数据质量审计。
- 所有 README 中历史验证声明的重新运行复核。
- 所有 PDF/HTML/历史报告内容的逐字审计。
- 四注册表的字段级充实、验证和后续自动化。

## 2. 文件数量基线

| 区域 | 文件数 | 审计状态 | 说明 |
|---|---:|---|---|
| `00.超级提示词工程` | 74 | PARTIAL-DEEP | 控制平面和 14-全链路审计资产持续扩展；B1-B7 结晶已落盘 |
| `01.通讯协议_幽灵通道` | 296 | VERIFIED-SUBSYSTEM | README/INDEX/HANDOFF/VERIFY/SDK入口已扫描，SDK/VERIFY 当前通过 |
| `02.通用知识库框架_Universal-KB` | 28 | VERIFIED-SUBSYSTEM | README/INDEX/docs/AGENTS/MemoryOS 已扫描；空目录保留、tempdir smoke 和模板边界已修 |
| `03.数据库管理_文件夹整理AI应用` | 153 | VERIFIED-SUBSYSTEM | README/AGENTS/app/mcp/verify/scripts/tests 已深读并修复关键运行断点 |
| `04.QCM-MVP-Emergence` | 148 | VERIFIED-SUBSYSTEM | README/HANDOFF/VERIFY/核心代码/qcm CLI/service/skill archive 已深读并验证 |
| `05.超极智脑_Q-SpecTrum` | 423 | VERIFIED-SUBSYSTEM | README/INDEX/AGENTS/Brain Protocol/run/API/MCP/engine/BRAIN-KB 已深读；pytest/E2E/API/MCP/status 当前通过 |
| 根入口文件 | 13 | PARTIAL-DEEP | `MISSION-MEMORY`, `AI_PROJECT_CONTEXT`, `qa_runner.py`, `qcm-universal-ai-system-v3.0.skill` 等已纳入审计 |
| `qcm-universal-ai-system-v3.0.skill` | 1 | VERIFIED-SUBSYSTEM | archive 作为根能力包登记；内部 43 文件已在 B4 解包验证 |
| `协同通用AI大模型开发交付包` | 14 | TEMPLATE-VERIFIED | 四体系模板、组装规则和 `VERIFY-DELIVERY.ps1` 已扫描；模板模式与 Strict 验证通过 |
| 合计 | 1150 | BASELINED | 当前 `ATOMIC-FILE-INVENTORY.jsonl` 口径；`.pytest_cache` 等运行缓存不计入基线 |

注：`rg --files` 默认受隐藏文件和忽略规则影响，读数会低于 PowerShell `Get-ChildItem -Force` 口径；本登记表采用 PowerShell 强制遍历并排除运行缓存的口径。

## 3. 文件类型基线

当前类型盘点显示主体为：

| 类型 | 数量 | 意义 |
|---|---:|---|
| `.md` | 537 | 协议、说明、交接、审计、知识库主体 |
| `.py` | 320 | 可运行应用、MCP、SDK、测试、脚本 |
| `.json` | 72 | 模板、配置、状态、数据对象 |
| 无扩展名 | 38 | 可能包含配置、脚本、包元数据或 `.gitkeep` 模板占位 |
| `.yaml` | 35 | 配置、工作流、角色、部署、审计注册表、统一状态账本、记忆源索引 |
| `.html` | 30 | Web UI 或导出文档 |
| `.sql` | 16 | 数据库结构或初始化脚本 |
| `.yml` | 15 | CI、配置、部署 |
| `.db` | 13 | SQLite 数据载体 |
| `.pdf` | 10 | 报告或交付材料，需单独 OCR/阅读策略 |
| `.jsonl` | 3 | 日志/记忆流 |

## 4. 已确认运行入口

| 子系统 | 命令/入口 | 状态 |
|---|---|---|
| `01` | `powershell -ExecutionPolicy Bypass -File .\VERIFY.ps1` | 当前重跑 299/299 verified，0 failed，0 missing |
| `01` | `python -m pytest "03_SDK与集成\02_开源社区包\ghost_channel开源库\tests" -q` | 当前重跑 18 passed |
| `01` | `python -m pytest "03_SDK与集成\04_SDK工程包\ghost-channel-sdk\python\tests" -q` | 当前重跑 68 passed |
| `01` | `python -m pytest "03_SDK与集成\03_企业SDK包\GhostHub_SDK\tests" -q` | 当前重跑 76 passed |
| `02` | `python -m py_compile "04-memory\memoryos.py"` | 当前重跑通过 |
| `02` | `python "04-memory\memoryos.py"` | 当前重跑通过，输出 MemoryOS smoke test |
| `03` | `python verify_install.py` | 当前重跑 23 pass / 0 fail / 1 warning；MCP 依赖已检查；`.env` 缺失为可选高级能力警告 |
| `03` | `python app.py --port <free> --no-bootstrap --daemon` | B7 当前启动 Flask；`/memory` 和 `/api/search?q=知识库` HTTP smoke 通过，搜索 10 条 |
| `03` | `python mcp_server.py` | MCP 入口存在；本轮未启动 |
| `03` | `python -m pytest tests -q` | 当前重跑 107 passed，3 warnings；已修复 MCP stdio UTF-8/调试输出污染、Web browse 目录逃逸、batch_import Path/统计问题，并隔离 vector_search 测试索引 |
| `03` | `python qa_runner.py validate --scope P03_WORKBUDDY_KB` | 当前重跑 3/3 PASS；含 install、107 tests、HTTP `/memory` + `/api/search` smoke |
| `04` | `python "02-代码编写\test_qcm_all.py"` | 当前重跑 25 PASS / 0 FAIL |
| `04` | `pytest "02-代码编写\test_roles.py" "02-代码编写\test_collaboration.py" "02-代码编写\test_sandbox.py" "02-代码编写\test_flywheel.py" "02-代码编写\test_summoning.py" -q` | 当前重跑 38 passed；不带 `02-代码编写` 的旧 shorthand 会失败 |
| `04` | `python "02-代码编写\test_config_sync.py"` | 当前重跑 4 passed；calculator/detector 常数与 qcm/config.py 同步 |
| `04` | `python health_check.py` | 当前重跑 6/6 READY |
| `04` | `python qa_runner.py validate --scope P04_QCM` | 当前重跑 5/5 PASS；含 runtime smoke |
| QCM Skill | `python qa_runner.py validate --scope QCM_SKILL` | 当前重跑 2/2 PASS；validator 0 issues，pytest 173 passed |
| `05` | `python verify-integration.py` | 当前重跑 PASS；1 个 runtime `_HANDOFF/` warning |
| `05` | `python run.py --status` | 当前重跑 ALL GREEN；run.py 已做 UTF-8 输出硬化 |
| `05` | `python run.py --query "Research our competitors"` | 当前重跑通过，路由到 ROLE-Q02 QCM Researcher |
| `05` | `pytest tests -q` | 当前重跑 158 passed；无线程解码警告 |
| `05` | `python run.py --e2e` | 当前重跑 13 passed / 0 failed；外部 ChromaDB Python 3.14 deprecation warning 保留为依赖侧提示 |
| `05` | `python qa_runner.py validate --scope P05_QSPECTRUM` | 当前重跑 6/6 PASS；含 integration/status/pytest/e2e/API/MCP |
| `05` | API smoke (`run.py --web --provider mock` on free port) | 当前启动并调用 `/api/status`, `/api/roles`, `/api/chat`；Q02/Q06/Q08 路由通过 |
| `05` | MCP stdio smoke (`qspectrum_mcp_server.py --provider mock`) | 当前 JSON-RPC initialize/tools/resources/execute_chat/query_database 通过；stdout 无非 JSON 污染 |
| `05` | `python verify-delivery.py --quick` | 当前静态交付检查 6/6 passed；Windows UTF-8 输出已修 |
| 用户交付包 | `powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1` | 当前运行通过，0 failures，0 warnings |
| 用户交付包 | `powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1 -Strict` | 当前运行通过，0 failures，0 warnings；严格模式是结构/交接门，正式项目仍需真实 smoke/test |
| ROOT | `python qa_runner.py validate --scope ROOT` | 当前重跑 7/7 PASS，自动 7/7；含 end-to-end 与 cross-interface 自动元验证 |
| ROOT | `python qa_runner.py validate` | 当前全量重跑 31/31 PASS，0 FAIL/WARN/SKIP，自动 31/31 |

## 5. 数据载体基线

已扫描到以下类型：

- `03/.workbuddy/index/search_index.db`
- `03/.workbuddy/记忆层/memory_data/short_term/*.jsonl`
- `03/.workbuddy/config/*.json`
- `03/.workbuddy/AI协作体系/模型配置/*.yaml`
- `05/AI项目管理/Platform/db/platform.db`
- `05/project_memory.db`
- `05/knowledge_graph.db`
- `05/knowledge_pipeline.db`
- `05/task_manager.db`
- `05/BRAIN-KB/.chroma_db/chroma.sqlite3`
- `05/_HANDOFF/reports/*.json`
- `05/.ghost_channel_state.json`
- `05/routing_keywords.json`
- `02/04-memory/config.yaml`

审计判断：

- 真实记忆与数据载体存在。
- 最大风险是多记忆源之间没有统一优先级、冲突解决和写入登记表。

## 6. 第一轮风险清单

| ID | 风险 | 等级 | 证据 | 建议 |
|---|---|---|---|---|
| R-001 | 机器可读注册表已有初始版，但字段仍需深读后持续填充 | High | `PROJECT/CAPABILITY/ARTIFACT/VALIDATION_REGISTRY.yaml` 已建立 | 下一轮补字段证据、自动校验和引用关系 |
| R-002 | `03` 与 `05` 都有记忆/知识库，读写优先级已从人读文档升级为机器索引初版，但尚未实测 | High | `MEMORY-SOURCE-PRIORITY.md` + `MEMORY-SOURCE-INDEX.yaml` 已建立 | 用真实任务测试冲突解决规则 |
| R-003 | 沙盘结果可能被误当验证结果 | Medium | `00/08`、`04` 都有沙盘概念 | 所有沙盘输出必须绑定 TEST/AUD |
| R-004 | 子包仍是骨架，Strict 不等价于真实业务运行验证 | Medium | `VERIFY-DELIVERY.ps1` 与 `-Strict` 当前 0 failures / 0 warnings；`scripts/verify.ps1` 是结构门包装器 | 具体项目交付时必须扩展/替换真实 smoke/test |
| R-005 | `05` 依赖描述曾有漂移 | Low | `requirements.txt`、`pyproject.toml`、README、QUICK-START、INSTALL-GUIDE 已对齐为 Python 3.10+ 与 requirements.txt | 后续新增依赖时同步入口文档与启动脚本 |
| R-006 | `01/02/04` 的验证语义不统一 | Medium | 子智能体审计发现 `01 VERIFY.ps1` 是完整性校验、`02` 是模板审查、`04 health_check.py` 语义需复核 | 用 `VALIDATION_REGISTRY.yaml` 区分 integrity/test/template/health/delivery gates |
| R-007 | 两个子 git 仓库已有未归属修改 | Medium | `03` 和 `05` `git status --short` 有修改 | 不覆盖；后续单独确认来源 |
| R-008 | 历史文档状态仍可能残留漂移；关键入口已收敛 | Medium | `01/02/04/05` 已有 crystal/sandbox 和当前验证；历史报告按需降权 | B7 只围绕真实 golden path 暴露的问题继续修复 |
| R-009 | MCP stdio 曾被中文调试输出/编码污染 | Low | 已在 `mcp_server.py` 固定 UTF-8 streams，并将工具调用期间 stdout 重定向到 stderr；当前 `python -m pytest tests -q` 为 107 passed | 保持 MCP stdio stdout 只输出 JSON-RPC；新增测试覆盖会继续守住 |
| R-010 | 历史报告/迁移计划残留旧本机路径表述 | Medium | 扩展 `rg` 发现 `03` 历史报告和迁移计划存在旧路径；本轮已将可执行示例改成占位路径 | 后续把扫描纳入固定验证，区分“运行文档泄漏”和“故意的 PathGuard/验证器测试样本” |
| R-011 | 自然语言到机器化调度还缺真实任务演练 | High | 已新增 `UNIFIED-STATUS-OBJECT-SPEC.md` 与 `UNIFIED-STATUS-LEDGER.yaml`，但还未用真实项目完整跑通 | 下一轮用真实任务演练并把注册表升级为可调度账本 |
| R-012 | `01` SDK 文档与实际包名 import 漂移已修复 | Low | 当前运行文档、示例和交付 HTML 已将轻量 SDK public namespace 对齐为 `ghost_channel_sdk`；底层协议包仍保留合法 `ghost_channel` | 保持 `rg` 扫描，避免旧示例回流 |
| R-013 | `02` 模板可能再次被误读成完整应用 | Low | B6 已明确 template 定位，补 PowerShell 命令、`.gitkeep`、tempdir smoke 和 crystal | 后续 P02 运行诉求默认路由到 03，除非明确要把 02 独立产品化 |
| R-014 | `04` 旧 CLI 参数与旧 quickstart 曾误导后续 AI | Low | 运行文档已改为 `--max-rounds`；QUICKSTART 已加当前入口提示 | 保持 `rg -- --rounds` 扫描，历史文档只能作为保留材料 |
| R-015 | `04` 嵌入 SDK 快照与 `01` 主 SDK 边界未登记 | Low | P04 crystal 已登记：P01 为协议权威，P04 内嵌 SDK 为 snapshot/demo context | 后续若修改 SDK，先路由 P01 |
| R-016 | B7 路由 smoke 曾只测 intent，不测平台/置信度/验证引用 | Low | 已扩展 `VAL-ROOT-ROUTE-SMOKE` 为 8 场景并校验 route_decision、platform、confidence、validation_refs | 保持黄金路径输入样本进入 ROOT smoke |
| R-017 | P03 HTTP 证据曾未进入验证注册表 | Low | 已新增 `VAL-03-HTTP-SMOKE` 并纳入 P03 scope；冷启动 search timeout 调整为 30s | 后续新增 API endpoint 时补 endpoint smoke |
| R-018 | ROOT 验收曾有两个 manual-current 汇总项 | Low | `VAL-END-TO-END` 与 `VAL-CROSS-INTERFACE` 已升级为自动元验证；ROOT scope 7/7 PASS | 不再用人工 CURRENT 充当自动验收 |

## 7. 下一轮深读顺序

为了接近用户要求的“100% 深读”，建议按以下顺序推进：

1. `00` 全部 39 文件逐行审计，输出控制平面冲突表。
2. 根目录与子包全部文件逐行审计；将 `VERIFY-DELIVERY.ps1 -Strict` 作为最终交付门。
3. `05` Brain Protocol、run/api/engine/MCP/DB/Memory/Handoff 已完成 B5 结晶；后续只需围绕新失败或新集成需求复核。
4. `03` app/MCP/MemoryOS/scripts/tests 深读。
5. `04` QCM pipeline/sandbox/flywheel/tests 已完成 B4 结晶；后续只需补动态召唤匹配深挖。
6. `01` Ghost Channel SDK/schema/deploy/VERIFY 深读。
7. `02` Universal-KB 模板与 `03` 应用版差异已完成 B6 边界审计；后续按真实新项目需求复核。
8. 深化四注册表、记忆源优先级和追踪矩阵实例。
9. 运行全套最小验证命令并记录当前证据。
10. 逐项关闭 `WORKFLOW-AUDIT-ISSUE-LOG.md` 中的 P0/P1 问题。

## 8. 审计结论

第一轮结论：

```text
母包方向合理，核心齿轮存在，运行入口存在，真实记忆载体存在。
当前最大缺口不是想法，而是登记、对齐、验证和跨记忆源治理。
若不持续维护四注册表、记忆源优先级和交付验证脚本，未来 AI 仍会靠上下文临时串联，容易再次漂移。
```
