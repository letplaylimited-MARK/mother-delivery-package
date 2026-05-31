# Workflow Audit Issue Log

> 中文名：全链路工作流审计问题日志。  
> 用途：把并行审计、命令验证和人工判断发现的“齿轮卡点”登记成可追踪问题，避免只停留在聊天结论。  
> 当前轮次：2026-05-27 全链路审计断裂点修复轮。  
> 证据口径：只把当前文件、当前命令输出、子智能体只读审计结果和可定位路径作为事实；历史报告只作为辅助线索。

## 1. 当前总体结论

```text
母包方向合理，核心齿轮存在，运行入口存在，真实记忆载体存在。
但它还不是“自然语言进入后自动调度所有系统”的完全机器化平台。
当前最大问题不是没有概念，而是：
  注册表字段还不够可调度
  自然语言到机器状态对象还没落地
  验证语义还需要拆分
  旧文档/旧命令/嵌入副本会误导后续 AI
  子包仍是模板，不是最终项目交付物
```

## 2. 本轮已复核证据

| 证据项 | 当前结果 | 结论 |
|---|---|---|
| 文件计数口径 | 当前 `qa_runner.py validate` 清洗计数 1150；原子清单记录 1150 文件原子；历史 1118/1138/1140/1148 基线是早期口径 | 文件计数只作漂移哨兵，不再作为“已逐文件语义读完”的证明 |
| 本机路径扫描 | 未命中当前母包根、旧 D 盘路径、`C:\Users\...` 等硬编码模式 | 当前可交付逻辑未发现本机绝对路径泄漏 |
| `01` manifest 校验 | 299 verified / 0 failed / 0 missing | 完整性校验通过 |
| `01` SDK 测试 | 18 + 68 + 76 + 22 = 184 passed | SDK 功能测试通过；必须和 manifest 校验分开记录 |
| `02` MemoryOS smoke | `py_compile` 通过；`memoryos.py` 运行输出短期记忆 1 条；smoke 临时数据不再写到母包根目录 | 模板内代码可运行；仍应定位为轻量模板 |
| `03` 安装验证 | 23 pass / 0 fail / 1 `.env` warning | 基础运行通过；MCP 依赖已纳入安装验证；高级 API 能力依赖 `.env` |
| `03` 测试 | 107 passed / 3 warnings | MCP stdio 编码/输出污染、Web browse 边界、batch_import 入口和 vector_search 测试隔离已修复 |
| `04` QCM 主测试 | 25 PASS / 0 FAIL；专项 pytest 38 passed；config-sync 4 passed | 核心测试与配置漂移守卫通过 |
| `04` runtime smoke | research R22 emergence；production JSON output；service `/health`/`/status`/`/simulate` HTTP 200；Cap-D/G flag 场景通过 | QCM 不只是测试可过，三模式入口也可运行 |
| `04` health check | 6/6 passed，READY | 健康检查与交付测试已对齐 |
| `qcm-v3.0.skill` | validator 0 issues / 100.0% / PASS；pytest 173 passed | 根目录关键技能包当前可解包、可验证、可测试 |
| `05` integration/status | integration OK with 1 runtime `_HANDOFF/` warning；status ALL GREEN | 主平台结构与状态入口当前可用 |
| `05` pytest/E2E/API/MCP | pytest 158 passed；`run.py --e2e` 13 passed / 0 failed；API smoke Q02/Q06/Q08；MCP smoke 18 tools / clean JSON-RPC stdout | 主平台不是只“结构存在”，CLI/API/MCP/runtime 已当前实测可运行 |
| 用户交付包普通验证 | PASS，0 failures，0 warnings | 模板态正常 |
| 用户交付包 Strict 验证 | 0 failures / 0 warnings | 正式项目交付门当前通过 |

## 3. P0/P1 问题清单

