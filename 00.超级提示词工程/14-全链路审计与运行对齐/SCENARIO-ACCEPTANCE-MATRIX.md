# Scenario Acceptance Matrix

> 中文名：黄金场景验收矩阵。  
> 用途：定义母包与通用 AI 协同开发是否真正跑通。  
> 原则：每条场景必须有输入、路由、执行入口、验证命令、通过标准和停止线。

## 1. 验收分级

| 等级 | 含义 |
|---|---|
| S0 | 文件和入口存在 |
| S1 | 命令或脚本可运行 |
| S2 | 真实 CLI/API/MCP/服务场景通过 |
| S3 | 跨子系统链路通过 |
| S4 | 可交付、可复现、可由未来 AI 接手 |

本母包的目标不是所有能力都达到 S4，而是每个核心黄金路径至少达到可证明的目标等级。

## 2. 黄金路径

| ID | 场景 | 目标等级 | 用户输入样例 | 目标路由 | 验收入口 | 通过标准 |
|---|---|---:|---|---|---|---|
| GS-01 | 新 AI 进入母包并完成唤醒 | S4 | 请读取母包并完成唤醒激活 | ROOT + 00/12 | `MISSION-MEMORY.md`, `MOTHER-PACK-ACTIVATION-GUIDE.md` | 输出 `awakening_check`，明确模型原生边界与母包/用户包边界 |
| GS-02 | 自然语言进入秘书路由 | S3 | 帮我测试05 Q-SpecTrum API和角色路由 | `qa_runner.py route` -> 05 | `python qa_runner.py route "<text>"` | 输出 `guide_secretary` YAML，含 `route_feedback` |
| GS-03 | 知识库与 MCP 工具层可运行 | S2 | 我要运行03知识库搜索和MCP工具 | 03 | `python verify_install.py`, Flask `/api/search`, `/memory` | 安装验证 0 fail；HTTP 200；搜索响应非空或可解释为空 |
| GS-04 | QCM 沙盘/角色评审可作为辅助决策 | S2 | 请用角色团队评审这个方案风险 | 04 + QCM skill | `test_qcm_all.py`, role/collaboration pytest, `health_check.py` | 测试通过；沙盘输出必须绑定验证建议 |
| GS-05 | Q-SpecTrum 主平台 CLI/API 可执行 | S3 | 请给出当前系统状态摘要 | 05 | `python run.py --status`, `run.py --query`, API `/api/chat` | System ALL GREEN；query/API 返回角色路由与响应 |
| GS-06 | 最终用户交付包可验收 | S4 | 准备最终用户交付包并严格验证 | USER_PACK | `VERIFY-DELIVERY.ps1 -Strict` | 0 failures；交付包四体系、追踪、验证报告存在 |
| GS-07 | 跨系统开发闭环 | S4 | 从想法到需求、规格、任务、测试、交付 | ROOT -> 00 -> 03/04/05 -> USER_PACK | `qa_runner.py validate`, `consistency`, 目标子系统测试 | 有 USO/traceability；验证 0 fail；交付门通过 |
| GS-08 | 对抗审计和停止重构 | S4 | 为什么这个项目一直重构，怎么收敛？ | 00/14 + 07 + 验证门 | issue log, breakpoint matrix, validation registry | 剩余问题被登记；没有失败证据则停止扩写 |

## 3. 当前基础门禁

| 门禁 | 命令 | 通过标准 |
|---|---|---|
| Root validation | `python qa_runner.py validate` | 0 FAIL |
| Root consistency | `python qa_runner.py consistency` | 10/10 PASS |
| Route smoke | `python qa_runner.py validate --scope ROOT` | `VAL-ROOT-ROUTE-SMOKE` PASS |
| User delivery strict | `powershell -ExecutionPolicy Bypass -File .\VERIFY-DELIVERY.ps1 -Strict` | 0 failures |
| P03 install | `python verify_install.py` | 0 failures |
| P05 E2E | `pytest tests/test_e2e_core_pipeline.py -q` | all pass |

