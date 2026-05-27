# Cross Project AI Collaboration Workflow

> 用途：让多个 AI 应用开发项目在同一套流程下协同，而不是各自孤立发展。

## 1. 标准闭环

```text
Intake
  -> Atomic ID
  -> Route
  -> Route Feedback
  -> Context Pack
  -> Unified Status Object
  -> Sandbox
  -> Execute
  -> Verify
  -> Audit
  -> Handoff
  -> Memory
```

## 2. 阶段定义

### 2.1 Intake：接收需求

要问清楚：

- 用户要解决业务问题、技术问题，还是体系问题？
- 输出是代码、文档、运行结果、审查报告，还是规划？
- 是否涉及多个子系统？

### 2.2 Route：子系统路由

使用 `02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md`。

原则：

- 单点任务进入单子系统。
- 跨系统任务默认由 `05.超极智脑_Q-SpecTrum` 做主线。
- `00` 只负责提示词和协同，不承载业务代码。
- 路由后必须产生 `route_feedback`：记录命中的路线、被排除的候选、路由后置信度、是否需要 `CONFIRM/CLARIFY/BLOCKED`。
- 路由反馈必须回写到 Guide Secretary Handoff 和 Context Pack，不能只停留在聊天结论。

### 2.2.1 Atomic ID：原子化编号

持续开发任务必须先建立或引用：

```text
GOAL -> REQ -> PRD -> SPEC -> TASK -> TEST -> AUD/FIX -> MEM
```

如果 AI 无法说清当前处理哪个 `REQ/TASK`，必须暂停执行，回到需求澄清和追踪矩阵。

跨文件夹任务还必须建立或引用统一状态对象：

```text
USO -> ledger_ref -> validation_refs -> handoff/memory
```

缺少 `USO ID` 或 `ledger_ref` 时，任务进入 `PAUSED`，不得直接跨目录修改。

### 2.3 Context Pack：组装上下文

使用 `03-上下文包模板/AI-CONTEXT-PACK-TEMPLATE.md`。

原则：

- 先小后大。
- 先入口文档，再代码。
- 先当前验证结果，再历史报告。

### 2.4 Execute：执行

按任务类型选择动作：

| 类型 | 动作 |
|---|---|
| 文档 | 生成/更新说明、索引、交接、路线图 |
| 代码 | 小步修改、保持子系统边界、遵循本地模式 |
| 验证 | 运行对应命令，记录真实输出 |
| 集成 | 先写接口契约，再接入实现 |
| 研究 | 标注来源、区分事实和推断 |
| 交付 | 区分母交付包与用户交付包，补齐价值/功能/结构/运作四体系 |

复杂任务执行前必须先完成角色团队沙盘；沙盘输出不等于完成证据，只能作为执行方案和风险清单。

### 2.5 Verify：验证

每个子系统有自己的验证门：

```text
01 -> VERIFY.ps1 是 manifest/integrity；SDK tests 需另跑三组 pytest
02 -> template review + memoryos.py compile/smoke；smoke 会产生测试记忆副作用
03 -> verify_install.py + pytest tests/；Windows 默认终端需 UTF-8 环境
04 -> test_qcm_all.py + pytest paper modules；health_check.py 是 needs-review，不是发布门
05 -> verify-integration.py + run.py --status；Windows 状态输出需 UTF-8 环境
USER_PACK -> VERIFY-DELIVERY.ps1 是模板/base gate；-Strict 是最终项目交付门
```

### 2.6 Handoff：交接

交接摘要必须包含：

```text
任务:
子系统:
读取文件:
改动文件:
验证命令:
验证结果:
已知风险:
下一步:
```

### 2.7 Memory：记忆沉淀

沉淀位置：

| 内容 | 写入位置 |
|---|---|
| 全局地图更新 | 根目录 `AI_PROJECT_CONTEXT.md` |
| 提示词/流程更新 | `00.超级提示词工程/` |
| Q-SpecTrum 长期记忆 | `05.超极智脑_Q-SpecTrum/_HANDOFF/` 或 `BRAIN-KB/` |
| 知识库内容 | `03.数据库管理_文件夹整理AI应用/05-知识沉淀/` |
| 最终用户交付内容 | `协同通用AI大模型开发交付包/01-价值体系/` 至 `04-运作体系/` |

## 3. 跨系统集成路线

### Phase 1：统一登记

建立或维护：

- 项目注册表
- 能力注册表
- 提示词注册表
- 验证命令注册表

### Phase 2：统一启动

让任何 AI 都按同一套启动顺序：

```text
MISSION-MEMORY.md
-> AI_PROJECT_CONTEXT.md
-> 00 README
-> Master Orchestrator Prompt
-> Model Native Collaboration Protocol
-> Mission Memory Awakening Protocol
-> Guide Secretary Protocol
-> Routing Matrix
-> Route Feedback
-> Context Pack
-> Unified Status Ledger
```

### Phase 3：统一验证

把各子系统验证命令变成一个总控验证流程。

### Phase 4：统一记忆

把任务结论沉淀到：

- 全局项目地图
- Q-SpecTrum `_HANDOFF`
- Universal-KB 知识沉淀

### Phase 5：统一产品化

以 `05` 为主平台，逐步把 `01/03/04` 的能力以 API/MCP/SDK 方式接入，而不是复制文件。

### Phase 6：统一交付

开发者先使用母交付包完成项目开发，再进入 `协同通用AI大模型开发交付包/` 填写：

- 价值体系：用户、问题、收益、验收指标。
- 功能体系：功能、流程、AI 能力、边界。
- 结构体系：目录、模块、数据流、接口、依赖。
- 运作体系：安装、启动、验证、维护、排错。

最后执行路径扫描、密钥清理、验证命令，再压缩交付给最终用户。

## 4. 禁止事项

- 禁止在没有验证的情况下宣称“已完成”。
- 禁止把旧报告当成当前状态。
- 禁止跨目录大规模重构而不建立回滚点。
- 禁止让提示词只停留在话术层，不绑定真实文件和命令。