| ID | 优先级 | 子系统 | 问题 | 影响 | 当前处置 |
|---|---|---|---|---|---|
| WAI-001 | P0 | ROOT/00 | 统一状态对象此前尚未落地，`id/type/status/source/evidence/validation/risks/next_action` 仍主要存在于蓝图和注册表 | AI 仍可能靠聊天上下文临时串联，难以真正调度 | 已新增 `UNIFIED-STATUS-OBJECT-SPEC.md` 和 `UNIFIED-STATUS-LEDGER.yaml`；下一步用真实任务演练 |
| WAI-002 | P0 | 00/14 | 注册表已有初版，但缺 `cwd`、精确命令、是否写文件、输入/输出 schema、来源行号、最近验证证据、失败降级 | 注册表仍是“索引”，还不是可执行调度账本 | 已给出统一状态对象字段模型；后续逐条补注册表字段 |
| WAI-003 | P1 | USER_PACK | Strict 门当前 0 failures | 后续若新项目内容回到模板占位，仍可能误交付空骨架 | 保持 `VERIFY-DELIVERY.ps1 -Strict` 为结构/交接门；正式项目另跑真实 smoke/test |
| WAI-004 | P1 | 01 | `VERIFY.ps1` 是 manifest 完整性校验，不是 SDK 全测试；README/INDEX 容易混读 | 后续 AI 可能错误宣称“VERIFY 通过 = 全部测试通过” | 已在本轮补跑 184 SDK 测试，并要求拆分验证语义 |
| WAI-005 | P1 | 01 | `ghost-channel-sdk` 运行示例和压力脚本曾使用旧 `ghost_channel` 命名空间，实际轻量 SDK 包名为 `ghost_channel_sdk` | 用户或 AI 可能导入错误包 | 已修复 Python 示例与压力脚本，并通过示例运行与 100 并发压力验证 |
| WAI-006 | P1 | 01/04 | `04` 内嵌幽灵通道 SDK 副本，`qcm/pipeline.py` 自实现部分协议能力 | `01` 主 SDK 与 `04` 快照/适配层可能漂移 | 已在 P04 crystal 标明：P01 是协议权威，P04 内嵌 SDK 是 snapshot/demo context |
| WAI-007 | P1 | 02 | README/docs 曾叙述为完整可运行系统，但控制面定位为轻量模板 | 模板可能被误当成可运行知识库应用 | 已明确 `P02_UNIVERSAL_KB` 为 template，完整运行应用以 03 为准，并补 B6 crystal |
| WAI-008 | P1 | 02 | 快速开始曾只给 Unix `mkdir -p`，对 Windows/PowerShell 不稳 | 开发者在目标环境复现失败 | 已补 PowerShell `Copy-Item` / `New-Item` 等价命令，并用 `.gitkeep` 保留空目录 |
| WAI-009 | P1 | 04 | `USER_GUIDE.md`/`SCENARIOS.md` 使用旧参数 `--rounds`，当前 `qcm/main.py` 使用 `--max-rounds` | 运行文档误导 | 已统一运行文档、README、INSTALL、SCENARIOS，并在 troubleshooting 保留旧参数提示 |
| WAI-010 | P1 | 04 | `QUICKSTART.md` 自称已被取代且引用历史目录 | 新 AI 可能读到旧入口 | 已补 2026-05-31 当前入口提示，并指向 README / handoff / P04 crystal；历史内容保留但降权 |
| WAI-011 | P1 | 04 | 动态召唤用 `required_skills` 匹配 `role_id`，尚不是技能向量/能力卡匹配 | 自然语言技能需求到角色调度仍薄弱 | 进入 QCM 深读与修复路线 |
| WAI-012 | P1 | 05 | `requirements.txt` 与 `pyproject.toml` 依赖叙述曾不一致 | 打包迁移时可能漏装依赖 | 已将 README / QUICK-START / 非技术用户自检对齐为 Python 3.10+ 与 `pip install -r requirements.txt` |
| WAI-013 | P1 | 03/05 | 多记忆源已有优先级文档，但尚未用真实任务实测冲突解决 | 长期记忆可能再次混淆 | 已新增 `MEMORY-SOURCE-INDEX.yaml`；下一步用真实项目任务做读写冲突演练 |
| WAI-014 | P1 | 00/12 | Guide Secretary 已有 `qa_runner.py route` 最小可执行入口，但部分中文场景仍以 CLARIFY 为主 | 自然语言到真实执行已可生成 YAML，但高置信自动执行仍需更多任务样本校准 | 已纳入 `VAL-ROOT-ROUTE-SMOKE`，并保留人工确认作为低置信保护 |
| WAI-015 | P0 | 00/02/03/06/12/14 | 断裂点散落：启动顺序、路由反馈、USO 追踪、暂停/阻塞状态、记忆源优先级、验证副作用缺少统一修复矩阵 | 后续 AI 只能凭经验猜测“先修哪三个”，容易漏掉隐蔽断裂点 | 已新增 `BREAKPOINT-REPAIR-MATRIX.md`，并同步修复 Guide、Handoff、Context Pack、Atomic Governance、Routing Matrix、Cross Workflow |
| WAI-016 | P0 | 05 | 回归测试依赖手动启动 `run.py --web`，干净环境下 pytest 无法证明 API 可用 | 测试通过/失败取决于外部状态，AI 容易误判 | 已改为 regression 自启动 mock API server，并纳入 `VAL-05-PYTEST`/`VAL-05-API-SMOKE` |
| WAI-017 | P0 | 05 | `ProjectOrchestrator.record_result()` 秒级 ID 冲突后异常路径未关闭 SQLite 连接，导致 `projects.db` 锁住，连续 chat 约 11 秒/次 | 真实 API 聊天会超时或显著变慢 | 已改用 `time.time_ns()`，并为 record_interaction/record_result 添加 `finally: conn.close()`；pytest/API smoke 通过 |
| WAI-018 | P1 | 05/Windows | `run.py --e2e` 子脚本与直接运行测试脚本在 Windows GBK 控制台下会 UnicodeEncodeError/DecodeError | 用户入口在 Windows 下不稳定 | 已为 e2e 子进程设置 UTF-8 环境，并为关键脚本 reconfigure stdout/stderr |
| WAI-019 | P1 | 05/docs | `SYSTEM-PROMPT.md`、`QUICK-START.md`、`README.md` 与当前 runtime/E2E 自检漂移 | 新 AI/非技术用户/开发者会被旧入口误导 | 已补当前 bootstrap capsule、方法/步骤/命令、developer integration facts；E2E 自评转绿 |
| WAI-020 | P1 | 02 | `memoryos.py` smoke 过去使用调用方相对路径 `./test_memory` | 在母包根目录运行验证会生成 root runtime artifact，后续 AI 可能误认成项目数据 | 已改为 `tempfile.TemporaryDirectory()`，并清理旧空 `test_memory` |
| WAI-021 | P1 | USER_PACK | `scripts/verify.ps1` 只是 Strict 包装器，容易被误解为真实业务验证入口 | 最终用户可能把结构门禁通过误当应用运行通过 | 已在 README、组装规则和脚本注释中声明：正式项目必须扩展/替换为真实 smoke/test |
| WAI-022 | P1 | 00/12 | B7 初始 route smoke 只断言 intent 与 route_feedback，未检查 route_decision、platform、confidence、validation_refs，也未覆盖 GS-07 | 黄金路径可能“看似可路由”，但缺真实跨系统可接手信息 | 已扩展 `VAL-ROOT-ROUTE-SMOKE` 为 8 场景，并断言决策、平台、置信度、route_feedback 与 validation_refs |
| WAI-023 | P1 | 03 | B7 初始矩阵要求 P03 HTTP `/memory` 与 `/api/search`，但验证注册表只覆盖 install/tests | GS-03 不能证明 Web/API 层真正可用 | 已新增 `VAL-03-HTTP-SMOKE`；冷启动 search 超时从 5s 调整为 30s，当前 P03 scope 3/3 PASS |
| WAI-024 | P1 | ROOT/00 | `VAL-END-TO-END` 与 `VAL-CROSS-INTERFACE` 曾只是 `verified_current` 人工汇总项 | 全量验证显示 ALL CLEAR 时仍有 2 个非自动灰区，后续 AI 可能误读验收强度 | 已升级为自动元验证；ROOT scope 当前 7/7 PASS，自动 7/7 |