## 4. 停止线

不得宣称黄金路径通过，除非：

- 路由有 `selected_route` 与 `confidence`。
- 执行入口已真实运行。
- 验证命令有当前输出。
- 失败或降级被登记。
- 涉及用户交付时 strict 门通过。

## 5. 下一步

每一次深读子系统，都必须把结果回写到本矩阵：

```yaml
scenario_result:
  scenario_id: "GS-XX"
  date: "YYYY-MM-DD"
  evidence_level: "VERIFIED|GAP|RISK"
  commands: []
  observed_result: ""
  blockers: []
  next_action: ""
```

## 6. 2026-05-31 B7 当前验收结果

| ID | evidence_level | commands | observed_result | blockers | next_action |
|---|---|---|---|---|---|
| GS-01 | VERIFIED | `python qa_runner.py route "请读取母包并完成唤醒激活"` | DIRECT 0.82；输出 `guide_secretary`、`route_feedback`、`validation_refs` 与 `awakening_check`，明确模型原生边界、母包边界、用户包边界 | 无当前阻塞 | 新 AI 接手前先读 `MISSION-MEMORY.md`、激活指南和本矩阵 |
| GS-02 | VERIFIED | `python qa_runner.py validate --scope ROOT` | `VAL-ROOT-ROUTE-SMOKE` 8/8 PASS，覆盖 route decision、platform、confidence、route_feedback、validation_refs | 无当前阻塞 | 后续新增核心入口样本时扩展 smoke 矩阵 |
| GS-03 | VERIFIED | `python qa_runner.py validate --scope P03_WORKBUDDY_KB` | 3/3 PASS；`VAL-03-HTTP-SMOKE` 启动 Flask，`/memory` 与 `/api/search?q=知识库` 通过，搜索 10 条，first_path=`05-知识沉淀\README.md` | 无当前阻塞 | 若 P03 API 继续扩展，新增 endpoint-level smoke |
| GS-04 | VERIFIED | `python qa_runner.py validate --scope P04_QCM`; `python qa_runner.py validate --scope QCM_SKILL` | P04 5/5 PASS；QCM skill 2/2 PASS | 无当前阻塞 | 沙盘输出必须继续绑定 TEST/AUD 或人工验收 |
| GS-05 | VERIFIED | `python qa_runner.py validate --scope P05_QSPECTRUM`; `python qa_runner.py route "请给出05 Q-SpecTrum当前系统状态摘要"` | P05 6/6 PASS；明确 P05 状态请求 DIRECT 0.82，platform=`P05_QSPECTRUM`，validation_refs 指向 status/API/MCP smoke | 无当前阻塞 | 保持模糊状态请求为 CLARIFY，避免误路由 |
| GS-06 | VERIFIED | `python qa_runner.py validate --scope USER_PACK` | 2/2 PASS；普通和 Strict 交付验证均 0 failures / 0 warnings | 无当前阻塞 | 真实项目交付时必须补业务 smoke/test，不只依赖结构门 |
| GS-07 | VERIFIED | `python qa_runner.py route "从想法到需求、规格、任务、测试、交付"`; `python qa_runner.py validate --scope ROOT` | 跨系统路由 DIRECT 0.81，platform=`cross_subsystem`，USO=`AUD-20260531-B7-CROSS-SYSTEM-GOLDEN-PATHS`；ROOT scope 7/7 自动 PASS，`VAL-END-TO-END` 与 `VAL-CROSS-INTERFACE` 元验证均 PASS | 新业务项目实例尚未生成；本次只验证控制面与当前子系统门 | 下一个真实用户项目作为 full S4 project-instance sample |
| GS-08 | VERIFIED | `python qa_runner.py route "为什么这个项目一直重构，怎么收敛？"`; B7 crystal/sandbox | REVIEW_AUDIT CONFIRM 0.68；停止线已登记：停止结构扩写，只修 failing validation、权威文档漂移或真实运行阻塞 | 无当前阻塞 | 任何新增功能必须先登记验证门和停止条件 |
