# Deep Understanding & Knowledge Crystallization Blueprint

> 中文名：深度理解、知识图谱与知识结晶蓝图。  
> 用途：把“先做足功课”变成可复核流程，避免未来 AI 直接扩写、重构或宣称已理解。  
> 当前状态：规划蓝图，后续每一批深读必须补证据、验证和状态对象。

## 1. 核心意图

本母包不是为了取代通用 AI 大模型，而是为通用 AI 提供一个可协作、可路由、可审计、可验证、可交付的项目操作环境。

正确关系是：

```text
通用 AI 大模型
  保留自身系统规则、工具边界、推理能力
  接收母包提供的项目上下文、角色协议、验证门和交付结构

母交付包
  不伪装成更高层 AI
  不要求模型拥有永久人格
  不把聊天上下文当长期记忆
  只提供真实文件、真实数据库、真实命令、真实交接和真实验收
```

因此，后续完善目标不是“继续创造更多提示词”，而是让自然语言任务能稳定进入：

```text
使命唤醒 -> 引导秘书 -> 路由矩阵 -> 最小上下文 -> 子系统执行
  -> 验证证据 -> 知识结晶 -> 长期记忆/交接 -> 用户交付包
```

## 2. 证据等级

每一次深读和结晶必须标注证据等级：

| 等级 | 含义 | 可进入长期记忆 |
|---|---|---|
| FACT | 文件或代码中明确写出 | 可以，需引用路径 |
| VERIFIED | 已通过命令、测试、服务/API 场景验证 | 可以，需记录命令 |
| INFERENCE | 基于多个事实的推理 | 谨慎进入，需标注推理链 |
| GAP | 缺失、冲突、不可运行或未验证 | 不作为完成事实 |
| RISK | 可能误导未来 AI 或影响交付 | 可进入风险清单 |

禁止把 `INFERENCE` 写成 `FACT`，禁止把 `GAP` 写成“未来已规划完成”。

## 3. 分批深读路线

### Batch 0：启动与边界

目标：确认母包使命、模型原生边界、母包/用户包边界。

必读：

- `MISSION-MEMORY.md`
- `MOTHER-PACK-ACTIVATION-GUIDE.md`
- `AI_PROJECT_CONTEXT.md`
- `00.超级提示词工程/11-模型原生协作协议/MODEL-NATIVE-COLLABORATION-PROTOCOL.md`
- `00.超级提示词工程/12-引导秘书逻辑/MISSION-MEMORY-AWAKENING-PROTOCOL.md`

产物：

- `awakening_check`
- 母包/用户包边界判断
- 停止线清单

### Batch 1：控制平面

目标：理解 00 如何把自然语言变成可追踪任务。

必读：

- `00.超级提示词工程/README.md`
- `00.超级提示词工程/01-总控提示词/MASTER-ORCHESTRATOR-PROMPT.md`
- `00.超级提示词工程/02-路由矩阵/SUBSYSTEM-ROUTING-MATRIX.md`
- `00.超级提示词工程/03-上下文包模板/AI-CONTEXT-PACK-TEMPLATE.md`
- `00.超级提示词工程/06-原子化开发治理/ATOMIC-AI-DEVELOPMENT-OPERATING-SYSTEM.md`
- `00.超级提示词工程/12-引导秘书逻辑/GUIDE-SECRETARY-PROTOCOL.md`
- `00.超级提示词工程/14-全链路审计与运行对齐/*.yaml`

产物：

- `guide_secretary_packet`
- `route_feedback`
- `USO` 状态对象草案
- 验证计划

### Batch 2：能力源子系统

目标：逐个理解子系统“能做什么、靠什么证明、边界在哪里”。

顺序：

1. `01.通讯协议_幽灵通道`：通信、同步、SDK、企业部署。
2. `03.数据库管理_文件夹整理AI应用`：知识库、文件治理、MemoryOS、MCP、检索。
3. `04.QCM-MVP-Emergence`：公式、角色协同、沙盘、飞轮、质量评审。
4. `05.超极智脑_Q-SpecTrum`：角色路由、Web/API、主运行平台、BRAIN-KB、平台 DB。
5. `02.通用知识库框架_Universal-KB`：轻量模板，不与 03 混淆。
6. `协同通用AI大模型开发交付包`：最终用户交付四体系。

每个子系统必须形成：

```yaml
subsystem_crystal:
  id: "<Pxx>"
  purpose: ""
  authority_files: []
  runtime_entrypoints: []
  data_sources: []
  commands_verified: []
  upstream: []
  downstream: []
  user_value: ""
  ai_collaboration_role: ""
  risks: []
  stop_lines: []
```

### Batch 3：跨系统齿轮咬合

目标：验证“不是每个文件夹单独能跑，而是任务能串起来”。

必须模拟的黄金路径：

1. 新 AI 进入母包，完成唤醒。
2. 用户自然语言进入 `qa_runner.py route`，生成秘书 YAML。
3. 知识/记忆任务进入 03，能检索和提供 MCP 工具层。
4. 复杂方案进入 04，能形成 QCM 角色评审和风险假设。
5. 执行/平台任务进入 05，CLI/API 能返回角色路由和响应。
6. 交付任务进入用户包，`VERIFY-DELIVERY.ps1 -Strict` 通过。

### Batch 4：对抗审计

目标：专门找 AI 容易说谎、幻觉、误判完成的地方。

审计项：

- 文档说通过但命令失败。
- 旧报告说失败但当前已修。
- smoke 被误当 release gate。
- 子模块 dirty 状态被忽略。
- 运行态 `_HANDOFF`、DB、cache 被误当源代码必需文件。
- 母包提示词被误认为高于模型系统规则。
- 用户包被误当母包镜像。

