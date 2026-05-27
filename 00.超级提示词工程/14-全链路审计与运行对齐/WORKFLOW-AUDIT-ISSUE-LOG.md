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
| 稳定文件基线 | 1118 文件，排除 `.git`、`node_modules`、`dist/build/coverage`、`__pycache__`、`.pytest_cache` | 本轮加入断裂点修复矩阵和记忆源索引后，`00` 为 39 文件 |
| 本机路径扫描 | 未命中当前母包根、旧 D 盘路径、`C:\Users\...` 等硬编码模式 | 当前可交付逻辑未发现本机绝对路径泄漏 |
| `01` manifest 校验 | 299 verified / 0 failed / 0 missing | 完整性校验通过 |
| `01` SDK 测试 | 18 + 68 + 76 = 162 passed | SDK 功能测试通过；必须和 manifest 校验分开记录 |
| `02` MemoryOS smoke | `py_compile` 通过；`memoryos.py` 运行输出短期记忆 1 条 | 模板内代码可运行；仍应定位为轻量模板 |
| `03` 安装验证 | 22 pass / 0 fail / 1 `.env` warning | 基础运行通过；高级 API 能力依赖 `.env` |
| `03` 测试 | UTF-8 环境下 103 passed / 3 warnings | Windows 验证必须固定 UTF-8 环境 |
| `04` QCM 主测试 | 25 PASS / 0 FAIL；专项 pytest 38 passed | 核心测试通过 |
| `04` health check | 4/6 passed，exit 1，NEEDS ATTENTION | 不是交付通过门；需要单独解释或修复阈值 |
| `05` integration/status | integration OK；status ALL GREEN | 主平台当前可用，Windows 需 `PYTHONUTF8=1` |
| 用户交付包普通验证 | PASS，0 failures，9 expected warnings | 模板态正常 |
| 用户交付包 Strict 验证 | 10 failures | 正式项目交付前必须补齐实例内容 |

## 3. P0/P1 问题清单