## 4. 深读与修复顺序

1. 先把 `UNIFIED-STATUS-LEDGER.yaml` 用真实任务跑通，让自然语言任务能落成 `GOAL/REQ/SPEC/TASK/TEST/AUD/MEM` 与验证记录。
2. 再把 `00/14` 注册表升级为可调度账本：补 `cwd`、命令、读写半径、输入输出、证据、失败处理、`side_effects`。
3. 用 `BREAKPOINT-REPAIR-MATRIX.md` 复核 6 个显式断裂点、4 个隐蔽断裂点是否都能被 Guide/Handoff/Context/USO 捕获。
4. 继续追踪 `01` 企业部署 Docker 在无本机 Docker 环境下的实际镜像构建验证；轻量 SDK import 示例已修复。
5. `02` 模板定位、Windows 快速开始、空目录保留与 MemoryOS smoke 副作用已修；后续仅在需要独立应用时再设计 `verify_kb` 干跑脚本。
6. `04` 旧 CLI 参数、旧 quickstart、SDK 快照边界已修；后续仅剩动态召唤匹配逻辑需深挖。
7. `05` 依赖说明已修；后续把 `00` 使命唤醒与 `05` Brain Protocol 建立显式桥接。
8. 用一个真实样例贯通：用户自然语言 -> guide_secretary YAML -> 需求/规格/任务/测试/审计/记忆 -> 能力调用 -> 用户交付包四体系。

## 5. 停止线

后续任何 AI 不能说：

- “已 100% 阅读理解全部 1150 文件”，除非有逐文件清单、阅读状态、证据和验证记录。
- “长期记忆已加载”，除非列出真实读取的文件、数据库或 handoff。
- “子包可以正式交付”，除非 `VERIFY-DELIVERY.ps1 -Strict` 为 0 failures 且项目验证入口通过。
- “01 全部验证已通过”，除非同时区分 manifest 校验、三组 SDK pytest、TypeScript/npm 测试和企业部署验证。
- “QCM 沙盘证明通过”，除非沙盘结论已经绑定到 TEST/AUD 或人工验收。
