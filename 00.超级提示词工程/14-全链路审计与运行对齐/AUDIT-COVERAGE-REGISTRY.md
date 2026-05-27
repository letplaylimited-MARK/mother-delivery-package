# Audit Coverage Registry

> 中文名：审计覆盖登记表。  
> 用途：记录当前这轮审计真正覆盖了什么、证据来自哪里、哪些仍然只是推断或缺口。  
> 时间：2026-05-26。  
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

未完成：

- 1118 个稳定基线文件逐文件语义审计。
- 所有 Python 模块的调用图/LSP 级分析。
- 所有 SQLite 表结构和数据质量审计。
- 所有 README 中历史验证声明的重新运行复核。
- 所有 PDF/HTML/历史报告内容的逐字审计。
- 四注册表的字段级充实、验证和后续自动化。

## 2. 文件数量基线

| 区域 | 文件数 | 审计状态 | 说明 |
|---|---:|---|---|
| `00.超级提示词工程` | 39 | PARTIAL-DEEP | 控制平面已重点读取；新增断裂点修复矩阵和记忆源索引后为 39 文件 |
| `01.通讯协议_幽灵通道` | 299 | ENTRYPOINT-SCAN | README/INDEX/HANDOFF/VERIFY/SDK入口已扫描 |
| `02.通用知识库框架_Universal-KB` | 21 | ENTRYPOINT-SCAN | README/AGENTS 已扫描 |
| `03.数据库管理_文件夹整理AI应用` | 172 | ENTRYPOINT-SCAN | README/AGENTS/app/mcp/verify 已扫描 |
| `04.QCM-MVP-Emergence` | 146 | ENTRYPOINT-SCAN | README/HANDOFF/VERIFY/核心代码入口已扫描 |
| `05.超极智脑_Q-SpecTrum` | 431 | ENTRYPOINT-SCAN | README/INDEX/AGENTS/Brain Protocol/run/API/MCP/verify 已扫描 |
| 根入口文档 | 3 | PARTIAL-DEEP | `MISSION-MEMORY`, `AI_PROJECT_CONTEXT`, `开发者母交付包使用说明` 已读取 |
| `协同通用AI大模型开发交付包` | 7 | TEMPLATE-VERIFIED | 四体系模板、组装规则和 `VERIFY-DELIVERY.ps1` 已扫描；模板模式验证通过 |
| 合计 | 1118 | BASELINED | 稳定交付基线；`.pytest_cache` 是验证命令临时生成物，不计入基线 |

注：`rg --files` 默认受隐藏文件和忽略规则影响，读数会低于 PowerShell `Get-ChildItem -Force` 口径；本登记表采用 PowerShell 强制遍历并排除运行缓存的口径。

## 3. 文件类型基线

当前类型盘点显示主体为：

| 类型 | 数量 | 意义 |
|---|---:|---|
| `.md` | 503 | 协议、说明、交接、审计、知识库主体 |
| `.py` | 312 | 可运行应用、MCP、SDK、测试、脚本 |
| `.json` | 76 | 模板、配置、状态、数据对象 |
| 无扩展名 | 28 | 可能包含配置、脚本或包元数据，需后续细审 |
| `.yaml` | 33 | 配置、工作流、角色、部署、审计注册表、统一状态账本、记忆源索引 |
| `.html` | 29 | Web UI 或导出文档 |
| `.sql` | 16 | 数据库结构或初始化脚本 |
| `.yml` | 14 | CI、配置、部署 |
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
| `03` | `python verify_install.py` | 当前重跑 22 pass / 0 fail / 1 warning；`.env` 缺失为可选高级能力警告 |
| `03` | `python app.py --port 5000` | Flask 入口存在；本轮未启动服务 |
| `03` | `python mcp_server.py` | MCP 入口存在；本轮未启动 |
| `03` | `$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'; pytest tests/ -q` | 当前重跑 103 passed，3 warnings；无 UTF-8 环境时 Windows 下曾出现 2 个 MCP 集成测试 UnicodeDecodeError |
| `04` | `python "02-代码编写\test_qcm_all.py"` | 当前重跑 25 PASS / 0 FAIL |
| `04` | `pytest "02-代码编写\test_roles.py" "02-代码编写\test_collaboration.py" "02-代码编写\test_sandbox.py" "02-代码编写\test_flywheel.py" "02-代码编写\test_summoning.py" -q` | 当前重跑 38 passed；不带 `02-代码编写` 的旧 shorthand 会失败 |
| `04` | `python health_check.py` | 当前重跑 4/6 NEEDS ATTENTION，exit 1；必须单独解释，不能当通过 |
| `05` | `python verify-integration.py` | 当前重跑 OK |
| `05` | `$env:PYTHONUTF8='1'; python run.py --status` | 当前重跑 ALL GREEN |
| `05` | `python run.py --web` | Web/API 入口存在；本轮未启动 |
| `05` | `python qspectrum_mcp_server.py` | MCP stdio 入口存在；本轮未启动 |
| 用户交付包 | `powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1` | 当前运行通过，0 failures，9 expected template warnings |
| 用户交付包 | `powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1 -Strict` | 当前按预期失败，10 failures；严格模式会抓项目实例缺口、普通模板占位和缺少项目验证入口 |