| ID | 优先级 | 子系统 | 问题 | 影响 | 当前处置 |
|---|---|---|---|---|---|
| WAI-001 | P0 | ROOT/00 | 统一状态对象此前尚未落地，`id/type/status/source/evidence/validation/risks/next_action` 仍主要存在于蓝图和注册表 | AI 仍可能靠聊天上下文临时串联，难以真正调度 | 已新增 `UNIFIED-STATUS-OBJECT-SPEC.md` 和 `UNIFIED-STATUS-LEDGER.yaml`；下一步用真实任务演练 |
| WAI-002 | P0 | 00/14 | 注册表已有初版，但缺 `cwd`、精确命令、是否写文件、输入/输出 schema、来源行号、最近验证证据、失败降级 | 注册表仍是“索引”，还不是可执行调度账本 | 已给出统一状态对象字段模型；后续逐条补注册表字段 |
| WAI-003 | P0 | USER_PACK | 子包是模板，Strict 失败 10 项 | 若误当正式交付包，会交付空骨架 | 保持 Strict 失败作为保护机制 |
| WAI-004 | P1 | 01 | `VERIFY.ps1` 是 manifest 完整性校验，不是 SDK 全测试；README/INDEX 容易混读 | 后续 AI 可能错误宣称“VERIFY 通过 = 全部测试通过” | 已在本轮补跑 162 SDK 测试，并要求拆分验证语义 |
| WAI-005 | P1 | 01 | `ghost-channel-sdk` 文档示例使用 `from ghost_channel import ...`，实际轻量 SDK 包名为 `ghost_channel_sdk` | 用户或 AI 可能导入错误包 | 下一轮修复 README 示例 |
| WAI-006 | P1 | 01/04 | `04` 内嵌幽灵通道 SDK 副本，`qcm/pipeline.py` 自实现部分协议能力 | `01` 主 SDK 与 `04` 快照/适配层可能漂移 | 需要在注册表标明权威来源与快照边界 |
| WAI-007 | P1 | 02 | README 叙述“完整功能已实现”，但控制面定位为轻量模板 | 模板可能被误当成可运行知识库应用 | 保持 `P02_UNIVERSAL_KB` 为 template；下一轮修正文案 |
| WAI-008 | P1 | 02 | 快速开始使用 `mkdir -p Universal-KB/{...}`，对 Windows/PowerShell 不稳 | 开发者在目标环境复现失败 | 下一轮补 PowerShell 等价命令或脚本 |
| WAI-009 | P1 | 04 | `USER_GUIDE.md`/`SCENARIOS.md` 使用旧参数 `--rounds`，当前 `qcm/main.py` 使用 `--max-rounds` | 运行文档误导 | 下一轮统一 QCM CLI 文档 |
| WAI-010 | P1 | 04 | `QUICKSTART.md` 自称已被取代且引用不存在的旧目录 | 新 AI 可能读到旧入口 | 下一轮改成跳转或归档说明 |
| WAI-011 | P1 | 04 | 动态召唤用 `required_skills` 匹配 `role_id`，尚不是技能向量/能力卡匹配 | 自然语言技能需求到角色调度仍薄弱 | 进入 QCM 深读与修复路线 |
| WAI-012 | P1 | 05 | `requirements.txt` 与 `pyproject.toml` 依赖叙述不一致 | 打包迁移时可能漏装依赖 | 下一轮统一安装说明 |
| WAI-013 | P1 | 03/05 | 多记忆源已有优先级文档，但尚未用真实任务实测冲突解决 | 长期记忆可能再次混淆 | 已新增 `MEMORY-SOURCE-INDEX.yaml`；下一步用真实项目任务做读写冲突演练 |
| WAI-014 | P1 | 00/12 | Guide Secretary 目前是协议和模板，尚无“输入自然语言 -> 输出 guide_secretary YAML”的可执行入口 | 自然语言到真实执行仍需人工桥接 | 已补 `route_feedback` 和 `traceability` 字段；下一轮建设最小可执行路由器或干跑脚本 |
| WAI-015 | P0 | 00/02/03/06/12/14 | 断裂点散落：启动顺序、路由反馈、USO 追踪、暂停/阻塞状态、记忆源优先级、验证副作用缺少统一修复矩阵 | 后续 AI 只能凭经验猜测“先修哪三个”，容易漏掉隐蔽断裂点 | 已新增 `BREAKPOINT-REPAIR-MATRIX.md`，并同步修复 Guide、Handoff、Context Pack、Atomic Governance、Routing Matrix、Cross Workflow |

## 4. 深读与修复顺序

1. 先把 `UNIFIED-STATUS-LEDGER.yaml` 用真实任务跑通，让自然语言任务能落成 `GOAL/REQ/SPEC/TASK/TEST/AUD/MEM` 与验证记录。
2. 再把 `00/14` 注册表升级为可调度账本：补 `cwd`、命令、读写半径、输入输出、证据、失败处理、`side_effects`。
3. 用 `BREAKPOINT-REPAIR-MATRIX.md` 复核 6 个显式断裂点、4 个隐蔽断裂点是否都能被 Guide/Handoff/Context/USO 捕获。
4. 修 `01` 轻量 SDK import 示例和旧包名/旧路径残留。
5. 修 `02` 模板定位、Windows 快速开始、可选 `verify_kb` 干跑脚本。
6. 修 `04` 旧 CLI 参数、旧 quickstart、SDK 快照边界和动态召唤匹配逻辑。
7. 修 `05` 依赖说明，并把 `00` 使命唤醒与 `05` Brain Protocol 建立显式桥接。
8. 用一个真实样例贯通：用户自然语言 -> guide_secretary YAML -> 需求/规格/任务/测试/审计/记忆 -> 能力调用 -> 用户交付包四体系。

## 5. 停止线

后续任何 AI 不能说：

- “已 100% 阅读理解全部 1118 文件”，除非有逐文件清单、阅读状态、证据和验证记录。
- “长期记忆已加载”，除非列出真实读取的文件、数据库或 handoff。
- “子包可以正式交付”，除非 `VERIFY-DELIVERY.ps1 -Strict` 为 0 failures 且项目验证入口通过。
- “01 全部验证已通过”，除非同时区分 manifest 校验、三组 SDK pytest、TypeScript/npm 测试和企业部署验证。
- “QCM 沙盘证明通过”，除非沙盘结论已经绑定到 TEST/AUD 或人工验收。