### Batch 5：交付闭环

目标：让外部 AI 或开发者不靠口头解释也能复现。

必须产物：

- Runbook：从 fresh checkout 到验证通过。
- Scenario Acceptance Matrix：黄金路径验收矩阵。
- Knowledge Graph Seed：项目/能力/数据源/验证/交付对象关系图。
- Crystallization Log：每批深读的事实、推论、缺口、风险。
- Stop-Rebuild Gate：什么时候该停止重构。

## 4. 知识图谱对象模型

后续知识图谱至少包含这些节点类型：

| 节点 | 说明 |
|---|---|
| `Project` | ROOT、00、01、02、03、04、05、USER_PACK |
| `Capability` | 能力注册表中的 CAP-* |
| `Artifact` | 关键文档、脚本、DB、测试、模板 |
| `RuntimeEntry` | CLI、API、MCP、Flask、PowerShell 验证入口 |
| `DataSource` | 真实记忆、索引、DB、BRAIN-KB、Handoff |
| `Validation` | VAL-*、pytest、PowerShell、service smoke |
| `Role` | 秘书、架构、知识、验证、交付、怀疑者等任务态角色 |
| `Risk` | 旧文档、假阳性、编码、路径、子模块、交付边界 |
| `DeliveryObject` | 用户包四体系与最终验收物 |

关键边类型：

| 边 | 说明 |
|---|---|
| `routes_to` | 用户意图或秘书输出路由到子系统 |
| `owns` | 项目拥有能力/文件/数据源 |
| `validates` | 验证项证明某能力或入口 |
| `reads_from` | 子系统或角色读取的权威记忆源 |
| `writes_to` | 可写入的长期记忆或交付产物 |
| `depends_on` | 能力依赖另一个子系统 |
| `must_not_confuse_with` | 防止副本、模板、历史报告混淆 |
| `delivers_to` | 母包产物如何进入用户交付包 |

## 5. 知识结晶格式

每个结晶单元必须短、硬、有证据：

```yaml
knowledge_crystal:
  id: "KC-YYYYMMDD-XXX"
  title: ""
  scope: "ROOT|P00|P01|P02|P03|P04|P05|USER_PACK|CROSS"
  evidence_level: "FACT|VERIFIED|INFERENCE|GAP|RISK"
  source_refs: []
  commands: []
  statement: ""
  implication: ""
  next_action: ""
  memory_target: "none|MISSION-MEMORY|AI_PROJECT_CONTEXT|BRAIN-KB|USO_LEDGER|USER_PACK"
```

结晶不是摘要。结晶必须回答：

1. 这个事实对未来 AI 行动有什么影响？
2. 它是否改变路由、验证、记忆或交付？
3. 如果错误，会造成什么误导？

## 6. 长期记忆写入门

只有满足以下条件之一，才允许写入长期记忆：

- 会改变未来启动顺序。
- 会改变子系统权威边界。
- 会改变验证命令或验收门。
- 会改变用户交付包边界。
- 是已复现的失败案例或修复模式。

禁止写入：

- 单次聊天感受。
- 未验证愿景。
- 角色沙盘中未经验证的意见。
- 旧报告中的过时状态。

## 7. 角色团队

任务态角色只在需要时启用，输出必须合并为一个决策。

| 角色 | 职责 | 禁止 |
|---|---|---|
| Guide Secretary | 意图识别、路由、交接包 | 直接执行复杂任务 |
| Chief Architect | 边界、依赖、系统图 | 无证据重构 |
| Knowledge Curator | 图谱、结晶、记忆源 | 把聊天当记忆 |
| Runtime Engineer | CLI/API/MCP/服务 smoke | 只看文件不运行 |
| Verification Auditor | 假阳性、回归、验收门 | 把 smoke 当 release |
| QCM Facilitator | 多角色沙盘、冲突推理 | 用沙盘替代验证 |
| Delivery Architect | 用户包四体系与交付门 | 把母包镜像给用户 |
| Skeptic | 反幻觉、停止线、证据追问 | 无限否定不收敛 |

## 8. 停止重构门

当以下条件满足时，应停止扩写或重构，转入交付/维护：

1. 当前任务有明确 `GOAL/REQ/TASK/TEST`。
2. 目标子系统入口已跑通。
3. 跨系统影响已记录。
4. `qa_runner.py validate` 无失败。
5. `qa_runner.py consistency` 无失败。
6. 用户包 strict 门对交付目标通过。
7. 剩余问题都登记为 `RISK/GAP`，并有 owner 与下一步。

如果没有新的失败证据，不应为了“更完整”继续重构。

## 9. 下一阶段执行顺序

1. 建立 `KNOWLEDGE-GRAPH-SEED.yaml`：把现有 PROJECT/CAPABILITY/ARTIFACT/VALIDATION/MEMORY 注册表串成图。
2. 建立 `SCENARIO-ACCEPTANCE-MATRIX.md`：固化六条黄金路径。
3. 按 Batch 2 深读每个子系统，逐批生成 `subsystem_crystal`。
4. 对每批深读运行对应命令，不用“文档看起来完整”代替验证。
5. 把稳定结论写回 `AI_PROJECT_CONTEXT.md` 或 `BRAIN-KB`，不稳定结论进入问题日志。

## 10. 最终判断

母包的高标准不是“文件很多、角色很多、提示词很完整”，而是：

```text
未来任意通用 AI 进入后，
知道自己不是被替代，
知道该读什么，
知道该问什么，
知道该调用哪个子系统，
知道如何证明完成，
知道什么时候停止。
```