## 5. 数据载体基线

已扫描到以下类型：

- `03/.workbuddy/index/search_index.db`
- `03/.workbuddy/记忆层/memory_data/short_term/*.jsonl`
- `03/.workbuddy/config/*.json`
- `03/.workbuddy/AI协作体系/模型配置/*.yaml`
- `05/platform.db`
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
| R-004 | 子包仍是骨架，严格交付模式未通过 | High | `VERIFY-DELIVERY.ps1` 已存在且模板模式通过；`-Strict` 暴露项目实例、占位符和项目验证入口缺口 | 具体项目交付时补上下文、交接、追踪、验证报告和项目验证入口 |
| R-005 | `05` 依赖描述有漂移 | Medium | `requirements.txt` 与 `pyproject.toml` 叙述不一致 | 统一依赖说明 |
| R-006 | `01/02/04` 的验证语义不统一 | Medium | 子智能体审计发现 `01 VERIFY.ps1` 是完整性校验、`02` 是模板审查、`04 health_check.py` 语义需复核 | 用 `VALIDATION_REGISTRY.yaml` 区分 integrity/test/template/health/delivery gates |
| R-007 | 两个子 git 仓库已有未归属修改 | Medium | `03` 和 `05` `git status --short` 有修改 | 不覆盖；后续单独确认来源 |
| R-008 | `01/02/04` 文档状态存在漂移 | Medium | 子智能体审计发现 `01` VERIFY 预期文本/测试路径、`02` 模板过度承诺与 quickstart 链接、`04` 文件数/运行命令/旧 superpowers 指令存在不一致 | 下一轮按子系统修复，不在本轮贸然覆盖 |
| R-009 | Windows UTF-8 环境未固定会导致 MCP 集成测试假失败 | Medium | `03` 默认 `pytest tests/ -q` 曾出现 2 个 UnicodeDecodeError；设置 `PYTHONUTF8=1` 与 `PYTHONIOENCODING=utf-8` 后 103 passed | 将 UTF-8 环境写入验证命令、README 和未来自动化脚本 |
| R-010 | 历史报告/迁移计划残留旧本机路径表述 | Medium | 扩展 `rg` 发现 `03` 历史报告和迁移计划存在旧路径；本轮已将可执行示例改成占位路径 | 后续把扫描纳入固定验证，区分“运行文档泄漏”和“故意的 PathGuard/验证器测试样本” |
| R-011 | 自然语言到机器化调度还缺真实任务演练 | High | 已新增 `UNIFIED-STATUS-OBJECT-SPEC.md` 与 `UNIFIED-STATUS-LEDGER.yaml`，但还未用真实项目完整跑通 | 下一轮用真实任务演练并把注册表升级为可调度账本 |
| R-012 | `01` SDK 文档与实际包名存在 import 漂移 | Medium | `ghost-channel-sdk/README.md` 使用 `from ghost_channel import ...`，实际轻量 SDK 包名为 `ghost_channel_sdk` | 下一轮统一示例 |
| R-013 | `02` 模板文档过度承诺，Windows 快速开始命令不稳 | Medium | README 写“完整功能已实现”，快速开始用 `mkdir -p ...` | 下一轮明确 template 定位并补 PowerShell 友好验证 |
| R-014 | `04` 旧 CLI 参数与旧 quickstart 会误导后续 AI | Medium | 文档存在 `--rounds`，当前 `qcm/main.py` 使用 `--max-rounds`；旧 quickstart 引用不存在目录 | 下一轮统一 QCM 入口文档 |
| R-015 | `04` 嵌入 SDK 快照与 `01` 主 SDK 边界未登记 | Medium | `04` 内含幽灵通道 SDK 副本，pipeline 又自实现协议概念 | 标明权威来源、快照边界和同步策略 |

## 7. 下一轮深读顺序

为了接近用户要求的“100% 深读”，建议按以下顺序推进：

1. `00` 全部 39 文件逐行审计，输出控制平面冲突表。
2. 根目录与子包全部文件逐行审计；将 `VERIFY-DELIVERY.ps1 -Strict` 作为最终交付门。
3. `05` Brain Protocol、run/api/engine/MCP/DB/Memory/Handoff 深读。
4. `03` app/MCP/MemoryOS/scripts/tests 深读。
5. `04` QCM pipeline/sandbox/flywheel/tests 深读。
6. `01` Ghost Channel SDK/schema/deploy/VERIFY 深读。
7. `02` Universal-KB 模板与 `03` 应用版差异审计。
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
